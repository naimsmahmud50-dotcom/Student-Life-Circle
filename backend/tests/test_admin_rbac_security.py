"""
========================================================================================
MODULE:    Admin Panel Server-Side RBAC & Security Test Suite
TOPIC:     Strict 401 vs 403 HTTP Separation, Session Verification & Role Authorization
FILE:      backend/tests/test_admin_rbac_security.py
PURPOSE:   Verifies zero-trust defense-in-depth protection for all administrative API routes.
           Guarantees that unauthenticated access receives 401 Unauthorized, unauthorized
           roles (such as students) receive 403 Forbidden, subject reviewers are scoped to
           review/quarantine actions, and only full administrators can execute production
           publishing.
AUDIENCE:  Security Engineers, Lead Backend Architects & Penetration Testers
STANDARDS: OWASP ASVS L2, Zero-Trust Architecture, Zero-Emoji Strict Compliance
========================================================================================
"""

import unittest
import asyncio
from backend.app.core.fastapi_shim import HTTPException, status
from backend.app.services.auth_service import auth_service
from backend.app.models.user import UserRoleEnum
from backend.app.schemas.question_schema import QuestionQuarantineRequest
from backend.app.schemas.live_and_admission_schema import (
    AIDraftGenerateRequest,
    SMEReviewDecisionRequest
)
from backend.app.api.v1.router import (
    quarantine_question_endpoint,
    view_audit_logs,
    generate_ai_question_draft,
    submit_question_for_review,
    get_sme_review_queue,
    review_and_decide_question,
    publish_approved_question
)


