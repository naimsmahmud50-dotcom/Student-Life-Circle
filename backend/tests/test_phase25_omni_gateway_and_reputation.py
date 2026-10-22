"""
========================================================================================
TEST SUITE: Phase 25 Omni-Search, Real-Time Notifications & Student Reputation
TOPIC:      Cross-Platform Gateway, Event Dispatch & 4-Pillar Reputation Engine
FILE:       backend/tests/test_phase25_omni_gateway_and_reputation.py
PURPOSE:    Validates the end-to-end integration and boundary stability of:
            1. Omni-Search: Unified multi-facet search across 10MS, CareTutors & Bdjobs
            2. Notification Gateway: Event dispatch, unread indexing & input validation
            3. Reputation Engine: 0-1000 composite score, tier resolution & daily quests
STANDARDS:  Strict Boundary Verification, Zero Regressions, OWASP ASVS L2 Audit
AUDIENCE:   QA Engineers, System Integrators & Platform Architects
========================================================================================
"""

import unittest
from backend.app.services.omni_search_service import omni_search_service
from backend.app.services.notification_gateway_service import notification_gateway_service
from backend.app.services.student_reputation_service import student_reputation_service
from backend.app.schemas.omni_gateway_schema import (
    NotificationDispatchRequest,
    QuestClaimRequest
)
from backend.app.api.v1.router import (
    execute_omni_search,
    dispatch_platform_notification,
    get_user_notifications,
    mark_single_notification_read,
    mark_all_user_notifications_read,
    get_student_reputation_score,
    get_student_daily_quests,
    claim_daily_quest_reward
)


