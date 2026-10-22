"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic Math & Science Whiteboard Solver
 * TOPIC:     Phase 132 Interactive Canvas & Pedagogical Socratic Step Guidance
 * FILE:      backend/tests/test_phase132_socratic_whiteboard.py
 * PHASE:     Phase 132 - Real-time Socratic AI Whiteboard Solver
 * PURPOSE:   Automated test suite validating:
 *            1. Developer Architecture Note headers & file presence
 *            2. Socratic session creation, lifecycle, and zero-IDOR multi-tenant isolation
 *            3. Pedagogical Hint Guard preventing direct solution leaking
 *            4. Common mathematical and physical STEM misconception detection
 *            5. Drawing stroke coordinate sanity, bounding boxes, and canvas buffer
 *            6. Step inquiry deduction evaluation and progressive milestone completion
 *            7. Supabase migration 010 Row Level Security policies
 *            8. Frontend canvas UI styling, 3D tactile buttons, and Zero-Emoji compliance
 * STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Pedagogical Hint Guard
 */
"""

import math
import os
import re
import unittest
from pathlib import Path

from backend.socratic.whiteboard_solver import (
    DirectAnswerLeakedException,
    DrawingStroke,
    DrawingStrokeBuffer,
    DrawingToolType,
    InvalidStrokeCoordinateException,
    MisconceptionDetector,
    PedagogicalHintGuard,
    Point2D,
    ProblemDomain,
    SocraticProblemSession,
    SocraticStep,
    SocraticWhiteboardSolver,
    UnauthorizedSessionAccessException,
)

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase132SocraticWhiteboard(unittest.TestCase):
    """
    Automated verification suite for Phase 132 Socratic Math & Science Whiteboard Solver.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.socratic_init = cls.root_dir / "backend" / "socratic" / "__init__.py"
        cls.solver_py = cls.root_dir / "backend" / "socratic" / "whiteboard_solver.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "010_socratic_whiteboard_rls.sql"
        cls.solver_tsx = cls.root_dir / "frontend" / "src" / "pages" / "socratic" / "solver.tsx"
        cls.test_py = cls.root_dir / "backend" / "tests" / "test_phase132_socratic_whiteboard.py"

    def test_01_all_phase132_files_exist_with_developer_headers(self):
        """Validates that all Phase 132 core files exist and possess mandatory Developer Architecture Note headers."""
        target_files = [
            self.socratic_init,
            self.solver_py,
            self.migration_sql,
            self.solver_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Missing required Phase 132 file: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE:", content, f"Missing Architecture header in {file_path}")
            self.assertIn("Phase 132", content, f"Missing Phase 132 reference in {file_path}")
            self.assertIn("Socratic Math & Science Whiteboard Solver", content, f"Missing module in {file_path}")

    def test_02_zero_emoji_compliance(self):
        """Strictly enforces zero emoji in all created Phase 132 code and migration files."""
        target_files = [
            self.socratic_init,
            self.solver_py,
            self.migration_sql,
            self.solver_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(len(matches), 0, f"Emoji violations detected in {file_path}: {matches}")

    def test_03_session_creation_and_zero_idor_isolation(self):
        """Validates session registration and IDOR multi-tenant defense."""
        solver = SocraticWhiteboardSolver()
        student_a = "student_alpha_001"
        student_b = "student_beta_002"

        session = solver.create_session(student_a, problem_key="prob_quad_01")
        self.assertTrue(session.session_id.startswith("socr_"))
        self.assertEqual(session.student_id, student_a)
        self.assertEqual(len(session.steps), 3)

        # Authorized access
        retrieved = solver.get_session(session.session_id, student_a)
        self.assertEqual(retrieved.session_id, session.session_id)

        # IDOR attempt by foreign student
        with self.assertRaises(UnauthorizedSessionAccessException):
            solver.get_session(session.session_id, student_b)

    def test_04_pedagogical_hint_guard_and_answer_leak_defense(self):
        """Tests that the Pedagogical Hint Guard prevents premature terminal answer dumping."""
        # Clean conceptual hint passes
        clean_hint = "উভয়পক্ষকে ২ দিয়ে ভাগ করে দেখুন x^2 এর সহগ কত দাঁড়ায়।"
        PedagogicalHintGuard.assert_no_direct_answer_leak(clean_hint, is_final_step=False)

        # Direct answer leaks must raise DirectAnswerLeakedException
        leaky_hints = [
            "সরাসরি উত্তর হলো x = 3",
            "The final answer is x = 4",
            "চূড়ান্ত সমাধান হলো x = 1/2",
            "অতএব উত্তর হলো ৪২",
        ]

        for bad_hint in leaky_hints:
            with self.assertRaises(DirectAnswerLeakedException):
                PedagogicalHintGuard.assert_no_direct_answer_leak(bad_hint, is_final_step=False)

        # Hint request sequential level validation
        self.assertTrue(PedagogicalHintGuard.validate_hint_request(current_level=1, requested_level=2))
        self.assertFalse(PedagogicalHintGuard.validate_hint_request(current_level=1, requested_level=3))

    def test_05_stem_misconception_detection(self):
        """Asserts accurate detection of classical STEM mathematical and physical misconceptions."""
        # 1. Freshman Exponent Trap in Algebra: (a + b)^2 = a^2 + b^2
        res_alg = MisconceptionDetector.evaluate_expression(
            ProblemDomain.ALGEBRA,
            "(a + b)^2 = a^2 + b^2"
        )
        self.assertIsNotNone(res_alg)
        self.assertEqual(res_alg["rule_id"], "FRESHMAN_EXPONENT_TRAP")
        self.assertIn("2ab", res_alg["remediation_bn"])

        # 2. Pythagorean Trigonometric Confusion: sin^2(x) - cos^2(x) = 1
        res_trig = MisconceptionDetector.evaluate_expression(
            ProblemDomain.TRIGONOMETRY,
            "sin^2 x - cos^2 x = 1"
        )
        self.assertIsNotNone(res_trig)
        self.assertEqual(res_trig["rule_id"], "TRIG_PYTHAGOREAN_CONFUSION")

        # 3. Missing Constant of Integration in Calculus
        res_calc_bad = MisconceptionDetector.evaluate_expression(
            ProblemDomain.CALCULUS,
            r"\int x dx = x^2/2"
        )
        self.assertIsNotNone(res_calc_bad)
        self.assertEqual(res_calc_bad["rule_id"], "CALCULUS_MISSING_CONSTANT")

        # Integral with constant correctly does NOT trigger misconception
        res_calc_good = MisconceptionDetector.evaluate_expression(
            ProblemDomain.CALCULUS,
            r"\int x dx = x^2/2 + C"
        )
        self.assertIsNone(res_calc_good)

        # 4. Derivative of Cosine missing negative sign
        res_deriv = MisconceptionDetector.evaluate_expression(
            ProblemDomain.CALCULUS,
            "d/dx(cos x) = sin x"
        )
        self.assertIsNotNone(res_deriv)
        self.assertEqual(res_deriv["rule_id"], "DERIVATIVE_COSINE_SIGN")

        # 5. Newton's 3rd Law Cancellation Myth in Mechanics
        res_mech = MisconceptionDetector.evaluate_expression(
            ProblemDomain.MECHANICS,
            "action and reaction cancel"
        )
        self.assertIsNotNone(res_mech)
        self.assertEqual(res_mech["rule_id"], "NEWTON_THIRD_LAW_PAIR")

    def test_06_drawing_stroke_buffer_and_coordinates(self):
        """Tests whiteboard canvas stroke ingestion, boundary bounds, and bounding box computation."""
        # Valid points
        p1 = Point2D(x=100.0, y=150.0, pressure=0.8)
        p2 = Point2D(x=200.0, y=250.0, pressure=0.9)
        self.assertTrue(p1.is_valid())

        stroke = DrawingStroke(
            stroke_id="strk_01",
            tool=DrawingToolType.PENCIL,
            color_hex="#0A2540",
            width=2.5,
            points=[p1, p2],
        )

        strokes: list = []
        strokes = DrawingStrokeBuffer.validate_and_append_stroke(strokes, stroke)
        self.assertEqual(len(strokes), 1)

        # Bounding Box Calculation
        bbox = DrawingStrokeBuffer.calculate_bounding_box(strokes)
        self.assertEqual(bbox, (100.0, 150.0, 200.0, 250.0))

        # Out of bounds points rejected
        bad_points = [
            Point2D(x=-10.0, y=50.0),
            Point2D(x=50.0, y=2500.0),
            Point2D(x=float("nan"), y=50.0),
        ]
        for bp in bad_points:
            bad_stroke = DrawingStroke(
                stroke_id="strk_bad",
                tool=DrawingToolType.PENCIL,
                color_hex="#0A2540",
                width=2.0,
                points=[bp],
            )
            with self.assertRaises(InvalidStrokeCoordinateException):
                DrawingStrokeBuffer.validate_and_append_stroke(strokes, bad_stroke)

    def test_07_stroke_serialization_roundtrip(self):
        """Verifies stroke JSON dictionary serialization and reconstruction."""
        p1 = Point2D(x=50.0, y=75.0, pressure=0.5)
        stroke = DrawingStroke(
            stroke_id="strk_roundtrip",
            tool=DrawingToolType.RULER,
            color_hex="#B45309",
            width=4.0,
            points=[p1],
            created_at=1700000000.0,
        )

        stroke_dict = stroke.to_dict()
        reconstructed = DrawingStroke.from_dict(stroke_dict)

        self.assertEqual(reconstructed.stroke_id, stroke.stroke_id)
        self.assertEqual(reconstructed.tool, DrawingToolType.RULER)
        self.assertEqual(reconstructed.color_hex, "#B45309")
        self.assertEqual(reconstructed.width, 4.0)
        self.assertEqual(len(reconstructed.points), 1)
        self.assertEqual(reconstructed.points[0].x, 50.0)

    def test_08_progressive_step_inquiry_and_milestones(self):
        """Tests student inquiry submission, progression, and milestone completion."""
        solver = SocraticWhiteboardSolver()
        student_id = "stu_progress_01"
        session = solver.create_session(student_id, problem_key="prob_quad_01")

        # Step 0: Initial state
        self.assertEqual(session.current_step_index, 0)
        self.assertFalse(session.is_all_steps_completed())

        # Unlock hints progressively
        step_0 = solver.unlock_next_hint(session.session_id, student_id)
        self.assertEqual(step_0.revealed_hint_level, 2)

        # Misconception check on deduction
        trap_resp = solver.submit_step_response(
            session.session_id,
            student_id,
            "(a+b)^2 = a^2 + b^2"
        )
        self.assertFalse(trap_resp["is_correct"])
        self.assertTrue(trap_resp["has_misconception"])

        # Incorrect submission
        vague_resp = solver.submit_step_response(
            session.session_id,
            student_id,
            "কিছু বুঝতে পারছি না"
        )
        self.assertFalse(vague_resp["is_correct"])
        self.assertFalse(vague_resp["has_misconception"])

        # Correct deduction for Step 0 (keyword 'ভাগ' or '2')
        valid_step0 = solver.submit_step_response(
            session.session_id,
            student_id,
            "উভয়পক্ষকে ২ দিয়ে ভাগ করতে হবে"
        )
        self.assertTrue(valid_step0["is_correct"])
        self.assertEqual(session.current_step_index, 1)

        # Correct deduction for Step 1 (keyword '7/4')
        valid_step1 = solver.submit_step_response(
            session.session_id,
            student_id,
            "মধ্যপদের জন্য b = 7/4"
        )
        self.assertTrue(valid_step1["is_correct"])
        self.assertEqual(session.current_step_index, 2)

        # Correct deduction for Step 2 (keyword '81/16')
        valid_step2 = solver.submit_step_response(
            session.session_id,
            student_id,
            "উভয়পক্ষে (7/4)^2 যোগ করলে ডানপক্ষে মান হয় 81/16"
        )
        self.assertTrue(valid_step2["is_correct"])
        self.assertTrue(valid_step2["all_steps_completed"])
        self.assertTrue(session.is_all_steps_completed())

    def test_09_supabase_migration_010_rls_integrity(self):
        """Verifies migration 010 establishes whiteboard tables and enforces 100% RLS."""
        sql_content = self.migration_sql.read_text(encoding="utf-8")

        required_tables = [
            "socratic_whiteboard_sessions",
            "socratic_step_attempts",
            "socratic_saved_workbooks",
        ]

        for tbl in required_tables:
            has_table = f"CREATE TABLE IF NOT EXISTS public.{tbl}" in sql_content or f"CREATE TABLE IF NOT EXISTS {tbl}" in sql_content
            self.assertTrue(has_table, f"Missing table creation for {tbl}")
            has_rls = f"ALTER TABLE public.{tbl} ENABLE ROW LEVEL SECURITY;" in sql_content or f"ALTER TABLE {tbl} ENABLE ROW LEVEL SECURITY;" in sql_content
            self.assertTrue(has_rls, f"Missing RLS enablement for {tbl}")

        # Confirm policy includes auth.uid() = user_id
        self.assertIn("auth.uid() = user_id", sql_content)
        self.assertIn("service_role", sql_content)

    def test_10_frontend_canvas_styling_and_icons(self):
        """Validates frontend solver page implements Paper Ivory canvas, 3D buttons, and pure Lucide icons."""
        tsx_content = self.solver_tsx.read_text(encoding="utf-8")

        # Academic paper ivory palette & 3D tactile buttons
        self.assertTrue(
            "bg-[#FAFAF8]" in tsx_content or "#FAFAF8" in tsx_content,
            "Missing Paper Ivory styling"
        )
        self.assertTrue("shadow-[0_4px_0_0" in tsx_content, "Missing 3D tactile button styling")

        # Drawing tool references
        self.assertIn("Pencil", tsx_content)
        self.assertIn("Ruler", tsx_content)
        self.assertIn("Compass", tsx_content)
        self.assertIn("Eraser", tsx_content)

        # Lucide vector icons
        expected_icons = ["Pencil", "Ruler", "Compass", "Eraser", "Sparkles", "CheckCircle2", "HelpCircle"]
        for icon in expected_icons:
            self.assertIn(icon, tsx_content, f"Missing expected Lucide icon: {icon}")


if __name__ == "__main__":
    unittest.main()
