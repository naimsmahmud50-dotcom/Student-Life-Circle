"""
================================================================================
TEST SUITE: Phase 66 Offline-First P2P Mesh Sync, Local CRDT Mutation Ledger & Disruption Tower
PURPOSE: Comprehensive unit & integration testing for Vector Clocks, Idempotency,
         WebRTC Classroom Mesh Topology, Chaos Emulation & Merkle Reconciliation.
================================================================================
"""

import unittest
from backend.app.services.offline_mesh_crdt_service import (
    OfflineMeshCrdtService,
    offline_mesh_crdt_service
)
from backend.app.schemas.offline_mesh_crdt_schema import (
    CrdtMutationDTO,
    MutationStageRequest,
    ChaosSimulationRequest,
    ReconcileBatchRequest
)


class TestPhase66OfflineMeshCrdt(unittest.TestCase):

    def setUp(self):
        self.service = OfflineMeshCrdtService(hmac_secret_key="test_offline_mesh_secret_2026")

    def test_01_idempotency_key_generation(self):
        k1 = self.service.calculate_idempotency_key("quiz_attempt_1", "Q1", "opt_A", "nonce_99")
        k2 = self.service.calculate_idempotency_key("quiz_attempt_1", "Q1", "opt_A", "nonce_99")
        k3 = self.service.calculate_idempotency_key("quiz_attempt_1", "Q1", "opt_B", "nonce_99")

        self.assertEqual(len(k1), 64)
        self.assertEqual(k1, k2)
        self.assertNotEqual(k1, k3)

    def test_02_stage_mutations_deduplication(self):
        mut1 = CrdtMutationDTO(
            mutation_id="mut_test_01",
            idempotency_key="key_001_unique",
            peer_id="peer_sakib",
            entity_type="EXAM_SUBMISSION",
            entity_id="quiz_test_1",
            op_type="MCQ_ANSWER",
            payload={"ans": "A"},
            vector_clock={"peer_sakib": 1},
            client_timestamp="2026-10-17T09:00:00Z"
        )
        req = MutationStageRequest(peer_id="peer_sakib", mutations=[mut1])
        res1 = self.service.stage_mutations(req)
        self.assertEqual(res1.staged_count, 1)

        # Re-staging same mutation must be rejected/deduplicated idempotently
        res2 = self.service.stage_mutations(req)
        self.assertEqual(res2.staged_count, 0)
        self.assertGreaterEqual(res2.current_queue_depth, 1)

    def test_03_crdt_vector_clock_dominance(self):
        mut_a = {
            "peer_id": "peer_a",
            "vector_clock": {"peer_a": 2, "peer_b": 1},
            "client_timestamp": "2026-10-17T09:00:05Z",
            "payload": {"score": 100}
        }
        mut_b = {
            "peer_id": "peer_b",
            "vector_clock": {"peer_a": 1, "peer_b": 1},
            "client_timestamp": "2026-10-17T09:00:02Z",
            "payload": {"score": 90}
        }
        winner = self.service.resolve_crdt_conflict(mut_a, mut_b)
        self.assertEqual(winner["peer_id"], "peer_a")
        self.assertEqual(winner["payload"]["score"], 100)

    def test_04_crdt_concurrent_tie_break(self):
        mut_a = {
            "peer_id": "peer_a",
            "vector_clock": {"peer_a": 2, "peer_b": 0},
            "client_timestamp": "2026-10-17T09:00:10Z",
            "payload": {"text": "A"}
        }
        mut_b = {
            "peer_id": "peer_b",
            "vector_clock": {"peer_a": 0, "peer_b": 2},
            "client_timestamp": "2026-10-17T09:00:12Z",  # Later timestamp wins
            "payload": {"text": "B"}
        }
        winner = self.service.resolve_crdt_conflict(mut_a, mut_b)
        self.assertEqual(winner["peer_id"], "peer_b")
        self.assertEqual(winner["payload"]["text"], "B")

    def test_05_mesh_topology_and_latency_scaling(self):
        topo_broadband = self.service.get_mesh_topology("FIBER_BROADBAND")
        self.assertTrue(topo_broadband.wan_gateway_available)
        self.assertEqual(topo_broadband.total_peers, 5)
        self.assertLess(topo_broadband.gossip_round_trip_ms, 30.0)

        topo_blackout = self.service.get_mesh_topology("COMPLETE_BLACKOUT")
        self.assertFalse(topo_blackout.wan_gateway_available)
        self.assertGreater(topo_blackout.gossip_round_trip_ms, 100.0)
        # Verify local WebRTC mesh edges still connect peers
        self.assertTrue(len(topo_blackout.mesh_edges) >= 4)

    def test_06_chaos_simulation_zero_data_loss(self):
        req = ChaosSimulationRequest(
            network_profile="INTERMITTENT_LOSS",
            packet_loss_pct=35.0,
            latency_ms=380.0
        )
        res = self.service.simulate_chaos_profile(req)
        self.assertEqual(res.profile_active, "INTERMITTENT_LOSS")
        self.assertEqual(res.data_loss_rate_pct, 0.0)
        self.assertTrue(res.offline_retention_guaranteed)

        req_blackout = ChaosSimulationRequest(network_profile="COMPLETE_BLACKOUT")
        res_blackout = self.service.simulate_chaos_profile(req_blackout)
        self.assertEqual(res_blackout.simulated_packet_loss_pct, 100.0)
        self.assertEqual(res_blackout.data_loss_rate_pct, 0.0)

    def test_07_reconcile_batch_and_merkle_root(self):
        mutations = [
            CrdtMutationDTO(
                mutation_id="mut_reconcile_1",
                idempotency_key="key_rec_01",
                peer_id="peer_sakib",
                entity_type="EXAM_SUBMISSION",
                entity_id="exam_101",
                op_type="MCQ_ANSWER",
                payload={"ans": "B"},
                vector_clock={"peer_sakib": 1},
                client_timestamp="2026-10-17T09:10:00Z"
            ),
            CrdtMutationDTO(
                mutation_id="mut_reconcile_2",
                idempotency_key="key_rec_02",
                peer_id="peer_sakib",
                entity_type="EXAM_SUBMISSION",
                entity_id="exam_101",
                op_type="MCQ_ANSWER",
                payload={"ans": "D"},
                vector_clock={"peer_sakib": 2},
                client_timestamp="2026-10-17T09:11:00Z"
            )
        ]
        # Stage first
        self.service.stage_mutations(MutationStageRequest(peer_id="peer_sakib", mutations=mutations))

        # Now reconcile
        req = ReconcileBatchRequest(
            batch_id="batch_rec_hsc_2026",
            peer_id="peer_sakib",
            mutations=mutations
        )
        res = self.service.reconcile_batch(req)
        self.assertEqual(res.batch_id, "batch_rec_hsc_2026")
        self.assertEqual(res.reconciled_count, 2)
        self.assertEqual(len(res.server_merkle_root), 64)
        self.assertEqual(len(res.attestation_signature), 64)
        self.assertTrue(res.applied_to_supabase)

    def test_08_router_endpoints_integration(self):
        from backend.app.api.v1.router import (
            stage_mutations_endpoint,
            get_mesh_topology_endpoint,
            simulate_chaos_endpoint,
            reconcile_batch_endpoint,
            get_queue_status_endpoint
        )
        import asyncio

        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)

            # Stage
            mut = CrdtMutationDTO(
                mutation_id="mut_async_01",
                idempotency_key="key_async_01",
                peer_id="peer_async",
                entity_type="ATTENDANCE",
                entity_id="session_01",
                op_type="ATTENDANCE_PUNCH",
                payload={"status": "PRESENT"},
                vector_clock={"peer_async": 1},
                client_timestamp="2026-10-17T09:15:00Z"
            )
            stage_res = loop.run_until_complete(stage_mutations_endpoint(
                MutationStageRequest(peer_id="peer_async", mutations=[mut])
            ))
            self.assertGreaterEqual(stage_res.current_queue_depth, 1)

            # Topology
            topo_res = loop.run_until_complete(get_mesh_topology_endpoint("FIBER_BROADBAND"))
            self.assertEqual(topo_res.network_profile, "FIBER_BROADBAND")

            # Chaos
            chaos_res = loop.run_until_complete(simulate_chaos_endpoint(
                ChaosSimulationRequest(network_profile="RURAL_2G_EDGE")
            ))
            self.assertEqual(chaos_res.profile_active, "RURAL_2G_EDGE")

            # Reconcile
            rec_res = loop.run_until_complete(reconcile_batch_endpoint(
                ReconcileBatchRequest(
                    batch_id="batch_async_01",
                    peer_id="peer_async",
                    mutations=[mut]
                )
            ))
            self.assertEqual(rec_res.reconciled_count, 1)

            # Queue Status
            q_res = loop.run_until_complete(get_queue_status_endpoint())
            self.assertIn("staged_queue_depth", q_res)
        finally:
            loop.close()


if __name__ == "__main__":
    unittest.main()
