# Bug Assessment: Backend API Error & Message English Standardization

## 1. Problem Description
During whitebox static code analysis of `backend/app/api/v1/router.py`, residual localized strings in Bengali were identified across multiple API response messages, error details, and query parameter descriptions:
- Multiple endpoints (e.g., focus sprint completion, CAT answer evaluation, study circle contributions, arbitration tribunal cases, and predictive analytics) emitted Bengali error descriptions such as `"ফোকাস স্প্রিন্ট সম্পন্নকরণে ত্রুটি।"` or `"ক্যাট উত্তর মূল্যায়নে ত্রুটি।"`.
- This violates the platform's architectural mandate: 100% English UI Chrome and API contracts across all endpoints, documentation, metrics, and error codes.
- Only educational question stems/options are permitted to adapt dynamically to student language preferences.

---

## 2. Root Cause Analysis
Earlier development phases introduced localized Bengali messages directly within exception handlers and standard API envelope messages in `backend/app/api/v1/router.py`. While the frontend UI was standardized in Phase 23, the backend exception detail messages remained in Bengali.

---

## 3. Remediation Strategy
1. Perform a comprehensive sweep across `backend/app/api/v1/router.py` to replace all Bengali exception `detail` strings and response `message` fields with clear, professional English equivalents.
2. Standardize error codes to machine-readable SCREAMING_SNAKE_CASE (e.g., `FOCUS_SPRINT_COMPLETION_ERROR`, `CAT_SESSION_NOT_FOUND`, `TRIBUNAL_VOTE_FAILED`).
3. Add a dedicated test assertion in `backend/tests/test_ui_language_architecture.py` verifying that `router.py` contains zero non-English strings in its exception handlers and route responses.
