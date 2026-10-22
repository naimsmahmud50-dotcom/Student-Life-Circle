# Bug Fix: Rate Limiter Empty Window Guard & Nested Minor PII Sanitization

- **Slug**: `offline-sync-empty-window-and-nested-pii`
- **Fixed**: 2026-10-14
- **Remediated Files**:
  - `backend/app/core/rate_limiter.py`
  - `backend/app/core/security_headers.py`
  - `backend/app/services/offline_sync_service.py`

## 1. Summary of Changes
1. **SlidingWindowRateLimiter (`rate_limiter.py`)**:
   - Guarded empty `valid_timestamps` with fallback to current time, preventing `IndexError` when `limit <= 0` or during instant lockdown policies.
2. **SecurityHeadersManager (`security_headers.py`)**:
   - Added recursive sanitization for nested dictionaries (`location`, `contact_details`), ensuring street-level PII (`address_line`, `house`, `road`, `street`, `mobile`) is masked with `[REDACTED_MINOR_PRIVACY_PROTECTED]` under ASVS L2.
3. **OfflineSyncService (`offline_sync_service.py`)**:
   - Added polymorphic object normalization supporting both raw dictionary payloads and validated BaseDTO / Pydantic instances.

## 2. Verification & Regression Tests
Added comprehensive test cases in `backend/tests/test_phase14_security_and_offline_sync.py` covering:
- Auth rate limit exhaustion (5th attempt permitted, 6th attempt blocked with retry-after > 0).
- Answer save throttling (60 saves allowed per minute, 61st throttled).
- Security headers verification (CSP, HSTS, X-Frame-Options DENY).
- Nested minor PII redaction for unauthorized requesters and full visibility for authorized guardians.
- Offline practice bundle generation with correct answer masking (anti-cheating).
- Offline batch answer sync with duplicate idempotency skip.
