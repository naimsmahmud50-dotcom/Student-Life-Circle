"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite
TOPIC:     Phase 102 Dignified Academic Gamification & Social Proof Tests
FILE:      backend/tests/test_phase102_dignified_gamification.py
PHASE:     Phase 102 - Dignified Gamification & Verifiable Social Proof
PURPOSE:   Asserts anti-burnout daily point caps (500 XP), empathetic streak
           recovery drill mechanics, cryptographic HMAC-SHA256 badge verification,
           Developer Architecture Note headers, and strict zero-emoji governance.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
"""

import os
import unittest
from backend.app.services.gamification_service import GamificationService, gamification_service


class TestPhase102DignifiedGamification(unittest.TestCase):
    """
    Automated verification suite for Phase 102 Dignified Gamification and Social Proof.
    """

    def setUp(self):
        self.service = GamificationService()

    def test_01_anti_burnout_daily_xp_capping(self):
        """Verify daily points are capped at 500 XP to prevent addictive binge studying."""
        user_id = "test-learner-anti-burnout-01"

        # Award 300 XP
        res1 = self.service.award_xp(user_id, 300, "math_quiz")
        self.assertEqual(res1["awarded_xp"], 300)
        self.assertEqual(res1["total_today_xp"], 300)
        self.assertFalse(res1["daily_capped"])

        # Award another 250 XP (total would be 550, but capped at 500)
        res2 = self.service.award_xp(user_id, 250, "physics_lab")
        self.assertEqual(res2["awarded_xp"], 200)  # Capped to 200 to hit 500
        self.assertEqual(res2["total_today_xp"], 500)
        self.assertTrue(res2["daily_capped"])

        # Attempt to earn more points after cap
        res3 = self.service.award_xp(user_id, 100, "chemistry_drill")
        self.assertEqual(res3["awarded_xp"], 0)
        self.assertEqual(res3["total_today_xp"], 500)
        self.assertTrue(res3["daily_capped"])
        self.assertIn("Daily study point cap reached", res3["message"])

    def test_02_streak_status_and_shield_activation(self):
        """Verify streak shield consumes one shield and sets is_frozen to True."""
        user_id = "test-learner-shield-01"
        status_initial = self.service.get_streak_status(user_id)
        self.assertEqual(status_initial["streak_shields"], 1)
        self.assertFalse(status_initial["is_frozen"])

        # Activate streak shield
        shield_res = self.service.use_streak_shield(user_id)
        self.assertTrue(shield_res["success"])
        self.assertEqual(shield_res["remaining_shields"], 0)

        # Status reflects frozen
        status_after = self.service.get_streak_status(user_id)
        self.assertTrue(status_after["is_frozen"])
        self.assertEqual(status_after["streak_shields"], 0)

        # Attempt to use shield when 0 remaining
        shield_fail = self.service.use_streak_shield(user_id)
        self.assertFalse(shield_fail["success"])

    def test_03_empathetic_streak_recovery_via_drill(self):
        """Verify that passing a review drill with >= 60% restores a broken streak."""
        user_id = "test-learner-recovery-01"
        user = self.service._ensure_user(user_id)
        user["current_streak"] = 15
        user["requires_recovery"] = True

        # Failed drill (score < 60%)
        fail_drill = self.service.recover_streak_via_drill(user_id, drill_score=55.0)
        self.assertFalse(fail_drill["recovered"])
        self.assertEqual(self.service.get_streak_status(user_id)["current_streak"], 15)

        # Passed drill (score >= 60%)
        pass_drill = self.service.recover_streak_via_drill(user_id, drill_score=85.0)
        self.assertTrue(pass_drill["recovered"])
        self.assertIn("empathetically restored", pass_drill["message"])
        self.assertEqual(self.service.get_streak_status(user_id)["current_streak"], 16)

    def test_04_cryptographic_badge_issuance_and_verification(self):
        """Verify HMAC-SHA256 tamper-evident badge generation and validation."""
        user_id = "test-scholar-badge-01"
        badge = self.service.award_mastery_badge(
            user_id=user_id,
            badge_id="badge-buet-calculus-top1",
            title="BUET Admission Calculus Champion",
            skill_name="Multivariable & Definite Calculus",
            percentile_rank=99.2,
            issuing_authority="BUET Department of Mathematics"
        )

        self.assertIsNotNone(badge["verification_hash"])
        self.assertEqual(len(badge["verification_hash"]), 64)
        self.assertIn("https://ogrojatra.edu.bd/verify/badge/", badge["qr_verification_url"])

        # Verify badge against ledger
        verified = self.service.verify_badge(badge["verification_hash"])
        self.assertIsNotNone(verified)
        self.assertEqual(verified["title"], "BUET Admission Calculus Champion")
        self.assertEqual(verified["percentile_rank"], 99.2)

        # Tampered hash must fail verification
        tampered_verified = self.service.verify_badge("tampered_fake_hash_1234567890abcdef")
        self.assertIsNone(tampered_verified)

    def test_05_portfolio_generation(self):
        """Verify complete user portfolio aggregation."""
        portfolio = self.service.get_portfolio("usr-me-student-01")
        self.assertIn("streak", portfolio)
        self.assertIn("xp_metrics", portfolio)
        self.assertIn("badges", portfolio)
        self.assertIn("milestones", portfolio)
        self.assertEqual(portfolio["xp_metrics"]["daily_cap"], 500)
        self.assertGreater(len(portfolio["milestones"]), 0)

    def test_06_developer_architecture_note_headers(self):
        """Verify standardized Developer Architecture Note header in all Phase 102 target files."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        phase102_files = [
            os.path.join(repo_root, "frontend", "src", "components", "gamification", "StreakShieldModal.tsx"),
            os.path.join(repo_root, "frontend", "src", "components", "gamification", "MasteryBadgeCard.tsx"),
            os.path.join(repo_root, "frontend", "src", "pages", "achievements.tsx"),
            os.path.join(repo_root, "backend", "app", "services", "gamification_service.py"),
            os.path.join(repo_root, "backend", "tests", "test_phase102_dignified_gamification.py")
        ]

        for file_path in phase102_files:
            self.assertTrue(os.path.exists(file_path), f"File missing: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                header = f.read(500)
                self.assertIn("DEVELOPER ARCHITECTURE NOTE", header, f"Missing header in: {file_path}")
                self.assertIn("Phase 102", header, f"Missing Phase 102 in: {file_path}")

    def test_07_zero_emoji_governance(self):
        """Verify strict zero-emoji compliance in Phase 102 target files."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        phase102_files = [
            os.path.join(repo_root, "frontend", "src", "components", "gamification", "StreakShieldModal.tsx"),
            os.path.join(repo_root, "frontend", "src", "components", "gamification", "MasteryBadgeCard.tsx"),
            os.path.join(repo_root, "frontend", "src", "pages", "achievements.tsx"),
            os.path.join(repo_root, "backend", "app", "services", "gamification_service.py")
        ]

        emoji_ranges = [
            (0x1F600, 0x1F64F),  # Emoticons
            (0x1F300, 0x1F5FF),  # Misc Symbols
            (0x1F680, 0x1F6FF),  # Transport
            (0x1F700, 0x1F77F),  # Alchemical
            (0x1F900, 0x1F9FF),  # Supplemental
            (0x2600, 0x26FF),    # Misc Symbols
            (0x2700, 0x27BF),    # Dingbats
        ]

        for file_path in phase102_files:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                for char in text:
                    cp = ord(char)
                    for start, end in emoji_ranges:
                        self.assertFalse(
                            start <= cp <= end,
                            f"Emoji character '{char}' (U+{cp:X}) detected in {file_path}"
                        )


if __name__ == "__main__":
    unittest.main()
