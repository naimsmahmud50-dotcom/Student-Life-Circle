"""
================================================================================
MODULE: Mock Interview & Career Fit Schemas (ইন্টারভিউ ও ক্যারিয়ার স্কিমা)
TOPIC: Dual-Resilience Pydantic v2 / BaseDTO Validation Contracts
FILE: backend/app/schemas/interview_and_career_matcher_schema.py
PURPOSE: Defines strictly validated input request and response models for the
         AI Mock Interview Evaluator and Algorithmic Career Fit Matcher.
         Provides automated fallback to standard dictionary-like DTO classes
         in environments where pydantic is not present.
AUDIENCE: Backend Engineers, API Client Developers, Schema Validators.
STANDARDS: OpenAPI 3.1.0 Standard, Pydantic v2 Core Models.
================================================================================
"""

from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field

    class MockInterviewStartRequest(BaseModel):
        candidate_id: str = Field(..., description="ইউনিক ক্যান্ডিডেট আইডি")
        track_id: str = Field("track_tech_swe", description="ইন্টারভিউ ট্র্যাক আইডি")
        is_minor: bool = Field(False, description="ক্যান্ডিডেট অপ্রাপ্তবয়স্ক কিনা (ASVS সুরক্ষা)")

    class MockInterviewAnswerRequest(BaseModel):
        answer_text: str = Field(..., min_length=1, description="ক্যান্ডিডেটের দেওয়া উত্তরের বিবরণ")

    class CareerFitAnalysisRequest(BaseModel):
        candidate_id: str = Field(..., description="ক্যান্ডিডেট আইডি")
        role_id: str = Field(..., description="টার্গেট ইন্ডাস্ট্রি রোল আইডি")
        candidate_skills: List[str] = Field(default_factory=list, description="ক্যান্ডিডেটের বর্তমান স্কিল তালিকা")
        verified_badges_count: int = Field(0, ge=0, description="ভেরিফায়েবল ব্যাজের সংখ্যা")
        quiz_mastery_pct: float = Field(75.0, ge=0.0, le=100.0, description="কুইজ বা ক্যাট টেস্টের গড় মেধা শতাংশ")

except ImportError:
    # Graceful Fallback DTO for environments without pydantic
    class BaseDTO:
        def __init__(self, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)

        def dict(self) -> Dict[str, Any]:
            return self.__dict__

    class MockInterviewStartRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(
            self,
            candidate_id: str = "",
            track_id: str = "track_tech_swe",
            is_minor: bool = False,
            **kwargs: Any
        ) -> None:
            super().__init__(
                candidate_id=candidate_id,
                track_id=track_id,
                is_minor=is_minor,
                **kwargs
            )

    class MockInterviewAnswerRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(self, answer_text: str = "", **kwargs: Any) -> None:
            super().__init__(answer_text=answer_text, **kwargs)

    class CareerFitAnalysisRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(
            self,
            candidate_id: str = "",
            role_id: str = "",
            candidate_skills: Optional[List[str]] = None,
            verified_badges_count: int = 0,
            quiz_mastery_pct: float = 75.0,
            **kwargs: Any
        ) -> None:
            super().__init__(
                candidate_id=candidate_id,
                role_id=role_id,
                candidate_skills=candidate_skills or [],
                verified_badges_count=verified_badges_count,
                quiz_mastery_pct=quiz_mastery_pct,
                **kwargs
            )
