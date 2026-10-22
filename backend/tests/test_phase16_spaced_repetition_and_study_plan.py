"""
================================================================================
MODULE: Automated Test Suite (স্বয়ংক্রিয় ভেরিফিকেশন ও টেস্ট ইঞ্জিন)
TOPIC: Phase 16 Spaced Repetition (SuperMemo SM-2) & Adaptive Study Plans
FILE: backend/tests/test_phase16_spaced_repetition_and_study_plan.py
PURPOSE: Comprehensive unit, scientific algorithm, and API integration tests
         validating SuperMemo SM-2 memory retention math, timezone resilience,
         weakness-targeted 7-day adaptive roadmaps, and daily milestone tracking.
AUDIENCE: QA Engineers, Cognitive Learning Scientists, CI/CD Pipeline.
STANDARDS: SuperMemo SM-2 Standard, Zone of Proximal Development, 100% Pass Rate.
================================================================================
"""

import unittest
from datetime import datetime, timedelta, timezone

from backend.app.services.spaced_repetition_service import spaced_repetition_service
from backend.app.services.study_plan_service import study_plan_service
from backend.app.api.v1.router import (
    generate_student_study_plan,
    get_student_study_plan,
    complete_study_milestone,
    record_spaced_review,
    get_due_spaced_reviews,
    get_spaced_retention_stats,
)
from backend.app.schemas.spaced_repetition_schema import (
    SpacedReviewRecordRequest,
    StudyPlanGenerateRequest,
    MilestoneCompleteRequest,
)


