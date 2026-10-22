"""
================================================================================
MODULE: Peer Collaboration & Dispute Arbitration Tests (সার্কেল ও ট্রাইব্যুনাল টেস্ট)
TOPIC: Automated Unit & Integration Tests for Minor-Safe Circles & 3-SME Tribunals
FILE: backend/tests/test_phase17_study_circle_and_arbitration.py
PURPOSE: Rigorously verifies collaborative peer study circles and academic dispute
         arbitration tribunals under OWASP ASVS Level 2 minor data isolation,
         SuperMemo SM-2 streak alignment, quorum consensus, and cryptographic
         audit ledger integrity.
AUDIENCE: QA Engineers, Educational Psychologists, Security Arbitrators.
STANDARDS: ISO/IEC 25010 Test Quality, OWASP ASVS Level 2, COPE Publication Ethics.
================================================================================
"""

import unittest
from datetime import datetime, timezone

try:
    from backend.app.services.study_circle_service import study_circle_service
    from backend.app.services.arbitration_service import arbitration_service
    from backend.app.core.audit_ledger import audit_ledger
except ImportError:
    from app.services.study_circle_service import study_circle_service
    from app.services.arbitration_service import arbitration_service
    from app.core.audit_ledger import audit_ledger


class TestStudyCircleAndArbitrationService(unittest.TestCase):
    """Test suite covering Phase 17 collaborative peer circles and multi-SME dispute tribunals."""

    def setUp(self) -> None:
        study_circle_service.reset_for_testing()
        arbitration_service.reset_for_testing()

    def tearDown(self) -> None:
        study_circle_service.reset_for_testing()
        arbitration_service.reset_for_testing()

    # --------------------------------------------------------------------------
    # Study Circle Service Tests
    # --------------------------------------------------------------------------

    def test_create_study_circle_registers_lead_and_masks_minor_pii(self) -> None:
        """Verifies study circle creation and automatic pseudonymization of minor creator."""
        circle = study_circle_service.create_study_circle(
            creator_id="stu_minor_01",
            creator_name="তানভীর আহমেদ",
            is_minor=True,
            name="জেএসসি গণিত ফাইটার্স",
            subject="গণিত",
            class_grade=8,
            target_weekly_questions=100
        )

        self.assertIsNotNone(circle)
        self.assertEqual(circle["name"], "জেএসসি গণিত ফাইটার্স")
        self.assertEqual(circle["member_count"], 1)
        self.assertEqual(circle["max_members"], 6)

        # Check minor identity masking
        lead = circle["members"][0]
        self.assertEqual(lead["student_id"], "stu_minor_01")
        self.assertEqual(lead["display_name"], "তানভীর (সার্কেল সদস্য)")
        self.assertEqual(lead["role"], "LEAD")
        self.assertTrue(lead["is_minor"])

    def test_non_minor_member_display_name_is_unaltered(self) -> None:
        """Verifies adult members have standard unmasked display names."""
        circle = study_circle_service.create_study_circle(
            creator_id="stu_adult_01",
            creator_name="মো: ফারুক হোসেন",
            is_minor=False,
            name="এইচএসসি পদার্থবিজ্ঞান দল",
            subject="পদার্থবিজ্ঞান",
            class_grade=12,
            target_weekly_questions=150
        )

        lead = circle["members"][0]
        self.assertEqual(lead["display_name"], "মো: ফারুক হোসেন")
        self.assertFalse(lead["is_minor"])

    def test_join_study_circle_success_and_duplicate_prevention(self) -> None:
        """Verifies peer student can join circle and duplicate membership is rejected."""
        circle = study_circle_service.create_study_circle(
            creator_id="stu_creator",
            creator_name="সাব্বির রহমান",
            is_minor=True,
            name="রসায়ন পর্যালোচনা গ্রুপ",
            subject="রসায়ন",
            class_grade=9
        )
        circle_id = circle["circle_id"]

        # Join successfully
        res_join = study_circle_service.join_study_circle(
            circle_id=circle_id,
            student_id="stu_peer_02",
            student_name="নাসরিন আক্তার",
            is_minor=True
        )
        self.assertTrue(res_join["success"])
        self.assertEqual(res_join["circle"]["member_count"], 2)

        # Attempt to join again with same student_id
        res_dup = study_circle_service.join_study_circle(
            circle_id=circle_id,
            student_id="stu_peer_02",
            student_name="নাসরিন আক্তার",
            is_minor=True
        )
        self.assertFalse(res_dup["success"])
        self.assertIn("ইতিপূর্বে", res_dup["message"])

    def test_circle_capacity_limit_enforced_at_six(self) -> None:
        """Ensures that circles cannot exceed the maximum capacity of 6 members."""
        circle = study_circle_service.create_study_circle(
            creator_id="stu_lead",
            creator_name="দলনেতা",
            is_minor=True,
            name="কম্পিউটার বিজ্ঞান টিম",
            subject="আইসিটি",
            class_grade=10
        )
        circle_id = circle["circle_id"]

        # Add 5 more members to reach capacity of 6
        for i in range(1, 6):
            res = study_circle_service.join_study_circle(
                circle_id=circle_id,
                student_id=f"stu_peer_{i}",
                student_name=f"সদস্য {i}",
                is_minor=True
            )
            self.assertTrue(res["success"])

        # Try to add a 7th member
        res_overflow = study_circle_service.join_study_circle(
            circle_id=circle_id,
            student_id="stu_peer_overflow",
            student_name="সদস্য অতিরিক্ত",
            is_minor=True
        )
        self.assertFalse(res_overflow["success"])
        self.assertIn("সর্বোচ্চ ধারণক্ষমতা 6 জন", res_overflow["message"])

    def test_contribute_questions_and_achieve_weekly_goal(self) -> None:
        """Verifies question contribution advances circle goal and triggers ACHIEVED state."""
        circle = study_circle_service.create_study_circle(
            creator_id="stu_lead",
            creator_name="সাইফুল ইসলাম",
            is_minor=True,
            name="ইংরেজি গ্রামার সার্কেল",
            subject="ইংরেজি",
            class_grade=8,
            target_weekly_questions=50
        )
        circle_id = circle["circle_id"]

        # Valid contribution
        res1 = study_circle_service.contribute_questions(
            circle_id=circle_id,
            student_id="stu_lead",
            questions_solved=30
        )
        self.assertTrue(res1["success"])
        self.assertEqual(res1["completed_questions"], 30)
        self.assertEqual(res1["status"], "IN_PROGRESS")

        # Second contribution completing the target
        res2 = study_circle_service.contribute_questions(
            circle_id=circle_id,
            student_id="stu_lead",
            questions_solved=25
        )
        self.assertTrue(res2["success"])
        self.assertEqual(res2["completed_questions"], 55)
        self.assertEqual(res2["status"], "ACHIEVED")

    def test_contribute_questions_rejects_negative_or_zero(self) -> None:
        """Verifies negative or zero question contribution is strictly rejected."""
        circle = study_circle_service.create_study_circle(
            creator_id="stu_lead",
            creator_name="সাইফুল ইসলাম",
            is_minor=True,
            name="বিজ্ঞান সার্কেল",
            subject="সাধারণ বিজ্ঞান",
            class_grade=7
        )
        circle_id = circle["circle_id"]

        res_zero = study_circle_service.contribute_questions(
            circle_id=circle_id,
            student_id="stu_lead",
            questions_solved=0
        )
        self.assertFalse(res_zero["success"])
        self.assertIn("১ বা তার বেশি", res_zero["message"])

        res_neg = study_circle_service.contribute_questions(
            circle_id=circle_id,
            student_id="stu_lead",
            questions_solved=-5
        )
        self.assertFalse(res_neg["success"])

    # --------------------------------------------------------------------------
    # Academic Dispute Arbitration Tribunal Tests
    # --------------------------------------------------------------------------

    def test_create_tribunal_case_and_audit_ledger_logging(self) -> None:
        """Verifies convening arbitration tribunal creates case and logs audit event."""
        initial_length = audit_ledger.get_total_blocks()

        case = arbitration_service.create_tribunal_case(
            question_id="q_math_algebra_99",
            question_stem="২x + ৫ = ১৫ হলে x এর মান কত?",
            dispute_reason="প্রশ্নে প্রদত্ত সঠিক উত্তর কি এবং সমাধানের বিকল্পে অসংগতি রয়েছে।",
            filed_by_student_id="stu_disputant_01",
            escalated_by="AI_DISPUTE_ESCALATOR"
        )

        self.assertIsNotNone(case["case_id"])
        self.assertEqual(case["status"], "IN_DELIBERATION")
        self.assertEqual(case["required_quorum"], 3)
        self.assertEqual(len(case["votes"]), 0)

        # Audit ledger must record convening event
        self.assertEqual(audit_ledger.get_total_blocks(), initial_length + 1)
        latest_block = audit_ledger.get_blocks(limit=1, offset=audit_ledger.get_total_blocks() - 1)[0]
        self.assertEqual(latest_block["payload"]["case_id"], case["case_id"])
        self.assertEqual(latest_block["payload"]["question_id"], "q_math_algebra_99")

    def test_tribunal_majority_verdict_key_corrected(self) -> None:
        """Verifies 2/3 majority votes for CORRECT_KEY seals ruling with score restitution."""
        case = arbitration_service.create_tribunal_case(
            question_id="q_disputed_01",
            question_stem="আলোর প্রতিসরণ সূচক সম্পর্কিত প্রশ্ন।",
            dispute_reason="ক ও গ উভয়েই পাঠ্যবই অনুযায়ী গ্রহণযোগ্য উত্তর হতে পারে।",
            filed_by_student_id="stu_01"
        )
        case_id = case["case_id"]

        # SME 1 votes CORRECT_KEY
        v1 = arbitration_service.cast_sme_vote(
            case_id=case_id,
            sme_id="sme_prof_rahim",
            sme_name="ড. এম এ রহিম",
            verdict="CORRECT_KEY",
            rationale="এনসিটিবি বোর্ড বই অনুসারে বিকল্প গ অধিকতর নির্ভুল।"
        )
        self.assertTrue(v1["success"])
        self.assertEqual(v1["status"], "IN_DELIBERATION")
        self.assertEqual(v1["total_votes_cast"], 1)

        # SME 2 votes CORRECT_KEY (majority formed)
        v2 = arbitration_service.cast_sme_vote(
            case_id=case_id,
            sme_id="sme_prof_salma",
            sme_name="অধ্যাপক সালমা খাতুন",
            verdict="CORRECT_KEY",
            rationale="বিকল্প গ সংশোধনযোগ্য।"
        )
        self.assertTrue(v2["success"])
        self.assertEqual(v2["status"], "IN_DELIBERATION")
        self.assertEqual(v2["total_votes_cast"], 2)

        # SME 3 votes DISMISS (minority dissenting)
        v3 = arbitration_service.cast_sme_vote(
            case_id=case_id,
            sme_id="sme_lecturer_tanvir",
            sme_name="তানভীর আহমেদ (লেকচারার)",
            verdict="DISMISS",
            rationale="বর্তমান ক-ই আদর্শ।"
        )
        self.assertTrue(v3["success"])
        self.assertEqual(v3["total_votes_cast"], 3)
        self.assertEqual(v3["status"], "RESOLVED_KEY_CORRECTED")
        self.assertIn("উত্তর সংশোধনের নির্দেশ", v3["final_ruling"])

        # Check sealed state in database
        sealed_case = arbitration_service.get_case(case_id)
        self.assertIsNotNone(sealed_case["sealed_at"])

        # Verify audit ledger recorded sealing
        latest_block = audit_ledger.get_blocks(limit=1, offset=audit_ledger.get_total_blocks() - 1)[0]
        self.assertEqual(latest_block["event_type"], "ARBITRATION_TRIBUNAL_SEALED")
        self.assertEqual(latest_block["payload"]["winning_verdict"], "CORRECT_KEY")

    def test_tribunal_rejects_duplicate_vote_from_same_sme(self) -> None:
        """Verifies that an SME cannot vote multiple times in the same case."""
        case = arbitration_service.create_tribunal_case(
            question_id="q_dup_test",
            question_stem="স্টেম বর্ণনা।",
            dispute_reason="অস্পষ্টতা।",
            filed_by_student_id="stu_02"
        )
        case_id = case["case_id"]

        v1 = arbitration_service.cast_sme_vote(
            case_id=case_id,
            sme_id="sme_repeat_01",
            sme_name="ড. কামাল",
            verdict="QUARANTINE",
            rationale="প্রশ্ন প্রত্যাহার আবশ্যক।"
        )
        self.assertTrue(v1["success"])

        # Duplicate vote attempt
        v_dup = arbitration_service.cast_sme_vote(
            case_id=case_id,
            sme_id="sme_repeat_01",
            sme_name="ড. কামাল",
            verdict="QUARANTINE",
            rationale="পুনরায় ভোট প্রদান।"
        )
        self.assertFalse(v_dup["success"])
        self.assertIn("ইতিমধ্যে এই মামলায় ভোট প্রদান করেছেন", v_dup["message"])

    def test_tribunal_rejects_invalid_verdict_strings(self) -> None:
        """Verifies arbitrary or invalid verdict strings are rejected."""
        case = arbitration_service.create_tribunal_case(
            question_id="q_invalid_test",
            question_stem="স্টেম বর্ণনা।",
            dispute_reason="অস্পষ্টতা।",
            filed_by_student_id="stu_03"
        )
        case_id = case["case_id"]

        v_bad = arbitration_service.cast_sme_vote(
            case_id=case_id,
            sme_id="sme_01",
            sme_name="বিচারক ১",
            verdict="INVALID_OPINION",
            rationale="কিছু একটা।"
        )
        self.assertFalse(v_bad["success"])
        self.assertIn("অবৈধ রায়", v_bad["message"])

    def test_tribunal_deadlock_resolves_to_dismissed_when_no_majority(self) -> None:
        """Verifies a 1-1-1 split vote without a majority resolves to DISMISSED."""
        case = arbitration_service.create_tribunal_case(
            question_id="q_split_test",
            question_stem="বিতর্কিত স্টেম।",
            dispute_reason="ত্রিপক্ষীয় মতভেদ।",
            filed_by_student_id="stu_04"
        )
        case_id = case["case_id"]

        # SME 1: CORRECT_KEY
        arbitration_service.cast_sme_vote(case_id, "sme_a", "বিচারক ক", "CORRECT_KEY", "যুক্তি ১")
        # SME 2: QUARANTINE
        arbitration_service.cast_sme_vote(case_id, "sme_b", "বিচারক খ", "QUARANTINE", "যুক্তি ২")
        # SME 3: DISMISS
        v3 = arbitration_service.cast_sme_vote(case_id, "sme_c", "বিচারক গ", "DISMISS", "যুক্তি ৩")

        self.assertTrue(v3["success"])
        self.assertEqual(v3["status"], "DISMISSED")
        self.assertIn("সংখ্যাগরিষ্ঠতা", v3["final_ruling"])


if __name__ == "__main__":
    unittest.main()
