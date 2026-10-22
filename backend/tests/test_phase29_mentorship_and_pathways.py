"""
Unit and Integration Test Suite: Phase 29
Verifies:
1. AlumniMentorshipService (1-on-1 booking, WebRTC tokens, double-booking prevention, escrow release)
2. AdaptiveLearningPathService (concept graph traversal, remedial sprint generation, readiness delta)
3. CertificateVerificationService (tamper-evident SHA-256 signing, public lookup, tamper detection)
4. Section 28 REST Routes in router.py
"""

import unittest
from backend.app.services.alumni_mentorship_service import AlumniMentorshipService
from backend.app.services.adaptive_learning_path_service import AdaptiveLearningPathService
from backend.app.services.certificate_verification_service import CertificateVerificationService
from backend.app.schemas.mentorship_and_pathway_schema import (
    BookMentorshipSessionRequest,
    GenerateAdaptivePathwayRequest,
    IssueCertificateRequest
)
from backend.app.api.v1.router import (
    list_alumni_mentors,
    get_alumni_mentor_profile,
    book_mentorship_session,
    get_mentorship_session_status,
    complete_mentorship_session,
    generate_adaptive_learning_pathway,
    get_adaptive_pathway_status,
    complete_remedial_sprint_step,
    issue_verifiable_certificate,
    verify_certificate_authenticity
)

