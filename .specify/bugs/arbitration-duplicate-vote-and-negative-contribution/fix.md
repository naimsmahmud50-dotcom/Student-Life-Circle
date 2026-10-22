# Bug Fix: Arbitration Duplicate Vote Guard & Study Circle Negative Contribution

- **Slug**: `arbitration-duplicate-vote-and-negative-contribution`
- **Fixed**: 2026-10-14
- **Component**: `backend/app/services/arbitration_service.py`, `backend/app/services/study_circle_service.py`

## 1. Summary of Changes
1. **`ArbitrationTribunalService`**:
   - Added validation for allowed verdicts: `ALLOWED_VERDICTS = {"CORRECT_KEY", "QUARANTINE", "DISMISS"}`.
   - Guarded against duplicate voting: rejected calls if `sme_id` already exists in `case["votes"]`.
   - Handled deadlock resolution: if the highest vote count is `< 2`, default ruling to `DISMISSED` due to lack of quorum consensus.
2. **`StudyCircleService`**:
   - Added positive integer guard in `contribute_questions`: rejected `questions_solved <= 0` with Bengali validation message.

## 2. Verification
Regression test suite in `backend/tests/test_phase17_study_circle_and_arbitration.py` verifies:
- Duplicate votes from the same SME arbitrator are rejected.
- Invalid verdicts are rejected.
- Negative or zero practice question contributions are rejected.
- Split vote deadlock gracefully resolves with integrity.
- All 76+ test cases pass cleanly.
