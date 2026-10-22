"""
Pydantic v2 schemas and DTOs for Phase 39:
- Autonomous Cyber Range & Zero-Trust Defense Sandbox
- High-Performance Computing (HPC) Parallel Job Scheduler (Slurm + Amdahl Speedup)
- University Venture Capital Angel Syndicate & SAFE Cap Table Dilution Simulator
Dual-resilience BaseDTO fallbacks included for robust cross-environment serialization.
"""

from typing import List, Optional, Dict, Any

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self, *args, **kwargs):
            return self.__dict__
        def model_dump(self, *args, **kwargs):
            return self.__dict__

    def Field(default=None, **kwargs):
        return default if default is not ... else None


# -----------------------------------------------------------------------------
# 1. Zero-Trust Cyber Range & Defense Sandbox Schemas
# -----------------------------------------------------------------------------

class ZeroTrustEvaluationRequest(BaseModel):
    student_id: str = Field(..., description="Student or session subject identifier")
    device_fingerprint: str = Field(..., description="Client device posture signature")
    ip_address: str = Field(default="127.0.0.1", description="Requester IP address")
    mfa_authenticated: bool = Field(default=True, description="Hardware MFA token status")
    geo_velocity_kmh: float = Field(default=0.0, description="Calculated geographic displacement velocity in km/h")
    payload_sample: Optional[str] = Field(default=None, description="Request payload sample to audit for injection")

class ZeroTrustEvaluationResponse(BaseModel):
    student_id: str
    trust_score: float
    access_granted: bool
    decision: str
    threat_level: str
    anomaly_flags: List[str]
    risk_factors: Dict[str, float]
    verification_timestamp: str

class ThreatDetectionRequest(BaseModel):
    payload_text: str = Field(..., description="Payload or request parameter string to inspect")
    context_type: str = Field(default="QUERY", description="Context: QUERY, HEADER, BODY, TOKEN")

class ThreatDetectionResponse(BaseModel):
    is_malicious: bool
    attack_types: List[str]
    sanitized_output: str
    risk_score: float
    detection_signature: str


# -----------------------------------------------------------------------------
# 2. HPC Parallel Job Scheduler & Amdahl Speedup Schemas
# -----------------------------------------------------------------------------

class HpcJobSubmitRequest(BaseModel):
    job_name: str = Field(..., description="Research compute job name (e.g. Distributed-LLM-FineTune)")
    student_id: str = Field(..., description="Authorized university researcher or student ID")
    gpu_type: str = Field(default="NVIDIA_H100", description="Accelerator: NVIDIA_H100, NVIDIA_A100, NVIDIA_L40S")
    gpu_count: int = Field(default=4, description="Number of GPUs requested")
    vram_gb_requested: float = Field(default=320.0, description="Total VRAM in GB requested")
    walltime_minutes: int = Field(default=120, description="Max walltime in minutes")
    parallel_fraction: float = Field(default=0.92, description="Amdahl parallelizable fraction (0.0 to 1.0)")

class HpcJobSubmitResponse(BaseModel):
    job_id: str
    job_name: str
    student_id: str
    priority_score: float
    queue_state: str
    allocated_nodes: int
    tflops_allocated: float
    estimated_wait_seconds: int
    allocated_vram_gb: float

class AmdahlSpeedupCalcRequest(BaseModel):
    parallel_fraction: float = Field(default=0.95, description="Fraction of execution time that is parallelizable (p)")
    processor_counts: Optional[List[int]] = Field(
        default=[1, 2, 4, 8, 16, 32, 64, 128],
        description="Array of processor/GPU counts to simulate"
    )

class AmdahlSpeedupCalcResponse(BaseModel):
    parallel_fraction: float
    serial_fraction: float
    theoretical_max_speedup: float
    speedup_curve: List[Dict[str, Any]]
    gustafson_scaled_speedup: List[Dict[str, Any]]
    efficiency_curve: List[Dict[str, Any]]


# -----------------------------------------------------------------------------
# 3. University Venture Capital & Angel Syndicate Schemas
# -----------------------------------------------------------------------------

class SafeDilutionCalcRequest(BaseModel):
    startup_name: str = Field(default="Agrojatra EdTech", description="Student venture name")
    safe_type: str = Field(default="POST_MONEY_SAFE", description="POST_MONEY_SAFE, PRE_MONEY_SAFE, CONVERTIBLE_NOTE")
    investment_amount_usd: float = Field(default=150000.0, description="Investment amount in USD")
    valuation_cap_usd: float = Field(default=3000000.0, description="SAFE Valuation Cap in USD")
    discount_pct: float = Field(default=20.0, description="Discount rate in percentage (e.g. 20%)")
    existing_founder_shares: int = Field(default=8000000, description="Current outstanding founder shares")

class SafeDilutionCalcResponse(BaseModel):
    startup_name: str
    safe_type: str
    investment_amount_usd: float
    valuation_cap_usd: float
    post_money_valuation_usd: float
    investor_equity_pct: float
    founder_equity_pct: float
    effective_share_price_usd: float
    new_shares_issued: int
    total_post_shares: int
    dilution_summary: str
    cap_table: List[Dict[str, Any]]

class AngelCommitmentRequest(BaseModel):
    startup_name: str = Field(..., description="Student venture name")
    student_founder_id: str = Field(..., description="Student founder ID")
    target_raise_usd: float = Field(default=250000.0, description="Target seed round in USD")
    investor_name: str = Field(default="Dhaka Tech Angels", description="Angel syndicate or fund name")
    syndicate_tier: str = Field(default="ACCREDITED_ANGEL", description="TIER: LEAD_VC, INSTITUTIONAL, ACCREDITED_ANGEL")
    commitment_amount_usd: float = Field(..., description="Committed investment in USD")

class AngelCommitmentResponse(BaseModel):
    commitment_id: str
    startup_name: str
    founder_id: str
    total_committed_usd: float
    target_raise_usd: float
    funding_progress_pct: float
    investor_count: int
    escrow_lock_seal: str
    status: str
