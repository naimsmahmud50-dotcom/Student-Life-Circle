"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Digital Examination Hall & Proctoring Integrity API Endpoints
TOPIC:     Phase 116 Digital Examination Hall & Proctoring Integrity Tower
FILE:      backend/app/api/v1/endpoints/exam_hall.py
PHASE:     Phase 116 - Digital Examination Hall & Proctoring Integrity Tower
PURPOSE:   Exposes versioned REST endpoints for exam desk session initialization,
           client heuristic telemetry logging, draft answer auto-saving, final
           submission with cryptographic SHA-256 seal, and teacher live monitor roster.
STANDARDS: REST OpenAPI 3.1, OWASP ASVS L2, Privacy-First Architecture, Strict Zero-Emoji
========================================================================================
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import APIRouter, HTTPException, Query, status
from backend.app.services.proctoring_integrity_service import (
    ProctoringIntegrityService,
    proctoring_integrity_service,
    SessionNotFoundException,
    ExamFinalizedException,
    ProctoringException,
)

router = APIRouter(prefix="/exam-hall", tags=["Digital Examination Hall"])


@router.post("/sessions/start", response_model=Dict[str, Any])
def start_exam_session(payload: Dict[str, Any]):
    """
    Initializes a new digital examination hall session for an examinee.
    """
    session_id = payload.get("session_id")
    student_id = payload.get("student_id")
    student_name = payload.get("student_name")
    exam_id = payload.get("exam_id")
    institution_id = payload.get("institution_id")

    if not session_id or not student_id or not student_name or not exam_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields: session_id, student_id, student_name, or exam_id.",
        )

    return proctoring_integrity_service.start_exam_session(
        session_id=session_id,
        student_id=student_id,
        student_name=student_name,
        exam_id=exam_id,
        institution_id=institution_id,
    )


@router.post("/sessions/{session_id}/telemetry", response_model=Dict[str, Any])
def log_telemetry_event(session_id: str, payload: Dict[str, Any]):
    """
    Logs client heuristic telemetry (e.g. TAB_SWITCH, WINDOW_BLUR, AUDIO_THRESHOLD_EXCEEDED).
    Returns real-time updated integrity score.
    """
    event_type = payload.get("event_type")
    value = float(payload.get("value", 1.0))
    metadata = payload.get("metadata", {})

    if not event_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing event_type parameter.",
        )

    try:
        return proctoring_integrity_service.record_telemetry_event(
            session_id=session_id,
            event_type=event_type,
            value=value,
            metadata=metadata,
        )
    except SessionNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ExamFinalizedException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/sessions/{session_id}/save-draft", response_model=Dict[str, Any])
def save_draft_answers(session_id: str, payload: Dict[str, Any]):
    """
    Periodically auto-saves draft question responses and flagged items.
    """
    answers = payload.get("answers", {})
    flagged = payload.get("flagged_questions")

    try:
        return proctoring_integrity_service.save_draft_answers(
            session_id=session_id,
            answers=answers,
            flagged_questions=flagged,
        )
    except SessionNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ExamFinalizedException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/sessions/{session_id}/finalize", response_model=Dict[str, Any])
def finalize_exam_submission(session_id: str, payload: Optional[Dict[str, Any]] = None):
    """
    Locks the examination desk and seals the submission with a SHA-256 cryptographic receipt.
    """
    final_answers = (payload or {}).get("final_answers")

    try:
        return proctoring_integrity_service.finalize_exam_submission(
            session_id=session_id,
            final_answers=final_answers,
        )
    except SessionNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ExamFinalizedException as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/sessions/{session_id}/status", response_model=Dict[str, Any])
def get_session_status(session_id: str):
    """
    Retrieves the current status, answered question count, and integrity band of a session.
    """
    try:
        session = proctoring_integrity_service.get_session(session_id)
        return {
            "session_id": session["session_id"],
            "student_id": session["student_id"],
            "student_name": session["student_name"],
            "exam_id": session["exam_id"],
            "status": session["status"],
            "questions_answered_count": len(session["answers"]),
            "flagged_questions_count": len(session["flagged_questions"]),
            "integrity_score": session["integrity_score"],
            "integrity_band": proctoring_integrity_service.get_integrity_band(session["integrity_score"]),
            "started_at": session["started_at"],
            "finalized_at": session["finalized_at"],
            "receipt_hash": session["receipt_hash"],
        }
    except SessionNotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/proctor/{exam_id}/roster", response_model=List[Dict[str, Any]])
def get_proctor_roster(exam_id: str):
    """
    Live teacher monitor roster for all students taking the exam.
    """
    return proctoring_integrity_service.get_proctor_roster(exam_id)
