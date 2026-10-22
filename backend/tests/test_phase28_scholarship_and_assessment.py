# ============================================================================
# MODULE: PHASE 28 VERIFICATION SUITE
# TOPIC: Micro-Scholarships, bKash Auto-Disbursement, ATS Resume Scorer & Coding Arena
# FILE: backend/tests/test_phase28_scholarship_and_assessment.py
# PURPOSE: Validate end-to-end functionality, ASVS L2 financial integrity,
#          concurrency double-disbursement guards, and REST contracts for Phase 28.
# STANDARDS: Unittest, OWASP ASVS L2, Sandbox Security Verification
# AUDIENCE: QA Engineers, Core Backend Engineers, Security Reviewers
# ============================================================================

import unittest
from backend.app.services.scholarship_endowment_service import ScholarshipEndowmentService
from backend.app.services.technical_assessment_service import TechnicalAssessmentService
from backend.app.schemas.scholarship_and_assessment_schema import (
    CreateEndowmentFundRequest,
    ApplyScholarshipRequest,
    DisburseScholarshipRequest,
    ATSResumeAnalysisRequest,
    SubmitTechnicalAssessmentRequest
)


class TestScholarshipEndowmentService(unittest.TestCase):
    """Unit tests verifying micro-scholarship endowment fund creation, scoring & payouts."""

    def setUp(self):
        self.service = ScholarshipEndowmentService()

    def test_create_endowment_fund_success(self):
        fund = self.service.create_endowment_fund(
            sponsor_id="spn-beximco",
            sponsor_name="Beximco Pharma Foundation",
            fund_title="Medical & Pharma Research Stipend",
            total_grant_bdt=120000.0,
            target_criteria="UNDERPRIVILEGED_STEM",
            disbursement_per_student_bdt=3000.0
        )
        self.assertTrue(fund["fund_id"].startswith("fund-"))
        self.assertEqual(fund["sponsor_name"], "Beximco Pharma Foundation")
        self.assertEqual(fund["total_grant_bdt"], 120000.0)
        self.assertEqual(fund["remaining_bdt"], 120000.0)
        self.assertEqual(fund["awarded_count"], 0)
        self.assertEqual(fund["status"], "ACTIVE")

    def test_create_endowment_fund_validation_errors(self):
        with self.assertRaises(ValueError):
            self.service.create_endowment_fund(
                sponsor_id="spn-01",
                sponsor_name="Sponsor",
                fund_title="",
                total_grant_bdt=50000.0
            )

        with self.assertRaises(ValueError):
            self.service.create_endowment_fund(
                sponsor_id="spn-01",
                sponsor_name="Sponsor",
                fund_title="Valid Title",
                total_grant_bdt=-1000.0  # negative
            )

        with self.assertRaises(ValueError):
            self.service.create_endowment_fund(
                sponsor_id="spn-01",
                sponsor_name="Sponsor",
                fund_title="Valid Title",
                total_grant_bdt=50000.0,
                disbursement_per_student_bdt=60000.0  # exceeds total
            )

    def test_list_endowment_funds_criteria_filtering(self):
        funds = self.service.list_endowment_funds(criteria="FEMALE_TECH")
        self.assertGreaterEqual(len(funds), 1)
        self.assertEqual(funds[0]["target_criteria"], "FEMALE_TECH")
        self.assertEqual(funds[0]["sponsor_name"], "Grameenphone Future-Leaders")

    def test_apply_scholarship_need_index_and_composite(self):
        # Underprivileged student (income <= 15k -> need_index = 100.0)
        app = self.service.apply_for_scholarship(
            fund_id="fund-pathao-stem-01",
            student_id="student-poor-01",
            student_name="Abdullah Al Mamun",
            family_monthly_income_bdt=12000.0,
            institution_name="Rangpur Govt College",
            cat_ability_theta=1.8,
            reputation_score=850.0,
            bkash_number="01711223344",
            statement_of_need="Need financial support to buy engineering books."
        )
        self.assertEqual(app["need_index"], 100.0)
        self.assertGreaterEqual(app["composite_score"], 75.0)
        self.assertEqual(app["status"], "APPROVED")
        self.assertEqual(app["grant_amount_bdt"], 3000.0)

    def test_apply_scholarship_invalid_bkash_number(self):
        with self.assertRaises(ValueError):
            self.service.apply_for_scholarship(
                fund_id="fund-pathao-stem-01",
                student_id="student-test",
                student_name="Test Student",
                family_monthly_income_bdt=20000.0,
                institution_name="Dhaka College",
                bkash_number="12345"  # invalid
            )

    def test_apply_scholarship_duplicate_blocked(self):
        # First application succeeds
        self.service.apply_for_scholarship(
            fund_id="fund-pathao-stem-01",
            student_id="student-dup-01",
            student_name="Dup Student",
            family_monthly_income_bdt=18000.0,
            institution_name="Dhaka College",
            bkash_number="01811223344"
        )
        # Duplicate application to the same fund must fail
        with self.assertRaises(ValueError):
            self.service.apply_for_scholarship(
                fund_id="fund-pathao-stem-01",
                student_id="student-dup-01",
                student_name="Dup Student",
                family_monthly_income_bdt=18000.0,
                institution_name="Dhaka College",
                bkash_number="01811223344"
            )

    def test_disburse_scholarship_success_and_sha256_ledger(self):
        app = self.service.apply_for_scholarship(
            fund_id="fund-buet89-relief-03",
            student_id="student-buet-relief",
            student_name="Sabbir Ahmed",
            family_monthly_income_bdt=14000.0,
            institution_name="BUET",
            cat_ability_theta=2.1,
            reputation_score=900.0,
            bkash_number="01911223344"
        )
        app_id = app["application_id"]

        # Disburse
        disburse_res = self.service.disburse_scholarship(
            application_id=app_id,
            disburser_id="admin-bdt-payout",
            channel="BKASH_DISBURSEMENT"
        )
        self.assertEqual(disburse_res["status"], "DISBURSED")
        receipt = disburse_res["receipt"]
        self.assertTrue(receipt["receipt_id"].startswith("tx-sch-"))
        self.assertEqual(len(receipt["cryptographic_hash"]), 64)
        self.assertEqual(receipt["amount_bdt"], 2500.0)

        # Check fund deduction
        fund = self.service._funds["fund-buet89-relief-03"]
        self.assertEqual(fund["awarded_count"], 3)
        self.assertEqual(fund["remaining_bdt"], 92500.0)

    def test_disburse_scholarship_double_payout_defense(self):
        app = self.service.apply_for_scholarship(
            fund_id="fund-buet89-relief-03",
            student_id="student-double-payout",
            student_name="Double Payout Student",
            family_monthly_income_bdt=15000.0,
            institution_name="BUET",
            bkash_number="01711998877"
        )
        app_id = app["application_id"]

        # First disbursement succeeds
        self.service.disburse_scholarship(app_id, "admin-payout")

        # Second disbursement on same application must fail
        with self.assertRaises(ValueError):
            self.service.disburse_scholarship(app_id, "admin-payout")

    def test_apply_scholarship_sanitizes_html_script(self):
        app = self.service.apply_for_scholarship(
            fund_id="fund-pathao-stem-01",
            student_id="student-xss-test",
            student_name="XSS Student",
            family_monthly_income_bdt=13000.0,
            institution_name="Dhaka College",
            bkash_number="01711223399",
            statement_of_need="Need grant <script>alert('xss')</script> for textbooks."
        )
        self.assertEqual(app["statement_of_need"], "Need grant alert('xss') for textbooks.")


