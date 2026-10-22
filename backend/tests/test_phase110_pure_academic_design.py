"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Design System & Academic Visual Standards Verification
TOPIC:     Phase 110 Pure Academic Design System & AI-Vibe Purge
FILE:      backend/tests/test_phase110_pure_academic_design.py
PHASE:     Phase 110 - Pure Academic Visual Design Elevation
PURPOSE:   Purges all AI-generated neon artifacts, establishing a prestigious,
           human-crafted Oxford/Cambridge academic design system with zero emojis.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA Contrast
"""

import os
import re
import unittest
from pathlib import Path


class TestPhase110PureAcademicDesign(unittest.TestCase):
    """
    Automated verification suite certifying:
    1. Pure Academic Design Tokens in globals.css (Oxford Navy, Academic Emerald, Scholar Gold, Paper Ivory).
    2. Eradication of neon gradients, cyber glow box-shadows, and purple/indigo buttons.
    3. Tactile 3D Oxford Academic buttons in button.tsx, index.tsx, and Navbar.tsx.
    4. Scholarly Deep Regal Ink Slate footer and zero-emoji compliance across all target files.
    5. Presence of standardized DEVELOPER ARCHITECTURE NOTE headers.
    """

    @classmethod
    def setUpClass(cls):
        cls.base_dir = Path(__file__).resolve().parent.parent.parent
        cls.frontend_dir = cls.base_dir / "frontend"
        cls.globals_css = cls.frontend_dir / "src" / "styles" / "globals.css"
        cls.tailwind_config = cls.frontend_dir / "tailwind.config.js"
        cls.button_component = cls.frontend_dir / "src" / "components" / "ui" / "button.tsx"
        cls.navbar_component = cls.frontend_dir / "src" / "components" / "layout" / "Navbar.tsx"
        cls.footer_component = cls.frontend_dir / "src" / "components" / "layout" / "Footer.tsx"
        cls.index_page = cls.frontend_dir / "src" / "pages" / "index.tsx"
        cls.specs_dir = cls.base_dir / "specs" / "014-phase110-pure-academic-design-purge"

        cls.emoji_pattern = re.compile(
            r"[\U0001F600-\U0001F64F"
            r"\U0001F300-\U0001F5FF"
            r"\U0001F680-\U0001F6FF"
            r"\U0001F1E0-\U0001F1FF"
            r"\U00002702-\U000027B0"
            r"\U000024C2-\U0001F251"
            r"\U0001F900-\U0001F9FF"
            r"\U0001FA70-\U0001FAFF"
            r"]+",
            flags=re.UNICODE,
        )

    def test_01_globals_css_pure_academic_tokens_and_neon_purge(self):
        """Verify globals.css defines Oxford academic tokens and has purged neon radial glows."""
        self.assertTrue(self.globals_css.exists(), "globals.css must exist.")
        content = self.globals_css.read_text(encoding="utf-8")

        # Academic design tokens
        self.assertIn("--color-oxford-navy: #0A2540", content)
        self.assertIn("--color-academic-emerald: #065F46", content)
        self.assertIn("--color-scholar-gold: #B45309", content)
        self.assertIn("--color-paper-ivory: #FAFAF8", content)
        self.assertIn("--color-ink-slate: #0B132B", content)

        # Tactile 3D button classes
        self.assertIn(".btn-3d-oxford", content)
        self.assertIn(".btn-3d-emerald", content)
        self.assertIn(".btn-paper-outline", content)

        # Absence of neon glow classes and ambient radial glows
        self.assertNotIn("glow-blue", content)
        self.assertNotIn("glow-teal", content)
        self.assertNotIn("glow-amber", content)
        self.assertIn("--bg-radial-ambient: none;", content)

    def test_02_tailwind_config_pure_academic_scales_and_paper_shadows(self):
        """Verify tailwind.config.js declares Oxford/Emerald scales and clean paper shadows."""
        self.assertTrue(self.tailwind_config.exists(), "tailwind.config.js must exist.")
        content = self.tailwind_config.read_text(encoding="utf-8")

        # Oxford Academic Navy & Academic Emerald scales
        self.assertIn("oxford", content)
        self.assertIn("#0A2540", content)
        self.assertIn("#051329", content)
        self.assertIn("emerald", content)
        self.assertIn("#065F46", content)
        self.assertIn("#044332", content)
        self.assertIn("paper", content)
        self.assertIn("scholar", content)
        self.assertIn("#B45309", content)

        # Paper and tactile depths in boxShadow
        self.assertIn("'paper':", content)
        self.assertIn("'tactile-oxford':", content)
        self.assertIn("'tactile-emerald':", content)

        # Absence of cyber neon glows
        self.assertNotIn("'glow-blue':", content)
        self.assertNotIn("'glow-teal':", content)
        self.assertNotIn("'glow-amber':", content)

    def test_03_button_component_tactile_3d_and_paper_variants(self):
        """Verify button.tsx implements 3D Oxford Navy, Academic Emerald, and Paper buttons."""
        self.assertTrue(self.button_component.exists(), "button.tsx must exist.")
        content = self.button_component.read_text(encoding="utf-8")

        # Variants
        for variant in ["'oxford'", "'emerald'", "'paper'", "'default'", "'brand'", "'teal'"]:
            self.assertIn(variant, content, f"Button variant {variant} must be supported.")

        # 3D Oxford physics
        self.assertIn("#0A2540", content)
        self.assertIn("#051329", content)
        self.assertIn("#065F46", content)
        self.assertIn("#044332", content)

        # Mobile touch target and Lucide Loader2
        self.assertIn("min-h-[44px]", content)
        self.assertIn("Loader2", content)
        self.assertIn("animate-spin", content)

    def test_04_homepage_and_layout_reskin_and_zero_ai_vibe(self):
        """Verify index.tsx, Navbar.tsx, and Footer.tsx have zero neon gradients and use academic palettes."""
        index_content = self.index_page.read_text(encoding="utf-8")
        navbar_content = self.navbar_component.read_text(encoding="utf-8")
        footer_content = self.footer_component.read_text(encoding="utf-8")

        # Zero forbidden neon gradient strings in homepage
        self.assertNotIn("bg-gradient-to-r from-blue-600 via-indigo-600", index_content)
        self.assertNotIn("bg-gradient-to-r from-blue-600 to-indigo-600", index_content)
        self.assertNotIn("bg-gradient-to-br from-slate-900 via-slate-900 to-blue-950", index_content)
        self.assertNotIn("text-purple-", index_content)
        self.assertNotIn("bg-purple-", index_content)
        self.assertNotIn("border-purple-", index_content)

        # Tactile 3D Oxford button usage
        self.assertIn("btn-3d-oxford", index_content)
        self.assertIn("#0A2540", index_content)
        self.assertIn("#065F46", index_content)

        # Navbar Oxford Navy brand
        self.assertIn("#0A2540", navbar_content)
        self.assertIn("shadow-[0_4px_0_0_#051329]", navbar_content)

        # Footer Deep Regal Ink Slate
        self.assertIn("#0B132B", footer_content)
        self.assertIn("#0A2540", footer_content)

    def test_05_developer_architecture_notes_and_strict_zero_emoji(self):
        """Verify all Phase 110 files contain standardized header notes and zero emojis."""
        target_files = [
            self.globals_css,
            self.tailwind_config,
            self.button_component,
            self.navbar_component,
            self.footer_component,
            self.index_page,
            Path(__file__),
            self.specs_dir / "spec.md",
            self.specs_dir / "plan.md",
            self.specs_dir / "tasks.md",
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Target file {file_path.name} must exist.")
            content = file_path.read_text(encoding="utf-8")

            # Architecture Note check
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"Missing DEVELOPER ARCHITECTURE NOTE in {file_path.name}",
            )
            self.assertIn(
                "Phase 110 - Pure Academic Visual Design Elevation",
                content,
                f"Missing Phase 110 identifier in {file_path.name}",
            )

            # Strict Zero-Emoji check
            emojis = self.emoji_pattern.findall(content)
            self.assertEqual(
                emojis,
                [],
                f"Strict Zero-Emoji Violation in {file_path.name}: Found emojis {emojis}",
            )


if __name__ == "__main__":
    unittest.main()
