# PLAN: Phase 133 — Direct-to-Mobile Micro-Scholarship Disbursement Vault with Proof-of-Merit

## 1. Architectural Strategy
The scholarship disbursement system functions as an automated institutional endowment vault. Students submit cryptographic Proof-of-Merit credentials which pass through a 4-tier evaluation pipeline before funds are disbursed via MFS gateways.

```mermaid
flowchart TD
    Student[Student Applicant] --> Portal[Scholarship Disbursement Portal]
    Portal --> Submission[Application: NID, Merit Credentials, MFS Wallet]
    Submission --> AntiFraud[Anti-Fraud Guard: Duplicate NID/Wallet, Velocity Limits]
    AntiFraud --> ProofOfMerit[Proof-of-Merit Evaluator: Olympiad Rank, GPA 5.0, District Quota]
    ProofOfMerit --> Approved[Approval & Stipend Allocation (BDT 3,000 - 15,000)]
    Approved --> MFSGateway[MFS Gateway: bKash / Nagad / Rocket with SHA-256 Hash]
    MFSGateway --> Ledger[(Immutable MFS Ledger: REVOKE UPDATE, DELETE)]
    Ledger --> Notification[Disbursement Attestation Receipt]
```

## 2. Implementation Steps
1. **Backend Package & Disbursement Vault**:
   - Write `backend/scholarship/__init__.py`.
   - Write `backend/scholarship/disbursement_vault.py` with `ProofOfMeritEvaluator`, `AntiFraudGuard`, `MFSDisbursementGateway`, and `ScholarshipVaultService`.
2. **Database Migration with 100% RLS & Immutability**:
   - Write `backend/migrations/011_scholarship_disbursement_rls.sql` with tables `scholarship_endowment_vaults`, `micro_scholarship_applications`, `mfs_disbursement_ledger`, `scholarship_fraud_audit_logs`.
   - Apply `REVOKE UPDATE, DELETE` on `mfs_disbursement_ledger` with immutability trigger.
3. **Frontend Banking UI**:
   - Write `frontend/src/pages/scholarship/disbursement.tsx` with Proof-of-Merit badge, MFS operator selection (bKash, Nagad, Rocket), stipend disbursement calculator, 3D tactile buttons, and pure Lucide vector icons.
4. **Automated Test Suite**:
   - Write `backend/tests/test_phase133_scholarship_disbursement.py` verifying headers, zero-emoji, Proof-of-Merit calculations, duplicate NID rejection, MFS wallet validation, SHA-256 transaction hashes, and Supabase RLS immutability.
5. **Execution & Regression Verification**:
   - Run zero-emoji sweep.
   - Run Phase 133 test suite.
   - Run full backend test discovery (all 1,485+ tests).
   - Compile Next.js production bundle (`npm run build`).
   - Start daemon and verify HTTP 200 on `/scholarship/disbursement`.
