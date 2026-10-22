"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite for NCTB Board Archives & KaTeX Bank
TOPIC:     Phase 112 Official NCTB Board Archives & KaTeX Mathematical Bank
FILE:      backend/tests/test_phase112_board_archives.py
PHASE:     Phase 112 - Official NCTB Board Archives & KaTeX Mathematical Bank
PURPOSE:   Automated unit and integration test suite certifying seed dataset integrity,
           cryptographic deduplication, balanced KaTeX math delimiters, faceted
           filtering performance, and strict zero-emoji compliance.
STANDARDS: NCTB Curriculum 2024, KaTeX Math Spec, UI/UX Pro Max, Strict Zero-Emoji
========================================================================================
"""

import json
import os
import re
import unittest
from pathlib import Path

from backend.app.services.board_archive_service import BoardArchiveService, board_archive_service


class TestPhase112BoardArchives(unittest.TestCase):
    """
    Test suite certifying Phase 112 Official NCTB Board Archives and KaTeX Bank.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.seed_file = cls.root_dir / "backend" / "app" / "db" / "seeds" / "nctb_board_past_papers_2015_2025.json"
        cls.frontend_viewer = cls.root_dir / "frontend" / "src" / "components" / "curriculum" / "BoardQuestionArchiveViewer.tsx"
        cls.frontend_page = cls.root_dir / "frontend" / "src" / "pages" / "board-archives.tsx"
        cls.service = board_archive_service

        cls.emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

    def test_01_seed_dataset_integrity(self):
        """Verifies existence, valid JSON, SSC/HSC coverage, 2015-2025 years, and subject breadth."""
        self.assertTrue(self.seed_file.exists(), "Seed file nctb_board_past_papers_2015_2025.json must exist.")
        
        with open(self.seed_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 15, "Archive must contain comprehensive question items.")

        levels = {item.get("level") for item in data}
        self.assertIn("SSC", levels, "Must include SSC questions.")
        self.assertIn("HSC", levels, "Must include HSC questions.")

        subjects = {item.get("subject") for item in data}
        expected_subjects = {"Physics", "Chemistry", "Higher Mathematics", "Biology", "Information & Communication Technology"}
        for subj in expected_subjects:
            self.assertIn(subj, subjects, f"Must include subject: {subj}")

        years = {item.get("year") for item in data}
        self.assertIn(2025, years, "Must include questions up to 2025.")
        self.assertIn(2015, years, "Must include questions from 2015.")

        question_types = {item.get("question_type") for item in data}
        self.assertIn("CQ", question_types, "Must include Creative Questions (CQ).")
        self.assertIn("MCQ", question_types, "Must include Multiple Choice Questions (MCQ).")

        # Verify CQ questions have 4 sub-questions (ka, kha, ga, gha)
        cq_items = [item for item in data if item.get("question_type") == "CQ"]
        for cq in cq_items:
            subs = cq.get("cq_sub_questions", {})
            self.assertIn("ka", subs, f"CQ {cq['id']} missing ka part")
            self.assertIn("kha", subs, f"CQ {cq['id']} missing kha part")
            self.assertIn("ga", subs, f"CQ {cq['id']} missing ga part")
            self.assertIn("gha", subs, f"CQ {cq['id']} missing gha part")
            self.assertEqual(cq.get("marks_total"), 10, "CQ total marks must equal 10.")

    def test_02_zero_duplicate_hashes_and_ids(self):
        """Verifies all questions possess unique identifiers and unique SHA-256 content hashes."""
        integrity_result = self.service.verify_archive_integrity()
        self.assertTrue(integrity_result["is_valid"], f"Archive integrity failed: {integrity_result}")
        self.assertEqual(len(integrity_result["duplicate_ids"]), 0, "Duplicate question IDs detected.")
        self.assertEqual(len(integrity_result["duplicate_hashes"]), 0, "Duplicate content hashes detected.")
        self.assertEqual(len(integrity_result["missing_fields"]), 0, "Questions missing required fields.")

    def test_03_katex_formula_validity(self):
        """Verifies that mathematical LaTeX equation delimiters are balanced and formatted cleanly."""
        integrity_result = self.service.verify_archive_integrity()
        self.assertEqual(
            len(integrity_result["katex_syntax_errors"]),
            0,
            f"KaTeX delimiter imbalance detected in questions: {integrity_result['katex_syntax_errors']}"
        )

        # Inspect sample LaTeX constructs
        all_papers = self.service.get_all_papers()
        combined_text = " ".join([p.get("stem_bn", "") + " " + p.get("explanation_bn", "") for p in all_papers])
        
        self.assertTrue(
            any(symbol in combined_text for symbol in ["\\frac", "\\sqrt", "\\cdot", "\\times", "t^2"]),
            "Archive must contain authentic LaTeX mathematical syntax."
        )

    def test_04_board_archive_service_filtering_and_facets(self):
        """Verifies multi-criteria filtering, search, pagination, and available facets."""
        # Filter by level
        hsc_papers = self.service.filter_papers(level="HSC")
        self.assertGreater(hsc_papers["total"], 0)
        for p in hsc_papers["items"]:
            self.assertEqual(p["level"], "HSC")

        # Filter by subject
        physics_papers = self.service.filter_papers(subject="Physics")
        self.assertGreater(physics_papers["total"], 0)
        for p in physics_papers["items"]:
            self.assertEqual(p["subject"], "Physics")

        # Filter by board and year
        dhaka_papers = self.service.filter_papers(board="Dhaka")
        self.assertGreater(dhaka_papers["total"], 0)
        for p in dhaka_papers["items"]:
            self.assertEqual(p["board"], "Dhaka")

        # Search query
        search_res = self.service.filter_papers(search_query="বল")
        self.assertGreater(search_res["total"], 0)

        # Test single item lookup
        first_id = physics_papers["items"][0]["id"]
        found = self.service.get_paper_by_id(first_id)
        self.assertIsNotNone(found)
        self.assertEqual(found["id"], first_id)

        # Facets
        facets = self.service.get_available_facets()
        self.assertIn("SSC", facets["levels"])
        self.assertIn("HSC", facets["levels"])
        self.assertIn(2025, facets["years"])
        self.assertIn(2015, facets["years"])

        # Stats
        stats = self.service.get_curriculum_coverage_stats()
        self.assertGreaterEqual(stats["total_questions"], 15)
        self.assertEqual(stats["year_range"], "2015-2025")
        self.assertTrue(stats["ka_tex_validated"])

    def test_05_frontend_archive_viewer_and_page_structure(self):
        """Verifies frontend components exist and declare required modes and typography."""
        self.assertTrue(self.frontend_viewer.exists(), "BoardQuestionArchiveViewer.tsx must exist.")
        self.assertTrue(self.frontend_page.exists(), "board-archives.tsx must exist.")

        viewer_code = self.frontend_viewer.read_text(encoding="utf-8")
        page_code = self.frontend_page.read_text(encoding="utf-8")

        # Check KaTeX Renderer integration
        self.assertIn("KaTeXRenderer", viewer_code)
        self.assertIn("katex-renderer", viewer_code)

        # Check Exam Mode & Study Mode
        self.assertIn("mode === 'study'", viewer_code)
        self.assertIn("mode === 'exam'", viewer_code)

        # Check Print Functionality
        self.assertIn("window.print()", viewer_code)
        self.assertIn("print:hidden", viewer_code)

        # Check Page Layout
        self.assertIn("<Navbar", page_code)
        self.assertIn("<Footer", page_code)
        self.assertIn("<AppHead", page_code)
        self.assertIn("BoardQuestionArchiveViewer", page_code)

    def test_06_developer_architecture_notes_and_strict_zero_emoji(self):
        """Asserts Developer Architecture Notes and strict Zero-Emoji compliance on all Phase 112 files."""
        target_files = [
            self.seed_file,
            self.root_dir / "backend" / "app" / "services" / "board_archive_service.py",
            self.root_dir / "backend" / "app" / "api" / "v1" / "endpoints" / "board_archives.py",
            self.frontend_viewer,
            self.frontend_page,
            Path(__file__).resolve(),
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")

            # Check header (skip pure json data)
            if file_path.suffix in [".py", ".tsx", ".ts"]:
                self.assertIn(
                    "DEVELOPER ARCHITECTURE NOTE:",
                    content,
                    f"File {file_path.name} missing Developer Architecture Note header."
                )

            # Check zero emojis
            matches = self.emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"File {file_path.name} violates strict Zero Emoji policy: found {matches}"
            )


if __name__ == "__main__":
    unittest.main()
