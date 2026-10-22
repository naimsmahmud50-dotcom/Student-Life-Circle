"""
========================================================================================
MODULE:    In-App Dispute & Learner Question Error Reporting Service
TOPIC:     Question Defect Reporting, Academic Integrity Bounties & Moderator Resolution
FILE:      backend/app/services/dispute_service.py
PURPOSE:   Empowers learners to report defective questions (WRONG_KEY, TYPO, AMBIGUOUS,
           OUT_OF_SYLLABUS) directly in-flow during quizzes or review. Provides subject
           matter moderators with an action queue to verify, correct answer keys, trigger
           quarantine, and reward vigilant students with Integrity Bounty points.
AUDIENCE:  Academic Integrity Officers, Content Moderation Team & AI Agents
STANDARDS: Crowd-Sourced QA with Moderator Gate, Quality Assurance, Audit Logging
========================================================================================
"""

import uuid
from typing import Dict, List, Optional, Tuple, Any
from backend.app.core.timekeeper import ServerTimekeeper
from backend.app.services.quarantine_service import QuarantineService


class DisputeService:
    """
    Manages crowdsourced question error reports and administrative resolution workflows.
    """

    ALLOWED_REASONS = {
        "WRONG_KEY",
        "TYPO",
        "AMBIGUOUS",
        "OUT_OF_SYLLABUS",
        "IMAGE_ISSUE",
        "OTHER"
    }

    RESOLUTION_ACTIONS = {
        "ACCEPT_KEY_CORRECTION",
        "ACCEPT_CONTENT_EDIT",
        "ACCEPT_AND_QUARANTINE",
        "REJECT_INVALID",
        "REJECT_DUPLICATE"
    }

    def __init__(self, quarantine_service: Optional[QuarantineService] = None):
        self._disputes: Dict[str, Dict[str, Any]] = {}
        self._student_bounties: Dict[str, int] = {}  # student_id -> total bounty points
        self._quarantine_service = quarantine_service or QuarantineService()

    def file_dispute(
        self,
        student_id: str,
        question_id: str,
        reason: str,
        explanation: str,
        quiz_attempt_id: Optional[str] = None,
        suggested_correct_option: Optional[str] = None
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Submits a learner error report for a question.
        Prevents spam duplicate submissions from the same student on the same pending question.
        """
        clean_reason = reason.strip().upper()
        if clean_reason not in self.ALLOWED_REASONS:
            return False, f"INVALID_REASON. Allowed: {list(self.ALLOWED_REASONS)}", None

        if not explanation or len(explanation.strip()) < 5:
            return False, "EXPLANATION_TOO_SHORT. Provide at least 5 characters.", None

        # Check for existing pending dispute by this student on this question
        for disp in self._disputes.values():
            if (disp["student_id"] == student_id and 
                disp["question_id"] == question_id and 
                disp["status"] == "PENDING"):
                return False, "A pending dispute for this question already exists from this student.", None

        dispute_id = f"disp_{uuid.uuid4().hex[:8]}"
        record = {
            "dispute_id": dispute_id,
            "student_id": student_id,
            "question_id": question_id,
            "quiz_attempt_id": quiz_attempt_id,
            "reason": clean_reason,
            "explanation": explanation.strip(),
            "suggested_correct_option": suggested_correct_option,
            "status": "PENDING",
            "created_at": ServerTimekeeper.get_server_iso_now(),
            "resolved_at": None,
            "resolved_by": None,
            "resolution_action": None,
            "resolution_notes": None,
            "bounty_awarded": 0,
            "quarantined": False
        }

        self._disputes[dispute_id] = record
        return True, "DISPUTE_FILED_SUCCESSFULLY", record

    def get_dispute(self, dispute_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single dispute record."""
        return self._disputes.get(dispute_id)

    def list_disputes(
        self,
        status: Optional[str] = None,
        question_id: Optional[str] = None,
        student_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Queries disputes with optional filters."""
        results = list(self._disputes.values())
        if status:
            results = [d for d in results if d["status"] == status.upper()]
        if question_id:
            results = [d for d in results if d["question_id"] == question_id]
        if student_id:
            results = [d for d in results if d["student_id"] == student_id]
        return results

    def resolve_dispute(
        self,
        dispute_id: str,
        moderator_id: str,
        action: str,
        resolution_notes: str,
        trigger_quarantine: bool = False,
        bounty_points: int = 15
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Subject matter moderator resolves a student dispute.
        Awards integrity bounty points to vigilant students upon accepted findings.
        Optionally triggers immediate quarantine isolation.
        """
        record = self._disputes.get(dispute_id)
        if not record:
            return False, "DISPUTE_NOT_FOUND", None

        if record["status"] in ("RESOLVED", "REJECTED"):
            return False, f"DISPUTE_ALREADY_CLOSED with status {record['status']}", None

        action_clean = action.strip().upper()
        if action_clean not in self.RESOLUTION_ACTIONS:
            return False, f"INVALID_ACTION. Allowed: {list(self.RESOLUTION_ACTIONS)}", None

        is_accepted = action_clean.startswith("ACCEPT")
        quarantine_triggered = False

        if is_accepted:
            record["status"] = "RESOLVED"
            record["bounty_awarded"] = bounty_points
            student_id = record["student_id"]
            self._student_bounties[student_id] = self._student_bounties.get(student_id, 0) + bounty_points

            if trigger_quarantine or action_clean == "ACCEPT_AND_QUARANTINE":
                self._quarantine_service.quarantine_question(
                    question_id=record["question_id"],
                    actor_id=moderator_id,
                    actor_role="MODERATOR",
                    reason=f"Dispute {dispute_id} accepted ({record['reason']}): {resolution_notes}"
                )
                quarantine_triggered = True
                record["quarantined"] = True
        else:
            record["status"] = "REJECTED"
            record["bounty_awarded"] = 0

        record["resolved_at"] = ServerTimekeeper.get_server_iso_now()
        record["resolved_by"] = moderator_id
        record["resolution_action"] = action_clean
        record["resolution_notes"] = resolution_notes.strip()

        return True, "DISPUTE_RESOLVED_SUCCESSFULLY", record

    def get_student_integrity_profile(self, student_id: str) -> Dict[str, Any]:
        """
        Returns student's crowdsourced quality contribution profile,
        including earned bounties and integrity badges.
        """
        student_disputes = [d for d in self._disputes.values() if d["student_id"] == student_id]
        total_filed = len(student_disputes)
        accepted_count = sum(1 for d in student_disputes if d["status"] == "RESOLVED")
        rejected_count = sum(1 for d in student_disputes if d["status"] == "REJECTED")
        total_bounty = self._student_bounties.get(student_id, 0)

        # Compute badges based on accepted disputes
        badges = []
        if accepted_count >= 1:
            badges.append({
                "badge_id": "VIGILANT_EYE",
                "title": "Vigilant Eye",
                "description": "Submitted 1+ confirmed academic correction."
            })
        if accepted_count >= 5:
            badges.append({
                "badge_id": "FACT_CHECKER",
                "title": "Fact Checker",
                "description": "Submitted 5+ verified question defect reports."
            })
        if any(d.get("quarantined") for d in student_disputes):
            badges.append({
                "badge_id": "SENTINEL_OF_TRUTH",
                "title": "Sentinel of Truth",
                "description": "Discovered a critical question flaw that led to platform-wide quarantine."
            })

        return {
            "student_id": student_id,
            "total_filed": total_filed,
            "accepted_count": accepted_count,
            "rejected_count": rejected_count,
            "pending_count": total_filed - (accepted_count + rejected_count),
            "total_bounty_points": total_bounty,
            "integrity_badges": badges
        }


# Singleton export for global access
dispute_service = DisputeService()
