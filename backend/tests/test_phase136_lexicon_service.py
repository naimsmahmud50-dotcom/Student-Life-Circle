"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Bilingual Curriculum Engine & NCTB Terminology Lexicon
 * TOPIC:     Phase 136 Instant Medium Switcher & Contextual Academic Terminology
 * FILE:      backend/tests/test_phase136_lexicon_service.py
 * PHASE:     Phase 136 - Dual-Curriculum Bilingual Terminology Switcher
 * PURPOSE:   Automated test suite validating:
 *            1. Developer Architecture Note headers & file presence
 *            2. Strict Zero-Emoji compliance
 *            3. Bidirectional lexicon lookup across Bengali and English terms
 *            4. Domain filtering by subject and grade tier
 *            5. Auto-glossing algorithms and reciprocal term embedding
 *            6. Multi-medium exam question rendering (Bangla, English, Dual, Inline)
 *            7. Benchmark question integrity and valid option indices
 *            8. Supabase migration 014 Row Level Security policies
 *            9. Frontend typography declarations and 3D tactile button styling
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Pure Academic Design, NCTB Aligned
 */
"""

import os
import re
import unittest
from pathlib import Path

from backend.curriculum.lexicon_service import (
    AcademicMedium,
    BENCHMARK_BILINGUAL_QUESTIONS,
    BENCHMARK_NCTB_LEXICON,
    BilingualQuestionItem,
    CurriculumSubject,
    GradeTier,
    NCTBLexiconEntry,
    NCTBLexiconService,
)

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase136LexiconService(unittest.TestCase):
    """
    Automated verification suite for Phase 136 Dual-Curriculum Bilingual Terminology Switcher.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.curriculum_init = cls.root_dir / "backend" / "curriculum" / "__init__.py"
        cls.service_py = cls.root_dir / "backend" / "curriculum" / "lexicon_service.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "014_curriculum_lexicon_rls.sql"
        cls.lexicon_tsx = cls.root_dir / "frontend" / "src" / "pages" / "curriculum" / "lexicon.tsx"
        cls.test_py = cls.root_dir / "backend" / "tests" / "test_phase136_lexicon_service.py"

    def test_01_all_phase136_files_exist_with_developer_headers(self):
        """Validates that all Phase 136 core files exist and possess mandatory Developer Architecture Note headers."""
        target_files = [
            self.curriculum_init,
            self.service_py,
            self.migration_sql,
            self.lexicon_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Missing required Phase 136 file: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE:", content, f"Missing Architecture header in {file_path}")
            self.assertIn("Phase 136", content, f"Missing Phase 136 reference in {file_path}")
            self.assertIn("Bilingual Curriculum Engine & NCTB Terminology Lexicon", content, f"Missing module in {file_path}")

    def test_02_zero_emoji_compliance(self):
        """Strictly enforces zero emoji in all created Phase 136 code and migration files."""
        target_files = [
            self.curriculum_init,
            self.service_py,
            self.migration_sql,
            self.lexicon_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(len(matches), 0, f"Emoji violations detected in {file_path}: {matches}")

    def test_03_bidirectional_lexicon_lookup(self):
        """Validates O(1) bidirectional lookup across Bengali and English terms."""
        service = NCTBLexiconService()

        # Lookup by Bengali term
        entry_kinematics = service.lookup_by_term("গতিবিদ্যা")
        self.assertIsNotNone(entry_kinematics)
        self.assertEqual(entry_kinematics.term_en, "Kinematics")
        self.assertEqual(entry_kinematics.subject, CurriculumSubject.PHYSICS)
        self.assertEqual(entry_kinematics.nctb_code, "NCTB-PHY-C02-KINEMATICS")

        # Lookup by English term (case-insensitive)
        entry_periodic = service.lookup_by_term("periodic table")
        self.assertIsNotNone(entry_periodic)
        self.assertEqual(entry_periodic.term_bn, "পর্যায় সারণি")
        self.assertEqual(entry_periodic.subject, CurriculumSubject.CHEMISTRY)

        # Lookup by exact ID
        entry_diff = service.lookup_by_id("LEX-MAT-001")
        self.assertIsNotNone(entry_diff)
        self.assertEqual(entry_diff.term_en, "Differentiation")
        self.assertEqual(entry_diff.term_bn, "অন্তরীকরণ")

    def test_04_lexicon_search_and_filters(self):
        """Validates keyword search and subject/grade filtering."""
        service = NCTBLexiconService()

        # Search by physics subject
        physics_entries = service.search_entries(subject=CurriculumSubject.PHYSICS)
        self.assertGreaterEqual(len(physics_entries), 4)
        for e in physics_entries:
            self.assertEqual(e.subject, CurriculumSubject.PHYSICS)

        # Search by chemistry subject
        chem_entries = service.search_entries(subject=CurriculumSubject.CHEMISTRY)
        self.assertGreaterEqual(len(chem_entries), 3)

        # Keyword search for "acid"
        acid_results = service.search_entries(query="acid")
        self.assertTrue(any(e.term_en == "Acid-Base Equilibrium" for e in acid_results))

        # Keyword search for Bengali "শ্বসন"
        resp_results = service.search_entries(query="শ্বসন")
        self.assertTrue(any(e.term_en == "Cellular Respiration" for e in resp_results))

    def test_05_unknown_term_handling_and_fallbacks(self):
        """Validates that unknown terms gracefully return None and empty queries return all entries."""
        service = NCTBLexiconService()

        self.assertIsNone(service.lookup_by_term("NonExistentAcademicTerm123"))
        self.assertIsNone(service.lookup_by_id("LEX-NONEXISTENT"))

        all_entries = service.search_entries()
        self.assertEqual(len(all_entries), service.total_entries)

    def test_06_text_auto_glossing_bangla_and_english(self):
        """Validates that auto-glossing algorithm embeds reciprocal translations."""
        service = NCTBLexiconService()

        # Bengali text glossing
        raw_bn = "পদার্থবিজ্ঞানে গতিবিদ্যা হলো একটি গুরুত্বপূর্ণ অধ্যায়।"
        annotated_bn = service.annotate_text_with_glossary(raw_bn, AcademicMedium.BANGLA)
        self.assertIn("গতিবিদ্যা (Kinematics)", annotated_bn)

        # English text glossing
        raw_en = "According to Kinematics, acceleration determines the rate of change of velocity."
        annotated_en = service.annotate_text_with_glossary(raw_en, AcademicMedium.ENGLISH_VERSION)
        self.assertIn("Kinematics (গতিবিদ্যা)", annotated_en)

    def test_07_exam_question_rendering_across_all_four_mediums(self):
        """Validates that render_question correctly formats all 4 medium variants."""
        service = NCTBLexiconService()
        benchmark_questions = service.get_benchmark_questions()
        q1 = benchmark_questions[0]

        # 1. Pure Bangla Medium
        rendered_bn = service.render_question(q1, AcademicMedium.BANGLA)
        self.assertEqual(rendered_bn["medium"], "BANGLA")
        self.assertEqual(rendered_bn["mode"], "SINGLE_MEDIUM")
        self.assertEqual(rendered_bn["prompt"], q1.prompt_bn)
        self.assertIsNone(rendered_bn["secondary"])

        # 2. Pure English Version
        rendered_en = service.render_question(q1, AcademicMedium.ENGLISH_VERSION)
        self.assertEqual(rendered_en["medium"], "ENGLISH_VERSION")
        self.assertEqual(rendered_en["mode"], "SINGLE_MEDIUM")
        self.assertEqual(rendered_en["prompt"], q1.prompt_en)
        self.assertIsNone(rendered_en["secondary"])

        # 3. Side-by-Side Dual Medium
        rendered_dual = service.render_question(q1, AcademicMedium.BILINGUAL_DUAL)
        self.assertEqual(rendered_dual["medium"], "BILINGUAL_DUAL")
        self.assertEqual(rendered_dual["mode"], "SIDE_BY_SIDE")
        self.assertEqual(rendered_dual["prompt"], q1.prompt_bn)
        self.assertIsNotNone(rendered_dual["secondary"])
        self.assertEqual(rendered_dual["secondary"]["prompt"], q1.prompt_en)

        # 4. Inline Annotated Mode
        rendered_inline = service.render_question(q1, AcademicMedium.INLINE_ANNOTATED)
        self.assertEqual(rendered_inline["medium"], "INLINE_ANNOTATED")
        self.assertEqual(rendered_inline["mode"], "INLINE_GLOSS")
        self.assertIn("গতিবিদ্যা (Kinematics)", rendered_inline["prompt"])

    def test_08_benchmark_questions_integrity(self):
        """Validates that all benchmark questions have valid option sets and correct indices."""
        service = NCTBLexiconService()
        questions = service.get_benchmark_questions()
        self.assertGreaterEqual(len(questions), 3)

        for q in questions:
            self.assertEqual(len(q.options_bn), 4, f"Question {q.question_id} must have exactly 4 Bengali options")
            self.assertEqual(len(q.options_en), 4, f"Question {q.question_id} must have exactly 4 English options")
            self.assertTrue(0 <= q.correct_index < 4, f"Invalid correct_index for {q.question_id}")
            self.assertTrue(len(q.prompt_bn) > 10)
            self.assertTrue(len(q.prompt_en) > 10)

    def test_09_migration_014_supabase_rls_security(self):
        """Verifies that migration 014 enables and forces RLS on all 4 tables with zero-IDOR policies."""
        sql_content = self.migration_sql.read_text(encoding="utf-8")
        required_tables = [
            "nctb_lexicon_entries",
            "bilingual_exam_templates",
            "student_medium_preferences",
            "lexicon_search_logs",
        ]

        for table in required_tables:
            self.assertIn(f"ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;", sql_content)
            self.assertIn(f"ALTER TABLE public.{table} FORCE ROW LEVEL SECURITY;", sql_content)

        # Verify tenant isolation and service_role clauses
        self.assertIn("auth.uid()", sql_content)
        self.assertIn("service_role", sql_content)

    def test_10_frontend_lexicon_markup_and_styling(self):
        """Verifies frontend console contains required medium switcher, fonts, and 3D tactile buttons."""
        tsx_content = self.lexicon_tsx.read_text(encoding="utf-8")
        self.assertIn("Hind_Siliguri", tsx_content)
        self.assertIn("Inter", tsx_content)
        self.assertIn("shadow-[0_4px_0_0_#051329]", tsx_content)
        self.assertIn("BENCHMARK_LEXICON_DATA", tsx_content)
        self.assertIn("BENCHMARK_EXAM_QUESTIONS", tsx_content)
        self.assertIn("toBengaliDigits", tsx_content)


if __name__ == "__main__":
    unittest.main()
