"""
Pydantic v2 Data Models: Distributed Shamir Secret Sharing & Ephemeral Exam Vault (Phase 69)
Enterprise schemas for k-of-n threshold cryptography, custodian key shares,
Lagrange interpolation requests, anti-tamper zeroization telemetry, and multisig receipts.
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

class ShamirShareDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    custodian_id: str = Field(..., description="Unique ID of the custodian holding this share")
    custodian_title: str = Field(..., description="Official title (e.g. Center Superintendent)")
    x_coordinate: int = Field(..., ge=1, description="Polynomial evaluation x-coordinate (1 to n)")
    y_share_hex: str = Field(..., description="Evaluation point f(x) mod p encoded as hex string")
    share_hash: str = Field(..., min_length=64, max_length=64, description="SHA-256 integrity hash of this share")
    issued_at: str = Field(..., description="ISO 8601 issuance timestamp")

class ExamCustodianDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    custodian_id: str = Field(..., description="Unique custodian identifier")
    name: str = Field(..., description="Full legal name of the appointed custodian")
    role: str = Field(..., description="Designation e.g. Head Examiner, Board Observer")
    public_key: str = Field(..., description="Public key / DID for cryptographic attestation")
    assigned_share_index: int = Field(..., ge=1, description="Associated polynomial x-index")
    is_share_presented: bool = Field(False, description="Whether this custodian has verified & submitted their share")
    verified_at: Optional[str] = Field(None, description="Timestamp when share was verified")

class EncryptedExamVaultDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vault_id: str = Field(..., description="UUID / Identifier of the exam vault")
    exam_code: str = Field(..., description="Course / Exam identifier (e.g. HSC-PHY-2026)")
    subject: str = Field(..., description="Subject name (e.g. Physics First Paper)")
    ciphertext_hex: str = Field(..., description="AES-256-GCM encrypted exam payload")
    iv_hex: str = Field(..., description="Initialization vector hex (12 bytes)")
    auth_tag_hex: str = Field(..., description="GCM authentication tag hex (16 bytes)")
    threshold_k: int = Field(3, ge=2, description="Minimum shares required for reconstruction")
    total_shares_n: int = Field(5, ge=2, description="Total shares distributed to custodians")
    prime_modulus_hex: str = Field(..., description="Finite field prime modulus p in hex")
    status: str = Field("LOCKED", description="'LOCKED', 'RECONSTRUCTED', 'TAMPER_ALERT', or 'WIPED'")
    created_at: str = Field(..., description="Creation timestamp")

class ThresholdReconstructRequest(BaseModel):
    vault_id: str = Field(..., min_length=3, max_length=64)
    shares: List[Dict[str, Any]] = Field(..., description="List of presented shares with x and y_hex")
    operator_id: str = Field(..., min_length=3, max_length=64)

class ThresholdReconstructResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    vault_id: str
    quorum_achieved: bool
    shares_provided_count: int
    threshold_required: int
    decrypted_content: Optional[str] = None
    reconstruction_time_ms: float
    tamper_detected: bool
    multisig_audit_receipt: Optional[Dict[str, Any]] = None
    message: str

class VaultTamperEventDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_id: str
    vault_id: str
    tamper_type: str
    detected_at: str
    ip_address: str
    zeroization_successful: bool

class ShamirKeySplitRequest(BaseModel):
    exam_code: str = Field(..., min_length=3, max_length=64)
    subject: str = Field(..., min_length=2, max_length=128)
    raw_content: str = Field(..., min_length=10)
    threshold_k: int = Field(3, ge=2, le=10)
    total_shares_n: int = Field(5, ge=2, le=10)

class ShamirKeySplitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    vault_id: str
    threshold_k: int
    total_shares_n: int
    shares: List[ShamirShareDTO]
    custodians: List[ExamCustodianDTO]
