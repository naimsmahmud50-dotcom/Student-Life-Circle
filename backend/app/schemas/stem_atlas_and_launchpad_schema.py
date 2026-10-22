"""
Pydantic v2 schemas and DTOs for Phase 33:
- Interactive STEM 3D Molecular Geometry & Chemical Reaction Balancer
- Autonomous Syllabus Knowledge Atlas & Past Board Exam Frequency Engine
- Decentralized Student Innovation Launchpad & Micro-Grant Incubator
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
# 1. STEM 3D Molecular Geometry & Chemical Balancing Schemas
# -----------------------------------------------------------------------------

class MolecularGeometryRequest(BaseModel):
    formula: str = "H2O"
    central_atom: Optional[str] = None
    steric_number: Optional[int] = None
    lone_pairs: Optional[int] = None

class MolecularGeometryResponse(BaseModel):
    formula: str
    central_atom: str
    steric_number: int
    bonded_atoms: int
    lone_pairs: int
    vsepr_notation: str
    ideal_bond_angle_deg: float
    actual_bond_angle_deg: float
    electron_geometry: str
    molecular_geometry: str
    hybridization: str
    is_polar: bool
    spatial_coordinates: List[Dict[str, Any]]
    explanation: str

class RedoxReactionBalanceRequest(BaseModel):
    reaction_equation: str = "MnO4- + Fe2+ -> Mn2+ + Fe3+"
    medium: str = "ACIDIC"  # "ACIDIC" or "BASIC"

class RedoxReactionBalanceResponse(BaseModel):
    unbalanced_equation: str
    balanced_equation: str
    medium: str
    oxidation_half_reaction: str
    reduction_half_reaction: str
    electrons_transferred: int
    is_balanced: bool = True
    method: str = "ION_ELECTRON_METHOD"


# -----------------------------------------------------------------------------
# 2. Syllabus Knowledge Atlas & Past Board Frequency Schemas
# -----------------------------------------------------------------------------

class SyllabusConceptNode(BaseModel):
    concept_id: str
    subject: str
    chapter: str
    title: str
    prerequisites: List[str]
    difficulty: str
    core_equations: List[str]
    key_definitions: str

class SyllabusGraphResponse(BaseModel):
    subject: str
    total_nodes: int
    nodes: List[Dict[str, Any]]
    dependency_edges: List[Dict[str, str]]

class BoardExamFrequencyResponse(BaseModel):
    subject: str
    chapter: str
    total_appearances: int
    frequency_by_board: Dict[str, int]
    high_yield_topics: List[str]

class FormulaReferenceResponse(BaseModel):
    subject: str
    chapter: str
    formulas: List[Dict[str, str]]


# -----------------------------------------------------------------------------
# 3. Student Innovation Launchpad & Micro-Grant Incubator Schemas
# -----------------------------------------------------------------------------

class PitchProjectRequest(BaseModel):
    title: str
    track: str = "AGRI_TECH"  # "AGRI_TECH", "FINTECH", "EDTECH", "HEALTH_AI"
    leader_student_id: str
    leader_student_name: str
    team_members: List[str] = []
    summary: str
    grant_requested_bdt: float = 25000.0
    demo_repo_url: str

class PitchProjectResponse(BaseModel):
    project_id: str
    title: str
    track: str
    leader_student_id: str
    leader_student_name: str
    summary: str
    grant_requested_bdt: float
    ip_proof_hash: str
    status: str
    votes_count: int
    grant_status: str
    created_at: str

class CastProjectVoteRequest(BaseModel):
    voter_student_id: str
    voter_reputation_score: float = 100.0

class ProjectVoteResponse(BaseModel):
    vote_id: str
    project_id: str
    voter_student_id: str
    weighted_vote_value: float
    new_total_votes: int
    voted_at: str

class ReleaseGrantTrancheRequest(BaseModel):
    milestone_stage: str = "PROTOTYPE_DEMO"  # "PROPOSAL_VALIDATION", "PROTOTYPE_DEMO", "PILOT_DEPLOYMENT"
    mentor_reviewer_id: str
    approval_notes: str = ""

class GrantTrancheResponse(BaseModel):
    release_id: str
    project_id: str
    milestone_stage: str
    amount_released_bdt: float
    escrow_balance_remaining_bdt: float
    mentor_reviewer_id: str
    status: str
    released_at: str
