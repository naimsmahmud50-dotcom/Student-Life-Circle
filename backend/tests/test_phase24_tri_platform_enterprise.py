"""
========================================================================================
TEST SUITE: Phase 24 Tri-Platform Enterprise Engine (10MS + CareTutors + Bdjobs)
TOPIC:      Video Micro-Classroom, Bilateral Tuition Privacy & Immutable CV Ledger
FILE:       backend/tests/test_phase24_tri_platform_enterprise.py
PURPOSE:    Validates the end-to-end integration and whitebox security of:
            1. 10 Minute School: In-lecture checkpoint quizzes & playback telemetry
            2. CareTutors: Live regional tuition feed, bilateral consent & IDOR contact shielding
            3. Bdjobs: Cryptographic CV snapshot freezing, SHA-256 HMAC & 5-stage pipeline
STANDARDS:  OWASP ASVS L2, Machine-Readable Envelopes, Strict Whitebox Verification
AUDIENCE:   QA Engineers, Security Auditors & Platform Architects
========================================================================================
"""

import unittest
from datetime import datetime, timezone

from backend.app.services.video_classroom_service import video_classroom_service
from backend.app.services.tuition_marketplace_service import (
    tuition_marketplace_service,
    mask_phone_number
)
from backend.app.services.job_placement_service import (
    job_placement_service,
    _CV_SNAPSHOT_SECRET
)
from backend.app.schemas.tri_platform_schema import (
    VideoProgressUpdateRequest,
    CheckpointQuizSubmitRequest,
    VideoNoteCreateRequest,
    TuitionMarketplaceListingCreateRequest,
    TuitionApplicationSubmitRequest,
    BilateralConsentUpdateRequest,
    JobPostingCreateRequest,
    CVSnapshotFreezeRequest,
    JobApplicationSubmitSealedRequest,
    PipelineStageAdvanceRequest
)
from backend.app.api.v1.router import (
    update_video_playback_progress,
    get_video_in_lecture_checkpoints,
    submit_video_checkpoint_quiz_answer,
    pin_video_timestamp_note,
    get_student_video_notes,
    create_guardian_tuition_listing,
    get_live_tuition_feed,
    apply_for_tuition_listing,
    update_bilateral_tuition_consent,
    get_tuition_contact_status,
    create_employer_job_posting,
    get_live_job_feed,
    freeze_candidate_cv_snapshot,
    verify_cv_snapshot_integrity,
    apply_for_job_with_sealed_cv,
    advance_hiring_pipeline_stage
)


