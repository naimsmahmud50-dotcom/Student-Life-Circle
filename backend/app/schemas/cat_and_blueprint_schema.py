"""
================================================================================
MODULE: Schemas & Data Contracts (ক্যাট ও ব্লুপ্রিন্ট কম্পোজার ডেটা মডেল)
TOPIC: Dual-Resilience BaseDTO Contract for Adaptive CAT & Curriculum Blueprints
FILE: backend/app/schemas/cat_and_blueprint_schema.py
PURPOSE: Defines strongly typed contract models for initiating Computerized
         Adaptive Testing (CAT) sessions, submitting item responses, evaluating
         IRT latent abilities (Theta), and authoring balanced curriculum blueprints.
AUDIENCE: Frontend Engineers, Backend Controllers, API Integration Testers.
STANDARDS: Pydantic v2 Contract Compatibility, ISO/IEC 25010 Data Quality.
================================================================================
"""

from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    class BaseModel:
        def __init__(self, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self) -> Dict[str, Any]:
            return self.__dict__
    def Field(*args: Any, **kwargs: Any) -> Any:
        return kwargs.get("default", None)


class CatSessionStartRequest(BaseModel):
    """Payload to initiate a new Computerized Adaptive Testing session."""
    student_id: str
    subject: str = "গণিত"
    initial_theta: float = 0.0


class CatAnswerSubmitRequest(BaseModel):
    """Payload when a student answers an administered adaptive question."""
    item_id: str
    selected_option_id: str


class BlueprintComposeRequest(BaseModel):
    """Payload to automatically compose and validate a curriculum exam blueprint."""
    name: str
    subject: str = "সাধারণ গণিত"
    class_grade: int = 8
    total_questions: int = 25
    duration_minutes: int = 25
    negative_marking: float = 0.0
    cognitive_distribution: Dict[str, float]
    chapter_distribution: Dict[str, float]
