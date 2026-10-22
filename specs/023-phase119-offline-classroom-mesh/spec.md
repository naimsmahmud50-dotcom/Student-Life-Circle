<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Phase 119 Offline P2P Classroom Mesh & Local CRDT Sync
FILE:      specs/023-phase119-offline-classroom-mesh/spec.md
PHASE:     Phase 119 - Offline P2P Classroom Mesh & Local CRDT Sync
PURPOSE:   Specifies offline peer-to-peer classroom station, Lamport-clock CRDT mutation
           ledger for up to 60 rural students, and resilient cloud reconciliation.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Specification: Phase 119 — Offline P2P Classroom Mesh & Local CRDT Sync

## 1. Background & Mission
In rural Bangladeshi upazilas, haor regions, and char areas, mobile internet connectivity is frequently unavailable or erratic. However, classrooms need to administer local quizzes, record student attendance, and preserve continuous learning without internet.

Phase 119 delivers an **Offline P2P Classroom Mesh Station & Local CRDT Mutation Ledger**:
1. **CRDT Mutation Ledger (`crdtMutationLedger.ts`)**:
   - State-based Conflict-free Replicated Data Type (CRDT) mutation ledger using Lamport logical timestamps.
   - Allows up to 60 rural students to connect locally to a teacher's offline hub over local Wi-Fi / Bluetooth.
   - Deterministic last-write-wins (LWW) and state-based register merging with `(lamport_timestamp, client_id)` tie-breaking.
   - Guarantees idempotency: submitting the same mutation multiple times yields the exact same state without duplications.
2. **Offline Classroom Station Dashboard (`OfflineClassroomStation.tsx`)**:
   - Clean, utilitarian, high-contrast interface designed for outdoor sunlight readability in rural schools.
   - Displays real-time connected student count (0 to 60), active local quiz session, local peer IP / station identifier, and pending mutation ledger queue count.
   - 3D tactile Oxford Navy buttons:
     - "লোকাল কুইজ শুরু করুন" (`shadow-[0_4px_0_0_#061727] active:translate-y-1 active:shadow-none bg-[#0A2540] text-white font-semibold rounded-2xl`).
     - "ক্লাউডে সিঙ্ক করুন" (`shadow-[0_4px_0_0_#061727] active:translate-y-1 active:shadow-none bg-[#0A2540] text-white font-semibold rounded-2xl`).
   - Pure Lucide vector icons (`WifiOff`, `Share2`, `RefreshCw`, `CheckCircle2`, `Database`, `Users`, `Check`).
3. **Cloud CRDT Sync Service (`offline_crdt_sync_service.py`)**:
   - Ingests batch reconciliation payloads when the teacher connects back to the internet.
   - Reconciles offline student attempts into primary databases idempotently, verifying cryptographic batch hashes.
4. **REST API Endpoints (`offline_sync.py`)**:
   - Versioned endpoint `POST /api/v1/offline-sync/batch-reconcile` and `GET /api/v1/offline-sync/station/{station_id}/status`.
   - Mounted in `backend/app/api/v1/router.py`.

---

## 2. Functional Requirements
- **FR-119.1 (Lamport Clock Ordering)**:
  - Lamport clock advances strictly monotonically on each local mutation: `clock = max(clock, incoming_clock) + 1`.
  - Mutation records contain `mutation_id`, `client_id`, `station_id`, `lamport_clock`, `mutation_type`, `payload`, `timestamp`.
- **FR-119.2 (Idempotent Merge)**:
  - Merging two mutation sets $A \cup B$ produces a consistent, conflict-free state regardless of arrival order.
- **FR-119.3 (Offline Classroom Station UI)**:
  - Displays station stats (connected students up to 60, pending mutations, sync status).
  - High contrast for outdoor readability (`#FAFAF8` background, `#0A2540` Oxford Navy typography, `#FFFFFF` cards).
  - Zero emojis, 100% Lucide vector icons.
- **FR-119.4 (Batch Cloud Reconcile)**:
  - Endpoint verifies batch checksum, extracts valid student quiz answers, and records synced status.

---

## 3. Verification Criteria
- Automated test `backend/tests/test_phase119_offline_crdt_sync.py` passes 100%.
- Zero-emoji sweep passes with 0 violations across 550+ files.
- Security sweep passes with 0 vulnerabilities.
- Global platform discover passes all 1,384+ tests.
