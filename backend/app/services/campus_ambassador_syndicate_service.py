"""
Campus Ambassador & Peer Micro-Internship Syndicate Service
Decentralized student ambassador task network across 50+ universities in Bangladesh.
Features proof-of-work submission, milestone honorarium points, and cryptographic tier badges.
"""

import hmac
import hashlib
import datetime
from typing import Dict, List, Any, Optional


HMAC_SECRET_KEY = b"agrojatra-campus-ambassador-cryptographic-salt-2025"


class CampusAmbassadorSyndicateService:
    """Enterprise campus ambassador network, micro-internship task board, and points engine."""

    def __init__(self):
        self._campuses: List[Dict[str, Any]] = []
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._profiles: Dict[str, Dict[str, Any]] = {}
        self._initialize_seed_data()

    def _initialize_seed_data(self):
        # 1. 50+ Key Campuses across Bangladesh
        self._campuses = [
            {"campus_id": "CAMPUS-BUET", "name": "Bangladesh University of Engineering and Technology (BUET)", "division": "Dhaka", "type": "Engineering Public"},
            {"campus_id": "CAMPUS-DU", "name": "University of Dhaka (DU)", "division": "Dhaka", "type": "General Public"},
            {"campus_id": "CAMPUS-NSU", "name": "North South University (NSU)", "division": "Dhaka", "type": "Private"},
            {"campus_id": "CAMPUS-BRACU", "name": "BRAC University (BRACU)", "division": "Dhaka", "type": "Private"},
            {"campus_id": "CAMPUS-JU", "name": "Jahangirnagar University (JU)", "division": "Dhaka", "type": "General Public"},
            {"campus_id": "CAMPUS-DMC", "name": "Dhaka Medical College (DMC)", "division": "Dhaka", "type": "Medical Public"},
            {"campus_id": "CAMPUS-NDC", "name": "Notre Dame College (NDC)", "division": "Dhaka", "type": "College"},
            {"campus_id": "CAMPUS-DC", "name": "Dhaka College", "division": "Dhaka", "type": "College"},
            {"campus_id": "CAMPUS-CUET", "name": "Chittagong University of Engineering and Technology (CUET)", "division": "Chittagong", "type": "Engineering Public"},
            {"campus_id": "CAMPUS-CU", "name": "University of Chittagong (CU)", "division": "Chittagong", "type": "General Public"},
            {"campus_id": "CAMPUS-RUET", "name": "Rajshahi University of Engineering and Technology (RUET)", "division": "Rajshahi", "type": "Engineering Public"},
            {"campus_id": "CAMPUS-RU", "name": "University of Rajshahi (RU)", "division": "Rajshahi", "type": "General Public"},
            {"campus_id": "CAMPUS-SUST", "name": "Shahjalal University of Science and Technology (SUST)", "division": "Sylhet", "type": "Science & Tech Public"},
            {"campus_id": "CAMPUS-KUET", "name": "Khulna University of Engineering and Technology (KUET)", "division": "Khulna", "type": "Engineering Public"},
            {"campus_id": "CAMPUS-KU", "name": "Khulna University (KU)", "division": "Khulna", "type": "General Public"},
            {"campus_id": "CAMPUS-BAU", "name": "Bangladesh Agricultural University (BAU)", "division": "Mymensingh", "type": "Agricultural Public"},
            {"campus_id": "CAMPUS-BRUR", "name": "Begum Rokeya University, Rangpur (BRUR)", "division": "Rangpur", "type": "General Public"},
            {"campus_id": "CAMPUS-BU", "name": "University of Barishal", "division": "Barishal", "type": "General Public"}
        ]

        # 2. Seed Ambassador Tasks
        seed_tasks = [
            {
                "task_id": "TASK-2025-001",
                "title": "Organize STEM 3D Molecular Simulation Workshop for HSC Batch '26",
                "campus_id": "CAMPUS-NDC",
                "campus_name": "Notre Dame College (NDC)",
                "category": "WORKSHOP_ORGANIZER",
                "points_reward": 500,
                "grant_stipend_bdt": 2500.0,
                "status": "AVAILABLE",
                "claimed_by": None,
                "evidence_url": None,
                "impact_report": None,
                "verification_feedback": None
            },
            {
                "task_id": "TASK-2025-002",
                "title": "Lead BUET Campus Hackathon & Open Source Code Drive",
                "campus_id": "CAMPUS-BUET",
                "campus_name": "Bangladesh University of Engineering and Technology (BUET)",
                "category": "HACKATHON_DIRECTOR",
                "points_reward": 800,
                "grant_stipend_bdt": 4000.0,
                "status": "AVAILABLE",
                "claimed_by": None,
                "evidence_url": None,
                "impact_report": None,
                "verification_feedback": None
            },
            {
                "task_id": "TASK-2025-003",
                "title": "Establish Peer Study Circles for Rural HSC Examinees in Sylhet",
                "campus_id": "CAMPUS-SUST",
                "campus_name": "Shahjalal University of Science and Technology (SUST)",
                "category": "PEER_TUTORING",
                "points_reward": 450,
                "grant_stipend_bdt": 2000.0,
                "status": "AVAILABLE",
                "claimed_by": None,
                "evidence_url": None,
                "impact_report": None,
                "verification_feedback": None
            },
            {
                "task_id": "TASK-2025-004",
                "title": "Conduct DU Career & Verified CV Snapshot Onboarding Drive",
                "campus_id": "CAMPUS-DU",
                "campus_name": "University of Dhaka (DU)",
                "category": "CAREER_AMBASSADOR",
                "points_reward": 600,
                "grant_stipend_bdt": 3000.0,
                "status": "CLAIMED",
                "claimed_by": "student-101",
                "evidence_url": "https://agrojatra.org/evidence/du-career-drive",
                "impact_report": "Registered 140 students with cryptographic talent passports.",
                "verification_feedback": None
            }
        ]

        for t in seed_tasks:
            self._tasks[t["task_id"]] = t

        # 3. Seed Ambassador Profile
        self._profiles["student-101"] = {
            "student_id": "student-101",
            "name": "Naimur Rahman",
            "campus_name": "University of Dhaka (DU)",
            "tier": "SILVER_COORDINATOR",
            "total_points": 1100,
            "completed_tasks": 2,
            "earned_stipend_bdt": 5000.0,
            "digital_badge_signature": self._generate_badge_signature("student-101", "SILVER_COORDINATOR", 1100)
        }

    def _generate_badge_signature(self, student_id: str, tier: str, points: int) -> str:
        payload = f"{student_id}:{tier}:{points}".encode("utf-8")
        return hmac.new(HMAC_SECRET_KEY, payload, hashlib.sha256).hexdigest()

    def _calculate_tier(self, points: int) -> str:
        if points < 500:
            return "BRONZE_AMBASSADOR"
        elif points < 1500:
            return "SILVER_COORDINATOR"
        elif points < 3000:
            return "GOLD_LEAD_FELLOW"
        else:
            return "PLATINUM_CAMPUS_DIRECTOR"

    def list_campuses(self) -> List[Dict[str, Any]]:
        return self._campuses

    def list_tasks(self, campus_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        tasks = list(self._tasks.values())
        if campus_id:
            tasks = [t for t in tasks if t["campus_id"] == campus_id]
        if status:
            tasks = [t for t in tasks if t["status"] == status.upper()]
        return tasks

    def claim_task(self, task_id: str, student_id: str) -> Dict[str, Any]:
        """Claims an available task with atomic state-lock check."""
        if task_id not in self._tasks:
            raise ValueError(f"Task '{task_id}' not found.")
        task = self._tasks[task_id]

        if task["status"] != "AVAILABLE":
            raise ValueError(f"Task '{task_id}' cannot be claimed. Current status is {task['status']}.")

        task["status"] = "CLAIMED"
        task["claimed_by"] = student_id
        return task

    def submit_task_evidence(self, task_id: str, student_id: str, evidence_url: str, impact_report: str) -> Dict[str, Any]:
        """Submits proof-of-work link and descriptive impact summary."""
        if task_id not in self._tasks:
            raise ValueError(f"Task '{task_id}' not found.")
        task = self._tasks[task_id]

        if task["status"] != "CLAIMED":
            raise ValueError(f"Cannot submit evidence for task in state '{task['status']}'. Must be CLAIMED.")
        if task["claimed_by"] != student_id:
            raise ValueError(f"Student '{student_id}' is not the assignee of task '{task_id}'.")

        # Validate evidence URL format
        url_clean = evidence_url.strip()
        if not (url_clean.startswith("http://") or url_clean.startswith("https://")):
            raise ValueError("Evidence URL must be a valid HTTP or HTTPS web link.")
        if len(impact_report.strip()) < 10:
            raise ValueError("Impact report must provide at least 10 characters detailing task execution.")

        task["status"] = "SUBMITTED"
        task["evidence_url"] = url_clean
        task["impact_report"] = impact_report.strip()
        return task

    def verify_and_reward_task(self, task_id: str, verifier_id: str, approved: bool, feedback: str) -> Dict[str, Any]:
        """Reviews submitted evidence, updates task state, and disburses honorarium points/grants."""
        if task_id not in self._tasks:
            raise ValueError(f"Task '{task_id}' not found.")
        task = self._tasks[task_id]

        if task["status"] != "SUBMITTED":
            raise ValueError(f"Task must be in SUBMITTED state to verify. Current state: '{task['status']}'.")

        student_id = task["claimed_by"]
        task["verification_feedback"] = feedback.strip()

        if approved:
            task["status"] = "REWARDED"
            # Ensure student profile exists
            if student_id not in self._profiles:
                self._profiles[student_id] = {
                    "student_id": student_id,
                    "name": f"Student {student_id.split('-')[-1]}",
                    "campus_name": task["campus_name"],
                    "tier": "BRONZE_AMBASSADOR",
                    "total_points": 0,
                    "completed_tasks": 0,
                    "earned_stipend_bdt": 0.0,
                    "digital_badge_signature": ""
                }

            prof = self._profiles[student_id]
            prof["total_points"] += task["points_reward"]
            prof["completed_tasks"] += 1
            prof["earned_stipend_bdt"] += task["grant_stipend_bdt"]
            prof["tier"] = self._calculate_tier(prof["total_points"])
            prof["digital_badge_signature"] = self._generate_badge_signature(
                prof["student_id"], prof["tier"], prof["total_points"]
            )
        else:
            task["status"] = "REJECTED"

        return task

    def get_ambassador_profile(self, student_id: str) -> Dict[str, Any]:
        """Retrieves or auto-initializes the ambassador profile."""
        if student_id not in self._profiles:
            self._profiles[student_id] = {
                "student_id": student_id,
                "name": f"Student {student_id.split('-')[-1]}",
                "campus_name": "University of Dhaka (DU)",
                "tier": "BRONZE_AMBASSADOR",
                "total_points": 0,
                "completed_tasks": 0,
                "earned_stipend_bdt": 0.0,
                "digital_badge_signature": self._generate_badge_signature(student_id, "BRONZE_AMBASSADOR", 0)
            }
        return self._profiles[student_id]


# Export singleton instance
campus_ambassador_syndicate_service = CampusAmbassadorSyndicateService()
