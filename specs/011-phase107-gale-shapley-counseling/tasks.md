<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 107 Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
FILE:      specs/011-phase107-gale-shapley-counseling/tasks.md
PHASE:     Phase 107 - Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
PURPOSE:   Ordered task list tracking atomic implementation steps for Deferred Acceptance
           matching, quota auto-spillover, migration cascade simulation, UI components, and test validation.
STANDARDS: Pareto-Optimal Deferred Acceptance, Quota Spillover Balancing, Zero-Emoji, UI/UX Pro Max
-->

# Tasks: Phase 107 — Centralized Admission Counseling & Gale-Shapley Stable Matching Hub

## Tasks Ledger

- [x] Task 1: Implement Gale-Shapley Counseling Service (`backend/app/services/gale_shapley_counseling_service.py`)
  - Student-proposing Deferred Acceptance algorithm with verified envy-free stability
  - Quota partitioning across General, Freedom Fighter, Tribal, District, Special Needs
  - Automatic quota spillover to General merit pool when unfilled
  - Multi-stage seat migration cascade simulator across sequential counseling rounds
  - Real-time admission probability predictor based on cut-off metrics
- [x] Task 2: Implement Admission Counseling Matrix Component (`frontend/src/components/admission/AdmissionCounselingMatrix.tsx`)
  - Elite university guidance room visual design with drag/reorder preference cards
  - Real-time admission probability badges with gentle gradients
  - Transparent quota explanations and eligibility toggle
  - Tactile 3D button physics (`shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`)
  - Zero-Emoji compliance and 'Hind Siliguri' + 'Plus Jakarta Sans' typography
- [x] Task 3: Implement Migration Cascade Visualizer Component (`frontend/src/components/admission/MigrationCascadeVisualizer.tsx`)
  - Multi-round seat migration cascade step visualizer
  - Upward migration pill badges (e.g., JU CSE -> DU CSE -> BUET CSE)
  - Round scrubber and cut-off rank change telemetry
  - Tactile 3D button physics (`shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`)
- [x] Task 4: Mount Counseling REST API Endpoints (`backend/app/api/v1/endpoints/counseling.py`)
  - `POST /api/v1/counseling/match`
  - `POST /api/v1/counseling/migrate-simulate`
  - `GET /api/v1/counseling/programs`
  - `POST /api/v1/counseling/predict-probability`
  - Mount router in `backend/app/api/v1/router.py`
- [x] Task 5: Implement Counseling Studio Host Page (`frontend/src/pages/counseling.tsx`)
  - Unified guidance studio page mounting Counseling Matrix and Migration Cascade Visualizer
  - Integration with Navbar, Footer, and AppHead
- [x] Task 6: Implement automated verification test suite (`backend/tests/test_phase107_gale_shapley_counseling.py`)
  - Gale-Shapley stability (zero blocking pairs)
  - Quota partitioning and automatic spillover to General pool
  - Multi-stage migration cascade simulation
  - REST API endpoint verification
  - Standardized Developer Architecture Note headers check and strict zero-emoji sweep
- [x] Task 7: Execute full regression test discovery (`python3 -m unittest discover -s backend/tests`) asserting 100% pass rate
