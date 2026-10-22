"""
Pydantic v2 schemas and DTOs for Phase 41:
- Brain-Computer Interface (BCI) & EEG Cognitive Telemetry
- Scientific Hypothesis Discovery & Rigorous Statistical Inference
- Supply Chain Operations Research & Logistics Optimization
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
# 1. BCI & EEG Cognitive Telemetry Schemas
# -----------------------------------------------------------------------------

class BciEegSamplesRequest(BaseModel):
    raw_samples: Optional[List[float]] = Field(default=None, description="Time-series voltage samples in microvolts (uV)")
    sampling_rate_hz: Optional[float] = Field(default=256.0, description="EEG sensor sampling rate in Hertz")
    channel: Optional[str] = Field(default="Cz", description="10-20 standard electrode location (Fp1, Fp2, Cz, Pz, O1, O2)")

class BciEegDecompositionResponse(BaseModel):
    channel: str
    sample_count: int
    sampling_rate_hz: float
    total_power_uV2: float
    band_powers_relative_pct: Dict[str, float]
    engagement_index: float
    fatigue_index: float
    focus_score: float
    fatigue_status: str
    recommendation: str


# -----------------------------------------------------------------------------
# 2. Scientific Hypothesis Discovery Schemas
# -----------------------------------------------------------------------------

class ContingencyHypothesisRequest(BaseModel):
    variable_a_name: str = Field(default="Interactive Simulation", description="Independent factor or treatment group")
    variable_b_name: str = Field(default="Concept Mastery", description="Dependent factor or outcome status")
    observed_matrix: Optional[List[List[int]]] = Field(default=None, description="2x2 contingency matrix [[a, b], [c, d]]")
    alpha: Optional[float] = Field(default=0.05, description="Significance rejection threshold (default 0.05)")
    bonferroni_hypotheses_count: Optional[int] = Field(default=1, description="Number of parallel hypotheses tested for family-wise error control")

class ContingencyHypothesisResponse(BaseModel):
    null_hypothesis_H0: str
    alternative_hypothesis_H1: str
    sample_size: int
    contingency_table: Dict[str, int]
    chi_square_stat: float
    degrees_of_freedom: int
    p_value: float
    fisher_exact_prob: float
    odds_ratio: float
    alpha_raw: float
    alpha_bonferroni_corrected: float
    bonferroni_hypotheses_count: int
    is_significant: bool
    verdict: str
    conclusion: str


# -----------------------------------------------------------------------------
# 3. Supply Chain Operations & Logistics Schemas
# -----------------------------------------------------------------------------

class EoqRopCalcRequest(BaseModel):
    annual_demand: float = Field(default=12000.0, description="Annual item demand units D")
    order_cost_usd: float = Field(default=50.0, description="Fixed order placement / setup cost S ($)")
    holding_cost_unit_year_usd: float = Field(default=2.5, description="Annual inventory carrying / holding cost per unit H ($)")
    lead_time_days: Optional[int] = Field(default=7, description="Replenishment lead time in days L")
    demand_std_dev_daily: Optional[float] = Field(default=5.0, description="Daily demand standard deviation sigma_d")
    service_level_pct: Optional[float] = Field(default=95.0, description="Target customer fill rate / service level % (90, 95, 99)")

class EoqRopCalcResponse(BaseModel):
    annual_demand_units: float
    order_cost_usd: float
    holding_cost_unit_year_usd: float
    optimal_order_quantity_eoq: int
    orders_per_year: float
    cycle_time_days: float
    annual_ordering_cost_usd: float
    annual_holding_cost_usd: float
    total_annual_inventory_cost_usd: float
    lead_time_days: int
    safety_stock_units: int
    reorder_point_rop_units: float
    service_level_pct: float
    z_score: float

class BullwhipEffectRequest(BaseModel):
    demand_orders: Optional[List[float]] = Field(default=None, description="End-customer retail demand series")
    retailer_orders: Optional[List[float]] = Field(default=None, description="Orders placed upstream to manufacturer")

class BullwhipEffectResponse(BaseModel):
    demand_variance: float
    order_variance: float
    bullwhip_ratio: float
    amplification_status: str
    recommendation: str

class ShortestRouteRequest(BaseModel):
    origin_hub: str = Field(default="Dhaka Central", description="Source distribution depot")
    destination_hub: str = Field(default="Chittagong Port", description="Destination center")

class ShortestRouteResponse(BaseModel):
    origin: str
    destination: str
    total_distance_km: int
    route_path: List[str]
    transit_hops: int
    status: str
