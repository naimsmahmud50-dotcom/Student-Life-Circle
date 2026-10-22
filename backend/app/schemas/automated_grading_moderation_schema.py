"""
================================================================================
MODULE: Automated Exam Grading, Handwritten Script OCR & Multi-Evaluator Blind Rubric Moderation Schemas
TOPIC: Pydantic Data Contracts for Script OCR, Step-Rubrics, Divergence Arbitration & Re-Scrutiny
FILE: backend/app/schemas/automated_grading_moderation_schema.py
PURPOSE: Strict data validation schemas for Phase 64 Automated Grading & Moderation Tower.
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


class BoundingBoxDTO(BaseModel):
    box_id: str = Field(..., description="Unique ID for segmented answer region")
    page_number: int = Field(1, description="Page index where answer was detected")
    x_min: float = Field(..., description="Left normalized coordinate [0.0 - 1.0]")
    y_min: float = Field(..., description="Top normalized coordinate [0.0 - 1.0]")
    x_max: float = Field(..., description="Right normalized coordinate [0.0 - 1.0]")
    y_max: float = Field(..., description="Bottom normalized coordinate [0.0 - 1.0]")
    sub_question_tag: str = Field(..., description="Tag e.g. Q1.a, Q1.b, Q1.c, Q1.d")
    confidence_score: float = Field(0.95, description="OCR recognition confidence [0.0 - 1.0]")
    recognized_text: str = Field(..., description="Recognized Bengali/English text or LaTeX formula")
    formula_detected: bool = Field(False, description="Whether mathematical symbols/equations were recognized")


class ScriptOCRUploadRequest(BaseModel):
    script_id: str = Field(..., description="Unique examination script identifier")
    student_id: str = Field(..., description="Candidate user identifier")
    exam_id: str = Field(..., description="Exam / subject challenge identifier")
    subject: str = Field("Higher Mathematics", description="Subject name")
    total_pages: int = Field(1, description="Number of handwritten manuscript pages")
    raw_text_payload: Optional[str] = Field(None, description="Optional raw OCR stream")
    custom_bounding_boxes: Optional[List[BoundingBoxDTO]] = Field(None, description="Pre-annotated bounding boxes")


class ScriptOCRUploadResponse(BaseModel):
    script_id: str
    student_id: str
    exam_id: str
    status: str
    total_boxes_detected: int
    avg_confidence: float
    bounding_boxes: List[Dict[str, Any]]
    processed_at: str


class RubricStepDTO(BaseModel):
    step_number: int = Field(..., description="Step sequence index (1, 2, 3...)")
    step_description: str = Field(..., description="Step requirement e.g. Formula derivation, substitution")
    max_marks: float = Field(..., description="Maximum marks for this sub-step")


class RubricCriterionDTO(BaseModel):
    criterion_id: str = Field(..., description="Sub-question identifier e.g. Q1.a")
    sub_question: str = Field(..., description="Sub-question name e.g. Question 1 (a)")
    max_marks: float = Field(..., description="Maximum marks for this sub-question")
    steps: List[RubricStepDTO] = Field(default=[], description="Sub-step grading breakdown")


class RubricEvaluateRequest(BaseModel):
    script_id: str = Field(..., description="Target script ID")
    criteria: List[RubricCriterionDTO] = Field(..., description="Grading rubric criteria")
    evaluator_role: str = Field("AI_PRE_GRADER", description="Role: AI_PRE_GRADER, EXAMINER_1, EXAMINER_2")
    evaluator_id: str = Field("evaluator_sys", description="Evaluator user or agent ID")


class RubricStepAwardDTO(BaseModel):
    step_number: int
    awarded_marks: float
    remarks: str


class RubricCriterionAwardDTO(BaseModel):
    criterion_id: str
    sub_question: str
    total_awarded: float
    max_marks: float
    step_breakdown: List[RubricStepAwardDTO] = []


class RubricEvaluateResponse(BaseModel):
    script_id: str
    evaluator_id: str
    evaluator_role: str
    total_score: float
    max_possible: float
    percentage: float
    criterion_scores: List[RubricCriterionAwardDTO]
    evaluated_at: str


class ExaminerScoreSubmitRequest(BaseModel):
    script_id: str = Field(..., description="Script identifier")
    examiner_id: str = Field(..., description="Examiner user identifier")
    examiner_role: str = Field(..., description="Role: EXAMINER_1, EXAMINER_2, ARBITER_3")
    subquestion_marks: Dict[str, float] = Field(..., description="Map of subquestion to awarded marks")
    examiner_feedback: Optional[str] = Field(None, description="Optional qualitative moderation feedback")


class ExaminerScoreSubmitResponse(BaseModel):
    script_id: str
    examiner_id: str
    examiner_role: str
    total_marks: float
    max_marks: float
    submission_timestamp: str


class ModerationAuditResponse(BaseModel):
    script_id: str
    score_examiner_1: Optional[float] = None
    score_examiner_2: Optional[float] = None
    score_difference: Optional[float] = None
    divergence_percentage: Optional[float] = None
    divergence_threshold_exceeded: bool = False
    arbiter_required: bool = False
    score_arbiter: Optional[float] = None
    final_moderated_score: Optional[float] = None
    status: str
    moderation_rule: str
    timestamp: str


class ReScrutinyAuditRequest(BaseModel):
    script_id: str = Field(..., description="Target script ID to re-scrutinize")
    scrutineer_id: str = Field("board_scrutineer_01", description="Board scrutiny officer ID")
    recheck_reason: str = Field("Post-publication review request", description="Reason for audit")


class ReScrutinyAuditResponse(BaseModel):
    script_id: str
    addition_error_found: bool
    unmarked_questions_count: int
    original_marks: float
    revised_marks: float
    is_grade_changed: bool
    tamper_seal_hash: str
    audit_verdict: str
    scrutinized_at: str


class CohortDistributionResponse(BaseModel):
    exam_id: str
    total_scripts_evaluated: int
    mean_score: float
    std_deviation: float
    highest_score: float
    lowest_score: float
    outlier_scripts: List[Dict[str, Any]]
    calculated_at: str
