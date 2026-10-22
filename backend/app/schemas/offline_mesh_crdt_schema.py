"""
================================================================================
MODULE: Offline-First P2P Mesh Sync, Local CRDT Mutation Ledger & Disruption Schemas
TOPIC: Pydantic Data Contracts for Vector Clocks, CRDT Mutations & Network Chaos
FILE: backend/app/schemas/offline_mesh_crdt_schema.py
PURPOSE: Strict data validation schemas for Phase 66 Offline-First Mesh Tower.
================================================================================
"""

from enum import Enum
from typing import Dict, Any, List, Optional
try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default


class NetworkProfileType(str, Enum):
    FIBER_BROADBAND = "FIBER_BROADBAND"
    RURAL_2G_EDGE = "RURAL_2G_EDGE"
    INTERMITTENT_LOSS = "INTERMITTENT_LOSS"
    COMPLETE_BLACKOUT = "COMPLETE_BLACKOUT"


class CrdtOperationType(str, Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    MERGE = "MERGE"
    ATTENDANCE_PUNCH = "ATTENDANCE_PUNCH"
    MCQ_ANSWER = "MCQ_ANSWER"


class CrdtMutationDTO(BaseModel):
    mutation_id: str = Field(..., description="Unique client-generated UUID for the mutation")
    idempotency_key: str = Field(..., description="SHA-256 HMAC of payload + client nonce for replay prevention")
    peer_id: str = Field(..., description="Device or peer identifier that generated the mutation")
    entity_type: str = Field(..., description="Domain entity: EXAM_SUBMISSION, WHITEBOARD_STROKE, ATTENDANCE")
    entity_id: str = Field(..., description="Target entity ID e.g. quiz_attempt_881")
    op_type: str = Field("MCQ_ANSWER", description="CRDT operation type")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary payload content")
    vector_clock: Dict[str, int] = Field(default_factory=dict, description="Lamport/Vector clock state per peer")
    client_timestamp: str = Field(..., description="ISO 8601 client timestamp")
    is_synced: bool = Field(False, description="Whether mutation has reconciled with Supabase cloud")


class MutationStageRequest(BaseModel):
    peer_id: str = Field(..., description="Originating peer ID")
    mutations: List[CrdtMutationDTO] = Field(..., description="Batch of local mutations staged while offline")
    network_profile: Optional[str] = Field("FIBER_BROADBAND", description="Current simulated or physical network profile")


class MutationStageResponse(BaseModel):
    staged_count: int
    rejected_count: int
    current_queue_depth: int
    storage_bytes: int
    message: str
    timestamp: str


class PeerMeshNodeDTO(BaseModel):
    peer_id: str = Field(..., description="Unique peer device ID")
    student_name: str = Field(..., description="Student / Candidate name")
    device_type: str = Field("Laptop", description="Device platform (Mobile, Tablet, Laptop)")
    is_online: bool = Field(True, description="Whether peer has WAN or local mesh connectivity")
    latency_ms: float = Field(12.0, description="P2P WebRTC DataChannel ping latency")
    hop_count: int = Field(1, description="Mesh routing hops to nearest WAN gateway")
    direct_connected_peers: List[str] = Field(default_factory=list, description="Directly peered devices in mesh")


class MeshTopologyResponse(BaseModel):
    network_profile: str
    active_mesh_id: str
    nodes: List[Dict[str, Any]]
    mesh_edges: List[Dict[str, Any]]
    total_peers: int
    wan_gateway_available: bool
    gossip_round_trip_ms: float
    timestamp: str


class ChaosSimulationRequest(BaseModel):
    network_profile: str = Field("INTERMITTENT_LOSS", description="Network chaos profile")
    packet_loss_pct: Optional[float] = Field(30.0, description="Simulated dropped packets percentage [0 - 100]")
    latency_ms: Optional[float] = Field(450.0, description="Simulated round-trip latency in ms")
    bandwidth_kbps: Optional[float] = Field(64.0, description="Simulated throughput cap in Kbps")


class ChaosSimulationResponse(BaseModel):
    profile_active: str
    status: str
    simulated_packet_loss_pct: float
    simulated_latency_ms: float
    bandwidth_limit_kbps: float
    queued_mutations_count: int
    delivered_mutations_count: int
    data_loss_rate_pct: float
    offline_retention_guaranteed: bool
    timestamp: str


class ReconcileBatchRequest(BaseModel):
    batch_id: str = Field(..., description="Reconciliation batch identifier")
    peer_id: str = Field(..., description="Reporting peer ID")
    mutations: List[CrdtMutationDTO] = Field(..., description="List of mutations being reconciled")
    client_merkle_root: Optional[str] = Field(None, description="Client computed SHA-256 Merkle root")


class ReconcileBatchResponse(BaseModel):
    batch_id: str
    reconciled_count: int
    conflicts_resolved: int
    server_merkle_root: str
    attestation_signature: str
    sync_latency_ms: float
    status: str
    applied_to_supabase: bool
    reconciled_at: str
