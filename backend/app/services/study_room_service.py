# ============================================================================
# MODULE: PEER STUDY CIRCLES & SYNCHRONOUS COLLABORATION SERVICE
# TOPIC: Real-time Study Rooms, WebRTC Signaling Tokens & Whiteboard Telemetry
# FILE: backend/app/services/study_room_service.py
# PURPOSE: Facilitate synchronous peer-to-peer audio/video study circles, synchronized
#          virtual whiteboards, and synchronized Pomodoro group sprints.
# STANDARDS: OWASP ASVS L2 Room Isolation, Cryptographic HMAC Session Tokens
# AUDIENCE: Students, Peer Scholars, Tutors & Educational Telemetry Systems
# ============================================================================

import hmac
import hashlib
import time
import uuid
from typing import Dict, List, Optional, Any


class StudyRoomCollaborationService:
    """
    Enterprise Peer Study Circle Engine.
    Powers synchronous study rooms with WebRTC signaling tokens, synchronized
    whiteboard scratchpads, live participant presence, and group sprint synchronization.
    """

    SECRET_SIGNING_KEY = b"agrojatra-study-room-entropy-salt-2026"

    def __init__(self):
        self._rooms: Dict[str, Dict[str, Any]] = {}
        self._init_seed_rooms()

    def _init_seed_rooms(self):
        """Pre-seeds live exemplary peer study circles across Bangladesh."""
        seed_rooms = [
            {
                "room_id": "room-buet-math-01",
                "title": "BUET Admission Math Sprint: Definite Integrals & Conics",
                "host_id": "student-tamim-buet",
                "host_name": "Tamim Iqbal",
                "topic": "Higher Mathematics",
                "target_grade": "Admission-BUET",
                "max_participants": 10,
                "is_private": False,
                "passcode": None,
                "created_at": "2026-10-14T10:00:00Z",
                "participants": [
                    {"user_id": "student-tamim-buet", "user_name": "Tamim Iqbal", "role": "HOST", "joined_at": "2026-10-14T10:00:00Z"},
                    {"user_id": "student-sadia-01", "user_name": "Sadia Afrin", "role": "PARTICIPANT", "joined_at": "2026-10-14T10:05:00Z"},
                    {"user_id": "student-fahim-02", "user_name": "Fahim Hasan", "role": "PARTICIPANT", "joined_at": "2026-10-14T10:12:00Z"},
                ],
                "pomodoro_state": {
                    "is_running": True,
                    "duration_minutes": 25,
                    "seconds_remaining": 1140,
                    "started_at": int(time.time()),
                    "action": "START"
                },
                "whiteboard_strokes": [
                    {
                        "stroke_id": "st-001",
                        "user_id": "student-tamim-buet",
                        "action": "FORMULA",
                        "formula_latex": r"\int_{0}^{\pi/2} \frac{\sin x}{\sin x + \cos x} dx = \frac{\pi}{4}",
                        "timestamp": "2026-10-14T10:15:00Z"
                    }
                ]
            },
            {
                "room_id": "room-med-bio-02",
                "title": "Medical Biology Rapid Revision: Human Physiology & Genetics",
                "host_id": "student-nusrat-med",
                "host_name": "Nusrat Jahan",
                "topic": "Biology Paper 2",
                "target_grade": "Admission-Medical",
                "max_participants": 8,
                "is_private": False,
                "passcode": None,
                "created_at": "2026-10-14T11:00:00Z",
                "participants": [
                    {"user_id": "student-nusrat-med", "user_name": "Nusrat Jahan", "role": "HOST", "joined_at": "2026-10-14T11:00:00Z"},
                    {"user_id": "student-rafiq-03", "user_name": "Rafiqul Islam", "role": "PARTICIPANT", "joined_at": "2026-10-14T11:04:00Z"}
                ],
                "pomodoro_state": {
                    "is_running": False,
                    "duration_minutes": 25,
                    "seconds_remaining": 1500,
                    "started_at": 0,
                    "action": "PAUSE"
                },
                "whiteboard_strokes": [
                    {
                        "stroke_id": "st-002",
                        "user_id": "student-nusrat-med",
                        "action": "STROKE",
                        "stroke_data": {"tool": "pen", "color": "#0284C7", "size": 3, "points": [{"x": 50, "y": 80}, {"x": 120, "y": 140}]},
                        "timestamp": "2026-10-14T11:10:00Z"
                    }
                ]
            }
        ]

        for r in seed_rooms:
            r["status"] = "ACTIVE"
            # Generate WebRTC room session token
            r["webrtc_session_token"] = self._generate_session_token(r["room_id"], r["host_id"])
            self._rooms[r["room_id"]] = r

    def _generate_session_token(self, room_id: str, user_id: str) -> str:
        """Generates a cryptographic HMAC-SHA256 session token for WebRTC signaling."""
        raw_payload = f"room:{room_id}|user:{user_id}|issued:{int(time.time())}".encode('utf-8')
        sig = hmac.new(self.SECRET_SIGNING_KEY, raw_payload, hashlib.sha256).hexdigest()[:24]
        return f"wrtc_sig_{sig}"

    def create_study_room(
        self,
        title: str,
        host_id: str,
        host_name: str,
        topic: str,
        target_grade: str,
        max_participants: int = 8,
        is_private: bool = False,
        passcode: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initializes a new real-time peer study room.
        Enforces constraints and assigns room session credentials.
        """
        if not title or not title.strip():
            raise ValueError("Room title cannot be empty.")
        if not host_id or not host_name:
            raise ValueError("Host credentials cannot be empty.")
        if is_private and (not passcode or len(passcode.strip()) < 4):
            raise ValueError("Private study rooms require a passcode of at least 4 characters.")

        room_id = f"room-{uuid.uuid4().hex[:10]}"
        session_token = self._generate_session_token(room_id, host_id)

        room_record = {
            "room_id": room_id,
            "title": title.strip(),
            "host_id": host_id,
            "host_name": host_name,
            "topic": topic.strip(),
            "target_grade": target_grade.strip(),
            "max_participants": max(2, min(50, max_participants)),
            "is_private": bool(is_private),
            "passcode": passcode.strip() if passcode else None,
            "webrtc_session_token": session_token,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "status": "ACTIVE",
            "participants": [
                {
                    "user_id": host_id,
                    "user_name": host_name,
                    "role": "HOST",
                    "joined_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                }
            ],
            "pomodoro_state": {
                "is_running": False,
                "duration_minutes": 25,
                "seconds_remaining": 1500,
                "started_at": 0,
                "action": "RESET"
            },
            "whiteboard_strokes": []
        }

        self._rooms[room_id] = room_record
        return room_record

    def list_active_study_rooms(
        self,
        topic: Optional[str] = None,
        grade: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Lists all active study rooms. If private, masks passcode and internal credentials.
        """
        results = []
        for r in self._rooms.values():
            if r.get("status") != "ACTIVE":
                continue
            if topic and topic.lower() not in r["topic"].lower():
                continue
            if grade and grade.lower() not in r["target_grade"].lower():
                continue

            public_view = {
                "room_id": r["room_id"],
                "title": r["title"],
                "host_name": r["host_name"],
                "topic": r["topic"],
                "target_grade": r["target_grade"],
                "is_private": r["is_private"],
                "current_participants": len(r["participants"]),
                "max_participants": r["max_participants"],
                "has_active_pomodoro": r["pomodoro_state"]["is_running"],
                "stroke_count": len(r["whiteboard_strokes"]),
                "created_at": r["created_at"]
            }
            results.append(public_view)
        return results

    def join_study_room(
        self,
        room_id: str,
        user_id: str,
        user_name: str,
        role: str = "PARTICIPANT",
        passcode: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Enrolls a student participant into an active room with access control checks.
        """
        if room_id not in self._rooms:
            raise KeyError(f"Study room {room_id} does not exist.")

        room = self._rooms[room_id]
        if room.get("status") != "ACTIVE":
            raise ValueError("This study room has concluded.")

        # Passcode check for private rooms
        if room["is_private"]:
            if not passcode or passcode.strip() != room["passcode"]:
                raise PermissionError("Incorrect passcode for private study room.")

        # Capacity check
        existing = [p for p in room["participants"] if p["user_id"] == user_id]
        if not existing and len(room["participants"]) >= room["max_participants"]:
            raise ValueError("Study room capacity reached. Cannot join.")

        if not existing:
            new_p = {
                "user_id": user_id,
                "user_name": user_name,
                "role": role if role in ["HOST", "CO_HOST", "PARTICIPANT", "OBSERVER"] else "PARTICIPANT",
                "joined_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            room["participants"].append(new_p)

        participant_token = self._generate_session_token(room_id, user_id)
        return {
            "room_id": room_id,
            "title": room["title"],
            "topic": room["topic"],
            "participant_token": participant_token,
            "role": role,
            "current_participants": len(room["participants"]),
            "webrtc_session_token": room["webrtc_session_token"]
        }

    def leave_study_room(self, room_id: str, user_id: str) -> Dict[str, Any]:
        """Removes a participant from a study room."""
        if room_id not in self._rooms:
            raise KeyError(f"Study room {room_id} does not exist.")
        room = self._rooms[room_id]
        room["participants"] = [p for p in room["participants"] if p["user_id"] != user_id]
        return {
            "room_id": room_id,
            "user_id": user_id,
            "remaining_participants": len(room["participants"]),
            "status": "LEFT"
        }

    def sync_whiteboard(
        self,
        room_id: str,
        user_id: str,
        action: str,
        stroke_data: Optional[Dict[str, Any]] = None,
        formula_latex: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synchronizes collaborative whiteboard strokes and LaTeX formula renders.
        """
        if room_id not in self._rooms:
            raise KeyError(f"Study room {room_id} does not exist.")
        room = self._rooms[room_id]

        # Ensure user is participant
        member_role = None
        for p in room["participants"]:
            if p["user_id"] == user_id:
                member_role = p.get("role", "PARTICIPANT")
                break

        if member_role is None and room["host_id"] != user_id:
            raise PermissionError("User is not an active participant in this study room.")

        if member_role == "OBSERVER":
            raise PermissionError("Observers have read-only access and cannot modify the whiteboard.")

        if formula_latex and len(formula_latex) > 2000:
            raise ValueError("Formula LaTeX exceeds maximum allowable size of 2000 characters.")

        action_upper = action.upper()
        if action_upper == "CLEAR":
            room["whiteboard_strokes"] = []
            return {
                "room_id": room_id,
                "action": "CLEAR",
                "total_strokes": 0,
                "cleared_by": user_id
            }

        stroke_entry = {
            "stroke_id": f"stk-{uuid.uuid4().hex[:8]}",
            "user_id": user_id,
            "action": action_upper,
            "stroke_data": stroke_data,
            "formula_latex": formula_latex,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        room["whiteboard_strokes"].append(stroke_entry)
        return {
            "room_id": room_id,
            "stroke_entry": stroke_entry,
            "total_strokes": len(room["whiteboard_strokes"])
        }

    def sync_pomodoro(
        self,
        room_id: str,
        host_id: str,
        duration_minutes: int = 25,
        action: str = "START"
    ) -> Dict[str, Any]:
        """
        Synchronizes room-wide Pomodoro sprint focus sessions.
        """
        if room_id not in self._rooms:
            raise KeyError(f"Study room {room_id} does not exist.")
        room = self._rooms[room_id]

        # Only host or co-host can control room timer
        host_match = room["host_id"] == host_id
        co_host_match = any(p["user_id"] == host_id and p.get("role") in ["HOST", "CO_HOST"] for p in room["participants"])
        if not host_match and not co_host_match:
            raise PermissionError("Only the room Host or Co-Host can control group Pomodoro sprints.")

        action_upper = action.upper()
        pomo = room["pomodoro_state"]
        if action_upper == "START":
            pomo["is_running"] = True
            pomo["duration_minutes"] = duration_minutes
            pomo["seconds_remaining"] = duration_minutes * 60
            pomo["started_at"] = int(time.time())
            pomo["action"] = "START"
        elif action_upper == "PAUSE":
            pomo["is_running"] = False
            pomo["action"] = "PAUSE"
        elif action_upper in ["RESET", "STOP"]:
            pomo["is_running"] = False
            pomo["seconds_remaining"] = duration_minutes * 60
            pomo["started_at"] = 0
            pomo["action"] = "RESET"
        else:
            raise ValueError(f"Unsupported pomodoro action: {action}")

        return {
            "room_id": room_id,
            "pomodoro_state": pomo
        }

    def get_room_state(self, room_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Retrieves complete live state of a room."""
        if room_id not in self._rooms:
            raise KeyError(f"Study room {room_id} does not exist.")
        room = self._rooms[room_id]
        return {
            "room_id": room["room_id"],
            "title": room["title"],
            "host_id": room["host_id"],
            "host_name": room["host_name"],
            "topic": room["topic"],
            "target_grade": room["target_grade"],
            "is_private": room["is_private"],
            "max_participants": room["max_participants"],
            "participants": room["participants"],
            "whiteboard_strokes": room["whiteboard_strokes"],
            "pomodoro_state": room["pomodoro_state"],
            "status": room.get("status", "ACTIVE"),
            "created_at": room["created_at"]
        }


# Global singleton instance
study_room_service = StudyRoomCollaborationService()
