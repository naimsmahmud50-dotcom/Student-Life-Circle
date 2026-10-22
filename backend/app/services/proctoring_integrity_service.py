"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Proctoring Integrity Tower & Exam Hall Telemetry Service
TOPIC:     Phase 116 Digital Examination Hall & Proctoring Integrity Tower
FILE:      backend/app/services/proctoring_integrity_service.py
PHASE:     Phase 116 - Digital Examination Hall & Proctoring Integrity Tower
PURPOSE:   Provides privacy-preserving client heuristic telemetry logging (tab switch,
           window blur, ambient audio threshold), dynamic integrity score evaluation,
           and tamper-evident SHA-256 cryptographic exam submission receipt sealing.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Privacy-First Architecture, Strict Zero-Emoji
========================================================================================
"""

import hashlib
import time
from typing import Any, Dict, List, Optional


class ProctoringException(Exception):
    """Base exception for proctoring integrity and exam hall errors."""
    pass


class SessionNotFoundException(ProctoringException):
    """Raised when an examination hall session cannot be found."""
    pass


class ExamFinalizedException(ProctoringException):
    """Raised when attempting to modify a finalized exam submission."""
    pass


class ProctoringIntegrityService:
    """
    Core service managing digital examination hall sessions, non-intrusive heuristic
    telemetry, student integrity scoring, and cryptographic receipt issuance.
    """

    EVENT_TAB_SWITCH = "TAB_SWITCH"
    EVENT_WINDOW_BLUR = "WINDOW_BLUR"
    EVENT_AUDIO_SURGE = "AUDIO_THRESHOLD_EXCEEDED"

    STATUS_ACTIVE = "ACTIVE"
    STATUS_FINALIZED = "FINALIZED"

    BAND_EXEMPLARY = "EXEMPLARY"          # Score >= 90
    BAND_MONITORED = "MONITORED"          # Score 70 - 89
    BAND_UNDER_REVIEW = "UNDER_REVIEW"    # Score < 70

    SALT = "OGROJATRA_ACADEMIC_PROCTOR_SALT_2026"

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._init_seed_session()

    def _init_seed_session(self) -> None:
        """Seeds an active exam session for initial teacher monitor verification."""
        seed_id = "exam_sess_ndc_phys_101"
        now = int(time.time())
        self._sessions[seed_id] = {
            "session_id": seed_id,
            "student_id": "stu_ndc_101",
            "student_name": "Tanvir Ahmed",
            "exam_id": "exam-ndc-phys-midterm-01",
            "institution_id": "inst-ndc-dhaka",
            "status": self.STATUS_ACTIVE,
            "started_at": now - 1200,
            "finalized_at": None,
            "telemetry_events": [
                {
                    "event_type": self.EVENT_TAB_SWITCH,
                    "value": 1.0,
                    "timestamp": now - 900,
                    "metadata": {"source": "visibilitychange"},
                }
            ],
            "answers": {
                "q_1": {"option_id": "opt_1b", "saved_at": now - 1100},
                "q_2": {"option_id": "opt_2a", "saved_at": now - 950},
            },
            "flagged_questions": ["q_2"],
            "integrity_score": 100.0,
            "receipt_hash": None,
        }

    def start_exam_session(
        self,
        session_id: str,
        student_id: str,
        student_name: str,
        exam_id: str,
        institution_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Initializes an examination desk session.
        Enforces a fresh starting integrity score of 100.0.
        """
        now = int(time.time())
        session = {
            "session_id": session_id,
            "student_id": student_id,
            "student_name": student_name,
            "exam_id": exam_id,
            "institution_id": institution_id or "inst-general",
            "status": self.STATUS_ACTIVE,
            "started_at": now,
            "finalized_at": None,
            "telemetry_events": [],
            "answers": {},
            "flagged_questions": [],
            "integrity_score": 100.0,
            "receipt_hash": None,
        }
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Fetches the session record by session_id."""
        if session_id not in self._sessions:
            raise SessionNotFoundException(f"Exam session '{session_id}' not found.")
        return self._sessions[session_id]

    def record_telemetry_event(
        self,
        session_id: str,
        event_type: str,
        value: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Records a client-side heuristic event (tab switch, window blur duration, audio surge).
        Immediately recalculates dynamic integrity score.
        """
        session = self.get_session(session_id)
        if session["status"] == self.STATUS_FINALIZED:
            raise ExamFinalizedException("Cannot log telemetry on a finalized exam session.")

        now = int(time.time())
        event = {
            "event_type": event_type,
            "value": float(value),
            "timestamp": now,
            "metadata": metadata or {},
        }
        session["telemetry_events"].append(event)
        session["integrity_score"] = self._compute_score(session["telemetry_events"])
        return {
            "session_id": session_id,
            "event_recorded": event,
            "current_integrity_score": session["integrity_score"],
            "integrity_band": self.get_integrity_band(session["integrity_score"]),
        }

    def _compute_score(self, events: List[Dict[str, Any]]) -> float:
        """
        Calculates student integrity score based on heuristic deductions:
        - Baseline: 100.0 points
        - Tab switch: 2 free switches; 4.0 points deduction per additional switch
        - Window blur duration: 5 seconds cumulative grace; 0.5 points deduction per additional second
        - Audio threshold surge: 3 free surges; 3.0 points deduction per additional surge
        Clamped to [0.0, 100.0] and rounded to 1 decimal place.
        """
        tab_switches = sum(1 for e in events if e["event_type"] == self.EVENT_TAB_SWITCH)
        blur_seconds = sum(e["value"] for e in events if e["event_type"] == self.EVENT_WINDOW_BLUR)
        audio_surges = sum(1 for e in events if e["event_type"] == self.EVENT_AUDIO_SURGE)

        deductions = 0.0

        if tab_switches > 2:
            deductions += (tab_switches - 2) * 4.0

        if blur_seconds > 5.0:
            deductions += (blur_seconds - 5.0) * 0.5

        if audio_surges > 3:
            deductions += (audio_surges - 3) * 3.0

        final_score = max(0.0, min(100.0, 100.0 - deductions))
        return round(final_score, 1)

    def get_integrity_band(self, score: float) -> str:
        """Categorizes integrity score into dignified non-punitive academic bands."""
        if score >= 90.0:
            return self.BAND_EXEMPLARY
        elif score >= 70.0:
            return self.BAND_MONITORED
        else:
            return self.BAND_UNDER_REVIEW

    def save_draft_answers(
        self,
        session_id: str,
        answers: Dict[str, Any],
        flagged_questions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Saves student answer selections and flagged items as auto-save draft."""
        session = self.get_session(session_id)
        if session["status"] == self.STATUS_FINALIZED:
            raise ExamFinalizedException("Cannot modify answers for a finalized exam session.")

        now = int(time.time())
        for q_id, opt in answers.items():
            session["answers"][q_id] = {
                "option_id": opt,
                "saved_at": now,
            }

        if flagged_questions is not None:
            session["flagged_questions"] = list(set(flagged_questions))

        return {
            "session_id": session_id,
            "saved_count": len(session["answers"]),
            "flagged_count": len(session["flagged_questions"]),
            "timestamp": now,
        }

    def finalize_exam_submission(
        self,
        session_id: str,
        final_answers: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Finalizes and locks the exam submission.
        Generates a tamper-evident SHA-256 cryptographic receipt seal.
        """
        session = self.get_session(session_id)
        if session["status"] == self.STATUS_FINALIZED:
            raise ExamFinalizedException(f"Exam session '{session_id}' has already been finalized.")

        now = int(time.time())
        if final_answers:
            self.save_draft_answers(session_id, final_answers)

        final_score = self._compute_score(session["telemetry_events"])
        session["integrity_score"] = final_score
        session["status"] = self.STATUS_FINALIZED
        session["finalized_at"] = now

        # Mint cryptographic SHA-256 seal
        hash_payload = (
            f"{session_id}:{session['student_id']}:{session['exam_id']}:"
            f"{final_score}:{now}:{self.SALT}"
        )
        receipt_hash = hashlib.sha256(hash_payload.encode("utf-8")).hexdigest()
        session["receipt_hash"] = receipt_hash

        return {
            "session_id": session_id,
            "student_id": session["student_id"],
            "exam_id": session["exam_id"],
            "status": self.STATUS_FINALIZED,
            "finalized_at": now,
            "total_answers_submitted": len(session["answers"]),
            "integrity_score": final_score,
            "integrity_band": self.get_integrity_band(final_score),
            "receipt_hash": receipt_hash,
            "verification_status": "CRYPTOGRAPHICALLY_SEALED",
        }

    def get_proctor_roster(self, exam_id: str) -> List[Dict[str, Any]]:
        """
        Returns live teacher monitor roster for all students in the exam hall.
        Presents calm, non-shaming academic status indicators.
        """
        roster = []
        for sess in self._sessions.values():
            if sess["exam_id"] == exam_id:
                score = sess["integrity_score"]
                roster.append({
                    "session_id": sess["session_id"],
                    "student_id": sess["student_id"],
                    "student_name": sess["student_name"],
                    "status": sess["status"],
                    "questions_answered": len(sess["answers"]),
                    "questions_flagged": len(sess["flagged_questions"]),
                    "telemetry_events_count": len(sess["telemetry_events"]),
                    "integrity_score": score,
                    "integrity_band": self.get_integrity_band(score),
                    "started_at": sess["started_at"],
                    "finalized_at": sess["finalized_at"],
                    "has_sealed_receipt": sess["receipt_hash"] is not None,
                })
        return roster


# Global singleton instance
proctoring_integrity_service = ProctoringIntegrityService()
