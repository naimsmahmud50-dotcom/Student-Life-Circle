"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    National Merit Scholarship & Autonomous Disbursement API Endpoints
TOPIC:     Phase 113 National Merit Scholarship Pool & Autonomous Disbursement
FILE:      backend/app/api/v1/endpoints/scholarships.py
PHASE:     Phase 113 - National Merit Scholarship Pool & Autonomous Disbursement
PURPOSE:   Exposes versioned REST endpoints for scholarship pool discovery,
           algorithmic merit-need evaluation, dual-authorization approvals,
           idempotent bKash/Nagad B2C payouts, and public cryptographic ledger auditing.
STANDARDS: REST OpenAPI 3.1, OWASP ASVS L2, FinTech B2C Security, Strict Zero-Emoji
========================================================================================
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import APIRouter, HTTPException, Query, status
from backend.app.services.scholarship_disbursement_service import (
    ScholarshipDisbursementService,
    scholarship_disbursement_service,
    EligibilityException,
    AuthorizationException,
    DoubleSpendingException,
    ScholarshipException,
)

router = APIRouter(prefix="/scholarships", tags=["National Merit Scholarships"])


@router.get("/pools", response_model=List[Dict[str, Any]])
def get_scholarship_pools():
    """Retrieves all active national merit and hardship scholarship endowment pools."""
    return scholarship_disbursement_service.get_all_pools()


@router.get("/pools/{pool_id}", response_model=Dict[str, Any])
def get_pool_by_id(pool_id: str):
    """Retrieves specific scholarship pool details, funding progress, and district quotas."""
    pool = scholarship_disbursement_service.get_pool(pool_id)
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Endowment pool '{pool_id}' not found."
        )
    return pool


@router.post("/evaluate-eligibility", response_model=Dict[str, Any])
def evaluate_eligibility(payload: Dict[str, Any]):
    """Evaluates applicant against GPA 5.0 / top 5% percentile and income threshold."""
    try:
        gpa = float(payload.get("gpa", 0.0))
        national_percentile = float(payload.get("national_percentile", 0.0))
        income = float(payload.get("monthly_family_income_bdt", 0.0))
        district = str(payload.get("district", "General")).strip()
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid numeric or district parameters provided."
        )

    return scholarship_disbursement_service.evaluate_eligibility(
        gpa=gpa,
        national_percentile=national_percentile,
        monthly_family_income_bdt=income,
        district=district,
    )


@router.post("/apply", response_model=Dict[str, Any])
def submit_scholarship_application(payload: Dict[str, Any]):
    """Submits a student application for scholarship pool allocation."""
    required = ["pool_id", "student_id", "student_name", "district", "gpa", "monthly_family_income_bdt", "mobile_wallet_number"]
    for r in required:
        if r not in payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: '{r}'"
            )

    try:
        app = scholarship_disbursement_service.submit_application(
            pool_id=payload["pool_id"],
            student_id=payload["student_id"],
            student_name=payload["student_name"],
            district=payload["district"],
            gpa=float(payload["gpa"]),
            national_percentile=float(payload.get("national_percentile", 0.0)),
            monthly_family_income_bdt=float(payload["monthly_family_income_bdt"]),
            mobile_wallet_number=payload["mobile_wallet_number"],
            wallet_provider=payload.get("wallet_provider", "bKash"),
        )
        return app
    except EligibilityException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except DoubleSpendingException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ScholarshipException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/approve", response_model=Dict[str, Any])
def approve_scholarship_application(payload: Dict[str, Any]):
    """Records dual-authorization signature (academic evaluator or finance custodian)."""
    app_id = payload.get("application_id")
    auth_id = payload.get("authorizer_id")
    role = payload.get("authorizer_role")
    notes = payload.get("notes")

    if not app_id or not auth_id or not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="application_id, authorizer_id, and authorizer_role are required."
        )

    try:
        updated_app = scholarship_disbursement_service.approve_application(
            application_id=app_id,
            authorizer_id=auth_id,
            authorizer_role=role,
            notes=notes,
        )
        return updated_app
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ScholarshipException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/disburse", response_model=Dict[str, Any])
def execute_disbursement(payload: Dict[str, Any]):
    """Executes idempotent bKash/Nagad B2C payout and generates cryptographic ledger seal."""
    app_id = payload.get("application_id")
    idempotency_key = payload.get("idempotency_key")
    operator_id = payload.get("operator_id", "vault_operator_auto")

    if not app_id or not idempotency_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="application_id and idempotency_key are required."
        )

    try:
        receipt = scholarship_disbursement_service.execute_disbursement(
            application_id=app_id,
            idempotency_key=idempotency_key,
            operator_id=operator_id,
        )
        return receipt
    except DoubleSpendingException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except AuthorizationException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ScholarshipException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/ledger", response_model=Dict[str, Any])
def get_public_ledger(
    district: Optional[str] = Query(None, description="Filter by district"),
    gateway: Optional[str] = Query(None, description="Filter by gateway provider: BKASH or NAGAD"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Retrieves public cryptographic disbursement ledger with anonymized student records."""
    return scholarship_disbursement_service.get_public_ledger(
        district=district,
        gateway_provider=gateway,
        limit=limit,
        offset=offset,
    )
