# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 81 - Payment & Escrow Verification Suite):
# Automated verification test suite for Phase 81: Bangladeshi Payment Gateways & Escrow Vault.
# Verifies:
# 1. bKash Merchant API: Token grant, payment create, execute with TRXID capture, query, and refund.
# 2. Nagad PG: RSA-2048 encryption, digital signature verification, and callback processing.
# 3. Tuition Milestone Escrow: Deposit locking, session logging, milestone approval, 5% fee deduction,
#    and auto-disbursement of 95% net honorarium to tutor wallet.
# 4. Dispute Arbitration: Escrow freezing, arbitrator tribunal resolution (release, refund, split).
# 5. Webhook Security: HMAC-SHA256 signature verification, 5-minute timestamp window, and replay mitigation.
# 6. Strict Zero-Emoji Governance: Enforces zero-emoji compliance across all Phase 81 files.
# ==============================================================================

import os
import time
import unittest
from typing import Dict, Any

from backend.app.services.payment.bkash_service import BkashMerchantCheckoutService
from backend.app.services.payment.nagad_service import NagadPaymentService
from backend.app.services.payment.escrow_vault_service import TuitionMilestoneEscrowService
from backend.app.services.payment.webhook_verifier import WebhookSecurityService
from backend.app.api.v1.endpoints.payments import router as payments_router


