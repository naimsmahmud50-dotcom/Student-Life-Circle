"""
========================================================================================
MODULE:    Diagnostic Gap Analysis & Personalized Sprint Service
TOPIC:     Topic Deficiency Diagnosis, Mastery Categorization & 7-Day Sprint Planner
FILE:      backend/app/services/diagnostic_service.py
PURPOSE:   Analyzes admission diagnostic mock tests across Physics, Chemistry, Math,
           and Biology. Maps topic error rates into three distinct categories:
           STRONG, NEEDS_REVISION, and CRITICAL_GAP. Formulates an achievable 7-day
           study sprint without deceptive "guaranteed admission" promises.
AUDIENCE:  Learning Analytics Specialists, Candidates & AI Agents
STANDARDS: Psychometric Transparency, Spaced Repetition, Anti-Deception Policy
========================================================================================
"""

from typing import Dict, List, Any


class DiagnosticService:
    """
    Evaluates topic competencies and structures targeted revision sprints.
    """

    @staticmethod
    def analyze_diagnostic_results(
        topic_performance: List[Dict[str, Any]]  # [{ "topic_name": "...", "correct": 2, "total": 5 }]
    ) -> Dict[str, Any]:
        """
        Classifies performance:
        >= 80% : STRONG (মজবুত ধারণা)
        50-79% : NEEDS_REVISION (রিভিশন প্রয়োজন)
        < 50%  : CRITICAL_GAP (জরুরি দুর্বলতা)
        """
        strong_topics = []
        revision_topics = []
        critical_gaps = []

        for item in topic_performance:
            total = item.get("total", 0)
            correct = item.get("correct", 0)
            topic_name = item.get("topic_name", "Unknown Topic")
            subject = item.get("subject", "General")

            if total <= 0:
                continue

            accuracy = (correct / total) * 100.0

            summary_item = {
                "topic_name": topic_name,
                "subject": subject,
                "accuracy_percent": round(accuracy, 1),
                "attempted": total,
                "correct": correct
            }

            if accuracy >= 80.0:
                strong_topics.append(summary_item)
            elif accuracy >= 50.0:
                revision_topics.append(summary_item)
            else:
                critical_gaps.append(summary_item)

        # Generate targeted 7-Day Sprint Plan recommendations
        sprint_recommendations = []
        for gap in critical_gaps[:3]:
            sprint_recommendations.append(
                f"দিন ১-৩: {gap['subject']} - '{gap['topic_name']}' ধারণার এনসিটিবি পাঠ্যবই ও মূল সূত্র রিভিশন।"
            )
        for rev in revision_topics[:2]:
            sprint_recommendations.append(
                f"দিন ৪-৫: {rev['subject']} - '{rev['topic_name']}' থেকে ২০টি প্র্যাকটিস MCQ সমাধান।"
            )
        sprint_recommendations.append("দিন ৬-৭: সম্পূর্ণ ক-ইউনিট ফুল-লেংথ টাইমড রিভিশন মক টেস্ট।")

        return {
            "status": "COMPLETED",
            "strong_count": len(strong_topics),
            "revision_count": len(revision_topics),
            "critical_gap_count": len(critical_gaps),
            "strong_topics": strong_topics,
            "revision_topics": revision_topics,
            "critical_gaps": critical_gaps,
            "seven_day_sprint_plan": sprint_recommendations,
            "disclaimer": "এই ফলাফল আপনার বর্তমান প্রস্তুতির ঘাটতি নির্দেশ করে; কোনো প্রকার ভর্তি নিশ্চয়তা দাবি করে না।"
        }


# Singleton Service Instance
diagnostic_service = DiagnosticService()
