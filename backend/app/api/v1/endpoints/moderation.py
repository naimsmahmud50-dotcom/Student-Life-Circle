"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Collaborative Question Bank Moderation API Endpoints
TOPIC:     Phase 117 Collaborative Question Bank Moderation & Peer-Review
FILE:      backend/app/api/v1/endpoints/moderation.py
PHASE:     Phase 117 - Collaborative Question Bank Moderation & Peer-Review
PURPOSE:   Exposes REST API endpoints for question drafting, multi-stage editorial
           review submissions, dual-examiner blind consensus tracking, emergency
           quarantine switch execution, and immutable moderation audit logs.
STANDARDS: REST OpenAPI 3.1, OWASP ASVS L2, Zero-Unreviewed-AI Policy, Strict Zero-Emoji
========================================================================================
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import APIRouter, HTTPException, Query, status
from backend.app.services.question_moderation_service import (
    QuestionModerationService,
    question_moderation_service,
    QuestionNotFoundException,
    InvalidStateTransitionException,
    SelfReviewException,
    DuplicateReviewException,
    QuarantinedQuestionException,
    ModerationException,
)

router = APIRouter(prefix="/moderation", tags=["Question Moderation & Peer-Review"])


@router.post("/questions/draft", response_model=Dict[str, Any])
def create_draft(payload: Dict[str, Any]):
    """
    Creates a new question draft in DRAFT status.
    """
    author_id = payload.get("author_id")
    author_name = payload.get("author_name")
    subject = payload.get("subject")
    topic = payload.get("topic")
    stem = payload.get("stem")
    options = payload.get("options", [])
    class_grade = int(payload.get("class_grade", 11))
    question_id = payload.get("question_id")

    if not author_id or not author_name or not subject or not stem or not options:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields: author_id, author_name, subject, stem, or options.",
        )

    return question_moderation_service.create_draft_question(
        author_id=author_id,
        author_name=author_name,
        subject=subject,
        topic=topic or "সাধারণ",
        stem=stem,
        options=options,
        class_grade=class_grade,
        question_id=question_id,
    )


@router.get("/questions/{question_id}", response_model=Dict[str, Any])
def get_question_details(question_id: str):
    """
    Retrieves full question details by ID including review history and diff snapshot.
    """
    try:
        return question_moderation_service.get_question(question_id)
    except QuestionNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/questions/{question_id}/submit", response_model=Dict[str, Any])
def submit_question_for_review(question_id: str, payload: Dict[str, Any]):
    """
    Submits a draft question for SME peer-review (DRAFT -> SME_REVIEW).
    """
    actor_id = payload.get("actor_id")
    if not actor_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing actor_id parameter.",
        )

    try:
        return question_moderation_service.submit_for_review(question_id, actor_id=actor_id)
    except QuestionNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidStateTransitionException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/questions/{question_id}/review", response_model=Dict[str, Any])
def submit_review_decision(question_id: str, payload: Dict[str, Any]):
    """
    Submits an educator's peer review decision (APPROVE, REVISE, REJECT).
    Enforces dual-examiner blind consensus and prevents author self-review.
    """
    examiner_id = payload.get("examiner_id")
    examiner_name = payload.get("examiner_name")
    decision = payload.get("decision")
    comments = payload.get("comments", "")

    if not examiner_id or not examiner_name or not decision:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing examiner_id, examiner_name, or decision parameter.",
        )

    try:
        return question_moderation_service.review_question(
            question_id=question_id,
            examiner_id=examiner_id,
            examiner_name=examiner_name,
            decision=decision,
            comments=comments,
        )
    except QuestionNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except SelfReviewException as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))
    except (DuplicateReviewException, InvalidStateTransitionException, QuarantinedQuestionException) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/questions/{question_id}/quarantine", response_model=Dict[str, Any])
def execute_emergency_quarantine(question_id: str, payload: Dict[str, Any]):
    """
    Emergency switch: Instantly pulls any question from live pools with audit log.
    """
    actor_id = payload.get("actor_id")
    actor_name = payload.get("actor_name", "বোর্ড অ্যাডমিন")
    reason = payload.get("reason")

    if not actor_id or not reason:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing actor_id or reason for emergency quarantine.",
        )

    try:
        return question_moderation_service.emergency_quarantine(
            question_id=question_id,
            actor_id=actor_id,
            actor_name=actor_name,
            reason=reason,
        )
    except QuestionNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/questions/{question_id}/remediate", response_model=Dict[str, Any])
def remediate_quarantined_question(question_id: str, payload: Dict[str, Any]):
    """
    Restores a quarantined question back to DRAFT with remediation notes and revised fields.
    """
    actor_id = payload.get("actor_id")
    remediation_notes = payload.get("remediation_notes")
    revised_stem = payload.get("revised_stem")
    revised_options = payload.get("revised_options")

    if not actor_id or not remediation_notes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing actor_id or remediation_notes.",
        )

    try:
        return question_moderation_service.remediate_quarantine(
            question_id=question_id,
            actor_id=actor_id,
            remediation_notes=remediation_notes,
            revised_stem=revised_stem,
            revised_options=revised_options,
        )
    except QuestionNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except InvalidStateTransitionException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/queue", response_model=List[Dict[str, Any]])
def get_moderation_queue(
    filter_status: Optional[str] = Query(None),
    subject: Optional[str] = Query(None),
):
    """
    Retrieves the queue of questions pending moderation.
    """
    return question_moderation_service.get_moderation_queue(
        filter_status=filter_status,
        subject=subject,
    )


@router.get("/audit-trail", response_model=List[Dict[str, Any]])
def get_audit_trail(question_id: Optional[str] = Query(None)):
    """
    Retrieves the immutable audit trail for moderation events.
    """
    return question_moderation_service.get_audit_trail(question_id=question_id)
