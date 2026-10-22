"""
DEVELOPER ARCHITECTURE NOTES:
--------------------------------------------------------------------------------
Target System: Ogrojatra National Educational Platform
Test Suite: Phase 98.1 Global Application Shell & Dignified Footer Verification
Purpose:
  Validates Tasks T655 and T656:
  1. Frontend Footer component integrity:
     - NCTB curriculum compliance badge
     - ISO 27001 and OWASP ASVS L2 security credentials
     - Authentic SVG payment rails badges for bKash, Nagad, and SSLCommerz
     - 4-column quick links grid: Academic Pathways, Career/Tuition, Governance
     - Emergency Hotline (16xxx / 1098 / 999) and digital safety compliance
  2. Next.js _app.tsx root wrapper integrity:
     - Global I18nProvider wrapping the entire component tree
     - Persistent Socratic AI Tutor Drawer with bottom-right FAB trigger
     - Network connectivity listeners (online/offline) with accessible toast banners
     - Theme persistence and dark mode synchronization
  3. Strict Zero-Emoji compliance and Developer Architecture Notes presence.
Standards:
  - WCAG 2.2 AAA Contrast Standards, Zero-Emoji Policy.
--------------------------------------------------------------------------------
"""

import os
import re
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class TestPhase981AppShellAndFooter(unittest.TestCase):
    """
    Automated test suite verifying the global application shell and dignified footer.
    """

    def setUp(self):
        self.frontend_dir = os.path.join(PROJECT_ROOT, "frontend")
        self.footer_path = os.path.join(self.frontend_dir, "src", "components", "layout", "Footer.tsx")
        self.app_path = os.path.join(self.frontend_dir, "src", "pages", "_app.tsx")
        self.layout_barrel_path = os.path.join(self.frontend_dir, "src", "components", "layout", "index.ts")

    def test_01_target_files_exist(self):
        """Verifies presence of Footer.tsx and _app.tsx."""
        self.assertTrue(os.path.isfile(self.footer_path), "Footer.tsx must exist")
        self.assertTrue(os.path.isfile(self.app_path), "_app.tsx must exist")
        self.assertTrue(os.path.isfile(self.layout_barrel_path), "layout/index.ts must exist")

    def test_02_footer_brand_and_mission(self):
        """Asserts Footer contains brand name, mission, and accreditation bar."""
        with open(self.footer_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Brand and mission checks
        self.assertIn("অগ্রযাত্রা", content, "Footer must contain Bengali brand name")
        self.assertIn("Student Growth Platform", content, "Footer must declare Student Growth Platform subtitle")
        self.assertIn("NCTB", content, "Footer must declare NCTB alignment")
        self.assertIn("ISO 27001", content, "Footer must declare ISO 27001 data vault certification")
        self.assertIn("OWASP ASVS L2", content, "Footer must declare OWASP ASVS L2 security seal")

    def test_03_footer_verified_payment_rails_svgs(self):
        """Asserts Footer contains authentic vector SVG badges for bKash, Nagad, and SSLCommerz."""
        with open(self.footer_path, "r", encoding="utf-8") as f:
            content = f.read()

        # bKash badge verification
        self.assertIn("bKash Verified Merchant", content)
        self.assertIn("#D12053", content, "bKash brand color must be present")

        # Nagad badge verification
        self.assertIn("Nagad Verified Merchant", content)
        self.assertIn("#F7941D", content, "Nagad brand color must be present")

        # SSLCommerz verification
        self.assertIn("SSLCOMMERZ", content)
        self.assertIn("PCI-DSS", content)

    def test_04_footer_quick_links_grid(self):
        """Asserts Footer contains 4-column quick links covering academic, career, and governance."""
        with open(self.footer_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Academic Pathways
        self.assertIn("/learn?stage=SSC", content)
        self.assertIn("/learn?stage=HSC", content)
        self.assertIn("/admission", content)
        self.assertIn("/practice", content)
        self.assertIn("/live-challenge", content)
        self.assertIn("stem-labs", content)

        # Career Engine & Tuition
        self.assertIn("/tuition", content)
        self.assertIn("/verify", content)
        self.assertIn("/career", content)
        self.assertIn("global-socratic-trigger", content)

        # Governance & Child Safety
        self.assertIn("অপ্রাপ্তবয়স্কদের তথ্য সুরক্ষা", content)
        self.assertIn("এসক্রো সম্মতি", content)
        self.assertIn("ব্যবহারের শর্তাবলী", content)

    def test_05_footer_emergency_hotline_and_legal(self):
        """Asserts emergency contact numbers and legal digital safety compliance statement."""
        with open(self.footer_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("১৬xxx", content, "Must display platform hotline")
        self.assertIn("১০৯৮", content, "Must display national child helpline 1098")
        self.assertIn("৯৯৯", content, "Must display emergency service 999")
        self.assertIn("ডিজিটাল নিরাপত্তা আইন", content, "Must include digital safety compliance statement")
        self.assertIn("২০২৬ অগ্রযাত্রা", content, "Must include copyright year")

    def test_06_app_root_i18n_provider_wrapping(self):
        """Asserts _app.tsx wraps the entire root Component with I18nProvider."""
        with open(self.app_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("I18nProvider", content, "_app.tsx must import and wrap with I18nProvider")
        self.assertIn("<I18nProvider>", content)
        self.assertIn("</I18nProvider>", content)
        self.assertIn("@/lib/i18n", content)

    def test_07_app_persistent_socratic_drawer_and_fab(self):
        """Asserts _app.tsx mounts the floating SocraticTutorDrawer and bottom-right FAB trigger."""
        with open(self.app_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("SocraticTutorDrawer", content, "_app.tsx must import SocraticTutorDrawer")
        self.assertIn("<SocraticTutorDrawer", content)
        self.assertIn("global-socratic-trigger", content, "Must have trigger FAB button id")
        self.assertIn("bottom-6 right-6", content, "Must be positioned at bottom-right of viewport")
        self.assertIn("min-h-[48px]", content, "Must maintain WCAG AAA 48px touch target")
        self.assertIn("aria-expanded", content, "Must provide accessible aria attributes")

    def test_08_app_offline_resilience_and_theme_persistence(self):
        """Asserts _app.tsx includes network connectivity listeners and theme persistence."""
        with open(self.app_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("addEventListener('offline'", content, "Must attach offline listener")
        self.assertIn("addEventListener('online'", content, "Must attach online listener")
        self.assertIn("WifiOff", content, "Must use WifiOff icon for disconnected state")
        self.assertIn("slc_theme", content, "Must persist theme in slc_theme")
        self.assertIn("classList.add('dark')", content, "Must toggle dark class on document element")

    def test_09_zero_emoji_compliance(self):
        """Enforces platform Zero-Emoji policy across Footer and _app.tsx."""
        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]"
        )

        files_to_check = [self.footer_path, self.app_path, __file__]

        for filepath in files_to_check:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                emojis = emoji_pattern.findall(content)
                self.assertEqual(
                    len(emojis),
                    0,
                    f"Zero-Emoji policy violation in {os.path.basename(filepath)}: found {emojis}",
                )

    def test_10_developer_architecture_notes_presence(self):
        """Verifies presence of Developer Architecture Notes header."""
        header_needle = "DEVELOPER ARCHITECTURE NOTE"
        for filepath in [self.footer_path, self.app_path, __file__]:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn(
                    header_needle,
                    content,
                    f"{os.path.basename(filepath)} must contain Developer Architecture Note header",
                )


if __name__ == "__main__":
    unittest.main()
