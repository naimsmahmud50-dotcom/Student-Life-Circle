"""
===================================================================================
Module: Cognitive Burnout Prevention & Mental Fatigue Engine
Topic: Mathematical Strain Accumulation, Sleep Deficit & Recharge Prescriptions
File: backend/app/services/burnout_prevention_service.py
Purpose: Evaluates continuous cognitive study strain, sleep deficits, and break
         intervals to compute a real-time Cognitive Fatigue Index (0.0 to 100.0),
         triggering proactive recovery interventions and minor-safe guardian alerts.
Audience: Developers, Educational Psychologists, QA Engineers, System Architects
Standards: Clean Architecture, OWASP ASVS Level 2, Full Type Hints, Zero-Emoji
===================================================================================
"""

from typing import Dict, Any, List, Optional
import math


class BurnoutPreventionService:
    """
    Cognitive Burnout Prevention & Mental Health Shield.
    Quantifies neural strain and mental fatigue from continuous study,
    sleep deficits, and break deprivation, prescribing personalized recharge protocols.
    """

    RECHARGE_PROTOCOLS = {
        "OPTIMAL_FLOW": [
            {"protocol": "স্বাভাবিক হাইড্রেটিং", "duration_min": 2, "description_bn": "এক গ্লাস বিশুদ্ধ পানি পান করুন এবং স্বাভাবিক গতি বজায় রাখুন।"}
        ],
        "MODERATE_STRAIN": [
            {"protocol": "২০-২০-২০ ভিজ্যুয়াল রুল", "duration_min": 5, "description_bn": "পড়ার বই বা স্ক্রিন থেকে চোখ সরিয়ে ২০ ফুট দূরের কোনো বস্তুর দিকে তাকিয়ে চোখের পেশি শিথিল করুন।"},
            {"protocol": "হালকা স্ট্রেচিং", "duration_min": 5, "description_bn": "ঘাড়, কাঁধ ও পিঠের জড়তা দূর করতে মৃদু স্ট্রেচিং অনুশীলন করুন।"}
        ],
        "HIGH_FATIGUE": [
            {"protocol": "নন-স্লিপ ডিপ রেস্ট (NSDR)", "duration_min": 15, "description_bn": "শান্ত পরিবেশে চোখ বন্ধ করে শুয়ে বা বসে গভীর শ্বাস-প্রশ্বাসের মাধ্যমে স্নায়বিক চাপ উপশম করুন।"},
            {"protocol": "পুষ্টিকর হালকা নাস্তা", "duration_min": 10, "description_bn": "মস্তিষ্কে গ্লুকোজ সরবরাহ নিশ্চিত করতে বাদাম, ফল বা দুধ গ্রহণ করুন।"}
        ],
        "BURNOUT_RISK": [
            {"protocol": "অবিলম্বে পড়াশোনা স্থগিতকরণ", "duration_min": 60, "description_bn": "মস্তিষ্ক অতিরিক্ত অবসাদগ্রস্ত। অন্তত ১ ঘণ্টার জন্য যেকোনো পড়াশোনা বা স্ক্রিন ব্যবহার সম্পূর্ণ বন্ধ রাখুন।"},
            {"protocol": "উন্মুক্ত বাতাসে হাঁটা", "duration_min": 20, "description_bn": "খোলা প্রাকৃতিক বাতাসে মৃদু পায়চারি করে মানসিক সতেজতা ফিরিয়ে আনুন।"}
        ]
    }

    def __init__(self):
        self._fatigue_history: Dict[str, List[Dict[str, Any]]] = {}
        self._guardian_alerts: List[Dict[str, Any]] = []

    def reset_for_testing(self) -> None:
        """Resets in-memory fatigue logs and alerts for testing."""
        self._fatigue_history.clear()
        self._guardian_alerts.clear()

    def evaluate_cognitive_fatigue(
        self,
        student_id: str,
        continuous_study_hours: float,
        sleep_hours_last_night: float = 7.5,
        total_study_hours_today: float = 4.0,
        break_minutes_today: float = 30.0,
        is_minor: bool = True
    ) -> Dict[str, Any]:
        """
        Computes the Cognitive Fatigue Index (0.0 to 100.0) based on mathematical
        accumulation of strain, sleep deficit, and interval breaks.
        """
        # Defensive parameter clamping
        safe_cont = max(0.0, min(18.0, float(continuous_study_hours)))
        safe_sleep = max(0.0, min(16.0, float(sleep_hours_last_night)))
        safe_total = max(safe_cont, min(20.0, float(total_study_hours_today)))
        safe_breaks = max(0.0, min(360.0, float(break_minutes_today)))

        # 1. Base study load: up to 55 points from cumulative day hours
        base_load = min(55.0, safe_total * 5.5)

        # 2. Continuous study penalty (escalates superlinearly beyond 2 hours)
        if safe_cont > 2.0:
            cont_penalty = math.pow(safe_cont - 2.0, 1.35) * 8.5
        else:
            cont_penalty = 0.0

        # 3. Sleep Deficit Penalty (Standard need: 7.5 hours)
        sleep_deficit = max(0.0, 7.5 - safe_sleep)
        sleep_penalty = sleep_deficit * 6.8

        # 4. Break relief deduction (Every 10 min break relieves ~2.5 fatigue points)
        break_relief = min(25.0, safe_breaks * 0.25)

        # Composite Fatigue Index Calculation
        raw_fatigue = base_load + cont_penalty + sleep_penalty - break_relief
        fatigue_index = round(max(5.0, min(100.0, raw_fatigue)), 1)

        # Classify Fatigue Tier
        if fatigue_index <= 30.0:
            tier = "OPTIMAL_FLOW"
            tier_label_bn = "সর্বোচ্চ মনন ও স্বাভাবিক কার্যকারিতা"
            badge_color = "emerald"
            cognitive_capacity_retention_pct = 98.0
        elif fatigue_index <= 60.0:
            tier = "MODERATE_STRAIN"
            tier_label_bn = "সহনশীল মানসিক চাপ (সাধারণ বিরতি কাম্য)"
            badge_color = "amber"
            cognitive_capacity_retention_pct = 85.0
        elif fatigue_index <= 80.0:
            tier = "HIGH_FATIGUE"
            tier_label_bn = "উচ্চ মানসিক ক্লান্তি (ধারণক্ষমতা হ্রাস পাচ্ছে)"
            badge_color = "orange"
            cognitive_capacity_retention_pct = 68.0
        else:
            tier = "BURNOUT_RISK"
            tier_label_bn = "তীব্র অবসাদ সতর্কতা (পড়াশোনা স্থগিত করা আবশ্যক)"
            badge_color = "rose"
            cognitive_capacity_retention_pct = 45.0

        prescriptions = self.RECHARGE_PROTOCOLS.get(tier, self.RECHARGE_PROTOCOLS["MODERATE_STRAIN"])

        # Guardian Safety Care Alert (OWASP ASVS Minor Safeguard)
        guardian_alert_sent = False
        guardian_message = None
        if is_minor and tier == "BURNOUT_RISK":
            guardian_alert_sent = True
            guardian_message = "অভিভাবকের প্রতি বার্তা: শিক্ষার্থী আজ দীর্ঘ সময় একটানা পড়াশোনা করায় মানসিক অবসাদের লক্ষণ দেখা যাচ্ছে। তাকে একটু বিশ্রাম ও পুষ্টিকর হালকা খাবার গ্রহণের পরামর্শ দিন।"
            if not any(a["student_id"] == student_id for a in self._guardian_alerts):
                self._guardian_alerts.append({
                    "student_id": student_id,
                    "fatigue_index": fatigue_index,
                    "message": guardian_message
                })

        result = {
            "success": True,
            "student_id": student_id,
            "fatigue_index": fatigue_index,
            "fatigue_tier": tier,
            "fatigue_tier_label_bn": tier_label_bn,
            "badge_color": badge_color,
            "cognitive_capacity_retention_pct": cognitive_capacity_retention_pct,
            "inputs_analyzed": {
                "continuous_study_hours": safe_cont,
                "sleep_hours": safe_sleep,
                "total_study_hours_today": safe_total,
                "break_minutes": safe_breaks
            },
            "strain_breakdown": {
                "base_study_load": round(base_load, 1),
                "continuous_strain_penalty": round(cont_penalty, 1),
                "sleep_deficit_penalty": round(sleep_penalty, 1),
                "break_relief_deduction": round(break_relief, 1)
            },
            "recharge_prescriptions": prescriptions,
            "guardian_safety_alert": {
                "alert_triggered": guardian_alert_sent,
                "guardian_advisory_bn": guardian_message
            }
        }

        # Store in student history
        if student_id not in self._fatigue_history:
            self._fatigue_history[student_id] = []
        self._fatigue_history[student_id].append(result)

        return result

    def get_student_burnout_status(self, student_id: str) -> Dict[str, Any]:
        """Returns the latest evaluated burnout status for a student."""
        history = self._fatigue_history.get(student_id, [])
        if not history:
            # Default baseline
            return self.evaluate_cognitive_fatigue(
                student_id=student_id,
                continuous_study_hours=1.5,
                sleep_hours_last_night=7.5,
                total_study_hours_today=3.0,
                break_minutes_today=25.0
            )
        return history[-1]


# Global singleton instance
burnout_prevention_service = BurnoutPreventionService()
