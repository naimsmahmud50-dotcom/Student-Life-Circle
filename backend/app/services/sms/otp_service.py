# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 82 - Cryptographic SMS OTP Service):
# This service generates and verifies cryptographically secure 6-digit numeric
# One-Time Passwords (OTPs) with a strict 3-minute Time-To-Live (TTL) stored in
# Redis (with resilient in-memory fallback via CacheService).
#
# Security Invariants & Features:
# 1. Cryptographic Randomness: Uses Python's `secrets.randbelow()` to eliminate
#    predictability and pseudo-random seed vulnerabilities.
# 2. Hash-at-Rest Storage: Stores the SHA-256 digest of the OTP rather than raw
#    digits in Redis/cache, mitigating risks from memory/cache dumps.
# 3. Single-Use Replay Prevention: The OTP key is purged immediately upon successful
#    verification or upon reaching maximum failed attempts (3 attempts).
# 4. Anti-SMS-Bombing Rate Limits: Mandates verification against the 3-requests-per-
#    15-minutes quota before any dispatch is executed.
# 5. Bangla Unicode Notification: Dispatches formatted Bangla SMS with security warnings.
# 6. Zero-Emoji Policy Enforced: Strictly uses clean technical text and Lucide icons.
# ==============================================================================

import time
import secrets
import hashlib
import hmac
from typing import Dict, Any, Optional

from backend.app.services.sms.adapters import (
    normalize_bd_phone,
    mask_phone_for_logging
)
from backend.app.services.sms.sms_gateway_service import sms_gateway_service
from backend.app.services.cache_service import cache_service

# Configuration constants
OTP_TTL_SECONDS = 180  # 3 minutes
MAX_VERIFICATION_ATTEMPTS = 3


