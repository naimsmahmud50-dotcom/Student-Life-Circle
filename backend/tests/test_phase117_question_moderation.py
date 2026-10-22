"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite for Question Bank Moderation & Peer-Review
TOPIC:     Phase 117 Collaborative Question Bank Moderation & Peer-Review
FILE:      backend/tests/test_phase117_question_moderation.py
PHASE:     Phase 117 - Collaborative Question Bank Moderation & Peer-Review
PURPOSE:   Automated unit and integration test suite certifying multi-stage editorial
           state transitions, dual-examiner blind consensus enforcement, author self-review
           prevention, emergency quarantine isolation, and strict zero-emoji standards.
STANDARDS: OWASP ASVS L2, Zero-Unreviewed-AI Policy, Pure Academic Design, Strict Zero-Emoji
========================================================================================
"""

import re
import unittest
from pathlib import Path

from backend.app.services.question_moderation_service import (
    QuestionModerationService,
    question_moderation_service,
    QuestionNotFoundException,
    InvalidStateTransitionException,
    SelfReviewException,
    DuplicateReviewException,
    QuarantinedQuestionException,
)
from backend.app.services.quiz_engine import quiz_engine


class TestPhase117QuestionModeration(unittest.TestCase):
    """
    Test suite certifying Phase 117 Collaborative Question Bank Moderation & Peer-Review.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.service_file = cls.root_dir / "backend" / "app" / "services" / "question_moderation_service.py"
        cls.endpoints_file = cls.root_dir / "backend" / "app" / "api" / "v1" / "endpoints" / "moderation.py"
        cls.frontend_diff = cls.root_dir / "frontend" / "src" / "components" / "moderation" / "KaTeXVisualDiffViewer.tsx"
        cls.frontend_tribunal = cls.root_dir / "frontend" / "src" / "components" / "moderation" / "QuestionReviewTribunal.tsx"

        cls.emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

    def setUp(self):
        # Create a fresh isolated service instance for each test
        self.service = QuestionModerationService()

    def test_01_state_machine_transitions_and_validations(self):
        """Verifies multi-stage state transitions: DRAFT -> SME_REVIEW -> BOARD_MODERATED -> APPROVED."""
        q_id = "test-q-trans-01"
        author_id = "author-01"
        created = self.service.create_draft_question(
            author_id=author_id,
            author_name="Author Name",
            subject="পদার্থবিজ্ঞান ১ম পত্র",
            topic="গতিবিদ্যা",
            stem="গতিশক্তির সমীকরণ কোনটি?",
            options=[
                {"key": "A", "text": "$E_k = \\frac{1}{2}mv^2$", "is_correct": True},
                {"key": "B", "text": "$E_k = mv$", "is_correct": False},
            ],
            question_id=q_id,
        )

        self.assertEqual(created["status"], QuestionModerationService.STATE_DRAFT)

        # Illegal review while in DRAFT
        with self.assertRaises(InvalidStateTransitionException):
            self.service.review_question(
                question_id=q_id,
                examiner_id="sme-01",
                examiner_name="Examiner One",
                decision=QuestionModerationService.DECISION_APPROVE,
                comments="Good",
            )

        # Transition: DRAFT -> SME_REVIEW
        submitted = self.service.submit_for_review(q_id, actor_id=author_id)
        self.assertEqual(submitted["status"], QuestionModerationService.STATE_SME_REVIEW)

        # 1st Examiner approves: SME_REVIEW -> BOARD_MODERATED
        rev1 = self.service.review_question(
            question_id=q_id,
            examiner_id="sme-01",
            examiner_name="Examiner One",
            decision=QuestionModerationService.DECISION_APPROVE,
            comments="সমীকরণ সঠিক।",
        )
        self.assertEqual(rev1["status"], QuestionModerationService.STATE_BOARD_MODERATED)
        self.assertEqual(rev1["approvals_count"], 1)

        # 2nd Examiner approves: BOARD_MODERATED -> APPROVED
        rev2 = self.service.review_question(
            question_id=q_id,
            examiner_id="board-02",
            examiner_name="Examiner Two",
            decision=QuestionModerationService.DECISION_APPROVE,
            comments="বোর্ড স্ট্যান্ডার্ড অনুযায়ী অনুমোদিত।",
        )
        self.assertEqual(rev2["status"], QuestionModerationService.STATE_APPROVED)
        self.assertEqual(rev2["approvals_count"], 2)

    def test_02_dual_examiner_blind_consensus_and_self_review_prevention(self):
        """Verifies author self-review prevention and duplicate review rejections."""
        q_id = "test-q-consensus-02"
        author_id = "author-dr-hasan"
        self.service.create_draft_question(
            author_id=author_id,
            author_name="ড. হাসান",
            subject="উচ্চতর গণিত ১ম পত্র",
            topic="ক্যালকুলাস",
            stem="$\\lim_{x \\to 0} \\frac{\\sin x}{x} = ?$",
            options=[
                {"key": "A", "text": "$1$", "is_correct": True},
                {"key": "B", "text": "$0$", "is_correct": False},
            ],
            question_id=q_id,
        )
        self.service.submit_for_review(q_id, actor_id=author_id)

        # 1. Author attempts self-review -> SelfReviewException
        with self.assertRaises(SelfReviewException):
            self.service.review_question(
                question_id=q_id,
                examiner_id=author_id,
                examiner_name="ড. হাসান",
                decision=QuestionModerationService.DECISION_APPROVE,
                comments="নিজে তৈরি করেছি, সঠিক।",
            )

        # 2. First legitimate reviewer endorses
        self.service.review_question(
            question_id=q_id,
            examiner_id="examiner-01",
            examiner_name="প্রফেসর কবির",
            decision=QuestionModerationService.DECISION_APPROVE,
            comments="অনুমোদনযোগ্য।",
        )

        # 3. Same examiner attempts duplicate review -> DuplicateReviewException
        with self.assertRaises(DuplicateReviewException):
            self.service.review_question(
                question_id=q_id,
                examiner_id="examiner-01",
                examiner_name="প্রফেসর কবির",
                decision=QuestionModerationService.DECISION_APPROVE,
                comments="আবার অনুমোদন করছি।",
            )

        # 4. A revision request demotes back to DRAFT
        rev_demote = self.service.review_question(
            question_id=q_id,
            examiner_id="examiner-02",
            examiner_name="প্রফেসর রশীদ",
            decision=QuestionModerationService.DECISION_REVISE,
            comments="ব্যাখ্যা অংশে আরও বিস্তারিত যোগ করুন।",
        )
        self.assertEqual(rev_demote["status"], QuestionModerationService.STATE_DRAFT)

    def test_03_emergency_quarantine_instant_isolation_and_audit(self):
        """Verifies emergency quarantine switch isolates item from live pool and logs audit."""
        q_id = "test-q-quarantine-03"
        self.service.create_draft_question(
            author_id="author-03",
            author_name="লেখক ৩",
            subject="রসায়ন ১ম পত্র",
            topic="রাসায়নিক পরিবর্তন",
            stem="ভুল সমীকরণ সংবলিত প্রশ্ন",
            options=[{"key": "A", "text": "বিকল্প", "is_correct": True}],
            question_id=q_id,
        )
        self.service.submit_for_review(q_id, actor_id="author-03")

        # Emergency quarantine invoked
        res = self.service.emergency_quarantine(
            question_id=q_id,
            actor_id="admin-invigilator-01",
            actor_name="প্রধান পরীক্ষা নিয়ন্ত্রক",
            reason="প্রশ্নে টাইপো ও সমীকরণে বিভ্রান্তি পাওয়া গেছে।",
        )

        self.assertEqual(res["status"], QuestionModerationService.STATE_QUARANTINED)
        self.assertIn(q_id, quiz_engine._quarantined_questions)

        # Quarantined item cannot be reviewed
        with self.assertRaises(QuarantinedQuestionException):
            self.service.review_question(
                question_id=q_id,
                examiner_id="examiner-99",
                examiner_name="Examiner 99",
                decision=QuestionModerationService.DECISION_APPROVE,
                comments="অনুমোদন",
            )

        # Audit trail recorded
        audit = self.service.get_audit_trail(q_id)
        quarantine_events = [e for e in audit if e["action"] == "EMERGENCY_QUARANTINE"]
        self.assertEqual(len(quarantine_events), 1)
        self.assertEqual(quarantine_events[0]["details"]["reason"], "প্রশ্নে টাইপো ও সমীকরণে বিভ্রান্তি পাওয়া গেছে।")

    def test_04_quarantine_remediation_workflow(self):
        """Verifies remediating a quarantined question back to DRAFT for revision."""
        q_id = "test-q-remediate-04"
        self.service.create_draft_question(
            author_id="author-04",
            author_name="লেখক ৪",
            subject="তথ্য ও যোগাযোগ প্রযুক্তি",
            topic="সংখ্যা পদ্ধতি",
            stem="বাইনারি ১০১০ এর দশমিক মান কত?",
            options=[{"key": "A", "text": "১০", "is_correct": True}],
            question_id=q_id,
        )
        self.service.emergency_quarantine(
            question_id=q_id,
            actor_id="admin-01",
            actor_name="অ্যাডমিন",
            reason="বিকল্প উত্তরে ভুল",
        )

        # Remediate back to draft
        remediated = self.service.remediate_quarantine(
            question_id=q_id,
            actor_id="editor-01",
            remediation_notes="বিকল্প উত্তর সংশোধন করা হয়েছে।",
            revised_stem="বাইনারি $(1010)_2$ এর সমতুল্য দশমিক মান কত?",
        )

        self.assertEqual(remediated["status"], QuestionModerationService.STATE_DRAFT)
        self.assertEqual(remediated["version"], 2)
        self.assertNotIn(q_id, quiz_engine._quarantined_questions)

        # Can now re-submit for review
        resubmitted = self.service.submit_for_review(q_id, actor_id="editor-01")
        self.assertEqual(resubmitted["status"], QuestionModerationService.STATE_SME_REVIEW)

    def test_05_frontend_component_architecture_and_tactile_styling(self):
        """Verifies frontend components adhere to pure academic design, 3D tactile buttons, and KaTeX."""
        self.assertTrue(self.frontend_diff.exists(), "KaTeXVisualDiffViewer.tsx must exist.")
        self.assertTrue(self.frontend_tribunal.exists(), "QuestionReviewTribunal.tsx must exist.")

        diff_content = self.frontend_diff.read_text(encoding="utf-8")
        tribunal_content = self.frontend_tribunal.read_text(encoding="utf-8")

        # 1. Tactile 3D Emerald button
        self.assertIn("shadow-[0_4px_0_0_#0F766E]", tribunal_content)
        self.assertIn("active:translate-y-1", tribunal_content)
        self.assertIn("active:shadow-none", tribunal_content)
        self.assertIn("bg-emerald-700", tribunal_content)
        self.assertIn("প্রশ্ন অনুমোদন করুন", tribunal_content)
        self.assertIn("সংশোধনের নির্দেশ দিন", tribunal_content)
        self.assertIn("জরুরি কোয়ারেন্টিন", tribunal_content)

        # 2. Keyboard shortcuts
        self.assertIn("keydown", tribunal_content)
        self.assertIn("KeyA", tribunal_content.replace("'a'", "'KeyA'"))
        self.assertIn("শর্টকাট", tribunal_content)

        # 3. KaTeX formula diffing and highlights
        self.assertIn("KaTeXRenderer", diff_content)
        self.assertIn("bg-emerald-50", diff_content)
        self.assertIn("bg-rose-50", diff_content)
        self.assertIn("পাশাপাশি তুলনা", diff_content)
        self.assertIn("একক বিস্তারিত দৃশ্য", diff_content)

        # 4. Pure Lucide icons
        self.assertIn("Split", diff_content)
        self.assertIn("Columns", diff_content)
        self.assertIn("Layers", diff_content)
        self.assertIn("CheckCircle2", tribunal_content)
        self.assertIn("AlertCircle", tribunal_content)
        self.assertIn("Users", tribunal_content)

    def test_06_architecture_notes_and_zero_emoji_enforcement(self):
        """Verifies Developer Architecture Notes and strict zero-emoji enforcement across all Phase 117 files."""
        files_to_check = [
            self.service_file,
            self.endpoints_file,
            self.frontend_diff,
            self.frontend_tribunal,
            Path(__file__),
        ]

        for file_path in files_to_check:
            self.assertTrue(file_path.exists(), f"File {file_path.name} must exist.")
            content = file_path.read_text(encoding="utf-8")

            # Assert Developer Architecture Note
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"File {file_path.name} is missing standardized DEVELOPER ARCHITECTURE NOTE.",
            )

            # Assert zero emojis
            emoji_matches = self.emoji_pattern.findall(content)
            self.assertEqual(
                len(emoji_matches),
                0,
                f"File {file_path.name} contains emoji violations: {emoji_matches}",
            )


if __name__ == "__main__":
    unittest.main()
