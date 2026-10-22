"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    API Endpoints - Socratic AI Realtime Streaming
TOPIC:     Server-Sent Events (SSE), OWASP LLM01 Guardrails, Multi-Modal Vision
FILE:      backend/app/api/v1/endpoints/socratic_ai.py
PURPOSE:   Exposes production Server-Sent Events (SSE) endpoints for real-time token-by-token
           streaming of Socratic dialogue. Supports GET and POST streaming protocols,
           base64 vision upload for handwritten equations, OWASP LLM01 injection defense,
           and bilingual step-by-step guidance for Bangladeshi students.
AUDIENCE:  Backend Engineers, Mobile/Web Clients & AI Autonomous Agents
STANDARDS: W3C SSE, OWASP LLM01, KaTeX Math Syntax, Strict Zero-Emoji
========================================================================================
"""

import json
from typing import AsyncGenerator, Dict, Any, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    Query,
    HTTPException,
    StreamingResponse,
    JSONResponse,
    status
)
from backend.app.services.ai.gemini_streaming_service import (
    gemini_streaming_service,
    prompt_injection_shield
)

router = APIRouter(prefix="/socratic", tags=["Multi-Modal AI Socratic Tutor"])

# Standard HTTP headers for resilient Server-Sent Events (SSE) streaming
SSE_HEADERS = {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}


async def format_sse_event_stream(
    query: str,
    session_id: str,
    image_base64: Optional[str] = None,
    subject: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """
    Transforms token dictionaries from GeminiStreamingService into W3C compliant
    Server-Sent Event lines (`data: <json>\\n\\n`).
    """
    try:
        async for token_event in gemini_streaming_service.stream_socratic_response(
            query=query,
            session_id=session_id,
            image_base64=image_base64,
            subject=subject
        ):
            payload = json.dumps(token_event, ensure_ascii=False)
            yield f"data: {payload}\n\n"
    except Exception as exc:
        error_payload = json.dumps({
            "token": "",
            "done": True,
            "session_id": session_id,
            "error": str(exc),
            "status": "STREAM_EXCEPTION"
        }, ensure_ascii=False)
        yield f"data: {error_payload}\n\n"


@router.get("/chat/stream")
async def socratic_chat_stream_get_endpoint(
    session_id: str = Query(..., description="Unique conversation session ID"),
    query: str = Query(..., description="Student inquiry or problem statement"),
    image_base64: Optional[str] = Query(None, description="Optional base64 image for handwritten math parsing"),
    subject: Optional[str] = Query(None, description="Subject context (e.g. physics, math, chemistry)")
):
    """
    Server-Sent Events (SSE) endpoint providing instant token-by-token typing effect.
    Accepts student question, validates against OWASP LLM01 injection, and streams
    Socratic guidance in Bengali with KaTeX math notation.
    """
    if not query or not query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query parameter 'query' cannot be empty."
        )

    if not session_id or not session_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session ID parameter 'session_id' cannot be empty."
        )

    generator = format_sse_event_stream(
        query=query.strip(),
        session_id=session_id.strip(),
        image_base64=image_base64,
        subject=subject
    )

    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers=SSE_HEADERS
    )


@router.post("/chat/stream")
async def socratic_chat_stream_post_endpoint(payload: Dict[str, Any]):
    """
    POST variant for streaming Socratic chat, enabling large multi-modal payloads
    (such as high-resolution handwritten math photos) without URL length restrictions.
    """
    session_id = payload.get("session_id", "").strip()
    query = payload.get("query", "").strip()
    image_base64 = payload.get("image_base64")
    subject = payload.get("subject")

    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload field 'query' is required."
        )

    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload field 'session_id' is required."
        )

    generator = format_sse_event_stream(
        query=query,
        session_id=session_id,
        image_base64=image_base64,
        subject=subject
    )

    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers=SSE_HEADERS
    )


@router.post("/sessions/reset")
async def reset_socratic_session_endpoint(payload: Dict[str, Any]):
    """
    Resets the conversation history for a given session ID.
    """
    session_id = payload.get("session_id", "").strip()
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'session_id' is required."
        )

    if session_id in gemini_streaming_service.sessions:
        del gemini_streaming_service.sessions[session_id]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "session_id": session_id,
            "status": "RESET_SUCCESSFUL",
            "message": "সক্রেটিক কথোপকথনের সেশন সফলভাবে রিসেট করা হয়েছে।"
        }
    )


@router.get("/health")
async def socratic_health_endpoint():
    """
    Diagnostic healthcheck returning engine availability, model configuration,
    and active session metrics.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "OPERATIONAL",
            "service": "Ogrojatra Socratic AI Streaming Tutor",
            "model": gemini_streaming_service.model_name,
            "active_sessions": len(gemini_streaming_service.sessions),
            "guardrails": "OWASP_LLM01_ACTIVE",
            "zero_emoji": True
        }
    )
