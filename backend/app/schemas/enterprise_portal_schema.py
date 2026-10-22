# ============================================================================
# MODULE: ENTERPRISE PORTAL & ESCROW SCHEMAS
# TOPIC: Dual-Party Escrow, Guardian Telemetry & Corporate Talent Acquisition DTOs
# FILE: backend/app/schemas/enterprise_portal_schema.py
# PURPOSE: Resilient Pydantic v2 and BaseDTO validation schemas for Phase 26
#          financial milestones, parental health telemetry, and recruiter contracts.
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
# 1. HONORARIUM ESCROW DTO SCHEMAS
# ----------------------------------------------------------------------------

class CreateEscrowContractRequest(BaseModel):
    contract_id: str = Field(..., description="Unique contract identifier")
    tuition_id: str = Field(..., description="Associated tuition listing identifier")
    guardian_id: str = Field(..., description="Guardian user identifier")
    tutor_id: str = Field(..., description="Tutor user identifier")
    total_bdt: float = Field(..., gt=0, description="Total monthly honorarium in BDT")
    sessions_committed: int = Field(..., gt=0, description="Number of committed lessons/sessions")
    payment_method: Optional[str] = Field("BKASH_ESCROW", description="Payment channel (BKASH_ESCROW, NAGAD_ESCROW, BANK)")


class LogSessionCompletionRequest(BaseModel):
    contract_id: str = Field(..., description="Escrow contract identifier")
    tutor_id: str = Field(..., description="Tutor user identifier")
    session_number: int = Field(..., gt=0, description="Sequential session number (e.g., 1, 2, 3...)")
    topic_covered: str = Field(..., description="Subject chapter or curriculum topic covered")
    duration_minutes: Optional[int] = Field(90, gt=0, description="Duration in minutes")


class ReleaseMilestoneFundsRequest(BaseModel):
    contract_id: str = Field(..., description="Escrow contract identifier")
    session_number: int = Field(..., gt=0, description="Session number whose milestone funds are being released")
    authorizer_id: str = Field(..., description="Guardian or automated system authorizer ID")


class RaiseMilestoneDisputeRequest(BaseModel):
    contract_id: str = Field(..., description="Escrow contract identifier")
    session_number: int = Field(..., gt=0, description="Disputed session number")
    guardian_id: str = Field(..., description="Guardian user identifier")
    reason: str = Field(..., min_length=5, description="Clear description of the dispute reason")


# ----------------------------------------------------------------------------
# 2. GUARDIAN TELEMETRY DTO SCHEMAS
# ----------------------------------------------------------------------------

class ToggleSafetyLockRequest(BaseModel):
    guardian_id: str = Field(..., description="Guardian user identifier")
    student_id: str = Field(..., description="Student user identifier")
    lock_active: bool = Field(..., description="True to engage emergency safety lock; False to disengage")
    reason: Optional[str] = Field(None, description="Optional explanation for the safety lock")


# ----------------------------------------------------------------------------
# 3. CORPORATE TALENT SCOUT DTO SCHEMAS
# ----------------------------------------------------------------------------

class DispatchInterviewInvitationRequest(BaseModel):
    recruiter_id: str = Field(..., description="Recruiter user identifier")
    company_name: str = Field(..., description="Hiring organization name")
    candidate_id: str = Field(..., description="Candidate student identifier")
    role_title: str = Field(..., description="Target internship or entry-level job title")
    proposed_date: Optional[str] = Field("Flexible Schedule", description="Proposed interview date and time")
    message: Optional[str] = Field(None, description="Custom message to candidate")


class ShortlistCandidateRequest(BaseModel):
    recruiter_id: str = Field(..., description="Recruiter user identifier")
    candidate_id: str = Field(..., description="Candidate student identifier")
