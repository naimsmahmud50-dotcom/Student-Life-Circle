"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Video Services - HLS Streaming & In-Lecture Interactive Checkpoints
TOPIC:     Adaptive Bitrate (240p-1080p), Dual Audio, Anti-Scrubbing Telemetry
FILE:      backend/app/services/video_service.py
PURPOSE:   Provides enterprise video streaming services for the Ogrojatra Learning Hub:
           1. HLS Manifest & Multi-Bitrate Catalog (240p Data Saver for rural Bangladesh,
              360p, 720p HD, 1080p Full HD, and Auto ABR).
           2. Dual Audio Track Management (Bengali explanation / English commentary).
           3. In-Lecture Interactive Checkpoints (pauses playback, requires answer,
              correct resumes, incorrect rewinds 30s with pedagogical hints).
           4. Anti-Scrubbing Video Telemetry (15s heartbeat tracking actual watched time
              to prevent speed-skipping / scrubbing cheats for course completion).
           5. Completion Criteria (minimum 90% actual watch time + 100% mandatory checkpoints).
AUDIENCE:  Backend Engineers, Video Infrastructure Specialists & AI Coding Agents
STANDARDS: HLS RFC 8216, OWASP ASVS L2, UI/UX Pro Max, Strict Zero-Emoji
========================================================================================
"""

import time
import math
from typing import Dict, List, Any, Optional, Set


# =============================================================================
# 1. HLS Stream & Audio Models
# =============================================================================
class HLSStreamQuality:
    def __init__(
        self,
        name: str,
        resolution: str,
        bitrate_kbps: int,
        manifest_url: str,
        is_data_saver: bool = False
    ):
        self.name = name  # "240p", "360p", "720p", "1080p", "Auto"
        self.resolution = resolution
        self.bitrate_kbps = bitrate_kbps
        self.manifest_url = manifest_url
        self.is_data_saver = is_data_saver

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "resolution": self.resolution,
            "bitrate_kbps": self.bitrate_kbps,
            "manifest_url": self.manifest_url,
            "is_data_saver": self.is_data_saver
        }


class AudioTrack:
    def __init__(self, language: str, label_bn: str, label_en: str, is_default: bool = False):
        self.language = language  # "bn", "en"
        self.label_bn = label_bn
        self.label_en = label_en
        self.is_default = is_default

    def to_dict(self) -> Dict[str, Any]:
        return {
            "language": self.language,
            "label_bn": self.label_bn,
            "label_en": self.label_en,
            "is_default": self.is_default
        }


# =============================================================================
# 2. Interactive In-Lecture Checkpoints
# =============================================================================
class InteractiveCheckpoint:
    def __init__(
        self,
        checkpoint_id: str,
        timestamp_seconds: float,
        question_id: str,
        stem_bn: str,
        options: List[Dict[str, str]],
        correct_key: str,
        explanation_hint_bn: str,
        must_pass: bool = True,
        rewind_seconds: float = 30.0
    ):
        self.checkpoint_id = checkpoint_id
        self.timestamp_seconds = timestamp_seconds
        self.question_id = question_id
        self.stem_bn = stem_bn
        self.options = options  # [{"key": "A", "text": "..."}, ...]
        self.correct_key = correct_key  # "A", "B", "C", "D"
        self.explanation_hint_bn = explanation_hint_bn
        self.must_pass = must_pass
        self.rewind_seconds = rewind_seconds

    def to_dict(self, include_correct_key: bool = False) -> Dict[str, Any]:
        data = {
            "checkpoint_id": self.checkpoint_id,
            "timestamp_seconds": self.timestamp_seconds,
            "question_id": self.question_id,
            "stem_bn": self.stem_bn,
            "options": self.options,
            "must_pass": self.must_pass,
            "rewind_seconds": self.rewind_seconds
        }
        if include_correct_key:
            data["correct_key"] = self.correct_key
            data["explanation_hint_bn"] = self.explanation_hint_bn
        return data


# =============================================================================
# 3. Lecture Manifest Model
# =============================================================================
class LectureManifest:
    def __init__(
        self,
        lecture_id: str,
        title_bn: str,
        subject: str,
        duration_seconds: float,
        master_playlist_url: str,
        qualities: List[HLSStreamQuality],
        audio_tracks: List[AudioTrack],
        checkpoints: List[InteractiveCheckpoint]
    ):
        self.lecture_id = lecture_id
        self.title_bn = title_bn
        self.subject = subject
        self.duration_seconds = duration_seconds
        self.master_playlist_url = master_playlist_url
        self.qualities = qualities
        self.audio_tracks = audio_tracks
        # Ensure checkpoints are strictly sorted in chronological order
        self.checkpoints = sorted(checkpoints, key=lambda c: c.timestamp_seconds)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lecture_id": self.lecture_id,
            "title_bn": self.title_bn,
            "subject": self.subject,
            "duration_seconds": self.duration_seconds,
            "master_playlist_url": self.master_playlist_url,
            "qualities": [q.to_dict() for q in self.qualities],
            "audio_tracks": [a.to_dict() for a in self.audio_tracks],
            "checkpoints": [c.to_dict(include_correct_key=False) for c in self.checkpoints]
        }


# =============================================================================
# 4. Anti-Scrubbing Telemetry Session
# =============================================================================
class StudentVideoTelemetrySession:
    """
    Maintains continuous watch verification per student per lecture.
    Implements anti-scrubbing heuristics preventing scrub-skipping cheats.
    """
    def __init__(self, student_id: str, lecture_id: str, total_duration: float):
        self.student_id = student_id
        self.lecture_id = lecture_id
        self.total_duration = total_duration
        self.last_heartbeat_time = time.time()
        self.last_position_seconds = 0.0
        self.total_watched_seconds = 0.0
        self.completed_checkpoints: Set[str] = set()
        self.failed_attempts: Dict[str, int] = {}
        self.is_completed = False
        self.playback_rate = 1.0

    def record_heartbeat(
        self,
        current_position_seconds: float,
        playback_rate: float = 1.0,
        current_wall_time: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Processes 15s client heartbeat. Calculates verified elapsed watch time.
        Detects scrub-jumping: If position delta exceeds wall clock delta by >2x,
        only the legitimate elapsed wall-time is credited toward watched progress.
        """
        now = current_wall_time if current_wall_time is not None else time.time()
        wall_time_delta = max(0.0, now - self.last_heartbeat_time)
        pos_delta = current_position_seconds - self.last_position_seconds

        self.playback_rate = max(0.5, min(2.5, playback_rate))

        # Legitimate forward playback check
        if 0.0 <= pos_delta <= (wall_time_delta * self.playback_rate * 1.5):
            # Normal continuous playback: credit full delta
            credited_seconds = pos_delta
        elif pos_delta > (wall_time_delta * self.playback_rate * 1.5):
            # Scrub forward detected! Credit only legitimate elapsed wall time
            credited_seconds = min(wall_time_delta * self.playback_rate, 15.0 * self.playback_rate)
        else:
            # Rewind / jump back or pause: no forward credit
            credited_seconds = 0.0

        self.total_watched_seconds = min(
            self.total_duration,
            self.total_watched_seconds + credited_seconds
        )
        self.last_position_seconds = max(0.0, min(current_position_seconds, self.total_duration))
        self.last_heartbeat_time = now

        completion_pct = round(min(100.0, (self.total_watched_seconds / self.total_duration) * 100.0), 1)

        return {
            "student_id": self.student_id,
            "lecture_id": self.lecture_id,
            "current_position_seconds": round(self.last_position_seconds, 2),
            "total_watched_seconds": round(self.total_watched_seconds, 2),
            "completion_percentage": completion_pct,
            "completed_checkpoints": list(self.completed_checkpoints)
        }


