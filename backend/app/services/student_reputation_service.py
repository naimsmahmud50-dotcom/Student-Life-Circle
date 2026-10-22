"""
========================================================================================
MODULE:    Holistic Student Reputation & Gamified Quest Engine
TOPIC:     4-Pillar Composite Score, Reputation Tiers & Habit Acceleration Quests
FILE:      backend/app/services/student_reputation_service.py
PURPOSE:   Calculates the continuous 0-1000 Student Life-Cycle Reputation Score:
           1. Academic Mastery (35% - CAT ability θ & video checkpoint scores)
           2. Tutoring Reliability (25% - CareTutors ratings & completed sessions)
           3. Career Preparedness (25% - Bdjobs verified skills & sealed CV snapshots)
           4. Community Integrity (15% - Tribunal jurist quorum & peer circle notes)
           Promotes students across 4 merit tiers: Novice Scholar -> Eminence Fellow.
STANDARDS: Non-Discriminatory Metric Aggregation, Gamification Pedagogy, ASVS L2 Safe
AUDIENCE:  Student Engagement Architects, Gamification Designers & AI Agents
========================================================================================
"""

import math
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class StudentReputationService:
    """
    Holistic Student Growth Engine consolidating all learning, tutoring,
    and career achievements into an authoritative composite reputation score.
    """

    TIER_NOVICE_SCHOLAR = "NOVICE_SCHOLAR"
    TIER_ACADEMIC_EXPLORER = "ACADEMIC_EXPLORER"
    TIER_MASTER_MENTOR = "MASTER_MENTOR"
    TIER_EMINENCE_FELLOW = "EMINENCE_FELLOW"

    def __init__(self):
        # student_id -> dict of student metrics
        self._profiles: Dict[str, Dict[str, Any]] = {}
        # student_id -> list of quest dicts
        self._quests: Dict[str, List[Dict[str, Any]]] = {}
        self._seed_benchmark_profiles()

    def _seed_benchmark_profiles(self):
        """Pre-seeds demo student profile with multi-platform activities."""
        demo_id = "student_demo_01"
        self._profiles[demo_id] = {
            "student_id": demo_id,
            "cat_ability_theta": 2.15,
            "checkpoints_passed": 6,
            "tutor_rating": 4.95,
            "completed_tuition_sessions": 8,
            "verified_skills_count": 6,
            "sealed_cv_snapshots_count": 2,
            "ats_high_matches_count": 3,
            "tribunal_votes_cast": 3,
            "study_circle_notes_contributed": 4,
            "extra_bonus_points": 50
        }
        self._initialize_daily_quests(demo_id)

    def _initialize_daily_quests(self, student_id: str):
        """Generates standard daily growth quests for a student."""
        self._quests[student_id] = [
            {
                "quest_id": "quest_cp_01",
                "title": "Mastery Checkpoint",
                "description": "Pass 1 in-lecture checkpoint quiz on calculus or physics.",
                "pillar": "ACADEMIC",
                "target_count": 1,
                "current_count": 1,
                "reward_points": 25,
                "is_completed": True,
                "is_claimed": False
            },
            {
                "quest_id": "quest_sr_02",
                "title": "Spaced Recall Sprint",
                "description": "Review 5 spaced repetition flashcards from your mistake ledger.",
                "pillar": "ACADEMIC",
                "target_count": 5,
                "current_count": 5,
                "reward_points": 20,
                "is_completed": True,
                "is_claimed": False
            },
            {
                "quest_id": "quest_tuit_03",
                "title": "Tuition Match Scout",
                "description": "Browse 3 curated regional tuition openings in your district.",
                "pillar": "TUITION",
                "target_count": 3,
                "current_count": 3,
                "reward_points": 15,
                "is_completed": True,
                "is_claimed": False
            },
            {
                "quest_id": "quest_cv_04",
                "title": "Career CV Seal",
                "description": "Verify 1 technical or STEM skill and freeze an immutable CV snapshot.",
                "pillar": "CAREER",
                "target_count": 1,
                "current_count": 1,
                "reward_points": 30,
                "is_completed": True,
                "is_claimed": False
            }
        ]

    # ----------------------------------------------------------------------------------
    # TOPIC: 4-PILLAR REPUTATION COMPUTATION
    # ----------------------------------------------------------------------------------

    def calculate_reputation_score(self, student_id: str) -> Dict[str, Any]:
        """
        Calculates the 0-1000 Composite Reputation Score across the 4 pillars.
        Guarantees zero division by zero and safe score clamping.
        """
        clean_id = (student_id or "").strip()
        profile = self._profiles.get(clean_id, {
            "student_id": clean_id,
            "cat_ability_theta": 0.0,
            "checkpoints_passed": 0,
            "tutor_rating": 0.0,
            "completed_tuition_sessions": 0,
            "verified_skills_count": 0,
            "sealed_cv_snapshots_count": 0,
            "ats_high_matches_count": 0,
            "tribunal_votes_cast": 0,
            "study_circle_notes_contributed": 0,
            "extra_bonus_points": 0
        })

        # Pillar 1: Academic Mastery (Max 350 pts)
        # Baseline 150 + theta * 50 + checkpoints * 20
        theta = profile.get("cat_ability_theta", 0.0)
        checkpoints = profile.get("checkpoints_passed", 0)
        academic_raw = 150 + int(theta * 50) + (checkpoints * 20)
        academic_pts = max(0, min(academic_raw, 350))

        # Pillar 2: Tutoring Reliability (Max 250 pts)
        # Rating 0-5.0 gives up to 180 pts, sessions give 10 pts each
        rating = profile.get("tutor_rating", 0.0)
        sessions = profile.get("completed_tuition_sessions", 0)
        tutor_raw = int((rating / 5.0) * 180) + (sessions * 10)
        tutor_pts = max(0, min(tutor_raw, 250))

        # Pillar 3: Career Preparedness (Max 250 pts)
        skills = profile.get("verified_skills_count", 0)
        snapshots = profile.get("sealed_cv_snapshots_count", 0)
        ats_matches = profile.get("ats_high_matches_count", 0)
        career_raw = (skills * 25) + (snapshots * 35) + (ats_matches * 15)
        career_pts = max(0, min(career_raw, 250))

        # Pillar 4: Community Integrity (Max 150 pts)
        votes = profile.get("tribunal_votes_cast", 0)
        notes = profile.get("study_circle_notes_contributed", 0)
        integrity_raw = (votes * 25) + (notes * 20)
        integrity_pts = max(0, min(integrity_raw, 150))

        # Extra claimed quest bonuses
        bonus_pts = profile.get("extra_bonus_points", 0)

        composite_score = max(0, min(academic_pts + tutor_pts + career_pts + integrity_pts + bonus_pts, 1000))

        # Tier Resolution
        if composite_score >= 750:
            tier = self.TIER_EMINENCE_FELLOW
            tier_display = "Eminence Fellow"
            next_tier_progress = 100.0
        elif composite_score >= 500:
            tier = self.TIER_MASTER_MENTOR
            tier_display = "Master Mentor"
            next_tier_progress = round(((composite_score - 500) / 250) * 100.0, 1)
        elif composite_score >= 250:
            tier = self.TIER_ACADEMIC_EXPLORER
            tier_display = "Academic Explorer"
            next_tier_progress = round(((composite_score - 250) / 250) * 100.0, 1)
        else:
            tier = self.TIER_NOVICE_SCHOLAR
            tier_display = "Novice Scholar"
            next_tier_progress = round((composite_score / 250) * 100.0, 1)

        # Percentile approximation: Normal CDF over population mean 450, std 180
        z = (composite_score - 450) / 180.0
        percentile = round(0.5 * (1.0 + math.erf(z / math.sqrt(2.0))) * 100.0, 1)
        percentile = max(1.0, min(percentile, 99.9))

        return {
            "success": True,
            "student_id": student_id,
            "composite_score": composite_score,
            "tier": tier,
            "tier_display": tier_display,
            "percentile": percentile,
            "academic_mastery_points": academic_pts,
            "tutoring_reliability_points": tutor_pts,
            "career_preparedness_points": career_pts,
            "community_integrity_points": integrity_pts,
            "bonus_points": bonus_pts,
            "radar_breakdown": {
                "academic": round((academic_pts / 350.0) * 100.0, 1),
                "tutoring": round((tutor_pts / 250.0) * 100.0, 1),
                "career": round((career_pts / 250.0) * 100.0, 1),
                "integrity": round((integrity_pts / 150.0) * 100.0, 1)
            },
            "next_tier_progress_percent": next_tier_progress,
            "message": f"Reputation Score calculated: {composite_score}/1000 ({tier_display})."
        }

    # ----------------------------------------------------------------------------------
    # TOPIC: GAMIFIED DAILY QUESTS
    # ----------------------------------------------------------------------------------

    def get_daily_quests(self, student_id: str) -> Dict[str, Any]:
        """Retrieves active daily quests and claim status."""
        if student_id not in self._quests:
            self._initialize_daily_quests(student_id)

        quests = self._quests[student_id]
        claimed_pts = sum(q["reward_points"] for q in quests if q["is_claimed"])

        return {
            "success": True,
            "student_id": student_id,
            "quests": quests,
            "total_claimed_points_today": claimed_pts
        }

    def claim_quest_reward(self, student_id: str, quest_id: str) -> Dict[str, Any]:
        """
        Claims reward points for a completed quest and adds them to reputation bonus.
        """
        if student_id not in self._quests:
            self._initialize_daily_quests(student_id)

        quests = self._quests[student_id]
        quest = next((q for q in quests if q["quest_id"] == quest_id), None)
        if not quest:
            return {
                "success": False,
                "error_code": "QUEST_NOT_FOUND",
                "message": f"Quest '{quest_id}' not found."
            }

        if not quest["is_completed"]:
            return {
                "success": False,
                "error_code": "QUEST_NOT_COMPLETED",
                "message": f"Quest '{quest['title']}' has not been completed yet."
            }

        if quest["is_claimed"]:
            return {
                "success": False,
                "error_code": "QUEST_ALREADY_CLAIMED",
                "message": f"Quest reward of {quest['reward_points']} points has already been claimed."
            }

        quest["is_claimed"] = True
        profile = self._profiles.setdefault(student_id, {"student_id": student_id, "extra_bonus_points": 0})
        profile["extra_bonus_points"] = profile.get("extra_bonus_points", 0) + quest["reward_points"]

        # Recalculate new score
        new_score = self.calculate_reputation_score(student_id)

        return {
            "success": True,
            "quest_id": quest_id,
            "points_awarded": quest["reward_points"],
            "new_composite_score": new_score["composite_score"],
            "tier": new_score["tier_display"],
            "message": f"Claimed +{quest['reward_points']} reputation points for '{quest['title']}'!"
        }


# Singleton instance
student_reputation_service = StudentReputationService()
