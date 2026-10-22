"""
===================================================================================
Module: Competitive Admission Analytics Engine
Topic: Multi-Track Admission Probability, Sensitivity Simulation & High-ROI Guidance
File: backend/app/services/admission_probability_service.py
Purpose: Evaluates student subject profiles against top competitive admission tracks
         (BUET, DU Ka, Medical, GST), computes logistic probability scores, conducts
         What-If sensitivity simulations, and pinpoints high-yield chapter targets.
Audience: Developers, Academic Mentors, QA Engineers, System Architects
Standards: Clean Architecture, OWASP ASVS Level 2, Full Type Hints, Zero-Emoji
===================================================================================
"""

from typing import Dict, Any, List, Optional
import math


class AdmissionProbabilityService:
    """
    Evaluates probability of competitive university admission in Bangladesh,
    conducts What-If sensitivity analysis, and delivers high-ROI academic advice.
    """

    ADMISSION_TRACKS: Dict[str, Dict[str, Any]] = {
        "BUET_ENG": {
            "track_id": "BUET_ENG",
            "name_bn": "বুয়েট প্রকৌশল ও স্থাপত্য অনুষদ",
            "category": "ENGINEERING",
            "seats": 1305,
            "min_required_gpa": 5.00,
            "weights": {
                "higher_math": 0.40,
                "physics": 0.40,
                "chemistry": 0.20
            },
            "cutoff_score_benchmark": 82.5,
            "logistic_steepness_k": 0.16,
            "high_yield_chapters": [
                {"subject": "higher_math", "chapter": "ক্যালকুলাস: যোগজীকরণ ও অন্তরীকরণ", "weight_bn": "খুব উচ্চ"},
                {"subject": "higher_math", "chapter": "ত্রিকোণমিতি ও কনিক্স", "weight_bn": "উচ্চ"},
                {"subject": "physics", "chapter": "গতিবিদ্যা ও নিউটোনিয়ান বলবিদ্যা", "weight_bn": "খুব উচ্চ"},
                {"subject": "physics", "chapter": "স্থির তড়িৎ ও চল তড়িৎ", "weight_bn": "উচ্চ"},
                {"subject": "chemistry", "chapter": "জৈব রসায়ন বিক্রিয়াকৌশল", "weight_bn": "উচ্চ"}
            ]
        },
        "DU_KA": {
            "track_id": "DU_KA",
            "name_bn": "ঢাকা বিশ্ববিদ্যালয় 'ক' ইউনিট (বিজ্ঞান অনুষদ)",
            "category": "GENERAL_SCIENCE",
            "seats": 1851,
            "min_required_gpa": 4.80,
            "weights": {
                "physics": 0.30,
                "chemistry": 0.30,
                "higher_math": 0.25,
                "biology": 0.15
            },
            "cutoff_score_benchmark": 74.0,
            "logistic_steepness_k": 0.14,
            "high_yield_chapters": [
                {"subject": "physics", "chapter": "কাজ, ক্ষমতা ও শক্তি এবং মহাকর্ষ", "weight_bn": "উচ্চ"},
                {"subject": "chemistry", "chapter": "গুণগত রসায়ন ও দ্রাব্যতা নীতি", "weight_bn": "উচ্চ"},
                {"subject": "higher_math", "chapter": "ম্যাট্রিক্স, নির্ণায়ক ও বৃত্ত", "weight_bn": "উচ্চ"},
                {"subject": "biology", "chapter": "কোষ রসায়ন ও জিনতত্ত্ব", "weight_bn": "মাঝারি"}
            ]
        },
        "MEDICAL_MBBS": {
            "track_id": "MEDICAL_MBBS",
            "name_bn": "জাতীয় সরকারি মেডিকেল কলেজ (এমবিবিএস)",
            "category": "MEDICAL",
            "seats": 5382,
            "min_required_gpa": 4.75,
            "weights": {
                "biology": 0.35,
                "chemistry": 0.30,
                "physics": 0.20,
                "english": 0.15
            },
            "cutoff_score_benchmark": 73.5,
            "logistic_steepness_k": 0.15,
            "high_yield_chapters": [
                {"subject": "biology", "chapter": "মানব শারীরতত্ত্ব: রক্ত, সংবহন ও পরিপাক", "weight_bn": "খুব উচ্চ"},
                {"subject": "biology", "chapter": "উদ্ভিদ শারীরতত্ত্ব ও প্রজনন", "weight_bn": "উচ্চ"},
                {"subject": "chemistry", "chapter": "জৈব যৌগ ও রাসায়নিক পরিবর্তন", "weight_bn": "উচ্চ"},
                {"subject": "english", "chapter": "Grammar: Subject-Verb, Preposition, Vocabulary", "weight_bn": "উচ্চ"}
            ]
        },
        "DU_GA": {
            "track_id": "DU_GA",
            "name_bn": "ঢাকা বিশ্ববিদ্যালয় 'গ' ইউনিট (ব্যবসায় অনুষদ)",
            "category": "BUSINESS",
            "seats": 1050,
            "min_required_gpa": 4.50,
            "weights": {
                "accounting": 0.35,
                "business_org": 0.25,
                "english": 0.25,
                "bangla": 0.15
            },
            "cutoff_score_benchmark": 71.0,
            "logistic_steepness_k": 0.14,
            "high_yield_chapters": [
                {"subject": "accounting", "chapter": "আর্থিক বিবরণী বিশ্লেষণ ও জাবেদা", "weight_bn": "খুব উচ্চ"},
                {"subject": "english", "chapter": "Reading Comprehension & Error Detection", "weight_bn": "উচ্চ"},
                {"subject": "business_org", "chapter": "কোম্পানি সংগঠন ও বিপণন নীতিমালা", "weight_bn": "উচ্চ"}
            ]
        },
        "GST_SCIENCE": {
            "track_id": "GST_SCIENCE",
            "name_bn": "জিএসটি গুচ্ছ বিশ্ববিদ্যালয় (বিজ্ঞান বিভাগ)",
            "category": "CLUSTER",
            "seats": 12500,
            "min_required_gpa": 4.00,
            "weights": {
                "physics": 0.30,
                "chemistry": 0.30,
                "higher_math": 0.20,
                "biology": 0.20
            },
            "cutoff_score_benchmark": 61.0,
            "logistic_steepness_k": 0.12,
            "high_yield_chapters": [
                {"subject": "physics", "chapter": "পদার্থের গাঠনিক ধর্ম ও পর্যায়বৃত্ত গতি", "weight_bn": "উচ্চ"},
                {"subject": "chemistry", "chapter": "পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন", "weight_bn": "উচ্চ"},
                {"subject": "higher_math", "chapter": "সরলরেখা ও ত্রিকোণমিতিক সমীকরণ", "weight_bn": "উচ্চ"}
            ]
        }
    }

    def __init__(self):
        self._audit_logs: List[Dict[str, Any]] = []

    def reset_for_testing(self) -> None:
        """Clears in-memory audit logs for unit tests."""
        self._audit_logs.clear()

    @staticmethod
    def _logistic(x: float, k: float) -> float:
        """Standard logistic function bounded in (0, 1)."""
        # Defensive clamp to avoid math.overflow
        val = max(-15.0, min(15.0, k * x))
        return 1.0 / (1.0 + math.exp(-val))

    def evaluate_admission_probabilities(
        self,
        student_id: str,
        subject_scores: Dict[str, float],
        predicted_cgpa: float = 5.00
    ) -> Dict[str, Any]:
        """
        Evaluates admission likelihood across all configured tracks,
        determines risk categories, and highlights high-ROI chapter targets.
        """
        projections: List[Dict[str, Any]] = []

        safe_cgpa = max(0.0, min(5.00, float(predicted_cgpa)))

        for track_id, config in self.ADMISSION_TRACKS.items():
            weights = config["weights"]
            cutoff = config["cutoff_score_benchmark"]
            k = config["logistic_steepness_k"]
            min_gpa = config["min_required_gpa"]

            # Calculate weighted score for track
            weighted_score = 0.0
            total_weight = 0.0
            missing_subjects: List[str] = []

            for sub_key, weight in weights.items():
                if sub_key in subject_scores:
                    raw_score = max(0.0, min(100.0, float(subject_scores[sub_key])))
                    weighted_score += raw_score * weight
                    total_weight += weight
                else:
                    missing_subjects.append(sub_key)
                    # Assign baseline assumption of 50.0 for missing subject
                    weighted_score += 50.0 * weight
                    total_weight += weight

            # Track weighted mastery
            track_mastery = weighted_score / max(0.001, total_weight)

            # Raw logistic probability based on distance from cutoff
            score_diff = track_mastery - cutoff
            raw_prob = self._logistic(score_diff, k)

            # GPA Eligibility Penalty
            gpa_eligible = safe_cgpa >= min_gpa
            if not gpa_eligible:
                gpa_penalty_factor = max(0.1, safe_cgpa / max(1.0, min_gpa))
                final_prob = raw_prob * (gpa_penalty_factor ** 2)
            else:
                final_prob = raw_prob

            prob_pct = round(final_prob * 100.0, 1)

            # Classify Risk Tier
            if prob_pct >= 75.0:
                tier = "HIGH_PROBABILITY"
                tier_label_bn = "উচ্চ সম্ভাবনা"
                tier_color = "emerald"
            elif prob_pct >= 50.0:
                tier = "COMPETITIVE"
                tier_label_bn = "প্রতিযোগিতামূলক (লড়াই সম্ভব)"
                tier_color = "amber"
            elif prob_pct >= 30.0:
                tier = "STRETCH_GOAL"
                tier_label_bn = "কঠিন কিন্তু সম্ভাব্য"
                tier_color = "indigo"
            else:
                tier = "CRITICAL_ATTENTION"
                tier_label_bn = "বিশেষ জোর দেয়া প্রয়োজন"
                tier_color = "rose"

            # Top High-ROI Recommendations for this track
            # Pick subjects with highest weight and score below 85
            subject_roi_potentials = []
            for sub_key, weight in weights.items():
                cur_score = max(0.0, min(100.0, float(subject_scores.get(sub_key, 50.0))))
                headroom = max(0.0, 95.0 - cur_score)
                # Marginal gain = weight * headroom
                roi_index = weight * headroom
                subject_roi_potentials.append({
                    "subject": sub_key,
                    "current_score": cur_score,
                    "weight": weight,
                    "roi_index": round(roi_index, 2)
                })

            subject_roi_potentials.sort(key=lambda x: x["roi_index"], reverse=True)
            top_roi_subject = subject_roi_potentials[0]["subject"] if subject_roi_potentials else None

            # Filter high yield chapters for top ROI subject
            relevant_chapters = [
                c for c in config["high_yield_chapters"]
                if c["subject"] == top_roi_subject
            ]
            if not relevant_chapters:
                relevant_chapters = config["high_yield_chapters"][:2]

            projections.append({
                "track_id": track_id,
                "name_bn": config["name_bn"],
                "category": config["category"],
                "total_seats": config["seats"],
                "min_required_gpa": min_gpa,
                "gpa_eligible": gpa_eligible,
                "track_mastery_pct": round(track_mastery, 1),
                "admission_probability_pct": prob_pct,
                "probability_tier": tier,
                "probability_tier_label_bn": tier_label_bn,
                "badge_color": tier_color,
                "top_lever_subject": top_roi_subject,
                "missing_subjects": missing_subjects,
                "is_partially_estimated": len(missing_subjects) > 0,
                "high_yield_recommendations": relevant_chapters
            })

        self._audit_logs.append({
            "action": "ADMISSION_PROBABILITY_EVAL",
            "student_id": student_id,
            "track_count": len(projections)
        })

        return {
            "success": True,
            "student_id": student_id,
            "predicted_cgpa": safe_cgpa,
            "projections": projections
        }

    def simulate_what_if_sensitivity(
        self,
        student_id: str,
        track_id: str,
        baseline_subject_scores: Dict[str, float],
        score_deltas: Dict[str, float],
        current_rank: int = 15000
    ) -> Dict[str, Any]:
        """
        Simulates the effect of targeted subject score improvements on admission odds
        and estimated national rank movement.
        """
        config = self.ADMISSION_TRACKS.get(track_id)
        if not config:
            return {
                "success": False,
                "message": f"ভর্তি ট্র্যাক '{track_id}' পাওয়া যায়নি।"
            }

        weights = config["weights"]
        cutoff = config["cutoff_score_benchmark"]
        k = config["logistic_steepness_k"]

        # Compute Baseline
        baseline_weighted = sum(
            max(0.0, min(100.0, float(baseline_subject_scores.get(sub, 50.0)))) * w
            for sub, w in weights.items()
        ) / max(0.001, sum(weights.values()))

        baseline_prob = self._logistic(baseline_weighted - cutoff, k)

        # Compute Simulated Scores
        simulated_scores: Dict[str, float] = {}
        for sub, w in weights.items():
            base = max(0.0, min(100.0, float(baseline_subject_scores.get(sub, 50.0))))
            delta = float(score_deltas.get(sub, 0.0))
            # Safe clamping between 0 and 100
            simulated_scores[sub] = max(0.0, min(100.0, base + delta))

        simulated_weighted = sum(
            simulated_scores[sub] * w for sub, w in weights.items()
        ) / max(0.001, sum(weights.values()))

        simulated_prob = self._logistic(simulated_weighted - cutoff, k)

        prob_delta_pct = round((simulated_prob - baseline_prob) * 100.0, 1)

        # Estimate Rank Jump: ~1200 ranks improvement per 1% overall weighted gain near competitive threshold
        score_diff_overall = simulated_weighted - baseline_weighted
        rank_displacement = int(round(score_diff_overall * 1250.0))
        projected_new_rank = max(1, current_rank - rank_displacement)

        # Study effort requirement estimation (~6 study hours per 1% mark improvement)
        total_delta_points = sum(max(0.0, float(d)) for d in score_deltas.values())
        estimated_study_hours = int(round(total_delta_points * 5.5))

        if total_delta_points <= 10.0:
            feasibility = "HIGH"
            feasibility_label_bn = "অনায়াসে অর্জনযোগ্য (২-৩ সপ্তাহের সুনির্দিষ্ট অনুশীলন)"
        elif total_delta_points <= 20.0:
            feasibility = "MODERATE"
            feasibility_label_bn = "পরিশ্রমসাধ্য কিন্তু সম্পূর্ণ বাস্তবসম্মত"
        else:
            feasibility = "INTENSIVE"
            feasibility_label_bn = "নিবিড় একাগ্রতা ও দীর্ঘমেয়াদী রিভিশন আবশ্যক"

        return {
            "success": True,
            "student_id": student_id,
            "track_id": track_id,
            "track_name_bn": config["name_bn"],
            "baseline_weighted_score": round(baseline_weighted, 1),
            "simulated_weighted_score": round(simulated_weighted, 1),
            "baseline_probability_pct": round(baseline_prob * 100.0, 1),
            "simulated_probability_pct": round(simulated_prob * 100.0, 1),
            "probability_gain_pct": prob_delta_pct,
            "current_national_rank": current_rank,
            "projected_new_rank": projected_new_rank,
            "rank_leap": rank_displacement,
            "estimated_sprint_study_hours": estimated_study_hours,
            "feasibility_assessment": {
                "tier": feasibility,
                "label_bn": feasibility_label_bn
            },
            "simulated_scores": simulated_scores
        }


# Global singleton instance
admission_probability_service = AdmissionProbabilityService()
