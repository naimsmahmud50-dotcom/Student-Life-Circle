"""
Pydantic v2 schemas and DTOs for Phase 36:
- Orbital Aerospace Telemetry & Satellite Mechanics Sandbox
- Global Research Grant & Post-Doctoral Fellowship Clearinghouse
- Multi-Agent Swarm Peer Tutoring Grid
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
        return default


# -----------------------------------------------------------------------------
# 1. Orbital Aerospace Telemetry & Satellite Schemas
# -----------------------------------------------------------------------------

class SatelliteOrbitRequest(BaseModel):
    satellite_name: str = "Bangabandhu-Satellite-1"
    perigee_altitude_km: float = Field(default=35786.0, description="Perigee altitude above Earth surface in km")
    apogee_altitude_km: float = Field(default=35786.0, description="Apogee altitude above Earth surface in km")
    inclination_deg: float = Field(default=0.0, description="Orbital inclination in degrees")

class SatelliteOrbitResponse(BaseModel):
    satellite_name: str
    orbit_type: str  # LEO, MEO, GEO, HEO
    semi_major_axis_km: float
    eccentricity: float
    period_minutes: float
    mean_orbital_velocity_kms: float
    perigee_velocity_kms: float
    apogee_velocity_kms: float
    is_geostationary: bool
    notes: str

class GroundStationPassRequest(BaseModel):
    satellite_name: str = "BRAC-Onnesha-CubeSat"
    station_name: str = "Dhaka SPARRSO Ground Station"
    station_lat: float = 23.7771
    station_lon: float = 90.3807
    orbit_altitude_km: float = 400.0
    carrier_frequency_mhz: float = 437.5

class GroundStationPassResponse(BaseModel):
    satellite_name: str
    station_name: str
    station_coordinates: str
    next_pass_utc: str
    max_elevation_deg: float
    duration_seconds: int
    max_doppler_shift_khz: float
    pass_quality: str  # EXCELLENT, GOOD, MARGINAL

class RfLinkBudgetRequest(BaseModel):
    carrier_frequency_mhz: float = 437.5
    tx_power_watts: float = 2.0
    tx_antenna_gain_dbi: float = 2.15
    distance_km: float = 650.0
    rx_antenna_gain_dbi: float = 14.5
    rx_noise_temp_k: float = 150.0
    data_rate_kbps: float = 9.6

class RfLinkBudgetResponse(BaseModel):
    fspl_db: float
    eirp_dbw: float
    rx_power_dbm: float
    eb_n0_db: float
    required_eb_n0_db: float
    link_margin_db: float
    link_status: str  # CLOSED, MARGINAL, BROKEN


# -----------------------------------------------------------------------------
# 2. Global Research Grant & Fellowship Schemas
# -----------------------------------------------------------------------------

class FellowshipSearchQuery(BaseModel):
    degree_level: Optional[str] = None  # MASTERS, PHD, POSTDOC
    field_of_study: Optional[str] = None  # STEM, CS_AI, PUBLIC_HEALTH, ECONOMICS
    destination_country: Optional[str] = None

class FellowshipResponse(BaseModel):
    fellowship_id: str
    title: str
    sponsor_agency: str
    host_countries: List[str]
    degree_levels: List[str]
    funding_type: str  # FULL_RIDE, PARTIAL_TUITION, RESEARCH_STIPEND
    monthly_stipend_approx_bdt: float
    annual_allowance_usd: float
    deadline: str
    eligibility_summary: str
    official_portal_url: str

class SopEvaluationRequest(BaseModel):
    target_fellowship_id: str = "FULBRIGHT-FOREIGN-STUDENT-2025"
    field_of_study: str = "Electrical Engineering & Nanotechnology"
    sop_text: str

class SopEvaluationResponse(BaseModel):
    target_fellowship: str
    word_count: int
    lexical_density_pct: float
    academic_rigor_score: float  # 0 to 100
    overall_readiness_tier: str  # HIGHLY_COMPETITIVE, COMPETITIVE, NEEDS_REVISION
    strengths: List[str]
    weaknesses: List[str]
    actionable_recommendations: List[str]

class GrantBudgetCalculationRequest(BaseModel):
    direct_research_costs_usd: float = 12000.0
    equipment_stipend_usd: float = 5000.0
    travel_conference_usd: float = 3000.0
    overhead_rate_pct: float = 15.0

class GrantBudgetCalculationResponse(BaseModel):
    direct_costs_usd: float
    overhead_usd: float
    total_budget_usd: float
    total_budget_bdt: float
    effective_exchange_rate_bdt: float
    breakdown_usd: Dict[str, float]


# -----------------------------------------------------------------------------
# 3. Multi-Agent Swarm Peer Tutoring Grid Schemas
# -----------------------------------------------------------------------------

class SwarmAgentProfile(BaseModel):
    agent_id: str
    agent_name: str
    persona_title: str
    intellectual_specialty: str
    epistemic_stance: str

class SwarmStudyPodRequest(BaseModel):
    topic: str
    student_query: str
    academic_level: str = "UNDERGRADUATE"  # HIGHER_SECONDARY, UNDERGRADUATE, GRADUATE

class SwarmAgentContribution(BaseModel):
    agent_id: str
    agent_name: str
    persona_title: str
    argument: str
    key_formula_or_analogy: str
    confidence_score: float

class SwarmStudyPodResponse(BaseModel):
    session_id: str
    topic: str
    academic_level: str
    agent_contributions: List[SwarmAgentContribution]
    dialectical_consensus: str
    core_takeaways: List[str]
    recommended_active_recall_challenge: str
