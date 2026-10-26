"""
========================================================================================
MODULE:    Phase 164 - Live MCQ Routine & Mega Model Test Hub Verification Suite
FILE:      backend/tests/test_phase164_exam_routine_and_model_test.py
PURPOSE:   Comprehensive unit and integration test suite validating the 200-day BCS
           and Admission daily routine calendar, Friday Mega Model Test countdowns,
           negative marking score calculations (+1.0 / -0.25, -0.50), and reminder subscriptions.
STANDARDS: Zero-Emoji, ASVS L2, Resilient BaseDTO, 100% Deterministic Execution
========================================================================================
"""

import unittest
import os
from backend.app.core.fastapi_shim import HTTPException, status
from backend.app.core.config import settings
from backend.app.schemas.exam_routine_schema import (
    ExamTypeEnum,
    TrackCategoryEnum,
    ExamRoutineItem,
    NegativeMarkSimulationRequest,
    RoutineSubscribeRequest,
)
from backend.app.services.exam_routine_service import exam_routine_service
from backend.app.api.v1.endpoints.exam_routine_router import (
    list_exam_routines,
    get_exam_routine_detail,
    simulate_negative_marking_score,
    subscribe_to_routine_alerts,
)


class TestExamRoutineAndModelTestHub(unittest.TestCase):
    def setUp(self):
        self.service = exam_routine_service

    def test_01_get_routines_default(self):
        res = self.service.get_routines()
        self.assertTrue(res.success)
        self.assertGreaterEqual(len(res.routines), 6)
        self.assertEqual(res.active_day, 42)
        self.assertIsNotNone(res.mega_test_scheduled_at)
        self.assertTrue(bool(res.server_time))

    def test_02_filter_by_exam_type(self):
        res_bcs = self.service.get_routines(exam_type=ExamTypeEnum.BCS_PRELI)
        self.assertTrue(all(r.exam_type == ExamTypeEnum.BCS_PRELI for r in res_bcs.routines))

        res_adm = self.service.get_routines(exam_type=ExamTypeEnum.ADMISSION_VARSITY)
        self.assertTrue(all(r.exam_type == ExamTypeEnum.ADMISSION_VARSITY for r in res_adm.routines))

    def test_03_filter_by_track_category(self):
        res_bangla = self.service.get_routines(track_category=TrackCategoryEnum.BANGLA)
        self.assertTrue(all(r.track_category == TrackCategoryEnum.BANGLA for r in res_bangla.routines))

        res_math = self.service.get_routines(track_category=TrackCategoryEnum.MATH_SCIENCE)
        self.assertTrue(all(r.track_category == TrackCategoryEnum.MATH_SCIENCE for r in res_math.routines))

    def test_04_get_routine_by_id_found(self):
        routine = self.service.get_routine_by_id("rtn-bcs-mega-001")
        self.assertIsNotNone(routine)
        self.assertTrue(routine.is_mega_model_test)
        self.assertEqual(routine.duration_minutes, 120)
        self.assertEqual(routine.total_questions, 200)

    def test_05_get_routine_by_id_not_found(self):
        routine = self.service.get_routine_by_id("non-existent-routine-xyz")
        self.assertIsNone(routine)

    def test_06_simulate_negative_marking_top_percentile(self):
        # 100 questions: 85 correct, 10 wrong (-2.50), 5 unanswered -> net 82.5 (>=80% top 1%)
        req = NegativeMarkSimulationRequest(
            total_questions=100,
            correct_answers=85,
            wrong_answers=10,
            unanswered=5,
            negative_factor=0.25,
            mark_per_question=1.0,
        )
        res = self.service.simulate_negative_marking(req)
        self.assertTrue(res.success)
        self.assertEqual(res.gross_score, 85.0)
        self.assertEqual(res.penalty_deducted, 2.50)
        self.assertEqual(res.net_score, 82.5)
        self.assertGreaterEqual(res.estimated_percentile, 98.0)
        self.assertIn("মেধাতালিকা টপ ১%", res.merit_bracket)

    def test_07_simulate_negative_marking_penalty_and_weakness_flags(self):
        # 100 questions: 40 correct, 50 wrong (-12.50), 10 unanswered -> net 27.5
        req = NegativeMarkSimulationRequest(
            total_questions=100,
            correct_answers=40,
            wrong_answers=50,
            unanswered=10,
            negative_factor=0.25,
            mark_per_question=1.0,
        )
        res = self.service.simulate_negative_marking(req)
        self.assertEqual(res.penalty_deducted, 12.50)
        self.assertLess(res.estimated_percentile, 70.0)
        # Check weakness flags triggered for wrong answers and heavy penalty
        flags_text = " ".join(res.weakness_flags)
        self.assertIn("উচ্চ ভুল উত্তরের হার", flags_text)
        self.assertIn("অতিরিক্ত পেনাল্টি", flags_text)

    def test_08_negative_marking_sum_validation(self):
        # Sum does not match total questions -> must raise ValueError
        with self.assertRaises(ValueError):
            NegativeMarkSimulationRequest(
                total_questions=100,
                correct_answers=60,
                wrong_answers=20,
                unanswered=10, # 60+20+10 = 90 != 100
                negative_factor=0.25,
            )

    def test_09_subscribe_to_routine(self):
        req = RoutineSubscribeRequest(
            routine_id="rtn-bcs-001",
            channels=["IN_APP", "PUSH"],
        )
        res = self.service.subscribe_to_routine("usr-student-42", req)
        self.assertTrue(res.success)
        self.assertTrue(res.subscription_id.startswith("sub-"))
        self.assertIn("সফলভাবে সক্রিয় হয়েছে", res.message)

    def test_10_router_endpoint_dispatch(self):
        # Direct router invocation with preview active override
        list_res = list_exam_routines(exam_type=None, track_category=None, day_number=None, x_feature_override="preview_active")
        self.assertTrue(list_res.success)

        detail_res = get_exam_routine_detail("rtn-bcs-002", x_feature_override="preview_active")
        self.assertEqual(detail_res.routine_code, "BCS-200-DAY-002")

        sub_res = subscribe_to_routine_alerts(
            payload=RoutineSubscribeRequest(routine_id="rtn-bcs-002"),
            authorization="Bearer test_token_xyz",
            x_feature_override="preview_active",
        )
        self.assertTrue(sub_res.success)

    def test_11_migration_017_syntax_and_security(self):
        migration_path = os.path.join(
            os.path.dirname(__file__), "..", "migrations", "017_exam_routine_and_model_test_rls.sql"
        )
        self.assertTrue(os.path.exists(migration_path))
        with open(migration_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Security & Architectural invariants
        self.assertIn("ENABLE ROW LEVEL SECURITY", content)
        self.assertIn("FORCE ROW LEVEL SECURITY", content)
        self.assertIn("ROLLBACK INSTRUCTIONS", content)
        self.assertIn("DROP TABLE IF EXISTS public.exam_routines CASCADE;", content)
        self.assertIn("DROP TABLE IF EXISTS public.routine_subscriptions CASCADE;", content)

        # Zero-Emoji verification
        for char in content:
            self.assertLess(ord(char), 0x1F600, f"Emoji character detected in migration: {char}")

    def test_12_feature_gate_enforcement(self):
        # When flag is OFF and no override, endpoints must raise 403 Forbidden
        original_flag = getattr(settings, "FEATURE_EXAM_ROUTINE", False)
        try:
            settings.FEATURE_EXAM_ROUTINE = False

            with self.assertRaises(HTTPException) as ctx:
                list_exam_routines(exam_type=None, track_category=None, day_number=None)
            self.assertEqual(ctx.exception.status_code, status.HTTP_403_FORBIDDEN)

            with self.assertRaises(HTTPException) as ctx2:
                get_exam_routine_detail("rtn-bcs-001")
            self.assertEqual(ctx2.exception.status_code, status.HTTP_403_FORBIDDEN)

            # Admin authorization bypasses gate
            admin_sub = subscribe_to_routine_alerts(
                payload=RoutineSubscribeRequest(routine_id="rtn-bcs-001"),
                authorization="Bearer admin_super_token",
            )
            self.assertTrue(admin_sub.success)

            # When flag is ON, public access is permitted
            settings.FEATURE_EXAM_ROUTINE = True
            open_res = list_exam_routines(exam_type=None, track_category=None, day_number=None)
            self.assertTrue(open_res.success)
        finally:
            settings.FEATURE_EXAM_ROUTINE = original_flag

    def test_13_input_validation_boundary_conditions(self):
        # Negative correct / wrong / unanswered answers must be rejected
        with self.assertRaises(ValueError):
            NegativeMarkSimulationRequest(
                total_questions=100,
                correct_answers=-10,
                wrong_answers=110,
                unanswered=0,
            )

        with self.assertRaises(ValueError):
            NegativeMarkSimulationRequest(
                total_questions=100,
                correct_answers=80,
                wrong_answers=-5,
                unanswered=25,
            )

        # Negative factor or non-positive mark must be rejected
        with self.assertRaises(ValueError):
            NegativeMarkSimulationRequest(
                total_questions=100,
                correct_answers=70,
                wrong_answers=20,
                unanswered=10,
                negative_factor=-0.25,
            )

        with self.assertRaises(ValueError):
            NegativeMarkSimulationRequest(
                total_questions=100,
                correct_answers=70,
                wrong_answers=20,
                unanswered=10,
                mark_per_question=0.0,
            )

        # Subscription validation
        with self.assertRaises(ValueError):
            RoutineSubscribeRequest(routine_id="")

        with self.assertRaises(ValueError):
            RoutineSubscribeRequest(routine_id="x" * 105)

        # Valid subscription channel filtering
        req = RoutineSubscribeRequest(routine_id="rtn-001", channels=["push", "INVALID_CHANNEL", "sms"])
        self.assertEqual(req.channels, ["PUSH", "SMS"])


if __name__ == "__main__":
    unittest.main()
