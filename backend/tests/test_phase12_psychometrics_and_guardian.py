"""
========================================================================================
MODULE:    Phase 12 Automated Test Suite
TOPIC:     Adaptive Psychometrics, Anti-Toxic Habits, Guardian Safety & Crowdsourced QA
FILE:      backend/tests/test_phase12_psychometrics_and_guardian.py
PURPOSE:   Validates the integrity, mathematical stability, and child safety compliance
           of Phase 12 services:
           1. Psychometric Mastery (Elo ability calibration, ZPD bands, overflow guards).
           2. Anti-Toxic Habit Engine (streak freeze passes, non-punitive comeback boosts).
           3. Guardian Safety Operations (pairing tokens, tuition co-signing, privacy).
           4. In-App Question Dispute & Crowdsourced QA (moderator gates, integrity bounties).
AUDIENCE:  QA Engineers, Safety Compliance Officers & Autonomous Test Runners
STANDARDS: Zero-Emoji Microcopy, ASVS L2 Child Privacy, 100% Deterministic Testing
========================================================================================
"""

import unittest
from datetime import datetime, date, timedelta
from backend.app.services.psychometrics_service import PsychometricsService
from backend.app.services.guardian_service import GuardianService
from backend.app.services.dispute_service import DisputeService
from backend.app.services.quarantine_service import QuarantineService
from backend.app.services.quiz_engine import quiz_engine
from backend.app.api.v1.router import api_router


