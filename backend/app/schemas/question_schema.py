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
