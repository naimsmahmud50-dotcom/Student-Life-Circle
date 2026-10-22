"""
========================================================================================
MODULE:    Live Challenge & Admission Engine Schemas
TOPIC:     Data Transfer Objects for Nationwide Contests, Mocks & Diagnostic Sprints
FILE:      backend/app/schemas/live_and_admission_schema.py
PURPOSE:   Defines request and response validation contracts for Scheduled Live
           Challenges and Admission Diagnostic Mocks. Resiliently runs with Pydantic
           v2 or fallback BaseDTO.
AUDIENCE:  Exam Architects, Analytics Specialists & AI Agents
STANDARDS: Server Authoritative Time, Psychometric Transparency, Non-Emoji Microcopy
========================================================================================
"""

from typing import Optional, List, Dict, Any
from backend.app.schemas.quiz_schema import BaseDTO


class LiveSessionPrewarmRequest(BaseDTO):
    """Payload to pre-warm a scheduled live challenge blueprint into cache."""
    blueprint_title: str
    start_time: str
    end_time: str
    duration_minutes: int = 25
    questions: Optional[List[Dict[str, Any]]] = None


class LeaderboardOptOutRequest(BaseDTO):
    """Payload to toggle student's public leaderboard visibility for mental peace."""
    opt_out: bool = True


class DiagnosticAnalyzeRequest(BaseDTO):
    """Payload containing topic accuracy metrics to generate a 7-day revision sprint."""
    topic_performance: List[Dict[str, Any]]


class AIDraftGenerateRequest(BaseDTO):
    """Payload for generating an AI question draft."""
    subject: str = "পদার্থবিজ্ঞান ১ম পত্র"
    topic: str = "গতিবিদ্যা ও বলবিদ্যা"
    concept: str = "সুষম ত্বরণে দূরত্বের সমীকরণ"
    cognitive_level: str = "APPLICATION"
    curriculum: str = "NCTB_2024"
    class_grade: int = 10


class SMEReviewDecisionRequest(BaseDTO):
    """Payload for SME approval or rejection of an AI draft."""
    approve: bool = True
    rejection_reason: Optional[str] = None

