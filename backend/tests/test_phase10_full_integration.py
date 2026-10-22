"""
========================================================================================
MODULE:    Automated Verification Test Suite - Phase 10 Full Integration
TOPIC:     End-to-End API Router Verification for Live, Admission, Tuition & Career
FILE:      backend/tests/test_phase10_full_integration.py
PURPOSE:   Verifies all newly mounted REST API endpoints in router.py. Tests:
           1. Live challenge listing, pre-warming, session start, pseudonymous leaderboards,
              and mental wellness opt-out preference.
           2. University admission blueprints catalog, verified circulars, and diagnostic
              gap analysis with 7-day personalized study sprint.
           3. Tuition marketplace listing creation, tutor application, and bilateral contact
              consent disclosure.
           4. Career engine evidence portfolio, immutable CV snapshots, and recruiter pipeline.
           5. Curricula registry and spaced-repetition mistake replay revision queue.
AUDIENCE:  QA Engineers, System Integrators & AI Agents
STANDARDS: Zero Regressions, Async Verification, ASVS L2 Data Minimization
========================================================================================
"""

import asyncio
import unittest
from backend.app.api.v1.router import (
    health_check,
    get_curricula_catalog,
    get_revision_queue,
    list_live_sessions,
    prewarm_live_session,
    start_live_session,
    get_live_leaderboard,
    leaderboard_privacy_opt_out,
    list_admission_blueprints,
    analyze_diagnostic_sprint,
    list_verified_circulars,
    get_tuition_listings,
    create_tuition_listing,
    apply_for_tuition,
    grant_tuition_consent,
    add_student_skill,
    get_student_skills,
    create_cv_snapshot,
    list_career_opportunities,
    apply_to_job,
    update_application_stage
)
from backend.app.schemas.opportunity_schema import (
    TuitionListingCreateRequest,
    TuitionApplyRequest,
    ContactConsentGrantRequest,
    StudentSkillAddRequest,
    CVSnapshotCreateRequest,
    JobApplicationSubmitRequest,
    ApplicationStageUpdateRequest
)
from backend.app.schemas.live_and_admission_schema import (
    LiveSessionPrewarmRequest,
    LeaderboardOptOutRequest,
    DiagnosticAnalyzeRequest
)
from backend.app.schemas.quiz_schema import QuizMode


