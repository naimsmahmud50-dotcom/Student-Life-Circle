"""
Pydantic Schemas for Phase 59: Multi-LLM AI Gateway & Prompt Injection Shield.
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


# --- Schemas for Multi-LLM Router Gateway ---
class MultiLlmRouteRequest(BaseModel):
    prompt: str = Field(..., description="Prompt or query to send to LLM gateway")
    task_type: Optional[str] = Field("math_reasoning", description="math_reasoning, essay_evaluation, fast_mcq_chat, code_check")
    max_tokens: Optional[int] = Field(1024, description="Maximum generation token budget")
    preferred_provider: Optional[str] = Field("auto", description="auto, gemini, claude, deepseek")


class MultiLlmRouteResponse(BaseModel):
    selected_model: str
    provider: str
    routing_reason: str
    fallback_occurred: bool
    token_count: int
    estimated_cost_usd: float
    estimated_cost_bdt: float
    generated_text: str


# --- Schemas for Prompt Injection Sanitizer ---
class PromptSanitizeRequest(BaseModel):
    raw_user_input: str = Field(..., description="Untrusted student/user prompt input")
    system_context: Optional[str] = Field(None, description="System instructions or grading rubrics")
    enable_canary: Optional[bool] = Field(True, description="Inject cryptographic canary tripwire")


class PromptSanitizeResponse(BaseModel):
    is_safe: bool
    risk_score: int
    attack_vectors_detected: List[str]
    sanitized_bounded_prompt: str
    canary_token: Optional[str]
    verdict: str


# --- Schemas for Semantic Output Validator ---
class OutputValidateRequest(BaseModel):
    raw_model_output: str = Field(..., description="Generated raw text from the AI model")
    target_sink: Optional[str] = Field("html_dom", description="html_dom, shell_sandbox, json_structured")
    canary_token_to_verify: Optional[str] = Field(None, description="Active canary token to monitor for leak")


class OutputValidateResponse(BaseModel):
    is_safe_to_sink: bool
    sanitized_output: str
    canary_leak_detected: bool
    violations_stripped: List[str]
    sink_target: str
