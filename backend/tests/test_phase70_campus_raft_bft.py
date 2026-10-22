"""
Phase 70 Unit & Integration Tests: Autonomous Campus Raft Quorum & Byzantine Fault Tolerant SMR
Validates cluster topology, Raft leader election, majority log quorum, chained Merkle state roots,
Byzantine fault detection, chaos fault injection (split-brain partition, leader assassination), and REST APIs.
"""

import unittest
from backend.app.services.campus_raft_bft_service import CampusRaftBftService

class TestPhase70CampusRaftBft(unittest.TestCase):

    def setUp(self):
        self.service = CampusRaftBftService()

    def test_initial_cluster_topology(self):
        topo = self.service.get_cluster_topology()
        self.assertEqual(topo["total_nodes"], 5)
        self.assertEqual(topo["quorum_size"], 3)
        self.assertEqual(topo["byzantine_tolerance_f"], 1)
        self.assertEqual(topo["cluster_status"], "HEALTHY_QUORUM")
        self.assertEqual(topo["active_term"], 1)
        self.assertEqual(topo["current_leader_id"], "node-dhaka-alpha")
        self.assertGreaterEqual(len(topo["logs"]), 3)
        self.assertEqual(len(topo["merkle_latest_root"]), 64)

    def test_leader_heartbeat_emission(self):
        hb = self.service.emit_heartbeat()
        self.assertTrue(hb["success"])
        self.assertEqual(hb["leader_id"], "node-dhaka-alpha")
        self.assertEqual(hb["acks_count"], 5)
        self.assertTrue(hb["quorum_maintained"])

    def test_log_proposal_and_quorum_commit(self):
        res = self.service.propose_log_entry(
            command_type="EXAM_VAULT_UNLOCK",
            payload={"vault_id": "vault-hsc-phy-001", "room_id": "hall-402"},
            client_id="exam-superintendent"
        )
        self.assertTrue(res["is_committed"])
        self.assertEqual(res["status"], "COMMITTED")
        self.assertGreaterEqual(len(res["quorum_acks"]), 3)
        self.assertEqual(len(res["entry_hash"]), 64)
        self.assertEqual(len(res["merkle_state_root"]), 64)

        # Confirm state machine was updated
        topo = self.service.get_cluster_topology()
        self.assertGreaterEqual(topo["state_machine_count"], 4)

    def test_raft_election_and_term_advancement(self):
        initial_term = self.service.active_term
        res = self.service.trigger_election(candidate_node_id="node-ctg-beta")
        self.assertTrue(res["quorum_achieved"])
        self.assertEqual(res["new_term"], initial_term + 1)
        self.assertEqual(res["elected_leader"], "node-ctg-beta")
        self.assertIn("node-ctg-beta", res["votes_granted"])
        self.assertGreaterEqual(len(res["votes_granted"]), 3)

        # Check topology reflects new leader
        topo = self.service.get_cluster_topology()
        self.assertEqual(topo["current_leader_id"], "node-ctg-beta")
        self.assertEqual(topo["active_term"], initial_term + 1)

    def test_partition_chaos_and_subquorum_isolation(self):
        # Partition 3 followers so only 2 nodes remain online
        self.service.inject_chaos_fault("PARTITION_NODE", "node-ctg-beta")
        self.service.inject_chaos_fault("PARTITION_NODE", "node-raj-gamma")
        self.service.inject_chaos_fault("PARTITION_NODE", "node-syl-delta")

        topo = self.service.get_cluster_topology()
        self.assertEqual(topo["cluster_status"], "SPLIT_BRAIN_DEGRADED")

        # Now propose an entry with only 2 online nodes (sub-quorum)
        res = self.service.propose_log_entry(
            command_type="ATTENDANCE_BATCH_SEAL",
            payload={"batch_id": "batch-889"}
        )
        self.assertFalse(res["is_committed"])
        self.assertEqual(res["status"], "UNCOMMITTED_SUB_QUORUM")
        self.assertLess(len(res["quorum_acks"]), 3)

        # Heal one partition to restore quorum (3 nodes online)
        heal_res = self.service.inject_chaos_fault("HEAL_PARTITION", "node-ctg-beta")
        self.assertFalse(heal_res["is_isolated"])

        # Propose again - should now commit
        res2 = self.service.propose_log_entry(
            command_type="ATTENDANCE_BATCH_SEAL_RETRY",
            payload={"batch_id": "batch-889-retry"}
        )
        self.assertTrue(res2["is_committed"])
        self.assertEqual(res2["status"], "COMMITTED")

    def test_byzantine_fault_corruption_and_quarantine(self):
        # Inject Byzantine behavior on Sylhet Delta
        res = self.service.inject_chaos_fault("CORRUPT_BYZANTINE", "node-syl-delta")
        self.assertTrue(res["is_byzantine"])

        topo = self.service.get_cluster_topology()
        self.assertEqual(topo["cluster_status"], "BYZANTINE_ANOMALY")

        # Heartbeat should exclude Byzantine node from honest acks
        hb = self.service.emit_heartbeat()
        self.assertNotIn("node-syl-delta", hb["acks"])

        # Purge Byzantine fault
        purge_res = self.service.inject_chaos_fault("PURGE_BYZANTINE", "node-syl-delta")
        self.assertFalse(purge_res["is_byzantine"])

        topo_after = self.service.get_cluster_topology()
        self.assertEqual(topo_after["cluster_status"], "HEALTHY_QUORUM")

    def test_leader_assassination_failover(self):
        old_leader = self.service.get_leader()
        self.assertIsNotNone(old_leader)
        old_leader_id = old_leader["node_id"]

        # Kill the leader
        kill_res = self.service.inject_chaos_fault("KILL_LEADER")
        self.assertEqual(kill_res["assassinated_leader_id"], old_leader_id)

        # A new leader should have been elected
        new_leader = self.service.get_leader()
        self.assertIsNotNone(new_leader)
        self.assertNotEqual(new_leader["node_id"], old_leader_id)
        self.assertEqual(self.service.nodes[old_leader_id]["role"], "PARTITIONED")
        self.assertTrue(self.service.nodes[old_leader_id]["is_isolated"])

    def test_router_endpoints_integration(self):
        import asyncio
        from backend.app.api.v1.router import (
            get_campus_raft_cluster_endpoint,
            emit_campus_raft_heartbeat_endpoint,
            propose_campus_raft_log_endpoint,
            trigger_campus_raft_election_endpoint,
            get_campus_raft_status_endpoint
        )

        # GET /cluster
        data1 = asyncio.run(get_campus_raft_cluster_endpoint())
        self.assertEqual(data1["total_nodes"], 5)
        self.assertEqual(data1["quorum_size"], 3)

        # POST /heartbeat
        hb = asyncio.run(emit_campus_raft_heartbeat_endpoint())
        self.assertTrue(hb["success"])

        # POST /log/propose
        res = asyncio.run(propose_campus_raft_log_endpoint(command_type="ASYNC_TEST_COMMAND"))
        self.assertTrue(res["is_committed"])

        # POST /election/trigger
        el = asyncio.run(trigger_campus_raft_election_endpoint())
        self.assertTrue(el["quorum_achieved"])

        # GET /status
        st = asyncio.run(get_campus_raft_status_endpoint())
        self.assertIn("cluster_status", st)
        self.assertEqual(st["total_nodes"], 5)


if __name__ == "__main__":
    unittest.main()