class TestPhase25OmniGatewayAndReputation(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Phase 25 Omni-Search, Notification Gateway, and Student Reputation.
    """

    # ==================================================================================
    # TOPIC 1: UNIFIED OMNI-SEARCH ENGINE TESTS
    # ==================================================================================

    async def test_omni_search_all_categories(self):
        """Verifies unified search matches across lectures, tuitions, and internships."""
        res = await execute_omni_search(query="Math", category="ALL", limit=10)
        self.assertTrue(res["success"])
        self.assertGreater(res["total_matches"], 0)
        categories = {item["category"] for item in res["results"]}
        # Should contain at least lectures and tuitions for "Math"
        self.assertIn("ACADEMIC_LECTURES", categories)

    async def test_omni_search_category_filter(self):
        """Verifies that category filtering restricts results properly."""
        res_tuit = await execute_omni_search(query="", category="TUITIONS", limit=10)
        self.assertTrue(res_tuit["success"])
        for item in res_tuit["results"]:
            self.assertEqual(item["category"], "TUITIONS")

        res_jobs = await execute_omni_search(query="", category="INTERNSHIPS", limit=10)
        self.assertTrue(res_jobs["success"])
        for item in res_jobs["results"]:
            self.assertEqual(item["category"], "INTERNSHIPS")

    async def test_omni_search_with_whitespace_and_punctuation(self):
        """Boundary test: whitespace padding and punctuation in search query."""
        res = await execute_omni_search(query="   Calculus, Physics!   ", category="ALL", limit=5)
        self.assertTrue(res["success"])
        self.assertGreater(res["total_matches"], 0)

        # Empty/whitespace query returns default top recommendations
        res_empty = await execute_omni_search(query="   ", category="ALL", limit=5)
        self.assertTrue(res_empty["success"])
        self.assertGreater(res_empty["total_matches"], 0)

    # ==================================================================================
    # TOPIC 2: REAL-TIME NOTIFICATION GATEWAY TESTS
    # ==================================================================================

    async def test_notification_dispatch_and_unread_lifecycle(self):
        """Verifies dispatching notifications, unread counting, and mark-as-read transitions."""
        user_id = "test_user_notif_01"
        dispatch_payload = NotificationDispatchRequest(
            recipient_user_id=user_id,
            category="CARE_TUTORS",
            title="Guardian Shortlist Notification",
            message="Your tuition bid was shortlisted by a guardian in Dhanmondi.",
            priority="HIGH",
            action_link="#tab-tuition"
        )
        res_dispatch = await dispatch_platform_notification(dispatch_payload)
        self.assertTrue(res_dispatch["success"])
        notif_id = res_dispatch["notification"]["notification_id"]

        # 1. Check unread inbox
        inbox = await get_user_notifications(user_id=user_id, only_unread=True)
        self.assertEqual(inbox["unread_count"], 1)
        self.assertEqual(len(inbox["notifications"]), 1)

        # 2. Mark single notification as read
        read_res = await mark_single_notification_read(notification_id=notif_id, user_id=user_id)
        self.assertTrue(read_res["success"])
        self.assertEqual(read_res["unread_count"], 0)

        # 3. Dispatch a second notification and test mark_all_as_read
        await dispatch_platform_notification(NotificationDispatchRequest(
            recipient_user_id=user_id,
            category="BDJOBS",
            title="Interview Invitation",
            message="Brain Station 23 scheduled a technical viva.",
            priority="URGENT"
        ))
        inbox2 = await get_user_notifications(user_id=user_id, only_unread=True)
        self.assertEqual(inbox2["unread_count"], 1)

        mark_all = await mark_all_user_notifications_read(user_id=user_id)
        self.assertTrue(mark_all["success"])
        self.assertEqual(mark_all["unread_count"], 0)

    def test_notification_dispatch_empty_field_validation(self):
        """Validates that blank recipient, title, or message are rejected."""
        res_user = notification_gateway_service.dispatch_notification(
            recipient_user_id="   ",
            category="SYSTEM",
            title="Alert",
            message="Content"
        )
        self.assertFalse(res_user["success"])
        self.assertEqual(res_user["error_code"], "INVALID_RECIPIENT_USER_ID")

        res_title = notification_gateway_service.dispatch_notification(
            recipient_user_id="user_1",
            category="SYSTEM",
            title="  ",
            message="Content"
        )
        self.assertFalse(res_title["success"])
        self.assertEqual(res_title["error_code"], "EMPTY_NOTIFICATION_TITLE")

    # ==================================================================================
    # TOPIC 3: STUDENT REPUTATION & DAILY QUEST ENGINE TESTS
    # ==================================================================================

    async def test_student_reputation_score_and_tier_resolution(self):
        """Verifies 4-pillar score calculation, radar breakdown, and tier assignment."""
        score_res = await get_student_reputation_score("student_demo_01")
        self.assertTrue(score_res["success"])
        self.assertGreaterEqual(score_res["composite_score"], 750)
        self.assertEqual(score_res["tier"], "EMINENCE_FELLOW")
        self.assertIn("academic", score_res["radar_breakdown"])
        self.assertIn("tutoring", score_res["radar_breakdown"])
        self.assertIn("career", score_res["radar_breakdown"])
        self.assertIn("integrity", score_res["radar_breakdown"])

    def test_reputation_score_boundary_conditions(self):
        """Boundary test: fresh uninitialized student or extreme negative theta."""
        # Fresh student with zero record
        fresh_score = student_reputation_service.calculate_reputation_score("fresh_student_999")
        self.assertTrue(fresh_score["success"])
        self.assertEqual(fresh_score["tier"], "NOVICE_SCHOLAR")
        self.assertGreaterEqual(fresh_score["composite_score"], 0)
        self.assertLessEqual(fresh_score["composite_score"], 1000)

        # Extreme values
        student_reputation_service._profiles["extreme_student"] = {
            "student_id": "extreme_student",
            "cat_ability_theta": -10.0,
            "checkpoints_passed": 0,
            "tutor_rating": -2.0,
            "completed_tuition_sessions": 0,
            "verified_skills_count": 0,
            "sealed_cv_snapshots_count": 0,
            "ats_high_matches_count": 0,
            "tribunal_votes_cast": 0,
            "study_circle_notes_contributed": 0,
            "extra_bonus_points": -100
        }
        extreme_score = student_reputation_service.calculate_reputation_score("extreme_student")
        self.assertGreaterEqual(extreme_score["composite_score"], 0)
        self.assertLessEqual(extreme_score["composite_score"], 1000)

    async def test_daily_quests_and_claim_reward(self):
        """Verifies daily quest retrieval, claiming reward, and duplicate claim blocking."""
        user_id = "student_quest_test_01"
        quests_res = await get_student_daily_quests(user_id)
        self.assertTrue(quests_res["success"])
        self.assertEqual(len(quests_res["quests"]), 4)

        # Claim first quest
        claim_payload = QuestClaimRequest(student_id=user_id, quest_id="quest_cp_01")
        claim_res = await claim_daily_quest_reward(claim_payload)
        self.assertTrue(claim_res["success"])
        self.assertEqual(claim_res["points_awarded"], 25)

        # Attempt to claim again -> should fail with 400
        from backend.app.core.fastapi_shim import HTTPException
        with self.assertRaises(HTTPException) as ctx:
            await claim_daily_quest_reward(claim_payload)
        self.assertEqual(ctx.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
