"""
AlumniMentorshipService:
Enterprise 1-on-1 Alumni Mentorship & Career Advisory Vault.
Connects students and university admission aspirants with verified top alumni
(BUET, DU, IBA, Medical, Tech Leads).
Features:
- Verified Alumni Directory with domain specialties & hourly fees
- Concurrency-safe slot reservation (prevents double booking)
- Dynamic WebRTC 1-on-1 signaling channel tokens
- Milestone Escrow fee holding and bKash transaction recording
- Bilateral rating and session closure
"""

import uuid
import hashlib
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class AlumniMentorshipService:
    def __init__(self):
        self._lock = threading.Lock()
        self._mentors: Dict[str, Dict[str, Any]] = {
            "mentor-buet-01": {
                "mentor_id": "mentor-buet-01",
                "name": "Nafis Imtiaz",
                "alma_mater": "BUET • CSE '22",
                "current_role": "Senior Software Engineer @ bKash",
                "specialties": ["BUET Admission Strategy", "System Design & Algorithms", "Tech Interview Prep"],
                "hourly_fee_bdt": 500.0,
                "available_slots": ["2026-10-18 19:00", "2026-10-18 21:00", "2026-10-19 20:00"],
                "rating": 4.98,
                "total_sessions": 64,
                "verified": True
            },
            "mentor-iba-02": {
                "mentor_id": "mentor-iba-02",
                "name": "Anika Tabassum",
                "alma_mater": "IBA, University of Dhaka • BBA '23",
                "current_role": "Management Trainee @ Unilever Bangladesh",
                "specialties": ["IBA Admission Math & English", "Analytical Reasoning", "Corporate CV & Case Prep"],
                "hourly_fee_bdt": 600.0,
                "available_slots": ["2026-10-18 18:00", "2026-10-20 19:30"],
                "rating": 4.94,
                "total_sessions": 48,
                "verified": True
            },
            "mentor-dmc-03": {
                "mentor_id": "mentor-dmc-03",
                "name": "Dr. Sazzad Hossain",
                "alma_mater": "Dhaka Medical College • MBBS '21",
                "current_role": "Resident Physician & Medical Admission Counselor",
                "specialties": ["Medical Admission Biology & Chemistry", "Exam Day Time Management", "Stress Shield"],
                "hourly_fee_bdt": 400.0,
                "available_slots": ["2026-10-19 17:00", "2026-10-21 21:00"],
                "rating": 4.96,
                "total_sessions": 52,
                "verified": True
            }
        }
        self._sessions: Dict[str, Dict[str, Any]] = {}

    def get_all_mentors(self, specialty_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock:
            mentors = list(self._mentors.values())
            if specialty_filter:
                q = specialty_filter.lower()
                mentors = [
                    m for m in mentors 
                    if any(q in s.lower() for s in m["specialties"]) or q in m["alma_mater"].lower()
                ]
            return mentors

    def get_mentor_by_id(self, mentor_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._mentors.get(mentor_id)

    def book_session(
        self,
        mentor_id: str,
        student_id: str,
        student_name: str,
        slot_time: str,
        topic_focus: str,
        target_ambition: str,
        fee_bdt: float = 500.0,
        payment_method: str = "bKash"
    ) -> Dict[str, Any]:
        with self._lock:
            if mentor_id not in self._mentors:
                raise ValueError(f"Mentor '{mentor_id}' does not exist.")
            
            mentor = self._mentors[mentor_id]
            if slot_time not in mentor["available_slots"]:
                raise ValueError(f"Slot '{slot_time}' is either unavailable or has already been booked.")

            # Atomically remove slot to prevent double-booking
            mentor["available_slots"].remove(slot_time)

            session_id = f"sess-{uuid.uuid4().hex[:10]}"
            # Generate WebRTC channel token
            channel_seed = f"{session_id}:{mentor_id}:{student_id}:{slot_time}"
            webrtc_token = "wrtc_" + hashlib.sha256(channel_seed.encode("utf-8")).hexdigest()[:24]
            escrow_tx_id = f"ESC-{payment_method[:2].upper()}-{uuid.uuid4().hex[:8].upper()}"

            session = {
                "session_id": session_id,
                "mentor_id": mentor_id,
                "mentor_name": mentor["name"],
                "student_id": student_id,
                "student_name": student_name,
                "slot_time": slot_time,
                "topic_focus": topic_focus,
                "target_ambition": target_ambition,
                "fee_bdt": fee_bdt,
                "status": "CONFIRMED",
                "webrtc_channel_token": webrtc_token,
                "escrow_tx_id": escrow_tx_id,
                "payment_method": payment_method,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            self._sessions[session_id] = session
            return session

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._sessions.get(session_id)

    def complete_session_and_release_escrow(self, session_id: str, student_rating: float) -> Dict[str, Any]:
        with self._lock:
            if session_id not in self._sessions:
                raise ValueError(f"Session '{session_id}' not found.")
            session = self._sessions[session_id]
            if session["status"] == "COMPLETED":
                raise ValueError("Session has already been marked completed.")
            
            session["status"] = "COMPLETED"
            session["student_rating"] = student_rating
            session["escrow_status"] = "FUNDS_RELEASED_TO_MENTOR"

            # Update mentor metrics
            mentor = self._mentors.get(session["mentor_id"])
            if mentor:
                total = mentor["total_sessions"]
                curr_rating = mentor["rating"]
                mentor["rating"] = round(((curr_rating * total) + student_rating) / (total + 1), 2)
                mentor["total_sessions"] += 1

            return session

alumni_mentorship_service = AlumniMentorshipService()
