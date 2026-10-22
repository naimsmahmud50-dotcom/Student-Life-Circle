"""
================================================================================
TEST SUITE: Phase 62 Collaborative Whiteboard, WebRTC Low-Latency Voice Mesh & LaTeX Canvas
STANDARDS: WebRTC Mesh, CRDT Vector Sync, MathJax/KaTeX LaTeX Formulas, ASVS 4.0 L2
PURPOSE: Comprehensive unit test coverage for collaborative whiteboard sessions,
         vector stroke sync, LaTeX sanitization, WebRTC signaling, and tutor podium.
================================================================================
"""

import unittest
from backend.app.services.collaborative_whiteboard_webrtc_service import CollaborativeWhiteboardWebrtcService


class TestCollaborativeWhiteboardWebrtc(unittest.TestCase):

    def setUp(self):
        self.service = CollaborativeWhiteboardWebrtcService()
        self.default_session_id = "session:nctb:math10:calculus"
        self.tutor_id = "tutor:pro:tanvir_hasan"
        self.student_id = "student:user:alice_rahman"

    # --------------------------------------------------------------------------
    # 1. Session Lifecycle Tests
    # --------------------------------------------------------------------------
    def test_default_session_seeded(self):
        state = self.service.get_session_state(self.default_session_id)
        self.assertIsNotNone(state)
        self.assertEqual(state["topic"], "NCTB Class 10 Higher Math: Definite Integrals & Geometric Area")
        self.assertGreater(len(state["strokes"]), 0)
        self.assertGreater(len(state["formulas"]), 0)
        self.assertGreater(len(state["webrtc_peers"]), 0)

    def test_create_custom_session(self):
        new_session = self.service.create_session(
            topic="Physics Class 12: Electromagnetic Waves",
            tutor_id="tutor:pro:shams",
            curriculum="NCTB",
            grade_level=12,
            max_students=40
        )
        self.assertIn("session:", new_session["session_id"])
        self.assertEqual(new_session["grade_level"], 12)
        self.assertEqual(new_session["max_students"], 40)
        self.assertFalse(new_session["canvas_locked"])

    def test_get_session_state_retrieval(self):
        state = self.service.get_session_state(self.default_session_id)
        self.assertEqual(state["curriculum"], "NCTB")
        self.assertFalse(state["canvas_locked"])
        self.assertEqual(state["tutor_id"], self.tutor_id)

    # --------------------------------------------------------------------------
    # 2. Vector Canvas Delta & CRDT Sync Tests
    # --------------------------------------------------------------------------
    def test_tutor_stroke_sync(self):
        stroke = {
            "stroke_id": "stroke:test:001",
            "author_id": self.tutor_id,
            "tool_type": "pen",
            "color": "#10B981",
            "width": 3.0,
            "points": [[10.0, 10.0], [20.0, 25.0], [30.0, 40.0]],
            "timestamp": 1773000005000.0,
            "is_erased": False
        }
        res = self.service.sync_canvas(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            new_strokes=[stroke]
        )
        self.assertTrue(res["acknowledged"])
        self.assertGreaterEqual(res["active_stroke_count"], 3)

    def test_student_stroke_sync_when_unlocked(self):
        stroke = {
            "stroke_id": "stroke:test:student_001",
            "author_id": self.student_id,
            "tool_type": "highlighter",
            "color": "#F59E0B",
            "width": 10.0,
            "points": [[100.0, 100.0], [150.0, 100.0]],
            "timestamp": 1773000006000.0,
            "is_erased": False
        }
        res = self.service.sync_canvas(
            session_id=self.default_session_id,
            caller_id=self.student_id,
            caller_role="student",
            new_strokes=[stroke]
        )
        self.assertTrue(res["acknowledged"])

    def test_canvas_lock_enforcement_student_denied(self):
        # Tutor locks canvas
        self.service.apply_podium_control(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            action="lock_canvas"
        )
        # Student attempts to draw
        stroke = {
            "stroke_id": "stroke:test:blocked",
            "author_id": self.student_id,
            "tool_type": "pen",
            "points": [[5.0, 5.0]],
            "timestamp": 1773000007000.0
        }
        res = self.service.sync_canvas(
            session_id=self.default_session_id,
            caller_id=self.student_id,
            caller_role="student",
            new_strokes=[stroke]
        )
        self.assertFalse(res["acknowledged"])
        self.assertTrue(res["canvas_locked"])

    def test_canvas_lock_enforcement_tutor_allowed(self):
        # Tutor locks canvas
        self.service.apply_podium_control(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            action="lock_canvas"
        )
        # Tutor draws
        stroke = {
            "stroke_id": "stroke:tutor:permitted",
            "author_id": self.tutor_id,
            "tool_type": "pen",
            "points": [[50.0, 50.0]],
            "timestamp": 1773000008000.0
        }
        res = self.service.sync_canvas(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            new_strokes=[stroke]
        )
        self.assertTrue(res["acknowledged"])

    def test_stroke_erasure_tombstoning(self):
        res = self.service.sync_canvas(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            erased_stroke_ids=["stroke:init:axis_x"]
        )
        self.assertTrue(res["acknowledged"])
        state = self.service.get_session_state(self.default_session_id)
        axis_stroke = next(s for s in state["strokes"] if s["stroke_id"] == "stroke:init:axis_x")
        self.assertTrue(axis_stroke["is_erased"])

    # --------------------------------------------------------------------------
    # 3. LaTeX Equation Studio Tests
    # --------------------------------------------------------------------------
    def test_latex_formula_addition(self):
        formula = {
            "formula_id": "formula:test:pythagoras",
            "author_id": self.tutor_id,
            "latex_source": r"a^2 + b^2 = c^2",
            "position_x": 120.0,
            "position_y": 200.0,
            "font_size": 22,
            "is_pinned": True
        }
        res = self.service.sync_canvas(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            new_formulas=[formula]
        )
        self.assertTrue(res["acknowledged"])
        self.assertGreaterEqual(res["active_formula_count"], 2)

    def test_latex_formula_sanitization_anti_griefing(self):
        malicious_formula = {
            "formula_id": "formula:test:exploit",
            "author_id": self.student_id,
            "latex_source": r"\def\evil{XSS}<script>alert(1)</script> x + y = z",
            "position_x": 50.0,
            "position_y": 50.0
        }
        res = self.service.sync_canvas(
            session_id=self.default_session_id,
            caller_id=self.student_id,
            caller_role="student",
            new_formulas=[malicious_formula]
        )
        self.assertTrue(res["acknowledged"])
        state = self.service.get_session_state(self.default_session_id)
        f_entry = next(f for f in state["formulas"] if f["formula_id"] == "formula:test:exploit")
        self.assertNotIn(r"\def", f_entry["latex_source"])
        self.assertNotIn("<script", f_entry["latex_source"])
        self.assertIn("x + y = z", f_entry["latex_source"])

    # --------------------------------------------------------------------------
    # 4. WebRTC Audio Mesh Signaling Tests
    # --------------------------------------------------------------------------
    def test_webrtc_signal_broadcast(self):
        res = self.service.route_webrtc_signal(
            session_id=self.default_session_id,
            sender_id=self.tutor_id,
            signal_type="offer",
            payload={"type": "offer", "sdp": "v=0\r\no=alice..."}
        )
        self.assertEqual(res["mesh_status"], "P2P_MESH_HEALTHY")
        self.assertGreaterEqual(res["dispatched_peers_count"], 1)

    def test_webrtc_signal_vad_active(self):
        res = self.service.route_webrtc_signal(
            session_id=self.default_session_id,
            sender_id=self.student_id,
            signal_type="vad_active",
            payload={"is_speaking": True, "audio_db": -18.2}
        )
        self.assertEqual(res["mesh_status"], "P2P_MESH_HEALTHY")
        state = self.service.get_session_state(self.default_session_id)
        peer = next(p for p in state["webrtc_peers"] if p["user_id"] == self.student_id)
        self.assertTrue(peer["is_speaking"])

    def test_webrtc_signal_mute_state(self):
        res = self.service.route_webrtc_signal(
            session_id=self.default_session_id,
            sender_id=self.tutor_id,
            signal_type="mute_state",
            payload={"audio_muted": True}
        )
        self.assertEqual(res["mesh_status"], "P2P_MESH_HEALTHY")
        state = self.service.get_session_state(self.default_session_id)
        peer = next(p for p in state["webrtc_peers"] if p["user_id"] == self.tutor_id)
        self.assertTrue(peer["audio_muted"])

    # --------------------------------------------------------------------------
    # 5. Tutor Podium Controls & Classroom Governance Tests
    # --------------------------------------------------------------------------
    def test_podium_lock_canvas_success(self):
        res = self.service.apply_podium_control(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            action="lock_canvas"
        )
        self.assertTrue(res["success"])
        self.assertTrue(res["canvas_locked"])

    def test_podium_unlock_canvas_success(self):
        res = self.service.apply_podium_control(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            action="unlock_canvas"
        )
        self.assertTrue(res["success"])
        self.assertFalse(res["canvas_locked"])

    def test_podium_mute_all(self):
        res = self.service.apply_podium_control(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            action="mute_all"
        )
        self.assertTrue(res["success"])
        self.assertIn("student:user:alice_rahman", res["muted_peers"])

    def test_podium_spotlight_student(self):
        res = self.service.apply_podium_control(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            action="spotlight_student",
            target_student_id="student:user:alice_rahman"
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["spotlighted_student_id"], "student:user:alice_rahman")

    def test_podium_clear_canvas(self):
        res = self.service.apply_podium_control(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            action="clear_canvas"
        )
        self.assertTrue(res["success"])
        state = self.service.get_session_state(self.default_session_id)
        for s in state["strokes"]:
            self.assertTrue(s["is_erased"])

    def test_podium_unauthorized_student_access_denied(self):
        res = self.service.apply_podium_control(
            session_id=self.default_session_id,
            caller_id=self.student_id,
            caller_role="student",
            action="lock_canvas"
        )
        self.assertFalse(res["success"])
        self.assertIn("ACCESS_DENIED", res["status_message"])

    def test_server_seq_monotonic_increment(self):
        state_pre = self.service.get_session_state(self.default_session_id)
        seq_pre = state_pre["server_seq"]
        res = self.service.sync_canvas(
            session_id=self.default_session_id,
            caller_id=self.tutor_id,
            caller_role="tutor",
            new_strokes=[]
        )
        self.assertGreater(res["server_seq"], seq_pre)


if __name__ == "__main__":
    unittest.main()
