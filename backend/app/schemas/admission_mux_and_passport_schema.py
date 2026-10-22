"""
Pydantic v2 schemas and DTOs for Phase 30:
- Centralized Multi-University Admission Multiplexer & Circular Eligibility Matcher
- Offline-First PWA CRDT Delta-Sync Engine for Low-Bandwidth Networks
- Universal Student Talent Passport & Recruiter Proof-of-Skill Radar
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

class CheckAdmissionEligibilityRequest(BaseModel):
    student_id: str
    hsc_gpa: float
    ssc_gpa: float
    academic_group: str = "SCIENCE"
    subject_grades: Dict[str, str] = Field(default_factory=dict)

class UniversityEligibilityReport(BaseModel):
    university_code: str
    university_name: str
    unit_name: str
    is_eligible: bool
    min_gpa_required: float
    exam_date: str
    application_fee_bdt: float
    status_reason: str

class BatchApplyUniversityRequest(BaseModel):
    student_id: str
    student_name: str
    hsc_roll: str
    hsc_registration: str
    university_codes: List[str]
    payment_channel: str = "bKash"

class BatchApplyResponse(BaseModel):
    batch_id: str
    student_id: str
    total_fee_bdt: float
    applied_universities: List[str]
    admit_cards: List[Dict[str, Any]]
    conflicts_detected: List[str]
    payment_status: str
    created_at: str

class CRDTDeltaMutation(BaseModel):
    mutation_id: str
    client_timestamp: str
    vector_clock: int
    entity_type: str  # "QUIZ_ANSWER", "NOTE", "BOOKMARK"
    entity_id: str
    payload: Dict[str, Any]

class OfflineDeltaSyncRequest(BaseModel):
    client_id: str
    student_id: str
    last_synced_vector_clock: int = 0
    mutations: List[Dict[str, Any]] = Field(default_factory=list)

class OfflineDeltaSyncResponse(BaseModel):
    sync_status: str  # "SUCCESS", "RECONCILED", "PARTIAL"
    reconciled_clock: int
    applied_count: int
    conflicts_resolved: int
    server_state_digest: str
    synced_at: str

class GenerateTalentPassportRequest(BaseModel):
    student_id: str
    public_handle: str
    include_mentorship_badges: bool = True
    include_code_evaluations: bool = True

class TalentPassportResponse(BaseModel):
    passport_id: str
    student_id: str
    student_name: str
    public_handle: str
    shareable_url: str
    cat_latent_ability_theta: float
    academic_standing: str
    verified_skills: List[str]
    credentials_summary: Dict[str, Any]
    qr_payload: str
    qr_signature: str
    verified: bool = True
    created_at: str
