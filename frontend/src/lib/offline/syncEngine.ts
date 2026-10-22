/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - OFFLINE-FIRST CRDT SYNC ENGINE:
 * MODULE:    Client-Side Background Sync & Conflict Resolution Engine
 * TOPIC:     Last-Write-Wins (LWW), Vector Clocks & Auto-Reconnection Replay
 * FILE:      frontend/src/lib/offline/syncEngine.ts
 * PURPOSE:   Coordinates background synchronization between client-side IndexedDB and
 *            the backend FastAPI `/api/v1/quiz-attempts/sync` endpoint:
 *            1. Network State Monitoring: Detects online/offline browser state changes
 *               and responds to Service Worker background sync triggers.
 *            2. Conflict Resolution: Implements deterministic Last-Write-Wins (LWW)
 *               reconciliation leveraging high-precision client timestamps and vector clocks.
 *            3. Batch Flusher: Idempotently replays buffered answer mutations with
 *               UUID v4 deduplication tokens upon reconnect.
 *            4. Reactive Status Telemetry: Publishes real-time sync states (online,
 *               offline, syncing, pending count) to UI indicators.
 * AUDIENCE:  Offline Sync Engineers, Frontend Architects & Full-Stack Developers
 * STANDARDS: CRDT State Reconciliation, PWA Background Sync API, Strict Zero-Emoji
 * ========================================================================================
 */

import {
  getPendingOfflineAnswers,
  markAnswersAsSynced,
  clearSyncedAnswers,
  OfflineAnswerRecord
} from './indexedDbStorage';

export interface SyncStatus {
  isOnline: boolean;
  isSyncing: boolean;
  pendingCount: number;
  lastSyncedAt: number | null;
  lastError: string | null;
}

export type SyncStatusListener = (status: SyncStatus) => void;

class OfflineSyncEngine {
  private isOnline: boolean = typeof navigator !== 'undefined' ? navigator.onLine : true;
  private isSyncing: boolean = false;
  private pendingCount: number = 0;
  private lastSyncedAt: number | null = null;
  private lastError: string | null = null;
  private listeners: Set<SyncStatusListener> = new Set();
  private autoSyncInterval: any = null;

  constructor() {
    this.initNetworkListeners();
    this.refreshPendingCount();
  }

