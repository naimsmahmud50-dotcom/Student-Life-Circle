# Bug Fix Specification: Expression Sanitization, Cryptographic HMAC Seals & Telemetry Guardrails

## Applied Remediations

### 1. Math Expression Sanitization & Deterministic Rule Engine
- Implemented `_sanitize_expression(text)` stripping non-math punctuation `[;`$<>{}|\\]`.
- Fully eliminated any usage of `eval`, `exec`, or dynamic bytecode compilation.
- Pattern matching against verified canonical problem blueprints ensures non-malleable, textbook-accurate step derivations.

### 2. Cryptographic HMAC-SHA256 Referral Token Seals & Quota Locks
- Implemented HMAC-SHA256 signature generator:
  `hmac.new(SALT, f"{alumni_id}:{student_id}:{company}:{timestamp}", sha256).hexdigest()`.
- Referral token structure: `AGROREF|<referral_id>|<signature[:16]>`.
- Verification endpoint validates the exact HMAC signature before acknowledging authenticity to employers.
- Enforced atomic check `alumni["active_referrals_count"] >= alumni["max_monthly_referrals"]` raising `ValueError` on quota exhaustion.
- Enforced per-student single referral constraint per company preventing duplicate spam.

### 3. Speech Telemetry Clamping & Zero-Division Shield
- Implemented bounded duration calculation in `evaluate_response`:
  `duration_min = max(audio_duration_seconds / 60.0, 0.1)`.
- WPM cadence safely categorized into `OPTIMAL` (110-165 WPM), `HESITANT` (<110 WPM), or `TOO_RUSHED` (>165 WPM).
- Bounded response latency scoring ensuring resilient calculations regardless of client network jitter.
