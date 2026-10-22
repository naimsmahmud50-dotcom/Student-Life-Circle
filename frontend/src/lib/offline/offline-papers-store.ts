/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    PWA, Offline Experience & Mobile Optimization
 * TOPIC:     Phase 139 Service Worker, IndexedDB Past Paper Vault & Sub-1s Mobile Engine
 * FILE:      frontend/src/lib/offline/offline-papers-store.ts
 * PHASE:     Phase 139 - PWA, Offline Experience & Mobile Optimization
 * PURPOSE:   Provides persistent client-side IndexedDB storage for offline NCTB board
 *            question papers, offline reading lists, and background sync queues.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Workbox-Grade SW, idb Offline Vault, WCAG 2.2 AAA
 */

import { BoardQuestionItem } from '@/components/curriculum/BoardQuestionArchiveViewer';
import rawSeedBoardQuestions from '@/data/nctb_board_past_papers_2015_2025.json';

export interface OfflineReadingRecord {
  paper_id: string;
  saved_at: number;
  last_read_at: number;
  notes_bn?: string;
  progress_percent: number;
}

export interface OfflineSyncQueueItem {
  id: string;
  action: 'SUBMIT_PRACTICE_ATTEMPT' | 'SYNC_READ_STATUS';
  payload: Record<string, any>;
  created_at: number;
  retry_count: number;
  synced: boolean;
}

export interface OfflineVaultStats {
  totalPapers: number;
  subjects: string[];
  boards: string[];
  lastSyncTime: number;
}

const DB_NAME = 'SLC_Board_Papers_Vault';
const DB_VERSION = 1;

const STORE_PAPERS = 'board_papers';
const STORE_READING_LIST = 'reading_list';
const STORE_SYNC_QUEUE = 'sync_queue';

// In-Memory Fallback for environments where IndexedDB is unsupported or in SSR
class MemoryStorageFallback {
  papers: Map<string, BoardQuestionItem> = new Map();
  readingList: Map<string, OfflineReadingRecord> = new Map();
  syncQueue: Map<string, OfflineSyncQueueItem> = new Map();

  constructor() {
    // Pre-populate in-memory fallback with seed board questions
    const seed = rawSeedBoardQuestions as BoardQuestionItem[];
    for (const q of seed) {
      this.papers.set(q.id, q);
    }
  }
}

const memoryFallback = new MemoryStorageFallback();

export const isIndexedDbSupported = (): boolean => {
  return typeof window !== 'undefined' && typeof window.indexedDB !== 'undefined';
};

/**
 * Initializes and upgrades the IndexedDB database schema for Board Papers.
 */
export const openBoardPapersVault = (): Promise<IDBDatabase | null> => {
  if (!isIndexedDbSupported()) {
    return Promise.resolve(null);
  }

  return new Promise((resolve, reject) => {
    const request = window.indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = (event.target as IDBOpenDBRequest).result;

      // 1. Board Papers Store
      if (!db.objectStoreNames.contains(STORE_PAPERS)) {
        const store = db.createObjectStore(STORE_PAPERS, { keyPath: 'id' });
        store.createIndex('subject', 'subject', { unique: false });
        store.createIndex('board', 'board', { unique: false });
        store.createIndex('year', 'year', { unique: false });
        store.createIndex('level', 'level', { unique: false });
      }

      // 2. Reading List Store
      if (!db.objectStoreNames.contains(STORE_READING_LIST)) {
        const readingStore = db.createObjectStore(STORE_READING_LIST, { keyPath: 'paper_id' });
        readingStore.createIndex('last_read_at', 'last_read_at', { unique: false });
      }

      // 3. Offline Sync Queue Store
      if (!db.objectStoreNames.contains(STORE_SYNC_QUEUE)) {
        const syncStore = db.createObjectStore(STORE_SYNC_QUEUE, { keyPath: 'id' });
        syncStore.createIndex('synced', 'synced', { unique: false });
        syncStore.createIndex('created_at', 'created_at', { unique: false });
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
};

/**
 * Saves a single board question to the offline vault.
 */
export const saveBoardQuestionToVault = async (paper: BoardQuestionItem): Promise<void> => {
  const db = await openBoardPapersVault();
  if (!db) {
    memoryFallback.papers.set(paper.id, paper);
    return;
  }

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_PAPERS, 'readwrite');
    const store = tx.objectStore(STORE_PAPERS);
    const req = store.put(paper);

    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
};

/**
 * Bulk saves board questions into the vault.
 */
export const saveMultipleBoardQuestions = async (papers: BoardQuestionItem[]): Promise<void> => {
  const db = await openBoardPapersVault();
  if (!db) {
    papers.forEach((p) => memoryFallback.papers.set(p.id, p));
    return;
  }

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_PAPERS, 'readwrite');
    const store = tx.objectStore(STORE_PAPERS);

    papers.forEach((p) => store.put(p));

    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
};

/**
 * Retrieves a single board question by ID from the vault.
 */
export const getBoardQuestionFromVault = async (id: string): Promise<BoardQuestionItem | null> => {
  const db = await openBoardPapersVault();
  if (!db) {
    return memoryFallback.papers.get(id) || null;
  }

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_PAPERS, 'readonly');
    const store = tx.objectStore(STORE_PAPERS);
    const req = store.get(id);

    req.onsuccess = () => {
      if (req.result) {
        resolve(req.result as BoardQuestionItem);
      } else {
        // Fallback to seed in case not yet persisted
        const seed = rawSeedBoardQuestions as BoardQuestionItem[];
        const found = seed.find((item) => item.id === id) || null;
        resolve(found);
      }
    };
    req.onerror = () => reject(req.error);
  });
};

