# Bug Fix: Admission Negative Marking Score Clamping

- **Slug**: `admission-negative-scoring`
- **Fixed**: 2026-10-14T12:05:00Z
- **Assessment**: ./assessment.md
- **Status**: applied

## Summary

Removed artificial `max(0.0, raw_score)` floor for competitive admission mocks and live challenges with negative marking. Candidates who accumulate more penalties than correct answers will now see their true negative net score (e.g. -0.50), reflecting actual university admission standards (DU/Medical/BUET). Standard practice tests remain non-negative.

## Changes

| File | Change | Notes |
|------|--------|-------|
| `backend/app/services/quiz_engine.py` | modified | Added `is_competitive` check allowing negative score for MOCK_EXAM and LIVE_CHALLENGE |
| `backend/tests/test_phase11_content_pipeline.py` | added test | `test_03_admission_mock_true_negative_score` locks down regression prevention |

## Diff Highlights

```python
# For competitive admission mock and live challenge modes, reflect true negative score
is_competitive = attempt.get("mode") in (QuizMode.MOCK_EXAM, QuizMode.LIVE_CHALLENGE) and negative_val > 0.0
final_score = round(raw_score, 2) if is_competitive else round(max(0.0, raw_score), 2)
```

## Tests Added or Updated

- `backend/tests/test_phase11_content_pipeline.py::test_03_admission_mock_true_negative_score` — Asserts that 1 correct (+1.0) and 8 wrong (-2.0) with -0.25 penalty yields `-1.0` in `QuizMode.MOCK_EXAM`.

## Local Verification

- Commands run: `PYTHONPATH=. python3 -m unittest discover -s backend/tests -p "test_*.py"` → 35/35 tests passing in 0.14s.
- Verified that anytime practice without negative marking still never falls below 0.0.

## Deviations from Assessment

None. The remediation directly implemented the proposed conditional negative scoring logic.

## Follow-ups

- Surface negative score highlight in the admission diagnostic view so students are alerted to excessive guessing habits.
