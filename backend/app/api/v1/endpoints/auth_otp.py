# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 82 - SMS OTP & Guardian Consent Gateway Endpoints):
# This module exposes production REST API endpoints for phone OTP authentication,
# rate-limited SMS dispatching, and minor student guardian consent workflows.
#
# Endpoints Exposed:
# 1. POST /auth-otp/send: Dispatches a 6-digit numeric OTP with 3-minute TTL,
#    enforcing a strict 3-requests-per-15-minutes rate limit per phone number.
# 2. POST /auth-otp/verify: Verifies candidate OTP against SHA-256 hash in cache;
#    purges immediately on success to eliminate replay attacks.
# 3. POST /auth-otp/guardian/request-consent: Dispatches 1-click guardian consent
#    SMS for minor students (age < 16) with a 24-hour cryptographic token link.
# 4. GET /auth-otp/guardian/verify-token: Validates guardian consent link token.
# 5. POST /auth-otp/guardian/grant-consent: Records affirmative guardian consent,
#    lifting profile privacy lockdowns and messaging restrictions.
# 6. POST /auth-otp/guardian/revoke-consent: Allows guardians to revoke consent,
#    instantly restoring private lockdown mode.
# 7. GET /auth-otp/guardian/student-status/{student_id}: Returns child safety status.
# 8. GET /auth-otp/audit-logs: Returns append-only SMS and OTP verification audit logs.
#
# Standards & Policies:
# - Zero-Emoji Policy Enforced: Strictly uses clean technical text and Lucide icons.
# - ASVS L2 / OWASP Top 10: Anti-SMS bombing, Zero-IDOR, child privacy protection.
# ==============================================================================

from typing import Dict, Any, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    Header,
    HTTPException,
    Query,
    status
)
from backend.app.services.sms import (
    sms_gateway_service,
    otp_service,
    guardian_consent_service,
    normalize_bd_phone
)

router = APIRouter(prefix="/auth-otp", tags=["SMS OTP & Guardian Consent Gateway"])


# =============================================================================
# 1. SMS OTP Authentication Endpoints
# =============================================================================
@router.post("/send")
async def send_sms_otp_endpoint(payload: Dict[str, Any]):
    """
    Dispatches a 6-digit numeric OTP to the requested Bangladeshi phone number.
    Enforces maximum 3 requests per 15 minutes.
    """
    phone = payload.get("phone", "")
    purpose = payload.get("purpose", "LOGIN")
    user_id = payload.get("user_id")
    test_mode = payload.get("test_mode", False)

    if not phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number is required."
        )

    res = await otp_service.generate_and_send_otp(
        phone=phone,
        purpose=purpose,
        user_id=user_id,
        return_raw_for_testing=test_mode
    )

    if not res.get("success", False):
        if res.get("error") == "RATE_LIMIT_EXCEEDED":
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=res.get("message", "Maximum OTP requests reached. Please wait."),
                headers={"Retry-After": str(res.get("retry_after_seconds", 900))}
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("error", "Failed to dispatch OTP.")
        )

    return res


@router.post("/verify")
async def verify_sms_otp_endpoint(payload: Dict[str, Any]):
    """
    Verifies a 6-digit numeric OTP against the SHA-256 hash stored in cache.
    Purges key immediately upon success to prevent replay attacks.
    """
    phone = payload.get("phone", "")
    otp = payload.get("otp", "")
    purpose = payload.get("purpose")

    if not phone or not otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both phone and OTP digits are required."
        )

    res = await otp_service.verify_otp(phone=phone, otp=otp, purpose=purpose)
    if not res.get("verified", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("message", res.get("error", "Invalid or expired OTP."))
        )

    return res


# =============================================================================
# 2. Guardian Consent Flow for Minor Students (Age < 16)
# =============================================================================
@router.post("/guardian/request-consent")
async def request_guardian_consent_endpoint(payload: Dict[str, Any]):
    """
    Dispatches a 1-click guardian consent SMS for a minor student (<16).
    Locks the student's profile to strictly private mode until consent is confirmed.
    """
    student_id = payload.get("student_id", "")
    student_name = payload.get("student_name", "")
    guardian_phone = payload.get("guardian_phone", "")
    student_age = int(payload.get("student_age", 15))
    callback_url = payload.get("callback_url")

    if not student_id or not guardian_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID and guardian phone number are required."
        )

    res = await guardian_consent_service.request_guardian_consent(
        student_id=student_id,
        student_name=student_name,
        guardian_phone=guardian_phone,
        student_age=student_age,
        custom_callback_url=callback_url
    )

    if not res.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("message", res.get("error", "Failed to request consent."))
        )

    return res


@router.get("/guardian/verify-token")
async def verify_guardian_consent_token_endpoint(token: str = Query(...)):
    """
    Validates the 1-click consent token dispatched via SMS to the guardian.
    Returns minor student name and verification link status.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consent token is required."
        )

    res = await guardian_consent_service.verify_consent_token(token)
    if not res.get("valid", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("message", res.get("error", "Invalid or expired consent token."))
        )

    return res


@router.post("/guardian/grant-consent")
async def grant_guardian_consent_endpoint(payload: Dict[str, Any]):
    """
    Guardian confirms affirmative consent, unlocking minor student profile
    permissions and allowing verified messaging.
    """
    token = payload.get("token", "")
    relationship = payload.get("relationship", "PARENT")
    guardian_name = payload.get("guardian_name")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consent token is required."
        )

    res = await guardian_consent_service.grant_consent(
        token=token,
        relationship=relationship,
        guardian_name=guardian_name
    )

    if not res.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("message", res.get("error", "Consent grant failed."))
        )

    return res


@router.post("/guardian/revoke-consent")
async def revoke_guardian_consent_endpoint(payload: Dict[str, Any]):
    """
    Allows guardian to revoke affirmative consent at any time,
    immediately re-locking the student's profile to private mode.
    """
    student_id = payload.get("student_id", "")
    guardian_phone = payload.get("guardian_phone", "")
    reason = payload.get("reason", "Guardian initiated revocation.")

    if not student_id or not guardian_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID and guardian phone are required."
        )

    res = await guardian_consent_service.revoke_consent(
        student_id=student_id,
        guardian_phone=guardian_phone,
        reason=reason
    )

    if not res.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=res.get("message", res.get("error", "Revocation failed."))
        )

    return res


@router.get("/guardian/student-status/{student_id}")
async def get_student_privacy_status_endpoint(student_id: str):
    """
    Returns minor student safety and privacy status, indicating whether public
    messaging and discovery are unlocked.
    """
    if not student_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID is required."
        )

    return guardian_consent_service.get_student_privacy_status(student_id)


# =============================================================================
# 3. SMS & Verification Audit Logs
# =============================================================================
@router.get("/audit-logs")
async def get_sms_audit_logs_endpoint(limit: int = Query(50)):
    """
    Retrieves recent append-only audit trail records for SMS dispatches,
    OTP attempts, and guardian consent events.
    """
    sms_logs = sms_gateway_service.get_audit_records(limit=limit)
    otp_logs = otp_service.get_audit_records(limit=limit)
    guardian_logs = guardian_consent_service.get_audit_records(limit=limit)

    return {
        "status": "SUCCESS",
        "counts": {
            "sms_dispatches": len(sms_logs),
            "otp_attempts": len(otp_logs),
            "guardian_events": len(guardian_logs)
        },
        "sms_dispatches": sms_logs,
        "otp_attempts": otp_logs,
        "guardian_events": guardian_logs
    }
