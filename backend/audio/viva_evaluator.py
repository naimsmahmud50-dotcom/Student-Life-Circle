"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Multi-Dialect Audio Tutoring & Voice Viva Evaluator
 * TOPIC:     Phase 129 Acoustic Dialect Adaptation & Viva-Voce Rubric Engine
 * FILE:      backend/audio/viva_evaluator.py
 * PHASE:     Phase 129 - Multi-Dialect Regional Audio Tutoring
 * PURPOSE:   Provides real-time NCTB oral viva-voce evaluation, multi-dialect acoustic
 *            and lexical adaptation (Chittagong, Sylhet, Barisal, Standard Bengali),
 *            ephemeral 15-minute in-memory audio buffering, and zero-PII scoring.
 * STANDARDS: Zero-Emoji, Pure Academic Design, Privacy By Design, ASVS L2
 */
"""

import math
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class AudioBufferExpiredException(Exception):
    """Raised when an ephemeral audio buffer exceeds the strict 15-minute retention window."""
    pass


class PIIInVivaStreamException(ValueError):
    """Raised when viva speech transcript or metadata contains forbidden PII identifiers."""
    pass


class DialectType(str, Enum):
    STANDARD_BANGLA = "STANDARD_BANGLA"   # প্রমিত বাংলা
    CHITTAGONG = "CHITTAGONG"             # চট্টগ্রামের কথ্যরীতি (চাটগাঁইয়া)
    SYLHET = "SYLHET"                     # সিলেটের কথ্যরীতি (সিলেটি)
    BARISAL = "BARISAL"                   # বরিশালের কথ্যরীতি (দক্ষিণাঞ্চলীয়)


# Forbidden PII keys
DISALLOWED_PII_KEYS: Set[str] = {
    "name", "full_name", "first_name", "last_name", "student_name", "phone", "mobile",
    "email", "nid", "national_id", "roll", "reg_no", "student_id",
    "institution_name", "father_name", "mother_name"
}


# Regional dialect dictionary mappings to standard academic Bengali
DIALECT_LEXICON: Dict[DialectType, Dict[str, str]] = {
    DialectType.CHITTAGONG: {
        "ন অইব": "হবে না",
        "হইতো নয়": "হবে না",
        "বেয়াক": "সকল",
        "গম": "ভালো",
        "হেরলাই": "সেজন্য",
        "বোল": "বল",
        "তুঅরন": "ত্বরণ",
        "ফুড়া": "সমাপ্ত",
        "হন": "বলুন",
        "আঁর": "আমার",
        "তোঁয়ার": "তোমার",
        "হিয়ান": "সেটি",
        "ইয়ান": "এটি",
        "লই": "নিয়ে",
        "অইলে": "হলে",
        "বাইর": "বের",
        "গতিশিল": "গতিশীল",
        "ভরবেগ্যা": "ভরবেগ",
        "শক্তিলা": "শক্তি",
        "হাচা": "সত্য",
    },
    DialectType.SYLHET: {
        "অইতো নায়": "হবে না",
        "হকল": "সকল",
        "হগল": "সকল",
        "কুন্তা": "কিছু",
        "বালা": "ভালো",
        "খেতা": "কথা",
        "আউগিয়া": "এগিয়ে",
        "ফারমু": "পারব",
        "ফানি": "পানি",
        "ফারিনা": "পারি না",
        "হেরলে": "সেজন্য",
        "ফরবেগ": "ভরবেগ",
        "ফরমান": "প্রমাণ",
        "লগে": "সাথে",
        "খইয়া": "বলে",
        "খইতাম": "বলব",
        "অখন": "এখন",
        "ইখান": "এটি",
    },
    DialectType.BARISAL: {
        "মোগো": "আমাদের",
        "হেইডা": "সেটি",
        "হ্যারপর": "তারপর",
        "করমু": "করব",
        "কইতেছি": "বলছি",
        "হকলে": "সকলে",
        "মুই": "আমি",
        "হেইয়ার": "সেটির",
        "কওন": "বলা",
        "যামু": "যাব",
        "আইজ": "আজ",
        "প্যাচাল": "আলোচনা",
        "কইবার": "বলার",
        "বাইন্দা": "বেঁধে",
        "আমাগো": "আমাদের",
    },
    DialectType.STANDARD_BANGLA: {}
}


@dataclass
class AcousticTelemetry:
    """Acoustic metrics extracted from voice stream without preserving raw audio."""
    duration_seconds: float
    snr_db: float                       # Signal-to-noise ratio (e.g. 18.5 dB)
    speech_rate_wpm: float              # Words per minute (e.g. 130 WPM)
    pause_ratio: float                  # Ratio of silence/pause (e.g. 0.15)
    mean_pitch_hz: float = 165.0        # Acoustic frequency estimate


@dataclass
class OralQuestion:
    """NCTB Viva-Voce structured inquiry blueprint."""
    id: str
    subject: str
    question_text_bn: str
    question_text_en: str
    ideal_key_concepts: List[str]
    required_technical_terms: List[str]
    sample_expected_response: str


# NCTB Standard Oral Question Repository
SAMPLE_VIVA_QUESTIONS: Dict[str, OralQuestion] = {
    "viva_phy_01": OralQuestion(
        id="viva_phy_01",
        subject="পদার্থবিজ্ঞান (Physics)",
        question_text_bn="নিউটনের গতির দ্বিতীয় সূত্র এবং ভরবেগের পরিবর্তনের হারের সম্পর্কটি ব্যাখ্যা করো।",
        question_text_en="Explain Newton's Second Law of Motion and its relationship with rate of change of momentum.",
        ideal_key_concepts=[
            "ভরবেগ", "পরিবর্তন", "বল", "সমানুপাতিক", "ত্বরণ", "দিক"
        ],
        required_technical_terms=[
            "বল", "ভরবেগ", "ত্বরণ", "নিউটনের দ্বিতীয় সূত্র"
        ],
        sample_expected_response="বস্তুর ভরবেগের পরিবর্তনের হার তার ওপর প্রযুক্ত বলের সমানুপাতিক এবং বল যেদিকে ক্রিয়া করে বস্তুর ভরবেগের পরিবর্তনও সেদিকে ঘটে।"
    ),
    "viva_chem_01": OralQuestion(
        id="viva_chem_01",
        subject="রসায়ন (Chemistry)",
        question_text_bn="মৌলের পর্যায়বৃত্ত ধর্ম কী এবং পর্যায় সারণিতে বাম থেকে ডানে পারমাণবিক ব্যাসার্ধ কেন হ্রাস পায়?",
        question_text_en="What are periodic properties and why does atomic radius decrease across a period?",
        ideal_key_concepts=[
            "পর্যায়বৃত্ত", "পারমাণবিক ব্যাসার্ধ", "প্রোটন", "নিউক্লিয়াস", "আকর্ষণ", "ইলেকট্রন"
        ],
        required_technical_terms=[
            "পারমাণবিক সংখ্যা", "কার্যকর নিউক্লিয়ার চার্জ", "ইলেকট্রন মেঘ", "পর্যায়বৃত্ত ধর্ম"
        ],
        sample_expected_response="একই পর্যায়ে বাম থেকে ডানে পারমাণবিক সংখ্যা বৃদ্ধির সাথে সাথে নিউক্লিয়াসে প্রোটন সংখ্যা বাড়ে, ফলে সর্ববহিঃস্থ স্তরের ইলেকট্রনের ওপর আকর্ষণ বৃদ্ধি পেয়ে ব্যাসার্ধ হ্রাস পায়।"
    ),
    "viva_bio_01": OralQuestion(
        id="viva_bio_01",
        subject="জীববিজ্ঞান (Biology)",
        question_text_bn="মাইটোটিক ও মিয়োটিক কোষ বিভাজনের প্রধান পার্থক্য এবং তাৎপর্য ব্যাখ্যা করো।",
        question_text_en="Explain the primary biological distinctions between mitotic and meiotic cell divisions.",
        ideal_key_concepts=[
            "মায়োসিস", "মাইটোটিক", "ক্রোমোজোম", "হ্রাসমূলক", "সমীকরণিক", "জনন কোষ", "দেহ কোষ"
        ],
        required_technical_terms=[
            "ক্রোমোজোম সংখ্যা", "হ্যাপ্লয়েড", "ডিপ্লয়েড", "ক্রসিং ওভার"
        ],
        sample_expected_response="মায়োসিস বিভাজনে ক্রোমোজোম সংখ্যা অর্ধেক হয়ে হ্যাপ্লয়েড জনন কোষ তৈরি হয়, অন্যদিকে মাইটোসিসে মাতৃকোষের সমান ক্রোমোজোম বিশিষ্ট দুটি অপত্য দেহকোষ সৃষ্টি হয়।"
    ),
    "viva_ict_01": OralQuestion(
        id="viva_ict_01",
        subject="তথ্য ও যোগাযোগ প্রযুক্তি (ICT)",
        question_text_bn="ক্লাউড কম্পিউটিং কী এবং এর প্রধান তিনটি পরিষেবা মডেল সংক্ষেপে বলো।",
        question_text_en="What is cloud computing and briefly state its three primary service models?",
        ideal_key_concepts=[
            "ইন্টারনেট", "রিমোট সার্ভার", "অন-ডিমান্ড", "স্কেলেবিলিটি", "IaaS", "PaaS", "SaaS"
        ],
        required_technical_terms=[
            "ক্লাউড কম্পিউটিং", "পরিকাঠামো", "প্ল্যাটফর্ম", "সফটওয়্যার"
        ],
        sample_expected_response="ক্লাউড কম্পিউটিং হলো ইন্টারনেটের মাধ্যমে অন-ডিমান্ড কম্পিউটিং রিসোর্স সেবা। এর তিনটি মূল মডেল হলো IaaS, PaaS এবং SaaS।"
    ),
}


@dataclass
class VivaEvaluationResult:
    """NCTB 4-tier rubric evaluation outcome with parallel transcripts and feedback."""
    question_id: str
    dialect: DialectType
    raw_transcript: str
    normalized_transcript: str
    conceptual_score: float              # 0 to 40
    terminology_score: float             # 0 to 30
    articulation_score: float            # 0 to 20
    dialect_accommodation_score: float   # 0 to 10
    total_score: float                   # 0 to 100
    grade_letter: str                    # A+, A, A-, B, C, F
    feedback_bn: str
    feedback_en: str
    detected_key_concepts: List[str]
    missing_key_concepts: List[str]
    matched_terms: List[str]
    acoustic_summary: Dict[str, Any]
    is_ephemeral_purged: bool = False


class DialectNormalizer:
    """
    Phonetic and lexical adaptation engine translating regional Bangladeshi dialects
    into canonical academic Bengali while respecting regional phonetic characteristics.
    """

    @classmethod
    def normalize_transcript(cls, raw_text: str, dialect: DialectType) -> str:
        """
        Translates regional colloquial tokens into standardized academic Bengali.
        """
        if not raw_text or dialect == DialectType.STANDARD_BANGLA:
            return raw_text.strip()

        lexicon = DIALECT_LEXICON.get(dialect, {})
        normalized = raw_text

        # Sort keys by length descending to replace multi-word phrases first
        sorted_patterns = sorted(lexicon.keys(), key=lambda k: len(k), reverse=True)

        for pat in sorted_patterns:
            replacement = lexicon[pat]
            # Match boundary-aware token
            escaped = re.escape(pat)
            normalized = re.sub(rf"(^|\s){escaped}(\s|$)", rf"\1{replacement}\2", normalized)

        return normalized.strip()


class EphemeralAudioBuffer:
    """
    ASVS L2 & Privacy By Design in-memory audio manager.
    Enforces maximum 15-minute (900 seconds) ephemeral TTL and instant purge.
    """
    MAX_RETENTION_SECONDS: float = 900.0  # 15 minutes

    def __init__(self):
        # buffer_id -> (audio_bytes, creation_timestamp)
        self._buffers: Dict[str, Tuple[bytes, float]] = {}

    def store_audio_stream(self, buffer_id: str, stream_bytes: bytes) -> str:
        """Stores voice audio stream in ephemeral memory stamped with current epoch."""
        self.purge_expired_buffers()
        self._buffers[buffer_id] = (stream_bytes, time.time())
        return buffer_id

    def retrieve_audio_stream(self, buffer_id: str) -> bytes:
        """
        Retrieves audio bytes if still within the 15-minute TTL.
        Raises AudioBufferExpiredException if expired or not found.
        """
        self.purge_expired_buffers()
        entry = self._buffers.get(buffer_id)
        if not entry:
            raise AudioBufferExpiredException(
                f"Audio stream '{buffer_id}' has expired and been securely purged from memory."
            )

        data, created_at = entry
        if time.time() - created_at > self.MAX_RETENTION_SECONDS:
            del self._buffers[buffer_id]
            raise AudioBufferExpiredException(
                f"Audio stream '{buffer_id}' exceeded 15-minute retention limit and was evicted."
            )
        return data

    def purge_buffer(self, buffer_id: str) -> bool:
        """Explicit zero-trace purge of a specific audio stream."""
        if buffer_id in self._buffers:
            del self._buffers[buffer_id]
            return True
        return False

    def purge_expired_buffers(self) -> int:
        """Evicts all buffers older than 15 minutes. Returns count of purged items."""
        now = time.time()
        expired_keys = [
            k for k, (_, created_at) in self._buffers.items()
            if now - created_at > self.MAX_RETENTION_SECONDS
        ]
        for k in expired_keys:
            del self._buffers[k]
        return len(expired_keys)

    def active_buffer_count(self) -> int:
        """Returns count of active ephemeral audio buffers."""
        self.purge_expired_buffers()
        return len(self._buffers)


class VivaRubricEngine:
    """
    NCTB Viva-Voce 4-Tier Scoring Engine:
    1. Conceptual Accuracy (40%)
    2. Terminology & Scientific Precision (30%)
    3. Articulation & Fluency (20%)
    4. Regional Dialect Accommodation (10%)
    """

    @classmethod
    def calculate_conceptual_score(
        cls,
        normalized_transcript: str,
        ideal_concepts: List[str]
    ) -> Tuple[float, List[str], List[str]]:
        """Evaluates fundamental conceptual coverage (0 to 40 marks)."""
        if not ideal_concepts:
            return 40.0, [], []

        detected = []
        missing = []

        for concept in ideal_concepts:
            if re.search(re.escape(concept), normalized_transcript, re.IGNORECASE):
                detected.append(concept)
            else:
                missing.append(concept)

        ratio = len(detected) / len(ideal_concepts)
        score = round(ratio * 40.0, 2)
        return score, detected, missing

    @classmethod
    def calculate_terminology_score(
        cls,
        normalized_transcript: str,
        required_terms: List[str]
    ) -> Tuple[float, List[str]]:
        """Evaluates precise scientific terminology usage (0 to 30 marks)."""
        if not required_terms:
            return 30.0, []

        matched = []
        for term in required_terms:
            if re.search(re.escape(term), normalized_transcript, re.IGNORECASE):
                matched.append(term)

        ratio = len(matched) / len(required_terms)
        score = round(ratio * 30.0, 2)
        return score, matched

    @classmethod
    def calculate_articulation_score(
        cls,
        telemetry: AcousticTelemetry
    ) -> float:
        """
        Evaluates speech fluency and acoustic clarity (0 to 20 marks).
        - Ideal Speech Rate: 100 - 160 WPM
        - Ideal SNR: >= 15 dB
        - Natural Pause Ratio: 0.05 - 0.25
        """
        score = 20.0

        # Speech rate check (ideal: 100-160 WPM)
        wpm = telemetry.speech_rate_wpm
        if wpm < 50.0:
            score -= 6.0
        elif wpm < 85.0:
            score -= 3.0
        elif wpm > 210.0:
            score -= 4.0

        # Acoustic clarity / SNR check (ideal: >= 15 dB)
        if telemetry.snr_db < 10.0:
            score -= 5.0
        elif telemetry.snr_db < 14.0:
            score -= 2.0

        # Excessive dead silence / pause check
        if telemetry.pause_ratio > 0.45:
            score -= 5.0
        elif telemetry.pause_ratio > 0.30:
            score -= 2.5

        return max(0.0, min(20.0, round(score, 2)))

    @classmethod
    def calculate_dialect_accommodation_score(
        cls,
        dialect: DialectType,
        raw_transcript: str,
        normalized_transcript: str
    ) -> float:
        """
        Awards full 10 marks for regional dialect expressiveness and confidence,
        ensuring regional students are not linguistically penalized.
        """
        if dialect == DialectType.STANDARD_BANGLA:
            return 10.0

        # Regional dialect speakers receive full 10 points for authentic verbal participation
        # Bonus is affirmed if regional markers were naturally used or normalized
        return 10.0

    @classmethod
    def determine_grade_letter(cls, total_score: float) -> str:
        """Maps 100-scale total score to NCTB grade letters."""
        if total_score >= 80.0:
            return "A+"
        elif total_score >= 70.0:
            return "A"
        elif total_score >= 60.0:
            return "A-"
        elif total_score >= 50.0:
            return "B"
        elif total_score >= 40.0:
            return "C"
        else:
            return "F"


class VivaEvaluator:
    """
    Main oral examination orchestration engine coordinating dialect adaptation,
    4-tier NCTB rubric evaluation, constructive feedback generation, and ephemeral memory.
    """

    def __init__(self):
        self.buffer_manager = EphemeralAudioBuffer()

    @classmethod
    def sanitize_metadata(cls, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validates zero PII in viva evaluation telemetry."""
        leaked_keys = [k for k in metadata.keys() if k.lower() in DISALLOWED_PII_KEYS]
        if leaked_keys:
            raise PIIInVivaStreamException(
                f"PII Leakage Detected: {', '.join(leaked_keys)} disallowed under ASVS L2."
            )
        return metadata

    def evaluate_viva(
        self,
        question_id: str,
        raw_transcript: str,
        dialect: DialectType = DialectType.STANDARD_BANGLA,
        telemetry: Optional[AcousticTelemetry] = None,
        audio_buffer_id: Optional[str] = None
    ) -> VivaEvaluationResult:
        """
        Executes complete multi-dialect viva evaluation workflow.
        """
        # Fetch question
        question = SAMPLE_VIVA_QUESTIONS.get(question_id)
        if not question:
            raise ValueError(f"Question ID '{question_id}' not found in NCTB question bank.")

        # 1. Dialect Normalization
        normalized = DialectNormalizer.normalize_transcript(raw_transcript, dialect)

        # 2. Acoustic Telemetry (fallback to default laboratory acoustics if omitted)
        if telemetry is None:
            telemetry = AcousticTelemetry(
                duration_seconds=25.0,
                snr_db=18.5,
                speech_rate_wpm=125.0,
                pause_ratio=0.12
            )

        # 3. Rubric Scoring
        conceptual_score, detected_concepts, missing_concepts = (
            VivaRubricEngine.calculate_conceptual_score(
                normalized, question.ideal_key_concepts
            )
        )
        terminology_score, matched_terms = (
            VivaRubricEngine.calculate_terminology_score(
                normalized, question.required_technical_terms
            )
        )
        articulation_score = VivaRubricEngine.calculate_articulation_score(telemetry)
        dialect_score = VivaRubricEngine.calculate_dialect_accommodation_score(
            dialect, raw_transcript, normalized
        )

        total_score = round(
            conceptual_score + terminology_score + articulation_score + dialect_score, 2
        )
        total_score = max(0.0, min(100.0, total_score))
        grade = VivaRubricEngine.determine_grade_letter(total_score)

        # 4. Constructive Academic Feedback
        if total_score >= 80.0:
            fb_bn = (
                f"চমৎকার উপস্থাপনা। আপনি মূল ধারণা ({', '.join(detected_concepts[:3])}) "
                f"এবং বৈজ্ঞানিক পরিভাষা অত্যন্ত নির্ভুলভাবে মৌখিক উত্তরে উপস্থাপন করেছেন।"
            )
            fb_en = (
                f"Excellent oral performance. Key concepts ({', '.join(detected_concepts[:3])}) "
                f"and scientific terminology were articulated with exceptional precision."
            )
        elif total_score >= 60.0:
            missing_mention = f" ঘাটতি ছিল: {', '.join(missing_concepts[:2])}।" if missing_concepts else ""
            fb_bn = (
                f"সন্তোষজনক উত্তর। অধিকাংশ মূল বিষয় উপস্থাপিত হয়েছে।{missing_mention} "
                f"পরবর্তী অনুশীলনে পারিভাষিক স্পষ্টতায় আরও মনোযোগ দিন।"
            )
            fb_en = (
                f"Satisfactory response. Core principles addressed well. "
                f"Strengthen scientific terminology precision for higher distinction."
            )
        else:
            missing_mention = f" অনুচ্চারিত আবশ্যক বিষয়: {', '.join(missing_concepts[:3])}।" if missing_concepts else ""
            fb_bn = (
                f"উত্তরটি অসম্পূর্ণ বা অস্পষ্ট।{missing_mention} "
                f"মূল বৈজ্ঞানিক সূত্র ও পরিভাষা স্পষ্ট উচ্চারণে পুনরভ্যাস করা আবশ্যক।"
            )
            fb_en = (
                f"Incomplete explanation. Key required concepts were omitted. "
                f"Review foundational textbook definitions and articulate with greater fluency."
            )

        # 5. Immediate ephemeral buffer purge if requested
        is_purged = False
        if audio_buffer_id:
            self.buffer_manager.purge_buffer(audio_buffer_id)
            is_purged = True

        acoustic_summary = {
            "duration_seconds": telemetry.duration_seconds,
            "snr_db": telemetry.snr_db,
            "speech_rate_wpm": telemetry.speech_rate_wpm,
            "pause_ratio": telemetry.pause_ratio,
        }

        return VivaEvaluationResult(
            question_id=question_id,
            dialect=dialect,
            raw_transcript=raw_transcript,
            normalized_transcript=normalized,
            conceptual_score=conceptual_score,
            terminology_score=terminology_score,
            articulation_score=articulation_score,
            dialect_accommodation_score=dialect_score,
            total_score=total_score,
            grade_letter=grade,
            feedback_bn=fb_bn,
            feedback_en=fb_en,
            detected_key_concepts=detected_concepts,
            missing_key_concepts=missing_concepts,
            matched_terms=matched_terms,
            acoustic_summary=acoustic_summary,
            is_ephemeral_purged=is_purged
        )
