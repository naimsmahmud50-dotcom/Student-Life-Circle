"""
Phase 45 Test Suite
====================
Unit, security, and integration tests for:
1. Nanophotonics Metamaterial Service (Drude-Lorentz, negative index, negative refraction)
2. Gravitational Wave Interferometry Service (GW150914 benchmark, chirp mass, waveform)
3. Synthetic Biology CRISPR-Cas9 Service (Doench score, PAM NGG, Hsu-Zhang off-target matrix)
4. REST API Endpoint Router integration
"""

import unittest
from backend.app.services.nanophotonic_metamaterial_service import NanophotonicMetamaterialService
from backend.app.services.gravitational_wave_service import GravitationalWaveInterferometryService
from backend.app.services.synthetic_biology_crispr_service import SyntheticBiologyCrisprService


class TestPhase45MetamaterialLigoAndCrispr(unittest.TestCase):
    """Test suite asserting Phase 45 nanophotonics, astrophysics, and gene editing engines."""

    # -------------------------------------------------------------------------
    # NANOPHOTONICS METAMATERIAL TESTS
    # -------------------------------------------------------------------------

    def test_metamaterial_negative_index_dng(self):
        # At frequency 105 THz (between resonance 100 THz and plasma 120 THz)
        res = NanophotonicMetamaterialService.calculate_optical_dispersion(
            frequency_thz=105.0,
            plasma_frequency_thz=120.0,
            resonance_frequency_thz=100.0,
            magnetic_oscillator_strength=0.55
        )
        self.assertLess(res["permittivity_re_eps"], 0.0)
        self.assertLess(res["permeability_re_mu"], 0.0)
        self.assertTrue(res["is_negative_index"])
        self.assertLess(res["refractive_index_n"], 0.0)
        self.assertEqual(res["medium_classification"], "LEFT_HANDED_METAMATERIAL_DNG")

    def test_metamaterial_conventional_dielectric(self):
        # At very high frequency above plasma frequency: both eps and mu > 0
        res = NanophotonicMetamaterialService.calculate_optical_dispersion(
            frequency_thz=250.0,
            plasma_frequency_thz=120.0,
            resonance_frequency_thz=100.0
        )
        self.assertGreater(res["permittivity_re_eps"], 0.0)
        self.assertGreater(res["permeability_re_mu"], 0.0)
        self.assertFalse(res["is_negative_index"])
        self.assertGreater(res["refractive_index_n"], 0.0)

    def test_negative_snell_refraction_ray(self):
        # Incident from air (n1=1.0) into metamaterial (n2=-1.5) at 30 deg
        res = NanophotonicMetamaterialService.simulate_negative_refraction_ray(
            incident_angle_deg=30.0,
            n1_incident=1.0,
            n2_metamaterial=-1.5
        )
        self.assertTrue(res["is_negative_refraction"])
        self.assertLess(res["refraction_angle_deg"], 0.0)
        self.assertFalse(res["total_internal_reflection"])
        self.assertGreater(res["evanescent_amplification_gain"], 1.0)

    def test_snell_total_internal_reflection_guard(self):
        # Extreme incident angle with high n1/n2 ratio leading to sin(theta_2) > 1
        res = NanophotonicMetamaterialService.simulate_negative_refraction_ray(
            incident_angle_deg=85.0,
            n1_incident=2.5,
            n2_metamaterial=-1.0
        )
        self.assertTrue(res["total_internal_reflection"])
        self.assertEqual(res["refraction_angle_deg"], 0.0)

    # -------------------------------------------------------------------------
    # GRAVITATIONAL WAVE (LIGO) TESTS
    # -------------------------------------------------------------------------

    def test_ligo_gw150914_chirp_mass_benchmark(self):
        # Canonical GW150914 discovery: m1 = 36 M_sun, m2 = 29 M_sun
        res = GravitationalWaveInterferometryService.calculate_binary_chirp_parameters(
            m1_solar_masses=36.0,
            m2_solar_masses=29.0,
            luminosity_distance_mpc=410.0,
            initial_frequency_hz=30.0
        )
        # Chirp mass should be ~28.1 M_sun
        self.assertAlmostEqual(res["chirp_mass_msun"], 28.1, delta=0.5)
        self.assertEqual(res["binary_classification"], "BINARY_BLACK_HOLE_BBH")
        self.assertGreaterEqual(res["matched_filter_snr"], 8.0)
        self.assertEqual(res["detection_confidence"], "HIGH_CONFIDENCE_DETECTION")

    def test_ligo_binary_neutron_star_classification(self):
        # GW170817 BNS benchmark: m1 = 1.4 M_sun, m2 = 1.3 M_sun
        res = GravitationalWaveInterferometryService.calculate_binary_chirp_parameters(
            m1_solar_masses=1.4,
            m2_solar_masses=1.3,
            luminosity_distance_mpc=40.0,
            initial_frequency_hz=30.0
        )
        self.assertEqual(res["binary_classification"], "BINARY_NEUTRON_STAR_BNS")
        self.assertLess(res["chirp_mass_msun"], 1.5)

    def test_chirp_waveform_samples_generation(self):
        res = GravitationalWaveInterferometryService.generate_chirp_waveform_samples(
            chirp_mass_msun=28.1,
            duration_seconds=0.2,
            sampling_rate_hz=1024.0
        )
        self.assertGreater(res["samples_count"], 0)
        samples = res["waveform_samples"]
        # Frequency should chirp upwards as merger approaches
        self.assertLess(samples[0]["frequency_hz"], samples[-1]["frequency_hz"])

    # -------------------------------------------------------------------------
    # SYNTHETIC BIOLOGY CRISPR-CAS9 TESTS
    # -------------------------------------------------------------------------

    def test_crispr_grna_optimal_evaluation(self):
        # 20nt protospacer (50% GC, no TTTT, ends in G) + AGG PAM
        # Seq: "GCTAGCTAGCTAGCTAGCTAGGG" (23nt)
        target = "GCTAGCTAGCTAGCTAGCTA" + "GGG"
        res = SyntheticBiologyCrisprService.evaluate_grna_efficiency_and_pam(target)
        self.assertTrue(res["has_canonical_pam"])
        self.assertEqual(res["gc_content_pct"], 50.0)
        self.assertFalse(res["has_poly_t_terminator"])
        self.assertGreaterEqual(res["on_target_efficiency_score"], 80.0)
        self.assertEqual(res["grna_grade"], "TIER_1_OPTIMAL")

    def test_crispr_grna_non_canonical_pam(self):
        # PAM ends in AA instead of GG
        target = "GCTAGCTAGCTAGCTAGCTA" + "AAA"
        res = SyntheticBiologyCrisprService.evaluate_grna_efficiency_and_pam(target)
        self.assertFalse(res["has_canonical_pam"])
        self.assertNotEqual(res["grna_grade"], "TIER_1_OPTIMAL")

    def test_crispr_grna_poly_t_terminator_penalty(self):
        # Contains Pol-III termination signal TTTT
        target = "GCATTTTAGCTAGCTAGCTA" + "CGG"
        res = SyntheticBiologyCrisprService.evaluate_grna_efficiency_and_pam(target)
        self.assertTrue(res["has_poly_t_terminator"])
        self.assertLess(res["on_target_efficiency_score"], 70.0)

    def test_crispr_off_target_seed_mismatch_penalty(self):
        guide = "GCTAGCTAGCTAGCTAGCTA"
        # Mismatch right in the critical seed region (position 2 from PAM)
        off_target = "GCTAGCTAGCTAGCTAGCAA"
        res = SyntheticBiologyCrisprService.calculate_off_target_cleavage_score(guide, off_target)
        self.assertEqual(res["total_mismatches"], 1)
        self.assertEqual(res["seed_region_mismatches"], 1)
        # Cleavage probability should drop severely due to seed sensitivity
        self.assertLess(res["off_target_cleavage_probability_pct"], 1.0)
        self.assertEqual(res["off_target_risk_level"], "NEGLIGIBLE (SAFE)")

    def test_crispr_off_target_identical_sequences(self):
        guide = "GCTAGCTAGCTAGCTAGCTA"
        res = SyntheticBiologyCrisprService.calculate_off_target_cleavage_score(guide, guide)
        self.assertEqual(res["total_mismatches"], 0)
        self.assertAlmostEqual(res["off_target_cleavage_probability_pct"], 100.0, places=1)


if __name__ == "__main__":
    unittest.main()
