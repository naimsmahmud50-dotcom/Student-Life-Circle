"""
Comprehensive Automated Unit Tests for Phase 60:
The Grand Convergence & Adaptive Persona Router.
"""

import unittest
from backend.app.services.grand_convergence_attestation_service import GrandConvergenceAttestationService
from backend.app.services.adaptive_persona_router_service import AdaptivePersonaRouterService
from backend.app.services.universal_omni_convergence_search_service import UniversalOmniConvergenceSearchService


class TestPhase60GrandConvergence(unittest.TestCase):

    def setUp(self):
        self.attestation_service = GrandConvergenceAttestationService()
        self.persona_service = AdaptivePersonaRouterService()
        self.search_service = UniversalOmniConvergenceSearchService()

    # --- GrandConvergenceAttestationService Tests ---
    def test_attestation_platform_convergence_structure(self):
        res = self.attestation_service.attest_platform_convergence(
            operator_id="ops:lead_architect",
            verified_tests_count=734
        )
        self.assertEqual(res["total_phases"], 60)
        self.assertEqual(res["overall_health"], "ALL_60_PHASES_OPERATIONAL")
        self.assertEqual(res["operational_sla"], "99.99% High-Availability")
        self.assertEqual(res["verified_tests_count"], 734)
        self.assertIn("Student Life Circle", res["platform_name"])
        self.assertTrue(res["global_merkle_root"].startswith("0x"))
        self.assertEqual(len(res["global_merkle_root"]), 66)

    def test_attestation_six_pillars_verification(self):
        res = self.attestation_service.attest_platform_convergence()
        pillars = res["pillars"]
        self.assertEqual(len(pillars), 6)
        
        total_subsystems = sum(p["subsystems_total"] for p in pillars)
        active_subsystems = sum(p["subsystems_active"] for p in pillars)
        self.assertEqual(total_subsystems, 60)
        self.assertEqual(active_subsystems, 60)

        for pillar in pillars:
            self.assertEqual(pillar["status"], "HEALTHY_OPERATIONAL")
            self.assertGreater(pillar["latency_ms"], 0.0)
            self.assertIn("pillar_id", pillar)
            self.assertIn("name", pillar)

    def test_attestation_merkle_root_integrity(self):
        res1 = self.attestation_service.attest_platform_convergence()
        res2 = self.attestation_service.attest_platform_convergence()
        # Same configuration produces deterministic Merkle root
        self.assertEqual(res1["global_merkle_root"], res2["global_merkle_root"])

    # --- AdaptivePersonaRouterService Tests ---
    def test_persona_routing_student(self):
        res = self.persona_service.route_persona(user_role="student", device_tier="desktop")
        self.assertEqual(res["user_role"], "student")
        self.assertIn("Scholar", res["role_display_title"])
        self.assertIn("practice", res["primary_navigation_tabs"])
        self.assertIn("verifiable-credentials-zkp", res["primary_navigation_tabs"])
        self.assertGreaterEqual(len(res["dashboard_kpis"]), 3)
        self.assertGreaterEqual(len(res["quick_action_shortcuts"]), 2)
        self.assertFalse(res["accessibility_parameters"]["low_bandwidth_optimized"])

    def test_persona_routing_educator(self):
        res = self.persona_service.route_persona(user_role="educator")
        self.assertEqual(res["user_role"], "educator")
        self.assertIn("Educator", res["role_display_title"])
        self.assertIn("coaching-batch-pool", res["primary_navigation_tabs"])
        self.assertIn("voice-viva-simulator", res["primary_navigation_tabs"])
        self.assertTrue(any(k["label"] == "Active Batches" for k in res["dashboard_kpis"]))

    def test_persona_routing_guardian(self):
        res = self.persona_service.route_persona(user_role="guardian")
        self.assertEqual(res["user_role"], "guardian")
        self.assertIn("Guardian", res["role_display_title"])
        self.assertIn("tuition-matching", res["primary_navigation_tabs"])
        self.assertTrue(any("bKash" in a["title"] for a in res["quick_action_shortcuts"]))

    def test_persona_routing_institutional_admin(self):
        res = self.persona_service.route_persona(user_role="institutional_admin")
        self.assertEqual(res["user_role"], "institutional_admin")
        self.assertIn("Registrar", res["role_display_title"])
        self.assertIn("migration-drift-index", res["primary_navigation_tabs"])
        self.assertIn("tenant-merkle-cdc", res["primary_navigation_tabs"])
        self.assertTrue(any("RLS Policy" in k["label"] for k in res["dashboard_kpis"]))

    def test_persona_routing_corporate_recruiter(self):
        res = self.persona_service.route_persona(user_role="corporate_recruiter")
        self.assertEqual(res["user_role"], "corporate_recruiter")
        self.assertIn("Recruiter", res["role_display_title"])
        self.assertIn("verifiable-credentials-zkp", res["primary_navigation_tabs"])
        self.assertTrue(any("ZKP Proofs" in k["label"] for k in res["dashboard_kpis"]))

    def test_persona_routing_accessibility_low_bandwidth(self):
        res = self.persona_service.route_persona(user_role="student", device_tier="mobile_low_bandwidth")
        access = res["accessibility_parameters"]
        self.assertTrue(access["low_bandwidth_optimized"])
        self.assertEqual(access["brotli_compression_level"], 11)
        self.assertTrue(access["reduced_motion"])
        self.assertEqual(access["touch_target_min_px"], 44)

    def test_persona_routing_unknown_role_fallback(self):
        res = self.persona_service.route_persona(user_role="unknown_guest")
        self.assertEqual(res["user_role"], "unknown_guest")
        self.assertEqual(res["role_display_title"], "Academic Scholar & Career Explorer")

    # --- UniversalOmniConvergenceSearchService Tests ---
    def test_omni_search_empty_query(self):
        res = self.search_service.search_omni(query="")
        self.assertEqual(res["total_matches"], 0)
        self.assertEqual(len(res["results"]), 0)
        self.assertGreater(len(res["suggested_terms"]), 0)

    def test_omni_search_lectures_matching(self):
        res = self.search_service.search_omni(query="calculus")
        self.assertGreaterEqual(res["total_matches"], 1)
        titles = [r["title"] for r in res["results"]]
        self.assertTrue(any("Physics" in t or "Algorithms" in t for t in titles))
        self.assertGreater(res["search_latency_ms"], 0.0)

    def test_omni_search_tuition_matching(self):
        res = self.search_service.search_omni(query="dhanmondi")
        self.assertGreaterEqual(res["total_matches"], 1)
        first_match = res["results"][0]
        self.assertEqual(first_match["category"], "tuitions")
        self.assertIn("Dhanmondi", first_match["title"])

    def test_omni_search_jobs_matching(self):
        res = self.search_service.search_omni(query="fastapi")
        self.assertGreaterEqual(res["total_matches"], 1)
        first_match = res["results"][0]
        self.assertEqual(first_match["category"], "jobs")
        self.assertIn("Brain Station 23", first_match["title"])

    def test_omni_search_stem_labs_matching(self):
        res = self.search_service.search_omni(query="vsepr")
        self.assertGreaterEqual(res["total_matches"], 1)
        first_match = res["results"][0]
        self.assertEqual(first_match["category"], "labs")
        self.assertIn("Molecular", first_match["title"])

    def test_omni_search_category_filter(self):
        res = self.search_service.search_omni(query="physics", category_filter="tuitions")
        for item in res["results"]:
            self.assertEqual(item["category"], "tuitions")

    def test_omni_search_results_relevance_sorting(self):
        res = self.search_service.search_omni(query="heap sort")
        scores = [r["relevance_score"] for r in res["results"]]
        self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main()