class TestPhase24TriPlatformEnterprise(unittest.IsolatedAsyncioTestCase):
    """
    Comprehensive test suite for Phase 24 Tri-Platform convergence features.
    """

    # ==================================================================================
    # TOPIC 1: 10 MINUTE SCHOOL BENCHMARK - VIDEO MICRO-CLASSROOM & CHECKPOINTS
    # ==================================================================================

    async def test_video_playback_progress_telemetry(self):
        """Verifies playback progress recording and completion percentage computation."""
        payload = VideoProgressUpdateRequest(
            video_id="vid_diff_01",
            student_id="student_101",
            current_timestamp_seconds=270.0,
            total_duration_seconds=600.0,
            resolution="1080p",
            playback_speed=1.25
        )
        res = await update_video_playback_progress(payload)
        self.assertTrue(res["success"])
        state = res["playback_state"]
        self.assertEqual(state["video_id"], "vid_diff_01")
        self.assertEqual(state["completion_percentage"], 45.0)
        self.assertFalse(state["is_completed"])
        self.assertEqual(state["playback_speed"], 1.25)

        # Test completed threshold (>= 90%)
        payload_complete = VideoProgressUpdateRequest(
            video_id="vid_diff_01",
            student_id="student_101",
            current_timestamp_seconds=570.0,
            total_duration_seconds=600.0
        )
        res_comp = await update_video_playback_progress(payload_complete)
        self.assertTrue(res_comp["playback_state"]["is_completed"])

    async def test_in_lecture_checkpoint_quiz_correct_and_incorrect(self):
        """Verifies in-lecture checkpoint evaluation, explanations, and milestone unlocks."""
        # 1. Fetch checkpoints
        checkpoints = await get_video_in_lecture_checkpoints("vid_diff_01")
        self.assertGreaterEqual(len(checkpoints), 1)
        cp = checkpoints[0]
        self.assertEqual(cp["checkpoint_id"], "cp_diff_01")

        # 2. Submit Incorrect Option
        wrong_payload = CheckpointQuizSubmitRequest(
            video_id="vid_diff_01",
            checkpoint_id="cp_diff_01",
            student_id="student_102",
            timestamp_seconds=252.0,
            selected_option_index=2  # Option 0 is correct
        )
        res_wrong = await submit_video_checkpoint_quiz_answer(wrong_payload)
        self.assertTrue(res_wrong["success"])
        self.assertFalse(res_wrong["is_correct"])
        self.assertIsNone(res_wrong["milestone_unlocked"])
        self.assertIn("Chain Rule", res_wrong["explanation"])

        # 3. Submit Correct Option
        correct_payload = CheckpointQuizSubmitRequest(
            video_id="vid_diff_01",
            checkpoint_id="cp_diff_01",
            student_id="student_102",
            timestamp_seconds=252.0,
            selected_option_index=0
        )
        res_correct = await submit_video_checkpoint_quiz_answer(correct_payload)
        self.assertTrue(res_correct["success"])
        self.assertTrue(res_correct["is_correct"])
        self.assertEqual(res_correct["milestone_unlocked"], "Chain Rule Foundations")
        self.assertGreater(res_correct["mastery_score"], 0)

    async def test_timestamped_notes_pinning_and_retrieval(self):
        """Verifies student bookmark note creation at timestamp and chronological retrieval."""
        note_payload = VideoNoteCreateRequest(
            video_id="vid_diff_01",
            student_id="student_103",
            timestamp_seconds=184.5,
            note_text="Remember: substitution u = g(x) must be differentiated first.",
            is_bookmarked=True
        )
        res = await pin_video_timestamp_note(note_payload)
        self.assertTrue(res["success"])
        self.assertEqual(res["note"]["formatted_timestamp"], "03:04")

        # Retrieve notes
        notes = await get_student_video_notes(video_id="vid_diff_01", student_id="student_103")
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["note_text"], "Remember: substitution u = g(x) must be differentiated first.")

    # ==================================================================================
    # TOPIC 2: CARETUTORS BENCHMARK - TUITION MARKETPLACE & BILATERAL CONSENT
    # ==================================================================================

    def test_phone_number_masking_utility(self):
        """Validates that phone masking properly conceals sensitive PII digits."""
        raw = "+8801712345678"
        masked = mask_phone_number(raw)
        self.assertEqual(masked, "+880 17•• ••••78")
        self.assertNotIn("3456", masked)

    async def test_guardian_tuition_post_and_feed_masking(self):
        """Verifies Guardian tuition creation and automatic feed PII redaction."""
        listing_payload = TuitionMarketplaceListingCreateRequest(
            creator_user_id="guard_sec_01",
            class_grade=11,
            curriculum="NCTB",
            medium="BANGLA_MEDIUM",
            subject="Higher Mathematics & Physics",
            location_district="Dhaka",
            location_thana="Mirpur",
            days_per_week=3,
            gender_preference="ANY",
            salary_budget_bdt=8500,
            guardian_phone="+8801799887766",
            requirements="Focus on vector geometry and calculus."
        )
        res = await create_guardian_tuition_listing(listing_payload)
        self.assertTrue(res["success"])
        created = res["listing"]
        self.assertEqual(created["location_thana"], "Mirpur")
        self.assertIn("masked_guardian_phone", created)
        self.assertNotIn("01799887766", created["masked_guardian_phone"])

        # Feed query
        feed = await get_live_tuition_feed(district="Dhaka", search_query="Mirpur")
        self.assertGreaterEqual(len(feed), 1)
        item = next(x for x in feed if x["id"] == created["id"])
        self.assertNotIn("guardian_phone", item)  # Raw PII must be completely stripped

    async def test_tuition_bilateral_consent_handshake(self):
        """Verifies mutual bilateral consent state machine and contact revelation."""
        # 1. Post Listing
        post_res = await create_guardian_tuition_listing(TuitionMarketplaceListingCreateRequest(
            creator_user_id="guardian_bilat_01",
            class_grade=12,
            subject="Physics",
            location_district="Chattogram",
            location_thana="Panchlaish",
            salary_budget_bdt=8000,
            guardian_phone="+8801811223344"
        ))
        listing_id = post_res["listing"]["id"]

        # 2. Tutor Applies
        apply_res = await apply_for_tuition_listing(TuitionApplicationSubmitRequest(
            listing_id=listing_id,
            tutor_user_id="tutor_buet_01",
            tutor_name="Tanvir Hasan",
            tutor_university="BUET",
            tutor_cgpa_or_gpa="3.92",
            tutor_phone="+8801755667788",
            cover_letter="I secured 1st place in National Physics Olympiad."
        ))
        self.assertTrue(apply_res["success"])
        app_id = apply_res["application"]["application_id"]
        self.assertEqual(apply_res["application"]["status"], "PENDING")

        # 3. Check Contact Status before consent (Must be masked)
        status_before = await get_tuition_contact_status(
            application_id=app_id,
            requesting_user_id="guardian_bilat_01"
        )
        self.assertFalse(status_before["contact_unlocked"])
        self.assertIn("masked_phone", status_before)

        # 4. Guardian Approves
        guard_consent = await update_bilateral_tuition_consent(BilateralConsentUpdateRequest(
            listing_id=listing_id,
            application_id=app_id,
            actor_user_id="guardian_bilat_01",
            action="GUARDIAN_APPROVE"
        ))
        self.assertTrue(guard_consent["success"])
        self.assertEqual(guard_consent["status"], "GUARDIAN_APPROVED")
        self.assertFalse(guard_consent["contact_unlocked"])

        # 5. Tutor Accepts (Completes Bilateral Agreement)
        tutor_consent = await update_bilateral_tuition_consent(BilateralConsentUpdateRequest(
            listing_id=listing_id,
            application_id=app_id,
            actor_user_id="tutor_buet_01",
            action="TUTOR_ACCEPT"
        ))
        self.assertTrue(tutor_consent["success"])
        self.assertEqual(tutor_consent["status"], "MUTUAL_CONSENT_UNLOCKED")
        self.assertTrue(tutor_consent["contact_unlocked"])

        # 6. Check Contact Status after bilateral consent
        status_after_guardian = await get_tuition_contact_status(
            application_id=app_id,
            requesting_user_id="guardian_bilat_01"
        )
        self.assertTrue(status_after_guardian["contact_unlocked"])
        self.assertEqual(status_after_guardian["tutor_phone"], "+8801755667788")

        status_after_tutor = await get_tuition_contact_status(
            application_id=app_id,
            requesting_user_id="tutor_buet_01"
        )
        self.assertTrue(status_after_tutor["contact_unlocked"])
        self.assertEqual(status_after_tutor["guardian_phone"], "+8801811223344")

    # ==================================================================================
    # TOPIC 3: WHITEBOX SECURITY & IDOR DEFENSE (/strix-source-aware-whitebox)
    # ==================================================================================

    async def test_whitebox_idor_unauthorized_contact_disclosure_blocked(self):
        """
        ASVS L2 Whitebox Security Test:
        Verifies that an unauthorized third-party user cannot access contact details
        of another party's tuition application even if mutual consent was granted.
        """
        # Create listing and complete handshake
        post_res = await create_guardian_tuition_listing(TuitionMarketplaceListingCreateRequest(
            creator_user_id="guardian_idor_01",
            class_grade=10,
            subject="Chemistry",
            location_district="Sylhet",
            location_thana="Zindabazar",
            salary_budget_bdt=10000,
            guardian_phone="+8801999888777"
        ))
        listing_id = post_res["listing"]["id"]

        apply_res = await apply_for_tuition_listing(TuitionApplicationSubmitRequest(
            listing_id=listing_id,
            tutor_user_id="tutor_idor_01",
            tutor_name="Nafis Iqbal",
            tutor_university="SUST",
            tutor_cgpa_or_gpa="3.85",
            tutor_phone="+8801888777666"
        ))
        app_id = apply_res["application"]["application_id"]

        # Complete mutual consent
        await update_bilateral_tuition_consent(BilateralConsentUpdateRequest(
            listing_id=listing_id,
            application_id=app_id,
            actor_user_id="guardian_idor_01",
            action="GUARDIAN_APPROVE"
        ))
        await update_bilateral_tuition_consent(BilateralConsentUpdateRequest(
            listing_id=listing_id,
            application_id=app_id,
            actor_user_id="tutor_idor_01",
            action="TUTOR_ACCEPT"
        ))

        # Attempt IDOR attack by malicious outsider
        from backend.app.core.fastapi_shim import HTTPException
        with self.assertRaises(HTTPException) as ctx:
            await get_tuition_contact_status(
                application_id=app_id,
                requesting_user_id="attacker_user_666"
            )
        self.assertEqual(ctx.exception.status_code, 403)

    # ==================================================================================
    # TOPIC 4: BDJOBS BENCHMARK - CAREER ARENA & IMMUTABLE CV SNAPSHOT LEDGER
    # ==================================================================================

    async def test_cv_snapshot_canonical_hashing_and_tamper_detection(self):
        """Verifies cryptographic freezing with SHA-256 and detects unauthorized payload tampering."""
        freeze_payload = CVSnapshotFreezeRequest(
            candidate_user_id="cand_sec_01",
            full_name="Mahmud Hasan",
            academic_institution="University of Dhaka (CSE)",
            academic_cgpa=3.95,
            cat_ability_theta=2.15,
            verified_skills=["Python", "FastAPI", "Distributed Systems", "SQL"],
            portfolio_urls=["https://github.com/mahmud/agrojatra"]
        )
        freeze_res = await freeze_candidate_cv_snapshot(freeze_payload)
        self.assertTrue(freeze_res["success"])
        snapshot = freeze_res["snapshot"]
        snap_id = snapshot["snapshot_id"]

        self.assertIn("urn:cv-snapshot:sha256:", snapshot["urn"])
        self.assertEqual(len(snapshot["sha256_hash"]), 64)
        self.assertEqual(len(snapshot["hmac_signature"]), 64)

        # 1. Verify authentic snapshot
        ver_res = await verify_cv_snapshot_integrity(snapshot_id=snap_id)
        self.assertTrue(ver_res["is_valid"])
        self.assertFalse(ver_res["tampered"])

        # 2. Simulate malicious in-memory tampering (e.g. inflating CGPA to 4.00)
        tampered_record = job_placement_service._cv_snapshots[snap_id]
        tampered_record["payload"]["academic_cgpa"] = 4.00  # Tampering!

        # 3. Verify that tampering is immediately detected
        ver_tampered = await verify_cv_snapshot_integrity(snapshot_id=snap_id)
        self.assertFalse(ver_tampered["is_valid"])
        self.assertTrue(ver_tampered["tampered"])
        self.assertIn("TAMPERING DETECTED", ver_tampered["message"])

    async def test_job_application_with_sealed_cv_and_ats_match(self):
        """Verifies job application binding to sealed CV and ATS skill matching."""
        # 1. Freeze authentic CV
        freeze_res = await freeze_candidate_cv_snapshot(CVSnapshotFreezeRequest(
            candidate_user_id="cand_ats_01",
            full_name="Ayesha Siddiqua",
            academic_institution="BUET (EEE)",
            academic_cgpa=3.88,
            cat_ability_theta=1.92,
            verified_skills=["Python", "FastAPI", "PostgreSQL", "REST APIs", "Git"]
        ))
        snap_id = freeze_res["snapshot"]["snapshot_id"]

        # 2. Apply for Brain Station 23 Intern job (requires Python, FastAPI, PostgreSQL, REST APIs, Git)
        apply_payload = JobApplicationSubmitSealedRequest(
            job_id="job_bs23_01",
            candidate_user_id="cand_ats_01",
            cv_snapshot_id=snap_id,
            expected_salary_bdt=25000,
            cover_note="Passionate about scalable microservices."
        )
        app_res = await apply_for_job_with_sealed_cv(apply_payload)
        self.assertTrue(app_res["success"])
        app = app_res["application"]
        self.assertEqual(app["current_stage"], "APPLIED")
        self.assertEqual(app["ats_match_percentage"], 100.0)

        # 3. Advance hiring pipeline stage
        adv_res = await advance_hiring_pipeline_stage(
            application_id=app["application_id"],
            payload=PipelineStageAdvanceRequest(
                application_id=app["application_id"],
                employer_user_id="emp_bs23",
                new_stage="INTERVIEW",
                feedback_notes="Candidate has 100% skill match. Scheduled technical viva."
            )
        )
        self.assertTrue(adv_res["success"])
        self.assertEqual(adv_res["new_stage"], "INTERVIEW")
        self.assertEqual(len(adv_res["stage_history"]), 2)


if __name__ == "__main__":
    unittest.main()
