# Bug Assessment: Math Expression Injection, Referral Token Malleability & Viva Telemetry Bounds

## Scope & Vulnerability Surface
- **Modules**: `MathProblemSolverService`, `AlumniReferralNetworkService`, `VoiceVivaSimulatorService`
- **Standards Applied**: OWASP ASVS L2, `/strix-source-aware-whitebox`, `/speckit-bug-fix`

### 1. Candidate Vulnerability A: Math Expression Parser Injection
- **Observation**: If math expressions or LaTeX strings submitted by users are processed with dynamic code execution (`eval`, `exec`, or unsafe AST parsing), attackers could trigger remote code execution.
- **Impact**: Server compromise, data exfiltration, and host sandbox escape.
- **Mitigation Requirement**: Zero reliance on `eval()` or `exec()`. Mathematical expressions must be tokenized, sanitized with character boundary filters, and resolved against deterministic analytical derivation rules.

### 2. Candidate Vulnerability B: Referral Forgery, Quota Bypasses & Double-Endorsement
- **Observation**: Corporate employers trust alumni referrals for fast-track hiring. If referral tokens are predictable or lack HMAC authentication, students could forge endorsements. Concurrency race conditions could also allow exceeding an alumni's monthly referral quota.
- **Impact**: Fake employee endorsements, recruiter trust collapse, and spamming hiring partners.
- **Mitigation Requirement**: HMAC-SHA256 cryptographic signatures binding alumni ID, student ID, target company, and issue timestamp with internal secret salt. Thread-safe atomic checking of monthly referral quotas and per-student company locks.

### 3. Candidate Vulnerability C: Zero Audio Duration Division by Zero in Speech Cadence
- **Observation**: In intermittent networks, an audio submission with `audio_duration_seconds = 0` or negative latency could trigger a `ZeroDivisionError` during Words-Per-Minute (WPM) calculation.
- **Impact**: Unhandled server exceptions (500 Internal Server Error) and denial of service.
- **Mitigation Requirement**: Defensive clamping: `duration_min = max(audio_duration_seconds / 60.0, 0.1)` and bounded latency scoring.
