"""
================================================================================
MODULE: Schemas & Data Contracts (ক্রেডেনশিয়াল ও অডিট লেজার স্কিমা)
TOPIC: Dual-Resilience BaseDTO Schema for Credentials & Cryptographic Ledger
FILE: backend/app/schemas/credential_and_audit_schema.py
PURPOSE: Defines strongly typed contract models for academic credential issuance,
         public verifiable badge queries, and audit ledger integrity verification.
         Provides transparent fallback to BaseDTO if Pydantic is not globally installed.
AUDIENCE: Frontend Engineers, Backend Service Controllers, API Evaluators.
STANDARDS: Pydantic v2 Contract Compatibility, W3C Verifiable Credentials.
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


class CredentialIssueRequest(BaseModel):
    """Payload for issuing an academic mastery credential or skill badge."""
    student_id: str
    student_name: str
    is_minor: bool = False
    badge_type: str = "SUBJECT_MASTERY"
    title: str
    description: str
    subject: str
    mastery_score: float = 0.0
    evidence: Optional[Dict[str, Any]] = None


class CredentialVerificationResponse(BaseModel):
    """Response returned when an employer or third party queries a credential."""
    valid: bool
    credential_id: str
    badge_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[str] = None
    mastery_score: Optional[float] = None
    issued_at: Optional[str] = None
    issuer: Optional[Dict[str, Any]] = None
    recipient: Optional[Dict[str, Any]] = None
    status: str = "VALID"
    signature: Optional[str] = None
    verification_url: Optional[str] = None
    message: Optional[str] = None


class AuditVerificationResponse(BaseModel):
    """Cryptographic ledger integrity validation report."""
    valid: bool
    total_blocks: int
    corrupted_index: Optional[int] = None
    message: str
