# ==============================================================================
# File: backend/app/schemas/pooler_masking_fdw_schema.py
# Phase: 53 - Connection Pooler Hygiene, Dynamic Masking & Federated FDW Schemas
# Topic: Connection Session State Hygiene, Dynamic Row/Column Masking & FDW Security
# Description: Defines dual-resilience Pydantic models for Pooler session isolation,
#              dynamic student record masking, and federated postgres_fdw audits.
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

# --- Connection Pooler Hygiene Models ---

class PoolerSessionAuditRequest(BaseModel):
    sql_statements: List[str] = Field(..., description="List of SQL statements executed in connection session")

class PoolerSessionAuditResponse(BaseModel):
    is_hygienic: bool
    risk_score: float
    total_statements: int
    violations_detected: int
    violations: List[Dict[str, Any]]
    safe_sql_patch: str

class PoolerResetVerifyRequest(BaseModel):
    connection_meta: Dict[str, Any] = Field(..., description="Recycled connection metadata and reset queries")

class PoolerResetVerifyResponse(BaseModel):
    reset_verified: bool
    status: str
    issues: List[str]
    pool_mode: str
    recommendation: str

class PoolerBenchmarkRequest(BaseModel):
    concurrent_tenants: int = Field(10, description="Number of concurrent tenant sessions")
    total_transactions: int = Field(50, description="Total transactions to simulate")

class PoolerBenchmarkResponse(BaseModel):
    concurrent_tenants: int
    total_transactions: int
    safe_transactions: int
    prevented_contaminations: int
    isolation_pass_rate: float
    avg_reset_latency_ms: float
    benchmark_status: str

# --- Dynamic Data Masking Models ---

class StudentRecordMaskRequest(BaseModel):
    record: Dict[str, Any] = Field(..., description="Raw student record containing PII and academic data")
    viewer_role: str = Field("student", description="Role: student, public, faculty, bursar, academic_dean, registrar")
    masking_policy: Optional[Dict[str, bool]] = Field(None, description="Optional custom boolean flags for masking")

class StudentRecordMaskResponse(BaseModel):
    masked_record: Dict[str, Any]
    viewer_role: str
    applied_rules: List[str]
    redaction_count: int
    watermark: str

class MaskedViewSqlGenerateRequest(BaseModel):
    table_name: str = Field("students", description="Source PostgreSQL table name")
    view_name: Optional[str] = Field(None, description="Optional target view name")
    column_rules: Optional[Dict[str, str]] = Field(None, description="Custom column CASE expressions")

class MaskedViewSqlGenerateResponse(BaseModel):
    sql: str
    table_name: str
    view_name: str

class InferenceRiskEvaluateRequest(BaseModel):
    dataset: List[Dict[str, Any]] = Field(..., description="Sample student records dataset")
    masked_columns: List[str] = Field(..., description="Columns considered quasi-identifiers (e.g. gpa, department)")

class InferenceRiskEvaluateResponse(BaseModel):
    records_evaluated: int
    unique_quasi_tuples: int
    uniques_count: int
    re_identification_risk_percent: float
    risk_rating: str
    findings: List[str]

# --- Federated FDW Security Models ---

class FdwServerAuditRequest(BaseModel):
    server_config: Dict[str, Any] = Field(..., description="PostgreSQL FOREIGN SERVER definition and options")

class FdwServerAuditResponse(BaseModel):
    server_name: str
    compliant: bool
    risk_score: float
    findings_count: int
    findings: List[Dict[str, str]]
    hardened_options: Dict[str, Any]

class FdwUserMappingsValidateRequest(BaseModel):
    user_mappings: List[Dict[str, Any]] = Field(..., description="List of USER MAPPING definitions on foreign servers")

class FdwUserMappingsValidateResponse(BaseModel):
    is_secure: bool
    total_mappings_analyzed: int
    violations_detected: int
    violations: List[Dict[str, Any]]
    status: str

class FederatedQuerySanitizeRequest(BaseModel):
    remote_sql: str = Field(..., description="Federated query intended for remote university server")
    allowed_schemas: Optional[List[str]] = Field(None, description="Permitted remote database schemas")

class FederatedQuerySanitizeResponse(BaseModel):
    allowed: bool
    sanitized_sql: str
    target_schema: str
    rejection_reason: Optional[str] = None
    security_flag: str
