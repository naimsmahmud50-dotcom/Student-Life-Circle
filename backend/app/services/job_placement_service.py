"""
========================================================================================
MODULE:    Career Placement Arena & Cryptographic CV Snapshot Service
TOPIC:     Bdjobs Benchmark - Student Internships, Immutable CV Ledger & 5-Stage Tracker
FILE:      backend/app/services/job_placement_service.py
PURPOSE:   Orchestrates student career acceleration modeled after Bdjobs:
           1. Verified Student Internships & Entry-Level Job Board (Software, AI, EdTech).
           2. Immutable Sealed CV Snapshots: Generates SHA-256 fingerprints & HMAC signatures
              freezing applicant credentials at the exact moment of application.
           3. 5-Stage Live Application Pipeline Tracker (Saved -> Applied -> Viewed -> Interview -> Offer).
           4. Cryptographic Tamper-Proofing & ATS Match Scoring based on verified skills.
STANDARDS: Cryptographic Audit Trail, OWASP ASVS L2 Non-Repudiation, Canonical Serialization
AUDIENCE:  Career Platform Engineers, Technical Recruiters & AI Agents
========================================================================================
"""

import copy
import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

_CV_SNAPSHOT_SECRET = b"agrojatra_secure_cv_snapshot_hmac_master_key_2026"


