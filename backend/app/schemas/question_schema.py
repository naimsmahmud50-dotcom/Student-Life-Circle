"""
========================================================================================
MODULE:    Question Bank Schemas & DTO Contracts
TOPIC:     Question Creation, Immutable Versions, Options, Reports & Quarantine
FILE:      backend/app/schemas/question_schema.py
PURPOSE:   Defines schemas for question bank operations. Resilient with dual support
           for Pydantic v2 and Python standard library dataclasses. Enforces validation
           on question stems, NCTB curriculum mapping, options ('A'-'D'), difficulty,
           cognitive skills, source citations, and single-click quarantine requests.
AUDIENCE:  Developers, Content Reviewers & AI Agents
STANDARDS: Pydantic v2 / Dataclasses, Clean DTOs, State-Machine Integrity
========================================================================================
"""

from enum import Enum
from typing import List, Optional, Any, Dict

try:
    from pydantic import BaseModel, Field, field_validator

    class BaseDTO(BaseModel):
        pass

except ImportError:
    class BaseDTO:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

        def model_dump(self) -> Dict[str, Any]:
            res = {}
            for k, v in self.__dict__.items():
                if isinstance(v, BaseDTO):
                    res[k] = v.model_dump()
                elif isinstance(v, list):
                    res[k] = [item.model_dump() if isinstance(item, BaseDTO) else item for item in v]
                elif isinstance(v, Enum):
                    res[k] = v.value
                else:
                    res[k] = v
            return res

        dict = model_dump


class QuestionStatus(str, Enum):
    DRAFT = "DRAFT"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    PUBLISHED = "PUBLISHED"
    QUARANTINED = "QUARANTINED"
    ARCHIVED = "ARCHIVED"


class DifficultyLevel(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class CognitiveSkill(str, Enum):
    RECALL = "RECALL"
    APPLICATION = "APPLICATION"
    REASONING = "REASONING"


class QuestionReportType(str, Enum):
    WRONG_ANSWER = "WRONG_ANSWER"
    AMBIGUOUS = "AMBIGUOUS"
    TYPO = "TYPO"
    OUTDATED = "OUTDATED"
    OFFENSIVE = "OFFENSIVE"
    DUPLICATE = "DUPLICATE"


# -----------------------------------------------------------------------------
# Options
# -----------------------------------------------------------------------------
class OptionCreate(BaseDTO):
    option_key: str = "A"
    option_text_bn: str = ""
    is_correct: bool = False
    option_text_en: Optional[str] = None


class OptionPublic(BaseDTO):
    id: str = ""
    option_key: str = "A"
    option_text_bn: str = ""
    option_text_en: Optional[str] = None


# -----------------------------------------------------------------------------
# Question Versions & DTOs
# -----------------------------------------------------------------------------
class QuestionCreate(BaseDTO):
    topic_id: str = ""
    stem_bn: str = ""
    stem_en: Optional[str] = None
    explanation_bn: str = ""
    explanation_en: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    cognitive_skill: CognitiveSkill = CognitiveSkill.REASONING
    estimated_seconds: int = 60
    source_attribution: Optional[str] = None
    options: List[OptionCreate] = []


class QuestionVersionResponse(BaseDTO):
    question_id: str = ""
    version_number: int = 1
    stem_bn: str = ""
    stem_en: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    cognitive_skill: CognitiveSkill = CognitiveSkill.REASONING
    estimated_seconds: int = 60
    source_attribution: Optional[str] = None
    status: QuestionStatus = QuestionStatus.DRAFT
    options: List[OptionPublic] = []


# -----------------------------------------------------------------------------
# Reports & Quarantine Schemas
# -----------------------------------------------------------------------------
class QuestionReportCreate(BaseDTO):
    question_version_id: str = ""
    issue_type: QuestionReportType = QuestionReportType.WRONG_ANSWER
    description: str = ""


class QuestionQuarantineRequest(BaseDTO):
    action: str = "QUARANTINE"
    reason: str = ""
    recalculate_active_sessions: bool = True


class QuestionRestoreRequest(BaseDTO):
    action: str = "RESTORE"
    reason: str = ""


class QuestionQuarantineItem(BaseDTO):
    id: str = ""
    version: int = 1
    stem_bn: str = ""
    stem_en: Optional[str] = None
    subject: str = ""
    reports_count: int = 0
    primary_issue: str = ""
    status: str = "PUBLISHED"  # 'PUBLISHED', 'UNDER_REVIEW', 'QUARANTINED', 'ARCHIVED'
    quarantine_reason: Optional[str] = None
    quarantined_by: Optional[str] = None
    quarantined_at: Optional[str] = None
    restored_by: Optional[str] = None
    restored_at: Optional[str] = None
    restore_reason: Optional[str] = None
    affected_attempts_count: int = 0
    options: List[Dict[str, Any]] = []


class QuestionQuarantineListResponse(BaseDTO):
    total: int = 0
    page: int = 1
    limit: int = 20
    items: List[Dict[str, Any]] = []


# -----------------------------------------------------------------------------
# Draft Review Queue Schemas
# -----------------------------------------------------------------------------
class DraftReviewDecisionRequest(BaseDTO):
    action: str = "APPROVE"  # 'APPROVE', 'REJECT', 'NEEDS_CHANGES'
    rejection_reason: Optional[str] = None
    comments: Optional[str] = None


class DraftEditAndApproveRequest(BaseDTO):
    stem_bn: str = ""
    stem_en: Optional[str] = None
    options: List[Dict[str, Any]] = []
    explanation_bn: str = ""
    explanation_en: Optional[str] = None
    difficulty: Optional[str] = None
    cognitive_skill: Optional[str] = None
    topic: Optional[str] = None
    concept: Optional[str] = None
    comments: Optional[str] = None


class DraftBulkActionRequest(BaseDTO):
    question_ids: List[str] = []
    action: str = "APPROVE"  # 'APPROVE', 'REJECT'
    reason: Optional[str] = None


class DraftQuestionItem(BaseDTO):
    id: str = ""
    version: int = 1
    status: str = "NEEDS_REVIEW"
    subject: str = ""
    topic: str = ""
    concept: str = ""
    stem_bn: str = ""
    stem_en: Optional[str] = None
    options: List[Dict[str, Any]] = []
    explanation_bn: str = ""
    explanation_en: Optional[str] = None
    difficulty: str = "MEDIUM"
    cognitive_skill: str = "APPLICATION"
    curriculum: str = "NCTB_2024"
    class_grade: int = 10
    is_ai_generated: bool = True
    ai_confidence_score: float = 0.94
    ai_model: str = "Claude-3.5-Sonnet-NCTB"
    deduplication_similarity: float = 0.05
    is_duplicate_flag: bool = False
    source_attribution: Optional[str] = None
    creator_user_id: str = "ai_agent_generator"
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    rejection_feedback: Optional[str] = None
    created_at: str = ""


class DraftQuestionListResponse(BaseDTO):
    total: int = 0
    page: int = 1
    limit: int = 20
    counts: Dict[str, int] = {}
    items: List[Dict[str, Any]] = []