class TestTechnicalAssessmentService(unittest.TestCase):
    """Unit tests verifying ATS resume matching and secure coding challenge sandbox."""

    def setUp(self):
        self.service = TechnicalAssessmentService()

    def test_analyze_resume_ats_success(self):
        cv_text = """
        Experienced Junior Python Backend Developer with strong skills in FastAPI, PostgreSQL,
        and Docker. Built scalable REST API services using asyncio, Redis caching, and PyTest
        for automated testing. Proficient with Git version control and Linux environments.
        """
        res = self.service.analyze_resume_ats(
            candidate_id="cand-001",
            job_id="job-pathao-python",
            role_title="Junior Python Engineer",
            cv_text=cv_text,
            target_skills=["python", "fastapi", "postgresql", "docker", "redis", "git"]
        )
        self.assertEqual(res["ats_compatibility_score"], 100.0)
        self.assertIn("python", res["found_keywords"])
        self.assertIn("fastapi", res["found_keywords"])
        self.assertIn("docker", res["found_keywords"])

    def test_analyze_resume_ats_too_short_error(self):
        with self.assertRaises(ValueError):
            self.service.analyze_resume_ats(
                candidate_id="cand-001",
                job_id="job-01",
                role_title="Engineer",
                cv_text="Too short"
            )

    def test_list_and_get_assessments(self):
        asmts = self.service.list_assessments(role="Python")
        self.assertGreaterEqual(len(asmts), 1)
        asmt_id = asmts[0]["assessment_id"]

        detail = self.service.get_assessment(asmt_id)
        self.assertEqual(detail["assessment_id"], asmt_id)
        self.assertIn("starter_code", detail)

    def test_evaluate_code_submission_pass(self):
        solution_code = """
        def two_sum(nums: list, target: int) -> list:
            seen = {}
            for i, num in enumerate(nums):
                diff = target - num
                if diff in seen:
                    return [seen[diff], i]
                seen[num] = i
            return []
        """
        res = self.service.evaluate_code_submission(
            candidate_id="cand-solver-01",
            assessment_id="asmt-py-algo-01",
            language="python",
            code_solution=solution_code,
            time_spent_seconds=420
        )
        self.assertTrue(res["is_passed"])
        self.assertEqual(res["passed_tests"], 3)
        self.assertEqual(res["technical_score"], 100.0)

    def test_evaluate_code_submission_security_sandbox(self):
        malicious_code = """
        import os
        os.system("cat /etc/passwd")
        """
        with self.assertRaises(PermissionError):
            self.service.evaluate_code_submission(
                candidate_id="cand-hacker",
                assessment_id="asmt-py-algo-01",
                language="python",
                code_solution=malicious_code
            )

    def test_evaluate_code_submission_blocks_getattr_and_importlib(self):
        code_with_getattr = "x = getattr(builtins, 'eval')('1+1')"
        with self.assertRaises(PermissionError):
            self.service.evaluate_code_submission(
                candidate_id="cand-exploit",
                assessment_id="asmt-py-algo-01",
                language="python",
                code_solution=code_with_getattr
            )

        code_with_importlib = "import importlib; m = importlib.import_module('os')"
        with self.assertRaises(PermissionError):
            self.service.evaluate_code_submission(
                candidate_id="cand-exploit",
                assessment_id="asmt-py-algo-01",
                language="python",
                code_solution=code_with_importlib
            )

    def test_evaluate_code_empty_error(self):
        with self.assertRaises(ValueError):
            self.service.evaluate_code_submission(
                candidate_id="cand-empty",
                assessment_id="asmt-py-algo-01",
                language="python",
                code_solution=""
            )


