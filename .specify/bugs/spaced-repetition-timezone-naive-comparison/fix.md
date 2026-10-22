# Bug Fix: Spaced Repetition Due Date Timezone-Aware vs Naive Comparison

- **Slug**: `spaced-repetition-timezone-naive-comparison`
- **Applied**: 2026-10-14
- **Component**: `backend/app/services/spaced_repetition_service.py`

## 1. Remediation Applied
1. In `SpacedRepetitionService.record_review`:
   - If `review_timestamp` is provided and offset-naive (`now.tzinfo is None`), it is safely converted to UTC (`now.replace(tzinfo=timezone.utc)`).
2. In `SpacedRepetitionService.get_due_reviews`:
   - Both `target_time` and `due_at` are normalized to UTC-aware datetimes before performing the `due_at <= target_time` comparison, eliminating `TypeError: can't compare offset-naive and offset-aware datetimes`.

## 2. Verification Plan
- Unit test in `backend/tests/test_phase16_spaced_repetition_and_study_plan.py`:
  - Test calling `get_due_reviews` passing both timezone-naive `datetime` and timezone-aware `datetime(timezone.utc)`.
  - Assert both comparisons execute without raising exceptions.
