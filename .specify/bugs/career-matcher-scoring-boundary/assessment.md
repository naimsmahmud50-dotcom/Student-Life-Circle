# Bug Assessment: Career Matcher Negative Badges Clamping & Interview Empty Answer Guard

- **Slug**: `career-matcher-scoring-boundary`
- **Assessed**: 2026-10-14
- **Severity**: MEDIUM
- **Component**: `backend/app/services/career_matcher_service.py`, `backend/app/services/interview_coach_service.py`

## 1. Problem Description & Root Cause
1. **Career Matcher Negative Badges Clamping**:
   - In `CareerMatcherService.analyze_career_fit`, if `verified_badges_count` is provided as a negative integer (e.g. `-3`), the bonus multiplier calculation reduces candidate score below zero.
2. **Empty Skills List Normalization**:
   - If `candidate_skills` contains whitespace-only entries, normalization may create redundant iterations.

## 2. Proposed Remediation
1. **In `CareerMatcherService.analyze_career_fit`**:
   - Clamp `safe_badges = max(0, int(verified_badges_count))` before applying the bonus weight formula.
2. **In `InterviewCoachService.submit_interview_answer`**:
   - Ensure explicit guard against empty or whitespace-only answers.

## 3. Files to Change
- `backend/app/services/career_matcher_service.py`
- `backend/app/services/interview_coach_service.py`

## 4. Risks & Considerations
Zero risk. Strengthens mathematical boundary guarantees and eliminates negative score anomalies.
