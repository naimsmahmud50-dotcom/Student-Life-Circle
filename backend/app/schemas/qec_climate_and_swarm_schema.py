"""
Pydantic Schemas for Phase 43
==============================
Quantum Error Correction, Atmospheric Climate Modeling & Micro-Robotics Swarm.
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
# QUANTUM ERROR CORRECTION SCHEMAS
# =========================================================================

class SurfaceLatticeInitRequest(BaseModel):
    distance: int = Field(default=3, ge=3, le=15, description="Odd code distance d")


class PauliErrorInjectionRequest(BaseModel):
    code_distance: int = Field(default=3, ge=3, le=15, description="Code distance")
    error_rate_p: float = Field(default=0.005, ge=0.0, le=0.5, description="Physical error rate")
    explicit_errors: Optional[List[Dict[str, Any]]] = Field(default=None, description="Optional manual errors")


class QecDecodingRequest(BaseModel):
    code_distance: int = Field(default=3, ge=3, le=15, description="Code distance d")
    physical_error_p: float = Field(default=0.005, ge=1e-6, le=0.5, description="Physical error rate")
    syndrome_defects_count: int = Field(default=1, ge=0, description="Measured stabilizer syndrome defects")


# =========================================================================
# ATMOSPHERIC CLIMATE SCHEMAS
# =========================================================================

class RadiativeForcingRequest(BaseModel):
    co2_concentration_ppm: float = Field(..., ge=1.0, description="Atmospheric CO2 in ppm")
    ch4_concentration_ppb: float = Field(default=1900.0, ge=1.0, description="Methane in ppb")
    n2o_concentration_ppb: float = Field(default=335.0, ge=1.0, description="Nitrous oxide in ppb")
    baseline_co2_ppm: float = Field(default=280.0, ge=1.0, description="Pre-industrial baseline in ppm")


class PlanetaryEnergyBalanceRequest(BaseModel):
    planetary_albedo: float = Field(default=0.30, ge=0.0, le=0.99, description="Planetary reflectance")
    effective_emissivity: float = Field(default=0.612, ge=0.1, le=1.0, description="Effective emissivity")
    solar_irradiance: float = Field(default=1361.0, ge=100.0, description="Solar constant W/m^2")
    greenhouse_forcing_delta_f: float = Field(default=0.0, description="Radiative forcing perturbation W/m^2")


# =========================================================================
# MICRO-ROBOTICS SWARM SCHEMAS
# =========================================================================

class SwarmSimulationStepRequest(BaseModel):
    agents: Optional[List[Dict[str, Any]]] = Field(default=None, description="Agent state list")
    target_waypoint: Optional[List[float]] = Field(default=None, description="Goal coordinate [x, y]")
    obstacles: Optional[List[List[float]]] = Field(default=None, description="Obstacle centers [[x, y], ...]")
    dt_seconds: float = Field(default=0.1, ge=0.01, le=1.0, description="Time step in seconds")
    weight_separation: float = Field(default=1.5, ge=0.0, description="Separation force weight")
    weight_alignment: float = Field(default=1.0, ge=0.0, description="Alignment force weight")
    weight_cohesion: float = Field(default=1.0, ge=0.0, description="Cohesion force weight")
