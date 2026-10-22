"""
================================================================================
MODULE: Curriculum Assessment & Exam Design (কারিকুলাম অ্যাসেসমেন্ট ও ব্লুপ্রিন্ট কম্পোজার)
TOPIC: Automated Board Exam Blueprint Composer & Bloom's Cognitive Balancer
FILE: backend/app/services/blueprint_composer_service.py
PURPOSE: Automatically generates and validates rigorous exam blueprints adhering to
         NCTB, SSC, HSC, and University Admission specifications. Balances Bloom's
         Taxonomy cognitive levels (Knowledge, Comprehension, Application, Higher Order),
         enforces chapter weightings, and verifies negative marking constraints.
AUDIENCE: Curriculum Specialists, Head Examiners, Assessment Directors.
STANDARDS: NCTB Creative Question Assessment Framework, Bloom's Revised Taxonomy.
================================================================================
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class BlueprintComposerService:
    """Composes and validates academically balanced exam blueprints."""

    PRESET_BLUEPRINTS: Dict[str, Dict[str, Any]] = {
        "nctb_class8_math": {
            "blueprint_id": "nctb_class8_math",
            "name": "এনসিটিবি অষ্টম শ্রেণি গণিত চূড়ান্ত মডেল টেস্ট",
            "subject": "সাধারণ গণিত",
            "class_grade": 8,
            "total_questions": 25,
            "duration_minutes": 25,
            "negative_marking": 0.0,
            "cognitive_distribution": {
                "knowledge": 30.0,        # জ্ঞানমূলক (৩০%)
                "comprehension": 40.0,    # অনুধাবনমূলক (৪০%)
                "application": 20.0,      # প্রয়োগমূলক (২০%)
                "higher_order": 10.0,     # উচ্চতর দক্ষতা (১০%)
            },
            "chapter_distribution": {
                "প্যাটার্ন ও সংখ্যা": 20.0,
                "মুনাফা ও শতকরা": 25.0,
                "বীজগণিতীয় সূত্রাবলী": 30.0,
                "জ্যামিতি ও পিথাগোরাস": 25.0,
            },
        },
        "du_admission_ka_physics": {
            "blueprint_id": "du_admission_ka_physics",
            "name": "ঢাকা বিশ্ববিদ্যালয় 'ক' ইউনিট পদার্থবিজ্ঞান ভর্তি মক",
            "subject": "পদার্থবিজ্ঞান",
            "class_grade": 12,
            "total_questions": 15,
            "duration_minutes": 15,
            "negative_marking": 0.25,
            "cognitive_distribution": {
                "knowledge": 15.0,
                "comprehension": 35.0,
                "application": 35.0,
                "higher_order": 15.0,
            },
            "chapter_distribution": {
                "ভেক্টর": 20.0,
                "গতিবিদ্যা ও নিউটনিয়ান বলবিদ্যা": 30.0,
                "কাজ, শক্তি ও ক্ষমতা": 25.0,
                "পদার্থের গাঠনিক ধর্ম": 25.0,
            },
        },
    }

    def __init__(self) -> None:
        # Custom generated blueprints: blueprint_id -> BlueprintDict
        self._custom_blueprints: Dict[str, Dict[str, Any]] = {}

    def compose_blueprint(
        self,
        name: str,
        subject: str,
        class_grade: int,
        total_questions: int,
        duration_minutes: int,
        cognitive_distribution: Dict[str, float],
        chapter_distribution: Dict[str, float],
        negative_marking: float = 0.0,
    ) -> Dict[str, Any]:
        """Composes and validates a new curriculum-aligned exam blueprint."""
        # Validate total questions
        if total_questions < 5 or total_questions > 100:
            return {
                "success": False,
                "message": "মোট প্রশ্ন সংখ্যা অবশ্যই ৫ থেকে ১০০ এর মধ্যে হতে হবে।",
            }

        # Validate duration
        if duration_minutes < 5:
            return {
                "success": False,
                "message": "পরীক্ষার সময়কাল অবশ্যই কমপক্ষে ৫ মিনিট হতে হবে।",
            }

        # Validate negative marking
        if negative_marking < 0.0 or negative_marking > 1.0:
            return {
                "success": False,
                "message": "নেগেটিভ মার্কিং মান ০.০ থেকে ১.০ এর মধ্যে হতে হবে।",
            }

        # Validate Non-Negative Percentages
        if any(v < 0.0 for v in cognitive_distribution.values()) or any(v < 0.0 for v in chapter_distribution.values()):
            return {
                "success": False,
                "message": "কোনো শতকরা হার ঋণাত্মক হতে পারবে না।",
            }

        # Validate Cognitive Distribution Sum (must equal ~100%)
        cog_sum = sum(cognitive_distribution.values())
        if abs(cog_sum - 100.0) > 1.0:
            return {
                "success": False,
                "message": f"জ্ঞানীয় স্তরের মোট হার ১০০% হতে হবে (বর্তমান যোগফল: {cog_sum}%)।",
            }

        # Validate Chapter Distribution Sum (must equal ~100%)
        chap_sum = sum(chapter_distribution.values())
        if abs(chap_sum - 100.0) > 1.0:
            return {
                "success": False,
                "message": f"অধ্যায়সমূহের মোট হার ১০০% হতে হবে (বর্তমান যোগফল: {chap_sum}%)।",
            }

        blueprint_id = f"bp_custom_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc).isoformat()

        # Calculate exact item allocations
        item_allocation_by_cognition: Dict[str, int] = {}
        for cog_level, pct in cognitive_distribution.items():
            count = max(1, round((pct / 100.0) * total_questions))
            item_allocation_by_cognition[cog_level] = count

        # Adjust any rounding discrepancies to match total_questions exactly
        allocated_total = sum(item_allocation_by_cognition.values())
        diff = total_questions - allocated_total
        if diff != 0:
            # Adjust the largest cognitive level
            largest_level = max(item_allocation_by_cognition.items(), key=lambda x: x[1])[0]
            item_allocation_by_cognition[largest_level] += diff

        blueprint_record = {
            "blueprint_id": blueprint_id,
            "name": name,
            "subject": subject,
            "class_grade": class_grade,
            "total_questions": total_questions,
            "duration_minutes": duration_minutes,
            "negative_marking": negative_marking,
            "cognitive_distribution": cognitive_distribution,
            "chapter_distribution": chapter_distribution,
            "exact_item_allocation": item_allocation_by_cognition,
            "created_at": now,
            "validation_status": "APPROVED_BALANCED",
            "pedagogical_notes": [
                f"মোট প্রশ্ন: {total_questions}টি, সময়: {duration_minutes} মিনিট।",
                f"জ্ঞানমূলক: {item_allocation_by_cognition.get('knowledge', 0)}টি, অনুধাবনমূলক: {item_allocation_by_cognition.get('comprehension', 0)}টি।",
                f"প্রয়োগমূলক: {item_allocation_by_cognition.get('application', 0)}টি, উচ্চতর দক্ষতা: {item_allocation_by_cognition.get('higher_order', 0)}টি।",
                f"নেগেটিভ মার্কিং: প্রতি ভুল উত্তরে -{negative_marking} কর্তন প্রযোজ্য।" if negative_marking > 0 else "নেগেটিভ মার্কিং নেই।",
            ],
        }

        self._custom_blueprints[blueprint_id] = blueprint_record
        return {
            "success": True,
            "blueprint": blueprint_record,
            "message": "ব্লুপ্রিন্ট সফলভাবে প্রস্তুত ও অনুমোদিত হয়েছে।",
        }

    def get_blueprint(self, blueprint_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves preset or custom generated blueprint by ID."""
        if blueprint_id in self.PRESET_BLUEPRINTS:
            return self.PRESET_BLUEPRINTS[blueprint_id]
        return self._custom_blueprints.get(blueprint_id)

    def list_presets(self) -> List[Dict[str, Any]]:
        """Returns all pre-configured official curriculum blueprints."""
        return list(self.PRESET_BLUEPRINTS.values())

    def reset_for_testing(self) -> None:
        """Clears custom blueprints for test isolation."""
        self._custom_blueprints.clear()


# Global Singleton Service
blueprint_composer_service = BlueprintComposerService()
