"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Adaptive Examination & Dynamic CAT Tower Endpoints
TOPIC:     Computerized Adaptive Testing Session Ingestion & Ability Evaluation
FILE:      backend/app/api/v1/endpoints/adaptive_exam.py
PHASE:     Phase 105 - AI Adaptive CAT Examination Tower
PURPOSE:   Provides REST API endpoints for starting dynamic 3-PL CAT sessions,
           submitting sequential student answers, recalculating latent ability (Theta),
           and delivering visual convergence diagnostics with percentile benchmarks.
STANDARDS: UI/UX Pro Max, IRT 3-PL Latent Ability Math, Zero-Emoji, Human-Centric
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    HTTPException,
    JSONResponse,
    Query,
    status
)
from backend.app.services.cat_engine_service import cat_engine_service

router = APIRouter(prefix="/cat", tags=["AI Adaptive CAT Examination Tower"])


@router.post("/start", status_code=status.HTTP_200_OK)
async def start_adaptive_exam_session(payload: Dict[str, Any]):
    """
    Initializes a new Computerized Adaptive Testing (CAT) session under the
    3-Parameter Logistic (3-PL) model, selecting the first optimal diagnostic item.
    """
    student_id = payload.get("student_id", "stu_anonymous")
    subject = payload.get("subject", "বিজ্ঞান")
    initial_theta = float(payload.get("initial_theta", 0.0))
    target_se = float(payload.get("target_se", 0.25))
    use_3pl = payload.get("use_3pl_bank", True)

    session = cat_engine_service.start_cat_session(
        student_id=student_id,
        subject=subject,
        initial_theta=initial_theta,
        target_se=target_se,
        use_3pl_bank=use_3pl
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=session)


@router.post("/submit-step", status_code=status.HTTP_200_OK)
async def submit_adaptive_exam_step(payload: Dict[str, Any]):
    """
    Evaluates student response, updates latent ability (Theta) via IRT Bayesian EAP,
    recalculates standard error, and serves the next item maximizing Fisher Information.
    """
    session_id = payload.get("session_id")
    item_id = payload.get("item_id")
    selected_option_id = payload.get("selected_option_id")

    if not session_id or not item_id or not selected_option_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="session_id, item_id, and selected_option_id are required fields."
        )

    result = cat_engine_service.submit_cat_answer(
        session_id=session_id,
        item_id=item_id,
        selected_option_id=selected_option_id
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error evaluating adaptive response.")
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.get("/result", status_code=status.HTTP_200_OK)
async def get_adaptive_exam_result(session_id: str = Query(..., description="Active or completed CAT session ID")):
    """
    Retrieves complete ability diagnostics, convergence trajectory, and authentic
    admission readiness percentile for the specified CAT session.
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter 'session_id' is required."
        )

    session = cat_engine_service.get_session(session_id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CAT session '{session_id}' was not found."
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=session)


@router.get("/result/{session_id}", status_code=status.HTTP_200_OK)
async def get_adaptive_exam_result_by_path(session_id: str):
    """Path-based alternative for retrieving CAT session diagnostic results."""
    session = cat_engine_service.get_session(session_id=session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CAT session '{session_id}' was not found."
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=session)
