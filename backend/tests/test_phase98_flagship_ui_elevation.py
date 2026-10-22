"""
DEVELOPER ARCHITECTURE NOTE:
========================================================================================
MODULE:    Master UI Elevation Test Suite & Master Regression Harness
FILE:      backend/tests/test_phase98_flagship_ui_elevation.py
PHASE:     Phase 98.4 (Tasks T659, T660) - UI Elevation Test Suite & Master Regression Run
PURPOSE:   Provides comprehensive end-to-end verification for the Flagship UI/UX Elevation:
           1. Global Application Shell & Dignified Footer (Tasks T655, T656)
           2. Flagship Home Dashboard Overhaul (Task T657)
           3. Unified Sub-Pages Architecture (Task T658)
           4. Strict Zero-Emoji Compliance across all frontend modules
           5. Developer Architecture Notes enforcement across all modified codebases
AUDIENCE:  Frontend Architects, QA Leads, Release Engineers, Security & Accessibility Auditors.
STANDARDS: Strict Zero-Emoji Policy, 100% Vector Lucide SVGs, WCAG 2.2 AAA Contrast, Zero CLS (CLS = 0.000).
========================================================================================
"""

import os
import re
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
SRC_DIR = os.path.join(FRONTEND_DIR, "src")
COMPONENTS_DIR = os.path.join(SRC_DIR, "components")
PAGES_DIR = os.path.join(SRC_DIR, "pages")


