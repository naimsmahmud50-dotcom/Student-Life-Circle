"""
========================================================================================
MODULE:    Live MCQ Engine, Attempts & Spaced Repetition Models
TOPIC:     Test Blueprints, Live Sessions, Attempts, Answers, Results & Mastery
FILE:      backend/app/models/quiz.py
PURPOSE:   Implements entities powering the Live MCQ engine and Spaced Repetition.
           Maintains test blueprints for admission/board models, scheduled windows
           for synchronized live events, server-locked student attempts, idempotent
           answer storage, score tallies, and topic mastery revision queues.
AUDIENCE:  Engineers, Psychometricians, Scoring Specialists & AI Agents
STANDARDS: Clean Architecture, Idempotency Standard (RFC 7231), Fair Scoring
========================================================================================
"""

from typing import Optional
from backend.app.models.base import BaseModel
from backend.app.schemas.quiz_schema import QuizMode, AttemptStatus


class TestBlueprint(BaseModel):
    """
    Blueprint configuration defining exam question count, duration, and marking rules.
    """
    def __init__(
        self,
        title: str,
        mode: QuizMode,
        stage: str,
        total_questions: int,
        duration_seconds: int,
        subject_id: Optional[str] = None,
        negative_marking_value: float = 0.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.mode = mode
        self.stage = stage
        self.subject_id = subject_id
        self.total_questions = total_questions
        self.duration_seconds = duration_seconds
        self.negative_marking_value = negative_marking_value


class LiveSession(BaseModel):
    """
    Synchronized event instance for nationwide scheduled challenges.
    """
    def __init__(
        self,
        blueprint_id: str,
        title: str,
        start_time: str,
        end_time: str,
        status: str = "SCHEDULED",  # 'SCHEDULED', 'ACTIVE', 'CALCULATING', 'CLOSED'
        is_frozen: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.blueprint_id = blueprint_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.is_frozen = is_frozen


class QuizAttempt(BaseModel):
    """
    Individual student attempt bounded by server start and expiration timestamps.
    """
    def __init__(
        self,
        user_id: str,
        blueprint_id: str,
        started_at: str,
        expires_at: str,
        random_seed: int,
        live_session_id: Optional[str] = None,
        submitted_at: Optional[str] = None,
        status: AttemptStatus = AttemptStatus.IN_PROGRESS,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.blueprint_id = blueprint_id
        self.live_session_id = live_session_id
        self.started_at = started_at
        self.expires_at = expires_at
        self.submitted_at = submitted_at
        self.status = status
        self.random_seed = random_seed


class AttemptAnswer(BaseModel):
    """
    Individual answer recorded with UUID idempotency key to prevent duplication.
    """
    def __init__(
        self,
        attempt_id: str,
        question_version_id: str,
        idempotency_key: str,
        selected_option_id: Optional[str] = None,
        time_taken_seconds: float = 0.0,
        is_correct: Optional[bool] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.attempt_id = attempt_id
        self.question_version_id = question_version_id
        self.selected_option_id = selected_option_id
        self.idempotency_key = idempotency_key
        self.time_taken_seconds = time_taken_seconds
        self.is_correct = is_correct


class MasteryRecord(BaseModel):
    """
    Topic-level student mastery and SuperMemo SM-2 Spaced Repetition queue.
    """
    def __init__(
        self,
        student_id: str,
        topic_id: str,
        attempt_count: int = 0,
        correct_count: int = 0,
        last_attempted_at: Optional[str] = None,
        next_revision_due: Optional[str] = None,
        mastery_level: float = 0.0,  # 0.00 to 1.00
        is_in_mistake_queue: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.student_id = student_id
        self.topic_id = topic_id
        self.attempt_count = attempt_count
        self.correct_count = correct_count
        self.last_attempted_at = last_attempted_at
        self.next_revision_due = next_revision_due
        self.mastery_level = mastery_level
        self.is_in_mistake_queue = is_in_mistake_queue
