"""
Pydantic v2 schemas and DTOs for Phase 31:
- Autonomous AI LaTeX Mathematical Step-by-Step Problem Solver & Misconception Engine
- Decentralized Multi-Campus Alumni Job Referral Graph & Corporate Fast-Track Gateway
- Smart Voice/Audio Viva-Voce Oral Exam & Speech Cadence Simulator
Dual-resilience BaseDTO fallbacks included for robust serialization.
"""

from typing import List, Optional, Dict, Any

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


# -----------------------------------------------------------------------------
# 1. Autonomous AI Math Solver & Misconception Schemas
# -----------------------------------------------------------------------------

class SolveMathStepwiseRequest(BaseModel):
    problem_statement: str
    topic_domain: str = "CALCULUS"  # "CALCULUS", "TRIGONOMETRY", "KINEMATICS", "ALGEBRA"
    student_id: str = "std-demo"

class DerivationStep(BaseModel):
    step_number: int
    latex_expression: str
    explanation: str
    rule_applied: str
    is_crucial_step: bool = False

class StepwiseSolutionResponse(BaseModel):
    problem_id: str
    topic_domain: str
    initial_expression_latex: str
    final_answer_latex: str
    steps: List[Dict[str, Any]]
    total_steps: int
    verified: bool = True

class DiagnoseMisconceptionRequest(BaseModel):
    problem_id: str
    step_number: int
    student_derived_latex: str

class MisconceptionReport(BaseModel):
    step_number: int
    is_valid: bool
    misconception_type: Optional[str] = None
    diagnostic_feedback: str
    socratic_hint: str


# -----------------------------------------------------------------------------
# 2. Multi-Campus Alumni Referral Network Schemas
# -----------------------------------------------------------------------------

class AlumniProfileDTO(BaseModel):
    alumni_id: str
    alumni_name: str
    company: str
    role_title: str
    alma_mater: str
    department: str
    graduation_year: int
    max_monthly_referrals: int = 5
    active_referrals_count: int = 0

class CreateReferralEndorsementRequest(BaseModel):
    alumni_id: str
    student_id: str
    student_name: str
    target_role: str
    endorsement_notes: str = ""

class ReferralEndorsementResponse(BaseModel):
    referral_id: str
    alumni_id: str
    alumni_name: str
    student_id: str
    student_name: str
    target_company: str
    target_role: str
    endorsement_token: str
    hmac_signature: str
    status: str  # "ISSUED", "SUBMITTED", "EMPLOYER_REVIEW", "INTERVIEW_SCHEDULED"
    created_at: str


# -----------------------------------------------------------------------------
# 3. Smart Voice Viva-Voce Oral Simulator Schemas
# -----------------------------------------------------------------------------

class StartVivaSessionRequest(BaseModel):
    student_id: str
    viva_category: str = "TECH_BACKEND"  # "TECH_BACKEND", "BCS_ORAL", "BUET_ADMISSION"
    difficulty: str = "INTERMEDIATE"

class SubmitAudioVivaResponseRequest(BaseModel):
    session_id: str
    question_id: str
    audio_duration_seconds: float
    transcribed_text: str
    response_latency_seconds: float

class VivaQuestionEvaluation(BaseModel):
    question_id: str
    fluency_score: float  # 0 to 100
    precision_score: float  # 0 to 100
    wpm_cadence: float
    cadence_rating: str  # "OPTIMAL", "TOO_RUSHED", "HESITANT"
    feedback: str

class VivaSessionSummaryResponse(BaseModel):
    session_id: str
    student_id: str
    category: str
    overall_score: float
    average_fluency: float
    average_latency_sec: float
    question_evaluations: List[Dict[str, Any]]
    status: str  # "IN_PROGRESS", "COMPLETED"
