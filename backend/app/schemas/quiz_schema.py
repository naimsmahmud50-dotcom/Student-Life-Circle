"""
========================================================================================
MODULE:    Quiz Engine Schemas & Execution Contracts
TOPIC:     Attempt Initialization, Idempotent Answer Saves, Scoring & Mistake Replay
FILE:      backend/app/schemas/quiz_schema.py
PURPOSE:   Specifies request and response DTOs for the Live MCQ engine. Fully resilient
           to run with Pydantic v2 when installed, or standard Python dataclasses
           with dictionary serialization methods (model_dump / dict).
AUDIENCE:  Developers, Exam System Engineers & AI Agents
STANDARDS: Pydantic v2 / Dataclasses, Idempotency Standard, OWASP ASVS L2
========================================================================================
"""

from enum import Enum
from typing import List, Optional, Any, Dict

try:
    from pydantic import BaseModel, Field

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


class QuizMode(str, Enum):
    ANYTIME_PRACTICE = "ANYTIME_PRACTICE"
    LIVE_CHALLENGE = "LIVE_CHALLENGE"
    MOCK_EXAM = "MOCK_EXAM"
    MISTAKE_REPLAY = "MISTAKE_REPLAY"


class AttemptStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"
    EXPIRED = "EXPIRED"


# -----------------------------------------------------------------------------
# Quiz Session & Attempt DTOs
# -----------------------------------------------------------------------------
class ActiveQuizQuestion(BaseDTO):
    question_version_id: str
    order: int
    stem_bn: str
    stem_en: Optional[str] = None
    options: List[dict] = []
    estimated_seconds: int = 60


class QuizAttemptStartResponse(BaseDTO):
    attempt_id: str
    status: AttemptStatus
    mode: QuizMode
    started_at: str
    expires_at: str
    server_time: str
    remaining_seconds: int
    total_questions: int
    negative_marking_value: float = 0.0
    questions: List[ActiveQuizQuestion] = []


class AnswerSaveRequest(BaseDTO):
    selected_option_id: Optional[str] = None
    time_taken_seconds: Optional[float] = None
    client_timestamp: Optional[float] = None


class AnswerSaveResponse(BaseDTO):
    status: str = "SAVED"
    attempt_id: str
    question_version_id: str
    saved_at: str
    is_session_active: bool = True


class MistakeReviewItem(BaseDTO):
    question_version_id: str
    stem_bn: str
    selected_option_key: Optional[str] = None
    correct_option_key: str
    correct_option_text_bn: str
    explanation_bn: str
    misconception_tag: Optional[str] = None
    added_to_mistake_queue: bool = True


class QuizResultResponse(BaseDTO):
    attempt_id: str
    status: AttemptStatus
    raw_score: float
    total_questions: int
    correct_count: int
    incorrect_count: int
    unanswered_count: int
    accuracy_percentage: float
    time_spent_seconds: int
    rank: Optional[int] = None
    percentile: Optional[float] = None
    mistakes: List[MistakeReviewItem] = []
    next_recommended_action: str = ""
