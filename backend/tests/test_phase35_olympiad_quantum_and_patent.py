"""
Unit, Integration, and Security Test Suite: Phase 35
Verifies:
1. NationalOlympiadArenaService (STEM Olympiads BdMO/BdPhO/BdIO/BDBO, grading rubrics, penalty timers, percentiles)
2. SemiconductorQuantumSandboxService (PN junction depletion dynamics, built-in potential, 1D Quantum Well wave states)
3. UniversityPatentRegistryService (patent disclosures, claims, SHA-256 cryptographic seals, prior art novelty analyzer)
4. Section 34 REST Routes in router.py
"""

import unittest
from backend.app.services.national_olympiad_arena_service import (
    NationalOlympiadArenaService,
    national_olympiad_arena_service
)
from backend.app.services.semiconductor_quantum_sandbox_service import (
    SemiconductorQuantumSandboxService,
    semiconductor_quantum_sandbox_service
)
from backend.app.services.university_patent_registry_service import (
    UniversityPatentRegistryService,
    university_patent_registry_service
)
from backend.app.schemas.olympiad_quantum_and_patent_schema import (
    OlympiadSubmissionRequest,
    PnJunctionSimRequest,
    QuantumWellSimRequest,
    PatentDisclosureFileRequest,
    PatentPriorArtSearchRequest
)
from backend.app.api.v1.router import (
    list_olympiad_problems,
    submit_olympiad_solution,
    get_olympiad_leaderboard,
    simulate_semiconductor_pn_junction,
    simulate_quantum_well,
    file_university_patent_disclosure,
    get_university_patent_disclosure,
    search_patent_prior_art
)


