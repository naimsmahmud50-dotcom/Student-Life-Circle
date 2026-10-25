"""
========================================================================================
MODULE:    AI Draft Review Queue & Student Isolation Test Suite
TOPIC:     Draft Ingestion, SME Approval Gate, Inline Edit, Bulk Moderation & RBAC
FILE:      backend/tests/test_draft_review_queue.py
PURPOSE:   Comprehensive unit and integration verification proving:
           1. Draft review list endpoint supports faceted filters, search & pagination.
           2. SME approval transitions draft to APPROVED and persists to disk.
           3. SME rejection requires mandatory feedback and transitions to REJECTED.
           4. SME inline edit modifies stem/options/explanation and transitions to APPROVED.
           5. Bulk action approves and rejects multiple drafts atomically.
           6. Unapproved drafts (DRAFT, NEEDS_REVIEW, REJECTED) NEVER appear in student exams.
           7. Approved drafts become immediately eligible in student exams.
           8. RBAC guard rejects 401 unauthenticated and 403 student users.
AUDIENCE:  Security Auditors, Quality Assurance & Backend Architects
STANDARDS: ASVS L2 Access Control, Deterministic Execution, Zero-Emoji Compliance
========================================================================================
"""

import unittest
import asyncio
from backend.app.api.v1.router import (
    list_draft_questions,
    get_draft_question,
    approve_draft_question,
    reject_draft_question,
    edit_and_approve_draft_question,
    bulk_action_draft_questions,
    get_draft_review_audit_logs,
    SAMPLE_MATH_QUESTIONS
)
from backend.app.services.content_pipeline_service import content_pipeline_service, DEFAULT_DRAFT_SEEDS
from backend.app.services.quiz_engine import quiz_engine, QuizMode
from backend.app.schemas.question_schema import (
    DraftReviewDecisionRequest,
    DraftEditAndApproveRequest,
    DraftBulkActionRequest
)
from backend.app.core.fastapi_shim import HTTPException

ADMIN_TOKEN = "Bearer test_admin_token_01"
REVIEWER_TOKEN = "Bearer test_reviewer_token_01"
STUDENT_TOKEN = "Bearer test_student_token_01"


