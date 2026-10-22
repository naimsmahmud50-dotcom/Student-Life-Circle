"""
Pydantic v2 schemas and DTOs for Phase 38:
- Post-Quantum Cryptography & Lattice Key Encapsulation (ML-KEM / Kyber-768)
- Smart Renewable Energy Micro-Grid Dispatch Simulator (Solar PV + LiFePO4 BESS)
- Decentralized Carbon Offset Registry & Verifiable Green Certificate Ledger
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
# 1. Post-Quantum Cryptography (ML-KEM / Kyber) Schemas
# -----------------------------------------------------------------------------

class PqcKeyGenRequest(BaseModel):
    algorithm: str = Field(default="ML-KEM-768", description="PQC parameterization: ML-KEM-512, ML-KEM-768, ML-KEM-1024")
    seed: Optional[str] = Field(default=None, description="Optional deterministic seed for reproducibility")

class PqcKeyGenResponse(BaseModel):
    algorithm: str
    security_level_nist: int
    classical_security_bits: int
    quantum_security_bits: int
    public_key_hex: str
    secret_key_hex: str
    public_key_fingerprint: str
    dimension_k: int
    modulus_q: int
    degree_n: int

class PqcEncapsulateRequest(BaseModel):
    public_key_hex: str = Field(..., description="Recipient's ML-KEM public key in hex")
    algorithm: str = Field(default="ML-KEM-768", description="Target PQC algorithm")
    message_seed: Optional[str] = Field(default=None, description="Optional random seed for encapsulation")

class PqcEncapsulateResponse(BaseModel):
    algorithm: str
    ciphertext_hex: str
    ciphertext_fingerprint: str
    shared_secret_hex: str
    shared_secret_bits: int
    status: str

class PqcDecapsulateRequest(BaseModel):
    secret_key_hex: str = Field(..., description="Recipient's ML-KEM private key in hex")
    ciphertext_hex: str = Field(..., description="Ciphertext to decapsulate in hex")
    public_key_hex: Optional[str] = Field(default=None, description="Optional public key for Fujisaki-Okamoto re-encryption check")
    algorithm: str = Field(default="ML-KEM-768", description="Target PQC algorithm")

class PqcDecapsulateResponse(BaseModel):
    algorithm: str
    recovered_shared_secret_hex: str
    is_valid: bool
    constant_time_verified: bool
    status: str

class PqcQuantumSecurityAssessmentRequest(BaseModel):
    algorithm: str = Field(default="ML-KEM-768", description="Cryptographic primitive to benchmark")

class PqcQuantumSecurityAssessmentResponse(BaseModel):
    algorithm: str
    category: str
    shor_vulnerable: bool
    grover_vulnerable: bool
    classical_security_bits: int
    quantum_security_bits: int
    lattice_type: str
    nist_standard: str
    recommendation: str


# -----------------------------------------------------------------------------
# 2. Smart Grid Renewable Dispatch Schemas
# -----------------------------------------------------------------------------

class SolarPvCalcRequest(BaseModel):
    array_area_m2: float = Field(default=250.0, description="Solar panel total aperture area in square meters")
    efficiency: float = Field(default=0.21, description="Solar panel efficiency (e.g. 0.21 for 21% mono-PERC)")
    irradiance_w_per_m2: float = Field(default=850.0, description="Solar surface irradiance in W/m^2")
    ambient_temp_c: float = Field(default=32.0, description="Ambient air temperature in Celsius")
    temp_coefficient: float = Field(default=0.0038, description="Power loss per deg C above 25C (default 0.38%/C)")
    system_performance_ratio: float = Field(default=0.82, description="Inverter and wiring performance ratio (PR)")

class SolarPvCalcResponse(BaseModel):
    cell_temperature_c: float
    dc_power_kw: float
    ac_power_kw: float
    thermal_derating_pct: float
    hourly_energy_kwh: float

class MicroGridDispatchRequest(BaseModel):
    solar_area_m2: float = Field(default=300.0, description="Rooftop solar collector area in m^2")
    solar_efficiency: float = Field(default=0.20, description="Solar PV module efficiency")
    battery_capacity_kwh: float = Field(default=120.0, description="LiFePO4 battery capacity in kWh")
    battery_initial_soc: float = Field(default=0.50, description="Initial State of Charge (0.0 to 1.0)")
    battery_max_charge_kw: float = Field(default=40.0, description="Maximum battery charging power in kW")
    battery_max_discharge_kw: float = Field(default=50.0, description="Maximum battery discharging power in kW")
    battery_efficiency_roundtrip: float = Field(default=0.90, description="Round-trip efficiency")
    grid_tariff_peak_bdt_per_kwh: float = Field(default=13.5, description="Peak electricity grid tariff in BDT")
    grid_tariff_offpeak_bdt_per_kwh: float = Field(default=8.2, description="Off-peak electricity tariff in BDT")
    custom_hourly_load_kw: Optional[List[float]] = Field(default=None, description="Optional 24-hour load curve (kW)")
    custom_hourly_irradiance: Optional[List[float]] = Field(default=None, description="Optional 24-hour irradiance (W/m^2)")

class HourlyDispatchStep(BaseModel):
    hour: int
    load_kw: float
    solar_generation_kw: float
    battery_power_kw: float
    battery_soc_pct: float
    grid_import_kw: float
    grid_export_kw: float
    hourly_cost_bdt: float

class MicroGridDispatchResponse(BaseModel):
    total_load_kwh: float
    total_solar_generated_kwh: float
    total_battery_discharged_kwh: float
    total_battery_charged_kwh: float
    total_grid_imported_kwh: float
    total_grid_exported_kwh: float
    final_battery_soc_pct: float
    peak_demand_unshaved_kw: float
    peak_demand_shaved_kw: float
    peak_shaving_reduction_pct: float
    renewable_fraction_pct: float
    daily_cost_with_microgrid_bdt: float
    daily_baseline_cost_no_microgrid_bdt: float
    daily_savings_bdt: float
    hourly_dispatch: List[Dict[str, Any]]


# -----------------------------------------------------------------------------
# 3. Decentralized Carbon Offset Registry Schemas
# -----------------------------------------------------------------------------

class CarbonOffsetMintRequest(BaseModel):
    student_id: str = Field(..., description="Student or team unique identifier")
    project_name: str = Field(..., description="Clean energy or student campus innovation project name")
    renewable_energy_kwh: float = Field(..., description="Clean renewable energy generated in kWh")
    grid_emissions_factor: float = Field(default=0.635, description="Grid carbon intensity factor (kg CO2e per kWh)")
    project_category: str = Field(default="SOLAR_MICROGRID", description="Project category (SOLAR_MICROGRID, BIOENERGY, RECYCLING)")
    verification_notes: Optional[str] = Field(default="Verified via Campus Automated Microgrid Inverter API")

class CarbonOffsetCertificateResponse(BaseModel):
    certificate_id: str
    owner_id: str
    project_name: str
    project_category: str
    renewable_energy_kwh: float
    tco2e_avoided: float
    emissions_factor_used: float
    status: str
    minted_at: str
    certificate_hash: str
    previous_block_hash: str
    verification_seal: str
    is_retired: bool

class CarbonOffsetRetireRequest(BaseModel):
    certificate_id: str = Field(..., description="Certificate ID to permanently retire")
    student_id: str = Field(..., description="Authorized owner student ID")
    beneficiary_name: str = Field(..., description="Entity or event claiming the carbon offset")
    retirement_reason: str = Field(..., description="Specific purpose for offset retirement")

class CarbonOffsetRetireResponse(BaseModel):
    certificate_id: str
    owner_id: str
    tco2e_retired: float
    beneficiary_name: str
    retirement_reason: str
    retired_at: str
    retirement_receipt_hash: str
    status: str
    success: bool
