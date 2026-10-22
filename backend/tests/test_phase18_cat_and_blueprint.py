"""
================================================================================
MODULE: Psychometrics & Curriculum Blueprint Tests (ক্যাট ও ব্লুপ্রিন্ট টেস্ট)
TOPIC: Automated Unit & Integration Tests for 2-PL IRT CAT & Exam Blueprints
FILE: backend/tests/test_phase18_cat_and_blueprint.py
PURPOSE: Rigorously verifies Computerized Adaptive Testing (CAT) ability estimation,
         Fisher Information item selection, convergence criteria, and automated
         curriculum blueprint composition under NCTB and Bloom's Taxonomy standards.
AUDIENCE: QA Engineers, Psychometricians, Assessment Directors.
STANDARDS: ISO/IEC 25010 Quality Model, Psychometric Society IRT Guidelines.
================================================================================
"""

import math
import unittest

try:
    from backend.app.services.cat_engine_service import cat_engine_service
    from backend.app.services.blueprint_composer_service import blueprint_composer_service
except ImportError:
    from app.services.cat_engine_service import cat_engine_service
    from app.services.blueprint_composer_service import blueprint_composer_service


class TestCatAndBlueprintService(unittest.TestCase):
    """Test suite covering Phase 18 Computerized Adaptive Testing and Curriculum Blueprint Composer."""

    def setUp(self) -> None:
        cat_engine_service.reset_for_testing()
        blueprint_composer_service.reset_for_testing()

    def tearDown(self) -> None:
        cat_engine_service.reset_for_testing()
        blueprint_composer_service.reset_for_testing()

    # --------------------------------------------------------------------------
    # Computerized Adaptive Testing (CAT) Tests
    # --------------------------------------------------------------------------

    def test_cat_session_start_selects_first_item_and_initializes_theta(self) -> None:
        """Verifies session initialization, starting theta, and sanitized first question."""
        session = cat_engine_service.start_cat_session(
            student_id="stu_test_01",
            subject="গণিত",
            initial_theta=0.0
        )

        self.assertIsNotNone(session["session_id"])
        self.assertEqual(session["student_id"], "stu_test_01")
        self.assertEqual(session["current_theta"], 0.0)
        self.assertEqual(session["standard_error"], 1.0)
        self.assertFalse(session["is_complete"])
        self.assertIsNotNone(session["current_item"])

        # Sensitive parameters must be stripped from student item
        item = session["current_item"]
        self.assertNotIn("correct_option_id", item)
        self.assertNotIn("discrimination_a", item)
        self.assertNotIn("difficulty_b", item)
        self.assertIn("stem_bn", item)
        self.assertEqual(len(item["options"]), 4)

    def test_cat_submit_correct_answer_increases_theta_and_lowers_se(self) -> None:
        """Verifies that answering correctly raises Theta and decreases Standard Error."""
        session = cat_engine_service.start_cat_session(
            student_id="stu_test_02",
            subject="গণিত",
            initial_theta=0.0
        )
        session_id = session["session_id"]
        item_id = session["current_item"]["item_id"]

        # Find correct option for this item from bank
        item_meta = next(it for it in cat_engine_service.CALIBRATED_ITEM_BANK if it["item_id"] == item_id)
        correct_opt = item_meta["correct_option_id"]

        res = cat_engine_service.submit_cat_answer(
            session_id=session_id,
            item_id=item_id,
            selected_option_id=correct_opt
        )

        self.assertTrue(res["success"])
        self.assertTrue(res["last_answer_correct"])
        updated_session = res["session"]

        # Theta should increase
        self.assertGreater(updated_session["current_theta"], 0.0)
        # Standard error should decrease
        self.assertLess(updated_session["standard_error"], 1.0)
        self.assertEqual(updated_session["items_administered_count"], 1)

    def test_cat_submit_incorrect_answer_decreases_theta(self) -> None:
        """Verifies that an incorrect response lowers Theta."""
        session = cat_engine_service.start_cat_session(
            student_id="stu_test_03",
            subject="গণিত",
            initial_theta=0.5
        )
        session_id = session["session_id"]
        item_id = session["current_item"]["item_id"]

        # Deliberately submit incorrect option
        item_meta = next(it for it in cat_engine_service.CALIBRATED_ITEM_BANK if it["item_id"] == item_id)
        wrong_opt = "d" if item_meta["correct_option_id"] != "d" else "a"

        res = cat_engine_service.submit_cat_answer(
            session_id=session_id,
            item_id=item_id,
            selected_option_id=wrong_opt
        )

        self.assertTrue(res["success"])
        self.assertFalse(res["last_answer_correct"])
        self.assertLess(res["session"]["current_theta"], 0.5)

    def test_cat_adaptive_convergence_and_classification(self) -> None:
        """Simulates consecutive correct answers until convergence, verifying mastery band."""
        session = cat_engine_service.start_cat_session(
            student_id="stu_high_performer",
            subject="গণিত",
            initial_theta=0.0
        )
        session_id = session["session_id"]

        # Answer items correctly until test terminates
        for _ in range(8):
            active_item = session.get("current_item")
            if not active_item or session.get("is_complete"):
                break

            item_id = active_item["item_id"]
            meta = next(it for it in cat_engine_service.CALIBRATED_ITEM_BANK if it["item_id"] == item_id)
            res = cat_engine_service.submit_cat_answer(session_id, item_id, meta["correct_option_id"])
            session = res["session"]

        final_session = cat_engine_service.get_session(session_id)
        self.assertTrue(final_session["is_complete"])
        self.assertIsNotNone(final_session["final_ability_category"])
        self.assertIn("দক্ষতা", final_session["final_ability_category"])

    def test_cat_rejects_empty_option_and_mismatched_item(self) -> None:
        """Verifies validation guards for empty option and invalid item IDs."""
        session = cat_engine_service.start_cat_session("stu_err_test")
        session_id = session["session_id"]
        active_item_id = session["current_item"]["item_id"]

        # Empty option
        res_empty = cat_engine_service.submit_cat_answer(session_id, active_item_id, "")
        self.assertFalse(res_empty["success"])
        self.assertIn("অপশন নির্বাচন", res_empty["message"])

        # Mismatched item_id
        res_mismatch = cat_engine_service.submit_cat_answer(session_id, "wrong_item_id", "a")
        self.assertFalse(res_mismatch["success"])
        self.assertIn("মিলছে না", res_mismatch["message"])

    def test_cat_handles_nan_and_inf_initial_theta(self) -> None:
        """Verifies float('nan') or float('inf') are safely sanitized to 0.0."""
        session_nan = cat_engine_service.start_cat_session("stu_nan", initial_theta=float("nan"))
        self.assertEqual(session_nan["current_theta"], 0.0)

        session_inf = cat_engine_service.start_cat_session("stu_inf", initial_theta=float("inf"))
        self.assertEqual(session_inf["current_theta"], 0.0)

    # --------------------------------------------------------------------------
    # Curriculum Blueprint Composer Tests
    # --------------------------------------------------------------------------

    def test_blueprint_compose_successful_and_allocations_match_total(self) -> None:
        """Verifies balanced blueprint creation and exact item allocations."""
        res = blueprint_composer_service.compose_blueprint(
            name="এসএসসি গণিত মডেল টেস্ট ২০২৬",
            subject="গণিত",
            class_grade=10,
            total_questions=30,
            duration_minutes=30,
            cognitive_distribution={
                "knowledge": 30.0,
                "comprehension": 40.0,
                "application": 20.0,
                "higher_order": 10.0,
            },
            chapter_distribution={
                "বাস্তব সংখ্যা": 20.0,
                "বীজগণিতীয় রাশি": 30.0,
                "জ্যামিতি": 30.0,
                "ত্রিকোণমিতি": 20.0,
            },
            negative_marking=0.0
        )

        self.assertTrue(res["success"])
        bp = res["blueprint"]
        self.assertEqual(bp["name"], "এসএসসি গণিত মডেল টেস্ট ২০২৬")
        self.assertEqual(bp["total_questions"], 30)
        self.assertEqual(bp["validation_status"], "APPROVED_BALANCED")

        # Sum of exact item allocations must equal total_questions exactly
        allocations = bp["exact_item_allocation"]
        self.assertEqual(sum(allocations.values()), 30)

    def test_blueprint_compose_rejects_non_100_percent_sums(self) -> None:
        """Verifies that distributions not summing to ~100% are rejected."""
        res = blueprint_composer_service.compose_blueprint(
            name="ভুল ব্লুপ্রিন্ট",
            subject="পদার্থবিজ্ঞান",
            class_grade=11,
            total_questions=20,
            duration_minutes=20,
            cognitive_distribution={
                "knowledge": 50.0,
                "comprehension": 20.0,  # Sum = 70%, invalid!
            },
            chapter_distribution={
                "ভেক্টর": 100.0,
            }
        )

        self.assertFalse(res["success"])
        self.assertIn("মোট হার ১০০% হতে হবে", res["message"])

    def test_blueprint_compose_rejects_negative_percentages(self) -> None:
        """Verifies that negative percentage values are rejected even if sum is 100%."""
        res = blueprint_composer_service.compose_blueprint(
            name="ঋণাত্মক ব্লুপ্রিন্ট",
            subject="রসায়ন",
            class_grade=9,
            total_questions=25,
            duration_minutes=25,
            cognitive_distribution={
                "knowledge": -10.0,
                "comprehension": 110.0,  # Sum is 100%, but negative is illegal!
            },
            chapter_distribution={
                "পরমাণুর গঠন": 100.0,
            }
        )

        self.assertFalse(res["success"])
        self.assertIn("ঋণাত্মক হতে পারবে না", res["message"])

    def test_blueprint_compose_validates_duration_and_negative_marking_bounds(self) -> None:
        """Verifies constraints on exam duration and negative marking values."""
        # Duration too short (< 5 mins)
        res_time = blueprint_composer_service.compose_blueprint(
            name="দ্রুত টেস্ট",
            subject="বাংলা",
            class_grade=8,
            total_questions=10,
            duration_minutes=2,
            cognitive_distribution={"knowledge": 100.0},
            chapter_distribution={"গদ্য": 100.0}
        )
        self.assertFalse(res_time["success"])
        self.assertIn("কমপক্ষে ৫ মিনিট", res_time["message"])

        # Negative marking > 1.0
        res_neg = blueprint_composer_service.compose_blueprint(
            name="অতিরিক্ত পেনাল্টি",
            subject="বাংলা",
            class_grade=8,
            total_questions=10,
            duration_minutes=15,
            cognitive_distribution={"knowledge": 100.0},
            chapter_distribution={"গদ্য": 100.0},
            negative_marking=1.5
        )
        self.assertFalse(res_neg["success"])
        self.assertIn("০.০ থেকে ১.০", res_neg["message"])

    def test_blueprint_presets_are_available(self) -> None:
        """Verifies that standard preset blueprints are loaded and accessible."""
        presets = blueprint_composer_service.list_presets()
        self.assertGreaterEqual(len(presets), 2)

        preset_ids = [p["blueprint_id"] for p in presets]
        self.assertIn("nctb_class8_math", preset_ids)
        self.assertIn("du_admission_ka_physics", preset_ids)

        du_bp = blueprint_composer_service.get_blueprint("du_admission_ka_physics")
        self.assertIsNotNone(du_bp)
        self.assertEqual(du_bp["negative_marking"], 0.25)


if __name__ == "__main__":
    unittest.main()
