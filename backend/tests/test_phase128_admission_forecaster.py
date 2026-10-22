"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    University Admission Forecaster & Sigmoid Rank Predictor
 * TOPIC:     Phase 128 Statistical Cut-Off Engine & Admission Probability Calibration
 * FILE:      backend/tests/test_phase128_admission_forecaster.py
 * PHASE:     Phase 128 - Autonomous Admission Cut-Off Forecaster
 * PURPOSE:   Comprehensive automated test suite validating:
 *            1. Developer Architecture Note headers & file presence
 *            2. Calibrated sigmoid probability mathematical invariants & monotonicity
 *            3. Institutional eligibility gates (BUET, DU Ka/Kha/Ga, Medical, GST)
 *            4. Quota offset threshold calculations
 *            5. Merit rank range interval estimates
 *            6. ASVS L2 Zero-PII sanitization & defense against data leakage
 *            7. Supabase migration 006 RLS policies and table structures
 *            8. Frontend 3D tactile button styling, Lucide icons, and Zero-Emoji compliance
 *            9. 10-year historical series dataset integrity (2015-2025).
 * STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Calibrated Probability
 */
"""

import math
import os
import re
import unittest
from pathlib import Path

from backend.analytics.admission_forecaster import (
    AdmissionForecaster,
    AcademicRecord,
    AdmissionUnit,
    QuotaType,
    ProbabilityTier,
    ForecastPrediction,
    EligibilityResult,
    PIILeakageDetectedException,
    HISTORICAL_CUTOFF_SERIES,
    UNIT_CONFIGS,
    QUOTA_OFFSETS,
)

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase128AdmissionForecaster(unittest.TestCase):
    """
    Automated test verification suite for Phase 128 Autonomous Admission Forecaster.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.analytics_init = cls.root_dir / "backend" / "analytics" / "__init__.py"
        cls.forecaster_py = cls.root_dir / "backend" / "analytics" / "admission_forecaster.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "006_admission_forecast_rls.sql"
        cls.predictor_tsx = cls.root_dir / "frontend" / "src" / "pages" / "admission" / "predictor.tsx"
        cls.admission_tsx = cls.root_dir / "frontend" / "src" / "pages" / "admission.tsx"
        cls.spec_md = cls.root_dir / "specs" / "032-phase128-admission-forecaster" / "spec.md"
        cls.plan_md = cls.root_dir / "specs" / "032-phase128-admission-forecaster" / "plan.md"
        cls.tasks_md = cls.root_dir / "specs" / "032-phase128-admission-forecaster" / "tasks.md"
        cls.test_file = Path(__file__).resolve()

        cls.target_files = [
            cls.analytics_init,
            cls.forecaster_py,
            cls.migration_sql,
            cls.predictor_tsx,
            cls.test_file,
        ]

    def test_01_all_target_files_exist_and_headers_valid(self):
        """Verify all target files exist and contain standardized Developer Architecture Note."""
        for file_path in self.target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"Missing Developer Architecture Note in {file_path.name}"
            )
            self.assertIn(
                "Phase 128 - Autonomous Admission Cut-Off Forecaster",
                content,
                f"Missing Phase 128 identifier in {file_path.name}"
            )

    def test_02_strict_zero_emoji_compliance(self):
        """Strictly enforces Zero-Emoji across all Phase 128 codebase files."""
        for file_path in self.target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"Zero-Emoji violation in {file_path.name}: Found emojis {matches}"
            )

    def test_03_sigmoid_probability_mathematical_bounds_and_monotonicity(self):
        """Validates mathematical bounds [0, 1] and strictly monotonically increasing behavior."""
        # Extreme low score
        p_low = AdmissionForecaster.calculate_sigmoid_probability(
            composite_score=0.0, median_cutoff_x0=74.5, slope_k=0.16
        )
        self.assertGreaterEqual(p_low, 0.0)
        self.assertLess(p_low, 0.01)

        # Cutoff midpoint (x == x0)
        p_mid = AdmissionForecaster.calculate_sigmoid_probability(
            composite_score=74.5, median_cutoff_x0=74.5, slope_k=0.16
        )
        self.assertAlmostEqual(p_mid, 0.50, places=2)

        # Extreme high score
        p_high = AdmissionForecaster.calculate_sigmoid_probability(
            composite_score=100.0, median_cutoff_x0=74.5, slope_k=0.16
        )
        self.assertLessEqual(p_high, 1.0)
        self.assertGreater(p_high, 0.95)

        # Monotonicity test
        scores = [40.0, 50.0, 60.0, 70.0, 74.5, 80.0, 90.0, 100.0]
        probs = [
            AdmissionForecaster.calculate_sigmoid_probability(
                composite_score=s, median_cutoff_x0=74.5, slope_k=0.16
            )
            for s in scores
        ]
        for i in range(len(probs) - 1):
            self.assertLessEqual(
                probs[i],
                probs[i + 1],
                f"Sigmoid probability must be monotonically non-decreasing: {probs[i]} > {probs[i+1]}"
            )

    def test_04_eligibility_gates_buet(self):
        """Tests strict eligibility gate conditions for BUET Engineering."""
        # Valid candidate: GPA 5.0 with Phy, Chem, Math 5.0
        valid_rec = AcademicRecord(
            ssc_gpa=5.0,
            hsc_gpa=5.0,
            physics_gp=5.0,
            chemistry_gp=5.0,
            math_gp=5.0,
            exam_sim_score=82.0
        )
        elig = AdmissionForecaster.evaluate_eligibility(AdmissionUnit.BUET, valid_rec)
        self.assertTrue(elig.is_eligible)
        self.assertEqual(len(elig.violations_en), 0)

        # Failing candidate: Higher Math GP is 4.0 (requires 5.0)
        math_fail_rec = AcademicRecord(
            ssc_gpa=5.0,
            hsc_gpa=5.0,
            physics_gp=5.0,
            chemistry_gp=5.0,
            math_gp=4.0,
            exam_sim_score=82.0
        )
        math_fail_elig = AdmissionForecaster.evaluate_eligibility(AdmissionUnit.BUET, math_fail_rec)
        self.assertFalse(math_fail_elig.is_eligible)
        self.assertTrue(any("Higher Math" in v for v in math_fail_elig.violations_en))
        self.assertTrue(any("উচ্চতর গণিত" in v for v in math_fail_elig.violations_bn))

        # Full forecast should return INELIGIBLE tier and 0 probability
        forecast = AdmissionForecaster.generate_forecast(AdmissionUnit.BUET, math_fail_rec)
        self.assertEqual(forecast.tier, ProbabilityTier.INELIGIBLE)
        self.assertEqual(forecast.calibrated_probability, 0.0)

    def test_05_eligibility_gates_medical_and_du(self):
        """Tests medical and Dhaka University admission prerequisite checks."""
        # Medical requires Biology GP >= 4.0 and combined GPA >= 9.0
        med_rec_valid = AcademicRecord(
            ssc_gpa=5.0,
            hsc_gpa=5.0,
            biology_gp=5.0,
            exam_sim_score=80.0  # 80 exam + (5*15 + 5*25 = 200 GPA) = 280 composite (Safe tier >= 278)
        )
        elig_med = AdmissionForecaster.evaluate_eligibility(AdmissionUnit.MEDICAL, med_rec_valid)
        self.assertTrue(elig_med.is_eligible)

        med_forecast = AdmissionForecaster.generate_forecast(AdmissionUnit.MEDICAL, med_rec_valid)
        self.assertGreater(med_forecast.composite_score, 260.0)
        self.assertEqual(med_forecast.tier, ProbabilityTier.SAFE)

        # Medical with Biology GP 3.5 fails
        med_rec_bio_fail = AcademicRecord(
            ssc_gpa=5.0,
            hsc_gpa=5.0,
            biology_gp=3.5,
            exam_sim_score=75.0
        )
        elig_med_fail = AdmissionForecaster.evaluate_eligibility(AdmissionUnit.MEDICAL, med_rec_bio_fail)
        self.assertFalse(elig_med_fail.is_eligible)
        self.assertTrue(any("Biology" in v for v in elig_med_fail.violations_en))

        # DU Ka requires combined GPA >= 8.0
        du_low_gpa = AcademicRecord(
            ssc_gpa=3.5,
            hsc_gpa=3.5,  # combined = 7.0 < 8.0
            physics_gp=4.0,
            chemistry_gp=4.0,
            exam_sim_score=70.0
        )
        du_elig = AdmissionForecaster.evaluate_eligibility(AdmissionUnit.DU_KA, du_low_gpa)
        self.assertFalse(du_elig.is_eligible)

    def test_06_quota_offsets_and_modulation(self):
        """Tests that quota benefits adjust the effective threshold and elevate chance."""
        rec = AcademicRecord(
            ssc_gpa=5.0,
            hsc_gpa=5.0,
            physics_gp=5.0,
            chemistry_gp=5.0,
            math_gp=5.0,
            exam_sim_score=71.0  # Slightly below BUET median cutoff (74.5)
        )

        gen_forecast = AdmissionForecaster.generate_forecast(
            AdmissionUnit.BUET, rec, quota=QuotaType.GENERAL
        )
        ff_forecast = AdmissionForecaster.generate_forecast(
            AdmissionUnit.BUET, rec, quota=QuotaType.FREEDOM_FIGHTER
        )

        # Freedom fighter cut-off threshold should be 6.5 marks lower
        self.assertEqual(
            ff_forecast.effective_cutoff_threshold,
            round(gen_forecast.effective_cutoff_threshold - 6.5, 2)
        )

        # Probability for FF quota candidate must be significantly higher than general quota
        self.assertGreater(
            ff_forecast.calibrated_probability,
            gen_forecast.calibrated_probability
        )

        # Verify all quota types exist in registry
        self.assertIn(QuotaType.TRIBAL, QUOTA_OFFSETS)
        self.assertIn(QuotaType.SPECIAL_NEEDS, QUOTA_OFFSETS)
        self.assertIn(QuotaType.ENGLISH_MEDIUM, QUOTA_OFFSETS)

    def test_07_merit_rank_range_projection_consistency(self):
        """Ensures predicted merit rank intervals are positive, bounded, and logically ordered."""
        units = [
            AdmissionUnit.BUET,
            AdmissionUnit.DU_KA,
            AdmissionUnit.MEDICAL,
            AdmissionUnit.GST,
        ]
        for unit in units:
            # Top candidate rank range
            rank_min_high, rank_max_high = AdmissionForecaster.estimate_rank_range(
                unit=unit, probability=0.92, is_eligible=True
            )
            self.assertGreaterEqual(rank_min_high, 1)
            self.assertLess(rank_min_high, rank_max_high)

            # Borderline candidate rank range
            rank_min_mid, rank_max_mid = AdmissionForecaster.estimate_rank_range(
                unit=unit, probability=0.45, is_eligible=True
            )
            self.assertGreater(rank_min_mid, rank_min_high)
            self.assertGreater(rank_max_mid, rank_max_high)

            # Ineligible candidate
            rank_min_ineligible, rank_max_ineligible = AdmissionForecaster.estimate_rank_range(
                unit=unit, probability=0.0, is_eligible=False
            )
            self.assertGreater(rank_min_ineligible, UNIT_CONFIGS[unit].total_seats)

    def test_08_asvs_l2_zero_pii_sanitization(self):
        """Ensures request sanitizer strictly rejects any PII keys."""
        # Clean scholastic payload must pass without exception
        clean_payload = {
            "ssc_gpa": 5.0,
            "hsc_gpa": 5.0,
            "physics_gp": 5.0,
            "chemistry_gp": 5.0,
            "math_gp": 5.0,
            "exam_sim_score": 80.0,
            "unit": "BUET",
            "quota": "GENERAL"
        }
        sanitized = AdmissionForecaster.sanitize_request(clean_payload)
        self.assertEqual(sanitized, clean_payload)

        # Leaking payload containing student name or phone must raise PIILeakageDetectedException
        disallowed_tests = [
            {"ssc_gpa": 5.0, "name": "Abdur Rahim"},
            {"ssc_gpa": 5.0, "phone": "+8801711223344"},
            {"ssc_gpa": 5.0, "email": "student@example.com"},
            {"ssc_gpa": 5.0, "nid": "19981234567890"},
            {"ssc_gpa": 5.0, "roll": "102938"},
        ]
        for leaking_dict in disallowed_tests:
            with self.assertRaises(PIILeakageDetectedException):
                AdmissionForecaster.sanitize_request(leaking_dict)

    def test_09_supabase_migration_rls_integrity(self):
        """Validates that migration 006 enforces RLS, auth.uid() isolation, and zero-PII table schema."""
        content = self.migration_sql.read_text(encoding="utf-8")
        self.assertIn("admission_prediction_logs", content)
        self.assertIn("ALTER TABLE public.admission_prediction_logs ENABLE ROW LEVEL SECURITY;", content)
        self.assertIn("ALTER TABLE public.admission_prediction_logs FORCE ROW LEVEL SECURITY;", content)
        self.assertIn("user_id = auth.uid()", content)
        self.assertIn("idx_admission_logs_user_id", content)

    def test_10_frontend_predictor_pure_academic_styling(self):
        """Validates frontend predictor page for Oxford Navy palette, 3D tactile buttons, and Lucide icons."""
        content = self.predictor_tsx.read_text(encoding="utf-8")
        
        # Oxford Navy color
        self.assertIn("#0A2540", content)
        # 3D tactile buttons
        self.assertIn("shadow-[0_4px_0_0_", content)
        self.assertIn("active:translate-y-1", content)
        # Academic Lucide icons
        self.assertIn("GraduationCap", content)
        self.assertIn("Building2", content)
        self.assertIn("Calculator", content)
        self.assertIn("ShieldCheck", content)
        # ASVS L2 Zero-PII mention
        self.assertIn("ASVS L2", content)

        # Admission Hub link integration
        admission_content = self.admission_tsx.read_text(encoding="utf-8")
        self.assertIn("/admission/predictor", admission_content)

    def test_11_historical_cutoff_series_integrity(self):
        """Validates that 10-year historical series spans 2015 to 2025 across all primary institutions."""
        required_units = [
            AdmissionUnit.BUET.value,
            AdmissionUnit.DU_KA.value,
            AdmissionUnit.MEDICAL.value,
            AdmissionUnit.GST.value,
        ]
        for u in required_units:
            series = HISTORICAL_CUTOFF_SERIES.get(u)
            self.assertIsNotNone(series, f"Historical series missing for {u}")
            self.assertIn(2015, series)
            self.assertIn(2020, series)
            self.assertIn(2025, series)
            # Verify values are positive and realistic
            for year, val in series.items():
                self.assertGreater(val, 30.0)


if __name__ == "__main__":
    unittest.main()
