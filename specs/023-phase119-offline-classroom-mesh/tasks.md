<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 119 Offline P2P Classroom Mesh & Local CRDT Sync
FILE:      specs/023-phase119-offline-classroom-mesh/tasks.md
PHASE:     Phase 119 - Offline P2P Classroom Mesh & Local CRDT Sync
PURPOSE:   Establishes Lamport-clock CRDT mutation ledger, teacher offline station UI,
           cloud batch reconciliation service, and automated test suite.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Tasks: Phase 119 — Offline P2P Classroom Mesh & Local CRDT Sync

## Tasks Ledger

- [x] Task 1: Implement CRDT Mutation Ledger (`frontend/src/lib/offline/crdtMutationLedger.ts`)
  - State-based CRDT mutation ledger using Lamport logical clocks
  - Deterministic LWW merge resolution with `(lamport_clock, client_id)` tie-breaking
  - Idempotent remote mutation merging for up to 60 rural students
  - Batch payload export with SHA-256 verification hash
- [x] Task 2: Build Offline Classroom Station Component (`frontend/src/components/offline-mesh/OfflineClassroomStation.tsx`)
  - High-contrast utilitarian dashboard for rural outdoor readability
  - Connected students counter (up to 60), local quiz status, pending mutation count
  - 3D tactile Oxford Navy buttons: "লোকাল কুইজ শুরু করুন" and "ক্লাউডে সিঙ্ক করুন"
  - Pure Lucide vector icons (`WifiOff`, `Share2`, `RefreshCw`, `CheckCircle`, `Database`, `Users`)
- [x] Task 3: Implement Offline CRDT Sync Service (`backend/app/services/offline_crdt_sync_service.py`)
  - Idempotent batch reconciliation of offline student mutations
  - Checksum validation and deduplication
  - Sync audit history tracking
- [x] Task 4: Implement REST Endpoints & Mount Router (`backend/app/api/v1/endpoints/offline_sync.py` and `router.py`)
  - Endpoints: batch reconciliation, station status
  - Mount in `backend/app/api/v1/router.py`
- [x] Task 5: Automated Test Suite (`backend/tests/test_phase119_offline_crdt_sync.py`)
  - Assert Lamport clock monotonicity and tie-breaking
  - Assert conflict-free merge idempotency
  - Assert batch payload checksum validation
  - Assert frontend tactile buttons, high-contrast styling, and pure Lucide icons
  - Assert Developer Architecture Notes and strict zero emojis across all Phase 119 files
- [x] Task 6: Platform Regression Discovery & Certification
  - Run zero-emoji sweep, security audit, and full platform discovery across 1,384+ tests
