"""
========================================================================================
MODULE:    User Identity, Profiles & Minor Consent Domain Models
TOPIC:     Unified Accounts, Pseudonyms, Role Enums, Student Evolution & Guardian Links
FILE:      backend/app/models/user.py
PURPOSE:   Implements the core identity entities. Realizes the blueprint's principle
           of "One Profile, Lifelong Journey" where a user identity scales from school
           to career. Enforces pseudonyms for leaderboard anonymity, minor privacy
           guardrails, guardian consent approval lifecycles, and RBAC role assignments.
AUDIENCE:  Backend Developers, Security Auditors & AI Agents
STANDARDS: OWASP ASVS L2, COPPA/Minor Privacy By Default, Clean Architecture
========================================================================================
"""

from enum import Enum
from typing import List, Optional
from backend.app.models.base import BaseModel


class UserRoleEnum(str, Enum):
    STUDENT = "STUDENT"
    GUARDIAN = "GUARDIAN"
    TUTOR = "TUTOR"
    EMPLOYER = "EMPLOYER"
    CONTENT_EDITOR = "CONTENT_EDITOR"
    SUBJECT_REVIEWER = "SUBJECT_REVIEWER"
    SAFETY_MODERATOR = "SAFETY_MODERATOR"
    ADMIN = "ADMIN"


class EducationStageEnum(str, Enum):
    PRIMARY = "PRIMARY"       # Class 1-5
    MIDDLE = "MIDDLE"         # Class 6-8
    SSC = "SSC"               # Class 9-10
    HSC = "HSC"               # Class 11-12
    ADMISSION = "ADMISSION"   # University Admission Candidate
    UNIVERSITY = "UNIVERSITY" # Undergraduate / Graduate
    JOB_SEEKER = "JOB_SEEKER" # Career & Lifelong Learner


class User(BaseModel):
    """
    Core identity record. One user can maintain multiple permissioned roles.
    """
    def __init__(
        self,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        password_hash: str = "",
        full_name: str = "",
        pseudonym: str = "",  # Anonymized handle for leaderboard display (Minor safety)
        avatar_url: Optional[str] = None,
        is_phone_verified: bool = False,
        is_email_verified: bool = False,
        is_active: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.email = email
        self.phone = phone
        self.password_hash = password_hash
        self.full_name = full_name
        self.pseudonym = pseudonym or f"Learner_{self.id[:6]}"
        self.avatar_url = avatar_url
        self.is_phone_verified = is_phone_verified
        self.is_email_verified = is_email_verified
        self.is_active = is_active


class StudentProfile(BaseModel):
    """
    Learner profile that evolves across academic stages without requiring new accounts.
    """
    def __init__(
        self,
        user_id: str,
        stage: EducationStageEnum = EducationStageEnum.MIDDLE,
        class_grade: Optional[int] = 7,
        curriculum_version: str = "NCTB-2024",
        medium: str = "BANGLA",  # 'BANGLA' | 'ENGLISH_VERSION'
        target_exam: Optional[str] = None,  # e.g. 'DU_UNIT_A', 'BUET', 'MEDICAL'
        is_minor: bool = True,
        privacy_mode: str = "PRIVATE",  # 'PRIVATE', 'PSEUDONYMOUS', 'PUBLIC_PORTFOLIO'
        **kwargs
    ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.stage = stage
        self.class_grade = class_grade
        self.curriculum_version = curriculum_version
        self.medium = medium
        self.target_exam = target_exam
        self.is_minor = is_minor
        self.privacy_mode = privacy_mode


class GuardianLink(BaseModel):
    """
    Consent-managed connection between a student and their guardian.
    """
    def __init__(
        self,
        student_id: str,
        guardian_user_id: str,
        relationship: str = "PARENT",  # 'FATHER', 'MOTHER', 'LEGAL_GUARDIAN'
        consent_status: str = "PENDING",  # 'PENDING', 'APPROVED', 'REVOKED'
        approved_at: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.student_id = student_id
        self.guardian_user_id = guardian_user_id
        self.relationship = relationship
        self.consent_status = consent_status
        self.approved_at = approved_at
