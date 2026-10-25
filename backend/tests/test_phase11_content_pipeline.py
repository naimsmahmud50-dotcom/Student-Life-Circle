"""
========================================================================================
MODULE:    Automated Verification Test Suite - Phase 11 Content Pipeline & Bug Fixes
TOPIC:     AI Draft Generation, SME Review State Machine, Publishing & True Negative Scoring
FILE:      backend/tests/test_phase11_content_pipeline.py
PURPOSE:   Verifies:
           1. AI question generation enforces DRAFT status and includes pedagogical distractors.
           2. Human Subject Matter Expert (SME) approval gate strictly blocks unreviewed AI.
           3. Lifecycle state machine: DRAFT -> NEEDS_REVIEW -> APPROVED -> PUBLISHED.
           4. Rejection flow returning flawed questions back to DRAFT with feedback.
           5. Admission negative marking scoring regression test allowing true net negative scores.
           6. REST API routes for AI content drafting, review queuing, and publishing.
AUDIENCE:  QA Engineers, AI Architects & CI/CD Pipelines
STANDARDS: Zero Regressions, TDD Red-Green-Refactor, ASVS L2 Content Governance
========================================================================================
"""

import asyncio
import unittest
from backend.app.services.content_pipeline_service import ContentPipelineService
from backend.app.services.quiz_engine import QuizEngineService, QuizMode
from backend.app.api.v1.router import (
    generate_ai_question_draft,
    submit_question_for_review,
    get_sme_review_queue,
    review_and_decide_question,
    publish_approved_question
)
from backend.app.schemas.live_and_admission_schema import (
    AIDraftGenerateRequest,
    SMEReviewDecisionRequest
)


