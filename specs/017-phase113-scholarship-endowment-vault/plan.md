<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Plan
TOPIC:     Phase 113 National Merit Scholarship Pool & Autonomous Disbursement
FILE:      specs/017-phase113-scholarship-endowment-vault/plan.md
PHASE:     Phase 113 - National Merit Scholarship Pool & Autonomous Disbursement
PURPOSE:   Engineering roadmap for building the scholarship disbursement service,
           endowment card, ledger modal, API endpoints, and zero-regression tests.
STANDARDS: OWASP ASVS L2, FinTech B2C Security, Pure Academic Design, Strict Zero-Emoji
-->

# Implementation Plan: Phase 113 — National Merit Scholarship Pool & Autonomous Disbursement

## Architectural Roadmap

1. **Step 1: Scholarship Disbursement Service (`backend/app/services/scholarship_disbursement_service.py`)**
   - Endowment fund registry with district quota tracking.
   - Algorithmic eligibility evaluator (merit GPA 5.0 / top 5% exam percentile + income <= 15,000 BDT).
   - Dual-authorization workflow state machine: `SUBMITTED` -> `ACADEMIC_APPROVED` -> `DUAL_APPROVED` -> `DISBURSED`.
   - Simulated bKash Merchant B2C / Nagad Bulk Pay gateway adapters.
   - Idempotency key lock manager preventing double-spending.
   - Cryptographic transaction seal generator (`SHA-256`) and immutable audit logs.
   - Public anonymized ledger exporter.

2. **Step 2: Scholarship Endowment Card Component (`frontend/src/components/scholarship/ScholarshipEndowmentCard.tsx`)**
   - Academic Oxford Navy styling with Scholarly Gold accents.
   - District quota allocation breakdown (Kurigram, Sunamganj, Bandarban, Barguna, etc.).
   - Fund progress meter, beneficiary count, and grant sizes.
   - Tactile 3D Oxford Navy buttons ("আবেদন জমা দিন", "বৃত্তি অনুমোদন করুন", "পাবলিক লেজার অডিট").
   - Pure Lucide SVG icons.

3. **Step 3: Public Disbursement Ledger Modal (`frontend/src/components/scholarship/DisbursementLedgerModal.tsx`)**
   - Modal interface displaying live, immutable transaction records.
   - Masked student IDs (`STU-****-9482`), districts, amounts in BDT, transaction hashes, and dual-custodian signatures.
   - Search/filter by district and payment gateway.

4. **Step 4: REST API Endpoints (`backend/app/api/v1/endpoints/scholarships.py`)**
   - `GET /scholarships/pools`: List active endowment pools and district quotas.
   - `POST /scholarships/evaluate-eligibility`: Evaluate student qualifications.
   - `POST /scholarships/apply`: Submit student scholarship application.
   - `POST /scholarships/approve`: Record academic/financial custodian authorization.
   - `POST /scholarships/disburse`: Execute bKash/Nagad B2C payout with idempotency.
   - `GET /scholarships/ledger`: Return public anonymized cryptographic ledger.
   - Mount router into `backend/app/api/v1/router.py`.

5. **Step 5: Automated Test Suite (`backend/tests/test_phase113_scholarship_disbursement.py`)**
   - Unit and integration tests for eligibility logic, dual-authorization, double-spending prevention, cryptographic hashing, and zero-emoji compliance.

6. **Step 6: Full Platform Regression Discovery**
   - Execute `python3 -m unittest discover -s backend/tests` to assert 100% pass rate across all 1,348+ tests.
   - Execute AST security sweep and zero-emoji sweep.