class TestAdminRBACSecurity(unittest.TestCase):
    """
    Exhaustive security audit tests verifying strict RBAC enforcement across administrative routes.
    """

    def setUp(self):
        # Tokens seeded by default in AuthService
        self.admin_token = "Bearer test_admin_token_01"
        self.reviewer_token = "Bearer test_reviewer_token_01"
        self.student_token = "Bearer test_student_token_01"

    def test_missing_authorization_header_returns_401(self):
        """Unauthenticated requests without Authorization header must strictly fail with 401."""
        payload = QuestionQuarantineRequest(
            reason="Ambiguous options in physics question",
            recalculate_active_sessions=True
        )

        # 1. Quarantine Endpoint
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(quarantine_question_endpoint(
                question_id="qst_physics_101",
                payload=payload,
                authorization=None
            ))
        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("অথরাইজেশন হেডার অনুপস্থিত", ctx.exception.detail)

        # 2. Audit Logs Endpoint
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(view_audit_logs(authorization=None))
        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)

        # 3. Review Queue Endpoint
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(get_sme_review_queue(authorization=None))
        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)

        # 4. Content Publish Endpoint
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(publish_approved_question(
                question_id="qst_chem_201",
                authorization=None
            ))
        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_or_malformed_token_returns_401(self):
        """Tampered or invalid Bearer tokens must be rejected with 401."""
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(view_audit_logs(authorization="Bearer completely_bogus_token_xyz"))
        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("সেশন মেয়াদোত্তীর্ণ বা অকার্যকর", ctx.exception.detail)

    def test_expired_session_token_returns_401(self):
        """Expired sessions must be rejected with 401 and cleaned up immediately."""
        temp_token = "test_expiring_token_999"
        auth_service._sessions[temp_token] = {
            "user_id": "usr_admin_01",
            "roles": [UserRoleEnum.ADMIN.value],
            "expires_at": "2020-01-01T00:00:00+00:00"
        }

        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(view_audit_logs(authorization=f"Bearer {temp_token}"))
        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        # Token must have been cleaned up from active session store
        self.assertNotIn(temp_token, auth_service._sessions)

    def test_revoked_session_after_logout_returns_401(self):
        """Logged-out sessions must be immediately barred from admin endpoints."""
        temp_token = "test_transient_token_888"
        auth_service._sessions[temp_token] = {
            "user_id": "usr_admin_01",
            "roles": [UserRoleEnum.ADMIN.value]
        }

        # Valid prior to logout
        result = asyncio.run(view_audit_logs(authorization=f"Bearer {temp_token}"))
        self.assertIn("records", result)

        # Logout / Revocation
        revoked = auth_service.logout_session(temp_token)
        self.assertTrue(revoked)

        # Barred after logout
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(view_audit_logs(authorization=f"Bearer {temp_token}"))
        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_student_role_attempting_admin_access_returns_403_forbidden(self):
        """Authenticated student must receive strict 403 Forbidden on any admin endpoint."""
        payload = QuestionQuarantineRequest(
            reason="Student attempt to tamper question state",
            recalculate_active_sessions=False
        )

        # 1. Student attempting quarantine
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(quarantine_question_endpoint(
                question_id="qst_bio_301",
                payload=payload,
                authorization=self.student_token
            ))
        self.assertEqual(ctx.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("অননুমোদিত প্রবেশাধিকার", ctx.exception.detail)

        # 2. Student attempting to view audit logs
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(view_audit_logs(authorization=self.student_token))
        self.assertEqual(ctx.exception.status_code, status.HTTP_403_FORBIDDEN)

        # 3. Student attempting to publish content
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(publish_approved_question(
                question_id="qst_bio_301",
                authorization=self.student_token
            ))
        self.assertEqual(ctx.exception.status_code, status.HTTP_403_FORBIDDEN)

    def test_subject_reviewer_access_quarantine_and_review_succeeds_200(self):
        """Subject reviewer must successfully access quarantine, review queue, and audit logs."""
        payload = QuestionQuarantineRequest(
            reason="Incorrect formula in option B",
            recalculate_active_sessions=True
        )

        # Reviewer can quarantine
        res = asyncio.run(quarantine_question_endpoint(
            question_id="qst_phys_404",
            payload=payload,
            authorization=self.reviewer_token
        ))
        self.assertEqual(res["new_state"], "QUARANTINED")
        self.assertEqual(res["status"], "SUCCESS")

        # Reviewer can view audit trail
        logs = asyncio.run(view_audit_logs(authorization=self.reviewer_token))
        self.assertIsInstance(logs["records"], list)
        self.assertGreaterEqual(logs["total_records"], 1)

        # Reviewer can view review queue
        queue = asyncio.run(get_sme_review_queue(authorization=self.reviewer_token))
        self.assertIn("items", queue)

    def test_subject_reviewer_attempting_publish_returns_403_forbidden(self):
        """Subject reviewer must NOT be able to publish live content; only full ADMIN may publish."""
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(publish_approved_question(
                question_id="qst_live_release_01",
                authorization=self.reviewer_token
            ))
        self.assertEqual(ctx.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("আবশ্যক রোল ['ADMIN']", ctx.exception.detail)

    def test_full_admin_can_perform_all_operations(self):
        """Full administrator must have authorized access across all operations."""
        # 1. Draft AI Question
        draft_req = AIDraftGenerateRequest(
            subject="Physics",
            topic="Thermodynamics",
            concept="First Law",
            cognitive_level="APPLY",
            curriculum="NCTB-2024",
            class_grade=11
        )
        draft_res = asyncio.run(generate_ai_question_draft(
            payload=draft_req,
            authorization=self.admin_token
        ))
        self.assertEqual(draft_res["status"], "SUCCESS")
        qid = draft_res["question_id"]

        # 2. Submit for review
        submit_res = asyncio.run(submit_question_for_review(
            question_id=qid,
            authorization=self.admin_token
        ))
        self.assertEqual(submit_res["status"], "QUEUED")

        # 3. Review and approve
        dec_req = SMEReviewDecisionRequest(approve=True)
        dec_res = asyncio.run(review_and_decide_question(
            question_id=qid,
            payload=dec_req,
            authorization=self.admin_token
        ))
        self.assertEqual(dec_res["status"], "SUCCESS")

        # 4. Publish
        pub_res = asyncio.run(publish_approved_question(
            question_id=qid,
            authorization=self.admin_token
        ))
        self.assertEqual(pub_res["status"], "SUCCESS")

    def test_audit_log_captures_authenticated_actor_identity(self):
        """Audit trail must immutably log the authenticated user ID and role, preventing actor spoofing."""
        payload = QuestionQuarantineRequest(
            reason="Typo in stem statement",
            recalculate_active_sessions=False
        )

        asyncio.run(quarantine_question_endpoint(
            question_id="qst_chem_505",
            payload=payload,
            authorization=self.reviewer_token
        ))

        audit_res = asyncio.run(view_audit_logs(authorization=self.admin_token))
        last_entry = audit_res["records"][-1]

        self.assertEqual(last_entry["entity_id"], "qst_chem_505")
        self.assertEqual(last_entry["actor_id"], "usr_reviewer_01")
        self.assertEqual(last_entry["actor_role"], UserRoleEnum.SUBJECT_REVIEWER.value)


if __name__ == "__main__":
    unittest.main()
