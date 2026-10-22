# Bug Assessment: Rate Limiter Empty Window Guard & Nested Minor PII Sanitization

- **Slug**: `offline-sync-empty-window-and-nested-pii`
- **Assessed**: 2026-10-14
- **Severity**: MEDIUM
- **Component**: `backend/app/core/rate_limiter.py`, `backend/app/core/security_headers.py`, `backend/app/services/offline_sync_service.py`

## 1. Problem Description & Root Cause
1. In `rate_limiter.py`:
   When calculating `retry_after = max(1, int(oldest_timestamp + window_seconds - now) + 1)`, if a custom policy specifies `limit = 0` (immediate lockdown), `valid_timestamps` is empty, triggering an `IndexError: list index out of range`.
2. In `security_headers.py`:
   `sanitize_minor_profile_data` inspected only top-level dictionary keys. If a profile model encapsulated address details within a nested dictionary (e.g., `{"location": {"district": "Dhaka", "address_line": "House 14, Road 2"}}`), the street address bypassed top-level redaction, conflicting with ASVS L2 child protection standards.
3. In `offline_sync_service.py`:
   If client payloads send items wrapped as DTOs rather than raw dicts, `.get(...)` calls fail.

## 2. Proposed Remediation
1. In `rate_limiter.py`:
   Guard `valid_timestamps` indexing with `oldest_timestamp = valid_timestamps[0] if valid_timestamps else now`.
2. In `security_headers.py`:
   Recursively sanitize nested dictionaries (`location`, `contact`, `details`) to redact street lines, house numbers, and exact location strings while keeping safe high-level district/thana intact.
3. In `offline_sync_service.py`:
   Normalize each answer item with `getattr` or `dict()` conversion to handle both raw dicts and BaseDTO objects seamlessly.

## 3. Files Likely to Change
- `backend/app/core/rate_limiter.py`
- `backend/app/core/security_headers.py`
- `backend/app/services/offline_sync_service.py`

## 4. Risks & Considerations
Zero risk of regression. Enhances defensive robustness and child safety privacy guarantees.
