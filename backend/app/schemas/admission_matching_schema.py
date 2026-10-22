"""
DEVELOPER ARCHITECTURE NOTE - MODULE 69:
National Centralized Admission Matrix & Gale-Shapley Stable Matching Schemas
Provides high-integrity Pydantic v2 domain schemas and standard fallback DTOs for:
1. Multi-Institutional Seat & Quota Allocations (General, District, Freedom Fighter, Tribal, Special Needs).
2. Student Preference Ranking and Dynamic Candidate Portfolios.
3. Gale-Shapley Deferred Acceptance (DA) Algorithm Outputs and Envy-Free Attestations.
4. Autonomous Multi-Round Migration Cascade Simulations.
5. Probabilistic Admission Rank Heuristics across BUET, Medical, DU, and GST Clusters.
"""

from enum import Enum
from typing import List, Dict, Optional, Any

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self, *args, **kwargs):
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        def model_dump(self, *args, **kwargs):
            return self.dict(*args, **kwargs)

    def Field(default=None, **kwargs):
        return default


class QuotaCategoryEnum(str, Enum):
    GENERAL = "GENERAL"
    DISTRICT = "DISTRICT"
    FREEDOM_FIGHTER = "FREEDOM_FIGHTER"
    TRIBAL_ETHNIC = "TRIBAL_ETHNIC"
    SPECIAL_NEEDS = "SPECIAL_NEEDS"


class ProgramSeatCapacityDTO(BaseModel):
    program_id: str
    institution_name: str
    program_name: str
    total_seats: int
    quota_distribution: Dict[str, int]
    historical_cutoff_rank: int


class CandidatePreferenceDTO(BaseModel):
    candidate_id: str
    full_name: str
    merit_rank: int
    admission_score: float
    preferred_program_ids: List[str]
    quota_category: QuotaCategoryEnum = QuotaCategoryEnum.GENERAL
    assigned_program_id: Optional[str] = None


class AllocationItemDTO(BaseModel):
    candidate_id: str
    full_name: str
    merit_rank: int
    assigned_program_id: str
    institution_name: str
    program_name: str
    quota_applied: str
    preference_order: int


class MatchingRunRequest(BaseModel):
    candidates: Optional[List[CandidatePreferenceDTO]] = None
    allow_quota_spillover: bool = True


class MatchingRunResponse(BaseModel):
    total_candidates: int
    total_programs: int
    total_seats_allocated: int
    unmatched_count: int
    is_envy_free: bool
    stability_score: float
    allocations: List[AllocationItemDTO]
    execution_time_ms: float


class MigrationStepDTO(BaseModel):
    step_number: int
    candidate_id: str
    candidate_name: str
    prior_program_id: Optional[str]
    new_program_id: str
    reason: str


class MigrationSimulationRequest(BaseModel):
    vacating_candidate_ids: List[str]


class MigrationSimulationResponse(BaseModel):
    vacated_seats_count: int
    total_cascades: int
    migration_steps: List[MigrationStepDTO]
    updated_allocations: List[AllocationItemDTO]


class AdmissionProbabilityQueryDTO(BaseModel):
    candidate_merit_rank: int
    target_program_id: str
    quota_category: QuotaCategoryEnum = QuotaCategoryEnum.GENERAL


class AdmissionProbabilityResponseDTO(BaseModel):
    candidate_merit_rank: int
    target_program_id: str
    institution_name: str
    program_name: str
    historical_cutoff_rank: int
    admission_probability: float
    confidence_interval: str
    risk_tier: str
    recommendation: str


class AdmissionMatrixStatusDTO(BaseModel):
    active_programs_count: int
    total_national_seats: int
    algorithm_version: str
    quota_categories_active: int
    system_health: str
