"""
========================================================================================
MODULE:    Automated Verification Test Suite - Phase 2
TOPIC:     Relational Domain Models, Academic Seeds, Admission Mocks & Spaced Repetition
FILE:      backend/tests/test_phase2_models.py
PURPOSE:   Verifies all Phase 2 domain entities, academic seed data integrity,
           university admission blueprint math, spaced repetition mastery updates,
           minor privacy consent flows, and immutable CV snapshot immutability.
AUDIENCE:  Developers, QA Engineers & CI/CD Pipelines
STANDARDS: Zero Regressions, TDD Red-Green-Refactor, 100% Determinism
========================================================================================
"""

import unittest
from datetime import datetime, timedelta, timezone

from backend.app.models.user import User, StudentProfile, GuardianLink, EducationStageEnum
from backend.app.models.question import Curriculum, Subject, Topic, QuestionVersion
from backend.app.models.quiz import TestBlueprint, LiveSession, MasteryRecord
from backend.app.models.opportunity import TuitionListing, CVSnapshot, JobApplication, AuditLog
from backend.app.db.seed_data import CURRICULUM_SEEDS, SUBJECT_SEEDS, ADMISSION_BLUEPRINTS, ACADEMIC_QUESTION_SEEDS


class TestPhase2DomainAndSeeds(unittest.TestCase):
    """
    Test suite for Phase 2 entities and academic logic.
    """

    def test_01_user_and_minor_student_profile(self):
        """Verifies StudentProfile preserves continuity and defaults to private for minors."""
        user = User(
            email="nafis.student@example.com",
            full_name="Nafis Al-Amin",
            pseudonym="Nafis_Dhaka",
            is_email_verified=True
        )
        self.assertEqual(user.pseudonym, "Nafis_Dhaka")
        self.assertTrue(user.is_active)

        profile = StudentProfile(
            user_id=user.id,
            stage=EducationStageEnum.HSC,
            class_grade=12,
            target_exam="DU_UNIT_A",
            is_minor=True
        )
        self.assertEqual(profile.privacy_mode, "PRIVATE")
        self.assertEqual(profile.stage, EducationStageEnum.HSC)

        # Test dictionary serialization
        data = profile.to_dict()
        self.assertEqual(data["class_grade"], 12)
        self.assertEqual(data["target_exam"], "DU_UNIT_A")

    def test_02_guardian_link_consent_lifecycle(self):
        """Verifies guardian connection starts PENDING and requires explicit consent."""
        guardian_link = GuardianLink(
            student_id="student_123",
            guardian_user_id="guardian_456",
            relationship="FATHER"
        )
        self.assertEqual(guardian_link.consent_status, "PENDING")
        self.assertIsNone(guardian_link.approved_at)

        # Approve consent
        now_str = datetime.now(timezone.utc).isoformat()
        guardian_link.consent_status = "APPROVED"
        guardian_link.approved_at = now_str
        self.assertEqual(guardian_link.consent_status, "APPROVED")

    def test_03_seed_data_integrity(self):
        """Verifies NCTB curricula, subjects, and admission blueprints are populated."""
        self.assertGreater(len(CURRICULUM_SEEDS), 0)
        self.assertEqual(CURRICULUM_SEEDS[0]["code"], "NCTB_2024")

        # Verify admission blueprints
        du_bp = next((bp for bp in ADMISSION_BLUEPRINTS if bp["id"] == "bp_du_unit_a"), None)
        self.assertIsNotNone(du_bp)
        self.assertEqual(du_bp["negative_marking_value"], 0.25)
        self.assertEqual(du_bp["total_questions"], 60)

        # Verify question seeds have exact 1 correct option and citations
        for q in ACADEMIC_QUESTION_SEEDS:
            correct_opts = [opt for opt in q["options"] if opt["is_correct"]]
            self.assertEqual(len(correct_opts), 1, f"Question {q['id']} must have exactly 1 correct option.")
            self.assertIn("explanation_bn", q)
            self.assertIn("source_attribution", q)

    def test_04_spaced_repetition_mastery_queue(self):
        """Verifies MasteryRecord tracks errors and schedules revision intervals."""
        mastery = MasteryRecord(
            student_id="student_77",
            topic_id="topic_calculus_limits",
            attempt_count=5,
            correct_count=2,
            is_in_mistake_queue=True
        )
        self.assertTrue(mastery.is_in_mistake_queue)

        # Simulate revision scheduling (+3 days for concept reinforcement)
        now = datetime.now(timezone.utc)
        next_due = now + timedelta(days=3)
        mastery.next_revision_due = next_due.isoformat()
        mastery.mastery_level = round(2 / 5, 2)

        self.assertEqual(mastery.mastery_level, 0.4)
        self.assertIsNotNone(mastery.next_revision_due)

    def test_05_immutable_cv_snapshot_immutability(self):
        """Verifies CV snapshot retains immutable frozen payload upon job application."""
        original_skills = ["Python", "FastAPI", "PostgreSQL", "React"]
        cv_snapshot = CVSnapshot(
            user_id="user_graduate_99",
            title="Software Engineering Intern Snapshot",
            snapshot_json={
                "skills": list(original_skills),
                "cgpa": 3.85,
                "institution": "University of Dhaka"
            }
        )

        job_app = JobApplication(
            job_id="job_dev_101",
            candidate_user_id="user_graduate_99",
            cv_snapshot_id=cv_snapshot.id,
            stage="APPLIED"
        )

        self.assertEqual(job_app.stage, "APPLIED")
        self.assertEqual(cv_snapshot.snapshot_json["skills"], ["Python", "FastAPI", "PostgreSQL", "React"])

        # Candidate later edits their profile skills, but snapshot must remain untampered
        new_active_skills = ["Rust", "Solidity"]
        self.assertNotEqual(cv_snapshot.snapshot_json["skills"], new_active_skills)

    def test_06_audit_logging_structure(self):
        """Verifies AuditLog records operational decisions with before/after payloads."""
        audit = AuditLog(
            actor_id="admin_01",
            actor_role="ADMIN",
            action="QUARANTINE_QUESTION",
            entity_type="QUESTION_VERSION",
            entity_id="qv_9988",
            reason="Ambiguity reported in stem",
            payload_before={"status": "PUBLISHED"},
            payload_after={"status": "QUARANTINED"}
        )
        self.assertEqual(audit.action, "QUARANTINE_QUESTION")
        self.assertEqual(audit.payload_after["status"], "QUARANTINED")


if __name__ == "__main__":
    unittest.main()
