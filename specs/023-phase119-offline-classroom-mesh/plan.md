<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 119 Offline P2P Classroom Mesh & Local CRDT Sync
FILE:      specs/023-phase119-offline-classroom-mesh/plan.md
PHASE:     Phase 119 - Offline P2P Classroom Mesh & Local CRDT Sync
PURPOSE:   Architectural blueprint for Lamport CRDT mutation ledger, teacher offline
           station dashboard, cloud batch reconciliation service, and test suite.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Implementation Plan: Phase 119 — Offline P2P Classroom Mesh & Local CRDT Sync

## Data Flow & Architecture

```
 [Rural Student Device 1] --\
 [Rural Student Device 2] ----> [Teacher Station Offline Hub]
 [Rural Student Device 60] -/        | (Lamport CRDT Mutation Ledger)
                                     | Local Wi-Fi / Bluetooth
                                     v
                       [OfflineClassroomStation Dashboard]
                                     |
                                     | Internet Re-established
                                     v
                      [Batch Cloud Reconcile Endpoint]
                                     |
                                     v
                   [OfflineCrdtSyncService Reconciler]
```

## Work Breakdown Structure

1. **Frontend CRDT Mutation Ledger (`frontend/src/lib/offline/crdtMutationLedger.ts`)**:
   - Class `CrdtMutationLedger`:
     - Internal Lamport logical clock counter.
     - Mutation entries: `{ mutation_id, client_id, station_id, lamport_clock, mutation_type, payload, timestamp }`.
     - Method `recordMutation(type, payload)`: advances clock and registers mutation.
     - Method `mergeRemoteMutations(remoteMutations)`: deterministic LWW resolution with `(lamport_clock, client_id)` tie-breaking.
     - Method `getStateSnapshot()`: resolves effective quiz answers per student.
     - Method `exportBatchPayload()`: formats pending mutations for cloud sync with SHA-256 batch checksum.
     - Method `markSynced(syncedMutationIds)`.

2. **Frontend Offline Classroom Station (`frontend/src/components/offline-mesh/OfflineClassroomStation.tsx`)**:
   - High-contrast utilitarian outdoor dashboard:
     - Header: Station status, local IP, SSID, offline indicator ("অফলাইন মোড সক্রিয় — স্থানীয় মেশ নেটওয়ার্ক").
     - 4 Metric cards: Connected students (0-60), Pending CRDT mutations, Answered questions, Sync status.
     - Peer student roster with device type, connection signal, and last mutation timestamp.
     - Tactile 3D Oxford Navy action buttons:
       - "লোকাল কুইজ শুরু করুন" (`shadow-[0_4px_0_0_#061727] active:translate-y-1 active:shadow-none bg-[#0A2540]`).
       - "ক্লাউডে সিঙ্ক করুন" (`shadow-[0_4px_0_0_#061727] active:translate-y-1 active:shadow-none bg-[#0A2540]`).
     - Pure Lucide icons (`WifiOff`, `Share2`, `RefreshCw`, `CheckCircle2`, `Database`, `Users`).

3. **Backend Offline CRDT Sync Service (`backend/app/services/offline_crdt_sync_service.py`)**:
   - Class `OfflineCrdtSyncService`:
     - Reconciles batches of CRDT mutations.
     - Verifies checksum hash integrity.
     - Deduplicates already-applied mutations (idempotent).
     - Updates student records into primary platform databases.
     - Maintains sync audit logs.

4. **REST Endpoints (`backend/app/api/v1/endpoints/offline_sync.py`)**:
   - `POST /offline-sync/batch-reconcile`: Receives batch payload from teacher station.
   - `GET /offline-sync/station/{station_id}/status`: Fetches last sync timestamp and status.
   - Mount in `backend/app/api/v1/router.py`.

5. **Automated Verification Suite (`backend/tests/test_phase119_offline_crdt_sync.py`)**:
   - Test 1: Lamport logical clock progression and ordering.
   - Test 2: Conflict-free merge determinism and idempotency.
   - Test 3: Batch payload verification and SHA-256 checksum check.
   - Test 4: Offline station status and synchronization reconciliation.
   - Test 5: Frontend component tactile styling, outdoor high contrast, and Lucide icons.
   - Test 6: Zero-emoji compliance and standardized Developer Architecture Notes.
