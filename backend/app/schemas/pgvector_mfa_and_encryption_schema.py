"""
================================================================================
MODULE: Supabase pgvector, MFA Passkey & Field Encryption Schemas
TOPIC: Pydantic Validation Models for Semantic Vector Search, WebAuthn & Crypto
FILE: backend/app/schemas/pgvector_mfa_and_encryption_schema.py
PURPOSE: Strict data validation contracts for Phase 48 API endpoints.
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


class VectorSimilaritySearchRequest(BaseModel):
    query_vector: List[float] = Field(..., description="Query vector embedding")
    corpus: List[Dict[str, Any]] = Field(..., description="Corpus documents with embedding and tenant_id")
    caller_tenant_id: str = Field(..., description="Tenant ID of calling user")
    caller_role: str = Field("authenticated", description="Role: authenticated, anon, or service_role")
    top_k: int = Field(3, description="Number of top matches to return")
    similarity_threshold: float = Field(0.70, description="Minimum cosine similarity")


class VectorSimilaritySearchResponse(BaseModel):
    total_candidates: int
    matched_count: int
    cross_tenant_leaks_prevented: int
    results: List[Dict[str, Any]]
    top_similarity: float


class VectorGroundingCheckRequest(BaseModel):
    ai_response_embedding: List[float] = Field(..., description="Embedding of generated AI answer")
    verified_syllabus_chunks: List[List[float]] = Field(..., description="Verified NCTB/university syllabus chunks")
    grounding_threshold: float = Field(0.82, description="Minimum similarity required for syllabus grounding")


class VectorGroundingCheckResponse(BaseModel):
    is_grounded: bool
    confidence_score: float
    threshold_required: float
    verdict: str
    recommendation: str


class TotpEnrollRequest(BaseModel):
    user_id: str
    issuer: str = "Agrojatra Platform"


class TotpEnrollResponse(BaseModel):
    factor_id: str
    factor_type: str
    status: str
    secret_hex: str
    otpauth_uri: str
    backup_recovery_codes_plaintext: List[str]
    backup_codes_hashed: List[str]
    current_time_step_code: str


class TotpVerifyRequest(BaseModel):
    secret_hex: str
    user_code: str
    drift_steps: int = 1


class TotpVerifyResponse(BaseModel):
    is_valid: bool
    current_aal: str
    reason: str
    drift_offset: Optional[int] = None


class PasskeyChallengeRequest(BaseModel):
    user_id: str
    user_email: str


class PasskeyChallengeResponse(BaseModel):
    challenge: str
    rp: Dict[str, str]
    user: Dict[str, str]
    pubKeyCredParams: List[Dict[str, Any]]
    timeout: int
    attestation: str
    userVerification: str


class PasskeyVerifyRequest(BaseModel):
    challenge: str
    client_origin: str
    client_rp_id: str
    credential_id: str
    signature: str


class PasskeyVerifyResponse(BaseModel):
    verified: bool
    aal: str
    credential_id: Optional[str] = None
    reason: str


class EnvelopeEncryptRequest(BaseModel):
    plaintext: str
    associated_data: Optional[str] = None


class EnvelopeEncryptResponse(BaseModel):
    ciphertext_hex: str
    data_nonce_hex: str
    encrypted_dek_hex: str
    dek_nonce_hex: str
    blind_index_hex: str
    cipher_algorithm: str
    associated_data: Optional[str] = None


class EnvelopeDecryptRequest(BaseModel):
    ciphertext_hex: str
    data_nonce_hex: str
    encrypted_dek_hex: str
    dek_nonce_hex: str
    associated_data: Optional[str] = None


class EnvelopeDecryptResponse(BaseModel):
    success: bool
    plaintext: Optional[str] = None
    cipher_algorithm: Optional[str] = None
    error: Optional[str] = None
