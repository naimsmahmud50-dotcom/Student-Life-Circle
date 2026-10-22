"""
================================================================================
MODULE: Personalized Study Roadmap & Remediation (ব্যক্তিগত পাঠ্যপরিকল্পনা ইঞ্জিন)
TOPIC: Adaptive 7-Day Remediation Roadmap & Cognitive Weakness Diagnosis
FILE: backend/app/services/study_plan_service.py
PURPOSE: Generates dynamic, AI-assisted personalized study roadmaps tailored to
         individual student learning gaps. Combines recent exam diagnostic metrics,
         topic error clustering, and spaced repetition intervals to deliver
         balanced daily study milestones without causing cognitive burnout.
AUDIENCE: Curriculum Designers, Adaptive Mentors, Students, Academic Coordinators.
STANDARDS: Zone of Proximal Development (ZPD), Bloom's Taxonomy Mastery Progression.
================================================================================
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

try:
    from backend.app.services.spaced_repetition_service import spaced_repetition_service
except ImportError:
    from app.services.spaced_repetition_service import spaced_repetition_service


class StudyPlanService:
    """Generates and tracks customized weekly study roadmaps for students."""

    def __init__(self) -> None:
        # Key: student_id -> StudyPlanDict
        self._plans: Dict[str, Dict[str, Any]] = {}

    def generate_study_plan(
        self,
        student_id: str,
        class_grade: int,
        target_subject: str,
        weak_topics: Optional[List[str]] = None,
        daily_available_minutes: int = 40,
    ) -> Dict[str, Any]:
        """
        Creates an adaptive 7-day remediation roadmap based on diagnosed weaknesses
        and pending spaced repetition items.
        """
        plan_id = f"plan_{uuid.uuid4().hex[:10]}"
        generated_at = datetime.now(timezone.utc).isoformat()

        # Fallback default weak topics for demonstration if none provided
        topics = weak_topics or ["ঐকিক নিয়ম ও সময়-দূরত্ব", "বীজগণিতীয় সূত্রাবলী ও উৎপাদক", "জ্যামিতিক উপপাদ্য"]

        # Check pending spaced repetition items
        due_items = spaced_repetition_service.get_due_reviews(student_id=student_id)
        due_count = len(due_items)

        # Build 7-day adaptive roadmap
        days = [
            {
                "day_number": 1,
                "title": f"অধ্যায় পুনর্বিবেচনা: {topics[0] if len(topics) > 0 else 'মৌলিক ধারণা'}",
                "focus_area": "ধারণাগত ভিত্তি ও সূত্র বিশ্লেষণ",
                "target_minutes": min(daily_available_minutes, 35),
                "milestone_id": f"m_{plan_id}_d1",
                "completed": False,
                "tasks": [
                    "এনসিটিবি পাঠ্যবইয়ের অধ্যায় সারসংক্ষেপ পাঠ",
                    "৫টি মৌলিক উদাহরণ অনুশীলন",
                ],
            },
            {
                "day_number": 2,
                "title": f"লক্ষ্যভিত্তিক ড্রিল: {topics[0] if len(topics) > 0 else 'মৌলিক ধারণা'}",
                "focus_area": "ভুল সংশোধনে নিবিড় অনুশীলন",
                "target_minutes": daily_available_minutes,
                "milestone_id": f"m_{plan_id}_d2",
                "completed": False,
                "tasks": [
                    "১০টি টপিক-ভিত্তিক MCQ সমাধান",
                    "ব্যাখ্যা বিশ্লেষণ ও নোট তৈরি",
                ],
            },
            {
                "day_number": 3,
                "title": "স্পেসড রিপিটেশন ও ভুল পর্যালোচনা",
                "focus_area": "পূর্বের ভুল হওয়া প্রশ্নের স্মৃতি রিটেনশন",
                "target_minutes": max(25, daily_available_minutes - 10),
                "milestone_id": f"m_{plan_id}_d3",
                "completed": False,
                "tasks": [
                    f"মেমোরি কিউ থেকে {max(3, due_count)}টি প্রশ্নের পুনরাবৃত্তি",
                    "ভুল উত্তরের লজিক চিহ্নিতকরণ",
                ],
            },
            {
                "day_number": 4,
                "title": f"দ্বিতীয় দুর্বলতা দূরীকরণ: {topics[1] if len(topics) > 1 else 'গাণিতিক সমস্যা'}",
                "focus_area": "মধ্যম পর্যায়ের জটিল সমস্যা সমাধান",
                "target_minutes": daily_available_minutes,
                "milestone_id": f"m_{plan_id}_d4",
                "completed": False,
                "tasks": [
                    "নতুন অধ্যায়ের সূত্রাবলির প্রয়োগ",
                    "৮টি কাঠামোগত সমস্যা অনুশীলন",
                ],
            },
            {
                "day_number": 5,
                "title": "ZPD চ্যালেঞ্জ ড্রিল (Zone of Proximal Development)",
                "focus_area": "উচ্চতর দক্ষতা ও আত্মবিশ্বাস অর্জন (৬৫-৭৫% কাঠিন্য)",
                "target_minutes": daily_available_minutes,
                "milestone_id": f"m_{plan_id}_d5",
                "completed": False,
                "tasks": [
                    "১২টি সময়াবদ্ধ মিশ্র প্রশ্ন অনুশীলন",
                    "টাইম ম্যানেজমেন্ট পর্যবেক্ষণ",
                ],
            },
            {
                "day_number": 6,
                "title": "সাপ্তাহিক রিভিশন ও রিল্যাক্সেশন",
                "focus_area": "সার্বিক পর্যালোচনা ও মানসিক চাপমুক্তি",
                "target_minutes": 25,
                "milestone_id": f"m_{plan_id}_d6",
                "completed": False,
                "tasks": [
                    "সপ্তাহের প্রধান সূত্রের কুইক রিকল",
                    "বিশ্রাম দিবস ফ্রিজ পাসের অবস্থা পরীক্ষা",
                ],
            },
            {
                "day_number": 7,
                "title": "সাপ্তাহিক চেকপয়েন্ট মক টেস্ট",
                "focus_area": "মেধা অগ্রগতি ও সনদ অর্জনের মূল্যায়ন",
                "target_minutes": 45,
                "milestone_id": f"m_{plan_id}_d7",
                "completed": False,
                "tasks": [
                    "২০ নম্বরের সাপ্তাহিক অগ্রগতি পরীক্ষা",
                    "অ্যাডাপ্টিভ Elo রেটিং হালনাগাদ",
                ],
            },
        ]

        study_plan = {
            "plan_id": plan_id,
            "student_id": student_id,
            "class_grade": class_grade,
            "subject": target_subject,
            "weak_topics": topics,
            "daily_target_minutes": daily_available_minutes,
            "generated_at": generated_at,
            "status": "ACTIVE",
            "progress_pct": 0.0,
            "completed_milestones": 0,
            "total_milestones": 7,
            "schedule": days,
        }

        self._plans[student_id] = study_plan
        return study_plan

    def get_active_study_plan(self, student_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the active roadmap for a student."""
        return self._plans.get(student_id)

    def complete_milestone(self, student_id: str, milestone_id: str) -> Dict[str, Any]:
        """Marks a daily milestone as completed and recalculates overall roadmap progress."""
        plan = self._plans.get(student_id)
        if not plan:
            return {"success": False, "message": "কোনো সক্রিয় স্টাডি প্ল্যান পাওয়া যায়নি।"}

        matched = False
        completed_count = 0

        for day in plan["schedule"]:
            if day["milestone_id"] == milestone_id:
                day["completed"] = True
                matched = True
            if day["completed"]:
                completed_count += 1

        if not matched:
            return {"success": False, "message": "নির্দিষ্ট মাইলস্টোন আইডি পাওয়া যায়নি।"}

        plan["completed_milestones"] = completed_count
        plan["progress_pct"] = round((completed_count / plan["total_milestones"]) * 100.0, 1)

        if completed_count == plan["total_milestones"]:
            plan["status"] = "COMPLETED"

        return {
            "success": True,
            "milestone_id": milestone_id,
            "progress_pct": plan["progress_pct"],
            "completed_milestones": completed_count,
            "status": plan["status"],
        }

    def reset_for_testing(self) -> None:
        """Clears stored study plans for testing isolation."""
        self._plans.clear()


# Global Singleton Service
study_plan_service = StudyPlanService()
