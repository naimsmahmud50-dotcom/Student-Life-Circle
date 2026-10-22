"""
Student Innovation Launchpad & Micro-Grant Incubator Service for Agrojatra Platform.
Provides decentralized hackathon project pitching, SHA-256 intellectual property proofing,
anti-Sybil peer community voting tribunal, and milestone-governed grant escrow tranche releases.
"""

import uuid
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class InnovationLaunchpadService:
    def __init__(self):
        self._projects: Dict[str, Dict[str, Any]] = {}
        self._votes: Dict[str, Dict[str, Any]] = {}  # key: f"{project_id}:{voter_id}"
        self._grant_releases: Dict[str, List[Dict[str, Any]]] = {}
        self._seed_default_projects()

    def _seed_default_projects(self):
        """Seed initial real-world student innovation ventures across Bangladeshi campuses."""
        p1_id = "PRJ-AGRI-01"
        self._projects[p1_id] = {
            "project_id": p1_id,
            "title": "Solar-Powered IoT Soil Salinity & Nitrate Sensor for Coastal Barisal",
            "track": "AGRI_TECH",
            "leader_student_id": "std-buet-01",
            "leader_student_name": "Tariqul Islam (BUET EEE)",
            "team_members": ["Sadman Sakib", "Mehnaz Tabassum"],
            "summary": "Low-cost sub-$15 edge IoT telemetry device notifying smallholder coastal farmers of soil salinity surges via SMS.",
            "grant_requested_bdt": 30000.0,
            "escrow_balance_remaining_bdt": 30000.0,
            "demo_repo_url": "https://github.com/buet-agri/salinity-iot",
            "ip_proof_hash": "IP-SHA256-A8F291BD56C198E2",
            "status": "VOTING_ACTIVE",
            "votes_count": 42,
            "grant_status": "ESCROW_LOCKED",
            "created_at": "2026-10-05T08:00:00+00:00",
        }
        self._grant_releases[p1_id] = []

        p2_id = "PRJ-HEALTH-02"
        self._projects[p2_id] = {
            "project_id": p2_id,
            "title": "On-Device Offline Dengue NS1 Rapid Antigen Image Classifier",
            "track": "HEALTH_AI",
            "leader_student_id": "std-dmc-02",
            "leader_student_name": "Dr. Anika Haque (DMC) & Farhan (DU CS)",
            "team_members": ["Farhan Kabir", "Nuzhat Zahin"],
            "summary": "Lightweight MobileNetV3 smartphone app diagnosing borderline faint faint dengue strip test lines under low rural clinic lighting.",
            "grant_requested_bdt": 25000.0,
            "escrow_balance_remaining_bdt": 25000.0,
            "demo_repo_url": "https://github.com/health-ai-bd/dengue-lens",
            "ip_proof_hash": "IP-SHA256-7E3C409BF104D59A",
            "status": "VOTING_ACTIVE",
            "votes_count": 68,
            "grant_status": "ESCROW_LOCKED",
            "created_at": "2026-10-08T11:30:00+00:00",
        }
        self._grant_releases[p2_id] = []

    def pitch_project(
        self,
        title: str,
        track: str,
        leader_student_id: str,
        leader_student_name: str,
        team_members: Optional[List[str]] = None,
        summary: str = "",
        grant_requested_bdt: float = 25000.0,
        demo_repo_url: str = "",
    ) -> Dict[str, Any]:
        """
        Registers a new student innovation project with cryptographic IP proofing on the platform ledger.
        """
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("Project title cannot be empty.")

        clean_url = demo_repo_url.strip()
        if not (clean_url.startswith("https://") or clean_url.startswith("http://") or clean_url.startswith("git://")):
            raise ValueError("Invalid repository URL. Must start with https://, http://, or git://")

        project_id = f"PRJ-{uuid.uuid4().hex[:8].upper()}"
        now_iso = datetime.now(timezone.utc).isoformat()

        # Compute SHA-256 IP Proof Hash
        ip_payload = f"{project_id}:{clean_title}:{leader_student_id}:{now_iso}"
        ip_hash = f"IP-SHA256-{hashlib.sha256(ip_payload.encode()).hexdigest()[:16].upper()}"

        grant_amount = max(5000.0, min(float(grant_requested_bdt), 100000.0))

        record = {
            "project_id": project_id,
            "title": clean_title,
            "track": track.strip().upper(),
            "leader_student_id": leader_student_id,
            "leader_student_name": leader_student_name,
            "team_members": team_members or [],
            "summary": summary,
            "grant_requested_bdt": grant_amount,
            "escrow_balance_remaining_bdt": grant_amount,
            "demo_repo_url": clean_url,
            "ip_proof_hash": ip_hash,
            "status": "VOTING_ACTIVE",
            "votes_count": 0,
            "grant_status": "ESCROW_LOCKED",
            "created_at": now_iso,
        }

        self._projects[project_id] = record
        self._grant_releases[project_id] = []

        return record

    def cast_vote(
        self,
        project_id: str,
        voter_student_id: str,
        voter_reputation_score: float = 100.0,
    ) -> Dict[str, Any]:
        """
        Casts a community vote with anti-Sybil protection (1 vote per student per project)
        and reputation-weighted scoring.
        """
        if project_id not in self._projects:
            raise ValueError(f"Project with ID '{project_id}' not found.")

        vote_key = f"{project_id}:{voter_student_id}"
        if vote_key in self._votes:
            raise ValueError(f"Duplicate vote rejected: Student '{voter_student_id}' has already voted for project '{project_id}'.")

        # Reputation weight multiplier (between 0.5x and 3.0x)
        weight = min(max(float(voter_reputation_score) / 100.0, 0.5), 3.0)

        now_iso = datetime.now(timezone.utc).isoformat()
        vote_id = f"VOTE-{uuid.uuid4().hex[:6].upper()}"

        self._votes[vote_key] = {
            "vote_id": vote_id,
            "project_id": project_id,
            "voter_student_id": voter_student_id,
            "weight": round(weight, 2),
            "voted_at": now_iso,
        }

        project = self._projects[project_id]
        project["votes_count"] += 1

        return {
            "vote_id": vote_id,
            "project_id": project_id,
            "voter_student_id": voter_student_id,
            "weighted_vote_value": round(weight, 2),
            "new_total_votes": project["votes_count"],
            "voted_at": now_iso,
        }

    def release_grant_tranche(
        self,
        project_id: str,
        milestone_stage: str,
        mentor_reviewer_id: str,
        approval_notes: str = "",
    ) -> Dict[str, Any]:
        """
        Releases micro-grant escrow tranches upon mentor milestone verification.
        Guards against duplicate tranche releases and out-of-order progression.
        """
        if project_id not in self._projects:
            raise ValueError(f"Project with ID '{project_id}' not found.")

        project = self._projects[project_id]

        valid_stages = {
            "PROPOSAL_VALIDATION": 0.30,  # 30% release
            "PROTOTYPE_DEMO": 0.40,       # 40% release
            "PILOT_DEPLOYMENT": 0.30,     # 30% release
        }

        stage_upper = milestone_stage.strip().upper()
        if stage_upper not in valid_stages:
            raise ValueError(f"Invalid milestone stage '{milestone_stage}'. Must be one of {list(valid_stages.keys())}.")

        existing_stages = [r["milestone_stage"] for r in self._grant_releases.get(project_id, [])]
        if stage_upper in existing_stages:
            raise ValueError(f"Double-release prevented: Tranche for stage '{stage_upper}' has already been released.")

        # Order verification
        if stage_upper == "PROTOTYPE_DEMO" and "PROPOSAL_VALIDATION" not in existing_stages:
            raise ValueError("Progression error: PROPOSAL_VALIDATION must be completed before PROTOTYPE_DEMO.")
        if stage_upper == "PILOT_DEPLOYMENT" and "PROTOTYPE_DEMO" not in existing_stages:
            raise ValueError("Progression error: PROTOTYPE_DEMO must be completed before PILOT_DEPLOYMENT.")

        ratio = valid_stages[stage_upper]
        release_amount = round(project["grant_requested_bdt"] * ratio, 2)
        project["escrow_balance_remaining_bdt"] = round(project["escrow_balance_remaining_bdt"] - release_amount, 2)

        if project["escrow_balance_remaining_bdt"] <= 0:
            project["grant_status"] = "FULLY_DISBURSED"
            project["status"] = "COMPLETED"
        else:
            project["grant_status"] = "TRANCHE_RELEASED"
            project["status"] = "FUNDED_IN_PROGRESS"

        now_iso = datetime.now(timezone.utc).isoformat()
        release_id = f"TRN-{uuid.uuid4().hex[:6].upper()}"

        release_record = {
            "release_id": release_id,
            "project_id": project_id,
            "milestone_stage": stage_upper,
            "amount_released_bdt": release_amount,
            "escrow_balance_remaining_bdt": project["escrow_balance_remaining_bdt"],
            "mentor_reviewer_id": mentor_reviewer_id,
            "approval_notes": approval_notes,
            "status": "DISBURSED_TO_STUDENT_ESCROW",
            "released_at": now_iso,
        }

        self._grant_releases[project_id].append(release_record)

        return release_record

    def list_projects(self, track: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists active innovation projects, optionally filtered by domain track."""
        projects = list(self._projects.values())
        if track and track.upper() != "ALL":
            projects = [p for p in projects if p["track"] == track.upper()]
        return projects

    def get_project_by_id(self, project_id: str) -> Dict[str, Any]:
        """Retrieves details of a project pitch and its grant release history."""
        if project_id not in self._projects:
            raise ValueError(f"Project with ID '{project_id}' not found.")
        proj = dict(self._projects[project_id])
        proj["tranche_releases"] = self._grant_releases.get(project_id, [])
        return proj


innovation_launchpad_service = InnovationLaunchpadService()