class TestPhase16SpacedRepetitionAndStudyPlan(unittest.TestCase):
    """Test suite covering Phase 16 Spaced Repetition and Adaptive Study Plans."""

    def setUp(self) -> None:
        """Reset service singletons before each test run for absolute isolation."""
        spaced_repetition_service.reset_for_testing()
        study_plan_service.reset_for_testing()

    def test_sm2_algorithm_progression_and_quality(self) -> None:
        """Verifies SuperMemo SM-2 interval calculations under various recall quality scores."""
        # 1. First review with perfect recall (q = 5)
        reps, interval, ef = spaced_repetition_service.calculate_sm2_interval(
            quality_score=5,
            repetitions=0,
            previous_interval_days=0,
            previous_ease_factor=2.5,
        )
        self.assertEqual(reps, 1)
        self.assertEqual(interval, 1)
        self.assertEqual(ef, 2.6)  # 2.5 + (0.1 - 0) = 2.6

        # 2. Second consecutive review with good recall (q = 4)
        reps, interval, ef = spaced_repetition_service.calculate_sm2_interval(
            quality_score=4,
            repetitions=1,
            previous_interval_days=interval,
            previous_ease_factor=ef,
        )
        self.assertEqual(reps, 2)
        self.assertEqual(interval, 6)
        self.assertAlmostEqual(ef, 2.6, places=1)

        # 3. Third review with q = 5
        reps, interval, ef = spaced_repetition_service.calculate_sm2_interval(
            quality_score=5,
            repetitions=2,
            previous_interval_days=6,
            previous_ease_factor=ef,
        )
        self.assertEqual(reps, 3)
        self.assertGreaterEqual(interval, 15)  # 6 * ~2.65 ~ 16

        # 4. Failure test (q = 1: incorrect answer resets repetition to 0 and interval to 1)
        reps, interval, ef = spaced_repetition_service.calculate_sm2_interval(
            quality_score=1,
            repetitions=reps,
            previous_interval_days=interval,
            previous_ease_factor=ef,
        )
        self.assertEqual(reps, 0)
        self.assertEqual(interval, 1)
        self.assertGreaterEqual(ef, spaced_repetition_service.MINIMUM_EASE_FACTOR)

    def test_timezone_naive_and_aware_due_comparisons(self) -> None:
        """Pins down regression fix: calling get_due_reviews with naive datetime raises no TypeError."""
        base_time = datetime.now(timezone.utc) - timedelta(days=2)

        # Record a question reviewed 2 days ago
        spaced_repetition_service.record_review(
            student_id="std_tz_test",
            question_id="q_math_55",
            topic="ত্রিকোণমিতি",
            quality_score=3,
            review_timestamp=base_time,
        )

        # 1. Query with timezone-aware datetime
        due_aware = spaced_repetition_service.get_due_reviews(
            student_id="std_tz_test",
            as_of_time=datetime.now(timezone.utc),
        )
        self.assertEqual(len(due_aware), 1)

        # 2. Query with offset-naive datetime (simulates unadorned datetime objects)
        naive_future_time = datetime.now() + timedelta(days=1)
        due_naive = spaced_repetition_service.get_due_reviews(
            student_id="std_tz_test",
            as_of_time=naive_future_time,
        )
        self.assertEqual(len(due_naive), 1)

    def test_student_mastery_stats_aggregation(self) -> None:
        """Verifies calculation of mastery and memory retention statistics."""
        # Fresh student with no items
        empty_stats = spaced_repetition_service.get_student_mastery_stats("std_fresh")
        self.assertEqual(empty_stats["total_tracked_questions"], 0)
        self.assertEqual(empty_stats["retention_rate_pct"], 100.0)

        # Record 4 successful reviews on q1 (reps >= 4 -> MASTERED)
        now = datetime.now(timezone.utc)
        for i in range(4):
            spaced_repetition_service.record_review(
                student_id="std_mastery",
                question_id="q_phy_01",
                topic="গতিবিদ্যা",
                quality_score=5,
                review_timestamp=now + timedelta(days=i * 2),
            )

        # Record 1 unsuccessful review on q2 (LEARNING)
        spaced_repetition_service.record_review(
            student_id="std_mastery",
            question_id="q_chem_02",
            topic="জৈব যৌগ",
            quality_score=2,
            review_timestamp=now,
        )

        stats = spaced_repetition_service.get_student_mastery_stats("std_mastery")
        self.assertEqual(stats["total_tracked_questions"], 2)
        self.assertEqual(stats["mastered_questions"], 1)
        self.assertEqual(stats["learning_questions"], 1)
        self.assertEqual(stats["retention_rate_pct"], 50.0)

    def test_study_plan_generation_and_milestones(self) -> None:
        """Verifies generating an adaptive 7-day study roadmap and completing daily milestones."""
        plan = study_plan_service.generate_study_plan(
            student_id="std_plan_01",
            class_grade=9,
            target_subject="পদার্থবিজ্ঞান",
            weak_topics=["আলোর প্রতিফলন", "কাজ ও শক্তি"],
            daily_available_minutes=45,
        )

        self.assertTrue(plan["plan_id"].startswith("plan_"))
        self.assertEqual(plan["total_milestones"], 7)
        self.assertEqual(plan["completed_milestones"], 0)
        self.assertEqual(plan["progress_pct"], 0.0)
        self.assertEqual(plan["status"], "ACTIVE")
        self.assertEqual(len(plan["schedule"]), 7)

        # Complete Day 1 milestone
        m1_id = plan["schedule"][0]["milestone_id"]
        res1 = study_plan_service.complete_milestone("std_plan_01", m1_id)
        self.assertTrue(res1["success"])
        self.assertEqual(res1["completed_milestones"], 1)
        self.assertAlmostEqual(res1["progress_pct"], 14.3, places=1)

        # Complete remaining 6 milestones to reach 100% completion
        for day in plan["schedule"][1:]:
            res = study_plan_service.complete_milestone("std_plan_01", day["milestone_id"])
            self.assertTrue(res["success"])

        active_plan = study_plan_service.get_active_study_plan("std_plan_01")
        self.assertEqual(active_plan["status"], "COMPLETED")
        self.assertEqual(active_plan["progress_pct"], 100.0)

    async def _async_test_api_endpoints(self) -> None:
        """Asynchronous helper testing Phase 16 REST endpoints."""
        # 1. Spaced review endpoint
        rev_req = SpacedReviewRecordRequest(
            student_id="usr_api_std_99",
            question_id="q_bio_12",
            topic="কোষ ও টিস্যু",
            quality_score=4,
        )
        rev_res = await record_spaced_review(rev_req)
        self.assertEqual(rev_res["status"], "SUCCESS")

        # 2. Spaced due & stats endpoints
        due_res = await get_due_spaced_reviews("usr_api_std_99")
        self.assertIn("due_questions", due_res)

        stats_res = await get_spaced_retention_stats("usr_api_std_99")
        self.assertEqual(stats_res["total_tracked_questions"], 1)

        # 3. Generate study plan endpoint
        plan_req = StudyPlanGenerateRequest(
            student_id="usr_api_std_99",
            class_grade=8,
            target_subject="গণিত",
            weak_topics=["উৎপাদকে বিশ্লেষণ"],
            daily_available_minutes=35,
        )
        plan_res = await generate_student_study_plan(plan_req)
        self.assertEqual(plan_res["status"], "SUCCESS")

        # 4. Get active plan
        plan_data = await get_student_study_plan("usr_api_std_99")
        self.assertEqual(plan_data["student_id"], "usr_api_std_99")

        # 5. Complete milestone endpoint
        m_req = MilestoneCompleteRequest(
            student_id="usr_api_std_99",
            milestone_id=plan_data["schedule"][0]["milestone_id"],
        )
        m_res = await complete_study_milestone(m_req)
        self.assertTrue(m_res["success"])
        self.assertEqual(m_res["completed_milestones"], 1)

    def test_api_endpoints_phase16(self) -> None:
        """Executes the async REST endpoints in standard test runner."""
        import asyncio
        asyncio.run(self._async_test_api_endpoints())


if __name__ == "__main__":
    unittest.main()
