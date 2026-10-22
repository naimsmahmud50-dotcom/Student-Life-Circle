# Bug Assessment: Omni-Search Whitespace Punctuation & Reputation Boundary Normalization

## 1. Problem Description
Static triage of Phase 25 components revealed potential boundary edge cases:
1. **Whitespace & Punctuation in Omni-Search**:
   - Queries with whitespace padding (e.g., `"  calculus  "`) or punctuation tokens (e.g., `"UI/UX"`, `"C++"`, `"Class-9"`) can fail exact token matching if naive split without normalization is used.
   - Empty/whitespace-only queries should return curated top recommendations instead of failing.
2. **Notification Recipient ID Mismatch**:
   - Dispatched notifications with unstripped recipient user IDs (e.g. `" student_demo_01 "`) would create separate inbox entries from canonical `"student_demo_01"`.
   - Empty notification titles or messages should be rejected with bad request validation.
3. **Reputation Score Boundary Stability**:
   - Extreme negative or uninitialized metrics (e.g., negative CAT theta, zero sessions, or out-of-range ratings) must be bounded strictly within 0 to 1000 without division by zero.

---

## 2. Root Cause Analysis
- `OmniSearchService._compute_relevance` split tokens on raw whitespace without stripping punctuation.
- `NotificationGatewayService` did not canonicalize recipient IDs with `.strip()`.
- `StudentReputationService` lacked explicit clamping on raw sub-scores before summation.

---

## 3. Proposed Remediation
1. In `OmniSearchService`:
   - Strip leading/trailing whitespace from queries.
   - Strip punctuation while retaining alphanumeric tokens and symbols (`+`, `#`, `/`).
2. In `NotificationGatewayService`:
   - Canonicalize `recipient_user_id.strip()`.
   - Reject empty titles or messages with error codes `EMPTY_NOTIFICATION_TITLE` and `EMPTY_NOTIFICATION_MESSAGE`.
3. In `StudentReputationService`:
   - Clamp all 4 pillar sub-scores: Academic (0-350), Tutoring (0-250), Career (0-250), Integrity (0-150).
   - Clamp composite score strictly to [0, 1000].
