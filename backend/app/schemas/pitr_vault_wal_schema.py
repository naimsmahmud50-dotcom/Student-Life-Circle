# ==============================================================================
# File: backend/app/schemas/pitr_vault_wal_schema.py
# Phase: 54 - PITR Disaster Recovery, Secret Rotation Vault & WAL Validator Schemas
# Topic: Point-in-Time Recovery Drills, Bundle Secret Leaks & WAL Archive Continuity
# Description: Defines dual-resilience Pydantic models for PITR snapshot simulation,
#              zero-downtime secret rotation, and PostgreSQL continuous WAL verification.
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

# --- PITR Disaster Recovery Models ---

class PitrSnapshotCreateRequest(BaseModel):
    target_epoch: int = Field(..., description="Target recovery epoch timestamp")
    snapshot_tag: str = Field(..., description="Snapshot label/tag (e.g. daily_pre_grade_release)")
    table_manifests: Dict[str, Dict[str, Any]] = Field(..., description="Table names to row counts and checksums")

class PitrSnapshotCreateResponse(BaseModel):
    snapshot_id: str
    snapshot_tag: str
    target_epoch: int
    basebackup_lsn: str
    manifest_digest: str
    tables: Dict[str, Dict[str, Any]]
    created_at: int
    status: str

class PitrDrillSimulateRequest(BaseModel):
    snapshot_id: str = Field(..., description="Snapshot ID to restore from")
    disaster_scenario: str = Field("accidental_drop_table", description="Scenario: accidental_drop_table, ransomware, corrupt_migration")
    target_recovery_epoch: Optional[int] = Field(None, description="Optional specific epoch target")

class PitrDrillSimulateResponse(BaseModel):
    success: bool
    drill_id: Optional[str] = None
    snapshot_id: str
    snapshot_tag: Optional[str] = None
    basebackup_lsn: Optional[str] = None
    disaster_scenario: str
    target_epoch: Optional[int] = None
    rpo_seconds: Optional[int] = None
    rpo_compliant: Optional[bool] = None
    rto_seconds: Optional[int] = None
    rto_compliant: Optional[bool] = None
    wal_segments_replayed: Optional[int] = None
    status: str

class PitrConsistencyVerifyRequest(BaseModel):
    original_manifest: Dict[str, Dict[str, Any]] = Field(..., description="Pre-disaster table manifests")
    restored_manifest: Dict[str, Dict[str, Any]] = Field(..., description="Post-restore table manifests")

class PitrConsistencyVerifyResponse(BaseModel):
    is_consistent: bool
    total_tables_checked: int
    mismatched_tables_count: int
    mismatched_tables: List[str]
    total_original_rows: int
    total_restored_rows: int
    data_loss_percentage: float
    integrity_verdict: str

# --- Secret Rotation Vault Models ---

class SecretScanRequest(BaseModel):
    content_or_bundle: str = Field(..., description="Client bundle JS, HTML markup, or API response text")

class SecretScanResponse(BaseModel):
    is_safe: bool
    has_critical_leak: bool
    total_leaks_found: int
    findings: List[Dict[str, Any]]
    remediation: str

class SecretRotationRequest(BaseModel):
    key_type: str = Field("service_role", description="Credential type to rotate: service_role, jwt_secret, anon")
    grace_period_seconds: int = Field(300, description="Overlapping grace period in seconds")

class SecretRotationResponse(BaseModel):
    rotation_id: str
    key_type: str
    active_key_id: str
    new_secret_masked: str
    deprecating_key_id: Optional[str] = None
    grace_period_seconds: int
    status: str
    message: str

class SecretRevokeRequest(BaseModel):
    key_id: str = Field(..., description="Credential identifier to immediately revoke")
    reason: str = Field(..., description="Security reason for immediate revocation")

class SecretRevokeResponse(BaseModel):
    key_id: str
    status: str
    revoked_at: int
    reason: str
    message: str

# --- WAL Archive Integrity Models ---

class WalRegisterRequest(BaseModel):
    segment_name: str = Field(..., description="24-character hex PostgreSQL WAL filename")
    timeline_id: int = Field(1, description="Database timeline identifier")
    segment_number: int = Field(..., description="Sequential segment number")
    checksum: str = Field(..., description="SHA-256 or CRC32 segment payload checksum")

class WalRegisterResponse(BaseModel):
    accepted: bool
    segment_name: str
    timeline_id: Optional[int] = None
    segment_number: Optional[int] = None
    checksum: Optional[str] = None
    archived_at: Optional[int] = None
    error: Optional[str] = None

class WalVerifyContinuityResponse(BaseModel):
    is_continuous: bool
    total_segments: int
    timelines_count: int
    missing_segments_count: int
    missing_segments: List[str]
    latest_segment: Optional[str] = None
    status: str

class WalEvaluateLagResponse(BaseModel):
    current_lag_seconds: int
    sla_seconds: int
    sla_met: bool
    latest_segment: Optional[str] = None
    total_archived_mb: int
    throughput_mb_sec: float
    status: str
