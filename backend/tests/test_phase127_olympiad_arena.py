"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    National STEM Olympiad Arena & Tournament Engine
TOPIC:     Phase 127 Real-time Competitive Olympiad & Live Bracket Ladder
FILE:      backend/tests/test_phase127_olympiad_arena.py
PHASE:     Phase 127 - National Live Multiplayer STEM Olympiad Arena
PURPOSE:   Comprehensive unit, integration, and security test suite validating:
           1. Elo matchmaking calculation and pairing
           2. Latency-compensated countdown timer and clock anomaly detection
           3. Anti-cheating time-locked cryptographic HMAC token validation
           4. Tournament ladder bracket advancement
           5. Percentile-based medal tier distributions
           6. Supabase Row Level Security (RLS) policies on olympiad tables
           7. Frontend 3D tactile button styling and KaTeX integration
           8. Strict Zero-Emoji compliance across all Phase 127 target files.
STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Sub-50ms Latency
========================================================================================
"""

import os
import re
import unittest
from pathlib import Path

from backend.olympiad.tournament_engine import (
    TournamentEngine,
    OlympiadParticipant,
    TournamentMatch,
    MedalTier,
    CheatingAnomalyException,
)

# Comprehensive Strict Zero-Emoji Regex covering Unicode emojis, pictographs, and symbols
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase127OlympiadArena(unittest.TestCase):
    """
    Automated verification suite validating Phase 127 National Live STEM Olympiad Arena.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.init_py = cls.root_dir / "backend" / "olympiad" / "__init__.py"
        cls.engine_py = cls.root_dir / "backend" / "olympiad" / "tournament_engine.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "005_olympiad_tournament_rls.sql"
        cls.frontend_tsx = cls.root_dir / "frontend" / "src" / "pages" / "olympiad" / "arena.tsx"
        cls.test_file = Path(__file__).resolve()

        cls.target_files = [
            cls.init_py,
            cls.engine_py,
            cls.migration_sql,
            cls.frontend_tsx,
            cls.test_file,
        ]

    def test_01_all_target_files_exist_and_headers_valid(self):
        """
        Verify all 5 Phase 127 target files exist and contain standardized Developer Architecture Note.
        """
        for file_path in self.target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"Missing Developer Architecture Note in {file_path.name}",
            )
            self.assertIn(
                "Phase 127 - National Live Multiplayer STEM Olympiad Arena",
                content,
                f"Missing Phase 127 identifier in {file_path.name}",
            )

    def test_02_elo_rating_calculation_and_pairing(self):
        """
        Verify Elo rating calculations, expected score formula, and contiguous matchmaking pairing.
        """
        # Equal ratings produce exactly 0.5 expected score
        exp_equal = TournamentEngine.calculate_expected_score(1500.0, 1500.0)
        self.assertAlmostEqual(exp_equal, 0.5, places=4)

        # Higher rating participant has higher expected score
        exp_higher = TournamentEngine.calculate_expected_score(1700.0, 1500.0)
        self.assertGreater(exp_higher, 0.75)
        self.assertLess(exp_higher, 0.80)

        # Winner rating increases, loser rating decreases symmetrically
        new_a, new_b = TournamentEngine.update_elo_rating(1600.0, 1600.0, score_a=1.0, k_factor=32.0)
        self.assertEqual(new_a, 1616.0)
        self.assertEqual(new_b, 1584.0)

        # Contiguous Elo pairing sorts candidates and pairs adjacent ranks
        candidates = [
            OlympiadParticipant(id="p1", name="A", elo_rating=1800.0),
            OlympiadParticipant(id="p2", name="B", elo_rating=1500.0),
            OlympiadParticipant(id="p3", name="C", elo_rating=1780.0),
            OlympiadParticipant(id="p4", name="D", elo_rating=1520.0),
        ]
        pairs = TournamentEngine.pair_participants_by_elo(candidates)
        self.assertEqual(len(pairs), 2)
        # Top pair: p1 (1800) and p3 (1780)
        self.assertEqual(pairs[0][0].id, "p1")
        self.assertEqual(pairs[0][1].id, "p3")
        # Second pair: p4 (1520) and p2 (1500)
        self.assertEqual(pairs[1][0].id, "p4")
        self.assertEqual(pairs[1][1].id, "p2")

    def test_03_latency_compensation_and_anomaly_detection(self):
        """
        Verify network latency compensation and anti-tamper clock anomaly detection.
        """
        server_now = 100000.0
        client_time = 99950.0  # Dispatched 50ms ago
        rtt_ms = 80.0          # 40ms one-way
        q_start = 80000.0

        # Compensated elapsed time: (client_time - rtt/2) - q_start
        # (99950 - 40) - 80000 = 19910ms = 19.910s
        comp_time = TournamentEngine.validate_and_compensate_latency(
            client_timestamp_ms=client_time,
            server_now_ms=server_now,
            rtt_ms=rtt_ms,
            question_start_server_ms=q_start,
        )
        self.assertEqual(comp_time, 19.910)

        # Invariant 1: Clock manipulation anomaly (client timestamp in the future beyond allowable jitter)
        future_client_time = server_now + 3000.0  # 3s in the future (exceeds 1.5s jitter threshold)
        with self.assertRaises(CheatingAnomalyException):
            TournamentEngine.validate_and_compensate_latency(
                client_timestamp_ms=future_client_time,
                server_now_ms=server_now,
                rtt_ms=50.0,
                question_start_server_ms=q_start,
            )

        # Invariant 2: Stale / Replayed submissions beyond allowable transit window
        stale_client_time = server_now - 120000.0  # 120s ago
        with self.assertRaises(CheatingAnomalyException):
            TournamentEngine.validate_and_compensate_latency(
                client_timestamp_ms=stale_client_time,
                server_now_ms=server_now,
                rtt_ms=50.0,
                question_start_server_ms=q_start,
            )

    def test_04_time_locked_cryptographic_hash(self):
        """
        Verify time-locked HMAC-SHA256 token generation and constant-time verification.
        """
        salt = "sovereign_bangladesh_stem_secret_salt_2026"
        token = TournamentEngine.generate_time_locked_hash(
            secret_salt=salt,
            tournament_id="tourn_hsc_2026",
            question_id="q_rocket_01",
            participant_id="user_rakib_01",
            option_id="opt_a",
            timestamp_ms=1729440000000,
            nonce="nonce_abc123xyz",
        )
        self.assertTrue(isinstance(token, str))
        self.assertEqual(len(token), 64)  # SHA-256 hex string

        # Valid token passes
        is_valid = TournamentEngine.verify_time_locked_hash(
            secret_salt=salt,
            tournament_id="tourn_hsc_2026",
            question_id="q_rocket_01",
            participant_id="user_rakib_01",
            option_id="opt_a",
            timestamp_ms=1729440000000,
            nonce="nonce_abc123xyz",
            provided_hash=token,
        )
        self.assertTrue(is_valid)

        # Tampered option ID fails
        is_tampered = TournamentEngine.verify_time_locked_hash(
            secret_salt=salt,
            tournament_id="tourn_hsc_2026",
            question_id="q_rocket_01",
            participant_id="user_rakib_01",
            option_id="opt_b",  # Tampered!
            timestamp_ms=1729440000000,
            nonce="nonce_abc123xyz",
            provided_hash=token,
        )
        self.assertFalse(is_tampered)

    def test_05_medal_tier_percentile_distribution(self):
        """
        Verify medal tier distributions (Gold 8%, Silver 17%, Bronze 25%, Honorable Mention 25%).
        """
        # Create 100 mock participants
        candidates = [
            OlympiadParticipant(
                id=f"cand_{i}",
                name=f"Student {i}",
                elo_rating=1500 + i,
                score=i,  # Scores 0 to 99
                total_time_ms=1000.0 - i,
            )
            for i in range(100)
        ]

        leaderboard = TournamentEngine.calculate_medal_tiers(candidates)
        self.assertEqual(len(leaderboard), 100)

        # Rank 1 must be highest score (cand_99) and have Gold Medal
        self.assertEqual(leaderboard[0]["rank"], 1)
        self.assertEqual(leaderboard[0]["participant_id"], "cand_99")
        self.assertEqual(leaderboard[0]["medal_tier"], "স্বর্ণপদক")

        # Counts per tier
        tier_counts = {}
        for entry in leaderboard:
            tier = entry["medal_tier"]
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        self.assertEqual(tier_counts.get("স্বর্ণপদক"), 8)           # Top 8%
        self.assertEqual(tier_counts.get("রৌপ্যপদক"), 17)          # Next 17% (9-25)
        self.assertEqual(tier_counts.get("ব্রোঞ্জপদক"), 25)         # Next 25% (26-50)
        self.assertEqual(tier_counts.get("বিশেষ সম্মাননা"), 25)     # Next 25% (51-75)
        self.assertEqual(tier_counts.get("অংশগ্রহণ সনদ"), 25)      # Remaining 25% (76-100)

    def test_06_tournament_bracket_ladder_progression(self):
        """
        Verify bracket ladder match generation, winner resolution, and round progression.
        """
        p1 = OlympiadParticipant(id="p1", name="Player 1", elo_rating=1700.0)
        p2 = OlympiadParticipant(id="p2", name="Player 2", elo_rating=1680.0)
        p3 = OlympiadParticipant(id="p3", name="Player 3", elo_rating=1650.0)
        p4 = OlympiadParticipant(id="p4", name="Player 4", elo_rating=1620.0)

        all_p = {p.id: p for p in [p1, p2, p3, p4]}

        # Round 1 (Semi-Finals)
        matches = TournamentEngine.generate_bracket_matches(
            participants=[p1, p2, p3, p4],
            round_number=1,
            round_name="Semi-Finals",
        )
        self.assertEqual(len(matches), 2)

        # Resolve match 1 (p1 beats p2)
        TournamentEngine.resolve_match(matches[0], score_a=3.0, score_b=1.0, latency_a_ms=25.0, latency_b_ms=30.0)
        self.assertEqual(matches[0].winner_id, "p1")

        # Resolve match 2 (p3 ties with p4 on score, but p3 has lower latency)
        TournamentEngine.resolve_match(matches[1], score_a=2.0, score_b=2.0, latency_a_ms=20.0, latency_b_ms=35.0)
        self.assertEqual(matches[1].winner_id, "p3")

        # Advance to Grand Finals
        finals = TournamentEngine.advance_to_next_round(
            completed_matches=matches,
            all_participants=all_p,
            next_round_number=2,
            next_round_name="Grand Finals",
        )
        self.assertEqual(len(finals), 1)
        self.assertEqual(finals[0].participant_a_id, "p1")
        self.assertEqual(finals[0].participant_b_id, "p3")

    def test_07_supabase_migration_rls_security(self):
        """
        Verify backend/migrations/005_olympiad_tournament_rls.sql enforces strict RLS policies.
        """
        content = self.migration_sql.read_text(encoding="utf-8")

        # Tables exist
        self.assertIn("CREATE TABLE IF NOT EXISTS public.olympiad_tournaments", content)
        self.assertIn("CREATE TABLE IF NOT EXISTS public.olympiad_submissions", content)
        self.assertIn("CREATE TABLE IF NOT EXISTS public.olympiad_audit_log", content)

        # RLS Enabled and Forced
        self.assertIn("ALTER TABLE public.olympiad_tournaments ENABLE ROW LEVEL SECURITY", content)
        self.assertIn("ALTER TABLE public.olympiad_tournaments FORCE ROW LEVEL SECURITY", content)
        self.assertIn("ALTER TABLE public.olympiad_submissions ENABLE ROW LEVEL SECURITY", content)
        self.assertIn("ALTER TABLE public.olympiad_submissions FORCE ROW LEVEL SECURITY", content)

        # Direct auth.uid() = participant_id bindings
        self.assertIn("auth.uid() = participant_id", content)

        # Immutability guarantees
        self.assertIn("REVOKE UPDATE, DELETE ON public.olympiad_submissions", content)
        self.assertIn("prevent_olympiad_submission_tampering", content)

    def test_08_frontend_arena_page_contract(self):
        """
        Verify frontend/src/pages/olympiad/arena.tsx incorporates 3D tactile buttons and KaTeX math.
        """
        content = self.frontend_tsx.read_text(encoding="utf-8")

        # 3D physical ledge depth on action buttons
        self.assertIn("shadow-[0_4px_0_0_#051329]", content)
        self.assertIn("active:translate-y-1", content)
        self.assertIn("active:shadow-none", content)
        self.assertIn("bg-[#0A2540]", content)

        # KaTeX Mathematical rendering
        self.assertIn("<KaTeXRenderer", content)

        # Latency-compensated indicator and tournament bracket
        self.assertIn("ল্যাটেন্সি সিঙ্কড", content)
        self.assertIn("ব্র্যাকেট", content)
        self.assertIn("স্বর্ণপদক", content)

    def test_09_strict_zero_emoji_compliance(self):
        """
        Verify 100% Zero-Emoji policy across all Phase 127 target files.
        """
        for file_path in self.target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(
                matches,
                [],
                f"Strict Zero-Emoji violation in {file_path.name}: Found emojis {matches}",
            )


if __name__ == "__main__":
    unittest.main()
