"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Career Skill-to-Job Matching Radar & Recruiter Pipeline
 * TOPIC:     Phase 134 Multi-Dimensional Competency Radar & Sealed CV Applications
 * FILE:      backend/tests/test_phase134_skill_matcher.py
 * PHASE:     Phase 134 - Algorithmic Skill-to-Job Matching Radar
 * PURPOSE:   Automated test suite validating:
 *            1. Developer Architecture Note headers & file presence
 *            2. 5-Axis Competency Radar vector calculations and boundary sanity
 *            3. Cosine similarity percentile job matching and rank ordering
 *            4. Immutable sealed CV snapshot generation and SHA-256 tamper verification
 *            5. Supabase migration 012 Row Level Security and sealed application immutability
 *            6. Frontend SVG radar markup, 3D tactile buttons, and Zero-Emoji compliance
 * STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Immutable CV Snapshots
 */
"""

import math
import os
import re
import unittest
from pathlib import Path

from backend.career.skill_matcher import (
    CompetencyRadar,
    CompetencyRadarEngine,
    InvalidRadarScoreException,
    JobMatchResult,
    JobPosting,
    RadarDimension,
    SealedCVSnapshot,
    SkillMatchingService,
    TamperedCVSnapshotException,
)

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase134SkillMatcher(unittest.TestCase):
    """
    Automated verification suite for Phase 134 Career Skill Matching Radar & Sealed CV Pipeline.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.career_init = cls.root_dir / "backend" / "career" / "__init__.py"
        cls.matcher_py = cls.root_dir / "backend" / "career" / "skill_matcher.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "012_career_skill_matching_rls.sql"
        cls.radar_tsx = cls.root_dir / "frontend" / "src" / "pages" / "career" / "radar.tsx"
        cls.test_py = cls.root_dir / "backend" / "tests" / "test_phase134_skill_matcher.py"

    def test_01_all_phase134_files_exist_with_developer_headers(self):
        """Validates that all Phase 134 core files exist and possess mandatory Developer Architecture Note headers."""
        target_files = [
            self.career_init,
            self.matcher_py,
            self.migration_sql,
            self.radar_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Missing required Phase 134 file: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE:", content, f"Missing Architecture header in {file_path}")
            self.assertIn("Phase 134", content, f"Missing Phase 134 reference in {file_path}")
            self.assertIn("Career Skill-to-Job Matching Radar & Recruiter Pipeline", content, f"Missing module in {file_path}")

    def test_02_zero_emoji_compliance(self):
        """Strictly enforces zero emoji in all created Phase 134 code and migration files."""
        target_files = [
            self.career_init,
            self.matcher_py,
            self.migration_sql,
            self.radar_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(len(matches), 0, f"Emoji violations detected in {file_path}: {matches}")

    def test_03_competency_radar_vector_and_boundary_checks(self):
        """Tests 5-dimensional competency radar vector conversion, overall average, and score bounds."""
        radar = CompetencyRadar(
            student_id="stu_lead_01",
            mathematics=95.0,
            algorithms=90.0,
            olympiads=85.0,
            communication=80.0,
            systems=75.0
        )
        vec = radar.to_vector()
        self.assertEqual(len(vec), 5)
        self.assertEqual(vec, [95.0, 90.0, 85.0, 80.0, 75.0])
        self.assertEqual(radar.overall_score(), 85.0)

        # Invalid score bounds (< 0.0 or > 100.0 or non-finite)
        bad_scores = [-5.0, 105.0, float("nan"), float("inf")]
        for bs in bad_scores:
            with self.assertRaises(InvalidRadarScoreException):
                CompetencyRadar(
                    student_id="stu_bad",
                    mathematics=bs,
                    algorithms=90.0,
                    olympiads=85.0,
                    communication=80.0,
                    systems=75.0
                )

    def test_04_cosine_similarity_calculation(self):
        """Tests mathematical accuracy of 5-dimensional vector cosine similarity."""
        # 1. Identical vectors must yield cosine similarity 1.0
        vec_a = [90.0, 85.0, 80.0, 75.0, 70.0]
        self.assertAlmostEqual(CompetencyRadarEngine.calculate_cosine_similarity(vec_a, vec_a), 1.0, places=5)

        # 2. Scaled vector (same direction) must yield cosine similarity 1.0
        vec_scaled = [45.0, 42.5, 40.0, 37.5, 35.0]
        self.assertAlmostEqual(CompetencyRadarEngine.calculate_cosine_similarity(vec_a, vec_scaled), 1.0, places=5)

        # 3. Orthogonal/Zero vector handling
        vec_zero = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertEqual(CompetencyRadarEngine.calculate_cosine_similarity(vec_a, vec_zero), 0.0)

        # 4. Dimension mismatch
        with self.assertRaises(ValueError):
            CompetencyRadarEngine.calculate_cosine_similarity([1.0, 2.0], [1.0, 2.0, 3.0])

    def test_05_job_matching_ranking_and_diagnostics(self):
        """Verifies candidate ranking across benchmark corporate jobs with strengths and gaps."""
        service = SkillMatchingService()
        quant_candidate = CompetencyRadar(
            student_id="stu_quant_pro",
            mathematics=98.0,
            algorithms=92.0,
            olympiads=95.0,
            communication=75.0,
            systems=70.0
        )

        matches = service.match_all_jobs(quant_candidate)
        self.assertGreaterEqual(len(matches), 4)

        # Quantitative Analyst or STEM Fellow should be the top match
        top_job_id = matches[0].job.job_id
        self.assertIn(top_job_id, ["job_quant_01", "job_stem_intern_04"])
        self.assertGreater(matches[0].match_percentage, 90.0)
        self.assertIn("গণিত ও বিশ্লেষণ", matches[0].strengths)

    def test_06_sealed_cv_snapshot_generation_and_tamper_detection(self):
        """Validates point-in-time SHA-256 sealed CV application generation and cryptographic verification."""
        service = SkillMatchingService()
        cand_radar = CompetencyRadar(
            student_id="stu_sec_01",
            mathematics=94.0,
            algorithms=92.0,
            olympiads=90.0,
            communication=85.0,
            systems=88.0
        )

        cv = service.submit_sealed_cv_application(
            student_id="stu_sec_01",
            job_id="job_ml_02",
            full_name="Mahmudul Hasan",
            institution="BUET",
            verified_gpa=4.00,
            olympiad_achievements=["National Olympiad Gold Medal"],
            radar=cand_radar
        )

        self.assertTrue(cv.snapshot_id.startswith("cv_"))
        self.assertEqual(len(cv.snapshot_hash), 64)  # SHA-256 hex string

        # 1. Authentic CV verification passes
        is_valid, ret_cv = service.verify_sealed_cv(cv.snapshot_id)
        self.assertTrue(is_valid)
        self.assertIsNotNone(ret_cv)

        # 2. Tampered CV (altered verified_gpa) must fail cryptographic verification
        ret_cv.verified_gpa = 3.20
        self.assertFalse(ret_cv.verify_integrity())

        # 3. Tampered CV (altered name) must fail cryptographic verification
        ret_cv.verified_gpa = 4.00
        ret_cv.full_name = "Impostor Name"
        self.assertFalse(ret_cv.verify_integrity())

    def test_07_supabase_migration_012_rls_and_immutability(self):
        """Verifies migration 012 establishes required tables, enforces 100% RLS, and asserts CV immutability."""
        sql_content = self.migration_sql.read_text(encoding="utf-8")

        required_tables = [
            "corporate_job_postings",
            "student_skill_radar_profiles",
            "sealed_job_applications",
            "recruiter_talent_bookmarks",
        ]

        for tbl in required_tables:
            has_table = f"CREATE TABLE IF NOT EXISTS public.{tbl}" in sql_content or f"CREATE TABLE IF NOT EXISTS {tbl}" in sql_content
            self.assertTrue(has_table, f"Missing table creation for {tbl}")
            has_rls = f"ALTER TABLE public.{tbl} ENABLE ROW LEVEL SECURITY;" in sql_content or f"ALTER TABLE {tbl} ENABLE ROW LEVEL SECURITY;" in sql_content
            self.assertTrue(has_rls, f"Missing RLS enablement for {tbl}")

        # Assert immutability on sealed CV applications
        self.assertIn("REVOKE UPDATE, DELETE ON public.sealed_job_applications", sql_content)
        self.assertIn("fn_block_sealed_cv_mutation", sql_content)

    def test_08_frontend_radar_markup_and_styling(self):
        """Validates frontend radar page contains SVG polygon, Oxford Navy palette, and pure Lucide icons."""
        tsx_content = self.radar_tsx.read_text(encoding="utf-8")

        # Color palette & 3D tactile buttons
        self.assertTrue(
            "bg-[#0A2540]" in tsx_content or "bg-[#FAFAF8]" in tsx_content,
            "Missing institutional background/navy palette"
        )
        self.assertTrue("shadow-[0_4px_0_0" in tsx_content, "Missing 3D tactile button styling")

        # SVG Radar elements
        self.assertIn("<svg", tsx_content)
        self.assertIn("<polygon", tsx_content)
        self.assertIn("RADAR_AXIS_LABELS", tsx_content)

        # Lucide vector icons
        expected_icons = ["Briefcase", "ShieldCheck", "CheckCircle2", "Target", "Lock", "Sliders"]
        for icon in expected_icons:
            self.assertIn(icon, tsx_content, f"Missing expected Lucide icon: {icon}")


if __name__ == "__main__":
    unittest.main()
