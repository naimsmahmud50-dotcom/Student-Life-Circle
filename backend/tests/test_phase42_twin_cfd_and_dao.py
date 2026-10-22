"""
Phase 42 Test Suite
====================
Unit, security, and integration tests for:
1. Digital Twin Simulation Service (telemetry, Mahalanobis, drift, Monte Carlo)
2. Computational Fluid Dynamics Service (Reynolds, Bernoulli, drag/lift, channel profile)
3. DAO Governance Protocol Service (quadratic voting, proposals, quorum verification)
4. REST API Endpoint Router integration
"""

import unittest
from backend.app.services.digital_twin_simulation_service import DigitalTwinSimulationService
from backend.app.services.computational_fluid_dynamics_service import ComputationalFluidDynamicsService
from backend.app.services.dao_governance_protocol_service import DaoGovernanceProtocolService


class TestPhase42DigitalTwinAndCFDAndDAO(unittest.TestCase):
    """Test suite asserting Phase 42 services and mathematics."""

    # -------------------------------------------------------------------------
    # DIGITAL TWIN TESTS
    # -------------------------------------------------------------------------

    def test_digital_twin_state_simulation_default(self):
        state = DigitalTwinSimulationService.simulate_twin_state()
        self.assertIn("readings", state)
        self.assertIn("health_status", state)
        self.assertEqual(state["total_sensors"], len(DigitalTwinSimulationService.SENSOR_PROFILES))

    def test_digital_twin_state_with_anomalous_reading(self):
        custom = {"temperature": 150.0, "rpm": 4500.0}
        state = DigitalTwinSimulationService.simulate_twin_state(sensors=custom)
        self.assertGreaterEqual(state["anomaly_count"], 2)
        self.assertIn(state["health_status"], ("DEGRADED", "CRITICAL"))

    def test_mahalanobis_distance_normal(self):
        obs = [25.0, 100.0]
        mean = [25.0, 100.0]
        cov = [[1.0, 0.2], [0.2, 2.0]]
        res = DigitalTwinSimulationService.mahalanobis_anomaly_score(obs, mean, cov)
        self.assertFalse(res["is_anomaly"])
        self.assertEqual(res["severity"], "NORMAL")
        self.assertAlmostEqual(res["mahalanobis_distance"], 0.0, places=4)

    def test_mahalanobis_distance_extreme_anomaly(self):
        obs = [85.0, 300.0]
        mean = [25.0, 100.0]
        cov = [[1.0, 0.0], [0.0, 1.0]]
        res = DigitalTwinSimulationService.mahalanobis_anomaly_score(obs, mean, cov)
        self.assertTrue(res["is_anomaly"])
        self.assertEqual(res["severity"], "CRITICAL")

    def test_mahalanobis_singular_covariance_matrix(self):
        obs = [20.0, 30.0]
        mean = [10.0, 15.0]
        # Linearly dependent rows => det = 0
        cov = [[2.0, 4.0], [1.0, 2.0]]
        res = DigitalTwinSimulationService.mahalanobis_anomaly_score(obs, mean, cov)
        self.assertIsInstance(res["mahalanobis_distance"], float)
        self.assertGreaterEqual(res["mahalanobis_distance"], 0.0)

    def test_sensor_drift_calibration(self):
        res = DigitalTwinSimulationService.calibrate_sensor_drift(
            raw_value=52.5,
            drift_rate_per_hour=0.05,
            elapsed_hours=50.0,
            reference_value=50.0
        )
        self.assertAlmostEqual(res["calibrated_value"], 50.0, places=4)
        self.assertEqual(res["calibration_quality"], "EXCELLENT")

    def test_monte_carlo_reliability(self):
        res = DigitalTwinSimulationService.monte_carlo_reliability(
            component_class="motor",
            mission_hours=500.0,
            simulations=500,
            seed=42
        )
        self.assertGreater(res["analytical_reliability"], 0.5)
        self.assertGreater(res["simulated_reliability"], 0.5)
        self.assertIn("analytical_mttf_hours", res)

    # -------------------------------------------------------------------------
    # COMPUTATIONAL FLUID DYNAMICS (CFD) TESTS
    # -------------------------------------------------------------------------

    def test_reynolds_laminar_flow(self):
        res = ComputationalFluidDynamicsService.classify_reynolds_regime(
            velocity=0.01,
            characteristic_length=0.05,
            fluid="water_20c"
        )
        self.assertEqual(res["regime"], "LAMINAR")
        self.assertLess(res["reynolds_number"], 2300.0)

    def test_reynolds_turbulent_flow(self):
        res = ComputationalFluidDynamicsService.classify_reynolds_regime(
            velocity=15.0,
            characteristic_length=0.5,
            fluid="air_20c"
        )
        self.assertEqual(res["regime"], "TURBULENT")
        self.assertGreater(res["reynolds_number"], 4000.0)

    def test_reynolds_zero_velocity_guard(self):
        res = ComputationalFluidDynamicsService.classify_reynolds_regime(
            velocity=0.0,
            characteristic_length=0.1,
            fluid="air_20c"
        )
        self.assertEqual(res["reynolds_number"], 0.0)
        self.assertEqual(res["regime"], "LAMINAR")

    def test_bernoulli_flow_solver(self):
        res = ComputationalFluidDynamicsService.solve_bernoulli_flow(
            p1_pascal=200000.0,
            v1_m_s=2.0,
            z1_meters=0.0,
            v2_m_s=6.0,
            z2_meters=2.0,
            fluid="water_20c"
        )
        self.assertLess(res["downstream_pressure_p2_pa"], 200000.0)
        self.assertIn("cavitation_risk", res)

    def test_aerodynamic_coefficients(self):
        res = ComputationalFluidDynamicsService.calculate_aerodynamic_coefficients(
            drag_force_newtons=12.5,
            lift_force_newtons=45.0,
            velocity_m_s=25.0,
            frontal_area_m2=0.5,
            fluid="air_20c"
        )
        self.assertGreater(res["drag_coefficient_cd"], 0.0)
        self.assertGreater(res["lift_coefficient_cl"], 0.0)
        self.assertGreater(res["lift_to_drag_ratio"], 1.0)

    def test_2d_laminar_channel_velocity_profile(self):
        res = ComputationalFluidDynamicsService.simulate_2d_laminar_channel_profile(
            channel_height_m=0.1,
            centerline_velocity_m_s=2.0,
            grid_points=11
        )
        samples = res["velocity_profile_samples"]
        self.assertEqual(len(samples), 11)
        # Centerline point should be highest velocity
        center_sample = samples[5]
        self.assertAlmostEqual(center_sample["velocity_m_s"], 2.0, places=2)
        # Wall boundary conditions (no-slip: velocity = 0)
        self.assertAlmostEqual(samples[0]["velocity_m_s"], 0.0, places=2)
        self.assertAlmostEqual(samples[-1]["velocity_m_s"], 0.0, places=2)

    # -------------------------------------------------------------------------
    # DAO GOVERNANCE TESTS
    # -------------------------------------------------------------------------

    def test_quadratic_voting_power_from_tokens(self):
        res = DaoGovernanceProtocolService.calculate_quadratic_voting(tokens=100.0)
        self.assertEqual(res["effective_votes_integer"], 10)
        self.assertEqual(res["tokens_utilized"], 100)

    def test_quadratic_voting_cost_for_desired_votes(self):
        res = DaoGovernanceProtocolService.calculate_quadratic_voting(tokens=200.0, votes=12.0)
        self.assertEqual(res["required_tokens"], 144.0)
        self.assertTrue(res["is_affordable"])
        self.assertEqual(res["token_balance_remaining"], 56.0)

    def test_dao_proposal_lifecycle_and_voting(self):
        p_id = "prop_ai_lab_expansion_01"
        prop = DaoGovernanceProtocolService.create_proposal(
            proposal_id=p_id,
            title="Expand Autonomous AI Cyber Lab",
            description="Allocate 50,000 SLC tokens to student GPU clusters.",
            proposer_address="0xStudentPioneer",
            quorum_pct=10.0,
            approval_threshold_pct=60.0
        )
        self.assertEqual(prop["status"], "ACTIVE")

        # Cast FOR vote with 10,000 tokens => 100 votes
        v1 = DaoGovernanceProtocolService.cast_quadratic_vote(
            proposal_id=p_id,
            voter_address="0xVoterAlice",
            tokens_allocated=10000.0,
            support="FOR"
        )
        self.assertEqual(v1["votes_minted"], 100.0)

        # Cast AGAINST vote with 900 tokens => 30 votes
        v2 = DaoGovernanceProtocolService.cast_quadratic_vote(
            proposal_id=p_id,
            voter_address="0xVoterBob",
            tokens_allocated=900.0,
            support="AGAINST"
        )
        self.assertEqual(v2["votes_minted"], 30.0)

        # Evaluate outcome
        outcome = DaoGovernanceProtocolService.evaluate_governance_outcome(p_id)
        self.assertIn("verdict", outcome)
        self.assertGreater(outcome["total_votes_for"], outcome["total_votes_against"])

    def test_dao_double_voting_prevention(self):
        p_id = "prop_double_vote_check"
        DaoGovernanceProtocolService.create_proposal(
            proposal_id=p_id,
            title="Double Vote Guard Test",
            description="Testing voter duplicate ballot correction.",
            proposer_address="0xGovernor"
        )
        # Alice votes 400 tokens (20 votes) FOR
        DaoGovernanceProtocolService.cast_quadratic_vote(
            proposal_id=p_id,
            voter_address="0xAlice",
            tokens_allocated=400.0,
            support="FOR"
        )
        # Alice updates ballot to 900 tokens (30 votes) AGAINST
        res = DaoGovernanceProtocolService.cast_quadratic_vote(
            proposal_id=p_id,
            voter_address="0xAlice",
            tokens_allocated=900.0,
            support="AGAINST"
        )
        # Votes for should be 0, votes against should be 30
        state = res["proposal_state"]
        self.assertEqual(state["votes_for"], 0.0)
        self.assertEqual(state["votes_against"], 30.0)


if __name__ == "__main__":
    unittest.main()
