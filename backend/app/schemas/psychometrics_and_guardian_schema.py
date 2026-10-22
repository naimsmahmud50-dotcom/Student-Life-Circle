"""
========================================================================================
MODULE:    Psychometrics, Guardian Safety & Dispute DTO Schemas
TOPIC:     Data Transfer Objects for Ability Tracking, Child Safety & Crowdsourced QA
FILE:      backend/app/schemas/psychometrics_and_guardian_schema.py
PURPOSE:   Defines request and response payload contracts for:
           1. Adaptive Elo psychometrics & anti-toxic streak freezes.
           2. Minor guardian pairing & legal tuition co-signatures (ASVS L2).
           3. In-app question defect disputes & moderator resolution bounties.
AUDIENCE:  API Engineers, Psychometricians, Safety Officers & AI Agents
STANDARDS: Pydantic v2 / BaseDTO fallback, ASVS L2 Child Privacy, Zero-Emoji Spec
========================================================================================
"""

from typing import Optional, List, Dict, Any
from backend.app.schemas.quiz_schema import BaseDTO


class PsychometricCalibrateRequest(BaseDTO):
    """Payload to calibrate student Elo rating based on an answered question."""
    student_id: str
    question_difficulty: float = 1200.0
    is_correct: bool


class StreakFreezeUseRequest(BaseDTO):
    """Payload to claim a Rest Day freeze pass preserving streak without penalty."""
    student_id: str


class GuardianLinkRequest(BaseDTO):
    """Payload for a guardian to pair with a minor student using a 6-digit code."""
    guardian_user_id: str
    minor_student_id: str
    pairing_token: str
    relationship: str = "PARENT"  # PARENT, FATHER, MOTHER, LEGAL_GUARDIAN


class TuitionCoSignRequest(BaseDTO):
    """Payload for a verified guardian to co-sign a tuition arrangement for a minor."""
    guardian_user_id: str
    tuition_listing_id: str
    minor_student_id: str
    guardian_notes: Optional[str] = None


class DisputeFileRequest(BaseDTO):
    """Payload for a learner to flag an erroneous question or flawed answer key."""
    student_id: str
    question_id: str
    reason: str  # WRONG_KEY, TYPO, AMBIGUOUS, OUT_OF_SYLLABUS, IMAGE_ISSUE, OTHER
    explanation: str
    quiz_attempt_id: Optional[str] = None
    suggested_correct_option: Optional[str] = None


class DisputeResolveRequest(BaseDTO):
    """Payload for an academic moderator to resolve a student question defect report."""
    moderator_id: str
    action: str  # ACCEPT_KEY_CORRECTION, ACCEPT_CONTENT_EDIT, ACCEPT_AND_QUARANTINE, REJECT_INVALID, REJECT_DUPLICATE
    resolution_notes: str
    trigger_quarantine: bool = False
    bounty_points: int = 15
