"""
========================================================================================
AGROJATRA / STUDENT LIFE CIRCLE - AUTOMATED TEST SUITE (PHASE 46)
MODULE: Nuclear SMR Reactor Physics, Interplanetary Astrodynamics & Topological Quantum Lab
FILE: backend/tests/test_phase46_smr_astrodynamics_and_topological.py
========================================================================================

TOPIC & TEST ARCHITECTURE OVERVIEW FOR NEW DEVELOPERS:
----------------------------------------------------------------------------------------
This suite validates the core physical models, mathematical fidelity, numerical stability,
and security protections for Phase 46:
1. Nuclear SMR Reactor Point Kinetics with 6 Delayed Groups & Doppler Feedback.
2. Interplanetary Astrodynamics Lambert Orbital Boundary Solver & Gravity Assist.
3. Topological Quantum Computing Kitaev Nanowires & Majorana Anyon Braiding.
4. Schema validation and direct router endpoint invocation.
========================================================================================
"""

import unittest
import asyncio
from backend.app.services.nuclear_smr_reactor_service import NuclearSmrReactorService
from backend.app.services.interplanetary_astrodynamics_service import InterplanetaryAstrodynamicsService
from backend.app.services.topological_quantum_service import TopologicalQuantumService
from backend.app.schemas.smr_astrodynamics_and_topological_schema import (
    SmrTransientRequest,
    DecayHeatRequest,
    LambertTransferRequest,
    GravityAssistRequest,
    MultiStageRocketRequest,
    KitaevWireRequest,
    AnyonBraidRequest
)
from backend.app.api.v1.router import (
    simulate_smr_transient,
    calculate_smr_decay_heat,
    solve_lambert_transfer,
    calculate_gravity_assist,
    calculate_multistage_rocket,
    evaluate_kitaev_wire,
    simulate_anyon_braiding
)


