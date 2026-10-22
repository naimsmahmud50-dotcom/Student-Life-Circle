# ==============================================================================
# File: backend/app/schemas/jwks_query_hardener_and_cdc_schema.py
# Phase: 49 - Supabase JWKS, Query Hardener & CDC Schemas
# Topic: Edge Token Binding, PostgREST Parameter Shield & CDC Engine Schemas
# Description: Defines dual-resilience Pydantic data models for Edge token verification,
#              JWKS key rotation, PostgREST query inspection, and CDC WAL event processing.
# ==============================================================================

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default

from typing import Dict, Any, List, Optional

# --- JWKS & Edge Token Verification Models ---

class JWKSRotationRequest(BaseModel):
    new_kid: str = Field(..., description="Unique key ID for the new signing key")
    algorithm: str = Field("RS256", description="Asymmetric algorithm (RS256 or ES256)")

class JWKSRotationResponse(BaseModel):
    rotated_successfully: bool
    active_kid: str
    algorithm: str
    total_keys: int

class EdgeTokenVerificationRequest(BaseModel):
    header: Dict[str, Any] = Field(..., description="JWT header containing alg and kid")
    payload: Dict[str, Any] = Field(..., description="JWT claims containing sub, iss, aud, jti, exp")
    client_supplied_user_id: Optional[str] = Field(None, description="Optional user ID supplied in request payload to test BFLA/IDOR")

class EdgeTokenVerificationResponse(BaseModel):
    valid: bool
    error_code: Optional[str] = None
    message: str
    server_uid: Optional[str] = None
    tenant_id: Optional[str] = None
    role: Optional[str] = None
    verified_at: Optional[float] = None

# --- PostgREST Query Hardening Models ---

class PostgrestQueryInspectRequest(BaseModel):
    table_name: str = Field(..., description="Target database table")
    raw_query_params: Dict[str, Any] = Field(..., description="Raw query parameters as parsed from HTTP request")
    verified_jwt_claims: Dict[str, Any] = Field(..., description="Verified JWT claims including tenant_id and role")

class PostgrestQueryInspectResponse(BaseModel):
    is_safe: bool
    table_name: str
    violations: List[Dict[str, Any]]
    hardened_params: Dict[str, Any]
    embed_depth: int
    enforced_tenant_id: str

# --- Database CDC & Audit Models ---

class WALEventIngestRequest(BaseModel):
    event_type: str = Field(..., description="INSERT, UPDATE, or DELETE")
    table_name: str = Field(..., description="Target Postgres table")
    record_id: str = Field(..., description="Primary key identifier")
    record_data: Dict[str, Any] = Field(..., description="Row data payload")
    actor_id: str = Field("system", description="User or system triggering mutation")
    commit_lsn: Optional[str] = Field(None, description="Postgres Log Sequence Number")

class WALEventIngestResponse(BaseModel):
    success: bool
    sequence_index: int
    block_hash: str
    commit_lsn: str
    tamper_evident: bool

class AuditIntegrityVerificationResponse(BaseModel):
    chain_valid: bool
    total_blocks_verified: Optional[int] = None
    tamper_detected_at_index: Optional[int] = None
    genesis_hash: Optional[str] = None
    latest_head_hash: Optional[str] = None
    status: str
    error: Optional[str] = None

class RealtimeBroadcastAuthRequest(BaseModel):
    event_index: int = Field(..., description="Index of the ingested WAL event in the audit chain")
    subscriber_user_id: str = Field(..., description="UUID of the connected websocket subscriber")
    subscriber_role: str = Field("student", description="Role of the subscriber (student, teacher, admin)")

class RealtimeBroadcastAuthResponse(BaseModel):
    authorized: bool
    broadcast_payload: Optional[Dict[str, Any]] = None
    message: str
