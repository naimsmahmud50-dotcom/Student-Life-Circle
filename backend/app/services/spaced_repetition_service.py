"""
================================================================================
MODULE: Adaptive Learning & Spaced Repetition Engine (মেধা ঘাটতি ও মেমোরি রিটেনশন)
TOPIC: SuperMemo SM-2 Scientific Spaced Repetition & Due Item Scheduler
FILE: backend/app/services/spaced_repetition_service.py
PURPOSE: Implements the SuperMemo SM-2 spaced repetition algorithm to optimize
         student memory retention and eradicate academic learning gaps. Calculates
         dynamic Ease Factors (EF), adaptive review intervals, and prioritizes
         erroneous NCTB questions for timely spaced review drills.
AUDIENCE: Learning Scientists, Adaptive Engine Developers, Academic Reviewers.
STANDARDS: SuperMemo SM-2 Standard, Cognitive Science Spaced Practice Principles.
================================================================================
"""

import math
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple


class SpacedRepetitionService:
    """Scientific spaced repetition memory scheduler based on SuperMemo SM-2."""

    DEFAULT_EASE_FACTOR = 2.5
    MINIMUM_EASE_FACTOR = 1.3

    def __init__(self) -> None:
        # Key: (student_id, question_id) -> ReviewItemDict
        self._items: Dict[Tuple[str, str], Dict[str, Any]] = {}

    def calculate_sm2_interval(
        self,
        quality_score: int,
        repetitions: int,
        previous_interval_days: int,
        previous_ease_factor: float,
    ) -> Tuple[int, int, float]:
        """
        Calculates next repetition count, interval in days, and updated Ease Factor.
        
        Args:
            quality_score: Integer from 0 (complete blackout) to 5 (perfect recall).
            repetitions: Number of consecutive successful recalls.
            previous_interval_days: Previous review interval in days.
            previous_ease_factor: Previous Ease Factor (default 2.5).

        Returns:
            Tuple of (new_repetitions, new_interval_days, new_ease_factor)
        """
        # Clamp quality score between 0 and 5
        q = max(0, min(5, quality_score))

        # 1. Calculate updated Ease Factor
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        delta_ef = 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)
        new_ef = max(self.MINIMUM_EASE_FACTOR, previous_ease_factor + delta_ef)
        new_ef = round(new_ef, 2)

        # 2. If recall failed (q < 3), restart repetition cycle
        if q < 3:
            new_reps = 0
            new_interval = 1  # Review again tomorrow
            return new_reps, new_interval, new_ef

        # 3. Successful recall progression
        new_reps = repetitions + 1
        if new_reps == 1:
            new_interval = 1
        elif new_reps == 2:
            new_interval = 6
        else:
            new_interval = max(1, math.ceil(previous_interval_days * new_ef))

        return new_reps, new_interval, new_ef

    def record_review(
        self,
        student_id: str,
        question_id: str,
        topic: str,
        quality_score: int,
        review_timestamp: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Records student performance on a question and schedules next review date."""
        now = review_timestamp or datetime.now(timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        key = (student_id, question_id)

        existing = self._items.get(key)
        if existing:
            prev_reps = existing["repetitions"]
            prev_interval = existing["interval_days"]
            prev_ef = existing["ease_factor"]
            total_reviews = existing["total_reviews"] + 1
        else:
            prev_reps = 0
            prev_interval = 0
            prev_ef = self.DEFAULT_EASE_FACTOR
            total_reviews = 1

        new_reps, new_interval, new_ef = self.calculate_sm2_interval(
            quality_score=quality_score,
            repetitions=prev_reps,
            previous_interval_days=prev_interval,
            previous_ease_factor=prev_ef,
        )

        next_due_date = now + timedelta(days=new_interval)

        record = {
            "student_id": student_id,
            "question_id": question_id,
            "topic": topic,
            "repetitions": new_reps,
            "interval_days": new_interval,
            "ease_factor": new_ef,
            "last_reviewed_at": now.isoformat(),
            "next_due_at": next_due_date.isoformat(),
            "last_quality_score": quality_score,
            "total_reviews": total_reviews,
            "status": "MASTERED" if new_reps >= 4 else "LEARNING",
        }

        self._items[key] = record
        return record

    def get_due_reviews(
        self,
        student_id: str,
        as_of_time: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """Returns all questions due for spaced repetition review as of the given time."""
        target_time = as_of_time or datetime.now(timezone.utc)
        if target_time.tzinfo is None:
            target_time = target_time.replace(tzinfo=timezone.utc)
        due_items = []

        for (s_id, _), item in self._items.items():
            if s_id != student_id:
                continue
            due_at = datetime.fromisoformat(item["next_due_at"])
            if due_at.tzinfo is None:
                due_at = due_at.replace(tzinfo=timezone.utc)
            # If due date has passed or is right now
            if due_at <= target_time:
                due_items.append(item)

        # Sort by urgency: lowest ease factor and oldest due date first
        due_items.sort(key=lambda x: (x["ease_factor"], x["next_due_at"]))
        return due_items

    def get_student_mastery_stats(self, student_id: str) -> Dict[str, Any]:
        """Aggregates spaced repetition memory retention statistics for a student."""
        student_items = [item for (s_id, _), item in self._items.items() if s_id == student_id]

        if not student_items:
            return {
                "student_id": student_id,
                "total_tracked_questions": 0,
                "mastered_questions": 0,
                "learning_questions": 0,
                "average_ease_factor": self.DEFAULT_EASE_FACTOR,
                "retention_rate_pct": 100.0,
            }

        mastered = sum(1 for it in student_items if it["status"] == "MASTERED")
        learning = len(student_items) - mastered
        avg_ef = sum(it["ease_factor"] for it in student_items) / len(student_items)

        successful_recalls = sum(1 for it in student_items if it["last_quality_score"] >= 3)
        retention_rate = (successful_recalls / len(student_items)) * 100.0

        return {
            "student_id": student_id,
            "total_tracked_questions": len(student_items),
            "mastered_questions": mastered,
            "learning_questions": learning,
            "average_ease_factor": round(avg_ef, 2),
            "retention_rate_pct": round(retention_rate, 1),
        }

    def reset_for_testing(self) -> None:
        """Clears memory state for isolated test execution."""
        self._items.clear()


# Global Singleton Service
spaced_repetition_service = SpacedRepetitionService()
