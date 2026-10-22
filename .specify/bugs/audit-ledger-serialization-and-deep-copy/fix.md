# Bug Fix: Audit Ledger Non-Primitive JSON Serialization & In-Memory Payload Mutation

- **Slug**: `audit-ledger-serialization-and-deep-copy`
- **Applied**: 2026-10-14
- **Component**: `backend/app/core/audit_ledger.py`

## 1. Remediation Applied
1. **Added `default=str` to `_canonical_json`**:
   Ensures any non-primitive data types (such as `datetime`, `UUID`, or custom domain objects) included in audit event payloads are deterministically converted to strings without raising a `TypeError`.
2. **Deep-Copied Payload in `AuditBlock` and `to_dict()`**:
   Imported standard `copy` module and enforced `copy.deepcopy(payload)` during block instantiation and in `to_dict()`. This eliminates shared dictionary reference vulnerabilities and prevents accidental in-memory modifications from triggering false-positive tamper alerts.

## 2. Verification Plan
- Unit test in `backend/tests/test_phase15_audit_and_credentials.py`:
  - Test recording events with complex payloads (`datetime`, `UUID`).
  - Test mutating the dictionary returned by `to_dict()` and verifying `audit_ledger.verify_integrity()` still returns `(True, None, ...)` without corruption.
  - Test intentional block tampering to verify tamper detection accurately isolates the corrupted block index.
