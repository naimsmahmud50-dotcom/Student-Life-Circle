"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Institutional White-Label Portal & Teacher Cockpit API Endpoints
TOPIC:     Phase 114 Institutional White-Label Portal & Teacher Cockpit
FILE:      backend/app/api/v1/endpoints/institution.py
PHASE:     Phase 114 - Institutional White-Label Portal & Teacher Cockpit
PURPOSE:   Exposes multi-tenant institutional endpoints for subdomain resolution,
           teacher model test scheduling, exam publishing, section gradebook management,
           and privacy-preserving statistical analytics.
STANDARDS: REST OpenAPI 3.1, OWASP ASVS L2, Multi-Tenant Isolation, Strict Zero-Emoji
========================================================================================
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import APIRouter, HTTPException, Query, status
from backend.app.services.institutional_portal_service import (
    InstitutionalPortalService,
    institutional_portal_service,
    TenantNotFoundException,
    TenantAccessDeniedException,
    ExamSchedulingException,
    InstitutionalException,
)

router = APIRouter(prefix="/institution", tags=["Institutional White-Label Portal"])


@router.get("/resolve-tenant", response_model=Dict[str, Any])
def resolve_tenant(identifier: str = Query(..., description="Subdomain or Institution ID")):
    """
    Resolves institutional tenant configuration by subdomain or tenant ID.
    e.g., 'ndc', 'ndc.ogrojatra.edu.bd', or 'inst-ndc-dhaka'.
    """
    try:
        return institutional_portal_service.resolve_institution(identifier)
    except TenantNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get("/{institution_id}/sections", response_model=List[Dict[str, Any]])
def get_institution_sections(institution_id: str):
    """
    Retrieves all academic sections belonging to the specified institution tenant.
    """
    try:
        return institutional_portal_service.get_sections(institution_id)
    except TenantNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.get("/{institution_id}/exams", response_model=List[Dict[str, Any]])
def list_institution_exams(institution_id: str, section_id: Optional[str] = Query(None)):
    """
    Lists scheduled model tests and examinations for an institution or specific section.
    """
    try:
        return institutional_portal_service.get_exams(institution_id, section_id=section_id)
    except TenantNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.post("/{institution_id}/exams", response_model=Dict[str, Any])
def create_institution_exam(institution_id: str, payload: Dict[str, Any]):
    """
    Creates and schedules a new section model test with teacher authorization.
    """
    try:
        teacher_id = payload.get("teacher_id")
        section_id = payload.get("section_id")
        title_bn = payload.get("title_bn")
        subject = payload.get("subject", "Physics")
        paper = payload.get("paper", "1st")
        duration_minutes = int(payload.get("duration_minutes", 60))
        total_marks = int(payload.get("total_marks", 50))
        due_timestamp = int(payload.get("due_timestamp", 0))
        question_ids = payload.get("question_ids", [])
        title_en = payload.get("title_en")

        if not teacher_id or not section_id or not title_bn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: teacher_id, section_id, or title_bn.",
            )

        return institutional_portal_service.create_exam(
            institution_id=institution_id,
            teacher_id=teacher_id,
            section_id=section_id,
            title_bn=title_bn,
            subject=subject,
            paper=paper,
            duration_minutes=duration_minutes,
            total_marks=total_marks,
            due_timestamp=due_timestamp,
            question_ids=question_ids,
            title_en=title_en,
        )
    except TenantNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TenantAccessDeniedException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except ExamSchedulingException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/{institution_id}/exams/{exam_id}/publish", response_model=Dict[str, Any])
def publish_institution_exam(institution_id: str, exam_id: str, payload: Optional[Dict[str, Any]] = None):
    """
    Publishes an exam to make it accessible to enrolled section students.
    """
    try:
        teacher_id = (payload or {}).get("teacher_id", "tch-default")
        return institutional_portal_service.publish_exam(
            institution_id=institution_id,
            exam_id=exam_id,
            teacher_id=teacher_id,
        )
    except TenantNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TenantAccessDeniedException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except ExamSchedulingException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{institution_id}/sections/{section_id}/gradebook", response_model=Dict[str, Any])
def get_section_gradebook(institution_id: str, section_id: str, exam_id: Optional[str] = Query(None)):
    """
    Retrieves the section gradebook containing student scores, feedback, and attendance.
    """
    try:
        return institutional_portal_service.get_section_gradebook(
            institution_id=institution_id,
            section_id=section_id,
            exam_id=exam_id,
        )
    except TenantNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TenantAccessDeniedException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))


@router.post("/{institution_id}/sections/{section_id}/approve-grades", response_model=Dict[str, Any])
def approve_section_grades(institution_id: str, section_id: str, payload: Dict[str, Any]):
    """
    Authorizes teacher approval of the gradebook roster.
    """
    try:
        exam_id = payload.get("exam_id")
        teacher_id = payload.get("teacher_id")
        if not exam_id or not teacher_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: exam_id or teacher_id.",
            )

        return institutional_portal_service.approve_grades(
            institution_id=institution_id,
            section_id=section_id,
            exam_id=exam_id,
            teacher_id=teacher_id,
        )
    except TenantNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TenantAccessDeniedException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except InstitutionalException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{institution_id}/sections/{section_id}/analytics/{exam_id}", response_model=Dict[str, Any])
def get_section_analytics(institution_id: str, section_id: str, exam_id: str):
    """
    Calculates privacy-preserving section performance distribution,
    standard deviation, and weak topic clusters without student shaming.
    """
    try:
        return institutional_portal_service.get_section_analytics(
            institution_id=institution_id,
            section_id=section_id,
            exam_id=exam_id,
        )
    except TenantNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TenantAccessDeniedException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except InstitutionalException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
