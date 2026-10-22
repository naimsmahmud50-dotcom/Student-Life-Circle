"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite for Grand Nationwide Rollout
TOPIC:     Phase 120 Grand Nationwide Rollout & Public Launch Sign-off
FILE:      backend/tests/test_phase120_grand_nationwide_rollout.py
PHASE:     Phase 120 - Grand Nationwide Rollout & Public Launch Sign-off
PURPOSE:   Automated verification test suite certifying production SRE health script,
           institutional About and Terms pages, National Launch Attestation completeness,
           unified router sub-router catalog, and zero-emoji compliance.
STANDARDS: OWASP ASVS L2, Production SRE Standards, Pure Academic Design, Strict Zero-Emoji
========================================================================================
"""

import os
import re
import subprocess
import unittest
from pathlib import Path


class TestPhase120GrandNationwideRollout(unittest.TestCase):
    """
    Test suite certifying Phase 120 Grand Nationwide Rollout & Public Launch Sign-off.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.deploy_script = cls.root_dir / "deploy.sh"
        cls.attestation_file = cls.root_dir / "NATIONAL_LAUNCH_ATTESTATION.md"
        cls.frontend_about = cls.root_dir / "frontend" / "src" / "pages" / "about.tsx"
        cls.frontend_terms = cls.root_dir / "frontend" / "src" / "pages" / "terms.tsx"
        cls.router_file = cls.root_dir / "backend" / "app" / "api" / "v1" / "router.py"

        cls.emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

    def test_01_deploy_sh_sre_health_execution(self):
        """Verifies ./deploy.sh health executes cleanly with exit code 0."""
        self.assertTrue(self.deploy_script.exists(), "deploy.sh must exist at repository root.")

        deploy_content = self.deploy_script.read_text(encoding="utf-8")
        self.assertIn("verify_preflight_architecture", deploy_content)
        self.assertIn("run_security_sweep.py", deploy_content)
        self.assertIn("run_zero_emoji_sweep.py", deploy_content)
        self.assertIn("run_supabase_security_audit.py", deploy_content)

        # Execute ./deploy.sh health in a subprocess
        result = subprocess.run(
            ["bash", str(self.deploy_script), "health"],
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            f"./deploy.sh health exited with non-zero code {result.returncode}. Output:\n{result.stderr}",
        )
        self.assertIn("All pre-flight architectural contracts verified successfully.", result.stdout)

    def test_02_institutional_about_page_integrity(self):
        """Verifies frontend/src/pages/about.tsx adheres to pure academic layout and pillars."""
        self.assertTrue(self.frontend_about.exists(), "about.tsx must exist.")
        content = self.frontend_about.read_text(encoding="utf-8")

        # Academic color palette tokens
        self.assertIn("#0A2540", content)
        self.assertIn("#FAFAF8", content)

        # Core architectural pillars
        self.assertIn("NCTB কারিকুলাম সামঞ্জস্য", content)
        self.assertIn("নজরদারি-মুক্ত পরীক্ষা হল", content)
        self.assertIn("প্রান্তিক অফলাইন মেশ", content)
        self.assertIn("পিয়ার-রিভিউ ট্রাইব্যুনাল", content)
        self.assertIn("১২০ টি", content)

        # Pure Lucide vector icons
        self.assertIn("ShieldCheck", content)
        self.assertIn("BookOpen", content)
        self.assertIn("Users", content)
        self.assertIn("Radio", content)
        self.assertIn("Lock", content)

    def test_03_institutional_terms_page_integrity(self):
        """Verifies frontend/src/pages/terms.tsx formal clauses and privacy protections."""
        self.assertTrue(self.frontend_terms.exists(), "terms.tsx must exist.")
        content = self.frontend_terms.read_text(encoding="utf-8")

        # Formal clauses
        self.assertIn("শিক্ষার্থী ডেটা সার্বভৌমত্ব ও ব্যক্তিগত সুরক্ষা", content)
        self.assertIn("নজরদারি-মুক্ত পরীক্ষা অখণ্ডতা ও প্রক্টরিং নিশ্চয়তা", content)
        self.assertIn("টিউশন ফি এসক্রো সুরক্ষা ও অভিভাবক ট্রাস্ট", content)
        self.assertIn("মেধা বৃত্তি ও নিরপেক্ষ ট্রাইব্যুনাল সালিশি", content)
        self.assertIn("অফলাইন পিয়ার-টু-পিয়ার শিক্ষাক্রম সমতা", content)

        # Pure Lucide icons
        self.assertIn("Scale", content)
        self.assertIn("ShieldCheck", content)
        self.assertIn("Lock", content)

    def test_04_national_launch_attestation_completeness(self):
        """Verifies NATIONAL_LAUNCH_ATTESTATION.md completeness and 120-phase sign-off."""
        self.assertTrue(self.attestation_file.exists(), "NATIONAL_LAUNCH_ATTESTATION.md must exist.")
        content = self.attestation_file.read_text(encoding="utf-8")

        self.assertIn("120 / 120 Phases", content)
        self.assertIn("1,384+", content)
        self.assertIn("WCAG 2.2 AAA", content)
        self.assertIn("Zero Facial Video Surveillance", content)
        self.assertIn("Oxford Academic Navy", content)
        self.assertIn("Production Sovereign Educational Operating System", content)

    def test_05_endpoint_catalog_completeness(self):
        """Verifies that all core endpoint modules are imported and mounted in router.py."""
        self.assertTrue(self.router_file.exists(), "router.py must exist.")
        router_content = self.router_file.read_text(encoding="utf-8")

        expected_routers = [
            "counseling_router",
            "guardian_console_router",
            "talent_pipeline_router",
            "board_archives_router",
            "scholarships_router",
            "institution_router",
            "exam_hall_router",
            "moderation_router",
            "knowledge_graph_router",
            "offline_sync_router",
        ]

        for r in expected_routers:
            self.assertIn(r, router_content, f"Router '{r}' is missing from router.py.")

    def test_06_architecture_notes_and_zero_emoji_enforcement(self):
        """Verifies Developer Architecture Notes and strict zero emojis across Phase 120 files."""
        files_to_check = [
            self.deploy_script,
            self.attestation_file,
            self.frontend_about,
            self.frontend_terms,
            Path(__file__),
        ]

        for file_path in files_to_check:
            self.assertTrue(file_path.exists(), f"File {file_path.name} must exist.")
            content = file_path.read_text(encoding="utf-8")

            # Assert Developer Architecture Note
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"File {file_path.name} is missing standardized DEVELOPER ARCHITECTURE NOTE.",
            )

            # Assert zero emojis
            emoji_matches = self.emoji_pattern.findall(content)
            self.assertEqual(
                len(emoji_matches),
                0,
                f"File {file_path.name} contains emoji violations: {emoji_matches}",
            )


if __name__ == "__main__":
    unittest.main()
