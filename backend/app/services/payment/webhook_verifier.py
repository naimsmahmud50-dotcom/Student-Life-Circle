# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 81 - Webhook Signature & Replay Prevention):
# This service enforces cryptographic webhook validation and replay prevention for
# all inbound payment events (bKash IPN, Nagad callbacks, escrow triggers).
# Security Standards:
# 1. HMAC-SHA256 Signature Verification: Validates the X-Signature header using the
#    platform webhook secret.
# 2. Strict 5-Minute Timestamp Window: Enforces that X-Timestamp is within +/- 300 seconds
#    of server clock time to thwart network replay attacks.
# 3. Nonce Tracking & Idempotency: Maintains an in-memory cache of seen nonces / signature
#    digests with automatic 10-minute TTL cleanup.
# 4. Strict Zero-Emoji Governance: All comments, log messages, and error codes use clean technical text.
# ==============================================================================

import os
import time
import hmac
import hashlib
import json
from typing import Dict, Any, Optional, Set
from datetime import datetime, timezone


class WebhookSecurityService:
    """
    Cryptographic webhook signature validator and replay attack defense engine.
    """

    MAX_TIMESTAMP_DRIFT_SECONDS = 300  # 5 minutes replay window

    def __init__(self, webhook_secret: Optional[str] = None):
        self.webhook_secret = webhook_secret or os.getenv("WEBHOOK_SIGNING_SECRET", "whsec_slc_payment_secret_2026")
        self._processed_signatures: Dict[str, float] = {}

    def compute_signature(self, payload: Dict[str, Any], timestamp_epoch: int) -> str:
        """
        Generates canonical HMAC-SHA256 signature over stringified JSON payload and timestamp.
        """
        canonical_str = json.dumps(payload, sort_keys=True)
        message = f"{timestamp_epoch}.{canonical_str}"
        return hmac.new(
            self.webhook_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def verify_webhook(
        self,
        payload: Dict[str, Any],
        signature: Optional[str],
        timestamp_header: Optional[str]
    ) -> Dict[str, Any]:
        """
        Validates webhook signature and checks for replay attacks.
        Returns validation verdict and diagnostic code.
        """
        # 1. Check Missing Headers
        if not signature:
            return {
                "is_valid": False,
                "error": "MISSING_SIGNATURE",
                "message": "Missing required X-Signature header.",
                "status_code": 401
            }

        if not timestamp_header:
            return {
                "is_valid": False,
                "error": "MISSING_TIMESTAMP",
                "message": "Missing required X-Timestamp header.",
                "status_code": 400
            }

        # 2. Verify Timestamp Window (5 minutes / 300 seconds)
        try:
            timestamp_epoch = int(timestamp_header)
        except ValueError:
            return {
                "is_valid": False,
                "error": "INVALID_TIMESTAMP_FORMAT",
                "message": "X-Timestamp must be an integer Unix epoch timestamp.",
                "status_code": 400
            }

        current_epoch = int(time.time())
        drift = abs(current_epoch - timestamp_epoch)

        if drift > self.MAX_TIMESTAMP_DRIFT_SECONDS:
            return {
                "is_valid": False,
                "error": "TIMESTAMP_OUT_OF_BOUNDS",
                "message": f"Webhook timestamp drift ({drift}s) exceeds maximum allowed window ({self.MAX_TIMESTAMP_DRIFT_SECONDS}s). Replay attack mitigated.",
                "status_code": 403
            }

        # 3. Check for Replay of Identical Signature
        self._cleanup_expired_nonces()
        if signature in self._processed_signatures:
            return {
                "is_valid": False,
                "error": "REPLAY_ATTACK_DETECTED",
                "message": "This webhook signature has already been processed within the active window.",
                "status_code": 409
            }

        # 4. Verify HMAC-SHA256 Signature Match
        expected_sig = self.compute_signature(payload, timestamp_epoch)
        if not hmac.compare_digest(expected_sig, signature):
            return {
                "is_valid": False,
                "error": "SIGNATURE_MISMATCH",
                "message": "Calculated signature does not match X-Signature header.",
                "status_code": 403
            }

        # Record signature to prevent replay
        self._processed_signatures[signature] = time.time()

        return {
            "is_valid": True,
            "message": "Webhook signature and timestamp validated successfully.",
            "timestamp": timestamp_epoch,
            "status_code": 200
        }

    def _cleanup_expired_nonces(self):
        """Evicts signatures older than 10 minutes from memory."""
        now = time.time()
        expired = [sig for sig, ts in self._processed_signatures.items() if (now - ts) > 600]
        for sig in expired:
            del self._processed_signatures[sig]


# Global Webhook Security Service Instance
webhook_security_service = WebhookSecurityService()
