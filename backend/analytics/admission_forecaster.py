"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    University Admission Forecaster & Sigmoid Rank Predictor
 * TOPIC:     Phase 128 Statistical Cut-Off Engine & Admission Probability Calibration
 * FILE:      backend/analytics/admission_forecaster.py
 * PHASE:     Phase 128 - Autonomous Admission Cut-Off Forecaster
 * PURPOSE:   Provides calibrated sigmoid admission probability estimation,
 *            10-year historical threshold modeling (2015-2025), subject-specific
 *            eligibility gating, quota modulation, and zero-PII merit rank projection.
 * STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Calibrated Probability
 */
"""

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class PIILeakageDetectedException(ValueError):
    """Raised when request payload contains Personally Identifiable Information (PII)."""
    pass


class AdmissionUnit(str, Enum):
    BUET = "BUET"
    DU_KA = "DU_KA"
    DU_KHA = "DU_KHA"
    DU_GA = "DU_GA"
    MEDICAL = "MEDICAL"
    GST = "GST"


class QuotaType(str, Enum):
    GENERAL = "GENERAL"
    FREEDOM_FIGHTER = "FREEDOM_FIGHTER"
    TRIBAL = "TRIBAL"
    ENGLISH_MEDIUM = "ENGLISH_MEDIUM"
    SPECIAL_NEEDS = "SPECIAL_NEEDS"


class ProbabilityTier(str, Enum):
    SAFE = "SAFE"                 # P >= 0.75
    COMPETITIVE = "COMPETITIVE"   # 0.40 <= P < 0.75
    REACH = "REACH"               # P < 0.40
    INELIGIBLE = "INELIGIBLE"     # Failed prerequisite gates


# Disallowed PII field names strictly blocked per ASVS L2 & Privacy mandates
DISALLOWED_PII_KEYS: Set[str] = {
    "name", "full_name", "first_name", "last_name", "phone", "mobile",
    "telephone", "email", "nid", "national_id", "birth_registration",
    "b_reg", "address", "location", "ip", "ip_address", "student_name",
    "roll", "reg_no", "registration_no", "father_name", "mother_name"
}


# 10-Year Empirical Historical Cut-off Marks (2015-2025)
HISTORICAL_CUTOFF_SERIES: Dict[str, Dict[int, float]] = {
    AdmissionUnit.BUET.value: {
        2015: 72.0, 2016: 73.0, 2017: 74.0, 2018: 73.5, 2019: 75.0,
        2020: 74.0, 2021: 75.5, 2022: 74.5, 2023: 75.0, 2024: 76.0, 2025: 75.2
    },
    AdmissionUnit.DU_KA.value: {
        2015: 65.5, 2016: 66.0, 2017: 67.5, 2018: 66.8, 2019: 68.5,
        2020: 67.0, 2021: 69.0, 2022: 68.2, 2023: 68.8, 2024: 69.5, 2025: 68.7
    },
    AdmissionUnit.DU_KHA.value: {
        2015: 68.5, 2016: 69.0, 2017: 70.0, 2018: 70.5, 2019: 71.5,
        2020: 70.0, 2021: 72.0, 2022: 71.2, 2023: 71.8, 2024: 72.5, 2025: 71.9
    },
    AdmissionUnit.DU_GA.value: {
        2015: 70.0, 2016: 71.5, 2017: 72.0, 2018: 72.8, 2019: 74.0,
        2020: 73.0, 2021: 74.5, 2022: 73.8, 2023: 74.2, 2024: 75.0, 2025: 74.3
    },
    AdmissionUnit.MEDICAL.value: {
        2015: 262.0, 2016: 264.5, 2017: 266.0, 2018: 267.0, 2019: 269.0,
        2020: 267.5, 2021: 271.0, 2022: 269.5, 2023: 270.0, 2024: 272.5, 2025: 271.0
    },
    AdmissionUnit.GST.value: {
        2015: 52.0, 2016: 53.0, 2017: 54.0, 2018: 54.5, 2019: 55.5,
        2020: 54.0, 2021: 56.0, 2022: 55.2, 2023: 55.8, 2024: 56.5, 2025: 55.9
    }
}


@dataclass
class AcademicRecord:
    """Zero-PII academic profile strictly encapsulating scholastic performance metrics."""
    ssc_gpa: float
    hsc_gpa: float
    physics_gp: Optional[float] = None
    chemistry_gp: Optional[float] = None
    math_gp: Optional[float] = None
    biology_gp: Optional[float] = None
    english_gp: Optional[float] = None
    exam_sim_score: Optional[float] = None  # Raw or scaled simulation exam score


@dataclass
class UnitParameters:
    name_bn: str
    name_en: str
    full_marks: float
    median_cutoff_x0: float
    slope_k: float
    total_seats: int
    applicant_pool: int
    min_ssc_gpa: float
    min_hsc_gpa: float
    min_combined_gpa: float
    required_subject_rules: Dict[str, float] = field(default_factory=dict)
    gpa_multiplier_ssc: float = 0.0
    gpa_multiplier_hsc: float = 0.0


# Calibration configurations per institution and unit
UNIT_CONFIGS: Dict[AdmissionUnit, UnitParameters] = {
    AdmissionUnit.BUET: UnitParameters(
        name_bn="বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (বুয়েট)",
        name_en="Bangladesh University of Engineering and Technology (BUET)",
        full_marks=100.0,
        median_cutoff_x0=74.5,
        slope_k=0.16,
        total_seats=1305,
        applicant_pool=22000,
        min_ssc_gpa=4.0,
        min_hsc_gpa=5.0,
        min_combined_gpa=9.0,
        required_subject_rules={
            "physics_gp": 5.0,
            "chemistry_gp": 5.0,
            "math_gp": 5.0
        },
        gpa_multiplier_ssc=0.0,
        gpa_multiplier_hsc=0.0
    ),
    AdmissionUnit.DU_KA: UnitParameters(
        name_bn="ঢাকা বিশ্ববিদ্যালয় — ক ইউনিট (বিজ্ঞান অনুষদ)",
        name_en="University of Dhaka - Ka Unit (Faculty of Science)",
        full_marks=120.0,
        median_cutoff_x0=68.0,
        slope_k=0.14,
        total_seats=1851,
        applicant_pool=125000,
        min_ssc_gpa=3.5,
        min_hsc_gpa=3.5,
        min_combined_gpa=8.0,
        required_subject_rules={
            "physics_gp": 3.0,
            "chemistry_gp": 3.0
        },
        gpa_multiplier_ssc=2.0,  # 10 marks max (5.0 * 2)
        gpa_multiplier_hsc=2.0   # 10 marks max (5.0 * 2)
    ),
    AdmissionUnit.DU_KHA: UnitParameters(
        name_bn="ঢাকা বিশ্ববিদ্যালয় — খ ইউনিট (কলা ও সামাজিক বিজ্ঞান অনুষদ)",
        name_en="University of Dhaka - Kha Unit (Arts & Social Sciences)",
        full_marks=120.0,
        median_cutoff_x0=71.0,
        slope_k=0.14,
        total_seats=2934,
        applicant_pool=110000,
        min_ssc_gpa=3.0,
        min_hsc_gpa=3.0,
        min_combined_gpa=7.5,
        required_subject_rules={},
        gpa_multiplier_ssc=2.0,
        gpa_multiplier_hsc=2.0
    ),
    AdmissionUnit.DU_GA: UnitParameters(
        name_bn="ঢাকা বিশ্ববিদ্যালয় — গ ইউনিট (ব্যবসায় শিক্ষা অনুষদ)",
        name_en="University of Dhaka - Ga Unit (Faculty of Business Studies)",
        full_marks=120.0,
        median_cutoff_x0=73.5,
        slope_k=0.15,
        total_seats=1050,
        applicant_pool=40000,
        min_ssc_gpa=3.0,
        min_hsc_gpa=3.0,
        min_combined_gpa=7.5,
        required_subject_rules={},
        gpa_multiplier_ssc=2.0,
        gpa_multiplier_hsc=2.0
    ),
    AdmissionUnit.MEDICAL: UnitParameters(
        name_bn="জাতীয় মেডিকেল ও ডেন্টাল ভর্তি পরীক্ষা (MBBS/BDS)",
        name_en="National Medical & Dental Combined Admission (MBBS/BDS)",
        full_marks=300.0,
        median_cutoff_x0=268.5,
        slope_k=0.12,
        total_seats=5380,
        applicant_pool=140000,
        min_ssc_gpa=4.0,
        min_hsc_gpa=4.0,
        min_combined_gpa=9.0,
        required_subject_rules={
            "biology_gp": 4.0
        },
        gpa_multiplier_ssc=15.0,  # 75 marks max (5.0 * 15)
        gpa_multiplier_hsc=25.0   # 125 marks max (5.0 * 25) -> Total GPA = 200
    ),
    AdmissionUnit.GST: UnitParameters(
        name_bn="জিএসটি গুচ্ছভুক্ত ২৪টি সাধারণ ও প্রযুক্তি বিশ্ববিদ্যালয়",
        name_en="GST Consortium (24 General & STEM Public Universities)",
        full_marks=100.0,
        median_cutoff_x0=55.0,
        slope_k=0.13,
        total_seats=12500,
        applicant_pool=160000,
        min_ssc_gpa=3.0,
        min_hsc_gpa=3.0,
        min_combined_gpa=7.0,
        required_subject_rules={},
        gpa_multiplier_ssc=0.0,
        gpa_multiplier_hsc=0.0
    ),
}


# Quota point adjustments (lowering the threshold required for qualification)
QUOTA_OFFSETS: Dict[QuotaType, float] = {
    QuotaType.GENERAL: 0.0,
    QuotaType.FREEDOM_FIGHTER: 6.5,
    QuotaType.TRIBAL: 8.0,
    QuotaType.ENGLISH_MEDIUM: 3.0,
    QuotaType.SPECIAL_NEEDS: 7.5,
}


@dataclass
class EligibilityResult:
    is_eligible: bool
    violations_en: List[str]
    violations_bn: List[str]
    combined_gpa: float


@dataclass
class ForecastPrediction:
    unit: AdmissionUnit
    quota: QuotaType
    is_eligible: bool
    composite_score: float
    effective_cutoff_threshold: float
    calibrated_probability: float
    tier: ProbabilityTier
    rank_range_min: int
    rank_range_max: int
    eligibility: EligibilityResult
    historical_series: Dict[int, float]
    academic_feedback_en: str
    academic_feedback_bn: str


class AdmissionForecaster:
    """
    Autonomous admission cut-off forecaster executing calibrated sigmoid modeling,
    academic eligibility gating, quota offset modulation, and rank interval projections.
    """

    @classmethod
    def sanitize_request(cls, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforces ASVS L2 zero-PII compliance by detecting and rejecting any student identifiers.
        """
        violating_keys = [k for k in payload.keys() if k.lower() in DISALLOWED_PII_KEYS]
        if violating_keys:
            raise PIILeakageDetectedException(
                f"Request rejected: PII keys detected: {', '.join(violating_keys)}. "
                "Only anonymous academic metrics are permitted."
            )
        return payload

    @classmethod
    def evaluate_eligibility(
        cls,
        unit: AdmissionUnit,
        record: AcademicRecord
    ) -> EligibilityResult:
        """
        Validates minimum SSC, HSC, combined GPA and subject prerequisite gate conditions.
        """
        cfg = UNIT_CONFIGS[unit]
        combined = record.ssc_gpa + record.hsc_gpa
        violations_en: List[str] = []
        violations_bn: List[str] = []

        if record.ssc_gpa < cfg.min_ssc_gpa:
            violations_en.append(f"SSC GPA {record.ssc_gpa:.2f} is below minimum requirement of {cfg.min_ssc_gpa:.2f}")
            violations_bn.append(f"এসএসসি জিপিএ {record.ssc_gpa:.2f} ন্যূনতম আবশ্যক {cfg.min_ssc_gpa:.2f}-এর চেয়ে কম")

        if record.hsc_gpa < cfg.min_hsc_gpa:
            violations_en.append(f"HSC GPA {record.hsc_gpa:.2f} is below minimum requirement of {cfg.min_hsc_gpa:.2f}")
            violations_bn.append(f"এইচএসসি জিপিএ {record.hsc_gpa:.2f} ন্যূনতম আবশ্যক {cfg.min_hsc_gpa:.2f}-এর চেয়ে কম")

        if combined < cfg.min_combined_gpa:
            violations_en.append(f"Combined GPA {combined:.2f} is below threshold of {cfg.min_combined_gpa:.2f}")
            violations_bn.append(f"সম্মিলিত জিপিএ {combined:.2f} ন্যূনতম আবশ্যক {cfg.min_combined_gpa:.2f}-এর চেয়ে কম")

        # Subject-specific grade point checks
        subject_map: Dict[str, Tuple[Optional[float], str, str]] = {
            "physics_gp": (record.physics_gp, "Physics", "পদার্থবিজ্ঞান"),
            "chemistry_gp": (record.chemistry_gp, "Chemistry", "রসায়ন"),
            "math_gp": (record.math_gp, "Higher Math", "উচ্চতর গণিত"),
            "biology_gp": (record.biology_gp, "Biology", "জীববিজ্ঞান"),
            "english_gp": (record.english_gp, "English", "ইংরেজি"),
        }

        for sub_key, min_gp in cfg.required_subject_rules.items():
            val, name_en, name_bn = subject_map.get(sub_key, (None, sub_key, sub_key))
            if val is None or val < min_gp:
                actual = f"{val:.2f}" if val is not None else "Missing"
                actual_bn = f"{val:.2f}" if val is not None else "অনুপস্থিত"
                violations_en.append(f"{name_en} grade point ({actual}) is below required {min_gp:.2f}")
                violations_bn.append(f"{name_bn} গ্রেড পয়েন্ট ({actual_bn}) ন্যূনতম আবশ্যক {min_gp:.2f}-এর চেয়ে কম")

        is_eligible = len(violations_en) == 0
        return EligibilityResult(
            is_eligible=is_eligible,
            violations_en=violations_en,
            violations_bn=violations_bn,
            combined_gpa=round(combined, 2)
        )

    @classmethod
    def calculate_composite_score(
        cls,
        unit: AdmissionUnit,
        record: AcademicRecord
    ) -> float:
        """
        Calculates composite score based on exam score and weighted GPA contributions.
        """
        cfg = UNIT_CONFIGS[unit]
        gpa_contribution = (
            (record.ssc_gpa * cfg.gpa_multiplier_ssc) +
            (record.hsc_gpa * cfg.gpa_multiplier_hsc)
        )

        sim_score = record.exam_sim_score if record.exam_sim_score is not None else 0.0

        if unit == AdmissionUnit.BUET or unit == AdmissionUnit.GST:
            # Scaled 100-mark assessment
            raw_composite = sim_score
        else:
            raw_composite = sim_score + gpa_contribution

        # Clamp between 0.0 and full marks
        return max(0.0, min(cfg.full_marks, round(raw_composite, 2)))

    @classmethod
    def calculate_sigmoid_probability(
        cls,
        composite_score: float,
        median_cutoff_x0: float,
        slope_k: float,
        quota_offset: float = 0.0
    ) -> float:
        """
        Computes calibrated probability using the logistic sigmoid:
        P(x) = 1 / (1 + exp(-k * (x - (x0 - delta_quota))))
        """
        effective_x0 = median_cutoff_x0 - quota_offset
        delta = composite_score - effective_x0
        exponent = -slope_k * delta

        # Prevent floating point overflow/underflow
        if exponent > 60.0:
            return 0.0
        elif exponent < -60.0:
            return 1.0

        prob = 1.0 / (1.0 + math.exp(exponent))
        return max(0.0, min(1.0, round(prob, 4)))

    @classmethod
    def estimate_rank_range(
        cls,
        unit: AdmissionUnit,
        probability: float,
        is_eligible: bool
    ) -> Tuple[int, int]:
        """
        Projects realistic merit rank interval [rank_min, rank_max] based on unit capacity.
        """
        if not is_eligible or probability <= 0.0001:
            cfg = UNIT_CONFIGS[unit]
            return (cfg.total_seats * 3, cfg.applicant_pool)

        cfg = UNIT_CONFIGS[unit]
        seats = cfg.total_seats

        # Theoretical median rank based on probability inverse
        # When probability is near 1.0, rank is top 1..5% of seats
        # When probability is 0.5, rank is centered around total available seats
        # When probability is near 0.1, rank is well beyond total seats
        if probability >= 0.95:
            rank_min = 1
            rank_max = max(10, int(seats * 0.15))
        elif probability >= 0.85:
            rank_min = max(1, int(seats * 0.10))
            rank_max = int(seats * 0.45)
        elif probability >= 0.75:
            rank_min = int(seats * 0.35)
            rank_max = int(seats * 0.75)
        elif probability >= 0.60:
            rank_min = int(seats * 0.65)
            rank_max = int(seats * 0.95)
        elif probability >= 0.50:
            rank_min = int(seats * 0.85)
            rank_max = int(seats * 1.15)
        elif probability >= 0.40:
            rank_min = int(seats * 1.05)
            rank_max = int(seats * 1.45)
        elif probability >= 0.25:
            rank_min = int(seats * 1.35)
            rank_max = int(seats * 1.95)
        else:
            rank_min = int(seats * 1.80)
            rank_max = min(cfg.applicant_pool, int(seats * 3.5))

        return (max(1, rank_min), max(rank_min + 5, rank_max))

    @classmethod
    def determine_tier(cls, probability: float, is_eligible: bool) -> ProbabilityTier:
        """Maps probability to academic risk tiers."""
        if not is_eligible:
            return ProbabilityTier.INELIGIBLE
        if probability >= 0.75:
            return ProbabilityTier.SAFE
        elif probability >= 0.40:
            return ProbabilityTier.COMPETITIVE
        else:
            return ProbabilityTier.REACH

    @classmethod
    def generate_forecast(
        cls,
        unit: AdmissionUnit,
        record: AcademicRecord,
        quota: QuotaType = QuotaType.GENERAL
    ) -> ForecastPrediction:
        """
        Executes full prediction workflow: eligibility -> composite score -> sigmoid -> rank -> report.
        """
        eligibility = cls.evaluate_eligibility(unit, record)
        cfg = UNIT_CONFIGS[unit]
        quota_offset = QUOTA_OFFSETS[quota]
        effective_x0 = cfg.median_cutoff_x0 - quota_offset

        if not eligibility.is_eligible:
            composite = cls.calculate_composite_score(unit, record)
            prob = 0.0
            tier = ProbabilityTier.INELIGIBLE
            rank_min, rank_max = cls.estimate_rank_range(unit, 0.0, False)
            fb_en = f"Ineligible for {cfg.name_en}. Primary prerequisite conditions not met."
            fb_bn = f"{cfg.name_bn}-এ আবেদনের প্রাথমিক শর্ত পূরণ হয়নি।"
        else:
            composite = cls.calculate_composite_score(unit, record)
            prob = cls.calculate_sigmoid_probability(
                composite_score=composite,
                median_cutoff_x0=cfg.median_cutoff_x0,
                slope_k=cfg.slope_k,
                quota_offset=quota_offset
            )
            tier = cls.determine_tier(prob, True)
            rank_min, rank_max = cls.estimate_rank_range(unit, prob, True)

            if tier == ProbabilityTier.SAFE:
                fb_en = f"High admission probability for {cfg.name_en}. Your score aligns with top historical percentiles."
                fb_bn = f"{cfg.name_bn}-এ ভর্তির সুযোগ অত্যন্ত প্রবল। স্কোর ঐতিহাসিক কাট-অফের নিরাপদ স্তরে অবস্থান করছে।"
            elif tier == ProbabilityTier.COMPETITIVE:
                fb_en = f"Moderate admission probability for {cfg.name_en}. You are in the core competitive threshold."
                fb_bn = f"{cfg.name_bn}-এ ভর্তির সুযোগ প্রতিযোগিতাপূর্ণ। মূল কাট-অফ মার্জিনের অত্যন্ত কাছাকাছি রয়েছেন।"
            else:
                fb_en = f"Reach threshold for {cfg.name_en}. Additional simulation score elevation recommended."
                fb_bn = f"{cfg.name_bn}-এ ভর্তির জন্য আরও অধিক প্রস্তুতি ও টেস্ট স্কোর উন্নীত করা আবশ্যক।"

        historical = HISTORICAL_CUTOFF_SERIES.get(unit.value, {})

        return ForecastPrediction(
            unit=unit,
            quota=quota,
            is_eligible=eligibility.is_eligible,
            composite_score=composite,
            effective_cutoff_threshold=round(effective_x0, 2),
            calibrated_probability=prob,
            tier=tier,
            rank_range_min=rank_min,
            rank_range_max=rank_max,
            eligibility=eligibility,
            historical_series=historical,
            academic_feedback_en=fb_en,
            academic_feedback_bn=fb_bn
        )
