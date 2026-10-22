"""
================================================================================
MODULE: Schemas & Data Contracts (স্পেসড রিপিটেশন ও স্টাডি প্ল্যান স্কিমা)
TOPIC: Dual-Resilience BaseDTO Contract for SM-2 Spaced Repetition & Study Plans
FILE: backend/app/schemas/spaced_repetition_schema.py
PURPOSE: Defines strongly typed contract models for recording SM-2 review
         performance, generating adaptive weekly remediation study roadmaps, and
         completing daily learning milestones.
AUDIENCE: Frontend Engineers, Backend Controllers, API Evaluators.
STANDARDS: Pydantic v2 Contract Compatibility, SuperMemo SM-2 Quality Standard.
================================================================================
"""

from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    class BaseModel:
        def __init__(self, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self) -> Dict[str, Any]:
            return self.__dict__
    def Field(*args: Any, **kwargs: Any) -> Any:
        return kwargs.get("default", None)


class SpacedReviewRecordRequest(BaseModel):
    """Payload when recording student review recall performance for SM-2 scheduling."""
    student_id: str
    question_id: str
    topic: str
    quality_score: int  # 0 to 5 per SuperMemo SM-2


class StudyPlanGenerateRequest(BaseModel):
    """Payload to generate a personalized 7-day adaptive remediation study plan."""
    student_id: str
    class_grade: int = 8
    target_subject: str = "গণিত"
    weak_topics: Optional[List[str]] = None
    daily_available_minutes: int = 40


class MilestoneCompleteRequest(BaseModel):
    """Payload to mark a specific daily study plan milestone as finished."""
    student_id: str
    milestone_id: str
