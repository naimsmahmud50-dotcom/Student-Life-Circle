"""
Pydantic v2 schemas and DTOs for Phase 34:
- Interactive Algorithm Complexity Sandbox & AST Code Analyzer
- Autonomous Academic Thesis & Research Paper Citation Graph
- Campus Ambassador & Peer Micro-Internship Syndicate
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
# 1. Algorithm Complexity Sandbox & AST Code Analyzer Schemas
# -----------------------------------------------------------------------------

class CodeComplexityRequest(BaseModel):
    code: str = "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr"
    language: str = "python"
    function_name: Optional[str] = None

class CodeComplexityResponse(BaseModel):
    code_length: int
    ast_parsed: bool
    detected_loops: int
    max_loop_nesting: int
    has_recursion: bool
    time_complexity: str
    space_complexity: str
    asymptotic_bound_explanation: str
    recommendations: List[str]

class AlgorithmTraceStep(BaseModel):
    step_number: int
    action: str
    current_state: List[Any]
    highlighted_indices: List[int]
    description: str

class AlgorithmTraceRequest(BaseModel):
    algorithm: str = "MERGE_SORT"  # BUBBLE_SORT, MERGE_SORT, QUICK_SORT, BINARY_SEARCH, FIBONACCI_DP
    input_data: List[int] = [9, 3, 7, 1, 5, 4, 8, 2]

class AlgorithmTraceResponse(BaseModel):
    algorithm: str
    input_data: List[int]
    total_steps: int
    steps: List[AlgorithmTraceStep]
    final_state: List[Any]
    time_taken_ms: float


# -----------------------------------------------------------------------------
# 2. Academic Thesis & Citation Graph Schemas
# -----------------------------------------------------------------------------

class ThesisPaperSubmitRequest(BaseModel):
    title: str = "Low-Resource Neural Machine Translation for Bangla Dialects"
    abstract: str = "We propose an unsupervised alignment framework with cross-lingual embeddings for regional Bangla dialects."
    authors: List[str] = ["Tanvir Ahmed", "Nusrat Jahan"]
    institution: str = "BUET"
    department: str = "Computer Science & Engineering"
    publication_year: int = 2025
    keywords: List[str] = ["Bangla NLP", "Machine Translation", "Dialects"]
    cited_paper_ids: List[str] = []

class ThesisPaperResponse(BaseModel):
    paper_id: str
    title: str
    abstract: str
    authors: List[str]
    institution: str
    department: str
    publication_year: int
    doi: str
    keywords: List[str]
    citation_count: int
    cited_by: List[str]
    cites: List[str]
    bibtex: str
    created_at: str

class ThesisSimilarityCheckRequest(BaseModel):
    text_sample: str
    min_shingle_size: int = 3

class ThesisSimilarityMatch(BaseModel):
    paper_id: str
    title: str
    institution: str
    similarity_score: float
    matched_fragments: List[str]

class ThesisSimilarityCheckResponse(BaseModel):
    originality_score: float
    highest_similarity: float
    flagged_as_duplicate: bool
    matches: List[ThesisSimilarityMatch]

class ResearchGrantMatchRequest(BaseModel):
    field_of_study: str = "Computer Science & AI"
    academic_level: str = "UNDERGRADUATE"

class ResearchGrantMatch(BaseModel):
    grant_id: str
    title: str
    funding_agency: str
    amount_bdt: float
    eligibility_criteria: List[str]
    deadline: str
    application_url: str

class ResearchGrantMatchResponse(BaseModel):
    matched_grants: List[ResearchGrantMatch]
    total_matched: int


# -----------------------------------------------------------------------------
# 3. Campus Ambassador & Peer Micro-Internship Syndicate Schemas
# -----------------------------------------------------------------------------

class CampusRegistryResponse(BaseModel):
    campuses: List[Dict[str, Any]]
    total_campuses: int

class AmbassadorTaskResponse(BaseModel):
    task_id: str
    title: str
    campus_id: str
    campus_name: str
    category: str
    points_reward: int
    grant_stipend_bdt: float
    status: str
    claimed_by: Optional[str]
    evidence_url: Optional[str]
    verification_feedback: Optional[str]

class ClaimAmbassadorTaskRequest(BaseModel):
    task_id: str
    student_id: str

class SubmitAmbassadorTaskRequest(BaseModel):
    task_id: str
    student_id: str
    evidence_url: str
    impact_report: str

class VerifyAmbassadorTaskRequest(BaseModel):
    task_id: str
    verifier_id: str
    approved: bool
    feedback: str

class AmbassadorProfileResponse(BaseModel):
    student_id: str
    name: str
    campus_name: str
    tier: str
    total_points: int
    completed_tasks: int
    earned_stipend_bdt: float
    digital_badge_signature: str