class OTPService:
    """
    Cryptographic OTP generator and verifier with Redis/CacheService integration.
    """

    def __init__(self, ttl_seconds: int = OTP_TTL_SECONDS):
        self.ttl_seconds = ttl_seconds
        self._audit_records = []

    def _hash_otp(self, otp_digits: str) -> str:
        """Computes SHA-256 hash of OTP string."""
        return hashlib.sha256(otp_digits.encode("utf-8")).hexdigest()

    async def generate_and_send_otp(
        self,
        phone: str,
        purpose: str = "LOGIN",
        user_id: Optional[str] = None,
        return_raw_for_testing: bool = False
    ) -> Dict[str, Any]:
        """
        Generates a 6-digit numeric OTP, enforces rate limits, caches the SHA-256 hash,
        and dispatches via the SMS Gateway.
        """
        norm_phone = normalize_bd_phone(phone)
        if len(norm_phone) < 11:
            return {
                "success": False,
                "error": "INVALID_PHONE_NUMBER",
                "phone": phone
            }

        # 1. Enforce Rate Limiting (max 3 requests per 15 min)
        is_allowed, attempts, retry_after = await sms_gateway_service.check_and_increment_rate_limit(norm_phone)
        if not is_allowed:
            return {
                "success": False,
                "error": "RATE_LIMIT_EXCEEDED",
                "message": f"Maximum OTP requests reached. Please wait {retry_after} seconds.",
                "retry_after_seconds": retry_after,
                "attempts": attempts
            }

        # 2. Cryptographic 6-digit OTP generation (100000 to 999999)
        otp_num = secrets.randbelow(900000) + 100000
        otp_str = str(otp_num)
        otp_hash = self._hash_otp(otp_str)

        # 3. Store in Redis/CacheService with 3-minute TTL
        cache_key = f"otp:{norm_phone}"
        cache_data = {
            "otp_hash": otp_hash,
            "purpose": purpose,
            "user_id": user_id,
            "failed_attempts": 0,
            "created_at": time.time(),
            "expires_at": time.time() + self.ttl_seconds
        }
        await cache_service.set(cache_key, cache_data, ttl_seconds=self.ttl_seconds)

        # 4. Compose Bangla Unicode Message
        bangla_message = (
            f"স্টুডেন্ট লাইফ সার্কেল ভেরিফিকেশন কোড: {otp_str}। "
            f"মেয়াদ ৩ মিনিট। কোডটি কারো সাথে শেয়ার করবেন না।"
        )

        # 5. Dispatch SMS
        dispatch_res = await sms_gateway_service.send_sms(
            to_phone=norm_phone,
            message=bangla_message,
            sender_id="StudentLife",
            is_masked=True
        )

        # 6. Audit logging
        self._record_audit(
            action="SMS_OTP_REQUESTED",
            phone=norm_phone,
            purpose=purpose,
            status="SUCCESS" if dispatch_res.get("success") else "DISPATCH_FAILED",
            details={"provider": dispatch_res.get("provider")}
        )

        response = {
            "success": dispatch_res.get("success", False),
            "recipient": mask_phone_for_logging(norm_phone),
            "purpose": purpose,
            "expires_in_seconds": self.ttl_seconds,
            "provider": dispatch_res.get("provider")
        }

        # For automated integration testing environments
        if return_raw_for_testing:
            response["raw_otp_testing_only"] = otp_str

        return response

    async def verify_otp(
        self,
        phone: str,
        otp: str,
        purpose: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Verifies the provided 6-digit OTP against the hashed value in cache.
        Purges on success to prevent replay attacks.
        """
        norm_phone = normalize_bd_phone(phone)
        cache_key = f"otp:{norm_phone}"

        cached_entry = await cache_service.get(cache_key)
        if not cached_entry or not isinstance(cached_entry, dict):
            self._record_audit(
                action="SMS_OTP_FAILED",
                phone=norm_phone,
                purpose=purpose or "UNKNOWN",
                status="EXPIRED_OR_NOT_FOUND",
                details={}
            )
            return {
                "verified": False,
                "error": "OTP_EXPIRED_OR_INVALID",
                "message": "OTP has expired or was not requested."
            }

        # Check maximum failed verification attempts
        failed_attempts = cached_entry.get("failed_attempts", 0)
        if failed_attempts >= MAX_VERIFICATION_ATTEMPTS:
            await cache_service.delete(cache_key)
            self._record_audit(
                action="SMS_OTP_LOCKED",
                phone=norm_phone,
                purpose=purpose or cached_entry.get("purpose", ""),
                status="MAX_ATTEMPTS_EXCEEDED",
                details={}
            )
            return {
                "verified": False,
                "error": "MAX_ATTEMPTS_EXCEEDED",
                "message": "Maximum incorrect verification attempts reached. Request a new OTP."
            }

        # Verify purpose if specified
        expected_purpose = cached_entry.get("purpose")
        if purpose and expected_purpose and purpose != expected_purpose:
            return {
                "verified": False,
                "error": "PURPOSE_MISMATCH",
                "message": "The OTP was requested for a different purpose."
            }

        # Secure constant-time hash comparison
        candidate_hash = self._hash_otp(otp.strip())
        stored_hash = cached_entry.get("otp_hash", "")

        if not hmac.compare_digest(candidate_hash, stored_hash):
            # Increment failed attempts
            cached_entry["failed_attempts"] = failed_attempts + 1
            remaining = MAX_VERIFICATION_ATTEMPTS - (failed_attempts + 1)
            time_left = max(1, int(cached_entry.get("expires_at", time.time()) - time.time()))
            await cache_service.set(cache_key, cached_entry, ttl_seconds=time_left)

            self._record_audit(
                action="SMS_OTP_FAILED",
                phone=norm_phone,
                purpose=expected_purpose or "",
                status="INVALID_DIGITS",
                details={"remaining_attempts": remaining}
            )
            return {
                "verified": False,
                "error": "INVALID_OTP",
                "message": "Incorrect verification code.",
                "attempts_remaining": remaining
            }

        # SUCCESS: Invalidate immediately to prevent replay
        await cache_service.delete(cache_key)

        self._record_audit(
            action="SMS_OTP_VERIFIED",
            phone=norm_phone,
            purpose=expected_purpose or "",
            status="SUCCESS",
            details={"user_id": cached_entry.get("user_id")}
        )

        return {
            "verified": True,
            "phone": norm_phone,
            "masked_phone": mask_phone_for_logging(norm_phone),
            "purpose": expected_purpose,
            "user_id": cached_entry.get("user_id"),
            "verified_at": time.time()
        }

    def _record_audit(
        self,
        action: str,
        phone: str,
        purpose: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Appends OTP audit record."""
        self._audit_records.append({
            "action": action,
            "masked_phone": mask_phone_for_logging(phone),
            "purpose": purpose,
            "status": status,
            "timestamp": time.time(),
            "details": details or {}
        })

    def get_audit_records(self, limit: int = 50):
        return self._audit_records[-limit:]

    def clear_audit_records(self):
        self._audit_records.clear()


# Global OTP Service Singleton
otp_service = OTPService()
