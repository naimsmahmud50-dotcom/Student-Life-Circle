"""
Pydantic v2 Data Models: Zero-Knowledge Airgap Attendance & DID Attestation (Phase 68)
Enterprise schemas for rolling proximity beacons, student DID credentials,
Ed25519 signature verification, anti-proxy replay defense, and Merkle attendance trees.
"""

from typing import List, Dict, Optional, Any
try:
    from pydantic import BaseModel, Field, ConfigDict
except ImportError:
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default
    def ConfigDict(**kwargs):
        return {}

class RollingBeaconTokenDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    beacon_id: str = Field(..., description="Proximity beacon emitter ID (e.g. BCN-DHAKA-10B)")
    classroom_id: str = Field(..., description="Target classroom room/section identifier")
    epoch_index: int = Field(..., ge=0, description="Rolling 30-second epoch counter")
    epoch_seconds: int = Field(30, description="Beacon validity interval in seconds")
    rolling_hash: str = Field(..., min_length=64, max_length=64, description="SHA-256 rolling HMAC token")
    teacher_did: str = Field(..., description="Institutional DID of the invigilator/teacher")
    valid_until: str = Field(..., description="ISO 8601 expiration timestamp")

class StudentDidCredentialDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    did: str = Field(..., description="W3C DID uri (e.g. did:slc:student:bd-dhaka-001)")
    student_id: str = Field(..., description="Academic student registration ID")
    student_name: str = Field(..., description="Full student name")
    roll_number: int = Field(..., ge=1)
    public_key_ed25519: str = Field(..., description="Ed25519 public key hex for signature validation")
    enrolled_classroom: str = Field(..., description="Classroom code (e.g. CLS-DHAKA-10B)")
    status: str = Field("verified", description="'verified', 'flagged_proxy', or 'unverified'")

class AttendancePunchRequest(BaseModel):
    classroom_id: str = Field(..., min_length=3, max_length=64)
    student_did: str = Field(..., min_length=5, max_length=128)
    beacon_epoch_hash: str = Field(..., min_length=64, max_length=64)
    nonce: str = Field(..., min_length=8, max_length=64)
    signature_ed25519: str = Field(..., min_length=64, max_length=128)
    timestamp_client: str = Field(...)

class AttendancePunchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    punch_id: str
    student_did: str
    student_name: str
    roll_number: int
    verified_at: str
    merkle_leaf_hash: str
    anti_proxy_verdict: str  # "VERIFIED_GENUINE", "REPLAY_REJECTED", "INVALID_SIGNATURE", "STALE_BEACON"
    message: str

class ClassroomAttendanceSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str
    classroom_id: str
    teacher_did: str
    total_enrolled: int
    total_punched: int
    attendance_rate_pct: float
    proxy_attacks_blocked: int
    merkle_root: str
    cloud_settlement_status: str  # "Airgap Staged", "Quorum Verified", "Settled to Supabase"
    beacon: RollingBeaconTokenDTO
    punches: List[AttendancePunchResponse] = Field(default_factory=list)

class MerkleBatchSettleRequest(BaseModel):
    session_id: str
    teacher_signature: str

class MerkleBatchSettleResponse(BaseModel):
    session_id: str
    settled_punches_count: int
    final_merkle_root: str
    settlement_timestamp: str
    supabase_transaction_id: str
    status: str
