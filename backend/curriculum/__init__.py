"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Bilingual Curriculum Engine & NCTB Terminology Lexicon
 * TOPIC:     Phase 136 Instant Medium Switcher & Contextual Academic Terminology
 * FILE:      backend/curriculum/__init__.py
 * PHASE:     Phase 136 - Dual-Curriculum Bilingual Terminology Switcher
 * PURPOSE:   Exposes NCTB curriculum terminology index models, medium enums,
 *            and the dual-curriculum exam question auto-localization service.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Pure Academic Design, NCTB Aligned
 */
"""

from .lexicon_service import (
    AcademicMedium,
    CurriculumSubject,
    GradeTier,
    NCTBLexiconEntry,
    BilingualQuestionItem,
    NCTBLexiconService,
    BENCHMARK_NCTB_LEXICON,
    BENCHMARK_BILINGUAL_QUESTIONS,
)

__all__ = [
    "AcademicMedium",
    "CurriculumSubject",
    "GradeTier",
    "NCTBLexiconEntry",
    "BilingualQuestionItem",
    "NCTBLexiconService",
    "BENCHMARK_NCTB_LEXICON",
    "BENCHMARK_BILINGUAL_QUESTIONS",
]
