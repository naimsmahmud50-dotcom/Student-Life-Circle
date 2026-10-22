"""
Pydantic v2 schemas and DTOs for Phase 40:
- Autonomous AI Formal Verification Sandbox (Hoare Logic & Mutation Score)
- Decentralized Knowledge Graph IPFS Merkle DAG Engine
- FinTech Quantitative Risk & Black-Scholes Analytics
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
        return default if default is not ... else None


# -----------------------------------------------------------------------------
# 1. Formal Verification & Mutation Testing Schemas
# -----------------------------------------------------------------------------

class HoareVerificationRequest(BaseModel):
    code_str: str = Field(..., description="Student algorithm source code snippet to verify")
    pre_condition: str = Field(default="n >= 0", description="Pre-condition assertion string P")
    post_condition: str = Field(default="result >= 0", description="Post-condition assertion string Q")
    loop_invariant: Optional[str] = Field(default=None, description="Candidate loop invariant assertion string I")
    ranking_variant: Optional[str] = Field(default=None, description="Ranking function variant V to prove termination")

class HoareVerificationResponse(BaseModel):
    verdict: str
    valid: bool
    message: str
    counterexample: Optional[Dict[str, Any]] = None
    invariants_held: bool
    termination_proven: bool
    ranking_variant: Optional[str] = None

class MutationScoreRequest(BaseModel):
    total_mutants: int = Field(default=20, description="Total number of mutated program variants generated")
    killed_mutants: int = Field(default=18, description="Number of mutants killed by the test suite")
    operators_applied: Optional[List[str]] = Field(default=None, description="List of mutation operators applied (e.g. AOR, ROR, LCR)")

class MutationScoreResponse(BaseModel):
    total_mutants: int
    killed_mutants: int
    survived_mutants: int
    mutation_score_pct: float
    adequacy_rating: str
    operators_applied: List[str]


# -----------------------------------------------------------------------------
# 2. Decentralized Knowledge DAG (IPFS) Schemas
# -----------------------------------------------------------------------------

class CreateDagNodeRequest(BaseModel):
    title: str = Field(..., description="Curriculum or syllabus node title")
    content: str = Field(..., description="Node Markdown / LaTeX body content")
    author: Optional[str] = Field(default="Academic Contributor", description="Creator identity")
    parent_cids: Optional[List[str]] = Field(default=None, description="List of ancestor CIDs in the syllabus DAG")
    tags: Optional[List[str]] = Field(default=None, description="Syllabus taxonomy tags")

class DagNodeResponse(BaseModel):
    cid: str
    title: str
    content: str
    author: str
    parents: List[str]
    tags: List[str]
    size_bytes: int
    sha256_hash: str
    pin_status: str
    federated_peers: List[str]

class VerifyDagNodeResponse(BaseModel):
    cid: str
    verified: bool
    status: str
    message: str
    sha256_hash: Optional[str] = None
    pin_status: Optional[str] = None
    size_bytes: Optional[int] = None

class DagStatusResponse(BaseModel):
    total_nodes: int
    total_bytes: int
    pinned_nodes: int
    federation_active: bool
    consensus_protocol: str


# -----------------------------------------------------------------------------
# 3. FinTech Quantitative Risk & Black-Scholes Schemas
# -----------------------------------------------------------------------------

class BlackScholesRequest(BaseModel):
    spot_price: float = Field(default=100.0, description="Underlying asset spot price S")
    strike_price: float = Field(default=100.0, description="Option strike price K")
    time_to_maturity: float = Field(default=1.0, description="Time to maturity in years T")
    risk_free_rate: float = Field(default=0.05, description="Annualized risk-free interest rate r")
    volatility: float = Field(default=0.20, description="Annualized volatility sigma")

class GreeksDTO(BaseModel):
    call_delta: float
    put_delta: float
    gamma: float
    call_theta_per_day: float
    put_theta_per_day: float
    vega_per_pct: float
    call_rho_per_pct: float
    put_rho_per_pct: float

class BlackScholesResponse(BaseModel):
    spot_price: float
    strike_price: float
    time_to_maturity_years: float
    risk_free_rate: float
    volatility: float
    call_price: float
    put_price: float
    intrinsic_value_call: float
    time_value_call: float
    greeks: GreeksDTO

class PortfolioVarRequest(BaseModel):
    portfolio_value: float = Field(default=100000.0, description="Current portfolio asset value ($)")
    expected_annual_return: float = Field(default=0.12, description="Expected annualized portfolio return (0.12 = 12%)")
    annual_volatility: float = Field(default=0.18, description="Annualized portfolio standard deviation / volatility")
    holding_period_days: Optional[int] = Field(default=1, description="Holding period in trading days")
    risk_free_rate: Optional[float] = Field(default=0.05, description="Benchmark risk-free rate")

class PortfolioVarResponse(BaseModel):
    portfolio_value: float
    holding_period_days: int
    period_expected_return_pct: float
    period_volatility_pct: float
    var_95_pct: float
    var_95_amount: float
    var_99_pct: float
    var_99_amount: float
    annualized_sharpe_ratio: float
    risk_adjusted_rating: str
