"""
========================================================================================
MODULE:    Opportunity Layer, CV Snapshots & Immutable Audit Models
TOPIC:     Tuition Marketplace, Evidence Portfolios, Job Applications & Audit Trails
FILE:      backend/app/models/opportunity.py
PURPOSE:   Implements entities for the real-world opportunity layer. Realizes the
           safe tuition marketplace with bilateral contact consent, skill evidence
           tracking (GitHub, live demos, certificates), immutable CV snapshots that
           freeze applicant data upon submission, and comprehensive audit logs.
AUDIENCE:  Marketplace Engineers, Trust & Safety Teams & AI Agents
STANDARDS: Data Minimization, Immutable CV Snapshots, OWASP ASVS L2 Audit Trail
========================================================================================
"""

from typing import Any, Dict, Optional
from backend.app.models.base import BaseModel


class TuitionListing(BaseModel):
    """
    Structured tuition offer or request with district/thana geographic scoping.
    """
    def __init__(
        self,
        creator_user_id: str,
        class_grade: int,
        curriculum: str,
        medium: str,
        subject: str,
        location_district: str,
        location_thana: str,
        is_online: bool = False,
        salary_range_min: Optional[int] = None,
        salary_range_max: Optional[int] = None,
        status: str = "PUBLISHED",  # 'DRAFT', 'PUBLISHED', 'CLOSED', 'REPORTED'
        **kwargs
    ):
        super().__init__(**kwargs)
        self.creator_user_id = creator_user_id
        self.class_grade = class_grade
        self.curriculum = curriculum
        self.medium = medium
        self.subject = subject
        self.location_district = location_district
        self.location_thana = location_thana
        self.is_online = is_online
        self.salary_range_min = salary_range_min
        self.salary_range_max = salary_range_max
        self.status = status


class TuitionApplication(BaseModel):
    """
    Tutor application with bilateral consent requirements before phone disclosure.
    """
    def __init__(
        self,
        listing_id: str,
        tutor_user_id: str,
        message: str = "",
        contact_consent_granted: bool = False,
        status: str = "APPLIED",  # 'APPLIED', 'SHORTLISTED', 'ACCEPTED', 'REJECTED'
        **kwargs
    ):
        super().__init__(**kwargs)
        self.listing_id = listing_id
        self.tutor_user_id = tutor_user_id
        self.message = message
        self.contact_consent_granted = contact_consent_granted
        self.status = status


class StudentSkill(BaseModel):
    """
    Evidence-backed skill claim linked to code repositories, certificates, or projects.
    """
    def __init__(
        self,
        student_id: str,
        skill_name: str,
        proficiency: str = "INTERMEDIATE",  # 'BEGINNER', 'INTERMEDIATE', 'ADVANCED'
        evidence_url: Optional[str] = None,
        is_verified: bool = False,
        verified_by: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.student_id = student_id
        self.skill_name = skill_name
        self.proficiency = proficiency
        self.evidence_url = evidence_url
        self.is_verified = is_verified
        self.verified_by = verified_by


class CVSnapshot(BaseModel):
    """
    Immutable frozen snapshot of a student's profile submitted to an employer.
    Subsequent edits to general profile do not alter submitted snapshots.
    """
    def __init__(
        self,
        user_id: str,
        title: str,
        snapshot_json: Dict[str, Any],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.title = title
        self.snapshot_json = snapshot_json


class JobListing(BaseModel):
    """
    Verified employer job or internship posting.
    """
    def __init__(
        self,
        employer_user_id: str,
        company_name: str,
        title: str,
        is_company_verified: bool = False,
        work_mode: str = "HYBRID",  # 'ONSITE', 'REMOTE', 'HYBRID'
        salary_range: Optional[str] = None,
        status: str = "ACTIVE",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.employer_user_id = employer_user_id
        self.company_name = company_name
        self.is_company_verified = is_company_verified
        self.title = title
        self.work_mode = work_mode
        self.salary_range = salary_range
        self.status = status


class JobApplication(BaseModel):
    """
    Candidate application tied to an immutable CV snapshot.
    """
    def __init__(
        self,
        job_id: str,
        candidate_user_id: str,
        cv_snapshot_id: str,
        stage: str = "APPLIED",  # 'APPLIED', 'VIEWED', 'INTERVIEW', 'OFFER', 'REJECTED'
        **kwargs
    ):
        super().__init__(**kwargs)
        self.job_id = job_id
        self.candidate_user_id = candidate_user_id
        self.cv_snapshot_id = cv_snapshot_id
        self.stage = stage


class AuditLog(BaseModel):
    """
    Immutable security and administration audit log.
    """
    def __init__(
        self,
        actor_id: str,
        actor_role: str,
        action: str,
        entity_type: str,
        entity_id: str,
        reason: str,
        payload_before: Optional[Dict[str, Any]] = None,
        payload_after: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.actor_id = actor_id
        self.actor_role = actor_role
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.reason = reason
        self.payload_before = payload_before
        self.payload_after = payload_after
        self.ip_address = ip_address
