"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Adaptive Neurodivergent Accessibility & Cognitive Eye-Pacing Reader Tower
FILE:      backend/app/schemas/neurodivergent_accessibility_schema.py
PURPOSE:   Pydantic v2 data models, DTOs, and validation contracts for:
           1. Bionic reading transformation with saccadic fixation anchor calculation.
           2. Multi-syllabic academic vocabulary deconstruction for dyslexic learners.
           3. Cognitive eye-pacing reader telemetry (Words-Per-Minute and dwell times).
           4. WCAG 2.2 Level AAA relative luminance and contrast ratio verification.
           5. Sensory contrast and color temperature tint presets for neuro-inclusivity.
STANDARDS: Pydantic v2 strict typing, WCAG 2.2 AAA (7:1 contrast), RFC 3339 timestamps.
========================================================================================
"""

from enum import Enum
from typing import List, Dict, Optional, Any

try:
    from pydantic import BaseModel, Field, ConfigDict
except ImportError:
    class BaseModel:  # type: ignore
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def dict(self):
            return self.__dict__
        def model_copy(self, **kwargs):
            d = dict(self.__dict__)
            d.update(kwargs)
            return self.__class__(**d)
    def Field(default=None, **kwargs):
        return default
    def ConfigDict(**kwargs):
        return {}


class ReadingAssistanceModeEnum(str, Enum):
    """Visual assistance modes for neurodivergent and dyslexic readers."""
    STANDARD = "STANDARD"
    BIONIC_FIXATION = "BIONIC_FIXATION"
    DYSLEXIA_WEIGHTED = "DYSLEXIA_WEIGHTED"
    SYLLABLE_DECOMPOSED = "SYLLABLE_DECOMPOSED"
    HIGH_CONTRAST_TINT = "HIGH_CONTRAST_TINT"


class ColorContrastPresetEnum(str, Enum):
    """Scientifically validated sensory color temperature profiles."""
    DEFAULT_DARK = "DEFAULT_DARK"
    WARM_AMBER_SEPIA = "WARM_AMBER_SEPIA"
    CALM_SLATE_CYAN = "CALM_SLATE_CYAN"
    SOLARIZED_YELLOW_BLACK = "SOLARIZED_YELLOW_BLACK"
    HIGH_CONTRAST_MONOCHROME = "HIGH_CONTRAST_MONOCHROME"


class BionicWordSegmentDTO(BaseModel):
    """Represents a single word decomposed into fixation anchor and trailing characters."""
    original_word: str
    fixation_anchor: str
    trailing_chars: str
    bold_length: int
    total_length: int


class BionicReadingTransformRequest(BaseModel):
    """Request to transform plain academic passage into bionic saccadic reading format."""
    text: str = Field(..., description="Plain academic passage or question stem")
    fixation_intensity: float = Field(default=0.5, ge=0.2, le=0.8, description="Proportion of word to bold")
    mode: ReadingAssistanceModeEnum = Field(default=ReadingAssistanceModeEnum.BIONIC_FIXATION)


class BionicReadingTransformResponse(BaseModel):
    """Response containing structured word segments and pre-rendered HTML format."""
    original_text: str
    html_formatted_text: str
    total_words: int
    average_fixation_chars: float
    estimated_reading_time_seconds: float
    mode: ReadingAssistanceModeEnum


class SyllableDecomposeRequest(BaseModel):
    """Request to deconstruct academic vocabulary into pronounceable syllables."""
    term: str = Field(..., description="Academic term to decompose (e.g. Photosynthesis, Electromagnetism)")
    language: str = Field(default="en")


class SyllableDecomposeResponse(BaseModel):
    """Decomposed syllable syllables with hyphenation and phonetic guide."""
    term: str
    syllables: List[str]
    hyphenated_term: str
    syllable_count: int
    stress_index: int
    phonetic_guide: str


class CognitivePacerConfigDTO(BaseModel):
    """Configuration for guided eye-pacing reader."""
    words_per_minute: int = Field(default=220, ge=80, le=600)
    chunk_size_words: int = Field(default=1, ge=1, le=5)
    pause_on_punctuation_ms: int = Field(default=150)
    line_spacing_multiplier: float = Field(default=1.8)


class CognitivePacerTelemetryDTO(BaseModel):
    """Calculated intervals and duration for cognitive pacer reader."""
    target_wpm: int
    interval_per_word_ms: float
    total_words: int
    total_duration_seconds: float
    saccadic_jump_arcs: int


class AccessibilityAuditMetricsDTO(BaseModel):
    """WCAG 2.2 AAA contrast and luminance evaluation results."""
    foreground_hex: str
    background_hex: str
    contrast_ratio: float
    wcag_aa_passed: bool
    wcag_aaa_passed: bool
    relative_luminance_fg: float
    relative_luminance_bg: float
    recommended_preset: ColorContrastPresetEnum


class AccessibilityStatusDTO(BaseModel):
    """Overall operational telemetry of the neurodivergent accessibility engine."""
    operational: bool
    supported_modes: List[str]
    supported_presets: List[str]
    total_bionic_transforms_served: int
    wcag_aaa_compliance_score: float
    active_dyslexia_profiles: int
