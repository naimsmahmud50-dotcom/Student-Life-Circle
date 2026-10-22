"""
DEVELOPER ARCHITECTURE NOTE - TEST SUITE:
Phase 75: National Centralized Admission Matrix & Gale-Shapley Stable Matching
Validates 10 core integration scenarios:
1. Program catalog loading and national seat totals
2. Gale-Shapley matching stability and strict envy-freeness
3. Top merit rank candidate 1st preference fulfillment
4. Quota allocation (Freedom Fighter, Tribal, District) and eligibility validation
5. Automated multi-round migration cascade when seats are vacated
6. Admission probability prediction for safe-tier rank profiles
7. Admission probability prediction for high-risk / out-of-range ranks
8. Affirmative action quota multiplier probability elevation
9. REST API match runner endpoint execution
10. REST API probability calculation endpoint execution
"""

import asyncio
import unittest
from backend.app.schemas.admission_matching_schema import (
    QuotaCategoryEnum,
    MatchingRunRequest,
    MigrationSimulationRequest,
    AdmissionProbabilityQueryDTO
)
from backend.app.services.admission_matching_service import (
    AdmissionMatchingService,
    admission_matching_service
)
from backend.app.api.v1.router import (
    run_admission_matching_endpoint,
    calculate_admission_probability_endpoint,
    list_admission_programs_endpoint,
    get_admission_matrix_status_endpoint
)


class TestPhase75AdmissionMatching(unittest.TestCase):
    def setUp(self):
        self.service = admission_matching_service

    def test_program_catalog_and_national_seats(self):
        """Verify 8 benchmark university programs are loaded with seats > 1,000."""
        programs = self.service.get_all_programs()
        self.assertEqual(len(programs), 8)
        total_seats = sum(p.total_seats for p in programs)
        self.assertGreaterEqual(total_seats, 1000)

        prog_ids = [p.program_id for p in programs]
        self.assertIn("BUET_CSE", prog_ids)
        self.assertIn("DMC_MBBS", prog_ids)
        self.assertIn("DU_IBA", prog_ids)

    def test_gale_shapley_matching_stability_and_envy_free(self):
        """Verify Gale-Shapley produces an envy-free matching with 1.00 stability score."""
        res = self.service.run_gale_shapley_matching()
        self.assertEqual(res.stability_score, 1.00)
        self.assertTrue(res.is_envy_free)
        self.assertEqual(res.total_candidates, 12)
        self.assertGreater(res.total_seats_allocated, 0)
        self.assertLess(res.execution_time_ms, 100.0)

    def test_top_merit_preference_satisfaction(self):
        """Verify rank 12 candidate receives their top preference (BUET_CSE)."""
        res = self.service.run_gale_shapley_matching()
        tanvir_alloc = next((a for a in res.allocations if a.candidate_id == "STU-BD-001"), None)
        self.assertIsNotNone(tanvir_alloc)
        self.assertEqual(tanvir_alloc.assigned_program_id, "BUET_CSE")
        self.assertEqual(tanvir_alloc.preference_order, 1)

    def test_quota_allocation_and_affirmative_action(self):
        """Verify candidates with quotas receive appropriate tracking."""
        res = self.service.run_gale_shapley_matching()
        ff_alloc = next((a for a in res.allocations if a.candidate_id == "STU-BD-003"), None)
        self.assertIsNotNone(ff_alloc)
        self.assertEqual(ff_alloc.quota_applied, "FREEDOM_FIGHTER")

        tribal_alloc = next((a for a in res.allocations if a.candidate_id == "STU-BD-006"), None)
        self.assertIsNotNone(tribal_alloc)
        self.assertEqual(tribal_alloc.quota_applied, "TRIBAL_ETHNIC")

    def test_migration_cascade_simulation(self):
        """Verify vacating candidates trigger migration promotions for downstream students."""
        req = MigrationSimulationRequest(vacating_candidate_ids=["STU-BD-001"])
        res = self.service.simulate_migration_cascade(req)
        self.assertEqual(res.vacated_seats_count, 1)
        self.assertGreater(len(res.migration_steps), 0)

        # First step should log the vacated seat
        first_step = res.migration_steps[0]
        self.assertEqual(first_step.candidate_id, "STU-BD-001")
        self.assertEqual(first_step.new_program_id, "VACATED")

    def test_admission_probability_safe_tier(self):
        """Verify high merit rank yields SAFE risk tier with probability >= 0.85."""
        query = AdmissionProbabilityQueryDTO(
            candidate_merit_rank=25,
            target_program_id="BUET_CSE",
            quota_category=QuotaCategoryEnum.GENERAL
        )
        res = self.service.calculate_admission_probability(query)
        self.assertGreaterEqual(res.admission_probability, 0.85)
        self.assertEqual(res.risk_tier, "SAFE")

    def test_admission_probability_high_risk_tier(self):
        """Verify rank far exceeding cutoff yields HIGH_RISK tier with probability < 0.20."""
        query = AdmissionProbabilityQueryDTO(
            candidate_merit_rank=950,
            target_program_id="BUET_CSE",
            quota_category=QuotaCategoryEnum.GENERAL
        )
        res = self.service.calculate_admission_probability(query)
        self.assertLess(res.admission_probability, 0.20)
        self.assertEqual(res.risk_tier, "HIGH_RISK")

    def test_quota_multiplier_probability_boost(self):
        """Verify affirmative action quota category increases probability for borderline ranks."""
        borderline_rank = 150
        q_gen = AdmissionProbabilityQueryDTO(
            candidate_merit_rank=borderline_rank,
            target_program_id="BUET_CSE",
            quota_category=QuotaCategoryEnum.GENERAL
        )
        res_gen = self.service.calculate_admission_probability(q_gen)

        q_ff = AdmissionProbabilityQueryDTO(
            candidate_merit_rank=borderline_rank,
            target_program_id="BUET_CSE",
            quota_category=QuotaCategoryEnum.FREEDOM_FIGHTER
        )
        res_ff = self.service.calculate_admission_probability(q_ff)

        self.assertGreater(res_ff.admission_probability, res_gen.admission_probability)

    def test_router_match_run_endpoint(self):
        """Verify router endpoint executes matching asynchronously."""
        res = asyncio.run(run_admission_matching_endpoint(None))
        self.assertEqual(res.stability_score, 1.00)
        self.assertTrue(res.is_envy_free)

    def test_router_probability_calculate_endpoint(self):
        """Verify router endpoint calculates probability asynchronously."""
        query = AdmissionProbabilityQueryDTO(
            candidate_merit_rank=80,
            target_program_id="DU_CSE",
            quota_category=QuotaCategoryEnum.GENERAL
        )
        res = asyncio.run(calculate_admission_probability_endpoint(query))
        self.assertEqual(res.target_program_id, "DU_CSE")
        self.assertGreaterEqual(res.admission_probability, 0.50)


if __name__ == "__main__":
    unittest.main()
