"""
================================================================================
MODULE: Autonomous Examination Proctoring, Gaze Heuristics & Integrity Audit Schemas
TOPIC: Pydantic Data Contracts for Vision Heuristics, Tab Blur, Suspicion Scoring & Overrides
FILE: backend/app/schemas/autonomous_proctoring_integrity_schema.py
PURPOSE: Strict data validation schemas for Phase 63 Examination Proctoring & Integrity Tower.
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


class ProctoringSessionStartRequest(BaseModel):
    student_id: str = Field(..., description="Student user UUID")
    exam_id: str = Field(..., description="Exam / challenge identifier")
    exam_title: str = Field("HSC Model Test", description="Exam title")
    tenant_id: str = Field("11111111-1111-1111-1111-111111111111", description="Academic tenant UUID")
    client_device_info: Optional[Dict[str, Any]] = Field(None, description="Client device, browser and camera hardware specs")


class ProctoringSessionStartResponse(BaseModel):
    session_id: str
    student_id: str
    exam_id: str
    status: str
    suspicion_score: float
    warnings_count: int
    started_at: str


class ProctoringEventRecordRequest(BaseModel):
    session_id: str = Field(..., description="Active proctoring session ID")
    event_type: str = Field(..., description="Event: GAZE_AWAY_FROM_SCREEN, SECONDARY_FACE_DETECTED, FACE_DISAPPEARED, TAB_SWITCHED, WINDOW_BLURRED, DEVTOOLS_OPENED, CLIPBOARD_PASTE")
    confidence_score: float = Field(0.9, description="Heuristic confidence from 0.0 to 1.0")
    duration_ms: float = Field(1000.0, description="Duration of anomaly in milliseconds")
    gaze_yaw_angle: Optional[float] = Field(None, description="Head/gaze yaw divergence in degrees")
    gaze_pitch_angle: Optional[float] = Field(None, description="Head/gaze pitch divergence in degrees")
    detected_faces_count: int = Field(1, description="Number of distinct faces visible in camera frame")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional context or camera telemetry")


class ProctoringEventRecordResponse(BaseModel):
    session_id: str
    event_id: str
    new_suspicion_score: float
    action_taken: str
    warnings_count: int
    is_locked: bool
    recorded_at: str


class ProctoringSessionReportResponse(BaseModel):
    session_id: str
    student_id: str
    exam_id: str
    overall_integrity_rating: str
    final_suspicion_score: float
    total_anomalies_count: int
    is_locked: bool
    events_summary: List[Dict[str, Any]]
    cryptographic_audit_hash: str
    generated_at: str


class ProctoringOverrideRequest(BaseModel):
    session_id: str = Field(..., description="Target proctoring session ID")
    proctor_id: str = Field(..., description="Proctor or invigilator user UUID")
    action: str = Field(..., description="Action: UNLOCK_EXAM, DISMISS_WARNINGS, FLAG_FOR_EXPULSION, REQUEST_WEBCAM_CHECK")
    justification_note: str = Field("Verified student technical issue with proctor approval", description="Audit trail rationale")


class ProctoringOverrideResponse(BaseModel):
    session_id: str
    proctor_id: str
    action_applied: str
    success: bool
    message: str
    new_status: str
    timestamp: str
