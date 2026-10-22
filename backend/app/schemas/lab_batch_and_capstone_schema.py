"""
Pydantic v2 schemas and DTOs for Phase 32:
- Interactive Virtual Science Lab (DC Circuit Simulator, Geometric Optics Ray Tracer, Acid-Base Titration)
- Neighborhood Multi-Guardian Micro-Coaching Pool with Fractional Escrow Splitting
- Corporate Industry Capstone Marketplace & Pre-Placement Offer (PPO) Conversion Tracker
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
# 1. Virtual Science Laboratory Simulation Schemas
# -----------------------------------------------------------------------------

class CircuitComponent(BaseModel):
    id: str
    type: str = "RESISTOR"  # "RESISTOR", "BULB", "CAPACITOR"
    value: float = 10.0  # Resistance in Ohms

class CircuitSimulationRequest(BaseModel):
    circuit_id: str = "ckt-demo-01"
    source_voltage: float = 12.0  # Volts
    configuration: str = "SERIES"  # "SERIES" or "PARALLEL"
    components: List[Dict[str, Any]] = []

class CircuitSimulationResponse(BaseModel):
    circuit_id: str
    source_voltage: float
    configuration: str
    total_resistance: float
    total_current: float
    total_power: float
    component_telemetry: List[Dict[str, Any]]
    is_short_circuit_safe: bool = True
    execution_status: str = "SUCCESS"

class OpticsRayTraceRequest(BaseModel):
    lens_type: str = "CONVEX"  # "CONVEX" or "CONCAVE"
    focal_length_cm: float = 15.0
    object_distance_cm: float = 30.0
    object_height_cm: float = 5.0

class OpticsRayTraceResponse(BaseModel):
    lens_type: str
    focal_length_cm: float
    object_distance_cm: float
    object_height_cm: float
    image_distance_cm: Optional[float] = None
    image_height_cm: Optional[float] = None
    magnification: Optional[float] = None
    image_nature: str  # "REAL_INVERTED", "VIRTUAL_UPRIGHT", or "AT_INFINITY"
    ray_coordinates: Dict[str, Any]
    is_at_focus: bool = False

class TitrationSimulationRequest(BaseModel):
    analyte: str = "HCl"
    titrant: str = "NaOH"
    analyte_volume_ml: float = 25.0
    analyte_molarity: float = 0.1
    titrant_molarity: float = 0.1
    indicator: str = "PHENOLPHTHALEIN"  # "PHENOLPHTHALEIN", "METHYL_ORANGE"

class TitrationSimulationResponse(BaseModel):
    analyte: str
    titrant: str
    equivalence_volume_ml: float
    equivalence_ph: float
    indicator: str
    titration_curve: List[Dict[str, Any]]
    initial_ph: float
    final_ph: float
    status: str = "COMPLETED"

class LabReportSynthesisRequest(BaseModel):
    lab_type: str = "CIRCUIT_OHMS_LAW"
    student_id: str = "std-demo"
    experimental_value: float
    theoretical_value: float
    observations: str = ""

class LabReportSynthesisResponse(BaseModel):
    report_id: str
    lab_type: str
    student_id: str
    experimental_value: float
    theoretical_value: float
    relative_error_pct: float
    conclusion: str
    verification_stamp: str
    generated_at: str


# -----------------------------------------------------------------------------
# 2. Multi-Guardian Micro-Coaching Pool Schemas
# -----------------------------------------------------------------------------

class CreateCoachingBatchRequest(BaseModel):
    batch_title: str
    subject: str = "Physics - HSC 2026"
    lead_guardian_id: str
    total_monthly_fee_bdt: float = 5000.0
    max_capacity: int = 5
    curriculum: str = "NCTB_SCIENCE"

class JoinBatchGuardianRequest(BaseModel):
    guardian_id: str
    guardian_name: str
    student_name: str

class CoachingBatchResponse(BaseModel):
    batch_id: str
    batch_title: str
    subject: str
    total_monthly_fee_bdt: float
    max_capacity: int
    current_guardians: int
    cost_per_guardian_bdt: float
    guardian_shares: List[Dict[str, Any]]
    status: str
    created_at: str

class LogBatchSessionRequest(BaseModel):
    session_topic: str
    attendees: List[str] = []
    duration_minutes: int = 60
    mentor_notes: str = ""

class BatchSessionResponse(BaseModel):
    session_id: str
    batch_id: str
    session_topic: str
    attendee_count: int
    attendance_pct: float
    logged_at: str


# -----------------------------------------------------------------------------
# 3. Corporate Industry Capstone Marketplace Schemas
# -----------------------------------------------------------------------------

class CapstoneBrief(BaseModel):
    capstone_id: str
    title: str
    corporate_partner: str
    industry_vertical: str
    difficulty: str
    stipend_bdt: float
    ppo_opportunity: bool
    key_skills: List[str]
    description: str

class SubmitCapstoneMilestoneRequest(BaseModel):
    student_id: str
    student_name: str
    milestone_stage: str = "ARCHITECTURE_PROPOSAL"  # ARCHITECTURE_PROPOSAL, PROTOTYPE_DEMO, FINAL_DELIVERABLES
    deliverables_url: str
    executive_summary: str

class CapstoneMilestoneResponse(BaseModel):
    submission_id: str
    capstone_id: str
    student_id: str
    student_name: str
    milestone_stage: str
    deliverables_url: str
    status: str
    score: float
    ppo_eligible: bool
    corporate_feedback: str
    submitted_at: str

class CapstoneDirectoryResponse(BaseModel):
    capstones: List[Dict[str, Any]]
    total: int
