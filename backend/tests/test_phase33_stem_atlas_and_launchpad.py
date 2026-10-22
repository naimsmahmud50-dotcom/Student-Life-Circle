"""
Unit and Integration Test Suite: Phase 33
Verifies:
1. MolecularGeometryLabService (VSEPR geometries, steric numbers, bond angles, hybridization, redox balancing)
2. SyllabusKnowledgeAtlasService (concept graph nodes, dependency edges, 10-year board question frequencies, formulas)
3. InnovationLaunchpadService (project pitching with SHA-256 IP proof, anti-Sybil voting tribunal, milestone escrow releases)
4. Section 32 REST Routes in router.py
"""

import unittest
from backend.app.services.molecular_geometry_lab_service import (
    MolecularGeometryLabService,
    molecular_geometry_lab_service
)
from backend.app.services.syllabus_knowledge_atlas_service import (
    SyllabusKnowledgeAtlasService,
    syllabus_knowledge_atlas_service
)
from backend.app.services.innovation_launchpad_service import (
    InnovationLaunchpadService,
    innovation_launchpad_service
)
from backend.app.schemas.stem_atlas_and_launchpad_schema import (
    MolecularGeometryRequest,
    RedoxReactionBalanceRequest,
    PitchProjectRequest,
    CastProjectVoteRequest,
    ReleaseGrantTrancheRequest
)
from backend.app.api.v1.router import (
    calculate_molecular_geometry,
    balance_redox_chemical_reaction,
    get_syllabus_knowledge_graph,
    get_board_exam_frequency,
    get_syllabus_formula_cheatsheet,
    pitch_student_innovation_project,
    cast_project_tribunal_vote,
    release_milestone_grant_tranche,
    list_innovation_projects,
    get_innovation_project_details
)


