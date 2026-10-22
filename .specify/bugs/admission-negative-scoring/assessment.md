# Bug Assessment: Admission Negative Marking Score Clamping

- **Slug**: `admission-negative-scoring`
- **Assessed**: 2026-10-14
- **Severity**: HIGH
- **Component**: `backend/app/services/quiz_engine.py` (line 268)

## 1. Problem Description & Root Cause
In `QuizEngineService.submit_and_score`, line 268 previously computed:
```python
raw_score = round(max(0.0, raw_score), 2)
```
For `MOCK_EXAM` and `LIVE_CHALLENGE` modes where high-stakes Bangladeshi admission rules apply (e.g., Dhaka University Unit-A, Medical MBBS), incorrect answers deduct 0.25 marks per mistake. If a student answers 2 questions correctly (+2.0) and 12 questions incorrectly (-3.0), their true net score is `-1.0`.

Clamping with `max(0.0, ...)` masks the actual negative penalty, leading to distorted rank calculations and giving candidates false confidence about their negative marking risk.

## 2. Proposed Remediation
1. In `submit_and_score`:
   - For `mode == QuizMode.MOCK_EXAM` or `mode == QuizMode.LIVE_CHALLENGE`: Allow true negative scores (do not clamp to 0.0).
   - For `mode == QuizMode.ANYTIME_PRACTICE`: Maintain non-negative floor (`max(0.0, raw_score)`) if configured without negative marking.
2. Add regression test in `backend/tests/test_phase11_content_pipeline.py` verifying that admission mock tests accurately record true negative net scores (e.g. -1.0) and do not clamp.

## 3. Files Likely to Change
- `backend/app/services/quiz_engine.py`
- `backend/tests/test_phase11_content_pipeline.py`

## 4. Risks & Considerations
Minimal blast radius. Existing practice tests with `negative_marking=0.0` will remain non-negative.
