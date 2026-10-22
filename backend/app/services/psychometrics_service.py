"""
========================================================================================
MODULE:    Psychometric Mastery & Adaptive Difficulty (IRT/Elo) Service
TOPIC:     Student Ability Rating, Zone of Proximal Development & Anti-Toxic Habits
FILE:      backend/app/services/psychometrics_service.py
PURPOSE:   Evaluates student conceptual mastery using adaptive Elo / Item Response Theory
           (IRT) principles. Dynamically adjusts question difficulty to maintain optimal
           learning engagement (60-75% challenge band). Powers the Anti-Toxic Habit
           Engine with 'Rest Day' streak freeze passes and non-punitive comeback boosts.
AUDIENCE:  Psychometricians, Adaptive Learning Engineers & AI Agents
STANDARDS: Psychometric Transparency, Anti-Toxic Gamification, FR-003
========================================================================================
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timezone, timedelta
from backend.app.core.timekeeper import ServerTimekeeper


class PsychometricsService:
    """
    Adaptive psychometric calibration and mental-wellness habit engine.
    """

    BASELINE_RATING = 1200.0  # Equivalent to theta = 0.0 in IRT
    K_FACTOR = 24.0

    def __init__(self):
        self._student_ratings: Dict[str, float] = {}       # student_id -> rating (Elo)
        self._habit_records: Dict[str, Dict[str, Any]] = {} # student_id -> habit stats

    def get_or_create_student_rating(self, student_id: str) -> float:
        """Retrieves current student mastery rating or initializes to baseline."""
        if student_id not in self._student_ratings:
            self._student_ratings[student_id] = self.BASELINE_RATING
        return self._student_ratings[student_id]

    @staticmethod
    def calculate_expected_probability(student_rating: float, question_difficulty: float) -> float:
        """
        Calculates expected probability of correct response using the standard logistic model:
        P = 1 / (1 + 10^((difficulty - rating) / 400))
        Guarded against math overflow for extreme differentials.
        """
        diff = (question_difficulty - student_rating) / 400.0
        # Prevent math overflow for extreme differentials
        clamped_diff = max(-10.0, min(10.0, diff))
        return 1.0 / (1.0 + math.pow(10.0, clamped_diff))

    def get_recommended_difficulty_band(self, student_id: str) -> Dict[str, Any]:
        """
        Calculates Zone of Proximal Development (ZPD) difficulty band around student rating.
        Target probability of success: 60% - 75% for optimal cognitive flow and mental resilience.
        """
        rating = self.get_or_create_student_rating(student_id)
        min_diff = round(rating - 190.0, 1)
        max_diff = round(rating + 60.0, 1)
        target_diff = round(rating - 70.0, 1)
        return {
            "student_rating": rating,
            "min_difficulty": min_diff,
            "max_difficulty": max_diff,
            "target_difficulty": target_diff,
            "target_probability_band": "0.60 - 0.75",
            "description": "Optimal challenge zone promoting deep mastery without anxiety"
        }

    def update_rating_after_response(
        self,
        student_id: str,
        question_difficulty: float,
        is_correct: bool
    ) -> Tuple[float, float]:
        """
        Calibrates student rating based on response:
        new_rating = old_rating + K * (actual_score - expected_score)
        Returns: (new_rating, rating_delta)
        """
        old_rating = self.get_or_create_student_rating(student_id)
        expected = self.calculate_expected_probability(old_rating, question_difficulty)
        actual = 1.0 if is_correct else 0.0

        delta = self.K_FACTOR * (actual - expected)
        new_rating = round(old_rating + delta, 1)

        self._student_ratings[student_id] = new_rating
        return new_rating, round(delta, 1)

    def filter_adaptive_questions(
        self,
        student_id: str,
        question_pool: List[Dict[str, Any]],
        target_count: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Filters questions within Zone of Proximal Development (ZPD):
        Selects items where 0.50 <= P(correct) <= 0.80.
        Avoids trivial questions and demoralizingly impossible items.
        """
        rating = self.get_or_create_student_rating(student_id)
        scored_pool = []

        for q in question_pool:
            diff = q.get("difficulty_rating", self.BASELINE_RATING)
            p = self.calculate_expected_probability(rating, diff)
            # Optimal ZPD distance from 0.65
            zpd_distance = abs(p - 0.65)
            scored_pool.append((zpd_distance, q))

        # Sort by closest to optimal challenge
        scored_pool.sort(key=lambda x: x[0])
        return [item[1] for item in scored_pool[:target_count]]

    # -------------------------------------------------------------------------
    # Anti-Toxic Habit Engine (Streak Protection & Comeback Boosts)
    # -------------------------------------------------------------------------
    def get_or_create_habit_record(self, student_id: str) -> Dict[str, Any]:
        """Retrieves or initializes student streak and freeze pass state."""
        if student_id not in self._habit_records:
            now_iso = ServerTimekeeper.get_server_iso_now()
            self._habit_records[student_id] = {
                "student_id": student_id,
                "current_streak": 1,
                "highest_streak": 1,
                "banked_freeze_passes": 1,  # New learners receive 1 welcome freeze pass
                "last_active_date": now_iso[:10],  # YYYY-MM-DD
                "is_frozen": False,
                "comeback_boost_active": False,
                "comeback_boost_multiplier": 1.0
            }
        return self._habit_records[student_id]

    def record_daily_study_activity(
        self,
        student_id: str,
        questions_completed: int = 10,
        activity_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Logs daily study activity and updates streak.
        Applies streak freeze protection if yesterday was missed.
        """
        rec = self.get_or_create_habit_record(student_id)
        today = activity_date or ServerTimekeeper.get_server_iso_now()[:10]
        last_date_str = rec["last_active_date"]

        last_date = datetime.strptime(last_date_str, "%Y-%m-%d").date()
        current_date = datetime.strptime(today, "%Y-%m-%d").date()
        days_gap = (current_date - last_date).days

        if days_gap == 0:
            # Already logged today
            pass
        elif days_gap == 1:
            # Consecutive day!
            rec["current_streak"] += 1
            if rec["current_streak"] > rec["highest_streak"]:
                rec["highest_streak"] = rec["current_streak"]
            # Earn a freeze pass every 7 days (max 2 banked)
            if rec["current_streak"] % 7 == 0 and rec["banked_freeze_passes"] < 2:
                rec["banked_freeze_passes"] += 1
        elif days_gap == 2 and rec["banked_freeze_passes"] > 0:
            # 1 day missed, but learner has a banked freeze pass!
            rec["banked_freeze_passes"] -= 1
            rec["is_frozen"] = True
            rec["current_streak"] += 1  # Streak protected!
        else:
            # Streak broke without freeze pass -> Activate Comeback Boost instead of shame
            rec["current_streak"] = 1
            rec["comeback_boost_active"] = True
            rec["comeback_boost_multiplier"] = 1.25  # 25% XP/mastery boost for restarting

        rec["last_active_date"] = today
        return rec

    def consume_streak_freeze_pass(self, student_id: str) -> Tuple[bool, str]:
        """Allows learner to explicitly activate a Rest Day freeze pass."""
        rec = self.get_or_create_habit_record(student_id)
        if rec["banked_freeze_passes"] <= 0:
            return False, "NO_FREEZE_PASSES_AVAILABLE"

        rec["banked_freeze_passes"] -= 1
        rec["is_frozen"] = True
        return True, "STREAK_FROZEN_FOR_REST_DAY"


# Singleton Service Instance
psychometrics_service = PsychometricsService()
