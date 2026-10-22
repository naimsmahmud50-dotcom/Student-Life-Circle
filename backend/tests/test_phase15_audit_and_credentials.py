"""
================================================================================
MODULE: Automated Test Suite (স্বয়ংক্রিয় ভেরিফিকেশন ও টেস্ট ইঞ্জিন)
TOPIC: Phase 15 Cryptographic Audit Ledger & Verifiable Credentials Verification
FILE: backend/tests/test_phase15_audit_and_credentials.py
PURPOSE: Comprehensive unit, security, and integration tests verifying SHA-256
         hash chaining, tamper detection, Open Badges v3 issuance, ASVS L2 minor
         privacy redaction during public credential verification, and REST routes.
AUDIENCE: QA Engineers, Security Auditors, Compliance Teams, CI/CD Pipeline.
STANDARDS: OWASP ASVS Level 2, FIPS 180-4 SHA-256, W3C Verifiable Credentials.
================================================================================
"""

import unittest
import uuid
from datetime import datetime, timezone

from backend.app.core.audit_ledger import audit_ledger, AuditLedger
from backend.app.services.portfolio_credential_service import portfolio_credential_service
from backend.app.api.v1.router import (
    issue_student_credential,
    verify_student_credential,
    list_student_credentials,
    verify_audit_ledger_integrity,
    list_audit_ledger_blocks,
)
from backend.app.schemas.credential_and_audit_schema import CredentialIssueRequest