  /**
   * Binds browser online/offline events and Service Worker message handlers.
   */
  private initNetworkListeners(): void {
    if (typeof window === 'undefined') return;

    window.addEventListener('online', () => {
      this.isOnline = true;
      this.lastError = null;
      this.notifyListeners();
      this.flushPendingAnswers();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      this.notifyListeners();
    });

    // Listen to Service Worker postMessage sync triggers
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'TRIGGER_OFFLINE_SYNC') {
          this.flushPendingAnswers();
        }
      });
    }

    // Periodic check every 60 seconds when online to clear backlogs
    this.autoSyncInterval = setInterval(() => {
      if (this.isOnline && !this.isSyncing) {
        this.flushPendingAnswers();
      }
    }, 60000);
  }

  /**
   * Refreshes the count of pending offline records from IndexedDB.
   */
  public async refreshPendingCount(): Promise<number> {
    try {
      const pending = await getPendingOfflineAnswers();
      this.pendingCount = pending.length;
      this.notifyListeners();
      return this.pendingCount;
    } catch {
      return 0;
    }
  }

  /**
   * Resolves conflicts between two answer submissions for the same question.
   * Deterministic Last-Write-Wins (LWW) based on client timestamp and vector clock counters.
   */
  public resolveConflict(local: OfflineAnswerRecord, incoming: OfflineAnswerRecord): OfflineAnswerRecord {
    // 1. Vector Clock Comparison if present
    const localClockSum = Object.values(local.vector_clock || {}).reduce((a, b) => a + b, 0);
    const incomingClockSum = Object.values(incoming.vector_clock || {}).reduce((a, b) => a + b, 0);

    if (localClockSum !== incomingClockSum) {
      return localClockSum > incomingClockSum ? local : incoming;
    }

    // 2. Fallback to LWW via client timestamp
    return local.client_timestamp >= incoming.client_timestamp ? local : incoming;
  }

  /**
   * Flushes all pending answers to the backend sync endpoint.
   */
  public async flushPendingAnswers(): Promise<{ synced: number; failed: number }> {
    if (!this.isOnline || this.isSyncing) {
      return { synced: 0, failed: 0 };
    }

    const pending = await getPendingOfflineAnswers();
    if (pending.length === 0) {
      this.pendingCount = 0;
      this.notifyListeners();
      return { synced: 0, failed: 0 };
    }

    this.isSyncing = true;
    this.notifyListeners();

    // Group pending answers by attempt_id
    const groupedByAttempt = new Map<string, OfflineAnswerRecord[]>();
    for (const record of pending) {
      const list = groupedByAttempt.get(record.attempt_id) || [];
      list.push(record);
      groupedByAttempt.set(record.attempt_id, list);
    }

    let totalSynced = 0;
    let totalFailed = 0;
    const syncedIds: string[] = [];

    for (const [attemptId, answers] of groupedByAttempt.entries()) {
      const studentId = answers[0]?.student_id || 'anonymous_student';

      // Deduplicate multiple answers to the same question using LWW
      const deduplicatedMap = new Map<string, OfflineAnswerRecord>();
      for (const ans of answers) {
        const existing = deduplicatedMap.get(ans.question_version_id);
        if (!existing) {
          deduplicatedMap.set(ans.question_version_id, ans);
        } else {
          deduplicatedMap.set(ans.question_version_id, this.resolveConflict(existing, ans));
        }
      }

      const deduplicatedAnswers = Array.from(deduplicatedMap.values());

      const payload = {
        student_id: studentId,
        attempt_id: attemptId,
        buffered_answers: deduplicatedAnswers.map((a) => ({
          question_version_id: a.question_version_id,
          selected_option_id: a.selected_option_id,
          idempotency_key: a.idempotency_key,
          time_taken_seconds: a.time_taken_seconds,
          client_timestamp: a.client_timestamp
        }))
      };

      try {
        const response = await fetch('/api/v1/quiz-attempts/sync', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Idempotency-Key': `sync_${attemptId}_${Date.now()}`
          },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          answers.forEach((a) => syncedIds.push(a.id));
          totalSynced += answers.length;
        } else {
          totalFailed += answers.length;
          this.lastError = `Server returned status ${response.status} during offline sync`;
        }
      } catch (err: any) {
        totalFailed += answers.length;
        this.lastError = err?.message || 'Network error during sync flush';
      }
    }

    if (syncedIds.length > 0) {
      await markAnswersAsSynced(syncedIds);
      await clearSyncedAnswers();
      this.lastSyncedAt = Date.now();

      // Dispatch custom DOM event for UI components
      if (typeof window !== 'undefined') {
        window.dispatchEvent(
          new CustomEvent('offline-sync-completed', {
            detail: { syncedCount: syncedIds.length }
          })
        );
      }
    }

    await this.refreshPendingCount();
    this.isSyncing = false;
    this.notifyListeners();

    return { synced: totalSynced, failed: totalFailed };
  }

  /**
   * Subscribes a UI component to sync status updates.
   */
  public subscribe(listener: SyncStatusListener): () => void {
    this.listeners.add(listener);
    listener(this.getStatus());

    return () => {
      this.listeners.delete(listener);
    };
  }

  /**
   * Returns current sync telemetry.
   */
  public getStatus(): SyncStatus {
    return {
      isOnline: this.isOnline,
      isSyncing: this.isSyncing,
      pendingCount: this.pendingCount,
      lastSyncedAt: this.lastSyncedAt,
      lastError: this.lastError
    };
  }

  private notifyListeners(): void {
    const status = this.getStatus();
    this.listeners.forEach((fn) => fn(status));
  }
}

// Global Sync Engine Singleton
export const syncEngine = new OfflineSyncEngine();
