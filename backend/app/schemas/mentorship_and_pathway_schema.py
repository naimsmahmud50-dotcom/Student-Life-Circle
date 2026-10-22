"""
Pydantic v2 schemas and DTOs for Phase 29:
- 1-on-1 Alumni Mentorship Marketplace & WebRTC Session Tokens
- Dynamic Remedial Adaptive Learning Pathways & Skill Dependency Graphs
- Cryptographic Proof-of-Skill Certificate Verification Gateway
Dual-resilience BaseDTO fallbacks included for robust serialization.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self, *args, **kwargs):
            return self.__dict__
        def model_dump(self, *args, **kwargs):
            return self.__dict__

    def Field(default=None, **kwargs):
        return default

class AlumniMentorProfile(BaseModel):
    mentor_id: str
    name: str
    alma_mater: str
    current_role: str
    specialties: List[str]
    hourly_fee_bdt: float = 500.0
    available_slots: List[str]
    rating: float = 4.95
    total_sessions: int = 42
    verified: bool = True

class BookMentorshipSessionRequest(BaseModel):
    mentor_id: str
    student_id: str
    student_name: str
    slot_time: str
    topic_focus: str
    target_ambition: str
    fee_bdt: float = 500.0
    payment_method: str = "bKash"

class MentorshipSessionResponse(BaseModel):
    session_id: str
    mentor_id: str
    student_id: str
    student_name: str
    slot_time: str
    topic_focus: str
    target_ambition: str
    status: str
    webrtc_channel_token: str
    escrow_tx_id: str
    created_at: str

class GenerateAdaptivePathwayRequest(BaseModel):
    student_id: str
    subject: str
    weak_topic_ids: List[str]
    target_mastery_pct: float = 90.0

class RemedialSprintStep(BaseModel):
    step_id: str
    step_type: str  # "DIAGNOSTIC", "MICRO_LECTURE", "PRACTICE_DRILL", "MASTERY_ASSESSMENT"
    title: str
    duration_minutes: int
    resource_url: str
    prerequisite_concept: str
    status: str = "PENDING"  # "PENDING", "IN_PROGRESS", "COMPLETED"

class AdaptivePathwayResponse(BaseModel):
    pathway_id: str
    student_id: str
    subject: str
    current_readiness_pct: float
    projected_mastery_pct: float
    steps: List[Dict[str, Any]]
    created_at: str

class IssueCertificateRequest(BaseModel):
    student_id: str
    student_name: str
    course_or_track: str
    grade_or_score: str
    skills_mastered: List[str]
    issued_by: str = "Agrojatra Academic Accreditation Council"

class CertificateVerificationResponse(BaseModel):
    certificate_id: str
    sha256_hash: str
    student_name: str
    course_or_track: str
    grade_or_score: str
    skills_mastered: List[str]
    issue_timestamp: str
    verified: bool
    issuer: str
    verification_url: str
