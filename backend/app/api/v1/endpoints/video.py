"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    API Endpoints - HLS Video Streaming & Checkpoint Telemetry
TOPIC:     Adaptive Bitrate Manifest, In-Lecture Quizzes, Anti-Scrubbing Heartbeats
FILE:      backend/app/api/v1/endpoints/video.py
PURPOSE:   Exposes production REST API endpoints for the Ogrojatra HLS video micro-classroom:
           1. GET /video/lecture/{lecture_id}: Returns HLS stream qualities (including 240p
              Data Saver for rural Bangladesh), audio tracks, and interactive checkpoints.
           2. POST /video/telemetry: 15-second heartbeat telemetry verifying actual watch
              seconds and preventing scrub-skipping cheats.
           3. POST /video/checkpoint/submit: Evaluates in-lecture quiz submissions, unlocking
              resume on correct answer or triggering a 30s rewind with explanation hints.
           4. GET /video/telemetry/{student_id}/{lecture_id}: Returns current student progress.
AUDIENCE:  Backend Engineers, Mobile/Web Clients & AI Coding Agents
STANDARDS: HLS RFC 8216, OWASP ASVS L2, UI/UX Pro Max, Strict Zero-Emoji
========================================================================================
"""

from typing import Dict, Any, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    HTTPException,
    JSONResponse,
    status
)
from backend.app.services.video_service import video_service

router = APIRouter(prefix="/video", tags=["HLS Video Player & In-Lecture Checkpoints"])


@router.get("/lecture/{lecture_id}")
async def get_lecture_manifest_endpoint(lecture_id: str):
    """
    Returns HLS streaming manifest, multi-bitrate qualities (Auto, 240p, 360p, 720p, 1080p),
    dual audio tracks, and interactive checkpoints for the requested lecture.
    """
    lecture = video_service.get_lecture(lecture_id)
    if not lecture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lecture with ID '{lecture_id}' not found."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=lecture.to_dict()
    )


@router.post("/telemetry")
async def record_video_telemetry_endpoint(payload: Dict[str, Any]):
    """
    Receives 15-second client heartbeats. Evaluates actual watched duration,
    flags scrubbing cheats, checks completion criteria, and returns active checkpoint triggers.
    """
    student_id = payload.get("student_id", "").strip()
    lecture_id = payload.get("lecture_id", "").strip()
    current_pos = payload.get("current_position")
    playback_rate = payload.get("playback_rate", 1.0)

    if not student_id or not lecture_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields 'student_id' and 'lecture_id' are required."
        )

    if current_pos is None or not isinstance(current_pos, (int, float)) or current_pos < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Valid non-negative 'current_position' is required."
        )

    telemetry = video_service.record_telemetry(
        student_id=student_id,
        lecture_id=lecture_id,
        current_position_seconds=float(current_pos),
        playback_rate=float(playback_rate)
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=telemetry
    )


@router.post("/checkpoint/submit")
async def submit_checkpoint_answer_endpoint(payload: Dict[str, Any]):
    """
    Evaluates student answer for an in-lecture checkpoint quiz.
    On success: returns resume_playback=True.
    On failure: returns resume_playback=False, rewind_to_seconds (30s prior), and pedagogical hint.
    """
    student_id = payload.get("student_id", "").strip()
    lecture_id = payload.get("lecture_id", "").strip()
    checkpoint_id = payload.get("checkpoint_id", "").strip()
    selected_key = payload.get("selected_key", "").strip()

    if not student_id or not lecture_id or not checkpoint_id or not selected_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fields 'student_id', 'lecture_id', 'checkpoint_id', and 'selected_key' are required."
        )

    result = video_service.submit_checkpoint_answer(
        student_id=student_id,
        lecture_id=lecture_id,
        checkpoint_id=checkpoint_id,
        selected_key=selected_key
    )

    if result.get("status") == "ERROR":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Checkpoint evaluation error.")
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result
    )


@router.get("/telemetry/{student_id}/{lecture_id}")
async def get_student_telemetry_endpoint(student_id: str, lecture_id: str):
    """
    Returns verified watch seconds, completion status, and passed checkpoints for a student.
    """
    session = video_service.get_or_create_session(student_id, lecture_id)
    lecture = video_service.get_lecture(lecture_id)

    total_duration = lecture.duration_seconds if lecture else session.total_duration
    completion_pct = round(min(100.0, (session.total_watched_seconds / total_duration) * 100.0), 1)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "student_id": student_id,
            "lecture_id": lecture_id,
            "total_watched_seconds": round(session.total_watched_seconds, 2),
            "current_position_seconds": round(session.last_position_seconds, 2),
            "completion_percentage": completion_pct,
            "is_completed": session.is_completed,
            "completed_checkpoints": list(session.completed_checkpoints)
        }
    )
