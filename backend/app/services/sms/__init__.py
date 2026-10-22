# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 82 - SMS & Guardian Services Barrel Export):
# Unified module export for all SMS aggregators, cryptographic OTP generation,
# and guardian consent verification services.
# ==============================================================================

from backend.app.services.sms.adapters import (
    SMSAdapter,
    GreenwebSMSAdapter,
    TeletalkSMSAdapter,
    ElitbuzzSMSAdapter,
    TwilioSMSAdapter,
    MockSMSAdapter,
    is_bangla_unicode,
    calculate_sms_parts,
    normalize_bd_phone,
    mask_phone_for_logging
)
from backend.app.services.sms.sms_gateway_service import (
    SMSGatewayService,
    sms_gateway_service,
    MAX_OTP_PER_15_MINUTES,
    RATE_LIMIT_WINDOW_SECONDS
)
from backend.app.services.sms.otp_service import (
    OTPService,
    otp_service,
    OTP_TTL_SECONDS,
    MAX_VERIFICATION_ATTEMPTS
)
from backend.app.services.sms.guardian_consent_service import (
    GuardianConsentService,
    guardian_consent_service,
    CONSENT_TOKEN_TTL_SECONDS,
    MINOR_AGE_THRESHOLD
)

__all__ = [
    "SMSAdapter",
    "GreenwebSMSAdapter",
    "TeletalkSMSAdapter",
    "ElitbuzzSMSAdapter",
    "TwilioSMSAdapter",
    "MockSMSAdapter",
    "is_bangla_unicode",
    "calculate_sms_parts",
    "normalize_bd_phone",
    "mask_phone_for_logging",
    "SMSGatewayService",
    "sms_gateway_service",
    "MAX_OTP_PER_15_MINUTES",
    "RATE_LIMIT_WINDOW_SECONDS",
    "OTPService",
    "otp_service",
    "OTP_TTL_SECONDS",
    "MAX_VERIFICATION_ATTEMPTS",
    "GuardianConsentService",
    "guardian_consent_service",
    "CONSENT_TOKEN_TTL_SECONDS",
    "MINOR_AGE_THRESHOLD",
]