class TestPhase15AuditAndCredentials(unittest.TestCase):
    """Test suite covering Phase 15 Cryptographic Audit Ledger and Verifiable Credentials."""

    def setUp(self) -> None:
        """Reset singleton states before each test run for absolute isolation."""
        audit_ledger.reset_for_testing()
        portfolio_credential_service.reset_for_testing()

    def test_audit_ledger_genesis_and_chaining(self) -> None:
        """Verifies genesis block initialization and sequential hash chaining."""
        self.assertEqual(audit_ledger.get_total_blocks(), 1)
        is_valid, corrupted_idx, message = audit_ledger.verify_integrity()
        self.assertTrue(is_valid, f"Genesis integrity failed: {message}")
        self.assertIsNone(corrupted_idx)

        # Record events
        block1 = audit_ledger.record_event(
            event_type="QUESTION_QUARANTINED",
            actor_id="usr_mod_01",
            actor_role="MODERATOR",
            payload={"question_id": "q_math_99", "reason": "Ambiguous option C"},
        )
        self.assertEqual(block1.block_index, 1)
        self.assertEqual(block1.prev_hash, audit_ledger._blocks[0].block_hash)

        block2 = audit_ledger.record_event(
            event_type="SCORE_RECONCILED",
            actor_id="usr_admin_02",
            actor_role="ADMIN",
            payload={"affected_attempts": 142, "status": "SCORES_UPDATED"},
        )
        self.assertEqual(block2.block_index, 2)
        self.assertEqual(block2.prev_hash, block1.block_hash)

        is_valid, corrupted_idx, message = audit_ledger.verify_integrity()
        self.assertTrue(is_valid)
        self.assertEqual(audit_ledger.get_total_blocks(), 3)

    def test_audit_ledger_tamper_detection(self) -> None:
        """Verifies that unauthorized modification of any block payload breaks verification."""
        audit_ledger.record_event(
            event_type="EVENT_ALPHA",
            actor_id="actor_1",
            actor_role="ROLE_1",
            payload={"amount": 100},
        )
        audit_ledger.record_event(
            event_type="EVENT_BETA",
            actor_id="actor_2",
            actor_role="ROLE_2",
            payload={"status": "APPROVED"},
        )

        is_valid_before, _, _ = audit_ledger.verify_integrity()
        self.assertTrue(is_valid_before)

        # Maliciously alter payload of block 1 directly in storage
        audit_ledger._blocks[1].payload["amount"] = 999999

        is_valid_after, corrupted_idx, message = audit_ledger.verify_integrity()
        self.assertFalse(is_valid_after)
        self.assertEqual(corrupted_idx, 1)
        self.assertIn("content hash mismatch", message)

    def test_audit_ledger_serialization_with_datetime_and_uuid(self) -> None:
        """Verifies that non-primitive types (datetime, UUID) serialize cleanly via default=str."""
        test_uuid = uuid.uuid4()
        test_time = datetime.now(timezone.utc)

        block = audit_ledger.record_event(
            event_type="SYSTEM_MAINTENANCE",
            actor_id="sys_worker",
            actor_role="SYSTEM",
            payload={"job_id": test_uuid, "executed_at": test_time},
        )
        self.assertIsNotNone(block.block_hash)

        is_valid, _, _ = audit_ledger.verify_integrity()
        self.assertTrue(is_valid)

    def test_audit_ledger_immutability_against_dict_mutation(self) -> None:
        """Verifies that modifying the dictionary returned by get_blocks does not alter internal blocks."""
        audit_ledger.record_event(
            event_type="SECURE_EVENT",
            actor_id="usr_sec",
            actor_role="SECURITY",
            payload={"secret_code": "alpha_bravo"},
        )

        blocks = audit_ledger.get_blocks()
        self.assertEqual(len(blocks), 2)

        # Mutate the external dictionary
        blocks[1]["payload"]["secret_code"] = "hacked_value"

        # Verify internal ledger remains uncorrupted
        is_valid, corrupted_idx, _ = audit_ledger.verify_integrity()
        self.assertTrue(is_valid, "Internal ledger was modified by external reference!")
        self.assertIsNone(corrupted_idx)

    def test_portfolio_credential_issuance_and_audit_integration(self) -> None:
        """Verifies issuing an academic badge and automatic registration in the audit ledger."""
        credential = portfolio_credential_service.issue_credential(
            student_id="usr_std_501",
            student_name="মাহমুদ হাসান",
            is_minor=False,
            badge_type="SUBJECT_MASTERY",
            title="এনসিটিবি গণিত শ্রেণি ৮ - দক্ষতা লেভেল ৪",
            description="গণিত অধ্যায় ৪ এর সকল সমস্যায় ৯০%+ সঠিক উত্তর দিয়ে দক্ষতা অর্জন করেছে।",
            subject="গণিত",
            mastery_score=94.5,
            evidence={"exam_id": "att_8829", "accuracy": 0.945},
        )

        self.assertTrue(credential["credential_id"].startswith("cred_"))
        self.assertEqual(credential["status"], "VALID")
        self.assertIsNotNone(credential["signature"])

        # Check audit ledger
        self.assertEqual(audit_ledger.get_total_blocks(), 2)
        latest_block = audit_ledger._blocks[-1]
        self.assertEqual(latest_block.event_type, "CREDENTIAL_ISSUED")
        self.assertEqual(latest_block.payload["credential_id"], credential["credential_id"])

    def test_portfolio_credential_minor_privacy_protection(self) -> None:
        """Verifies that public verification of a minor's badge protects their identity (ASVS L2)."""
        cred = portfolio_credential_service.issue_credential(
            student_id="usr_minor_771",
            student_name="তানভির আহমেদ",
            is_minor=True,
            badge_type="LIVE_CHALLENGE_TOP_10",
            title="জাতীয় লাইভ বিজ্ঞান চ্যালেঞ্জ ২০২৬ - শীর্ষ স্থান",
            description="বিজ্ঞান প্রতিযোগিতায় শীর্ষ ১০% মেধা অর্জন।",
            subject="বিজ্ঞান",
            mastery_score=88.0,
        )

        verification = portfolio_credential_service.verify_credential(cred["credential_id"])
        self.assertTrue(verification["valid"])
        self.assertEqual(verification["status"], "VALID")

        # Confirm student real identity is pseudonymized
        recipient = verification["recipient"]
        self.assertTrue(recipient["is_minor"])
        self.assertIn("সুরক্ষিত অপ্রাপ্তবয়স্ক প্রোফাইল", recipient["name"])
        self.assertNotIn("usr_minor_771", str(recipient))

    def test_portfolio_credential_signature_tamper_detection(self) -> None:
        """Verifies that modifying a credential's signature causes verification failure."""
        cred = portfolio_credential_service.issue_credential(
            student_id="usr_std_302",
            student_name="সাদিয়া আফরিন",
            is_minor=False,
            badge_type="INTEGRITY_BOUNTY_SENTINEL",
            title="সততা বাউন্টি ও প্ল্যাটফর্ম সেন্টিনেল",
            description="ভুল প্রশ্ন শনাক্ত করে প্ল্যাটফর্মের গুণমান রক্ষায় অবদান।",
            subject="সকল বিষয়",
            mastery_score=100.0,
        )

        # Alter the stored signature
        portfolio_credential_service._credentials[cred["credential_id"]]["signature"] = "tampered_fake_signature"

        verification = portfolio_credential_service.verify_credential(cred["credential_id"])
        self.assertFalse(verification["valid"])
        self.assertIn("signature mismatch", verification["message"])

    def test_portfolio_credential_revocation(self) -> None:
        """Verifies credential revocation and audit ledger trail."""
        cred = portfolio_credential_service.issue_credential(
            student_id="usr_std_404",
            student_name="কামরুল হাসান",
            is_minor=False,
            badge_type="TEST_BADGE",
            title="অস্থায়ী ব্যাজ",
            description="টেস্টিং সার্টিফিকেট",
            subject="সাধারণ জ্ঞান",
            mastery_score=75.0,
        )

        revocation_success = portfolio_credential_service.revoke_credential(
            credential_id=cred["credential_id"],
            reason="Plagiarism detected in exam attempt",
            actor_id="usr_admin_audit",
        )
        self.assertTrue(revocation_success)

        verification = portfolio_credential_service.verify_credential(cred["credential_id"])
        self.assertFalse(verification["valid"])
        self.assertIn("REVOKED", verification["message"])

        # Check audit block
        latest_block = audit_ledger._blocks[-1]
        self.assertEqual(latest_block.event_type, "CREDENTIAL_REVOKED")
        self.assertEqual(latest_block.payload["reason"], "Plagiarism detected in exam attempt")

    async def _async_test_api_endpoints(self) -> None:
        """Asynchronous helper testing REST controller endpoints."""
        req = CredentialIssueRequest(
            student_id="usr_api_std_1",
            student_name="ফারহানা হক",
            is_minor=False,
            badge_type="ADMISSION_EXCELLENCE",
            title="ডিইউ 'ক' ইউনিট মেধা সার্টিফিকেট",
            description="বিশ্ববিদ্যালয় ভর্তি মক পরীক্ষায় প্রথম স্থান।",
            subject="পদার্থবিজ্ঞান",
            mastery_score=92.0,
        )

        issue_res = await issue_student_credential(req)
        self.assertEqual(issue_res["status"], "SUCCESS")
        cred_id = issue_res["credential"]["credential_id"]

        verify_res = await verify_student_credential(cred_id)
        self.assertTrue(verify_res["valid"])

        student_list_res = await list_student_credentials("usr_api_std_1")
        self.assertEqual(student_list_res["total_credentials"], 1)

        audit_verify_res = await verify_audit_ledger_integrity()
        self.assertTrue(audit_verify_res["valid"])
        self.assertGreaterEqual(audit_verify_res["total_blocks"], 2)

        blocks_res = await list_audit_ledger_blocks(limit=10, offset=0)
        self.assertGreaterEqual(len(blocks_res["blocks"]), 2)

    def test_api_endpoints_phase15(self) -> None:
        """Executes the async REST endpoints in standard test runner."""
        import asyncio
        asyncio.run(self._async_test_api_endpoints())


if __name__ == "__main__":
    unittest.main()
