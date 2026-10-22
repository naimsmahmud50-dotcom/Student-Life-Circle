"""
Unit, Integration, and Security Test Suite: Phase 36
Verifies:
1. OrbitalMechanicsSatelliteService (Keplerian orbits, ground station pass tracking, RF link budget calculations)
2. GlobalResearchGrantService (Fellowship directory, SOP lexical density & academic rigor evaluation, grant budget conversion)
3. MultiAgentSwarmTutoringService (3-agent collaborative study pod, consensus synthesis, active recall challenges)
4. Section 35 REST Routes in router.py
"""

import unittest
from backend.app.services.orbital_mechanics_satellite_service import (
    OrbitalMechanicsSatelliteService,
    orbital_mechanics_satellite_service
)
from backend.app.services.global_research_grant_service import (
    GlobalResearchGrantService,
    global_research_grant_service
)
from backend.app.services.multi_agent_swarm_tutoring_service import (
    MultiAgentSwarmTutoringService,
    multi_agent_swarm_tutoring_service
)
from backend.app.schemas.satellite_grant_and_swarm_schema import (
    SatelliteOrbitRequest,
    GroundStationPassRequest,
    RfLinkBudgetRequest,
    FellowshipSearchQuery,
    SopEvaluationRequest,
    GrantBudgetCalculationRequest,
    SwarmStudyPodRequest
)
from backend.app.api.v1.router import (
    calculate_satellite_orbit,
    predict_satellite_pass,
    calculate_satellite_rf_link_budget,
    list_global_fellowships,
    evaluate_research_sop,
    calculate_grant_budget,
    get_swarm_agent_profiles,
    run_swarm_study_pod
)


