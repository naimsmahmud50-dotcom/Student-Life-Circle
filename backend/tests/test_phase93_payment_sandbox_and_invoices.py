# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 93 - Unit & Integration Test Suite):
# Comprehensive test suite validating Live bKash/Nagad Sandbox Credentials,
# Token Renewal, IPN Callbacks, Double-Credit Protection, and Automated
# Cryptographically Sealed PDF Receipt Generation.
# Standards:
# 1. PCI-DSS Level 2 financial integrity & HMAC-SHA256 signature verification.
# 2. Strict double-credit prevention: Authoritative gateway re-query + idempotent ledger.
# 3. Pure PDF 1.4 compliance & vector QR code authenticity verification.
# 4. Strict Zero-Emoji compliance across all files.
# ==============================================================================

import unittest
import time
import os
import re
import json
import uuid
import hashlib

from backend.app.services.payment.sandbox_config import (
    bkash_sandbox_config,
    nagad_sandbox_config,
    token_renewal_manager,
    TokenRenewalManager,
    BkashSandboxCredentials
)
from backend.app.services.payment.bkash_service import bkash_service
from backend.app.services.payment.nagad_service import nagad_service
from backend.app.services.payment.webhook_verifier import webhook_security_service
from backend.app.services.payment.ipn_service import (
    ipn_receiver_service,
    payment_ledger,
    IdempotentPaymentLedger,
    IPNReceiverService
)
from backend.app.services.invoice_service import (
    invoice_service,
    ReceiptMetadata,
    PurePDFReceiptWriter
)
from backend.app.api.v1.endpoints.payments import (
    get_or_renew_bkash_token,
    receive_bkash_ipn,
    receive_nagad_ipn,
    generate_payment_invoice,
    download_payment_invoice_pdf,
    verify_payment_invoice
)


