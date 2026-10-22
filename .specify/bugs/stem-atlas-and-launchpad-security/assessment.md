# Bug Assessment: Chemical Parser ReDoS, Sybil Vote Tampering & Escrow Tranche Race Conditions

## Scope & Vulnerability Surface
- **Modules**: `MolecularGeometryLabService`, `SyllabusKnowledgeAtlasService`, `InnovationLaunchpadService`
- **Standards Applied**: OWASP ASVS L2, `/strix-source-aware-whitebox`, `/speckit-bug-fix`

### 1. Candidate Vulnerability A: Chemical Formula Parsing ReDoS & Unbounded Strings
- **Observation**: If molecular formula inputs are matched with unanchored or complex nested regular expressions, attackers could provide adversarial payloads causing catastrophic catastrophic backtracking (Regular Expression Denial of Service).
- **Impact**: CPU exhaustion, server event loop blocking, and denial of service.
- **Mitigation Requirement**: Strict sanitization with character stripping `re.sub(r"[^A-Za-z0-9]", "", formula)` and hard length limit (`<= 30` characters) prior to parsing.

### 2. Candidate Vulnerability B: Sybil Attack & Vote Flooding in Innovation Tribunal
- **Observation**: In community voting for micro-grants, fraudulent accounts or automated scripts could cast thousands of votes for a specific venture, skewing fund allocation away from deserving student innovators.
- **Impact**: Fraudulent grant distribution, loss of student community trust, and grant capital leakage.
- **Mitigation Requirement**: Atomic per-student project vote locking using composite indexing `f"{project_id}:{voter_student_id}"` raising `ValueError` on duplicates. Dynamic reputation weight clamping `[0.5x, 3.0x]` based on verified CAT ability and academic reputation.

### 3. Candidate Vulnerability C: Grant Escrow Double-Disbursement & Out-of-Order Release
- **Observation**: Micro-grant escrow funds (up to 100,000 BDT) are disbursed in tranches (30%, 40%, 30%). If concurrent HTTP requests arrive or if milestone progression is skipped, the platform escrow vault could be double-drained.
- **Impact**: Irreversible loss of venture capital, premature grant release without prototype verification.
- **Mitigation Requirement**: Mandatory stage progression verification (`PROPOSAL_VALIDATION` -> `PROTOTYPE_DEMO` -> `PILOT_DEPLOYMENT`), duplicate stage release locks, and remaining balance tracking.

### 4. Candidate Vulnerability D: Untrusted Project Repository URL Protocol Smuggling
- **Observation**: Student pitch submissions accepting arbitrary URLs could allow internal network SSRF (`http://169.254.169.254` or `file:///etc/passwd`) or client-side XSS (`javascript:alert(1)`).
- **Impact**: Server metadata leakage or cross-site scripting in admin/mentor review dashboards.
- **Mitigation Requirement**: Strict scheme validation requiring `https://`, `http://`, or `git://` prefixes.
