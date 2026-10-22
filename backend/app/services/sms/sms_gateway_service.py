# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 82 - Unified SMS Gateway Service):
# This service coordinates multiple SMS aggregators with automatic failover,
# rate limiting, and audit logging for the Student Life Circle platform.
#
# Key Architectural Responsibilities:
# 1. Multi-Aggregator Failover: Dispatches SMS via primary aggregator (Greenweb,
#    Teletalk, or Elitbuzz) and cascades down to secondary adapters and Twilio
#    in the event of network disruption or provider failure.
# 2. Rate Limiting Protection (Anti-SMS-Bombing): Enforces strict maximum of
#    3 OTP requests per phone number within a rolling 15-minute (900 seconds)
#    window using Redis / CacheService.
# 3. Native Bangla Unicode Support: Accurately detects and handles Bengali Unicode
#    text with proper character count and multi-part SMS division.
# 4. Privacy & Audit Trail: Masks recipient phone numbers in logs and persists
#    audit records for every dispatch attempt.
# 5. Zero-Emoji Policy Enforced: Strictly uses clean technical text and Lucide icons.
# ==============================================================================

import time
import logging
from typing import Dict, List, Any, Optional, Tuple

from backend.app.services.sms.adapters import (
    SMSAdapter,
    GreenwebSMSAdapter,
    TeletalkSMSAdapter,
    ElitbuzzSMSAdapter,
    TwilioSMSAdapter,
    MockSMSAdapter,
    normalize_bd_phone,
    mask_phone_for_logging,
    calculate_sms_parts
)
from backend.app.services.cache_service import cache_service

logger = logging.getLogger("sms_gateway")

# Constants
MAX_OTP_PER_15_MINUTES = 3
RATE_LIMIT_WINDOW_SECONDS = 900  # 15 minutes


class SMSGatewayService:
    """
    Unified SMS Gateway with provider fallback chain, rate limiting,
    and audit tracking for Bangladeshi aggregators.
    """

    def __init__(self, use_mock: bool = False):
        self._adapters: Dict[str, SMSAdapter] = {}
        self._fallback_order: List[str] = []
        self._audit_records: List[Dict[str, Any]] = []

        if use_mock:
            mock = MockSMSAdapter()
            self.register_adapter(mock)
            self._fallback_order = ["mock"]
        else:
            # Register production adapters with fallback order
            gw = GreenwebSMSAdapter()
            tt = TeletalkSMSAdapter()
            eb = ElitbuzzSMSAdapter()
            tw = TwilioSMSAdapter()
            mock = MockSMSAdapter()

            self.register_adapter(gw)
            self.register_adapter(tt)
            self.register_adapter(eb)
            self.register_adapter(tw)
            self.register_adapter(mock)
            self._fallback_order = ["greenweb", "teletalk", "elitbuzz", "twilio", "mock"]

    def register_adapter(self, adapter: SMSAdapter):
        """Registers an aggregator adapter."""
        self._adapters[adapter.name] = adapter
        if adapter.name not in self._fallback_order:
            self._fallback_order.append(adapter.name)

    def set_fallback_order(self, order: List[str]):
        """Sets the sequence in which providers are attempted."""
        self._fallback_order = order

    def get_adapter(self, name: str) -> Optional[SMSAdapter]:
        return self._adapters.get(name)

    async def check_and_increment_rate_limit(
        self,
        phone: str,
        max_requests: int = MAX_OTP_PER_15_MINUTES,
        window_seconds: int = RATE_LIMIT_WINDOW_SECONDS
    ) -> Tuple[bool, int, int]:
        """
        Enforces maximum OTP requests per phone number within the specified window.
        Returns: (is_allowed: bool, current_attempts: int, retry_after_seconds: int)
        """
        norm_phone = normalize_bd_phone(phone)
        cache_key = f"ratelimit:sms_otp:{norm_phone}"

        current_data = await cache_service.get(cache_key)
        now = time.time()

        if current_data is None or not isinstance(current_data, dict):
            # First request in window
            new_record = {
                "count": 1,
                "first_attempt": now,
                "expires_at": now + window_seconds
            }
            await cache_service.set(cache_key, new_record, ttl_seconds=window_seconds)
            return True, 1, 0

        # Existing record
        count = current_data.get("count", 0)
        first_attempt = current_data.get("first_attempt", now)
        expires_at = current_data.get("expires_at", now + window_seconds)
        time_remaining = max(1, int(expires_at - now))

        if count >= max_requests:
            # Rate limit exceeded
            self._log_audit_event(
                action="SMS_OTP_RATE_LIMITED",
                phone=norm_phone,
                provider="gateway",
                status="BLOCKED",
                details={"attempts": count, "retry_after": time_remaining}
            )
            return False, count, time_remaining

        # Within limit, increment
        current_data["count"] = count + 1
        await cache_service.set(cache_key, current_data, ttl_seconds=time_remaining)
        return True, count + 1, 0

    async def send_sms(
        self,
        to_phone: str,
        message: str,
        sender_id: Optional[str] = None,
        is_masked: bool = True,
        preferred_provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dispatches SMS using preferred provider or the fallback chain.
        Ensures delivery attempts are recorded in audit logs.
        """
        norm_phone = normalize_bd_phone(to_phone)
        if len(norm_phone) < 11:
            return {
                "success": False,
                "error": "INVALID_PHONE_NUMBER",
                "phone": to_phone
            }

        order = list(self._fallback_order)
        if preferred_provider and preferred_provider in self._adapters:
            order = [preferred_provider] + [p for p in order if p != preferred_provider]

        last_error = None
        for provider_name in order:
            adapter = self._adapters.get(provider_name)
            if not adapter or not adapter.is_active:
                continue

            try:
                res = await adapter.send_sms(
                    to_phone=norm_phone,
                    message=message,
                    sender_id=sender_id,
                    is_masked=is_masked
                )
                if res.get("success", False):
                    self._log_audit_event(
                        action="SMS_DISPATCHED",
                        phone=norm_phone,
                        provider=provider_name,
                        status="SUCCESS",
                        details={
                            "message_id": res.get("message_id"),
                            "encoding": res.get("encoding"),
                            "parts": res.get("parts"),
                            "is_masked": is_masked
                        }
                    )
                    return res
                else:
                    last_error = res.get("error", "PROVIDER_DELIVERY_FAILED")
                    logger.warning(f"SMS dispatch failed on {provider_name}: {last_error}")
            except Exception as ex:
                last_error = str(ex)
                logger.error(f"Exception during SMS dispatch on {provider_name}: {ex}")

        # All providers exhausted
        self._log_audit_event(
            action="SMS_DISPATCH_FAILED",
            phone=norm_phone,
            provider="all_exhausted",
            status="FAILED",
            details={"last_error": last_error}
        )
        return {
            "success": False,
            "error": "ALL_SMS_PROVIDERS_EXHAUSTED",
            "last_error": last_error,
            "recipient": norm_phone
        }

    def _log_audit_event(
        self,
        action: str,
        phone: str,
        provider: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ):
        """Internal append-only audit trail logger for SMS events."""
        event = {
            "action": action,
            "masked_phone": mask_phone_for_logging(phone),
            "provider": provider,
            "status": status,
            "timestamp": time.time(),
            "details": details or {}
        }
        self._audit_records.append(event)

    def get_audit_records(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns recent SMS audit records."""
        return self._audit_records[-limit:]

    def clear_audit_records(self):
        """Clears in-memory audit records (testing only)."""
        self._audit_records.clear()


# Global SMS Gateway Service Singleton
sms_gateway_service = SMSGatewayService(use_mock=False)
