"""
Pydantic Schemas for Phase 42
==============================
Digital Twin Simulation, Computational Fluid Dynamics & DAO Governance Protocol.
Dual-resilience with BaseDTO fallback support.
"""

from typing import Any, Dict, List, Optional
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


# =========================================================================
# DIGITAL TWIN SCHEMAS
# =========================================================================

class TwinStateSimulationRequest(BaseModel):
    sensors: Optional[Dict[str, float]] = Field(default=None, description="Custom sensor mapping")
    noise_sigma: float = Field(default=0.05, ge=0.0, le=1.0, description="Noise standard deviation")


class MahalanobisAnomalyRequest(BaseModel):
    observation: List[float] = Field(..., description="Current sensor vector")
    mean_vector: List[float] = Field(..., description="Historical mean vector")
    covariance_matrix: List[List[float]] = Field(..., description="Covariance matrix NxN")


class SensorDriftCalibrationRequest(BaseModel):
    raw_value: float = Field(..., description="Raw sensor value")
    drift_rate_per_hour: float = Field(..., description="Drift rate per hour")
    elapsed_hours: float = Field(..., ge=0.0, description="Elapsed hours since calibration")
    reference_value: Optional[float] = Field(default=None, description="Known ground truth reference")


class MonteCarloReliabilityRequest(BaseModel):
    component_class: str = Field(default="default", description="Component class key")
    mission_hours: float = Field(default=1000.0, gt=0.0, description="Mission duration in hours")
    simulations: int = Field(default=1000, ge=10, le=10000, description="Monte Carlo sample count")
    seed: Optional[int] = Field(default=None, description="Random seed")


# =========================================================================
# COMPUTATIONAL FLUID DYNAMICS (CFD) SCHEMAS
# =========================================================================

class ReynoldsRegimeRequest(BaseModel):
    velocity: float = Field(..., ge=0.0, description="Flow velocity (m/s)")
    characteristic_length: float = Field(..., gt=0.0, description="Pipe diameter or chord length (m)")
    fluid: str = Field(default="air_20c", description="Fluid type name")
    custom_density: Optional[float] = Field(default=None, gt=0.0, description="Custom density kg/m^3")
    custom_viscosity: Optional[float] = Field(default=None, gt=0.0, description="Custom dynamic viscosity Pa.s")


class BernoulliFlowRequest(BaseModel):
    p1_pascal: float = Field(..., ge=0.0, description="Upstream static pressure (Pa)")
    v1_m_s: float = Field(..., ge=0.0, description="Upstream velocity (m/s)")
    z1_meters: float = Field(default=0.0, description="Upstream elevation (m)")
    v2_m_s: float = Field(..., ge=0.0, description="Downstream velocity (m/s)")
    z2_meters: float = Field(default=0.0, description="Downstream elevation (m)")
    fluid: str = Field(default="water_20c", description="Fluid catalog key")


class AerodynamicCoefficientsRequest(BaseModel):
    drag_force_newtons: float = Field(..., ge=0.0, description="Measured drag force (N)")
    lift_force_newtons: float = Field(..., description="Measured lift force (N)")
    velocity_m_s: float = Field(..., gt=0.0, description="Freestream velocity (m/s)")
    frontal_area_m2: float = Field(..., gt=0.0, description="Frontal or wing reference area (m^2)")
    fluid: str = Field(default="air_20c", description="Fluid catalog key")


class ChannelProfileRequest(BaseModel):
    channel_height_m: float = Field(default=0.05, gt=0.0, description="Channel height (m)")
    centerline_velocity_m_s: float = Field(default=1.5, gt=0.0, description="Max centerline velocity (m/s)")
    grid_points: int = Field(default=11, ge=5, le=51, description="Number of discretization points")


# =========================================================================
# DAO GOVERNANCE SCHEMAS
# =========================================================================

class QuadraticVotingCalcRequest(BaseModel):
    tokens: float = Field(..., ge=0.0, description="Token budget or tokens to stake")
    votes: Optional[float] = Field(default=None, ge=0.0, description="Desired vote count")


class ProposalCreateRequest(BaseModel):
    proposal_id: str = Field(..., description="Unique proposal hash or identifier")
    title: str = Field(..., min_length=3, max_length=150, description="Proposal headline")
    description: str = Field(..., description="Proposal details and implementation specs")
    proposer_address: str = Field(..., description="Proposer wallet or student identity")
    total_supply: float = Field(default=1000000.0, gt=0.0, description="Total governance tokens in circulation")
    quorum_pct: float = Field(default=20.0, ge=1.0, le=100.0, description="Quorum threshold percentage")
    approval_threshold_pct: float = Field(default=66.0, ge=50.0, le=100.0, description="Supermajority threshold")
    voting_period_hours: float = Field(default=72.0, gt=0.0, description="Voting window in hours")
    timelock_delay_hours: float = Field(default=24.0, ge=0.0, description="Execution timelock delay")


class QuadraticVoteCastRequest(BaseModel):
    proposal_id: str = Field(..., description="Target proposal identifier")
    voter_address: str = Field(..., description="Voter wallet or student address")
    tokens_allocated: float = Field(..., gt=0.0, description="Tokens to stake under quadratic curve")
    support: str = Field(default="FOR", description="FOR, AGAINST, or ABSTAIN")
