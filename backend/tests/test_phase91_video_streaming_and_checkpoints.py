"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Test Suite - HLS Video Streaming & In-Lecture Interactive Quizzes
TOPIC:     Adaptive Bitrate (240p Data Saver), Anti-Scrubbing Telemetry, Zero-Emoji
FILE:      backend/tests/test_phase91_video_streaming_and_checkpoints.py
PURPOSE:   Automated verification test suite for Phase 91:
           1. HLS multi-bitrate stream qualities (including 240p rural BD Data Saver).
           2. Dual audio track metadata (Bengali narration / English commentary).
           3. In-lecture interactive checkpoints (chronological sorting, options).
           4. Anti-scrubbing video progress telemetry (15s heartbeat anti-cheat).
           5. Checkpoint answer evaluation (correct resumes, incorrect rewinds 30s).
           6. Course completion criteria (90% watch time + mandatory checkpoints).
           7. Video REST endpoints in backend/app/api/v1/endpoints/video.py.
           8. Frontend HlsLecturePlayer component features and zero-emoji compliance.
AUDIENCE:  QA Engineers, SRE Leads, Video Infrastructure Reviewers & Autonomous Agents
STANDARDS: HLS RFC 8216, OWASP ASVS L2, UI/UX Pro Max, Strict Zero-Emoji
========================================================================================
"""

import unittest
import asyncio
import os
import re

from backend.app.services.video_service import (
    VideoService,
    video_service,
    HLSStreamQuality,
    AudioTrack,
    InteractiveCheckpoint,
    LectureManifest,
    StudentVideoTelemetrySession
)
from backend.app.api.v1.endpoints.video import (
    get_lecture_manifest_endpoint,
    record_video_telemetry_endpoint,
    submit_checkpoint_answer_endpoint,
    get_student_telemetry_endpoint
)
from backend.app.core.fastapi_shim import HTTPException


class TestVideoHLSAndAudioManifest(unittest.TestCase):
    """
    Tests HLS multi-bitrate streams, rural Bangladesh data saver mode, and dual audio.
    """

    def setUp(self):
        self.service = VideoService()
        self.lecture = self.service.get_lecture("lec_phys_01")

    def test_lecture_exists(self):
        self.assertIsNotNone(self.lecture, "Benchmark lecture 'lec_phys_01' must exist")
        self.assertEqual(self.lecture.subject, "physics")
        self.assertEqual(self.lecture.duration_seconds, 600.0)

    def test_qualities_and_data_saver_mode(self):
        quality_names = [q.name for q in self.lecture.qualities]
        self.assertIn("Auto", quality_names)
        self.assertIn("240p", quality_names)
        self.assertIn("360p", quality_names)
        self.assertIn("720p", quality_names)
        self.assertIn("1080p", quality_names)

        q240 = next(q for q in self.lecture.qualities if q.name == "240p")
        self.assertTrue(q240.is_data_saver, "240p must be flagged as data saver for rural BD")
        self.assertLessEqual(q240.bitrate_kbps, 500)

    def test_dual_audio_tracks(self):
        languages = [a.language for a in self.lecture.audio_tracks]
        self.assertIn("bn", languages)
        self.assertIn("en", languages)

        bn_track = next(a for a in self.lecture.audio_tracks if a.language == "bn")
        self.assertTrue(bn_track.is_default, "Bengali audio must be the default track")


class TestInteractiveCheckpoints(unittest.TestCase):
    """
    Verifies checkpoint ordering, multiple choice structure, and pedagogical hints.
    """

    def setUp(self):
        self.service = VideoService()
        self.lecture = self.service.get_lecture("lec_phys_01")

    def test_checkpoints_sorted_chronologically(self):
        checkpoints = self.lecture.checkpoints
        self.assertGreaterEqual(len(checkpoints), 2)
        timestamps = [c.timestamp_seconds for c in checkpoints]
        self.assertEqual(timestamps, sorted(timestamps), "Checkpoints must be sorted chronologically")

    def test_checkpoint_options_and_hints(self):
        cp1 = self.lecture.checkpoints[0]
        self.assertEqual(cp1.checkpoint_id, "cp_phys_01")
        self.assertEqual(cp1.timestamp_seconds, 185.0)
        self.assertEqual(len(cp1.options), 4, "Checkpoint must have exactly 4 options")
        self.assertEqual(cp1.correct_key, "A")
        self.assertTrue(cp1.must_pass)
        self.assertEqual(cp1.rewind_seconds, 30.0)
        self.assertIn("$", cp1.stem_bn)
        self.assertIn("\\theta", cp1.stem_bn)


class TestAntiScrubbingTelemetry(unittest.TestCase):
    """
    Tests the anti-scrubbing progress telemetry algorithms.
    """

    def setUp(self):
        self.session = StudentVideoTelemetrySession(
            student_id="stu_test_99",
            lecture_id="lec_phys_01",
            total_duration=600.0
        )

    def test_normal_continuous_playback_progression(self):
        # Initial heartbeat at t=0
        base_time = 1000.0
        self.session.last_heartbeat_time = base_time
        self.session.last_position_seconds = 0.0

        # Heartbeat 1: 15s later, player at 15s
        res1 = self.session.record_heartbeat(
            current_position_seconds=15.0,
            playback_rate=1.0,
            current_wall_time=base_time + 15.0
        )
        self.assertEqual(res1["total_watched_seconds"], 15.0)
        self.assertEqual(res1["current_position_seconds"], 15.0)

        # Heartbeat 2: 15s later, player at 30s
        res2 = self.session.record_heartbeat(
            current_position_seconds=30.0,
            playback_rate=1.0,
            current_wall_time=base_time + 30.0
        )
        self.assertEqual(res2["total_watched_seconds"], 30.0)

    def test_anti_scrubbing_cheat_detection(self):
        base_time = 1000.0
        self.session.last_heartbeat_time = base_time
        self.session.last_position_seconds = 10.0
        self.session.total_watched_seconds = 10.0

        # Student scrubs / jumps from 10s to 500s in 5 wall-clock seconds!
        res = self.session.record_heartbeat(
            current_position_seconds=500.0,
            playback_rate=1.0,
            current_wall_time=base_time + 5.0
        )

        # Position jumped to 500s, but watched time MUST NOT jump to 500s!
        # It must be capped at legitimate wall time (5s credit -> 10 + 5 = 15s)
        self.assertLessEqual(res["total_watched_seconds"], 15.0)
        self.assertNotEqual(res["total_watched_seconds"], 500.0, "Scrubbing cheat must be prevented")


class TestCheckpointSubmissionAndCompletionCriteria(unittest.TestCase):
    """
    Verifies checkpoint pass/fail logic, rewind instructions, and completion gates.
    """

    def setUp(self):
        self.service = VideoService()
        self.student_id = "stu_checkpoint_user"
        self.lecture_id = "lec_phys_01"

    def test_correct_submission_resumes_playback(self):
        res = self.service.submit_checkpoint_answer(
            student_id=self.student_id,
            lecture_id=self.lecture_id,
            checkpoint_id="cp_phys_01",
            selected_key="A"
        )
        self.assertEqual(res["status"], "PASSED")
        self.assertTrue(res["is_correct"])
        self.assertTrue(res["resume_playback"])
        self.assertIsNone(res["rewind_to_seconds"])

    def test_incorrect_submission_rewinds_30_seconds(self):
        res = self.service.submit_checkpoint_answer(
            student_id=self.student_id,
            lecture_id=self.lecture_id,
            checkpoint_id="cp_phys_01",
            selected_key="C"  # Incorrect option
        )
        self.assertEqual(res["status"], "FAILED")
        self.assertFalse(res["is_correct"])
        self.assertFalse(res["resume_playback"])
        # cp_phys_01 is at 185.0s; 185 - 30 = 155.0s
        self.assertEqual(res["rewind_to_seconds"], 155.0)
        self.assertIn("explanation_hint", res)
        self.assertIn("সেকেন্ড পেছনে", res["message"])

    def test_completion_criteria_enforcement(self):
        session = self.service.get_or_create_session(self.student_id, self.lecture_id)

        # Case 1: Watched 95% of video (570s / 600s), but checkpoints NOT completed
        session.total_watched_seconds = 570.0
        session.completed_checkpoints.clear()

        telemetry = self.service.record_telemetry(
            student_id=self.student_id,
            lecture_id=self.lecture_id,
            current_position_seconds=570.0
        )
        self.assertFalse(telemetry["is_completed"], "Cannot be completed without passing mandatory checkpoints")

        # Case 2: Passed all mandatory checkpoints AND watched >= 90%
        session.completed_checkpoints.add("cp_phys_01")
        session.completed_checkpoints.add("cp_phys_02")

        telemetry2 = self.service.record_telemetry(
            student_id=self.student_id,
            lecture_id=self.lecture_id,
            current_position_seconds=570.0
        )
        self.assertTrue(telemetry2["is_completed"], "Should be completed once 90% watched + checkpoints passed")


class TestVideoRESTEndpoints(unittest.IsolatedAsyncioTestCase):
    """
    Tests the FastAPI REST endpoints for lectures, telemetry, and checkpoints.
    """

    async def test_get_lecture_manifest_endpoint(self):
        resp = await get_lecture_manifest_endpoint("lec_phys_01")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content["lecture_id"], "lec_phys_01")
        self.assertIn("qualities", resp.content)
        self.assertIn("audio_tracks", resp.content)

    async def test_get_lecture_not_found(self):
        with self.assertRaises(HTTPException) as ctx:
            await get_lecture_manifest_endpoint("non_existent_lec")
        self.assertEqual(ctx.exception.status_code, 404)

    async def test_record_telemetry_endpoint(self):
        payload = {
            "student_id": "stu_ep_01",
            "lecture_id": "lec_phys_01",
            "current_position": 45.0,
            "playback_rate": 1.25
        }
        resp = await record_video_telemetry_endpoint(payload)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content["student_id"], "stu_ep_01")
        self.assertIn("completion_percentage", resp.content)

    async def test_submit_checkpoint_endpoint(self):
        payload = {
            "student_id": "stu_ep_02",
            "lecture_id": "lec_phys_01",
            "checkpoint_id": "cp_phys_01",
            "selected_key": "A"
        }
        resp = await submit_checkpoint_answer_endpoint(payload)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content["status"], "PASSED")

    async def test_get_student_telemetry_endpoint(self):
        resp = await get_student_telemetry_endpoint("stu_ep_01", "lec_phys_01")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("total_watched_seconds", resp.content)


class TestFrontendHlsPlayerComponent(unittest.TestCase):
    """
    Verifies frontend/src/components/video/HlsLecturePlayer.tsx
    meets the architectural requirements.
    """

    def setUp(self):
        self.player_path = "frontend/src/components/video/HlsLecturePlayer.tsx"

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.player_path), f"Missing {self.player_path}")

    def test_component_architecture_and_features(self):
        with open(self.player_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Architecture note
        self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)
        # 240p Data saver
        self.assertIn("240p", content)
        self.assertIn("ডাটা সেভার", content)
        # Pitch-corrected speed controls
        self.assertIn("preservesPitch", content)
        # Dual audio tracks
        self.assertIn("audioTracks", content)
        # In-lecture checkpoints & 30s rewind
        self.assertIn("activeCheckpoint", content)
        self.assertIn("rewind_to_seconds", content)
        # KaTeX integration
        self.assertIn("KaTeXRenderer", content)
        # 15s Telemetry heartbeat
        self.assertIn("/api/v1/video/telemetry", content)
        # Zero CLS fixed aspect ratio
        self.assertIn("aspect-video", content)
        # Touch targets (min 44px/48px)
        self.assertIn("min-h-[44px]", content)


class TestZeroEmojiCompliance(unittest.TestCase):
    """
    Strict Zero-Emoji Compliance across all Phase 91 files.
    """

    PHASE_91_FILES = [
        "backend/app/services/video_service.py",
        "backend/app/api/v1/endpoints/video.py",
        "frontend/src/components/video/HlsLecturePlayer.tsx",
        "backend/tests/test_phase91_video_streaming_and_checkpoints.py"
    ]

    EMOJI_PATTERN = re.compile(
        r"[\U0001F600-\U0001F64F"  # Emoticons
        r"\U0001F300-\U0001F5FF"  # Misc symbols & pictographs
        r"\U0001F680-\U0001F6FF"  # Transport & map
        r"\U0001F700-\U0001F77F"  # Alchemical symbols
        r"\U0001F780-\U0001F7FF"  # Geometric shapes
        r"\U0001F800-\U0001F8FF"  # Supplemental arrows
        r"\U0001F900-\U0001F9FF"  # Supplemental symbols & pictographs
        r"\U0001FA00-\U0001FA6F"  # Chess symbols
        r"\U0001FA70-\U0001FAFF"  # Symbols & pictographs extended-A
        r"\U00002702-\U000027B0"  # Dingbats
        r"\U000024C2-\U0001F251"
        r"]+",
        flags=re.UNICODE
    )

    def test_strict_zero_emoji_in_phase91_files(self):
        for file_rel in self.PHASE_91_FILES:
            if not os.path.exists(file_rel):
                continue
            with open(file_rel, "r", encoding="utf-8") as f:
                content = f.read()
            match = self.EMOJI_PATTERN.search(content)
            self.assertIsNone(
                match,
                f"Strict Zero-Emoji Violation in {file_rel}: Found emoji '{match.group(0) if match else ''}'"
            )

    def test_developer_architecture_notes_presence(self):
        for file_rel in self.PHASE_91_FILES:
            if not os.path.exists(file_rel):
                continue
            with open(file_rel, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"Missing DEVELOPER ARCHITECTURE NOTE in {file_rel}"
            )


if __name__ == "__main__":
    unittest.main()
