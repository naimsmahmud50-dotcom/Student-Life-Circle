"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Centralized Admission Counseling & Gale-Shapley Stable Matching Endpoints
TOPIC:     REST API Endpoints for Deferred Acceptance Matching & Migration Simulation
FILE:      backend/app/api/v1/endpoints/counseling.py
PHASE:     Phase 107 - Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
PURPOSE:   Provides REST API endpoints for candidate preference submission,
           Pareto-optimal Gale-Shapley deferred acceptance matching execution,
           quota spillover balancing, multi-round migration simulation, and probability estimation.
STANDARDS: Pareto-Optimal Deferred Acceptance, Quota Spillover Balancing, Zero-Emoji, UI/UX Pro Max
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    HTTPException,
    JSONResponse,
    Query,
    status
)
from backend.app.services.gale_shapley_counseling_service import gale_shapley_counseling_service

router = APIRouter(prefix="/counseling", tags=["Centralized Admission Counseling & Gale-Shapley Stable Matching"])


@router.post("/match", status_code=status.HTTP_200_OK)
async def run_gale_shapley_admission_match(payload: Dict[str, Any]):
    """
    Executes Student-Proposing Deferred Acceptance (Gale-Shapley) matching.
    Guarantees mathematically stable, envy-free allocations with quota general spillover.
    """
    students = payload.get("students")
    if not students or not isinstance(students, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'students' must be a non-empty list of candidate objects."
        )

    programs = payload.get("programs")  # Optional custom program definitions

    result = gale_shapley_counseling_service.run_matching(students, programs=programs)
    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.post("/migrate-simulate", status_code=status.HTTP_200_OK)
async def simulate_admission_migration_cascade(payload: Dict[str, Any]):
    """
    Simulates multi-stage seat migration cascades across multiple counseling rounds
    following candidate cancellations or withdrawals.
    """
    students = payload.get("students")
    if not students or not isinstance(students, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'students' must be a non-empty list of candidate objects."
        )

    cancellations = payload.get("cancellations", [])
    num_rounds = int(payload.get("num_rounds", 3))

    simulation = gale_shapley_counseling_service.simulate_migration_cascade(
        students=students,
        cancellations=cancellations,
        num_rounds=num_rounds
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=simulation)


@router.get("/programs", status_code=status.HTTP_200_OK)
async def list_counseling_programs(cluster: Optional[str] = Query(None)):
    """
    Lists calibrated university departments and engineering/medical programs with capacities.
    """
    programs = gale_shapley_counseling_service.list_programs(cluster=cluster)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"programs": programs, "total": len(programs)})


@router.post("/predict-probability", status_code=status.HTTP_200_OK)
async def predict_candidate_admission_probability(payload: Dict[str, Any]):
    """
    Calculates admission probability percentage and guidance tier based on merit rank,
    target program, and quota category.
    """
    merit_rank = payload.get("merit_rank")
    target_program_id = payload.get("target_program_id")

    if merit_rank is None or not target_program_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields 'merit_rank' and 'target_program_id' are required."
        )

    quota = payload.get("quota", "GENERAL")
    prediction = gale_shapley_counseling_service.predict_admission_probability(
        merit_rank=int(merit_rank),
        target_program_id=str(target_program_id).strip(),
        quota=str(quota).strip()
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=prediction)
