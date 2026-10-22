# ==============================================================================
# File: backend/app/schemas/edge_gateway_webhook_audit_schema.py
# Phase: 52 - Edge Function Zero-Trust Gateway, Webhook Guard & PostgREST Audit Schemas
# Topic: Edge Verification, Svix Webhook Replay Protection & Hash-Chained Audit Trail
# Description: Defines dual-resilience Pydantic models for Edge function zero-trust validation,
#              Database webhook replay defense, and PostgREST cryptographic audit logs.
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

# --- Edge Function Zero-Trust Gateway Models ---

class EdgeRequestVerifyRequest(BaseModel):
    headers: Dict[str, str] = Field(..., description="Incoming HTTP request headers")
    secret: Optional[str] = Field(None, description="Optional JWT signing secret override")
    allowed_audiences: Optional[List[str]] = Field(None, description="Permitted audience claims")

class EdgeRequestVerifyResponse(BaseModel):
    is_valid: bool
    reason: str
    security_flags: List[str]
    user_id: Optional[str] = None
    role: str = "anonymous"
    tenant_id: Optional[str] = None
    claims: Dict[str, Any] = {}

class EdgeActionAuthorizeRequest(BaseModel):
    user_role: str = Field(..., description="Caller authenticated role")
    function_name: str = Field(..., description="Target serverless Edge function")
    requested_action: str = Field(..., description="Action to perform (e.g. finalize, disburse)")

class EdgeActionAuthorizeResponse(BaseModel):
    allowed: bool
    user_role: str
    function_name: str
    requested_action: str
    required_roles: List[str]
    timestamp: str
    verdict_signature: str
    message: str

# --- Database Webhook Replay Guard Models ---

class WebhookVerifyRequest(BaseModel):
    headers: Dict[str, str] = Field(..., description="Webhook HTTP headers (e.g. webhook-id, webhook-signature)")
    payload: str = Field(..., description="Raw text payload of the webhook")
    secret: Optional[str] = Field(None, description="Svix webhook secret (whsec_...)")
    max_age_seconds: int = Field(300, description="Max acceptable age in seconds before replay cutoff")

class WebhookVerifyResponse(BaseModel):
    verified: bool
    reason: str
    error_code: Optional[str] = None
    msg_id: Optional[str] = None
    timestamp: Optional[int] = None
    latency_seconds: Optional[int] = None

class WebhookAttestRequest(BaseModel):
    event_type: str = Field(..., description="Event type (e.g. INSERT, UPDATE, DELETE)")
    table_name: str = Field(..., description="Source database table")
    record_id: str = Field(..., description="UUID or ID of the affected record")
    payload: Dict[str, Any] = Field(..., description="Event record payload dictionary")

class WebhookAttestResponse(BaseModel):
    attestation_id: str
    event_type: str
    table_name: str
    record_id: str
    payload_sha256: str
    verified_at: int
    attestation_signature: str
    status: str

# --- PostgREST Hash-Chained Audit Trail Models ---

class AuditRecordRequest(BaseModel):
    actor_id: str = Field(..., description="Identifier of the executing user/service")
    actor_role: str = Field(..., description="Role: student, faculty, academic_dean, service_role")
    action: str = Field(..., description="Audit action: RPC_EXEC, ROW_INSERT, ROW_UPDATE, ROW_DELETE")
    schema_name: str = Field("public", description="Database schema")
    target_entity: str = Field(..., description="Target RPC or table name")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Contextual event payload")
    ip_address: str = Field("127.0.0.1", description="Client source IP address")

class AuditRecordResponse(BaseModel):
    index: int
    timestamp: int
    actor_id: str
    actor_role: str
    action: str
    schema_name: str
    target_entity: str
    metadata: Dict[str, Any]
    ip_address: str
    prev_hash: str
    entry_hash: str

class AuditChainVerifyResponse(BaseModel):
    is_valid: bool
    total_entries: int
    chain_head_hash: str
    broken_index: Optional[int] = None
    reason: str

class AuditAnomaliesResponse(BaseModel):
    threat_level: str
    anomalies_detected: int
    anomalies: List[Dict[str, Any]]
    analyzed_entries: int
    window_seconds: int