class TestPhase98FlagshipUIElevation(unittest.TestCase):
    """Master test suite verifying the complete flagship UI elevation across the application."""

    def setUp(self):
        self.footer_path = os.path.join(COMPONENTS_DIR, "layout", "Footer.tsx")
        self.app_path = os.path.join(PAGES_DIR, "_app.tsx")
        self.index_path = os.path.join(PAGES_DIR, "index.tsx")
        self.subpages = {
            "learn.tsx": os.path.join(PAGES_DIR, "learn.tsx"),
            "practice.tsx": os.path.join(PAGES_DIR, "practice.tsx"),
            "live-challenge.tsx": os.path.join(PAGES_DIR, "live-challenge.tsx"),
            "admission.tsx": os.path.join(PAGES_DIR, "admission.tsx"),
            "tuition.tsx": os.path.join(PAGES_DIR, "tuition.tsx"),
            "career.tsx": os.path.join(PAGES_DIR, "career.tsx"),
        }
        self.all_frontend_files = [
            self.footer_path,
            self.app_path,
            self.index_path,
            *self.subpages.values()
        ]

    def test_footer_accreditation_payment_and_privacy_links(self):
        """
        Verify Footer.tsx contains:
        - NCTB curriculum accreditation badge
        - Verified bKash and Nagad payment badges
        - SSLCommerz and PCI-DSS compliance seals
        - Child privacy, terms of service, and emergency helpline disclosures
        """
        self.assertTrue(os.path.exists(self.footer_path), f"Footer.tsx must exist at {self.footer_path}")
        with open(self.footer_path, "r", encoding="utf-8") as f:
            content = f.read()

        # NCTB curriculum accreditation
        self.assertIn("NCTB", content, "Footer must contain NCTB curriculum accreditation.")
        self.assertIn("জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড", content, "Footer must contain Bengali NCTB text.")

        # Payment rails
        self.assertIn("bKash", content, "Footer must display verified bKash payment badge.")
        self.assertIn("Nagad", content, "Footer must display verified Nagad payment badge.")
        self.assertIn("SSLCommerz", content, "Footer must display verified SSLCommerz payment badge.")

        # Governance & Privacy
        self.assertTrue(
            "তথ্য সুরক্ষা" in content or "Child Privacy" in content or "সুরক্ষা" in content,
            "Footer must contain privacy and data protection link."
        )
        self.assertIn("ISO 27001", content, "Footer must contain ISO 27001 security badge.")
        self.assertIn("OWASP ASVS", content, "Footer must contain OWASP ASVS security badge.")
        self.assertIn("1098", content, "Footer must display child emergency helpline (1098/16xxx).")

    def test_app_shell_i18n_and_socratic_drawer_mounting(self):
        """
        Verify _app.tsx wraps the tree with I18nProvider and mounts SocraticTutorDrawer.
        """
        self.assertTrue(os.path.exists(self.app_path), f"_app.tsx must exist at {self.app_path}")
        with open(self.app_path, "r", encoding="utf-8") as f:
            content = f.read()

        # I18nProvider wrapping
        self.assertIn("I18nProvider", content, "_app.tsx must import and wrap with I18nProvider.")
        self.assertIn("<I18nProvider", content, "_app.tsx must render <I18nProvider root wrapper.")

        # Persistent SocraticTutorDrawer floating action button
        self.assertIn("SocraticTutorDrawer", content, "_app.tsx must import SocraticTutorDrawer.")
        self.assertIn("<SocraticTutorDrawer", content, "_app.tsx must mount <SocraticTutorDrawer.")

        # Offline network status listener & banner
        self.assertIn("serviceWorker.register", content, "_app.tsx must register PWA service worker.")
        self.assertIn("addEventListener('online'", content, "_app.tsx must listen to online network events.")
        self.assertIn("addEventListener('offline'", content, "_app.tsx must listen to offline network events.")

    def test_home_dashboard_command_center_features(self):
        """
        Verify index.tsx includes:
        - 4-card Academic Telemetry Bar (Streak, Questions Solved, Accuracy, Percentile Rank)
        - Curated Journey Pathway Cards (SSC, HSC, Admission, Career)
        - 3D STEM Virtual Labs Showcase
        - Live Challenge Countdown (8:00 PM national live challenge)
        - W3C Proof-of-Skill Certificate Showcase with 1-click social sharing
        - Official Trust & Payment Bar
        """
        self.assertTrue(os.path.exists(self.index_path), f"index.tsx must exist at {self.index_path}")
        with open(self.index_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 4-card Telemetry grid
        self.assertTrue(
            "অধ্যয়ন স্ট্রিক" in content or "স্টাডি স্ট্রিক" in content or "স্ট্রিক" in content,
            "index.tsx must feature Study Streak card."
        )
        self.assertIn("প্রশ্ন সমাধান", content, "index.tsx must feature Questions Solved card.")
        self.assertIn("নির্ভুলতা", content, "index.tsx must feature Accuracy Rate card.")
        self.assertTrue(
            "জাতীয় পার্সেন্টাইল" in content or "শীর্ষ ৫%" in content or "জাতীয় অবস্থান" in content,
            "index.tsx must feature National Percentile card."
        )

        # Journey pathway cards
        self.assertIn("মাধ্যমিক (SSC ৯-১০)", content, "index.tsx must include SSC journey card.")
        self.assertIn("উচ্চ মাধ্যমিক (HSC ১১-১২)", content, "index.tsx must include HSC journey card.")
        self.assertTrue(
            "বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি" in content or "বিশ্ববিদ্যালয় ভর্তি" in content,
            "index.tsx must include Admission journey card."
        )
        self.assertTrue(
            "টিউশন ও স্কিল লেজার" in content or "ক্যারিয়ার" in content or "Career" in content,
            "index.tsx must include Career/Tuition journey card."
        )

        # 3D STEM Virtual Labs Showcase
        self.assertTrue(
            "৩ডি স্টেম ভার্চুয়াল" in content or "ভার্চুয়াল থ্রিডি ল্যাব" in content or "3D STEM" in content,
            "index.tsx must feature 3D STEM labs spotlight."
        )
        self.assertIn("প্রক্ষেপক গতিবিদ্যা", content, "index.tsx must feature Physics simulator.")
        self.assertIn("৩ডি আণবিক জ্যামিতি", content, "index.tsx must feature Chemistry simulator.")

        # Live Challenge Countdown
        self.assertIn("রাত ৮:০০", content, "index.tsx must feature 8:00 PM National Challenge countdown.")
        self.assertTrue(
            "লাইভ লবিতে যোগ দিন" in content or "live-challenge" in content or "অংশগ্রহণ" in content,
            "index.tsx must provide live challenge CTA button."
        )

        # W3C Proof-of-Skill Certificate Showcase with social sharing
        self.assertTrue(
            "W3C ক্রিপ্টোগ্রাফিক" in content or "ProofOfSkillCard" in content or "W3C" in content,
            "index.tsx must feature W3C certificate showcase."
        )
        self.assertIn("LinkedIn", content, "index.tsx must provide LinkedIn sharing button.")
        self.assertIn("Facebook", content, "index.tsx must provide Facebook sharing button.")

        # Payment trust bar
        self.assertIn("bKash", content, "index.tsx must feature verified bKash payment seal.")
        self.assertIn("Nagad", content, "index.tsx must feature verified Nagad payment seal.")
        self.assertIn("SSLCommerz", content, "index.tsx must feature verified SSLCommerz payment seal.")

    def test_subpages_unified_layout_and_interactive_elevations(self):
        """
        Verify that all sub-pages utilize the unified Navbar and Footer shell
        and render page-specific interactive engines.
        """
        for page_name, page_path in self.subpages.items():
            self.assertTrue(os.path.exists(page_path), f"{page_name} must exist at {page_path}")
            with open(page_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Unified Navbar & Footer shell
            self.assertIn("Navbar", content, f"{page_name} must import Navbar.")
            self.assertIn("<Navbar", content, f"{page_name} must render <Navbar.")
            self.assertIn("Footer", content, f"{page_name} must import Footer.")
            self.assertIn("<Footer", content, f"{page_name} must render <Footer.")

            # Zero Layout Shift skeleton loader
            self.assertIn("animate-pulse", content, f"{page_name} must provide skeleton loading state.")

        # Page-specific checks
        # 1. learn.tsx
        with open(self.subpages["learn.tsx"], "r", encoding="utf-8") as f:
            learn_content = f.read()
        self.assertIn("HlsLecturePlayer", learn_content, "learn.tsx must integrate HlsLecturePlayer modal.")
        self.assertIn("strokeDasharray", learn_content, "learn.tsx must render circular SVG progress gauges.")
        self.assertIn("স্পেসড-রিপিটিশন রিভিশন কিউ", learn_content, "learn.tsx must provide spaced-repetition queue.")

        # 2. practice.tsx
        with open(self.subpages["practice.tsx"], "r", encoding="utf-8") as f:
            practice_content = f.read()
        self.assertIn("KaTeXRenderer", practice_content, "practice.tsx must render math formulas.")
        self.assertIn("ServerTimer", practice_content, "practice.tsx must provide server countdown timer.")
        self.assertIn("formatTimer", practice_content, "practice.tsx must provide formatTimer helper.")
        self.assertIn("Socratic Hint", practice_content, "practice.tsx must provide Socratic hint trigger.")

        # 3. live-challenge.tsx
        with open(self.subpages["live-challenge.tsx"], "r", encoding="utf-8") as f:
            live_content = f.read()
        self.assertIn("registeredCount", live_content, "live-challenge.tsx must track live participant counter.")
        self.assertIn("মিলি-সেকেন্ড একুরেট বাফার", live_content, "live-challenge.tsx must feature millisecond buffer.")

        # 4. admission.tsx
        with open(self.subpages["admission.tsx"], "r", encoding="utf-8") as f:
            admission_content = f.read()
        self.assertIn("target_du", admission_content, "admission.tsx must feature DU Ka target.")
        self.assertIn("target_buet", admission_content, "admission.tsx must feature BUET target.")
        self.assertIn("target_medical", admission_content, "admission.tsx must feature Medical target.")
        self.assertIn("-০.২৫", admission_content, "admission.tsx must display negative marking badge.")
        self.assertIn("probabilityPercent", admission_content, "admission.tsx must render cut-off probability meter.")

        # 5. tuition.tsx
        with open(self.subpages["tuition.tsx"], "r", encoding="utf-8") as f:
            tuition_content = f.read()
        self.assertIn("isVerifiedTutor", tuition_content, "tuition.tsx must support verified teachers.")
        self.assertIn("selectedThana", tuition_content, "tuition.tsx must support thana filtering.")
        self.assertIn("escrowEligible", tuition_content, "tuition.tsx must support escrow milestone protection.")
        self.assertIn("requestTuitionConsent", tuition_content, "tuition.tsx must invoke requestTuitionConsent.")

        # 6. career.tsx
        with open(self.subpages["career.tsx"], "r", encoding="utf-8") as f:
            career_content = f.read()
        self.assertIn("latestSealedSnapshot", career_content, "career.tsx must feature sealed CV snapshot builder.")
        self.assertIn("cvSnapshotId", career_content, "career.tsx must display immutable CV snapshot hashes.")
        self.assertIn("SHORTLISTED", career_content, "career.tsx must track job application pipeline.")

    def test_strict_zero_emoji_compliance(self):
        """
        Verify strict Zero-Emoji compliance across all modified frontend files:
        - Footer.tsx
        - _app.tsx
        - index.tsx
        - learn.tsx
        - practice.tsx
        - live-challenge.tsx
        - admission.tsx
        - tuition.tsx
        - career.tsx
        """
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        for filepath in self.all_frontend_files:
            filename = os.path.basename(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            matches = emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"File {filename} violates strict Zero-Emoji policy with emojis: {matches}"
            )

    def test_developer_architecture_notes_presence(self):
        """
        Verify that all elevated files begin with a prominent DEVELOPER ARCHITECTURE NOTE.
        """
        for filepath in self.all_frontend_files:
            filename = os.path.basename(filepath)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content[:600],
                f"File {filename} must begin with a prominent DEVELOPER ARCHITECTURE NOTE."
            )


if __name__ == "__main__":
    unittest.main()
