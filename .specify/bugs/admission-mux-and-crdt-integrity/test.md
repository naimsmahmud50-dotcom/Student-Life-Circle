# Verification Report: Admission Multiplexer, CRDT Sync & Talent Passport Security

## Test Suite Execution
- **File**: `backend/tests/test_phase30_admission_mux_and_passport.py`
- **Methodology**: Automated Unit & Integration testing under Python `unittest`.

### Verification Matrix
1. **Eligibility Check & Grade Requirements**:
   - Tests Science group eligibility across BUET (5.0 HSC / 9.5 combined), DU Ka-Unit (4.0 HSC / 8.5 combined), Medical, CKRUET, and GST.
   - Asserts non-Science or sub-GPA candidates receive explicit `is_eligible=False` with status reason breakdown.
2. **Schedule Conflict Detection**:
   - Asserts that if two selected circulars share the same exam date, `conflicts_detected` flags the collision.
3. **Batch Application Settlement & Admit Card Generation**:
   - Asserts 1-click batch application generates unique admit card IDs, roll numbers, exam venues, and room assignments.
4. **CRDT Mutation Deduplication & Idempotency**:
   - Sends duplicate `mutation_id` in subsequent sync request; asserts `applied_count == 0` and status is `IDEMPOTENT_NOOP`.
5. **Set-Union & LWW CRDT Merging**:
   - Tests concurrent bookmark and notes mutations, verifying correct vector clock progression and state digest generation.
6. **Minor PII Shield on Public Talent Passports**:
   - Asserts `get_passport_by_handle` masks phone, email, and address on recruiter view while keeping authentic CAT $\theta$ and verified skill badges.
   - Asserts authenticated student view retains personal details.
7. **Cryptographic QR Signature Verification**:
   - Validates authentic signature matches; asserts tampered signatures return `False`.
