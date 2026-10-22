"""
================================================================================
MODULE: Schemas & Data Contracts (সোক্র্যাটিক টিউটর ও ভিজ্যুয়ালাইজার স্কিমা)
TOPIC: Dual-Resilience BaseDTO Contract for Socratic Tutoring & Vector Diagrams
FILE: backend/app/schemas/socratic_and_visualizer_schema.py
PURPOSE: Defines strongly typed contract models for initializing Socratic AI
         dialogues, exchanging pedagogical scaffolding messages, requesting
         graded hints without answer leakage, and fetching SVG visualizer models.
AUDIENCE: Frontend Engineers, Backend Controllers, API Integration Testers.
STANDARDS: Pydantic v2 Contract Compatibility, OWASP ASVS Level 2 Child Privacy.
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


class SocraticSessionStartRequest(BaseModel):
    """Payload to initiate a new Socratic AI tutoring dialogue."""
    student_id: str
    question_id: str = "q_math_pythagoras"
    is_minor: bool = True


class SocraticMessageSendRequest(BaseModel):
    """Payload when a student sends a response to the Socratic tutor."""
    message_text: str


class SocraticHintRequest(BaseModel):
    """Payload to request the next progressive scaffolding hint."""
    student_id: str


class GeometryVisualizerRequest(BaseModel):
    """Payload to request procedural SVG geometric visualization."""
    concept_id: str = "pythagoras_proof"
    param_a: float = 6.0
    param_b: float = 8.0
