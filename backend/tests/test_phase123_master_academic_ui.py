"""
DEVELOPER ARCHITECTURE NOTE:
========================================================================================
MODULE:    Master Academic UI & Pro Tactile Button Elevation Test Suite
TOPIC:     Zero AI Vibe, Duolingo/Brilliant-grade 3D Tactile Buttons, Oxford Palette
FILE:      backend/tests/test_phase123_master_academic_ui.py
PHASE:     Phase 123 - Master Academic UI & Pro Tactile Button Elevation
PURPOSE:   Asserts that all buttons, cards, backgrounds, and headers adhere strictly to:
           1. Pure Academic Palette (Oxford Navy #0A2540, Emerald #065F46, Paper White #FFFFFF).
           2. 3D physical press button physics (4px bottom ledge shadow-[0_4px_0_0_#051329], active:translate-y-1).
           3. Zero AI neon gradients, zero glowing drop-shadows, and zero purple/indigo neon.
           4. Typography standards ('Hind Siliguri' line-height 1.75, 'Plus Jakarta Sans', 'Inter').
           5. 100% Lucide-React SVG vector icons and strict Zero-Emoji compliance.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
========================================================================================
"""

import unittest
import os
import re
from pathlib import Path


class TestPhase123MasterAcademicUI(unittest.TestCase):
    """
    Automated test suite certifying Phase 123 Master Academic UI & Pro Tactile Button Elevation.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.frontend_dir = cls.repo_root / "frontend"

        # Target Files
        cls.globals_css_path = cls.frontend_dir / "src" / "styles" / "globals.css"
        cls.tailwind_config_path = cls.frontend_dir / "tailwind.config.js"
        cls.button_path = cls.frontend_dir / "src" / "components" / "ui" / "button.tsx"
        cls.index_path = cls.frontend_dir / "src" / "pages" / "index.tsx"
        cls.dashboard_path = cls.frontend_dir / "src" / "pages" / "dashboard.tsx"
        cls.navbar_path = cls.frontend_dir / "src" / "components" / "layout" / "Navbar.tsx"
        cls.footer_path = cls.frontend_dir / "src" / "components" / "layout" / "Footer.tsx"

        # File Contents
        cls.globals_css = cls.globals_css_path.read_text(encoding="utf-8")
        cls.tailwind_config = cls.tailwind_config_path.read_text(encoding="utf-8")
        cls.button_content = cls.button_path.read_text(encoding="utf-8")
        cls.index_content = cls.index_path.read_text(encoding="utf-8")
        cls.dashboard_content = cls.dashboard_path.read_text(encoding="utf-8")
        cls.navbar_content = cls.navbar_path.read_text(encoding="utf-8")
        cls.footer_content = cls.footer_path.read_text(encoding="utf-8")

        cls.target_contents = [
            ("globals.css", cls.globals_css),
            ("tailwind.config.js", cls.tailwind_config),
            ("button.tsx", cls.button_content),
            ("index.tsx", cls.index_content),
            ("dashboard.tsx", cls.dashboard_content),
            ("Navbar.tsx", cls.navbar_content),
            ("Footer.tsx", cls.footer_content),
        ]

    def test_01_developer_architecture_notes_presence(self):
        """Verify all target files contain the standardized Phase 123 Developer Architecture Note header."""
        for filename, content in self.target_contents:
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"File {filename} is missing the DEVELOPER ARCHITECTURE NOTE header."
            )
            self.assertIn(
                "Phase 123",
                content,
                f"File {filename} is missing Phase 123 reference in the architecture note."
            )

    def test_02_pure_academic_color_palette_tokens(self):
        """Verify globals.css and tailwind.config.js declare Oxford Navy, Emerald, Paper, Scholar Gold, and Crimson."""
        # Check globals.css tokens
        self.assertIn("#0A2540", self.globals_css, "Oxford Navy #0A2540 must be in globals.css")
        self.assertIn("#051329", self.globals_css, "Oxford Depth #051329 must be in globals.css")
        self.assertIn("#065F46", self.globals_css, "Academic Emerald #065F46 must be in globals.css")
        self.assertIn("#033829", self.globals_css, "Academic Forest Depth #033829 must be in globals.css")
        self.assertIn("#B45309", self.globals_css, "Scholar Gold #B45309 must be in globals.css")
        self.assertIn("#FAFAF8", self.globals_css, "Paper Ivory #FAFAF8 must be in globals.css")
        self.assertIn("#FFFFFF", self.globals_css, "Paper White #FFFFFF must be in globals.css")
        self.assertIn("#991B1B", self.globals_css, "Burgundy Crimson #991B1B must be in globals.css")

        # Check tailwind.config.js tokens
        self.assertIn("oxford", self.tailwind_config, "oxford palette must be configured in tailwind.config.js")
        self.assertIn("emerald", self.tailwind_config, "emerald palette must be configured in tailwind.config.js")
        self.assertIn("scholar", self.tailwind_config, "scholar palette must be configured in tailwind.config.js")
        self.assertIn("paper", self.tailwind_config, "paper palette must be configured in tailwind.config.js")
        self.assertIn("burgundy", self.tailwind_config, "burgundy palette must be configured in tailwind.config.js")

    def test_03_pro_tactile_3d_button_classes_and_physics(self):
        """Verify tactile 3D physical button definitions in button.tsx and globals.css."""
        # 1. Oxford Primary 3D button physics in button.tsx
        self.assertIn("shadow-[0_4px_0_0_#051329]", self.button_content)
        self.assertIn("active:translate-y-1", self.button_content)
        self.assertIn("active:shadow-none", self.button_content)
        self.assertIn("hover:bg-[#0E3357]", self.button_content)
        self.assertIn("rounded-2xl", self.button_content)

        # 2. Paper secondary button physics in button.tsx
        self.assertIn("bg-white text-slate-800 border border-slate-300", self.button_content)
        self.assertIn("shadow-sm", self.button_content)
        self.assertIn("active:translate-y-0.5", self.button_content)

        # 3. Academic Forest Green / Mastery button physics in button.tsx
        self.assertIn("shadow-[0_4px_0_0_#033829]", self.button_content)
        self.assertIn("hover:bg-[#087858]", self.button_content)

        # 4. globals.css tactile utility classes
        self.assertIn(".btn-3d-oxford", self.globals_css)
        self.assertIn(".btn-3d-emerald", self.globals_css)
        self.assertIn(".btn-paper-outline", self.globals_css)
        self.assertIn("box-shadow: 0 4px 0 0 #051329", self.globals_css)
        self.assertIn("box-shadow: 0 4px 0 0 #033829", self.globals_css)

    def test_04_academic_typography_standards(self):
        """Verify typography configuration: Hind Siliguri, Plus Jakarta Sans, Inter, line-height 1.75."""
        self.assertIn("family=Hind+Siliguri", self.globals_css)
        self.assertIn("family=Plus+Jakarta+Sans", self.globals_css)
        self.assertIn("family=Inter", self.globals_css)
        self.assertIn("line-height: 1.75", self.globals_css)

        # Tailwind font families
        self.assertIn("Hind Siliguri", self.tailwind_config)
        self.assertIn("Plus Jakarta Sans", self.tailwind_config)
        self.assertIn("Inter", self.tailwind_config)

    def test_05_absence_of_neon_glow_and_ai_vibe(self):
        """Verify strict elimination of neon glows, glowing shadows, and purple gradient cards."""
        # Tailwind must NOT have neon glow shadows
        self.assertNotIn("'glow-blue':", self.tailwind_config)
        self.assertNotIn("'glow-teal':", self.tailwind_config)
        self.assertNotIn("'glow-amber':", self.tailwind_config)

        # index.tsx must not contain neon gradients or purple cards
        self.assertNotIn("bg-gradient-to-r from-blue-600 via-indigo-600", self.index_content)
        self.assertNotIn("text-purple-", self.index_content)
        self.assertNotIn("bg-purple-", self.index_content)
        self.assertNotIn("border-purple-", self.index_content)

    def test_06_strict_zero_emoji_compliance(self):
        """Assert 100% Zero-Emoji policy across all Phase 123 target files."""
        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|"
            r"[\u2600-\u27bf]|"
            r"[\u2300-\u23ff]|"
            r"[\u2b50-\u2b55]|"
            r"[\ufe00-\ufe0f]"
        )

        for filename, content in self.target_contents:
            emojis = emoji_pattern.findall(content)
            self.assertEqual(
                len(emojis),
                0,
                f"Zero-Emoji policy violation in {filename}: {emojis}"
            )


if __name__ == "__main__":
    unittest.main()
