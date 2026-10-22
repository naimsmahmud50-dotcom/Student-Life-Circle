"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite for National Merit Scholarships
TOPIC:     Phase 113 National Merit Scholarship Pool & Autonomous Disbursement
FILE:      backend/tests/test_phase113_scholarship_disbursement.py
PHASE:     Phase 113 - National Merit Scholarship Pool & Autonomous Disbursement
PURPOSE:   Automated unit and integration test suite certifying algorithmic merit-need
           evaluation, dual-authorization escrow governance, atomic double-spending
           defense, bKash/Nagad B2C payouts, and strict zero-emoji compliance.
STANDARDS: OWASP ASVS L2, FinTech B2C Security, Pure Academic Design, Strict Zero-Emoji
========================================================================================
"""

import json
import os
import re
import unittest
import uuid
from pathlib import Path

from backend.app.services.scholarship_disbursement_service import (
    ScholarshipDisbursementService,
    EligibilityException,
    AuthorizationException,
    DoubleSpendingException,
    ScholarshipException,
)


class TestPhase113ScholarshipDisbursement(unittest.TestCase):
    """
    Test suite certifying Phase 113 National Merit Scholarship Pool and Disbursement.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.service_file = cls.root_dir / "backend" / "app" / "services" / "scholarship_disbursement_service.py"
        cls.endpoints_file = cls.root_dir / "backend" / "app" / "api" / "v1" / "endpoints" / "scholarships.py"
        cls.frontend_card = cls.root_dir / "frontend" / "src" / "components" / "scholarship" / "ScholarshipEndowmentCard.tsx"
        cls.frontend_modal = cls.root_dir / "frontend" / "src" / "components" / "scholarship" / "DisbursementLedgerModal.tsx"

        cls.emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

    def setUp(self):
        # Create a fresh isolated service instance for each test
        self.service = ScholarshipDisbursementService()

    def test_01_merit_and_need_eligibility_evaluation(self):
        """Verifies algorithmic merit-need qualification under standard and district quotas."""
        # Case A: GPA 5.0 with low income -> Eligible
        res_a = self.service.evaluate_eligibility(
            gpa=5.0,
            national_percentile=80.0,
            monthly_family_income_bdt=12000.0,
            district="Dhaka",
        )
        self.assertTrue(res_a["is_eligible"])
        self.assertTrue(res_a["merit_qualified"])
        self.assertTrue(res_a["need_qualified"])

        # Case B: Top 5% (percentile 96.5) with low income -> Eligible
        res_b = self.service.evaluate_eligibility(
            gpa=4.8,
            national_percentile=96.5,
            monthly_family_income_bdt=14000.0,
            district="Chittagong",
        )
        self.assertTrue(res_b["is_eligible"])

        # Case C: Priority District affirmative action cutoff (Kurigram income 18,000 <= 20,000) -> Eligible
        res_c = self.service.evaluate_eligibility(
            gpa=5.0,
            national_percentile=90.0,
            monthly_family_income_bdt=18000.0,
            district="Kurigram",
        )
        self.assertTrue(res_c["is_eligible"])
        self.assertTrue(res_c["is_priority_district"])

        # Case D: Non-priority district with income 18,000 (> 15,000 standard cutoff) -> Ineligible
        res_d = self.service.evaluate_eligibility(
            gpa=5.0,
            national_percentile=90.0,
            monthly_family_income_bdt=18000.0,
            district="Dhaka",
        )
        self.assertFalse(res_d["is_eligible"])
        self.assertFalse(res_d["need_qualified"])

        # Case E: High income -> Ineligible
        res_e = self.service.evaluate_eligibility(
            gpa=5.0,
            national_percentile=99.0,
            monthly_family_income_bdt=60000.0,
            district="Kurigram",
        )
        self.assertFalse(res_e["is_eligible"])

        # Case F: Low academic merit -> Ineligible
        res_f = self.service.evaluate_eligibility(
            gpa=3.6,
            national_percentile=60.0,
            monthly_family_income_bdt=8000.0,
            district="Barguna",
        )
        self.assertFalse(res_f["is_eligible"])

    def test_02_dual_authorization_workflow(self):
        """Verifies two-person rule: academic evaluator followed by finance custodian."""
        student_id = f"stu_{uuid.uuid4().hex[:8]}"
        app = self.service.submit_application(
            pool_id="pool-national-merit-2026",
            student_id=student_id,
            student_name="Rakibul Hasan",
            district="Sunamganj",
            gpa=5.0,
            national_percentile=97.0,
            monthly_family_income_bdt=11000.0,
            mobile_wallet_number="01712345678",
            wallet_provider="bKash",
        )
        self.assertEqual(app["status"], self.service.STATUS_SUBMITTED)

        # Premature approval by finance custodian fails
        with self.assertRaises(AuthorizationException):
            self.service.approve_application(
                application_id=app["application_id"],
                authorizer_id="fin_custodian_01",
                authorizer_role="finance_custodian",
            )

        # Step 1: Academic Evaluator signs
        app = self.service.approve_application(
            application_id=app["application_id"],
            authorizer_id="prof_academic_01",
            authorizer_role="academic_evaluator",
            notes="Transcripts verified with NCTB board roll.",
        )
        self.assertEqual(app["status"], self.service.STATUS_ACADEMIC_APPROVED)

        # Anti-collusion: Same person cannot sign as finance custodian
        with self.assertRaises(AuthorizationException):
            self.service.approve_application(
                application_id=app["application_id"],
                authorizer_id="prof_academic_01",
                authorizer_role="finance_custodian",
            )

        # Step 2: Separate Finance Custodian signs
        app = self.service.approve_application(
            application_id=app["application_id"],
            authorizer_id="treasury_officer_02",
            authorizer_role="finance_custodian",
            notes="Escrow fund locked.",
        )
        self.assertEqual(app["status"], self.service.STATUS_DUAL_APPROVED)

    def test_03_double_spending_and_idempotency_defense(self):
        """Verifies atomic state locking and idempotency key protection against double-spending."""
        student_id = f"stu_{uuid.uuid4().hex[:8]}"
        app = self.service.submit_application(
            pool_id="pool-national-merit-2026",
            student_id=student_id,
            student_name="Fatima Akter",
            district="Bandarban",
            gpa=5.0,
            national_percentile=98.0,
            monthly_family_income_bdt=9500.0,
            mobile_wallet_number="01812345678",
            wallet_provider="Nagad",
        )

        idempotency_key = f"idem_{uuid.uuid4().hex[:16]}"

        # Attempt disbursement before approval -> Fails
        with self.assertRaises(AuthorizationException):
            self.service.execute_disbursement(
                application_id=app["application_id"],
                idempotency_key=idempotency_key,
                operator_id="operator_01",
            )

        # Grant dual approvals
        self.service.approve_application(app["application_id"], "eval_01", "academic_evaluator")
        self.service.approve_application(app["application_id"], "fin_02", "finance_custodian")

        # Initial pool remaining
        pool_initial = self.service.get_pool("pool-national-merit-2026")
        initial_remaining = pool_initial["remaining_bdt"]

        # First legitimate disbursement
        receipt1 = self.service.execute_disbursement(
            application_id=app["application_id"],
            idempotency_key=idempotency_key,
            operator_id="operator_01",
        )
        self.assertEqual(receipt1["verification_status"], "VERIFIED_ON_LEDGER")
        self.assertEqual(receipt1["disbursed_amount_bdt"], 10000.0)

        # Pool remaining decreased
        pool_after = self.service.get_pool("pool-national-merit-2026")
        self.assertEqual(pool_after["remaining_bdt"], initial_remaining - 10000.0)

        # Re-play with IDENTICAL idempotency key -> Returns cached receipt without double deduction
        receipt2 = self.service.execute_disbursement(
            application_id=app["application_id"],
            idempotency_key=idempotency_key,
            operator_id="operator_01",
        )
        self.assertEqual(receipt1["ledger_seal_sha256"], receipt2["ledger_seal_sha256"])
        self.assertEqual(pool_after["remaining_bdt"], self.service.get_pool("pool-national-merit-2026")["remaining_bdt"])

        # Second disbursement attempt with DIFFERENT idempotency key -> Blocked by state check
        new_idempotency_key = f"idem_{uuid.uuid4().hex[:16]}"
        with self.assertRaises(DoubleSpendingException):
            self.service.execute_disbursement(
                application_id=app["application_id"],
                idempotency_key=new_idempotency_key,
                operator_id="operator_01",
            )

    def test_04_cryptographic_receipt_and_public_ledger(self):
        """Verifies SHA-256 seal integrity and PII anonymization on public audit trail."""
        student_id = f"stu_{uuid.uuid4().hex[:8]}"
        app = self.service.submit_application(
            pool_id="pool-rural-stem-2026",
            student_id=student_id,
            student_name="Tarek Mahmud",
            district="Kurigram",
            gpa=5.0,
            national_percentile=99.0,
            monthly_family_income_bdt=10000.0,
            mobile_wallet_number="01912345678",
            wallet_provider="bKash",
        )

        self.service.approve_application(app["application_id"], "eval_01", "academic_evaluator")
        self.service.approve_application(app["application_id"], "fin_02", "finance_custodian")

        receipt = self.service.execute_disbursement(
            application_id=app["application_id"],
            idempotency_key=f"idem_{uuid.uuid4().hex[:12]}",
            operator_id="operator_01",
        )

        # Validate SHA-256 seal (64 hex characters)
        seal = receipt["ledger_seal_sha256"]
        self.assertEqual(len(seal), 64)
        self.assertTrue(re.match(r"^[a-f0-9]{64}$", seal))

        # Query public ledger
        ledger = self.service.get_public_ledger()
        self.assertGreater(ledger["total_disbursed_count"], 0)
        
        # Verify student privacy protection: NO legal name present in public ledger
        ledger_json = json.dumps(ledger)
        self.assertNotIn("Tarek Mahmud", ledger_json)
        self.assertNotIn("01912345678", ledger_json)
        self.assertIn("STU-****-", ledger_json)

    def test_05_frontend_components_integrity(self):
        """Verifies frontend components exist and declare tactile 3D button depth."""
        self.assertTrue(self.frontend_card.exists(), "ScholarshipEndowmentCard.tsx must exist.")
        self.assertTrue(self.frontend_modal.exists(), "DisbursementLedgerModal.tsx must exist.")

        card_code = self.frontend_card.read_text(encoding="utf-8")
        modal_code = self.frontend_modal.read_text(encoding="utf-8")

        # Check tactile 3D Oxford button classes
        self.assertIn("shadow-[0_4px_0_0_#051329]", card_code)
        self.assertIn("আবেদন জমা দিন", card_code)
        self.assertIn("বৃত্তি অনুমোদন করুন", card_code)

        # Check modal structure
        self.assertIn("পাবলিক স্কলারশিপ ডিসবার্সমেন্ট লেজার", modal_code)
        self.assertIn("anonymous_student_token", modal_code)
        self.assertIn("ledger_seal_sha256", modal_code)

    def test_06_developer_architecture_notes_and_strict_zero_emoji(self):
        """Asserts Developer Architecture Notes and strict zero-emoji compliance on all Phase 113 files."""
        target_files = [
            self.service_file,
            self.endpoints_file,
            self.frontend_card,
            self.frontend_modal,
            Path(__file__).resolve(),
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")

            # Check header
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"File {file_path.name} missing Developer Architecture Note header."
            )

            # Check zero emojis
            matches = self.emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"File {file_path.name} violates strict Zero Emoji policy: found {matches}"
            )


if __name__ == "__main__":
    unittest.main()
