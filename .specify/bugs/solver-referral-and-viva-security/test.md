# Verification Report: Math Solver, Alumni Referral & Voice Viva Security

## Test Suite Execution
- **File**: `backend/tests/test_phase31_solver_referral_and_viva.py`
- **Methodology**: Automated Unit & Integration testing under Python `unittest`.

### Verification Matrix
1. **Math Solver Stepwise Derivation & Sanity**:
   - Asserts canonical calculus product rule derivation generates 3 distinct steps with applied rules.
   - Asserts integration by parts problem produces accurate mathematical steps.
   - Asserts generic expressions are sanitized without invoking code evaluation.
2. **Intermediate Misconception Diagnostics**:
   - Tests detection of `CHAIN_RULE_OMISSION` and `SIGN_INVERSION` in student-submitted intermediate steps.
   - Asserts Socratic hint delivery without leaking final answer.
3. **Alumni Directory & Quota Enforcement**:
   - Asserts listing alumni by company filter works as expected.
   - Asserts creating a referral increments alumni referral count and returns HMAC-sealed token.
   - Asserts duplicate referral for same company by same student is rejected with `ValueError`.
   - Asserts exceeding `max_monthly_referrals` raises `ValueError`.
4. **Cryptographic Referral Verification**:
   - Asserts genuine token is verified as `AUTHENTIC`.
   - Asserts tampered token is rejected as `TAMPERED_SIGNATURE` or `INVALID_FORMAT`.
5. **Viva-Voce Speech Telemetry & WPM Cadence**:
   - Tests `start_session` initializes session record with domain questions.
   - Tests `evaluate_response` handles normal, hesitant, rushed, and zero-duration audio inputs without crash.
   - Asserts session summary aggregates fluency and precision scores.
6. **Section 30 REST Endpoints**:
   - Asserts all 8 async router endpoints respond with correct status codes and payloads.
