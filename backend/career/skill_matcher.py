"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Career Skill-to-Job Matching Radar & Recruiter Pipeline
 * TOPIC:     Phase 134 Multi-Dimensional Competency Radar & Sealed CV Applications
 * FILE:      backend/career/skill_matcher.py
 * PHASE:     Phase 134 - Algorithmic Skill-to-Job Matching Radar
 * PURPOSE:   Provides multi-dimensional competency radar calculation, vector
 *            cosine similarity job matching, and immutable sealed CV snapshots.
 * STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Immutable CV Snapshots
 */
"""

import hashlib
import json
import math
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class RadarDimension(str, Enum):
    MATHEMATICS = "MATHEMATICS"
    ALGORITHMS = "ALGORITHMS"
    OLYMPIADS = "OLYMPIADS"
    COMMUNICATION = "COMMUNICATION"
    SYSTEMS = "SYSTEMS"


class InvalidRadarScoreException(ValueError):
    """Raised when a competency score is outside the valid 0.0 to 100.0 boundary."""
    pass


class TamperedCVSnapshotException(ValueError):
    """Raised when a sealed CV application fails cryptographic SHA-256 verification."""
    pass


@dataclass
class CompetencyRadar:
    """Normalized multi-dimensional skill radar representing student capability."""
    student_id: str
    mathematics: float
    algorithms: float
    olympiads: float
    communication: float
    systems: float
    computed_at: float = field(default_factory=time.time)

    def __post_init__(self):
        for dim, val in [
            ("mathematics", self.mathematics),
            ("algorithms", self.algorithms),
            ("olympiads", self.olympiads),
            ("communication", self.communication),
            ("systems", self.systems),
        ]:
            if not math.isfinite(val) or val < 0.0 or val > 100.0:
                raise InvalidRadarScoreException(
                    f"Score for {dim} ({val}) is invalid. Must be finite float in [0.0, 100.0]."
                )

    def to_vector(self) -> List[float]:
        return [
            self.mathematics,
            self.algorithms,
            self.olympiads,
            self.communication,
            self.systems,
        ]

    def overall_score(self) -> float:
        vec = self.to_vector()
        return sum(vec) / len(vec)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "student_id": self.student_id,
            "mathematics": round(self.mathematics, 1),
            "algorithms": round(self.algorithms, 1),
            "olympiads": round(self.olympiads, 1),
            "communication": round(self.communication, 1),
            "systems": round(self.systems, 1),
            "overall_score": round(self.overall_score(), 1),
            "computed_at": self.computed_at,
        }


@dataclass
class JobPosting:
    """Corporate or Startup vacancy benchmarked against competency dimensions."""
    job_id: str
    title_en: str
    title_bn: str
    company_name: str
    location: str
    required_radar: CompetencyRadar
    salary_range_bdt: str
    job_type: str
    is_active: bool = True
    tags: List[str] = field(default_factory=list)


@dataclass
class JobMatchResult:
    """Matching calculation output comparing student radar with job requirement."""
    job: JobPosting
    match_percentage: float
    cosine_similarity: float
    strengths: List[str]
    gap_dimensions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job.job_id,
            "title_en": self.job.title_en,
            "title_bn": self.job.title_bn,
            "company_name": self.job.company_name,
            "location": self.job.location,
            "salary_range_bdt": self.job.salary_range_bdt,
            "job_type": self.job.job_type,
            "match_percentage": round(self.match_percentage, 1),
            "cosine_similarity": round(self.cosine_similarity, 4),
            "strengths": self.strengths,
            "gap_dimensions": self.gap_dimensions,
            "required_radar": self.job.required_radar.to_dict(),
        }


@dataclass
class SealedCVSnapshot:
    """Immutable point-in-time cryptographic application record anchored by SHA-256."""
    snapshot_id: str
    student_id: str
    job_id: str
    full_name: str
    institution: str
    verified_gpa: float
    olympiad_achievements: List[str]
    radar_snapshot: Dict[str, float]
    applied_at: float
    snapshot_hash: str = ""

    def compute_canonical_hash(self) -> str:
        payload = {
            "snapshot_id": self.snapshot_id,
            "student_id": self.student_id,
            "job_id": self.job_id,
            "full_name": self.full_name,
            "institution": self.institution,
            "verified_gpa": f"{self.verified_gpa:.2f}",
            "olympiad_achievements": sorted(self.olympiad_achievements),
            "radar_snapshot": {k: f"{v:.1f}" for k, v in sorted(self.radar_snapshot.items())},
            "applied_at": f"{self.applied_at:.4f}",
        }
        canonical_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        return hashlib.sha256(canonical_bytes).hexdigest()

    def verify_integrity(self) -> bool:
        expected = self.compute_canonical_hash()
        return self.snapshot_hash == expected


class CompetencyRadarEngine:
    """
    Computes multi-dimensional radar scores and vector cosine similarity.
    """

    @classmethod
    def calculate_cosine_similarity(cls, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Computes cosine similarity between two 5-dimensional vectors.
        Returns value in [0.0, 1.0].
        """
        if len(vec_a) != len(vec_b):
            raise ValueError(f"Vector dimension mismatch: {len(vec_a)} vs {len(vec_b)}")

        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0

        similarity = dot_product / (norm_a * norm_b)
        # Numerical clamping
        return max(0.0, min(1.0, similarity))

    @classmethod
    def match_candidate_to_job(
        cls,
        candidate_radar: CompetencyRadar,
        job: JobPosting
    ) -> JobMatchResult:
        """
        Calculates match percentage and identifies relative strengths and competency gaps.
        """
        c_vec = candidate_radar.to_vector()
        j_vec = job.required_radar.to_vector()

        cosine_sim = cls.calculate_cosine_similarity(c_vec, j_vec)

        # Scale similarity adjusted for magnitude fulfillment
        # Ratio of candidate overall to required overall
        c_overall = candidate_radar.overall_score()
        j_overall = job.required_radar.overall_score()
        magnitude_ratio = min(1.0, c_overall / j_overall) if j_overall > 0 else 1.0

        # Weighted match percentage
        match_pct = (cosine_sim * 0.6 + magnitude_ratio * 0.4) * 100.0
        match_pct = max(0.0, min(100.0, match_pct))

        # Dimensions comparison
        dimensions = ["গণিত ও বিশ্লেষণ", "অ্যালগরিদম ও কোডিং", "অলিম্পিয়াড সমস্যা সমাধান", "যোগাযোগ ও ভাষা", "সিস্টেম আর্কিটেকচার"]
        strengths = []
        gaps = []

        for name, c_val, j_val in zip(dimensions, c_vec, j_vec):
            if c_val >= j_val:
                strengths.append(name)
            elif (j_val - c_val) >= 15.0:
                gaps.append(f"{name} (ঘাটতি: {int(j_val - c_val)} পয়েন্ট)")

        return JobMatchResult(
            job=job,
            match_percentage=match_pct,
            cosine_similarity=cosine_sim,
            strengths=strengths,
            gap_dimensions=gaps,
        )


