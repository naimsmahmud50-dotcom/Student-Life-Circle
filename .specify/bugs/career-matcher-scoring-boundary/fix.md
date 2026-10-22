# Bug Fix: Career Matcher Negative Badges Clamping & Interview Empty Answer Guard

- **Slug**: `career-matcher-scoring-boundary`
- **Fixed**: 2026-10-14
- **Component**: `backend/app/services/career_matcher_service.py`, `backend/app/services/interview_coach_service.py`

## 1. Summary of Changes
1. **`CareerMatcherService`**:
   - Clamped `safe_badges = max(0, int(verified_badges_count))` and `safe_mastery = max(0.0, min(100.0, float(quiz_mastery_pct)))`, guaranteeing that negative inputs cannot corrupt calculation of match scores.
   - Filtered out whitespace and empty skill tokens during normalization.
2. **`InterviewCoachService`**:
   - Added explicit boundary check on `answer_text` to verify non-empty string before evaluation and reject empty strings with a friendly Bengali message.

## 2. Verification
Regression test suite in `backend/tests/test_phase20_interview_and_career_matcher.py` verifies:
- Career fit analysis handles negative badges count without negative score penalty.
- Interview coach rejects empty/whitespace answer submissions.
- Full test suite passes with zero regressions.
