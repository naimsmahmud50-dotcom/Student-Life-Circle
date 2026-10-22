"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Suite for Nationwide Live Exam & Playwright E2E
TOPIC:     Phase 125 Nationwide Live Exam & Playwright E2E Journey
FILE:      backend/tests/test_phase125_nationwide_live_exam.py
PHASE:     Phase 125 - Nationwide Live Exam & Playwright E2E Journey
PURPOSE:   Automated unit, integration, and compliance tests verifying Playwright E2E
           test configuration, end-to-end exam journey specifications (TC-NAT-01 to
           TC-NAT-06), k6 distributed load profile and sub-second SLAs, tactile 3D
           button aesthetics, and strict zero-emoji mandate.
STANDARDS: Playwright Headless Standards, Sub-second Latency, Strict Zero-Emoji, WCAG 2.2 AAA
========================================================================================
"""

import json
import os
import re
import unittest
from pathlib import Path

# Comprehensive Strict Zero-Emoji Regex covering Unicode emojis, pictographs, and symbols
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase125NationwideLiveExam(unittest.TestCase):
    """
    Automated verification suite validating Phase 125 Nationwide Live Exam & Playwright E2E.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.playwright_cfg = cls.root_dir / "frontend" / "playwright.config.ts"
        cls.e2e_spec = cls.root_dir / "frontend" / "e2e" / "nationwide_exam_journey.spec.ts"
        cls.k6_script = cls.root_dir / "tests" / "load" / "k6_national_exam.js"
        cls.test_file = Path(__file__).resolve()

        cls.target_files = [
            cls.playwright_cfg,
            cls.e2e_spec,
            cls.k6_script,
            cls.test_file,
        ]

    def test_target_files_exist_and_headers_valid(self):
        """
        Verify all 4 Phase 125 target files exist and contain standardized Developer Architecture Note.
        """
        for file_path in self.target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"Missing Developer Architecture Note header in {file_path.name}",
            )
            self.assertIn(
                "Phase 125 - Nationwide Live Exam & Playwright E2E Journey",
                content,
                f"Missing Phase 125 identifier in {file_path.name}",
            )
            self.assertIn(
                "Zero-Emoji",
                content,
                f"Missing Zero-Emoji declaration in {file_path.name}",
            )

    def test_playwright_config_structure(self):
        """
        Verify frontend/playwright.config.ts configures headless execution, multi-browser matrix,
        mobile viewports, and report artifacts.
        """
        content = self.playwright_cfg.read_text(encoding="utf-8")

        # Headless mode
        self.assertIn("headless: true", content)

        # Multi-browser & mobile viewport project definitions
        self.assertIn("'chromium'", content)
        self.assertIn("'firefox'", content)
        self.assertIn("'webkit'", content)
        self.assertIn("'mobile-pixel-7'", content)
        self.assertIn("'mobile-iphone-14'", content)

        # Mobile viewport specifications
        self.assertIn("width: 412", content)
        self.assertIn("height: 915", content)
        self.assertIn("width: 390", content)
        self.assertIn("height: 844", content)

        # Reporters
        self.assertIn("html", content)
        self.assertIn("json", content)
        self.assertIn("playwright-report", content)

    def test_e2e_nationwide_exam_journey_coverage(self):
        """
        Verify frontend/e2e/nationwide_exam_journey.spec.ts covers all required user journeys.
        """
        content = self.e2e_spec.read_text(encoding="utf-8")

        # 6 Test Cases defined
        for i in range(1, 7):
            self.assertIn(f"TC-NAT-0{i}", content, f"Missing test case TC-NAT-0{i}")

        # TC-NAT-01: Auth & SMS OTP verification
        self.assertIn("ওটিপি পাঠান", content)
        self.assertIn("৬ ডিজিট ওটিপি", content)
        self.assertIn("যাচাই করুন", content)
        self.assertIn("ওটিপি যাচাই সম্পন্ন হয়েছে", content)

        # TC-NAT-02: Live Challenge Arena & Timer
        self.assertIn("জাতীয় স্টেম অলিম্পিয়াড ২০২৬", content)
        self.assertIn("নেগেটিভ মার্কিং: -০.২৫", content)
        self.assertIn("সার্ভার-অথরিটেটিভ টাইমার", content)
        self.assertIn("পরীক্ষায় অংশগ্রহণ করুন", content)

        # TC-NAT-03: NCTB HSC Physics with KaTeX
        self.assertIn("একটি বস্তুর ভর", content)
        self.assertIn("সঠিক উত্তর!", content)
        self.assertIn("নিউটনের ২য় সূত্র", content)

        # TC-NAT-04: Network Disconnect & Local Buffer
        self.assertIn("setOffline(true)", content)
        self.assertIn("অফলাইন বাফার", content)
        self.assertIn("setOffline(false)", content)
        self.assertIn("অনলাইন সিঙ্কড", content)

        # TC-NAT-05: Tactile Submission & X-Idempotency-Key
        self.assertIn("খাতা জমা দিন", content)
        self.assertIn("x-idempotency-key", content)
        self.assertIn("টপ ১% জাতীয় মেধা", content)
        self.assertIn("সক্রেটিক বিশ্লেষণ ও পারফরম্যান্স ব্রেকডাউন", content)

        # TC-NAT-06: Mobile Ergonomics & Zero Horizontal Overflow
        self.assertIn("Pixel 7", content)
        self.assertIn("iPhone 14", content)
        self.assertIn("scrollWidth", content)
        self.assertIn("clientWidth", content)
        self.assertIn("toBeGreaterThanOrEqual(44)", content)

    def test_k6_load_test_profile_and_thresholds(self):
        """
        Verify tests/load/k6_national_exam.js defines sub-second latency thresholds and stages.
        """
        content = self.k6_script.read_text(encoding="utf-8")

        # Sub-second latency SLA thresholds
        self.assertIn("p(95)<200", content)
        self.assertIn("p(99)<500", content)
        self.assertIn("rate<0.01", content)

        # Distributed stages
        self.assertIn("stages", content)
        self.assertIn("duration", content)
        self.assertIn("target", content)

        # Idempotency and live exam endpoint simulation
        self.assertIn("X-Idempotency-Key", content)
        self.assertIn("/api/v1/exam/national/answer", content)

    def test_strict_zero_emoji_compliance(self):
        """
        Verify 100% Zero-Emoji policy across all Phase 125 target files.
        """
        for file_path in self.target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(
                matches,
                [],
                f"Strict Zero-Emoji violation in {file_path.name}: Found emojis {matches}",
            )

    def test_tactile_3d_button_styling_in_practice_page(self):
        """
        Verify practice page and live challenge page use tactile 3D physical ledge styling.
        """
        practice_file = self.root_dir / "frontend" / "src" / "pages" / "practice.tsx"
        self.assertTrue(practice_file.exists())
        content = practice_file.read_text(encoding="utf-8")

        # 3D physical ledge depth and active compression classes
        self.assertIn("shadow-[0_4px_0_0_", content)
        self.assertIn("active:translate-y-1", content)
        self.assertIn("active:shadow-none", content)

        # Verify KaTeX renderer and Server timer integrations
        self.assertIn("<KaTeXRenderer", content)
        self.assertIn("<ServerTimer", content)


if __name__ == "__main__":
    unittest.main()
