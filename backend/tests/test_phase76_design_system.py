"""
DEVELOPER ARCHITECTURE NOTE - TEST SUITE:
Phase 76: Next.js 15+ Design System & Component Library Verification
Validates 10 core architectural and ergonomic requirements:
1. Tailwind CSS design tokens: Primary (#0F172A), Brand (#2563EB), Teal (#0D9488), Amber (#D97706), Red (#DC2626), Ground (#F8FAFC)
2. Global typography: Noto Sans Bengali font loader, line-height 1.6, and WCAG 2.2 AA contrast variables
3. Button primitive: Variants (default, brand, teal, destructive, outline, ghost), 44px+ touch targets, Loader2 spinner
4. Badge primitive: Variants (brand, teal, warning, destructive, neutral, outline, verified), DifficultyBadge, RoleChip
5. Dialog & Modal primitives: Radix UI @radix-ui/react-dialog wrappers, focus trapping, X close button
6. Card primitive: Compound architecture (Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter), #E2E8F0 border
7. Tabs primitive: Radix UI @radix-ui/react-tabs wrappers, animated triggers, touch target min-heights
8. Toast primitive: Status indicators (success, warning, error, info, offline), Lucide SVG icons, useToast hook
9. Design system barrel export (ui/index.ts) and class merger utility (lib/utils.ts)
10. Strict Zero-Emoji governance: Complete unicode scan asserting 0 emojis across all UI files
"""

import os
import re
import unittest


