"""
========================================================================================
MODULE:    Opportunity Schemas: Tuition Marketplace & Career Engine
TOPIC:     Data Transfer Objects for Tuition Listings, Consent & CV Snapshots
FILE:      backend/app/schemas/opportunity_schema.py
PURPOSE:   Defines request and response validation contracts for the Tuition Marketplace
           and Student Career Engine. Resiliently runs with Pydantic v2 or fallback BaseDTO.
AUDIENCE:  Marketplace Engineers, Career Service Devs & AI Agents
STANDARDS: Strict Type Contracts, Data Minimization, ASVS L2 Privacy
========================================================================================
"""

from typing import Optional, List, Dict, Any
from backend.app.schemas.quiz_schema import BaseDTO


class TuitionListingCreateRequest(BaseDTO):
    """Payload for creating a new tuition listing."""
    class_grade: int
    curriculum: str = "NCTB"
    medium: str = "BANGLA"
    subject: str
    location_district: str
    location_thana: str
    is_online: bool = False
    salary_range_min: Optional[int] = 3000
    salary_range_max: Optional[int] = 5000


class TuitionApplyRequest(BaseDTO):
    """Payload when a verified tutor applies to an open tuition listing."""
    message: str = "আমি এই বিষয়ের উপর পাঠদানে আগ্রহী ও অভিজ্ঞ।"


class ContactConsentGrantRequest(BaseDTO):
    """Payload when a learner or guardian grants bilateral contact access."""
    tutor_user_id: str


class StudentSkillAddRequest(BaseDTO):
    """Payload to add a verified or evidence-backed skill claim to student profile."""
    skill_name: str
    proficiency: str = "INTERMEDIATE"  # BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
    evidence_url: Optional[str] = None


class CVSnapshotCreateRequest(BaseDTO):
    """Payload to freeze candidate qualifications into an immutable JSON snapshot."""
    application_title: str
    student_data: Dict[str, Any]


class JobApplicationSubmitRequest(BaseDTO):
    """Payload to submit candidate application referencing a frozen CV snapshot."""
    job_id: str
    cv_snapshot_id: str


class ApplicationStageUpdateRequest(BaseDTO):
    """Payload for recruiter pipeline state transitions."""
    new_stage: str  # SAVED, APPLIED, VIEWED, SHORTLISTED, INTERVIEW, OFFER, REJECTED
