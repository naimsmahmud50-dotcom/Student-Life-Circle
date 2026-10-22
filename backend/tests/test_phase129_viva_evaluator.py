"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Multi-Dialect Audio Tutoring & Voice Viva Evaluator
 * TOPIC:     Phase 129 Acoustic Dialect Adaptation & Viva-Voce Rubric Engine
 * FILE:      backend/tests/test_phase129_viva_evaluator.py
 * PHASE:     Phase 129 - Multi-Dialect Regional Audio Tutoring
 * PURPOSE:   Comprehensive automated test suite validating:
 *            1. Developer Architecture Note headers & file presence
 *            2. Multi-dialect normalization parity (Chittagong, Sylhet, Barisal)
 *            3. NCTB 4-tier rubric evaluation mathematical bounds [0, 100]
 *            4. Anti-discrimination regional dialect accommodation points
 *            5. Ephemeral in-memory audio buffering and 15-minute TTL eviction
 *            6. ASVS L2 Zero-PII sanitization & defense against telemetry leakage
 *            7. Supabase migration 007 RLS policies and zero audio storage
 *            8. Frontend audio lab console, 3D tactile buttons, and Zero-Emoji compliance.
 * STANDARDS: Zero-Emoji, Pure Academic Design, Privacy By Design, ASVS L2
 */
