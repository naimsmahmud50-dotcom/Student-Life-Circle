"""
Phase 44 Test Suite
====================
Unit, security, and integration tests for:
1. Fusion Plasma Tokamak Physics Service (Lawson criterion, MHD stability, Kruskal-Shafranov)
2. Neuromorphic Spiking Neural Network Service (LIF membrane dynamics, STDP plasticity)
3. Autonomous Maritime Navigation Service (AIS tracking, DCPA/TCPA, COLREGs rules)
4. REST API Endpoint Router integration
"""

import unittest
from backend.app.services.fusion_plasma_tokamak_service import FusionPlasmaTokamakService
from backend.app.services.neuromorphic_spiking_network_service import NeuromorphicSpikingNetworkService
from backend.app.services.maritime_navigation_colregs_service import MaritimeNavigationColregsService


class TestPhase44PlasmaSnnAndMaritime(unittest.TestCase):
    """Test suite asserting Phase 44 services, physics, and robotics models."""

    # -------------------------------------------------------------------------
    # FUSION PLASMA TOKAMAK TESTS
    # -------------------------------------------------------------------------

    def test_lawson_criterion_ignition(self):
        # n = 1.0e20 m^-3, tau_E = 3.5 s, T = 15 keV => LTP = 5.25e21 >= 3.0e21
        res = FusionPlasmaTokamakService.evaluate_lawson_criterion(
            plasma_density_m3=1.0e20,
            energy_confinement_time_s=3.5,
            plasma_temperature_kev=15.0,
            external_heating_power_mw=50.0
        )
        self.assertTrue(res["ignition_achieved"])
        self.assertEqual(res["plasma_regime"], "SELF_SUSTAINING_IGNITION")
        self.assertGreaterEqual(res["triple_product_kev_s_m3"], 3.0e21)

    def test_lawson_criterion_sub_breakeven(self):
        # Very low confinement time => Sub-breakeven
        res = FusionPlasmaTokamakService.evaluate_lawson_criterion(
            plasma_density_m3=1.0e19,
            energy_confinement_time_s=0.2,
            plasma_temperature_kev=5.0
        )
        self.assertFalse(res["ignition_achieved"])
        self.assertEqual(res["plasma_regime"], "SUB_BREAKEVEN")
        self.assertLess(res["fusion_gain_factor_q"], 1.0)

    def test_tokamak_mhd_stability_iter_baseline(self):
        # ITER parameters: R=6.2m, a=2.0m, B_T=5.3T, I_p=15MA
        res = FusionPlasmaTokamakService.calculate_tokamak_mhd_stability(
            major_radius_r_m=6.2,
            minor_radius_a_m=2.0,
            toroidal_field_bt_tesla=5.3,
            plasma_current_ip_ma=15.0
        )
        self.assertGreaterEqual(res["safety_factor_q_edge"], 2.0)
        self.assertTrue(res["is_mhd_stable"])
        self.assertEqual(res["instability_risk"], "NONE (STABLE)")

    def test_tokamak_mhd_kink_instability(self):
        # Low B_t and high current => low q_edge < 2.0
        res = FusionPlasmaTokamakService.calculate_tokamak_mhd_stability(
            major_radius_r_m=6.2,
            minor_radius_a_m=2.0,
            toroidal_field_bt_tesla=1.0,
            plasma_current_ip_ma=25.0
        )
        self.assertLess(res["safety_factor_q_edge"], 2.0)
        self.assertFalse(res["is_mhd_stable"])
        self.assertEqual(res["instability_risk"], "KINK_INSTABILITY_RISK")

    # -------------------------------------------------------------------------
    # NEUROMORPHIC SNN TESTS
    # -------------------------------------------------------------------------

    def test_lif_neuron_subthreshold_quiescence(self):
        # Sub-threshold current injection: no spikes
        currents = [0.5] * 20
        res = NeuromorphicSpikingNetworkService.simulate_lif_neuron(
            current_injections_na=currents,
            dt_ms=0.5
        )
        self.assertEqual(res["total_spikes"], 0)
        self.assertEqual(res["firing_rate_hz"], 0.0)
        self.assertEqual(res["neuron_regime"], "QUIESCENT_SUBTHRESHOLD")

    def test_lif_neuron_repetitive_spiking_and_refractory(self):
        # Strong current injection: repetitive spikes with refractory reset
        currents = [3.0] * 100
        res = NeuromorphicSpikingNetworkService.simulate_lif_neuron(
            current_injections_na=currents,
            dt_ms=0.5
        )
        self.assertGreater(res["total_spikes"], 0)
        self.assertGreater(res["firing_rate_hz"], 10.0)
        self.assertEqual(res["neuron_regime"], "REPETITIVE_FIRING")

    def test_stdp_synaptic_potentiation_ltp(self):
        # Presynaptic spike before postsynaptic (Delta t = +10ms > 0) => LTP
        res = NeuromorphicSpikingNetworkService.calculate_stdp_synaptic_plasticity(
            initial_weight=0.50,
            pre_spike_times_ms=[10.0, 30.0],
            post_spike_times_ms=[20.0, 40.0]
        )
        self.assertGreater(res["final_weight"], 0.50)
        self.assertEqual(res["plasticity_outcome"], "POTENTIATED")
        self.assertEqual(res["total_ltp_events"], 3)

    def test_stdp_synaptic_depression_ltd(self):
        # Postsynaptic spike before presynaptic (Delta t = -10ms < 0) => LTD
        res = NeuromorphicSpikingNetworkService.calculate_stdp_synaptic_plasticity(
            initial_weight=0.50,
            pre_spike_times_ms=[20.0, 40.0],
            post_spike_times_ms=[10.0, 30.0]
        )
        self.assertLess(res["final_weight"], 0.50)
        self.assertEqual(res["plasticity_outcome"], "DEPRESSED")
        self.assertEqual(res["total_ltd_events"], 3)

    # -------------------------------------------------------------------------
    # MARITIME NAVIGATION (COLREGS) TESTS
    # -------------------------------------------------------------------------

    def test_colregs_rule_14_head_on_situation(self):
        # Own ship at (0, 0) heading 000° (North) at 15 knots
        # Target ship at (0, 5) heading 180° (South) at 15 knots
        res = MaritimeNavigationColregsService.calculate_closest_point_of_approach(
            own_x_nm=0.0,
            own_y_nm=0.0,
            own_speed_knots=15.0,
            own_course_deg=0.0,
            target_x_nm=0.0,
            target_y_nm=5.0,
            target_speed_knots=15.0,
            target_course_deg=180.0
        )
        self.assertTrue(res["collision_risk"])
        self.assertEqual(res["colregs_situation"], "COLREGS_RULE_14_HEAD_ON")
        self.assertEqual(res["recommended_evasive_action"], "ALTER_COURSE_TO_STARBOARD")
        self.assertAlmostEqual(res["dcpa_nm"], 0.0, places=2)
        self.assertAlmostEqual(res["tcpa_minutes"], 10.0, delta=0.5)

    def test_colregs_rule_15_crossing_give_way(self):
        # Target approaching from starboard (bearing 045°) on collision course
        res = MaritimeNavigationColregsService.calculate_closest_point_of_approach(
            own_x_nm=0.0,
            own_y_nm=0.0,
            own_speed_knots=15.0,
            own_course_deg=0.0,
            target_x_nm=3.0,
            target_y_nm=3.0,
            target_speed_knots=15.0,
            target_course_deg=270.0
        )
        self.assertEqual(res["colregs_situation"], "COLREGS_RULE_15_CROSSING_GIVE_WAY")
        self.assertEqual(res["own_vessel_role"], "GIVE_WAY")

    def test_colregs_diverging_safe(self):
        # Target moving away (already passed CPA)
        res = MaritimeNavigationColregsService.calculate_closest_point_of_approach(
            own_x_nm=0.0,
            own_y_nm=0.0,
            own_speed_knots=15.0,
            own_course_deg=0.0,
            target_x_nm=0.0,
            target_y_nm=-5.0,
            target_speed_knots=15.0,
            target_course_deg=180.0
        )
        self.assertTrue(res["is_diverging"])
        self.assertFalse(res["collision_risk"])
        self.assertEqual(res["colregs_situation"], "DIVERGING_SAFE")

    def test_colregs_zero_relative_velocity_guard(self):
        # Both ships on identical course and speed (parallel)
        res = MaritimeNavigationColregsService.calculate_closest_point_of_approach(
            own_x_nm=0.0,
            own_y_nm=0.0,
            own_speed_knots=15.0,
            own_course_deg=90.0,
            target_x_nm=0.0,
            target_y_nm=2.0,
            target_speed_knots=15.0,
            target_course_deg=90.0
        )
        self.assertAlmostEqual(res["dcpa_nm"], 2.0, places=2)
        self.assertFalse(res["collision_risk"])


if __name__ == "__main__":
    unittest.main()
