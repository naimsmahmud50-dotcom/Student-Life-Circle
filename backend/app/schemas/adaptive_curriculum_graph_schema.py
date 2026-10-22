"""
================================================================================
MODULE: AI Adaptive Curriculum, Bayesian Knowledge Graph & Memory Decay Schemas
TOPIC: Pydantic Data Contracts for Knowledge DAG, BKT Updates & Forgetting Curve
FILE: backend/app/schemas/adaptive_curriculum_graph_schema.py
PURPOSE: Strict data validation schemas for Phase 65 Adaptive Curriculum Engine.
================================================================================
"""

from enum import Enum
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


class BloomTaxonomyLevel(str, Enum):
    REMEMBER = "REMEMBER"
    UNDERSTAND = "UNDERSTAND"
    APPLY = "APPLY"
    ANALYZE = "ANALYZE"
    EVALUATE = "EVALUATE"
    CREATE = "CREATE"


class RelationType(str, Enum):
    PREREQUISITE = "PREREQUISITE"
    CO_REQUISITE = "CO_REQUISITE"
    EXTENSION = "EXTENSION"
    APPLICATION = "APPLICATION"


class ConceptNodeDTO(BaseModel):
    concept_id: str = Field(..., description="Unique concept node ID (e.g., MATH-CALC-001)")
    title: str = Field(..., description="Standard academic concept title")
    subject: str = Field(..., description="Academic subject e.g. Higher Mathematics, Physics")
    grade_level: str = Field(..., description="Class or level e.g. HSC Class 11-12")
    bloom_level: str = Field("UNDERSTAND", description="Bloom taxonomy cognitive depth")
    estimated_minutes: int = Field(45, description="Typical study time to grasp concept")
    description: str = Field("", description="Pedagogical description of the concept")
    prerequisites: List[str] = Field(default_factory=list, description="Immediate prerequisite concept IDs")
    learning_objectives: List[str] = Field(default_factory=list, description="Measurable mastery outcomes")


class KnowledgeEdgeDTO(BaseModel):
    source_id: str = Field(..., description="Prerequisite concept node ID")
    target_id: str = Field(..., description="Downstream concept node ID")
    relation_type: str = Field("PREREQUISITE", description="Edge relationship type")
    weight: float = Field(1.0, description="Strength of prerequisite coupling [0.0 - 1.0]")


class StudentMasteryStateDTO(BaseModel):
    student_id: str = Field(..., description="Learner ID")
    concept_id: str = Field(..., description="Target concept ID")
    p_mastery: float = Field(0.1, description="Current Bayesian Knowledge Tracing mastery probability [0.0 - 1.0]")
    review_count: int = Field(0, description="Total number of reviews/practice attempts")
    last_practiced_at: str = Field(..., description="ISO 8601 timestamp of last interaction")
    stability_days: float = Field(1.0, description="Ebbinghaus memory stability S in days")
    retention_probability: float = Field(1.0, description="Projected current recall probability R(t)")
    history_correct: int = Field(0, description="Count of correct responses")
    history_incorrect: int = Field(0, description="Count of incorrect responses")


class BktUpdateRequest(BaseModel):
    student_id: str = Field(..., description="Learner ID")
    concept_id: str = Field(..., description="Concept node ID being assessed")
    is_correct: bool = Field(..., description="Whether the student answered correctly")
    p_prior: Optional[float] = Field(None, description="Initial mastery prior P(L_t-1). Defaults to current state")
    p_guess: Optional[float] = Field(0.20, description="Probability of guessing correctly without mastery P(G)")
    p_slip: Optional[float] = Field(0.10, description="Probability of slipping/making a mistake despite mastery P(S)")
    p_transit: Optional[float] = Field(0.15, description="Probability of learning/transitioning on this step P(T)")


class BktUpdateResponse(BaseModel):
    student_id: str
    concept_id: str
    previous_mastery: float
    posterior_mastery: float
    new_mastery: float
    delta: float
    mastery_classification: str
    is_mastered: bool
    retention_projection_7d: float
    retention_projection_30d: float
    timestamp: str


class RemedialPathwayRequest(BaseModel):
    student_id: str = Field(..., description="Learner ID")
    failed_concept_id: str = Field(..., description="Concept where the student failed a quiz or exam item")
    max_depth: Optional[int] = Field(3, description="Maximum upward traversal depth in DAG")


class RemedialPathwayResponse(BaseModel):
    student_id: str
    failed_concept_id: str
    root_cause_concept_id: str
    root_cause_title: str
    identified_gaps: List[Dict[str, Any]]
    remedial_sequence: List[Dict[str, Any]]
    estimated_recovery_hours: float
    action_plan: str
    traversal_depth: int


class AdaptiveScheduleRequest(BaseModel):
    student_id: str = Field(..., description="Learner ID")
    subject: str = Field("Higher Mathematics", description="Subject for study plan")
    available_hours_per_day: float = Field(2.0, description="Study hours student can commit daily")
    horizon_days: int = Field(7, description="Number of days in schedule")


class AdaptiveScheduleResponse(BaseModel):
    student_id: str
    subject: str
    horizon_days: int
    daily_sessions: List[Dict[str, Any]]
    total_target_concepts: int
    decayed_concepts_reviewed: int
    new_concepts_introduced: int
    predicted_retention_gain: float
    generated_at: str


class CurriculumGraphResponse(BaseModel):
    subject: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    total_concepts: int
    total_prerequisites: int
    topological_levels: int
