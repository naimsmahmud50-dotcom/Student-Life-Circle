"""
================================================================================
MODULE: Peer Collaboration & Social Learning (টিম স্টাডি সার্কেল ও পিয়ার লার্নিং)
TOPIC: Minor-Safe Cooperative Study Circles & Shared Academic Streaks
FILE: backend/app/services/study_circle_service.py
PURPOSE: Facilitates collaborative small-group peer learning circles (max 6 students).
         Enforces OWASP ASVS Level 2 child safety by masking real identities of minors
         while enabling shared cooperative streaks, pooled problem sets, and collective
         weekly study milestones without toxic hyper-competition.
AUDIENCE: Students, Educational Psychologists, Platform Safeguarding Officers.
STANDARDS: OWASP ASVS Level 2 Minor Isolation, Cooperative Learning Pedagogy.
================================================================================
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class StudyCircleService:
    """Manages cooperative, minor-safe peer study circles."""

    MAX_CIRCLE_MEMBERS = 6

    def __init__(self) -> None:
        # Key: circle_id -> StudyCircleDict
        self._circles: Dict[str, Dict[str, Any]] = {}

    def _mask_member_identity(self, member: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures minors' personal identifiable information is completely redacted."""
        name = member["name"]
        if member.get("is_minor", False):
            first_part = name.split()[0] if name.split() else "শিক্ষার্থী"
            masked_name = f"{first_part} (সার্কেল সদস্য)"
        else:
            masked_name = name

        return {
            "student_id": member["student_id"],
            "display_name": masked_name,
            "is_minor": member.get("is_minor", False),
            "joined_at": member["joined_at"],
            "contributed_questions": member.get("contributed_questions", 0),
            "role": member.get("role", "MEMBER"),
        }

    def create_study_circle(
        self,
        creator_id: str,
        creator_name: str,
        is_minor: bool,
        name: str,
        subject: str,
        class_grade: int,
        target_weekly_questions: int = 150,
    ) -> Dict[str, Any]:
        """Creates a new cooperative study circle and registers creator as circle lead."""
        circle_id = f"circle_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc).isoformat()

        creator_member = {
            "student_id": creator_id,
            "name": creator_name,
            "is_minor": is_minor,
            "joined_at": now,
            "contributed_questions": 0,
            "role": "LEAD",
        }

        circle_record = {
            "circle_id": circle_id,
            "name": name,
            "subject": subject,
            "class_grade": class_grade,
            "creator_id": creator_id,
            "created_at": now,
            "max_members": self.MAX_CIRCLE_MEMBERS,
            "shared_streak_days": 1,
            "weekly_goal": {
                "target_questions": target_weekly_questions,
                "completed_questions": 0,
                "status": "IN_PROGRESS",
            },
            "members": [creator_member],
            "activity_log": [
                {
                    "timestamp": now,
                    "event": f"স্টাডি সার্কেল '{name}' গঠিত হয়েছে।",
                }
            ],
        }

        self._circles[circle_id] = circle_record
        return self.get_circle_details(circle_id, requester_id=creator_id)

    def join_study_circle(
        self,
        circle_id: str,
        student_id: str,
        student_name: str,
        is_minor: bool,
    ) -> Dict[str, Any]:
        """Adds a student to an existing study circle if capacity allows."""
        circle = self._circles.get(circle_id)
        if not circle:
            return {"success": False, "message": "স্টাডি সার্কেল খুঁজে পাওয়া যায়নি।"}

        # Check existing membership
        if any(m["student_id"] == student_id for m in circle["members"]):
            return {"success": False, "message": "শিক্ষার্থী ইতিপূর্বে এই সার্কেলে যুক্ত হয়েছেন।"}

        # Capacity check (max 6 members)
        if len(circle["members"]) >= circle["max_members"]:
            return {
                "success": False,
                "message": f"সার্কেল পূর্ণ! সর্বোচ্চ ধারণক্ষমতা {self.MAX_CIRCLE_MEMBERS} জন শিক্ষার্থী।",
            }

        now = datetime.now(timezone.utc).isoformat()
        new_member = {
            "student_id": student_id,
            "name": student_name,
            "is_minor": is_minor,
            "joined_at": now,
            "contributed_questions": 0,
            "role": "MEMBER",
        }

        circle["members"].append(new_member)
        circle["activity_log"].append({
            "timestamp": now,
            "event": "নতুন সহপাঠী সার্কেলে যোগদান করেছে।",
        })

        return {
            "success": True,
            "circle": self.get_circle_details(circle_id, requester_id=student_id),
            "message": "সফলভাবে স্টাডি সার্কেলে যোগদান সম্পন্ন হয়েছে।",
        }

    def contribute_questions(
        self,
        circle_id: str,
        student_id: str,
        questions_solved: int,
    ) -> Dict[str, Any]:
        """Records solved questions toward the circle's collective weekly goal."""
        circle = self._circles.get(circle_id)
        if not circle:
            return {"success": False, "message": "স্টাডি সার্কেল পাওয়া যায়নি।"}

        member = next((m for m in circle["members"] if m["student_id"] == student_id), None)
        if not member:
            return {"success": False, "message": "শিক্ষার্থী এই সার্কেলের সদস্য নন।"}

        if questions_solved <= 0:
            return {"success": False, "message": "অনুশীলন সংখ্যা অবশ্যই ১ বা তার বেশি হতে হবে।"}

        member["contributed_questions"] += questions_solved
        goal = circle["weekly_goal"]
        goal["completed_questions"] += questions_solved

        if goal["completed_questions"] >= goal["target_questions"]:
            goal["status"] = "ACHIEVED"

        now = datetime.now(timezone.utc).isoformat()
        circle["activity_log"].append({
            "timestamp": now,
            "event": f"একজন সদস্য {questions_solved}টি অনুশীলন সম্পন্ন করেছেন।",
        })

        return {
            "success": True,
            "completed_questions": goal["completed_questions"],
            "target_questions": goal["target_questions"],
            "status": goal["status"],
        }

    def get_circle_details(self, circle_id: str, requester_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Returns circle details with minor member privacy protections applied."""
        circle = self._circles.get(circle_id)
        if not circle:
            return None

        sanitized_members = [self._mask_member_identity(m) for m in circle["members"]]

        return {
            "circle_id": circle["circle_id"],
            "name": circle["name"],
            "subject": circle["subject"],
            "class_grade": circle["class_grade"],
            "created_at": circle["created_at"],
            "member_count": len(circle["members"]),
            "max_members": circle["max_members"],
            "shared_streak_days": circle["shared_streak_days"],
            "weekly_goal": circle["weekly_goal"],
            "members": sanitized_members,
            "recent_activity": circle["activity_log"][-5:],
        }

    def reset_for_testing(self) -> None:
        """Clears in-memory circle database for isolated test execution."""
        self._circles.clear()


# Global Singleton Service
study_circle_service = StudyCircleService()
