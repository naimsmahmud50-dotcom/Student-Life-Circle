"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Guardian Trust Console & Child Digital Safety Endpoints
TOPIC:     REST API Endpoints for Non-Intrusive Telemetry & Tuition Escrow
FILE:      backend/app/api/v1/endpoints/guardian_console.py
PHASE:     Phase 108 - Guardian Trust Console & Child Digital Safety Portal
PURPOSE:   Provides REST API endpoints for guardian academic summaries,
           strict child privacy wall enforcement (ASVS L2 HTTP 403),
           and dual-party tuition escrow milestone releases with SMS OTP.
STANDARDS: ASVS L2 Minor Privacy Boundary, Zero-Intrusion Safeguards, Zero-Emoji, UI/UX Pro Max
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    HTTPException,
    JSONResponse,
    Query,
    status
)
from backend.app.services.guardian_trust_service import (
    ChildPrivacyBoundaryException,
    guardian_trust_service
)

router = APIRouter(prefix="/guardian", tags=["Guardian Trust Console & Child Digital Safety"])


@router.get("/summary", status_code=status.HTTP_200_OK)
async def get_guardian_family_summary(
    guardian_id: Optional[str] = Query("GUARD_2026_01", description="Guardian unique identifier")
):
    """
    Retrieves aggregate, non-invasive learning progress for all linked children:
    study hours, subject mastery, practice consistency, and upcoming exams.
    """
    summary = guardian_trust_service.get_guardian_summary(guardian_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=summary)


@router.get("/child/{child_id}/private-chat", status_code=status.HTTP_403_FORBIDDEN)
async def get_child_private_chat_endpoint(
    child_id: str,
    guardian_id: Optional[str] = Query("GUARD_2026_01")
):
    """
    ASVS L2 Minor Privacy Boundary Wall.
    Strictly forbids guardians from intercepting adolescent peer messages or personal notes.
    """
    try:
        guardian_trust_service.get_child_private_chat(guardian_id, child_id)
    except ChildPrivacyBoundaryException as ex:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(ex)
        )
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"error": "Privacy violation blocked"})


@router.get("/escrow/milestones", status_code=status.HTTP_200_OK)
async def list_pending_escrow_milestones(
    guardian_id: Optional[str] = Query("GUARD_2026_01")
):
    """
    Returns verified tutoring milestones ready for guardian review and fee release.
    """
    milestones = guardian_trust_service.get_pending_escrow_milestones(guardian_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"milestones": milestones, "total": len(milestones)})


@router.post("/escrow/approve", status_code=status.HTTP_200_OK)
async def approve_tuition_escrow_milestone(payload: Dict[str, Any]):
    """
    Validates SMS OTP and releases monthly tuition payment to tutor with cryptographic audit receipt.
    """
    guardian_id = payload.get("guardian_id", "GUARD_2026_01")
    milestone_id = payload.get("milestone_id")
    otp_code = payload.get("otp_code")

    if not milestone_id or not otp_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields 'milestone_id' and 'otp_code' are required."
        )

    result = guardian_trust_service.approve_tuition_escrow(
        guardian_id=str(guardian_id).strip(),
        milestone_id=str(milestone_id).strip(),
        otp_code=str(otp_code).strip()
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to approve tuition escrow milestone.")
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
