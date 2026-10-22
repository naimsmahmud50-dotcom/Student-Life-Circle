/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CLIENT-SIDE INDEXEDDB STORAGE:
 * MODULE:    Offline IndexedDB Storage Engine & Practice Cache
 * TOPIC:     Local Database Stores for Practice Bundles, Offline Answers & Profile Cache
 * FILE:      frontend/src/lib/offline/indexedDbStorage.ts
 * PURPOSE:   Provides persistent client-side storage for offline-first learning:
 *            1. `practice_sets`: Stores complete offline question bundles downloaded
 *               for disconnected practice in rural Char/haor regions.
 *            2. `answers_queue`: Buffers student answer submissions with client-side
 *               timestamps, UUID v4 idempotency keys, and CRDT vector clocks.
 *            3. `profiles_cache`: Caches learner profile details for zero-latency offline UI.
 *            Includes an automatic in-memory fallback for SSR hydration and Node environments.
 * AUDIENCE:  Frontend Architects, Offline-First Specialists & Full-Stack Engineers
 * STANDARDS: W3C IndexedDB 3.0, ASVS L2 Client Resilience, Strict Zero-Emoji
 * ========================================================================================
 */

export interface OfflinePracticeQuestion {
  question_id: string;
  stem_bn: string;
  options: Array<{
    option_id: string;
    option_key: string;
    text_bn: string;
  }>;
  explanation_bn?: string;
  cognitive_skill?: string;
}

export interface OfflinePracticeBundle {
  bundle_id: string;
  class_grade: number;
  subject: string;
  generated_at: string;
  total_items: number;
  offline_version: string;
  questions: OfflinePracticeQuestion[];
  downloaded_at?: number;
}

export interface OfflineAnswerRecord {
  id: string; // Composite key: ${attempt_id}_${question_version_id}
  attempt_id: string;
  student_id: string;
  question_version_id: string;
  selected_option_id: string | null;
  idempotency_key: string;
  time_taken_seconds: number;
  client_timestamp: number; // Unix timestamp in milliseconds
  vector_clock?: Record<string, number>;
  synced: boolean;
  retry_count: number;
}

const DB_NAME = 'SLC_Offline_DB';
const DB_VERSION = 1;

const STORE_PRACTICE = 'practice_sets';
const STORE_ANSWERS = 'answers_queue';
const STORE_PROFILES = 'profiles_cache';

// In-Memory Fallback Store for SSR and environments lacking IndexedDB
class MemoryStorageFallback {
  practiceSets: Map<string, OfflinePracticeBundle> = new Map();
  answersQueue: Map<string, OfflineAnswerRecord> = new Map();
  profilesCache: Map<string, any> = new Map();
}

const memoryFallback = new MemoryStorageFallback();

const isIndexedDbAvailable = (): boolean => {
  return typeof window !== 'undefined' && typeof window.indexedDB !== 'undefined';
};

/**
 * Initializes and upgrades the IndexedDB database schema.
 */
export const openDatabase = (): Promise<IDBDatabase | null> => {
  if (!isIndexedDbAvailable()) {
    return Promise.resolve(null);
  }

  return new Promise((resolve, reject) => {
    const request = window.indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;

      // 1. Practice Bundles Store
      if (!db.objectStoreNames.contains(STORE_PRACTICE)) {
        const practiceStore = db.createObjectStore(STORE_PRACTICE, { keyPath: 'bundle_id' });
        practiceStore.createIndex('subject', 'subject', { unique: false });
        practiceStore.createIndex('class_grade', 'class_grade', { unique: false });
      }

      // 2. Answers Mutation Queue Store
      if (!db.objectStoreNames.contains(STORE_ANSWERS)) {
        const answersStore = db.createObjectStore(STORE_ANSWERS, { keyPath: 'id' });
        answersStore.createIndex('attempt_id', 'attempt_id', { unique: false });
        answersStore.createIndex('synced', 'synced', { unique: false });
        answersStore.createIndex('client_timestamp', 'client_timestamp', { unique: false });
      }

      // 3. User Profiles Cache Store
      if (!db.objectStoreNames.contains(STORE_PROFILES)) {
        db.createObjectStore(STORE_PROFILES, { keyPath: 'user_id' });
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
};

/**
 * Saves a downloaded offline practice bundle to local storage.
 */
export const saveOfflinePracticeSet = async (bundle: OfflinePracticeBundle): Promise<void> => {
  const enrichedBundle = {
    ...bundle,
    downloaded_at: bundle.downloaded_at || Date.now()
  };

  const db = await openDatabase();
  if (!db) {
    memoryFallback.practiceSets.set(bundle.bundle_id, enrichedBundle);
    return;
  }

  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_PRACTICE], 'readwrite');
    const store = transaction.objectStore(STORE_PRACTICE);
    const request = store.put(enrichedBundle);

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
};

/**
 * Retrieves a cached offline practice bundle by ID.
 */
export const getOfflinePracticeSet = async (bundleId: string): Promise<OfflinePracticeBundle | null> => {
  const db = await openDatabase();
  if (!db) {
    return memoryFallback.practiceSets.get(bundleId) || null;
  }

  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_PRACTICE], 'readonly');
    const store = transaction.objectStore(STORE_PRACTICE);
    const request = store.get(bundleId);

    request.onsuccess = () => resolve(request.result || null);
    request.onerror = () => reject(request.error);
  });
};

