# Bug Fix: Psychometrics & Guardian Service Interface Alignment

- **Slug**: `psychometrics-guardian-interface-mismatch`
- **Fixed**: 2026-10-14
- **Remediated Files**:
  - `backend/app/services/psychometrics_service.py`
  - `backend/app/services/guardian_service.py`

## 1. Summary of Changes
1. **PsychometricsService:**
   - Implemented `get_recommended_difficulty_band(student_id)`:
     - Calculates optimal cognitive flow zone (Zone of Proximal Development, 60%–75% challenge band).
     - Returns `min_difficulty`, `max_difficulty`, `target_difficulty`, and `target_probability_band`.
   - Enhanced `calculate_expected_probability`:
     - Added clamping on exponent `clamped_diff = max(-10.0, min(10.0, diff))` to prevent `math.pow` range errors during large Elo differentials.
2. **GuardianService:**
   - Implemented primary `record_tuition_co_signature` matching router signatures, with full support for `guardian_notes`.
   - Implemented primary `get_minor_guardian_overview` matching router queries.
   - Maintained backward-compatible aliases for `co_sign_tuition_request` and `get_guardian_progress_summary`.

## 2. Verification & Regression Lockdown
Created comprehensive automated tests in `backend/tests/test_phase12_psychometrics_and_guardian.py` covering:
- Elo rating calibration and ZPD band retrieval.
- Math overflow safety under extreme Elo differences (+5000 / -5000).
- Streak freeze Rest Day passes and comeback boost multiplier (+25%).
- Minor pairing code generation, guardian account linkage, and token invalidation.
- Guardian tuition co-signature with notes and permission gating.
- Minor privacy overview verification.
- In-app learner question dispute reporting, duplicate prevention, and moderator resolution with bounty award.
