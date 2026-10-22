"""
Pydantic v2 schemas and DTOs for Phase 35:
- National STEM Olympiad Arena & Mathematical Proof Evaluator
- Interactive Semiconductor Physics & Quantum Mechanics Sandbox
- Autonomous Intellectual Property & University Patent Filing Registry
Dual-resilience BaseDTO fallbacks included for robust serialization.
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
# 1. National STEM Olympiad Arena Schemas
# -----------------------------------------------------------------------------

class OlympiadProblemResponse(BaseModel):
    problem_id: str
    competition: str  # BDMO, BDPHO, BDIO, BDBO
    year: int
    division: str  # PRIMARY, JUNIOR, SECONDARY, HIGHER_SECONDARY
    title: str
    statement: str
    difficulty_elo: int
    max_score: float
    sample_hint: str

class OlympiadSubmissionRequest(BaseModel):
    problem_id: str
    student_id: str
    student_name: str
    solution_text: str
    numerical_answer: Optional[float] = None
    time_spent_seconds: int = 120

class OlympiadSubmissionResponse(BaseModel):
    submission_id: str
    problem_id: str
    student_id: str
    is_correct: bool
    fractional_score: float
    max_score: float
    time_penalty: float
    net_score: float
    feedback: str
    official_solution_breakdown: str
    submitted_at: str

class OlympiadLeaderboardEntry(BaseModel):
    rank: int
    student_id: str
    student_name: str
    division: str
    total_score: float
    solved_count: int
    percentile: float

class OlympiadLeaderboardResponse(BaseModel):
    competition: str
    entries: List[OlympiadLeaderboardEntry]
    total_participants: int


# -----------------------------------------------------------------------------
# 2. Semiconductor & Quantum Sandbox Schemas
# -----------------------------------------------------------------------------

class PnJunctionSimRequest(BaseModel):
    semiconductor_material: str = "SILICON"  # SILICON, GERMANIUM, GALLIUM_ARSENIDE
    acceptor_doping_na_cm3: float = 1e16
    donor_doping_nd_cm3: float = 1e16
    reverse_bias_voltage_v: float = 0.0
    temperature_kelvin: float = 300.0

class PnJunctionSimResponse(BaseModel):
    material: str
    built_in_potential_v: float
    depletion_width_um: float
    x_p_depletion_um: float
    x_n_depletion_um: float
    peak_electric_field_kv_cm: float
    junction_capacitance_pf_cm2: float
    bandgap_ev: float
    spatial_electric_field_profile: List[Dict[str, float]]

class QuantumWellSimRequest(BaseModel):
    well_width_nm: float = 5.0
    particle_mass_ratio: float = 0.067  # e.g., GaAs conduction electron m*/m0
    state_levels: int = 3

class QuantumWellEnergyLevel(BaseModel):
    level_n: int
    energy_ev: float
    wavelength_nm: float

class QuantumWellSimResponse(BaseModel):
    well_width_nm: float
    effective_mass_kg: float
    energy_levels: List[QuantumWellEnergyLevel]
    wavefunction_samples: List[Dict[str, float]]


# -----------------------------------------------------------------------------
# 3. University Patent Filing & Prior Art Registry Schemas
# -----------------------------------------------------------------------------

class PatentDisclosureFileRequest(BaseModel):
    title: str = "Edge-Optimized Spiking Neural Processor for Bangla Acoustic Feature Extraction"
    abstract: str = "An ultra-low power asynchronous neuromorphic CMOS core computing continuous wavelet speech features at sub-millivolt supply levels."
    inventors: List[str] = ["Tanvir Ahmed", "Prof. Dr. Mohammad Kaykobad"]
    institution: str = "BUET"
    ipc_classification: str = "G06F"
    claims: List[str] = [
        "A neuromorphic CMOS circuit architecture comprising asynchronous event-driven synaptic arrays.",
        "The circuit of claim 1 wherein each wavelet filter bank operates in the subthreshold analog domain."
    ]
    technical_field: str = "AI and Semiconductor Electronics"

class PatentDisclosureResponse(BaseModel):
    patent_id: str
    title: str
    abstract: str
    inventors: List[str]
    institution: str
    ipc_classification: str
    claims: List[str]
    novelty_score: float
    cryptographic_disclosure_seal: str
    filed_at: str

class PatentPriorArtSearchRequest(BaseModel):
    search_query: str
    min_novelty_threshold: float = 0.3

class PatentPriorArtMatch(BaseModel):
    patent_id: str
    title: str
    institution: str
    similarity_index: float
    overlapping_claims: List[str]

class PatentPriorArtSearchResponse(BaseModel):
    search_query: str
    matches: List[PatentPriorArtMatch]
    is_patentable_novel: bool
    average_novelty_score: float