class TestPhase46SmrAstrodynamicsAndTopological(unittest.TestCase):
    """
    Comprehensive verification of Phase 46 services, numerical stability,
    and REST handler functions.
    """

    # =========================================================================
    # 1. NUCLEAR SMR REACTOR PHYSICS TESTS
    # =========================================================================

    def test_smr_steady_state_precursors(self):
        """Verify initial 6-group delayed precursor concentrations are strictly positive and balanced."""
        p_rated = 200.0  # MW
        precursors = NuclearSmrReactorService.get_steady_state_precursors(p_rated)
        self.assertEqual(len(precursors), 6)
        for c_i in precursors:
            self.assertGreater(c_i, 0.0)

        # Total precursor sum should be proportional to beta / Lambda
        self.assertGreater(sum(precursors), p_rated)

    def test_smr_decay_heat_way_wigner(self):
        """Verify ANS-5.1 decay heat evaluation yields physically realistic post-shutdown power."""
        p_rated = 200.0
        # At t=10s after scram, decay heat is typically ~5-7% of rated power
        decay_10s = NuclearSmrReactorService.calculate_decay_heat(p_rated, time_after_scram_s=10.0)
        self.assertGreater(decay_10s, 2.0)
        self.assertLess(decay_10s, 25.0)

        # Decay heat at t=100s must be strictly less than at t=10s
        decay_100s = NuclearSmrReactorService.calculate_decay_heat(p_rated, time_after_scram_s=100.0)
        self.assertLess(decay_100s, decay_10s)

    def test_smr_transient_negative_feedback_stability(self):
        """Verify inherent Doppler and moderator feedback prevents reactor runaway."""
        res = NuclearSmrReactorService.simulate_reactor_transient(
            rated_thermal_power_mw=200.0,
            initial_power_mw=200.0,
            reactivity_insertion_pcm=150.0,  # Positive reactivity step
            fuel_doppler_coeff_pcm_per_c=-3.5,
            moderator_coeff_pcm_per_c=-10.0,
            initial_fuel_temp_c=650.0,
            transient_duration_s=8.0,
            time_step_s=0.05
        )
        self.assertEqual(res["status"], "COMPLETED")
        self.assertTrue(res["is_passively_safe"])
        self.assertGreater(res["peak_fuel_temp_c"], 650.0)
        self.assertLess(res["peak_fuel_temp_c"], res["fuel_melting_limit_c"])
        self.assertGreater(res["safety_margin_to_melt_c"], 500.0)
        self.assertGreater(len(res["time_series"]), 5)

    def test_smr_scram_trigger(self):
        """Verify automatic SCRAM triggers on extreme reactivity or temperature excursion."""
        res = NuclearSmrReactorService.simulate_reactor_transient(
            rated_thermal_power_mw=200.0,
            initial_power_mw=200.0,
            reactivity_insertion_pcm=550.0,  # Near prompt critical (> 0.8 beta)
            fuel_doppler_coeff_pcm_per_c=-2.0,
            transient_duration_s=6.0,
            scram_enabled=True
        )
        self.assertEqual(res["status"], "COMPLETED")
        self.assertTrue(res["scram_triggered"])
        self.assertGreaterEqual(res["scram_time_s"], 0.0)

    # =========================================================================
    # 2. INTERPLANETARY ASTRODYNAMICS TESTS
    # =========================================================================

    def test_astrodynamics_lambert_hohmann_transfer(self):
        """Verify Earth-to-Mars orbital transfer solver yields Keplerian parameters."""
        res = InterplanetaryAstrodynamicsService.solve_lambert_transfer(
            r1_au=1.0,
            r2_au=1.524,
            transfer_angle_deg=180.0,
            time_of_flight_days=258.8
        )
        self.assertEqual(res["status"], "COMPLETED")
        # Semi-major axis a = (1.0 + 1.524)/2 ~ 1.262 AU
        self.assertAlmostEqual(res["semi_major_axis_au"], 1.262, places=2)
        # Eccentricity e = (1.524 - 1.0)/(1.524 + 1.0) ~ 0.207
        self.assertAlmostEqual(res["eccentricity"], 0.2076, places=2)
        self.assertGreater(res["delta_v_total_km_s"], 5.0)
        self.assertLess(res["delta_v_total_km_s"], 7.0)

    def test_astrodynamics_gravity_assist_mars(self):
        """Verify hyperbolic flyby deflection and heliocentric velocity boost."""
        res = InterplanetaryAstrodynamicsService.calculate_gravity_assist(
            planet_name="MARS",
            v_infinity_in_km_s=5.65,
            flyby_periapsis_altitude_km=500.0
        )
        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(res["planet"], "MARS")
        self.assertGreater(res["deflection_angle_deg"], 0.0)
        self.assertGreater(res["heliocentric_delta_v_gain_km_s"], 0.0)
        self.assertGreater(res["periapsis_velocity_km_s"], res["v_infinity_km_s"])
        self.assertTrue(res["safe_from_atmospheric_drag"])

    def test_astrodynamics_multistage_rocket_staging(self):
        """Verify Tsiolkovsky multi-stage rocket equation calculates mission Delta-v."""
        res = InterplanetaryAstrodynamicsService.calculate_multistage_rocket(
            payload_mass_kg=1500.0
        )
        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(res["num_stages"], 3)
        self.assertGreater(res["total_launch_mass_kg"], 100000.0)
        self.assertGreater(res["total_delta_v_km_s"], 12.0)
        self.assertEqual(res["mission_capability"], "INTERPLANETARY_TRANSFER")

    # =========================================================================
    # 3. TOPOLOGICAL QUANTUM COMPUTING TESTS
    # =========================================================================

    def test_topological_kitaev_wire_phase_boundary(self):
        """Verify topological vs trivial superconductor phase boundary for 1D Kitaev wire."""
        # Case 1: Topological phase (|mu| < 2t, e.g. mu=0.4, t=1.0 -> 0.4 < 2.0)
        topo_res = TopologicalQuantumService.evaluate_kitaev_wire(
            num_sites_n=40,
            hopping_amplitude_t_mev=1.0,
            superconducting_gap_delta_mev=0.5,
            chemical_potential_mu_mev=0.4,
            temperature_kelvin=0.05
        )
        self.assertEqual(topo_res["status"], "COMPLETED")
        self.assertTrue(topo_res["is_topological"])
        self.assertEqual(topo_res["phase"], "TOPOLOGICAL_SUPERCONDUCTOR")
        self.assertGreater(topo_res["topological_protection_fidelity"], 0.95)

        # Case 2: Trivial phase (|mu| >= 2t, e.g. mu=2.5, t=1.0 -> 2.5 > 2.0)
        triv_res = TopologicalQuantumService.evaluate_kitaev_wire(
            num_sites_n=40,
            hopping_amplitude_t_mev=1.0,
            superconducting_gap_delta_mev=0.5,
            chemical_potential_mu_mev=2.5,
            temperature_kelvin=0.05
        )
        self.assertEqual(triv_res["status"], "COMPLETED")
        self.assertFalse(triv_res["is_topological"])
        self.assertEqual(triv_res["phase"], "TRIVIAL_INSULATOR")
        self.assertEqual(triv_res["topological_protection_fidelity"], 0.0)

    def test_topological_majorana_end_localization(self):
        """Verify Majorana zero modes are exponentially localized at wire boundaries."""
        res = TopologicalQuantumService.evaluate_kitaev_wire(
            num_sites_n=30,
            hopping_amplitude_t_mev=1.0,
            superconducting_gap_delta_mev=0.8,
            chemical_potential_mu_mev=0.0
        )
        profile = res["spatial_profile"]
        self.assertEqual(len(profile), 30)

        # Left boundary (site 1) has peak left mode
        self.assertAlmostEqual(profile[0]["majorana_left_prob"], 1.0, places=2)
        # Right boundary (site 30) has peak right mode
        self.assertAlmostEqual(profile[-1]["majorana_right_prob"], 1.0, places=2)
        # Deep bulk (site 15) has decaying near-zero probability
        self.assertLess(profile[14]["majorana_left_prob"], 0.05)
        self.assertLess(profile[14]["majorana_right_prob"], 0.05)

    def test_topological_anyon_braiding_sigma1_phase_gate(self):
        """Verify elementary anyon braiding operations correctly simulate quantum gates."""
        # sigma_1 acts as Phase Gate S = diag(1, i)
        res = TopologicalQuantumService.simulate_anyon_braiding(
            braid_sequence=["sigma_1"],
            initial_state="|0>"
        )
        self.assertEqual(res["status"], "COMPLETED")
        self.assertAlmostEqual(res["final_prob_zero"], 1.0, places=3)
        self.assertAlmostEqual(res["final_prob_one"], 0.0, places=3)
        self.assertTrue(res["artin_yang_baxter_satisfied"])

        # sigma_2 acts as superposition rotation
        res2 = TopologicalQuantumService.simulate_anyon_braiding(
            braid_sequence=["sigma_2"],
            initial_state="|0>"
        )
        self.assertAlmostEqual(res2["final_prob_zero"], 0.5, places=2)
        self.assertAlmostEqual(res2["final_prob_one"], 0.5, places=2)

    def test_topological_braid_length_dos_guard(self):
        """Verify excessive braid sequence length is safely clamped to 20 ops without error."""
        long_sequence = ["sigma_1"] * 50
        res = TopologicalQuantumService.simulate_anyon_braiding(
            braid_sequence=long_sequence,
            initial_state="|0>"
        )
        self.assertEqual(res["status"], "COMPLETED")
        self.assertEqual(res["num_braid_steps"], 20)

    # =========================================================================
    # 4. REST ROUTER HANDLER INTEGRATION TESTS
    # =========================================================================

    def test_phase46_router_handlers_direct_invocation(self):
        """Verify all Phase 46 REST handler functions execute cleanly with valid payloads."""
        # 1. SMR Transient
        req1 = SmrTransientRequest(rated_thermal_power_mw=150.0, transient_duration_s=5.0)
        res1 = asyncio.run(simulate_smr_transient(req1))
        self.assertEqual(res1["status"], "COMPLETED")

        # 2. SMR Decay Heat
        req2 = DecayHeatRequest(rated_power_mw=200.0, time_after_scram_s=30.0)
        res2 = asyncio.run(calculate_smr_decay_heat(req2))
        self.assertEqual(res2["status"], "COMPLETED")
        self.assertIn("decay_heat_mw", res2)

        # 3. Astrodynamics Lambert
        req3 = LambertTransferRequest(departure_radius_au=1.0, arrival_radius_au=1.524)
        res3 = asyncio.run(solve_lambert_transfer(req3))
        self.assertEqual(res3["status"], "COMPLETED")

        # 4. Astrodynamics Gravity Assist
        req4 = GravityAssistRequest(planet_name="JUPITER")
        res4 = asyncio.run(calculate_gravity_assist(req4))
        self.assertEqual(res4["planet"], "JUPITER")

        # 5. Astrodynamics Rocket
        req5 = MultiStageRocketRequest(payload_mass_kg=2000.0)
        res5 = asyncio.run(calculate_multistage_rocket(req5))
        self.assertEqual(res5["status"], "COMPLETED")

        # 6. Topological Kitaev Wire
        req6 = KitaevWireRequest(num_sites=20, chemical_potential_mev=0.1)
        res6 = asyncio.run(evaluate_kitaev_wire(req6))
        self.assertTrue(res6["is_topological"])

        # 7. Topological Braiding
        req7 = AnyonBraidRequest(braid_sequence=["sigma_1", "sigma_2"])
        res7 = asyncio.run(simulate_anyon_braiding(req7))
        self.assertEqual(res7["status"], "COMPLETED")


if __name__ == "__main__":
    unittest.main()
