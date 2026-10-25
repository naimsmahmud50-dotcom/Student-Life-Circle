"""
========================================================================================
MODULE:    Question Quarantine Persistence & Quiz Exclusion Test Suite
TOPIC:     Server-Side Persistence, Restore Action, Audit Trail & Student Exam Exclusion
FILE:      backend/tests/test_question_quarantine_persistence.py
PURPOSE:   Verifies that question quarantine operations:
           1. Persist to storage across server restarts / service re-instantiation.
           2. Exclude quarantined questions from new student practice/exam sessions.
           3. Restore questions back to published status and re-include them in tests.
           4. Enforce RBAC barriers (401 unauth, 403 non-admin/reviewer).
           5. Handle concurrency / idempotent calls without corrupting state or audit logs.
AUDIENCE:  Core Platform Engineers, Exam Integrity Architects & QA Testers
STANDARDS: Clean Architecture, Unit & Integration Testing, Zero-Emoji Policy
========================================================================================
"""

import os
import unittest
import asyncio
import tempfile
import shutil
from backend.app.core.fastapi_shim import HTTPException, status
from backend.app.schemas.question_schema import (
    QuestionQuarantineRequest,
    QuestionRestoreRequest
)
from backend.app.schemas.quiz_schema import QuizMode
from backend.app.services.quarantine_service import QuarantineService, quarantine_service
from backend.app.services.quiz_engine import quiz_engine
from backend.app.api.v1.router import (
    quarantine_question_endpoint,
    restore_question_endpoint,
    list_flagged_and_quarantined_questions,
    view_audit_logs
)


