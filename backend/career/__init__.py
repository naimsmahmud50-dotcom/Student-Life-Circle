"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Career Skill-to-Job Matching Radar & Recruiter Pipeline
 * TOPIC:     Phase 134 Multi-Dimensional Competency Radar & Sealed CV Applications
 * FILE:      backend/career/__init__.py
 * PHASE:     Phase 134 - Algorithmic Skill-to-Job Matching Radar
 * PURPOSE:   Exposes the multi-dimensional skill radar models, vector cosine
 *            matching algorithm, and sealed CV snapshot services.
 * STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Immutable CV Snapshots
 */
"""

from .skill_matcher import (
    RadarDimension,
    CompetencyRadar,
    JobPosting,
    JobMatchResult,
    SealedCVSnapshot,
    CompetencyRadarEngine,
    SkillMatchingService,
    InvalidRadarScoreException,
    TamperedCVSnapshotException,
)

__all__ = [
    "RadarDimension",
    "CompetencyRadar",
    "JobPosting",
    "JobMatchResult",
    "SealedCVSnapshot",
    "CompetencyRadarEngine",
    "SkillMatchingService",
    "InvalidRadarScoreException",
    "TamperedCVSnapshotException",
]
