"""
================================================================================
TEST SUITE: Phase 63 Autonomous Examination Proctoring & Integrity Audit Tower
STANDARDS: Computer Vision Heuristics, Time-Series Audit Ledger, ASVS 4.0 L2
PURPOSE: Comprehensive unit test coverage for vision heuristics, gaze tracking,
         progressive warning escalation, exam auto-lock, and proctor overrides.
================================================================================
"""

import unittest
from backend.app.services.autonomous_proctoring_integrity_service import AutonomousProctoringIntegrityService


class TestAutonomousProctoringIntegrity(unittest.TestCase):

    def setUp(self):
        self.service = AutonomousProctoringIntegrityService()
        self.default_session_id = "proctor:exam:hsc2026:math_live"
        self.student_id = "student:user:alice_rahman"
        self.proctor_id = "proctor:user:dr_kamal"

    # --------------------------------------------------------------------------
    # 1. Session Lifecycle Tests
    # --------------------------------------------------------------------------
    def test_default_proctoring_session_seeded(self):
        rep = self.service.get_session_report(self.default_session_id)
        self.assertEqual(rep["student_id"], self.student_id)
        self.assertFalse(rep["is_locked"])
        self.assertGreater(rep["final_suspicion_score"], 0.0)
        self.assertGreaterEqual(rep["total_anomalies_count"], 1)

    def test_start_proctoring_session(self):
        session = self.service.start_session(
            student_id="student:user:karim",
            exam_id="exam:buet:math_01",
            exam_title="BUET Admission Diagnostic Model Test"
        )
        self.assertIn("proctor:", session["session_id"])
        self.assertEqual(session["status"], "MONITORING")
        self.assertEqual(session["suspicion_score"], 0.0)
        self.assertEqual(session["warnings_count"], 0)
        self.assertFalse(session["is_locked"])

    # --------------------------------------------------------------------------
    # 2. Vision Heuristics & Anomaly Event Tests
    # --------------------------------------------------------------------------
    def test_record_gaze_away_low_impact(self):
        session = self.service.start_session(
            student_id="student:user:test_gaze",
            exam_id="exam:test:001"
        )
        sid = session["session_id"]
        res = self.service.record_event(
            session_id=sid,
            event_type="GAZE_AWAY_FROM_SCREEN",
            confidence_score=0.8,
            duration_ms=1000.0,
            gaze_yaw_angle=12.0
        )
        self.assertGreater(res["new_suspicion_score"], 0.0)
        self.assertLess(res["new_suspicion_score"], 15.0)
        self.assertFalse(res["is_locked"])

    def test_record_gaze_away_sharp_yaw_long_duration(self):
        session = self.service.start_session(
            student_id="student:user:test_sharp_gaze",
            exam_id="exam:test:002"
        )
        sid = session["session_id"]
        res = self.service.record_event(
            session_id=sid,
            event_type="GAZE_AWAY_FROM_SCREEN",
            confidence_score=1.0,
            duration_ms=3500.0,
            gaze_yaw_angle=42.0  # Sharp head turn
        )
        # Base weight 8.0 + 7.0 adjustment = 15.0
        self.assertGreaterEqual(res["new_suspicion_score"], 15.0)

    def test_record_secondary_face_detected(self):
        session = self.service.start_session(
            student_id="student:user:test_faces",
            exam_id="exam:test:003"
        )
        sid = session["session_id"]
        res = self.service.record_event(
            session_id=sid,
            event_type="GAZE_AWAY_FROM_SCREEN",
            confidence_score=1.0,
            detected_faces_count=2  # Secondary person in frame
        )
        # Overrides to SECONDARY_FACE_DETECTED (weight 25.0)
        self.assertGreaterEqual(res["new_suspicion_score"], 25.0)
        self.assertEqual(res["action_taken"], "WARNING_ISSUED")

    def test_record_face_disappeared(self):
        session = self.service.start_session(
            student_id="student:user:test_disappear",
            exam_id="exam:test:004"
        )
        sid = session["session_id"]
        res = self.service.record_event(
            session_id=sid,
            event_type="GAZE_AWAY_FROM_SCREEN",
            confidence_score=1.0,
            detected_faces_count=0  # Student walked away
        )
        self.assertGreaterEqual(res["new_suspicion_score"], 12.0)

    def test_record_tab_switched(self):
        session = self.service.start_session(
            student_id="student:user:test_tab",
            exam_id="exam:test:005"
        )
        sid = session["session_id"]
        res = self.service.record_event(
            session_id=sid,
            event_type="TAB_SWITCHED",
            confidence_score=1.0
        )
        self.assertEqual(res["new_suspicion_score"], 15.0)

    def test_record_devtools_opened_critical(self):
        session = self.service.start_session(
            student_id="student:user:test_devtools",
            exam_id="exam:test:006"
        )
        sid = session["session_id"]
        res = self.service.record_event(
            session_id=sid,
            event_type="DEVTOOLS_OPENED",
            confidence_score=1.0
        )
        self.assertEqual(res["new_suspicion_score"], 35.0)
        self.assertEqual(res["action_taken"], "WARNING_ISSUED")

    def test_record_clipboard_paste(self):
        session = self.service.start_session(
            student_id="student:user:test_paste",
            exam_id="exam:test:007"
        )
        sid = session["session_id"]
        res = self.service.record_event(
            session_id=sid,
            event_type="CLIPBOARD_PASTE",
            confidence_score=1.0
        )
        self.assertEqual(res["new_suspicion_score"], 12.0)

    # --------------------------------------------------------------------------
    # 3. Progressive Escalation & Exam Lock Tests
    # --------------------------------------------------------------------------
    def test_progressive_warning_issued(self):
        session = self.service.start_session(student_id="st:warn1", exam_id="ex:01")
        sid = session["session_id"]
        # Trigger event giving score >= 20.0
        res = self.service.record_event(session_id=sid, event_type="SECONDARY_FACE_DETECTED", confidence_score=1.0)
        self.assertEqual(res["action_taken"], "WARNING_ISSUED")
        self.assertEqual(res["warnings_count"], 1)

    def test_progressive_penalty_issued(self):
        session = self.service.start_session(student_id="st:pen1", exam_id="ex:02")
        sid = session["session_id"]
        self.service.record_event(session_id=sid, event_type="SECONDARY_FACE_DETECTED", confidence_score=1.0) # +25
        res = self.service.record_event(session_id=sid, event_type="SECONDARY_FACE_DETECTED", confidence_score=1.0) # +25 -> 50
        self.assertEqual(res["action_taken"], "PROGRESSIVE_PENALTY")
        self.assertEqual(res["warnings_count"], 2)

    def test_progressive_exam_locked(self):
        session = self.service.start_session(student_id="st:lock1", exam_id="ex:03")
        sid = session["session_id"]
        self.service.record_event(session_id=sid, event_type="DEVTOOLS_OPENED", confidence_score=1.0) # +35
        self.service.record_event(session_id=sid, event_type="DEVTOOLS_OPENED", confidence_score=1.0) # +35 -> 70
        res = self.service.record_event(session_id=sid, event_type="TAB_SWITCHED", confidence_score=1.0) # +15 -> 85
        self.assertTrue(res["is_locked"])
        self.assertEqual(res["action_taken"], "EXAM_LOCKED")
        self.assertGreaterEqual(res["new_suspicion_score"], 75.0)

    def test_suspicion_score_capped_at_100(self):
        session = self.service.start_session(student_id="st:cap1", exam_id="ex:04")
        sid = session["session_id"]
        for _ in range(5):
            res = self.service.record_event(session_id=sid, event_type="DEVTOOLS_OPENED", confidence_score=1.0)
        self.assertEqual(res["new_suspicion_score"], 100.0)

    # --------------------------------------------------------------------------
    # 4. Report & Cryptographic Audit Hash Tests
    # --------------------------------------------------------------------------
    def test_get_session_report_clean(self):
        session = self.service.start_session(student_id="st:clean", exam_id="ex:clean")
        rep = self.service.get_session_report(session["session_id"])
        self.assertEqual(rep["overall_integrity_rating"], "CLEAN_ACADEMIC_RECORD")
        self.assertEqual(rep["final_suspicion_score"], 0.0)
        self.assertFalse(rep["is_locked"])

    def test_get_session_report_compromised(self):
        session = self.service.start_session(student_id="st:comp", exam_id="ex:comp")
        sid = session["session_id"]
        for _ in range(4):
            self.service.record_event(session_id=sid, event_type="DEVTOOLS_OPENED", confidence_score=1.0)
        rep = self.service.get_session_report(sid)
        self.assertEqual(rep["overall_integrity_rating"], "COMPROMISED")
        self.assertTrue(rep["is_locked"])

    def test_session_report_cryptographic_hash(self):
        rep = self.service.get_session_report(self.default_session_id)
        hash_val = rep["cryptographic_audit_hash"]
        self.assertEqual(len(hash_val), 64)
        # Consistent hash verification
        rep2 = self.service.get_session_report(self.default_session_id)
        self.assertEqual(rep2["cryptographic_audit_hash"], hash_val)

    # --------------------------------------------------------------------------
    # 5. Proctor Overrides Tests
    # --------------------------------------------------------------------------
    def test_proctor_override_unlock_exam(self):
        session = self.service.start_session(student_id="st:override_lock", exam_id="ex:05")
        sid = session["session_id"]
        # Lock exam
        for _ in range(3):
            self.service.record_event(session_id=sid, event_type="DEVTOOLS_OPENED", confidence_score=1.0)
        
        # Unlock via proctor
        res = self.service.apply_override(
            session_id=sid,
            proctor_id=self.proctor_id,
            action="UNLOCK_EXAM",
            justification_note="Candidate webcam verified, accidental click"
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["new_status"], "MONITORING")
        rep = self.service.get_session_report(sid)
        self.assertFalse(rep["is_locked"])

    def test_proctor_override_dismiss_warnings(self):
        session = self.service.start_session(student_id="st:override_warn", exam_id="ex:06")
        sid = session["session_id"]
        self.service.record_event(session_id=sid, event_type="TAB_SWITCHED", confidence_score=1.0)
        self.service.record_event(session_id=sid, event_type="TAB_SWITCHED", confidence_score=1.0)

        res = self.service.apply_override(
            session_id=sid,
            proctor_id=self.proctor_id,
            action="DISMISS_WARNINGS",
            justification_note="Candidate notification pop-up dismissed"
        )
        self.assertTrue(res["success"])
        rep = self.service.get_session_report(sid)
        self.assertLess(rep["final_suspicion_score"], 30.0)

    def test_proctor_override_flag_expulsion(self):
        session = self.service.start_session(student_id="st:expel", exam_id="ex:07")
        sid = session["session_id"]
        res = self.service.apply_override(
            session_id=sid,
            proctor_id=self.proctor_id,
            action="FLAG_FOR_EXPULSION",
            justification_note="Physical cheating device observed in mirror"
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["new_status"], "EXPULSION_RECOMMENDED")

    def test_proctor_override_nonexistent_session(self):
        res = self.service.apply_override(
            session_id="session:does_not_exist",
            proctor_id=self.proctor_id,
            action="UNLOCK_EXAM"
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["new_status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
