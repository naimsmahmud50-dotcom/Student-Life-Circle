"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Multi-Dialect Audio Tutoring & Voice Viva Evaluator
 * TOPIC:     Phase 129 Acoustic Dialect Adaptation & Viva-Voce Rubric Engine
 * FILE:      backend/audio/__init__.py
 * PHASE:     Phase 129 - Multi-Dialect Regional Audio Tutoring
 * PURPOSE:   Exports the multi-dialect viva evaluator engine, rubrics, and normalizer.
 * STANDARDS: Zero-Emoji, Pure Academic Design, Privacy By Design, ASVS L2
 */
"""

from backend.audio.viva_evaluator import (
    VivaEvaluator,
    DialectType,
    DialectNormalizer,
    VivaRubricEngine,
    AcousticTelemetry,
    OralQuestion,
    VivaEvaluationResult,
    EphemeralAudioBuffer,
    AudioBufferExpiredException,
)

__all__ = [
    "VivaEvaluator",
    "DialectType",
    "DialectNormalizer",
    "VivaRubricEngine",
    "AcousticTelemetry",
    "OralQuestion",
    "VivaEvaluationResult",
    "EphemeralAudioBuffer",
    "AudioBufferExpiredException",
]