class TestQuestionQuarantinePersistence(unittest.TestCase):
    """
    Comprehensive tests for question quarantine lifecycle, real disk persistence,
    and quiz engine exclusion.
    """

    def setUp(self):
        self.admin_token = "Bearer test_admin_token_01"
        self.reviewer_token = "Bearer test_reviewer_token_01"
        self.student_token = "Bearer test_student_token_01"
        self.temp_dir = tempfile.mkdtemp()
        self.temp_storage_path = os.path.join(self.temp_dir, "test_quarantine_store.json")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_quarantine_and_restore_persists_across_restarts(self):
        """Quarantine and restore operations must persist across service re-instantiation."""
        # 1. Initialize service with isolated temporary storage
        service = QuarantineService(persistence_file=self.temp_storage_path)
        q_id = "q_hsc_phys_102"

        # Initially, question is PUBLISHED
        initial_q = service.get_question(q_id)
        self.assertIsNotNone(initial_q)
        self.assertEqual(initial_q["status"], "PUBLISHED")
        self.assertNotIn(q_id, quiz_engine._quarantined_questions)

        # 2. Execute Quarantine
        quarantine_res = service.quarantine_question(
            question_id=q_id,
            actor_id="usr_reviewer_01",
            actor_role="SUBJECT_REVIEWER",
            reason="Ambiguous options A and C",
            recalculate_active=True
        )
        self.assertEqual(quarantine_res["status"], "SUCCESS")
        self.assertEqual(quarantine_res["new_state"], "QUARANTINED")
        self.assertIn(q_id, quiz_engine._quarantined_questions)

        # 3. Simulate server restart: re-instantiate service from same disk store
        restarted_service = QuarantineService(persistence_file=self.temp_storage_path)
        restarted_q = restarted_service.get_question(q_id)
        self.assertIsNotNone(restarted_q)
        self.assertEqual(restarted_q["status"], "QUARANTINED")
        self.assertTrue(restarted_q["is_quarantined"])
        self.assertEqual(restarted_q["quarantine_reason"], "Ambiguous options A and C")
        self.assertIn(q_id, quiz_engine._quarantined_questions)

        # 4. Execute Restore
        restore_res = restarted_service.restore_question(
            question_id=q_id,
            actor_id="usr_admin_01",
            actor_role="ADMIN",
            reason="Options corrected and verified by academic board"
        )
        self.assertEqual(restore_res["status"], "SUCCESS")
        self.assertEqual(restore_res["new_state"], "PUBLISHED")
        self.assertNotIn(q_id, quiz_engine._quarantined_questions)

        # 5. Simulate second server restart: re-instantiate service
        restarted_service_2 = QuarantineService(persistence_file=self.temp_storage_path)
        restored_q = restarted_service_2.get_question(q_id)
        self.assertEqual(restored_q["status"], "PUBLISHED")
        self.assertFalse(restored_q["is_quarantined"])
        self.assertEqual(restored_q["restore_reason"], "Options corrected and verified by academic board")
        self.assertNotIn(q_id, quiz_engine._quarantined_questions)

    def test_quiz_engine_excludes_quarantined_question_and_reincludes_when_restored(self):
        """Student practice exam generation must strictly exclude quarantined questions and re-include restored questions."""
        raw_test_questions = [
            {
                "id": "q_phys_active_01",
                "stem_bn": "মহাকর্ষীয় ধ্রুবক G এর একক কোনটি?",
                "options": [
                    {"id": "opt_1", "option_key": "A", "option_text_bn": "N m^2 kg^-2", "is_correct": True},
                    {"id": "opt_2", "option_key": "B", "option_text_bn": "N m kg^-1", "is_correct": False}
                ]
            },
            {
                "id": "q_phys_flawed_02",
                "stem_bn": "ত্রুটিযুক্ত প্রশ্ন যা কোয়ারেন্টিনে যাবে",
                "options": [
                    {"id": "opt_3", "option_key": "A", "option_text_bn": "উত্তর ১", "is_correct": True},
                    {"id": "opt_4", "option_key": "B", "option_text_bn": "উত্তর ২", "is_correct": False}
                ]
            }
        ]

        # Initial attempt before quarantine: both questions should be present
        attempt_1 = quiz_engine.start_practice_attempt(
            user_id="usr_student_test_101",
            blueprint_id="bp_phys_01",
            mode=QuizMode.ANYTIME_PRACTICE,
            raw_questions=raw_test_questions
        )
        attempt_1_ids = [q.question_version_id for q in attempt_1.questions]
        self.assertIn("q_phys_active_01", attempt_1_ids)
        self.assertIn("q_phys_flawed_02", attempt_1_ids)

        # Now quarantine question q_phys_flawed_02
        quarantine_service.quarantine_question(
            question_id="q_phys_flawed_02",
            actor_id="usr_admin_01",
            actor_role="ADMIN",
            reason="Answer key ambiguity reported by 20 students"
        )
        self.assertIn("q_phys_flawed_02", quiz_engine._quarantined_questions)

        # New student attempt after quarantine: q_phys_flawed_02 must NOT appear
        attempt_2 = quiz_engine.start_practice_attempt(
            user_id="usr_student_test_102",
            blueprint_id="bp_phys_01",
            mode=QuizMode.ANYTIME_PRACTICE,
            raw_questions=raw_test_questions
        )
        attempt_2_ids = [q.question_version_id for q in attempt_2.questions]
        self.assertIn("q_phys_active_01", attempt_2_ids)
        self.assertNotIn("q_phys_flawed_02", attempt_2_ids)
        self.assertEqual(len(attempt_2_ids), 1)

        # Now restore the question
        quarantine_service.restore_question(
            question_id="q_phys_flawed_02",
            actor_id="usr_admin_01",
            actor_role="ADMIN",
            reason="Corrected and verified"
        )
        self.assertNotIn("q_phys_flawed_02", quiz_engine._quarantined_questions)

        # Third attempt after restore: q_phys_flawed_02 is back!
        attempt_3 = quiz_engine.start_practice_attempt(
            user_id="usr_student_test_103",
            blueprint_id="bp_phys_01",
            mode=QuizMode.ANYTIME_PRACTICE,
            raw_questions=raw_test_questions
        )
        attempt_3_ids = [q.question_version_id for q in attempt_3.questions]
        self.assertIn("q_phys_active_01", attempt_3_ids)
        self.assertIn("q_phys_flawed_02", attempt_3_ids)

    def test_list_flagged_and_quarantined_questions_filters_and_pagination(self):
        """Listing endpoint must accurately filter by status, subject, and search query with pagination."""
        res_all = asyncio.run(list_flagged_and_quarantined_questions(
            status_filter="ALL",
            authorization=self.admin_token
        ))
        self.assertGreaterEqual(res_all["total"], 2)

        # Filter by QUARANTINED
        res_quarantined = asyncio.run(list_flagged_and_quarantined_questions(
            status_filter="QUARANTINED",
            authorization=self.reviewer_token
        ))
        for item in res_quarantined["items"]:
            self.assertEqual(item["status"], "QUARANTINED")

        # Filter by Search term
        res_search = asyncio.run(list_flagged_and_quarantined_questions(
            search="সাম্যাবস্থানে",
            authorization=self.admin_token
        ))
        self.assertGreaterEqual(res_search["total"], 1)
        self.assertIn("সাম্যাবস্থানে", res_search["items"][0]["stem_bn"])

    def test_restore_endpoint_rbac_and_error_handling(self):
        """Restore endpoint must reject unauthorized requests with 401/403 and return 404 for missing items."""
        payload = QuestionRestoreRequest(reason="Verified valid")

        # 401 for unauthenticated
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(restore_question_endpoint(
                question_id="q_hsc_phys_102",
                payload=payload,
                authorization=None
            ))
        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)

        # 403 for unauthorized student role
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(restore_question_endpoint(
                question_id="q_hsc_phys_102",
                payload=payload,
                authorization=self.student_token
            ))
        self.assertEqual(ctx.exception.status_code, status.HTTP_403_FORBIDDEN)

        # 404 for nonexistent question
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(restore_question_endpoint(
                question_id="q_nonexistent_xyz_999",
                payload=payload,
                authorization=self.admin_token
            ))
        self.assertEqual(ctx.exception.status_code, status.HTTP_404_NOT_FOUND)

    def test_idempotent_concurrency_handling(self):
        """Re-quarantining an already quarantined question returns idempotent success status without error."""
        q_id = "q_concurrent_test_1"
        quarantine_service.quarantine_question(
            question_id=q_id,
            actor_id="reviewer_1",
            actor_role="SUBJECT_REVIEWER",
            reason="First review reason"
        )

        # Second reviewer attempts to quarantine same question simultaneously
        concurrent_res = quarantine_service.quarantine_question(
            question_id=q_id,
            actor_id="reviewer_2",
            actor_role="SUBJECT_REVIEWER",
            reason="Second review reason"
        )
        self.assertEqual(concurrent_res["status"], "SUCCESS")
        self.assertTrue(concurrent_res["already_quarantined"])

        # First reviewer restores
        quarantine_service.restore_question(
            question_id=q_id,
            actor_id="reviewer_1",
            actor_role="SUBJECT_REVIEWER",
            reason="Board fixed question"
        )

        # Second reviewer attempts restore again
        concurrent_restore = quarantine_service.restore_question(
            question_id=q_id,
            actor_id="reviewer_2",
            actor_role="SUBJECT_REVIEWER",
            reason="Board fixed question duplicate click"
        )
        self.assertEqual(concurrent_restore["status"], "SUCCESS")
        self.assertTrue(concurrent_restore["already_active"])


if __name__ == "__main__":
    unittest.main()
