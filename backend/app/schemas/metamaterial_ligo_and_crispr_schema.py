"""
Pydantic Schemas for Phase 45
==============================
Nanophotonics Metamaterial, Gravitational Wave Interferometry & CRISPR Gene Lab.
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
# NANOPHOTONICS METAMATERIAL SCHEMAS
# =========================================================================

class OpticalDispersionRequest(BaseModel):
    frequency_thz: float = Field(default=105.0, gt=0.0, description="Optical probe frequency (THz)")
    plasma_frequency_thz: float = Field(default=120.0, gt=0.0, description="Drude plasma frequency omega_p (THz)")
    resonance_frequency_thz: float = Field(default=100.0, gt=0.0, description="Magnetic resonance frequency omega_0 (THz)")
    electron_damping_thz: float = Field(default=2.0, ge=0.0, description="Drude damping gamma_e (THz)")
    magnetic_damping_thz: float = Field(default=3.0, ge=0.0, description="Lorentz magnetic damping gamma_m (THz)")
    magnetic_oscillator_strength: float = Field(default=0.55, ge=0.0, le=1.0, description="Oscillator strength F")


class NegativeRefractionRequest(BaseModel):
    incident_angle_deg: float = Field(default=30.0, ge=0.0, le=89.0, description="Incident angle in degrees")
    n1_incident: float = Field(default=1.0, gt=0.0, description="Incident medium index (e.g. air=1.0)")
    n2_metamaterial: float = Field(default=-1.5, description="Metamaterial refractive index (negative)")
    slab_thickness_nm: float = Field(default=150.0, gt=0.0, description="Superlens slab thickness (nm)")
    wavelength_nm: float = Field(default=632.8, gt=0.0, description="Vacuum wavelength (nm)")


# =========================================================================
# GRAVITATIONAL WAVE INTERFEROMETRY SCHEMAS
# =========================================================================

class GravitationalChirpRequest(BaseModel):
    m1_solar_masses: float = Field(default=36.0, gt=0.0, description="Primary compact object mass (M_sun)")
    m2_solar_masses: float = Field(default=29.0, gt=0.0, description="Secondary compact object mass (M_sun)")
    luminosity_distance_mpc: float = Field(default=410.0, gt=0.0, description="Luminosity distance (Mpc)")
    initial_frequency_hz: float = Field(default=30.0, ge=10.0, le=1000.0, description="Starting detector frequency (Hz)")


class ChirpWaveformRequest(BaseModel):
    chirp_mass_msun: float = Field(default=28.1, gt=0.0, description="Chirp mass in solar masses")
    duration_seconds: float = Field(default=0.5, ge=0.1, le=2.0, description="Waveform duration window (s)")
    sampling_rate_hz: float = Field(default=2048.0, ge=512.0, le=4096.0, description="Sample rate (Hz)")


# =========================================================================
# SYNTHETIC BIOLOGY CRISPR-CAS9 SCHEMAS
# =========================================================================

class CrisprGrnaEvaluationRequest(BaseModel):
    sequence_23nt: str = Field(..., min_length=23, max_length=23, description="23-nucleotide DNA sequence (20nt protospacer + 3nt PAM)")


class CrisprOffTargetRequest(BaseModel):
    guide_20nt: str = Field(..., min_length=20, max_length=20, description="20nt guide protospacer sequence")
    potential_off_target_20nt: str = Field(..., min_length=20, max_length=20, description="20nt putative genomic off-target site")