class TestPhase10FullIntegration(unittest.TestCase):
    """
    Integration test suite verifying all Phase 10 API router endpoints.
    """

    def test_01_health_and_curricula_endpoints(self):
        """Verifies health check and NCTB curricula catalog endpoints."""
        health = asyncio.run(health_check())
        self.assertEqual(health["status"], "healthy")
        self.assertEqual(health["version"], "2.0.0")
        self.assertIn("server_time", health)

        catalog = asyncio.run(get_curricula_catalog())
        self.assertGreater(len(catalog["curricula"]), 0)
        self.assertGreater(len(catalog["subjects"]), 0)
        # Check presence of Class 7, SSC, and HSC subjects
        subject_names = [s["name_bn"] for s in catalog["subjects"]]
        self.assertTrue(any("পদার্থবিজ্ঞান" in name for name in subject_names))

        rev_queue = asyncio.run(get_revision_queue("usr_student_01"))
        self.assertEqual(rev_queue["user_id"], "usr_student_01")
        self.assertGreaterEqual(rev_queue["queue_count"], 1)

    def test_02_live_challenge_full_flow(self):
        """Verifies session listing, pre-warming, starting, leaderboard, and opt-out."""
        # 1. List live sessions
        sessions = asyncio.run(list_live_sessions())
        self.assertGreaterEqual(len(sessions["active_sessions"]), 1)
        session_id = sessions["active_sessions"][0]["session_id"]

        # 2. Prewarm session
        prewarm_payload = LiveSessionPrewarmRequest(
            blueprint_title="HSC Physics Live",
            start_time="2026-10-15T20:00:00Z",
            end_time="2026-10-15T20:25:00Z",
            duration_minutes=25
        )
        prewarm_res = asyncio.run(prewarm_live_session(session_id, prewarm_payload))
        self.assertEqual(prewarm_res["status"], "PREWARMED")

        # 3. Start live attempt
        attempt = asyncio.run(start_live_session(session_id=session_id, user_id="usr_live_test_01"))
        self.assertIsNotNone(attempt.attempt_id)
        self.assertEqual(attempt.mode, QuizMode.LIVE_CHALLENGE)
        self.assertGreaterEqual(len(attempt.questions), 1)

        # 4. Get leaderboard
        leaderboard = asyncio.run(get_live_leaderboard(session_id))
        self.assertEqual(leaderboard["session_id"], session_id)
        self.assertGreaterEqual(leaderboard["total_ranked"], 1)
        # Ensure rankings are sorted with rank 1 at the top
        self.assertEqual(leaderboard["rankings"][0]["rank"], 1)

        # 5. Leaderboard privacy opt-out toggle
        opt_out_payload = LeaderboardOptOutRequest(opt_out=True)
        opt_out_res = asyncio.run(leaderboard_privacy_opt_out(user_id="usr_live_test_01", payload=opt_out_payload))
        self.assertTrue(opt_out_res["opted_out_of_public_leaderboard"])

    def test_03_admission_hub_and_diagnostic_sprint(self):
        """Verifies admission blueprints, circulars, and diagnostic analysis."""
        blueprints = asyncio.run(list_admission_blueprints())
        self.assertGreaterEqual(blueprints["total"], 1)
        # Check DU Unit-A blueprint presence
        du_bp = next((bp for bp in blueprints["blueprints"] if bp["id"] == "bp_du_unit_a"), None)
        self.assertIsNotNone(du_bp)
        self.assertEqual(du_bp["negative_marking_value"], 0.25)

        # Diagnostic sprint calculation
        diagnostic_payload = DiagnosticAnalyzeRequest(
            topic_performance=[
                {"topic_name": "গতিবিদ্যা ও বলবিদ্যা", "subject": "পদার্থবিজ্ঞান", "correct": 5, "total": 5},   # 100% -> STRONG
                {"topic_name": "গুণগত রসায়ন", "subject": "রসায়ন", "correct": 3, "total": 5},                   # 60% -> NEEDS_REVISION
                {"topic_name": "অন্তরীকরণ (Calculus)", "subject": "উচ্চতর গণিত", "correct": 1, "total": 5},     # 20% -> CRITICAL_GAP
            ]
        )
        sprint = asyncio.run(analyze_diagnostic_sprint(diagnostic_payload))
        self.assertEqual(sprint["strong_count"], 1)
        self.assertEqual(sprint["revision_count"], 1)
        self.assertEqual(sprint["critical_gap_count"], 1)
        self.assertIn("seven_day_sprint_plan", sprint)
        self.assertGreaterEqual(len(sprint["seven_day_sprint_plan"]), 1)

        # Verified circulars
        circulars = asyncio.run(list_verified_circulars())
        self.assertGreaterEqual(len(circulars["circulars"]), 1)
        self.assertTrue(circulars["circulars"][0]["is_verified"])

    def test_04_tuition_marketplace_and_bilateral_consent(self):
        """Verifies tuition listing creation, tutor application, and bilateral contact consent."""
        # 1. Create listing
        create_payload = TuitionListingCreateRequest(
            class_grade=9,
            curriculum="NCTB",
            medium="BANGLA",
            subject="উচ্চতর গণিত ও পদার্থবিজ্ঞান",
            location_district="Dhaka",
            location_thana="Mirpur",
            is_online=False,
            salary_range_min=6000,
            salary_range_max=8000
        )
        create_res = asyncio.run(create_tuition_listing(create_payload, user_id="guardian_mirpur_01"))
        self.assertEqual(create_res["status"], "SUCCESS")
        listing_id = create_res["listing"]["id"]

        # 2. Search listings
        listings_res = asyncio.run(get_tuition_listings(district="Dhaka", class_grade=9))
        self.assertGreaterEqual(len(listings_res["listings"]), 1)

        # 3. Tutor applies to listing
        apply_payload = TuitionApplyRequest(message="আমি বুয়েট থেকে স্নাতক, যত্ন সহকারে পড়াবো।")
        apply_res = asyncio.run(apply_for_tuition(
            listing_id=listing_id,
            payload=apply_payload,
            tutor_id="tutor_buet_01"
        ))
        self.assertEqual(apply_res["status"], "APPLIED")
        # Contact consent must NOT be granted immediately (privacy protection)
        self.assertFalse(apply_res["contact_consent_granted"])

        # 4. Guardian/Learner grants bilateral consent
        consent_payload = ContactConsentGrantRequest(tutor_user_id="tutor_buet_01")
        consent_res = asyncio.run(grant_tuition_consent(
            listing_id=listing_id,
            payload=consent_payload,
            guardian_or_learner_id="guardian_mirpur_01"
        ))
        self.assertEqual(consent_res["status"], "CONSENT_GRANTED")

    def test_05_career_portfolio_and_immutable_cv_snapshot(self):
        """Verifies skills portfolio, immutable CV freezing, and recruiter pipeline."""
        student_id = "std_cs_graduate_01"

        # 1. Add verified skill claim
        skill_payload = StudentSkillAddRequest(
            skill_name="Full Stack Development (FastAPI + Next.js)",
            proficiency="ADVANCED",
            evidence_url="https://github.com/student/student-life-circle"
        )
        skill_res = asyncio.run(add_student_skill(payload=skill_payload, student_id=student_id))
        self.assertEqual(skill_res["status"], "SUCCESS")
        self.assertTrue(skill_res["skill"]["is_verified"])

        # 2. Get student skills
        skills_list = asyncio.run(get_student_skills(student_id))
        self.assertGreaterEqual(skills_list["total_skills"], 1)

        # 3. Create frozen CV snapshot
        student_profile_data = {
            "name": "Mahmud Hasan",
            "education": "B.Sc. in Computer Science & Engineering",
            "cgpa": 3.85,
            "skills": ["Python", "FastAPI", "React", "PostgreSQL"],
            "projects": ["Student Growth Platform"]
        }
        cv_payload = CVSnapshotCreateRequest(
            application_title="Junior Software Engineer Application",
            student_data=student_profile_data
        )
        snapshot_res = asyncio.run(create_cv_snapshot(payload=cv_payload, user_id=student_id))
        self.assertEqual(snapshot_res["status"], "FROZEN")
        snapshot_id = snapshot_res["snapshot_id"]

        # Mutate the source data to verify snapshot immutability
        student_profile_data["skills"].append("Hacked Skill")
        frozen_skills = snapshot_res["snapshot"]["snapshot_json"]["skills"]
        self.assertNotIn("Hacked Skill", frozen_skills, "Snapshot must remain strictly immutable!")

        # 4. Apply to job using snapshot
        jobs_res = asyncio.run(list_career_opportunities())
        self.assertGreaterEqual(len(jobs_res["jobs"]), 1)
        job_id = jobs_res["jobs"][0]["id"]

        job_apply_payload = JobApplicationSubmitRequest(job_id=job_id, cv_snapshot_id=snapshot_id)
        job_apply_res = asyncio.run(apply_to_job(payload=job_apply_payload, candidate_id=student_id))
        self.assertEqual(job_apply_res["status"], "APPLIED")
        self.assertEqual(job_apply_res["stage"], "APPLIED")

        # 5. Recruiter updates candidate stage
        stage_payload = ApplicationStageUpdateRequest(new_stage="INTERVIEW")
        stage_res = asyncio.run(update_application_stage(job_id=job_id, candidate_id=student_id, payload=stage_payload))
        self.assertEqual(stage_res["status"], "SUCCESS")
        self.assertEqual(stage_res["new_stage"], "INTERVIEW")


if __name__ == "__main__":
    unittest.main()
