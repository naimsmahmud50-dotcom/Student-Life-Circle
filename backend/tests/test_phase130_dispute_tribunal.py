"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Parent-Teacher Conference & Escrow Dispute Tribunal
 * TOPIC:     Phase 130 Institutional Appointment & Formal Escrow Arbitration
 * FILE:      backend/tests/test_phase130_dispute_tribunal.py
 * PHASE:     Phase 130 - Institutional PTC & Escrow Dispute Tribunal
 * PURPOSE:   Comprehensive automated test suite validating:
 *            1. Developer Architecture Note headers & file presence
 *            2. Escrow dispute lodging, cryptographic SHA-256 evidence hashing
 *            3. Zero-IDOR tenancy access defense on dispute dockets
 *            4. 3-Party ombudsman arbitration rulings and payout calculations
 *            5. PTC conference time-slot conflict avoidance
 *            6. Zero-IDOR tenancy access defense on PTC appointments
 *            7. Supabase migration 008 RLS policies and table structures
 *            8. Frontend 3D tactile buttons, Lucide icons, and Zero-Emoji compliance.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Strict Supabase RLS, Pure Academic UI
 */
"""

import os
import re
import time
import unittest
from pathlib import Path

from backend.escrow.dispute_tribunal import (
    EscrowDisputeTribunal,
    DisputeStatus,
    ArbitrationRulingType,
    DisputeActorRole,
    DisputeEvidence,
    DisputeCase,
    DisputeRuling,
    UnauthorizedDisputeAccessException,
    InvalidDisputeTransitionException,
)
from backend.portal.ptc_booking import (
    PTCBookingManager,
    PTCStatus,
    PTCAgendaTopic,
    AppointmentSlot,
    PTCAppointment,
    UnauthorizedPTCAccessException,
    PTCSlotConflictException,
)

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase130DisputeTribunal(unittest.TestCase):
    """
    Automated test verification suite for Phase 130 Institutional PTC & Escrow Dispute Tribunal.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.escrow_init = cls.root_dir / "backend" / "escrow" / "__init__.py"
        cls.tribunal_py = cls.root_dir / "backend" / "escrow" / "dispute_tribunal.py"
        cls.portal_init = cls.root_dir / "backend" / "portal" / "__init__.py"
        cls.ptc_py = cls.root_dir / "backend" / "portal" / "ptc_booking.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "008_ptc_and_escrow_tribunal_rls.sql"
        cls.tribunal_tsx = cls.root_dir / "frontend" / "src" / "pages" / "tribunal" / "disputes.tsx"
        cls.ptc_tsx = cls.root_dir / "frontend" / "src" / "pages" / "guardian" / "ptc.tsx"
        cls.spec_md = cls.root_dir / "specs" / "034-phase130-ptc-tribunal" / "spec.md"
        cls.plan_md = cls.root_dir / "specs" / "034-phase130-ptc-tribunal" / "plan.md"
        cls.tasks_md = cls.root_dir / "specs" / "034-phase130-ptc-tribunal" / "tasks.md"
        cls.test_file = Path(__file__).resolve()

        cls.target_files = [
            cls.escrow_init,
            cls.tribunal_py,
            cls.portal_init,
            cls.ptc_py,
            cls.migration_sql,
            cls.tribunal_tsx,
            cls.ptc_tsx,
            cls.test_file,
        ]

    def test_01_all_target_files_exist_and_headers_valid(self):
        """Verify all target files exist and contain standardized Developer Architecture Note."""
        for file_path in self.target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"Missing Developer Architecture Note in {file_path.name}"
            )
            self.assertIn(
                "Phase 130 - Institutional PTC & Escrow Dispute Tribunal",
                content,
                f"Missing Phase 130 identifier in {file_path.name}"
            )

    def test_02_strict_zero_emoji_compliance(self):
        """Strictly enforces Zero-Emoji across all Phase 130 codebase files."""
        for file_path in self.target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"Zero-Emoji violation in {file_path.name}: Found emojis {matches}"
            )

    def test_03_dispute_lifecycle_and_evidence_hashing(self):
        """Validates formal dispute lodging and SHA-256 cryptographic evidence hashing."""
        tribunal = EscrowDisputeTribunal()
        case = tribunal.lodge_dispute(
            case_id="case_101",
            guardian_id="usr_guardian_01",
            tutor_id="usr_tutor_01",
            escrow_amount=8000.0,
            reason_bn="৪টি ক্লাস অপূর্ণ রয়েছে",
            reason_en="4 classes were not delivered"
        )
        self.assertEqual(case.status, DisputeStatus.LODGED)
        self.assertEqual(case.escrow_amount, 8000.0)

        # Submit evidence
        evidence = tribunal.submit_evidence(
            case_id="case_101",
            evidence_id="ev_01",
            caller_id="usr_guardian_01",
            caller_role=DisputeActorRole.GUARDIAN,
            title="উপস্থিতি খাতা",
            content="৮টি ক্লাস স্বাক্ষরিত হয়েছে"
        )
        self.assertEqual(case.status, DisputeStatus.EVIDENCE_SUBMITTED)
        self.assertEqual(len(evidence.evidence_hash), 64)  # SHA-256 64-hex chars
        self.assertEqual(len(case.evidence_items), 1)

    def test_04_zero_idor_dispute_access_defense(self):
        """Strict Zero-IDOR test: Unauthorized third party cannot access docket or submit evidence."""
        tribunal = EscrowDisputeTribunal()
        tribunal.lodge_dispute(
            case_id="case_102",
            guardian_id="usr_guardian_01",
            tutor_id="usr_tutor_01",
            escrow_amount=6500.0,
            reason_bn="ফি বিরোধ",
            reason_en="Fee dispute"
        )

        # Authorized guardian access passes
        case_g = tribunal.get_case_for_actor("case_102", "usr_guardian_01", DisputeActorRole.GUARDIAN)
        self.assertIsNotNone(case_g)

        # Authorized tutor access passes
        case_t = tribunal.get_case_for_actor("case_102", "usr_tutor_01", DisputeActorRole.TUTOR)
        self.assertIsNotNone(case_t)

        # Authorized ombudsman access passes
        case_o = tribunal.get_case_for_actor("case_102", "usr_ombudsman_99", DisputeActorRole.OMBUDSMAN)
        self.assertIsNotNone(case_o)

        # Unauthorized intruder access MUST be blocked with UnauthorizedDisputeAccessException
        with self.assertRaises(UnauthorizedDisputeAccessException):
            tribunal.get_case_for_actor("case_102", "usr_unauthorized_attacker", DisputeActorRole.GUARDIAN)

        with self.assertRaises(UnauthorizedDisputeAccessException):
            tribunal.submit_evidence(
                case_id="case_102",
                evidence_id="ev_spoof",
                caller_id="usr_unauthorized_attacker",
                caller_role=DisputeActorRole.TUTOR,
                title="ভুয়া প্রমাণ",
                content="Spoofed evidence"
            )

    def test_05_ombudsman_ruling_and_payout_calculations(self):
        """Validates 3-party arbitration verdicts (Release, Refund, Split) and payout math."""
        tribunal = EscrowDisputeTribunal()
        tribunal.lodge_dispute(
            case_id="case_split",
            guardian_id="usr_guardian_01",
            tutor_id="usr_tutor_01",
            escrow_amount=10000.0,
            reason_bn="আংশিক ক্লাস সম্পন্ন",
            reason_en="Partial classes completed"
        )

        # Schedule hearing
        tribunal.schedule_hearing("case_split", "usr_ombudsman_01", time.time() + 3600)

        # Ruling: 70% to tutor, 30% to guardian
        ruling = tribunal.issue_ruling(
            case_id="case_split",
            ombudsman_id="usr_ombudsman_01",
            ruling_type=ArbitrationRulingType.PARTIAL_SPLIT,
            split_ratio_tutor=0.70,
            reasoning_bn="৭টি ক্লাস সঠিকভাবে পরিচালিত হয়েছে",
            reasoning_en="7 out of 10 classes verified"
        )
        self.assertEqual(ruling.payout_tutor, 7000.0)
        self.assertEqual(ruling.payout_guardian, 3000.0)
        self.assertEqual(len(ruling.ruling_hash), 64)

        # Test FULL_REFUND on another docket
        tribunal.lodge_dispute(
            case_id="case_refund",
            guardian_id="usr_guardian_02",
            tutor_id="usr_tutor_02",
            escrow_amount=5000.0,
            reason_bn="কোনো ক্লাস নেওয়া হয়নি",
            reason_en="Zero classes taken"
        )
        ruling_ref = tribunal.issue_ruling(
            case_id="case_refund",
            ombudsman_id="usr_ombudsman_01",
            ruling_type=ArbitrationRulingType.FULL_REFUND,
            split_ratio_tutor=0.0,
            reasoning_bn="টিউটর অনুপস্থিত ছিলেন",
            reasoning_en="Tutor completely absent"
        )
        self.assertEqual(ruling_ref.payout_tutor, 0.0)
        self.assertEqual(ruling_ref.payout_guardian, 5000.0)

    def test_06_ptc_slot_booking_and_conflict_avoidance(self):
        """Validates Parent-Teacher Conference slot booking and overlap conflict prevention."""
        portal = PTCBookingManager()
        now = time.time() + 86400  # Tomorrow

        # Book first appointment
        appt1 = portal.book_appointment(
            appointment_id="ptc_001",
            guardian_id="usr_guard_1",
            teacher_id="usr_teacher_A",
            student_id="usr_stud_1",
            slot_id="slot_01",
            start_timestamp=now,
            duration_minutes=30,
            agenda_topic=PTCAgendaTopic.ACADEMIC_PROGRESS,
            notes_bn="গণিত ফলাফল",
            notes_en="Math results"
        )
        self.assertEqual(appt1.status, PTCStatus.REQUESTED)
        self.assertEqual(len(appt1.meeting_passcode), 6)

        # Attempt to book overlapping appointment with same teacher MUST raise PTCSlotConflictException
        with self.assertRaises(PTCSlotConflictException):
            portal.book_appointment(
                appointment_id="ptc_conflict",
                guardian_id="usr_guard_2",
                teacher_id="usr_teacher_A",  # Same teacher
                student_id="usr_stud_2",
                slot_id="slot_02",
                start_timestamp=now + 600,  # Starts 10 mins into previous 30-min session
                duration_minutes=30,
                agenda_topic=PTCAgendaTopic.EXAM_PREPARATION,
                notes_bn="পরীক্ষা প্রস্তুতি",
                notes_en="Exam prep"
            )

        # Booking non-overlapping slot with same teacher succeeds
        appt2 = portal.book_appointment(
            appointment_id="ptc_002",
            guardian_id="usr_guard_2",
            teacher_id="usr_teacher_A",
            student_id="usr_stud_2",
            slot_id="slot_03",
            start_timestamp=now + 2400,  # 40 mins later
            duration_minutes=30,
            agenda_topic=PTCAgendaTopic.EXAM_PREPARATION,
            notes_bn="পদার্থবিজ্ঞান প্রস্তুতি",
            notes_en="Physics prep"
        )
        self.assertEqual(appt2.status, PTCStatus.REQUESTED)

    def test_07_zero_idor_ptc_tenancy_defense(self):
        """Strict Zero-IDOR test: Non-involved user cannot read or confirm conference passes."""
        portal = PTCBookingManager()
        now = time.time() + 86400

        portal.book_appointment(
            appointment_id="ptc_tenancy_test",
            guardian_id="usr_guard_1",
            teacher_id="usr_teacher_A",
            student_id="usr_stud_1",
            slot_id="slot_10",
            start_timestamp=now,
            duration_minutes=30,
            agenda_topic=PTCAgendaTopic.MENTAL_WELLBEING,
            notes_bn="মনোযোগ কাউন্সেলিং",
            notes_en="Wellbeing notes"
        )

        # Guardian and teacher can retrieve
        self.assertIsNotNone(portal.get_appointment_for_actor("ptc_tenancy_test", "usr_guard_1"))
        self.assertIsNotNone(portal.get_appointment_for_actor("ptc_tenancy_test", "usr_teacher_A"))

        # Intruder receives UnauthorizedPTCAccessException
        with self.assertRaises(UnauthorizedPTCAccessException):
            portal.get_appointment_for_actor("ptc_tenancy_test", "usr_malicious_neighbor")

        with self.assertRaises(UnauthorizedPTCAccessException):
            portal.confirm_appointment("ptc_tenancy_test", "usr_malicious_neighbor")

    def test_08_supabase_migration_008_rls_integrity(self):
        """Validates migration 008 RLS policies, zero-IDOR barriers, and index definitions."""
        content = self.migration_sql.read_text(encoding="utf-8")
        self.assertIn("ALTER TABLE public.ptc_appointments ENABLE ROW LEVEL SECURITY;", content)
        self.assertIn("ALTER TABLE public.escrow_disputes ENABLE ROW LEVEL SECURITY;", content)
        self.assertIn("ALTER TABLE public.dispute_evidence_logs ENABLE ROW LEVEL SECURITY;", content)
        self.assertIn("ALTER TABLE public.tribunal_rulings ENABLE ROW LEVEL SECURITY;", content)
        self.assertIn("guardian_id = auth.uid()", content)
        self.assertIn("teacher_id = auth.uid()", content)
        self.assertIn("tutor_id = auth.uid()", content)

    def test_09_frontend_tribunal_and_ptc_styling(self):
        """Validates frontend pages for Oxford Navy palette, 3D tactile buttons, and Lucide icons."""
        tribunal_content = self.tribunal_tsx.read_text(encoding="utf-8")
        ptc_content = self.ptc_tsx.read_text(encoding="utf-8")

        # Color palette
        self.assertIn("#0A2540", tribunal_content)
        self.assertIn("#0A2540", ptc_content)

        # 3D tactile buttons
        self.assertIn("shadow-[0_4px_0_0_", tribunal_content)
        self.assertIn("active:translate-y-1", tribunal_content)
        self.assertIn("shadow-[0_4px_0_0_", ptc_content)
        self.assertIn("active:translate-y-1", ptc_content)

        # Lucide icons
        self.assertIn("Scale", tribunal_content)
        self.assertIn("Gavel", tribunal_content)
        self.assertIn("Calendar", ptc_content)
        self.assertIn("Users", ptc_content)

        # Zero-IDOR mention
        self.assertIn("Zero-IDOR", tribunal_content)
        self.assertIn("Zero-IDOR", ptc_content)


if __name__ == "__main__":
    unittest.main()
