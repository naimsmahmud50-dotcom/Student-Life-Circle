"""
Pydantic v2 schemas and DTOs for Phase 37:
- Edge AI Robotics & Autonomous Drone Mission Simulator
- Genomic Bioinformatics & CRISPR sgRNA Sequence Engine
- Biomedical Diagnostic Sandbox & ROC-AUC Pathology Lab
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
        return default


# -----------------------------------------------------------------------------
# 1. Edge AI Robotics & Drone Simulator Schemas
# -----------------------------------------------------------------------------

class DronePidSimRequest(BaseModel):
    kp: float = Field(default=1.2, description="Proportional gain")
    ki: float = Field(default=0.05, description="Integral gain")
    kd: float = Field(default=0.35, description="Derivative gain")
    target_angle_deg: float = Field(default=15.0, description="Target pitch/roll angle in degrees")
    initial_angle_deg: float = Field(default=0.0, description="Initial angle in degrees")
    dt_seconds: float = Field(default=0.02, description="Time step in seconds (e.g. 50 Hz loop)")
    steps: int = Field(default=80, description="Number of simulation steps")

class DronePidSimResponse(BaseModel):
    settling_time_seconds: float
    overshoot_pct: float
    steady_state_error_deg: float
    is_stable: bool
    status_summary: str
    trajectory_sample: List[Dict[str, float]]

class DroneEnduranceRequest(BaseModel):
    mass_kg: float = Field(default=1.45, description="Total drone AUW in kg")
    rotor_count: int = Field(default=4, description="Number of rotors (4 for quadcopter, 6 for hexacopter)")
    battery_capacity_mah: float = Field(default=5200.0, description="LiPo capacity in milliampere-hours")
    battery_voltage_v: float = Field(default=14.8, description="LiPo nominal voltage (e.g. 4S = 14.8V)")
    hover_efficiency_g_per_w: float = Field(default=8.2, description="Motor thrust efficiency in grams per Watt")

class DroneEnduranceResponse(BaseModel):
    total_weight_n: float
    hover_power_watts: float
    battery_energy_wh: float
    hover_time_minutes: float
    thrust_to_weight_ratio: float
    flight_readiness: str  # MISSION_READY, SUB_OPTIMAL, DANGEROUSLY_OVERWEIGHT


# -----------------------------------------------------------------------------
# 2. Genomic Bioinformatics & CRISPR Schemas
# -----------------------------------------------------------------------------

class SequenceAlignRequest(BaseModel):
    sequence_a: str = Field(default="ATGCGATCGATCGATC", description="Query DNA/RNA sequence")
    sequence_b: str = Field(default="ATGCGATGGATCGATC", description="Reference DNA/RNA sequence")
    alignment_type: str = Field(default="GLOBAL", description="GLOBAL (Needleman-Wunsch) or LOCAL (Smith-Waterman)")
    match_score: int = 2
    mismatch_penalty: int = -1
    gap_penalty: int = -2

class SequenceAlignResponse(BaseModel):
    alignment_type: str
    aligned_seq_a: str
    aligned_seq_b: str
    alignment_score: int
    identity_pct: float
    matches: int
    mismatches: int
    gaps: int

class CrisprGuideScanRequest(BaseModel):
    target_dna_sequence: str = Field(
        default="ATGCGTACCGGATCGATCGATCGGATCGAATCGATCGG",
        description="Target genomic locus sequence (minimum 23 nt)"
    )
    pam_motif: str = Field(default="NGG", description="PAM motif: NGG for SpCas9")

class CrisprGuideResponse(BaseModel):
    target_length_nt: int
    transcribed_mrna: str
    gc_content_pct: float
    melting_temperature_c: float
    guide_count: int
    guides: List[Dict[str, Any]]


# -----------------------------------------------------------------------------
# 3. Biomedical Diagnostic Sandbox & ROC-AUC Schemas
# -----------------------------------------------------------------------------

class DiagnosticConfusionMatrixRequest(BaseModel):
    true_positives: int = 185
    false_positives: int = 15
    true_negatives: int = 280
    false_negatives: int = 20

class DiagnosticPerformanceResponse(BaseModel):
    total_samples: int
    sensitivity_tpr: float
    specificity_tnr: float
    positive_predictive_value_ppv: float
    negative_predictive_value_npv: float
    f1_score: float
    balanced_accuracy: float
    diagnostic_tier: str  # CLINICALLY_VALIDATED, ACCEPTABLE_SCREENING, INADEQUATE

class DiagnosticRocCurveRequest(BaseModel):
    disease_name: str = "Pulmonary Tuberculosis (Chest X-Ray)"
    current_threshold: float = Field(default=0.50, description="Decision probability threshold [0.05, 0.95]")

class DiagnosticRocCurveResponse(BaseModel):
    disease_name: str
    auc_roc: float
    current_threshold: float
    operating_point_sensitivity: float
    operating_point_specificity: float
    curve_points: List[Dict[str, float]]
    clinical_recommendation: str
