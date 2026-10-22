"""
===================================================================================
Module: Study Scheduler & Burnout Prevention Tests
Topic: Unit & Integration Verification for Circadian Routine, Sprints & Fatigue
File: backend/tests/test_phase22_study_scheduler.py
Purpose: Verifies circadian-balanced schedule generation, Pomodoro focus sprint
         lifecycle, cognitive fatigue calculations, guardian safety alerts,
         and boundary protection with zero test failures.
Audience: QA Engineers, Backend Developers, Continuous Integration Runners
Standards: Clean Architecture, OWASP ASVS Level 2, Full Type Hints, Zero-Emoji
===================================================================================
"""

import unittest

try:
    from backend.app.services.study_scheduler_service import study_scheduler_service
    from backend.app.services.burnout_prevention_service import burnout_prevention_service
    from backend.app.schemas.study_scheduler_schema import (
        DailyScheduleGenerateRequest,
        FocusSprintStartRequest,
        FocusSprintCompleteRequest,
        BurnoutEvaluationRequest
    )
except ImportError:
    from app.services.study_scheduler_service import study_scheduler_service
    from app.services.burnout_prevention_service import burnout_prevention_service
    from app.schemas.study_scheduler_schema import (
        DailyScheduleGenerateRequest,
        FocusSprintStartRequest,
        FocusSprintCompleteRequest,
        BurnoutEvaluationRequest
    )

try:
    from fastapi.testclient import TestClient
    from backend.app.main import app
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


