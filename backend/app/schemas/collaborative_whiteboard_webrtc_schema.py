"""
================================================================================
MODULE: Realtime Collaborative Whiteboard, WebRTC Low-Latency Voice Mesh & LaTeX Canvas Schemas
TOPIC: Pydantic Data Contracts for Vector Canvas, LaTeX Sync, WebRTC Signaling & Tutor Podium
FILE: backend/app/schemas/collaborative_whiteboard_webrtc_schema.py
PURPOSE: Strict data validation schemas for Phase 62 Collaborative Classroom System.
================================================================================
"""

from typing import Dict, Any, List, Optional
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default


class WhiteboardStrokeDelta(BaseModel):
    stroke_id: str = Field(..., description="Unique UUID for vector stroke")
    author_id: str = Field(..., description="Author user UUID")
    tool_type: str = Field("pen", description="Tool: pen, highlighter, eraser, line, rectangle, circle, arrow")
    color: str = Field("#2563EB", description="Stroke hex color")
    width: float = Field(2.5, description="Stroke width in pixels")
    points: List[List[float]] = Field(..., description="Array of [x, y] coordinate pairs")
    timestamp: float = Field(..., description="Timestamp in millisecond epoch")
    is_erased: bool = Field(False, description="Tombstone flag for CRDT soft deletion")


class LatexFormulaNode(BaseModel):
    formula_id: str = Field(..., description="Unique UUID for mathematical formula element")
    author_id: str = Field(..., description="Author user UUID")
    latex_source: str = Field(..., description="Raw LaTeX math code (e.g. \\int_{a}^{b} f(x) dx)")
    position_x: float = Field(..., description="Canvas X coordinate in pixels")
    position_y: float = Field(..., description="Canvas Y coordinate in pixels")
    font_size: int = Field(18, description="Rendered font size in pixels")
    is_pinned: bool = Field(False, description="Pinned by tutor to prevent accidental movement")


class WhiteboardSyncRequest(BaseModel):
    session_id: str = Field(..., description="Classroom whiteboard session ID")
    client_seq: int = Field(1, description="Client monotonic sequence number")
    caller_id: str = Field(..., description="Calling participant user UUID")
    caller_role: str = Field("student", description="Role: tutor, student, guardian, institutional_admin")
    new_strokes: Optional[List[WhiteboardStrokeDelta]] = Field(None, description="New or updated stroke deltas")
    new_formulas: Optional[List[LatexFormulaNode]] = Field(None, description="New or updated LaTeX formula nodes")
    erased_stroke_ids: Optional[List[str]] = Field(None, description="List of stroke IDs to mark as erased")


class WhiteboardSyncResponse(BaseModel):
    session_id: str
    server_seq: int
    acknowledged: bool
    active_stroke_count: int
    active_formula_count: int
    canvas_locked: bool
    sync_timestamp: str


class WebRtcSignalRequest(BaseModel):
    session_id: str = Field(..., description="Target classroom session ID")
    sender_id: str = Field(..., description="Originating peer user UUID")
    target_id: Optional[str] = Field(None, description="Target peer user UUID or None for broadcast mesh")
    signal_type: str = Field(..., description="Signal: offer, answer, ice_candidate, mute_state, vad_active")
    payload: Dict[str, Any] = Field(..., description="WebRTC SDP, ICE candidate object, or VAD metrics")


class WebRtcSignalResponse(BaseModel):
    session_id: str
    signal_id: str
    dispatched_peers_count: int
    latency_ms: float
    mesh_status: str
    timestamp: str


class PodiumControlRequest(BaseModel):
    session_id: str = Field(..., description="Target classroom session ID")
    caller_id: str = Field(..., description="Calling tutor or admin UUID")
    caller_role: str = Field("tutor", description="Role: tutor or institutional_admin")
    action: str = Field(..., description="Action: lock_canvas, unlock_canvas, mute_all, spotlight_student, clear_canvas")
    target_student_id: Optional[str] = Field(None, description="Target student UUID for spotlight or mute")


class PodiumControlResponse(BaseModel):
    session_id: str
    action_applied: str
    success: bool
    status_message: str
    canvas_locked: bool
    muted_peers: List[str]
    spotlighted_student_id: Optional[str]


class WhiteboardSessionCreateRequest(BaseModel):
    topic: str = Field(..., description="Academic lecture / problem-solving topic")
    tutor_id: str = Field(..., description="Lead tutor user UUID")
    curriculum: str = Field("NCTB", description="Curriculum: NCTB, Cambridge, Edexcel, IB")
    grade_level: int = Field(10, description="Academic class grade (1-12)")
    max_students: int = Field(25, description="Maximum concurrent students in audio mesh")


class WhiteboardSessionStateResponse(BaseModel):
    session_id: str
    topic: str
    tutor_id: str
    curriculum: str
    grade_level: int
    participants_count: int
    canvas_locked: bool
    strokes: List[WhiteboardStrokeDelta]
    formulas: List[LatexFormulaNode]
    webrtc_peers: List[Dict[str, Any]]
    created_at: str
