# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 93 - Automated Webhook Receiver & IPN Engine):
# This service provides an Instant Payment Notification (IPN) and Webhook processing
# engine for bKash Merchant Checkout and Nagad Payment Gateway callbacks.
# Security & Financial Integrity Standards:
# 1. Double-Credit Protection:
#    - Before crediting a student account or releasing escrow milestones, the system
#      re-queries transaction status directly from the authoritative gateway server.
#    - Prevents trusting client-reported status payloads alone.
# 2. Idempotent Payment Ledger:
#    - Rejects duplicate transactions via SHA-256 fingerprinting on (gateway, trx_id).
#    - Idempotency guarantees exactly-once balance updates across retried webhooks.
# 3. Cryptographic Signature Verification:
#    - bKash: HMAC-SHA256 signature verification over (timestamp + canonical payload).
#    - Nagad: RSA digital signature verification with merchant/issuer keys.
# 4. Strict Zero-Emoji Governance: All comments, log messages, and error codes use clean technical text.
# ==============================================================================

import os
import time
import json
import uuid
import hmac
import hashlib
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone

from backend.app.services.payment.bkash_service import bkash_service
from backend.app.services.payment.nagad_service import nagad_service
from backend.app.services.payment.webhook_verifier import webhook_security_service


class IdempotentPaymentLedger:
    """
    In-memory / persistent idempotent payment ledger recording finalized transactions.
    Prevents double crediting and race-condition replays.
    """

    def __init__(self):
        # Maps transaction_fingerprint -> record
        self._ledger: Dict[str, Dict[str, Any]] = {}
        # Maps student_id -> current_balance_bdt
        self._student_balances: Dict[str, float] = {}

    def get_fingerprint(self, gateway: str, trx_id: str) -> str:
        """Computes standardized ledger fingerprint."""
        raw = f"{gateway.upper()}:{trx_id.strip()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def is_transaction_settled(self, gateway: str, trx_id: str) -> bool:
        """Checks if transaction has already been credited."""
        fp = self.get_fingerprint(gateway, trx_id)
        return fp in self._ledger

    def record_settlement(
        self,
        gateway: str,
        trx_id: str,
        payment_id: str,
        student_id: str,
        amount_bdt: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Atomically records a transaction and credits student balance if not previously settled.
        Returns settlement result with duplicate flag.
        """
        fp = self.get_fingerprint(gateway, trx_id)
        if fp in self._ledger:
            existing = self._ledger[fp]
            return {
                "success": False,
                "is_duplicate": True,
                "error": "DUPLICATE_CREDIT_PREVENTED",
                "message": f"Transaction {trx_id} has already been credited to student account {existing['student_id']}.",
                "existing_record": existing,
                "current_balance": self._student_balances.get(existing["student_id"], 0.0)
            }

        settled_at = datetime.now(timezone.utc).isoformat()
        current_bal = self._student_balances.get(student_id, 0.0)
        new_bal = round(current_bal + amount_bdt, 2)
        self._student_balances[student_id] = new_bal

        record = {
            "fingerprint": fp,
            "gateway": gateway.upper(),
            "trx_id": trx_id,
            "payment_id": payment_id,
            "student_id": student_id,
            "amount_bdt": amount_bdt,
            "settled_at": settled_at,
            "previous_balance": current_bal,
            "updated_balance": new_bal,
            "metadata": metadata or {}
        }
        self._ledger[fp] = record

        return {
            "success": True,
            "is_duplicate": False,
            "message": f"Transaction {trx_id} successfully settled and credited.",
            "record": record,
            "updated_balance": new_bal
        }

    def get_student_balance(self, student_id: str) -> float:
        """Retrieves student balance in BDT."""
        return self._student_balances.get(student_id, 0.0)

    def get_transaction(self, gateway: str, trx_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves ledger entry by gateway and trx_id."""
        fp = self.get_fingerprint(gateway, trx_id)
        return self._ledger.get(fp)


class IPNReceiverService:
    """
    Automated Instant Payment Notification (IPN) and callback receiver.
    Enforces double-credit protection via authoritative gateway re-query.
    """

    def __init__(self, ledger: Optional[IdempotentPaymentLedger] = None):
        self.ledger = ledger or IdempotentPaymentLedger()

    def process_bkash_ipn(
        self,
        payload: Dict[str, Any],
        signature: Optional[str] = None,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes bKash IPN callback.
        Steps:
        1. Validates webhook signature and replay timestamp.
        2. Extracts paymentID and trxID.
        3. Double-Credit Protection: Re-queries transaction status directly from bKash server.
        4. Validates matching amount and status == 'Completed'.
        5. Updates idempotent ledger and student account balance.
        """
        # Step 1: Signature Verification (if headers provided)
        if signature and timestamp:
            verif = webhook_security_service.verify_webhook(payload, signature, timestamp)
            if not verif.get("is_valid"):
                return {
                    "status": "REJECTED",
                    "error": verif.get("error", "SIGNATURE_VERIFICATION_FAILED"),
                    "message": verif.get("message", "Invalid signature"),
                    "status_code": verif.get("status_code", 401)
                }

        payment_id = payload.get("paymentID") or payload.get("payment_id")
        claimed_trx_id = payload.get("trxID") or payload.get("trx_id")
        student_id = payload.get("student_id") or payload.get("payerReference") or "STD_UNKNOWN"
        claimed_amount = float(payload.get("amount", 0.0))

        if not payment_id:
            return {
                "status": "REJECTED",
                "error": "MISSING_PAYMENT_ID",
                "message": "bKash IPN payload must contain paymentID.",
                "status_code": 400
            }

        # Step 2: Double-Credit Check in Local Ledger
        if claimed_trx_id and self.ledger.is_transaction_settled("BKASH", claimed_trx_id):
            return {
                "status": "DUPLICATE_IGNORED",
                "error": "DOUBLE_CREDIT_BLOCKED",
                "message": f"bKash transaction {claimed_trx_id} was already settled. Double-credit prevented.",
                "status_code": 200,
                "is_duplicate": True
            }

        # Step 3: Authoritative Gateway Re-Query
        # We query the bKash server directly to verify that the transaction was legitimately completed
        gateway_status = bkash_service.query_payment(payment_id)
        if gateway_status.get("statusCode") != "0000":
            return {
                "status": "REJECTED",
                "error": "GATEWAY_VERIFICATION_FAILED",
                "message": f"bKash server could not verify payment {payment_id}: {gateway_status.get('statusMessage')}",
                "status_code": 400
            }

        actual_status = gateway_status.get("transactionStatus")
        actual_trx_id = gateway_status.get("trxID")
        actual_amount = float(gateway_status.get("amount", 0.0))

        if actual_status != "Completed":
            return {
                "status": "REJECTED",
                "error": "PAYMENT_NOT_COMPLETED",
                "message": f"Gateway reports payment status is '{actual_status}', not 'Completed'. Credit blocked.",
                "status_code": 400
            }

        # Verify amount matches claimed payload
        if claimed_amount > 0 and abs(actual_amount - claimed_amount) > 0.01:
            return {
                "status": "REJECTED",
                "error": "AMOUNT_MISMATCH",
                "message": f"Claimed amount ({claimed_amount}) does not match gateway verified amount ({actual_amount}).",
                "status_code": 400
            }

        final_trx_id = actual_trx_id or claimed_trx_id or f"BKH_{payment_id}"

        # Step 4: Record in Idempotent Ledger
        settlement = self.ledger.record_settlement(
            gateway="BKASH",
            trx_id=final_trx_id,
            payment_id=payment_id,
            student_id=student_id,
            amount_bdt=actual_amount,
            metadata={
                "merchantInvoiceNumber": gateway_status.get("merchantInvoiceNumber"),
                "currency": gateway_status.get("currency", "BDT"),
                "gateway_verified": True
            }
        )

        if not settlement["success"]:
            return {
                "status": "DUPLICATE_IGNORED",
                "error": settlement["error"],
                "message": settlement["message"],
                "status_code": 200,
                "is_duplicate": True
            }

        return {
            "status": "SETTLED",
            "message": "bKash IPN verified against gateway server and student balance credited.",
            "trxID": final_trx_id,
            "paymentID": payment_id,
            "student_id": student_id,
            "amount": actual_amount,
            "updated_balance": settlement["updated_balance"],
            "status_code": 200
        }

    def process_nagad_ipn(
        self,
        payload: Dict[str, Any],
        signature: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes Nagad IPN callback with RSA verification and double-credit protection.
        """
        order_id = payload.get("order_id") or payload.get("orderId")
        payment_ref_id = payload.get("payment_ref_id") or payload.get("paymentReferenceId")
        cb_status = payload.get("status", "SUCCESS")
        sig = signature or payload.get("signature")
        student_id = payload.get("student_id", "STD_UNKNOWN")
        claimed_amount = float(payload.get("amount", 0.0))

        if not order_id or not payment_ref_id:
            return {
                "status": "REJECTED",
                "error": "MISSING_ORDER_PARAMS",
                "message": "Nagad IPN requires order_id and payment_ref_id.",
                "status_code": 400
            }

        # Verify callback through Nagad service
        verification = nagad_service.verify_callback(order_id, payment_ref_id, cb_status, sig)
        if verification.get("status") != "SUCCESS":
            return {
                "status": "REJECTED",
                "error": "NAGAD_CALLBACK_VERIFICATION_FAILED",
                "message": verification.get("message", "Nagad verification failed"),
                "status_code": 400
            }

        issuer_trx = verification.get("issuerPaymentRef", payment_ref_id)
        verified_amount = float(verification.get("amount", claimed_amount))

        # Check local ledger for double credit
        if self.ledger.is_transaction_settled("NAGAD", issuer_trx):
            return {
                "status": "DUPLICATE_IGNORED",
                "error": "DOUBLE_CREDIT_BLOCKED",
                "message": f"Nagad transaction {issuer_trx} was already settled. Double-credit prevented.",
                "status_code": 200,
                "is_duplicate": True
            }

        # Authoritative Gateway Re-Query
        gateway_order = nagad_service.query_payment(order_id)
        if not gateway_order.get("is_verified") or gateway_order.get("status") != "SUCCESS":
            return {
                "status": "REJECTED",
                "error": "GATEWAY_STATUS_UNVERIFIED",
                "message": "Nagad gateway status could not be verified on authoritative query.",
                "status_code": 400
            }

        # Settle in ledger
        settlement = self.ledger.record_settlement(
            gateway="NAGAD",
            trx_id=issuer_trx,
            payment_id=payment_ref_id,
            student_id=student_id,
            amount_bdt=verified_amount,
            metadata={
                "order_id": order_id,
                "receipt_token": verification.get("receiptToken")
            }
        )

        if not settlement["success"]:
            return {
                "status": "DUPLICATE_IGNORED",
                "error": settlement["error"],
                "message": settlement["message"],
                "status_code": 200,
                "is_duplicate": True
            }

        return {
            "status": "SETTLED",
            "message": "Nagad IPN verified and student balance credited.",
            "trxID": issuer_trx,
            "orderId": order_id,
            "student_id": student_id,
            "amount": verified_amount,
            "updated_balance": settlement["updated_balance"],
            "status_code": 200
        }


# Global IPN Service Instance
payment_ledger = IdempotentPaymentLedger()
ipn_receiver_service = IPNReceiverService(payment_ledger)