class TestPhase81PaymentAndEscrow(unittest.TestCase):

    def setUp(self):
        self.bkash = BkashMerchantCheckoutService()
        self.nagad = NagadPaymentService()
        self.escrow = TuitionMilestoneEscrowService()
        self.webhook = WebhookSecurityService(webhook_secret="test_wh_secret_2026")

    # --------------------------------------------------------------------------
    # 1. bKash Merchant Checkout API Lifecycle
    # --------------------------------------------------------------------------
    def test_bkash_create_execute_query_and_refund(self):
        # 1. Grant Token
        token_res = self.bkash.grant_token()
        self.assertEqual(token_res["statusCode"], "0000")
        self.assertTrue(token_res["id_token"].startswith("bkt_"))

        # 2. Create Payment
        create_res = self.bkash.create_payment(
            amount=5000.0,
            merchant_invoice_number="INV_SLC_1001",
            payer_reference="usr_guardian_01"
        )
        self.assertEqual(create_res["statusCode"], "0000")
        payment_id = create_res["paymentID"]
        self.assertTrue(payment_id.startswith("TR"))
        self.assertIn("checkout?paymentID=", create_res["bkashURL"])

        # 3. Execute Payment
        exec_res = self.bkash.execute_payment(payment_id)
        self.assertEqual(exec_res["statusCode"], "0000")
        self.assertEqual(exec_res["transactionStatus"], "Completed")
        trx_id = exec_res["trxID"]
        self.assertTrue(trx_id.startswith("BKH"))
        self.assertIsNotNone(exec_res.get("receipt_hash"))

        # Idempotent re-execution returns identical receipt
        exec_repeat = self.bkash.execute_payment(payment_id)
        self.assertEqual(exec_repeat["trxID"], trx_id)

        # 4. Query Payment
        query_res = self.bkash.query_payment(payment_id)
        self.assertEqual(query_res["statusCode"], "0000")
        self.assertEqual(query_res["trxID"], trx_id)

        # 5. Refund Payment
        refund_res = self.bkash.refund_payment(
            payment_id=payment_id,
            trx_id=trx_id,
            amount=5000.0,
            reason="TUTOR_UNAVAILABLE"
        )
        self.assertEqual(refund_res["statusCode"], "0000")
        self.assertTrue(refund_res["refundTrxID"].startswith("RFD"))

    # --------------------------------------------------------------------------
    # 2. Nagad PG RSA-2048 Encryption & Callback Verification
    # --------------------------------------------------------------------------
    def test_nagad_rsa_encryption_and_callback_verification(self):
        order_id = "NGD_ORD_TEST_99"

        # 1. Initialize Payment
        init_res = self.nagad.initialize_payment(
            order_id=order_id,
            amount=6000.0
        )
        self.assertEqual(init_res["status"], "SUCCESS")
        self.assertIsNotNone(init_res["sensitiveData"])
        self.assertIsNotNone(init_res["signature"])
        payment_ref = init_res["paymentReferenceId"]
        self.assertTrue(payment_ref.startswith("NREF"))

        # 2. Verify Callback
        cb_res = self.nagad.verify_callback(
            order_id=order_id,
            payment_ref_id=payment_ref,
            status="SUCCESS"
        )
        self.assertEqual(cb_res["status"], "SUCCESS")
        self.assertTrue(cb_res["issuerPaymentRef"].startswith("NGD"))
        self.assertIsNotNone(cb_res.get("receiptToken"))

        # 3. Query Payment
        q_res = self.nagad.query_payment(order_id)
        self.assertEqual(q_res["status"], "SUCCESS")
        self.assertTrue(q_res["is_verified"])

    # --------------------------------------------------------------------------
    # 3. Dual-Party Tuition Milestone Escrow Lifecycle
    # --------------------------------------------------------------------------
    def test_escrow_deposit_milestone_and_auto_disbursement(self):
        contract_id = "ESC_TEST_TUITION_01"

        # 1. Guardian deposits tuition into escrow
        deposit_res = self.escrow.deposit_tuition_fee(
            contract_id=contract_id,
            guardian_id="usr_guardian_kamal",
            tutor_id="usr_tutor_tanvir",
            amount_bdt=10000.0,
            gateway="BKASH",
            payment_reference="BKH987654321",
            sessions_agreed=10
        )
        self.assertEqual(deposit_res["status"], "ESCROW_DEPOSIT_CONFIRMED")
        self.assertEqual(deposit_res["vault_status"], "HELD_IN_ESCROW")

        # 2. Tutor logs completed session
        log_res = self.escrow.log_teaching_session(
            contract_id=contract_id,
            tutor_id="usr_tutor_tanvir",
            session_number=1,
            topic="Calculus: Limits & Continuity"
        )
        self.assertEqual(log_res["status"], "SESSION_LOGGED_SUCCESSFULLY")
        self.assertEqual(log_res["vault_status"], "SESSION_LOGGED")

        # 3. Guardian approves milestone with auto-disbursement
        approve_res = self.escrow.approve_milestone(
            contract_id=contract_id,
            guardian_id="usr_guardian_kamal",
            session_number=1,
            auto_disburse=True
        )
        self.assertEqual(approve_res["status"], "HONORARIUM_DISBURSED")
        self.assertEqual(approve_res["vault_status"], "FUNDS_DISBURSED")

        # Assert 5% platform fee and 95% net payout
        self.assertEqual(approve_res["gross_amount_bdt"], 10000.0)
        self.assertEqual(approve_res["platform_fee_bdt"], 500.0)   # 5%
        self.assertEqual(approve_res["net_payout_bdt"], 9500.0)    # 95%
        self.assertIsNotNone(approve_res["settlement_hash"])

    # --------------------------------------------------------------------------
    # 4. Escrow Dispute & Arbitration Resolution
    # --------------------------------------------------------------------------
    def test_escrow_dispute_and_arbitration_resolution(self):
        contract_id = "ESC_DISPUTE_02"

        self.escrow.deposit_tuition_fee(
            contract_id=contract_id,
            guardian_id="usr_guardian_02",
            tutor_id="usr_tutor_02",
            amount_bdt=8000.0,
            gateway="NAGAD",
            payment_reference="NGD123456789",
            sessions_agreed=8
        )

        # Guardian raises dispute
        dispute_res = self.escrow.raise_dispute(
            contract_id=contract_id,
            disputant_id="usr_guardian_02",
            reason="Tutor missed 3 scheduled classes without notice."
        )
        self.assertEqual(dispute_res["status"], "ESCROW_DISPUTE_FROZEN")
        self.assertEqual(dispute_res["vault_status"], "DISPUTE_FROZEN")

        # Tutor attempts to log session while frozen -> blocked
        blocked_log = self.escrow.log_teaching_session(
            contract_id=contract_id,
            tutor_id="usr_tutor_02",
            session_number=2,
            topic="Physics"
        )
        self.assertIn("error", blocked_log)

        # Arbitrator reviews and orders 50-50 split
        arbitration_res = self.escrow.resolve_arbitration(
            contract_id=contract_id,
            arbitrator_id="usr_admin_judge",
            decision="SPLIT_50_50",
            resolution_notes="Half of classes verified; remaining half refunded."
        )
        self.assertEqual(arbitration_res["status"], "ARBITRATED_SPLIT_EXECUTED")
        self.assertEqual(arbitration_res["tutor_payout_bdt"], 4000.0)
        self.assertEqual(arbitration_res["guardian_refund_bdt"], 4000.0)

    # --------------------------------------------------------------------------
    # 5. Webhook HMAC-SHA256 Signature & Replay Prevention
    # --------------------------------------------------------------------------
    def test_webhook_hmac_signature_and_replay_protection(self):
        test_payload = {
            "event_type": "PAYMENT_CONFIRMED",
            "trx_id": "BKH_TEST_WH_01",
            "amount": 5000.0
        }
        current_epoch = int(time.time())

        # 1. Valid Signature & Valid Timestamp
        valid_sig = self.webhook.compute_signature(test_payload, current_epoch)
        res_valid = self.webhook.verify_webhook(test_payload, valid_sig, str(current_epoch))
        self.assertTrue(res_valid["is_valid"])
        self.assertEqual(res_valid["status_code"], 200)

        # 2. Missing Signature Header
        res_no_sig = self.webhook.verify_webhook(test_payload, None, str(current_epoch))
        self.assertFalse(res_no_sig["is_valid"])
        self.assertEqual(res_no_sig["error"], "MISSING_SIGNATURE")

        # 3. Missing Timestamp Header
        res_no_ts = self.webhook.verify_webhook(test_payload, valid_sig, None)
        self.assertFalse(res_no_ts["is_valid"])
        self.assertEqual(res_no_ts["error"], "MISSING_TIMESTAMP")

        # 4. Expired Timestamp (> 300 seconds / 5 minutes drift)
        old_epoch = current_epoch - 360  # 6 minutes ago
        old_sig = self.webhook.compute_signature(test_payload, old_epoch)
        res_expired = self.webhook.verify_webhook(test_payload, old_sig, str(old_epoch))
        self.assertFalse(res_expired["is_valid"])
        self.assertEqual(res_expired["error"], "TIMESTAMP_OUT_OF_BOUNDS")

        # 5. Replay Attack of Already Processed Signature
        # The first test already processed valid_sig
        res_replay = self.webhook.verify_webhook(test_payload, valid_sig, str(current_epoch))
        self.assertFalse(res_replay["is_valid"])
        self.assertEqual(res_replay["error"], "REPLAY_ATTACK_DETECTED")

        # 6. Tampered Payload Mismatch
        tampered_payload = {"event_type": "PAYMENT_CONFIRMED", "amount": 999999.0}
        new_epoch = current_epoch + 1
        new_sig = self.webhook.compute_signature(test_payload, new_epoch)
        res_mismatch = self.webhook.verify_webhook(tampered_payload, new_sig, str(new_epoch))
        self.assertFalse(res_mismatch["is_valid"])
        self.assertEqual(res_mismatch["error"], "SIGNATURE_MISMATCH")

    # --------------------------------------------------------------------------
    # 6. Payments Router Verification
    # --------------------------------------------------------------------------
    def test_payment_endpoints_routing(self):
        self.assertIsNotNone(payments_router)
        self.assertTrue(hasattr(payments_router, "routes"))

    # --------------------------------------------------------------------------
    # 7. Strict Zero-Emoji Governance Across Phase 81 Files
    # --------------------------------------------------------------------------
    def test_strict_zero_emoji_governance_across_phase81_files(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files_to_check = [
            os.path.join(base_dir, "app", "services", "payment", "bkash_service.py"),
            os.path.join(base_dir, "app", "services", "payment", "nagad_service.py"),
            os.path.join(base_dir, "app", "services", "payment", "escrow_vault_service.py"),
            os.path.join(base_dir, "app", "services", "payment", "webhook_verifier.py"),
            os.path.join(base_dir, "app", "services", "payment", "__init__.py"),
            os.path.join(base_dir, "app", "api", "v1", "endpoints", "payments.py"),
            os.path.join(os.path.dirname(base_dir), "frontend", "src", "components", "payment", "PaymentModal.tsx"),
            os.path.join(os.path.dirname(base_dir), "frontend", "src", "components", "payment", "EscrowMilestoneCard.tsx"),
            os.path.join(os.path.dirname(base_dir), "frontend", "src", "components", "payment", "index.ts")
        ]

        def contains_emoji(text: str) -> bool:
            for char in text:
                cp = ord(char)
                if (0x1F600 <= cp <= 0x1F64F or
                    0x1F300 <= cp <= 0x1F5FF or
                    0x1F680 <= cp <= 0x1F6FF or
                    0x1F700 <= cp <= 0x1F77F or
                    0x1F780 <= cp <= 0x1F7FF or
                    0x1F800 <= cp <= 0x1F8FF or
                    0x1F900 <= cp <= 0x1F9FF or
                    0x1FA00 <= cp <= 0x1FA6F or
                    0x1FA70 <= cp <= 0x1FAFF or
                    0x2600 <= cp <= 0x26FF or
                    0x2700 <= cp <= 0x27BF):
                    return True
            return False

        for fpath in files_to_check:
            self.assertTrue(os.path.exists(fpath), f"File {fpath} must exist")
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertFalse(contains_emoji(content), f"Rogue emoji detected in {fpath}")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE", content, f"Missing Developer Note in {fpath}")


if __name__ == "__main__":
    unittest.main()
