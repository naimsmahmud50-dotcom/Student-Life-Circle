# SPEC: Phase 133 — Direct-to-Mobile Micro-Scholarship Disbursement Vault with Proof-of-Merit

## 1. Overview
Phase 133 introduces the **Direct-to-Mobile Micro-Scholarship Disbursement Vault**, an institutional financial technology module providing automated, merit-verified educational stipends directly to students via Bangladesh's Mobile Financial Services (MFS: bKash, Nagad, Rocket). The system validates cryptographic Proof-of-Merit credentials (Olympiad podium ranks, Board exam GPA 5.0, rural district quotas), executes anti-fraud and sybil checks (duplicate NID, multi-identity wallets), and records immutable financial disbursements.

## 2. Architectural Pillars
1. **Developer Architecture Note**: Standardized header block on every created/modified file.
2. **Proof-of-Merit Cryptographic Evaluation**: Automatically qualifies applicants based on verifiable educational achievements and district equity weighting.
3. **Multi-Vector Fraud Prevention Engine**:
   - Duplicate NID / Birth Registration Certificate defense.
   - Cross-account student ID binding defense.
   - Bangladeshi MFS MSISDN format verification (`+8801[3-9]\d{8}`).
   - Velocity rate limits preventing multiple disbursements within a calendar cohort.
4. **MFS Payout Clearinghouse Simulator**:
   - bKash, Nagad, Rocket API disbursement simulation.
   - Cryptographic SHA-256 transaction hash generation.
   - Idempotency key tracking preventing double-spending.
5. **Supabase Financial Immutability (Migration 011)**:
   - 100% Row Level Security with `REVOKE UPDATE, DELETE` on `mfs_disbursement_ledger` ensuring immutable audit trails under ASVS L2.
6. **Academic Banking Aesthetic**: Oxford Navy (`#0A2540`), Academic Emerald (`#065F46`), Scholar Gold (`#B45309`), 3D physical tactile buttons, and pure Lucide SVG vector icons.

## 3. File Inventory
- `backend/scholarship/__init__.py`: Package exports for disbursement vault and fraud engine.
- `backend/scholarship/disbursement_vault.py`: Core logic for Proof-of-Merit scoring, anti-fraud checks, and MFS disbursement processing.
- `backend/migrations/011_scholarship_disbursement_rls.sql`: Immutable ledger schema and RLS policies.
- `frontend/src/pages/scholarship/disbursement.tsx`: Institutional scholarship portal with application flow, MFS selector, and transaction tracker.
- `backend/tests/test_phase133_scholarship_disbursement.py`: Automated test suite.
