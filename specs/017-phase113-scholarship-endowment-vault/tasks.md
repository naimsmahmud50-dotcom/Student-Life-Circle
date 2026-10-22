<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 113 National Merit Scholarship Pool & Autonomous Disbursement
FILE:      specs/017-phase113-scholarship-endowment-vault/tasks.md
PHASE:     Phase 113 - National Merit Scholarship Pool & Autonomous Disbursement
PURPOSE:   Tracks implementation and verification of scholarship disbursement service,
           endowment card, ledger modal, API endpoints, and regression tests.
STANDARDS: OWASP ASVS L2, FinTech B2C Security, Pure Academic Design, Strict Zero-Emoji
-->

# Tasks: Phase 113 — National Merit Scholarship Pool & Autonomous Disbursement

## Tasks Ledger

- [x] Task 1: Implement Scholarship Disbursement Service (`backend/app/services/scholarship_disbursement_service.py`)
  - Merit evaluation logic (GPA 5.0 or top 5% exam percentile + income <= 15,000 BDT)
  - District quota allocations (Kurigram, Sunamganj, Bandarban, Barguna, etc.)
  - Dual-authorization escrow release (evaluator + custodian)
  - bKash Merchant B2C Disbursement / Nagad Bulk Pay adapter simulation
  - Double-spending defense with atomic idempotency keys and state checks
  - Cryptographic SHA-256 transaction receipts and immutable audit logging
- [x] Task 2: Build Scholarship Endowment Card Component (`frontend/src/components/scholarship/ScholarshipEndowmentCard.tsx`)
  - Pure Academic Oxford Navy and Scholarly Gold aesthetics
  - District quota badges and fund progress meter
  - Tactile 3D Oxford Navy buttons for application, approval, and audit
  - Pure Lucide SVG icons and zero emojis
- [x] Task 3: Build Public Disbursement Ledger Modal (`frontend/src/components/scholarship/DisbursementLedgerModal.tsx`)
  - Anonymized student transaction records (`STU-****-XXXX`)
  - Real-time district, amount (BDT), gateway, and SHA-256 seal display
  - Search and filter by district or gateway
- [x] Task 4: Implement and Mount REST API Endpoints (`backend/app/api/v1/endpoints/scholarships.py`)
  - Endpoints: pools, evaluate-eligibility, apply, approve, disburse, ledger
  - Mount router in `backend/app/api/v1/router.py`
- [x] Task 5: Implement Automated Unit & Integration Tests (`backend/tests/test_phase113_scholarship_disbursement.py`)
  - Verify eligibility evaluation (merit + need + district quota)
  - Verify dual-authorization workflow and double-spending protection
  - Verify bKash/Nagad B2C execution and SHA-256 receipt integrity
  - Verify Developer Architecture Notes and strict Zero-Emoji compliance
- [x] Task 6: Platform Regression Discovery & Certification
  - Run full platform test discovery (`python3 -m unittest discover -s backend/tests`)
  - Run zero-emoji sweep and security sweep
