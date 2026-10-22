"""
========================================================================================
MODULE:    Phase 13 Automated Enterprise Test Suite & Persona Lifecycle
TOPIC:     Whole-Journey Multi-Persona End-to-End Simulation & Health Diagnostics
FILE:      backend/tests/test_phase13_enterprise_and_personas.py
PURPOSE:   Simulates an entire student journey across all educational stages:
           1. Class 8 Student: Practice quiz, Elo mastery calibration, streak protection.
           2. Minor Child Safety: 6-digit guardian pairing, tuition co-signing gate (ASVS L2).
           3. Admission Candidate: Timed mock exam with real negative marking.
           4. University/Job Seeker: Skills portfolio & immutable CV snapshot creation.
           5. Academic Crowdsourced QA: Dispute filing, moderator review, integrity bounty.
           6. Enterprise Ops: Deep system health, live telemetry, and ASVS L2 compliance.
AUDIENCE:  QA Engineers, Enterprise Architects & Autonomous Compliance Auditors
STANDARDS: Zero-Emoji Microcopy, ASVS L2 Data Minimization, 100% Deterministic Testing
========================================================================================
"""

import asyncio
import unittest
from backend.app.services.system_diagnostics_service import system_diagnostics_service
from backend.app.services.quiz_engine import quiz_engine
from backend.app.services.psychometrics_service import psychometrics_service
from backend.app.services.guardian_service import guardian_service
from backend.app.services.tuition_service import tuition_service
from backend.app.services.career_service import career_service
from backend.app.services.dispute_service import dispute_service
from backend.app.schemas.quiz_schema import QuizMode
from backend.app.api.v1.router import (
    get_system_health,
    get_system_telemetry,
    get_system_compliance
)


