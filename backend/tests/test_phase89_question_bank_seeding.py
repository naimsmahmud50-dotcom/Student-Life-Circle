"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE - PHASE 89 TEST SUITE:
MODULE:    Question Bank Seeding & KaTeX Validation Test Engine
TOPIC:     Curriculum Seed Integrity, LaTeX Delimiters, SHA-256 Deduplication, Frontend A11y
FILE:      backend/tests/test_phase89_question_bank_seeding.py
PURPOSE:   Automated unit and integration test suite verifying:
           1. Existence and quotas of all 5 curriculum seed databases (100+ SSC Physics, HSC Chem, BUET, DU, Medical).
           2. Question integrity: exactly 4 unique options, exactly 1 correct answer, non-empty Bengali explanations.
           3. KaTeX Equation Sanitizer: balanced math delimiters ($...$, $$...$$), bracket closure, and macro validity.
           4. SHA-256 Content Deduplication: zero duplicate questions within or across board curriculum sets.
           5. QuestionBankSeeder execution in dry-run and live modes with zero invalid items.
           6. Frontend component presence and KaTeX/Diagram integration.
           7. Strict Zero-Emoji compliance and prominent Developer Architecture Notes.
AUDIENCE:  QA Engineers, Curriculum Specialists, Test Runners & AI Agents
STANDARDS: Python unittest, KaTeX v0.16+, NCTB Guidelines, Zero-Emoji Spec
========================================================================================
"""

import unittest
import json
import re
from pathlib import Path

from backend.scripts.seed_questions import (
    KaTeXEquationSanitizer,
    QuestionIntegrityValidator,
    DeduplicationEngine,
    QuestionBankSeeder
)


class TestCurriculumSeedFiles(unittest.TestCase):
    """Verifies existence, valid JSON structure, and item counts of the 5 curriculum databases."""

    SEEDS_DIR = Path("backend/app/db/seeds")

    def test_all_five_seed_files_exist(self):
        """Tests that all 5 required curriculum seed files exist on disk."""
        expected_files = [
            "nctb_ssc_physics.json",
            "nctb_hsc_chemistry.json",
            "buet_math_admission.json",
            "du_ka_admission.json",
            "medical_admission.json"
        ]
        for filename in expected_files:
            filepath = self.SEEDS_DIR / filename
            self.assertTrue(filepath.exists(), f"Missing curriculum seed file: {filepath}")

    def test_ssc_physics_has_over_100_board_questions(self):
        """Verifies nctb_ssc_physics.json contains 100+ past board questions."""
        filepath = self.SEEDS_DIR / "nctb_ssc_physics.json"
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 100, f"Expected 100+ SSC physics questions, found {len(data)}")

    def test_admission_datasets_counts(self):
        """Verifies HSC chemistry, BUET math, DU Ka, and Medical datasets have authentic counts."""
        dataset_expectations = {
            "nctb_hsc_chemistry.json": 30,
            "buet_math_admission.json": 30,
            "du_ka_admission.json": 30,
            "medical_admission.json": 30
        }
        for filename, min_count in dataset_expectations.items():
            filepath = self.SEEDS_DIR / filename
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertGreaterEqual(
                len(data),
                min_count,
                f"File {filename} has {len(data)} items, expected at least {min_count}"
            )


class TestQuestionIntegrity(unittest.TestCase):
    """Verifies that every question adheres to strict academic multiple-choice constraints."""

    SEEDS_DIR = Path("backend/app/db/seeds")

    def test_all_questions_have_exactly_four_unique_options_and_one_correct(self):
        """Ensures every question in all seed files has 4 options and 1 correct answer."""
        seed_files = [
            "nctb_ssc_physics.json",
            "nctb_hsc_chemistry.json",
            "buet_math_admission.json",
            "du_ka_admission.json",
            "medical_admission.json"
        ]

        total_checked = 0
        for filename in seed_files:
            filepath = self.SEEDS_DIR / filename
            with open(filepath, "r", encoding="utf-8") as f:
                questions = json.load(f)

            for idx, q in enumerate(questions):
                total_checked += 1
                is_valid, errors = QuestionIntegrityValidator.validate(q)
                self.assertTrue(
                    is_valid,
                    f"Integrity validation failed in {filename} item #{idx+1}: {errors}"
                )

                # Explicitly check 4 unique options
                options = q.get("options", [])
                self.assertEqual(len(options), 4, f"Question #{idx+1} in {filename} does not have 4 options")
                keys = [opt.get("key") or opt.get("option_key") for opt in options]
                self.assertEqual(sorted(keys), ["A", "B", "C", "D"])

                # Check explanation is non-empty Bengali
                explanation = q.get("explanation_bn", "")
                self.assertGreater(len(explanation.strip()), 5)

        self.assertGreaterEqual(total_checked, 250)


class TestKaTeXLaTeXValidation(unittest.TestCase):
    """Verifies KaTeX equation sanitization, delimiter balance, and math parsing."""

    def test_valid_latex_equations_pass(self):
        """Tests that standard math, physics, and chemistry equations pass validation."""
        valid_samples = [
            "গতিশক্তি $E_k = \\frac{1}{2}mv^2$ এবং ভরবেগ $p = mv$।",
            "পানির প্রতিসরাঙ্ক $n = \\frac{c}{v} = 1.33$।",
            "$\\vec{A} \\times \\vec{B} = \\vec{0}$ এবং $\\vec{A} \\cdot \\vec{B} = 0$",
            "$$\\lim_{x \\to 0} \\frac{\\tan x - \\sin x}{x^3} = \\frac{1}{2}$$",
            "লুকাস বিকারক ($ZnCl_2 + \\text{HCl}$) ৩° অ্যালকোহলের সাথে তৎক্ষণাৎ বিক্রিয়া করে।"
        ]
        for sample in valid_samples:
            is_valid, err = KaTeXEquationSanitizer.validate_latex(sample)
            self.assertTrue(is_valid, f"Expected valid LaTeX for: {sample}, error: {err}")

    def test_invalid_latex_fails(self):
        """Tests that unbalanced delimiters or brackets are rejected."""
        invalid_samples = [
            "বেগ $v = u + at এবং সরণ $s$।",  # Unbalanced single dollar sign
            "বল $F = \\frac{m}{a$",           # Unbalanced bracket inside math
            "ক্ষেত্রফল $A = \\pi r^{2$",      # Unbalanced curly brace
            "সমীকরণ $$ \\int x dx"            # Unclosed display math
        ]
        for sample in invalid_samples:
            is_valid, err = KaTeXEquationSanitizer.validate_latex(sample)
            self.assertFalse(is_valid, f"Expected invalid LaTeX for: {sample}")
            self.assertIsNotNone(err)

    def test_all_seed_equations_are_valid_katex(self):
        """Verifies that all 250+ seed questions contain 100% valid KaTeX syntax."""
        seeder = QuestionBankSeeder()
        seed_files = [
            "nctb_ssc_physics.json",
            "nctb_hsc_chemistry.json",
            "buet_math_admission.json",
            "du_ka_admission.json",
            "medical_admission.json"
        ]
        for sf in seed_files:
            filepath = seeder.seeds_dir / sf
            with open(filepath, "r", encoding="utf-8") as f:
                questions = json.load(f)
            for idx, q in enumerate(questions):
                # Validate stem
                v_stem, err_stem = KaTeXEquationSanitizer.validate_latex(q.get("stem_bn", ""))
                self.assertTrue(v_stem, f"LaTeX error in stem #{idx+1} of {sf}: {err_stem}")
                # Validate explanation
                v_exp, err_exp = KaTeXEquationSanitizer.validate_latex(q.get("explanation_bn", ""))
                self.assertTrue(v_exp, f"LaTeX error in explanation #{idx+1} of {sf}: {err_exp}")


class TestDeduplicationAndSeeder(unittest.TestCase):
    """Verifies SHA-256 question deduplication and seeder runner execution."""

    def test_deduplication_engine_detects_duplicates(self):
        """Tests that identical questions generate identical SHA-256 fingerprints."""
        stem = "স্কেলার রাশি কোনটি?"
        opts1 = [
            {"key": "A", "text_bn": "বেগ"},
            {"key": "B", "text_bn": "ত্বরণ"},
            {"key": "C", "text_bn": "বল"},
            {"key": "D", "text_bn": "কাজ"}
        ]
        opts2 = [
            {"key": "A", "text_bn": "কাজ"},
            {"key": "B", "text_bn": "বল"},
            {"key": "C", "text_bn": "ত্বরণ"},
            {"key": "D", "text_bn": "বেগ"}
        ]

        hash1 = DeduplicationEngine.compute_hash(stem, opts1)
        hash2 = DeduplicationEngine.compute_hash(stem, opts2)
        # Because options are sorted before hashing, order permutation yields identical hash
        self.assertEqual(hash1, hash2)

    def test_question_bank_seeder_run(self):
        """Runs the seeder in dry-run mode and verifies zero invalid questions."""
        seeder = QuestionBankSeeder()
        stats = seeder.seed_all(dry_run=True)

        self.assertEqual(stats["total_files"], 5)
        self.assertGreaterEqual(stats["total_questions_processed"], 250)
        self.assertEqual(stats["invalid_questions"], 0)
        self.assertEqual(stats["duplicates_filtered"], 0)
        self.assertGreaterEqual(stats["successfully_seeded"], 250)


class TestFrontendQuizComponents(unittest.TestCase):
    """Verifies frontend KaTeX renderer, scientific diagram, and question card components."""

    def test_katex_renderer_component(self):
        """Tests frontend/src/components/quiz/katex-renderer.tsx exists and has required logic."""
        file_path = Path("frontend/src/components/quiz/katex-renderer.tsx")
        self.assertTrue(file_path.exists(), "katex-renderer.tsx must exist")
        content = file_path.read_text(encoding="utf-8")

        self.assertIn("KaTeXRenderer", content)
        self.assertIn("display-math", content)
        self.assertIn("inline-math", content)
        self.assertIn('role="math"', content)
        self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)

    def test_scientific_diagram_component(self):
        """Tests frontend/src/components/quiz/scientific-diagram.tsx exists with pinch-to-zoom."""
        file_path = Path("frontend/src/components/quiz/scientific-diagram.tsx")
        self.assertTrue(file_path.exists(), "scientific-diagram.tsx must exist")
        content = file_path.read_text(encoding="utf-8")

        self.assertIn("ScientificDiagram", content)
        self.assertIn("handleTouchMove", content)
        self.assertIn("handleResetZoom", content)
        self.assertIn("scale", content)
        self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)

    def test_question_card_component(self):
        """Tests frontend/src/components/quiz/question-card.tsx exists with KaTeX and OptionCard."""
        file_path = Path("frontend/src/components/quiz/question-card.tsx")
        self.assertTrue(file_path.exists(), "question-card.tsx must exist")
        content = file_path.read_text(encoding="utf-8")

        self.assertIn("QuestionCard", content)
        self.assertIn("KaTeXRenderer", content)
        self.assertIn("OptionCard", content)
        self.assertIn("getDifficultyBadge", content)
        self.assertIn("ScientificDiagram", content)
        self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)

    def test_option_card_updated_with_katex(self):
        """Tests frontend/src/components/quiz/option-card.tsx integrates KaTeXRenderer."""
        file_path = Path("frontend/src/components/quiz/option-card.tsx")
        self.assertTrue(file_path.exists(), "option-card.tsx must exist")
        content = file_path.read_text(encoding="utf-8")

        self.assertIn("KaTeXRenderer", content)
        self.assertIn("<KaTeXRenderer content={textBn} />", content)


class TestZeroEmojiCompliance(unittest.TestCase):
    """Enforces zero-emoji standard across all Phase 89 files."""

    EMOJI_PATTERN = re.compile(
        r"[\U0001F600-\U0001F64F"
        r"\U0001F300-\U0001F5FF"
        r"\U0001F680-\U0001F6FF"
        r"\U0001F700-\U0001F77F"
        r"\U0001F780-\U0001F7FF"
        r"\U0001F800-\U0001F8FF"
        r"\U0001F900-\U0001F9FF"
        r"\U0001FA00-\U0001FA6F"
        r"\U0001FA70-\U0001FAFF"
        r"\U00002702-\U000027B0"
        r"\U000024C2-\U0001F251]"
    )

    FILES_TO_CHECK = [
        "backend/app/db/seeds/nctb_ssc_physics.json",
        "backend/app/db/seeds/nctb_hsc_chemistry.json",
        "backend/app/db/seeds/buet_math_admission.json",
        "backend/app/db/seeds/du_ka_admission.json",
        "backend/app/db/seeds/medical_admission.json",
        "backend/app/db/seeds/build_seed_datasets.py",
        "backend/scripts/seed_questions.py",
        "frontend/src/components/quiz/katex-renderer.tsx",
        "frontend/src/components/quiz/scientific-diagram.tsx",
        "frontend/src/components/quiz/question-card.tsx",
        "frontend/src/components/quiz/option-card.tsx"
    ]

    def test_strict_zero_emoji(self):
        """Verifies zero emojis exist in any Phase 89 file."""
        for file_rel in self.FILES_TO_CHECK:
            file_path = Path(file_rel)
            if not file_path.exists():
                continue
            content = file_path.read_text(encoding="utf-8")
            match = self.EMOJI_PATTERN.search(content)
            self.assertIsNone(match, f"Found prohibited emoji in {file_rel}: {match.group() if match else ''}")

    def test_developer_architecture_notes_presence(self):
        """Verifies developer architecture notes exist in Phase 89 code files."""
        code_files = [
            "backend/app/db/seeds/build_seed_datasets.py",
            "backend/scripts/seed_questions.py",
            "frontend/src/components/quiz/katex-renderer.tsx",
            "frontend/src/components/quiz/scientific-diagram.tsx",
            "frontend/src/components/quiz/question-card.tsx",
            "frontend/src/components/quiz/option-card.tsx"
        ]
        for file_rel in code_files:
            file_path = Path(file_rel)
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE", content, f"Missing architecture note in {file_rel}")


if __name__ == "__main__":
    unittest.main()
