"""
Campus Raft BFT Service (Phase 70)
Autonomous Campus Raft Quorum, Byzantine Fault Tolerant (BFT) Consensus & State Machine Replication (SMR).
Simulates a multi-campus distributed consensus ring across 5 university nodes with
leader election, log replication quorum, Byzantine poison rejection, and split-brain chaos resilience.
"""

import hashlib
import json
import time
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any

class CampusRaftBftService:
    """Enterprise 5-node Raft & BFT state machine consensus engine."""

    INITIAL_NODES = [
        {
            "node_id": "node-dhaka-alpha",
            "campus_name": "Dhaka Central Campus",
            "endpoint_url": "https://dhaka-core.academic.edu/rpc",
            "current_term": 1,
            "role": "LEADER",
            "voted_for": "node-dhaka-alpha",
            "commit_index": 3,
            "last_applied": 3,
            "ping_latency_ms": 2.1,
            "is_byzantine": False,
            "is_isolated": False,
            "last_heartbeat_at": ""
        },
        {
            "node_id": "node-ctg-beta",
            "campus_name": "Chittagong Maritime Node",
            "endpoint_url": "https://ctg-edge.academic.edu/rpc",
            "current_term": 1,
            "role": "FOLLOWER",
            "voted_for": "node-dhaka-alpha",
            "commit_index": 3,
            "last_applied": 3,
            "ping_latency_ms": 14.5,
            "is_byzantine": False,
            "is_isolated": False,
            "last_heartbeat_at": ""
        },
        {
            "node_id": "node-raj-gamma",
            "campus_name": "Rajshahi Varendra Node",
            "endpoint_url": "https://raj-edge.academic.edu/rpc",
            "current_term": 1,
            "role": "FOLLOWER",
            "voted_for": "node-dhaka-alpha",
            "commit_index": 3,
            "last_applied": 3,
            "ping_latency_ms": 18.2,
            "is_byzantine": False,
            "is_isolated": False,
            "last_heartbeat_at": ""
        },
        {
            "node_id": "node-syl-delta",
            "campus_name": "Sylhet Tea Garden Edge",
            "endpoint_url": "https://sylhet-edge.academic.edu/rpc",
            "current_term": 1,
            "role": "FOLLOWER",
            "voted_for": "node-dhaka-alpha",
            "commit_index": 3,
            "last_applied": 3,
            "ping_latency_ms": 16.8,
            "is_byzantine": False,
            "is_isolated": False,
            "last_heartbeat_at": ""
        },
        {
            "node_id": "node-khu-epsilon",
            "campus_name": "Khulna Sundarban Gateway",
            "endpoint_url": "https://khulna-edge.academic.edu/rpc",
            "current_term": 1,
            "role": "FOLLOWER",
            "voted_for": "node-dhaka-alpha",
            "commit_index": 3,
            "last_applied": 3,
            "ping_latency_ms": 19.4,
            "is_byzantine": False,
            "is_isolated": False,
            "last_heartbeat_at": ""
        }
    ]

    def __init__(self):
        self.cluster_id = "bft-raft-academic-ring-01"
        self.active_term = 1
        self.quorum_size = 3  # floor(5/2) + 1
        self.total_nodes = 5
        self.byzantine_f = 1  # floor((5-1)/3)
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.logs: List[Dict[str, Any]] = []
        self.state_machine_records: List[Dict[str, Any]] = []
        self.telemetry_events: List[Dict[str, Any]] = []
        self._initialize_cluster()

    def _get_utc_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _hash_entry(self, index: int, term: int, cmd: str, payload: Dict[str, Any]) -> str:
        raw = f"{index}:{term}:{cmd}:{json.dumps(payload, sort_keys=True)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _compute_chained_merkle(self, prev_root: str, entry_hash: str) -> str:
        return hashlib.sha256(f"{prev_root}:{entry_hash}".encode("utf-8")).hexdigest()

    def _initialize_cluster(self):
        now = self._get_utc_now()
        self.nodes = {}
        for n in self.INITIAL_NODES:
            item = dict(n)
            item["last_heartbeat_at"] = now
            self.nodes[item["node_id"]] = item

        # Seed initial committed entries
        seed_merkle = "0000000000000000000000000000000000000000000000000000000000000000"
        init_commands = [
            ("CLUSTER_GENESIS", {"genesis_initiator": "dhaka-central-admin", "nodes": list(self.nodes.keys())}),
            ("EXAM_REGISTRY_INIT", {"session": "HSC-2026-NATIONAL", "total_registered": 145000}),
            ("CAMPUS_CREDENTIAL_ROTATION", {"epoch": "2026-Q4", "active_dids": 5})
        ]

        cur_root = seed_merkle
        for i, (cmd, payload) in enumerate(init_commands, start=1):
            ehash = self._hash_entry(i, 1, cmd, payload)
            cur_root = self._compute_chained_merkle(cur_root, ehash)
            entry = {
                "index": i,
                "term": 1,
                "command_type": cmd,
                "payload": payload,
                "entry_hash": ehash,
                "merkle_state_root": cur_root,
                "timestamp": now,
                "is_committed": True,
                "quorum_acks": list(self.nodes.keys())
            }
            self.logs.append(entry)
            self.state_machine_records.append({"index": i, "command": cmd, "payload": payload, "applied_at": now})

    def get_leader(self) -> Optional[Dict[str, Any]]:
        for n in self.nodes.values():
            if n["role"] == "LEADER" and not n["is_isolated"]:
                return n
        return None

    def get_cluster_topology(self) -> Dict[str, Any]:
        leader = self.get_leader()
        leader_id = leader["node_id"] if leader else None

        # Determine cluster health
        online_honest_nodes = [
            n for n in self.nodes.values()
            if not n["is_isolated"] and not n["is_byzantine"]
        ]
        isolated_nodes = [n for n in self.nodes.values() if n["is_isolated"]]
        byzantine_nodes = [n for n in self.nodes.values() if n["is_byzantine"]]

        if len(online_honest_nodes) >= self.quorum_size:
            if byzantine_nodes:
                status = "BYZANTINE_ANOMALY"
            elif isolated_nodes:
                status = "SPLIT_BRAIN_DEGRADED"
            elif leader is None:
                status = "LEADER_ELECTION"
            else:
                status = "HEALTHY_QUORUM"
        else:
            status = "SPLIT_BRAIN_DEGRADED"

        return {
            "cluster_id": self.cluster_id,
            "active_term": self.active_term,
            "current_leader_id": leader_id,
            "quorum_size": self.quorum_size,
            "total_nodes": self.total_nodes,
            "byzantine_tolerance_f": self.byzantine_f,
            "nodes": list(self.nodes.values()),
            "logs": self.logs[-15:],  # Return recent 15 logs
            "cluster_status": status,
            "merkle_latest_root": self.logs[-1]["merkle_state_root"] if self.logs else "",
            "state_machine_count": len(self.state_machine_records),
            "updated_at": self._get_utc_now()
        }

    def emit_heartbeat(self) -> Dict[str, Any]:
        leader = self.get_leader()
        now = self._get_utc_now()
        if not leader:
            return {
                "success": False,
                "error": "No authoritative active leader available to emit heartbeats.",
                "term": self.active_term
            }

        acks = []
        for nid, node in self.nodes.items():
            if node["is_isolated"]:
                continue
            if node["is_byzantine"]:
                # Byzantine node fails or gives poisoned response
                continue
            node["last_heartbeat_at"] = now
            node["current_term"] = self.active_term
            acks.append(nid)

        quorum_maintained = len(acks) >= self.quorum_size
        return {
            "success": True,
            "leader_id": leader["node_id"],
            "term": self.active_term,
            "acks_count": len(acks),
            "acks": acks,
            "quorum_maintained": quorum_maintained,
            "timestamp": now
        }

    def propose_log_entry(self, command_type: str, payload: Dict[str, Any], client_id: str = "sys-admin") -> Dict[str, Any]:
        leader = self.get_leader()
        if not leader:
            raise ValueError("Consensus proposal rejected: Cluster currently has no active Leader. Trigger an election first.")

        now = self._get_utc_now()
        new_index = len(self.logs) + 1
        entry_hash = self._hash_entry(new_index, self.active_term, command_type, payload)
        prev_merkle = self.logs[-1]["merkle_state_root"] if self.logs else "0"*64
        merkle_root = self._compute_chained_merkle(prev_merkle, entry_hash)

        # Broadcast append entries to all nodes
        acks = [leader["node_id"]]
        for nid, node in self.nodes.items():
            if nid == leader["node_id"]:
                continue
            if node["is_isolated"]:
                continue
            if node["is_byzantine"]:
                # Byzantine node rejects or sends malformed signature, do not tally ack
                continue
            acks.append(nid)

        is_committed = len(acks) >= self.quorum_size

        entry = {
            "index": new_index,
            "term": self.active_term,
            "command_type": command_type,
            "payload": payload,
            "entry_hash": entry_hash,
            "merkle_state_root": merkle_root,
            "timestamp": now,
            "is_committed": is_committed,
            "quorum_acks": acks
        }
        self.logs.append(entry)

        if is_committed:
            # Apply to replicated state machine
            self.state_machine_records.append({
                "index": new_index,
                "command": command_type,
                "payload": payload,
                "applied_at": now
            })
            leader["commit_index"] = new_index
            leader["last_applied"] = new_index
            for ack_id in acks:
                self.nodes[ack_id]["commit_index"] = new_index
                self.nodes[ack_id]["last_applied"] = new_index

        self.telemetry_events.append({
            "timestamp": now,
            "event": "LOG_PROPOSED",
            "index": new_index,
            "term": self.active_term,
            "command": command_type,
            "is_committed": is_committed,
            "acks": acks
        })

        return {
            "index": new_index,
            "term": self.active_term,
            "entry_hash": entry_hash,
            "merkle_state_root": merkle_root,
            "is_committed": is_committed,
            "quorum_acks": acks,
            "quorum_required": self.quorum_size,
            "status": "COMMITTED" if is_committed else "UNCOMMITTED_SUB_QUORUM"
        }

    def trigger_election(self, candidate_node_id: Optional[str] = None) -> Dict[str, Any]:
        """Simulate Raft leader election with randomized election timeout trigger."""
        now = self._get_utc_now()
        # Pick candidate: requested or first non-isolated honest follower
        eligible_candidates = [
            n for n in self.nodes.values()
            if not n["is_isolated"] and not n["is_byzantine"]
        ]
        if not eligible_candidates:
            raise ValueError("Election cannot proceed: No eligible non-isolated honest nodes remain in cluster.")

        candidate = None
        if candidate_node_id and candidate_node_id in self.nodes:
            target = self.nodes[candidate_node_id]
            if not target["is_isolated"] and not target["is_byzantine"]:
                candidate = target

        if not candidate:
            # Prefer a follower
            followers = [n for n in eligible_candidates if n["role"] == "FOLLOWER"]
            candidate = followers[0] if followers else eligible_candidates[0]

        # Step 1: Increment term & become CANDIDATE
        self.active_term += 1
        for n in self.nodes.values():
            if n["role"] == "LEADER":
                n["role"] = "FOLLOWER"
            n["voted_for"] = None

        candidate["current_term"] = self.active_term
        candidate["role"] = "CANDIDATE"
        candidate["voted_for"] = candidate["node_id"]

        # Step 2: Solicit RequestVote from peers
        votes_granted = [candidate["node_id"]]
        rejections = []

        for nid, node in self.nodes.items():
            if nid == candidate["node_id"]:
                continue
            if node["is_isolated"]:
                rejections.append({"node_id": nid, "reason": "NODE_ISOLATED_PARTITION"})
                continue
            if node["is_byzantine"]:
                # Byzantine node refuses or votes against candidate maliciously
                rejections.append({"node_id": nid, "reason": "BYZANTINE_ADVERSARIAL_DENIAL"})
                continue

            # Honest peer grants vote
            node["current_term"] = self.active_term
            node["voted_for"] = candidate["node_id"]
            votes_granted.append(nid)

        quorum_achieved = len(votes_granted) >= self.quorum_size
        if quorum_achieved:
            candidate["role"] = "LEADER"
            # Demote others to FOLLOWER
            for nid, node in self.nodes.items():
                if nid != candidate["node_id"] and node["role"] != "PARTITIONED":
                    node["role"] = "FOLLOWER"
        else:
            candidate["role"] = "FOLLOWER"

        self.telemetry_events.append({
            "timestamp": now,
            "event": "ELECTION_COMPLETED",
            "term": self.active_term,
            "candidate": candidate["node_id"],
            "quorum_achieved": quorum_achieved,
            "votes_granted": votes_granted
        })

        return {
            "new_term": self.active_term,
            "candidate_id": candidate["node_id"],
            "quorum_achieved": quorum_achieved,
            "elected_leader": candidate["node_id"] if quorum_achieved else None,
            "votes_granted": votes_granted,
            "votes_needed": self.quorum_size,
            "timestamp": now
        }

    def inject_chaos_fault(self, action: str, target_node_id: Optional[str] = None) -> Dict[str, Any]:
        """Inject Chaos engineering fault: split-brain, byzantine poison, or leader assassination."""
        now = self._get_utc_now()
        action = action.upper()

        if action == "PARTITION_NODE":
            target_id = target_node_id or "node-ctg-beta"
            if target_id not in self.nodes:
                raise ValueError(f"Unknown node ID: {target_id}")
            node = self.nodes[target_id]
            was_leader = (node["role"] == "LEADER")
            node["is_isolated"] = True
            node["role"] = "PARTITIONED"

            election_triggered = False
            if was_leader:
                # Trigger failover election among remaining partition
                election_res = self.trigger_election()
                election_triggered = True

            return {
                "action": "PARTITION_NODE",
                "target_node_id": target_id,
                "is_isolated": True,
                "was_leader": was_leader,
                "election_triggered": election_triggered,
                "timestamp": now
            }

        elif action == "HEAL_PARTITION":
            target_id = target_node_id or "node-ctg-beta"
            if target_id not in self.nodes:
                raise ValueError(f"Unknown node ID: {target_id}")
            node = self.nodes[target_id]
            node["is_isolated"] = False
            node["role"] = "FOLLOWER"
            node["current_term"] = self.active_term
            leader = self.get_leader()
            if leader:
                node["commit_index"] = leader["commit_index"]
                node["last_applied"] = leader["last_applied"]

            return {
                "action": "HEAL_PARTITION",
                "target_node_id": target_id,
                "is_isolated": False,
                "synced_to_commit": node["commit_index"],
                "timestamp": now
            }

        elif action == "CORRUPT_BYZANTINE":
            target_id = target_node_id or "node-syl-delta"
            if target_id not in self.nodes:
                raise ValueError(f"Unknown node ID: {target_id}")
            node = self.nodes[target_id]
            node["is_byzantine"] = True

            return {
                "action": "CORRUPT_BYZANTINE",
                "target_node_id": target_id,
                "is_byzantine": True,
                "quarantine_status": "BYZANTINE_DETECTED_FILTERED",
                "timestamp": now
            }

        elif action == "PURGE_BYZANTINE":
            target_id = target_node_id or "node-syl-delta"
            if target_id not in self.nodes:
                raise ValueError(f"Unknown node ID: {target_id}")
            node = self.nodes[target_id]
            node["is_byzantine"] = False

            return {
                "action": "PURGE_BYZANTINE",
                "target_node_id": target_id,
                "is_byzantine": False,
                "timestamp": now
            }

        elif action == "KILL_LEADER":
            leader = self.get_leader()
            if not leader:
                raise ValueError("Cannot kill leader: No current leader exists.")
            old_leader_id = leader["node_id"]
            leader["is_isolated"] = True
            leader["role"] = "PARTITIONED"

            # Failover election
            election_result = self.trigger_election()
            return {
                "action": "KILL_LEADER",
                "assassinated_leader_id": old_leader_id,
                "election_result": election_result,
                "timestamp": now
            }

        else:
            raise ValueError(f"Unsupported chaos action: {action}")

campus_raft_bft_service = CampusRaftBftService()
