"""
========================================================================================
AGROJATRA / STUDENT LIFE CIRCLE - ADVANCED ENGINEERING & STEM RESEARCH LAB
MODULE: Schemas for Nuclear SMR, Astrodynamics & Topological Quantum Lab
FILE: backend/app/schemas/smr_astrodynamics_and_topological_schema.py
========================================================================================

TOPIC DESCRIPTION & ARCHITECTURAL OVERVIEW FOR NEW DEVELOPERS:
----------------------------------------------------------------------------------------
This module defines high-resilience Pydantic v2 data transfer objects (DTOs) for Phase 46:
1. Small Modular Reactor (SMR) point kinetics, Doppler feedback, and decay heat inputs.
2. Interplanetary Astrodynamics Lambert orbital transfer, flyby swing-by, and multi-stage rocket.
3. Topological Quantum Computing Kitaev nanowire and non-Abelian anyon braid sequences.

DUAL-RESILIENCE ARCHITECTURE:
Gracefully handles environments where Pydantic v2 is present or absent with a fallback BaseModel.
========================================================================================
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
# NUCLEAR SMR REACTOR SCHEMAS
# =========================================================================

class SmrTransientRequest(BaseModel):
    rated_thermal_power_mw: float = Field(default=200.0, gt=0.0, description="Rated core thermal power (MW)")
    initial_power_mw: float = Field(default=200.0, gt=0.0, description="Starting power (MW)")
    reactivity_insertion_pcm: float = Field(default=100.0, description="Step reactivity insertion in pcm (1 pcm = 1e-5 dk/k)")
    fuel_doppler_coeff_pcm_per_c: float = Field(default=-3.2, description="Doppler temperature coefficient alpha_f (pcm/C)")
    moderator_coeff_pcm_per_c: float = Field(default=-12.5, description="Moderator temperature coefficient alpha_m (pcm/C)")
    initial_fuel_temp_c: float = Field(default=650.0, gt=0.0, description="Initial fuel center temperature (C)")
    initial_mod_temp_c: float = Field(default=300.0, gt=0.0, description="Initial moderator/coolant temperature (C)")
    coolant_inlet_temp_c: float = Field(default=250.0, gt=0.0, description="Coolant inlet temperature (C)")
    transient_duration_s: float = Field(default=10.0, ge=1.0, le=120.0, description="Simulation duration in seconds")
    time_step_s: float = Field(default=0.05, ge=0.005, le=0.2, description="RK4 integration time step (s)")
    scram_enabled: bool = Field(default=False, description="Enable automatic control rod SCRAM trigger")


class DecayHeatRequest(BaseModel):
    rated_power_mw: float = Field(default=200.0, gt=0.0, description="Rated thermal power (MW)")
    time_after_scram_s: float = Field(default=10.0, ge=0.1, description="Cooling time after reactor shutdown (s)")
    operating_time_s: float = Field(default=1.0e7, ge=100.0, description="Operating history duration (s)")


# =========================================================================
# INTERPLANETARY ASTRODYNAMICS SCHEMAS
# =========================================================================

class LambertTransferRequest(BaseModel):
    departure_radius_au: float = Field(default=1.0, gt=0.0, description="Departure orbit radius in Astronomical Units (AU)")
    arrival_radius_au: float = Field(default=1.524, gt=0.0, description="Arrival orbit radius in Astronomical Units (AU)")
    transfer_angle_deg: float = Field(default=180.0, ge=1.0, le=359.0, description="True anomaly transfer angle in degrees")
    time_of_flight_days: float = Field(default=258.8, gt=1.0, description="Mission time of flight in Earth days")


class GravityAssistRequest(BaseModel):
    planet_name: str = Field(default="MARS", description="Flyby celestial body (e.g. 'MARS', 'JUPITER', 'EARTH')")
    v_infinity_in_km_s: float = Field(default=5.65, gt=0.0, description="Hyperbolic excess speed v_inf (km/s)")
    flyby_periapsis_altitude_km: float = Field(default=500.0, gt=50.0, description="Flyby periapsis altitude above planetary surface (km)")
    planet_heliocentric_speed_km_s: float = Field(default=24.1, gt=0.0, description="Orbital speed of planet around Sun (km/s)")


class MultiStageRocketRequest(BaseModel):
    payload_mass_kg: float = Field(default=1000.0, gt=0.0, description="Mission scientific payload mass (kg)")
    stages: Optional[List[Dict[str, float]]] = Field(default=None, description="Custom list of rocket stages [dry_mass_kg, propellant_mass_kg, isp_sec]")


# =========================================================================
# TOPOLOGICAL QUANTUM COMPUTING SCHEMAS
# =========================================================================

class KitaevWireRequest(BaseModel):
    num_sites: int = Field(default=40, ge=4, le=200, description="Number of lattice sites along the superconducting nanowire")
    hopping_amplitude_mev: float = Field(default=1.0, gt=0.0, description="Fermionic hopping parameter t (meV)")
    superconducting_gap_mev: float = Field(default=0.5, gt=0.0, description="p-wave pairing amplitude Delta (meV)")
    chemical_potential_mev: float = Field(default=0.4, description="Chemical potential mu (meV)")
    temperature_kelvin: float = Field(default=0.05, gt=0.0, le=10.0, description="Cryogenic temperature (K)")


class AnyonBraidRequest(BaseModel):
    braid_sequence: List[str] = Field(default=["sigma_1", "sigma_2"], description="Sequence of elementary anyon swap braid operations")
    initial_state: str = Field(default="|0>", description="Initial computational basis state ('|0>', '|1>', '|+>')")
