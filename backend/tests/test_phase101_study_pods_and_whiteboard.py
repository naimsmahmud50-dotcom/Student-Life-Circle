"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite
TOPIC:     Phase 101 Collaborative Study Pods & Real-Time Whiteboard Tests
FILE:      backend/tests/test_phase101_study_pods_and_whiteboard.py
PHASE:     Phase 101 - Real-Time Study Pods & Collaborative Whiteboard
PURPOSE:   Asserts strict room capacity limits (max 8 peers), vector stroke and
           LaTeX formula delta history, WebRTC VAD telemetry, zero-emoji compliance,
           and Developer Architecture Note headers.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
"""

import os
import unittest
from backend.app.api.v1.endpoints.study_pods import StudyPodRegistry, MAX_POD_CAPACITY, router as study_pods_router


class TestPhase101StudyPodsAndWhiteboard(unittest.TestCase):
    """
    Automated verification suite for Phase 101 Real-Time Study Pods and Whiteboard.
    """

    def setUp(self):
        self.registry = StudyPodRegistry()

    def test_01_study_pod_creation_and_capacity_capping(self):
        """Verify pod creation properly caps max capacity at 8 peers."""
        pod = self.registry.create_pod(
            title="BUET Admission Higher Math Pod",
            subject="Higher Mathematics",
            creator_id="usr-buet-01",
            creator_name="Naim Hasan",
            max_capacity=10  # Attempting to exceed 8
        )
        self.assertEqual(pod["max_capacity"], MAX_POD_CAPACITY)
        self.assertEqual(len(pod["participants"]), 1)
        self.assertEqual(pod["participants"][0]["user_id"], "usr-buet-01")
        self.assertEqual(pod["title"], "BUET Admission Higher Math Pod")
        self.assertEqual(pod["status"], "active")

    def test_02_room_capacity_gating_blocks_ninth_peer(self):
        """Verify that joining stops and raises ValueError when pod reaches 8 peers."""
        pod = self.registry.create_pod(
            title="Physics Mechanics Cohort",
            subject="Physics",
            creator_id="peer-1",
            creator_name="Peer 1",
            max_capacity=8
        )
        pod_id = pod["pod_id"]

        # Add 7 more peers (total 8 peers)
        for i in range(2, 9):
            self.registry.join_pod(
                pod_id=pod_id,
                user_id=f"peer-{i}",
                user_name=f"Peer {i}",
                role="student"
            )

        updated_pod = self.registry.get_pod(pod_id)
        self.assertEqual(len(updated_pod["participants"]), 8)

        # 9th peer attempts to join -> MUST raise ValueError
        with self.assertRaises(ValueError) as ctx:
            self.registry.join_pod(
                pod_id=pod_id,
                user_id="peer-9",
                user_name="Peer 9",
                role="student"
            )
        self.assertIn("maximum capacity of 8 peers", str(ctx.exception))

    def test_03_idempotent_rejoin(self):
        """Verify that a peer rejoining the same pod does not consume extra slots."""
        pod = self.registry.create_pod(
            title="Chemistry Organic Synthesis",
            subject="Chemistry",
            creator_id="creator-01",
            creator_name="Creator"
        )
        pod_id = pod["pod_id"]

        self.registry.join_pod(pod_id, "student-01", "Student One")
        self.assertEqual(len(self.registry.get_pod(pod_id)["participants"]), 2)

        # Same user rejoins
        self.registry.join_pod(pod_id, "student-01", "Student One")
        self.assertEqual(len(self.registry.get_pod(pod_id)["participants"]), 2)

    def test_04_leave_study_pod(self):
        """Verify member departure reduces count and cleans telemetry."""
        pod = self.registry.create_pod(
            title="Biology Genetics",
            subject="Biology",
            creator_id="creator-bio",
            creator_name="Bio Lead"
        )
        pod_id = pod["pod_id"]

        self.registry.join_pod(pod_id, "student-bio-01", "Sadia")
        self.assertEqual(len(self.registry.get_pod(pod_id)["participants"]), 2)

        self.registry.leave_pod(pod_id, "student-bio-01")
        self.assertEqual(len(self.registry.get_pod(pod_id)["participants"]), 1)

    def test_05_whiteboard_delta_synchronization(self):
        """Verify vector stroke and LaTeX formula additions, erasures, and versioning."""
        pod = self.registry.create_pod(
            title="Calculus Integration Sprint",
            subject="Mathematics",
            creator_id="tutor-01"
        )
        pod_id = pod["pod_id"]

        # Append freehand stroke
        stroke_delta = {
            "stroke_id": "stroke-001",
            "author_id": "tutor-01",
            "tool_type": "pen",
            "color": "#2563EB",
            "width": 3,
            "points": [[10, 10], [15, 20], [25, 30]],
            "timestamp": 123456789
        }
        res1 = self.registry.append_whiteboard_delta(pod_id, "stroke", stroke_delta, "tutor-01")
        self.assertTrue(res1["acknowledged"])
        self.assertEqual(res1["total_strokes"], 1)
        self.assertEqual(res1["version"], 2)

        # Append LaTeX formula stamp
        formula_delta = {
            "formula_id": "form-001",
            "author_id": "tutor-01",
            "latex_source": "\\int_{0}^{\\infty} e^{-x^2} dx",
            "position_x": 100,
            "position_y": 150,
            "font_size": 18
        }
        res2 = self.registry.append_whiteboard_delta(pod_id, "formula", formula_delta, "tutor-01")
        self.assertEqual(res2["total_formulas"], 1)

        # Verify whiteboard state
        wb_state = self.registry.get_whiteboard(pod_id)
        self.assertEqual(len(wb_state["strokes"]), 1)
        self.assertEqual(len(wb_state["formulas"]), 1)

        # Erase formula
        self.registry.append_whiteboard_delta(pod_id, "erase", {"formula_id": "form-001"}, "tutor-01")
        wb_state_after_erase = self.registry.get_whiteboard(pod_id)
        self.assertEqual(len(wb_state_after_erase["formulas"]), 0)

        # Clear canvas
        self.registry.append_whiteboard_delta(pod_id, "clear", {}, "tutor-01")
        wb_state_cleared = self.registry.get_whiteboard(pod_id)
        self.assertEqual(len(wb_state_cleared["strokes"]), 0)

    def test_06_voice_mesh_telemetry(self):
        """Verify VAD voice activity detection telemetry recording and retrieval."""
        pod = self.registry.create_pod(
            title="Audio Mesh Test Pod",
            subject="General",
            creator_id="peer-audio-01"
        )
        pod_id = pod["pod_id"]

        self.registry.update_telemetry(pod_id, "peer-audio-01", is_speaking=True, audio_level_db=-18.5)
        telemetry = self.registry.get_telemetry(pod_id)
        self.assertIn("peer-audio-01", telemetry["peers"])
        self.assertTrue(telemetry["peers"]["peer-audio-01"]["is_speaking"])
        self.assertEqual(telemetry["peers"]["peer-audio-01"]["audio_level_db"], -18.5)

    def test_07_developer_architecture_note_headers(self):
        """Verify all Phase 101 target files contain the standardized Developer Architecture Note header."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        phase101_files = [
            os.path.join(repo_root, "frontend", "src", "components", "study-pods", "CollaborativeWhiteboard.tsx"),
            os.path.join(repo_root, "frontend", "src", "components", "study-pods", "StudyPodRoom.tsx"),
            os.path.join(repo_root, "frontend", "src", "lib", "webrtc", "voiceMesh.ts"),
            os.path.join(repo_root, "backend", "app", "api", "v1", "endpoints", "study_pods.py"),
            os.path.join(repo_root, "backend", "tests", "test_phase101_study_pods_and_whiteboard.py")
        ]

        for file_path in phase101_files:
            self.assertTrue(os.path.exists(file_path), f"File missing: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(500)
                self.assertIn("DEVELOPER ARCHITECTURE NOTE", content, f"Missing header in: {file_path}")
                self.assertIn("Phase 101", content, f"Missing Phase 101 in: {file_path}")

    def test_08_zero_emoji_governance(self):
        """Verify strict zero emoji policy across Phase 101 files."""
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        phase101_files = [
            os.path.join(repo_root, "frontend", "src", "components", "study-pods", "CollaborativeWhiteboard.tsx"),
            os.path.join(repo_root, "frontend", "src", "components", "study-pods", "StudyPodRoom.tsx"),
            os.path.join(repo_root, "backend", "app", "api", "v1", "endpoints", "study_pods.py")
        ]

        # Common emoji Unicode ranges to detect
        emoji_ranges = [
            (0x1F600, 0x1F64F),  # Emoticons
            (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
            (0x1F680, 0x1F6FF),  # Transport and Map
            (0x1F700, 0x1F77F),  # Alchemical
            (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
            (0x2600, 0x26FF),    # Misc Symbols
            (0x2700, 0x27BF),    # Dingbats
        ]

        for file_path in phase101_files:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                for char in text:
                    code_point = ord(char)
                    for start, end in emoji_ranges:
                        self.assertFalse(
                            start <= code_point <= end,
                            f"Emoji character '{char}' (U+{code_point:X}) found in {file_path}"
                        )


if __name__ == "__main__":
    unittest.main()
