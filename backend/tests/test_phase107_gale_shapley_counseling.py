"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite
TOPIC:     Phase 107 Centralized Admission Counseling & Gale-Shapley Tests
FILE:      backend/tests/test_phase107_gale_shapley_counseling.py
PHASE:     Phase 107 - Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
PURPOSE:   Asserts Gale-Shapley student-proposing deferred acceptance stability (zero blocking pairs),
           quota partitioning and automatic general spillover, multi-stage seat migration cascading,
           REST API endpoints, and strict zero-emoji governance.
STANDARDS: Pareto-Optimal Deferred Acceptance, Quota Spillover Balancing, Zero-Emoji, UI/UX Pro Max
"""

import asyncio
import json
import os
import unittest
from pathlib import Path

from backend.app.services.gale_shapley_counseling_service import (
    GaleShapleyCounselingService,
    gale_shapley_counseling_service
)
from backend.app.api.v1.endpoints.counseling import (
    run_gale_shapley_admission_match,
    simulate_admission_migration_cascade,
    list_counseling_programs,
    predict_candidate_admission_probability
)
from backend.app.core.fastapi_shim import HTTPException


def is_emoji_char(char: str) -> bool:
    """Detects whether a character is a decorative unicode emoji."""
    code = ord(char)
    return (
        0x1F600 <= code <= 0x1F64F or
        0x1F300 <= code <= 0x1F5FF or
        0x1F680 <= code <= 0x1F6FF or
        0x1F900 <= code <= 0x1F9FF or
        0x1FA70 <= code <= 0x1FAFF or
        0x2600 <= code <= 0x26FF or
        0x2700 <= code <= 0x27BF
    )


def contains_emoji(text: str) -> bool:
    """Returns True if string contains any decorative unicode emoji."""
    return any(is_emoji_char(c) for c in text)


class TestPhase107GaleShapleyCounseling(unittest.TestCase):
    """
    Automated verification suite for Phase 107 Centralized Admission Counseling & Gale-Shapley Hub.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.service_path = cls.repo_root / "backend" / "app" / "services" / "gale_shapley_counseling_service.py"
        cls.endpoint_path = cls.repo_root / "backend" / "app" / "api" / "v1" / "endpoints" / "counseling.py"
        cls.matrix_path = cls.repo_root / "frontend" / "src" / "components" / "admission" / "AdmissionCounselingMatrix.tsx"
        cls.cascade_path = cls.repo_root / "frontend" / "src" / "components" / "admission" / "MigrationCascadeVisualizer.tsx"
        cls.page_path = cls.repo_root / "frontend" / "src" / "pages" / "counseling.tsx"
        cls.tasks_path = cls.repo_root / "specs" / "011-phase107-gale-shapley-counseling" / "tasks.md"

    def test_01_gale_shapley_deferred_acceptance_mathematical_stability(self):
        """Verifies that Student-Proposing Gale-Shapley generates 100% stable, envy-free matching."""
        # 4 students competing for 2 programs with capacity 1 each
        test_programs = {
            "PROG_A": {
                "program_id": "PROG_A",
                "institution_name": "University A",
                "department_name": "Dept A",
                "total_capacity": 1,
                "quota_capacities": {"GENERAL": 1},
                "historical_cutoff_rank": 10
            },
            "PROG_B": {
                "program_id": "PROG_B",
                "institution_name": "University B",
                "department_name": "Dept B",
                "total_capacity": 1,
                "quota_capacities": {"GENERAL": 1},
                "historical_cutoff_rank": 20
            }
        }

        # S1 (Rank 1) prefers PROG_A, then PROG_B
        # S2 (Rank 2) prefers PROG_A, then PROG_B
        # S3 (Rank 3) prefers PROG_B, then PROG_A
        test_students = [
            {"student_id": "s1", "name": "Student 1", "merit_rank": 1, "preferences": ["PROG_A", "PROG_B"]},
            {"student_id": "s2", "name": "Student 2", "merit_rank": 2, "preferences": ["PROG_A", "PROG_B"]},
            {"student_id": "s3", "name": "Student 3", "merit_rank": 3, "preferences": ["PROG_B", "PROG_A"]},
        ]

        result = gale_shapley_counseling_service.run_matching(test_students, test_programs)
        self.assertTrue(result["success"])
        self.assertTrue(result["is_stable"])
        self.assertEqual(result["blocking_pairs_count"], 0)

        # S1 has best rank, must get first choice PROG_A
        alloc_map = {a["student_id"]: a["matched_program"] for a in result["allocations"]}
        self.assertEqual(alloc_map["s1"], "PROG_A")
        # S2 rejected from PROG_A, proposes to PROG_B and beats S3 because Rank 2 < Rank 3
        self.assertEqual(alloc_map["s2"], "PROG_B")
        # S3 is unmatched
        self.assertIsNone(alloc_map["s3"])

    def test_02_quota_partitioning_and_automatic_general_spillover(self):
        """Verifies that unfilled affirmative action quota seats automatically spill over into General pool."""
        test_programs = {
            "ELITE_ENG": {
                "program_id": "ELITE_ENG",
                "institution_name": "Top Engineering",
                "department_name": "CSE",
                "total_capacity": 3,
                "quota_capacities": {
                    "GENERAL": 1,
                    "FREEDOM_FIGHTER": 2  # 2 seats reserved
                },
                "historical_cutoff_rank": 50
            }
        }

        # 3 students apply:
        # S1: General, Rank 1
        # S2: General, Rank 2
        # S3: General, Rank 3
        # (Zero Freedom Fighter applicants!)
        students = [
            {"student_id": "s1", "merit_rank": 1, "quotas": ["GENERAL"], "preferences": ["ELITE_ENG"]},
            {"student_id": "s2", "merit_rank": 2, "quotas": ["GENERAL"], "preferences": ["ELITE_ENG"]},
            {"student_id": "s3", "merit_rank": 3, "quotas": ["GENERAL"], "preferences": ["ELITE_ENG"]},
        ]

        result = gale_shapley_counseling_service.run_matching(students, test_programs)
        self.assertTrue(result["is_stable"])
        # All 2 unfilled FF seats must spill over into General, so all 3 students are matched!
        self.assertEqual(result["total_spillover_seats"], 2)
        self.assertEqual(result["matched_students"], 3)
        self.assertEqual(result["unmatched_students"], 0)

        alloc_map = {a["student_id"]: a["matched_quota"] for a in result["allocations"]}
        self.assertEqual(alloc_map["s1"], "GENERAL")
        self.assertEqual(alloc_map["s2"], "GENERAL_SPILLOVER")
        self.assertEqual(alloc_map["s3"], "GENERAL_SPILLOVER")

    def test_03_multi_stage_seat_migration_cascade_simulation(self):
        """Verifies upward seat reallocation cascades across multiple rounds after top candidate withdrawals."""
        test_programs = {
            "BUET_CSE": {
                "program_id": "BUET_CSE",
                "total_capacity": 1,
                "quota_capacities": {"GENERAL": 1},
                "historical_cutoff_rank": 10
            },
            "DU_CSE": {
                "program_id": "DU_CSE",
                "total_capacity": 1,
                "quota_capacities": {"GENERAL": 1},
                "historical_cutoff_rank": 20
            },
            "JU_CSE": {
                "program_id": "JU_CSE",
                "total_capacity": 1,
                "quota_capacities": {"GENERAL": 1},
                "historical_cutoff_rank": 30
            }
        }

        # S1 (Rank 1): BUET_CSE
        # S2 (Rank 2): BUET_CSE, then DU_CSE
        # S3 (Rank 3): DU_CSE, then JU_CSE
        # S4 (Rank 4): JU_CSE
        students = [
            {"student_id": "s1", "name": "Student 1", "merit_rank": 1, "preferences": ["BUET_CSE"]},
            {"student_id": "s2", "name": "Student 2", "merit_rank": 2, "preferences": ["BUET_CSE", "DU_CSE"]},
            {"student_id": "s3", "name": "Student 3", "merit_rank": 3, "preferences": ["DU_CSE", "JU_CSE"]},
            {"student_id": "s4", "name": "Student 4", "merit_rank": 4, "preferences": ["JU_CSE"]},
        ]

        # S1 cancels their seat in BUET (e.g. going abroad or medical)
        cascade = gale_shapley_counseling_service.simulate_migration_cascade(
            students=students,
            programs=test_programs,
            cancellations=["s1"],
            num_rounds=2
        )

        self.assertTrue(cascade["success"])
        self.assertEqual(cascade["total_rounds"], 2)
        self.assertGreater(cascade["total_upward_migrations"], 0)

        # In Round 2:
        # S2 migrates from DU_CSE to BUET_CSE
        # S3 migrates from JU_CSE to DU_CSE
        # S4 gets admitted to JU_CSE
        r2 = cascade["rounds"][1]
        r2_allocs = {a["student_id"]: a["matched_program"] for a in r2["allocations"]}
        self.assertEqual(r2_allocs["s2"], "BUET_CSE")
        self.assertEqual(r2_allocs["s3"], "DU_CSE")
        self.assertEqual(r2_allocs["s4"], "JU_CSE")

    def test_04_admission_probability_predictor(self):
        """Verifies probability scores and tier classifications across merit rank spectrum."""
        svc = gale_shapley_counseling_service

        # BUET CSE historical cutoff is 165
        # Rank 50 is well within top 70% -> HIGH tier
        pred_high = svc.predict_admission_probability(merit_rank=50, target_program_id="BUET_CSE")
        self.assertEqual(pred_high["tier"], "HIGH")
        self.assertGreaterEqual(pred_high["probability_percent"], 85.0)

        # Rank 150 is between 70% and 100% -> MODERATE tier
        pred_mod = svc.predict_admission_probability(merit_rank=150, target_program_id="BUET_CSE")
        self.assertEqual(pred_mod["tier"], "MODERATE")
        self.assertTrue(55.0 <= pred_mod["probability_percent"] <= 85.0)

        # Rank 200 is between 100% and 135% -> AMBITIOUS tier
        pred_amb = svc.predict_admission_probability(merit_rank=200, target_program_id="BUET_CSE")
        self.assertEqual(pred_amb["tier"], "AMBITIOUS")

        # Rank 1000 is far beyond cutoff -> LOW tier
        pred_low = svc.predict_admission_probability(merit_rank=1000, target_program_id="BUET_CSE")
        self.assertEqual(pred_low["tier"], "LOW")

        # Quota multiplier expands effective cutoff
        pred_quota = svc.predict_admission_probability(
            merit_rank=200,
            target_program_id="BUET_CSE",
            quota="FREEDOM_FIGHTER"
        )
        self.assertGreater(pred_quota["effective_cutoff_rank"], 165)

    async def _test_async_endpoints(self):
        """Helper to run async endpoint unit tests."""
        def extract_content(res):
            if hasattr(res, "body"):
                return json.loads(res.body.decode("utf-8"))
            return getattr(res, "content", {})

        # 1. Run matching endpoint
        match_payload = {
            "students": [
                {"student_id": "s_1", "merit_rank": 10, "preferences": ["BUET_CSE", "DU_CSE"]},
                {"student_id": "s_2", "merit_rank": 20, "preferences": ["DU_CSE"]}
            ]
        }
        match_res = await run_gale_shapley_admission_match(match_payload)
        self.assertEqual(match_res.status_code, 200)
        match_data = extract_content(match_res)
        self.assertTrue(match_data["success"])
        self.assertTrue(match_data["is_stable"])

        # 2. Invalid students list raises 400
        with self.assertRaises(HTTPException) as cm:
            await run_gale_shapley_admission_match({"students": []})
        self.assertEqual(cm.exception.status_code, 400)

        # 3. Migration simulation endpoint
        sim_payload = {
            "students": [
                {"student_id": "s_1", "merit_rank": 10, "preferences": ["BUET_CSE"]},
                {"student_id": "s_2", "merit_rank": 20, "preferences": ["BUET_CSE", "DU_CSE"]}
            ],
            "cancellations": ["s_1"],
            "num_rounds": 2
        }
        sim_res = await simulate_admission_migration_cascade(sim_payload)
        self.assertEqual(sim_res.status_code, 200)
        sim_data = extract_content(sim_res)
        self.assertTrue(sim_data["success"])
        self.assertEqual(sim_data["total_rounds"], 2)

        # 4. List programs endpoint
        prog_res = await list_counseling_programs(cluster=None)
        self.assertEqual(prog_res.status_code, 200)
        prog_data = extract_content(prog_res)
        self.assertGreaterEqual(prog_data["total"], 6)

        # 5. Predict probability endpoint
        pred_payload = {
            "merit_rank": 120,
            "target_program_id": "BUET_CSE",
            "quota": "GENERAL"
        }
        pred_res = await predict_candidate_admission_probability(pred_payload)
        self.assertEqual(pred_res.status_code, 200)
        pred_data = extract_content(pred_res)
        self.assertIn("probability_percent", pred_data)

        # 6. Predict probability with missing fields raises 400
        with self.assertRaises(HTTPException) as cm:
            await predict_candidate_admission_probability({"merit_rank": None})
        self.assertEqual(cm.exception.status_code, 400)

    def test_05_rest_api_endpoints_match_migrate_predict(self):
        """Verifies Phase 107 REST API endpoints through direct async invocation."""
        asyncio.run(self._test_async_endpoints())

    def test_06_developer_architecture_note_and_strict_zero_emoji(self):
        """Verifies Developer Architecture Note headers and strict zero-emoji governance across Phase 107 files."""
        phase107_files = [
            self.service_path,
            self.endpoint_path,
            self.matrix_path,
            self.cascade_path,
            self.page_path,
            self.tasks_path,
            Path(__file__)
        ]

        for file_path in phase107_files:
            self.assertTrue(file_path.exists(), f"File does not exist: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"Missing Developer Architecture Note in {file_path.name}"
            )
            self.assertIn(
                "Phase 107",
                content,
                f"Missing Phase 107 reference in {file_path.name}"
            )
            self.assertFalse(
                contains_emoji(content),
                f"Strict Zero-Emoji violation detected in {file_path.name}"
            )


if __name__ == "__main__":
    unittest.main()
