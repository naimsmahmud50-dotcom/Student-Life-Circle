"""
DEVELOPER ARCHITECTURE NOTES:
--------------------------------------------------------------------------------
Target System: Ogrojatra National Educational Platform
Test Suite: Phase 98.2 Flagship Home Dashboard Verification (Task T657)
Purpose:
  Validates frontend/src/pages/index.tsx overhaul:
  1. Dynamic Hero Section:
     - Dignified greeting ("স্বাগতম, ভবিষ্যৎ গড়ার অগ্রযাত্রায়")
     - Academic stage selector chips (SSC, HSC, Admission, Career)
     - Quick Resume primary CTA button
  2. 4-Card Academic Telemetry Grid:
     - Study Streak ("৭ দিনের স্ট্রিক", Flame SVG)
     - Questions Solved ("১২৮টি প্রশ্ন সমাধান", CheckCircle SVG)
     - Accuracy Rate ("৮৬.৪% নির্ভুলতা", Target SVG)
     - National Percentile ("শীর্ষ ৫% শিক্ষার্থী", Award SVG)
  3. Curated Journey Pathways (4 Visual Cards with progress meters):
     - SSC 9-10 (68%), HSC 11-12 (82%), Admission (45%), Tuition/Career (90%)
  4. 3D STEM Virtual Labs Showcase:
     - Projectile Motion Simulator & 3D Molecular Geometry cards with instant modal launchers
  5. Live Challenge Spotlight:
     - Synchronized 8:00 PM National Challenge countdown timer & participant counter
  6. Socratic AI Instant Solver banner:
     - "যেকোনো প্রশ্নের ছবি তুলুন বা লিখুন" with 1-click drawer trigger
  7. W3C Proof-of-Skill Certificate Showcase:
     - Real-time preview of verified certificate with QR code and LinkedIn/Facebook share
  8. Official Trust & Payment Bar:
     - Verified logos for bKash, Nagad, and SSLCommerz
  9. Strict Zero-Emoji compliance and Developer Architecture Notes.
Standards:
  - WCAG 2.2 AAA Contrast, Zero-Emoji Policy.
--------------------------------------------------------------------------------
"""