class TestPhase29MentorshipAndPathways(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mentor_service = AlumniMentorshipService()
        self.pathway_service = AdaptiveLearningPathService()
        self.cert_service = CertificateVerificationService()

    def test_list_mentors_and_specialty_filter(self):
        all_mentors = self.mentor_service.get_all_mentors()
        self.assertGreaterEqual(len(all_mentors), 3)

        buet_mentors = self.mentor_service.get_all_mentors(specialty_filter="BUET")
        self.assertTrue(any("BUET" in m["alma_mater"] for m in buet_mentors))

        iba_mentors = self.mentor_service.get_all_mentors(specialty_filter="IBA")
        self.assertTrue(any("IBA" in m["alma_mater"] for m in iba_mentors))

    def test_book_mentorship_session_success(self):
        mentor = self.mentor_service.get_all_mentors()[0]
        slot = mentor["available_slots"][0]
        session = self.mentor_service.book_session(
            mentor_id=mentor["mentor_id"],
            student_id="std-88",
            student_name="Tarek Rahman",
            slot_time=slot,
            topic_focus="BUET CSE Admission Strategy & Math Drill",
            target_ambition="BUET CSE Enrollment",
            fee_bdt=500.0,
            payment_method="bKash"
        )
        self.assertIn("session_id", session)
        self.assertEqual(session["status"], "CONFIRMED")
        self.assertTrue(session["webrtc_channel_token"].startswith("wrtc_"))
        self.assertTrue(session["escrow_tx_id"].startswith("ESC-BK-"))
        # Verify slot was evicted
        self.assertNotIn(slot, self.mentor_service.get_mentor_by_id(mentor["mentor_id"])["available_slots"])

    def test_double_booking_slot_rejected(self):
        mentor = self.mentor_service.get_all_mentors()[0]
        slot = mentor["available_slots"][0]
        # First booking succeeds
        self.mentor_service.book_session(
            mentor_id=mentor["mentor_id"],
            student_id="std-88",
            student_name="Tarek Rahman",
            slot_time=slot,
            topic_focus="Calculus",
            target_ambition="BUET",
            fee_bdt=500.0
        )
        # Concurrent second booking must fail with ValueError
        with self.assertRaises(ValueError):
            self.mentor_service.book_session(
                mentor_id=mentor["mentor_id"],
                student_id="std-99",
                student_name="Sumi Akter",
                slot_time=slot,
                topic_focus="Calculus",
                target_ambition="BUET",
                fee_bdt=500.0
            )

    def test_complete_mentorship_session_and_release_escrow(self):
        mentor = self.mentor_service.get_all_mentors()[0]
        slot = mentor["available_slots"][0]
        session = self.mentor_service.book_session(
            mentor_id=mentor["mentor_id"],
            student_id="std-88",
            student_name="Tarek Rahman",
            slot_time=slot,
            topic_focus="Calculus",
            target_ambition="BUET"
        )
        completed = self.mentor_service.complete_session_and_release_escrow(
            session_id=session["session_id"],
            student_rating=5.0
        )
        self.assertEqual(completed["status"], "COMPLETED")
        self.assertEqual(completed["escrow_status"], "FUNDS_RELEASED_TO_MENTOR")
        self.assertEqual(completed["student_rating"], 5.0)

        # Duplicate complete raises ValueError
        with self.assertRaises(ValueError):
            self.mentor_service.complete_session_and_release_escrow(
                session_id=session["session_id"],
                student_rating=5.0
            )

    def test_adaptive_pathway_generation(self):
        pathway = self.pathway_service.generate_pathway(
            student_id="std-404",
            subject="Higher Mathematics",
            weak_topic_ids=["chain_rule", "integration_by_parts"],
            target_mastery_pct=92.0
        )
        self.assertIn("pathway_id", pathway)
        self.assertEqual(pathway["subject"], "Higher Mathematics")
        self.assertLessEqual(pathway["current_readiness_pct"], 80.0)
        self.assertEqual(pathway["projected_mastery_pct"], 92.0)
        # Each topic generates 3 steps + 1 final milestone = 7 steps
        self.assertEqual(len(pathway["steps"]), 7)
        self.assertEqual(pathway["steps"][0]["step_type"], "DIAGNOSTIC")
        self.assertEqual(pathway["steps"][1]["step_type"], "MICRO_LECTURE")
        self.assertEqual(pathway["steps"][2]["step_type"], "PRACTICE_DRILL")
        self.assertEqual(pathway["steps"][-1]["step_type"], "MASTERY_ASSESSMENT")

    def test_adaptive_pathway_step_completion(self):
        pathway = self.pathway_service.generate_pathway(
            student_id="std-404",
            subject="Higher Mathematics",
            weak_topic_ids=["chain_rule"],
            target_mastery_pct=90.0
        )
        initial_readiness = pathway["current_readiness_pct"]
        updated = self.pathway_service.complete_step(
            pathway_id=pathway["pathway_id"],
            step_id="step-1"
        )
        self.assertEqual(updated["steps"][0]["status"], "COMPLETED")
        self.assertGreater(updated["current_readiness_pct"], initial_readiness)

    def test_issue_and_verify_certificate_success(self):
        cert = self.cert_service.issue_certificate(
            student_id="std-777",
            student_name="Nadia Islam",
            course_or_track="Full-Stack Web Development & Microservices",
            grade_or_score="96.0% (Tier 1 High Distinction)",
            skills_mastered=["Python", "FastAPI", "React", "PostgreSQL", "Docker"]
        )
        self.assertTrue(cert["certificate_id"].startswith("AGRO-"))
        self.assertEqual(len(cert["sha256_hash"]), 64)

        # Verification by Certificate ID
        res_by_id = self.cert_service.verify_certificate(identifier=cert["certificate_id"])
        self.assertTrue(res_by_id["verified"])
        self.assertEqual(res_by_id["student_name"], "Nadia Islam")
        self.assertFalse(res_by_id["tamper_detected"])

        # Verification by SHA-256 Hash
        res_by_hash = self.cert_service.verify_certificate(identifier=cert["sha256_hash"])
        self.assertTrue(res_by_hash["verified"])
        self.assertEqual(res_by_hash["certificate_id"], cert["certificate_id"])

    def test_certificate_tamper_detection(self):
        cert = self.cert_service.issue_certificate(
            student_id="std-888",
            student_name="Mahir Faysal",
            course_or_track="NCTB Class 10 Physics Masterclass",
            grade_or_score="82.0%",
            skills_mastered=["Kinematics", "Optics"]
        )
        # Simulate unauthorized database tampering of grade
        cert["grade_or_score"] = "99.9% (Falsified Score)"

        res = self.cert_service.verify_certificate(identifier=cert["certificate_id"])
        self.assertFalse(res["verified"])
        self.assertTrue(res["tamper_detected"])

    def test_certificate_not_found(self):
        res = self.cert_service.verify_certificate(identifier="AGRO-INVALID-999")
        self.assertFalse(res["verified"])
        self.assertIn("not found", res["message"])

    # REST Endpoint Integration Tests
    async def test_rest_endpoints(self):
        mentors = await list_alumni_mentors(specialty=None)
        self.assertGreaterEqual(len(mentors), 3)

        mentor_id = mentors[0]["mentor_id"]
        profile = await get_alumni_mentor_profile(mentor_id=mentor_id)
        self.assertEqual(profile["mentor_id"], mentor_id)

        # Book session via router
        booking_payload = BookMentorshipSessionRequest(
            mentor_id=mentor_id,
            student_id="std-123",
            student_name="Labib Khan",
            slot_time=profile["available_slots"][0],
            topic_focus="IBA Math Strategy",
            target_ambition="IBA Admission",
            fee_bdt=500.0,
            payment_method="bKash"
        )
        session = await book_mentorship_session(payload=booking_payload)
        self.assertEqual(session["status"], "CONFIRMED")

        # Generate pathway via router
        pathway_payload = GenerateAdaptivePathwayRequest(
            student_id="std-123",
            subject="Physics",
            weak_topic_ids=["rotational_dynamics"],
            target_mastery_pct=95.0
        )
        pathway = await generate_adaptive_learning_pathway(payload=pathway_payload)
        self.assertIn("pathway_id", pathway)

        # Verify certificate via router
        cert_payload = IssueCertificateRequest(
            student_id="std-123",
            student_name="Labib Khan",
            course_or_track="Physics Excellence",
            grade_or_score="94.5%",
            skills_mastered=["Rotational Dynamics", "Newtonian Laws"]
        )
        issued_cert = await issue_verifiable_certificate(payload=cert_payload)
        verify_result = await verify_certificate_authenticity(identifier=issued_cert["certificate_id"])
        self.assertTrue(verify_result["verified"])

if __name__ == "__main__":
    unittest.main()
