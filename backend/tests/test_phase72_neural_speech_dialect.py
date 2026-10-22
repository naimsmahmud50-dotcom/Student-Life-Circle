"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Test Suite: Neural Bengali Speech Synthesis & Regional Dialect Tutoring Engine
FILE:      backend/tests/test_phase72_neural_speech_dialect.py
PURPOSE:   Comprehensive unit and integration test suite validating:
           1. Dialect transliteration engine across 5 regional dialects
              (Chittagonian, Sylheti, Noakhailla, Barisali, Rangpuri) with IPA phonetic mapping.
           2. Neural speech synthesis telemetry: duration, sample rate, 3-tier Opus bitrate
              (6kbps, 16kbps, 48kbps), waveform peaks, and phoneme timestamp alignment.
           3. Caching layer idempotency and cache-hit verification.
           4. Dialect vocabulary bridge dictionary lookup and fallback handling.
           5. REST API endpoint handlers in router.py.
STANDARDS: 100% assertions coverage, zero emojis, ASVS L2 compliance.
========================================================================================
"""

import asyncio
import unittest

from backend.app.schemas.neural_speech_dialect_schema import (
    DialectEnum,
    AudioQualityTierEnum,
    DialectTransliterateRequest,
    SpeechSynthesizeRequest,
    DialectVocabBridgeRequest,
)
from backend.app.services.neural_speech_dialect_service import (
    NeuralSpeechDialectService,
    neural_speech_dialect_service
)
from backend.app.api.v1.router import (
    transliterate_bengali_dialect_endpoint,
    synthesize_speech_endpoint,
    bridge_dialect_vocabulary_endpoint,
    list_supported_dialects_endpoint,
    get_speech_dialect_status_endpoint
)


class TestNeuralSpeechDialectEngine(unittest.TestCase):
    """
    Test cases asserting the accuracy, performance, and API behavior
    of the Neural Bengali Speech Synthesis and Regional Dialect Tutoring Tower.
    """

    def setUp(self):
        self.service = NeuralSpeechDialectService()

    def test_chittagonian_dialect_transliteration(self):
        """Test transliteration from Standard Bengali to Chittagonian."""
        req = DialectTransliterateRequest(
            text="আমি ভালো আছি",
            source_dialect=DialectEnum.STANDARD_CHOLITO,
            target_dialect=DialectEnum.CHITTAGONIAN
        )
        resp = self.service.transliterate_dialect(req)
        self.assertEqual(resp.source_dialect, DialectEnum.STANDARD_CHOLITO)
        self.assertEqual(resp.target_dialect, DialectEnum.CHITTAGONIAN)
        self.assertIn("আঁই", resp.transliterated_text)
        self.assertIn("গম", resp.transliterated_text)
        self.assertGreater(len(resp.vocab_substitutions), 0)
        self.assertIn("ãĩ", resp.phonetic_ipa)

    def test_sylheti_dialect_transliteration(self):
        """Test transliteration from Standard Bengali to Sylheti."""
        req = DialectTransliterateRequest(
            text="আমি যাব এবং ভালো খাবার খাব",
            source_dialect=DialectEnum.STANDARD_CHOLITO,
            target_dialect=DialectEnum.SYLHETI
        )
        resp = self.service.transliterate_dialect(req)
        self.assertIn("যাইমু", resp.transliterated_text)
        self.assertIn("ভালা", resp.transliterated_text)
        self.assertIn("খাইর", resp.transliterated_text)
        self.assertGreaterEqual(resp.confidence_score, 0.90)

    def test_noakhailla_dialect_transliteration(self):
        """Test transliteration to Noakhailla dialect."""
        req = DialectTransliterateRequest(
            text="ছেলে পানি খাচ্ছে এবং টাকা দিচ্ছে",
            source_dialect=DialectEnum.STANDARD_CHOLITO,
            target_dialect=DialectEnum.NOAKHAILLA
        )
        resp = self.service.transliterate_dialect(req)
        self.assertIn("হোলা", resp.transliterated_text)
        self.assertIn("হানি", resp.transliterated_text)
        self.assertIn("টিয়া", resp.transliterated_text)

    def test_barisali_dialect_transliteration(self):
        """Test transliteration to Barisali dialect."""
        req = DialectTransliterateRequest(
            text="আমি যাব এবং আমরা সবাই ভালো আছি",
            source_dialect=DialectEnum.STANDARD_CHOLITO,
            target_dialect=DialectEnum.BARISALI
        )
        resp = self.service.transliterate_dialect(req)
        self.assertIn("মুই", resp.transliterated_text)
        self.assertIn("মোরা", resp.transliterated_text)
        self.assertIn("ভালা", resp.transliterated_text)

    def test_rangpuri_dialect_transliteration(self):
        """Test transliteration to Rangpuri dialect."""
        req = DialectTransliterateRequest(
            text="আমি যাব এবং ছেলে ভালো আছে",
            source_dialect=DialectEnum.STANDARD_CHOLITO,
            target_dialect=DialectEnum.RANGPURI
        )
        resp = self.service.transliterate_dialect(req)
        self.assertIn("মুই", resp.transliterated_text)
        self.assertIn("বেটাছোল", resp.transliterated_text)
        self.assertIn("সোন্দর", resp.transliterated_text)

    def test_speech_synthesis_ultra_low_bandwidth(self):
        """Test ultra-low bandwidth Opus 6kbps audio synthesis for 2G networks."""
        req = SpeechSynthesizeRequest(
            text="নিউটনের গতির দ্বিতীয় সূত্র অনুযায়ী বল হলো ভর এবং ত্বরণের গুণফল।",
            dialect=DialectEnum.STANDARD_CHOLITO,
            quality_tier=AudioQualityTierEnum.ULTRA_LOW_BANDWIDTH_6KBPS,
            speed_rate=1.0
        )
        resp = self.service.synthesize_speech(req)
        self.assertTrue(resp.audio_id.startswith("aud_"))
        self.assertEqual(resp.bitrate_kbps, 6)
        self.assertEqual(resp.sample_rate_hz, 16000)
        self.assertGreater(resp.duration_seconds, 1.0)
        self.assertGreater(resp.estimated_size_bytes, 0)
        self.assertEqual(len(resp.waveform_peaks), 32)
        self.assertFalse(resp.cache_hit)

        # Second identical request should return cache hit
        resp2 = self.service.synthesize_speech(req)
        self.assertTrue(resp2.cache_hit)

    def test_speech_synthesis_studio_hd(self):
        """Test Studio HD 48kbps audio synthesis."""
        req = SpeechSynthesizeRequest(
            text="উচ্চতর গণিত ও পদার্থবিজ্ঞান অনুশীলন সেট।",
            dialect=DialectEnum.CHITTAGONIAN,
            quality_tier=AudioQualityTierEnum.STUDIO_HD_48KBPS,
            speed_rate=1.25,
            pitch_multiplier=1.1
        )
        resp = self.service.synthesize_speech(req)
        self.assertEqual(resp.bitrate_kbps, 48)
        self.assertEqual(resp.sample_rate_hz, 48000)
        self.assertGreater(len(resp.phoneme_timestamps), 0)

    def test_vocabulary_bridge_lookup(self):
        """Test looking up regional vocabulary terms."""
        req = DialectVocabBridgeRequest(
            word_or_phrase="গম",
            dialect=DialectEnum.CHITTAGONIAN
        )
        resp = self.service.bridge_vocabulary(req)
        self.assertEqual(resp.source_word, "গম")
        self.assertIn("ভালো", resp.standard_equivalent)
        self.assertEqual(resp.ipa_transcription, "/gɔm/")

        req_sylheti = DialectVocabBridgeRequest(
            word_or_phrase="কিতা",
            dialect=DialectEnum.SYLHETI
        )
        resp_sylheti = self.service.bridge_vocabulary(req_sylheti)
        self.assertIn("কী", resp_sylheti.standard_equivalent)

    def test_speech_engine_status(self):
        """Test operational health status report."""
        status_dto = self.service.get_status()
        self.assertEqual(status_dto.engine_status, "OPERATIONAL")
        self.assertEqual(len(status_dto.supported_dialects), 6)
        self.assertGreaterEqual(status_dto.models_loaded, 1)

    def test_router_endpoints_coroutine_execution(self):
        """Direct coroutine integration test for all Phase 72 REST API endpoints."""
        # 1. Transliterate endpoint
        t_req = DialectTransliterateRequest(
            text="আমি ভালো আছি",
            source_dialect=DialectEnum.STANDARD_CHOLITO,
            target_dialect=DialectEnum.CHITTAGONIAN
        )
        t_res = asyncio.run(transliterate_bengali_dialect_endpoint(t_req))
        self.assertIn("গম", t_res.transliterated_text)

        # 2. Synthesize endpoint
        s_req = SpeechSynthesizeRequest(
            text="পরীক্ষার প্রস্তুতি",
            dialect=DialectEnum.BARISALI,
            quality_tier=AudioQualityTierEnum.BALANCED_16KBPS
        )
        s_res = asyncio.run(synthesize_speech_endpoint(s_req))
        self.assertEqual(s_res.bitrate_kbps, 16)

        # 3. Vocab Bridge endpoint
        v_req = DialectVocabBridgeRequest(
            word_or_phrase="হোলা",
            dialect=DialectEnum.NOAKHAILLA
        )
        v_res = asyncio.run(bridge_dialect_vocabulary_endpoint(v_req))
        self.assertIn("ছেলে", v_res.standard_equivalent)

        # 4. Dialects list endpoint
        d_res = asyncio.run(list_supported_dialects_endpoint())
        self.assertIn("CHITTAGONIAN", d_res["dialects"])
        self.assertIn("ULTRA_LOW_BANDWIDTH_6KBPS", d_res["quality_tiers"])

        # 5. Status endpoint
        stat_res = asyncio.run(get_speech_dialect_status_endpoint())
        self.assertEqual(stat_res.engine_status, "OPERATIONAL")


if __name__ == "__main__":
    unittest.main()