class TestPhase35OlympiadQuantumAndPatent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.olympiad_service = NationalOlympiadArenaService()
        self.semi_service = SemiconductorQuantumSandboxService()
        self.patent_service = UniversityPatentRegistryService()

    # -------------------------------------------------------------------------
    # 1. NationalOlympiadArenaService Tests
    # -------------------------------------------------------------------------

    def test_list_problems_and_filters(self):
        all_probs = self.olympiad_service.list_problems()
        self.assertGreaterEqual(len(all_probs), 4)

        bdmo_probs = self.olympiad_service.list_problems(competition="BDMO")
        self.assertGreaterEqual(len(bdmo_probs), 1)
        self.assertEqual(bdmo_probs[0]["competition"], "BDMO")

        sec_probs = self.olympiad_service.list_problems(division="SECONDARY")
        self.assertGreaterEqual(len(sec_probs), 1)

    def test_get_problem_success(self):
        prob = self.olympiad_service.get_problem("OLYMP-BDMO-2024-01")
        self.assertEqual(prob["problem_id"], "OLYMP-BDMO-2024-01")
        self.assertIn("Gaussian", prob["sample_hint"])

    def test_get_nonexistent_problem_raises_error(self):
        with self.assertRaises(ValueError):
            self.olympiad_service.get_problem("NONEXISTENT-PROB-999")

    def test_submit_solution_fully_correct(self):
        res = self.olympiad_service.submit_solution(
            problem_id="OLYMP-BDMO-2024-01",
            student_id="student-bdmo-01",
            student_name="Naimur Rahman",
            solution_text="Using prime factorization 2025 = 3^4 * 5^2 over Gaussian integers mod 4...",
            numerical_answer=8.0,
            time_spent_seconds=120
        )
        self.assertTrue(res["is_correct"])
        self.assertGreaterEqual(res["net_score"], 8.0)
        self.assertEqual(res["time_penalty"], 0.0)

    def test_submit_solution_partial_credit(self):
        # Incorrect numerical answer but correct keyword derivation
        res = self.olympiad_service.submit_solution(
            problem_id="OLYMP-BDMO-2024-01",
            student_id="student-bdmo-02",
            student_name="Tariq Hasan",
            solution_text="We consider the prime factorization and Gaussian integers...",
            numerical_answer=12.0,  # Incorrect count
            time_spent_seconds=150
        )
        self.assertFalse(res["is_correct"])
        self.assertGreater(res["net_score"], 0.0)

    def test_submit_solution_short_proof_raises_error(self):
        with self.assertRaises(ValueError):
            self.olympiad_service.submit_solution(
                problem_id="OLYMP-BDMO-2024-01",
                student_id="student-test",
                student_name="Test",
                solution_text="Too short",
                numerical_answer=8.0
            )

    def test_submit_solution_time_penalty_applied(self):
        res = self.olympiad_service.submit_solution(
            problem_id="OLYMP-BDMO-2024-01",
            student_id="student-slow",
            student_name="Slow Solver",
            solution_text="Factorization method using Gaussian primes.",
            numerical_answer=8.0,
            time_spent_seconds=300  # 120s over standard limit -> penalty = 120 * 0.005 = 0.60
        )
        self.assertEqual(res["time_penalty"], 0.6)
        self.assertLess(res["net_score"], res["fractional_score"])

    def test_get_leaderboard(self):
        board = self.olympiad_service.get_leaderboard("BDMO")
        self.assertEqual(board["competition"], "BDMO")
        self.assertGreaterEqual(board["total_participants"], 3)
        self.assertEqual(board["entries"][0]["rank"], 1)

    # -------------------------------------------------------------------------
    # 2. SemiconductorQuantumSandboxService Tests
    # -------------------------------------------------------------------------

    def test_simulate_pn_junction_silicon(self):
        res = self.semi_service.simulate_pn_junction(
            semiconductor_material="SILICON",
            acceptor_doping_na_cm3=1e16,
            donor_doping_nd_cm3=1e16,
            reverse_bias_voltage_v=0.0,
            temperature_kelvin=300.0
        )
        self.assertEqual(res["material"], "SILICON")
        self.assertGreater(res["built_in_potential_v"], 0.6)
        self.assertLess(res["built_in_potential_v"], 0.8)
        self.assertGreater(res["depletion_width_um"], 0.3)
        self.assertGreater(res["peak_electric_field_kv_cm"], 10.0)
        self.assertEqual(len(res["spatial_electric_field_profile"]), 21)

    def test_simulate_pn_junction_reverse_bias_widening(self):
        zero_bias = self.semi_service.simulate_pn_junction(reverse_bias_voltage_v=0.0)
        reverse_bias = self.semi_service.simulate_pn_junction(reverse_bias_voltage_v=5.0)
        self.assertGreater(reverse_bias["depletion_width_um"], zero_bias["depletion_width_um"])
        self.assertGreater(reverse_bias["peak_electric_field_kv_cm"], zero_bias["peak_electric_field_kv_cm"])

    def test_simulate_pn_junction_zero_doping_clamp(self):
        # Pass 0.0 and negative values to verify defensive clamping
        res = self.semi_service.simulate_pn_junction(
            acceptor_doping_na_cm3=0.0,
            donor_doping_nd_cm3=-10.0,
            temperature_kelvin=0.0
        )
        self.assertGreater(res["built_in_potential_v"], 0.0)
        self.assertGreater(res["depletion_width_um"], 0.0)

    def test_simulate_quantum_well_gaas(self):
        res = self.semi_service.simulate_quantum_well(
            well_width_nm=5.0,
            particle_mass_ratio=0.067,
            state_levels=3
        )
        self.assertEqual(res["well_width_nm"], 5.0)
        self.assertEqual(len(res["energy_levels"]), 3)
        e1 = res["energy_levels"][0]["energy_ev"]
        e2 = res["energy_levels"][1]["energy_ev"]
        e3 = res["energy_levels"][2]["energy_ev"]
        self.assertAlmostEqual(e2 / e1, 4.0, delta=0.05)
        self.assertAlmostEqual(e3 / e1, 9.0, delta=0.1)
        self.assertEqual(len(res["wavefunction_samples"]), 25)

    def test_simulate_quantum_well_zero_width_clamp(self):
        res = self.semi_service.simulate_quantum_well(well_width_nm=0.0)
        self.assertEqual(res["well_width_nm"], 0.5)

    # -------------------------------------------------------------------------
    # 3. UniversityPatentRegistryService Tests
    # -------------------------------------------------------------------------

    def test_seed_patents_loaded(self):
        patents = self.patent_service.list_all_patents()
        self.assertGreaterEqual(len(patents), 3)

    def test_file_patent_disclosure_success(self):
        res = self.patent_service.file_patent_disclosure(
            title="Photonic Synaptic Memory Arrays Using Phase-Change Metamaterials",
            abstract="Integrated optical non-volatile memory cell achieving multi-bit storage for ultra-low latency optical tensor acceleration.",
            inventors=["Dr. Feroz Ahmed", "Tahsin Rahman"],
            institution="BUET",
            ipc_classification="G02F 1/01",
            claims=["An optical memory cell comprising a chalcogenide waveguide core."]
        )
        self.assertTrue(res["patent_id"].startswith("PAT-BUET"))
        self.assertTrue(res["cryptographic_disclosure_seal"].startswith("SEAL-SHA256-BUET"))
        self.assertGreaterEqual(res["novelty_score"], 60.0)

    def test_file_patent_empty_fields_raises_error(self):
        with self.assertRaises(ValueError):
            self.patent_service.file_patent_disclosure(
                title="",
                abstract="Some abstract",
                inventors=["Inventor 1"],
                institution="DU"
            )

    def test_get_patent_disclosure_success(self):
        pat = self.patent_service.get_patent_disclosure("PAT-BUET-2024-001")
        self.assertEqual(pat["patent_id"], "PAT-BUET-2024-001")
        self.assertEqual(pat["institution"], "BUET")

    def test_get_nonexistent_patent_raises_error(self):
        with self.assertRaises(ValueError):
            self.patent_service.get_patent_disclosure("INVALID-PAT-000")

    def test_search_prior_art_similar_match(self):
        query = "Spiking neural processor continuous acoustic wavelet speech features"
        res = self.patent_service.search_prior_art(query)
        self.assertGreater(len(res["matches"]), 0)
        self.assertEqual(res["matches"][0]["patent_id"], "PAT-BUET-2024-001")

    def test_search_prior_art_novel(self):
        query = "Topological superconducting qubits on twisting bilayer graphene lattices"
        res = self.patent_service.search_prior_art(query)
        self.assertTrue(res["is_patentable_novel"])
        self.assertGreaterEqual(res["average_novelty_score"], 80.0)

    def test_search_prior_art_short_query_raises_error(self):
        with self.assertRaises(ValueError):
            self.patent_service.search_prior_art("Ab")

    # -------------------------------------------------------------------------
    # 4. Section 34 REST Routes Tests
    # -------------------------------------------------------------------------

    async def test_route_list_olympiad_problems(self):
        probs = await list_olympiad_problems(competition="BDMO")
        self.assertGreater(len(probs), 0)

    async def test_route_submit_olympiad_solution(self):
        payload = OlympiadSubmissionRequest(
            problem_id="OLYMP-BDMO-2024-01",
            student_id="student-api-01",
            student_name="Naimur Rahman",
            solution_text="Full mathematical derivation over prime factorization Gaussian integers.",
            numerical_answer=8.0,
            time_spent_seconds=100
        )
        res = await submit_olympiad_solution(payload)
        self.assertTrue(res["is_correct"])

    async def test_route_get_olympiad_leaderboard(self):
        res = await get_olympiad_leaderboard(competition="BDMO")
        self.assertEqual(res["competition"], "BDMO")
        self.assertGreater(len(res["entries"]), 0)

    async def test_route_simulate_pn_junction(self):
        payload = PnJunctionSimRequest(semiconductor_material="SILICON", reverse_bias_voltage_v=2.0)
        res = await simulate_semiconductor_pn_junction(payload)
        self.assertEqual(res["material"], "SILICON")
        self.assertGreater(res["depletion_width_um"], 0.4)

    async def test_route_simulate_quantum_well(self):
        payload = QuantumWellSimRequest(well_width_nm=4.0, state_levels=3)
        res = await simulate_quantum_well(payload)
        self.assertEqual(len(res["energy_levels"]), 3)

    async def test_route_patent_disclosures(self):
        file_payload = PatentDisclosureFileRequest(
            title="Bio-Compatible Micro-Capacitor Array",
            abstract="Implantable energy storage array with sub-micron titanium oxide dielectric.",
            inventors=["Dr. S. K. Roy"],
            institution="DMC",
            ipc_classification="A61B 5/00"
        )
        filed = await file_university_patent_disclosure(file_payload)
        self.assertTrue(filed["patent_id"].startswith("PAT-DMC"))

        fetched = await get_university_patent_disclosure(filed["patent_id"])
        self.assertEqual(fetched["patent_id"], filed["patent_id"])

        search_payload = PatentPriorArtSearchRequest(search_query="Implantable titanium oxide micro capacitor")
        search_res = await search_patent_prior_art(search_payload)
        self.assertIn("matches", search_res)


if __name__ == '__main__':
    unittest.main()
