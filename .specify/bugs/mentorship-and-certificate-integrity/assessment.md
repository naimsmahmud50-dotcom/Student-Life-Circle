# Bug Assessment: Mentorship Double-Booking & Certificate Non-Malleability Integrity

## Scope & Vulnerability Surface
- **Module**: `AlumniMentorshipService` & `CertificateVerificationService`
- **Standards Applied**: OWASP ASVS L2, `/strix-source-aware-whitebox`, `/speckit-bug-fix`

### 1. Identified Candidate Vulnerability A: Slot Reservation Race Condition
- **Observation**: In high-demand mentorship booking (e.g. 15 minutes before BUET admission exam announcement), concurrent booking requests could attempt to reserve the identical calendar slot if read-then-write checks are non-atomic.
- **Impact**: Double-booking causes calendar collision, duplicate escrow fee capture, and degraded student-mentor trust.
- **Mitigation Requirement**: Thread-safe atomic lock (`self._lock`) with pre-check and immediate slot eviction before session record synthesis.

### 2. Identified Candidate Vulnerability B: Certificate Hash Malleability
- **Observation**: If certificate signature hashes are formed with simple concatenated strings without delimiters or secret entropy, delimiter collision attacks could allow forging identical hashes across different student names/courses.
- **Impact**: Dishonest actors could falsify academic accreditation certificates on employer verification gateways.
- **Mitigation Requirement**: Canonical pipe-delimited encoding with internal platform salt:
  `sha256(student_id + "|" + student_name + "|" + course + "|" + grade + "|" + timestamp + "|" + SALT)`
  and verification-time regeneration with discrepancy detection (`tamper_detected`).
