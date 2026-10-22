"""
================================================================================
TEST SUITE: Phase 64 Automated Exam Grading, Handwritten Script OCR & Multi-Evaluator Moderation
PURPOSE: Comprehensive unit & integration testing for Script Segmentation, Rubrics,
         15% Divergence Threshold Arbitration, and Cryptographic Re-Scrutiny.
================================================================================
"""

import unittest
from backend.app.services.automated_grading_moderation_service import AutomatedGradingModerationService
from backend.app.schemas.automated_grading_moderation_schema import (
    BoundingBoxDTO,
    RubricCriterionDTO,
    RubricStepDTO
)


class TestPhase64AutomatedGradingModeration(unittest.TestCase):

    def setUp(self):
        self.service = AutomatedGradingModerationService(
            hmac_secret_key="test_board_examination_secret_key_2026"
        )

    def test_01_script_upload_default_boxes(self):
        res = self.service.upload_and_segment_script(
            script_id="script_hsc_101",
            student_id="student_sakib_01",
            exam_id="hsc_math_2026",
            subject="Higher Mathematics",
            total_pages=2
        )
        self.assertEqual(res["script_id"], "script_hsc_101")
        self.assertEqual(res["status"], "SEGMENTED")
        self.assertEqual(res["total_boxes_detected"], 4)
        self.assertGreaterEqual(res["avg_confidence"], 0.90)
        self.assertTrue(any(b["sub_question_tag"] == "Q1.a" for b in res["bounding_boxes"]))

    def test_02_custom_bounding_boxes(self):
        custom = [
            BoundingBoxDTO(
                box_id="c_box_1",
                page_number=1,
                x_min=0.1,
                y_min=0.1,
                x_max=0.8,
                y_max=0.4,
                sub_question_tag="Q2.a",
                confidence_score=0.98,
                recognized_text="d/dx(sin x) = cos x",
                formula_detected=True
            )
        ]
        res = self.service.upload_and_segment_script(
            script_id="script_custom_01",
            student_id="student_fahim_02",
            exam_id="hsc_math_2026",
            custom_bounding_boxes=custom
        )
        self.assertEqual(res["total_boxes_detected"], 1)
        self.assertEqual(res["avg_confidence"], 0.98)
        self.assertEqual(res["bounding_boxes"][0]["sub_question_tag"], "Q2.a")

    def test_03_rubric_evaluation_with_steps(self):
        criteria = [
            RubricCriterionDTO(
                criterion_id="Q1.b",
                sub_question="Question 1 (b)",
                max_marks=4.0,
                steps=[
                    RubricStepDTO(step_number=1, step_description="Integration by parts formula", max_marks=1.0),
                    RubricStepDTO(step_number=2, step_description="u and v substitution", max_marks=1.0),
                    RubricStepDTO(step_number=3, step_description="Evaluation of integral", max_marks=2.0)
                ]
            )
        ]
        res = self.service.evaluate_rubric(
            script_id="script_hsc_101",
            criteria=criteria,
            evaluator_role="AI_PRE_GRADER",
            evaluator_id="ai_grader_v2"
        )
        self.assertEqual(res["script_id"], "script_hsc_101")
        self.assertEqual(res["max_possible"], 4.0)
        self.assertGreater(res["total_score"], 0.0)
        self.assertLessEqual(res["total_score"], 4.0)
        self.assertEqual(len(res["criterion_scores"][0]["step_breakdown"]), 3)

    def test_04_rubric_evaluation_single_step_fallback(self):
        criteria = [
            RubricCriterionDTO(
                criterion_id="Q1.a",
                sub_question="Question 1 (a)",
                max_marks=2.0,
                steps=[]
            )
        ]
        res = self.service.evaluate_rubric(
            script_id="script_hsc_101",
            criteria=criteria
        )
        self.assertEqual(res["max_possible"], 2.0)
        self.assertGreater(res["total_score"], 0.0)

    def test_05_record_examiner_score_examiner_1(self):
        res = self.service.record_examiner_score(
            script_id="script_hsc_101",
            examiner_id="examiner_nasir",
            examiner_role="EXAMINER_1",
            subquestion_marks={"Q1.a": 2.0, "Q1.b": 3.5, "Q1.c": 4.0, "Q1.d": 3.5},
            examiner_feedback="Clean mathematical derivation"
        )
        self.assertEqual(res["script_id"], "script_hsc_101")
        self.assertEqual(res["total_marks"], 13.0)
        self.assertEqual(res["examiner_role"], "EXAMINER_1")

    def test_06_record_examiner_score_invalid_role(self):
        with self.assertRaises(ValueError):
            self.service.record_examiner_score(
                script_id="script_hsc_101",
                examiner_id="user_unknown",
                examiner_role="STUDENT_PEER",
                subquestion_marks={"Q1.a": 2.0}
            )

    def test_07_moderation_audit_single_examiner_pending(self):
        self.service.record_examiner_score(
            script_id="script_pending_01",
            examiner_id="ex_1",
            examiner_role="EXAMINER_1",
            subquestion_marks={"Q1": 75.0}
        )
        audit = self.service.get_moderation_audit("script_pending_01")
        self.assertEqual(audit["status"], "PENDING_EVALUATION")
        self.assertIsNone(audit["divergence_percentage"])
        self.assertFalse(audit["arbiter_required"])

    def test_08_moderation_harmonized_within_15_percent(self):
        # Examiner 1: 80 marks, Examiner 2: 74 marks -> diff = 6 marks (6%) <= 15%
        self.service.record_examiner_score(
            script_id="script_harm_01",
            examiner_id="ex_1",
            examiner_role="EXAMINER_1",
            subquestion_marks={"Q1": 80.0}
        )
        self.service.record_examiner_score(
            script_id="script_harm_01",
            examiner_id="ex_2",
            examiner_role="EXAMINER_2",
            subquestion_marks={"Q1": 74.0}
        )
        audit = self.service.get_moderation_audit("script_harm_01")
        self.assertEqual(audit["status"], "HARMONIZED")
        self.assertEqual(audit["score_difference"], 6.0)
        self.assertEqual(audit["divergence_percentage"], 6.0)
        self.assertFalse(audit["divergence_threshold_exceeded"])
        self.assertFalse(audit["arbiter_required"])
        self.assertEqual(audit["final_moderated_score"], 77.0)

    def test_09_moderation_exact_15_percent_threshold(self):
        # Examiner 1: 85 marks, Examiner 2: 70 marks -> diff = 15 marks (15.0%) <= 15%
        self.service.record_examiner_score(
            script_id="script_border_15",
            examiner_id="ex_1",
            examiner_role="EXAMINER_1",
            subquestion_marks={"Q1": 85.0}
        )
        self.service.record_examiner_score(
            script_id="script_border_15",
            examiner_id="ex_2",
            examiner_role="EXAMINER_2",
            subquestion_marks={"Q1": 70.0}
        )
        audit = self.service.get_moderation_audit("script_border_15")
        self.assertEqual(audit["status"], "HARMONIZED")
        self.assertFalse(audit["divergence_threshold_exceeded"])
        self.assertEqual(audit["final_moderated_score"], 77.5)

    def test_10_moderation_divergence_exceeds_15_triggers_arbiter(self):
        # Examiner 1: 88 marks, Examiner 2: 66 marks -> diff = 22 marks (22%) > 15%
        self.service.record_examiner_score(
            script_id="script_div_01",
            examiner_id="ex_1",
            examiner_role="EXAMINER_1",
            subquestion_marks={"Q1": 88.0}
        )
        self.service.record_examiner_score(
            script_id="script_div_01",
            examiner_id="ex_2",
            examiner_role="EXAMINER_2",
            subquestion_marks={"Q1": 66.0}
        )
        audit = self.service.get_moderation_audit("script_div_01")
        self.assertEqual(audit["status"], "NEEDS_ARBITRATION")
        self.assertTrue(audit["divergence_threshold_exceeded"])
        self.assertTrue(audit["arbiter_required"])
        self.assertIsNone(audit["final_moderated_score"])

    def test_11_arbitration_resolution_closer_to_examiner_1(self):
        # Ex 1: 88, Ex 2: 66, Arbiter: 86 (closer to Ex 1: diff 2 vs diff 20)
        self.service.record_examiner_score("script_arb_01", "ex_1", "EXAMINER_1", {"Q1": 88.0})
        self.service.record_examiner_score("script_arb_01", "ex_2", "EXAMINER_2", {"Q1": 66.0})
        self.service.record_examiner_score("script_arb_01", "head_arbiter", "ARBITER_3", {"Q1": 86.0})

        audit = self.service.get_moderation_audit("script_arb_01")
        self.assertEqual(audit["status"], "ARBITRATED")
        self.assertFalse(audit["arbiter_required"])
        # Expected score: average of Arbiter (86) and Ex 1 (88) = 87.0
        self.assertEqual(audit["final_moderated_score"], 87.0)

    def test_12_arbitration_resolution_closer_to_examiner_2(self):
        # Ex 1: 90, Ex 2: 65, Arbiter: 68 (closer to Ex 2: diff 3 vs diff 22)
        self.service.record_examiner_score("script_arb_02", "ex_1", "EXAMINER_1", {"Q1": 90.0})
        self.service.record_examiner_score("script_arb_02", "ex_2", "EXAMINER_2", {"Q1": 65.0})
        self.service.record_examiner_score("script_arb_02", "head_arbiter", "ARBITER_3", {"Q1": 68.0})

        audit = self.service.get_moderation_audit("script_arb_02")
        self.assertEqual(audit["status"], "ARBITRATED")
        # Expected score: average of Arbiter (68) and Ex 2 (65) = 66.5
        self.assertEqual(audit["final_moderated_score"], 66.5)

    def test_13_arbitration_resolution_equidistant(self):
        # Ex 1: 90, Ex 2: 70, Arbiter: 80 (diff 10 from both)
        self.service.record_examiner_score("script_arb_03", "ex_1", "EXAMINER_1", {"Q1": 90.0})
        self.service.record_examiner_score("script_arb_03", "ex_2", "EXAMINER_2", {"Q1": 70.0})
        self.service.record_examiner_score("script_arb_03", "head_arbiter", "ARBITER_3", {"Q1": 80.0})

        audit = self.service.get_moderation_audit("script_arb_03")
        self.assertEqual(audit["status"], "ARBITRATED")
        self.assertEqual(audit["final_moderated_score"], 80.0)

    def test_14_rescrutiny_accurate_addition_seal(self):
        self.service.upload_and_segment_script("script_rescrutiny_01", "st_1", "hsc_math")
        self.service.record_examiner_score(
            script_id="script_rescrutiny_01",
            examiner_id="ex_1",
            examiner_role="EXAMINER_1",
            subquestion_marks={"Q1.a": 2.0, "Q1.b": 4.0, "Q1.c": 4.0, "Q1.d": 4.0}
        )
        audit = self.service.perform_rescrutiny("script_rescrutiny_01")
        self.assertFalse(audit["addition_error_found"])
        self.assertEqual(audit["unmarked_questions_count"], 0)
        self.assertFalse(audit["is_grade_changed"])
        self.assertIn("Grade Retained", audit["audit_verdict"])
        self.assertTrue(len(audit["tamper_seal_hash"]) == 64)

    def test_15_rescrutiny_detects_addition_discrepancy(self):
        # Manually seed an examiner score with deliberate math error in sum
        self.service._examiner_scores["script_math_err"] = {
            "EXAMINER_1": {
                "examiner_id": "careless_ex",
                "subquestion_marks": {"Q1.a": 2.0, "Q1.b": 4.0, "Q1.c": 4.0, "Q1.d": 4.0},
                "total_marks": 12.0  # Real sum is 14.0!
            }
        }
        audit = self.service.perform_rescrutiny("script_math_err")
        self.assertTrue(audit["addition_error_found"])
        self.assertTrue(audit["is_grade_changed"])
        self.assertEqual(audit["original_marks"], 12.0)
        self.assertEqual(audit["revised_marks"], 14.0)
        self.assertIn("Grade Changed", audit["audit_verdict"])

    def test_16_rescrutiny_detects_unmarked_questions(self):
        self.service.upload_and_segment_script("script_unmarked_01", "st_2", "hsc_math")
        # Examiner only marked Q1.a and Q1.b, missing Q1.c and Q1.d
        self.service.record_examiner_score(
            script_id="script_unmarked_01",
            examiner_id="ex_1",
            examiner_role="EXAMINER_1",
            subquestion_marks={"Q1.a": 2.0, "Q1.b": 4.0}
        )
        audit = self.service.perform_rescrutiny("script_unmarked_01")
        self.assertEqual(audit["unmarked_questions_count"], 2)
        self.assertTrue(audit["is_grade_changed"])
        self.assertIn("Investigation Flagged", audit["audit_verdict"])

    def test_17_cohort_distribution_default(self):
        dist = self.service.get_cohort_distribution("hsc_math_empty")
        self.assertEqual(dist["total_scripts_evaluated"], 5)
        self.assertGreater(dist["mean_score"], 0.0)
        self.assertGreater(dist["std_deviation"], 0.0)
        self.assertIsInstance(dist["outlier_scripts"], list)

    def test_18_cohort_distribution_with_live_scripts(self):
        # Add 3 scripts to exam
        for i, val in enumerate([90.0, 85.0, 80.0]):
            sid = f"script_live_{i}"
            self.service.upload_and_segment_script(sid, f"st_{i}", "exam_live_99")
            self.service.record_examiner_score(sid, "ex_1", "EXAMINER_1", {"Q1": val})
            self.service.record_examiner_score(sid, "ex_2", "EXAMINER_2", {"Q1": val})

        dist = self.service.get_cohort_distribution("exam_live_99")
        self.assertEqual(dist["total_scripts_evaluated"], 3)
        self.assertEqual(dist["mean_score"], 85.0)
        self.assertEqual(dist["highest_score"], 90.0)
        self.assertEqual(dist["lowest_score"], 80.0)

    def test_19_cohort_outlier_z_score_detection(self):
        # Populate exam with normal distribution + 1 extreme outlier
        for i in range(10):
            sid = f"script_norm_{i}"
            self.service.upload_and_segment_script(sid, f"st_norm_{i}", "exam_z_score")
            self.service.record_examiner_score(sid, "ex_1", "EXAMINER_1", {"Q1": 70.0 + (i % 3)})
            self.service.record_examiner_score(sid, "ex_2", "EXAMINER_2", {"Q1": 70.0 + (i % 3)})

        # Outlier script
        self.service.upload_and_segment_script("script_outlier_low", "st_low", "exam_z_score")
        self.service.record_examiner_score("script_outlier_low", "ex_1", "EXAMINER_1", {"Q1": 5.0})
        self.service.record_examiner_score("script_outlier_low", "ex_2", "EXAMINER_2", {"Q1": 5.0})

        dist = self.service.get_cohort_distribution("exam_z_score")
        self.assertTrue(any(o["script_id"] == "script_outlier_low" for o in dist["outlier_scripts"]))

    def test_20_tamper_seal_cryptographic_uniqueness(self):
        self.service.upload_and_segment_script("script_seal_1", "st_a", "math")
        self.service.upload_and_segment_script("script_seal_2", "st_b", "math")
        res1 = self.service.perform_rescrutiny("script_seal_1")
        res2 = self.service.perform_rescrutiny("script_seal_2")
        self.assertNotEqual(res1["tamper_seal_hash"], res2["tamper_seal_hash"])


if __name__ == "__main__":
    unittest.main()