class TestPhase12PsychometricsAndGuardian(unittest.TestCase):
    """
    Automated test cases for Phase 12 capabilities.
    """

    def setUp(self):
        self.psychometrics = PsychometricsService()
        self.guardian = GuardianService()
        self.quarantine = QuarantineService()
        self.dispute = DisputeService(quarantine_service=self.quarantine)

    # -------------------------------------------------------------------------
    # 1. Psychometrics & ZPD Tests
    # -------------------------------------------------------------------------
    def test_psychometrics_elo_calibration(self):
        student_id = "std_test_adaptive_01"
        initial_rating = self.psychometrics.get_or_create_student_rating(student_id)
        self.assertEqual(initial_rating, 1200.0)

        # Correct response against equal difficulty question
        new_rating, delta = self.psychometrics.update_rating_after_response(
            student_id=student_id,
            question_difficulty=1200.0,
            is_correct=True
        )
        self.assertGreater(new_rating, initial_rating)
        self.assertEqual(delta, 12.0)
        self.assertEqual(new_rating, 1212.0)

        # Incorrect response against same difficulty
        new_rating_2, delta_2 = self.psychometrics.update_rating_after_response(
            student_id=student_id,
            question_difficulty=1212.0,
            is_correct=False
        )
        self.assertLess(new_rating_2, new_rating)

    def test_psychometrics_zpd_recommendation(self):
        student_id = "std_test_zpd_01"
        self.psychometrics._student_ratings[student_id] = 1350.0

        zpd = self.psychometrics.get_recommended_difficulty_band(student_id)
        self.assertEqual(zpd["student_rating"], 1350.0)
        self.assertLess(zpd["min_difficulty"], zpd["target_difficulty"])
        self.assertLess(zpd["target_difficulty"], zpd["max_difficulty"])
        self.assertEqual(zpd["target_probability_band"], "0.60 - 0.75")

    def test_psychometrics_overflow_safety(self):
        """Ensures extreme Elo differentials do not trigger math overflow exceptions."""
        prob_extreme_high = self.psychometrics.calculate_expected_probability(
            student_rating=1200.0,
            question_difficulty=50000.0
        )
        self.assertIsInstance(prob_extreme_high, float)
        self.assertGreaterEqual(prob_extreme_high, 0.0)
        self.assertLessEqual(prob_extreme_high, 1.0)

        prob_extreme_low = self.psychometrics.calculate_expected_probability(
            student_rating=1200.0,
            question_difficulty=-50000.0
        )
        self.assertIsInstance(prob_extreme_low, float)
        self.assertGreaterEqual(prob_extreme_low, 0.0)
        self.assertLessEqual(prob_extreme_low, 1.0)

    # -------------------------------------------------------------------------
    # 2. Anti-Toxic Habit Engine Tests
    # -------------------------------------------------------------------------
    def test_anti_toxic_habits_and_streak_freeze(self):
        student_id = "std_test_habit_01"
        record = self.psychometrics.get_or_create_habit_record(student_id)
        self.assertEqual(record["banked_freeze_passes"], 1)

        # Day 1: Activity
        self.psychometrics.record_daily_study_activity(student_id, activity_date="2026-10-10")
        self.assertEqual(record["current_streak"], 1)

        # Day 2: Consecutive
        self.psychometrics.record_daily_study_activity(student_id, activity_date="2026-10-11")
        self.assertEqual(record["current_streak"], 2)

        # Day 3 was missed! Day 4 activity (days_gap == 2) with banked freeze pass
        self.psychometrics.record_daily_study_activity(student_id, activity_date="2026-10-13")
        self.assertEqual(record["current_streak"], 3)  # Streak preserved
        self.assertEqual(record["banked_freeze_passes"], 0)  # Pass used

        # Multiple days missed (days_gap > 2) with 0 passes left -> Comeback Boost activates
        self.psychometrics.record_daily_study_activity(student_id, activity_date="2026-10-20")
        self.assertEqual(record["current_streak"], 1)
        self.assertTrue(record["comeback_boost_active"])
        self.assertEqual(record["comeback_boost_multiplier"], 1.25)

    def test_explicit_streak_freeze_consumption(self):
        student_id = "std_test_freeze_02"
        record = self.psychometrics.get_or_create_habit_record(student_id)
        self.assertEqual(record["banked_freeze_passes"], 1)

        success, msg = self.psychometrics.consume_streak_freeze_pass(student_id)
        self.assertTrue(success)
        self.assertEqual(msg, "STREAK_FROZEN_FOR_REST_DAY")
        self.assertEqual(record["banked_freeze_passes"], 0)

        # Second attempt with 0 passes fails cleanly
        fail_success, fail_msg = self.psychometrics.consume_streak_freeze_pass(student_id)
        self.assertFalse(fail_success)
        self.assertEqual(fail_msg, "NO_FREEZE_PASSES_AVAILABLE")

    # -------------------------------------------------------------------------
    # 3. Guardian Safety Operations Tests
    # -------------------------------------------------------------------------
    def test_guardian_minor_pairing_lifecycle(self):
        minor_id = "std_minor_001"
        guardian_id = "usr_parent_001"

        # 1. Generate pairing token
        token = self.guardian.generate_minor_pairing_token(minor_id)
        self.assertEqual(len(token), 6)
        self.assertTrue(token.isdigit())

        # 2. Pair guardian with minor using token
        success, msg, link = self.guardian.link_guardian_to_minor(
            guardian_user_id=guardian_id,
            minor_student_id=minor_id,
            pairing_token=token,
            relationship="MOTHER"
        )
        self.assertTrue(success)
        self.assertEqual(msg, "GUARDIAN_LINKED_SUCCESSFULLY")
        self.assertIsNotNone(link)
        self.assertEqual(link["relationship"], "MOTHER")

        # 3. Token is invalidated after use
        fail_success, fail_msg, _ = self.guardian.link_guardian_to_minor(
            guardian_user_id="usr_parent_002",
            minor_student_id=minor_id,
            pairing_token=token
        )
        self.assertFalse(fail_success)
        self.assertEqual(fail_msg, "INVALID_OR_EXPIRED_PAIRING_TOKEN")

    def test_guardian_tuition_co_signing_gate(self):
        minor_id = "std_minor_002"
        guardian_id = "usr_parent_002"
        unlinked_user_id = "usr_stranger_001"
        listing_id = "tuit_listing_089"

        # Establish linkage first
        token = self.guardian.generate_minor_pairing_token(minor_id)
        self.guardian.link_guardian_to_minor(guardian_id, minor_id, token)

        # Unlinked user cannot co-sign
        fail_success, fail_msg, _ = self.guardian.record_tuition_co_signature(
            guardian_user_id=unlinked_user_id,
            tuition_listing_id=listing_id,
            minor_student_id=minor_id
        )
        self.assertFalse(fail_success)
        self.assertEqual(fail_msg, "UNAUTHORIZED_NOT_LINKED_TO_MINOR")

        # Linked guardian co-signs successfully
        success, msg, sig = self.guardian.record_tuition_co_signature(
            guardian_user_id=guardian_id,
            tuition_listing_id=listing_id,
            minor_student_id=minor_id,
            guardian_notes="I approve 3 days a week tuition for my daughter."
        )
        self.assertTrue(success)
        self.assertEqual(msg, "TUITION_CO_SIGNED")
        self.assertEqual(sig["guardian_notes"], "I approve 3 days a week tuition for my daughter.")

    def test_guardian_privacy_overview(self):
        minor_id = "std_minor_003"
        guardian_id = "usr_parent_003"

        token = self.guardian.generate_minor_pairing_token(minor_id)
        self.guardian.link_guardian_to_minor(guardian_id, minor_id, token)

        success, msg, overview = self.guardian.get_minor_guardian_overview(
            guardian_user_id=guardian_id,
            minor_student_id=minor_id
        )
        self.assertTrue(success)
        self.assertEqual(overview["minor_privacy_mode"], "ACTIVE")
        self.assertIn("study_consistency_streak", overview)
        self.assertIn("strongest_subject", overview)

    # -------------------------------------------------------------------------
    # 4. In-App Question Dispute & Crowdsourced QA Tests
    # -------------------------------------------------------------------------
    def test_in_app_dispute_reporting_and_resolution(self):
        student_id = "std_vigilant_001"
        question_id = "q_hsc_physics_042"

        # 1. File valid dispute
        success, msg, record = self.dispute.file_dispute(
            student_id=student_id,
            question_id=question_id,
            reason="WRONG_KEY",
            explanation="The answer key designates option A, but calculation gives 9.8 m/s^2 which is option C.",
            suggested_correct_option="C"
        )
        self.assertTrue(success)
        self.assertEqual(record["status"], "PENDING")

        # 2. Duplicate pending dispute by same student is rejected
        dup_success, dup_msg, _ = self.dispute.file_dispute(
            student_id=student_id,
            question_id=question_id,
            reason="WRONG_KEY",
            explanation="Submitting again to be sure."
        )
        self.assertFalse(dup_success)

        # 3. Moderator resolves dispute
        disp_id = record["dispute_id"]
        res_success, res_msg, resolved_record = self.dispute.resolve_dispute(
            dispute_id=disp_id,
            moderator_id="usr_mod_sme_01",
            action="ACCEPT_KEY_CORRECTION",
            resolution_notes="Verified calculation. Key corrected from A to C.",
            bounty_points=20
        )
        self.assertTrue(res_success)
        self.assertEqual(resolved_record["status"], "RESOLVED")
        self.assertEqual(resolved_record["bounty_awarded"], 20)

        # 4. Check student integrity profile
        profile = self.dispute.get_student_integrity_profile(student_id)
        self.assertEqual(profile["accepted_count"], 1)
        self.assertEqual(profile["total_bounty_points"], 20)
        self.assertEqual(len(profile["integrity_badges"]), 1)
        self.assertEqual(profile["integrity_badges"][0]["badge_id"], "VIGILANT_EYE")

    def test_dispute_quarantine_trigger(self):
        student_id = "std_vigilant_002"
        question_id = "q_compromised_item_99"

        # File critical defect dispute
        success, _, record = self.dispute.file_dispute(
            student_id=student_id,
            question_id=question_id,
            reason="AMBIGUOUS",
            explanation="Both option B and D are identical due to a copy-paste error."
        )
        self.assertTrue(success)

        # Moderator accepts and triggers quarantine
        disp_id = record["dispute_id"]
        res_success, _, resolved = self.dispute.resolve_dispute(
            dispute_id=disp_id,
            moderator_id="usr_mod_sme_02",
            action="ACCEPT_AND_QUARANTINE",
            resolution_notes="Question wording is fundamentally flawed. Quarantined.",
            trigger_quarantine=True
        )
        self.assertTrue(res_success)
        self.assertTrue(resolved["quarantined"])
        self.assertIn(question_id, quiz_engine._quarantined_questions)

        # Verify SENTINEL_OF_TRUTH badge awarded
        profile = self.dispute.get_student_integrity_profile(student_id)
        badge_ids = [b["badge_id"] for b in profile["integrity_badges"]]
        self.assertIn("SENTINEL_OF_TRUTH", badge_ids)

    def test_router_endpoints_integration(self):
        """Validates all Phase 12 endpoints exposed through API router."""
        import asyncio
        from backend.app.api.v1.router import (
            get_student_psychometrics,
            calibrate_student_rating,
            get_question_recommendation,
            activate_streak_freeze,
            generate_guardian_pairing_token,
            link_guardian_account,
            co_sign_minor_tuition,
            get_guardian_minor_overview,
            file_question_dispute,
            list_question_disputes,
            get_dispute_by_id,
            resolve_question_dispute,
            get_student_integrity_profile
        )
        from backend.app.schemas.psychometrics_and_guardian_schema import (
            PsychometricCalibrateRequest,
            StreakFreezeUseRequest,
            GuardianLinkRequest,
            TuitionCoSignRequest,
            DisputeFileRequest,
            DisputeResolveRequest
        )

        async def run_async_tests():
            # 1. Psychometrics
            psy_resp = await get_student_psychometrics("std_router_test_01")
            self.assertEqual(psy_resp["student_id"], "std_router_test_01")
            self.assertEqual(psy_resp["elo_rating"], 1200.0)

            cal_payload = PsychometricCalibrateRequest(
                student_id="std_router_test_01",
                question_difficulty=1200.0,
                is_correct=True
            )
            cal_resp = await calibrate_student_rating(cal_payload)
            self.assertEqual(cal_resp["new_rating"], 1212.0)

            rec_resp = await get_question_recommendation("std_router_test_01")
            self.assertIn("difficulty_band", rec_resp)

            freeze_payload = StreakFreezeUseRequest(student_id="std_router_test_01")
            freeze_resp = await activate_streak_freeze(freeze_payload)
            self.assertEqual(freeze_resp["status"], "SUCCESS")

            # 2. Guardian Safety
            token_resp = await generate_guardian_pairing_token("std_minor_router_01")
            self.assertEqual(len(token_resp["pairing_token"]), 6)

            link_payload = GuardianLinkRequest(
                guardian_user_id="usr_guardian_router_01",
                minor_student_id="std_minor_router_01",
                pairing_token=token_resp["pairing_token"],
                relationship="PARENT"
            )
            link_resp = await link_guardian_account(link_payload)
            self.assertEqual(link_resp["status"], "SUCCESS")

            cosign_payload = TuitionCoSignRequest(
                guardian_user_id="usr_guardian_router_01",
                tuition_listing_id="tuit_router_101",
                minor_student_id="std_minor_router_01",
                guardian_notes="Confirmed arrangement."
            )
            cosign_resp = await co_sign_minor_tuition(cosign_payload)
            self.assertEqual(cosign_resp["status"], "SUCCESS")

            overview_resp = await get_guardian_minor_overview(
                minor_student_id="std_minor_router_01",
                guardian_user_id="usr_guardian_router_01"
            )
            self.assertEqual(overview_resp["status"], "SUCCESS")
            self.assertEqual(overview_resp["overview"]["minor_privacy_mode"], "ACTIVE")

            # 3. Crowdsourced Disputes
            disp_payload = DisputeFileRequest(
                student_id="std_router_test_01",
                question_id="q_router_item_01",
                reason="TYPO",
                explanation="Typo in physics unit (m/s instead of m/s^2)."
            )
            disp_file_resp = await file_question_dispute(disp_payload)
            self.assertEqual(disp_file_resp["status"], "SUCCESS")
            disp_id = disp_file_resp["dispute"]["dispute_id"]

            disp_list_resp = await list_question_disputes(status="PENDING")
            self.assertGreaterEqual(disp_list_resp["total_disputes"], 1)

            disp_detail_resp = await get_dispute_by_id(disp_id)
            self.assertEqual(disp_detail_resp["dispute_id"], disp_id)

            disp_res_payload = DisputeResolveRequest(
                moderator_id="usr_mod_router_01",
                action="ACCEPT_CONTENT_EDIT",
                resolution_notes="Typo fixed in question stem.",
                bounty_points=15
            )
            disp_res_resp = await resolve_question_dispute(disp_id, disp_res_payload)
            self.assertEqual(disp_res_resp["status"], "SUCCESS")

            integ_profile = await get_student_integrity_profile("std_router_test_01")
            self.assertGreaterEqual(integ_profile["total_bounty_points"], 15)

        asyncio.run(run_async_tests())


if __name__ == "__main__":
    unittest.main()
