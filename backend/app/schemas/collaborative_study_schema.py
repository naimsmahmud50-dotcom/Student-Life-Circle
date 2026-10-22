# ============================================================================
# MODULE: COLLABORATIVE STUDY & BOUNTY TRIBUNAL SCHEMAS
# TOPIC: Peer Study Circles, Synchronous Whiteboard & Gamified Bounty Arena DTOs
# FILE: backend/app/schemas/collaborative_study_schema.py
# PURPOSE: Resilient Pydantic v2 and BaseDTO validation schemas for Phase 27
#          real-time collaborative rooms, whiteboard telemetry, and bounty tribunals.
# STANDARDS: ASVS L2 Contract Validation, Dual-Resilience BaseDTO Fallback
# AUDIENCE: Frontend Engineers, API Gateway Consumers, Security Auditors
# ============================================================================

from typing import Optional, List, Dict, Any

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(*args, **kwargs):
        return None


# ----------------------------------------------------------------------------
# 1. STUDY ROOM COLLABORATION DTO SCHEMAS
# ----------------------------------------------------------------------------

class CreateStudyRoomRequest(BaseModel):
    title: str = Field(..., description="Descriptive title of the study room")
    host_id: str = Field(..., description="Student user identifier of the host")
    host_name: str = Field(..., description="Display name of the room host")
    topic: str = Field(..., description="Academic topic or subject focus (e.g. Higher Math, Organic Chemistry)")
    target_grade: str = Field(..., description="Target academic level (e.g. HSC-2026, Admission-BUET)")
    max_participants: int = Field(8, ge=2, le=50, description="Maximum concurrent room capacity")
    is_private: bool = Field(False, description="Flag for password-protected study room")
    passcode: Optional[str] = Field(None, description="Optional access passcode for private rooms")


class JoinStudyRoomRequest(BaseModel):
    room_id: str = Field(..., description="Unique study room identifier")
    user_id: str = Field(..., description="Joining student user identifier")
    user_name: str = Field(..., description="Display name of joining student")
    role: str = Field("PARTICIPANT", description="Room role: HOST, CO_HOST, PARTICIPANT, OBSERVER")
    passcode: Optional[str] = Field(None, description="Passcode if room is private")


class WhiteboardSyncRequest(BaseModel):
    room_id: str = Field(..., description="Study room identifier")
    user_id: str = Field(..., description="Author student identifier")
    action: str = Field(..., description="Whiteboard action: STROKE, FORMULA, CLEAR, UNDO")
    stroke_data: Optional[Dict[str, Any]] = Field(None, description="Coordinates, brush color, stroke size")
    formula_latex: Optional[str] = Field(None, description="LaTeX mathematical expression or chemical formula")


class PomodoroSyncRequest(BaseModel):
    room_id: str = Field(..., description="Study room identifier")
    host_id: str = Field(..., description="Host or co-host initiating sync")
    duration_minutes: int = Field(25, ge=5, le=120, description="Sprint duration in minutes")
    action: str = Field("START", description="Action: START, PAUSE, RESUME, RESET")


# ----------------------------------------------------------------------------
# 2. GAMIFIED BOUNTY TRIBUNAL DTO SCHEMAS
# ----------------------------------------------------------------------------

class CreateBountyRequest(BaseModel):
    poster_id: str = Field(..., description="Student posting the bounty")
    poster_name: str = Field(..., description="Display name of the poster")
    title: str = Field(..., description="Concise summary of the academic problem")
    subject: str = Field(..., description="Subject domain (Physics, Mathematics, Chemistry, Computer Science)")
    problem_statement: str = Field(..., description="Full problem text and specific requirements")
    bounty_bdt: float = Field(..., ge=0.0, description="Escrowed BDT reward for accepted solution")
    bounty_reputation_pts: int = Field(50, ge=10, description="Reputation honor points awarded")
    attachment_url: Optional[str] = Field(None, description="Optional diagram or problem sheet URL")


class SubmitSolutionRequest(BaseModel):
    bounty_id: str = Field(..., description="Target bounty problem identifier")
    scholar_id: str = Field(..., description="Scholar student submitting the solution")
    scholar_name: str = Field(..., description="Display name of the solver")
    explanation: str = Field(..., description="Comprehensive step-by-step conceptual solution")
    latex_proof: Optional[str] = Field(None, description="Formal mathematical/scientific derivation in LaTeX")
    code_snippet: Optional[str] = Field(None, description="Optional code solution or numerical simulation")


class VerdictBountyRequest(BaseModel):
    bounty_id: str = Field(..., description="Target bounty identifier")
    evaluator_id: str = Field(..., description="Original poster or designated tribunal member identifier")
    decision: str = Field(..., description="Tribunal verdict: ACCEPT, REJECT, REQUEST_REVISION")
    feedback: Optional[str] = Field(None, description="Constructive feedback or reason for verdict")
