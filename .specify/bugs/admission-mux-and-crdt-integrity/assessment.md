# Bug Assessment: Admission Multiplexer Collisions, CRDT Mutation Replay & Minor PII Shield

## Scope & Vulnerability Surface
- **Modules**: `UniversityAdmissionMultiplexerService`, `OfflineDeltaSyncService`, `StudentTalentPassportService`
- **Standards Applied**: OWASP ASVS L2, `/strix-source-aware-whitebox`, `/speckit-bug-fix`

### 1. Candidate Vulnerability A: Schedule Clash in Batch University Applications
- **Observation**: Students applying to multiple universities in Bangladesh frequently encounter overlapping entrance test schedules (e.g. DU Ka-Unit vs Medical or BUET vs Engineering cluster). Submitting blind batch payments for conflicting exam slots leads to financial loss and missed exams.
- **Impact**: Financial waste and severe student distress.
- **Mitigation Requirement**: Real-time cross-circular schedule collision detection in `detect_schedule_conflicts` and explicit conflict warnings embedded in batch application receipts.

### 2. Candidate Vulnerability B: CRDT Offline Mutation Replay & Clock Drift
- **Observation**: In intermittent 2G networks, network retries can send the identical mutation batch multiple times, or manipulated client clocks can cause inconsistent state reconciliation.
- **Impact**: Duplicate answers, corrupted study notes, and erratic bookmark states.
- **Mitigation Requirement**: Idempotent deduplication via unique `mutation_id` tracking, monotonic server vector clock bounding, and SHA-256 state digest verification.

### 3. Candidate Vulnerability C: Unauthenticated Minor PII Exposure via Public Talent Passports
- **Observation**: Talent passports are intended to be shared publicly with recruiters and employers. If the public endpoint returns raw student records, minors' phone numbers, residential addresses, and exact emails are exposed to scrapers and bad actors.
- **Impact**: Privacy violations, minor exploitation, and regulatory non-compliance with data protection guidelines.
- **Mitigation Requirement**: Architectural Minor PII Redaction Shield on recruiter views (`is_recruiter_view=True`) masking residential address, direct phone number, and personal email while exposing verified competencies, CAT $\theta$, and relay-based communication channels.
