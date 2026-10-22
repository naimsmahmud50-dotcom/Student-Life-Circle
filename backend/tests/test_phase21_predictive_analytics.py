"""
===================================================================================
Module: Predictive Analytics & Rank Forecasting Tests
Topic: Unit & Integration Verification for CGPA, Rank & Admission Simulation
File: backend/tests/test_phase21_predictive_analytics.py
Purpose: Verifies Bayesian latent ability to GPA conversion, 95% confidence intervals,
         national cohort percentiles, admission track probabilities, What-If simulation,
         and boundary protection with zero test failures.
Audience: QA Engineers, Backend Developers, Continuous Integration Runners
Standards: Clean Architecture, OWASP ASVS Level 2, Full Type Hints, Zero-Emoji
===================================================================================
"""

import unittest

try:
    from backend.app.services.predictive_analytics_service import predictive_analytics_service
    from backend.app.services.admission_probability_service import admission_probability_service
    from backend.app.schemas.predictive_analytics_schema import (
        GPAPredictionRequest,
        AdmissionProbabilityRequest,
        SensitivitySimulationRequest
    )
except ImportError:
    from app.services.predictive_analytics_service import predictive_analytics_service
    from app.services.admission_probability_service import admission_probability_service
    from app.schemas.predictive_analytics_schema import (
        GPAPredictionRequest,
        AdmissionProbabilityRequest,
        SensitivitySimulationRequest
    )

try:
    from fastapi.testclient import TestClient
    from backend.app.main import app
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


