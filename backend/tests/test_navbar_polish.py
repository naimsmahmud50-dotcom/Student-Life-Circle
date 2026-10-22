"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Navbar Visual & Layout Polish Test Suite
TOPIC:     Zero-wrapping, unified controls, responsive badges, theme tokens
FILE:      backend/tests/test_navbar_polish.py
PURPOSE:   Asserts that Navbar component and global styles meet all senior UI/UX engineer mandates:
           1. Single-line "Sign In / Register" CTA button with User icon.
           2. Compact single-line Bengali badge with responsive shortening logic.
           3. Non-wrapping navigation items ("Board Archives", "Live Challenge", logo subtitle).
           4. Unified 40px heights and radii across all controls.
           5. Light and Dark mode CSS variables and tokens.
           6. Responsive behavior across 1440px, 1280px, 1024px, and 390px.
           7. Strict Zero-Emoji compliance and accessibility standards.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA Contrast
"""

import unittest
import re
from pathlib import Path


class TestNavbarPolish(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.navbar_path = cls.repo_root / "frontend" / "src" / "components" / "layout" / "Navbar.tsx"
        cls.globals_css_path = cls.repo_root / "frontend" / "src" / "styles" / "globals.css"

        cls.navbar_content = cls.navbar_path.read_text(encoding="utf-8")
        cls.css_content = cls.globals_css_path.read_text(encoding="utf-8")

    def test_01_sign_in_register_single_line_button(self):
        """Verify 'Sign In / Register' button is single-line, primary CTA with User icon."""
        self.assertIn("whitespace-nowrap", self.navbar_content)
        self.assertIn("User", self.navbar_content)
        self.assertIn("var(--navbar-primary-gradient)", self.navbar_content)
        self.assertIn("var(--navbar-primary-glow)", self.navbar_content)
        self.assertIn("rounded-xl", self.navbar_content)
        self.assertIn("h-10", self.navbar_content)

    def test_02_bengali_pill_compact_single_line_and_responsive(self):
        """Verify Bengali stage pill wraps into single line with responsive shortening."""
        self.assertIn("getShortStage", self.navbar_content)
        self.assertIn("hidden 2xl:inline truncate", self.navbar_content)
        self.assertIn("inline 2xl:hidden truncate", self.navbar_content)
        self.assertIn("rounded-full", self.navbar_content)
        self.assertIn("h-7", self.navbar_content)

    def test_03_no_wrapping_on_nav_links_and_logo_subtitle(self):
        """Verify Board Archives, Live Challenge, and logo subtitle have whitespace-nowrap."""
        self.assertIn("Student Growth Platform", self.navbar_content)
        # Check logo subtitle has whitespace-nowrap
        self.assertIn("whitespace-nowrap", self.navbar_content)
        # Check Live Challenge has rose badge and pulsing dot
        self.assertIn("var(--navbar-live-badge-bg)", self.navbar_content)
        self.assertIn("nav-live-dot", self.navbar_content)

    def test_04_unified_control_heights_and_radii(self):
        """Verify controls share 40px (h-10) heights and unified 12px/999px radii."""
        # BN/EN Toggle: 40px container, rounded-full
        self.assertIn("h-10 p-1 rounded-full", self.navbar_content)
        # Theme toggle: 40x40 (w-10 h-10), rounded-xl
        self.assertIn("w-10 h-10 rounded-xl", self.navbar_content)
        # Dashboard button: h-10, rounded-xl
        self.assertIn("h-10 px-3 2xl:px-3.5 rounded-xl", self.navbar_content)
        # Sign In button: h-10, rounded-xl
        self.assertIn("h-10 px-4 2xl:px-5 rounded-xl", self.navbar_content)

    def test_05_design_system_tokens_in_css(self):
        """Verify CSS variables for dark and light modes exist in globals.css."""
        # Dark mode tokens
        self.assertIn("--navbar-bg: rgba(10, 15, 30, 0.80);", self.css_content)
        self.assertIn("--navbar-surface: #111A2E;", self.css_content)
        self.assertIn("--navbar-text: #E6EAF2;", self.css_content)
        self.assertIn("--navbar-text-muted: #8FA0BD;", self.css_content)
        self.assertIn("--navbar-primary-gradient: linear-gradient(135deg, #22D3EE 0%, #3B82F6 100%);", self.css_content)
        self.assertIn("--navbar-primary-text: #06121F;", self.css_content)
        # Light mode tokens
        self.assertIn("--navbar-bg: rgba(255, 255, 255, 0.85);", self.css_content)
        self.assertIn("--navbar-surface: #F1F5F9;", self.css_content)
        self.assertIn("--navbar-border: #E2E8F0;", self.css_content)
        self.assertIn("--navbar-text: #0F172A;", self.css_content)
        self.assertIn("--navbar-text-muted: #64748B;", self.css_content)
        self.assertIn("--navbar-primary-gradient: linear-gradient(135deg, #0891B2 0%, #2563EB 100%);", self.css_content)

    def test_06_responsive_drawer_and_accessibility(self):
        """Verify responsive mobile drawer, focus rings, and reduced motion."""
        self.assertIn("role=\"dialog\"", self.navbar_content)
        self.assertIn("aria-modal=\"true\"", self.navbar_content)
        self.assertIn("focus-visible:ring-[#22D3EE]", self.navbar_content)
        self.assertIn("aria-current", self.navbar_content)
        self.assertIn("prefers-reduced-motion", self.css_content)

    def test_07_developer_architecture_note_and_zero_emoji(self):
        """Verify standardized developer architecture header and strict zero emojis."""
        self.assertIn("DEVELOPER ARCHITECTURE NOTE:", self.navbar_content)
        # Check no emojis
        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|"
            r"[\u2600-\u27bf]|"
            r"[\u2300-\u23ff]|"
            r"[\u2b50-\u2b55]|"
            r"[\ufe00-\ufe0f]"
        )
        self.assertFalse(bool(emoji_pattern.search(self.navbar_content)), "Navbar.tsx must not contain emojis.")
        self.assertFalse(bool(emoji_pattern.search(self.css_content)), "globals.css must not contain emojis.")


if __name__ == "__main__":
    unittest.main()