class TestPhase13EnterpriseAndPersonas(unittest.TestCase):
    """
    Simulates the entire multi-persona lifecycle through enterprise services.
    """

    def test_system_diagnostics_service(self):
        """Verifies health checks, telemetry metrics, and ASVS L2 compliance reports."""
        health = system_diagnostics_service.get_health_status()
        self.assertEqual(health["status"], "HEALTHY")
        self.assertEqual(health["platform_name"], "Student Growth Platform (অগ্রযাত্রা)")
        self.assertIn("subsystems", health)
        self.assertEqual(health["subsystems"]["guardian_safety"], "OPERATIONAL")
        self.assertEqual(health["subsystems"]["psychometrics_irt"], "OPERATIONAL")

        telemetry = system_diagnostics_service.get_telemetry_metrics()
        self.assertIn("active_student_attempts", telemetry)
        self.assertIn("quarantined_questions", telemetry)
        self.assertIn("content_pipeline", telemetry)

        compliance = system_diagnostics_service.validate_security_compliance()
        self.assertEqual(compliance["overall_compliance"], "COMPLIANT_ASVS_L2")
        self.assertEqual(len(compliance["checklist"]), 5)
        for check in compliance["checklist"]:
            self.assertEqual(check["status"], "COMPLIANT")

    def test_whole_journey_student_lifecycle(self):
        """
        End-to-End Persona Journey:
        Student (Sadia) -> Practice -> Elo Ability -> Guardian Link -> Tuition Co-Sign ->
        Admission Mock -> Career CV Snapshot -> Defect Dispute -> Moderator Bounty.
        """
        student_id = "std_sadia_full_journey_01"
        guardian_id = "usr_parent_sadia_01"
        tutor_id = "usr_tutor_kamrul_01"

        # Step 1: Practice Quiz & Elo Ability Tracking
        initial_rating = psychometrics_service.get_or_create_student_rating(student_id)
        self.assertEqual(initial_rating, 1200.0)

        new_rating, delta = psychometrics_service.update_rating_after_response(
            student_id=student_id,
            question_difficulty=1200.0,
            is_correct=True
        )
        self.assertEqual(new_rating, 1212.0)
        self.assertEqual(delta, 12.0)

        # Habit & Rest Day pass
        habit = psychometrics_service.get_or_create_habit_record(student_id)
        self.assertEqual(habit["banked_freeze_passes"], 1)

        freeze_ok, _ = psychometrics_service.consume_streak_freeze_pass(student_id)
        self.assertTrue(freeze_ok)

        # Step 2: Guardian Pairing (Minor Student Protection)
        pairing_token = guardian_service.generate_minor_pairing_token(student_id)
        self.assertEqual(len(pairing_token), 6)

        link_ok, _, link_record = guardian_service.link_guardian_to_minor(
            guardian_user_id=guardian_id,
            minor_student_id=student_id,
            pairing_token=pairing_token,
            relationship="MOTHER"
        )
        self.assertTrue(link_ok)
        self.assertEqual(link_record["relationship"], "MOTHER")

        # Step 3: Tuition Request & Guardian Co-Signing Gate
        listing = tuition_service.create_listing(
            creator_user_id=student_id,
            class_grade=8,
            curriculum="NCTB_2024",
            medium="Bangla Medium",
            subject="সাধারণ বিজ্ঞান ও গণিত",
            location_district="Dhaka",
            location_thana="Mirpur",
            is_online=False,
            salary_range_min=5000,
            salary_range_max=7000
        )
        listing_id = listing.id

        # Tutor applies
        ok, app, msg = tuition_service.apply_for_tuition(
            listing_id=listing_id,
            tutor_user_id=tutor_id,
            message="৮ম শ্রেণির গণিত ও পদার্থবিজ্ঞানে ৫ বছরের পড়ানোর অভিজ্ঞতা।"
        )
        self.assertTrue(ok)
        self.assertEqual(app.status, "APPLIED")

        # Guardian Co-Signs on behalf of minor
        cosign_ok, _, sig = guardian_service.record_tuition_co_signature(
            guardian_user_id=guardian_id,
            tuition_listing_id=listing_id,
            minor_student_id=student_id,
            guardian_notes="অনুমোদিত। সপ্তাহে ৩ দিন পড়ানো হবে।"
        )
        self.assertTrue(cosign_ok)
        self.assertIsNotNone(sig)

        # Bilateral consent disclosed
        consent_ok, consent_msg = tuition_service.grant_contact_consent(
            listing_id=listing_id,
            tutor_user_id=tutor_id,
            learner_or_guardian_id=student_id
        )
        self.assertTrue(consent_ok)
        self.assertEqual(consent_msg, "CONTACT_DISCLOSED")

        # Step 4: Admission Mock Exam (University Preparation)
        sample_questions = [
            {
                "id": "q_phys_mock_01",
                "stem_bn": "বল ও ত্বরণের সম্পর্ক কোনটি?",
                "options": [
                    {"id": "opt1_a", "option_key": "A", "option_text_bn": "F = ma", "is_correct": True},
                    {"id": "opt1_b", "option_key": "B", "option_text_bn": "F = m/a", "is_correct": False},
                ],
                "explanation_bn": "নিউটনের ২য় সূত্রানুসারে F = ma।"
            },
            {
                "id": "q_phys_mock_02",
                "stem_bn": "কাজের মাত্রা কী?",
                "options": [
                    {"id": "opt2_a", "option_key": "A", "option_text_bn": "[MLT⁻²]", "is_correct": False},
                    {"id": "opt2_b", "option_key": "B", "option_text_bn": "[ML²T⁻²]", "is_correct": True},
                ],
                "explanation_bn": "কাজ = বল × সরণ = ML²T⁻²।"
            }
        ]

        attempt_resp = quiz_engine.start_practice_attempt(
            user_id=student_id,
            blueprint_id="bp_du_unit_a",
            mode=QuizMode.MOCK_EXAM,
            raw_questions=sample_questions,
            negative_marking=0.25
        )
        attempt_id = attempt_resp.attempt_id

        # Answer q1 correctly (opt1_a)
        quiz_engine.save_answer_idempotent(
            attempt_id=attempt_id,
            user_id=student_id,
            question_version_id="q_phys_mock_01",
            selected_option_id="opt1_a",
            idempotency_key="idem_q1"
        )
        # Answer q2 incorrectly (opt2_a instead of opt2_b)
        quiz_engine.save_answer_idempotent(
            attempt_id=attempt_id,
            user_id=student_id,
            question_version_id="q_phys_mock_02",
            selected_option_id="opt2_a",
            idempotency_key="idem_q2"
        )

        ok, result, msg = quiz_engine.submit_and_score(attempt_id, student_id)
        self.assertTrue(ok)
        self.assertEqual(result.raw_score, 0.75)

        # Step 5: Career Engine & Immutable CV Snapshot
        career_service.add_student_skill(
            student_id=student_id,
            skill_name="Python & Machine Learning",
            proficiency="ADVANCED",
            evidence_url="https://github.com/sadia/deep-learning-bangla"
        )
        cv = career_service.create_cv_snapshot(
            user_id=student_id,
            application_title="Junior AI Engineer",
            student_data={
                "headline": "CSE Undergraduate passionate about NLP & EdTech",
                "skills": ["Python & Machine Learning"]
            }
        )
        self.assertIsNotNone(cv.id)
        self.assertEqual(cv.title, "Junior AI Engineer")

        # Step 6: In-App Defect Dispute & Integrity Bounty
        disp_ok, _, disp_record = dispute_service.file_dispute(
            student_id=student_id,
            question_id="q_phys_mock_02",
            reason="WRONG_KEY",
            explanation="The answer key was mislabeled in the official mock paper.",
            quiz_attempt_id=attempt_id
        )
        self.assertTrue(disp_ok)

        # Moderator accepts and awards 25 bounty points
        res_ok, _, res_rec = dispute_service.resolve_dispute(
            dispute_id=disp_record["dispute_id"],
            moderator_id="usr_chief_mod_01",
            action="ACCEPT_KEY_CORRECTION",
            resolution_notes="Answer key verified and corrected.",
            bounty_points=25
        )
        self.assertTrue(res_ok)
        self.assertEqual(res_rec["bounty_awarded"], 25)

        # Verify Integrity Profile
        profile = dispute_service.get_student_integrity_profile(student_id)
        self.assertEqual(profile["total_bounty_points"], 25)
        self.assertGreaterEqual(len(profile["integrity_badges"]), 1)

    def test_router_enterprise_endpoints(self):
        """Validates /system/health, /system/telemetry, and /system/compliance via async router."""
        async def run_async():
            health = await get_system_health()
            self.assertEqual(health["status"], "HEALTHY")

            telemetry = await get_system_telemetry()
            self.assertIn("active_student_attempts", telemetry)

            compliance = await get_system_compliance()
            self.assertEqual(compliance["overall_compliance"], "COMPLIANT_ASVS_L2")

        asyncio.run(run_async())


if __name__ == "__main__":
    unittest.main()
