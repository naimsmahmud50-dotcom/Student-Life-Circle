# ==============================================================================
# File: backend/app/schemas/presence_rls_and_anonymization_schema.py
# Phase: 51 - Realtime Presence, RLS Compliance & Privacy Vault Schemas
# Topic: Realtime Ephemeral Sessions, PostgreSQL Compliance & Differential Privacy
# Description: Defines dual-resilience Pydantic models for Realtime presence authentication,
#              RLS policy compliance audits, and K-Anonymity privacy vault evaluations.
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

# --- Realtime Presence Integrity Models ---

class PresenceTicketGenerateRequest(BaseModel):
    channel_name: str = Field(..., description="Target Realtime presence channel name (e.g. room:circle_101)")
    user_id: str = Field(..., description="User UUID")
    user_role: str = Field("student", description="Role: student, mentor, proctor, admin")
    ttl_seconds: int = Field(300, description="Ticket validity TTL in seconds")

class PresenceTicketGenerateResponse(BaseModel):
    channel_name: str
    user_id: str
    user_role: str
    session_id: str
    expires_at: float
    presence_signature: str
    issued_at: float

class PresenceJoinRequest(BaseModel):
    channel_name: str = Field(..., description="Target Realtime presence channel name")
    user_id: str = Field(..., description="User UUID")
    session_id: str = Field(..., description="Session identifier from presence ticket")
    user_role: str = Field(..., description="User role")
    expires_at: float = Field(..., description="Expiration timestamp from presence ticket")
    signature: str = Field(..., description="HMAC-SHA256 signature from presence ticket")
    client_metadata: Optional[Dict[str, Any]] = Field(None, description="Optional client state metadata")

class PresenceJoinResponse(BaseModel):
    authorized: bool
    channel_name: Optional[str] = None
    session_id: Optional[str] = None
    active_peer_count: Optional[int] = None
    error_code: Optional[str] = None
    message: str

class PresenceHeartbeatRequest(BaseModel):
    channel_name: str = Field(..., description="Channel name")
    session_id: str = Field(..., description="Active session ID")

class PresenceHeartbeatResponse(BaseModel):
    recorded: bool
    message: str

# --- PostgreSQL RLS Compliance Models ---

class RlsComplianceScanRequest(BaseModel):
    table_name: str = Field(..., description="Name of the PostgreSQL database table")
    rls_enabled: bool = Field(..., description="Whether RLS is enabled on the table")
    policies: List[Dict[str, Any]] = Field([], description="List of configured policies {name, cmd, using, with_check}")

class RlsComplianceScanResponse(BaseModel):
    table_name: str
    rls_enabled: bool
    compliance_score: int
    status: str
    violations: List[Dict[str, Any]]
    remediation_sql: str

class SecurityDefinerScanRequest(BaseModel):
    function_name: str = Field(..., description="Name of the stored procedure / SQL function")
    security_type: str = Field("SECURITY INVOKER", description="SECURITY DEFINER or SECURITY INVOKER")
    search_path_set: bool = Field(False, description="Whether function explicitly defines SET search_path = ''")

class SecurityDefinerScanResponse(BaseModel):
    function_name: str
    security_type: str
    is_secure: bool
    violations: List[Dict[str, Any]]
    remediation_sql: str

# --- Differential Privacy & Anonymization Models ---

class LaplaceNoiseInjectRequest(BaseModel):
    true_value: float = Field(..., description="Exact numerical aggregate value (e.g. average GPA)")
    sensitivity: float = Field(1.0, description="Global query sensitivity")
    epsilon: float = Field(0.5, description="Privacy budget epsilon")

class LaplaceNoiseInjectResponse(BaseModel):
    true_value: float
    noisy_value: float
    noise_added: float
    epsilon_budget: float
    scale_parameter: float
    privacy_guarantee: str

class KAnonymityEvaluateRequest(BaseModel):
    records: List[Dict[str, Any]] = Field(..., description="List of dataset rows")
    quasi_identifiers: List[str] = Field(..., description="Quasi-identifier attribute columns")

class KAnonymityEvaluateResponse(BaseModel):
    is_k_anonymous: bool
    k_min_achieved: int
    required_k_min: int
    total_equivalence_classes: int
    total_records: int
    max_re_identification_risk: float
    status: str