class TestPhase11ContentPipeline(unittest.TestCase):
    """
    Test suite for AI content drafting, SME review lifecycle, and negative scoring regression.
    """

    def setUp(self):
        self.pipeline_service = ContentPipelineService()
        self.quiz_engine = QuizEngineService()

    def test_01_ai_draft_generation_and_distractor_structure(self):
        """Verifies AI draft generates valid distractors and enforces DRAFT state."""
        draft = self.pipeline_service.generate_ai_draft(
            subject="পদার্থবিজ্ঞান ১ম পত্র",
            topic="গতিবিদ্যা ও বলবিদ্যা",
            concept="সুষম ত্বরণে অতিক্রান্ত দূরত্ব",
            class_grade=10
        )
        self.assertEqual(draft["status"], "DRAFT")
        self.assertTrue(draft["is_ai_generated"])
        self.assertGreaterEqual(len(draft["options"]), 4)
        
        # Verify distractors include rationale and exactly one correct answer
        correct_options = [opt for opt in draft["options"] if opt["is_correct"]]
        self.assertEqual(len(correct_options), 1)
        self.assertIn("distractor_rationale", draft["options"][0])

    def test_02_human_sme_approval_gate_and_state_machine(self):
        """Verifies strict state machine transitions and blocks unreviewed publication."""
        draft = self.pipeline_service.generate_ai_draft(
            subject="রসায়ন ১ম পত্র",
            topic="গুণগত রসায়ন",
            concept="কোয়ান্টাম সংখ্যা"
        )
        q_id = draft["id"]

        # Attempt to publish directly from DRAFT must be rejected
        pub_ok, reason = self.pipeline_service.publish_approved_question(q_id, publisher_id="admin_01")
        self.assertFalse(pub_ok)
        self.assertIn("CANNOT_PUBLISH_UNAPPROVED_QUESTION", reason)

        # Transition to NEEDS_REVIEW
        submit_ok, submit_reason = self.pipeline_service.submit_for_sme_review(q_id)
        self.assertTrue(submit_ok)
        self.assertEqual(draft["status"], "NEEDS_REVIEW")

        # SME approves question
        app_ok, app_reason, item = self.pipeline_service.review_and_approve_draft(
            question_id=q_id,
            sme_user_id="sme_reviewer_01",
            approve=True
        )
        self.assertTrue(app_ok)
        self.assertEqual(item["status"], "APPROVED")
        self.assertEqual(item["reviewed_by_sme_id"], "sme_reviewer_01")

        # Now question can be published to active pools
        pub_ok, pub_reason = self.pipeline_service.publish_approved_question(q_id, publisher_id="admin_01")
        self.assertTrue(pub_ok)
        self.assertEqual(item["status"], "PUBLISHED")

    def test_03_sme_rejection_returns_to_draft_with_feedback(self):
        """Verifies that SME rejection returns question to DRAFT with actionable feedback."""
        draft = self.pipeline_service.generate_ai_draft(
            subject="উচ্চতর গণিত",
            topic="ত্রিকোণমিতি",
            concept="যৌগিক কোণ"
        )
        q_id = draft["id"]
        self.pipeline_service.submit_for_sme_review(q_id)

        rej_ok, rej_reason, item = self.pipeline_service.review_and_approve_draft(
            question_id=q_id,
            sme_user_id="sme_math_01",
            approve=False,
            rejection_reason="অপশন C এবং D এর গাণিতিক মানে মুদ্রণ ত্রুটি রয়েছে।"
        )
        self.assertTrue(rej_ok)
        self.assertEqual(item["status"], "DRAFT")
        self.assertIn("মুদ্রণ ত্রুটি", item["rejection_feedback"])

    def test_04_admission_mock_true_negative_score_regression(self):
        """
        Regression Test for Bug: admission-negative-scoring
        Proves that competitive admission mocks reflect true net negative score
        and do not clamp to 0.0 when penalties exceed correct marks.
        """
        # Create 10-question mock test attempt with negative marking = 0.25
        raw_questions = [
            {
                "id": f"q_neg_{i}",
                "stem_bn": f"টেস্ট প্রশ্ন {i}",
                "options": [
                    {"id": f"opt_{i}_a", "option_key": "A", "option_text_bn": "সঠিক", "is_correct": True},
                    {"id": f"opt_{i}_b", "option_key": "B", "option_text_bn": "ভুল", "is_correct": False},
                ]
            }
            for i in range(10)
        ]

        attempt = self.quiz_engine.start_practice_attempt(
            user_id="std_admission_candidate",
            blueprint_id="bp_du_unit_a",
            mode=QuizMode.MOCK_EXAM,
            raw_questions=raw_questions,
            duration_minutes=15,
            negative_marking=0.25
        )
        attempt_id = attempt.attempt_id

        # Candidate answers 1 question correctly (Question 0)
        self.quiz_engine.save_answer_idempotent(
            attempt_id=attempt_id,
            user_id="std_admission_candidate",
            question_version_id="q_neg_0",
            selected_option_id="opt_0_a",  # Correct (+1.0)
            idempotency_key="key_01"
        )

        # Candidate answers 8 questions incorrectly (Questions 1 to 8: 8 * -0.25 = -2.0)
        for i in range(1, 9):
            self.quiz_engine.save_answer_idempotent(
                attempt_id=attempt_id,
                user_id="std_admission_candidate",
                question_version_id=f"q_neg_{i}",
                selected_option_id=f"opt_{i}_b",  # Incorrect
                idempotency_key=f"key_{i}"
            )
        # Question 9 is left unanswered (0 penalty)

        # Submit and score
        success, result, reason = self.quiz_engine.submit_and_score(
            attempt_id=attempt_id,
            user_id="std_admission_candidate"
        )
        self.assertTrue(success)
        self.assertEqual(result.correct_count, 1)
        self.assertEqual(result.incorrect_count, 8)
        self.assertEqual(result.unanswered_count, 1)
        # Score calculation: 1 * 1.0 - 8 * 0.25 = 1.0 - 2.0 = -1.0
        self.assertEqual(result.raw_score, -1.0, "Admission mock score must NOT be clamped to 0.0!")

    def test_05_api_router_ai_content_pipeline_endpoints(self):
        """Verifies end-to-end REST router endpoints for AI drafting, review, and publishing."""
        admin_auth = "Bearer test_admin_token_01"

        # 1. Generate AI Draft via API
        draft_payload = AIDraftGenerateRequest(
            subject="পদার্থবিজ্ঞান ১ম পত্র",
            topic="গতিবিদ্যা",
            concept="নিউটনের বলবিদ্যার সূত্রাবলী"
        )
        draft_res = asyncio.run(generate_ai_question_draft(
            payload=draft_payload,
            admin_id="usr_admin_01",
            authorization=admin_auth
        ))
        self.assertEqual(draft_res["status"], "SUCCESS")
        q_id = draft_res["question_id"]
        self.assertEqual(draft_res["lifecycle_state"], "DRAFT")

        # 2. Submit for review via API
        submit_res = asyncio.run(submit_question_for_review(
            question_id=q_id,
            authorization=admin_auth
        ))
        self.assertEqual(submit_res["status"], "QUEUED")

        # 3. View review queue via API
        queue_res = asyncio.run(get_sme_review_queue(
            status_filter="NEEDS_REVIEW",
            authorization=admin_auth
        ))
        self.assertGreaterEqual(queue_res["total_pending"], 1)

        # 4. SME approves via API
        decision_payload = SMEReviewDecisionRequest(approve=True)
        decision_res = asyncio.run(review_and_decide_question(
            question_id=q_id,
            payload=decision_payload,
            sme_id="usr_sme_expert_01",
            authorization=admin_auth
        ))
        self.assertEqual(decision_res["status"], "SUCCESS")
        self.assertEqual(decision_res["new_state"], "APPROVED")

        # 5. Publish via API
        publish_res = asyncio.run(publish_approved_question(
            question_id=q_id,
            publisher_id="usr_admin_01",
            authorization=admin_auth
        ))
        self.assertEqual(publish_res["status"], "SUCCESS")


if __name__ == "__main__":
    unittest.main()
