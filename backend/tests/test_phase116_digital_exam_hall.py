"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite for Digital Examination Hall
TOPIC:     Phase 116 Digital Examination Hall & Proctoring Integrity Tower
FILE:      backend/tests/test_phase116_digital_exam_hall.py
PHASE:     Phase 116 - Digital Examination Hall & Proctoring Integrity Tower
PURPOSE:   Automated unit and integration test suite certifying client heuristic
           telemetry logging, dynamic integrity score calculations, tamper-evident
           SHA-256 cryptographic receipt verification, teacher proctor roster,
           tactile 3D styling, and strict zero-emoji compliance.
STANDARDS: OWASP ASVS L2, Privacy-First Architecture, Pure Academic Design, Strict Zero-Emoji
========================================================================================
"""

import hashlib
import re
import unittest
from pathlib import Path

from backend.app.services.proctoring_integrity_service import (
    ProctoringIntegrityService,
    proctoring_integrity_service,
    SessionNotFoundException,
    ExamFinalizedException,
    ProctoringException,
)


class TestPhase116DigitalExamHall(unittest.TestCase):
    """
    Test suite certifying Phase 116 Digital Examination Hall & Proctoring Integrity Tower.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.service_file = cls.root_dir / "backend" / "app" / "services" / "proctoring_integrity_service.py"
        cls.endpoints_file = cls.root_dir / "backend" / "app" / "api" / "v1" / "endpoints" / "exam_hall.py"
        cls.frontend_desk = cls.root_dir / "frontend" / "src" / "components" / "exam-hall" / "DigitalExamDesk.tsx"
        cls.frontend_monitor = cls.root_dir / "frontend" / "src" / "components" / "exam-hall" / "ProctorTeacherMonitor.tsx"

        cls.emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

    def setUp(self):
        # Create a fresh isolated service instance for each test
        self.service = ProctoringIntegrityService()

    def test_01_session_lifecycle_and_draft_answers(self):
        """Verifies session initialization, draft answer auto-saving, and flagged questions."""
        sess_id = "test-sess-001"
        session = self.service.start_exam_session(
            session_id=sess_id,
            student_id="stu-2026-99",
            student_name="Nafis Iqbal",
            exam_id="exam-math-2026",
            institution_id="inst-ndc-dhaka",
        )

        self.assertEqual(session["session_id"], sess_id)
        self.assertEqual(session["status"], ProctoringIntegrityService.STATUS_ACTIVE)
        self.assertEqual(session["integrity_score"], 100.0)
        self.assertIsNone(session["finalized_at"])
        self.assertIsNone(session["receipt_hash"])

        # Auto-save draft answers
        draft = self.service.save_draft_answers(
            session_id=sess_id,
            answers={"q_1": "opt_A", "q_2": "opt_C"},
            flagged_questions=["q_2"],
        )
        self.assertEqual(draft["saved_count"], 2)
        self.assertEqual(draft["flagged_count"], 1)

        fetched = self.service.get_session(sess_id)
        self.assertIn("q_1", fetched["answers"])
        self.assertEqual(fetched["answers"]["q_1"]["option_id"], "opt_A")
        self.assertIn("q_2", fetched["flagged_questions"])

        # Querying unknown session raises SessionNotFoundException
        with self.assertRaises(SessionNotFoundException):
            self.service.get_session("non-existent-session-id")

    def test_02_heuristic_telemetry_event_logging_and_score_deductions(self):
        """Verifies privacy-preserving client heuristic event logging and scoring deductions."""
        sess_id = "test-sess-002"
        self.service.start_exam_session(
            session_id=sess_id,
            student_id="stu-2026-101",
            student_name="Shadman Sakib",
            exam_id="exam-chem-2026",
        )

        # 1. First 2 tab switches: 0 deduction (2 grace switches)
        self.service.record_telemetry_event(sess_id, ProctoringIntegrityService.EVENT_TAB_SWITCH, 1.0)
        res2 = self.service.record_telemetry_event(sess_id, ProctoringIntegrityService.EVENT_TAB_SWITCH, 1.0)
        self.assertEqual(res2["current_integrity_score"], 100.0)
        self.assertEqual(res2["integrity_band"], ProctoringIntegrityService.BAND_EXEMPLARY)

        # 2. 3rd tab switch: 4.0 points deduction -> 96.0
        res3 = self.service.record_telemetry_event(sess_id, ProctoringIntegrityService.EVENT_TAB_SWITCH, 1.0)
        self.assertEqual(res3["current_integrity_score"], 96.0)
        self.assertEqual(res3["integrity_band"], ProctoringIntegrityService.BAND_EXEMPLARY)

        # 3. Window blur: 5.0 seconds grace. Total blur of 15.0 seconds -> excess 10.0s * 0.5 = 5.0 deduction
        # Score: 96.0 - 5.0 = 91.0
        res_blur = self.service.record_telemetry_event(
            sess_id, ProctoringIntegrityService.EVENT_WINDOW_BLUR, 15.0
        )
        self.assertEqual(res_blur["current_integrity_score"], 91.0)
        self.assertEqual(res_blur["integrity_band"], ProctoringIntegrityService.BAND_EXEMPLARY)

        # 4. Audio threshold surge: 3 grace surges. 4th surge = excess 1 * 3.0 deduction
        # Score: 91.0 - 3.0 = 88.0 -> transitions to BAND_MONITORED
        for _ in range(4):
            res_audio = self.service.record_telemetry_event(
                sess_id, ProctoringIntegrityService.EVENT_AUDIO_SURGE, 1.0
            )
        self.assertEqual(res_audio["current_integrity_score"], 88.0)
        self.assertEqual(res_audio["integrity_band"], ProctoringIntegrityService.BAND_MONITORED)

        # 5. Heavy deductions dropping below 70.0 -> transitions to BAND_UNDER_REVIEW
        for _ in range(5):
            res_heavy = self.service.record_telemetry_event(
                sess_id, ProctoringIntegrityService.EVENT_TAB_SWITCH, 1.0
            )
        # Tab count is now 3 + 5 = 8. Excess = 6 * 4.0 = 24.0
        # Blur deduction: 5.0
        # Audio deduction: 3.0
        # Total deduction: 32.0 -> Score = 68.0
        self.assertEqual(res_heavy["current_integrity_score"], 68.0)
        self.assertEqual(res_heavy["integrity_band"], ProctoringIntegrityService.BAND_UNDER_REVIEW)

    def test_03_tamper_evident_sha256_cryptographic_receipt_sealing(self):
        """Verifies exam submission finalization and SHA-256 seal verification."""
        sess_id = "test-sess-003"
        student_id = "stu-2026-105"
        exam_id = "exam-phys-2026"

        self.service.start_exam_session(
            session_id=sess_id,
            student_id=student_id,
            student_name="Zarin Tasnim",
            exam_id=exam_id,
        )

        final_answers = {"q_1": "opt_A", "q_2": "opt_B", "q_3": "opt_D"}
        result = self.service.finalize_exam_submission(sess_id, final_answers=final_answers)

        self.assertEqual(result["status"], ProctoringIntegrityService.STATUS_FINALIZED)
        self.assertEqual(result["verification_status"], "CRYPTOGRAPHICALLY_SEALED")
        self.assertEqual(result["total_answers_submitted"], 3)
        self.assertIsNotNone(result["receipt_hash"])
        self.assertEqual(len(result["receipt_hash"]), 64)  # 64-char hex SHA-256

        # Recompute expected hash to confirm cryptographic integrity
        finalized_at = result["finalized_at"]
        final_score = result["integrity_score"]
        expected_payload = (
            f"{sess_id}:{student_id}:{exam_id}:{final_score}:{finalized_at}:"
            f"{ProctoringIntegrityService.SALT}"
        )
        expected_hash = hashlib.sha256(expected_payload.encode("utf-8")).hexdigest()
        self.assertEqual(result["receipt_hash"], expected_hash)

        # Modifying finalized session raises ExamFinalizedException
        with self.assertRaises(ExamFinalizedException):
            self.service.save_draft_answers(sess_id, {"q_4": "opt_C"})

        with self.assertRaises(ExamFinalizedException):
            self.service.record_telemetry_event(sess_id, ProctoringIntegrityService.EVENT_TAB_SWITCH, 1.0)

        with self.assertRaises(ExamFinalizedException):
            self.service.finalize_exam_submission(sess_id)

    def test_04_teacher_proctor_roster_and_integrity_bands(self):
        """Verifies real-time examinee roster retrieval for invigilators and teachers."""
        exam_id = "exam-common-001"
        self.service.start_exam_session("s1", "std1", "Student One", exam_id)
        self.service.start_exam_session("s2", "std2", "Student Two", exam_id)

        # Student Two incurs deductions
        for _ in range(5):
            self.service.record_telemetry_event("s2", ProctoringIntegrityService.EVENT_TAB_SWITCH, 1.0)

        # Student One finalizes
        self.service.finalize_exam_submission("s1", final_answers={"q_1": "opt_A"})

        roster = self.service.get_proctor_roster(exam_id)
        self.assertEqual(len(roster), 2)

        roster_map = {r["session_id"]: r for r in roster}
        self.assertEqual(roster_map["s1"]["status"], ProctoringIntegrityService.STATUS_FINALIZED)
        self.assertTrue(roster_map["s1"]["has_sealed_receipt"])
        self.assertEqual(roster_map["s1"]["integrity_band"], ProctoringIntegrityService.BAND_EXEMPLARY)

        self.assertEqual(roster_map["s2"]["status"], ProctoringIntegrityService.STATUS_ACTIVE)
        self.assertFalse(roster_map["s2"]["has_sealed_receipt"])
        self.assertEqual(roster_map["s2"]["integrity_band"], ProctoringIntegrityService.BAND_MONITORED)

    def test_05_frontend_component_architecture_and_tactile_styling(self):
        """Verifies frontend components adhere to pure academic design, 3D tactile buttons, and KaTeX."""
        self.assertTrue(self.frontend_desk.exists(), "DigitalExamDesk.tsx must exist.")
        self.assertTrue(self.frontend_monitor.exists(), "ProctorTeacherMonitor.tsx must exist.")

        desk_content = self.frontend_desk.read_text(encoding="utf-8")
        monitor_content = self.frontend_monitor.read_text(encoding="utf-8")

        # 1. Tactile 3D Oxford Navy buttons
        self.assertIn("shadow-[0_4px_0_0_#061727]", desk_content)
        self.assertIn("active:translate-y-1", desk_content)
        self.assertIn("active:shadow-none", desk_content)
        self.assertIn("উত্তর নিশ্চিত করুন", desk_content)
        self.assertIn("পরীক্ষা সমাপ্ত করুন", desk_content)

        self.assertIn("shadow-[0_4px_0_0_#061727]", monitor_content)
        self.assertIn("active:translate-y-1", monitor_content)

        # 2. Calm emerald integrity badge
        self.assertIn("পরীক্ষা অখণ্ডতা সক্রিয়", desk_content)
        self.assertIn("স্বয়ংক্রিয় সংরক্ষণ সম্পন্ন", desk_content)

        # 3. KaTeX Renderer formula integration
        self.assertIn("KaTeXRenderer", desk_content)

        # 4. Pure Lucide icons
        self.assertIn("ShieldCheck", desk_content)
        self.assertIn("CheckCircle2", desk_content)
        self.assertIn("Clock", desk_content)
        self.assertIn("AlertCircle", desk_content)
        self.assertIn("Flag", desk_content)

        self.assertIn("Users", monitor_content)
        self.assertIn("ShieldCheck", monitor_content)
        self.assertIn("CheckCircle2", monitor_content)

    def test_06_architecture_notes_and_zero_emoji_enforcement(self):
        """Verifies Developer Architecture Notes and strict zero-emoji enforcement across all Phase 116 files."""
        files_to_check = [
            self.service_file,
            self.endpoints_file,
            self.frontend_desk,
            self.frontend_monitor,
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
