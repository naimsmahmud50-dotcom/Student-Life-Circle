import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional, Tuple


class DatabaseWebhookReplayGuardService:
    """
    Svix-compatible Webhook Signature Verification and Anti-Replay Shield for Supabase Database Webhooks.
    Protects against captured replay attacks, forged webhook callbacks, and timestamp manipulation.
    """

    DEFAULT_SECRET = "whsec_supa_db_webhook_secret_key_2026_salt"
    MAX_CLOCK_SKEW_SECONDS = 60
    DEFAULT_MAX_AGE_SECONDS = 300  # 5 minutes sliding replay window

    def __init__(self, secret: str = DEFAULT_SECRET):
        self.secret = secret
        # Map of msg_id -> timestamp recorded, with auto-pruning
        self._processed_messages: Dict[str, float] = {}

    def _cleanup_expired_messages(self, current_time: float, max_age: int) -> None:
        """Prunes messages older than 2 * max_age to prevent unbounded memory growth."""
        cutoff = current_time - (max_age * 2)
        expired_keys = [
            k for k, v in self._processed_messages.items() if v < cutoff
        ]
        for k in expired_keys:
            del self._processed_messages[k]

    def sign_test_webhook(
        self,
        msg_id: str,
        timestamp: int,
        payload_str: str,
        secret: Optional[str] = None,
    ) -> str:
        """
        Generates a valid Svix-style v1 signature string for a webhook payload: 'v1,<signature>'.
        Signing string: '{msg_id}.{timestamp}.{payload_str}'
        """
        active_secret = secret or self.secret
        raw_secret = active_secret
        if raw_secret.startswith("whsec_"):
            raw_secret = raw_secret[6:]

        to_sign = f"{msg_id}.{timestamp}.{payload_str}".encode("utf-8")
        computed_sig = hmac.new(
            raw_secret.encode("utf-8"), to_sign, hashlib.sha256
        ).digest()
        encoded = base64.b64encode(computed_sig).decode("utf-8")
        return f"v1,{encoded}"

    def verify_webhook_signature(
        self,
        headers: Dict[str, str],
        payload_bytes: bytes,
        secret: Optional[str] = None,
        max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
    ) -> Dict[str, Any]:
        """
        Validates Svix/Supabase webhook headers, authenticates HMAC-SHA256 signature,
        and enforces anti-replay timestamp & nonce checks.
        """
        active_secret = secret or self.secret
        raw_secret = active_secret
        if raw_secret.startswith("whsec_"):
            raw_secret = raw_secret[6:]

        normalized = {k.lower(): v for k, v in headers.items()}
        msg_id = (
            normalized.get("webhook-id")
            or normalized.get("svix-id")
            or normalized.get("x-supabase-event-id")
        )
        timestamp_str = (
            normalized.get("webhook-timestamp")
            or normalized.get("svix-timestamp")
            or normalized.get("x-supabase-event-timestamp")
        )
        sig_header = (
            normalized.get("webhook-signature")
            or normalized.get("svix-signature")
            or normalized.get("x-supabase-event-signature")
        )

        if not msg_id or not timestamp_str or not sig_header:
            return {
                "verified": False,
                "reason": "Missing required webhook headers (id, timestamp, or signature)",
                "error_code": "MISSING_HEADERS",
                "msg_id": msg_id,
            }

        # 1. Validate Timestamp & Anti-Replay
        try:
            ts = int(timestamp_str)
        except ValueError:
            return {
                "verified": False,
                "reason": "Webhook timestamp must be an integer unix epoch",
                "error_code": "INVALID_TIMESTAMP",
                "msg_id": msg_id,
            }

        now = int(time.time())
        # Check future timestamp (clock skew limit)
        if ts > now + self.MAX_CLOCK_SKEW_SECONDS:
            return {
                "verified": False,
                "reason": f"Webhook timestamp is in the future ({ts} > {now + self.MAX_CLOCK_SKEW_SECONDS})",
                "error_code": "FUTURE_TIMESTAMP_REJECTED",
                "msg_id": msg_id,
            }

        # Check expired timestamp (replay window)
        if now - ts > max_age_seconds:
            return {
                "verified": False,
                "reason": f"Webhook event expired ({now - ts}s old > max allowed {max_age_seconds}s)",
                "error_code": "REPLAY_WINDOW_EXPIRED",
                "msg_id": msg_id,
            }

        # 2. Check Duplicate Nonce / msg_id
        self._cleanup_expired_messages(now, max_age_seconds)
        if msg_id in self._processed_messages:
            return {
                "verified": False,
                "reason": f"Duplicate webhook message ID '{msg_id}' detected; possible replay attack",
                "error_code": "DUPLICATE_MESSAGE_REPLAY",
                "msg_id": msg_id,
            }

        # 3. Compute and Verify HMAC Signature
        payload_str = payload_bytes.decode("utf-8", errors="replace")
        to_sign = f"{msg_id}.{ts}.{payload_str}".encode("utf-8")
        expected_digest = hmac.new(
            raw_secret.encode("utf-8"), to_sign, hashlib.sha256
        ).digest()
        expected_b64 = base64.b64encode(expected_digest).decode("utf-8")
        expected_hex = expected_digest.hex()

        # Webhook signature header may contain space-separated candidate signatures (e.g. "v1,abc v1,def")
        passed = False
        candidates = sig_header.split(" ")
        for candidate in candidates:
            parts = candidate.split(",", 1)
            if len(parts) == 2 and parts[0] == "v1":
                sig_val = parts[1]
                if hmac.compare_digest(sig_val, expected_b64) or hmac.compare_digest(sig_val, expected_hex):
                    passed = True
                    break

        if not passed:
            return {
                "verified": False,
                "reason": "Cryptographic webhook HMAC-SHA256 signature mismatch",
                "error_code": "SIGNATURE_MISMATCH",
                "msg_id": msg_id,
            }

        # Record message ID in processed cache to block replay attacks
        self._processed_messages[msg_id] = now

        return {
            "verified": True,
            "reason": "Webhook authenticated and verified against replay attacks",
            "error_code": None,
            "msg_id": msg_id,
            "timestamp": ts,
            "latency_seconds": now - ts,
        }

    def attest_and_record_event(
        self,
        event_type: str,
        table_name: str,
        record_id: str,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Creates an immutable, cryptographically attested receipt for a processed database event.
        """
        payload_json = json.dumps(payload, sort_keys=True)
        payload_sha256 = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        now = int(time.time())
        attestation_id = f"attest_{hashlib.sha256(f'{event_type}:{table_name}:{record_id}:{now}'.encode()).hexdigest()[:16]}"

        receipt_input = f"{attestation_id}:{event_type}:{table_name}:{record_id}:{payload_sha256}:{now}"
        receipt_sig = hmac.new(
            self.secret.encode("utf-8"), receipt_input.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return {
            "attestation_id": attestation_id,
            "event_type": event_type,
            "table_name": table_name,
            "record_id": record_id,
            "payload_sha256": payload_sha256,
            "verified_at": now,
            "attestation_signature": f"att_v1_{receipt_sig[:32]}",
            "status": "ATTESTED_VALID",
        }