class TestPhase28RestEndpoints(unittest.IsolatedAsyncioTestCase):
    """Integration tests verifying Section 27 REST API routing in router.py."""

    async def test_endowment_create_and_apply_endpoint(self):
        from backend.app.api.v1.router import (
            create_endowment_fund,
            list_endowment_funds,
            apply_for_scholarship,
            disburse_scholarship_funds
        )

        create_req = CreateEndowmentFundRequest(
            sponsor_id="spn-alumni-01",
            sponsor_name="IBA Alumni Association",
            fund_title="IBA BBA Tuition Grant 2026",
            total_grant_bdt=80000.0,
            target_criteria="GENERAL_MERIT",
            disbursement_per_student_bdt=2000.0
        )
        fund = await create_endowment_fund(create_req)
        fund_id = fund["fund_id"]
        self.assertEqual(fund["sponsor_name"], "IBA Alumni Association")

        funds = await list_endowment_funds(criteria="GENERAL_MERIT")
        self.assertGreaterEqual(len(funds), 1)

        apply_req = ApplyScholarshipRequest(
            fund_id=fund_id,
            student_id="std-iba-01",
            student_name="Nabil Ahmed",
            family_monthly_income_bdt=16000.0,
            institution_name="IBA, University of Dhaka",
            cat_ability_theta=1.9,
            reputation_score=880.0,
            bkash_number="01755667788",
            statement_of_need="Tuition stipend for semester registration."
        )
        app = await apply_for_scholarship(apply_req)
        app_id = app["application_id"]
        self.assertGreaterEqual(app["composite_score"], 70.0)

        disburse_req = DisburseScholarshipRequest(
            application_id=app_id,
            disburser_id="admin-iba-payout",
            channel="BKASH_DISBURSEMENT"
        )
        payout = await disburse_scholarship_funds(disburse_req)
        self.assertEqual(payout["status"], "DISBURSED")
        self.assertEqual(payout["receipt"]["amount_bdt"], 2000.0)

    async def test_career_ats_and_assessment_endpoint(self):
        from backend.app.api.v1.router import (
            analyze_resume_ats,
            list_technical_assessments,
            submit_technical_assessment
        )

        ats_req = ATSResumeAnalysisRequest(
            candidate_id="cand-rest-01",
            job_id="job-bengal-01",
            role_title="Backend Intern",
            cv_text="Proficient in Python, FastAPI, SQL database management, Git, and Docker containers.",
            target_skills=["python", "fastapi", "sql", "docker", "git"]
        )
        ats_res = await analyze_resume_ats(ats_req)
        self.assertEqual(ats_res["ats_compatibility_score"], 100.0)

        asmts = await list_technical_assessments(role="Python")
        self.assertGreaterEqual(len(asmts), 1)

        sub_req = SubmitTechnicalAssessmentRequest(
            candidate_id="cand-rest-01",
            assessment_id="asmt-py-algo-01",
            language="python",
            code_solution="def two_sum(nums, target): seen = {}; return []",
            time_spent_seconds=240
        )
        sub_res = await submit_technical_assessment(sub_req)
        self.assertTrue(sub_res["is_passed"])
        self.assertEqual(sub_res["technical_score"], 100.0)


if __name__ == "__main__":
    unittest.main()