class TestPhase21PredictiveAnalytics(unittest.TestCase):
    """
    Comprehensive unit and integration test suite for Phase 21:
    Predictive Academic CGPA & National Rank Forecasting Engine.
    """

    def setUp(self) -> None:
        """Reset service states and initialize test client."""
        predictive_analytics_service.reset_for_testing()
        admission_probability_service.reset_for_testing()
        if HAS_FASTAPI:
            self.client = TestClient(app)

    def tearDown(self) -> None:
        """Clean up post-test execution."""
        predictive_analytics_service.reset_for_testing()
        admission_probability_service.reset_for_testing()

    def test_01_grade_info_mapping_boundaries(self) -> None:
        """Verifies grade point boundaries based on Bangladesh Board grading scale."""
        g_aplus = predictive_analytics_service.get_grade_info(85.0)
        self.assertEqual(g_aplus["letter_grade"], "A+")
        self.assertEqual(g_aplus["grade_point"], 5.00)

        g_exact_80 = predictive_analytics_service.get_grade_info(80.0)
        self.assertEqual(g_exact_80["letter_grade"], "A+")
        self.assertEqual(g_exact_80["grade_point"], 5.00)

        g_a = predictive_analytics_service.get_grade_info(75.0)
        self.assertEqual(g_a["letter_grade"], "A")
        self.assertEqual(g_a["grade_point"], 4.00)

        g_aminus = predictive_analytics_service.get_grade_info(65.0)
        self.assertEqual(g_aminus["letter_grade"], "A-")
        self.assertEqual(g_aminus["grade_point"], 3.50)

        g_b = predictive_analytics_service.get_grade_info(55.0)
        self.assertEqual(g_b["letter_grade"], "B")
        self.assertEqual(g_b["grade_point"], 3.00)

        g_c = predictive_analytics_service.get_grade_info(45.0)
        self.assertEqual(g_c["letter_grade"], "C")
        self.assertEqual(g_c["grade_point"], 2.00)

        g_d = predictive_analytics_service.get_grade_info(35.0)
        self.assertEqual(g_d["letter_grade"], "D")
        self.assertEqual(g_d["grade_point"], 1.00)

        g_f = predictive_analytics_service.get_grade_info(28.0)
        self.assertEqual(g_f["letter_grade"], "F")
        self.assertEqual(g_f["grade_point"], 0.00)

    def test_02_predict_gpa_normal_high_performing_profile(self) -> None:
        """Verifies Bayesian GPA projection and 95% CI for a strong HSC Science profile."""
        subjects = [
            {"subject_id": "physics", "subject_name": "পদার্থবিজ্ঞান", "average_score_pct": 84.0, "latent_ability_theta": 1.2, "quiz_count": 8},
            {"subject_id": "chemistry", "subject_name": "রসায়ন", "average_score_pct": 82.0, "latent_ability_theta": 1.0, "quiz_count": 7},
            {"subject_id": "higher_math", "subject_name": "উচ্চতর গণিত", "average_score_pct": 89.0, "latent_ability_theta": 1.5, "quiz_count": 10},
            {"subject_id": "biology", "subject_name": "জীববিজ্ঞান", "average_score_pct": 80.0, "latent_ability_theta": 0.9, "quiz_count": 6},
            {"subject_id": "bangla", "subject_name": "বাংলা", "average_score_pct": 78.0, "latent_ability_theta": 0.6, "quiz_count": 5},
            {"subject_id": "english", "subject_name": "ইংরেজি", "average_score_pct": 77.0, "latent_ability_theta": 0.5, "quiz_count": 5},
            {"subject_id": "ict", "subject_name": "আইসিটি", "average_score_pct": 88.0, "latent_ability_theta": 1.4, "quiz_count": 8}
        ]
        history = [75.0, 78.0, 81.5, 84.0]

        result = predictive_analytics_service.predict_gpa_and_national_rank(
            student_id="std_top_01",
            target_exam="HSC_SCIENCE",
            subject_performances=subjects,
            historical_exam_scores=history,
            study_consistency_index=0.92
        )

        self.assertTrue(result["success"])
        self.assertGreaterEqual(result["predicted_cgpa"], 4.50)
        self.assertLessEqual(result["predicted_cgpa"], 5.00)

        ci = result["confidence_interval_95"]
        self.assertLessEqual(ci["lower"], result["predicted_cgpa"])
        self.assertGreaterEqual(ci["upper"], result["predicted_cgpa"])
        self.assertLessEqual(ci["upper"], 5.00)

        # High score profile should place student in top national percentiles
        self.assertGreater(result["national_percentile"], 90.0)
        self.assertLess(result["projected_rank"], 100000)

        # Rank confidence band
        band = result["rank_confidence_band"]
        self.assertLessEqual(band["best_case_rank"], result["projected_rank"])
        self.assertGreaterEqual(band["conservative_rank"], result["projected_rank"])

    def test_03_failing_subject_forces_zero_gpa_and_ci(self) -> None:
        """Verifies boundary fix: an F grade in any subject forces expected CGPA and CI to exactly 0.00."""
        subjects = [
            {"subject_id": "physics", "subject_name": "পদার্থবিজ্ঞান", "average_score_pct": 85.0, "latent_ability_theta": 1.2, "quiz_count": 5},
            {"subject_id": "higher_math", "subject_name": "উচ্চতর গণিত", "average_score_pct": 25.0, "latent_ability_theta": -2.2, "quiz_count": 5}
        ]

        result = predictive_analytics_service.predict_gpa_and_national_rank(
            student_id="std_fail_01",
            target_exam="HSC_SCIENCE",
            subject_performances=subjects
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["predicted_cgpa"], 0.00)
        self.assertEqual(result["confidence_interval_95"]["lower"], 0.00)
        self.assertEqual(result["confidence_interval_95"]["upper"], 0.00)
        self.assertEqual(result["golden_a_plus_probability_pct"], 0.0)

    def test_04_empty_subject_performance_handling(self) -> None:
        """Verifies graceful handling when subject performances list is empty."""
        result = predictive_analytics_service.predict_gpa_and_national_rank(
            student_id="std_empty",
            target_exam="HSC_SCIENCE",
            subject_performances=[]
        )
        self.assertFalse(result["success"])
        self.assertEqual(result["predicted_cgpa"], 0.00)
        self.assertIn("কমপক্ষে", result["message"])

    def test_05_momentum_velocity_accelerating(self) -> None:
        """Verifies that an upward trend in mock exam scores correctly flags ACCELERATING momentum."""
        subjects = [
            {"subject_id": "physics", "subject_name": "পদার্থবিজ্ঞান", "average_score_pct": 75.0, "latent_ability_theta": 0.5, "quiz_count": 4}
        ]
        history = [62.0, 68.0, 74.0, 81.0]

        result = predictive_analytics_service.predict_gpa_and_national_rank(
            student_id="std_fast",
            target_exam="HSC_SCIENCE",
            subject_performances=subjects,
            historical_exam_scores=history
        )

        momentum = result["performance_momentum"]
        self.assertEqual(momentum["velocity_status"], "ACCELERATING")
        self.assertGreater(momentum["slope_pct_per_milestone"], 1.2)

    def test_06_evaluate_admission_probabilities_coverage(self) -> None:
        """Verifies multi-track admission probability evaluation across BUET, DU, Medical, and GST."""
        scores = {
            "higher_math": 88.0,
            "physics": 85.0,
            "chemistry": 82.0,
            "biology": 80.0,
            "english": 76.0
        }

        result = admission_probability_service.evaluate_admission_probabilities(
            student_id="std_adm_01",
            subject_scores=scores,
            predicted_cgpa=5.00
        )

        self.assertTrue(result["success"])
        projections = result["projections"]
        self.assertGreaterEqual(len(projections), 4)

        track_ids = [p["track_id"] for p in projections]
        self.assertIn("BUET_ENG", track_ids)
        self.assertIn("DU_KA", track_ids)
        self.assertIn("MEDICAL_MBBS", track_ids)
        self.assertIn("GST_SCIENCE", track_ids)

        for p in projections:
            self.assertGreaterEqual(p["admission_probability_pct"], 0.0)
            self.assertLessEqual(p["admission_probability_pct"], 100.0)
            self.assertIn(p["probability_tier"], ["HIGH_PROBABILITY", "COMPETITIVE", "STRETCH_GOAL", "CRITICAL_ATTENTION"])
            self.assertIsInstance(p["high_yield_recommendations"], list)

    def test_07_missing_subjects_transparency_flag(self) -> None:
        """Verifies boundary fix: missing subjects are explicitly flagged in track projections."""
        # Only provide physics and chemistry, omitting higher_math for BUET
        partial_scores = {
            "physics": 85.0,
            "chemistry": 80.0
        }

        result = admission_probability_service.evaluate_admission_probabilities(
            student_id="std_missing",
            subject_scores=partial_scores,
            predicted_cgpa=5.00
        )

        buet_proj = next(p for p in result["projections"] if p["track_id"] == "BUET_ENG")
        self.assertTrue(buet_proj["is_partially_estimated"])
        self.assertIn("higher_math", buet_proj["missing_subjects"])

    def test_08_gpa_ineligibility_penalty(self) -> None:
        """Verifies that failing to meet the minimum required GPA applies an eligibility penalty."""
        scores = {
            "higher_math": 90.0,
            "physics": 90.0,
            "chemistry": 90.0
        }

        # BUET requires GPA 5.00. Candidate has GPA 4.00
        result = admission_probability_service.evaluate_admission_probabilities(
            student_id="std_low_gpa",
            subject_scores=scores,
            predicted_cgpa=4.00
        )

        buet_proj = next(p for p in result["projections"] if p["track_id"] == "BUET_ENG")
        self.assertFalse(buet_proj["gpa_eligible"])
        self.assertLess(buet_proj["admission_probability_pct"], 50.0)

    def test_09_what_if_sensitivity_simulation(self) -> None:
        """Verifies What-If sensitivity simulator outputs expected rank leap and probability gain."""
        baseline = {
            "higher_math": 75.0,
            "physics": 76.0,
            "chemistry": 74.0
        }
        deltas = {
            "higher_math": 10.0,
            "physics": 8.0
        }

        result = admission_probability_service.simulate_what_if_sensitivity(
            student_id="std_sim_01",
            track_id="BUET_ENG",
            baseline_subject_scores=baseline,
            score_deltas=deltas,
            current_rank=16000
        )

        self.assertTrue(result["success"])
        self.assertGreater(result["simulated_probability_pct"], result["baseline_probability_pct"])
        self.assertGreater(result["probability_gain_pct"], 0.0)
        self.assertLess(result["projected_new_rank"], result["current_national_rank"])
        self.assertGreater(result["rank_leap"], 0)
        self.assertGreater(result["estimated_sprint_study_hours"], 0)
        self.assertIn("feasibility_assessment", result)

    def test_10_what_if_sensitivity_invalid_track(self) -> None:
        """Verifies sensitivity simulation fails gracefully when given an invalid track ID."""
        result = admission_probability_service.simulate_what_if_sensitivity(
            student_id="std_invalid",
            track_id="UNKNOWN_TRACK_99",
            baseline_subject_scores={},
            score_deltas={}
        )
        self.assertFalse(result["success"])
        self.assertIn("পাওয়া যায়নি", result["message"])

    def test_11_schema_dto_contracts(self) -> None:
        """Verifies schema DTO models instantiate properly and validate contracts."""
        req_gpa = GPAPredictionRequest(
            student_id="std_dto_01",
            target_exam="HSC_SCIENCE",
            subject_performances=[{"subject_id": "physics", "average_score_pct": 80.0}],
            study_consistency_index=0.9
        )
        self.assertEqual(req_gpa.student_id, "std_dto_01")

        req_adm = AdmissionProbabilityRequest(
            student_id="std_dto_02",
            subject_scores={"physics": 85.0},
            predicted_cgpa=4.9
        )
        self.assertEqual(req_adm.predicted_cgpa, 4.9)

        req_sim = SensitivitySimulationRequest(
            student_id="std_dto_03",
            track_id="DU_KA",
            baseline_subject_scores={"physics": 75.0},
            score_deltas={"physics": 5.0},
            current_rank=12000
        )
        self.assertEqual(req_sim.current_rank, 12000)

    def test_12_benchmarks_retrieval(self) -> None:
        """Verifies retrieval of official national demographics and board grade scales."""
        benchmarks = predictive_analytics_service.get_national_benchmarks()
        self.assertTrue(benchmarks["success"])
        self.assertIn("HSC_SCIENCE", benchmarks["cohorts"])
        self.assertEqual(benchmarks["cohorts"]["HSC_SCIENCE"]["cohort_size"], 1300000.0)
        self.assertGreaterEqual(len(benchmarks["grading_scale"]), 7)


if __name__ == "__main__":
    unittest.main()