class JobPlacementService:
    """
    Enterprise Career Placement Service providing Bdjobs-level hiring workflows
    with cryptographic sealed CV snapshots and real-time pipeline telemetry.
    """

    STAGE_SAVED = "SAVED"
    STAGE_APPLIED = "APPLIED"
    STAGE_VIEWED = "VIEWED"
    STAGE_INTERVIEW = "INTERVIEW"
    STAGE_OFFER = "OFFER"
    STAGE_REJECTED = "REJECTED"

    VALID_STAGES = [STAGE_SAVED, STAGE_APPLIED, STAGE_VIEWED, STAGE_INTERVIEW, STAGE_OFFER, STAGE_REJECTED]

    def __init__(self):
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._cv_snapshots: Dict[str, Dict[str, Any]] = {}
        self._applications: Dict[str, Dict[str, Any]] = {}
        self._seed_benchmark_jobs()

    def _seed_benchmark_jobs(self):
        """Pre-seeds Bdjobs benchmark entry-level and internship opportunities."""
        seed_jobs = [
            {
                "id": "job_bs23_01",
                "employer_user_id": "emp_bs23",
                "company_name": "Brain Station 23",
                "title": "Junior Software Engineer Intern (Python / FastAPI)",
                "domain": "SOFTWARE_ENGINEERING",
                "work_mode": "HYBRID",
                "location": "Dhaka (Mohakhali DOHS)",
                "salary_range_bdt": "20,000 - 30,000 BDT/month",
                "required_skills": ["Python", "FastAPI", "PostgreSQL", "REST APIs", "Git"],
                "description": "Join our cloud enterprise engineering division. Hands-on exposure to high-scale distributed systems.",
                "status": "ACTIVE",
                "applicant_count": 8,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "job_pathao_02",
                "employer_user_id": "emp_pathao",
                "company_name": "Pathao",
                "title": "Data Analytics & Logistics Modeling Intern",
                "domain": "DATA_AI",
                "work_mode": "ONSITE",
                "location": "Dhaka (Gulshan-1)",
                "salary_range_bdt": "18,000 - 25,000 BDT/month",
                "required_skills": ["Python", "SQL", "Pandas", "Data Visualization", "Statistics"],
                "description": "Analyze fleet allocation algorithms, rider demand forecasting, and marketplace heatmaps.",
                "status": "ACTIVE",
                "applicant_count": 12,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "job_shikho_03",
                "employer_user_id": "emp_shikho",
                "company_name": "Shikho Technologies",
                "title": "EdTech STEM Curriculum & Content Associate",
                "domain": "EDTECH_STEM",
                "work_mode": "REMOTE",
                "location": "Dhaka (Remote)",
                "salary_range_bdt": "16,000 - 22,000 BDT/month",
                "required_skills": ["Calculus", "Physics", "Pedagogical Scaffolding", "Bengali & English"],
                "description": "Design interactive STEM question blueprints, Bloom's Taxonomy rubrics, and video lesson notes.",
                "status": "ACTIVE",
                "applicant_count": 5,
                "created_at": datetime.now(timezone.utc).isoformat()
            },
            {
                "id": "job_bkash_04",
                "employer_user_id": "emp_bkash",
                "company_name": "bKash Limited",
                "title": "Software Quality Assurance (SQA) & Automation Intern",
                "domain": "SOFTWARE_ENGINEERING",
                "work_mode": "HYBRID",
                "location": "Dhaka (Shadhinata Tower)",
                "salary_range_bdt": "22,000 - 32,000 BDT/month",
                "required_skills": ["Test Automation", "PyTest", "API Testing", "Postman", "CI/CD"],
                "description": "Verify high-throughput mobile financial services APIs, regression suites, and ISO 27001 compliance.",
                "status": "ACTIVE",
                "applicant_count": 14,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
        for item in seed_jobs:
            self._jobs[item["id"]] = item

    # ----------------------------------------------------------------------------------
    # TOPIC: IMMUTABLE SEALED CV SNAPSHOT LEDGER (SHA-256 + HMAC)
    # ----------------------------------------------------------------------------------

    def freeze_cv_snapshot(
        self,
        candidate_user_id: str,
        full_name: str,
        academic_institution: str,
        academic_cgpa: float,
        cat_ability_theta: float,
        verified_skills: List[str],
        portfolio_urls: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Freezes candidate qualifications into an immutable cryptographic snapshot.
        Generates canonical SHA-256 hash and HMAC-SHA256 signature to guarantee
        non-repudiation and prevent retroactive tampering by candidates or employers.
        """
        frozen_timestamp = datetime.now(timezone.utc).isoformat()
        raw_payload = {
            "candidate_user_id": candidate_user_id,
            "full_name": full_name,
            "academic_institution": academic_institution,
            "academic_cgpa": round(academic_cgpa, 2),
            "cat_ability_theta": round(cat_ability_theta, 3),
            "verified_skills": sorted(list(set(verified_skills))),
            "portfolio_urls": portfolio_urls or [],
            "frozen_timestamp": frozen_timestamp
        }

        # Canonical deterministic JSON string
        canonical_bytes = json.dumps(raw_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        sha256_hash = hashlib.sha256(canonical_bytes).hexdigest()

        # HMAC signature
        signature = hmac.new(_CV_SNAPSHOT_SECRET, canonical_bytes, hashlib.sha256).hexdigest()

        snapshot_id = f"cv_snap_{candidate_user_id[:6]}_{sha256_hash[:8]}"
        snapshot_record = {
            "snapshot_id": snapshot_id,
            "candidate_user_id": candidate_user_id,
            "payload": copy.deepcopy(raw_payload),
            "canonical_bytes": canonical_bytes.decode("utf-8"),
            "sha256_hash": sha256_hash,
            "hmac_signature": signature,
            "urn": f"urn:cv-snapshot:sha256:{sha256_hash}",
            "frozen_at": frozen_timestamp
        }
        self._cv_snapshots[snapshot_id] = snapshot_record

        return {
            "success": True,
            "snapshot": snapshot_record,
            "message": "CV Snapshot sealed cryptographically with SHA-256 and HMAC signature."
        }

    def verify_cv_snapshot(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Validates cryptographic integrity of a frozen CV snapshot.
        Verifies that content has not been tampered with since creation.
        """
        record = self._cv_snapshots.get(snapshot_id)
        if not record:
            return {
                "success": False,
                "error_code": "SNAPSHOT_NOT_FOUND",
                "message": f"Snapshot '{snapshot_id}' does not exist in audit ledger."
            }

        # Recompute canonical hash from stored payload
        recomputed_bytes = json.dumps(record["payload"], sort_keys=True, separators=(",", ":")).encode("utf-8")
        recomputed_hash = hashlib.sha256(recomputed_bytes).hexdigest()
        recomputed_sig = hmac.new(_CV_SNAPSHOT_SECRET, recomputed_bytes, hashlib.sha256).hexdigest()

        is_hash_valid = hmac.compare_digest(record["sha256_hash"], recomputed_hash)
        is_sig_valid = hmac.compare_digest(record["hmac_signature"], recomputed_sig)
        tampered = not (is_hash_valid and is_sig_valid)

        return {
            "success": True,
            "snapshot_id": snapshot_id,
            "candidate_user_id": record["candidate_user_id"],
            "sha256_hash": record["sha256_hash"],
            "is_valid": not tampered,
            "tampered": tampered,
            "frozen_at": record["frozen_at"],
            "urn": record["urn"],
            "message": "Snapshot integrity verified: 100% authentic and tamper-free." if not tampered else "TAMPERING DETECTED!"
        }

    # ----------------------------------------------------------------------------------
    # TOPIC: 5-STAGE APPLICATION PIPELINE TRACKER
    # ----------------------------------------------------------------------------------

    def submit_application_with_sealed_cv(
        self,
        job_id: str,
        candidate_user_id: str,
        cv_snapshot_id: str,
        expected_salary_bdt: Optional[int] = None,
        cover_note: str = ""
    ) -> Dict[str, Any]:
        """
        Submits job application binding the immutable sealed CV snapshot.
        Enforces candidate ownership of the snapshot to prevent spoofing.
        """
        job = self._jobs.get(job_id)
        if not job or job["status"] != "ACTIVE":
            return {
                "success": False,
                "error_code": "JOB_NOT_FOUND_OR_CLOSED",
                "message": "Job listing is closed or does not exist."
            }

        snapshot = self._cv_snapshots.get(cv_snapshot_id)
        if not snapshot or snapshot["candidate_user_id"] != candidate_user_id:
            return {
                "success": False,
                "error_code": "UNAUTHORIZED_CV_SNAPSHOT",
                "message": "You cannot submit a CV snapshot belonging to another candidate."
            }

        app_key = f"{job_id}:{candidate_user_id}"
        if app_key in self._applications:
            return {
                "success": False,
                "error_code": "ALREADY_APPLIED",
                "message": "You have already applied for this job listing."
            }

        # Calculate ATS Skill Match
        required = set(job.get("required_skills", []))
        candidate_skills = set(snapshot["payload"].get("verified_skills", []))
        matched = required.intersection(candidate_skills)
        match_score = round((len(matched) / max(len(required), 1)) * 100.0, 1)

        now = datetime.now(timezone.utc).isoformat()
        app_id = f"app_job_{job_id}_{candidate_user_id}"
        application = {
            "application_id": app_id,
            "job_id": job_id,
            "candidate_user_id": candidate_user_id,
            "cv_snapshot_id": cv_snapshot_id,
            "cv_sha256_hash": snapshot["sha256_hash"],
            "ats_match_percentage": match_score,
            "expected_salary_bdt": expected_salary_bdt,
            "cover_note": cover_note,
            "current_stage": self.STAGE_APPLIED,
            "stage_history": [
                {
                    "stage": self.STAGE_APPLIED,
                    "timestamp": now,
                    "updated_by": candidate_user_id,
                    "notes": "Application submitted with cryptographically sealed CV."
                }
            ],
            "created_at": now
        }
        self._applications[app_key] = application
        self._applications[app_id] = application
        job["applicant_count"] = job.get("applicant_count", 0) + 1

        return {
            "success": True,
            "application": application,
            "message": f"Job application submitted successfully. ATS Skill Match: {match_score}%."
        }

    def advance_application_stage(
        self,
        application_id: str,
        employer_user_id: str,
        new_stage: str,
        feedback_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Advances the candidate through the 5-Stage hiring pipeline:
        Saved -> Applied -> Viewed -> Interview -> Offer / Rejected.
        Verifies employer authority.
        """
        app = self._applications.get(application_id)
        if not app:
            return {
                "success": False,
                "error_code": "APPLICATION_NOT_FOUND",
                "message": "Application could not be found."
            }

        job = self._jobs.get(app["job_id"])
        if not job or job["employer_user_id"] != employer_user_id:
            return {
                "success": False,
                "error_code": "FORBIDDEN_EMPLOYER_ACTION",
                "message": "Only the hiring employer can advance application stages."
            }

        if new_stage not in self.VALID_STAGES:
            return {
                "success": False,
                "error_code": "INVALID_PIPELINE_STAGE",
                "message": f"Stage '{new_stage}' is not a valid hiring pipeline stage."
            }

        now = datetime.now(timezone.utc).isoformat()
        app["current_stage"] = new_stage
        app["stage_history"].append({
            "stage": new_stage,
            "timestamp": now,
            "updated_by": employer_user_id,
            "notes": feedback_notes or f"Application moved to {new_stage} stage."
        })

        return {
            "success": True,
            "application_id": application_id,
            "new_stage": new_stage,
            "stage_history": app["stage_history"],
            "message": f"Application pipeline advanced to {new_stage} successfully."
        }

    def get_job_feed(
        self,
        domain: Optional[str] = None,
        work_mode: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieves active job listings with optional domain & work mode filters."""
        results = []
        for job in self._jobs.values():
            if job["status"] != "ACTIVE":
                continue
            if domain and job["domain"] != domain:
                continue
            if work_mode and job["work_mode"] != work_mode:
                continue
            if search_query:
                q = search_query.lower()
                matched = (
                    q in job["title"].lower()
                    or q in job["company_name"].lower()
                    or any(q in s.lower() for s in job["required_skills"])
                )
                if not matched:
                    continue
            results.append(job)

        return sorted(results, key=lambda x: x["created_at"], reverse=True)


# Singleton instance
job_placement_service = JobPlacementService()
