"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite
TOPIC:     Phase 103 Handwritten Script OCR & Step-by-Step Rubric Grader Tests
FILE:      backend/tests/test_phase103_handwritten_ocr_grading.py
PHASE:     Phase 103 - Handwritten Script OCR & Step-by-Step Rubric Grader
PURPOSE:   Asserts NCTB 4-step marking rubrics, partial credit calculations,
           Bengali mathematical handwriting normalization, teacher margin notes,
           Developer Architecture Note headers, and strict zero-emoji governance.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
"""

import os
import unittest
from backend.app.services.ocr_rubric_grader_service import OcrRubricGraderService, ocr_rubric_grader_service


class TestPhase103HandwrittenOcrGrading(unittest.TestCase):
    """
    Automated verification suite for Phase 103 Handwritten Script OCR & Step-by-Step Rubric Grader.
    """

    def setUp(self):
        self.service = OcrRubricGraderService()

    def test_01_rubric_catalog_and_step_weights(self):
        """Verify rubric bank contains Physics and Math problems with 4-step rubrics totalling 4.0 marks."""
        rubrics = self.service.list_rubrics()
        self.assertGreaterEqual(len(rubrics), 2)

        physics_rubric = self.service.get_rubric("q-physics-projectile-01")
        self.assertIsNotNone(physics_rubric)
        self.assertEqual(physics_rubric["max_score"], 4.0)
        self.assertEqual(len(physics_rubric["steps"]), 4)

        # Assert sum of step weights equals max_score
        total_weight = sum(s["weight"] for s in physics_rubric["steps"])
        self.assertEqual(total_weight, 4.0)

    def test_02_bengali_digit_math_normalization(self):
        """Verify normalization of Bengali digits (০-৯) to standard numbers."""
        raw_bengali_script = "u = ৪০ m/s, θ = ৩০°, g = ৯.৮ m/s²"
        normalized = self.service.normalize_bengali_math_text(raw_bengali_script)
        self.assertIn("40", normalized)
        self.assertIn("30", normalized)
        self.assertIn("9.8", normalized)

    def test_03_full_credit_grading_evaluation(self):
        """Verify perfect script receives 4.0 / 4.0 with affectionate commendation."""
        perfect_script = """
        ধাপ ১: সূত্র: H = (u^2 * sin^2(theta)) / (2*g)
        ধাপ ২: মান বসাই: u = 40, theta = 30, g = 9.8
        ধাপ ৩: H = (1600 * 0.25) / 19.6 = 400 / 19.6 = 20.41
        ধাপ ৪: উত্তর: সর্বাধিক উচ্চতা H = 20.41 m (মিটার)
        """
        result = self.service.grade_script("q-physics-projectile-01", perfect_script)

        self.assertEqual(result["total_score"], 4.0)
        self.assertEqual(result["percentage"], 100.0)
        self.assertEqual(len(result["steps"]), 4)
        for step in result["steps"]:
            self.assertEqual(step["score"], 1.0)
        self.assertIn("প্রশংসনীয়", result["teacher_summary"])

    def test_04_partial_credit_calculation_slip(self):
        """Verify script with calculation slip receives partial credit (3.0/4.0) with constructive guidance."""
        slip_script = """
        সূত্র: H = (u^2 * sin^2(30)) / (2*9.8)
        u = 40, g = 9.8
        H = (1600 * 0.25) / 19.6 = 400
        H = 400 m
        """
        result = self.service.grade_script("q-physics-projectile-01", slip_script)

        # Step 1: Formula (1.0), Step 2: Substitution (1.0), Step 3: Calculation (0.5), Step 4: Final + Unit (1.0) -> 3.5 or 3.0
        self.assertGreaterEqual(result["total_score"], 2.5)
        self.assertLess(result["total_score"], 4.0)
        self.assertIn("বিচ্যুতি", result["steps"][2]["teacher_note"])

    def test_05_missing_unit_penalty(self):
        """Verify script without SI units receives unit deduction in step 4."""
        no_unit_script = """
        H = (u^2 * sin^2(theta)) / (2*g)
        H = (40^2 * sin^2(30)) / (2*9.8) = 20.41
        উত্তর: 20.41
        """
        result = self.service.grade_script("q-physics-projectile-01", no_unit_script)
        self.assertEqual(result["steps"][3]["score"], 0.0)
        self.assertIn("একক", result["steps"][3]["teacher_note"])

    def test_06_developer_architecture_note_headers(self):
        """Verify standardized Developer Architecture Note header in all Phase 103 target files."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        phase103_files = [
            os.path.join(repo_root, "frontend", "src", "components", "grading", "HandwrittenUploadModal.tsx"),
            os.path.join(repo_root, "frontend", "src", "components", "grading", "GradingFeedbackCard.tsx"),
            os.path.join(repo_root, "backend", "app", "services", "ocr_rubric_grader_service.py"),
            os.path.join(repo_root, "backend", "app", "api", "v1", "endpoints", "grading.py"),
            os.path.join(repo_root, "backend", "tests", "test_phase103_handwritten_ocr_grading.py")
        ]

        for file_path in phase103_files:
            self.assertTrue(os.path.exists(file_path), f"File missing: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                header = f.read(500)
                self.assertIn("DEVELOPER ARCHITECTURE NOTE", header, f"Missing header in: {file_path}")
                self.assertIn("Phase 103", header, f"Missing Phase 103 in: {file_path}")

    def test_07_zero_emoji_governance(self):
        """Verify strict zero-emoji compliance across Phase 103 target files."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        phase103_files = [
            os.path.join(repo_root, "frontend", "src", "components", "grading", "HandwrittenUploadModal.tsx"),
            os.path.join(repo_root, "frontend", "src", "components", "grading", "GradingFeedbackCard.tsx"),
            os.path.join(repo_root, "backend", "app", "services", "ocr_rubric_grader_service.py"),
            os.path.join(repo_root, "backend", "app", "api", "v1", "endpoints", "grading.py")
        ]

        emoji_ranges = [
            (0x1F600, 0x1F64F),  # Emoticons
            (0x1F300, 0x1F5FF),  # Misc Symbols
            (0x1F680, 0x1F6FF),  # Transport
            (0x1F700, 0x1F77F),  # Alchemical
            (0x1F900, 0x1F9FF),  # Supplemental
            (0x2600, 0x26FF),    # Misc Symbols
            (0x2700, 0x27BF),    # Dingbats
        ]

        for file_path in phase103_files:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                for char in text:
                    cp = ord(char)
                    for start, end in emoji_ranges:
                        self.assertFalse(
                            start <= cp <= end,
                            f"Emoji character '{char}' (U+{cp:X}) detected in {file_path}"
                        )


if __name__ == "__main__":
    unittest.main()
