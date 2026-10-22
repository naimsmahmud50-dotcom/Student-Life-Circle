"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Corporate Talent Acquisition & Cryptographic Skill Pipeline Endpoints
TOPIC:     REST API Endpoints for Candidate Discovery, CV Verification & Interview Offers
FILE:      backend/app/api/v1/endpoints/talent_pipeline.py
PHASE:     Phase 109 - Corporate Talent Acquisition & Cryptographic Skill Pipeline
PURPOSE:   Provides REST API endpoints for recruiters to search talent using
           cosine vector similarity matching, verify cryptographic W3C skill credentials,
           and dispatch verified interview offers with CTC salary terms.
STANDARDS: W3C Verifiable Credentials, Vector Cosine Similarity, Zero-Emoji, UI/UX Pro Max
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    HTTPException,
    JSONResponse,
    Query,
    status
)
from backend.app.services.corporate_talent_pipeline_service import corporate_talent_pipeline_service

router = APIRouter(prefix="/talent", tags=["Corporate Talent Acquisition & Cryptographic Skill Pipeline"])


@router.get("/candidates", status_code=status.HTTP_200_OK)
async def list_talent_candidates(
    min_cgpa: float = Query(0.0),
    university: Optional[str] = Query(None),
    skill: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
    min_match_percent: float = Query(0.0)
):
    """
    Returns candidate talent roster ranked by vector skill match percentage,
    with filters for CGPA, university, skill tags, and recruitment stage.
    """
    candidates = corporate_talent_pipeline_service.search_candidates(
        min_cgpa=min_cgpa,
        institution_filter=university,
        skill_filter=skill,
        stage_filter=stage,
        min_match_percent=min_match_percent
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"candidates": candidates, "total": len(candidates)})


@router.post("/interview/invite", status_code=status.HTTP_200_OK)
async def dispatch_interview_invitation(payload: Dict[str, Any]):
    """
    Issues a verified interview offer to a student candidate with role details,
    scheduled date, and CTC salary in BDT, advancing recruitment stage.
    """
    candidate_id = payload.get("candidate_id")
    company_name = payload.get("company_name")
    job_title = payload.get("job_title")
    ctc_salary_bdt = payload.get("ctc_salary_bdt")
    interview_date = payload.get("interview_date")

    if not candidate_id or not company_name or not job_title or not ctc_salary_bdt or not interview_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields 'candidate_id', 'company_name', 'job_title', 'ctc_salary_bdt', and 'interview_date' are required."
        )

    result = corporate_talent_pipeline_service.invite_to_interview(
        candidate_id=str(candidate_id).strip(),
        company_name=str(company_name).strip(),
        job_title=str(job_title).strip(),
        ctc_salary_bdt=int(ctc_salary_bdt),
        interview_date=str(interview_date).strip()
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to issue interview offer.")
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)


@router.post("/cv-snapshot/verify", status_code=status.HTTP_200_OK)
async def verify_cv_snapshot_endpoint(payload: Dict[str, Any]):
    """
    Cryptographically verifies a candidate's sealed CV snapshot against HMAC-SHA256 signature,
    confirming proof-of-skill authenticity and uncompromised academic credentials.
    """
    candidate_id = payload.get("candidate_id")
    cgpa = payload.get("cgpa")
    institution = payload.get("institution")
    verified_skills = payload.get("verified_skills", {})
    signature = payload.get("signature")

    if not candidate_id or cgpa is None or not institution or not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields 'candidate_id', 'cgpa', 'institution', and 'signature' are required."
        )

    audit_result = corporate_talent_pipeline_service.verify_cv_snapshot(
        candidate_id=str(candidate_id).strip(),
        cgpa=float(cgpa),
        institution=str(institution).strip(),
        verified_skills=verified_skills,
        provided_signature=str(signature).strip()
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=audit_result)


@router.post("/match-score", status_code=status.HTTP_200_OK)
async def calculate_custom_match_score(payload: Dict[str, Any]):
    """
    Calculates cosine vector similarity score between custom corporate job requirements
    and a candidate's verified skill vector.
    """
    job_requirements = payload.get("job_requirements")
    candidate_skills = payload.get("candidate_skills")

    if not job_requirements or not candidate_skills:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields 'job_requirements' and 'candidate_skills' must be non-empty dictionaries."
        )

    sim = corporate_talent_pipeline_service.compute_cosine_similarity(
        job_requirements=job_requirements,
        candidate_skills=candidate_skills
    )
    match_percent = round(sim * 100.0, 1)

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "cosine_similarity": round(sim, 4),
        "match_percent": match_percent,
        "tier": "HIGH" if match_percent >= 85 else "STRONG" if match_percent >= 70 else "POTENTIAL"
    })
