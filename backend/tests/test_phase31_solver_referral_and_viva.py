"""
Unit and Integration Test Suite: Phase 31
Verifies:
1. MathProblemSolverService (stepwise LaTeX derivations, intermediate misconception detection, Socratic hints)
2. AlumniReferralNetworkService (campus alumni graph, HMAC referral tokens, quota limits, anti-duplicate controls)
3. VoiceVivaSimulatorService (oral viva session lifecycle, WPM cadence scoring, latency telemetry, summary reports)
4. Section 30 REST Routes in router.py
"""

import unittest
from backend.app.services.math_problem_solver_service import (
    MathProblemSolverService,
    math_problem_solver_service
)
from backend.app.services.alumni_referral_network_service import (
    AlumniReferralNetworkService,
    alumni_referral_network_service
)
from backend.app.services.voice_viva_simulator_service import (
    VoiceVivaSimulatorService,
    voice_viva_simulator_service
)
from backend.app.schemas.solver_referral_and_viva_schema import (
    SolveMathStepwiseRequest,
    DiagnoseMisconceptionRequest,
    CreateReferralEndorsementRequest,
    StartVivaSessionRequest,
    SubmitAudioVivaResponseRequest
)
from backend.app.api.v1.router import (
    solve_mathematical_problem_stepwise,
    diagnose_student_derivation_step,
    list_verified_alumni_directory,
    issue_alumni_referral_endorsement,
    verify_alumni_referral_token,
    start_voice_viva_session,
    submit_viva_audio_response,
    get_viva_session_report
)


