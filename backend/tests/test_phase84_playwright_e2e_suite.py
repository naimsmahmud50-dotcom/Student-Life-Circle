"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE - PHASE 84 PLAYWRIGHT E2E VERIFICATION SUITE:
MODULE:    Automated Test Suite for Playwright E2E Configuration & Journey Validation
TOPIC:     Multi-Browser & Mobile Emulation, Zero-Emoji Governance & E2E Resiliency
FILE:      backend/tests/test_phase84_playwright_e2e_suite.py
PURPOSE:   Provides exhaustive automated verification of Phase 84 deliverables:
           1. Playwright Test runner configuration (Chromium, Firefox, WebKit, Pixel 7, iPhone 14)
           2. End-to-end user journeys (auth, quiz offline-to-online, tuition escrow, 69 modules)
           3. Minimum 44px+ touch-target ergonomics (WCAG 2.2 AA)
           4. Strict Zero-Emoji compliance (0 emojis across all files)
           5. Prominent Developer Architecture Notes on every created or modified file
           6. Self-contained HTML evidence report and JSON telemetry generation
AUDIENCE:  QA Engineers, CI/CD Architects, Security Reviewers & System Auditors
STANDARDS: UI/UX Pro Max, OWASP Zero-IDOR, Strict Zero-Emoji Governance
========================================================================================
"""

import unittest
import os
import json
import re
from pathlib import Path

# Strict Zero-Emoji Regex covering Unicode emojis, symbols, and dingbats
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF\U0001FA70-\U0001FAFF]"
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = REPO_ROOT / "frontend"
E2E_DIR = FRONTEND_DIR / "e2e"
SCRIPTS_DIR = FRONTEND_DIR / "scripts"
REPORT_DIR = FRONTEND_DIR / "playwright-report"


class TestPhase84PlaywrightE2ESuite(unittest.TestCase):
    """
    Automated verification suite validating Phase 84 Playwright test automation deliverables.
    """

    def test_playwright_config_files_exist_and_configured(self):
        """
        Verify that both frontend/playwright.config.ts and root playwright.config.ts exist.
        """
        frontend_cfg = FRONTEND_DIR / "playwright.config.ts"
        root_cfg = REPO_ROOT / "playwright.config.ts"

        self.assertTrue(frontend_cfg.exists(), "frontend/playwright.config.ts must exist")
        self.assertTrue(root_cfg.exists(), "Root playwright.config.ts must exist")

        content = frontend_cfg.read_text(encoding="utf-8")

        # Verify browser and mobile project definitions
        self.assertIn("'chromium'", content)
        self.assertIn("'firefox'", content)
        self.assertIn("'webkit'", content)
        self.assertIn("'mobile-pixel-7'", content)
        self.assertIn("'mobile-iphone-14'", content)

        # Verify mobile viewports
        self.assertIn("width: 412", content)
        self.assertIn("height: 915", content)
        self.assertIn("width: 390", content)
        self.assertIn("height: 844", content)

        # Verify webServer and reporters
        self.assertIn("webServer", content)
        self.assertIn("playwright-report", content)

    def test_package_json_dependencies_and_scripts(self):
        """
        Verify that frontend/package.json contains @playwright/test and e2e test scripts.
        """
        pkg_file = FRONTEND_DIR / "package.json"
        self.assertTrue(pkg_file.exists(), "frontend/package.json must exist")

        with open(pkg_file, "r", encoding="utf-8") as f:
            pkg_data = json.load(f)

        # DevDependencies
        dev_deps = pkg_data.get("devDependencies", {})
        self.assertIn("@playwright/test", dev_deps)

        # Scripts
        scripts = pkg_data.get("scripts", {})
        self.assertIn("test:e2e", scripts)
        self.assertIn("test:e2e:ui", scripts)
        self.assertIn("test:e2e:report", scripts)

    def test_e2e_specs_and_helpers_exist(self):
        """
        Verify all 4 core journey specs and helper fixtures exist.
        """
        required_files = [
            E2E_DIR / "helpers" / "e2e-fixtures.ts",
            E2E_DIR / "auth_journey.spec.ts",
            E2E_DIR / "quiz_journey.spec.ts",
            E2E_DIR / "tuition_marketplace.spec.ts",
            E2E_DIR / "module_directory.spec.ts",
        ]

        for file_path in required_files:
            self.assertTrue(file_path.exists(), f"File {file_path.name} must exist under frontend/e2e/")

    def test_auth_journey_spec_invariants(self):
        """
        Verify auth_journey.spec.ts contains required minor protection and stage selection assertions.
        """
        spec = (E2E_DIR / "auth_journey.spec.ts").read_text(encoding="utf-8")
        self.assertIn("TC-AUTH-01", spec)
        self.assertIn("TC-AUTH-02", spec)
        self.assertIn("TC-AUTH-03", spec)
        self.assertIn("TC-AUTH-04", spec)
        self.assertIn("শিশু ও অপ্রাপ্তবয়স্ক সুরক্ষা", spec)
        self.assertIn("Pixel 7", spec)

    def test_quiz_journey_spec_invariants(self):
        """
        Verify quiz_journey.spec.ts tests 44px+ touch targets, offline disconnect, and mistake replay.
        """
        spec = (E2E_DIR / "quiz_journey.spec.ts").read_text(encoding="utf-8")
        self.assertIn("TC-QUIZ-01", spec)
        self.assertIn("TC-QUIZ-02", spec)
        self.assertIn("TC-QUIZ-03", spec)
        self.assertIn("TC-QUIZ-04", spec)
        self.assertIn("toBeGreaterThanOrEqual(44)", spec)
        self.assertIn("setOffline(true)", spec)
        self.assertIn("অফলাইন বাফার", spec)
        self.assertIn("অনলাইন সিঙ্কড", spec)
        self.assertIn("রিভিশন কিউ-তে যুক্ত হয়েছে", spec)

    def test_tuition_marketplace_spec_invariants(self):
        """
        Verify tuition_marketplace.spec.ts tests privacy masking and bilateral consent.
        """
        spec = (E2E_DIR / "tuition_marketplace.spec.ts").read_text(encoding="utf-8")
        self.assertIn("TC-TUI-01", spec)
        self.assertIn("TC-TUI-02", spec)
        self.assertIn("TC-TUI-03", spec)
        self.assertIn("TC-TUI-04", spec)
        self.assertIn("০১৭*** (দ্বিপাক্ষিক লক)", spec)
        self.assertIn("আবেদন ও যোগাযোগ সম্মতি", spec)
        self.assertIn("দ্বিপাক্ষিক অনুমোদন নীতি", spec)

    def test_module_directory_spec_invariants(self):
        """
        Verify module_directory.spec.ts tests dual perspective (core vs 69) and zero JS errors.
        """
        spec = (E2E_DIR / "module_directory.spec.ts").read_text(encoding="utf-8")
        self.assertIn("TC-MOD-01", spec)
        self.assertIn("TC-MOD-02", spec)
        self.assertIn("TC-MOD-03", spec)
        self.assertIn("TC-MOD-04", spec)
        self.assertIn("TC-MOD-05", spec)
        self.assertIn("কোর হাব (Tabs 1-5)", spec)
        self.assertIn("সমস্ত মডিউল (Tabs 1-69)", spec)
        self.assertIn("assertZeroErrors()", spec)

    def test_e2e_runner_generates_html_report_and_json_results(self):
        """
        Verify that frontend/scripts/run-e2e.py executes and generates the HTML report and JSON results.
        """
        runner_file = SCRIPTS_DIR / "run-e2e.py"
        self.assertTrue(runner_file.exists(), "frontend/scripts/run-e2e.py must exist")

        # Run the runner module directly
        import importlib.util
        spec = importlib.util.spec_from_file_location("run_e2e", runner_file)
        run_e2e = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run_e2e)

        results = run_e2e.run_e2e_verification()
        run_e2e.generate_html_report(results)

        self.assertEqual(results["failed_tests"], 0)
        self.assertEqual(results["total_tests"], 85)
        self.assertEqual(results["passed_tests"], 85)
        self.assertEqual(results["zero_emoji_audit"], "100% COMPLIANT")

        # Check output HTML file
        html_file = REPORT_DIR / "index.html"
        json_file = REPORT_DIR / "test-results.json"
        self.assertTrue(html_file.exists(), "playwright-report/index.html must be generated")
        self.assertTrue(json_file.exists(), "playwright-report/test-results.json must be generated")

        html_text = html_file.read_text(encoding="utf-8")
        self.assertIn("অগ্রযাত্রা - Playwright E2E অডিট ও এভিডেন্স রিপোর্ট", html_text)
        self.assertIn("85 টি", html_text)
        self.assertIn("100%", html_text)

    def test_strict_zero_emoji_compliance_across_all_phase84_files(self):
        """
        Strictly assert zero emojis across all Phase 84 files, configs, scripts, and reports.
        """
        phase84_files = [
            FRONTEND_DIR / "playwright.config.ts",
            REPO_ROOT / "playwright.config.ts",
            E2E_DIR / "helpers" / "e2e-fixtures.ts",
            E2E_DIR / "auth_journey.spec.ts",
            E2E_DIR / "quiz_journey.spec.ts",
            E2E_DIR / "tuition_marketplace.spec.ts",
            E2E_DIR / "module_directory.spec.ts",
            SCRIPTS_DIR / "run-e2e.py",
            REPORT_DIR / "index.html",
        ]

        for file_path in phase84_files:
            if not file_path.exists():
                continue
            content = file_path.read_text(encoding="utf-8")
            emojis = EMOJI_PATTERN.findall(content)
            self.assertEqual(
                emojis,
                [],
                f"Strict Zero-Emoji Violation in {file_path.name}: Found emojis {emojis}"
            )

    def test_developer_architecture_notes_present_on_all_files(self):
        """
        Verify that every newly created Phase 84 file includes a prominent Developer Architecture Note at the top.
        """
        files_to_check = [
            FRONTEND_DIR / "playwright.config.ts",
            REPO_ROOT / "playwright.config.ts",
            E2E_DIR / "helpers" / "e2e-fixtures.ts",
            E2E_DIR / "auth_journey.spec.ts",
            E2E_DIR / "quiz_journey.spec.ts",
            E2E_DIR / "tuition_marketplace.spec.ts",
            E2E_DIR / "module_directory.spec.ts",
            SCRIPTS_DIR / "run-e2e.py",
        ]

        for file_path in files_to_check:
            self.assertTrue(file_path.exists(), f"File {file_path.name} must exist")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"File {file_path.name} must begin with a DEVELOPER ARCHITECTURE NOTE"
            )


if __name__ == "__main__":
    unittest.main()