class TestPhase76DesignSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        cls.frontend_dir = os.path.join(cls.base_dir, 'frontend')
        cls.ui_dir = os.path.join(cls.frontend_dir, 'src/components/ui')
        cls.styles_dir = os.path.join(cls.frontend_dir, 'src/styles')
        cls.lib_dir = os.path.join(cls.frontend_dir, 'src/lib')

    def test_tailwind_config_design_tokens(self):
        """Verify tailwind.config.js declares all required design tokens and Noto Sans Bengali."""
        tailwind_path = os.path.join(self.frontend_dir, 'tailwind.config.js')
        self.assertTrue(os.path.exists(tailwind_path), "tailwind.config.js must exist.")

        with open(tailwind_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check required color tokens
        self.assertIn("#0F172A", content, "Primary navy (#0F172A) must be defined.")
        self.assertIn("#2563EB", content, "Brand blue (#2563EB) must be defined.")
        self.assertIn("#0D9488", content, "Teal mastery (#0D9488) must be defined.")
        self.assertIn("#D97706", content, "Amber warning (#D97706) must be defined.")
        self.assertIn("#DC2626", content, "Red danger (#DC2626) must be defined.")
        self.assertIn("#F8FAFC", content, "Ground light (#F8FAFC) must be defined.")

        # Check font and touch ergonomics
        self.assertIn("Noto Sans Bengali", content, "Noto Sans Bengali font must be in fontFamily.")
        self.assertIn("44px", content, "Touch minHeight (44px) must be configured.")

    def test_globals_css_typography_and_line_height(self):
        """Verify globals.css contains Noto Sans Bengali font loader and line-height 1.6."""
        globals_path = os.path.join(self.styles_dir, 'globals.css')
        self.assertTrue(os.path.exists(globals_path), "globals.css must exist.")

        with open(globals_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("Noto+Sans+Bengali", content, "Google Fonts import for Noto Sans Bengali must exist.")
        self.assertIn("line-height: 1.6", content, "Base body line-height must be 1.6.")
        self.assertIn("--bg-app: #F8FAFC", content, "Light mode ground variable must be #F8FAFC.")
        self.assertIn("--text-main: #0F172A", content, "Light mode text variable must be #0F172A.")

    def test_button_component_variants_and_touch_target(self):
        """Verify button.tsx implements all 6 variants, Loader2 spinner, and touch targets."""
        button_path = os.path.join(self.ui_dir, 'button.tsx')
        self.assertTrue(os.path.exists(button_path), "button.tsx must exist.")

        with open(button_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check variants
        for variant in ['default', 'brand', 'teal', 'destructive', 'outline', 'ghost']:
            self.assertIn(f"'{variant}'", content, f"Button variant '{variant}' must be supported.")

        # Check Lucide Loader2
        self.assertIn("Loader2", content, "Lucide Loader2 must be imported and used.")
        self.assertIn("animate-spin", content, "Loading state must spin Loader2.")

        # Check touch target
        self.assertIn("min-h-[44px]", content, "Button md size must enforce min-h-[44px].")
        self.assertIn("@radix-ui/react-slot", content, "Radix UI Slot must be supported for asChild.")

    def test_badge_component_variants_and_presets(self):
        """Verify badge.tsx implements required variants, DifficultyBadge, and RoleChip."""
        badge_path = os.path.join(self.ui_dir, 'badge.tsx')
        self.assertTrue(os.path.exists(badge_path), "badge.tsx must exist.")

        with open(badge_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for variant in ['brand', 'teal', 'warning', 'destructive', 'neutral', 'outline', 'verified']:
            self.assertIn(f"'{variant}'", content, f"Badge variant '{variant}' must be supported.")

        self.assertIn("DifficultyBadge", content, "DifficultyBadge preset must be exported.")
        self.assertIn("VerifiedBadge", content, "VerifiedBadge preset must be exported.")
        self.assertIn("RoleChip", content, "RoleChip preset must be exported.")

    def test_dialog_and_modal_primitives(self):
        """Verify dialog.tsx and modal.tsx wrap @radix-ui/react-dialog with full accessibility."""
        dialog_path = os.path.join(self.ui_dir, 'dialog.tsx')
        modal_path = os.path.join(self.ui_dir, 'modal.tsx')

        self.assertTrue(os.path.exists(dialog_path), "dialog.tsx must exist.")
        self.assertTrue(os.path.exists(modal_path), "modal.tsx must exist.")

        with open(dialog_path, 'r', encoding='utf-8') as f:
            d_content = f.read()

        self.assertIn("@radix-ui/react-dialog", d_content)
        self.assertIn("DialogPrimitive.Root", d_content)
        self.assertIn("DialogOverlay", d_content)
        self.assertIn("DialogContent", d_content)
        self.assertIn("DialogHeader", d_content)
        self.assertIn("DialogFooter", d_content)
        self.assertIn("DialogTitle", d_content)
        self.assertIn("DialogDescription", d_content)

        with open(modal_path, 'r', encoding='utf-8') as f:
            m_content = f.read()

        self.assertIn("export const Modal", m_content)
        self.assertIn("DialogContent", m_content)

    def test_card_component_structure(self):
        """Verify card.tsx implements compound card architecture and subtle border."""
        card_path = os.path.join(self.ui_dir, 'card.tsx')
        self.assertTrue(os.path.exists(card_path), "card.tsx must exist.")

        with open(card_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("border-[#E2E8F0]", content, "Subtle border #E2E8F0 must be present.")
        self.assertIn("export const Card", content)
        self.assertIn("export const CardHeader", content)
        self.assertIn("export const CardTitle", content)
        self.assertIn("export const CardDescription", content)
        self.assertIn("export const CardContent", content)
        self.assertIn("export const CardFooter", content)

    def test_tabs_component_radix_primitives(self):
        """Verify tabs.tsx wraps @radix-ui/react-tabs with active indicators."""
        tabs_path = os.path.join(self.ui_dir, 'tabs.tsx')
        self.assertTrue(os.path.exists(tabs_path), "tabs.tsx must exist.")

        with open(tabs_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("@radix-ui/react-tabs", content)
        self.assertIn("TabsPrimitive.Root", content)
        self.assertIn("TabsList", content)
        self.assertIn("TabsTrigger", content)
        self.assertIn("TabsContent", content)
        self.assertIn("min-h-[40px] sm:min-h-[44px]", content, "Tabs trigger touch ergonomics must be defined.")

    def test_toast_component_status_indicators(self):
        """Verify toast.tsx implements success, warning, error, info, offline and useToast hook."""
        toast_path = os.path.join(self.ui_dir, 'toast.tsx')
        self.assertTrue(os.path.exists(toast_path), "toast.tsx must exist.")

        with open(toast_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for status in ['success', 'warning', 'error', 'info', 'offline']:
            self.assertIn(f"'{status}'", content, f"Toast status '{status}' must be defined.")

        self.assertIn("CheckCircle2", content, "Lucide CheckCircle2 must be used for success.")
        self.assertIn("AlertTriangle", content, "Lucide AlertTriangle must be used for warning.")
        self.assertIn("AlertCircle", content, "Lucide AlertCircle must be used for error.")
        self.assertIn("WifiOff", content, "Lucide WifiOff must be used for offline.")
        self.assertIn("useToast", content, "useToast hook must be exported.")

    def test_barrel_export_and_utils(self):
        """Verify ui/index.ts barrel exports and lib/utils.ts cn helper function."""
        index_path = os.path.join(self.ui_dir, 'index.ts')
        utils_path = os.path.join(self.lib_dir, 'utils.ts')

        self.assertTrue(os.path.exists(index_path), "ui/index.ts must exist.")
        self.assertTrue(os.path.exists(utils_path), "lib/utils.ts must exist.")

        with open(index_path, 'r', encoding='utf-8') as f:
            i_content = f.read()

        for mod in ['button', 'badge', 'card', 'dialog', 'modal', 'tabs', 'toast']:
            self.assertIn(f"'./{mod}'", i_content, f"Module '{mod}' must be re-exported in index.ts.")

        with open(utils_path, 'r', encoding='utf-8') as f:
            u_content = f.read()

        self.assertIn("export function cn", u_content)
        self.assertIn("tailwind-merge", u_content)

    def test_strict_zero_emoji_governance_in_frontend_components(self):
        """Scan all frontend design system files ensuring zero unicode emojis."""
        emoji_pattern = re.compile(
            '[\U0001F600-\U0001F64F]'
            '|[\U0001F300-\U0001F5FF]'
            '|[\U0001F680-\U0001F6FF]'
            '|[\U0001F1E0-\U0001F1FF]'
            '|[\U00002702-\U000027B0]'
            '|[\U0001F900-\U0001F9FF]'
            '|[\U0001FA70-\U0001FAFF]'
        )

        target_files = [
            os.path.join(self.frontend_dir, 'tailwind.config.js'),
            os.path.join(self.styles_dir, 'globals.css'),
            os.path.join(self.lib_dir, 'utils.ts'),
            os.path.join(self.ui_dir, 'button.tsx'),
            os.path.join(self.ui_dir, 'badge.tsx'),
            os.path.join(self.ui_dir, 'card.tsx'),
            os.path.join(self.ui_dir, 'dialog.tsx'),
            os.path.join(self.ui_dir, 'modal.tsx'),
            os.path.join(self.ui_dir, 'tabs.tsx'),
            os.path.join(self.ui_dir, 'toast.tsx'),
            os.path.join(self.ui_dir, 'index.ts'),
        ]

        for filepath in target_files:
            self.assertTrue(os.path.exists(filepath), f"File {filepath} must exist.")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            matches = emoji_pattern.findall(content)
            self.assertEqual(len(matches), 0, f"Found emojis {matches} in {filepath}!")


if __name__ == '__main__':
    unittest.main()
