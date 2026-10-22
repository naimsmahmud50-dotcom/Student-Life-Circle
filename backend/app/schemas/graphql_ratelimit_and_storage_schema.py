# ==============================================================================
# File: backend/app/schemas/graphql_ratelimit_and_storage_schema.py
# Phase: 50 - Supabase GraphQL, Rate Limit & Storage Schemas
# Topic: Schema Introspection, Token Bucket Rate Limiting, & Multipart Antivirus
# Description: Defines dual-resilience Pydantic data models for pg_graphql query
#              inspection, edge token bucket rate limiting, and storage upload sanitization.
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

# --- pg_graphql Inspection Models ---

class GraphqlQueryInspectRequest(BaseModel):
    query: str = Field(..., description="GraphQL query or mutation string")
    caller_role: str = Field("anon", description="Caller role: anon, student, teacher, developer, admin")
    caller_user_id: Optional[str] = Field(None, description="Optional caller user UUID")

class GraphqlQueryInspectResponse(BaseModel):
    authorized: bool
    caller_role: str
    calculated_depth: int
    max_allowable_depth: int
    complexity_score: int
    max_complexity_budget: int
    violations: List[Dict[str, Any]]
    status: str

class GraphqlParityAuditRequest(BaseModel):
    table_name: str = Field(..., description="Target database table")
    postgrest_allowed_columns: List[str] = Field(..., description="Columns exposed via PostgREST RLS")
    graphql_type_fields: List[str] = Field(..., description="Fields defined in pg_graphql type schema")

class GraphqlParityAuditResponse(BaseModel):
    table_name: str
    has_parity_risk: bool
    graphql_overexposed_fields: List[str]
    postgrest_only_fields: List[str]
    recommendation: str

# --- Edge Rate Limiting Models ---

class EdgeRateLimitCheckRequest(BaseModel):
    client_ip: str = Field(..., description="IPv4 or IPv6 client address")
    user_id: Optional[str] = Field(None, description="User UUID if request is authenticated")
    tenant_id: str = Field("inst_default", description="Institutional tenant identifier")
    endpoint: str = Field("/rest/v1/data", description="Requested API endpoint URI")
    custom_cost: Optional[int] = Field(None, description="Optional custom token consumption weight")

class EdgeRateLimitCheckResponse(BaseModel):
    allowed: bool
    client_key: str
    reason: Optional[str] = None
    detail: str
    remaining_tokens: float
    retry_after_seconds: int
    penalty_active: bool

# --- Storage Multipart & Sanitizer Models ---

class StoragePresignedTicketRequest(BaseModel):
    bucket_id: str = Field(..., description="Target storage bucket ID (e.g. transcripts, bursary_receipts)")
    file_path: str = Field(..., description="Target object path inside bucket")
    user_id: str = Field(..., description="Owner user UUID")
    allowed_mime_types: List[str] = Field(..., description="List of accepted MIME types")
    max_size_bytes: int = Field(10485760, description="Maximum allowable file size in bytes")
    ttl_seconds: int = Field(900, description="Ticket validity duration in seconds")

class StoragePresignedTicketResponse(BaseModel):
    ticket_id: str
    bucket_id: str
    target_path: str
    user_id: str
    max_size_bytes: int
    allowed_mime_types: List[str]
    expires_at: float
    hmac_signature: str
    upload_endpoint: str

class StorageUploadSanitizeRequest(BaseModel):
    file_content_base64: str = Field(..., description="Base64 encoded binary file payload")
    declared_mime_type: str = Field(..., description="Declared HTTP Content-Type header")
    file_name: str = Field(..., description="Original filename with extension")

class StorageUploadSanitizeResponse(BaseModel):
    safe: bool
    was_sanitized: bool
    violations: List[Dict[str, Any]]
    declared_mime_type: str
    file_size_bytes: int
    enforced_download_headers: Dict[str, str]
    status: str
