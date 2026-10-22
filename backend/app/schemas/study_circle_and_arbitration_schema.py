"""
================================================================================
MODULE: Schemas & Data Contracts (স্টাডি সার্কেল ও আরবিট্রেশন ট্রাইব্যুনাল স্কিমা)
TOPIC: Dual-Resilience BaseDTO Contract for Peer Circles & Dispute Arbitration
FILE: backend/app/schemas/study_circle_and_arbitration_schema.py
PURPOSE: Defines strongly typed contract models for creating collaborative peer
         study circles, contributing solved questions to shared group goals,
         convening 3-SME arbitration tribunals, and casting consensus votes.
AUDIENCE: Frontend Engineers, Backend Controllers, API Integration Testers.
STANDARDS: Pydantic v2 Contract Compatibility, OWASP ASVS Level 2 Child Privacy.
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


class StudyCircleCreateRequest(BaseModel):
    """Payload to create a new collaborative peer study circle."""
    creator_id: str
    creator_name: str
    is_minor: bool = True
    name: str
    subject: str = "গণিত"
    class_grade: int = 8
    target_weekly_questions: int = 150


class StudyCircleJoinRequest(BaseModel):
    """Payload for a student to join an existing study circle."""
    student_id: str
    student_name: str
    is_minor: bool = True


class StudyCircleContributeRequest(BaseModel):
    """Payload when a member contributes solved practice questions to group goals."""
    student_id: str
    questions_solved: int = 1


class TribunalCaseCreateRequest(BaseModel):
    """Payload to escalate a disputed academic question to the multi-SME tribunal."""
    question_id: str
    question_stem: str
    dispute_reason: str
    filed_by_student_id: str


class TribunalVoteRequest(BaseModel):
    """Payload for an SME arbitrator to cast a vote on a tribunal case."""
    sme_id: str
    sme_name: str
    verdict: str  # "CORRECT_KEY", "QUARANTINE", "DISMISS"
    rationale: str
