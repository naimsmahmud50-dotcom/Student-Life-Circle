# IMPLEMENTATION PLAN: Phase 127 — National Live Multiplayer STEM Olympiad Arena & Tournament Ladder

## 1. Architecture Overview
This plan establishes the architecture and execution steps for Phase 127:
- `backend/olympiad/__init__.py`: Package initialization.
- `backend/olympiad/tournament_engine.py`: Elo pairing, latency compensation, tournament bracket state, anti-cheating hash verification, and medal distributions.
- `backend/migrations/005_olympiad_tournament_rls.sql`: Supabase table definitions with Row-Level Security (RLS) policies and time-locked constraints.
- `frontend/src/pages/olympiad/arena.tsx`: Live multiplayer competition arena with real-time bracket visualization, KaTeX question canvas, tactile 3D buttons, and zero AI vibe.
- `backend/tests/test_phase127_olympiad_arena.py`: Comprehensive test suite testing all functional logic, security invariants, design compliance, and zero emojis.

## 2. Execution Steps

### Step 1: Backend Tournament Engine & Cryptographic Integrity
- Create `backend/olympiad/__init__.py` and `backend/olympiad/tournament_engine.py`.
- Implement `TournamentEngine` class with:
  * Elo calculation: `calculate_expected_score(rating_a, rating_b)` and `update_elo_rating(rating_a, rating_b, score_a, k_factor)`.
  * Participant pairing: `pair_participants_by_elo(participants)`.
  * Latency compensation: `validate_and_compensate_latency(client_timestamp, server_now, rtt_ms, max_jitter_ms)`.
  * Anti-cheating hash: `generate_time_locked_hash(secret_salt, tournament_id, question_id, participant_id, option_id, timestamp, nonce)` and `verify_time_locked_hash(...)`.
  * Bracket progression: `advance_bracket_round(bracket_matches, match_results)`.
  * Medal tier classification: `calculate_medal_tiers(participants_scores)`.

### Step 2: Supabase Migration with Hardened RLS
- Create `backend/migrations/005_olympiad_tournament_rls.sql`.
- Create tables: `olympiad_tournaments`, `olympiad_participants`, `olympiad_submissions`, `olympiad_audit_log`.
- Apply strict `ENABLE ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY`.
- Create policies enforcing `auth.uid() = participant_id` on submissions and public read for tournaments.

### Step 3: Frontend Olympiad Arena (`frontend/src/pages/olympiad/arena.tsx`)
- Build the real-time arena component.
- Display interactive tournament ladder bracket (Round of 16 -> Quarter Finals -> Semi Finals -> Grand Finals).
- Render NCTB HSC STEM questions with KaTeX mathematical formulas.
- Implement 3D physical ledge tactile buttons (`bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none`).
- Provide sub-50ms latency indicator (`ল্যাটেন্সি সিঙ্কড`), server-synchronized countdown, and instant Socratic post-match analysis.
- Strict Zero-Emoji compliance with Lucide-React SVG icons.

### Step 4: Automated Verification Test Suite (`test_phase127_olympiad_arena.py`)
- Test Elo mathematics and contiguous rating pairing.
- Test network jitter compensation and clock-tampering detection.
- Test medal tier boundaries (Gold 8%, Silver 17%, Bronze 25%, Honorable Mention 25%).
- Test anti-cheating time-locked HMAC verification.
- Test Supabase SQL migration RLS statements.
- Test frontend arena source code for tactile button classes and KaTeX integration.
- Test strict zero-emoji compliance.

### Step 5: Platform-wide Verification & Certification
- Run `python3 backend/scripts/run_zero_emoji_sweep.py`.
- Run `python3 -m unittest backend/tests/test_phase127_olympiad_arena.py`.
- Run full test discovery: `python3 -m unittest discover -s backend/tests -p "test_*.py"`.
- Produce `PHASE_127_OLYMPIAD_ARENA_REPORT.md`.
