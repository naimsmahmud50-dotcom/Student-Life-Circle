"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Collaborative Question Bank Moderation & Peer-Review Service
TOPIC:     Phase 117 Collaborative Question Bank Moderation & Peer-Review
FILE:      backend/app/services/question_moderation_service.py
PHASE:     Phase 117 - Collaborative Question Bank Moderation & Peer-Review
PURPOSE:   Enforces multi-stage editorial state machine (Draft -> SME Review -> Board
           Moderated -> Approved -> Quarantined), dual-examiner blind review consensus,
           author self-review prevention, and emergency quarantine instant isolation.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Unreviewed-AI Policy, Strict Zero-Emoji
========================================================================================
"""

import time
import uuid
from typing import Any, Dict, List, Optional, Set
from backend.app.services.quiz_engine import quiz_engine


class ModerationException(Exception):
    """Base exception for question moderation errors."""
    pass


class QuestionNotFoundException(ModerationException):
    """Raised when a question ID does not exist in moderation registry."""
    pass


class InvalidStateTransitionException(ModerationException):
    """Raised when an illegal state machine transition is attempted."""
    pass


class SelfReviewException(ModerationException):
    """Raised when an author attempts to approve or review their own question."""
    pass


class DuplicateReviewException(ModerationException):
    """Raised when an examiner attempts to submit multiple reviews in the same stage."""
    pass


class QuarantinedQuestionException(ModerationException):
    """Raised when attempting actions on a quarantined question prior to remediation."""
    pass


class QuestionModerationService:
    """
    Manages the collaborative peer-review editorial pipeline for examination questions.
    """

    STATE_DRAFT = "DRAFT"
    STATE_SME_REVIEW = "SME_REVIEW"
    STATE_BOARD_MODERATED = "BOARD_MODERATED"
    STATE_APPROVED = "APPROVED"
    STATE_QUARANTINED = "QUARANTINED"

    DECISION_APPROVE = "APPROVE"
    DECISION_REVISE = "REVISE"
    DECISION_REJECT = "REJECT"

    # Permitted state progression rules
    VALID_TRANSITIONS = {
        STATE_DRAFT: {STATE_SME_REVIEW, STATE_QUARANTINED},
        STATE_SME_REVIEW: {STATE_BOARD_MODERATED, STATE_DRAFT, STATE_QUARANTINED},
        STATE_BOARD_MODERATED: {STATE_APPROVED, STATE_DRAFT, STATE_QUARANTINED},
        STATE_APPROVED: {STATE_QUARANTINED, STATE_DRAFT},
        STATE_QUARANTINED: {STATE_DRAFT},
    }

    def __init__(self):
        self._questions: Dict[str, Dict[str, Any]] = {}
        self._audit_log: List[Dict[str, Any]] = []
        self._init_seed_questions()

    def _init_seed_questions(self) -> None:
        """Seeds initial question records spanning all moderation stages."""
        now = int(time.time())
        seed_id_1 = "mod-q-phys-01"
        self._questions[seed_id_1] = {
            "question_id": seed_id_1,
            "author_id": "usr-author-01",
            "author_name": "ড. মোহাম্মদ রফিকুল ইসলাম",
            "subject": "পদার্থবিজ্ঞান ১ম পত্র",
            "topic": "নিউটনীয় বলবিদ্যা",
            "class_grade": 11,
            "stem": "একটি বস্তুর ওপর প্রযুক্ত বল $F = 6t^2 + 2t$ হলে, $t = 2\\text{ s}$ সময়ে বস্তুর ভরবেগের পরিবর্তন কত? (যেখানে $t = 0$ সময়ে ভরবেগ শূন্য)",
            "options": [
                {"key": "A", "text": "$20\\text{ kg}\\cdot\\text{m/s}$", "is_correct": True, "explanation": "$\\Delta p = \\int_0^2 (6t^2 + 2t) dt = [2t^3 + t^2]_0^2 = 16 + 4 = 20$"},
                {"key": "B", "text": "$16\\text{ kg}\\cdot\\text{m/s}$", "is_correct": False, "explanation": "ভুল সমাকলন"},
                {"key": "C", "text": "$24\\text{ kg}\\cdot\\text{m/s}$", "is_correct": False, "explanation": "ভুল মান"},
                {"key": "D", "text": "$12\\text{ kg}\\cdot\\text{m/s}$", "is_correct": False, "explanation": "তাত্ক্ষণিক বলের সাথে বিভ্রান্তি"},
            ],
            "status": self.STATE_SME_REVIEW,
            "version": 1,
            "original_draft": {
                "stem": "একটি বস্তুর ওপর প্রযুক্ত বল $F = 6t^2 + 2$ হলে ভরবেগ কত?",
                "options": [
                    {"key": "A", "text": "$20\\text{ kg}\\cdot\\text{m/s}$", "is_correct": True},
                    {"key": "B", "text": "$16\\text{ kg}\\cdot\\text{m/s}$", "is_correct": False},
                ],
            },
            "reviews": [],
            "created_at": now - 3600,
            "updated_at": now - 1800,
        }

        seed_id_2 = "mod-q-chem-02"
        self._questions[seed_id_2] = {
            "question_id": seed_id_2,
            "author_id": "usr-author-02",
            "author_name": "প্রফেসর আকলিমা বেগম",
            "subject": "রসায়ন ১ম পত্র",
            "topic": "গুণগত রসায়ন",
            "class_grade": 11,
            "stem": "হাইড্রোজেন পরমাণুর বামার সিরিজের জন্য সর্বনিম্ন তরঙ্গদৈর্ঘ্যের ফোটনের শক্তি কত?",
            "options": [
                {"key": "A", "text": "$3.4\\text{ eV}$", "is_correct": True, "explanation": "$E = 13.6 / 2^2 = 3.4\\text{ eV}$"},
                {"key": "B", "text": "$1.51\\text{ eV}$", "is_correct": False, "explanation": "প্যাশ্চেন সিরিজ"},
                {"key": "C", "text": "$13.6\\text{ eV}$", "is_correct": False, "explanation": "লাইম্যান সিরিজ"},
                {"key": "D", "text": "$0.85\\text{ eV}$", "is_correct": False, "explanation": "ব্র্যাকেট সিরিজ"},
            ],
            "status": self.STATE_BOARD_MODERATED,
            "version": 1,
            "original_draft": {
                "stem": "হাইড্রোজেনের বামার সিরিজের শক্তি কত?",
                "options": [],
            },
            "reviews": [
                {
                    "examiner_id": "usr-sme-01",
                    "examiner_name": "ড. ফারহানা হক",
                    "decision": self.DECISION_APPROVE,
                    "comments": "পাঠ্যসূচির সাথে সংগতিপূর্ণ এবং সমীকরণ নির্ভুল।",
                    "timestamp": now - 1200,
                }
            ],
            "created_at": now - 7200,
            "updated_at": now - 1200,
        }

    def create_draft_question(
        self,
        author_id: str,
        author_name: str,
        subject: str,
        topic: str,
        stem: str,
        options: List[Dict[str, Any]],
        class_grade: int = 11,
        question_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Creates a new question draft.
        Initial state is always DRAFT.
        """
        now = int(time.time())
        q_id = question_id or f"mod-q-{uuid.uuid4().hex[:8]}"

        record = {
            "question_id": q_id,
            "author_id": author_id,
            "author_name": author_name,
            "subject": subject,
            "topic": topic,
            "class_grade": class_grade,
            "stem": stem,
            "options": options,
            "status": self.STATE_DRAFT,
            "version": 1,
            "original_draft": {
                "stem": stem,
                "options": options,
            },
            "reviews": [],
            "created_at": now,
            "updated_at": now,
        }
        self._questions[q_id] = record
        self._log_audit(
            action="CREATE_DRAFT",
            question_id=q_id,
            actor_id=author_id,
            details={"subject": subject, "topic": topic},
        )
        return record

    def get_question(self, question_id: str) -> Dict[str, Any]:
        """Retrieves a question record by ID."""
        if question_id not in self._questions:
            raise QuestionNotFoundException(f"Question '{question_id}' not found.")
        return self._questions[question_id]

    def submit_for_review(self, question_id: str, actor_id: str) -> Dict[str, Any]:
        """
        Transitions question from DRAFT to SME_REVIEW.
        """
        question = self.get_question(question_id)
        if question["status"] != self.STATE_DRAFT:
            raise InvalidStateTransitionException(
                f"Cannot submit for review: Question '{question_id}' is in status '{question['status']}', expected '{self.STATE_DRAFT}'."
            )

        now = int(time.time())
        question["status"] = self.STATE_SME_REVIEW
        question["updated_at"] = now

        self._log_audit(
            action="SUBMIT_FOR_REVIEW",
            question_id=question_id,
            actor_id=actor_id,
            details={"previous_status": self.STATE_DRAFT, "new_status": self.STATE_SME_REVIEW},
        )
        return question

    def review_question(
        self,
        question_id: str,
        examiner_id: str,
        examiner_name: str,
        decision: str,
        comments: str,
    ) -> Dict[str, Any]:
        """
        Records an educator's peer review decision.
        Enforces:
        1. No self-review by author.
        2. No duplicate review by same examiner in current stage.
        3. Dual-examiner blind consensus logic:
           - In SME_REVIEW + APPROVE -> transitions to BOARD_MODERATED (1st endorsement).
           - In BOARD_MODERATED + APPROVE -> transitions to APPROVED (2nd distinct endorsement).
           - If REVISE or REJECT -> reverts question to DRAFT with feedback.
        """
        question = self.get_question(question_id)
        current_status = question["status"]

        if current_status == self.STATE_QUARANTINED:
            raise QuarantinedQuestionException(
                f"Question '{question_id}' is quarantined and cannot be reviewed."
            )

        if current_status not in {self.STATE_SME_REVIEW, self.STATE_BOARD_MODERATED}:
            raise InvalidStateTransitionException(
                f"Question '{question_id}' is in status '{current_status}', not open for review."
            )

        # 1. Author cannot review own question
        if question["author_id"] == examiner_id:
            raise SelfReviewException("Authors are strictly prohibited from reviewing their own questions.")

        # 2. Check for duplicate review by same examiner
        existing_examiners: Set[str] = {r["examiner_id"] for r in question["reviews"]}
        if examiner_id in existing_examiners:
            raise DuplicateReviewException(
                f"Examiner '{examiner_id}' has already submitted a review for question '{question_id}'."
            )

        now = int(time.time())
        review_entry = {
            "examiner_id": examiner_id,
            "examiner_name": examiner_name,
            "decision": decision,
            "comments": comments,
            "stage_at_review": current_status,
            "timestamp": now,
        }
        question["reviews"].append(review_entry)
        question["updated_at"] = now

        # 3. Consensus & State Transition Logic
        if decision == self.DECISION_APPROVE:
            if current_status == self.STATE_SME_REVIEW:
                question["status"] = self.STATE_BOARD_MODERATED
                transition_note = "1st endorsement recorded; moved to Board Moderation."
            elif current_status == self.STATE_BOARD_MODERATED:
                # 2nd approval achieved!
                question["status"] = self.STATE_APPROVED
                transition_note = "Dual consensus achieved (2/2); question Approved for live pool."
            else:
                transition_note = "Approval recorded."
        else:
            # Revision requested or rejected -> reverts back to DRAFT
            question["status"] = self.STATE_DRAFT
            transition_note = f"Revision requested by {examiner_name}; reverted to Draft."

        self._log_audit(
            action="REVIEW_SUBMITTED",
            question_id=question_id,
            actor_id=examiner_id,
            details={
                "decision": decision,
                "comments": comments,
                "previous_status": current_status,
                "new_status": question["status"],
                "note": transition_note,
            },
        )

        return {
            "question_id": question_id,
            "status": question["status"],
            "approvals_count": sum(1 for r in question["reviews"] if r["decision"] == self.DECISION_APPROVE),
            "total_reviews": len(question["reviews"]),
            "latest_review": review_entry,
        }

    def emergency_quarantine(
        self,
        question_id: str,
        actor_id: str,
        actor_name: str,
        reason: str,
    ) -> Dict[str, Any]:
        """
        Emergency switch: Instantly pulls any question from live exam pools and marks it QUARANTINED.
        Records an immutable audit trail entry and registers in quiz engine's quarantine set.
        """
        question = self.get_question(question_id)
        previous_status = question["status"]

        now = int(time.time())
        question["status"] = self.STATE_QUARANTINED
        question["updated_at"] = now
        question["quarantine_metadata"] = {
            "quarantined_by": actor_id,
            "actor_name": actor_name,
            "reason": reason,
            "quarantined_at": now,
            "previous_status": previous_status,
        }

        # Synchronize with live quiz engine to immediately isolate the item
        quiz_engine._quarantined_questions.add(question_id)

        self._log_audit(
            action="EMERGENCY_QUARANTINE",
            question_id=question_id,
            actor_id=actor_id,
            details={
                "previous_status": previous_status,
                "new_status": self.STATE_QUARANTINED,
                "reason": reason,
            },
        )

        return {
            "question_id": question_id,
            "status": self.STATE_QUARANTINED,
            "quarantined_at": now,
            "reason": reason,
            "actor_id": actor_id,
        }

    def remediate_quarantine(
        self,
        question_id: str,
        actor_id: str,
        remediation_notes: str,
        revised_stem: Optional[str] = None,
        revised_options: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Restores a quarantined question back to DRAFT status for editorial revisions.
        Removes the question from the quiz engine quarantine isolation set.
        """
        question = self.get_question(question_id)
        if question["status"] != self.STATE_QUARANTINED:
            raise InvalidStateTransitionException(
                f"Question '{question_id}' is not in QUARANTINED status (current: {question['status']})."
            )

        now = int(time.time())
        question["status"] = self.STATE_DRAFT
        question["version"] += 1
        question["updated_at"] = now

        if revised_stem is not None:
            question["stem"] = revised_stem
        if revised_options is not None:
            question["options"] = revised_options

        # Reset reviews for the new version cycle
        question["reviews"] = []

        # Remove from quiz engine quarantine
        if question_id in quiz_engine._quarantined_questions:
            quiz_engine._quarantined_questions.remove(question_id)

        self._log_audit(
            action="REMEDIATE_QUARANTINE",
            question_id=question_id,
            actor_id=actor_id,
            details={"remediation_notes": remediation_notes, "new_version": question["version"]},
        )

        return question

    def get_moderation_queue(
        self,
        filter_status: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Returns questions pending moderation with filtering capabilities.
        """
        results = []
        for q in self._questions.values():
            if filter_status and q["status"] != filter_status:
                continue
            if subject and q["subject"] != subject:
                continue

            approvals_count = sum(1 for r in q["reviews"] if r["decision"] == self.DECISION_APPROVE)
            results.append({
                "question_id": q["question_id"],
                "author_id": q["author_id"],
                "author_name": q["author_name"],
                "subject": q["subject"],
                "topic": q["topic"],
                "class_grade": q["class_grade"],
                "stem": q["stem"],
                "status": q["status"],
                "version": q["version"],
                "approvals_count": approvals_count,
                "total_reviews": len(q["reviews"]),
                "created_at": q["created_at"],
                "updated_at": q["updated_at"],
            })
        return results

    def get_audit_trail(self, question_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns the immutable moderation audit trail."""
        if question_id:
            return [entry for entry in self._audit_log if entry["question_id"] == question_id]
        return list(self._audit_log)

    def _log_audit(
        self,
        action: str,
        question_id: str,
        actor_id: str,
        details: Dict[str, Any],
    ) -> None:
        """Appends an event to the immutable audit trail."""
        self._audit_log.append({
            "audit_id": f"mod-aud-{len(self._audit_log) + 1}",
            "action": action,
            "question_id": question_id,
            "actor_id": actor_id,
            "timestamp": int(time.time()),
            "details": details,
        })


# Global singleton instance
question_moderation_service = QuestionModerationService()
