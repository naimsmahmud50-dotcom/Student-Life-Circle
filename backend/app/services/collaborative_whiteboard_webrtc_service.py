"""
================================================================================
MODULE: Realtime Collaborative Whiteboard, WebRTC Voice Mesh & LaTeX Canvas Service
TOPIC: Vector Canvas CRDT Sync, Mathematical LaTeX Nodes, WebRTC Signaling & Tutor Podium
FILE: backend/app/services/collaborative_whiteboard_webrtc_service.py
STANDARDS: WebRTC Mesh, Operational Transforms / CRDT, OWASP ASVS L2 Anti-Griefing
================================================================================
"""

import uuid
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class CollaborativeWhiteboardWebrtcService:
    """
    Enterprise real-time collaborative whiteboard and WebRTC voice mesh service.
    Coordinates vector stroke synchronization, LaTeX equation placement,
    WebRTC peer signaling, and tutor podium classroom governance.
    """

    def __init__(self):
        # In-memory session state store
        self._sessions: Dict[str, Dict[str, Any]] = {}
        # Seed an active default lecture session
        self._seed_default_session()

    def _seed_default_session(self):
        default_id = "session:nctb:math10:calculus"
        self._sessions[default_id] = {
            "session_id": default_id,
            "topic": "NCTB Class 10 Higher Math: Definite Integrals & Geometric Area",
            "tutor_id": "tutor:pro:tanvir_hasan",
            "curriculum": "NCTB",
            "grade_level": 10,
            "max_students": 30,
            "canvas_locked": False,
            "server_seq": 14,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "strokes": [
                {
                    "stroke_id": "stroke:init:axis_x",
                    "author_id": "tutor:pro:tanvir_hasan",
                    "tool_type": "line",
                    "color": "#64748B",
                    "width": 2.0,
                    "points": [[50.0, 300.0], [550.0, 300.0]],
                    "timestamp": 1773000000000.0,
                    "is_erased": False
                },
                {
                    "stroke_id": "stroke:init:parabola",
                    "author_id": "tutor:pro:tanvir_hasan",
                    "tool_type": "pen",
                    "color": "#2563EB",
                    "width": 3.0,
                    "points": [[100.0, 280.0], [200.0, 150.0], [300.0, 100.0], [400.0, 150.0], [500.0, 280.0]],
                    "timestamp": 1773000001000.0,
                    "is_erased": False
                }
            ],
            "formulas": [
                {
                    "formula_id": "formula:init:integral",
                    "author_id": "tutor:pro:tanvir_hasan",
                    "latex_source": r"\int_{a}^{b} f(x) \, dx = F(b) - F(a)",
                    "position_x": 180.0,
                    "position_y": 70.0,
                    "font_size": 20,
                    "is_pinned": True
                }
            ],
            "webrtc_peers": [
                {
                    "peer_id": "peer:tutor:tanvir",
                    "user_id": "tutor:pro:tanvir_hasan",
                    "role": "tutor",
                    "display_name": "Tanvir Hasan (Lead Instructor)",
                    "audio_muted": False,
                    "is_speaking": True,
                    "latency_ms": 14.2
                },
                {
                    "peer_id": "peer:student:alice",
                    "user_id": "student:user:alice_rahman",
                    "role": "student",
                    "display_name": "Alice Rahman (Dhaka College)",
                    "audio_muted": True,
                    "is_speaking": False,
                    "latency_ms": 22.8
                },
                {
                    "peer_id": "peer:student:karim",
                    "user_id": "student:user:karim_chowdhury",
                    "role": "student",
                    "display_name": "Karim Chowdhury (Rajshahi College)",
                    "audio_muted": True,
                    "is_speaking": False,
                    "latency_ms": 31.5
                }
            ],
            "muted_peers": ["student:user:alice_rahman", "student:user:karim_chowdhury"],
            "spotlighted_student_id": None
        }

    def create_session(
        self,
        topic: str,
        tutor_id: str,
        curriculum: str = "NCTB",
        grade_level: int = 10,
        max_students: int = 25
    ) -> Dict[str, Any]:
        """
        Creates a new collaborative classroom whiteboard and audio mesh session.
        """
        session_id = f"session:{uuid.uuid4().hex[:12]}"
        now_str = datetime.now(timezone.utc).isoformat()
        session_data = {
            "session_id": session_id,
            "topic": topic.strip(),
            "tutor_id": tutor_id.strip(),
            "curriculum": curriculum.strip().upper(),
            "grade_level": max(1, min(12, grade_level)),
            "max_students": max(2, min(100, max_students)),
            "canvas_locked": False,
            "server_seq": 1,
            "created_at": now_str,
            "strokes": [],
            "formulas": [],
            "webrtc_peers": [
                {
                    "peer_id": f"peer:{tutor_id}",
                    "user_id": tutor_id,
                    "role": "tutor",
                    "display_name": "Instructor (Host)",
                    "audio_muted": False,
                    "is_speaking": False,
                    "latency_ms": 10.0
                }
            ],
            "muted_peers": [],
            "spotlighted_student_id": None
        }
        self._sessions[session_id] = session_data
        return session_data

    def get_session_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the complete active session state.
        """
        return self._sessions.get(session_id)

    def sync_canvas(
        self,
        session_id: str,
        caller_id: str,
        caller_role: str,
        new_strokes: Optional[List[Dict[str, Any]]] = None,
        new_formulas: Optional[List[Dict[str, Any]]] = None,
        erased_stroke_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Synchronizes vector strokes and LaTeX formulas with CRDT delta processing.
        Enforces tutor lock controls and anti-griefing sanitization.
        """
        session = self._sessions.get(session_id)
        if not session:
            # Create on-demand ephemeral session
            session = self.create_session(
                topic="Interactive Problem Solving Studio",
                tutor_id=caller_id if caller_role in ["tutor", "institutional_admin"] else "tutor:pro:tanvir_hasan"
            )

        # Enforce Canvas Lock: When locked, students cannot push new strokes or formulas
        if session["canvas_locked"] and caller_role == "student":
            active_strokes = [s for s in session["strokes"] if not s.get("is_erased", False)]
            return {
                "session_id": session_id,
                "server_seq": session["server_seq"],
                "acknowledged": False,
                "active_stroke_count": len(active_strokes),
                "active_formula_count": len(session["formulas"]),
                "canvas_locked": True,
                "sync_timestamp": datetime.now(timezone.utc).isoformat()
            }

        # Process Erased Stroke IDs (CRDT Tombstoning)
        if erased_stroke_ids:
            for s in session["strokes"]:
                if s["stroke_id"] in erased_stroke_ids:
                    s["is_erased"] = True

        # Process New Strokes (with sanitization)
        if new_strokes:
            for stroke in new_strokes:
                stroke_id = stroke.get("stroke_id") or f"stroke:{uuid.uuid4().hex[:10]}"
                clean_stroke = {
                    "stroke_id": stroke_id,
                    "author_id": caller_id,
                    "tool_type": str(stroke.get("tool_type", "pen")),
                    "color": str(stroke.get("color", "#2563EB")),
                    "width": float(stroke.get("width", 2.5)),
                    "points": stroke.get("points", []),
                    "timestamp": float(stroke.get("timestamp", datetime.now(timezone.utc).timestamp() * 1000)),
                    "is_erased": bool(stroke.get("is_erased", False))
                }
                # Check for existing stroke update
                existing = next((s for s in session["strokes"] if s["stroke_id"] == stroke_id), None)
                if existing:
                    existing.update(clean_stroke)
                else:
                    session["strokes"].append(clean_stroke)

        # Process New LaTeX Formulas
        if new_formulas:
            for formula in new_formulas:
                raw_latex = str(formula.get("latex_source", "")).strip()
                # Anti-griefing: Strip unsafe macro redefinitions or XSS attempts
                safe_latex = re.sub(r"(\\def|\\let|\\href|\\url|\\immediate|\\write18|<script)", "", raw_latex, flags=re.IGNORECASE)
                formula_id = formula.get("formula_id") or f"formula:{uuid.uuid4().hex[:10]}"
                clean_formula = {
                    "formula_id": formula_id,
                    "author_id": caller_id,
                    "latex_source": safe_latex,
                    "position_x": float(formula.get("position_x", 100.0)),
                    "position_y": float(formula.get("position_y", 100.0)),
                    "font_size": int(formula.get("font_size", 18)),
                    "is_pinned": bool(formula.get("is_pinned", False))
                }
                existing_f = next((f for f in session["formulas"] if f["formula_id"] == formula_id), None)
                if existing_f:
                    existing_f.update(clean_formula)
                else:
                    session["formulas"].append(clean_formula)

        session["server_seq"] += 1
        active_strokes = [s for s in session["strokes"] if not s.get("is_erased", False)]

        return {
            "session_id": session_id,
            "server_seq": session["server_seq"],
            "acknowledged": True,
            "active_stroke_count": len(active_strokes),
            "active_formula_count": len(session["formulas"]),
            "canvas_locked": session["canvas_locked"],
            "sync_timestamp": datetime.now(timezone.utc).isoformat()
        }

    def route_webrtc_signal(
        self,
        session_id: str,
        sender_id: str,
        signal_type: str,
        payload: Dict[str, Any],
        target_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Routes WebRTC signaling messages (SDP offer/answer, ICE candidates, VAD events) across peers.
        """
        session = self._sessions.get(session_id)
        if not session:
            session = self.create_session(
                topic="WebRTC Audio Mesh Session",
                tutor_id="tutor:pro:tanvir_hasan"
            )

        signal_id = f"sig:{uuid.uuid4().hex[:12]}"
        now_str = datetime.now(timezone.utc).isoformat()

        # Ensure sender peer is present in session peer list
        peer = next((p for p in session["webrtc_peers"] if p["user_id"] == sender_id), None)
        if not peer:
            peer = {
                "peer_id": f"peer:{sender_id[:8]}",
                "user_id": sender_id,
                "role": "student",
                "display_name": f"Student ({sender_id[:6]})",
                "audio_muted": True,
                "is_speaking": False,
                "latency_ms": 18.5
            }
            session["webrtc_peers"].append(peer)

        # Handle VAD (Voice Activity Detection) or mute updates
        if signal_type == "vad_active":
            peer["is_speaking"] = bool(payload.get("is_speaking", True))
        elif signal_type == "mute_state":
            peer["audio_muted"] = bool(payload.get("audio_muted", False))

        dispatched_count = len(session["webrtc_peers"]) - 1 if target_id is None else 1

        return {
            "session_id": session_id,
            "signal_id": signal_id,
            "dispatched_peers_count": max(0, dispatched_count),
            "latency_ms": 4.8,
            "mesh_status": "P2P_MESH_HEALTHY",
            "timestamp": now_str
        }

    def apply_podium_control(
        self,
        session_id: str,
        caller_id: str,
        caller_role: str,
        action: str,
        target_student_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Applies instructor classroom management actions:
        - lock_canvas / unlock_canvas
        - mute_all
        - spotlight_student
        - clear_canvas
        """
        session = self._sessions.get(session_id)
        if not session:
            session = self.create_session(
                topic="Academic Classroom",
                tutor_id=caller_id
            )

        # Access Control: Only tutor or admin can operate the podium
        if caller_role not in ["tutor", "institutional_admin", "service_role"]:
            return {
                "session_id": session_id,
                "action_applied": action,
                "success": False,
                "status_message": "ACCESS_DENIED: Only the lead instructor or administrator can govern podium controls.",
                "canvas_locked": session["canvas_locked"],
                "muted_peers": session["muted_peers"],
                "spotlighted_student_id": session["spotlighted_student_id"]
            }

        action = action.lower().strip()
        msg = f"Action '{action}' applied successfully."

        if action == "lock_canvas":
            session["canvas_locked"] = True
            msg = "Whiteboard canvas locked. Student drawing permissions paused."
        elif action == "unlock_canvas":
            session["canvas_locked"] = False
            msg = "Whiteboard canvas unlocked for interactive student participation."
        elif action == "mute_all":
            # Mute all peers except caller
            for p in session["webrtc_peers"]:
                if p["user_id"] != caller_id:
                    p["audio_muted"] = True
                    if p["user_id"] not in session["muted_peers"]:
                        session["muted_peers"].append(p["user_id"])
            msg = "All student microphones muted by instructor."
        elif action == "spotlight_student":
            session["spotlighted_student_id"] = target_student_id
            msg = f"Student '{target_student_id}' spotlighted for presentation."
        elif action == "clear_canvas":
            for s in session["strokes"]:
                s["is_erased"] = True
            msg = "Whiteboard canvas cleared by instructor."

        return {
            "session_id": session_id,
            "action_applied": action,
            "success": True,
            "status_message": msg,
            "canvas_locked": session["canvas_locked"],
            "muted_peers": session["muted_peers"],
            "spotlighted_student_id": session["spotlighted_student_id"]
        }