"""

import os
import re
import time
import unittest
from pathlib import Path

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
    PIIInVivaStreamException,
    SAMPLE_VIVA_QUESTIONS,
)

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase129VivaEvaluator(unittest.TestCase):
    """
    Automated test verification suite for Phase 129 Multi-Dialect Audio Tutoring & Viva Evaluator.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.audio_init = cls.root_dir / "backend" / "audio" / "__init__.py"
        cls.evaluator_py = cls.root_dir / "backend" / "audio" / "viva_evaluator.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "007_viva_evaluator_rls.sql"
        cls.viva_tsx = cls.root_dir / "frontend" / "src" / "pages" / "viva" / "evaluator.tsx"
        cls.spec_md = cls.root_dir / "specs" / "033-phase129-viva-evaluator" / "spec.md"
        cls.plan_md = cls.root_dir / "specs" / "033-phase129-viva-evaluator" / "plan.md"
        cls.tasks_md = cls.root_dir / "specs" / "033-phase129-viva-evaluator" / "tasks.md"
        cls.test_file = Path(__file__).resolve()

        cls.target_files = [
            cls.audio_init,
            cls.evaluator_py,
            cls.migration_sql,
            cls.viva_tsx,
            cls.test_file,
        ]

    def test_01_all_target_files_exist_and_headers_valid(self):
        """Verify all target files exist and contain standardized Developer Architecture Note."""
        for file_path in self.target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"Missing Developer Architecture Note in {file_path.name}"
            )
            self.assertIn(
                "Phase 129 - Multi-Dialect Regional Audio Tutoring",
                content,
                f"Missing Phase 129 identifier in {file_path.name}"
            )

    def test_02_strict_zero_emoji_compliance(self):
        """Strictly enforces Zero-Emoji across all Phase 129 codebase files."""
        for file_path in self.target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"Zero-Emoji violation in {file_path.name}: Found emojis {matches}"
            )

    def test_03_dialect_normalization_chittagong(self):
        """Validates Chittagong regional colloquial translation to standard academic Bengali."""
        raw_ctg = "বস্তুর ভরবেগ্যা পরিবর্তনের হার প্রযুক্ত বোল এর সমানুপাতিক আর বলের দিকেই পরিবর্তন অইব"
        normalized = DialectNormalizer.normalize_transcript(raw_ctg, DialectType.CHITTAGONG)

        # Expected canonical tokens
        self.assertIn("ভরবেগ", normalized)
        self.assertIn("বল", normalized)
        self.assertNotIn("ভরবেগ্যা", normalized)
        self.assertNotIn("বোল", normalized)

    def test_04_dialect_normalization_sylhet_and_barisal(self):
        """Validates Sylhet and Barisal dialect translation to standard academic Bengali."""
        # Sylhet dialect test
        raw_syl = "বস্তুর ফরবেগ পরিবর্তনের হার প্রযুক্ত বলের লগে সমানুপাতিক অইতো নায়"
        norm_syl = DialectNormalizer.normalize_transcript(raw_syl, DialectType.SYLHET)
        self.assertIn("ভরবেগ", norm_syl)
        self.assertIn("সাথে", norm_syl)
        self.assertIn("হবে না", norm_syl)
        self.assertNotIn("ফরবেগ", norm_syl)
        self.assertNotIn("অইতো নায়", norm_syl)

        # Barisal dialect test
        raw_bar = "মোগো বস্তুর ভরবেগ পরিবর্তনের হার প্রযুক্ত বলের সমানুপাতিক হ্যারপর বল যেম্মে যাইবে"
        norm_bar = DialectNormalizer.normalize_transcript(raw_bar, DialectType.BARISAL)
        self.assertIn("আমাদের", norm_bar)
        self.assertIn("তারপর", norm_bar)
        self.assertNotIn("মোগো", norm_bar)
        self.assertNotIn("হ্যারপর", norm_bar)

    def test_05_rubric_scoring_mathematical_bounds_and_grades(self):
        """Validates mathematical rubric bounds (0 to 100) and grade assignment."""
        evaluator = VivaEvaluator()

        # High-scoring response
        transcript_high = (
            "নিউটনের দ্বিতীয় সূত্র অনুসারে বস্তুর ভরবেগের পরিবর্তনের হার তার ওপর প্রযুক্ত বলের সমানুপাতিক "
            "এবং বল যেদিকে ক্রিয়া করে ত্বরণ ও ভরবেগের পরিবর্তনও সেদিকে ঘটে। এর দ্বারা F = ma প্রমাণিত হয়।"
        )
        telemetry_clean = AcousticTelemetry(
            duration_seconds=20.0,
            snr_db=22.0,
            speech_rate_wpm=130.0,
            pause_ratio=0.10
        )
        res_high = evaluator.evaluate_viva(
            question_id="viva_phy_01",
            raw_transcript=transcript_high,
            dialect=DialectType.STANDARD_BANGLA,
            telemetry=telemetry_clean
        )
        self.assertGreaterEqual(res_high.total_score, 80.0)
        self.assertLessEqual(res_high.total_score, 100.0)
        self.assertEqual(res_high.grade_letter, "A+")
        self.assertGreaterEqual(res_high.conceptual_score, 30.0)
        self.assertGreaterEqual(res_high.terminology_score, 25.0)

        # Empty / failing response
        res_empty = evaluator.evaluate_viva(
            question_id="viva_phy_01",
            raw_transcript="কিছু মনে পড়ছে না স্যার",
            dialect=DialectType.STANDARD_BANGLA,
            telemetry=telemetry_clean
        )
        self.assertLess(res_empty.total_score, 40.0)
        self.assertEqual(res_empty.grade_letter, "F")

    def test_06_dialect_accommodation_parity(self):
        """Ensures regional dialect speakers receive equal accommodation marks without geographic bias."""
        evaluator = VivaEvaluator()
        telemetry = AcousticTelemetry(
            duration_seconds=22.0,
            snr_db=20.0,
            speech_rate_wpm=125.0,
            pause_ratio=0.12
        )

        # Regional Chittagong response with dialect phrasing
        ctg_raw = "বস্তুর ভরবেগ্যা পরিবর্তনের হার প্রযুক্ত বোল এর সমানুপাতিক আর বলের দিকেই পরিবর্তন অইব"
        res_ctg = evaluator.evaluate_viva(
            question_id="viva_phy_01",
            raw_transcript=ctg_raw,
            dialect=DialectType.CHITTAGONG,
            telemetry=telemetry
        )

        # Dialect accommodation score must be full 10.0
        self.assertEqual(res_ctg.dialect_accommodation_score, 10.0)
        # Normalized transcript should successfully capture core physics concepts
        self.assertIn("ভরবেগ", res_ctg.detected_key_concepts)
        self.assertIn("বল", res_ctg.detected_key_concepts)
        self.assertGreaterEqual(res_ctg.total_score, 70.0)

    def test_07_ephemeral_audio_buffer_ttl_and_purge(self):
        """Tests that audio streams are strictly kept in-memory and evicted after 15 minutes."""
        buffer_mgr = EphemeralAudioBuffer()
        buf_id = "stream_sess_101"
        dummy_audio = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00"

        # 1. Store and verify active
        buffer_mgr.store_audio_stream(buf_id, dummy_audio)
        self.assertEqual(buffer_mgr.active_buffer_count(), 1)

        # 2. Retrieve within TTL
        retrieved = buffer_mgr.retrieve_audio_stream(buf_id)
        self.assertEqual(retrieved, dummy_audio)

        # 3. Simulate 16 minutes elapsed (960 seconds > 900 seconds TTL)
        buffer_mgr._buffers[buf_id] = (dummy_audio, time.time() - 960.0)
        with self.assertRaises(AudioBufferExpiredException):
            buffer_mgr.retrieve_audio_stream(buf_id)

        # Buffer must now be evicted
        self.assertEqual(buffer_mgr.active_buffer_count(), 0)

        # 4. Instant purge upon scoring
        buffer_mgr.store_audio_stream("stream_sess_102", dummy_audio)
        self.assertTrue(buffer_mgr.purge_buffer("stream_sess_102"))
        self.assertEqual(buffer_mgr.active_buffer_count(), 0)

    def test_08_asvs_l2_zero_pii_sanitization(self):
        """Validates that viva evaluation requests reject all student PII keys."""
        clean_meta = {"dialect": "CHITTAGONG", "question_id": "viva_phy_01", "attempt_sec": 30}
        sanitized = VivaEvaluator.sanitize_metadata(clean_meta)
        self.assertEqual(sanitized, clean_meta)

        # Disallowed personal identifiers must raise PIIInVivaStreamException
        pii_leaks = [
            {"student_name": "Tariqul Islam"},
            {"phone": "+8801811223344"},
            {"email": "tariq@example.com"},
            {"nid": "19951234567890"},
            {"roll": "10029"},
        ]
        for leaking in pii_leaks:
            with self.assertRaises(PIIInVivaStreamException):
                VivaEvaluator.sanitize_metadata(leaking)

    def test_09_supabase_migration_007_rls_integrity(self):
        """Validates migration 007 RLS policies, zero audio retention, and immutability."""
        content = self.migration_sql.read_text(encoding="utf-8")
        self.assertIn("viva_evaluations", content)
        self.assertIn("ALTER TABLE public.viva_evaluations ENABLE ROW LEVEL SECURITY;", content)
        self.assertIn("ALTER TABLE public.viva_evaluations FORCE ROW LEVEL SECURITY;", content)
        self.assertIn("student_id = auth.uid()", content)
        self.assertIn("audio_retained BOOLEAN NOT NULL DEFAULT FALSE", content)
        self.assertIn("idx_viva_evaluations_student_id", content)

    def test_10_frontend_audio_laboratory_styling(self):
        """Validates frontend viva laboratory for Oxford Navy palette, 3D tactile buttons, and Lucide icons."""
        content = self.viva_tsx.read_text(encoding="utf-8")
        # Color palette
        self.assertIn("#0A2540", content)
        # Tactile 3D buttons
        self.assertIn("shadow-[0_4px_0_0_", content)
        self.assertIn("active:translate-y-1", content)
        # Professional audio lab icons
        self.assertIn("Mic", content)
        self.assertIn("Volume2", content)
        self.assertIn("Square", content)
        self.assertIn("ShieldCheck", content)
        # ASVS L2 ephemeral notice
        self.assertIn("ASVS L2", content)


if __name__ == "__main__":
    unittest.main()