import os
import re
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class TestPhase982FlagshipHomeDashboard(unittest.TestCase):
    """
    Automated test suite asserting the completeness and integrity of the flagship home dashboard.
    """

    def setUp(self):
        self.frontend_dir = os.path.join(PROJECT_ROOT, "frontend")
        self.index_path = os.path.join(self.frontend_dir, "src", "pages", "index.tsx")

    def test_01_index_file_exists(self):
        """Verifies frontend/src/pages/index.tsx exists and is non-empty."""
        self.assertTrue(os.path.isfile(self.index_path), "index.tsx must exist")
        self.assertGreater(os.path.getsize(self.index_path), 1000)

    def test_02_dynamic_hero_section(self):
        """Asserts hero section contains dignified greeting, stage selector chips, and quick resume CTA."""
        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Hero greeting
        self.assertIn("স্বাগতম, ভবিষ্যৎ গড়ার", content)
        self.assertIn("অগ্রযাত্রায়", content)

        # Stage chips
        self.assertIn("মাধ্যমিক (SSC ৯-১০)", content)
        self.assertIn("উচ্চ মাধ্যমিক (HSC ১১-১২)", content)
        self.assertIn("বিশ্ববিদ্যালয় ভর্তি (Admission)", content)
        self.assertIn("টিউশন ও ক্যারিয়ার (Career)", content)

        # Quick resume CTA
        self.assertIn("পড়াশোনা শুরু করুন (Quick Resume)", content)
        self.assertIn("/practice", content)

    def test_03_four_card_academic_telemetry_grid(self):
        """Asserts 4-card telemetry grid contains study streak, solved questions, accuracy, and percentile."""
        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Study Streak
        self.assertIn("৭ দিনের স্ট্রিক", content)
        self.assertIn("Flame", content)

        # 2. Questions Solved
        self.assertIn("১২৮টি প্রশ্ন সমাধান", content)
        self.assertIn("CheckCircle2", content)

        # 3. Accuracy Rate
        self.assertIn("৮৬.৪% নির্ভুলতা", content)
        self.assertIn("Target", content)

        # 4. National Percentile
        self.assertIn("শীর্ষ ৫% শিক্ষার্থী", content)
        self.assertIn("Award", content)

    def test_04_curated_journey_pathways_four_cards(self):
        """Asserts 4 curated pathways exist with progress meters and direct links."""
        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Pathway 1: SSC
        self.assertIn("মাধ্যমিক (SSC) বোর্ড প্রস্তুতি", content)
        self.assertIn("৬৮% সম্পন্ন", content)
        self.assertIn("w-[68%]", content)
        self.assertIn("/learn?stage=SSC", content)

        # Pathway 2: HSC
        self.assertIn("উচ্চ মাধ্যমিক (HSC) বিজ্ঞান", content)
        self.assertIn("৮২% সম্পন্ন", content)
        self.assertIn("w-[82%]", content)
        self.assertIn("/learn?stage=HSC", content)

        # Pathway 3: Admission
        self.assertIn("বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি", content)
        self.assertIn("৪৫% সম্পন্ন", content)
        self.assertIn("w-[45%]", content)
        self.assertIn("/admission", content)

        # Pathway 4: Tuition & Career
        self.assertIn("টিউশন ও স্কিল লেজার", content)
        self.assertIn("৯০% প্রোফাইল", content)
        self.assertIn("w-[90%]", content)
        self.assertIn("/tuition", content)

    def test_05_three_d_stem_virtual_labs_showcase(self):
        """Asserts 3D STEM labs section contains Projectile and Molecular Geometry cards and modal triggers."""
        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Projectile Motion Lab
        self.assertIn("প্রক্ষেপক গতিবিদ্যা সিমুলেটর", content)
        self.assertIn("Projectile Motion", content)

        # Molecular Geometry Lab
        self.assertIn("৩ডি আণবিক জ্যামিতি ও সংকরায়ন", content)
        self.assertIn("Molecular Geometry", content)

        # Modal triggers and component embedding
        self.assertIn("ল্যাব চালু করুন", content)
        self.assertIn("activeLabModal", content)
        self.assertIn("<PhysicsProjectileLab", content)
        self.assertIn("<ChemistryMolecularViewer", content)

    def test_06_live_challenge_spotlight_card(self):
        """Asserts 8:00 PM National Challenge spotlight contains countdown timer and participant counter."""
        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("আজ রাত ৮:০০ টার জাতীয় অলিম্পিয়াড চ্যালেঞ্জ", content)
        self.assertIn("জাতীয় লাইভ কুইজ প্রতিযোগিতা ২০২৬", content)
        self.assertIn("countdown", content)
        self.assertIn("৪,৮৫০+ প্রতিযোগী শিক্ষার্থী", content)
        self.assertIn("লাইভ লবিতে যোগ দিন", content)
        self.assertIn("/live-challenge", content)

    def test_07_socratic_ai_instant_solver_banner(self):
        """Asserts Socratic AI instant solver banner exists with 1-click drawer summon."""
        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("যেকোনো প্রশ্নের ছবি তুলুন বা লিখুন", content)
        self.assertIn("সক্রেটিক টিউটর চালু করুন", content)
        self.assertIn("global-socratic-trigger", content)

    def test_08_w3c_proof_of_skill_certificate_showcase(self):
        """Asserts W3C certificate showcase renders certificate card and social share triggers."""
        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("ProofOfSkillCard", content)
        self.assertIn("SocialShareButtons", content)
        self.assertIn("OGRO-2026-F982A1B4", content)
        self.assertIn("তানজিম হাসান", content)
        self.assertIn("/verify/", content)

    def test_09_official_trust_and_payment_bar(self):
        """Asserts official bKash and Nagad payment trust badges are present."""
        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("bKash Verified", content)
        self.assertIn("Nagad Verified", content)
        self.assertIn("SSLCommerz", content)

    def test_10_zero_emoji_and_architecture_notes(self):
        """Enforces platform Zero-Emoji policy and Developer Architecture Notes header."""
        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]"
        )

        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()
            emojis = emoji_pattern.findall(content)
            self.assertEqual(len(emojis), 0, f"Zero-Emoji policy violation in index.tsx: {emojis}")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)


if __name__ == "__main__":
    unittest.main()
