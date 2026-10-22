# ============================================================================
# MODULE: SCHOLARSHIP ENDOWMENT & TECHNICAL ASSESSMENT SCHEMAS
# TOPIC: Micro-Scholarships, bKash Auto-Disbursement, ATS Resume Scorer & Coding Arena
# FILE: backend/app/schemas/scholarship_and_assessment_schema.py
# PURPOSE: Resilient Pydantic v2 and BaseDTO validation schemas for Phase 28
#          endowments, merit-need composite calculations, and code assessment.
# STANDARDS: ASVS L2 Contract Validation, Dual-Resilience BaseDTO Fallback
# AUDIENCE: Frontend Engineers, API Gateway Consumers, Financial Arbitrators
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
# 1. MICRO-SCHOLARSHIP ENDOWMENT DTO SCHEMAS
# ----------------------------------------------------------------------------

class CreateEndowmentFundRequest(BaseModel):
    sponsor_id: str = Field(..., description="Corporate or alumni donor identifier")
    sponsor_name: str = Field(..., description="Display name of corporate sponsor or donor")
    fund_title: str = Field(..., description="Title of the endowment fund")
    total_grant_bdt: float = Field(..., gt=0.0, description="Total committed endowment fund in BDT")
    target_criteria: str = Field("UNDERPRIVILEGED_STEM", description="Criteria: UNDERPRIVILEGED_STEM, FEMALE_TECH, GENERAL_MERIT")
    disbursement_per_student_bdt: float = Field(..., gt=0.0, description="Stipend amount per awarded student")


class ApplyScholarshipRequest(BaseModel):
    fund_id: str = Field(..., description="Endowment fund identifier")
    student_id: str = Field(..., description="Applicant student identifier")
    student_name: str = Field(..., description="Display name of applicant")
    family_monthly_income_bdt: float = Field(..., ge=0.0, description="Family monthly income in BDT for need-index")
    institution_name: str = Field(..., description="Educational institution or college")
    cat_ability_theta: float = Field(0.0, description="Psychometric latent ability score theta")
    reputation_score: float = Field(0.0, ge=0.0, le=1000.0, description="Composite student reputation score")
    bkash_number: str = Field(..., description="Verified bKash or Nagad wallet MSISDN")
    statement_of_need: str = Field(..., description="Brief statement explaining academic goals and financial need")


class DisburseScholarshipRequest(BaseModel):
    application_id: str = Field(..., description="Approved scholarship application identifier")
    disburser_id: str = Field(..., description="Administrator or automated payout authority identifier")
    channel: Optional[str] = Field("BKASH_DISBURSEMENT", description="Disbursement channel: BKASH_DISBURSEMENT, NAGAD_DISBURSEMENT, BANK")


# ----------------------------------------------------------------------------
# 2. AI RESUME TAILOR & TECHNICAL ASSESSMENT DTO SCHEMAS
# ----------------------------------------------------------------------------

class ATSResumeAnalysisRequest(BaseModel):
    candidate_id: str = Field(..., description="Candidate student identifier")
    job_id: str = Field(..., description="Target job or internship listing identifier")
    role_title: str = Field(..., description="Job role title (e.g. Junior Python Engineer)")
    cv_text: str = Field(..., description="Extracted plain-text from cryptographic CV snapshot")
    target_skills: List[str] = Field(default_factory=list, description="Target skillset required by employer")


class SubmitTechnicalAssessmentRequest(BaseModel):
    candidate_id: str = Field(..., description="Candidate student identifier")
    assessment_id: str = Field(..., description="Unique assessment problem identifier")
    language: str = Field("python", description="Programming language: python, javascript, sql")
    code_solution: str = Field(..., description="Source code submitted for automated testing")
    time_spent_seconds: int = Field(..., ge=0, description="Time spent solving the challenge")
