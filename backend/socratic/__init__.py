"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic Math & Science Whiteboard Solver
 * TOPIC:     Phase 132 Interactive Canvas & Pedagogical Socratic Step Guidance
 * FILE:      backend/socratic/__init__.py
 * PHASE:     Phase 132 - Real-time Socratic AI Whiteboard Solver
 * PURPOSE:   Exposes the Socratic solver domain models, pedagogical hint guard,
 *            misconception detector, and whiteboard stroke buffer.
 * STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Pedagogical Hint Guard
 */
"""

from .whiteboard_solver import (
    ProblemDomain,
    HintLevel,
    DrawingToolType,
    Point2D,
    DrawingStroke,
    SocraticStep,
    SocraticProblemSession,
    PedagogicalHintGuard,
    DirectAnswerLeakedException,
    InvalidStrokeCoordinateException,
    MisconceptionDetector,
    DrawingStrokeBuffer,
    SocraticWhiteboardSolver,
)

__all__ = [
    "ProblemDomain",
    "HintLevel",
    "DrawingToolType",
    "Point2D",
    "DrawingStroke",
    "SocraticStep",
    "SocraticProblemSession",
    "PedagogicalHintGuard",
    "DirectAnswerLeakedException",
    "InvalidStrokeCoordinateException",
    "MisconceptionDetector",
    "DrawingStrokeBuffer",
    "SocraticWhiteboardSolver",
]
