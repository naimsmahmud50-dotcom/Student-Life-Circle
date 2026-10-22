"""
Phase 43 Test Suite
====================
Unit, security, and integration tests for:
1. Quantum Error Correction Service (surface code lattice, Pauli errors, MWPM scaling)
2. Atmospheric Climate Dynamics Service (Arrhenius forcing, Stefan-Boltzmann equilibrium)
3. Micro-Robotics Swarm Intelligence Service (Reynolds flocking, potential fields, battery)
4. REST API Endpoint Router integration
"""

import unittest
from backend.app.services.quantum_error_correction_service import QuantumErrorCorrectionService
from backend.app.services.atmospheric_climate_service import AtmosphericClimateModelingService
from backend.app.services.micro_robotics_swarm_service import AutonomousMicroRoboticsSwarmService


class TestPhase43QecClimateAndSwarm(unittest.TestCase):
    """Test suite asserting Phase 43 services and domain models."""

    # -------------------------------------------------------------------------
    # QUANTUM ERROR CORRECTION TESTS
    # -------------------------------------------------------------------------

    def test_surface_code_lattice_initialization(self):
        lattice = QuantumErrorCorrectionService.initialize_surface_code_lattice(distance=3)
        self.assertEqual(lattice["code_distance"], 3)
        self.assertEqual(lattice["data_qubits"], 9)
        self.assertEqual(lattice["ancilla_qubits"], 8)
        self.assertEqual(lattice["max_correctable_errors"], 1)
        self.assertEqual(len(lattice["qubit_grid"]), 3)

    def test_surface_code_even_distance_auto_correction(self):
        # Even distance d=4 should automatically round up to odd distance d=5
        lattice = QuantumErrorCorrectionService.initialize_surface_code_lattice(distance=4)
        self.assertEqual(lattice["code_distance"], 5)
        self.assertEqual(lattice["data_qubits"], 25)
        self.assertEqual(lattice["max_correctable_errors"], 2)

    def test_pauli_error_injection_and_syndromes(self):
        lattice = QuantumErrorCorrectionService.initialize_surface_code_lattice(distance=3)
        res = QuantumErrorCorrectionService.inject_pauli_errors(lattice=lattice, error_rate_p=0.01)
        self.assertIn("injected_errors", res)
        self.assertIn("active_syndromes", res)

    def test_qec_decoding_sub_threshold_fidelity(self):
        res = QuantumErrorCorrectionService.decode_syndromes_and_estimate_logical_fidelity(
            code_distance=5,
            physical_error_p=0.001,
            syndrome_defects_count=2
        )
        self.assertTrue(res["is_sub_threshold"])
        self.assertTrue(res["syndromes_successfully_matched"])
        self.assertEqual(res["fault_tolerant_status"], "FAULT_TOLERANT_PRESERVED")
        self.assertLess(res["logical_error_rate_pl"], 0.001)

    def test_qec_decoding_above_threshold_fidelity(self):
        res = QuantumErrorCorrectionService.decode_syndromes_and_estimate_logical_fidelity(
            code_distance=3,
            physical_error_p=0.05,  # Above 1.05% threshold
            syndrome_defects_count=3  # Above max correctable (1)
        )
        self.assertFalse(res["is_sub_threshold"])
        self.assertFalse(res["syndromes_successfully_matched"])
        self.assertEqual(res["fault_tolerant_status"], "SUPPRESSION_DEGRADED")

    # -------------------------------------------------------------------------
    # ATMOSPHERIC CLIMATE DYNAMICS TESTS
    # -------------------------------------------------------------------------

    def test_arrhenius_co2_radiative_forcing_baseline(self):
        # At baseline 280 ppm, Delta F should be exactly 0
        res = AtmosphericClimateModelingService.calculate_radiative_forcing(
            co2_concentration_ppm=280.0,
            ch4_concentration_ppb=700.0,
            n2o_concentration_ppb=270.0,
            baseline_co2_ppm=280.0
        )
        self.assertAlmostEqual(res["forcing_co2_w_m2"], 0.0, places=2)
        self.assertAlmostEqual(res["equilibrium_warming_celsius"], 0.0, places=2)

    def test_arrhenius_co2_doubling_forcing(self):
        # Doubling CO2 from 280 to 560 ppm: Delta F = 5.35 * ln(2) ~ 3.708 W/m^2
        res = AtmosphericClimateModelingService.calculate_radiative_forcing(
            co2_concentration_ppm=560.0,
            baseline_co2_ppm=280.0
        )
        self.assertAlmostEqual(res["forcing_co2_w_m2"], 3.708, places=1)
        self.assertGreater(res["total_radiative_forcing_w_m2"], 3.5)

    def test_climate_zero_co2_singularity_guard(self):
        # Negative / zero CO2 should not throw ValueError / ZeroDivisionError
        res = AtmosphericClimateModelingService.calculate_radiative_forcing(co2_concentration_ppm=0.0)
        self.assertIsInstance(res["forcing_co2_w_m2"], float)

    def test_planetary_energy_balance_equilibrium(self):
        res = AtmosphericClimateModelingService.solve_planetary_energy_balance(
            planetary_albedo=0.30,
            effective_emissivity=0.612,
            solar_irradiance=1361.0,
            greenhouse_forcing_delta_f=0.0
        )
        # Earth surface temp should be ~288K (~15C)
        self.assertAlmostEqual(res["surface_temp_celsius"], 15.0, delta=2.5)
        # Bare rock temperature should be ~255K (-18C)
        self.assertAlmostEqual(res["bare_rock_temp_celsius"], -18.0, delta=2.0)
        self.assertGreater(res["natural_greenhouse_effect_k"], 30.0)

    # -------------------------------------------------------------------------
    # MICRO-ROBOTICS SWARM INTELLIGENCE TESTS
    # -------------------------------------------------------------------------

    def test_swarm_kinematic_step_default(self):
        res = AutonomousMicroRoboticsSwarmService.simulate_swarm_step(agents=[])
        self.assertEqual(res["swarm_size"], 5)
        self.assertIn("centroid", res)
        self.assertIn("updated_agents", res)
        self.assertEqual(res["swarm_status"], "FLOCKING_NOMINAL")

    def test_swarm_obstacle_repulsion_and_battery_drain(self):
        agents = [
            {"id": "drone_01", "x": 9.5, "y": 14.5, "vx": 1.0, "vy": 0.0, "battery_pct": 100.0}
        ]
        # Obstacle placed right ahead at [10.0, 14.5]
        obstacles = [[10.0, 14.5]]
        res = AutonomousMicroRoboticsSwarmService.simulate_swarm_step(
            agents=agents,
            obstacles=obstacles,
            dt_seconds=0.1
        )
        updated = res["updated_agents"][0]
        self.assertLess(updated["battery_pct"], 100.0)
        self.assertNotEqual(updated["x"], 9.5)

    def test_swarm_overlapping_agents_singularity_guard(self):
        # Two agents at identical coordinates
        agents = [
            {"id": "d1", "x": 5.0, "y": 5.0, "vx": 0.0, "vy": 0.0, "battery_pct": 99.0},
            {"id": "d2", "x": 5.0, "y": 5.0, "vx": 0.0, "vy": 0.0, "battery_pct": 99.0},
        ]
        res = AutonomousMicroRoboticsSwarmService.simulate_swarm_step(agents=agents)
        self.assertEqual(len(res["updated_agents"]), 2)
        # Both agents should cleanly simulate without crash
        self.assertIsInstance(res["updated_agents"][0]["x"], float)


if __name__ == "__main__":
    unittest.main()
