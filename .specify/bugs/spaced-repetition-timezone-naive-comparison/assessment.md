# Bug Assessment: Spaced Repetition Due Date Timezone-Aware vs Naive Comparison

- **Slug**: `spaced-repetition-timezone-naive-comparison`
- **Assessed**: 2026-10-14
- **Severity**: MEDIUM
- **Component**: `backend/app/services/spaced_repetition_service.py`

## 1. Problem Description & Root Cause
In `SpacedRepetitionService.get_due_reviews(student_id, as_of_time)`:
- `item["next_due_at"]` is generated with `datetime.now(timezone.utc).isoformat()`, which is a timezone-aware ISO string.
- If a caller (such as a unit test, background worker, or client payload) passes an offset-naive datetime object for `as_of_time` (e.g., `datetime(2026, 10, 20)` or `datetime.utcnow()`), the comparison `due_at <= target_time` raises `TypeError: can't compare offset-naive and offset-aware datetimes`.

## 2. Proposed Remediation
1. In `SpacedRepetitionService.get_due_reviews`:
   - Standardize `target_time`: if `target_time.tzinfo is None`, apply `target_time = target_time.replace(tzinfo=timezone.utc)`.
   - Standardize `due_at`: if `due_at.tzinfo is None`, apply `due_at = due_at.replace(tzinfo=timezone.utc)`.
2. In `record_review`:
   - If `review_timestamp` is provided and offset-naive, automatically convert to UTC timezone-aware.

## 3. Files Likely to Change
- `backend/app/services/spaced_repetition_service.py`

## 4. Risks & Considerations
Zero risk of regression. Normalizes all datetimes to UTC, guaranteeing safe comparisons across different caller environments.
