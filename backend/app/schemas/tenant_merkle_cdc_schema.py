"""
Pydantic Schemas for Phase 55: Zero-Knowledge Multi-Tenant Partitioning,
Row-Level Cryptographic Attestation & Cross-Region CDC Replication.
Dual-resilience fallback included for zero-dependency test execution.
"""

from typing import Dict, Any, List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default


# --- Schemas for Tenant Partitioning ---
class PartitionRouteRequest(BaseModel):
    tenant_id: str = Field(..., description="Unique institutional tenant identifier (e.g. inst_buet, inst_du)")
    table_name: str = Field(..., description="Base logical table (e.g. students, academic_records, exams)")
    auth_token_signature: Optional[str] = Field(None, description="Cryptographic signature binding tenant to caller")
    query_filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Requested query filters")


class PartitionRouteResponse(BaseModel):
    success: bool
    tenant_id: str
    target_partition_table: str
    pruning_boundary_enforced: bool
    sanitized_filter: Dict[str, Any]
    security_verdict: str
    message: str


class PartitionEscapeProbeRequest(BaseModel):
    tenant_id: str
    malicious_query_clause: str


class PartitionEscapeProbeResponse(BaseModel):
    blocked: bool
    tenant_id: str
    detected_vector: str
    mitigation_applied: str
    query_rejected: bool


# --- Schemas for Row-Level Merkle Attestation ---
class RowAttestationRequest(BaseModel):
    record_id: str
    tenant_id: str
    entity_type: str
    payload: Dict[str, Any]


class RowAttestationResponse(BaseModel):
    record_id: str
    tenant_id: str
    canonical_payload_digest: str
    hmac_signature: str
    timestamp: str
    attestation_status: str


class MerkleTreeBuildRequest(BaseModel):
    tenant_id: str
    records: List[Dict[str, Any]]


class MerkleTreeBuildResponse(BaseModel):
    tenant_id: str
    merkle_root: str
    total_leaves: int
    leaf_hashes: List[str]
    tree_depth: int
    build_timestamp: str


class MerkleProofVerificationRequest(BaseModel):
    merkle_root: str
    leaf_hash: str
    proof_path: List[Dict[str, str]]  # list of {"position": "left"|"right", "hash": str}


class MerkleProofVerificationResponse(BaseModel):
    is_valid: bool
    calculated_root: str
    expected_root: str
    verdict: str


# --- Schemas for Cross-Region CDC Replication ---
class CdcEventRequest(BaseModel):
    event_id: str
    region_origin: str
    table_name: str
    operation: str  # INSERT, UPDATE, DELETE
    row_data: Dict[str, Any]
    vector_clock: Dict[str, int]
    commit_lsn: str
    timestamp: float


class CdcEventResponse(BaseModel):
    event_id: str
    status: str
    applied_operation: str
    conflict_detected: bool
    resolution_strategy: str
    winning_region: str
    updated_vector_clock: Dict[str, int]


class ReplicationLagReportResponse(BaseModel):
    source_region: str
    target_region: str
    replication_slot: str
    byte_lag: int
    time_lag_seconds: float
    sla_status: str
    dlq_quarantine_count: int
