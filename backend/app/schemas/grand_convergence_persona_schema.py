"""
Pydantic Schemas for Phase 60: The Grand Convergence & Adaptive Persona Router.
Dual-resilience fallback included for zero-dependency test execution.
"""

from typing import Dict, Any, List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover
    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
    def Field(default=None, **kwargs):
        return default


# --- Schemas for Grand Convergence Attestation ---
class GrandConvergenceAttestRequest(BaseModel):
    operator_id: Optional[str] = Field("ops:admin:convergence_monitor", description="Audit operator identity")
    include_test_metrics: Optional[bool] = Field(True, description="Whether to include test suite counts")


class GrandConvergenceAttestResponse(BaseModel):
    platform_name: str
    total_phases: int
    overall_health: str
    operational_sla: str
    global_merkle_root: str
    pillars: List[Dict[str, Any]]
    attestation_timestamp: str
    verified_tests_count: int


# --- Schemas for Adaptive Persona Router ---
class PersonaRouteRequest(BaseModel):
    user_role: str = Field(..., description="student, educator, guardian, institutional_admin, corporate_recruiter")
    device_tier: Optional[str] = Field("desktop", description="desktop, tablet, mobile_low_bandwidth")
    preferred_theme: Optional[str] = Field("auto", description="auto, dark, light")


class PersonaRouteResponse(BaseModel):
    user_role: str
    role_display_title: str
    primary_navigation_tabs: List[str]
    dashboard_kpis: List[Dict[str, Any]]
    quick_action_shortcuts: List[Dict[str, Any]]
    accessibility_parameters: Dict[str, Any]


# --- Schemas for Universal Omni-Search ---
class OmniSearchRequest(BaseModel):
    query: str = Field(..., description="Fuzzy search query string")
    category_filter: Optional[str] = Field("all", description="all, lectures, tuitions, jobs, labs, credentials")
    limit: Optional[int] = Field(10, description="Maximum results to return")


class OmniSearchResponse(BaseModel):
    query: str
    total_matches: int
    search_latency_ms: float
    results: List[Dict[str, Any]]
    suggested_terms: List[str]
