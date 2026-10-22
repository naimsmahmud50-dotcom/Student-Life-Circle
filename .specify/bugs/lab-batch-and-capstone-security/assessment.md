# Bug Assessment: Circuit Singularities, Escrow Rounding Drift & Milestone URL Injection

## Scope & Vulnerability Surface
- **Modules**: `VirtualScienceLabService`, `CoachingBatchPoolService`, `IndustryCapstoneService`
- **Standards Applied**: OWASP ASVS L2, `/strix-source-aware-whitebox`, `/speckit-bug-fix`

### 1. Candidate Vulnerability A: Circuit Simulator Zero-Resistance Short Circuit Singularity
- **Observation**: If a user submits a series or parallel circuit with 0 Ohm resistance (pure wire or closed switch without loads), Ohm's law $I = V / R$ triggers a `ZeroDivisionError` (500 Internal Server Error).
- **Impact**: Server crash, unhandled exceptions, and potential Denial of Service (DoS) via crafted zero-impedance payloads.
- **Mitigation Requirement**: Mandatory defensive floor clamping: `total_resistance = max(raw_total_r, 0.001)`. Explicitly flag `is_short_circuit_safe = False` and set `execution_status = "WARNING_SHORT_CIRCUIT"` when resistance drops below 0.05 Ohms.

### 2. Candidate Vulnerability B: Geometric Optics Focal Singularity Handling
- **Observation**: When object distance equals focal length ($u = f$) for a convex thin lens, the lens equation $1/v = 1/f - 1/u$ results in division by zero ($u - f = 0$), where the image forms at optical infinity.
- **Impact**: Floating-point exception or unhandled crash when calculating image coordinates and magnification.
- **Mitigation Requirement**: Exact focal boundary detection `abs(u - f) < 1e-4`. Return `image_nature = "AT_INFINITY"`, `image_distance_cm = None`, and `is_at_focus = True` with parallel ray coordinates instead of raising an arithmetic error.

### 3. Candidate Vulnerability C: Fractional Escrow Rounding Drift Leaks
- **Observation**: When $N$ guardians split a monthly tutoring fee (e.g. 5,000 BDT split across 3 guardians = 1666.6666... BDT per guardian), naive floating-point division or rounding can lose or generate fractions of cents (3 * 1666.67 = 5000.01 or 3 * 1666.66 = 4999.98), creating an accounting imbalance in the escrow vault.
- **Impact**: Escrow vault balance reconciliation leaks over time across hundreds of active neighborhood coaching batches.
- **Mitigation Requirement**: Exact cent reconciliation: calculate `remainder_drift = round(total_fee - (base_split * n), 2)` and allocate the discrepancy to the lead guardian (index 0). Asserts that $\sum \text{allocated\_amount\_bdt} \equiv \text{total\_monthly\_fee\_bdt}$ without exception.

### 4. Candidate Vulnerability D: Capstone Milestone URL Scheme SSRF & Protocol Smuggling
- **Observation**: When students submit milestone code repositories, accepting arbitrary strings or pseudo-protocols (`file://`, `javascript:`, `data:`, or `gopher://`) could expose internal services or enable stored XSS/SSRF in recruiter dashboards.
- **Impact**: Internal network probing, server-side request forgery, or stored cross-site scripting in employer admin portals.
- **Mitigation Requirement**: Strict protocol allowlist: submissions must start with `https://`, `http://`, or `git://`. Reject any untrusted or malformed URIs with descriptive `ValueError`.
