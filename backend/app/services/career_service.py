"""
========================================================================================
MODULE:    Career Engine, Evidence Portfolio & Immutable CV Snapshot Service
TOPIC:     Skill Evidence, Immutable Application Snapshots & Hiring Pipeline Stages
FILE:      backend/app/services/career_service.py
PURPOSE:   Powers student transition to internships and professional careers.
           Manages evidence-backed portfolio claims (GitHub repositories, live demos,
           credential issuers), generates immutable frozen CV snapshots per job
           application (preventing retro-editing), and tracks hiring pipelines.
AUDIENCE:  Career Services Engineers, Technical Recruiters & AI Agents
STANDARDS: Data Minimization, Immutable Snapshot Architecture, Non-Discrimination
========================================================================================
"""

import copy
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any

from backend.app.models.opportunity import StudentSkill, CVSnapshot, JobListing, JobApplication


class CareerService:
    """
    Evidence-backed portfolio and career application service.
    """

    def __init__(self):
        self._skills: Dict[str, List[StudentSkill]] = {}  # user_id -> skills
        self._snapshots: Dict[str, CVSnapshot] = {}
        self._jobs: Dict[str, JobListing] = {}
        self._applications: Dict[str, JobApplication] = {}

    def add_student_skill(
        self,
        student_id: str,
        skill_name: str,
        proficiency: str = "INTERMEDIATE",
        evidence_url: Optional[str] = None
    ) -> StudentSkill:
        """Adds a verified or evidence-linked skill record."""
        skill = StudentSkill(
            student_id=student_id,
            skill_name=skill_name,
            proficiency=proficiency,
            evidence_url=evidence_url,
            is_verified=bool(evidence_url)  # Basic verification flag
        )
        if student_id not in self._skills:
            self._skills[student_id] = []
        self._skills[student_id].append(skill)
        return skill

    def create_cv_snapshot(
        self,
        user_id: str,
        application_title: str,
        student_data: Dict[str, Any]
    ) -> CVSnapshot:
        """
        Freezes an immutable JSON snapshot of candidate qualifications.
        Future updates to the user's active profile will NOT rewrite this snapshot.
        Uses copy.deepcopy to prevent nested reference mutations.
        """
        snapshot = CVSnapshot(
            user_id=user_id,
            title=application_title,
            snapshot_json=copy.deepcopy(student_data)  # True deep frozen copy
        )
        self._snapshots[snapshot.id] = snapshot
        return snapshot

    def get_cv_snapshot(
        self,
        snapshot_id: str,
        user_id: Optional[str] = None
    ) -> Tuple[bool, Optional[CVSnapshot], str]:
        """
        Retrieves a candidate's frozen CV snapshot.
        Enforces IDOR prevention: if user_id is provided, it must match snapshot.user_id.
        """
        snapshot = self._snapshots.get(snapshot_id)
        if not snapshot:
            return False, None, "SNAPSHOT_NOT_FOUND"

        if user_id and snapshot.user_id != user_id:
            return False, None, "FORBIDDEN_SNAPSHOT_OWNERSHIP"

        return True, snapshot, "OK"


    def submit_job_application(
        self,
        job_id: str,
        candidate_user_id: str,
        cv_snapshot_id: str
    ) -> Tuple[bool, Optional[JobApplication], str]:
        """Submits an application linked to an immutable CV snapshot."""
        job = self._jobs.get(job_id)
        if not job or job.status != "ACTIVE":
            return False, None, "JOB_NOT_FOUND_OR_CLOSED"

        snapshot = self._snapshots.get(cv_snapshot_id)
        if not snapshot or snapshot.user_id != candidate_user_id:
            return False, None, "INVALID_OR_UNAUTHORIZED_CV_SNAPSHOT"

        app_key = f"{job_id}:{candidate_user_id}"
        if app_key in self._applications:
            return False, None, "ALREADY_APPLIED"

        app = JobApplication(
            job_id=job_id,
            candidate_user_id=candidate_user_id,
            cv_snapshot_id=cv_snapshot_id,
            stage="APPLIED"
        )
        self._applications[app_key] = app
        return True, app, "OK"

    def update_application_stage(
        self,
        job_id: str,
        candidate_user_id: str,
        new_stage: str
    ) -> Tuple[bool, str]:
        """Recruiter updates hiring stage: Applied -> Viewed -> Interview -> Offer."""
        app_key = f"{job_id}:{candidate_user_id}"
        app = self._applications.get(app_key)
        if not app:
            return False, "APPLICATION_NOT_FOUND"

        valid_stages = {"SAVED", "APPLIED", "VIEWED", "SHORTLISTED", "INTERVIEW", "OFFER", "REJECTED"}
        if new_stage not in valid_stages:
            return False, "INVALID_STAGE"

        app.stage = new_stage
        return True, "STAGE_UPDATED"


# Singleton Service Instance
career_service = CareerService()
