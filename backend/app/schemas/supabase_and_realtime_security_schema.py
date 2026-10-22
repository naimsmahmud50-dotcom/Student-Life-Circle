"""
================================================================================
MODULE: Supabase Security, Edge Boundary & Realtime Cryptographic Schemas
TOPIC: Pydantic Validation Models for RLS, PostgREST Defense, RPC Audit & Realtime
FILE: backend/app/schemas/supabase_and_realtime_security_schema.py
PURPOSE: Strict data validation contracts for Strix-Supabase API endpoints.
================================================================================
"""

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


class RlsEvaluationRequest(BaseModel):
    table_name: str = Field(..., description="Target database table name")
    action: str = Field(..., description="Action: SELECT, INSERT, UPDATE, or DELETE")
    caller_role: str = Field(..., description="Caller role: anon, authenticated, or service_role")
    caller_uid: Optional[str] = Field(None, description="User UUID from authenticated JWT")
    caller_tenant_id: Optional[str] = Field(None, description="Tenant UUID from authenticated JWT")
    target_owner_id: Optional[str] = Field(None, description="Owner UUID of target row")
    target_tenant_id: Optional[str] = Field(None, description="Tenant UUID of target row")
    client_payload_user_id: Optional[str] = Field(None, description="User ID passed in client body")
    is_browser_origin: bool = Field(False, description="True if request originates from browser client")


class RlsEvaluationResponse(BaseModel):
    verdict: str
    status_code: int
    reason: str
    applied_policy: str
    threat_level: str


class RlsGeneratePolicyRequest(BaseModel):
    table_name: str
    owner_column: str = "user_id"
    tenant_column: Optional[str] = "tenant_id"


class RlsGeneratePolicyResponse(BaseModel):
    table_name: str
    sql_script: str


class PostgrestSanitizeRequest(BaseModel):
    query_params: Dict[str, Any] = Field(..., description="URL query parameters from PostgREST client")


class PostgrestSanitizeResponse(BaseModel):
    is_safe: bool
    threat_score: int
    anomalies: List[str]
    sanitized_params: Dict[str, Any]
    recommended_action: str


class RpcAuditRequest(BaseModel):
    function_name: str
    sql_definition: str
    execution_context: str = "SECURITY INVOKER"


class RpcAuditResponse(BaseModel):
    function_name: str
    execution_context: str
    safety_score: int
    is_compliant: bool
    vulnerabilities: List[str]
    has_search_path_pinned: bool
    verifies_auth_uid: bool
    remediation_sql: str


class EdgeJwtVerifyRequest(BaseModel):
    auth_header: Optional[str] = None
    apikey_header: Optional[str] = None
    expected_issuer: str = "https://agrojatra.supabase.co/auth/v1"


class EdgeJwtVerifyResponse(BaseModel):
    is_valid: bool
    status_code: int
    reason: str
    user_id: Optional[str] = None
    role: str
    issuer: Optional[str] = None
    audience: Optional[str] = None


class StorageSignedUrlRequest(BaseModel):
    bucket_id: str
    file_path: str
    user_id: str
    ttl_seconds: int = 300
    content_type: str = "application/pdf"


class StorageSignedUrlResponse(BaseModel):
    bucket_id: str
    file_path: str
    is_private: bool
    signed_url: str
    expires_at: int
    ttl_seconds: int
    response_headers: Dict[str, str]
    security_status: str


class RealtimeChannelAuthRequest(BaseModel):
    channel_name: str
    user_id: str
    user_role: str = "student"
    tenant_id: str = "tenant_main"
    enrolled_circles: Optional[List[str]] = None
    linked_guardian_ids: Optional[List[str]] = None


class RealtimeChannelAuthResponse(BaseModel):
    authorized: bool
    channel_name: str
    access_level: str
    join_token: Optional[str] = None
    reason: str
