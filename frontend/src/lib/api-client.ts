/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - API CLIENT & NETWORK RESILIENCY:
 * MODULE:    Next.js 15+ Centralized Type-Safe API Client & Resilient Offline Interceptor
 * TOPIC:     Idempotency Headers (UUID v4), Global 401/403/429 Interceptors, Offline Queue
 * FILE:      frontend/src/lib/api-client.ts
 * PURPOSE:   Provides unified, strongly-typed asynchronous HTTP client between the Next.js
 *            frontend and FastAPI backend. Automatically attaches UUID v4 X-Idempotency-Key
 *            headers for mutating operations, injects Bearer auth tokens, intercepts 401/403/429
 *            errors, buffers answers offline for flaky rural 3G connections, and auto-replays on reconnect.
 * AUDIENCE:  Frontend Page Developers, Zustand State Stores & Network Auditors
 * STANDARDS: ASVS L2 Idempotency, W3C Fetch API, WCAG 2.2 AA Contrast, Zero-Emoji Architecture
 * ========================================================================================
 */

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// -----------------------------------------------------------------------------
// UUID v4 Generator for Idempotency
// -----------------------------------------------------------------------------
export function generateUUID(): string {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

// -----------------------------------------------------------------------------
// Offline Queue Buffer for Flaky Rural Connections (NCTB 2G/3G Edge)
// -----------------------------------------------------------------------------
export interface OfflineAnswerItem {
  attemptId: string;
  questionId: string;
  payload: {
    selected_option_id: string;
    time_taken_seconds: number;
  };
  idempotencyKey: string;
  timestamp: number;
}

const OFFLINE_QUEUE_KEY = 'ogrojatra_offline_answer_queue';

export function getOfflineQueue(): OfflineAnswerItem[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = localStorage.getItem(OFFLINE_QUEUE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function saveOfflineQueue(queue: OfflineAnswerItem[]): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(OFFLINE_QUEUE_KEY, JSON.stringify(queue));
  } catch (err) {
    console.error('Failed to write offline queue:', err);
  }
}

// -----------------------------------------------------------------------------
// Custom Structured API Error
// -----------------------------------------------------------------------------
export class ApiError extends Error {
  public status: number;
  public data: any;
  public retryAfterSeconds?: number;

  constructor(message: string, status: number, data?: any, retryAfterSeconds?: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
    this.retryAfterSeconds = retryAfterSeconds;
  }
}

// -----------------------------------------------------------------------------
// Core API Client Class
// -----------------------------------------------------------------------------
export class ApiClient {
  private token: string | null = null;
  private onUnauthorizedCallback?: () => void;
  private onRateLimitCallback?: (retryAfter: number) => void;

  constructor() {
    if (typeof window !== 'undefined') {
      try {
        this.token = localStorage.getItem('auth_token');
      } catch {
        this.token = null;
      }

      // Setup online auto-replay event listener
      window.addEventListener('online', () => {
        this.replayPendingAnswers();
      });
    }
  }

  public setToken(token: string | null): void {
    this.token = token;
    if (typeof window !== 'undefined') {
      try {
        if (token) {
          localStorage.setItem('auth_token', token);
        } else {
          localStorage.removeItem('auth_token');
        }
      } catch (e) {
        console.error('Failed to sync auth token in localStorage:', e);
      }
    }
  }

  public getToken(): string | null {
    if (!this.token && typeof window !== 'undefined') {
      try {
        this.token = localStorage.getItem('auth_token');
      } catch {
        this.token = null;
      }
    }
    return this.token;
  }

  public setOnUnauthorized(cb: () => void): void {
    this.onUnauthorizedCallback = cb;
  }

  public setOnRateLimit(cb: (retryAfter: number) => void): void {
    this.onRateLimitCallback = cb;
  }

  // ---------------------------------------------------------------------------
  // Generic Request Handler with Interceptors
  // ---------------------------------------------------------------------------
  public async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
    const method = (options.method || 'GET').toUpperCase();

    // Headers assembly
    const headers = new Headers(options.headers || {});
    if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
      headers.set('Content-Type', 'application/json');
    }
    headers.set('Accept', 'application/json');

    // Automatic Bearer token injection
    const activeToken = this.getToken();
    if (activeToken && !headers.has('Authorization')) {
      headers.set('Authorization', `Bearer ${activeToken}`);
    }

    // Automatic X-Idempotency-Key header for state-mutating requests
    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method) && !headers.has('X-Idempotency-Key')) {
      headers.set('X-Idempotency-Key', generateUUID());
    }

    const config: RequestInit = {
      ...options,
      headers,
      credentials: options.credentials || 'include',
    };

    try {
      const response = await fetch(url, config);

      // Global Interceptor: 401 Unauthorized
      if (response.status === 401) {
        this.setToken(null);
        if (this.onUnauthorizedCallback) {
          this.onUnauthorizedCallback();
        }
        throw new ApiError('Session expired or unauthorized. Please re-authenticate.', 401);
      }

      // Global Interceptor: 403 Forbidden
      if (response.status === 403) {
        let errData = {};
        try { errData = await response.json(); } catch {}
        throw new ApiError('Access forbidden. You lack permissions for this resource.', 403, errData);
      }

      // Global Interceptor: 429 Too Many Requests
      if (response.status === 429) {
        const retryHeader = response.headers.get('Retry-After');
        const retryAfterSeconds = retryHeader ? parseInt(retryHeader, 10) : 30;
        if (this.onRateLimitCallback) {
          this.onRateLimitCallback(retryAfterSeconds);
        }
        throw new ApiError(`Rate limit exceeded. Please wait ${retryAfterSeconds} seconds.`, 429, null, retryAfterSeconds);
      }

      // Handle other non-2xx errors
      if (!response.ok) {
        let errorData = null;
        try {
          errorData = await response.json();
        } catch {
          errorData = await response.text();
        }
        const message = (errorData && typeof errorData === 'object' && errorData.detail)
          ? errorData.detail
          : `HTTP error ${response.status}: ${response.statusText}`;
        throw new ApiError(message, response.status, errorData);
      }

      // Handle 204 No Content
      if (response.status === 204) {
        return {} as T;
      }

      return (await response.json()) as T;
    } catch (error: any) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError(
        error.message || 'Network connection failed. Operating in offline mode.',
        0,
        error
      );
    }
  }

  // ---------------------------------------------------------------------------
  // Ergonomic HTTP Shorthands
  // ---------------------------------------------------------------------------
  public get<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  public post<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  public put<T>(endpoint: string, data?: any, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  public delete<T>(endpoint: string, options?: RequestInit): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }

  // ---------------------------------------------------------------------------
  // Specialized Domain Endpoint Methods
  // ---------------------------------------------------------------------------

  /**
   * Practice & Quiz Endpoints (Phase 77 practice.tsx)
   */
  public async getPracticeSets(subject?: string, level?: string): Promise<any> {
    const params = new URLSearchParams();
    if (subject) params.set('subject', subject);
    if (level) params.set('level', level);
    const qs = params.toString() ? `?${params.toString()}` : '';
    return this.get(`/practice/sets${qs}`);
  }

  public async startQuizAttempt(setId: string): Promise<any> {
    return this.post(`/quiz-attempts/start`, { set_id: setId });
  }

  public async submitAnswer(
    attemptId: string,
    questionId: string,
    payload: { selected_option_id: string; time_taken_seconds: number }
  ): Promise<any> {
    const idempotencyKey = generateUUID();

    // Attempt direct submission
    try {
      return await this.post(`/quiz-attempts/${attemptId}/answers`, payload, {
        headers: { 'X-Idempotency-Key': idempotencyKey },
      });
    } catch (err: any) {
      // If network fails (status 0), buffer answer in local queue
      if (err.status === 0 || (typeof navigator !== 'undefined' && !navigator.onLine)) {
        const queue = getOfflineQueue();
        queue.push({
          attemptId,
          questionId,
          payload,
          idempotencyKey,
          timestamp: Date.now(),
        });
        saveOfflineQueue(queue);
        return {
          success: true,
          offline_buffered: true,
          message: 'Saved to offline local buffer. Will sync upon network reconnection.',
        };
      }
      throw err;
    }
  }

  public async completeQuizAttempt(attemptId: string): Promise<any> {
    return this.post(`/quiz-attempts/${attemptId}/complete`);
  }

  /**
   * Live Challenges Endpoints (Phase 77 live-challenge.tsx)
   */
  public async getLiveChallenges(): Promise<any> {
    return this.get(`/live-challenges/active`);
  }

  public async getLiveLeaderboard(challengeId: string): Promise<any> {
    return this.get(`/live-challenges/${challengeId}/leaderboard`);
  }

  /**
   * Admission Hub Endpoints (Phase 77 admission.tsx)
   */
  public async getAdmissionTests(unit?: string): Promise<any> {
    const qs = unit ? `?unit=${encodeURIComponent(unit)}` : '';
    return this.get(`/admission/blueprints${qs}`);
  }

  public async getAdmissionPrograms(unit?: string): Promise<any> {
    return this.getAdmissionTests(unit);
  }

  /**
   * Tuition Marketplace Endpoints (Phase 77 tuition.tsx)
   */
  public async getTuitions(filter?: { city?: string; subject?: string }): Promise<any> {
    const params = new URLSearchParams();
    if (filter?.city) params.set('city', filter.city);
    if (filter?.subject) params.set('subject', filter.subject);
    const qs = params.toString() ? `?${params.toString()}` : '';
    return this.get(`/tuitions/feed${qs}`);
  }

  public async getTuitionListings(filter?: { city?: string; subject?: string }): Promise<any> {
    return this.getTuitions(filter);
  }

  public async requestTuitionConsent(tuitionId: string, guardianId?: string): Promise<any> {
    return this.post(`/tuitions/${tuitionId}/consent-request`, { guardian_id: guardianId });
  }

  public async requestContactConsent(tuitionId: string): Promise<any> {
    return this.requestTuitionConsent(tuitionId);
  }

  /**
   * Career & Bdjobs Endpoints (Phase 77 career.tsx)
   */
  public async getCareerProfile(): Promise<any> {
    return this.get(`/career/profile`);
  }

  public async getSkillsPortfolio(): Promise<any> {
    return this.get(`/career/skills`);
  }

  public async getJobApplications(): Promise<any> {
    return this.get(`/career/applications`);
  }

  public async applyForJob(jobId: string, cvSnapshotId: string): Promise<any> {
    return this.post(`/career/jobs/${jobId}/apply`, { cv_snapshot_id: cvSnapshotId });
  }

  // ---------------------------------------------------------------------------
  // Resilient Offline Replay Engine
  // ---------------------------------------------------------------------------
  public async replayPendingAnswers(): Promise<number> {
    const queue = getOfflineQueue();
    if (queue.length === 0) return 0;

    let successfulReplays = 0;
    const remainingQueue: OfflineAnswerItem[] = [];

    for (const item of queue) {
      try {
        await this.post(
          `/quiz-attempts/${item.attemptId}/answers`,
          item.payload,
          { headers: { 'X-Idempotency-Key': item.idempotencyKey } }
        );
        successfulReplays++;
      } catch (err: any) {
        // If still network offline or server error, retain in queue
        if (err.status === 0 || err.status >= 500) {
          remainingQueue.push(item);
        }
      }
    }

    saveOfflineQueue(remainingQueue);
    return successfulReplays;
  }
}

// Singleton export
export const apiClient = new ApiClient();
