"""
Pydantic Schemas for Phase 56: Production Schema Migration, Drift Guard & Index Optimizer.
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


# --- Schemas for Schema Migration Engine ---
class MigrationPlanRequest(BaseModel):
    version_id: str = Field(..., description="Semantic version sequence, e.g. 20261015_01")
    migration_name: str = Field(..., description="Descriptive slug, e.g. add_academic_score_index")
    target_table: str = Field(..., description="Target database table")
    operation_type: str = Field(..., description="ADD_COLUMN, CREATE_INDEX, ALTER_TYPE, DROP_TABLE")
    column_definitions: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    index_definitions: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    raw_ddl_forward: Optional[str] = Field(None, description="Optional raw SQL forward statement")


class MigrationPlanResponse(BaseModel):
    version_id: str
    migration_name: str
    safety_verdict: str
    risk_score: int
    safe_to_apply: bool
    forward_sql: str
    rollback_sql: str
    lock_impact_estimate: str
    warnings: List[str]


# --- Schemas for Schema Drift Detector ---
class SchemaDriftScanRequest(BaseModel):
    environment_name: str = Field(..., description="Environment: staging, production, dr_replica")
    declared_schema: Dict[str, Any] = Field(..., description="Declared authoritative schema manifest")
    live_schema: Dict[str, Any] = Field(..., description="Live database catalog schema manifest")


class SchemaDriftScanResponse(BaseModel):
    environment_name: str
    drift_detected: bool
    declared_manifest_digest: str
    live_manifest_digest: str
    drift_details: List[Dict[str, Any]]
    remediation_sql: str
    parity_status: str


# --- Schemas for Index Optimizer Advisor ---
class IndexRecommendRequest(BaseModel):
    table_name: str = Field(..., description="Table name to optimize")
    query_clause: str = Field(..., description="High-frequency WHERE / ORDER BY query string")
    filter_columns: List[str] = Field(..., description="Filter columns")
    sort_columns: Optional[List[str]] = Field(default_factory=list, description="Sort columns")
    table_row_count: int = Field(default=100000, description="Total table rows")
    estimated_matched_rows: int = Field(default=250, description="Estimated matching rows")


class IndexRecommendResponse(BaseModel):
    table_name: str
    recommended_index_name: str
    index_type: str
    selectivity: float
    create_index_sql: str
    estimated_speedup_percent: float
    lock_safety: str


class IndexRedundancyScanResponse(BaseModel):
    total_indexes_scanned: int
    redundant_indexes_found: int
    redundancies: List[Dict[str, Any]]
    saved_write_iops_estimate_percent: float