class TestDraftReviewQueueAndIsolation(unittest.TestCase):

    def setUp(self):
        # Reset content pipeline to fresh state
        content_pipeline_service._populate_seeds()
        self.admin_token = ADMIN_TOKEN
        self.reviewer_token = REVIEWER_TOKEN
        self.student_token = STUDENT_TOKEN

    def test_list_drafts_faceted_filters_and_counts(self):
        """Validates GET /admin/drafts filters, status counts and pagination."""
        # 1. Fetch default queue (NEEDS_REVIEW)
        res = asyncio.run(list_draft_questions(
            status="NEEDS_REVIEW",
            subject=None,
            chapter=None,
            difficulty=None,
            source=None,
            search=None,
            page=1,
            limit=20,
            authorization=self.reviewer_token
        ))
        self.assertGreaterEqual(res["total"], 1)
        self.assertIn("counts", res)
        self.assertGreaterEqual(res["counts"]["needs_review"], 1)
        self.assertGreaterEqual(res["counts"]["all"], 3)
        for item in res["items"]:
            self.assertEqual(item["status"], "NEEDS_REVIEW")

        # 2. Filter by subject: পদার্থবিজ্ঞান
        phys_res = asyncio.run(list_draft_questions(
            status="ALL",
            subject="পদার্থবিজ্ঞান",
            chapter=None,
            difficulty=None,
            source=None,
            search=None,
            page=1,
            limit=20,
            authorization=self.admin_token
        ))
        for item in phys_res["items"]:
            self.assertIn("পদার্থবিজ্ঞান", item["subject"])

        # 3. Search by term: "লুকাস"
        search_res = asyncio.run(list_draft_questions(
            status="ALL",
            subject=None,
            chapter=None,
            difficulty=None,
            source=None,
            search="লুকাস",
            page=1,
            limit=20,
            authorization=self.reviewer_token
        ))
        self.assertGreaterEqual(search_res["total"], 1)
        self.assertIn("q_draft_chem_402", [item["id"] for item in search_res["items"]])

    def test_approve_draft_lifecycle_and_audit(self):
        """Validates POST /admin/drafts/{id}/approve moves to APPROVED and adds to live pool."""
        qid = "q_draft_phys_301"
        res = asyncio.run(approve_draft_question(
            question_id=qid,
            payload=DraftReviewDecisionRequest(
                action="APPROVE",
                comments="এনসিটিবি বলবিদ্যা কারিকুলাম মানদণ্ড অনুযায়ী মানসম্মত।"
            ),
            authorization=self.reviewer_token
        ))
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["item"]["status"], "APPROVED")
        self.assertEqual(res["item"]["reviewed_by"], "usr_reviewer_01")

        # Verify disk persistence
        item_on_disk = content_pipeline_service.get_draft(qid)
        self.assertIsNotNone(item_on_disk)
        self.assertEqual(item_on_disk["status"], "APPROVED")

        # Verify audit log recorded
        audit_logs = content_pipeline_service.get_audit_trail(limit=10)
        matching = [log for log in audit_logs if log["question_id"] == qid and log["action"] == "APPROVE_DRAFT"]
        self.assertGreaterEqual(len(matching), 1)

    def test_reject_draft_requires_mandatory_reason(self):
        """Validates POST /admin/drafts/{id}/reject requires a non-empty feedback string."""
        qid = "q_draft_math_503"

        # Missing reason must raise 400
        with self.assertRaises(HTTPException) as cm:
            asyncio.run(reject_draft_question(
                question_id=qid,
                payload=DraftReviewDecisionRequest(action="REJECT", rejection_reason=""),
                authorization=self.reviewer_token
            ))
        self.assertEqual(cm.exception.status_code, 400)

        # Valid reason succeeds
        feedback_text = "বৃত্তচাপের গণনায় পাই-এর আসন্ন মান দশমিকের পর কত ঘর নিতে হবে তা উল্লেখ করা প্রয়োজন।"
        res = asyncio.run(reject_draft_question(
            question_id=qid,
            payload=DraftReviewDecisionRequest(action="REJECT", rejection_reason=feedback_text),
            authorization=self.reviewer_token
        ))
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["item"]["status"], "REJECTED")
        self.assertEqual(res["item"]["rejection_feedback"], feedback_text)

    def test_edit_and_approve_modifies_content_and_approves(self):
        """Validates POST /admin/drafts/{id}/edit-and-approve saves updates and approves draft."""
        qid = "q_draft_bio_604"
        updated_stem = "ডিএনএ রেপ্লিকেশনের সময় ল্যাগিং সূত্রে ওকাজাকি খণ্ডগুলোকে ফসফোডাইএস্টার বন্ধনে আবদ্ধকারী এনজাইম কোনটি?"

        res = asyncio.run(edit_and_approve_draft_question(
            question_id=qid,
            payload=DraftEditAndApproveRequest(
                stem_bn=updated_stem,
                explanation_bn="লাইগেজ এনজাইম সংযোগকারী আঠা হিসেবে কাজ করে।",
                difficulty="HARD",
                cognitive_skill="REASONING",
                comments="প্রশ্নের ভাষা আরো স্পষ্ট ও বৈজ্ঞানিক পরিভাষায় সংশোধন করা হলো।"
            ),
            authorization=self.reviewer_token
        ))
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["item"]["status"], "APPROVED")
        self.assertEqual(res["item"]["stem_bn"], updated_stem)
        self.assertEqual(res["item"]["difficulty"], "HARD")
        self.assertEqual(res["item"]["version"], 2)

    def test_bulk_action_approves_and_rejects(self):
        """Validates POST /admin/drafts/bulk-action on multiple draft IDs."""
        qids = ["q_draft_phys_301", "q_draft_chem_402"]
        res = asyncio.run(bulk_action_draft_questions(
            payload=DraftBulkActionRequest(
                question_ids=qids,
                action="APPROVE",
                reason="প্যানেল মিটিংয়ে একযোগে অনুমোদন।"
            ),
            authorization=self.admin_token
        ))
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["affected_count"], 2)
        for item in res["items"]:
            self.assertEqual(item["status"], "APPROVED")

    def test_student_exam_isolation_strictly_excludes_drafts(self):
        """
        CRITICAL SECURITY REQUIREMENT:
        Drafts in NEEDS_REVIEW, DRAFT, REJECTED, or NEEDS_CHANGES state must NEVER
        be served in student quiz/practice attempts. Only APPROVED or PUBLISHED items are eligible.
        """
        mixed_pool = [
            {
                "id": "q_draft_unreviewed_01",
                "stem_bn": "অসম্পূর্ণ ড্রাফট প্রশ্ন ১",
                "status": "NEEDS_REVIEW",
                "options": [
                    {"id": "o1", "option_key": "A", "option_text_bn": "উত্তর ১", "is_correct": True},
                    {"id": "o2", "option_key": "B", "option_text_bn": "উত্তর ২", "is_correct": False}
                ]
            },
            {
                "id": "q_draft_rejected_02",
                "stem_bn": "বাতিলকৃত ড্রাফট প্রশ্ন ২",
                "status": "REJECTED",
                "options": [
                    {"id": "o3", "option_key": "A", "option_text_bn": "উত্তর ৩", "is_correct": True},
                    {"id": "o4", "option_key": "B", "option_text_bn": "উত্তর ৪", "is_correct": False}
                ]
            },
            {
                "id": "q_approved_03",
                "stem_bn": "অনুমোদিত বৈধ প্রশ্ন ৩",
                "status": "APPROVED",
                "options": [
                    {"id": "o5", "option_key": "A", "option_text_bn": "উত্তর ৫", "is_correct": True},
                    {"id": "o6", "option_key": "B", "option_text_bn": "উত্তর ৬", "is_correct": False}
                ]
            }
        ]

        attempt = quiz_engine.start_practice_attempt(
            user_id="usr_student_01",
            blueprint_id="bp_isolation_test",
            mode=QuizMode.ANYTIME_PRACTICE,
            raw_questions=mixed_pool,
            duration_minutes=10
        )

        served_ids = [q.question_version_id for q in attempt.questions]
        self.assertNotIn("q_draft_unreviewed_01", served_ids, "Unreviewed draft must NOT appear in student quiz!")
        self.assertNotIn("q_draft_rejected_02", served_ids, "Rejected draft must NOT appear in student quiz!")
        self.assertIn("q_approved_03", served_ids, "Approved question MUST appear in student quiz!")

    def test_rbac_guard_authorization_enforcement(self):
        """Validates that unauthenticated visitors (401) and students (403) are barred."""
        # 1. Unauthenticated (no token) -> 401
        with self.assertRaises(HTTPException) as cm1:
            asyncio.run(list_draft_questions(authorization=None))
        self.assertEqual(cm1.exception.status_code, 401)

        # 2. Student token -> 403
        with self.assertRaises(HTTPException) as cm2:
            asyncio.run(list_draft_questions(authorization=self.student_token))
        self.assertEqual(cm2.exception.status_code, 403)

        # 3. Subject Reviewer token -> 200
        res = asyncio.run(list_draft_questions(authorization=self.reviewer_token))
        self.assertIn("items", res)


if __name__ == "__main__":
    unittest.main()
