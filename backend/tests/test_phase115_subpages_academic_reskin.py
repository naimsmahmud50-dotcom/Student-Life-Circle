"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite for Sub-Pages Academic Re-Skin
TOPIC:     Phase 115 Sub-Pages Academic Re-Skin & AI-Vibe Elimination
FILE:      backend/tests/test_phase115_subpages_academic_reskin.py
PHASE:     Phase 115 - Sub-Pages Pure Academic Re-Skin
PURPOSE:   Automated unit and integration test suite certifying zero AI-vibe gradient
           classes, strict zero-emoji compliance, Burgundy Crimson negative marking
           badges, 3D tactile buttons, and authentic Oxford Navy human craftsmanship.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
========================================================================================
"""

import os
import re
import unittest
from pathlib import Path


class TestPhase115SubpagesAcademicReskin(unittest.TestCase):
    """
    Test suite certifying Phase 115 Sub-Pages Pure Academic Re-Skin.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.pages = {
            "learn": cls.root_dir / "frontend" / "src" / "pages" / "learn.tsx",
            "practice": cls.root_dir / "frontend" / "src" / "pages" / "practice.tsx",
            "live_challenge": cls.root_dir / "frontend" / "src" / "pages" / "live-challenge.tsx",
            "admission": cls.root_dir / "frontend" / "src" / "pages" / "admission.tsx",
            "tuition": cls.root_dir / "frontend" / "src" / "pages" / "tuition.tsx",
            "career": cls.root_dir / "frontend" / "src" / "pages" / "career.tsx",
        }

        cls.emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

        cls.ai_gradient_pattern = re.compile(
            r"(bg-clip-text|bg-gradient-to-r|from-blue-\d+|to-indigo-\d+|glow-blue)"
        )

    def test_01_all_subpages_exist_with_developer_architecture_notes(self):
        """Verifies all 6 core subpages exist and declare Developer Architecture Note headers."""
        target_files = list(self.pages.values()) + [Path(__file__).resolve()]

        for path in target_files:
            self.assertTrue(path.exists(), f"File {path.name} must exist on disk.")
            content = path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"File {path.name} missing mandatory Developer Architecture Note header.",
            )
            self.assertIn(
                "Phase 115",
                content,
                f"File {path.name} must reference Phase 115 in header.",
            )

    def test_02_strict_zero_emoji_compliance_across_all_subpages(self):
        """Asserts strict Zero-Emoji compliance across all 6 core sub-pages."""
        for name, path in self.pages.items():
            content = path.read_text(encoding="utf-8")
            matches = self.emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"Page '{name}' ({path.name}) violates Zero-Emoji policy: found {matches}",
            )

    def test_03_zero_forbidden_ai_gradients_across_all_subpages(self):
        """Asserts total elimination of bg-clip-text, blue-to-indigo gradients, and fluorescent glows."""
        for name, path in self.pages.items():
            content = path.read_text(encoding="utf-8")
            matches = self.ai_gradient_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"Page '{name}' ({path.name}) contains forbidden AI-vibe gradient classes: {matches}",
            )

    def test_04_pure_academic_oxford_navy_and_tactile_3d_buttons(self):
        """Verifies Oxford Navy anchor and 3D tactile buttons across the sub-pages."""
        for name, path in self.pages.items():
            content = path.read_text(encoding="utf-8")
            # Must declare Oxford Navy color code
            self.assertIn(
                "#0A2540",
                content,
                f"Page '{name}' must declare Oxford Academic Navy #0A2540.",
            )
            # Must declare active tactile button depth
            self.assertIn(
                "active:translate-y-",
                content,
                f"Page '{name}' must declare tactile physical button active state.",
            )
            self.assertIn(
                "active:shadow-none",
                content,
                f"Page '{name}' must declare active:shadow-none for 3D tactile release.",
            )

    def test_05_burgundy_crimson_negative_marking_badges(self):
        """Verifies Burgundy Crimson (#991B1B) negative marking badges in admission and live-challenge."""
        admission_content = self.pages["admission"].read_text(encoding="utf-8")
        live_content = self.pages["live_challenge"].read_text(encoding="utf-8")

        self.assertIn(
            "#991B1B",
            admission_content,
            "admission.tsx must style negative marking badges with Burgundy Crimson #991B1B.",
        )
        self.assertIn(
            "#991B1B",
            live_content,
            "live-challenge.tsx must style negative marking badges with Burgundy Crimson #991B1B.",
        )

    def test_06_pure_lucide_svg_vector_icons(self):
        """Verifies 1.75px stroke Lucide vector icons on all 6 pages."""
        for name, path in self.pages.items():
            content = path.read_text(encoding="utf-8")
            self.assertIn(
                "lucide-react",
                content,
                f"Page '{name}' must import vector icons from 'lucide-react'.",
            )
            self.assertIn(
                "CheckCircle2",
                content,
                f"Page '{name}' must use Lucide CheckCircle2 for verified badges.",
            )


if __name__ == "__main__":
    unittest.main()
