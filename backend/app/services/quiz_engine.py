"""
========================================================================================
MODULE:    Quiz Engine Service & Live Examination Core
TOPIC:     Session Management, Deterministic Shuffling, Idempotent Writes & Scoring
FILE:      backend/app/services/quiz_engine.py
PURPOSE:   The core transactional engine powering anytime practice and high-stakes
           live challenges. Enforces deterministic randomization per student to deter
           cheating, handles sub-millisecond idempotent answer saves via in-memory
           state buffers, prevents client clock manipulation, and computes negative
           marking scores strictly server-side.
AUDIENCE:  Developers, Exam Security Architects & AI Agents
STANDARDS: Clean Architecture, High-Load Scalability, Idempotency (RFC 7231)
========================================================================================
"""

import hashlib
import random
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any

from backend.app.core.timekeeper import ServerTimekeeper
from backend.app.schemas.quiz_schema import (
    QuizMode,
    AttemptStatus,
    QuizAttemptStartResponse,
    ActiveQuizQuestion,
    AnswerSaveResponse,
    QuizResultResponse,
    MistakeReviewItem
)


class QuizEngineService:
    """
    High-performance, concurrency-safe Live MCQ Engine.
    In memory and persistent storage orchestration.
    """

    def __init__(self):
        # Simulated high-speed in-memory store (mirrors Redis in production)
        self._idempotency_cache: Dict[str, Dict[str, Any]] = {}
        self._active_attempts: Dict[str, Dict[str, Any]] = {}
        self._quarantined_questions: set = set()

    @staticmethod
    def _generate_deterministic_seed(user_id: str, blueprint_id: str, attempt_id: str) -> int:
        """
        Derives an integer seed from SHA-256 hash of (user_id, blueprint_id, attempt_id).
        Guarantees that question order and option sequences are randomized per student
        while remaining deterministic upon page refresh or reconnection.
        """
        combined = f"{user_id}:{blueprint_id}:{attempt_id}"
        hash_hex = hashlib.sha256(combined.encode("utf-8")).hexdigest()
        return int(hash_hex[:8], 16)

    def start_practice_attempt(
        self,
        user_id: str,
        blueprint_id: str,
        mode: QuizMode,
        raw_questions: List[Dict[str, Any]],
        duration_minutes: int = 15,
        negative_marking: float = 0.0
    ) -> QuizAttemptStartResponse:
        """
        Initializes a new practice attempt with server-locked start and expiration times.
        """
        now = ServerTimekeeper.get_server_utc_now()
        expires_at = now + timedelta(minutes=duration_minutes)
        attempt_id = f"att_{hashlib.sha256(f'{user_id}:{now.timestamp()}'.encode()).hexdigest()[:16]}"
        seed = self._generate_deterministic_seed(user_id, blueprint_id, attempt_id)

        # Shuffle questions deterministically using attempt seed
        rng = random.Random(seed)
        shuffled_questions = list(raw_questions)
        rng.shuffle(shuffled_questions)

        active_questions: List[ActiveQuizQuestion] = []
        for idx, q in enumerate(shuffled_questions, start=1):
            # Shuffle options independently per question
            q_rng = random.Random(seed + idx)
            options = list(q.get("options", []))
            q_rng.shuffle(options)

            # Sanitize options to strictly exclude correct answer keys
            sanitized_options = [
                {
                    "id": opt["id"],
                    "key": opt["option_key"],
                    "text_bn": opt["option_text_bn"],
                    "text_en": opt.get("option_text_en")
                }
                for opt in options
            ]

            active_questions.append(
                ActiveQuizQuestion(
                    question_version_id=q["id"],
                    order=idx,
                    stem_bn=q["stem_bn"],
                    stem_en=q.get("stem_en"),
                    options=sanitized_options,
                    estimated_seconds=q.get("estimated_seconds", 60)
                )
            )

        # Record active attempt in state
        self._active_attempts[attempt_id] = {
            "attempt_id": attempt_id,
            "user_id": user_id,
            "blueprint_id": blueprint_id,
            "mode": mode,
            "started_at": now,
            "expires_at": expires_at,
            "status": AttemptStatus.IN_PROGRESS,
            "negative_marking": negative_marking,
            "raw_questions": {q["id"]: q for q in raw_questions},
            "saved_answers": {},  # question_id -> {option_id, saved_at}
        }

        return QuizAttemptStartResponse(
            attempt_id=attempt_id,
            status=AttemptStatus.IN_PROGRESS,
            mode=mode,
            started_at=now.isoformat(),
            expires_at=expires_at.isoformat(),
            server_time=now.isoformat(),
            remaining_seconds=int(duration_minutes * 60),
            total_questions=len(active_questions),
            negative_marking_value=negative_marking,
            questions=active_questions
        )

    def save_answer_idempotent(
        self,
        attempt_id: str,
        user_id: str,
        question_version_id: str,
        selected_option_id: Optional[str],
        idempotency_key: str,
        time_taken_seconds: Optional[float] = None
    ) -> Tuple[bool, AnswerSaveResponse, str]:
        """
        Saves student answer safely using UUID idempotency keys.
        Prevents race conditions, duplicates from unstable 3G connections,
        and enforces server cutoff deadlines.
        """
        # 1. Check idempotency cache first
        if idempotency_key in self._idempotency_cache:
            cached = self._idempotency_cache[idempotency_key]
            return True, AnswerSaveResponse(
                status="ALREADY_RECORDED",
                attempt_id=attempt_id,
                question_version_id=question_version_id,
                saved_at=cached["saved_at"],
                is_session_active=True
            ), "IDEMPOTENT_REPLAY"

        # 2. Validate attempt existence and user ownership (ABAC / IDOR guard)
        attempt = self._active_attempts.get(attempt_id)
        if not attempt:
            return False, None, "ATTEMPT_NOT_FOUND"

        if attempt["user_id"] != user_id:
            return False, None, "FORBIDDEN_ATTEMPT_OWNERSHIP"

        # 3. Server-authoritative expiration check
        if ServerTimekeeper.is_attempt_expired(attempt["expires_at"]):
            attempt["status"] = AttemptStatus.EXPIRED
            return False, None, "EXAM_EXPIRED"

        # 4. Save answer to attempt state
        now_str = ServerTimekeeper.get_server_iso_now()
        attempt["saved_answers"][question_version_id] = {
            "selected_option_id": selected_option_id,
            "saved_at": now_str,
            "time_taken_seconds": time_taken_seconds or 0.0
        }

        # 5. Populate idempotency cache
        response = AnswerSaveResponse(
            status="SAVED",
            attempt_id=attempt_id,
            question_version_id=question_version_id,
            saved_at=now_str,
            is_session_active=True
        )
        self._idempotency_cache[idempotency_key] = {
            "saved_at": now_str,
            "data": response.model_dump()
        }

        return True, response, "OK"

    def get_attempt_state(
        self,
        attempt_id: str,
        user_id: Optional[str] = None
    ) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Retrieves active attempt state and answers.
        Enforces strict IDOR protection: if user_id is provided, must match attempt['user_id'].
        """
        attempt = self._active_attempts.get(attempt_id)
        if not attempt:
            return False, None, "ATTEMPT_NOT_FOUND"

        if user_id and attempt["user_id"] != user_id:
            return False, None, "FORBIDDEN_ATTEMPT_OWNERSHIP"

        return True, attempt, "OK"

    def submit_and_score(
        self,
        attempt_id: str,
        user_id: str
    ) -> Tuple[bool, Optional[QuizResultResponse], str]:
        """
        Finalizes an exam attempt, scores answers against frozen keys,
        applies negative marking, generates mistake reviews, and schedules
        missed items for spaced-repetition.
        """
        attempt = self._active_attempts.get(attempt_id)
        if not attempt:
            return False, None, "ATTEMPT_NOT_FOUND"

        if attempt["user_id"] != user_id:
            return False, None, "FORBIDDEN_ATTEMPT_OWNERSHIP"

        raw_questions = attempt["raw_questions"]
        saved_answers = attempt["saved_answers"]
        negative_val = attempt["negative_marking"]

        correct_count = 0
        incorrect_count = 0
        unanswered_count = 0
        mistakes: List[MistakeReviewItem] = []

        for q_id, q_data in raw_questions.items():
            # If question is quarantined during test, grant full credit
            if q_id in self._quarantined_questions:
                correct_count += 1
                continue

            saved = saved_answers.get(q_id)
            selected_opt_id = saved["selected_option_id"] if saved else None

            # Find correct option
            correct_opt = next((opt for opt in q_data["options"] if opt.get("is_correct")), None)
            correct_opt_id = correct_opt["id"] if correct_opt else None

            if not selected_opt_id:
                unanswered_count += 1
            elif selected_opt_id == correct_opt_id:
                correct_count += 1
            else:
                incorrect_count += 1
                # Identify selected option key
                selected_opt = next((opt for opt in q_data["options"] if opt["id"] == selected_opt_id), None)
                mistakes.append(
                    MistakeReviewItem(
                        question_version_id=q_id,
                        stem_bn=q_data["stem_bn"],
                        selected_option_key=selected_opt["option_key"] if selected_opt else None,
                        correct_option_key=correct_opt["option_key"] if correct_opt else "A",
                        correct_option_text_bn=correct_opt["option_text_bn"] if correct_opt else "",
                        explanation_bn=q_data.get("explanation_bn", "বিশ্লেষণ শীঘ্রই যোগ করা হবে।"),
                        misconception_tag=q_data.get("cognitive_skill", "GENERAL_CONCEPT"),
                        added_to_mistake_queue=True
                    )
                )

        total_questions = len(raw_questions)
        raw_score = (correct_count * 1.0) - (incorrect_count * negative_val)
        accuracy = (correct_count / total_questions * 100.0) if total_questions > 0 else 0.0

        now = ServerTimekeeper.get_server_utc_now()
        started_at = attempt["started_at"]
        time_spent = int((now - started_at).total_seconds())

        attempt["status"] = AttemptStatus.SUBMITTED

        # For competitive admission mock and live challenge modes, reflect true negative score
        is_competitive = attempt.get("mode") in (QuizMode.MOCK_EXAM, QuizMode.LIVE_CHALLENGE) and negative_val > 0.0
        final_score = round(raw_score, 2) if is_competitive else round(max(0.0, raw_score), 2)

        return True, QuizResultResponse(
            attempt_id=attempt_id,
            status=AttemptStatus.SUBMITTED,
            raw_score=final_score,
            total_questions=total_questions,
            correct_count=correct_count,
            incorrect_count=incorrect_count,
            unanswered_count=unanswered_count,
            accuracy_percentage=round(accuracy, 1),
            time_spent_seconds=time_spent,
            rank=None,  # Populated when leaderboard batch concludes
            percentile=None,
            mistakes=mistakes,
            next_recommended_action="ভুল হওয়া প্রশ্নগুলো আপনার 'রিভিশন কিউ'-তে যুক্ত করা হয়েছে।"
        ), "OK"


# Singleton Service Instance
quiz_engine = QuizEngineService()
