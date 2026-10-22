"""
===================================================================================
Module: Predictive Analytics & Admission Schemas (ভবিষ্যদ্বাণী ও ভর্তি স্কিমা)
Topic: Dual-Resilience Pydantic v2 / BaseDTO Validation Contracts
File: backend/app/schemas/predictive_analytics_schema.py
Purpose: Defines validated input request and response models for Bayesian CGPA
         forecasting, National Cohort rank projections, Competitive Admission
         probabilities, and What-If sensitivity simulations.
Audience: Backend Engineers, API Client Developers, Schema Validators
Standards: OpenAPI 3.1.0 Standard, Pydantic v2 Core Models, Zero-Emoji
===================================================================================
"""

from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field

    class GPAPredictionRequest(BaseModel):
        student_id: str = Field(..., description="শিক্ষার্থীর ইউনিক আইডি")
        target_exam: str = Field("HSC_SCIENCE", description="টার্গেট জাতীয় পরীক্ষা (HSC_SCIENCE, SSC_SCIENCE, ইত্যাদি)")
        subject_performances: List[Dict[str, Any]] = Field(..., min_length=1, description="বিষয়ভিত্তিক পারফরম্যান্স তালিকা")
        historical_exam_scores: Optional[List[float]] = Field(default_factory=list, description="বিগত মাইলস্টোন বা মডেল টেস্ট স্কোরের তালিকা")
        study_consistency_index: float = Field(0.85, ge=0.0, le=1.0, description="পড়াশোনার ধারাবাহিকতা সূচক (০.০ - ১.০)")

    class AdmissionProbabilityRequest(BaseModel):
        student_id: str = Field(..., description="শিক্ষার্থীর ইউনিক আইডি")
        subject_scores: Dict[str, float] = Field(..., description="বিষয়ভিত্তিক প্রাপ্ত গড় নম্বর ডিকশনারি")
        predicted_cgpa: float = Field(5.00, ge=0.0, le=5.00, description="প্রত্যাশিত বোর্ড সিজিপিএ")

    class SensitivitySimulationRequest(BaseModel):
        student_id: str = Field(..., description="শিক্ষার্থীর ইউনিক আইডি")
        track_id: str = Field(..., description="টার্গেট বিশ্ববিদ্যালয় ভর্তি ট্র্যাক আইডি (যেমন: BUET_ENG, DU_KA)")
        baseline_subject_scores: Dict[str, float] = Field(..., description="বর্তমান বেসলাইন নম্বর")
        score_deltas: Dict[str, float] = Field(..., description="সিমুলেটেড নম্বর পরিবর্তন (+/- নম্বর)")
        current_rank: int = Field(15000, ge=1, description="বর্তমান আনুমানিক জাতীয় র‍্যাংক")

except ImportError:
    # Graceful Fallback DTO for environments without pydantic
    class BaseDTO:
        def __init__(self, **kwargs: Any) -> None:
            for k, v in kwargs.items():
                setattr(self, k, v)

        def dict(self) -> Dict[str, Any]:
            return self.__dict__

    class GPAPredictionRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(
            self,
            student_id: str = "",
            target_exam: str = "HSC_SCIENCE",
            subject_performances: Optional[List[Dict[str, Any]]] = None,
            historical_exam_scores: Optional[List[float]] = None,
            study_consistency_index: float = 0.85,
            **kwargs: Any
        ) -> None:
            super().__init__(
                student_id=student_id,
                target_exam=target_exam,
                subject_performances=subject_performances or [],
                historical_exam_scores=historical_exam_scores or [],
                study_consistency_index=study_consistency_index,
                **kwargs
            )

    class AdmissionProbabilityRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(
            self,
            student_id: str = "",
            subject_scores: Optional[Dict[str, float]] = None,
            predicted_cgpa: float = 5.00,
            **kwargs: Any
        ) -> None:
            super().__init__(
                student_id=student_id,
                subject_scores=subject_scores or {},
                predicted_cgpa=predicted_cgpa,
                **kwargs
            )

    class SensitivitySimulationRequest(BaseDTO):  # type: ignore[no-redef]
        def __init__(
            self,
            student_id: str = "",
            track_id: str = "",
            baseline_subject_scores: Optional[Dict[str, float]] = None,
            score_deltas: Optional[Dict[str, float]] = None,
            current_rank: int = 15000,
            **kwargs: Any
        ) -> None:
            super().__init__(
                student_id=student_id,
                track_id=track_id,
                baseline_subject_scores=baseline_subject_scores or {},
                score_deltas=score_deltas or {},
                current_rank=current_rank,
                **kwargs
            )
