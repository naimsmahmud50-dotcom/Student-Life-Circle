"""
========================================================================================
MODULE:    Security Policy & Offline Sync DTO Schemas
TOPIC:     Data Transfer Objects for Batch Offline Replay, Manifests & Security Policies
FILE:      backend/app/schemas/security_and_offline_schema.py
PURPOSE:   Defines request and response payload contracts for:
           1. PWA offline batch sync queues with idempotent replay tokens.
           2. Low-bandwidth offline practice manifest queries.
           3. Enterprise security headers and rate-limiting policy inspection.
AUDIENCE:  API Engineers, Mobile PWA Developers & AI Agents
STANDARDS: BaseDTO Resilience, PWA Offline-First, Zero-Emoji Spec
========================================================================================
"""

from typing import Optional, List, Dict, Any
from backend.app.schemas.quiz_schema import BaseDTO


class OfflineAnswerItemDTO(BaseDTO):
    """Buffered individual answer recorded while student was offline."""
    question_version_id: str
    selected_option_id: Optional[str] = None
    idempotency_key: str
    time_taken_seconds: float = 0.0


class OfflineSyncBatchRequest(BaseDTO):
    """Payload containing a list of buffered answers to sync upon reconnection."""
    student_id: str
    attempt_id: str
    buffered_answers: List[Dict[str, Any]]


class SecurityProfileSanitizeRequest(BaseDTO):
    """Payload to test or request minor data sanitization under ASVS L2."""
    student_profile: Dict[str, Any]
    requester_user_id: Optional[str] = None
    requester_roles: Optional[List[str]] = None
    authorized_guardian_ids: Optional[List[str]] = None
