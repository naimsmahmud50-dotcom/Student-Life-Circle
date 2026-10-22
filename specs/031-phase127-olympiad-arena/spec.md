# SPECIFICATION: Phase 127 — National Live Multiplayer STEM Olympiad Arena & Tournament Ladder

## 1. Executive Summary & Objective
Phase 127 introduces the National Live Multiplayer STEM Olympiad Arena & Tournament Ladder for the Ogrojatra platform. This system facilitates high-stakes, real-time scholastic tournaments across physics, mathematics, and chemistry for students in Bangladesh. The engine incorporates Elo-rating based pairing, live bracket progression, sub-50ms latency-compensated timers, and anti-cheating time-locked cryptographic hash verification under strict Supabase Row Level Security (RLS).

## 2. Mandatory Architectural Standards
- **Standardized Developer Architecture Note**: Every created or modified file MUST feature the standardized block header documenting Phase 127, ASVS L2, and sub-50ms latency standards.
- **Pure Academic Visual Philosophy (Zero AI Vibe)**:
  * Pure Paper Ivory (`#FAFAF8`) & Pure Paper White (`#FFFFFF`) surfaces.
  * Oxford Academic Navy (`#0A2540`) borders, headers, and accents.
  * 3D tactile buttons with physical bottom ledge: `bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] hover:bg-[#081C30] active:translate-y-1 active:shadow-none transition-all font-semibold rounded-lg`.
  * Strict Zero-Emoji Rule: 100% pure Lucide-React SVG vector icons only.

## 3. Technical Requirements

### A. Backend Tournament Engine (`backend/olympiad/tournament_engine.py`)
1. **Elo Rating & Pairing System**:
   - Standard FIDE/K-factor based calculation ($K=32$ for high-stakes junior tournaments).
   - Expected score formula: $E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}$.
   - Pairing algorithm: Sorts available participants by Elo rating and pairs contiguous candidates to ensure tight, balanced competitive matches.
2. **Latency-Compensated Server Timer**:
   - Measures one-way network transit latency ($L = \frac{RTT}{2}$).
   - Client submission timestamps are validated against server start time: $T_{\text{effective}} = T_{\text{client}} - L_{\text{transit}}$.
   - Enforces grace window ($\Delta t \le 1.5\text{s}$) to absorb rural mobile packet jitter while detecting and rejecting manipulated client clocks.
3. **Live Leaderboard & Instant Medal Tier Calculation**:
   - Percentile-based medal distribution modeled after the International Mathematical Olympiad (IMO) and Asian Physics Olympiad (APhO):
     * Top 8% $\rightarrow$ Gold Medal (`স্বর্ণপদক`)
     * Next 17% (8% to 25%) $\rightarrow$ Silver Medal (`রৌপ্যপদক`)
     * Next 25% (25% to 50%) $\rightarrow$ Bronze Medal (`ব্রোঞ্জপদক`)
     * Next 25% (50% to 75%) $\rightarrow$ Honorable Mention (`বিশেষ সম্মাননা`)
4. **Tournament Ladder Progression**:
   - Single-elimination / Swiss bracket management from Round 1 through Quarter-Finals, Semi-Finals, and Grand Finals.
   - Deterministic winner resolution using primary score and tie-breaking by lowest average latency-compensated response time.

### B. Supabase Security & Anti-Cheating (`backend/migrations/005_olympiad_tournament_rls.sql`)
1. **Tables**:
   - `olympiad_tournaments`: Tournament metadata, round status, participants, and bracket structure.
   - `olympiad_submissions`: Individual answer submissions, time-locked hashes, scores, and verification status.
2. **Row Level Security (RLS)**:
   - Enabled and forced on all olympiad tables.
   - `auth.uid() = participant_id` for submission inserts and reads.
   - Public read-only access for tournament bracket and finalized leaderboard summaries.
3. **Time-Locked Cryptographic Hash Verification**:
   - Prevents ahead-of-time scraping, pre-computation, or replay attacks.
   - Hash formulation: $\text{HMAC-SHA256}(\text{salt}, \text{tournament\_id} \parallel \text{question\_id} \parallel \text{selected\_option} \parallel \text{timestamp} \parallel \text{nonce})$.
   - Verified on server prior to score absorption.

### C. Frontend Olympiad Arena (`frontend/src/pages/olympiad/arena.tsx`)
1. **Live Tournament Bracket View**:
   - Visual tournament progression tree (Round of 16, Quarter-Finals, Semi-Finals, Finals).
2. **Competitive Question Canvas**:
   - NCTB HSC STEM questions rendered with KaTeX equations.
   - High-contrast typography and clear question stems.
3. **Tactile 3D Controls**:
   - Option cards with 44px+ touch targets and 3D physical depth.
   - Submit action button with active depression physics.
4. **Live Scoreboard & Latency Banner**:
   - Displays real-time match standing, current rank, and latency compensation status badge (`ল্যাটেন্সি সিঙ্কড`).

### D. Automated Verification Suite (`backend/tests/test_phase127_olympiad_arena.py`)
- Unit and integration tests certifying Elo rating math, pairing, timer compensation, medal allocation, cryptographic hash validation, RLS policies, frontend tactile classes, and zero-emoji compliance.
- 100% pass rate across entire platform test suite (1,423+ tests).