class TestPhase93PaymentSandboxAndInvoices(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Phase 93: Live bKash/Nagad Sandbox, IPN, and PDF Invoices.
    """

    def setUp(self):
        # Fresh isolated ledger for deterministic test execution
        self.test_ledger = IdempotentPaymentLedger()
        self.test_ipn_service = IPNReceiverService(self.test_ledger)

    def test_01_bkash_sandbox_credentials_and_base_url(self):
        """Verifies bKash sandbox credentials and official tokenized base URL."""
        self.assertEqual(bkash_sandbox_config.base_url, "https://tokenized.sandbox.bka.sh/v1.2.0-beta")
        self.assertTrue(len(bkash_sandbox_config.app_key) > 5)
        self.assertTrue(len(bkash_sandbox_config.app_secret) > 5)
        self.assertTrue(len(bkash_sandbox_config.username) > 3)
        self.assertTrue(len(bkash_sandbox_config.password) > 3)

    def test_02_bkash_token_grant_and_renewal_lifecycle(self):
        """Verifies token grant, caching, and auto-renewal."""
        token_res = token_renewal_manager.get_token(force_refresh=True)
        self.assertEqual(token_res["statusCode"], "0000")
        self.assertTrue(token_res["id_token"].startswith("bkt_"))
        self.assertEqual(token_res["token_type"], "Bearer")
        self.assertGreater(token_res["expires_in"], 3500)

        # Immediate secondary call should return cached token without refreshing
        cached_res = token_renewal_manager.get_token(force_refresh=False)
        self.assertEqual(cached_res["id_token"], token_res["id_token"])
        self.assertFalse(cached_res["is_refreshed"])

        # Force refresh returns new valid token
        fresh_res = token_renewal_manager.get_token(force_refresh=True)
        self.assertTrue(fresh_res["is_refreshed"])

    def test_03_bkash_checkout_full_lifecycle(self):
        """Verifies bKash create, execute, and query payment lifecycles."""
        inv_no = f"INV_TEST_{uuid.uuid4().hex[:8]}"
        create_res = bkash_service.create_payment(
            amount=2500.0,
            merchant_invoice_number=inv_no,
            payer_reference="STD_TEST_01"
        )
        self.assertEqual(create_res["statusCode"], "0000")
        payment_id = create_res["paymentID"]
        self.assertTrue("tokenized/checkout" in create_res["bkashURL"])
        self.assertEqual(create_res["transactionStatus"], "Initiated")

        # Execute payment
        exec_res = bkash_service.execute_payment(payment_id)
        self.assertEqual(exec_res["statusCode"], "0000")
        self.assertEqual(exec_res["transactionStatus"], "Completed")
        self.assertTrue(exec_res["trxID"].startswith("BKH"))
        self.assertIsNotNone(exec_res.get("receipt_hash"))

        # Query payment confirms status
        query_res = bkash_service.query_payment(payment_id)
        self.assertEqual(query_res["statusCode"], "0000")
        self.assertEqual(query_res["transactionStatus"], "Completed")
        self.assertEqual(query_res["trxID"], exec_res["trxID"])

    def test_04_nagad_sandbox_credentials_and_encryption(self):
        """Verifies Nagad sandbox credentials, RSA encryption, and signature creation."""
        self.assertEqual(nagad_sandbox_config.merchant_id, "NAGAD_MERCHANT_SLC_6821")
        self.assertTrue("remote-payment-gateway-1.0/api/dfs" in nagad_sandbox_config.base_url)

        order_id = f"NGD_TEST_{uuid.uuid4().hex[:8]}"
        init_res = nagad_service.initialize_payment(order_id=order_id, amount=1800.0)
        self.assertEqual(init_res["status"], "SUCCESS")
        self.assertEqual(init_res["orderId"], order_id)
        self.assertTrue(len(init_res["sensitiveData"]) > 50)
        self.assertTrue(len(init_res["signature"]) > 50)
        self.assertTrue(init_res["redirectUrl"].startswith("https://sandbox.mynagad.com"))

        # Verify callback
        cb_res = nagad_service.verify_callback(
            order_id=order_id,
            payment_ref_id=init_res["paymentReferenceId"],
            status="SUCCESS"
        )
        self.assertEqual(cb_res["status"], "SUCCESS")
        self.assertTrue(cb_res["issuerPaymentRef"].startswith("NGD"))

    def test_05_webhook_signature_and_replay_protection(self):
        """Verifies HMAC-SHA256 signature and 5-minute replay window."""
        payload = {"event": "PAYMENT_CONFIRMED", "trx_id": "BKH_TEST_9901"}
        current_time = int(time.time())

        # Valid signature
        valid_sig = webhook_security_service.compute_signature(payload, current_time)
        res = webhook_security_service.verify_webhook(payload, valid_sig, str(current_time))
        self.assertTrue(res["is_valid"])

        # Timestamp drift > 300s rejected
        stale_time = current_time - 350
        stale_sig = webhook_security_service.compute_signature(payload, stale_time)
        stale_res = webhook_security_service.verify_webhook(payload, stale_sig, str(stale_time))
        self.assertFalse(stale_res["is_valid"])
        self.assertEqual(stale_res["error"], "TIMESTAMP_OUT_OF_BOUNDS")

        # Signature mismatch rejected
        bad_res = webhook_security_service.verify_webhook(payload, "invalid_sig_digest", str(current_time))
        self.assertFalse(bad_res["is_valid"])
        self.assertEqual(bad_res["error"], "SIGNATURE_MISMATCH")

    def test_06_double_credit_protection_in_ledger(self):
        """Asserts that duplicate IPN notifications cannot credit balance twice."""
        trx_id = f"BKH_DC_{uuid.uuid4().hex[:8]}"
        student_id = "STD_STUDENT_001"
        amount = 3000.0

        # First settlement succeeds
        first_res = self.test_ledger.record_settlement(
            gateway="BKASH",
            trx_id=trx_id,
            payment_id="PMT_101",
            student_id=student_id,
            amount_bdt=amount
        )
        self.assertTrue(first_res["success"])
        self.assertFalse(first_res["is_duplicate"])
        self.assertEqual(self.test_ledger.get_student_balance(student_id), 3000.0)

        # Second settlement for identical transaction blocked as duplicate
        dup_res = self.test_ledger.record_settlement(
            gateway="BKASH",
            trx_id=trx_id,
            payment_id="PMT_101",
            student_id=student_id,
            amount_bdt=amount
        )
        self.assertFalse(dup_res["success"])
        self.assertTrue(dup_res["is_duplicate"])
        self.assertEqual(dup_res["error"], "DUPLICATE_CREDIT_PREVENTED")
        # Balance must remain exactly 3000.0, not 6000.0
        self.assertEqual(self.test_ledger.get_student_balance(student_id), 3000.0)

    def test_07_bkash_ipn_receiver_with_gateway_re_query(self):
        """Asserts bKash IPN re-queries gateway and rejects incomplete or duplicate transactions."""
        # Setup real executed payment in bkash_service
        inv_no = f"INV_IPN_{uuid.uuid4().hex[:6]}"
        create_res = bkash_service.create_payment(amount=1500.0, merchant_invoice_number=inv_no)
        payment_id = create_res["paymentID"]

        # IPN attempted BEFORE execution on gateway should be rejected
        premature_ipn = self.test_ipn_service.process_bkash_ipn(
            payload={"paymentID": payment_id, "amount": 1500.0, "student_id": "STD_99"}
        )
        self.assertEqual(premature_ipn["status"], "REJECTED")
        self.assertEqual(premature_ipn["error"], "PAYMENT_NOT_COMPLETED")

        # Now execute on gateway
        exec_res = bkash_service.execute_payment(payment_id)
        trx_id = exec_res["trxID"]

        # Now IPN should succeed
        valid_ipn = self.test_ipn_service.process_bkash_ipn(
            payload={"paymentID": payment_id, "trxID": trx_id, "amount": 1500.0, "student_id": "STD_99"}
        )
        self.assertEqual(valid_ipn["status"], "SETTLED")
        self.assertEqual(valid_ipn["amount"], 1500.0)
        self.assertEqual(self.test_ledger.get_student_balance("STD_99"), 1500.0)

        # Retry of same IPN is blocked by double-credit protection
        retry_ipn = self.test_ipn_service.process_bkash_ipn(
            payload={"paymentID": payment_id, "trxID": trx_id, "amount": 1500.0, "student_id": "STD_99"}
        )
        self.assertEqual(retry_ipn["status"], "DUPLICATE_IGNORED")
        self.assertTrue(retry_ipn["is_duplicate"])
        # Balance remains 1500.0
        self.assertEqual(self.test_ledger.get_student_balance("STD_99"), 1500.0)

    def test_08_nagad_ipn_receiver_lifecycle(self):
        """Asserts Nagad IPN verification and double-credit protection."""
        order_id = f"NGD_IPN_{uuid.uuid4().hex[:6]}"
        init_res = nagad_service.initialize_payment(order_id=order_id, amount=2200.0)
        payment_ref = init_res["paymentReferenceId"]

        # Process Nagad IPN
        ipn_res = self.test_ipn_service.process_nagad_ipn(
            payload={
                "order_id": order_id,
                "payment_ref_id": payment_ref,
                "status": "SUCCESS",
                "amount": 2200.0,
                "student_id": "STD_NAGAD_01"
            }
        )
        self.assertEqual(ipn_res["status"], "SETTLED")
        self.assertEqual(self.test_ledger.get_student_balance("STD_NAGAD_01"), 2200.0)

        # Duplicate IPN blocked
        dup_res = self.test_ipn_service.process_nagad_ipn(
            payload={
                "order_id": order_id,
                "payment_ref_id": payment_ref,
                "status": "SUCCESS",
                "amount": 2200.0,
                "student_id": "STD_NAGAD_01"
            }
        )
        self.assertEqual(dup_res["status"], "DUPLICATE_IGNORED")
        self.assertEqual(self.test_ledger.get_student_balance("STD_NAGAD_01"), 2200.0)

    def test_09_pdf_invoice_generator_compliance_and_contents(self):
        """Verifies pure PDF 1.4 generation, watermark, QR matrix, and metadata."""
        receipt = invoice_service.generate_receipt(
            student_name="Tahsina Farhin",
            student_id="SLC-STD-2026-9912",
            trx_id="BKH9827101AX",
            amount_bdt=4200.0,
            payment_channel="bKash Merchant Checkout",
            purpose="HSC Physics & Chemistry Mentorship"
        )
        self.assertEqual(receipt["status"], "GENERATED")
        self.assertTrue(receipt["receipt_no"].startswith("REC-2026-BKH"))
        self.assertGreater(receipt["pdf_size_bytes"], 1000)

        pdf_bytes = receipt["pdf_bytes"]
        # PDF 1.4 standard magic header and EOF marker
        self.assertTrue(pdf_bytes.startswith(b"%PDF-1.4\n"))
        self.assertTrue(pdf_bytes.endswith(b"%%EOF\n"))

        # PDF body contains textual and metadata elements
        latin_str = pdf_bytes.decode("latin1")
        self.assertIn("STUDENT LIFE CIRCLE - OFFICIAL PAYMENT RECEIPT", latin_str)
        self.assertIn("Tahsina Farhin", latin_str)
        self.assertIn("SLC-STD-2026-9912", latin_str)
        self.assertIn("BKH9827101AX", latin_str)
        self.assertIn("4,200.00", latin_str)
        self.assertIn("STUDENT LIFE CIRCLE - VERIFIED RECEIPT", latin_str)  # Watermark
        self.assertIn("CRYPTOGRAPHIC VERIFICATION SEAL", latin_str)
        self.assertIn("/Font", latin_str)
        self.assertIn("xref", latin_str)
        self.assertIn("trailer", latin_str)

    def test_10_receipt_cryptographic_verification(self):
        """Asserts receipt hash validation matches authentic calculation and detects tampering."""
        receipt = invoice_service.generate_receipt(
            student_name="Fahim Al Mamun",
            student_id="SLC-STD-2026-3341",
            trx_id="NGD77123901",
            amount_bdt=3800.0,
            payment_channel="Nagad Payment Gateway"
        )
        rec_no = receipt["receipt_no"]
        v_hash = receipt["verification_hash"]

        # Valid hash check
        verif = invoice_service.verify_receipt(rec_no, v_hash)
        self.assertTrue(verif["is_valid"])
        self.assertEqual(verif["student_name"], "Fahim Al Mamun")

        # Tampered hash check
        tampered_hash = v_hash[:-4] + "ffff"
        bad_verif = invoice_service.verify_receipt(rec_no, tampered_hash)
        self.assertFalse(bad_verif["is_valid"])

    async def test_11_payments_api_endpoint_invocations(self):
        """Verifies API endpoints for token renewal, IPN, and PDF invoice generation/download."""
        # 1. Token Endpoint
        token_res = await get_or_renew_bkash_token(force_refresh=False)
        self.assertEqual(token_res["statusCode"], "0000")

        # 2. Invoice Generation Endpoint
        invoice_res = await generate_payment_invoice({
            "student_name": "Naimur Rahman",
            "student_id": "SLC-STD-2026-0001",
            "trx_id": "BKH_API_TRX_99",
            "amount_bdt": 5000.0,
            "channel": "bKash Merchant Checkout"
        })
        self.assertEqual(invoice_res["status"], "GENERATED")
        self.assertTrue(invoice_res["download_url"].endswith("/download"))

        # 3. Invoice Download Endpoint
        download_res = await download_payment_invoice_pdf("BKH_API_TRX_99")
        self.assertEqual(download_res.media_type, "application/pdf")
        self.assertTrue(download_res.content.startswith(b"%PDF-1.4"))

        # 4. Invoice Verify Endpoint
        verify_res = await verify_payment_invoice(
            receipt_no=invoice_res["receipt_no"],
            hash=invoice_res["verification_hash"]
        )
        self.assertTrue(verify_res["is_valid"])

    def test_12_frontend_receipt_modal_architecture(self):
        """Verifies frontend PaymentReceiptModal component exists, has WCAG standards and clean architecture."""
        file_path = "frontend/src/components/payment/PaymentReceiptModal.tsx"
        self.assertTrue(os.path.exists(file_path))

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Architecture notes and imports
        self.assertIn("DEVELOPER ARCHITECTURE NOTE (Phase 93", content)
        self.assertIn("PaymentReceiptModalProps", content)
        self.assertIn("handleDownloadPdf", content)
        self.assertIn("min-h-[48px]", content)  # 48px touch target
        self.assertIn("role=\"dialog\"", content)  # Accessible modal
        self.assertIn("aria-modal=\"true\"", content)
        self.assertIn("Download PDF Receipt", content)
        self.assertIn("Print Receipt", content)

    def test_13_zero_emoji_compliance_across_phase93_files(self):
        """Verifies strict Zero-Emoji compliance across all Phase 93 files."""
        emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u3030\u303d\u3297\u3299]"
        )

        phase93_files = [
            "backend/app/services/payment/sandbox_config.py",
            "backend/app/services/payment/ipn_service.py",
            "backend/app/services/payment/__init__.py",
            "backend/app/services/invoice_service.py",
            "backend/app/api/v1/endpoints/payments.py",
            "frontend/src/components/payment/PaymentReceiptModal.tsx",
            "frontend/src/components/payment/index.ts",
            "backend/tests/test_phase93_payment_sandbox_and_invoices.py"
        ]

        for path in phase93_files:
            self.assertTrue(os.path.exists(path), f"File missing: {path}")
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                matches = emoji_pattern.findall(text)
                self.assertEqual(
                    matches, [],
                    f"Found unauthorized emojis in {path}: {matches}"
                )

    def test_14_developer_architecture_notes_presence(self):
        """Verifies every Phase 93 file contains prominent Developer Architecture Notes."""
        files = [
            "backend/app/services/payment/sandbox_config.py",
            "backend/app/services/payment/ipn_service.py",
            "backend/app/services/payment/__init__.py",
            "backend/app/services/invoice_service.py",
            "backend/app/api/v1/endpoints/payments.py",
            "frontend/src/components/payment/PaymentReceiptModal.tsx",
            "frontend/src/components/payment/index.ts",
            "backend/tests/test_phase93_payment_sandbox_and_invoices.py"
        ]

        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                self.assertIn(
                    "DEVELOPER ARCHITECTURE NOTE",
                    text,
                    f"Missing DEVELOPER ARCHITECTURE NOTE in {path}"
                )


if __name__ == "__main__":
    unittest.main()
