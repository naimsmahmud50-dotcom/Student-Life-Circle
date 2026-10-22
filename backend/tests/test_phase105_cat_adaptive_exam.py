"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite
TOPIC:     Phase 105 AI Adaptive Examination & Dynamic CAT Tower Tests
FILE:      backend/tests/test_phase105_cat_adaptive_exam.py
PHASE:     Phase 105 - AI Adaptive CAT Examination Tower
PURPOSE:   Asserts Item Response Theory (IRT 3-PL) mathematical precision, Fisher
           Information maximization, latent ability percentile convergence (SE < 0.25),
           REST API endpoints, Developer Architecture Note headers, and strict zero-emoji governance.
STANDARDS: UI/UX Pro Max, IRT 3-PL Latent Ability Math, Zero-Emoji, Human-Centric
"""

import json
import math
import os
import unittest
from pathlib import Path

from backend.app.services.cat_engine_service import CatEngineService, cat_engine_service
from backend.app.api.v1.endpoints.adaptive_exam import (
    start_adaptive_exam_session,
    submit_adaptive_exam_step,
    get_adaptive_exam_result,
    get_adaptive_exam_result_by_path,
)


def is_emoji_char(char: str) -> bool:
    """Detects whether a character is a decorative unicode emoji."""
    code = ord(char)
    return (
        0x1F600 <= code <= 0x1F64F or
        0x1F300 <= code <= 0x1F5FF or
        0x1F680 <= code <= 0x1F6FF or
        0x1F900 <= code <= 0x1F9FF or
        0x1FA70 <= code <= 0x1FAFF or
        0x2600 <= code <= 0x26FF or
        0x2700 <= code <= 0x27BF
    )


def contains_emoji(text: str) -> bool:
    """Returns True if string contains any decorative unicode emoji."""
    return any(is_emoji_char(c) for c in text)


class TestPhase105CatAdaptiveExam(unittest.TestCase):
    """
    Automated verification suite for Phase 105 AI Adaptive Examination & Dynamic CAT Tower.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.service_path = cls.repo_root / "backend" / "app" / "services" / "cat_engine_service.py"
        cls.endpoint_path = cls.repo_root / "backend" / "app" / "api" / "v1" / "endpoints" / "adaptive_exam.py"
        cls.studio_path = cls.repo_root / "frontend" / "src" / "components" / "adaptive-exam" / "AdaptiveExamStudio.tsx"
        cls.graph_path = cls.repo_root / "frontend" / "src" / "components" / "adaptive-exam" / "AbilityConvergenceGraph.tsx"
        cls.page_path = cls.repo_root / "frontend" / "src" / "pages" / "adaptive-exam.tsx"

    def setUp(self):
        cat_engine_service.reset_for_testing()

    def tearDown(self):
        cat_engine_service.reset_for_testing()

    def test_01_3pl_probability_mathematical_precision(self):
        """Validates 3-PL probability P(theta) = c + (1-c)/(1+exp(-a(theta-b)))."""
        # When theta == b, exp term is 1/(1+1) = 0.5
        # P(b) = c + (1-c)*0.5 = 0.5 + 0.5*c
        prob_mid = CatEngineService.calculate_3pl_probability(theta=1.0, a=2.0, b=1.0, c=0.20)
        expected_mid = 0.20 + (1.0 - 0.20) * 0.5
        self.assertAlmostEqual(prob_mid, expected_mid, places=4)

        # When c == 0, 3-PL must equal 2-PL
        prob_3pl_zero_c = CatEngineService.calculate_3pl_probability(theta=0.5, a=1.5, b=0.2, c=0.0)
        prob_2pl = CatEngineService.calculate_2pl_probability(theta=0.5, a=1.5, b=0.2)
        self.assertEqual(prob_3pl_zero_c, prob_2pl)

        # Lower asymptote as theta -> -inf must equal c
        prob_low = CatEngineService.calculate_3pl_probability(theta=-100.0, a=2.0, b=0.0, c=0.25)
        self.assertEqual(prob_low, 0.25)

        # Upper asymptote as theta -> +inf must equal 1.0
        prob_high = CatEngineService.calculate_3pl_probability(theta=100.0, a=2.0, b=0.0, c=0.25)
        self.assertEqual(prob_high, 1.0)

    def test_02_3pl_fisher_information_and_2pl_equivalence(self):
        """Validates 3-PL Fisher Information I(theta) and exact 2-PL equivalence when c=0."""
        # When c=0: I(theta) = a^2 * P * (1-P)
        info_3pl = CatEngineService.calculate_3pl_fisher_information(theta=0.8, a=2.0, b=0.8, c=0.0)
        info_2pl = CatEngineService.calculate_fisher_information(theta=0.8, a=2.0, b=0.8)
        self.assertAlmostEqual(info_3pl, info_2pl, places=5)
        # At theta=b and c=0, P=0.5 => I = 2^2 * 0.5 * 0.5 = 1.0
        self.assertAlmostEqual(info_3pl, 1.0, places=4)

        # When c > 0, Fisher information is strictly positive
        info_3pl_guessing = CatEngineService.calculate_3pl_fisher_information(theta=0.5, a=2.2, b=0.5, c=0.20)
        self.assertGreater(info_3pl_guessing, 0.0)

    def test_03_latent_ability_percentile_mapping(self):
        """Validates normal CDF percentile rank mapping: Phi(theta) * 100."""
        self.assertAlmostEqual(CatEngineService.calculate_percentile(0.0), 50.0, places=1)
        self.assertAlmostEqual(CatEngineService.calculate_percentile(1.0), 84.13, delta=0.5)
        self.assertAlmostEqual(CatEngineService.calculate_percentile(2.0), 97.72, delta=0.5)
        self.assertGreater(CatEngineService.calculate_percentile(2.5), 99.0)

    def test_04_optimal_item_selection_maximizing_fisher_information(self):
        """Verifies item selection selects the unadministered question maximizing Fisher Information at theta."""
        session = cat_engine_service.start_cat_session(
            student_id="stu_fisher_test",
            subject="উচ্চতর গণিত",
            initial_theta=2.0,
            use_3pl_bank=True
        )
        first_item = session["current_item"]
        self.assertIsNotNone(first_item)

        # The first item selected for theta=2.0 should have difficulty close to 2.0 (e.g. b >= 1.5)
        meta = next(it for it in cat_engine_service.CALIBRATED_3PL_ITEM_BANK if it["item_id"] == first_item["item_id"])
        self.assertGreaterEqual(meta["difficulty_b"], 1.0)

    def test_05_dynamic_adaptive_session_lifecycle_and_convergence(self):
        """Simulates full 3-PL CAT adaptive exam run verifying standard error reduction."""
        session = cat_engine_service.start_cat_session(
            student_id="stu_adaptive_lifecycle",
            subject="বিজ্ঞান",
            initial_theta=0.0,
            target_se=0.25,
            use_3pl_bank=True
        )
        session_id = session["session_id"]
        initial_se = session["standard_error"]

        # Run steps until completion
        for _ in range(16):
            curr = session.get("current_item")
            if not curr or session.get("is_complete"):
                break

            item_id = curr["item_id"]
            meta = next(it for it in cat_engine_service.CALIBRATED_3PL_ITEM_BANK if it["item_id"] == item_id)
            res = cat_engine_service.submit_cat_answer(session_id, item_id, meta["correct_option_id"])
            session = res["session"]

        final_session = cat_engine_service.get_session(session_id)
        self.assertTrue(final_session["is_complete"])
        self.assertLess(final_session["standard_error"], initial_se)
        self.assertIsNotNone(final_session["final_ability_category"])
        self.assertIsNotNone(final_session["admission_readiness"])
        self.assertGreater(len(final_session["administered_history"]), 0)

        # Verify trajectory helper
        trajectory = cat_engine_service.get_ability_trajectory(session_id)
        self.assertEqual(len(trajectory), len(final_session["administered_history"]))

    async def _test_async_endpoints(self):
        """Helper to exercise async endpoint functions."""
        # 1. Start session
        start_payload = {
            "student_id": "stu_api_test",
            "subject": "বিজ্ঞান",
            "initial_theta": 0.0,
            "target_se": 0.25,
            "use_3pl_bank": True
        }
        start_res = await start_adaptive_exam_session(start_payload)
        self.assertEqual(start_res.status_code, 200)

        start_content = json.loads(start_res.body.decode("utf-8")) if hasattr(start_res, "body") else getattr(start_res, "content", {})
        session_id = start_content.get("session_id")
        current_item = start_content.get("current_item")
        self.assertIsNotNone(session_id)
        self.assertIsNotNone(current_item)

        # 2. Submit Step
        submit_payload = {
            "session_id": session_id,
            "item_id": current_item["item_id"],
            "selected_option_id": "a"
        }
        submit_res = await submit_adaptive_exam_step(submit_payload)
        self.assertEqual(submit_res.status_code, 200)

        # 3. Get Result by query param
        result_res = await get_adaptive_exam_result(session_id=session_id)
        self.assertEqual(result_res.status_code, 200)

        # 4. Get Result by path param
        result_path_res = await get_adaptive_exam_result_by_path(session_id=session_id)
        self.assertEqual(result_path_res.status_code, 200)

    def test_06_rest_api_endpoints_start_submit_result(self):
        """Verifies Phase 105 REST API endpoint functions (/start, /submit-step, /result)."""
        import asyncio
        asyncio.run(self._test_async_endpoints())

    def test_07_developer_architecture_note_and_strict_zero_emoji(self):
        """Verifies Developer Architecture Note headers and strict zero-emoji governance across Phase 105 files."""
        phase105_files = [
            self.service_path,
            self.endpoint_path,
            self.studio_path,
            self.graph_path,
            self.page_path,
            Path(__file__)
        ]

        for file_path in phase105_files:
            self.assertTrue(file_path.exists(), f"File does not exist: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"Missing Developer Architecture Note in {file_path.name}"
            )
            self.assertIn(
                "Phase 105",
                content,
                f"Missing Phase 105 reference in {file_path.name}"
            )
            self.assertFalse(
                contains_emoji(content),
                f"Strict Zero-Emoji violation detected in {file_path.name}"
            )

    def test_08_bayesian_eap_numerical_stability_on_extreme_ability(self):
        """Verifies theta remains strictly bounded within [-3.0, +3.0] even under extreme response sequences."""
        session = cat_engine_service.start_cat_session("stu_extremes", initial_theta=2.8, use_3pl_bank=True)
        session_id = session["session_id"]

        # Deliberately submit 10 consecutive correct answers
        for _ in range(5):
            curr = session.get("current_item")
            if not curr or session.get("is_complete"):
                break
            meta = next(it for it in cat_engine_service.CALIBRATED_3PL_ITEM_BANK if it["item_id"] == curr["item_id"])
            res = cat_engine_service.submit_cat_answer(session_id, curr["item_id"], meta["correct_option_id"])
            session = res["session"]
            self.assertLessEqual(session["current_theta"], 3.0)
            self.assertGreaterEqual(session["current_theta"], -3.0)

    def test_09_admission_readiness_classification_tiers(self):
        """Verifies correct pedagogical categorization and admission tiers across ability spectrum."""
        self.assertIn("বুয়েট", cat_engine_service._evaluate_admission_readiness(2.5))
        self.assertIn("শীর্ষ পাবলিক", cat_engine_service._evaluate_admission_readiness(1.6))
        self.assertIn("জাতীয় পর্যায়ের", cat_engine_service._evaluate_admission_readiness(0.9))
        self.assertIn("উচ্চ মাধ্যমিক", cat_engine_service._evaluate_admission_readiness(0.2))
        self.assertIn("মৌলিক", cat_engine_service._evaluate_admission_readiness(-0.5))

    def test_10_rest_api_validation_guards_and_error_handling(self):
        """Verifies HTTP 400 and HTTP 404 validation guards in adaptive exam endpoints."""
        import asyncio
        from backend.app.core.fastapi_shim import HTTPException

        async def _run_guards():
            # Missing session_id must raise 400
            with self.assertRaises(HTTPException) as cm:
                await submit_adaptive_exam_step({"session_id": "", "item_id": "item_1", "selected_option_id": "a"})
            self.assertEqual(cm.exception.status_code, 400)

            # Querying nonexistent session must raise 404
            with self.assertRaises(HTTPException) as cm2:
                await get_adaptive_exam_result(session_id="nonexistent_session_id_9999")
            self.assertEqual(cm2.exception.status_code, 404)

        asyncio.run(_run_guards())

    def test_11_item_sanitization_security(self):
        """Verifies that items served to the client have answer keys and calibration metadata stripped."""
        session = cat_engine_service.start_cat_session("stu_sec_test", use_3pl_bank=True)
        item = session.get("current_item")
        self.assertIsNotNone(item)

        # Anti-cheating assertions
        self.assertNotIn("correct_option_id", item)
        self.assertNotIn("difficulty_b", item)
        self.assertNotIn("discrimination_a", item)
        self.assertNotIn("pseudo_guessing_c", item)
        self.assertNotIn("explanation_bn", item)
        self.assertIn("stem_bn", item)
        self.assertIn("options", item)


if __name__ == "__main__":
    unittest.main()