# =============================================================================
# 5. Video Service Manager
# =============================================================================
class VideoService:
    """
    Central Video Infrastructure Service managing HLS lectures, checkpoints,
    and anti-cheat student telemetry sessions.
    """

    def __init__(self):
        self._lectures: Dict[str, LectureManifest] = {}
        self._sessions: Dict[str, StudentVideoTelemetrySession] = {}  # f"{student_id}:{lecture_id}" -> session
        self._initialize_benchmark_lectures()

    def _initialize_benchmark_lectures(self):
        """Initializes authentic HSC / Admission benchmark video lectures."""
        # 1. HSC Physics - Projectile Motion (প্রক্ষেপকের গতি)
        hsc_physics_checkpoints = [
            InteractiveCheckpoint(
                checkpoint_id="cp_phys_01",
                timestamp_seconds=185.0,  # 03:05
                question_id="q_proj_01",
                stem_bn="একটি প্রক্ষেপককে $\\theta$ কোণে $v_0$ আদিবেগে নিক্ষেপ করা হলে, তার সর্বোচ্চ উচ্চতার সমীকরণ কোনটি?",
                options=[
                    {"key": "A", "text": "$H = \\frac{v_0^2 \\sin^2 \\theta}{2g}$"},
                    {"key": "B", "text": "$H = \\frac{v_0^2 \\sin 2\\theta}{g}$"},
                    {"key": "C", "text": "$H = \\frac{v_0 \\sin \\theta}{g}$"},
                    {"key": "D", "text": "$H = \\frac{v_0^2 \\cos^2 \\theta}{2g}$"}
                ],
                correct_key="A",
                explanation_hint_bn="সর্বোচ্চ উচ্চতায় উল্লম্ব বেগ $v_y = 0$ হয়। $v_y^2 = (v_0 \\sin \\theta)^2 - 2gH$ সমীকরণ থেকে $H = \\frac{v_0^2 \\sin^2 \\theta}{2g}$ পাওয়া যায়।",
                must_pass=True,
                rewind_seconds=30.0
            ),
            InteractiveCheckpoint(
                checkpoint_id="cp_phys_02",
                timestamp_seconds=420.0,  # 07:00
                question_id="q_proj_02",
                stem_bn="সর্বোচ্চ আনুভূমিক পাল্লার (Maximum Range) জন্য প্রক্ষেপণ কোণ $\\theta$ কত হওয়া আবশ্যক?",
                options=[
                    {"key": "A", "text": "$30^\\circ$"},
                    {"key": "B", "text": "$45^\\circ$"},
                    {"key": "C", "text": "$60^\\circ$"},
                    {"key": "D", "text": "$90^\\circ$"}
                ],
                correct_key="B",
                explanation_hint_bn="পাল্লা $R = \\frac{v_0^2 \\sin 2\\theta}{g}$। $\\sin 2\\theta$ এর সর্বোচ্চ মান $1$ যখন $2\\theta = 90^\\circ$ বা $\\theta = 45^\\circ$ হয়।",
                must_pass=True,
                rewind_seconds=30.0
            )
        ]

        physics_qualities = [
            HLSStreamQuality("Auto", "Adaptive", 0, "https://cdn.ogrojatra.edu.bd/hls/physics_proj_01/master.m3u8", False),
            HLSStreamQuality("240p", "426x240", 400, "https://cdn.ogrojatra.edu.bd/hls/physics_proj_01/240p.m3u8", True),  # Data Saver
            HLSStreamQuality("360p", "640x360", 800, "https://cdn.ogrojatra.edu.bd/hls/physics_proj_01/360p.m3u8", False),
            HLSStreamQuality("720p", "1280x720", 2500, "https://cdn.ogrojatra.edu.bd/hls/physics_proj_01/720p.m3u8", False),
            HLSStreamQuality("1080p", "1920x1080", 5000, "https://cdn.ogrojatra.edu.bd/hls/physics_proj_01/1080p.m3u8", False)
        ]

        physics_audio = [
            AudioTrack("bn", "বাংলা ধারাবর্ণনা", "Bengali Narration", is_default=True),
            AudioTrack("en", "ইংরেজি ব্যাখ্যা", "English Commentary", is_default=False)
        ]

        self._lectures["lec_phys_01"] = LectureManifest(
            lecture_id="lec_phys_01",
            title_bn="এইচএসসি পদার্থবিজ্ঞান ১ম পত্র: প্রক্ষেপকের গতি ও পাল্লা বিশ্লেষণ",
            subject="physics",
            duration_seconds=600.0,  # 10 minutes
            master_playlist_url="https://cdn.ogrojatra.edu.bd/hls/physics_proj_01/master.m3u8",
            qualities=physics_qualities,
            audio_tracks=physics_audio,
            checkpoints=hsc_physics_checkpoints
        )

    def get_lecture(self, lecture_id: str) -> Optional[LectureManifest]:
        return self._lectures.get(lecture_id)

    def get_or_create_session(self, student_id: str, lecture_id: str) -> StudentVideoTelemetrySession:
        key = f"{student_id}:{lecture_id}"
        if key not in self._sessions:
            lecture = self.get_lecture(lecture_id)
            duration = lecture.duration_seconds if lecture else 600.0
            self._sessions[key] = StudentVideoTelemetrySession(student_id, lecture_id, duration)
        return self._sessions[key]

    def record_telemetry(
        self,
        student_id: str,
        lecture_id: str,
        current_position_seconds: float,
        playback_rate: float = 1.0,
        current_wall_time: Optional[float] = None
    ) -> Dict[str, Any]:
        session = self.get_or_create_session(student_id, lecture_id)
        telemetry_result = session.record_heartbeat(current_position_seconds, playback_rate, current_wall_time)

        # Check completion criteria:
        # 1. Total watched seconds >= 90% of duration
        # 2. All mandatory checkpoints completed
        lecture = self.get_lecture(lecture_id)
        is_completed = False
        if lecture:
            mandatory_checkpoints = {c.checkpoint_id for c in lecture.checkpoints if c.must_pass}
            all_mandatory_passed = mandatory_checkpoints.issubset(session.completed_checkpoints)
            watched_enough = session.total_watched_seconds >= (lecture.duration_seconds * 0.90)
            is_completed = all_mandatory_passed and watched_enough

        session.is_completed = is_completed
        telemetry_result["is_completed"] = is_completed

        # Check if an upcoming checkpoint is within range
        upcoming = None
        if lecture:
            for cp in lecture.checkpoints:
                if cp.checkpoint_id not in session.completed_checkpoints:
                    if cp.timestamp_seconds <= current_position_seconds:
                        upcoming = cp.to_dict(include_correct_key=False)
                        break

        telemetry_result["active_checkpoint_trigger"] = upcoming
        return telemetry_result

    def submit_checkpoint_answer(
        self,
        student_id: str,
        lecture_id: str,
        checkpoint_id: str,
        selected_key: str
    ) -> Dict[str, Any]:
        """
        Evaluates a checkpoint answer.
        On success: unlocks lecture resume.
        On failure: triggers 30-second rewind instruction with pedagogical hint in Bengali.
        """
        lecture = self.get_lecture(lecture_id)
        if not lecture:
            return {"status": "ERROR", "message": "লেকচারটি পাওয়া যায়নি।"}

        checkpoint = next((c for c in lecture.checkpoints if c.checkpoint_id == checkpoint_id), None)
        if not checkpoint:
            return {"status": "ERROR", "message": "চেকপয়েন্টটি পাওয়া যায়নি।"}

        session = self.get_or_create_session(student_id, lecture_id)

        is_correct = (selected_key.strip().upper() == checkpoint.correct_key)

        if is_correct:
            session.completed_checkpoints.add(checkpoint_id)
            return {
                "status": "PASSED",
                "checkpoint_id": checkpoint_id,
                "is_correct": True,
                "resume_playback": True,
                "rewind_to_seconds": None,
                "message": "সঠিক উত্তর! চমৎকার বিশ্লেষণ। লেকচার পুনরায় শুরু হচ্ছে।"
            }
        else:
            session.failed_attempts[checkpoint_id] = session.failed_attempts.get(checkpoint_id, 0) + 1
            rewind_target = max(0.0, checkpoint.timestamp_seconds - checkpoint.rewind_seconds)
            return {
                "status": "FAILED",
                "checkpoint_id": checkpoint_id,
                "is_correct": False,
                "resume_playback": False,
                "rewind_to_seconds": rewind_target,
                "explanation_hint": checkpoint.explanation_hint_bn,
                "message": f"উত্তরটি সঠিক হয়নি। মূল ধারণাটি পুনরায় দেখার জন্য ভিডিওটি {int(checkpoint.rewind_seconds)} সেকেন্ড পেছনে নেওয়া হচ্ছে।"
            }


# Singleton instance
video_service = VideoService()
