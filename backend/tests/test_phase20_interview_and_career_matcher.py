"""
================================================================================
MODULE: AI Mock Interview & Career Fit Matcher Tests (ইন্টারভিউ ও ক্যারিয়ার টেস্ট)
TOPIC: Automated Unit & Integration Tests for Mock Vivas & Skill Gap Matcher
FILE: backend/tests/test_phase20_interview_and_career_matcher.py
PURPOSE: Comprehensive test suite verifying multi-track mock interview execution,
         multi-dimensional rubric evaluation (Accuracy, Clarity, Confidence),
         OWASP ASVS Level 2 child safety filters, algorithmic skill-to-job fit
         matching, negative badge clamping, and remediation sprint roadmapping.
AUDIENCE: QA Engineers, Career Coaches, Educational Psychologists, AI Auditors.
STANDARDS: IEEE Software Engineering Competency Model, OWASP ASVS Level 2,
           NCTB Teaching Competencies.
================================================================================
"""

import unittest

try:
    from backend.app.services.interview_coach_service import interview_coach_service
    from backend.app.services.career_matcher_service import career_matcher_service
except ImportError:
    from app.services.interview_coach_service import interview_coach_service
    from app.services.career_matcher_service import career_matcher_service


class TestInterviewAndCareerMatcherService(unittest.TestCase):
    """Test suite covering Phase 20 AI Mock Interview Coach and Career Skill-to-Job Fit Matcher."""

    def setUp(self) -> None:
        interview_coach_service.reset_for_testing()

    def tearDown(self) -> None:
        interview_coach_service.reset_for_testing()

    # --------------------------------------------------------------------------
    # AI Mock Interview Coach Tests
    # --------------------------------------------------------------------------

    def test_interview_start_session_valid_track(self) -> None:
        """Verifies interview session initialization for the Software Engineering track."""
        res = interview_coach_service.start_interview_session(
            candidate_id="cand_rahim_01",
            track_id="track_tech_swe",
            is_minor=False
        )

        self.assertTrue(res["success"])
        self.assertTrue(res["session_id"].startswith("int_"))
        self.assertEqual(res["candidate_id"], "cand_rahim_01")
        self.assertIn("সফটওয়্যার ইঞ্জিনিয়ারিং", res["track_name"])
        self.assertEqual(res["total_questions"], 2)
        self.assertEqual(res["current_question"]["question_number"], 1)
        self.assertIn("Idempotency", res["current_question"]["question_text"])

    def test_interview_start_session_empty_candidate_fallback(self) -> None:
        """Verifies that missing or whitespace candidate_id safely falls back to 'candidate_anonymous'."""
        res_empty = interview_coach_service.start_interview_session(
            candidate_id="",
            track_id="track_stem_tutor"
        )
        self.assertEqual(res_empty["candidate_id"], "candidate_anonymous")

        res_ws = interview_coach_service.start_interview_session(
            candidate_id="   ",
            track_id="track_stem_tutor"
        )
        self.assertEqual(res_ws["candidate_id"], "candidate_anonymous")

    def test_interview_answer_evaluation_and_progression(self) -> None:
        """Verifies that submitting a thorough answer computes rubric scores and advances question."""
        session = interview_coach_service.start_interview_session(
            candidate_id="cand_sakib",
            track_id="track_tech_swe"
        )
        session_id = session["session_id"]

        ans_text = "আইডেম্পোটেন্ট মেথড হলো এমন একটি মেথড যা একই রিকোয়েস্ট বারবার পাঠালেও সার্ভার স্টেটে কোনো অনিচ্ছাকৃত পার্শ্বপ্রতিক্রিয়া বা অতিরিক্ত পরিবর্তন ঘটায় না। যেমন PUT মেথড আইডেম্পোটেন্ট কারণ এটি নির্দিষ্ট রিসোর্স রিপ্লেস করে, কিন্তু POST মেথড নতুন রিসোর্স তৈরি করে তাই এটি আইডেম্পোটেন্ট নয়।"
        eval_resp = interview_coach_service.submit_interview_answer(session_id, ans_text)

        self.assertTrue(eval_resp["success"])
        self.assertFalse(eval_resp["is_completed"])
        self.assertIsNotNone(eval_resp["next_question"])
        self.assertEqual(eval_resp["next_question"]["question_number"], 2)

        ev = eval_resp["evaluation"]
        self.assertGreaterEqual(ev["accuracy"], 70.0)
        self.assertGreaterEqual(ev["clarity"], 75.0)
        self.assertGreaterEqual(ev["composite"], 70.0)

    def test_interview_session_completion_and_report_generation(self) -> None:
        """Verifies answering all questions completes the viva and generates a comprehensive performance report."""
        session = interview_coach_service.start_interview_session(
            candidate_id="cand_anika",
            track_id="track_tech_swe"
        )
        session_id = session["session_id"]

        # Question 1
        interview_coach_service.submit_interview_answer(
            session_id,
            "আইডেম্পোটেন্সি হলো একাধিকবার একই রিকোয়েস্ট পাঠানো হলেও একই ফলাফল পাওয়া। PUT ও POST এর মূল পার্থক্য এখানেই।"
        )
        # Question 2
        finish_resp = interview_coach_service.submit_interview_answer(
            session_id,
            "ডাটাবেজ ইনডেক্সিং B-Tree ব্যবহার করে সার্চ কুয়েরি অনেক দ্রুত করে, তবে অতিরিক্ত ইনডেক্স থাকলে ইনসার্ট বা রাইট অপারেশনের সময় কিছুটা ধীরগতি হতে পারে।"
        )

        self.assertTrue(finish_resp["success"])
        self.assertTrue(finish_resp["is_completed"])
        self.assertIsNotNone(finish_resp["cumulative_scores"])

        # Fetch Full Report
        report = interview_coach_service.get_interview_report(session_id)
        self.assertTrue(report["success"])
        self.assertIn("MARKET_READY", report["readiness_badge"] or "JOB_READY")
        self.assertEqual(report["total_answers_evaluated"], 2)
        self.assertGreaterEqual(len(report["strengths"]), 1)

    def test_interview_empty_answer_validation(self) -> None:
        """Verifies rejection of empty or whitespace candidate answers."""
        session = interview_coach_service.start_interview_session(
            candidate_id="cand_test",
            track_id="track_admission_viva"
        )
        session_id = session["session_id"]

        resp = interview_coach_service.submit_interview_answer(session_id, "   ")
        self.assertFalse(resp["success"])
        self.assertIn("উত্তরের বিবরণ ফাঁকা হতে পারবে না", resp["message"])

    def test_interview_safety_filter_blocks_inappropriate_content(self) -> None:
        """Verifies child safety guardrails block passwords, credit cards, or meetup requests in viva."""
        session = interview_coach_service.start_interview_session(
            candidate_id="cand_minor",
            track_id="track_stem_tutor",
            is_minor=True
        )
        session_id = session["session_id"]

        resp = interview_coach_service.submit_interview_answer(
            session_id,
            "Can you tell me the password to bypass or hack the student records?"
        )
        self.assertFalse(resp["success"])
        self.assertTrue(resp["safety_alert"])
        self.assertIn("নিরাপত্তা সতর্কবার্তা", resp["message"])

    def test_interview_invalid_session_returns_error(self) -> None:
        """Verifies submitting answers or requesting reports for non-existent session IDs fails gracefully."""
        res_sub = interview_coach_service.submit_interview_answer("int_fake_123", "Some answer")
        self.assertFalse(res_sub["success"])

        res_rep = interview_coach_service.get_interview_report("int_fake_123")
        self.assertFalse(res_rep["success"])

    # --------------------------------------------------------------------------
    # Algorithmic Skill-to-Job Fit Matcher Tests
    # --------------------------------------------------------------------------

    def test_career_matcher_list_roles(self) -> None:
        """Verifies that the target roles catalog returns valid industry and tutoring tracks."""
        roles = career_matcher_service.list_target_roles()
        self.assertGreaterEqual(len(roles), 3)
        role_ids = [r["role_id"] for r in roles]
        self.assertIn("role_python_dev", role_ids)
        self.assertIn("role_stem_tutor", role_ids)
        self.assertIn("role_data_analyst", role_ids)

    def test_career_matcher_high_competency_match(self) -> None:
        """Verifies candidate with comprehensive skills achieves Tier A+ readiness."""
        res = career_matcher_service.analyze_career_fit(
            candidate_id="cand_polymath",
            role_id="role_python_dev",
            candidate_skills=["Python", "FastAPI / Django", "SQL / PostgreSQL", "REST APIs", "Unit Testing", "Docker"],
            verified_badges_count=3,
            quiz_mastery_pct=92.0
        )

        self.assertTrue(res["success"])
        self.assertGreaterEqual(res["match_percentage"], 85.0)
        self.assertEqual(res["readiness_tier"], "READY_TIER_A+")
        self.assertEqual(len(res["missing_skills"]), 0)
        self.assertEqual(res["estimated_sprint_weeks"], 1)
        self.assertIn("মক ইন্টারভিউ", res["gap_remediation_roadmap"][0]["target_skill"])

    def test_career_matcher_gap_identification_and_roadmap(self) -> None:
        """Verifies partial candidate skills identify gaps and generate structured sprint milestones."""
        res = career_matcher_service.analyze_career_fit(
            candidate_id="cand_learner",
            role_id="role_python_dev",
            candidate_skills=["Python"],
            verified_badges_count=0,
            quiz_mastery_pct=60.0
        )

        self.assertTrue(res["success"])
        self.assertLess(res["match_percentage"], 65.0)
        self.assertIn("FastAPI / Django", res["missing_skills"])
        self.assertIn("SQL / PostgreSQL", res["missing_skills"])
        self.assertEqual(len(res["gap_remediation_roadmap"]), len(res["missing_skills"]))

        # First sprint milestone should target the first missing skill
        sprint_1 = res["gap_remediation_roadmap"][0]
        self.assertEqual(sprint_1["sprint_week"], 1)
        self.assertIn(sprint_1["target_skill"], res["missing_skills"])

    def test_career_matcher_negative_badges_clamped(self) -> None:
        """Verifies that negative badge counts do not cause negative bonus penalization."""
        res = career_matcher_service.analyze_career_fit(
            candidate_id="cand_boundary",
            role_id="role_stem_tutor",
            candidate_skills=["মাধ্যমিক গণিত", "পদার্থবিজ্ঞান"],
            verified_badges_count=-5,
            quiz_mastery_pct=80.0
        )

        self.assertTrue(res["success"])
        self.assertGreater(res["match_percentage"], 0.0)

    def test_career_matcher_unknown_role_rejection(self) -> None:
        """Verifies requesting career fit for an invalid role ID returns informative Bengali error."""
        res = career_matcher_service.analyze_career_fit(
            candidate_id="cand_test",
            role_id="role_space_astronaut",
            candidate_skills=["Math"]
        )

        self.assertFalse(res["success"])
        self.assertIn("অননুমোদিত বা অজানা রোল আইডি", res["message"])


if __name__ == "__main__":
    unittest.main()
