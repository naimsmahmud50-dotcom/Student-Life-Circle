"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Micro-Scholarship Disbursement Vault
 * TOPIC:     Phase 133 Mobile Financial Services Gateway & Proof-of-Merit Verification
 * FILE:      backend/tests/test_phase133_scholarship_disbursement.py
 * PHASE:     Phase 133 - Direct-to-Mobile Scholarship Disbursement Vault
 * PURPOSE:   Automated test suite validating:
 *            1. Developer Architecture Note headers & file presence
 *            2. Cryptographic Proof-of-Merit tier assignments & evaluation
 *            3. Anti-Fraud multi-vector defenses (duplicate NID, wallet hijacking, MSISDN format)
 *            4. MFS gateway settlement, SHA-256 transaction hashes, and idempotency
 *            5. Endowment vault liquidity tracking and exhaustion protection
 *            6. Supabase migration 011 Row Level Security and financial ledger immutability
 *            7. Frontend disbursement portal markup, 3D tactile buttons, and Zero-Emoji compliance
 * STANDARDS: Zero-Emoji, Financial Immutable Audit, ASVS L2, Fraud Prevention
 */
"""

import os
import re
import unittest
from pathlib import Path

from backend.scholarship.disbursement_vault import (
    AntiFraudGuard,
    DisbursementStatus,
    DisbursementTransaction,
    DuplicateNIDException,
    FraudulentClaimException,
    InsufficientVaultBalanceException,
    InvalidMFSWalletException,
    MFSDisbursementGateway,
    MFSProvider,
    ProofOfMeritEvaluator,
    ProofOfMeritRecord,
    ScholarshipTier,
    ScholarshipVaultService,
    TIER_DISBURSEMENT_AMOUNTS,
)

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase133ScholarshipDisbursement(unittest.TestCase):
    """
    Automated verification suite for Phase 133 Micro-Scholarship Disbursement Vault.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.scholarship_init = cls.root_dir / "backend" / "scholarship" / "__init__.py"
        cls.vault_py = cls.root_dir / "backend" / "scholarship" / "disbursement_vault.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "011_scholarship_disbursement_rls.sql"
        cls.disbursement_tsx = cls.root_dir / "frontend" / "src" / "pages" / "scholarship" / "disbursement.tsx"
        cls.test_py = cls.root_dir / "backend" / "tests" / "test_phase133_scholarship_disbursement.py"

    def test_01_all_phase133_files_exist_with_developer_headers(self):
        """Validates that all Phase 133 core files exist and possess mandatory Developer Architecture Note headers."""
        target_files = [
            self.scholarship_init,
            self.vault_py,
            self.migration_sql,
            self.disbursement_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Missing required Phase 133 file: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE:", content, f"Missing Architecture header in {file_path}")
            self.assertIn("Phase 133", content, f"Missing Phase 133 reference in {file_path}")
            self.assertIn("Micro-Scholarship Disbursement Vault", content, f"Missing module in {file_path}")

    def test_02_zero_emoji_compliance(self):
        """Strictly enforces zero emoji in all created Phase 133 code and migration files."""
        target_files = [
            self.scholarship_init,
            self.vault_py,
            self.migration_sql,
            self.disbursement_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(len(matches), 0, f"Emoji violations detected in {file_path}: {matches}")

    def test_03_proof_of_merit_tier_assignment(self):
        """Verifies accurate Proof-of-Merit qualification across all scholarship tiers."""
        # 1. National Gold: Olympiad Rank 1-3
        pom_gold = ProofOfMeritRecord(
            record_id="pom_01",
            student_id="stu_gold",
            nid_or_brn="NID_001",
            board_gpa=4.8,
            district="Dhaka",
            olympiad_rank=2
        )
        ok, tier, _ = ProofOfMeritEvaluator.evaluate(pom_gold)
        self.assertTrue(ok)
        self.assertEqual(tier, ScholarshipTier.NATIONAL_GOLD)
        self.assertEqual(TIER_DISBURSEMENT_AMOUNTS[tier], 15000)

        # 2. Regional Distinction: Golden GPA 5.0
        pom_regional = ProofOfMeritRecord(
            record_id="pom_02",
            student_id="stu_reg",
            nid_or_brn="NID_002",
            board_gpa=5.0,
            district="Chittagong",
            is_golden_gpa=True
        )
        ok, tier, _ = ProofOfMeritEvaluator.evaluate(pom_regional)
        self.assertTrue(ok)
        self.assertEqual(tier, ScholarshipTier.REGIONAL_DISTINCTION)
        self.assertEqual(TIER_DISBURSEMENT_AMOUNTS[tier], 8000)

        # 3. Rural Equity Bursary: Kurigram + GPA 4.7
        pom_rural = ProofOfMeritRecord(
            record_id="pom_03",
            student_id="stu_rural",
            nid_or_brn="NID_003",
            board_gpa=4.7,
            district="Kurigram"
        )
        ok, tier, _ = ProofOfMeritEvaluator.evaluate(pom_rural)
        self.assertTrue(ok)
        self.assertEqual(tier, ScholarshipTier.RURAL_EQUITY_BURSARY)
        self.assertEqual(TIER_DISBURSEMENT_AMOUNTS[tier], 5000)

        # 4. STEM Merit: General GPA 5.0
        pom_stem = ProofOfMeritRecord(
            record_id="pom_04",
            student_id="stu_stem",
            nid_or_brn="NID_004",
            board_gpa=5.0,
            district="Sylhet",
            is_golden_gpa=False
        )
        ok, tier, _ = ProofOfMeritEvaluator.evaluate(pom_stem)
        self.assertTrue(ok)
        self.assertEqual(tier, ScholarshipTier.STEM_MERIT_STIPEND)
        self.assertEqual(TIER_DISBURSEMENT_AMOUNTS[tier], 4000)

        # 5. Ineligible: Low GPA and no Olympiad rank
        pom_ineligible = ProofOfMeritRecord(
            record_id="pom_05",
            student_id="stu_ineligible",
            nid_or_brn="NID_005",
            board_gpa=3.8,
            district="Dhaka"
        )
        ok, tier, _ = ProofOfMeritEvaluator.evaluate(pom_ineligible)
        self.assertFalse(ok)
        self.assertIsNone(tier)

    def test_04_msisdn_wallet_normalization_and_validation(self):
        """Tests Bangladeshi MSISDN wallet parsing and rejection of invalid formats."""
        # Valid numbers
        self.assertEqual(AntiFraudGuard.normalize_and_validate_msisdn("01712345678"), "+8801712345678")
        self.assertEqual(AntiFraudGuard.normalize_and_validate_msisdn("+8801823456789"), "+8801823456789")
        self.assertEqual(AntiFraudGuard.normalize_and_validate_msisdn("8801934567890"), "+8801934567890")
        self.assertEqual(AntiFraudGuard.normalize_and_validate_msisdn("01300000000"), "+8801300000000")

        # Invalid formats
        invalid_numbers = [
            "01212345678",   # 012 is invalid operator prefix in BD
            "0171234567",    # 10 digits (too short)
            "017123456789",  # 12 digits (too long)
            "0191234abcd",   # letters
            "+14155552671",  # US phone number
        ]
        for inv in invalid_numbers:
            with self.assertRaises(InvalidMFSWalletException):
                AntiFraudGuard.normalize_and_validate_msisdn(inv)

    def test_05_anti_fraud_duplicate_nid_and_identity_defense(self):
        """Tests anti-fraud guard against duplicate NIDs, identity collisions, and wallet hijacking."""
        guard = AntiFraudGuard()
        student_1 = "stu_001"
        nid_1 = "19992612345678901"
        wallet_1 = "01711112222"

        # Initial clean claim
        guard.assert_no_fraudulent_claim(student_1, nid_1, wallet_1)
        guard.record_claim(student_1, nid_1, wallet_1)

        # 1. Duplicate claim with the same NID must raise DuplicateNIDException
        with self.assertRaises(DuplicateNIDException):
            guard.assert_no_fraudulent_claim("stu_another", nid_1, "01822223333")

        # 2. Student attempting to claim with a different NID
        with self.assertRaises(FraudulentClaimException):
            guard.assert_no_fraudulent_claim(student_1, "20002698765432100", "01733334444")

        # 3. Wallet hijacking: another student attempting to disburse to wallet_1
        with self.assertRaises(FraudulentClaimException):
            guard.assert_no_fraudulent_claim("stu_hijacker", "20012698765432199", wallet_1)

    def test_06_mfs_gateway_and_cryptographic_hash(self):
        """Tests MFS payout simulation and SHA-256 transaction hash generation."""
        providers = [MFSProvider.BKASH, MFSProvider.NAGAD, MFSProvider.ROCKET]
        wallet = "+8801712345678"
        amount = 15000
        idemp = "idemp_test_9988"

        for p in providers:
            mfs_ref, txn_hash = MFSDisbursementGateway.execute_payout(p, wallet, amount, idemp)
            self.assertTrue(mfs_ref.startswith(("BKS_", "NGD_", "RKT_")))
            self.assertEqual(len(txn_hash), 64)  # SHA-256 hex string

    def test_07_idempotency_and_vault_disbursement_service(self):
        """Tests end-to-end disbursement, ledger idempotency, and vault balance deduction."""
        vault = ScholarshipVaultService(initial_endowment_bdt=100000)
        self.assertEqual(vault.remaining_liquidity_bdt, 100000)

        # Successful disbursement
        txn1 = vault.disburse_scholarship(
            student_id="student_lead_01",
            nid_or_brn="NID_778899",
            board_gpa=5.0,
            district="Dhaka",
            mfs_provider=MFSProvider.BKASH,
            wallet_msisdn="01712345678",
            idempotency_key="idemp_unique_01",
            olympiad_rank=1
        )

        self.assertEqual(txn1.amount_bdt, 15000)
        self.assertEqual(txn1.tier, ScholarshipTier.NATIONAL_GOLD)
        self.assertEqual(txn1.status, DisbursementStatus.DISBURSED)
        self.assertEqual(vault.disbursed_bdt, 15000)
        self.assertEqual(vault.remaining_liquidity_bdt, 85000)

        # Idempotent retransmission must return identical transaction without second debit
        txn1_repeat = vault.disburse_scholarship(
            student_id="student_lead_01",
            nid_or_brn="NID_778899",
            board_gpa=5.0,
            district="Dhaka",
            mfs_provider=MFSProvider.BKASH,
            wallet_msisdn="01712345678",
            idempotency_key="idemp_unique_01",
            olympiad_rank=1
        )
        self.assertEqual(txn1_repeat.transaction_id, txn1.transaction_id)
        self.assertEqual(vault.disbursed_bdt, 15000)  # Balance unchanged

    def test_08_vault_liquidity_exhaustion_protection(self):
        """Tests that attempting to disburse beyond available liquidity raises InsufficientVaultBalanceException."""
        low_vault = ScholarshipVaultService(initial_endowment_bdt=10000)

        with self.assertRaises(InsufficientVaultBalanceException):
            low_vault.disburse_scholarship(
                student_id="student_high_01",
                nid_or_brn="NID_9999",
                board_gpa=5.0,
                district="Dhaka",
                mfs_provider=MFSProvider.BKASH,
                wallet_msisdn="01799999999",
                idempotency_key="idemp_exhaust_01",
                olympiad_rank=1  # Requires 15000 BDT, vault only has 10000
            )

    def test_09_supabase_migration_011_rls_and_immutability(self):
        """Verifies migration 011 establishes tables, enforces 100% RLS, and asserts ledger immutability."""
        sql_content = self.migration_sql.read_text(encoding="utf-8")

        required_tables = [
            "scholarship_endowment_vaults",
            "micro_scholarship_applications",
            "mfs_disbursement_ledger",
            "scholarship_fraud_audit_logs",
        ]

        for tbl in required_tables:
            has_table = f"CREATE TABLE IF NOT EXISTS public.{tbl}" in sql_content or f"CREATE TABLE IF NOT EXISTS {tbl}" in sql_content
            self.assertTrue(has_table, f"Missing table creation for {tbl}")
            has_rls = f"ALTER TABLE public.{tbl} ENABLE ROW LEVEL SECURITY;" in sql_content or f"ALTER TABLE {tbl} ENABLE ROW LEVEL SECURITY;" in sql_content
            self.assertTrue(has_rls, f"Missing RLS enablement for {tbl}")

        # Assert immutability revokes
        self.assertIn("REVOKE UPDATE, DELETE ON public.mfs_disbursement_ledger", sql_content)
        self.assertIn("fn_block_mfs_ledger_mutation", sql_content)

    def test_10_frontend_portal_styling_and_tactile_buttons(self):
        """Validates frontend disbursement portal implements Oxford Navy, 3D buttons, and pure Lucide icons."""
        tsx_content = self.disbursement_tsx.read_text(encoding="utf-8")

        # Color palette & 3D tactile buttons
        self.assertTrue(
            "bg-[#0A2540]" in tsx_content or "bg-[#FAFAF8]" in tsx_content,
            "Missing institutional background/navy palette"
        )
        self.assertTrue("shadow-[0_4px_0_0" in tsx_content, "Missing 3D tactile button styling")

        # MFS providers present
        self.assertIn("bKash", tsx_content)
        self.assertIn("Nagad", tsx_content)
        self.assertIn("Rocket", tsx_content)

        # Lucide vector icons
        expected_icons = ["Landmark", "ShieldCheck", "CheckCircle2", "Smartphone", "Award", "Lock"]
        for icon in expected_icons:
            self.assertIn(icon, tsx_content, f"Missing expected Lucide icon: {icon}")


if __name__ == "__main__":
    unittest.main()
