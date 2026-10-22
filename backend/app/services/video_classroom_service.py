"""
========================================================================================
MODULE:    Video Micro-Classroom & In-Lecture Checkpoint Service
TOPIC:     10 Minute School Benchmark - Interactive Video Learning, Checkpoints & Notes
FILE:      backend/app/services/video_classroom_service.py
PURPOSE:   Orchestrates high-retention video learning modeled after 10 Minute School:
           1. In-lecture interactive checkpoint quizzes at specific timestamp marks.
           2. Multi-speed playback telemetry (1.0x, 1.25x, 1.5x) and resume pointers.
           3. Real-time topic mastery score computation based on checkpoint accuracy.
           4. Timestamped student bookmark notes for exam revision.
STANDARDS: Interactive Video Pedagogy, Active Recall, Micro-Credential Unlocks
AUDIENCE:  EdTech Product Engineers, Content Developers & AI Agents
========================================================================================
"""

import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class VideoClassroomService:
    """
    Service managing 10 Minute School benchmark video micro-lectures.
    Integrates checkpoint quizzes into video timelines for active student recall.
    """

    def __init__(self):
        # In-memory storage for active video sessions, milestones, and notes
        self._playback_state: Dict[str, Dict[str, Any]] = {}  # f"{video_id}:{student_id}" -> state
        self._checkpoint_quizzes: Dict[str, List[Dict[str, Any]]] = {}  # video_id -> list of checkpoints
        self._student_notes: Dict[str, List[Dict[str, Any]]] = {}  # f"{video_id}:{student_id}" -> notes
        self._initialize_curriculum_catalog()

    def _initialize_curriculum_catalog(self):
        """Pre-populates sample benchmark micro-lectures and checkpoint quizzes."""
        vid_id = "vid_diff_01"
        self._checkpoint_quizzes[vid_id] = [
            {
                "checkpoint_id": "cp_diff_01",
                "timestamp_seconds": 252.0,  # 04:12 in lecture
                "question": "What is the derivative of f(x) = sin(x^2) with respect to x using the Chain Rule?",
                "options": [
                    "2x * cos(x^2)",
                    "cos(2x)",
                    "2 * sin(x) * cos(x)",
                    "-2x * cos(x^2)"
                ],
                "correct_option_index": 0,
                "explanation": "By the Chain Rule, d/dx[sin(u)] = cos(u) * du/dx. Here u = x^2, so du/dx = 2x, yielding 2x * cos(x^2).",
                "milestone_unlocked": "Chain Rule Foundations",
                "points": 100
            },
            {
                "checkpoint_id": "cp_diff_02",
                "timestamp_seconds": 540.0,  # 09:00 in lecture
                "question": "If y = e^(3x), what is dy/dx at x = 0?",
                "options": [
                    "1",
                    "3",
                    "e^3",
                    "0"
                ],
                "correct_option_index": 1,
                "explanation": "dy/dx = 3 * e^(3x). At x = 0, dy/dx = 3 * e^0 = 3 * 1 = 3.",
                "milestone_unlocked": "Exponential Derivatives Mastery",
                "points": 100
            }
        ]

    # ----------------------------------------------------------------------------------
    # TOPIC: PLAYBACK TELEMETRY & PROGRESS TRACKING
    # ----------------------------------------------------------------------------------

    def record_playback_progress(
        self,
        video_id: str,
        student_id: str,
        current_timestamp_seconds: float,
        total_duration_seconds: float,
        resolution: str = "1080p",
        playback_speed: float = 1.0
    ) -> Dict[str, Any]:
        """
        Records student playback progress, updates resume position,
        and computes completion percentage.
        """
        state_key = f"{video_id}:{student_id}"
        total_dur = max(total_duration_seconds, 1.0)
        bounded_timestamp = min(max(current_timestamp_seconds, 0.0), total_dur)
        completion_ratio = round((bounded_timestamp / total_dur) * 100.0, 1)

        is_completed = completion_ratio >= 90.0

        existing = self._playback_state.get(state_key, {})
        checkpoints_passed = existing.get("checkpoints_passed", [])

        state = {
            "video_id": video_id,
            "student_id": student_id,
            "current_timestamp_seconds": bounded_timestamp,
            "total_duration_seconds": total_dur,
            "completion_percentage": completion_ratio,
            "is_completed": is_completed,
            "resolution": resolution,
            "playback_speed": playback_speed,
            "checkpoints_passed": checkpoints_passed,
            "last_updated_at": datetime.now(timezone.utc).isoformat()
        }
        self._playback_state[state_key] = state

        return {
            "success": True,
            "playback_state": state,
            "message": "Playback progress successfully synchronized."
        }

    # ----------------------------------------------------------------------------------
    # TOPIC: IN-LECTURE CHECKPOINT QUIZ EVALUATION
    # ----------------------------------------------------------------------------------

    def get_video_checkpoints(self, video_id: str) -> List[Dict[str, Any]]:
        """Returns the in-lecture checkpoints defined for a video."""
        return self._checkpoint_quizzes.get(video_id, [])

    def submit_checkpoint_answer(
        self,
        video_id: str,
        checkpoint_id: str,
        student_id: str,
        timestamp_seconds: float,
        selected_option_index: int
    ) -> Dict[str, Any]:
        """
        Evaluates student answer for an in-lecture checkpoint.
        Updates student mastery and unlocks syllabus milestone if correct.
        """
        checkpoints = self._checkpoint_quizzes.get(video_id, [])
        checkpoint = next((cp for cp in checkpoints if cp["checkpoint_id"] == checkpoint_id), None)

        if not checkpoint:
            return {
                "success": False,
                "error_code": "CHECKPOINT_NOT_FOUND",
                "message": f"Checkpoint '{checkpoint_id}' not found for video '{video_id}'."
            }

        is_correct = (selected_option_index == checkpoint["correct_option_index"])
        state_key = f"{video_id}:{student_id}"
        state = self._playback_state.setdefault(state_key, {
            "video_id": video_id,
            "student_id": student_id,
            "current_timestamp_seconds": timestamp_seconds,
            "checkpoints_passed": [],
            "score": 0
        })

        if is_correct and checkpoint_id not in state["checkpoints_passed"]:
            state["checkpoints_passed"].append(checkpoint_id)
            state["score"] = state.get("score", 0) + checkpoint.get("points", 100)

        total_cps = len(checkpoints)
        passed_cps = len(state["checkpoints_passed"])
        mastery_score = round((passed_cps / max(total_cps, 1)) * 100.0, 1)

        return {
            "success": True,
            "checkpoint_id": checkpoint_id,
            "is_correct": is_correct,
            "selected_option_index": selected_option_index,
            "correct_option_index": checkpoint["correct_option_index"],
            "explanation": checkpoint["explanation"],
            "milestone_unlocked": checkpoint["milestone_unlocked"] if is_correct else None,
            "mastery_score": mastery_score,
            "points_awarded": checkpoint.get("points", 100) if is_correct else 0,
            "message": "Checkpoint evaluated successfully."
        }

    # ----------------------------------------------------------------------------------
    # TOPIC: TIMESTAMPE BOOKMARK NOTES
    # ----------------------------------------------------------------------------------

    def add_video_note(
        self,
        video_id: str,
        student_id: str,
        timestamp_seconds: float,
        note_text: str,
        is_bookmarked: bool = True
    ) -> Dict[str, Any]:
        """
        Saves a student revision note pinned to a specific video timestamp.
        """
        if not note_text.strip():
            return {
                "success": False,
                "error_code": "EMPTY_NOTE_CONTENT",
                "message": "Note content cannot be blank."
            }

        state_key = f"{video_id}:{student_id}"
        notes_list = self._student_notes.setdefault(state_key, [])

        note_id = f"note_{len(notes_list) + 1}_{int(timestamp_seconds)}"
        note_entry = {
            "note_id": note_id,
            "video_id": video_id,
            "student_id": student_id,
            "timestamp_seconds": timestamp_seconds,
            "formatted_timestamp": f"{int(timestamp_seconds // 60):02d}:{int(timestamp_seconds % 60):02d}",
            "note_text": note_text.strip(),
            "is_bookmarked": is_bookmarked,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        notes_list.append(note_entry)

        return {
            "success": True,
            "note": note_entry,
            "message": "Timestamp note pinned successfully."
        }

    def get_student_notes(self, video_id: str, student_id: str) -> List[Dict[str, Any]]:
        """Retrieves all notes created by a student for a video, sorted chronologically."""
        state_key = f"{video_id}:{student_id}"
        notes = self._student_notes.get(state_key, [])
        return sorted(notes, key=lambda n: n["timestamp_seconds"])


# Singleton instance
video_classroom_service = VideoClassroomService()