/**
 * Retrieves all saved board questions in the vault. If vault is empty,
 * pre-seeds with rawSeedBoardQuestions and returns them.
 */
export const getAllSavedBoardQuestions = async (): Promise<BoardQuestionItem[]> => {
  const db = await openBoardPapersVault();
  if (!db) {
    return Array.from(memoryFallback.papers.values());
  }

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_PAPERS, 'readwrite');
    const store = tx.objectStore(STORE_PAPERS);
    const req = store.getAll();

    req.onsuccess = () => {
      const results = req.result as BoardQuestionItem[];
      if (!results || results.length === 0) {
        // Pre-seed the vault with authentic board questions
        const seed = rawSeedBoardQuestions as BoardQuestionItem[];
        for (const item of seed) {
          store.put(item);
        }
        resolve(seed);
      } else {
        resolve(results);
      }
    };
    req.onerror = () => reject(req.error);
  });
};

/**
 * Performs client-side search and filtering across saved offline questions.
 */
export const searchSavedQuestions = async (
  query: string,
  filters?: { board?: string; subject?: string; year?: number }
): Promise<BoardQuestionItem[]> => {
  const allQuestions = await getAllSavedBoardQuestions();
  const qClean = query.trim().toLowerCase();

  return allQuestions.filter((item) => {
    if (filters?.board && item.board !== filters.board) {
      return false;
    }
    if (filters?.subject && item.subject !== filters.subject) {
      return false;
    }
    if (filters?.year && item.year !== filters.year) {
      return false;
    }

    if (!qClean) return true;

    return (
      item.subject_bn.toLowerCase().includes(qClean) ||
      item.board_bn.toLowerCase().includes(qClean) ||
      item.chapter.toLowerCase().includes(qClean) ||
      item.stem_bn.toLowerCase().includes(qClean) ||
      item.year.toString().includes(qClean)
    );
  });
};

/**
 * Records or updates reading status for a paper in the offline vault.
 */
export const markPaperAsRead = async (paperId: string, progressPercent = 100): Promise<void> => {
  const record: OfflineReadingRecord = {
    paper_id: paperId,
    saved_at: Date.now(),
    last_read_at: Date.now(),
    progress_percent: progressPercent
  };

  const db = await openBoardPapersVault();
  if (!db) {
    memoryFallback.readingList.set(paperId, record);
    return;
  }

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_READING_LIST, 'readwrite');
    const store = tx.objectStore(STORE_READING_LIST);
    const req = store.put(record);

    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
};

/**
 * Queues an offline submission for background sync when connection resumes.
 */
export const queueOfflineAction = async (
  action: OfflineSyncQueueItem['action'],
  payload: Record<string, any>
): Promise<string> => {
  const queueItem: OfflineSyncQueueItem = {
    id: `sync_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`,
    action,
    payload,
    created_at: Date.now(),
    retry_count: 0,
    synced: false
  };

  const db = await openBoardPapersVault();
  if (!db) {
    memoryFallback.syncQueue.set(queueItem.id, queueItem);
    return queueItem.id;
  }

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_SYNC_QUEUE, 'readwrite');
    const store = tx.objectStore(STORE_SYNC_QUEUE);
    const req = store.put(queueItem);

    req.onsuccess = () => resolve(queueItem.id);
    req.onerror = () => reject(req.error);
  });
};

/**
 * Calculates offline vault statistics.
 */
export const getOfflineVaultStats = async (): Promise<OfflineVaultStats> => {
  const allPapers = await getAllSavedBoardQuestions();
  const subjectsSet = new Set<string>();
  const boardsSet = new Set<string>();

  for (const paper of allPapers) {
    subjectsSet.add(paper.subject_bn);
    boardsSet.add(paper.board_bn);
  }

  return {
    totalPapers: allPapers.length,
    subjects: Array.from(subjectsSet),
    boards: Array.from(boardsSet),
    lastSyncTime: Date.now()
  };
};
