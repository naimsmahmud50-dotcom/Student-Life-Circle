"""
Test Suite: Phase 69 Distributed Shamir Secret Sharing & Ephemeral Exam Vault
Asserts that finite field polynomial secret splitting, Lagrange interpolation reconstruction,
sub-threshold secrecy, anti-tamper detection, and emergency zeroization operate correctly.
"""

import unittest
from backend.app.services.shamir_exam_vault_service import (
    ShamirExamVaultService,
    SECP256K1_PRIME
)

class TestPhase69ShamirExamVault(unittest.TestCase):
    def setUp(self):
        self.service = ShamirExamVaultService()

    def test_default_vault_seeded(self):
        """Verify default HSC Physics vault is pre-seeded with 3-of-5 threshold."""
        vault = self.service.vaults.get("vault-hsc-phy-001")
        self.assertIsNotNone(vault)
        self.assertEqual(vault["exam_code"], "HSC-PHY-2026")
        self.assertEqual(vault["threshold_k"], 3)
        self.assertEqual(vault["total_shares_n"], 5)
        self.assertEqual(vault["status"], "LOCKED")
        self.assertEqual(len(vault["shares"]), 5)

    def test_polynomial_split_generates_correct_shares(self):
        """Test splitting a custom secret generates n valid polynomial shares."""
        custom_content = "Confidential NCTB Class 10 Higher Math Model Exam 2026"
        res = self.service.create_split_vault(
            exam_code="SSC-HMATH-2026",
            subject="Higher Mathematics",
            raw_content=custom_content,
            threshold_k=3,
            total_shares_n=5
        )
        self.assertTrue(res.success)
        self.assertEqual(res.threshold_k, 3)
        self.assertEqual(res.total_shares_n, 5)
        self.assertEqual(len(res.shares), 5)
        self.assertEqual(len(res.custodians), 5)

        # Check unique x coordinates
        xs = [s.x_coordinate for s in res.shares]
        self.assertEqual(xs, [1, 2, 3, 4, 5])

    def test_quorum_reconstruction_any_three_shares(self):
        """Test that any 3 of 5 shares successfully decrypts the exam payload via Lagrange interpolation."""
        vault_id = "vault-hsc-phy-001"
        vault = self.service.vaults[vault_id]
        shares = vault["shares"]

        # Test with custodians [1, 2, 3]
        presented_123 = [
            {"x": 1, "y": shares[1]["y_hex"], "custodian_id": "cust-01"},
            {"x": 2, "y": shares[2]["y_hex"], "custodian_id": "cust-02"},
            {"x": 3, "y": shares[3]["y_hex"], "custodian_id": "cust-03"}
        ]
        res1 = self.service.reconstruct_and_decrypt_vault(vault_id, presented_123)
        self.assertTrue(res1.success)
        self.assertTrue(res1.quorum_achieved)
        self.assertIn("HSC Examination 2026", res1.decrypted_content)
        self.assertIn("Dynamics & Gravitation", res1.decrypted_content)
        self.assertFalse(res1.tamper_detected)
        self.assertIsNotNone(res1.multisig_audit_receipt)

        # Test with custodians [2, 4, 5] on a fresh split
        res_split = self.service.create_split_vault(
            exam_code="HSC-CHEM-2026",
            subject="Chemistry Paper 2",
            raw_content="Confidential Organic Chemistry Reaction Mechanisms",
            threshold_k=3,
            total_shares_n=5
        )
        s_dict = self.service.vaults[res_split.vault_id]["shares"]
        presented_245 = [
            {"x": 2, "y": s_dict[2]["y_hex"], "custodian_id": "cust-02"},
            {"x": 4, "y": s_dict[4]["y_hex"], "custodian_id": "cust-04"},
            {"x": 5, "y": s_dict[5]["y_hex"], "custodian_id": "cust-05"}
        ]
        res2 = self.service.reconstruct_and_decrypt_vault(res_split.vault_id, presented_245)
        self.assertTrue(res2.success)
        self.assertIn("Organic Chemistry Reaction Mechanisms", res2.decrypted_content)

    def test_insufficient_shares_fails_quorum(self):
        """Test that providing 2 shares (below threshold k=3) fails and discloses zero content."""
        vault_id = "vault-hsc-phy-001"
        shares = self.service.vaults[vault_id]["shares"]

        # Only 2 shares provided
        presented_sub = [
            {"x": 1, "y": shares[1]["y_hex"], "custodian_id": "cust-01"},
            {"x": 2, "y": shares[2]["y_hex"], "custodian_id": "cust-02"}
        ]
        res = self.service.reconstruct_and_decrypt_vault(vault_id, presented_sub)
        self.assertFalse(res.success)
        self.assertFalse(res.quorum_achieved)
        self.assertIsNone(res.decrypted_content)
        self.assertIn("Quorum not achieved", res.message)

    def test_tampered_share_triggers_security_alert(self):
        """Test that modifying a share triggers HMAC failure and logs tamper event."""
        vault_id = "vault-hsc-phy-001"
        shares = self.service.vaults[vault_id]["shares"]

        # Tampered y-coordinate
        tampered_shares = [
            {"x": 1, "y": shares[1]["y_hex"], "custodian_id": "cust-01"},
            {"x": 2, "y": hex(int(shares[2]["y_hex"], 16) + 1)[2:], "custodian_id": "cust-02"},  # Tampered bit
            {"x": 3, "y": shares[3]["y_hex"], "custodian_id": "cust-03"}
        ]
        res = self.service.reconstruct_and_decrypt_vault(vault_id, tampered_shares)
        self.assertFalse(res.success)
        self.assertTrue(res.tamper_detected)
        self.assertIsNone(res.decrypted_content)
        self.assertIn("tampered share detected", res.message)

        # Check vault status updated to TAMPER_ALERT
        summary = self.service.get_vault_summary(vault_id)
        self.assertEqual(summary["status"], "TAMPER_ALERT")
        self.assertGreater(summary["tamper_events_count"], 0)

    def test_emergency_zeroization(self):
        """Test zeroization wipes vault keys, sets status to WIPED, and prevents decrypt."""
        vault_id = "vault-hsc-phy-001"
        wipe_res = self.service.trigger_zeroization(vault_id, operator_id="admin:security-chief")
        self.assertTrue(wipe_res["success"])
        self.assertEqual(wipe_res["status"], "WIPED")

        # Try to reconstruct wiped vault
        presented = [
            {"x": 1, "y": "1234", "custodian_id": "cust-01"},
            {"x": 2, "y": "5678", "custodian_id": "cust-02"},
            {"x": 3, "y": "9abc", "custodian_id": "cust-03"}
        ]
        res = self.service.reconstruct_and_decrypt_vault(vault_id, presented)
        self.assertFalse(res.success)
        self.assertIn("zeroized", res.message)

    def test_custodian_listing(self):
        """Verify list of 5 designated custodian trustees."""
        custodians = self.service.get_custodians("vault-hsc-phy-001")
        self.assertEqual(len(custodians), 5)
        roles = [c.role for c in custodians]
        self.assertIn("Head Examiner & Board Convener", roles)
        self.assertIn("Center Superintendent", roles)
        self.assertIn("External Education Board Observer", roles)

    def test_vault_summary(self):
        """Verify summary returns threshold, total shares, and quorum metrics."""
        summary = self.service.get_vault_summary("vault-hsc-phy-001")
        self.assertEqual(summary["vault_id"], "vault-hsc-phy-001")
        self.assertEqual(summary["threshold_k"], 3)
        self.assertEqual(summary["total_shares_n"], 5)
        self.assertEqual(summary["shares_presented_count"], 0)
        self.assertEqual(summary["quorum_pct"], 0.0)

if __name__ == "__main__":
    unittest.main()
