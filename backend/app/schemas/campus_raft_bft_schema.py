"""
Pydantic v2 Data Models: Byzantine Fault Tolerant (BFT) Consensus & Autonomous Campus Raft Quorum (Phase 70)
Enterprise schemas for Raft consensus node states, replicated state machine logs,
AppendEntries heartbeats, RequestVote RPCs, Byzantine fault detection, and Chaos injections.
"""

from typing import List, Dict, Optional, Any
try:
    from pydantic import BaseModel, Field, ConfigDict
except ImportError:
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default
    def ConfigDict(**kwargs):
        return {}

class RaftNodeDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    node_id: str = Field(..., description="Unique Raft node identifier e.g. node-dhaka-alpha")
    campus_name: str = Field(..., description="Geographic campus name (e.g. Dhaka Central Campus)")
    endpoint_url: str = Field(..., description="Intra-cluster RPC endpoint URL")
    current_term: int = Field(1, ge=1, description="Current consensus epoch term")
    role: str = Field("FOLLOWER", description="'LEADER', 'FOLLOWER', 'CANDIDATE', 'PARTITIONED', or 'BYZANTINE'")
    voted_for: Optional[str] = Field(None, description="Candidate ID that received vote in current term")
    commit_index: int = Field(0, ge=0, description="Highest known committed log index")
    last_applied: int = Field(0, ge=0, description="Highest log index applied to state machine")
    ping_latency_ms: float = Field(..., ge=0.0, description="Inter-node roundtrip latency in ms")
    is_byzantine: bool = Field(False, description="Whether node injects malicious or conflicting proposals")
    is_isolated: bool = Field(False, description="Whether node is cut off by network partition")
    last_heartbeat_at: str = Field(..., description="ISO 8601 timestamp of last received heartbeat")

class RaftLogEntryDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    index: int = Field(..., ge=1, description="Monotonically increasing 1-indexed log position")
    term: int = Field(..., ge=1, description="Term when entry was originally proposed")
    command_type: str = Field(..., description="Command type (e.g. 'EXAM_VAULT_UNLOCK', 'MERKLE_ROOT_SYNC')")
    payload: Dict[str, Any] = Field(default_factory=dict, description="State machine payload parameters")
    entry_hash: str = Field(..., min_length=64, max_length=64, description="SHA-256 integrity hash of this log entry")
    merkle_state_root: str = Field(..., min_length=64, max_length=64, description="Cumulative Merkle root after applying this entry")
    timestamp: str = Field(..., description="ISO 8601 creation timestamp")
    is_committed: bool = Field(False, description="True once replicated to majority quorum (>= 3 nodes)")
    quorum_acks: List[str] = Field(default_factory=list, description="List of node IDs that acknowledged this entry")

class ClusterTopologyDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cluster_id: str = Field(..., description="Cluster identifier e.g. bft-raft-academic-ring-01")
    active_term: int = Field(..., ge=1, description="Global active term of the cluster leader")
    current_leader_id: Optional[str] = Field(None, description="Current authoritative Leader node ID")
    quorum_size: int = Field(3, description="Minimum nodes required for majority consensus (floor(n/2)+1)")
    total_nodes: int = Field(5, description="Total active member nodes in the cluster")
    byzantine_tolerance_f: int = Field(1, description="Maximum Byzantine faults tolerated f = floor((n-1)/3)")
    nodes: List[RaftNodeDTO] = Field(default_factory=list, description="Array of campus cluster nodes")
    logs: List[RaftLogEntryDTO] = Field(default_factory=list, description="Replicated Raft log entries")
    cluster_status: str = Field("HEALTHY_QUORUM", description="'HEALTHY_QUORUM', 'SPLIT_BRAIN_DEGRADED', 'LEADER_ELECTION', or 'BYZANTINE_ANOMALY'")
    updated_at: str = Field(..., description="Last topology evaluation timestamp")

class AppendEntriesRequest(BaseModel):
    term: int = Field(..., ge=1)
    leader_id: str = Field(...)
    prev_log_index: int = Field(..., ge=0)
    prev_log_term: int = Field(..., ge=0)
    entries: List[Dict[str, Any]] = Field(default_factory=list)
    leader_commit: int = Field(..., ge=0)

class AppendEntriesResponse(BaseModel):
    node_id: str = Field(...)
    term: int = Field(..., ge=1)
    success: bool = Field(...)
    match_index: int = Field(..., ge=0)
    error_reason: Optional[str] = Field(None)

class RequestVoteRequest(BaseModel):
    term: int = Field(..., ge=1)
    candidate_id: str = Field(...)
    last_log_index: int = Field(..., ge=0)
    last_log_term: int = Field(..., ge=0)

class RequestVoteResponse(BaseModel):
    node_id: str = Field(...)
    term: int = Field(..., ge=1)
    vote_granted: bool = Field(...)
    rejection_reason: Optional[str] = Field(None)

class ChaosFaultInjectionRequest(BaseModel):
    action: str = Field(..., description="'PARTITION_NODE', 'HEAL_PARTITION', 'CORRUPT_BYZANTINE', 'PURGE_BYZANTINE', 'TRIGGER_ELECTION', 'KILL_LEADER'")
    target_node_id: Optional[str] = Field(None, description="Target node for targeted fault injection")

class StateMachineSnapshotDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    snapshot_index: int = Field(..., ge=1)
    snapshot_term: int = Field(..., ge=1)
    merkle_root: str = Field(..., min_length=64, max_length=64)
    applied_records_count: int = Field(..., ge=0)
    state_hash: str = Field(..., min_length=64, max_length=64)
    created_at: str = Field(...)
