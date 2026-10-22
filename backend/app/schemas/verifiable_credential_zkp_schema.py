"""
Pydantic Schemas for Phase 58: W3C Verifiable Credential & ZKP Certificate Vault.
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


# --- Schemas for Verifiable Credential Engine ---
class IssueCredentialRequest(BaseModel):
    student_id: str = Field(..., description="Unique institutional student ID, e.g. DU-CSE-2022-0491")
    student_name: str = Field(..., description="Full legal name of the student")
    institution_did: str = Field(..., description="Decentralized Identifier of issuer, e.g. did:web:du.ac.bd")
    degree_title: str = Field(..., description="Title of academic degree or certification")
    cgpa: float = Field(..., description="Cumulative Grade Point Average (0.00 - 4.00)")
    graduation_year: int = Field(..., description="Year of graduation or conferral")
    honors_designation: Optional[str] = Field("First Class Honours", description="Academic distinction")


class VerifiableCredentialResponse(BaseModel):
    credential_id: str
    w3c_payload: Dict[str, Any]
    canonical_digest: str
    ed25519_signature: str
    status_list_index: int
    is_valid: bool
    svg_badge: str


class VerifyCredentialRequest(BaseModel):
    credential_payload: Dict[str, Any] = Field(..., description="W3C JSON-LD Credential object to verify")
    expected_issuer_did: Optional[str] = Field(None, description="Optional expected issuer DID filter")


class VerifyCredentialResponse(BaseModel):
    is_valid: bool
    issuer_verified: bool
    tamper_detected: bool
    revocation_status: str
    verification_report: str
    claimed_student_name: str
    claimed_degree: str


# --- Schemas for Zero-Knowledge Range Proof Service ---
class GenerateZkpProofRequest(BaseModel):
    credential_id: str = Field(..., description="Associated Verifiable Credential ID")
    actual_cgpa: float = Field(..., description="Actual CGPA to prove in zero-knowledge")
    threshold_cgpa: float = Field(..., description="Threshold to satisfy, e.g. 3.50")
    student_did: str = Field(..., description="Student DID / Public identity")


class ZkpRangeProofResponse(BaseModel):
    proof_id: str
    pedersen_commitment: str
    threshold_tested: float
    proof_valid: bool
    challenge_hash: str
    response_proof: str
    revealed_cgpa: Optional[float] = None  # None: raw score strictly hidden
    verifier_statement: str


# --- Schemas for Institutional Revocation Registry ---
class RevocationUpdateRequest(BaseModel):
    institution_did: str = Field(..., description="Issuer DID")
    status_list_index: int = Field(..., description="Bit index in the status list")
    is_revoked: bool = Field(..., description="True to revoke, False to reinstate")
    revocation_reason: Optional[str] = Field(None, description="Reason for suspension or revocation")
    dean_signature: str = Field(..., description="Academic Dean authorization signature")
    registrar_signature: str = Field(..., description="University Registrar authorization signature")


class RevocationCheckRequest(BaseModel):
    institution_did: str = Field(..., description="Issuer DID")
    status_list_index: int = Field(..., description="Bit index in the status list")


class RevocationCheckResponse(BaseModel):
    status_list_index: int
    is_revoked: bool
    revocation_reason: Optional[str]
    state_root_hash: str
    checked_at: str
