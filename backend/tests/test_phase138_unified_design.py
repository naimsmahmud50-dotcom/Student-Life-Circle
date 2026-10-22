"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Premium Design for Sub-pages
 * TOPIC:     Phase 138 Unified Design System, Tactile Physics & Sub-pages Elevation
 * FILE:      backend/tests/test_phase138_unified_design.py
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Automated test suite validating:
 *            1. Developer Architecture Note headers & file existence
 *            2. Strict Zero-Emoji compliance across all Phase 138 files
 *            3. UI Component Primitives export integrity in components/ui/index.ts
 *            4. Structural verification of Input, Select, Skeleton, EmptyState, ErrorState, PageHeader
 *            5. Sub-page integration across /practice, /board-archives, /modules, /learn, /dashboard
 *            6. Preservation of mission-critical test IDs in /practice
 *            7. Tactile 3D button physics and unified background tokens
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, UI/UX Pro Max, Academic Design
 */
"""

import os
import re
import unittest
from pathlib import Path

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class TestPhase138UnifiedDesign(unittest.TestCase):
    """
    Automated verification suite for Phase 138 Unified Premium Design for Sub-pages.
    """

    @classmethod
    def setUpClass(cls):
        cls.phase138_files = [
            REPO_ROOT / "frontend/src/components/ui/input.tsx",
            REPO_ROOT / "frontend/src/components/ui/select.tsx",
            REPO_ROOT / "frontend/src/components/ui/skeleton.tsx",
            REPO_ROOT / "frontend/src/components/ui/empty-state.tsx",
            REPO_ROOT / "frontend/src/components/ui/error-state.tsx",
            REPO_ROOT / "frontend/src/components/layout/PageHeader.tsx",
            REPO_ROOT / "frontend/src/pages/practice.tsx",
            REPO_ROOT / "frontend/src/pages/board-archives.tsx",
            REPO_ROOT / "frontend/src/pages/modules.tsx",
            REPO_ROOT / "frontend/src/pages/learn.tsx",
            REPO_ROOT / "frontend/src/pages/dashboard.tsx",
        ]

    def test_01_all_phase138_files_exist(self):
        """Verify that every Phase 138 component and page file exists."""
        for file_path in self.phase138_files:
            self.assertTrue(
                file_path.exists(),
                f"Missing Phase 138 file: {file_path.relative_to(REPO_ROOT)}"
            )

    def test_02_developer_architecture_note_headers(self):
        """Verify that every Phase 138 file has a Developer Architecture Note header."""
        for file_path in self.phase138_files:
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"File {file_path.name} missing DEVELOPER ARCHITECTURE NOTE header"
            )
            self.assertIn(
                "Phase 138",
                content,
                f"File {file_path.name} header does not reference Phase 138"
            )

    def test_03_strict_zero_emoji_compliance(self):
        """Verify that no Phase 138 file contains raw emojis."""
        violations = []
        for file_path in self.phase138_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            if matches:
                violations.append((file_path.name, matches))

        self.assertEqual(
            violations,
            [],
            f"Zero-Emoji violations detected in Phase 138 files: {violations}"
        )

    def test_04_ui_barrel_export_integrity(self):
        """Verify frontend/src/components/ui/index.ts exports all required primitives."""
        index_file = REPO_ROOT / "frontend/src/components/ui/index.ts"
        self.assertTrue(index_file.exists(), "components/ui/index.ts not found")
        content = index_file.read_text(encoding="utf-8")

        required_exports = [
            "input",
            "select",
            "skeleton",
            "empty-state",
            "error-state",
        ]
        for exp in required_exports:
            self.assertIn(
                exp,
                content,
                f"components/ui/index.ts does not export '{exp}'"
            )

    def test_05_input_primitive_capabilities(self):
        """Verify Input primitive has accessible label, helperText, error, prefix/suffix icons."""
        input_file = REPO_ROOT / "frontend/src/components/ui/input.tsx"
        content = input_file.read_text(encoding="utf-8")
        self.assertIn("label?: string", content)
        self.assertIn("error?: string", content)
        self.assertIn("helperText?: string", content)
        self.assertIn("prefixIcon", content)
        self.assertIn("suffixIcon", content)

    def test_06_select_primitive_capabilities(self):
        """Verify Select primitive has accessible options array, label, error, helperText."""
        select_file = REPO_ROOT / "frontend/src/components/ui/select.tsx"
        content = select_file.read_text(encoding="utf-8")
        self.assertIn("SelectOption", content)
        self.assertIn("options?: SelectOption[]", content)
        self.assertIn("label?: string", content)
        self.assertIn("error?: string", content)

    def test_07_page_header_capabilities(self):
        """Verify PageHeader component supports ambient glow, breadcrumbs, and stats bento."""
        header_file = REPO_ROOT / "frontend/src/components/layout/PageHeader.tsx"
        content = header_file.read_text(encoding="utf-8")
        self.assertIn("PageHeaderProps", content)
        self.assertIn("breadcrumbs?: BreadcrumbItem[]", content)
        self.assertIn("stats?: PageHeaderStat[]", content)
        self.assertIn("blur-3xl", content)

    def test_08_practice_page_elevation_and_test_ids(self):
        """Verify /practice integrates PageHeader, CardSkeleton and preserves critical test IDs."""
        practice_file = REPO_ROOT / "frontend/src/pages/practice.tsx"
        content = practice_file.read_text(encoding="utf-8")

        # Test ID preservation
        self.assertIn('data-testid="practice-exam-arena"', content)
        self.assertIn('data-testid="submit-answer-btn"', content)
        self.assertIn('data-testid="submit-exam-script-btn"', content)
        self.assertIn('data-testid="next-question-btn"', content)

        # Unified component usage
        self.assertIn("PageHeader", content)
        self.assertIn("CardSkeleton", content)
        self.assertIn("ErrorState", content)

    def test_09_board_archives_page_elevation(self):
        """Verify /board-archives synchronizes global theme and uses PageHeader."""
        archives_file = REPO_ROOT / "frontend/src/pages/board-archives.tsx"
        content = archives_file.read_text(encoding="utf-8")

        # Must not have isolated theme state that breaks root dark class
        self.assertNotIn("useState<'light' | 'dark'>('light')", content)
        self.assertNotIn("toggleTheme", content)

        # Must use PageHeader and standard layout
        self.assertIn("PageHeader", content)
        self.assertIn("Navbar", content)
        self.assertIn("Footer", content)
        self.assertIn("BoardQuestionArchiveViewer", content)

    def test_10_modules_page_elevation(self):
        """Verify /modules uses standard Navbar, PageHeader, and Footer."""
        modules_file = REPO_ROOT / "frontend/src/pages/modules.tsx"
        content = modules_file.read_text(encoding="utf-8")

        self.assertIn("Navbar", content)
        self.assertIn("PageHeader", content)
        self.assertIn("Footer", content)
        self.assertIn("ModuleDirectory", content)

    def test_11_tactile_3d_physics_tokens(self):
        """Verify 3D button press physics are present in sub-pages."""
        for path in [
            REPO_ROOT / "frontend/src/pages/practice.tsx",
            REPO_ROOT / "frontend/src/pages/board-archives.tsx",
            REPO_ROOT / "frontend/src/pages/learn.tsx",
            REPO_ROOT / "frontend/src/pages/dashboard.tsx",
        ]:
            content = path.read_text(encoding="utf-8")
            has_tactile = (
                "active:translate-y-1" in content or
                "active:translate-y-0.5" in content or
                "btn-3d-oxford" in content or
                "shadow-[0_4px_0_0" in content
            )
            self.assertTrue(
                has_tactile,
                f"File {path.name} lacks 3D tactile button physics tokens"
            )

    def test_12_unified_background_tokens(self):
        """Verify unified paper ivory / linear dark theme tokens across all sub-pages."""
        for path in [
            REPO_ROOT / "frontend/src/pages/practice.tsx",
            REPO_ROOT / "frontend/src/pages/board-archives.tsx",
            REPO_ROOT / "frontend/src/pages/modules.tsx",
            REPO_ROOT / "frontend/src/pages/learn.tsx",
            REPO_ROOT / "frontend/src/pages/dashboard.tsx",
        ]:
            content = path.read_text(encoding="utf-8")
            self.assertIn(
                "bg-[#FAFAF8]",
                content,
                f"File {path.name} missing paper ivory background token bg-[#FAFAF8]"
            )
            self.assertIn(
                "dark:bg-[#090D16]",
                content,
                f"File {path.name} missing linear dark theme token dark:bg-[#090D16]"
            )


if __name__ == "__main__":
    unittest.main()
