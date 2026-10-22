"""
================================================================================
TEST SUITE: Phase 65 AI Adaptive Curriculum, Bayesian Knowledge Graph & Memory Decay Engine
PURPOSE: Comprehensive unit & integration testing for Curriculum DAG Traversal,
         Bayesian Knowledge Tracing (BKT), Ebbinghaus Memory Decay & Remedial Pathways.
================================================================================
"""

import unittest
from backend.app.services.adaptive_curriculum_graph_service import (
    AdaptiveCurriculumGraphService,
    adaptive_curriculum_service
)
from backend.app.schemas.adaptive_curriculum_graph_schema import (
    BktUpdateRequest,
    RemedialPathwayRequest,
    AdaptiveScheduleRequest
)


class TestPhase65AdaptiveCurriculumGraph(unittest.TestCase):

    def setUp(self):
        self.service = AdaptiveCurriculumGraphService()

    def test_01_curriculum_graph_retrieval(self):
        graph = self.service.get_curriculum_graph("Higher Mathematics")
        self.assertEqual(graph.subject, "Higher Mathematics")
        self.assertGreaterEqual(graph.total_concepts, 10)
        self.assertGreaterEqual(graph.total_prerequisites, 8)
        self.assertGreaterEqual(graph.topological_levels, 5)

        # Check root nodes have level 1
        root_nodes = [n for n in graph.nodes if not n.get("prerequisites")]
        self.assertTrue(len(root_nodes) >= 2)
        for r in root_nodes:
            self.assertEqual(r["level"], 1)

        # Check downstream node has higher level than its prerequisites
        node_map = {n["concept_id"]: n for n in graph.nodes}
        chain_rule = node_map["MATH-CALC-004"]
        for p_id in chain_rule["prerequisites"]:
            self.assertLess(node_map[p_id]["level"], chain_rule["level"])

    def test_02_curriculum_graph_physics(self):
        graph = self.service.get_curriculum_graph("Physics")
        self.assertEqual(graph.subject, "Physics")
        self.assertGreaterEqual(graph.total_concepts, 5)
        self.assertTrue(any(n["concept_id"] == "PHYS-VEC-001" for n in graph.nodes))

    def test_03_bkt_update_correct_response(self):
        req = BktUpdateRequest(
            student_id="test_student_01",
            concept_id="MATH-CALC-002",
            is_correct=True,
            p_prior=0.30,
            p_guess=0.20,
            p_slip=0.10,
            p_transit=0.15
        )
        res = self.service.update_bayesian_mastery(req)
        self.assertEqual(res.student_id, "test_student_01")
        self.assertEqual(res.concept_id, "MATH-CALC-002")
        self.assertGreater(res.new_mastery, res.previous_mastery)
        self.assertGreater(res.delta, 0.0)
        self.assertIn(res.mastery_classification, ["NOVICE", "DEVELOPING", "PROFICIENT", "MASTERED"])

    def test_04_bkt_update_incorrect_response(self):
        req = BktUpdateRequest(
            student_id="test_student_02",
            concept_id="MATH-CALC-003",
            is_correct=False,
            p_prior=0.70,
            p_guess=0.20,
            p_slip=0.10,
            p_transit=0.10
        )
        res = self.service.update_bayesian_mastery(req)
        self.assertLess(res.posterior_mastery, res.previous_mastery)
        # Even with transit, incorrect answer drops mastery
        self.assertLess(res.new_mastery, res.previous_mastery)

    def test_05_bkt_mastery_threshold_reached(self):
        req = BktUpdateRequest(
            student_id="test_student_03",
            concept_id="MATH-ALG-001",
            is_correct=True,
            p_prior=0.82,
            p_guess=0.15,
            p_slip=0.05,
            p_transit=0.15
        )
        res = self.service.update_bayesian_mastery(req)
        self.assertGreaterEqual(res.new_mastery, 0.85)
        self.assertTrue(res.is_mastered)
        self.assertEqual(res.mastery_classification, "MASTERED")

    def test_06_ebbinghaus_retention_decay(self):
        base_mastery = 0.90
        stability_days = 5.0

        r0 = self.service.calculate_ebbinghaus_retention(base_mastery, 0.0, stability_days)
        r3 = self.service.calculate_ebbinghaus_retention(base_mastery, 3.0, stability_days)
        r7 = self.service.calculate_ebbinghaus_retention(base_mastery, 7.0, stability_days)
        r30 = self.service.calculate_ebbinghaus_retention(base_mastery, 30.0, stability_days)

        self.assertAlmostEqual(r0, 0.90, places=3)
        self.assertLess(r3, r0)
        self.assertLess(r7, r3)
        self.assertLess(r30, r7)

        # Higher stability yields higher retention
        r7_high_stability = self.service.calculate_ebbinghaus_retention(base_mastery, 7.0, stability_days=15.0)
        self.assertGreater(r7_high_stability, r7)

    def test_07_remedial_pathway_root_cause_diagnosis(self):
        # STD-65-DEMO has critical gaps in MATH-TRIG-002 (0.42) and MATH-CALC-002 (0.38)
        req = RemedialPathwayRequest(
            student_id="STD-65-DEMO",
            failed_concept_id="MATH-CALC-004",  # Chain rule
            max_depth=4
        )
        res = self.service.generate_remedial_pathway(req)
        self.assertEqual(res.student_id, "STD-65-DEMO")
        self.assertEqual(res.failed_concept_id, "MATH-CALC-004")
        self.assertGreaterEqual(len(res.identified_gaps), 1)
        self.assertGreaterEqual(len(res.remedial_sequence), 2)
        self.assertGreater(res.estimated_recovery_hours, 0.5)
        self.assertIn("Diagnosed root-cause", res.action_plan)

        # Sequence should end with the failed concept retest
        last_step = res.remedial_sequence[-1]
        self.assertEqual(last_step["concept_id"], "MATH-CALC-004")
        self.assertEqual(last_step["type"], "TARGET_RETEST")

    def test_08_adaptive_schedule_generation(self):
        req = AdaptiveScheduleRequest(
            student_id="STD-65-DEMO",
            subject="Higher Mathematics",
            available_hours_per_day=2.0,
            horizon_days=7
        )
        res = self.service.generate_adaptive_schedule(req)
        self.assertEqual(res.student_id, "STD-65-DEMO")
        self.assertEqual(res.horizon_days, 7)
        self.assertEqual(len(res.daily_sessions), 7)
        self.assertGreaterEqual(res.decayed_concepts_reviewed, 1)
        self.assertGreaterEqual(res.predicted_retention_gain, 0.20)

        # Verify daily study minutes are capped within capacity
        for day in res.daily_sessions:
            self.assertLessEqual(day["total_study_minutes"], 120)

    def test_09_student_mastery_snapshot(self):
        snapshot = self.service.get_student_mastery_snapshot("STD-65-DEMO", "Higher Mathematics")
        self.assertEqual(snapshot["student_id"], "STD-65-DEMO")
        self.assertEqual(snapshot["subject"], "Higher Mathematics")
        self.assertGreaterEqual(len(snapshot["concepts"]), 10)
        self.assertGreater(snapshot["average_mastery"], 0.0)
        self.assertGreaterEqual(snapshot["mastered_count"], 1)
        self.assertGreaterEqual(snapshot["critical_gap_count"], 1)

    def test_10_router_integration(self):
        from backend.app.api.v1.router import (
            get_curriculum_graph_endpoint,
            update_bayesian_mastery_endpoint,
            generate_remedial_pathway_endpoint,
            generate_adaptive_schedule_endpoint,
            get_student_mastery_snapshot_endpoint
        )
        import asyncio

        # Test router async functions directly
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            
            # Graph
            graph_res = loop.run_until_complete(get_curriculum_graph_endpoint("Higher Mathematics"))
            self.assertEqual(graph_res.subject, "Higher Mathematics")

            # BKT
            bkt_res = loop.run_until_complete(update_bayesian_mastery_endpoint(
                BktUpdateRequest(
                    student_id="std_async_01",
                    concept_id="MATH-TRIG-001",
                    is_correct=True
                )
            ))
            self.assertEqual(bkt_res.student_id, "std_async_01")

            # Remedial
            rem_res = loop.run_until_complete(generate_remedial_pathway_endpoint(
                RemedialPathwayRequest(
                    student_id="STD-65-DEMO",
                    failed_concept_id="MATH-CALC-004"
                )
            ))
            self.assertIsNotNone(rem_res.root_cause_concept_id)

            # Schedule
            sched_res = loop.run_until_complete(generate_adaptive_schedule_endpoint(
                AdaptiveScheduleRequest(
                    student_id="STD-65-DEMO",
                    subject="Higher Mathematics"
                )
            ))
            self.assertEqual(sched_res.horizon_days, 7)

            # Snapshot
            snap_res = loop.run_until_complete(get_student_mastery_snapshot_endpoint("STD-65-DEMO"))
            self.assertEqual(snap_res["student_id"], "STD-65-DEMO")
        finally:
            loop.close()


if __name__ == "__main__":
    unittest.main()