/**
 * Lists all available offline practice sets currently stored on the device.
 */
export const listOfflinePracticeSets = async (): Promise<OfflinePracticeBundle[]> => {
  const db = await openDatabase();
  if (!db) {
    return Array.from(memoryFallback.practiceSets.values());
  }

  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_PRACTICE], 'readonly');
    const store = transaction.objectStore(STORE_PRACTICE);
    const request = store.getAll();

    request.onsuccess = () => resolve(request.result || []);
    request.onerror = () => reject(request.error);
  });
};

/**
 * Enqueues an offline student answer with client timestamp and idempotency token.
 */
export const enqueueOfflineAnswer = async (answer: OfflineAnswerRecord): Promise<void> => {
  const recordId = answer.id || `${answer.attempt_id}_${answer.question_version_id}`;
  const record: OfflineAnswerRecord = {
    ...answer,
    id: recordId,
    client_timestamp: answer.client_timestamp || Date.now(),
    synced: false,
    retry_count: answer.retry_count || 0
  };

  const db = await openDatabase();
  if (!db) {
    memoryFallback.answersQueue.set(recordId, record);
    return;
  }

  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_ANSWERS], 'readwrite');
    const store = transaction.objectStore(STORE_ANSWERS);
    const request = store.put(record);

    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
};

/**
 * Retrieves pending (unsynced) offline answers awaiting background flush.
 */
export const getPendingOfflineAnswers = async (attemptId?: string): Promise<OfflineAnswerRecord[]> => {
  const db = await openDatabase();
  if (!db) {
    const all = Array.from(memoryFallback.answersQueue.values()).filter((a) => !a.synced);
    return attemptId ? all.filter((a) => a.attempt_id === attemptId) : all;
  }

  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_ANSWERS], 'readonly');
    const store = transaction.objectStore(STORE_ANSWERS);
    const request = store.getAll();

    request.onsuccess = () => {
      const records: OfflineAnswerRecord[] = request.result || [];
      const pending = records.filter((r) => !r.synced);
      if (attemptId) {
        resolve(pending.filter((r) => r.attempt_id === attemptId));
      } else {
        resolve(pending);
      }
    };
    request.onerror = () => reject(request.error);
  });
};

/**
 * Marks a batch of answer record IDs as successfully synchronized with the backend.
 */
export const markAnswersAsSynced = async (ids: string[]): Promise<void> => {
  if (ids.length === 0) return;

  const db = await openDatabase();
  if (!db) {
    ids.forEach((id) => {
      const rec = memoryFallback.answersQueue.get(id);
      if (rec) rec.synced = true;
    });
    return;
  }

  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_ANSWERS], 'readwrite');
    const store = transaction.objectStore(STORE_ANSWERS);

    let completed = 0;
    ids.forEach((id) => {
      const getReq = store.get(id);
      getReq.onsuccess = () => {
        const record = getReq.result;
        if (record) {
          record.synced = true;
          store.put(record);
        }
        completed++;
        if (completed === ids.length) {
          resolve();
        }
      };
      getReq.onerror = () => reject(getReq.error);
    });
  });
};

/**
 * Clears all already-synced answer records to maintain compact storage.
 */
export const clearSyncedAnswers = async (): Promise<void> => {
  const db = await openDatabase();
  if (!db) {
    for (const [id, rec] of memoryFallback.answersQueue.entries()) {
      if (rec.synced) {
        memoryFallback.answersQueue.delete(id);
      }
    }
    return;
  }

  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_ANSWERS], 'readwrite');
    const store = transaction.objectStore(STORE_ANSWERS);
    const request = store.getAll();

    request.onsuccess = () => {
      const records: OfflineAnswerRecord[] = request.result || [];
      records.forEach((r) => {
        if (r.synced) {
          store.delete(r.id);
        }
      });
      resolve();
    };
    request.onerror = () => reject(request.error);
  });
};

/**
 * Caches student profile details for instant offline display.
 */
export const cacheUserProfile = async (profile: any): Promise<void> => {
  if (!profile || !profile.user_id) return;
  const enriched = { ...profile, cached_at: Date.now() };

  const db = await openDatabase();
  if (!db) {
    memoryFallback.profilesCache.set(profile.user_id, enriched);
    return;
  }

  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_PROFILES], 'readwrite');
    const store = transaction.objectStore(STORE_PROFILES);
    const request = store.put(enriched);
    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
};

/**
 * Retrieves cached student profile details.
 */
export const getCachedUserProfile = async (userId: string): Promise<any | null> => {
  const db = await openDatabase();
  if (!db) {
    return memoryFallback.profilesCache.get(userId) || null;
  }

  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_PROFILES], 'readonly');
    const store = transaction.objectStore(STORE_PROFILES);
    const request = store.get(userId);
    request.onsuccess = () => resolve(request.result || null);
    request.onerror = () => reject(request.error);
  });
};