class SkillMatchingService:
    """
    Central service maintaining job vacancies, matching candidate radars, and creating sealed CVs.
    """

    BENCHMARK_JOBS: List[JobPosting] = [
        JobPosting(
            job_id="job_quant_01",
            title_en="Quantitative Financial Analyst",
            title_bn="কোয়ান্টিটেটিভ ফিন্যান্সিয়াল অ্যানালিস্ট",
            company_name="BRAC Bank & Institutional Capital",
            location="Dhaka (Gulshan)",
            required_radar=CompetencyRadar(
                student_id="req_quant",
                mathematics=92.0,
                algorithms=85.0,
                olympiads=88.0,
                communication=75.0,
                systems=70.0
            ),
            salary_range_bdt="৳৭০,০০০ - ৳১,২০,০০০",
            job_type="Full-time",
            tags=["Mathematics", "Stochastic Calculus", "Python", "Algorithmic Trading"]
        ),
        JobPosting(
            job_id="job_ml_02",
            title_en="Junior Machine Learning Engineer",
            title_bn="জুনিয়র মেশিন লার্নিং ইঞ্জিনিয়ার",
            company_name="Brain Station 23 / Silicon Valley Hub",
            location="Dhaka (Mohakhali)",
            required_radar=CompetencyRadar(
                student_id="req_ml",
                mathematics=88.0,
                algorithms=90.0,
                olympiads=85.0,
                communication=80.0,
                systems=82.0
            ),
            salary_range_bdt="৳৬৫,০০০ - ৳১,০০,০০০",
            job_type="Full-time",
            tags=["Deep Learning", "Linear Algebra", "PyTorch", "Algorithms"]
        ),
        JobPosting(
            job_id="job_systems_03",
            title_en="Systems Software & Distributed Architect",
            title_bn="সিস্টেমস সফটওয়্যার ও ডিস্ট্রিবিউটেড ইঞ্জিনিয়ার",
            company_name="TigerIT & Digital Infrastructure Ltd",
            location="Dhaka (Banani)",
            required_radar=CompetencyRadar(
                student_id="req_systems",
                mathematics=80.0,
                algorithms=94.0,
                olympiads=82.0,
                communication=70.0,
                systems=95.0
            ),
            salary_range_bdt="৳৮০,০০০ - ৳১,৫০,০০০",
            job_type="Full-time",
            tags=["C/C++", "Distributed Systems", "OS Architecture", "High Throughput"]
        ),
        JobPosting(
            job_id="job_stem_intern_04",
            title_en="STEM Olympiad Research Fellow",
            title_bn="স্টেম অলিম্পিয়াড রিসার্চ ফেলো",
            company_name="Bangladesh Mathematical Society (BMS)",
            location="Dhaka (Dhaka University Campus)",
            required_radar=CompetencyRadar(
                student_id="req_fellow",
                mathematics=95.0,
                algorithms=75.0,
                olympiads=95.0,
                communication=85.0,
                systems=60.0
            ),
            salary_range_bdt="৳৪০,০০০ - ৳৬০,০০০",
            job_type="Research Fellow",
            tags=["Pure Math", "Combinatorics", "Geometry", "Curriculum Mentoring"]
        ),
    ]

    def __init__(self):
        # job_id -> JobPosting
        self._jobs: Dict[str, JobPosting] = {j.job_id: j for j in self.BENCHMARK_JOBS}
        # snapshot_id -> SealedCVSnapshot
        self._sealed_applications: Dict[str, SealedCVSnapshot] = {}

    def get_job(self, job_id: str) -> JobPosting:
        job = self._jobs.get(job_id)
        if not job:
            raise KeyError(f"Job posting '{job_id}' not found.")
        return job

    def match_all_jobs(self, candidate_radar: CompetencyRadar) -> List[JobMatchResult]:
        """
        Ranks all active jobs by match percentage descending for the candidate.
        """
        results = []
        for job in self._jobs.values():
            if job.is_active:
                match = CompetencyRadarEngine.match_candidate_to_job(candidate_radar, job)
                results.append(match)

        # Sort descending by match percentage
        results.sort(key=lambda m: m.match_percentage, reverse=True)
        return results

    def submit_sealed_cv_application(
        self,
        student_id: str,
        job_id: str,
        full_name: str,
        institution: str,
        verified_gpa: float,
        olympiad_achievements: List[str],
        radar: CompetencyRadar
    ) -> SealedCVSnapshot:
        """
        Generates an immutable, point-in-time SHA-256 sealed CV application.
        """
        job = self.get_job(job_id)
        snapshot_id = f"cv_{uuid.uuid4().hex[:12]}"
        now = time.time()

        snapshot = SealedCVSnapshot(
            snapshot_id=snapshot_id,
            student_id=student_id,
            job_id=job.job_id,
            full_name=full_name,
            institution=institution,
            verified_gpa=verified_gpa,
            olympiad_achievements=olympiad_achievements,
            radar_snapshot={
                "mathematics": radar.mathematics,
                "algorithms": radar.algorithms,
                "olympiads": radar.olympiads,
                "communication": radar.communication,
                "systems": radar.systems,
            },
            applied_at=now,
        )
        snapshot.snapshot_hash = snapshot.compute_canonical_hash()

        self._sealed_applications[snapshot_id] = snapshot
        return snapshot

    def verify_sealed_cv(self, snapshot_id: str) -> Tuple[bool, Optional[SealedCVSnapshot]]:
        """
        Verifies mathematical provenance and tamper-proofing of sealed CV.
        """
        snapshot = self._sealed_applications.get(snapshot_id)
        if not snapshot:
            return False, None
        return snapshot.verify_integrity(), snapshot
