"""
===================================================================================
Module: Predictive Analytics & Forecasting Engine
Topic: Bayesian Latent Ability to CGPA & National Rank Estimation
File: backend/app/services/predictive_analytics_service.py
Purpose: Translates latent proficiency, historical performance, and consistency metrics
         into probabilistic CGPA forecasts with 95% confidence intervals, Golden A+
         likelihood, and national rank distributions over a 1.3M student cohort.
Audience: Developers, Academic Counselors, QA Engineers, System Architects
Standards: Clean Architecture, OWASP ASVS Level 2, Full Type Hints, Zero-Emoji
===================================================================================
"""

from typing import Dict, Any, List, Optional
import math


class PredictiveAnalyticsService:
    """
    Bayesian Predictive Academic Analytics Service.
    Projects expected board CGPA (0.00 to 5.00), Golden A+ odds,
    National Percentiles, and estimated merit ranks against national benchmarks.
    """

    # National Board Cohort Demographics (Benchmark: Bangladesh HSC / SSC Cohorts)
    NATIONAL_COHORTS: Dict[str, Dict[str, float]] = {
        "HSC_SCIENCE": {
            "cohort_size": 1300000.0,
            "mean_score": 58.5,
            "std_dev": 14.5,
            "golden_a_plus_benchmark": 80.0,
            "label_bn": "এইচএসসি বিজ্ঞান বিভাগ"
        },
        "HSC_COMMERCE": {
            "cohort_size": 1100000.0,
            "mean_score": 55.0,
            "std_dev": 13.8,
            "golden_a_plus_benchmark": 80.0,
            "label_bn": "এইচএসসি ব্যবসায় শিক্ষা"
        },
        "HSC_HUMANITIES": {
            "cohort_size": 1250000.0,
            "mean_score": 53.2,
            "std_dev": 13.2,
            "golden_a_plus_benchmark": 80.0,
            "label_bn": "এইচএসসি মানবিক বিভাগ"
        },
        "SSC_SCIENCE": {
            "cohort_size": 1800000.0,
            "mean_score": 62.0,
            "std_dev": 15.0,
            "golden_a_plus_benchmark": 80.0,
            "label_bn": "এসএসসি বিজ্ঞান বিভাগ"
        }
    }

    # Bangladesh Board Grading Scale Definition
    BOARD_GRADE_SCALE = [
        {"min_score": 80.0, "letter_grade": "A+", "grade_point": 5.00, "remark_bn": "অসাধারণ সাফল্য"},
        {"min_score": 70.0, "letter_grade": "A", "grade_point": 4.00, "remark_bn": "উত্তম সাফল্য"},
        {"min_score": 60.0, "letter_grade": "A-", "grade_point": 3.50, "remark_bn": "সন্তোষজনক"},
        {"min_score": 50.0, "letter_grade": "B", "grade_point": 3.00, "remark_bn": "গড়পরতা"},
        {"min_score": 40.0, "letter_grade": "C", "grade_point": 2.00, "remark_bn": "উন্নতি প্রয়োজন"},
        {"min_score": 33.0, "letter_grade": "D", "grade_point": 1.00, "remark_bn": "উত্তীর্ণ ন্যূনতম"},
        {"min_score": 0.0, "letter_grade": "F", "grade_point": 0.00, "remark_bn": "অকৃতকার্য"}
    ]

    def __init__(self):
        self._audit_logs: List[Dict[str, Any]] = []

    def reset_for_testing(self) -> None:
        """Resets service internal state for deterministic test suites."""
        self._audit_logs.clear()

    @staticmethod
    def _normal_cdf(z: float) -> float:
        """Cumulative distribution function for standard normal distribution N(0, 1)."""
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

    @classmethod
    def get_grade_info(cls, score_pct: float) -> Dict[str, Any]:
        """Maps a numeric percentage score to Bangladesh Board grade and grade point."""
        clamped_score = max(0.0, min(100.0, float(score_pct)))
        for grade in cls.BOARD_GRADE_SCALE:
            if clamped_score >= grade["min_score"]:
                return {
                    "letter_grade": grade["letter_grade"],
                    "grade_point": grade["grade_point"],
                    "remark_bn": grade["remark_bn"]
                }
        return {"letter_grade": "F", "grade_point": 0.00, "remark_bn": "অকৃতকার্য"}

    def predict_gpa_and_national_rank(
        self,
        student_id: str,
        target_exam: str,
        subject_performances: List[Dict[str, Any]],
        historical_exam_scores: Optional[List[float]] = None,
        study_consistency_index: float = 0.85
    ) -> Dict[str, Any]:
        """
        Calculates expected CGPA with 95% Confidence Interval, Golden A+ probability,
        and National Percentile / Rank estimation over the targeted cohort.
        """
        cohort_config = self.NATIONAL_COHORTS.get(target_exam, self.NATIONAL_COHORTS["HSC_SCIENCE"])
        consistency = max(0.0, min(1.0, float(study_consistency_index)))

        if not subject_performances:
            return {
                "success": False,
                "message": "কমপক্ষে একটি বিষয়ের পারফরম্যান্স ডেটা আবশ্যক।",
                "predicted_cgpa": 0.00,
                "confidence_interval_95": {"lower": 0.00, "upper": 0.00},
                "golden_a_plus_probability_pct": 0.0,
                "national_percentile": 0.0,
                "projected_rank": 0
            }

        processed_subjects: List[Dict[str, Any]] = []
        total_gpa_points = 0.0
        has_failing_subject = False
        golden_chances: List[float] = []
        mastery_scores: List[float] = []

        for sub in subject_performances:
            sub_id = sub.get("subject_id", "sub_unknown")
            sub_name = sub.get("subject_name", sub_id)
            avg_score = max(0.0, min(100.0, float(sub.get("average_score_pct", 50.0))))
            theta = max(-3.0, min(3.0, float(sub.get("latent_ability_theta", 0.0))))
            quiz_count = max(0, int(sub.get("quiz_count", 1)))

            # Latent ability logistic transformation to 0-100 scale: 1 / (1 + e^(-1.7 * theta)) * 100
            theta_pct = (1.0 / (1.0 + math.exp(-1.7 * theta))) * 100.0

            # Bayesian weighted blended mastery: 65% observed average + 35% IRT latent ability
            blended_mastery = (0.65 * avg_score) + (0.35 * theta_pct)
            
            # Consistency boost / penalty (-2.0% to +2.0%)
            consistency_adj = (consistency - 0.5) * 4.0
            adjusted_mastery = max(0.0, min(100.0, blended_mastery + consistency_adj))

            mastery_scores.append(adjusted_mastery)
            grade_info = self.get_grade_info(adjusted_mastery)
            gp = grade_info["grade_point"]

            if gp == 0.00:
                has_failing_subject = True

            total_gpa_points += gp

            # Subject Golden A+ chance (Probability that true score >= 80)
            # Subject standard deviation depends on quiz count stability
            sub_std = max(2.5, 9.0 / math.sqrt(max(1, quiz_count)))
            z_golden = (adjusted_mastery - 80.0) / sub_std
            sub_golden_prob = self._normal_cdf(z_golden)
            golden_chances.append(sub_golden_prob)

            processed_subjects.append({
                "subject_id": sub_id,
                "subject_name": sub_name,
                "adjusted_mastery_pct": round(adjusted_mastery, 1),
                "grade_point": gp,
                "letter_grade": grade_info["letter_grade"],
                "golden_a_plus_chance_pct": round(sub_golden_prob * 100.0, 1),
                "remark_bn": grade_info["remark_bn"]
            })

        # Base Expected CGPA calculation
        num_subjects = len(processed_subjects)
        if has_failing_subject:
            expected_cgpa = 0.00
        else:
            expected_cgpa = round(total_gpa_points / num_subjects, 2)
            expected_cgpa = max(1.00, min(5.00, expected_cgpa))

        # Overall Golden A+ Probability (Joint probability that all subjects attain A+)
        if has_failing_subject:
            golden_prob_total = 0.0
        else:
            joint_prob = 1.0
            for p in golden_chances:
                joint_prob *= p
            golden_prob_total = round(joint_prob * 100.0, 1)

        # 95% Confidence Interval for CGPA
        # Computed using historical mock exam score variance if available, else default standard error
        hist_scores = [max(0.0, min(100.0, float(s))) for s in (historical_exam_scores or [])]
        if len(hist_scores) >= 2:
            hist_mean = sum(hist_scores) / len(hist_scores)
            variance = sum((s - hist_mean) ** 2 for s in hist_scores) / (len(hist_scores) - 1)
            hist_std = math.sqrt(variance)
            se_score = hist_std / math.sqrt(len(hist_scores))
        else:
            se_score = 4.5

        # Translate score Standard Error to GPA delta (~0.02 GPA points per 1% mark)
        se_gpa = max(0.04, min(0.35, se_score * 0.025))
        if has_failing_subject:
            ci_lower = 0.00
            ci_upper = 0.00
        else:
            ci_lower = max(1.00, round(expected_cgpa - (1.96 * se_gpa), 2))
            ci_upper = min(5.00, round(expected_cgpa + (1.96 * se_gpa), 2))

        # National Percentile and Merit Rank Estimation
        cohort_mean = cohort_config["mean_score"]
        cohort_std = max(1.0, cohort_config["std_dev"])
        cohort_size = cohort_config["cohort_size"]

        overall_mastery = sum(mastery_scores) / len(mastery_scores)
        z_national = (overall_mastery - cohort_mean) / cohort_std
        national_percentile = round(self._normal_cdf(z_national) * 100.0, 2)

        # Expected Rank = CohortSize * (1 - Percentile)
        rank_proportion = max(0.000001, 1.0 - (national_percentile / 100.0))
        projected_rank = max(1, int(round(cohort_size * rank_proportion)))

        # Rank Confidence Boundaries (Best vs Conservative)
        z_best = z_national + (1.96 * (se_score / cohort_std))
        z_worst = z_national - (1.96 * (se_score / cohort_std))
        rank_best = max(1, int(round(cohort_size * max(0.000001, 1.0 - self._normal_cdf(z_best)))))
        rank_conservative = min(int(cohort_size), int(round(cohort_size * max(0.000001, 1.0 - self._normal_cdf(z_worst)))))

        # Performance Velocity / Momentum Slope
        if len(hist_scores) >= 2:
            n = len(hist_scores)
            x_vals = list(range(n))
            x_mean = sum(x_vals) / n
            y_mean = sum(hist_scores) / n
            denom = sum((x - x_mean) ** 2 for x in x_vals)
            if denom > 0:
                slope = sum((x_vals[i] - x_mean) * (hist_scores[i] - y_mean) for i in range(n)) / denom
            else:
                slope = 0.0
        else:
            slope = 0.0

        if slope > 1.2:
            velocity_status = "ACCELERATING"
            velocity_label_bn = "দ্রুত উন্নতিশীল (পজিটিভ মোমেন্টাম)"
        elif slope < -1.2:
            velocity_status = "DECELERATING"
            velocity_label_bn = "সতর্কতা: পারফরম্যান্স নিম্নমুখী"
        else:
            velocity_status = "STEADY"
            velocity_label_bn = "স্থিতিশীল ধারাবাহিকতা"

        result = {
            "success": True,
            "student_id": student_id,
            "target_exam": target_exam,
            "target_exam_label_bn": cohort_config["label_bn"],
            "predicted_cgpa": expected_cgpa,
            "confidence_interval_95": {
                "lower": ci_lower,
                "upper": ci_upper
            },
            "golden_a_plus_probability_pct": golden_prob_total,
            "overall_mastery_pct": round(overall_mastery, 1),
            "national_percentile": national_percentile,
            "projected_rank": projected_rank,
            "rank_confidence_band": {
                "best_case_rank": rank_best,
                "conservative_rank": rank_conservative,
                "total_cohort": int(cohort_size)
            },
            "performance_momentum": {
                "velocity_status": velocity_status,
                "velocity_label_bn": velocity_label_bn,
                "slope_pct_per_milestone": round(slope, 2)
            },
            "subject_breakdown": processed_subjects
        }

        self._audit_logs.append({
            "action": "GPA_PREDICTION",
            "student_id": student_id,
            "predicted_cgpa": expected_cgpa,
            "projected_rank": projected_rank
        })

        return result

    def get_national_benchmarks(self) -> Dict[str, Any]:
        """Returns standard benchmark percentiles and cut-off thresholds for national boards."""
        return {
            "success": True,
            "cohorts": self.NATIONAL_COHORTS,
            "grading_scale": self.BOARD_GRADE_SCALE
        }


# Global singleton instance
predictive_analytics_service = PredictiveAnalyticsService()
