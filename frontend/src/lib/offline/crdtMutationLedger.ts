/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    CRDT Mutation Ledger & Lamport Logical Clock Manager
 * TOPIC:     Phase 119 Offline P2P Classroom Mesh & Local CRDT Sync
 * FILE:      frontend/src/lib/offline/crdtMutationLedger.ts
 * PHASE:     Phase 119 - Offline P2P Classroom Mesh & Local CRDT Sync
 * PURPOSE:   Provides state-based Conflict-free Replicated Data Type (CRDT) mutation
 *            tracking with Lamport logical clocks, enabling up to 60 rural students
 *            to participate in offline quizzes and merge answers deterministically.
 * STANDARDS: UI/UX Pro Max, Distributed CRDT LWW Semantics, Zero-Emoji Spec
 */

export interface CrdtMutationRecord {
  mutation_id: string;
  client_id: string;
  station_id: string;
  lamport_clock: number;
  mutation_type: 'RECORD_ANSWER' | 'START_QUIZ' | 'FINISH_QUIZ' | 'ATTENDANCE_PING';
  payload: {
    student_id?: string;
    student_name?: string;
    roll_number?: string;
    quiz_id?: string;
    question_id?: string;
    option_id?: string;
    [key: string]: unknown;
  };
  timestamp: number;
  synced: boolean;
}

export interface ResolvedAnswer {
  quiz_id: string;
  student_id: string;
  question_id: string;
  option_id: string;
  lamport_clock: number;
  client_id: string;
  timestamp: number;
}

export interface BatchSyncPayload {
  station_id: string;
  batch_id: string;
  mutations_count: number;
  mutations: CrdtMutationRecord[];
  generated_at: number;
  checksum: string;
}

export class CrdtMutationLedger {
  private localStationId: string;
  private currentClock: number;
  private mutations: Map<string, CrdtMutationRecord>;
  private resolvedAnswers: Map<string, ResolvedAnswer>;

  constructor(stationId: string = 'station-hub-01', initialClock: number = 0) {
    this.localStationId = stationId;
    this.currentClock = initialClock;
    this.mutations = new Map<string, CrdtMutationRecord>();
    this.resolvedAnswers = new Map<string, ResolvedAnswer>();
  }

  /**
   * Advances the internal Lamport logical clock monotonically.
   */
  public advanceClock(incomingClock: number = 0): number {
    this.currentClock = Math.max(this.currentClock, incomingClock) + 1;
    return this.currentClock;
  }

  /**
   * Returns current Lamport clock value.
   */
  public getClock(): number {
    return this.currentClock;
  }

  /**
   * Records a local mutation into the ledger and advances clock.
   */
  public recordMutation(
    clientId: string,
    mutationType: CrdtMutationRecord['mutation_type'],
    payload: CrdtMutationRecord['payload']
  ): CrdtMutationRecord {
    const clock = this.advanceClock();
    const now = Date.now();
    const mutationId = `mut-${clientId}-${clock}-${now.toString(36)}`;

    const record: CrdtMutationRecord = {
      mutation_id: mutationId,
      client_id: clientId,
      station_id: this.localStationId,
      lamport_clock: clock,
      mutation_type: mutationType,
      payload,
      timestamp: now,
      synced: false,
    };

    this.mutations.set(mutationId, record);
    this.applyMutationToState(record);
    return record;
  }

  /**
   * Merges an array of remote mutations into the ledger.
   * Guarantees deterministic conflict resolution and idempotency.
   */
  public mergeRemoteMutations(remoteMutations: CrdtMutationRecord[]): {
    mergedCount: number;
    duplicateCount: number;
  } {
    let mergedCount = 0;
    let duplicateCount = 0;

    // Advance local clock past highest incoming clock
    for (const mut of remoteMutations) {
      if (this.mutations.has(mut.mutation_id)) {
        duplicateCount++;
        continue;
      }

      this.currentClock = Math.max(this.currentClock, mut.lamport_clock);
      this.mutations.set(mut.mutation_id, { ...mut, synced: false });
      this.applyMutationToState(mut);
      mergedCount++;
    }

    // Monotonic increment after batch ingestion
    if (mergedCount > 0) {
      this.currentClock += 1;
    }

    return { mergedCount, duplicateCount };
  }

  /**
   * Applies a mutation record to resolved state using Last-Write-Wins (LWW) with tie-breaking.
   */
  private applyMutationToState(mut: CrdtMutationRecord): void {
    if (mut.mutation_type === 'RECORD_ANSWER') {
      const { quiz_id, student_id, question_id, option_id } = mut.payload;
      if (!quiz_id || !student_id || !question_id || !option_id) return;

      const stateKey = `${quiz_id}:${student_id}:${question_id}`;
      const existing = this.resolvedAnswers.get(stateKey);

      if (!existing) {
        this.resolvedAnswers.set(stateKey, {
          quiz_id,
          student_id,
          question_id,
          option_id,
          lamport_clock: mut.lamport_clock,
          client_id: mut.client_id,
          timestamp: mut.timestamp,
        });
      } else {
        // Last-Write-Wins rule: higher lamport_clock wins; tie-break by client_id lexicographically
        const incomingWins =
          mut.lamport_clock > existing.lamport_clock ||
          (mut.lamport_clock === existing.lamport_clock &&
            mut.client_id > existing.client_id);

        if (incomingWins) {
          this.resolvedAnswers.set(stateKey, {
            quiz_id,
            student_id,
            question_id,
            option_id,
            lamport_clock: mut.lamport_clock,
            client_id: mut.client_id,
            timestamp: mut.timestamp,
          });
        }
      }
    }
  }

  /**
   * Returns all resolved answers.
   */
  public getResolvedAnswers(): ResolvedAnswer[] {
    return Array.from(this.resolvedAnswers.values());
  }

  /**
   * Returns count of unsynced pending mutations.
   */
  public getPendingCount(): number {
    let count = 0;
    for (const mut of this.mutations.values()) {
      if (!mut.synced) count++;
    }
    return count;
  }

  /**
   * Formats unsynced mutations into a batch synchronization payload for cloud sync.
   */
  public exportBatchPayload(): BatchSyncPayload {
    const unsynced: CrdtMutationRecord[] = [];
    for (const mut of this.mutations.values()) {
      if (!mut.synced) {
        unsynced.push(mut);
      }
    }

    const now = Date.now();
    const batchId = `batch-${this.localStationId}-${now.toString(36)}`;

    // Simple deterministic checksum calculation
    const payloadStr = unsynced.map((m) => m.mutation_id).join(':');
    let hash = 0;
    for (let i = 0; i < payloadStr.length; i++) {
      hash = (hash << 5) - hash + payloadStr.charCodeAt(i);
      hash |= 0;
    }
    const checksum = Math.abs(hash).toString(16).padStart(8, '0');

    return {
      station_id: this.localStationId,
      batch_id: batchId,
      mutations_count: unsynced.length,
      mutations: unsynced,
      generated_at: now,
      checksum,
    };
  }

  /**
   * Marks given mutation IDs as successfully synchronized to cloud.
   */
  public markSynced(mutationIds: string[]): number {
    let updated = 0;
    for (const id of mutationIds) {
      const mut = this.mutations.get(id);
      if (mut && !mut.synced) {
        mut.synced = true;
        updated++;
      }
    }
    return updated;
  }

  /**
   * Returns total mutation count in memory.
   */
  public getAllMutations(): CrdtMutationRecord[] {
    return Array.from(this.mutations.values());
  }
}