class TestPhase36SatelliteGrantAndSwarm(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.orbital_service = OrbitalMechanicsSatelliteService()
        self.grant_service = GlobalResearchGrantService()
        self.swarm_service = MultiAgentSwarmTutoringService()

    # -------------------------------------------------------------------------
    # 1. OrbitalMechanicsSatelliteService Tests
    # -------------------------------------------------------------------------

    def test_calculate_orbit_geo_bangabandhu(self):
        req = SatelliteOrbitRequest(
            satellite_name="Bangabandhu-Satellite-1",
            perigee_altitude_km=35786.0,
            apogee_altitude_km=35786.0,
            inclination_deg=0.0
        )
        res = self.orbital_service.calculate_orbit(req)
        self.assertEqual(res.orbit_type, "GEO")
        self.assertTrue(res.is_geostationary)
        self.assertAlmostEqual(res.period_minutes, 1436.0, delta=15.0)
        self.assertAlmostEqual(res.mean_orbital_velocity_kms, 3.07, delta=0.1)

    def test_calculate_orbit_leo_cubesat(self):
        req = SatelliteOrbitRequest(
            satellite_name="BRAC-Onnesha",
            perigee_altitude_km=400.0,
            apogee_altitude_km=400.0,
            inclination_deg=51.6
        )
        res = self.orbital_service.calculate_orbit(req)
        self.assertEqual(res.orbit_type, "LEO")
        self.assertFalse(res.is_geostationary)
        self.assertAlmostEqual(res.period_minutes, 92.5, delta=5.0)
        self.assertGreater(res.mean_orbital_velocity_kms, 7.5)

    def test_calculate_orbit_clamped_extremes(self):
        req = SatelliteOrbitRequest(
            satellite_name="Extreme-Probe",
            perigee_altitude_km=-500.0,  # Negative altitude clamped to >= 120.0
            apogee_altitude_km=150000.0,  # Clamped to <= 100000.0
            inclination_deg=210.0  # Clamped to <= 180.0
        )
        res = self.orbital_service.calculate_orbit(req)
        self.assertGreater(res.semi_major_axis_km, 6491.0)
        self.assertLess(res.eccentricity, 1.0)

    def test_predict_ground_station_pass_dhaka(self):
        req = GroundStationPassRequest(
            satellite_name="BRAC-Onnesha",
            station_name="Dhaka SPARRSO Station",
            station_lat=23.7771,
            station_lon=90.3807,
            orbit_altitude_km=450.0,
            carrier_frequency_mhz=437.5
        )
        res = self.orbital_service.predict_ground_station_pass(req)
        self.assertEqual(res.station_name, "Dhaka SPARRSO Station")
        self.assertIn("° N", res.station_coordinates)
        self.assertGreaterEqual(res.duration_seconds, 300)
        self.assertGreater(res.max_doppler_shift_khz, 5.0)
        self.assertIn(res.pass_quality, ["EXCELLENT", "GOOD", "MARGINAL"])

    def test_calculate_rf_link_budget_closed(self):
        req = RfLinkBudgetRequest(
            carrier_frequency_mhz=437.5,
            tx_power_watts=2.0,
            tx_antenna_gain_dbi=2.15,
            distance_km=600.0,
            rx_antenna_gain_dbi=14.5,
            rx_noise_temp_k=150.0,
            data_rate_kbps=9.6
        )
        res = self.orbital_service.calculate_rf_link_budget(req)
        self.assertGreater(res.fspl_db, 130.0)
        self.assertGreater(res.rx_power_dbm, -130.0)
        self.assertEqual(res.link_status, "CLOSED")
        self.assertGreater(res.link_margin_db, 3.0)

    def test_calculate_rf_link_budget_broken(self):
        req = RfLinkBudgetRequest(
            carrier_frequency_mhz=12000.0,
            tx_power_watts=0.01,
            tx_antenna_gain_dbi=0.0,
            distance_km=36000.0,
            rx_antenna_gain_dbi=0.0,
            rx_noise_temp_k=500.0,
            data_rate_kbps=1000.0
        )
        res = self.orbital_service.calculate_rf_link_budget(req)
        self.assertEqual(res.link_status, "BROKEN")
        self.assertLess(res.link_margin_db, 0.0)

    def test_calculate_rf_link_budget_singularity_protection(self):
        req = RfLinkBudgetRequest(
            carrier_frequency_mhz=0.0,  # Clamped to >= 1.0
            tx_power_watts=-5.0,  # Clamped to >= 0.0001
            tx_antenna_gain_dbi=0.0,
            distance_km=-100.0,  # Clamped to >= 1.0
            rx_antenna_gain_dbi=0.0,
            rx_noise_temp_k=-50.0,  # Clamped to >= 1.0
            data_rate_kbps=0.0  # Clamped to >= 0.1
        )
        res = self.orbital_service.calculate_rf_link_budget(req)
        self.assertGreater(res.fspl_db, 0.0)

    # -------------------------------------------------------------------------
    # 2. GlobalResearchGrantService Tests
    # -------------------------------------------------------------------------

    def test_list_all_fellowships(self):
        res = self.grant_service.list_fellowships()
        self.assertGreaterEqual(len(res), 5)
        ids = [f.fellowship_id for f in res]
        self.assertIn("FULBRIGHT-FOREIGN-STUDENT-2025", ids)
        self.assertIn("DAAD-EPOS-2025", ids)
        self.assertIn("ERASMUS-MUNDUS-EMJM-2025", ids)
        self.assertIn("COMMONWEALTH-SCHOLARSHIP-2025", ids)
        self.assertIn("MEXT-RESEARCH-2025", ids)

    def test_list_fellowships_filtered_by_degree(self):
        query = FellowshipSearchQuery(degree_level="POSTDOC")
        res = self.grant_service.list_fellowships(query=query)
        self.assertGreaterEqual(len(res), 1)
        for f in res:
            self.assertIn("POSTDOC", [lvl.upper() for lvl in f.degree_levels])

    def test_list_fellowships_filtered_by_country(self):
        query = FellowshipSearchQuery(destination_country="Japan")
        res = self.grant_service.list_fellowships(query=query)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].fellowship_id, "MEXT-RESEARCH-2025")

    def test_evaluate_sop_short_underflow(self):
        req = SopEvaluationRequest(
            target_fellowship_id="FULBRIGHT-FOREIGN-STUDENT-2025",
            field_of_study="Electrical Engineering",
            sop_text="I want to study abroad."
        )
        res = self.grant_service.evaluate_sop(req)
        self.assertEqual(res.overall_readiness_tier, "NEEDS_REVISION")
        self.assertLess(res.word_count, 30)
        self.assertGreater(len(res.actionable_recommendations), 0)

    def test_evaluate_sop_competitive_proposal(self):
        text = (
            "My central research question investigates quantum dot cellular automata for ultra-low power computing. "
            "Our primary objective is to simulate ballistic transport through graphene nanoribbons. "
            "The empirical methodology utilizes non-equilibrium Green's function frameworks and PyTorch neural solvers. "
            "This project will make a transformative contribution to Bangladesh's semiconductor ecosystem and national impact. "
            "I have reviewed the cutting-edge publications from the nano-electronics faculty and university laboratory."
        )
        req = SopEvaluationRequest(
            target_fellowship_id="FULBRIGHT-FOREIGN-STUDENT-2025",
            field_of_study="Quantum Engineering",
            sop_text=text
        )
        res = self.grant_service.evaluate_sop(req)
        self.assertIn(res.overall_readiness_tier, ["COMPETITIVE", "HIGHLY_COMPETITIVE"])
        self.assertGreaterEqual(res.academic_rigor_score, 70.0)
        self.assertGreater(res.lexical_density_pct, 40.0)
        self.assertGreaterEqual(len(res.strengths), 2)

    def test_evaluate_sop_xss_sanitization(self):
        xss_text = (
            "<script>alert('xss');</script> " * 20 +
            "Investigate research question and empirical methodology with contribution to faculty."
        )
        req = SopEvaluationRequest(
            target_fellowship_id="DAAD-EPOS-2025",
            field_of_study="Computer Science",
            sop_text=xss_text
        )
        res = self.grant_service.evaluate_sop(req)
        self.assertIsInstance(res.academic_rigor_score, float)

    def test_calculate_grant_budget(self):
        req = GrantBudgetCalculationRequest(
            direct_research_costs_usd=10000.0,
            equipment_stipend_usd=5000.0,
            travel_conference_usd=2000.0,
            overhead_rate_pct=10.0
        )
        res = self.grant_service.calculate_grant_budget(req)
        self.assertEqual(res.direct_costs_usd, 17000.0)
        self.assertEqual(res.overhead_usd, 1700.0)
        self.assertEqual(res.total_budget_usd, 18700.0)
        self.assertEqual(res.total_budget_bdt, 18700.0 * 121.50)
        self.assertIn("institutional_overhead", res.breakdown_usd)

    # -------------------------------------------------------------------------
    # 3. MultiAgentSwarmTutoringService Tests
    # -------------------------------------------------------------------------

    def test_get_agent_profiles(self):
        profiles = self.swarm_service.get_agent_profiles()
        self.assertEqual(len(profiles), 3)
        names = [p.agent_name for p in profiles]
        self.assertIn("Dr. Sophia Vance", names)
        self.assertIn("Prof. Richard Thorne", names)
        self.assertIn("Elena Rostova", names)

    def test_run_study_pod_deliberation(self):
        req = SwarmStudyPodRequest(
            topic="Quantum Harmonic Oscillator",
            student_query="Why is there zero-point energy even at absolute zero temperature?",
            academic_level="UNDERGRADUATE"
        )
        res = self.swarm_service.run_study_pod(req)
        self.assertTrue(res.session_id.startswith("SWARM-POD-"))
        self.assertEqual(len(res.agent_contributions), 3)
        self.assertIn("consensus", res.dialectical_consensus.lower())
        self.assertGreaterEqual(len(res.core_takeaways), 3)
        self.assertIn("Active Recall Problem", res.recommended_active_recall_challenge)

    def test_run_study_pod_empty_query_fallback(self):
        req = SwarmStudyPodRequest(topic="", student_query="")
        res = self.swarm_service.run_study_pod(req)
        self.assertEqual(len(res.agent_contributions), 3)
        self.assertIsNotNone(res.dialectical_consensus)

    # -------------------------------------------------------------------------
    # 4. Section 35 REST Router Tests (Async Integration)
    # -------------------------------------------------------------------------

    async def test_api_calculate_orbit(self):
        req = SatelliteOrbitRequest(
            satellite_name="Bangabandhu-1",
            perigee_altitude_km=35786.0,
            apogee_altitude_km=35786.0,
            inclination_deg=0.0
        )
        res = await calculate_satellite_orbit(req)
        self.assertEqual(res.orbit_type, "GEO")

    async def test_api_predict_pass(self):
        req = GroundStationPassRequest(
            satellite_name="Onnesha",
            station_name="Dhaka Station",
            station_lat=23.7771,
            station_lon=90.3807,
            orbit_altitude_km=400.0,
            carrier_frequency_mhz=437.5
        )
        res = await predict_satellite_pass(req)
        self.assertEqual(res.station_name, "Dhaka Station")

    async def test_api_rf_link_budget(self):
        req = RfLinkBudgetRequest(
            carrier_frequency_mhz=437.5,
            tx_power_watts=2.0,
            tx_antenna_gain_dbi=2.15,
            distance_km=700.0,
            rx_antenna_gain_dbi=14.5,
            rx_noise_temp_k=150.0,
            data_rate_kbps=9.6
        )
        res = await calculate_satellite_rf_link_budget(req)
        self.assertIn(res.link_status, ["CLOSED", "MARGINAL", "BROKEN"])

    async def test_api_list_fellowships(self):
        res = await list_global_fellowships(degree_level="MASTERS", destination_country=None)
        self.assertGreater(len(res), 0)

    async def test_api_evaluate_sop(self):
        req = SopEvaluationRequest(
            target_fellowship_id="FULBRIGHT-FOREIGN-STUDENT-2025",
            field_of_study="Data Science",
            sop_text="Investigate research questions with empirical methods and societal impact on faculty."
        )
        res = await evaluate_research_sop(req)
        self.assertIsNotNone(res.overall_readiness_tier)

    async def test_api_calculate_grant_budget(self):
        req = GrantBudgetCalculationRequest(
            direct_research_costs_usd=5000.0,
            equipment_stipend_usd=2000.0,
            travel_conference_usd=1000.0,
            overhead_rate_pct=15.0
        )
        res = await calculate_grant_budget(req)
        self.assertGreater(res.total_budget_bdt, 0.0)

    async def test_api_get_swarm_profiles(self):
        profiles = await get_swarm_agent_profiles()
        self.assertEqual(len(profiles), 3)

    async def test_api_run_swarm_study_pod(self):
        req = SwarmStudyPodRequest(
            topic="General Relativity",
            student_query="Curvature of spacetime and geodesic deviation."
        )
        res = await run_swarm_study_pod(req)
        self.assertEqual(len(res.agent_contributions), 3)


if __name__ == '__main__':
    unittest.main()
