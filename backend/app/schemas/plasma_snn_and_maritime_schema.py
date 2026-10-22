"""
Pydantic Schemas for Phase 44
==============================
Fusion Plasma Tokamak, Neuromorphic SNN & Maritime COLREGs Navigation.
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
# FUSION PLASMA TOKAMAK SCHEMAS
# =========================================================================

class LawsonCriterionRequest(BaseModel):
    plasma_density_m3: float = Field(default=1.0e20, ge=1e18, description="Electron/ion density (m^-3)")
    energy_confinement_time_s: float = Field(default=3.5, gt=0.0, description="Energy confinement time tau_E (s)")
    plasma_temperature_kev: float = Field(default=15.0, gt=0.0, description="Core plasma temperature (keV)")
    external_heating_power_mw: float = Field(default=50.0, ge=0.0, description="NBI/ECRH external heating (MW)")


class TokamakMhdRequest(BaseModel):
    major_radius_r_m: float = Field(default=6.2, gt=0.0, description="Tokamak major radius R (m)")
    minor_radius_a_m: float = Field(default=2.0, gt=0.0, description="Tokamak minor radius a (m)")
    toroidal_field_bt_tesla: float = Field(default=5.3, gt=0.0, description="Toroidal magnetic field B_T (Tesla)")
    plasma_current_ip_ma: float = Field(default=15.0, gt=0.0, description="Toroidal plasma current I_P (Mega-Amperes)")
    plasma_density_m3: float = Field(default=1.0e20, ge=1e18, description="Plasma density (m^-3)")
    plasma_temperature_kev: float = Field(default=15.0, gt=0.0, description="Core temperature (keV)")


# =========================================================================
# NEUROMORPHIC SNN SCHEMAS
# =========================================================================

class LifNeuronSimulationRequest(BaseModel):
    current_injections_na: List[float] = Field(..., description="Array of input current values in nA per time step")
    dt_ms: float = Field(default=0.5, ge=0.01, le=2.0, description="Simulation step (ms)")
    v_rest_mv: float = Field(default=-70.0, description="Resting potential (mV)")
    v_thresh_mv: float = Field(default=-55.0, description="Spike threshold (mV)")
    v_reset_mv: float = Field(default=-75.0, description="Post-spike reset (mV)")
    tau_m_ms: float = Field(default=20.0, gt=0.0, description="Membrane time constant (ms)")
    r_m_mohm: float = Field(default=10.0, gt=0.0, description="Membrane resistance (MOhm)")
    refractory_period_ms: float = Field(default=2.0, ge=0.0, description="Refractory window (ms)")


class StdpPlasticityRequest(BaseModel):
    initial_weight: float = Field(default=0.5, ge=0.0, le=1.0, description="Initial synaptic weight w in [0, 1]")
    pre_spike_times_ms: List[float] = Field(..., description="Array of presynaptic spike arrival timestamps (ms)")
    post_spike_times_ms: List[float] = Field(..., description="Array of postsynaptic spike emission timestamps (ms)")
    a_plus: float = Field(default=0.010, ge=0.0, description="Max potentiation rate A_+")
    a_minus: float = Field(default=0.012, ge=0.0, description="Max depression rate A_-")
    tau_plus_ms: float = Field(default=20.0, gt=0.0, description="Potentiation time window (ms)")
    tau_minus_ms: float = Field(default=20.0, gt=0.0, description="Depression time window (ms)")


# =========================================================================
# MARITIME NAVIGATION (COLREGS) SCHEMAS
# =========================================================================

class CpaCollisionRequest(BaseModel):
    own_x_nm: float = Field(default=0.0, description="Own ship X coordinate in nautical miles")
    own_y_nm: float = Field(default=0.0, description="Own ship Y coordinate in nautical miles")
    own_speed_knots: float = Field(default=15.0, ge=0.0, description="Own ship speed in knots")
    own_course_deg: float = Field(default=0.0, ge=0.0, le=360.0, description="Own ship true course in degrees")
    target_x_nm: float = Field(..., description="Target ship X coordinate in nautical miles")
    target_y_nm: float = Field(..., description="Target ship Y coordinate in nautical miles")
    target_speed_knots: float = Field(..., ge=0.0, description="Target ship speed in knots")
    target_course_deg: float = Field(..., ge=0.0, le=360.0, description="Target ship true course in degrees")
