# Bug Assessment: Psychometrics & Guardian Service Interface Alignment

- **Slug**: `psychometrics-guardian-interface-mismatch`
- **Assessed**: 2026-10-14
- **Severity**: HIGH
- **Component**: `backend/app/services/psychometrics_service.py`, `backend/app/services/guardian_service.py`, `backend/app/api/v1/router.py`

## 1. Problem Description & Root Cause
During cross-artifact `/speckit-analyze` between `backend/app/api/v1/router.py` and the newly authored Phase 12 services:
1. `router.py` invoked `psychometrics_service.get_recommended_difficulty_band(student_id)` to deliver the learner's Zone of Proximal Development (ZPD), but the method was not implemented on the `PsychometricsService` class, resulting in an `AttributeError` when queried.
2. In `psychometrics_service.calculate_expected_probability`, `math.pow(10.0, diff)` lacked boundary clamping on `diff`, risking an `OverflowError: math range error` on extreme uncalibrated Elo differentials.
3. `guardian_service.py` defined `co_sign_tuition_request` and `get_guardian_progress_summary`, whereas `router.py` called `record_tuition_co_signature` and `get_minor_guardian_overview`. Furthermore, guardian notes from the payload were not preserved.

## 2. Proposed Remediation
1. In `backend/app/services/psychometrics_service.py`:
   - Implement `get_recommended_difficulty_band(student_id) -> Dict[str, Any]` returning `min_difficulty`, `max_difficulty`, `target_difficulty`, and `target_probability_band`.
   - Add mathematical clamping on `diff` in `calculate_expected_probability` to `[-10.0, 10.0]`.
2. In `backend/app/services/guardian_service.py`:
   - Add alias / primary implementation for `record_tuition_co_signature` with `guardian_notes` support.
   - Add alias / primary implementation for `get_minor_guardian_overview`.
3. In `backend/tests/test_phase12_psychometrics_and_guardian.py`:
   - Add rigorous regression tests verifying that all psychometrics, guardian safety, and dispute methods resolve cleanly via both direct service calls and API router invocations.

## 3. Files Likely to Change
- `backend/app/services/psychometrics_service.py`
- `backend/app/services/guardian_service.py`
- `backend/tests/test_phase12_psychometrics_and_guardian.py`

## 4. Risks & Considerations
Zero breaking changes. Enhances stability and closes all interface divergences.
