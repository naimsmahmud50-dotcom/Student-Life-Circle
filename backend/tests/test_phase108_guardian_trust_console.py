"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite
TOPIC:     Phase 108 Guardian Trust Console & Child Digital Safety Tests
FILE:      backend/tests/test_phase108_guardian_trust_console.py
PHASE:     Phase 108 - Guardian Trust Console & Child Digital Safety Portal
PURPOSE:   Asserts child privacy boundary wall (ASVS L2 HTTP 403), non-intrusive
           academic telemetry aggregation, tuition escrow OTP milestone release,
           SHA-256 cryptographic audit logs, and strict zero-emoji governance.
STANDARDS: ASVS L2 Minor Privacy Boundary, Zero-Intrusion Safeguards, Zero-Emoji, UI/UX Pro Max
"""

import asyncio
import json
import os
import unittest
from pathlib import Path

from backend.app.services.guardian_trust_service import (
    ChildPrivacyBoundaryException,
    GuardianTrustService,
    guardian_trust_service
)
from backend.app.api.v1.endpoints.guardian_console import (
    get_guardian_family_summary,
    get_child_private_chat_endpoint,
    list_pending_escrow_milestones,
    approve_tuition_escrow_milestone
)
from backend.app.core.fastapi_shim import HTTPException


def is_emoji_char(char: str) -> bool:
    """Detects whether a character is a decorative unicode emoji."""
    code = ord(char)
    return (
        0x1F600 <= code <= 0x1F64F or
        0x1F300 <= code <= 0x1F5FF or
        0x1F680 <= code <= 0x1F6FF or
        0x1F900 <= code <= 0x1F9FF or
        0x1FA70 <= code <= 0x1FAFF or
        0x2600 <= code <= 0x26FF or
        0x2700 <= code <= 0x27BF
    )


def contains_emoji(text: str) -> bool:
    """Returns True if string contains any decorative unicode emoji."""
    return any(is_emoji_char(c) for c in text)


class TestPhase108GuardianTrustConsole(unittest.TestCase):
    """
    Automated verification suite for Phase 108 Guardian Trust Console & Child Digital Safety.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.service_path = cls.repo_root / "backend" / "app" / "services" / "guardian_trust_service.py"
        cls.endpoint_path = cls.repo_root / "backend" / "app" / "api" / "v1" / "endpoints" / "guardian_console.py"
        cls.dashboard_path = cls.repo_root / "frontend" / "src" / "components" / "guardian" / "GuardianDashboard.tsx"
        cls.escrow_card_path = cls.repo_root / "frontend" / "src" / "components" / "guardian" / "TuitionEscrowApprovalCard.tsx"
        cls.page_path = cls.repo_root / "frontend" / "src" / "pages" / "guardian.tsx"
        cls.tasks_path = cls.repo_root / "specs" / "012-phase108-guardian-trust-console" / "tasks.md"

    def setUp(self):
        guardian_trust_service.reset_for_testing()

    def test_01_child_privacy_boundary_wall_enforcement(self):
        """Verifies ASVS L2 child privacy wall strictly blocks guardian interception into peer communications."""
        svc = guardian_trust_service

        with self.assertRaises(ChildPrivacyBoundaryException) as cm:
            svc.get_child_private_chat("GUARD_2026_01", "STU_TAHSIN_01")

        self.assertIn("CHILD_PRIVACY_BOUNDARY_ENFORCED", str(cm.exception))
        self.assertIn("ASVS L2", str(cm.exception))

    def test_02_non_intrusive_academic_telemetry_aggregation(self):
        """Verifies summary aggregates high-level learning health without leaking private data."""
        svc = guardian_trust_service
        summary = svc.get_guardian_summary("GUARD_2026_01")

        self.assertIsNotNone(summary)
        self.assertEqual(summary["guardian_id"], "GUARD_2026_01")
        self.assertGreaterEqual(summary["children_count"], 2)

        child1 = summary["children"][0]
        self.assertEqual(child1["child_id"], "STU_TAHSIN_01")
        self.assertGreater(child1["weekly_study_hours"], 0)
        self.assertGreater(child1["study_streak_days"], 0)
        self.assertGreater(len(child1["subject_mastery"]), 0)
        self.assertGreater(len(child1["upcoming_exams"]), 0)

        # Ensure private chat logs are completely omitted from public summary
        self.assertNotIn("private_chat_logs", child1)

    def test_03_tuition_escrow_milestone_retrieval_and_approval(self):
        """Verifies dual-party tuition escrow milestone lifecycle, SMS OTP verification, and SHA-256 audit."""
        svc = guardian_trust_service

        # 1. Retrieve pending milestones
        milestones = svc.get_pending_escrow_milestones("GUARD_2026_01")
        self.assertEqual(len(milestones), 1)
        m = milestones[0]
        self.assertEqual(m["milestone_id"], "ESCROW_PHYSICS_OCT_2026")
        self.assertEqual(m["status"], "HELD_IN_ESCROW")
        self.assertEqual(m["completed_sessions"], 12)
        self.assertNotIn("valid_otp", m)  # Internal OTP must never be leaked

        # 2. Reject approval with invalid OTP
        bad_res = svc.approve_tuition_escrow("GUARD_2026_01", "ESCROW_PHYSICS_OCT_2026", "9999")
        self.assertFalse(bad_res["success"])
        self.assertIn("Invalid SMS OTP", bad_res["error"])

        # 3. Approve with valid OTP '8821'
        good_res = svc.approve_tuition_escrow("GUARD_2026_01", "ESCROW_PHYSICS_OCT_2026", "8821")
        self.assertTrue(good_res["success"])
        self.assertEqual(good_res["status"], "RELEASED_TO_TUTOR")
        self.assertIsNotNone(good_res["receipt_hash"])
        self.assertEqual(len(good_res["receipt_hash"]), 64)  # SHA-256 hex length

        # 4. Audit trail verification
        audit = svc.get_audit_trail()
        self.assertEqual(len(audit), 1)
        self.assertEqual(audit[0]["action"], "TUITION_ESCROW_RELEASE")
        self.assertEqual(audit[0]["receipt_hash"], good_res["receipt_hash"])

        # 5. Milestone is no longer in pending list
        after_milestones = svc.get_pending_escrow_milestones("GUARD_2026_01")
        self.assertEqual(len(after_milestones), 0)

    async def _test_async_endpoints(self):
        """Helper to run async endpoint unit tests."""
        def extract_content(res):
            if hasattr(res, "body"):
                return json.loads(res.body.decode("utf-8"))
            return getattr(res, "content", {})

        # 1. Summary endpoint
        summary_res = await get_guardian_family_summary(guardian_id="GUARD_2026_01")
        self.assertEqual(summary_res.status_code, 200)
        summary_data = extract_content(summary_res)
        self.assertEqual(summary_data["guardian_id"], "GUARD_2026_01")
        self.assertGreaterEqual(summary_data["children_count"], 1)

        # 2. Privacy wall endpoint MUST raise 403 Forbidden
        with self.assertRaises(HTTPException) as cm:
            await get_child_private_chat_endpoint(child_id="STU_TAHSIN_01", guardian_id="GUARD_2026_01")
        self.assertEqual(cm.exception.status_code, 403)
        self.assertIn("CHILD_PRIVACY_BOUNDARY_ENFORCED", str(cm.exception.detail))

        # 3. Pending milestones endpoint
        milestones_res = await list_pending_escrow_milestones(guardian_id="GUARD_2026_01")
        self.assertEqual(milestones_res.status_code, 200)
        milestones_data = extract_content(milestones_res)
        self.assertGreaterEqual(milestones_data["total"], 1)

        # 4. Approve escrow endpoint with valid OTP
        approve_payload = {
            "guardian_id": "GUARD_2026_01",
            "milestone_id": "ESCROW_PHYSICS_OCT_2026",
            "otp_code": "8821"
        }
        approve_res = await approve_tuition_escrow_milestone(approve_payload)
        self.assertEqual(approve_res.status_code, 200)
        approve_data = extract_content(approve_res)
        self.assertTrue(approve_data["success"])
        self.assertEqual(approve_data["status"], "RELEASED_TO_TUTOR")

        # 5. Approve with invalid OTP raises 400 Bad Request
        with self.assertRaises(HTTPException) as cm:
            await approve_tuition_escrow_milestone({
                "guardian_id": "GUARD_2026_01",
                "milestone_id": "ESCROW_PHYSICS_OCT_2026",
                "otp_code": "0000"
            })
        self.assertEqual(cm.exception.status_code, 400)

    def test_04_rest_api_endpoints_summary_privacy_escrow(self):
        """Verifies Phase 108 REST API endpoints through direct async invocation."""
        asyncio.run(self._test_async_endpoints())

    def test_05_developer_architecture_note_and_strict_zero_emoji(self):
        """Verifies Developer Architecture Note headers and strict zero-emoji governance across Phase 108 files."""
        phase108_files = [
            self.service_path,
            self.endpoint_path,
            self.dashboard_path,
            self.escrow_card_path,
            self.page_path,
            self.tasks_path,
            Path(__file__)
        ]

        for file_path in phase108_files:
            self.assertTrue(file_path.exists(), f"File does not exist: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"Missing Developer Architecture Note in {file_path.name}"
            )
            self.assertIn(
                "Phase 108",
                content,
                f"Missing Phase 108 reference in {file_path.name}"
            )
            self.assertFalse(
                contains_emoji(content),
                f"Strict Zero-Emoji violation detected in {file_path.name}"
            )


if __name__ == "__main__":
    unittest.main()
