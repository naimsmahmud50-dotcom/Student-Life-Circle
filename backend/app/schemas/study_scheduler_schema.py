"""
===================================================================================
Module: Study Scheduler & Burnout Shield Schemas (রুটিন ও বার্নআউট স্কিমা)
Topic: Dual-Resilience Pydantic v2 / BaseDTO Validation Contracts
File: backend/app/schemas/study_scheduler_schema.py
Purpose: Defines strictly validated input request and response models for circadian
         daily routine generation, Pomodoro focus sprints, and real-time burnout
         fatigue assessments.
Audience: Backend Engineers, API Client Developers, Schema Validators
Standards: OpenAPI 3.1.0 Standard, Pydantic v2 Core Models, Zero-Emoji
===================================================================================
"""

from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field

    class DailyScheduleGenerateRequest(BaseModel):
        student_id: str = Field(..., description="শিক্ষার্থীর ইউনিক আইডি")
        available_hours: float = Field(6.5, ge=1.0, le=16.0, description="দৈনিক উপলব্ধ পড়াশোনার মোট ঘণ্টা")
        weak_subjects: Optional[List[str]] = Field(default_factory=list, description="দুর্বল বিষয়সমূহের তালিকা")
        target_exam: str = Field("HSC_SCIENCE", description="টার্গেট পরীক্ষা")
        wake_time: str = Field("06:30", description="ঘুম থেকে ওঠার সময়")
        bedtime: str = Field("23:00", description="ঘুমাতে যাওয়ার সময়")

    class FocusSprintStartRequest(BaseModel):
        student_id: str = Field(..., description="শিক্ষার্থীর ইউনিক আইডি")
        slot_id: str = Field(..., description="রুটিনের স্লট আইডি")
        duration_minutes: int = Field(25, ge=10, le=90, description="পরিকল্পিত ফোকাস সময় (মিনিট)")
        sprint_type: str = Field("POMODORO_25", description="স্প্রিন্ট টাইপ")

    class FocusSprintCompleteRequest(BaseModel):
        actual_duration_minutes: int = Field(..., ge=1, le=180, description="প্রকৃত পড়াশোনার সময় (মিনিট)")
        distraction_count: int = Field(0, ge=0, description="মনোযোগ বিচ্যুতি সংখ্যা")
        self_reported_focus_score: int = Field(5, ge=1, le=5, description="শিক্ষার্থীর স্ব-মূল্যায়িত একাগ্রতা (১-৫)")

    class BurnoutEvaluationRequest(BaseModel):
        student_id: str = Field(..., description="শিক্ষার্থীর ইউনিক আইডি")
        continuous_study_hours: float = Field(..., ge=0.0, le=18.0, description="বিরতিহীন একটানা পড়ার সময়কাল (ঘণ্টা)")
        sleep_hours_last_night: float = Field(7.5, ge=0.0, le=16.0, description="গত রাতে মোট ঘুমের সময় (ঘণ্টা)")
        total_study_hours_today: float = Field(4.0, ge=0.0, le=20.0, description="আজকের দিনের মোট পড়ার সময় (ঘণ্টা)")
        break_minutes_today: float = Field(30.0, ge=0.0, le=360.0, description="আজকের মোট বিরতির সময় (মিনিট)")
        is_minor: bool = Field(True, description="শিক্ষার্থী অপ্রাপ্তবয়স্ক কিনা (ASVS অভিভাবক সুরক্ষা)")

except ImportError:
    # Graceful Fallback DTO for environments without pydantic
    class BaseDTO:
        def __init__(self, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)

        def dict(self) -> Dict[str, Any]:
            return self.__dict__

    class DailyScheduleGenerateRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(
            self,
            student_id: str = "",
            available_hours: float = 6.5,
            weak_subjects: Optional[List[str]] = None,
            target_exam: str = "HSC_SCIENCE",
            wake_time: str = "06:30",
            bedtime: str = "23:00",
            **kwargs: Any
        ) -> None:
            super().__init__(
                student_id=student_id,
                available_hours=available_hours,
                weak_subjects=weak_subjects or [],
                target_exam=target_exam,
                wake_time=wake_time,
                bedtime=bedtime,
                **kwargs
            )

    class FocusSprintStartRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(
            self,
            student_id: str = "",
            slot_id: str = "",
            duration_minutes: int = 25,
            sprint_type: str = "POMODORO_25",
            **kwargs: Any
        ) -> None:
            super().__init__(
                student_id=student_id,
                slot_id=slot_id,
                duration_minutes=duration_minutes,
                sprint_type=sprint_type,
                **kwargs
            )

    class FocusSprintCompleteRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(
            self,
            actual_duration_minutes: int = 25,
            distraction_count: int = 0,
            self_reported_focus_score: int = 5,
            **kwargs: Any
        ) -> None:
            super().__init__(
                actual_duration_minutes=actual_duration_minutes,
                distraction_count=distraction_count,
                self_reported_focus_score=self_reported_focus_score,
                **kwargs
            )

    class BurnoutEvaluationRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(
            self,
            student_id: str = "",
            continuous_study_hours: float = 2.0,
            sleep_hours_last_night: float = 7.5,
            total_study_hours_today: float = 4.0,
            break_minutes_today: float = 30.0,
            is_minor: bool = True,
            **kwargs: Any
        ) -> None:
            super().__init__(
                student_id=student_id,
                continuous_study_hours=continuous_study_hours,
                sleep_hours_last_night=sleep_hours_last_night,
                total_study_hours_today=total_study_hours_today,
                break_minutes_today=break_minutes_today,
                is_minor=is_minor,
                **kwargs
            )