class TestPhase31SolverReferralAndViva(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.math_service = MathProblemSolverService()
        self.referral_service = AlumniReferralNetworkService()
        self.viva_service = VoiceVivaSimulatorService()

    # -------------------------------------------------------------------------
    # 1. MathProblemSolverService Tests
    # -------------------------------------------------------------------------
    def test_solve_stepwise_calculus_product_rule(self):
        sol = self.math_service.solve_stepwise(
            problem_statement="Find derivative of x^2 * sin(x)",
            topic_domain="CALCULUS"
        )
        self.assertEqual(sol["problem_id"], "prob-calc-prod-01")
        self.assertEqual(sol["topic_domain"], "CALCULUS")
        self.assertEqual(sol["total_steps"], 3)
        self.assertIn(r"\sin(x)", sol["initial_expression_latex"])
        self.assertIn("Product Rule", sol["steps"][0]["rule_applied"])

    def test_solve_stepwise_integration_by_parts(self):
        sol = self.math_service.solve_stepwise(
            problem_statement="Integration by parts for x * e^x dx",
            topic_domain="CALCULUS"
        )
        self.assertEqual(sol["problem_id"], "prob-calc-byparts-02")
        self.assertIn(r"\int x e^x", sol["initial_expression_latex"])
        self.assertEqual(sol["total_steps"], 3)

    def test_solve_stepwise_generic_expression_sanitized(self):
        # Expression containing non-math characters
        sol = self.math_service.solve_stepwise(
            problem_statement="d/dx of polynomial; <script>alert(1)</script>",
            topic_domain="CALCULUS"
        )
        self.assertTrue(sol["verified"])
        self.assertNotIn("<script>", sol["initial_expression_latex"])
        self.assertGreaterEqual(sol["total_steps"], 2)

    def test_diagnose_step_misconception_detection(self):
        # Test product rule omission misconception on prob-calc-prod-01
        res = self.math_service.diagnose_step(
            problem_id="prob-calc-prod-01",
            step_number=2,
            student_derived_latex=r"f'(x) = 2x \cos(x)"
        )
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["misconception_type"], "CHAIN_RULE_OMISSION")
        self.assertIn("Product Rule", res["diagnostic_feedback"])
        self.assertIn("socratic_hint", res)

    def test_diagnose_step_valid_intermediate(self):
        res = self.math_service.diagnose_step(
            problem_id="prob-calc-prod-01",
            step_number=1,
            student_derived_latex=r"\frac{d}{dx}[u \cdot v] = u'v + uv'"
        )
        self.assertTrue(res["is_valid"])
        self.assertIsNone(res["misconception_type"])

    # -------------------------------------------------------------------------
    # 2. AlumniReferralNetworkService Tests
    # -------------------------------------------------------------------------
    def test_alumni_directory_and_filter(self):
        all_alumni = self.referral_service.get_alumni_directory()
        self.assertGreaterEqual(len(all_alumni), 4)

        goog_alumni = self.referral_service.get_alumni_directory(company_filter="Google")
        self.assertEqual(len(goog_alumni), 1)
        self.assertEqual(goog_alumni[0]["company"], "Google")

    def test_issue_referral_endorsement_and_token(self):
        alumni = self.referral_service.get_alumni_directory(company_filter="Google")[0]
        ref = self.referral_service.issue_referral_endorsement(
            alumni_id=alumni["alumni_id"],
            student_id="std-talent-01",
            student_name="Zubair Al Mahmud",
            target_role="Associate Cloud Solutions Architect",
            endorsement_notes="Demonstrated 98.4% algorithmic problem-solving ability in competitive arena."
        )
        self.assertTrue(ref["referral_id"].startswith("REF-"))
        self.assertEqual(ref["target_company"], "Google")
        self.assertTrue(ref["endorsement_token"].startswith("AGROREF|"))
        self.assertEqual(ref["status"], "ISSUED")

    def test_duplicate_referral_same_company_rejected(self):
        alumni = self.referral_service.get_alumni_directory(company_filter="Google")[0]
        self.referral_service.issue_referral_endorsement(
            alumni_id=alumni["alumni_id"],
            student_id="std-dup-01",
            student_name="Duplicate Candidate",
            target_role="Software Engineer"
        )
        # Attempt second referral for same company by same student
        with self.assertRaises(ValueError):
            self.referral_service.issue_referral_endorsement(
                alumni_id=alumni["alumni_id"],
                student_id="std-dup-01",
                student_name="Duplicate Candidate",
                target_role="Site Reliability Engineer"
            )

    def test_verify_referral_token_authentic_and_tampered(self):
        alumni = self.referral_service.get_alumni_directory(company_filter="bKash")[0]
        ref = self.referral_service.issue_referral_endorsement(
            alumni_id=alumni["alumni_id"],
            student_id="std-ver-01",
            student_name="Nafisa Tabassum",
            target_role="Junior Fintech Backend Engineer"
        )
        token = ref["endorsement_token"]

        # Authentic Token
        ver = self.referral_service.verify_referral_token(token)
        self.assertTrue(ver["is_valid"])
        self.assertEqual(ver["status"], "AUTHENTIC")
        self.assertEqual(ver["referral"]["student_name"], "Nafisa Tabassum")

        # Tampered Token
        tampered_token = token[:-4] + "DEAD"
        ver_tampered = self.referral_service.verify_referral_token(tampered_token)
        self.assertFalse(ver_tampered["is_valid"])
        self.assertEqual(ver_tampered["status"], "TAMPERED_SIGNATURE")

    def test_advance_referral_status(self):
        alumni = self.referral_service.get_alumni_directory(company_filter="Pathao")[0]
        ref = self.referral_service.issue_referral_endorsement(
            alumni_id=alumni["alumni_id"],
            student_id="std-stage-01",
            student_name="Arman Hossain",
            target_role="Machine Learning Intern"
        )
        adv = self.referral_service.advance_referral_status(ref["referral_id"], "INTERVIEW_SCHEDULED")
        self.assertEqual(adv["status"], "INTERVIEW_SCHEDULED")

    # -------------------------------------------------------------------------
    # 3. VoiceVivaSimulatorService Tests
    # -------------------------------------------------------------------------
    def test_start_viva_session_categories(self):
        sess_tech = self.viva_service.start_session("std-101", "TECH_BACKEND", "INTERMEDIATE")
        self.assertTrue(sess_tech["session_id"].startswith("viva-sess-"))
        self.assertEqual(sess_tech["viva_category"], "TECH_BACKEND")
        self.assertGreaterEqual(len(sess_tech["questions"]), 2)

        sess_bcs = self.viva_service.start_session("std-101", "BCS_ORAL", "HARD")
        self.assertEqual(sess_bcs["viva_category"], "BCS_ORAL")

    def test_evaluate_response_optimal_cadence(self):
        sess = self.viva_service.start_session("std-101", "TECH_BACKEND")
        q_id = sess["questions"][0]["question_id"]
        # Transcribe ~35 words in 15 seconds -> ~140 WPM (OPTIMAL)
        sample_text = (
            "A B-Tree index maintains logarithmic lookup efficiency by keeping nodes balanced. "
            "When a node exceeds capacity, a node split occurs, preserving O(log n) disk page reads."
        )
        ev = self.viva_service.evaluate_response(
            session_id=sess["session_id"],
            question_id=q_id,
            audio_duration_seconds=10.0,
            transcribed_text=sample_text,
            response_latency_seconds=2.1
        )
        self.assertEqual(ev["cadence_rating"], "OPTIMAL")
        self.assertGreaterEqual(ev["fluency_score"], 85.0)
        self.assertGreaterEqual(ev["precision_score"], 60.0)

    def test_evaluate_response_zero_duration_safe(self):
        sess = self.viva_service.start_session("std-101", "TECH_BACKEND")
        q_id = sess["questions"][0]["question_id"]
        # Defensive check against division by zero
        ev = self.viva_service.evaluate_response(
            session_id=sess["session_id"],
            question_id=q_id,
            audio_duration_seconds=0.0,
            transcribed_text="Brief response",
            response_latency_seconds=1.0
        )
        self.assertIsNotNone(ev)
        self.assertIn("cadence_rating", ev)

    def test_get_session_summary_aggregation(self):
        sess = self.viva_service.start_session("std-101", "TECH_BACKEND")
        q_id = sess["questions"][0]["question_id"]
        self.viva_service.evaluate_response(
            session_id=sess["session_id"],
            question_id=q_id,
            audio_duration_seconds=12.0,
            transcribed_text="B-Tree indexing balances nodes with logarithmic lookup.",
            response_latency_seconds=2.0
        )
        summary = self.viva_service.get_session_summary(sess["session_id"])
        self.assertEqual(summary["session_id"], sess["session_id"])
        self.assertGreater(summary["overall_score"], 0.0)
        self.assertEqual(len(summary["question_evaluations"]), 1)

    # -------------------------------------------------------------------------
    # 4. Section 30 REST Endpoints Tests
    # -------------------------------------------------------------------------
    async def test_router_math_solve_and_diagnose(self):
        req = SolveMathStepwiseRequest(
            problem_statement="Solve derivative of x^2 * sin(x)",
            topic_domain="CALCULUS"
        )
        res = await solve_mathematical_problem_stepwise(req)
        self.assertEqual(res["problem_id"], "prob-calc-prod-01")

        diag_req = DiagnoseMisconceptionRequest(
            problem_id="prob-calc-prod-01",
            step_number=2,
            student_derived_latex=r"f'(x) = 2x \cos(x)"
        )
        diag_res = await diagnose_student_derivation_step(diag_req)
        self.assertFalse(diag_res["is_valid"])

    async def test_router_referral_endorse_and_verify(self):
        alumni = (await list_verified_alumni_directory("Google"))[0]
        req = CreateReferralEndorsementRequest(
            alumni_id=alumni["alumni_id"],
            student_id="std-api-ref",
            student_name="Zubair",
            target_role="Cloud Engineer"
        )
        ref_res = await issue_alumni_referral_endorsement(req)
        self.assertEqual(ref_res["status"], "ISSUED")

        ver_res = await verify_alumni_referral_token(ref_res["endorsement_token"])
        self.assertTrue(ver_res["is_valid"])

    async def test_router_viva_session_lifecycle(self):
        start_req = StartVivaSessionRequest(
            student_id="std-api-viva",
            viva_category="BCS_ORAL"
        )
        sess = await start_voice_viva_session(start_req)
        self.assertEqual(sess["viva_category"], "BCS_ORAL")

        submit_req = SubmitAudioVivaResponseRequest(
            session_id=sess["session_id"],
            question_id=sess["questions"][0]["question_id"],
            audio_duration_seconds=20.0,
            transcribed_text="Graduation from LDC impacts tariff preferences under WTO GSP rules.",
            response_latency_seconds=2.5
        )
        eval_res = await submit_viva_audio_response(sess["session_id"], submit_req)
        self.assertIn("cadence_rating", eval_res)

        rep = await get_viva_session_report(sess["session_id"])
        self.assertEqual(rep["session_id"], sess["session_id"])


if __name__ == "__main__":
    unittest.main()
