# Bug Fix Specification: Formula Sanitization, Anti-Sybil Locks & Tranche Disbursal Guards

## Applied Remediations

### 1. Chemical Formula Length Clamping & Non-Backtracking Token Parsing
- In `MolecularGeometryLabService.calculate_molecular_geometry`:
  - Added formula length constraint: `if len(clean_formula) > 30: raise ValueError(...)`.
  - Replaced all complex regex matching with direct O(1) hash map lookup against verified molecular configurations.
  - In `balance_redox_reaction`: length constrained to `<= 120` chars with direct substring matching.

### 2. Atomic Anti-Sybil Vote Locking & Clamped Reputation Multipliers
- In `InnovationLaunchpadService.cast_vote`:
  - Formed unique composite key: `vote_key = f"{project_id}:{voter_student_id}"`.
  - Checked `if vote_key in self._votes: raise ValueError(...)`.
  - Enforced reputation multiplier clamping: `weight = min(max(float(voter_reputation_score) / 100.0, 0.5), 3.0)`.
  - Prevents automated vote stuffing and limits influence of outlier accounts.

### 3. Sequential Escrow Tranche Disbursal & Re-Release Locks
- In `InnovationLaunchpadService.release_grant_tranche`:
  - Enforced stage progression:
    - Stage 2 (`PROTOTYPE_DEMO`) requires Stage 1 (`PROPOSAL_VALIDATION`).
    - Stage 3 (`PILOT_DEPLOYMENT`) requires Stage 2 (`PROTOTYPE_DEMO`).
  - Added duplicate stage protection: `if stage_upper in existing_stages: raise ValueError(...)`.
  - Accurately tracks `escrow_balance_remaining_bdt` down to 0.00 BDT.

### 4. Project Repository URL Whitelist
- In `InnovationLaunchpadService.pitch_project`:
  - Validated that `clean_url.startswith("https://") or clean_url.startswith("http://") or clean_url.startswith("git://")`.
  - Rejects any malformed or malicious scheme attempts with a descriptive `ValueError`.
