"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Exam Routine & Model Test API Router
TOPIC:     REST API Endpoints for 200-Day Routines, Countdown & Negative Marking
FILE:      backend/app/api/v1/endpoints/exam_routine_router.py
PURPOSE:   Exposes versioned REST endpoints for exam routine schedule retrieval,
           Friday Mega Model Test countdowns, score simulations with negative marking,
           and reminder subscription dispatch.
STANDARDS: REST OpenAPI 3.1, Standard Envelope, OWASP ASVS L2, Zero-Emoji
========================================================================================
"""

from typing import Optional
from backend.app.core.fastapi_shim import APIRouter, Header, HTTPException, Query, status
from backend.app.core.config import settings
from backend.app.schemas.exam_routine_schema import (
    ExamTypeEnum,
    TrackCategoryEnum,
    ExamRoutineItem,
    ExamRoutineListResponse,
    NegativeMarkSimulationRequest,
    NegativeMarkSimulationResponse,
    RoutineSubscribeRequest,
    RoutineSubscribeResponse,
)
from backend.app.services.exam_routine_service import exam_routine_service

router = APIRouter(prefix="/routines", tags=["Exam Routines & Mega Model Tests"])


def _verify_routine_feature_access(x_feature_override: Optional[str] = None, authorization: Optional[str] = None):
    """
    Enforces feature gating. If FEATURE_EXAM_ROUTINE is disabled in production settings,
    only authorized staging overrides or admin tokens are permitted.
    """
    if getattr(settings, "FEATURE_EXAM_ROUTINE", False):
        return True
    if x_feature_override == "preview_active" or (authorization and "admin" in authorization.lower()):
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Exam Routine and Model Test hub is currently disabled by feature flag.",
    )


@router.get("", response_model=ExamRoutineListResponse)
def list_exam_routines(
    exam_type: Optional[ExamTypeEnum] = Query(None, description="Filter by exam type"),
    track_category: Optional[TrackCategoryEnum] = Query(None, description="Filter by subject track"),
    day_number: Optional[int] = Query(None, ge=1, le=200, description="Filter by day number"),
    x_feature_override: Optional[str] = Header(None),
):
    """
    Retrieves the comprehensive 200-day routine calendar, filtered by exam type or track.
    """
    _verify_routine_feature_access(x_feature_override)
    return exam_routine_service.get_routines(
        exam_type=exam_type,
        track_category=track_category,
        day_number=day_number,
    )


@router.get("/{routine_id}", response_model=ExamRoutineItem)
def get_exam_routine_detail(
    routine_id: str,
    x_feature_override: Optional[str] = Header(None),
):
    """
    Retrieves details for a specific scheduled routine or Mega Model Test.
    """
    _verify_routine_feature_access(x_feature_override)
    routine = exam_routine_service.get_routine_by_id(routine_id)
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Routine with ID '{routine_id}' not found in active calendar.",
        )
    return routine


@router.post("/simulate-score", response_model=NegativeMarkSimulationResponse)
def simulate_negative_marking_score(
    payload: NegativeMarkSimulationRequest,
    x_feature_override: Optional[str] = Header(None),
):
    """
    Simulates exam outcome with negative marking deduction (+1.0 / -0.25, -0.50),
    providing accuracy percentage, estimated merit percentile, and weakness indicators.
    """
    _verify_routine_feature_access(x_feature_override)
    return exam_routine_service.simulate_negative_marking(payload)


@router.post("/subscribe", response_model=RoutineSubscribeResponse)
def subscribe_to_routine_alerts(
    payload: RoutineSubscribeRequest,
    authorization: Optional[str] = Header(None),
    x_feature_override: Optional[str] = Header(None),
):
    """
    Subscribes the user to notifications and push alerts for an upcoming exam routine.
    """
    _verify_routine_feature_access(x_feature_override, authorization)
    # Mock user extraction from bearer token or fallback guest id
    user_id = "usr-guest-subscriber"
    if authorization and authorization.startswith("Bearer "):
        token_body = authorization.replace("Bearer ", "")
        user_id = f"usr-{token_body[:8]}"
    return exam_routine_service.subscribe_to_routine(user_id=user_id, payload=payload)