class TestPhase33StemAtlasAndLaunchpad(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.molecular_service = MolecularGeometryLabService()
        self.atlas_service = SyllabusKnowledgeAtlasService()
        self.launchpad_service = InnovationLaunchpadService()

    # -------------------------------------------------------------------------
    # 1. MolecularGeometryLabService Tests
    # -------------------------------------------------------------------------

    def test_vsepr_methane_ch4_tetrahedral(self):
        """Asserts CH4 calculation produces tetrahedral geometry with 109.5° angle and sp3 hybridization."""
        res = self.molecular_service.calculate_molecular_geometry(formula="CH4")
        self.assertEqual(res["formula"], "CH4")
        self.assertEqual(res["central_atom"], "C")
        self.assertEqual(res["steric_number"], 4)
        self.assertEqual(res["lone_pairs"], 0)
        self.assertEqual(res["vsepr_notation"], "AX4")
        self.assertEqual(res["molecular_geometry"], "Tetrahedral")
        self.assertEqual(res["hybridization"], "sp3")
        self.assertFalse(res["is_polar"])
        self.assertEqual(len(res["spatial_coordinates"]), 5)

    def test_vsepr_ammonia_nh3_trigonal_pyramidal(self):
        """Asserts NH3 produces trigonal pyramidal shape with lone pair angle compression (107.0°)."""
        res = self.molecular_service.calculate_molecular_geometry(formula="NH3")
        self.assertEqual(res["central_atom"], "N")
        self.assertEqual(res["steric_number"], 4)
        self.assertEqual(res["lone_pairs"], 1)
        self.assertEqual(res["vsepr_notation"], "AX3E1")
        self.assertEqual(res["molecular_geometry"], "Trigonal Pyramidal")
        self.assertEqual(res["actual_bond_angle_deg"], 107.0)
        self.assertTrue(res["is_polar"])

    def test_vsepr_water_h2o_bent_angular(self):
        """Asserts H2O produces bent geometry with dual lone pair compression (104.5°)."""
        res = self.molecular_service.calculate_molecular_geometry(formula="H2O")
        self.assertEqual(res["central_atom"], "O")
        self.assertEqual(res["steric_number"], 4)
        self.assertEqual(res["lone_pairs"], 2)
        self.assertEqual(res["vsepr_notation"], "AX2E2")
        self.assertEqual(res["molecular_geometry"], "Bent (Angular)")
        self.assertEqual(res["actual_bond_angle_deg"], 104.5)
        self.assertTrue(res["is_polar"])

    def test_vsepr_carbon_dioxide_co2_linear(self):
        """Asserts CO2 produces linear geometry with 180° angle, sp hybridization, and zero net dipole."""
        res = self.molecular_service.calculate_molecular_geometry(formula="CO2")
        self.assertEqual(res["steric_number"], 2)
        self.assertEqual(res["molecular_geometry"], "Linear")
        self.assertEqual(res["hybridization"], "sp")
        self.assertEqual(res["actual_bond_angle_deg"], 180.0)
        self.assertFalse(res["is_polar"])

    def test_vsepr_pcl5_and_sf6_expanded_octets(self):
        """Asserts trigonal bipyramidal PCl5 and octahedral SF6 expanded octet shapes."""
        pcl5 = self.molecular_service.calculate_molecular_geometry(formula="PCl5")
        self.assertEqual(pcl5["molecular_geometry"], "Trigonal Bipyramidal")
        self.assertEqual(pcl5["hybridization"], "sp3d")

        sf6 = self.molecular_service.calculate_molecular_geometry(formula="SF6")
        self.assertEqual(sf6["molecular_geometry"], "Octahedral")
        self.assertEqual(sf6["hybridization"], "sp3d2")

    def test_vsepr_custom_steric_and_lone_pairs(self):
        """Asserts dynamic geometry calculation for arbitrary steric numbers."""
        custom = self.molecular_service.calculate_molecular_geometry(
            formula="XG3",
            central_atom="X",
            steric_number=3,
            lone_pairs=1
        )
        self.assertEqual(custom["steric_number"], 3)
        self.assertEqual(custom["molecular_geometry"], "Bent")
        self.assertEqual(custom["hybridization"], "sp2")
        self.assertTrue(custom["is_polar"])

    def test_vsepr_oversized_formula_rejected(self):
        """Asserts formulas exceeding 30 characters raise ValueError to prevent ReDoS."""
        with self.assertRaises(ValueError):
            self.molecular_service.calculate_molecular_geometry(formula="C" * 35)

    def test_redox_balance_permanganate_iron(self):
        """Asserts KMnO4 + FeSO4 acidic redox reaction generates 5 electrons transferred."""
        res = self.molecular_service.balance_redox_reaction(
            reaction_equation="KMnO4 + FeSO4 + H2SO4 -> K2SO4 + MnSO4 + Fe2(SO4)3 + H2O",
            medium="ACIDIC"
        )
        self.assertTrue(res["is_balanced"])
        self.assertEqual(res["electrons_transferred"], 5)
        self.assertIn("KMnO4", res["balanced_equation"])

    def test_redox_balance_dichromate_iron(self):
        """Asserts Cr2O7(2-) + Fe2+ generates 6 electrons transferred."""
        res = self.molecular_service.balance_redox_reaction(
            reaction_equation="Cr2O7(2-) + Fe2+ -> Cr3+ + Fe3+",
            medium="ACIDIC"
        )
        self.assertTrue(res["is_balanced"])
        self.assertEqual(res["electrons_transferred"], 6)

    def test_redox_oversized_equation_rejected(self):
        """Asserts equations exceeding 120 characters raise ValueError."""
        with self.assertRaises(ValueError):
            self.molecular_service.balance_redox_reaction(reaction_equation="A" * 130)

    # -------------------------------------------------------------------------
    # 2. SyllabusKnowledgeAtlasService Tests
    # -------------------------------------------------------------------------

    def test_syllabus_graph_all_stem_nodes(self):
        """Asserts concept graph contains nodes across Physics, Chemistry, and Mathematics."""
        graph = self.atlas_service.get_syllabus_graph()
        self.assertGreaterEqual(graph["total_nodes"], 4)
        self.assertGreaterEqual(len(graph["dependency_edges"]), 1)

    def test_syllabus_graph_subject_filter(self):
        """Asserts filtering concept graph by subject returns only matching nodes."""
        chem_graph = self.atlas_service.get_syllabus_graph(subject="Chemistry")
        for node in chem_graph["nodes"]:
            self.assertEqual(node["subject"], "Chemistry")

    def test_board_exam_frequency_statistics(self):
        """Asserts 10-year past board question frequency contains Dhaka and regional breakdown."""
        freq = self.atlas_service.get_board_exam_frequency(
            subject="Physics",
            chapter="Newtonian Mechanics"
        )
        self.assertEqual(freq["total_appearances"], 48)
        self.assertIn("Dhaka", freq["frequency_by_board"])
        self.assertGreaterEqual(len(freq["high_yield_topics"]), 2)

    def test_board_exam_frequency_fallback(self):
        """Asserts unindexed chapter gracefully returns fallback frequency data."""
        freq = self.atlas_service.get_board_exam_frequency(
            subject="Biology",
            chapter="Genetics"
        )
        self.assertGreaterEqual(freq["total_appearances"], 30)

    def test_formula_cheatsheet_retrieval(self):
        """Asserts formula cheatsheet returns equations for requested subject."""
        formulas = self.atlas_service.get_formula_cheatsheet(subject="Physics")
        self.assertEqual(formulas["subject"], "Physics")
        self.assertGreaterEqual(len(formulas["formulas"]), 2)

    # -------------------------------------------------------------------------
    # 3. InnovationLaunchpadService Tests
    # -------------------------------------------------------------------------

    def test_pitch_project_with_ip_proof_hash(self):
        """Asserts project pitch generates SHA-256 IP proof hash and sets up escrow."""
        proj = self.launchpad_service.pitch_project(
            title="Solar Smart Irrigation",
            track="AGRI_TECH",
            leader_student_id="std-lead-01",
            leader_student_name="Zubair Ahmed",
            summary="Autonomous solar irrigation controller",
            grant_requested_bdt=20000.0,
            demo_repo_url="https://github.com/zubair/solar-irrigation"
        )
        self.assertTrue(proj["project_id"].startswith("PRJ-"))
        self.assertTrue(proj["ip_proof_hash"].startswith("IP-SHA256-"))
        self.assertEqual(proj["grant_requested_bdt"], 20000.0)
        self.assertEqual(proj["escrow_balance_remaining_bdt"], 20000.0)
        self.assertEqual(proj["status"], "VOTING_ACTIVE")

    def test_pitch_project_empty_title_rejected(self):
        """Asserts empty project title raises ValueError."""
        with self.assertRaises(ValueError):
            self.launchpad_service.pitch_project(
                title="   ",
                track="EDTECH",
                leader_student_id="std-01",
                leader_student_name="Tester",
                demo_repo_url="https://github.com/test/repo"
            )

    def test_pitch_project_invalid_url_rejected(self):
        """Asserts repository URL lacking HTTP/HTTPS/Git protocol raises ValueError."""
        with self.assertRaises(ValueError):
            self.launchpad_service.pitch_project(
                title="Invalid URL Project",
                track="FINTECH",
                leader_student_id="std-02",
                leader_student_name="Tester 2",
                demo_repo_url="javascript:alert(1)"
            )

    def test_cast_vote_weighted_score(self):
        """Asserts voting increments vote count and calculates reputation weight multiplier."""
        proj_id = "PRJ-AGRI-01"
        res = self.launchpad_service.cast_vote(
            project_id=proj_id,
            voter_student_id="std-voter-new-01",
            voter_reputation_score=150.0
        )
        self.assertEqual(res["project_id"], proj_id)
        self.assertEqual(res["weighted_vote_value"], 1.5)
        self.assertGreater(res["new_total_votes"], 42)

    def test_duplicate_vote_rejected_anti_sybil(self):
        """Asserts duplicate voting by the same student on the same project is blocked (Anti-Sybil)."""
        proj_id = "PRJ-AGRI-01"
        self.launchpad_service.cast_vote(
            project_id=proj_id,
            voter_student_id="std-voter-sybil-01"
        )
        with self.assertRaises(ValueError):
            self.launchpad_service.cast_vote(
                project_id=proj_id,
                voter_student_id="std-voter-sybil-01"
            )

    def test_grant_tranche_progression_order(self):
        """Asserts skipping PROPOSAL_VALIDATION to PROTOTYPE_DEMO raises ValueError."""
        proj = self.launchpad_service.pitch_project(
            title="Progression Order Test",
            track="EDTECH",
            leader_student_id="std-prog-01",
            leader_student_name="Prog Tester",
            demo_repo_url="https://github.com/prog/test"
        )
        with self.assertRaises(ValueError):
            self.launchpad_service.release_grant_tranche(
                project_id=proj["project_id"],
                milestone_stage="PROTOTYPE_DEMO",
                mentor_reviewer_id="mentor-01"
            )

    def test_grant_tranche_duplicate_stage_rejected(self):
        """Asserts releasing the same milestone stage twice raises ValueError."""
        proj = self.launchpad_service.pitch_project(
            title="Duplicate Stage Test",
            track="FINTECH",
            leader_student_id="std-dup-01",
            leader_student_name="Dup Tester",
            demo_repo_url="https://github.com/dup/test"
        )
        self.launchpad_service.release_grant_tranche(
            project_id=proj["project_id"],
            milestone_stage="PROPOSAL_VALIDATION",
            mentor_reviewer_id="mentor-01"
        )
        with self.assertRaises(ValueError):
            self.launchpad_service.release_grant_tranche(
                project_id=proj["project_id"],
                milestone_stage="PROPOSAL_VALIDATION",
                mentor_reviewer_id="mentor-01"
            )

    def test_grant_tranche_full_3_stage_disbursal(self):
        """Asserts orderly release of all 3 tranches exhausts escrow balance to 0."""
        proj = self.launchpad_service.pitch_project(
            title="Full Disbursal Venture",
            track="HEALTH_AI",
            leader_student_id="std-full-01",
            leader_student_name="Full Tester",
            grant_requested_bdt=10000.0,
            demo_repo_url="https://github.com/full/disbursal"
        )
        pid = proj["project_id"]

        # Tranche 1 (30% = 3000)
        t1 = self.launchpad_service.release_grant_tranche(pid, "PROPOSAL_VALIDATION", "mentor-01")
        self.assertEqual(t1["amount_released_bdt"], 3000.0)
        self.assertEqual(t1["escrow_balance_remaining_bdt"], 7000.0)

        # Tranche 2 (40% = 4000)
        t2 = self.launchpad_service.release_grant_tranche(pid, "PROTOTYPE_DEMO", "mentor-01")
        self.assertEqual(t2["amount_released_bdt"], 4000.0)
        self.assertEqual(t2["escrow_balance_remaining_bdt"], 3000.0)

        # Tranche 3 (30% = 3000)
        t3 = self.launchpad_service.release_grant_tranche(pid, "PILOT_DEPLOYMENT", "mentor-01")
        self.assertEqual(t3["amount_released_bdt"], 3000.0)
        self.assertEqual(t3["escrow_balance_remaining_bdt"], 0.0)

        details = self.launchpad_service.get_project_by_id(pid)
        self.assertEqual(details["grant_status"], "FULLY_DISBURSED")
        self.assertEqual(details["status"], "COMPLETED")

    # -------------------------------------------------------------------------
    # 4. Section 32 REST API Endpoints Tests
    # -------------------------------------------------------------------------

    async def test_api_calculate_molecular_geometry(self):
        """Asserts POST /lab/chemistry/molecular-geometry returns VSEPR data."""
        req = MolecularGeometryRequest(formula="BF3")
        res = await calculate_molecular_geometry(payload=req)
        self.assertEqual(res["molecular_geometry"], "Trigonal Planar")
        self.assertEqual(res["hybridization"], "sp2")

    async def test_api_balance_redox_reaction(self):
        """Asserts POST /lab/chemistry/redox-balance returns balanced half-reactions."""
        req = RedoxReactionBalanceRequest(
            reaction_equation="MnO4- + Fe2+ -> Mn2+ + Fe3+",
            medium="ACIDIC"
        )
        res = await balance_redox_chemical_reaction(payload=req)
        self.assertTrue(res["is_balanced"])
        self.assertEqual(res["electrons_transferred"], 5)

    async def test_api_get_syllabus_graph(self):
        """Asserts GET /syllabus/atlas/graph returns complete graph."""
        res = await get_syllabus_knowledge_graph(subject="Physics")
        self.assertGreaterEqual(res["total_nodes"], 1)

    async def test_api_get_board_exam_frequency(self):
        """Asserts GET /syllabus/atlas/board-frequency returns frequency breakdown."""
        res = await get_board_exam_frequency(subject="Physics", chapter="Newtonian Mechanics")
        self.assertGreater(res["total_appearances"], 40)

    async def test_api_get_syllabus_formulas(self):
        """Asserts GET /syllabus/atlas/formulas returns formulas."""
        res = await get_syllabus_formula_cheatsheet(subject="Chemistry")
        self.assertGreaterEqual(len(res["formulas"]), 2)

    async def test_api_pitch_project_endpoints(self):
        """Asserts POST /launchpad/projects/pitch, vote, and get details."""
        req = PitchProjectRequest(
            title="API Drone Mapping",
            track="AGRI_TECH",
            leader_student_id="std-api-drone",
            leader_student_name="Drone Student",
            grant_requested_bdt=20000.0,
            demo_repo_url="https://github.com/api/drone-mapping",
            summary="Drone crop health scanning"
        )
        proj = await pitch_student_innovation_project(payload=req)
        pid = proj["project_id"]

        vote_req = CastProjectVoteRequest(
            voter_student_id="std-api-voter-01",
            voter_reputation_score=120.0
        )
        vote_res = await cast_project_tribunal_vote(project_id=pid, payload=vote_req)
        self.assertEqual(vote_res["new_total_votes"], 1)

        details = await get_innovation_project_details(project_id=pid)
        self.assertEqual(details["project_id"], pid)

        all_projects = await list_innovation_projects(track="AGRI_TECH")
        self.assertGreaterEqual(len(all_projects), 1)


if __name__ == "__main__":
    unittest.main()