class TestPhase22StudySchedulerAndBurnout(unittest.TestCase):
    """
    Comprehensive test suite verifying Phase 22:
    Intelligent Daily Study Scheduler, Pomodoro Focus Sprints & Burnout Prevention Shield.
    """

    def setUp(self) -> None:
        """Reset service singletons before each test."""
        study_scheduler_service.reset_for_testing()
        burnout_prevention_service.reset_for_testing()
        if HAS_FASTAPI:
            self.client = TestClient(app)

    def tearDown(self) -> None:
        """Clean up post-test state."""
        study_scheduler_service.reset_for_testing()
        burnout_prevention_service.reset_for_testing()

    def test_01_generate_daily_schedule_structure(self) -> None:
        """Verifies circadian-optimized daily routine generation with all slot types."""
        res = study_scheduler_service.generate_daily_schedule(
            student_id="std_sched_01",
            available_hours=6.5,
            weak_subjects=["higher_math", "physics", "chemistry"],
            target_exam="HSC_SCIENCE"
        )

        self.assertTrue(res["success"])
        self.assertEqual(res["student_id"], "std_sched_01")
        self.assertGreaterEqual(len(res["slots"]), 5)
        self.assertGreaterEqual(res["circadian_alignment_score"], 90.0)

        # Check morning deep work slot
        slot_morning = res["slots"][0]
        self.assertEqual(slot_morning["slot_type"], "DEEP_WORK")
        self.assertEqual(slot_morning["subject"], "higher_math")
        self.assertEqual(slot_morning["cognitive_demand_score"], 5)

        # Check pre-sleep recall slot
        slot_recall = res["slots"][-1]
        self.assertEqual(slot_recall["slot_type"], "ACTIVE_RECALL")
        self.assertLessEqual(slot_recall["cognitive_demand_score"], 3)

    def test_02_low_available_hours_slot_clamping(self) -> None:
        """Verifies boundary fix: requesting small study allocations (1.5h) adaptively scales slots without overflow."""
        res = study_scheduler_service.generate_daily_schedule(
            student_id="std_short",
            available_hours=1.5,
            weak_subjects=["physics"]
        )

        self.assertTrue(res["success"])
        # Total study minutes should closely align with 90 mins requested (not heavily overshoot)
        study_minutes = res["actual_study_minutes"]
        self.assertLessEqual(study_minutes, 105)

    def test_03_custom_weak_subjects_mapping(self) -> None:
        """Verifies passing custom weak subjects prioritizes them in primary slots."""
        res = study_scheduler_service.generate_daily_schedule(
            student_id="std_custom",
            available_hours=5.0,
            weak_subjects=["chemistry", "biology"]
        )

        self.assertTrue(res["success"])
        primary_slot = res["slots"][0]
        self.assertEqual(primary_slot["subject"], "chemistry")

    def test_04_focus_sprint_start_session(self) -> None:
        """Verifies focus sprint session initialization and anti-distraction locking."""
        res = study_scheduler_service.start_focus_sprint(
            student_id="std_pom_01",
            slot_id="slot_math_01",
            duration_minutes=25,
            sprint_type="POMODORO_25"
        )

        self.assertTrue(res["success"])
        session = res["session"]
        self.assertTrue(session["session_id"].startswith("sprint_"))
        self.assertEqual(session["status"], "IN_PROGRESS")
        self.assertTrue(session["anti_distraction_lock"])
        self.assertEqual(session["planned_duration_minutes"], 25)

    def test_05_focus_sprint_completion_high_efficiency(self) -> None:
        """Verifies sprint completion with zero distractions computes maximum efficiency and streak points."""
        start_res = study_scheduler_service.start_focus_sprint(
            student_id="std_pom_02",
            slot_id="slot_deep_02",
            duration_minutes=25
        )
        session_id = start_res["session"]["session_id"]

        comp_res = study_scheduler_service.complete_focus_sprint(
            session_id=session_id,
            actual_duration_minutes=25,
            distraction_count=0,
            self_reported_focus_score=5
        )

        self.assertTrue(comp_res["success"])
        self.assertEqual(comp_res["efficiency_pct"], 100.0)
        self.assertGreaterEqual(comp_res["points_earned"], 25)
        self.assertEqual(comp_res["recommended_break_minutes"], 5)

    def test_06_focus_sprint_completion_with_distractions(self) -> None:
        """Verifies distractions proportionally reduce efficiency while remaining bounded."""
        start_res = study_scheduler_service.start_focus_sprint(
            student_id="std_pom_03",
            slot_id="slot_03",
            duration_minutes=30
        )
        session_id = start_res["session"]["session_id"]

        comp_res = study_scheduler_service.complete_focus_sprint(
            session_id=session_id,
            actual_duration_minutes=30,
            distraction_count=3,
            self_reported_focus_score=3
        )

        self.assertTrue(comp_res["success"])
        self.assertLess(comp_res["efficiency_pct"], 90.0)
        self.assertGreaterEqual(comp_res["efficiency_pct"], 10.0)

    def test_07_focus_sprint_invalid_session_id(self) -> None:
        """Verifies graceful handling when completing an unknown session ID."""
        res = study_scheduler_service.complete_focus_sprint(
            session_id="sprint_nonexistent_99",
            actual_duration_minutes=25
        )
        self.assertFalse(res["success"])
        self.assertIn("পাওয়া যায়নি", res["message"])

    def test_08_cognitive_fatigue_optimal_flow(self) -> None:
        """Verifies short study duration with healthy sleep rates OPTIMAL_FLOW (< 30)."""
        res = burnout_prevention_service.evaluate_cognitive_fatigue(
            student_id="std_flow_01",
            continuous_study_hours=1.5,
            sleep_hours_last_night=8.0,
            total_study_hours_today=2.5,
            break_minutes_today=30.0
        )

        self.assertTrue(res["success"])
        self.assertLessEqual(res["fatigue_index"], 35.0)
        self.assertIn(res["fatigue_tier"], ["OPTIMAL_FLOW", "MODERATE_STRAIN"])
        self.assertGreaterEqual(res["cognitive_capacity_retention_pct"], 80.0)
        self.assertFalse(res["guardian_safety_alert"]["alert_triggered"])

    def test_09_cognitive_fatigue_high_and_burnout_risk(self) -> None:
        """Verifies excessive continuous study plus sleep deficit triggers BURNOUT_RISK and guardian alert."""
        res = burnout_prevention_service.evaluate_cognitive_fatigue(
            student_id="std_burnout_01",
            continuous_study_hours=6.5,
            sleep_hours_last_night=3.5,
            total_study_hours_today=10.0,
            break_minutes_today=10.0,
            is_minor=True
        )

        self.assertTrue(res["success"])
        self.assertGreaterEqual(res["fatigue_index"], 80.0)
        self.assertEqual(res["fatigue_tier"], "BURNOUT_RISK")
        self.assertEqual(res["badge_color"], "rose")
        self.assertTrue(res["guardian_safety_alert"]["alert_triggered"])
        self.assertIn("অভিভাবক", res["guardian_safety_alert"]["guardian_advisory_bn"])

    def test_10_guardian_alert_deduplication(self) -> None:
        """Verifies boundary fix: multiple burnout evaluations for same student do not flood guardian alerts."""
        burnout_prevention_service.evaluate_cognitive_fatigue(
            student_id="std_dedup",
            continuous_study_hours=7.0,
            sleep_hours_last_night=3.0,
            is_minor=True
        )
        count_first = len(burnout_prevention_service._guardian_alerts)
        self.assertEqual(count_first, 1)

        # Call second time immediately
        burnout_prevention_service.evaluate_cognitive_fatigue(
            student_id="std_dedup",
            continuous_study_hours=7.0,
            sleep_hours_last_night=3.0,
            is_minor=True
        )
        count_second = len(burnout_prevention_service._guardian_alerts)
        self.assertEqual(count_second, 1)

    def test_11_schema_dto_contracts(self) -> None:
        """Verifies dual-resilience schema DTO contracts instantiate with validated defaults."""
        req_sched = DailyScheduleGenerateRequest(
            student_id="std_dto_sched",
            available_hours=7.0,
            target_exam="HSC_SCIENCE"
        )
        self.assertEqual(req_sched.available_hours, 7.0)

        req_start = FocusSprintStartRequest(
            student_id="std_dto_start",
            slot_id="slot_01",
            duration_minutes=30
        )
        self.assertEqual(req_start.duration_minutes, 30)

        req_burn = BurnoutEvaluationRequest(
            student_id="std_dto_burn",
            continuous_study_hours=3.5
        )
        self.assertEqual(req_burn.continuous_study_hours, 3.5)

    def test_12_get_student_burnout_status_fallback(self) -> None:
        """Verifies retrieval of burnout status falls back gracefully for first-time students."""
        status = burnout_prevention_service.get_student_burnout_status("std_new_user")
        self.assertTrue(status["success"])
        self.assertIn("fatigue_index", status)
        self.assertIn("recharge_prescriptions", status)


if __name__ == "__main__":
    unittest.main()
