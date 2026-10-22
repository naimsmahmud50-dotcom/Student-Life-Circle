# Bug Assessment: Audit Ledger Non-Primitive JSON Serialization & In-Memory Payload Mutation

- **Slug**: `audit-ledger-serialization-and-deep-copy`
- **Assessed**: 2026-10-14
- **Severity**: MEDIUM
- **Component**: `backend/app/core/audit_ledger.py`

## 1. Problem Description & Root Cause
1. **Serialization TypeError with Non-Primitive Types**:
   In `_canonical_json(data)`, `json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)` is used without a fallback serializer. If audit events include Python `datetime` objects, `UUID` instances, or custom classes in their `payload` dictionary, `json.dumps` raises `TypeError: Object of type ... is not JSON serializable`, halting the audit logging pipeline.
2. **In-Memory Payload Mutation Risk**:
   `AuditBlock.to_dict()` returned `self.payload` directly by reference. If a service or controller subsequently mutated the returned dictionary (e.g., adding a temporary view field), the internal state of the `AuditBlock` would be altered in memory, causing subsequent `verify_integrity()` calls to compute a mismatched hash and falsely report a compromised audit ledger.

## 2. Proposed Remediation
1. Update `_canonical_json` in `backend/app/core/audit_ledger.py` to include `default=str`, ensuring all datetime, UUID, and complex objects are deterministically converted to strings.
2. In `AuditBlock.to_dict()`, return a `copy.deepcopy(self.payload)` to guarantee absolute immutability of recorded audit blocks against downstream caller modifications.

## 3. Files Likely to Change
- `backend/app/core/audit_ledger.py`

## 4. Risks & Considerations
Zero risk of regression. Ensures uninterrupted audit logging across diverse payload types and fortifies mathematical integrity verification.
