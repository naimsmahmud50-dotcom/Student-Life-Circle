"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Dignified Academic Gamification & Verifiable Social Proof
TOPIC:     Anti-Burnout Capping, Empathetic Streak Recovery & Cryptographic Badges
FILE:      backend/app/services/gamification_service.py
PHASE:     Phase 102 - Dignified Gamification & Verifiable Social Proof
PURPOSE:   Drives mature academic gamification without toxic gaming mechanics.
           Enforces daily XP anti-burnout caps (500 XP / day), preserves streaks
           through empathetic freeze recovery drills, and generates verifiable
           cryptographic mastery badge hashes.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
"""

import hmac
import hashlib
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class GamificationService:
    """
    Dignified Academic Gamification and Social Proof Engine.
    Prioritizes mental well-being, healthy rest boundaries, and verifiable proof of mastery.
    """

    DAILY_XP_CAP = 500  # Strict daily cap to prevent addictive binge-studying and dopamine fatigue
    SECRET_KEY = b"ogrojatra-dignified-gamification-signature-2026"

    def __init__(self):
        # In-memory storage for user profiles, daily XP buckets, and badge ledgers
        self._users: Dict[str, Dict[str, Any]] = {}
        self._daily_xp: Dict[str, Dict[str, int]] = {}  # user_id -> { "YYYY-MM-DD": xp }
        self._badge_ledger: Dict[str, Dict[str, Any]] = {}
        self._init_seed_data()

    def _get_today_date_str(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def _init_seed_data(self):
        seed_user_id = "usr-me-student-01"
        self._users[seed_user_id] = {
            "user_id": seed_user_id,
            "current_streak": 24,
            "longest_streak": 42,
            "total_xp": 8450,
            "streak_shields": 2,
            "is_frozen": False,
            "requires_recovery": False,
            "last_active_day": self._get_today_date_str(),
            "earned_badges": []
        }
        self._daily_xp[seed_user_id] = {
            self._get_today_date_str(): 180
        }

        # Seed initial authentic badge
        badge = self.award_mastery_badge(
            user_id=seed_user_id,
            badge_id="badge-hsc-physics-mechanics-top3",
            title="HSC Physics Mechanics Mastery",
            skill_name="Classical Mechanics & Rotational Dynamics",
            percentile_rank=97.4,
            issuing_authority="National Curriculum & Olympiad Faculty"
        )
        self._users[seed_user_id]["earned_badges"].append(badge)

    def _ensure_user(self, user_id: str) -> Dict[str, Any]:
        if user_id not in self._users:
            self._users[user_id] = {
                "user_id": user_id,
                "current_streak": 1,
                "longest_streak": 1,
                "total_xp": 0,
                "streak_shields": 1,
                "is_frozen": False,
                "requires_recovery": False,
                "last_active_day": self._get_today_date_str(),
                "earned_badges": []
            }
        return self._users[user_id]

    def award_xp(self, user_id: str, amount: int, activity_type: str = "practice") -> Dict[str, Any]:
        """
        Awards learning points with anti-burnout daily capping (max 500 XP per calendar day).
        """
        self._ensure_user(user_id)
        today = self._get_today_date_str()
        user_daily = self._daily_xp.setdefault(user_id, {})
        current_today_xp = user_daily.get(today, 0)

        if current_today_xp >= self.DAILY_XP_CAP:
            return {
                "user_id": user_id,
                "awarded_xp": 0,
                "daily_capped": True,
                "total_today_xp": current_today_xp,
                "daily_cap_limit": self.DAILY_XP_CAP,
                "message": "Daily study point cap reached. Rest and reflection are essential for deep mastery."
            }

        # Calculate capped award
        eligible_xp = min(amount, self.DAILY_XP_CAP - current_today_xp)
        user_daily[today] = current_today_xp + eligible_xp
        self._users[user_id]["total_xp"] += eligible_xp
        self._users[user_id]["last_active_day"] = today

        return {
            "user_id": user_id,
            "awarded_xp": eligible_xp,
            "daily_capped": user_daily[today] >= self.DAILY_XP_CAP,
            "total_today_xp": user_daily[today],
            "daily_cap_limit": self.DAILY_XP_CAP,
            "activity_type": activity_type,
            "message": "Learning points awarded."
        }

    def get_streak_status(self, user_id: str) -> Dict[str, Any]:
        """Returns student streak metrics, active shields, and health state."""
        user = self._ensure_user(user_id)
        today = self._get_today_date_str()
        user_daily = self._daily_xp.setdefault(user_id, {})
        today_xp = user_daily.get(today, 0)

        return {
            "user_id": user_id,
            "current_streak": user["current_streak"],
            "longest_streak": user["longest_streak"],
            "streak_shields": user["streak_shields"],
            "is_frozen": user["is_frozen"],
            "requires_recovery": user["requires_recovery"],
            "last_active_day": user["last_active_day"],
            "today_xp": today_xp,
            "daily_cap": self.DAILY_XP_CAP,
            "is_daily_capped": today_xp >= self.DAILY_XP_CAP
        }

    def use_streak_shield(self, user_id: str) -> Dict[str, Any]:
        """Activates a Rest Day shield to protect the streak during unavoidable interruptions."""
        user = self._ensure_user(user_id)
        if user["streak_shields"] <= 0:
            return {
                "success": False,
                "message": "No streak shields available. Complete regular review drills to earn more shields.",
                "streak_shields": 0
            }

        user["streak_shields"] -= 1
        user["is_frozen"] = True
        return {
            "success": True,
            "message": "Streak shield activated. Your learning streak is protected for 24 hours.",
            "current_streak": user["current_streak"],
            "remaining_shields": user["streak_shields"]
        }

    def recover_streak_via_drill(self, user_id: str, drill_score: float) -> Dict[str, Any]:
        """
        Empathetic streak recovery: If a learner misses a day due to exams or illness,
        completing a review drill with >= 60% accuracy instantly restores their streak.
        """
        user = self._ensure_user(user_id)
        if drill_score < 60.0:
            return {
                "recovered": False,
                "message": "Review drill score must be at least 60% to restore streak.",
                "current_streak": user["current_streak"],
                "score_achieved": drill_score
            }

        user["requires_recovery"] = False
        user["is_frozen"] = False
        user["current_streak"] += 1
        if user["current_streak"] > user["longest_streak"]:
            user["longest_streak"] = user["current_streak"]

        # Award modest bonus XP subject to daily cap
        self.award_xp(user_id, 50, activity_type="streak_recovery_drill")

        return {
            "recovered": True,
            "message": "Learning streak empathetically restored! Rest is respected and progress continues.",
            "current_streak": user["current_streak"],
            "longest_streak": user["longest_streak"]
        }

    def award_mastery_badge(
        self,
        user_id: str,
        badge_id: str,
        title: str,
        skill_name: str,
        percentile_rank: float,
        issuing_authority: str = "National Curriculum & Olympiad Faculty"
    ) -> Dict[str, Any]:
        """
        Issues a cryptographically signed academic mastery badge with verifiable HMAC-SHA256 hash.
        """
        self._ensure_user(user_id)
        timestamp = int(time.time())
        raw_payload = f"{user_id}:{badge_id}:{percentile_rank:.2f}:{timestamp}"
        signature = hmac.new(self.SECRET_KEY, raw_payload.encode("utf-8"), hashlib.sha256).hexdigest()

        badge_record = {
            "badge_id": badge_id,
            "user_id": user_id,
            "title": title,
            "skill_name": skill_name,
            "percentile_rank": percentile_rank,
            "issuing_authority": issuing_authority,
            "verification_hash": signature,
            "qr_verification_url": f"https://ogrojatra.edu.bd/verify/badge/{signature[:16]}",
            "issued_at": timestamp
        }

        self._badge_ledger[signature] = badge_record
        if badge_record not in self._users[user_id]["earned_badges"]:
            self._users[user_id]["earned_badges"].append(badge_record)

        return badge_record

    def verify_badge(self, verification_hash: str) -> Optional[Dict[str, Any]]:
        """Verifies badge authenticity against the tamper-evident ledger."""
        return self._badge_ledger.get(verification_hash)

    def get_portfolio(self, user_id: str) -> Dict[str, Any]:
        """Returns full achievements portfolio including streak, badges, and milestones."""
        user = self._ensure_user(user_id)
        today = self._get_today_date_str()
        today_xp = self._daily_xp.get(user_id, {}).get(today, 0)

        return {
            "user_id": user_id,
            "streak": {
                "current_streak": user["current_streak"],
                "longest_streak": user["longest_streak"],
                "streak_shields": user["streak_shields"],
                "is_frozen": user["is_frozen"],
                "requires_recovery": user["requires_recovery"]
            },
            "xp_metrics": {
                "total_xp": user["total_xp"],
                "today_xp": today_xp,
                "daily_cap": self.DAILY_XP_CAP,
                "is_capped": today_xp >= self.DAILY_XP_CAP
            },
            "badges": user["earned_badges"],
            "milestones": [
                {
                    "id": "ms-01",
                    "title": "প্রথম ৫০টি নির্ভুল উত্তর",
                    "category": "Accuracy",
                    "completed": True,
                    "date": "2026-09-15"
                },
                {
                    "id": "ms-02",
                    "title": "২১ দিনের অবিচল অধ্যবসায়",
                    "category": "Consistency",
                    "completed": True,
                    "date": "2026-10-10"
                },
                {
                    "id": "ms-03",
                    "title": "ক্যালকুলাস ও কণিক্স দক্ষতা (Top 5%)",
                    "category": "Subject Mastery",
                    "completed": True,
                    "date": "2026-10-18"
                },
                {
                    "id": "ms-04",
                    "title": "জাতীয় লাইভ অলিম্পিয়াড সেমিফাইনালিস্ট",
                    "category": "Olympiad",
                    "completed": False,
                    "date": "Pending"
                }
            ]
        }


gamification_service = GamificationService()
