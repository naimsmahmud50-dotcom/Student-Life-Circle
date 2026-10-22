# Bug Fix Specification: Collision Guards, Idempotent CRDT Reconciler & Minor PII Shield

## Applied Remediations

### 1. University Admission Multiplexer Collision Guard
- Implemented `detect_schedule_conflicts(university_codes)` mapping date strings to exam slots.
- When conflicts are found during batch application, they are captured in `conflicts_detected` without discarding non-conflicting applications.
- Enforced strict input validation rejecting empty or unknown university codes with `ValueError`.

### 2. Idempotent CRDT Reconciler & Vector Clock Monotonicity
- Introduced `_applied_mutations` in `OfflineDeltaSyncService` tracking previously applied `mutation_id` sets.
- Re-sent mutations are safely identified and skipped (`applied_count = 0`), returning status `IDEMPOTENT_NOOP`.
- Vector clock updates are strictly monotonic: `current_server_clock = max(current_server_clock, client_clock) + 1`.
- State digest computed deterministically via canonical JSON string serialization hashed with SHA-256.

### 3. Talent Passport Minor PII Redaction Shield
- Implemented strict separation between authenticated student view (`is_recruiter_view=False`) and public recruiter view (`is_recruiter_view=True`).
- On recruiter view:
  - Phone masked to `"PROTECTED: Recruiter Direct Messaging Gateway Enabled"`.
  - Email masked to `"VERIFIED: Recruiter In-App Communication Relay"`.
  - Address masked to `"REDACTED: Bangladesh Division Verified"`.
- Non-malleable HMAC/SHA-256 digital signature binds student identity, handle, and CAT ability score $\theta$ with secret salt.
