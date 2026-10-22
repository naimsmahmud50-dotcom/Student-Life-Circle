"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Test Suite: Adaptive Neurodivergent Accessibility & Cognitive Reader Tower
FILE:      backend/tests/test_phase74_neurodivergent_accessibility.py
PURPOSE:   Comprehensive unit and integration test suite validating:
           1. Bionic reading saccadic fixation bolding and intensity scaling.
           2. Multi-syllabic academic STEM terminology decomposition and hyphenation.
           3. Words-Per-Minute (WPM) cognitive pacer reader pacing calculations.
           4. W3C WCAG 2.2 Level AAA (7:1) relative luminance and contrast ratio auditing.
           5. Section 73 REST API router endpoints.
STANDARDS: 100% assertions coverage, zero emojis, ASVS L2 compliance.
========================================================================================
"""

import asyncio
import unittest

from backend.app.schemas.neurodivergent_accessibility_schema import (
    ReadingAssistanceModeEnum,
    ColorContrastPresetEnum,
    BionicReadingTransformRequest,
    SyllableDecomposeRequest,
    CognitivePacerConfigDTO,
)
from backend.app.services.neurodivergent_accessibility_service import (
    NeurodivergentAccessibilityService,
    hex_to_relative_luminance,
    neurodivergent_accessibility_service
)
from backend.app.api.v1.router import (
    transform_bionic_reading_endpoint,
    decompose_academic_syllables_endpoint,
    audit_contrast_ratio_endpoint,
    list_accessibility_presets_endpoint,
    get_accessibility_status_endpoint
)


class TestNeurodivergentAccessibilityTower(unittest.TestCase):
    """
    Test cases asserting the accuracy, WCAG 2.2 AAA math, and cognitive reading telemetry
    for dyslexic, ADHD, and visually sensitive students.
    """

    def setUp(self):
        self.service = NeurodivergentAccessibilityService()

    def test_bionic_reading_transformation(self):
        """Verify academic sentence produces bolded fixation anchors."""
        req = BionicReadingTransformRequest(
            text="Newton's laws of motion govern classical mechanics and universal gravitation.",
            fixation_intensity=0.5,
            mode=ReadingAssistanceModeEnum.BIONIC_FIXATION
        )
        resp = self.service.transform_bionic_reading(req)
        self.assertEqual(resp.total_words, 10)
        self.assertIn("<strong", resp.html_formatted_text)
        self.assertGreater(resp.average_fixation_chars, 1.5)
        self.assertGreater(resp.estimated_reading_time_seconds, 1.0)

    def test_bionic_reading_intensity_scaling(self):
        """Verify higher fixation intensity yields strictly more bolded anchor characters."""
        req_low = BionicReadingTransformRequest(
            text="Thermodynamics and electromagnetism",
            fixation_intensity=0.3
        )
        req_high = BionicReadingTransformRequest(
            text="Thermodynamics and electromagnetism",
            fixation_intensity=0.7
        )
        resp_low = self.service.transform_bionic_reading(req_low)
        resp_high = self.service.transform_bionic_reading(req_high)
        self.assertLess(resp_low.average_fixation_chars, resp_high.average_fixation_chars)

    def test_syllable_decomposition_photosynthesis(self):
        """Verify multi-syllabic academic word decomposition."""
        req = SyllableDecomposeRequest(term="Photosynthesis")
        resp = self.service.decompose_syllables(req)
        self.assertEqual(resp.syllables, ["pho", "to", "syn", "the", "sis"])
        self.assertEqual(resp.hyphenated_term, "pho-to-syn-the-sis")
        self.assertEqual(resp.syllable_count, 5)
        self.assertEqual(resp.stress_index, 2)

    def test_syllable_decomposition_electromagnetism(self):
        """Verify electromagnetism is cleanly decomposed into 6 syllables."""
        req = SyllableDecomposeRequest(term="Electromagnetism")
        resp = self.service.decompose_syllables(req)
        self.assertEqual(resp.syllable_count, 6)
        self.assertIn("mag", resp.syllables)
        self.assertIn("lec", resp.syllables)

    def test_cognitive_pacer_telemetry(self):
        """Verify 240 WPM pacing calculation produces accurate intervals."""
        config = CognitivePacerConfigDTO(words_per_minute=240, chunk_size_words=1)
        text = " " .join(["word"] * 120)
        telemetry = self.service.calculate_cognitive_pacer(config, text)
        self.assertEqual(telemetry.target_wpm, 240)
        self.assertEqual(telemetry.interval_per_word_ms, 250.0)
        self.assertEqual(telemetry.total_duration_seconds, 30.0)
        self.assertEqual(telemetry.saccadic_jump_arcs, 120)

    def test_wcag_aaa_contrast_audit_pass(self):
        """Verify pure black and white passes WCAG 2.2 Level AAA (ratio >= 7.0)."""
        metrics = self.service.audit_contrast_ratio("#FFFFFF", "#000000")
        self.assertEqual(metrics.contrast_ratio, 21.0)
        self.assertTrue(metrics.wcag_aa_passed)
        self.assertTrue(metrics.wcag_aaa_passed)

    def test_wcag_contrast_audit_fail(self):
        """Verify low-contrast colors are flagged as failing WCAG AA and AAA."""
        metrics = self.service.audit_contrast_ratio("#777777", "#888888")
        self.assertLess(metrics.contrast_ratio, 4.5)
        self.assertFalse(metrics.wcag_aa_passed)
        self.assertFalse(metrics.wcag_aaa_passed)

    def test_presets_structure(self):
        """Verify 5 scientifically validated sensory presets exist."""
        presets = self.service.get_presets()
        self.assertIn("DEFAULT_DARK", presets)
        self.assertIn("WARM_AMBER_SEPIA", presets)
        self.assertIn("CALM_SLATE_CYAN", presets)
        self.assertIn("SOLARIZED_YELLOW_BLACK", presets)
        self.assertIn("HIGH_CONTRAST_MONOCHROME", presets)
        self.assertEqual(len(presets), 5)

    def test_accessibility_status(self):
        """Verify engine health reporting."""
        status = self.service.get_status()
        self.assertTrue(status.operational)
        self.assertGreater(status.total_bionic_transforms_served, 0)
        self.assertGreaterEqual(status.wcag_aaa_compliance_score, 99.0)

    def test_rest_api_endpoints(self):
        """Verify Section 73 REST API routes return 200 OK responses."""
        bionic_req = BionicReadingTransformRequest(text="Quantum entanglement and teleportation")
        bionic_resp = asyncio.run(transform_bionic_reading_endpoint(bionic_req))
        self.assertEqual(bionic_resp.total_words, 4)

        syll_req = SyllableDecomposeRequest(term="gravitational")
        syll_resp = asyncio.run(decompose_academic_syllables_endpoint(syll_req))
        self.assertIn("grav", syll_resp.syllables)

        contrast_resp = asyncio.run(audit_contrast_ratio_endpoint(fg_hex="#FACC15", bg_hex="#000000"))
        self.assertTrue(contrast_resp.wcag_aaa_passed)

        presets = asyncio.run(list_accessibility_presets_endpoint())
        self.assertIn("DEFAULT_DARK", presets)

        status_resp = asyncio.run(get_accessibility_status_endpoint())
        self.assertTrue(status_resp.operational)


if __name__ == "__main__":
    unittest.main()
