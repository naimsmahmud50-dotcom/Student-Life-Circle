"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Exam Routine & Model Test Calendar Schemas
TOPIC:     Pydantic v2 / Resilient BaseDTO Contracts for Routine Hub
FILE:      backend/app/schemas/exam_routine_schema.py
PURPOSE:   Defines typed request and response schemas for 200-day BCS and Admission
           routine calendars, Friday Mega Model Test countdowns, negative marking
           simulations, and reminder subscription payloads.
STANDARDS: Pydantic v2 / Resilient BaseDTO, Python 3.12+ Type Annotations, Zero-Emoji
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


class ExamTypeEnum(str, Enum):
    BCS_PRELI = "BCS_PRELI"
    ADMISSION_VARSITY = "ADMISSION_VARSITY"
    HSC_BOARD = "HSC_BOARD"
    BANK_OFFICER = "BANK_OFFICER"


class TrackCategoryEnum(str, Enum):
    BANGLA = "BANGLA"
    ENGLISH = "ENGLISH"
    MATH_SCIENCE = "MATH_SCIENCE"
    GK = "GK"
    GENERAL = "GENERAL"


class ExamRoutineItem(BaseDTO):
    def __init__(
        self,
        id: str,
        routine_code: str,
        title: str,
        exam_type: ExamTypeEnum,
        track_category: TrackCategoryEnum,
        day_number: int,
        syllabus_summary: str,
        start_time: str,
        end_time: str,
        duration_minutes: int = 60,
        total_questions: int = 100,
        total_marks: float = 100.0,
        negative_mark_factor: float = 0.25,
        is_mega_model_test: bool = False,
        is_published: bool = True,
        live_participant_count: int = 0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.id = id
        self.routine_code = routine_code
        self.title = title
        self.exam_type = exam_type
        self.track_category = track_category
        self.day_number = day_number
        self.syllabus_summary = syllabus_summary
        self.start_time = start_time
        self.end_time = end_time
        self.duration_minutes = duration_minutes
        self.total_questions = total_questions
        self.total_marks = total_marks
        self.negative_mark_factor = negative_mark_factor
        self.is_mega_model_test = is_mega_model_test
        self.is_published = is_published
        self.live_participant_count = live_participant_count


class ExamRoutineListResponse(BaseDTO):
    def __init__(
        self,
        success: bool = True,
        routines: Optional[List[ExamRoutineItem]] = None,
        total: int = 0,
        active_day: int = 1,
        mega_test_scheduled_at: Optional[str] = None,
        server_time: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.success = success
        self.routines = routines or []
        self.total = total
        self.active_day = active_day
        self.mega_test_scheduled_at = mega_test_scheduled_at
        self.server_time = server_time


class NegativeMarkSimulationRequest(BaseDTO):
    def __init__(
        self,
        total_questions: int,
        correct_answers: int,
        wrong_answers: int,
        unanswered: int,
        negative_factor: float = 0.25,
        mark_per_question: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        if total_questions < 1:
            raise ValueError("total_questions must be at least 1")
        if correct_answers < 0 or wrong_answers < 0 or unanswered < 0:
            raise ValueError("correct_answers, wrong_answers, and unanswered must be non-negative integers")
        if negative_factor < 0:
            raise ValueError("negative_factor cannot be negative")
        if mark_per_question <= 0:
            raise ValueError("mark_per_question must be strictly positive")
        if (correct_answers + wrong_answers + unanswered) != total_questions:
            raise ValueError(f"Sum of correct ({correct_answers}), wrong ({wrong_answers}), and unanswered ({unanswered}) must equal total ({total_questions})")
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.wrong_answers = wrong_answers
        self.unanswered = unanswered
        self.negative_factor = negative_factor
        self.mark_per_question = mark_per_question


class NegativeMarkSimulationResponse(BaseDTO):
    def __init__(
        self,
        success: bool = True,
        total_questions: int = 0,
        correct_answers: int = 0,
        wrong_answers: int = 0,
        unanswered: int = 0,
        gross_score: float = 0.0,
        penalty_deducted: float = 0.0,
        net_score: float = 0.0,
        accuracy_percentage: float = 0.0,
        estimated_percentile: float = 0.0,
        merit_bracket: str = "",
        weakness_flags: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.success = success
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.wrong_answers = wrong_answers
        self.unanswered = unanswered
        self.gross_score = gross_score
        self.penalty_deducted = penalty_deducted
        self.net_score = net_score
        self.accuracy_percentage = accuracy_percentage
        self.estimated_percentile = estimated_percentile
        self.merit_bracket = merit_bracket
        self.weakness_flags = weakness_flags or []


class RoutineSubscribeRequest(BaseDTO):
    ALLOWED_CHANNELS = {"IN_APP", "PUSH", "EMAIL", "SMS"}

    def __init__(
        self,
        routine_id: str,
        channels: Optional[List[str]] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        if not routine_id or not isinstance(routine_id, str):
            raise ValueError("routine_id is required")
        if len(routine_id) > 100:
            raise ValueError("routine_id exceeds maximum allowed length of 100 characters")
        sanitized_channels = []
        for ch in (channels or ["IN_APP", "PUSH"]):
            if isinstance(ch, str) and ch.upper() in self.ALLOWED_CHANNELS:
                sanitized_channels.append(ch.upper())
        if not sanitized_channels:
            sanitized_channels = ["IN_APP", "PUSH"]
        self.routine_id = routine_id.strip()
        self.channels = sanitized_channels


class RoutineSubscribeResponse(BaseDTO):
    def __init__(
        self,
        success: bool = True,
        subscription_id: str = "",
        routine_id: str = "",
        subscribed_channels: Optional[List[str]] = None,
        message: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.success = success
        self.subscription_id = subscription_id
        self.routine_id = routine_id
        self.subscribed_channels = subscribed_channels or []
        self.message = message
