"""
Test Suite for Phase 98.3: Unified Sub-Pages Architecture (Task T658)
====================================================================
Verifies that all 6 core sub-pages:
  1. frontend/src/pages/learn.tsx
  2. frontend/src/pages/practice.tsx
  3. frontend/src/pages/live-challenge.tsx
  4. frontend/src/pages/admission.tsx
  5. frontend/src/pages/tuition.tsx
  6. frontend/src/pages/career.tsx

comply with:
  - Unified Navbar and 4-tier Footer integration.
  - Page-specific interactive feature completeness.
  - Strict Zero-Emoji Policy across all source files.
  - Mandatory DEVELOPER ARCHITECTURE NOTES.
  - Zero Layout Shift (CLS = 0.000) skeleton loading state compliance.
"""

import os
import re
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PAGES_DIR = os.path.join(BASE_DIR, "frontend", "src", "pages")


class TestPhase983UnifiedSubPages(unittest.TestCase):

    def setUp(self):
        self.subpages = [
            "learn.tsx",
            "practice.tsx",
            "live-challenge.tsx",
            "admission.tsx",
            "tuition.tsx",
            "career.tsx"
        ]
        self.page_contents = {}
        for page in self.subpages:
            path = os.path.join(PAGES_DIR, page)
            self.assertTrue(os.path.exists(path), f"File {page} must exist at {path}")
            with open(path, "r", encoding="utf-8") as f:
                self.page_contents[page] = f.read()

    def test_all_pages_import_and_render_navbar_and_footer(self):
        """Verify that all 6 sub-pages wrap within standard Navbar and Footer."""
        for page in self.subpages:
            content = self.page_contents[page]
            self.assertIn("Navbar", content, f"{page} must import Navbar.")
            self.assertIn("<Navbar", content, f"{page} must render <Navbar JSX tag.")
            self.assertIn("Footer", content, f"{page} must import Footer.")
            self.assertIn("<Footer", content, f"{page} must render <Footer JSX tag.")

    def test_strict_zero_emoji_policy(self):
        """Assert zero emojis in all 6 sub-page files."""
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        for page in self.subpages:
            content = self.page_contents[page]
            matches = emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"{page} violates strict Zero-Emoji policy with emojis: {matches}"
            )

    def test_developer_architecture_notes(self):
        """Assert every page starts with a prominent DEVELOPER ARCHITECTURE NOTE."""
        for page in self.subpages:
            content = self.page_contents[page]
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content[:600],
                f"{page} must feature a prominent DEVELOPER ARCHITECTURE NOTE."
            )

    def test_learn_page_interactive_elevations(self):
        """Verify learn.tsx includes circular progress gauges, HLS video player, and revision queue."""
        content = self.page_contents["learn.tsx"]
        self.assertIn("HlsLecturePlayer", content, "learn.tsx must integrate HlsLecturePlayer modal.")
        self.assertIn("স্পেসড-রিপিটিশন রিভিশন কিউ", content, "learn.tsx must provide spaced-repetition revision queue.")
        self.assertIn("রিভিশন কুইজ শুরু করুন", content, "learn.tsx must provide revision quiz CTA.")
        self.assertIn("strokeDasharray", content, "learn.tsx must provide circular SVG progress meters.")
        self.assertIn("animate-pulse", content, "learn.tsx must feature skeleton loading.")

    def test_practice_page_interactive_elevations(self):
        """Verify practice.tsx includes KaTeX formulas, server timer, and Socratic hints."""
        content = self.page_contents["practice.tsx"]
        self.assertIn("KaTeXRenderer", content, "practice.tsx must render mathematical formulas.")
        self.assertIn("ServerTimer", content, "practice.tsx must render server-synchronized timer.")
        self.assertIn("formatTimer", content, "practice.tsx must provide formatTimer helper.")
        self.assertIn("Socratic Hint", content, "practice.tsx must provide Socratic AI hint trigger.")
        self.assertIn("useQuizStore", content, "practice.tsx must integrate useQuizStore.")
        self.assertIn("useFilterStore", content, "practice.tsx must integrate useFilterStore.")
        self.assertIn("animate-pulse", content, "practice.tsx must feature skeleton loading.")

    def test_live_challenge_page_interactive_elevations(self):
        """Verify live-challenge.tsx includes live participants, server timer, and buffer."""
        content = self.page_contents["live-challenge.tsx"]
        self.assertIn("registeredCount", content, "live-challenge.tsx must track live participant count.")
        self.assertIn("প্রতিযোগী শিক্ষার্থী লাইভ", content, "live-challenge.tsx must show live participant banner.")
        self.assertIn("মিলি-সেকেন্ড একুরেট বাফার", content, "live-challenge.tsx must have millisecond buffer.")
        self.assertIn("apiClient.getLiveChallenges", content, "live-challenge.tsx must call getLiveChallenges.")
        self.assertIn("apiClient.getLiveLeaderboard", content, "live-challenge.tsx must call getLiveLeaderboard.")
        self.assertIn("animate-pulse", content, "live-challenge.tsx must feature skeleton loading.")

    def test_admission_page_interactive_elevations(self):
        """Verify admission.tsx includes DU Ka, BUET, Medical, negative marking, and cut-off meters."""
        content = self.page_contents["admission.tsx"]
        self.assertIn("target_du", content, "admission.tsx must feature DU Ka target.")
        self.assertIn("target_buet", content, "admission.tsx must feature BUET target.")
        self.assertIn("target_medical", content, "admission.tsx must feature Medical target.")
        self.assertIn("negativeMarking", content, "admission.tsx must display negative marking blueprint.")
        self.assertIn("-০.২৫", content, "admission.tsx must display -0.25 negative marking badge.")
        self.assertIn("probabilityPercent", content, "admission.tsx must display cut-off probability meter.")
        self.assertIn("apiClient.getAdmissionTests", content, "admission.tsx must call getAdmissionTests.")
        self.assertIn("animate-pulse", content, "admission.tsx must feature skeleton loading.")

    def test_tuition_page_interactive_elevations(self):
        """Verify tuition.tsx includes verified teacher cards, thana filters, and escrow milestone flow."""
        content = self.page_contents["tuition.tsx"]
        self.assertIn("isVerifiedTutor", content, "tuition.tsx must support verified teacher status.")
        self.assertIn("selectedThana", content, "tuition.tsx must support thana filtering.")
        self.assertIn("ধানমন্ডি", content, "tuition.tsx must include thana options like Dhanmondi.")
        self.assertIn("escrowEligible", content, "tuition.tsx must support escrow milestone flow.")
        self.assertIn("এসক্রো মাইলস্টোন", content, "tuition.tsx must display escrow milestone policy.")
        self.assertIn("requestTuitionConsent", content, "tuition.tsx must call requestTuitionConsent.")
        self.assertIn("Modal", content, "tuition.tsx must use Radix Modal wrapper.")
        self.assertIn("animate-pulse", content, "tuition.tsx must feature skeleton loading.")

    def test_career_page_interactive_elevations(self):
        """Verify career.tsx includes sealed cryptographic CV snapshots and application pipeline."""
        content = self.page_contents["career.tsx"]
        self.assertIn("latestSealedSnapshot", content, "career.tsx must feature sealed cryptographic CV snapshot builder.")
        self.assertIn("cvSnapshotId", content, "career.tsx must display immutable CV snapshot hashes.")
        self.assertIn("SHORTLISTED", content, "career.tsx must feature application pipeline stages.")
        self.assertIn("apiClient.getCareerProfile", content, "career.tsx must call getCareerProfile.")
        self.assertIn("animate-pulse", content, "career.tsx must feature skeleton loading.")


if __name__ == "__main__":
    unittest.main()
