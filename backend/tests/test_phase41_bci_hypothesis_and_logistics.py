"""
Unit, Integration, and Security Test Suite for Phase 41:
- Brain-Computer Interface (BCI) & EEG Cognitive Telemetry
- Scientific Hypothesis Discovery & Rigorous Statistical Inference
- Supply Chain Operations Research & Logistics Optimization
"""

import unittest
from backend.app.services.bci_cognitive_telemetry_service import BciCognitiveTelemetryService
from backend.app.services.scientific_hypothesis_discovery_service import ScientificHypothesisDiscoveryService
from backend.app.services.supply_chain_logistics_service import SupplyChainLogisticsOpsService
from backend.app.schemas.bci_hypothesis_and_logistics_schema import (
    BciEegSamplesRequest,
    ContingencyHypothesisRequest,
    EoqRopCalcRequest,
    BullwhipEffectRequest,
    ShortestRouteRequest
)


class TestPhase41BciHypothesisAndLogistics(unittest.TestCase):

    # -------------------------------------------------------------------------
    # 1. BCI & EEG Cognitive Telemetry Tests
    # -------------------------------------------------------------------------
    def test_bci_eeg_default_synthetic_epoch(self):
        """Test generating synthetic resting-state EEG epoch when samples are empty."""
        res = BciCognitiveTelemetryService.decompose_band_powers(raw_samples=[], channel="Cz")
        self.assertEqual(res["channel"], "Cz")
        self.assertEqual(res["sample_count"], 64)
        self.assertGreater(res["total_power_uV2"], 0.0)
        self.assertIn("band_powers_relative_pct", res)
        self.assertIn("alpha", res["band_powers_relative_pct"])
        self.assertIn("beta", res["band_powers_relative_pct"])

    def test_bci_eeg_frequency_bands_presence(self):
        """Test that all 5 standard bands (Delta, Theta, Alpha, Beta, Gamma) are decomposed."""
        samples = [10.0 * (i % 5) for i in range(32)]
        res = BciCognitiveTelemetryService.decompose_band_powers(raw_samples=samples, channel="Fp1")
        bands = res["band_powers_relative_pct"]
        for band in ["delta", "theta", "alpha", "beta", "gamma"]:
            self.assertIn(band, bands)
        # Sum of relative powers should be approximately 100%
        total_rel = sum(bands.values())
        self.assertAlmostEqual(total_rel, 100.0, delta=1.0)

    def test_bci_eeg_silent_flatline_samples_safe(self):
        """Test security audit: flatline zeros cannot cause division-by-zero."""
        flatline = [0.0] * 32
        res = BciCognitiveTelemetryService.decompose_band_powers(raw_samples=flatline, channel="Pz")
        self.assertGreater(res["total_power_uV2"], 0.0)
        self.assertGreaterEqual(res["engagement_index"], 0.0)
        self.assertGreaterEqual(res["fatigue_index"], 0.0)

    def test_bci_eeg_supported_channel_fallback(self):
        """Test fallback to 'Cz' when unsupported electrode string is passed."""
        res = BciCognitiveTelemetryService.decompose_band_powers(raw_samples=[], channel="INVALID_ELECTRODE")
        self.assertEqual(res["channel"], "Cz")

    def test_bci_eeg_flow_state_and_fatigue_statuses(self):
        """Test cognitive status strings (OPTIMAL_FLOW_STATE, BALANCED_ENGAGEMENT, ELEVATED_FATIGUE)."""
        res = BciCognitiveTelemetryService.decompose_band_powers(raw_samples=[], channel="O1")
        self.assertIn(res["fatigue_status"], ["OPTIMAL_FLOW_STATE", "BALANCED_ENGAGEMENT", "ELEVATED_FATIGUE"])
        self.assertIn("recommendation", res)

    # -------------------------------------------------------------------------
    # 2. Scientific Hypothesis Discovery Tests
    # -------------------------------------------------------------------------
    def test_hypothesis_statistically_significant_association(self):
        """Test detecting statistically significant association (p < 0.05)."""
        # Strong association table: high treatment success vs control
        table = [[45, 5], [10, 40]]
        res = ScientificHypothesisDiscoveryService.evaluate_contingency_hypothesis(
            variable_a_name="AI Tutoring",
            variable_b_name="Exam Pass",
            observed_matrix=table,
            alpha=0.05
        )
        self.assertTrue(res["is_significant"])
        self.assertEqual(res["verdict"], "REJECT_NULL_HYPOTHESIS")
        self.assertLess(res["p_value"], 0.05)
        self.assertGreater(res["odds_ratio"], 1.0)

    def test_hypothesis_fail_to_reject_null(self):
        """Test failing to reject null hypothesis when distribution is uniform."""
        table = [[20, 20], [20, 20]]
        res = ScientificHypothesisDiscoveryService.evaluate_contingency_hypothesis(
            variable_a_name="Study Time",
            variable_b_name="Outcome",
            observed_matrix=table,
            alpha=0.05
        )
        self.assertFalse(res["is_significant"])
        self.assertEqual(res["verdict"], "FAIL_TO_REJECT_NULL")
        self.assertGreater(res["p_value"], 0.05)

    def test_hypothesis_zero_sample_size(self):
        """Test security audit: empty observation matrix handled safely."""
        table = [[0, 0], [0, 0]]
        res = ScientificHypothesisDiscoveryService.evaluate_contingency_hypothesis(
            variable_a_name="Factor 1",
            variable_b_name="Factor 2",
            observed_matrix=table
        )
        self.assertFalse(res["is_significant"])
        self.assertEqual(res["verdict"], "INSUFFICIENT_OBSERVATIONS")
        self.assertEqual(res["sample_size"], 0)

    def test_hypothesis_bonferroni_correction_stricter(self):
        """Test that Bonferroni correction tightens significance threshold alpha."""
        table = [[25, 10], [15, 20]]
        res_single = ScientificHypothesisDiscoveryService.evaluate_contingency_hypothesis(
            variable_a_name="A",
            variable_b_name="B",
            observed_matrix=table,
            alpha=0.05,
            bonferroni_hypotheses_count=1
        )
        res_multi = ScientificHypothesisDiscoveryService.evaluate_contingency_hypothesis(
            variable_a_name="A",
            variable_b_name="B",
            observed_matrix=table,
            alpha=0.05,
            bonferroni_hypotheses_count=10
        )
        self.assertEqual(res_single["alpha_bonferroni_corrected"], 0.05)
        self.assertEqual(res_multi["alpha_bonferroni_corrected"], 0.005)

    def test_hypothesis_fisher_exact_prob(self):
        """Test calculation of Fisher's exact test probability."""
        table = [[8, 2], [1, 5]]
        res = ScientificHypothesisDiscoveryService.evaluate_contingency_hypothesis(
            variable_a_name="Group A",
            variable_b_name="Group B",
            observed_matrix=table
        )
        self.assertGreater(res["fisher_exact_prob"], 0.0)
        self.assertLessEqual(res["fisher_exact_prob"], 1.0)

    # -------------------------------------------------------------------------
    # 3. Supply Chain Operations & Logistics Tests
    # -------------------------------------------------------------------------
    def test_eoq_standard_calculation(self):
        """Test classic EOQ: D=12,000, S=$50, H=$2.50 -> Q* = sqrt((2*12000*50)/2.5) = sqrt(480,000) = ~693 units."""
        res = SupplyChainLogisticsOpsService.calculate_eoq_and_rop(
            annual_demand=12000.0,
            order_cost_usd=50.0,
            holding_cost_unit_year_usd=2.5,
            lead_time_days=7,
            demand_std_dev_daily=5.0,
            service_level_pct=95.0
        )
        self.assertEqual(res["optimal_order_quantity_eoq"], 693)
        self.assertGreater(res["total_annual_inventory_cost_usd"], 0.0)
        self.assertEqual(res["orders_per_year"], 17.32)
        self.assertEqual(res["z_score"], 1.645)
        self.assertGreater(res["safety_stock_units"], 0)
        self.assertGreater(res["reorder_point_rop_units"], 0)

    def test_eoq_zero_and_negative_input_clamping(self):
        """Test security audit: negative or zero demand/costs are clamped to safe minimums."""
        res = SupplyChainLogisticsOpsService.calculate_eoq_and_rop(
            annual_demand=-1000.0,
            order_cost_usd=0.0,
            holding_cost_unit_year_usd=-5.0,
            lead_time_days=-3
        )
        self.assertGreaterEqual(res["optimal_order_quantity_eoq"], 1)
        self.assertGreater(res["total_annual_inventory_cost_usd"], 0.0)

    def test_eoq_service_level_z_scores(self):
        """Test Z-score mapping across 90%, 95%, and 99% service levels."""
        res_90 = SupplyChainLogisticsOpsService.calculate_eoq_and_rop(1000, 20, 2, service_level_pct=90.0)
        res_95 = SupplyChainLogisticsOpsService.calculate_eoq_and_rop(1000, 20, 2, service_level_pct=95.0)
        res_99 = SupplyChainLogisticsOpsService.calculate_eoq_and_rop(1000, 20, 2, service_level_pct=99.0)
        self.assertEqual(res_90["z_score"], 1.282)
        self.assertEqual(res_95["z_score"], 1.645)
        self.assertEqual(res_99["z_score"], 2.326)
        self.assertGreater(res_99["safety_stock_units"], res_95["safety_stock_units"])

    def test_bullwhip_variance_amplification(self):
        """Test Bullwhip ratio calculation when upstream order variance exceeds demand."""
        demand = [100.0, 102.0, 98.0, 101.0, 99.0]
        orders = [100.0, 130.0, 70.0, 140.0, 60.0]
        res = SupplyChainLogisticsOpsService.calculate_bullwhip_effect(demand, orders)
        self.assertGreater(res["bullwhip_ratio"], 1.0)
        self.assertIn("AMPLIFICATION", res["amplification_status"])

    def test_bullwhip_insufficient_data_safe(self):
        """Test Bullwhip safety guard with empty or single-element list."""
        res = SupplyChainLogisticsOpsService.calculate_bullwhip_effect([100.0], [100.0])
        self.assertEqual(res["bullwhip_ratio"], 1.0)
        self.assertEqual(res["amplification_status"], "NEUTRAL")

    def test_dijkstra_shortest_route_dhaka_to_chittagong(self):
        """Test finding shortest route from Dhaka Central to Chittagong Port."""
        res = SupplyChainLogisticsOpsService.find_shortest_delivery_route("Dhaka Central", "Chittagong Port")
        self.assertEqual(res["status"], "OPTIMAL_SHORTEST_PATH_FOUND")
        self.assertEqual(res["origin"], "Dhaka Central")
        self.assertEqual(res["destination"], "Chittagong Port")
        # Route: Dhaka -> Narayanganj (20) -> Cumilla (80) -> Chittagong (130) = 230 km
        self.assertEqual(res["total_distance_km"], 230)
        self.assertEqual(res["route_path"], ["Dhaka Central", "Narayanganj Depot", "Cumilla Center", "Chittagong Port"])
        self.assertEqual(res["transit_hops"], 3)

    def test_dijkstra_shortest_route_dhaka_to_rajshahi(self):
        """Test shortest path from Dhaka Central to Rajshahi University Hub."""
        res = SupplyChainLogisticsOpsService.find_shortest_delivery_route("Dhaka Central", "Rajshahi University Hub")
        self.assertEqual(res["status"], "OPTIMAL_SHORTEST_PATH_FOUND")
        self.assertGreater(res["total_distance_km"], 0)
        self.assertIn("Rajshahi University Hub", res["route_path"])

    def test_dijkstra_same_origin_destination(self):
        """Test routing when origin equals destination."""
        res = SupplyChainLogisticsOpsService.find_shortest_delivery_route("Dhaka Central", "Dhaka Central")
        self.assertEqual(res["status"], "IMMEDIATE_DESTINATION")
        self.assertEqual(res["total_distance_km"], 0)
        self.assertEqual(res["transit_hops"], 0)

    def test_dijkstra_unrecognized_hub_fallback(self):
        """Test fallback when unknown hub names are passed."""
        res = SupplyChainLogisticsOpsService.find_shortest_delivery_route("UNKNOWN_HUB_1", "UNKNOWN_HUB_2")
        self.assertEqual(res["origin"], "Dhaka Central")
        self.assertEqual(res["destination"], "Chittagong Port")
        self.assertEqual(res["status"], "OPTIMAL_SHORTEST_PATH_FOUND")

    # -------------------------------------------------------------------------
    # 4. Pydantic v2 / BaseDTO Schema Fallback Tests
    # -------------------------------------------------------------------------
    def test_phase41_schemas_instantiation(self):
        """Test instantiating all Phase 41 request and response schemas."""
        req1 = BciEegSamplesRequest(raw_samples=[1.0, 2.0], channel="Cz")
        self.assertEqual(req1.channel, "Cz")

        req2 = ContingencyHypothesisRequest(variable_a_name="A", variable_b_name="B")
        self.assertEqual(req2.variable_a_name, "A")

        req3 = EoqRopCalcRequest(annual_demand=10000.0, order_cost_usd=40.0, holding_cost_unit_year_usd=2.0)
        self.assertEqual(req3.annual_demand, 10000.0)

        req4 = BullwhipEffectRequest()
        self.assertIsNone(req4.demand_orders)

        req5 = ShortestRouteRequest(origin_hub="Dhaka Central", destination_hub="Cumilla Center")
        self.assertEqual(req5.destination_hub, "Cumilla Center")


if __name__ == "__main__":
    unittest.main()
