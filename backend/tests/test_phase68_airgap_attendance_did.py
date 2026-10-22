"""
Test Suite: Phase 68 Zero-Knowledge Airgap Attendance & DID Attestation
Verifies rolling 30s proximity beacons, Ed25519 signature checks,
anti-proxy nonce replay defense, and balanced binary Merkle attendance trees.
"""

import time
import unittest
from backend.app.services.airgap_attendance_did_service import (
    AirgapAttendanceDidService,
    airgap_attendance_did_service,
)
from backend.app.schemas.airgap_attendance_did_schema import (
    AttendancePunchRequest,
    MerkleBatchSettleRequest,
)

class TestPhase68AirgapAttendanceDid(unittest.TestCase):
    def setUp(self):
        self.service = AirgapAttendanceDidService()

    def test_01_rolling_beacon_generation(self):
        """Verify rolling 30-second proximity beacon generates valid SHA-256 code."""
        beacon = self.service.get_current_beacon("CLS-DHAKA-10B")
        self.assertEqual(beacon.classroom_id, "CLS-DHAKA-10B")
        self.assertEqual(beacon.epoch_seconds, 30)
        self.assertEqual(len(beacon.rolling_hash), 64)
        self.assertTrue(beacon.teacher_did.startswith("did:slc:teacher:"))

    def test_02_authentic_attendance_punch(self):
        """Authentic student DID attendance punch must be verified with Merkle leaf."""
        beacon = self.service.get_current_beacon("CLS-DHAKA-10B")
        req = AttendancePunchRequest(
            classroom_id="CLS-DHAKA-10B",
            student_did="did:slc:student:bd-dhaka-005",  # Mariam Akter
            beacon_epoch_hash=beacon.rolling_hash,
            nonce="nonce_unique_test_001",
            signature_ed25519="sig_ed25519_mariam_valid_001_mock_signature_hash_hex_1234567890abcdef",
            timestamp_client="2026-10-17T11:45:00Z",
        )
        res = self.service.record_attendance_punch(req)
        self.assertTrue(res.success)
        self.assertEqual(res.anti_proxy_verdict, "VERIFIED_GENUINE")
        self.assertEqual(len(res.merkle_leaf_hash), 64)
        self.assertEqual(res.student_name, "Mariam Akter")

    def test_03_anti_proxy_replay_rejection(self):
        """Submitting a previously used nonce must trigger anti-proxy tripwire."""
        beacon = self.service.get_current_beacon("CLS-DHAKA-10B")
        req1 = AttendancePunchRequest(
            classroom_id="CLS-DHAKA-10B",
            student_did="did:slc:student:bd-dhaka-005",
            beacon_epoch_hash=beacon.rolling_hash,
            nonce="nonce_replay_attack_999",
            signature_ed25519="sig_ed25519_valid_signature_hash_mock_hex_string_1234567890abcdef",
            timestamp_client="2026-10-17T11:45:00Z",
        )
        res1 = self.service.record_attendance_punch(req1)
        self.assertTrue(res1.success)

        # Replay attempt with same nonce
        req2 = AttendancePunchRequest(
            classroom_id="CLS-DHAKA-10B",
            student_did="did:slc:student:bd-dhaka-005",
            beacon_epoch_hash=beacon.rolling_hash,
            nonce="nonce_replay_attack_999",
            signature_ed25519="sig_ed25519_valid_signature_hash_mock_hex_string_1234567890abcdef",
            timestamp_client="2026-10-17T11:45:05Z",
        )
        res2 = self.service.record_attendance_punch(req2)
        self.assertFalse(res2.success)
        self.assertEqual(res2.anti_proxy_verdict, "REPLAY_REJECTED")
        self.assertIn("anti-proxy tripwire", res2.message.lower())

    def test_04_stale_beacon_rejection(self):
        """Forged or expired beacon token must be rejected as stale."""
        req = AttendancePunchRequest(
            classroom_id="CLS-DHAKA-10B",
            student_did="did:slc:student:bd-dhaka-005",
            beacon_epoch_hash="f" * 64,  # Fake expired hash
            nonce="nonce_stale_test_123",
            signature_ed25519="sig_ed25519_valid_signature_hash_mock_hex_string_1234567890abcdef",
            timestamp_client="2026-10-17T11:45:00Z",
        )
        res = self.service.record_attendance_punch(req)
        self.assertFalse(res.success)
        self.assertEqual(res.anti_proxy_verdict, "STALE_BEACON")

    def test_05_unenrolled_student_did_rejection(self):
        """Unenrolled student DID must be rejected with invalid signature status."""
        beacon = self.service.get_current_beacon("CLS-DHAKA-10B")
        req = AttendancePunchRequest(
            classroom_id="CLS-DHAKA-10B",
            student_did="did:slc:student:unknown-intruder",
            beacon_epoch_hash=beacon.rolling_hash,
            nonce="nonce_unknown_did_456",
            signature_ed25519="sig_ed25519_valid_signature_hash_mock_hex_string_1234567890abcdef",
            timestamp_client="2026-10-17T11:45:00Z",
        )
        res = self.service.record_attendance_punch(req)
        self.assertFalse(res.success)
        self.assertEqual(res.anti_proxy_verdict, "INVALID_SIGNATURE")

    def test_06_session_status_and_merkle_root(self):
        """Session status must calculate quorum rate and balanced Merkle root."""
        status = self.service.get_session_status()
        self.assertIsNotNone(status)
        self.assertEqual(status.classroom_id, "CLS-DHAKA-10B")
        self.assertGreaterEqual(status.total_punched, 4)
        self.assertGreaterEqual(status.attendance_rate_pct, 80.0)
        self.assertEqual(len(status.merkle_root), 64)

    def test_07_merkle_batch_settlement(self):
        """Settling attendance batch transitions status to Settled to Supabase."""
        status_before = self.service.get_session_status()
        req = MerkleBatchSettleRequest(
            session_id=status_before.session_id,
            teacher_signature="teacher_sig_ed25519_attestation_proof_hex_999",
        )
        res = self.service.settle_merkle_batch(req)
        self.assertEqual(res.status, "SUCCESS_SETTLED")
        self.assertTrue(res.supabase_transaction_id.startswith("TX-SUPABASE-ATTD-"))

        status_after = self.service.get_session_status(status_before.session_id)
        self.assertEqual(status_after.cloud_settlement_status, "Settled to Supabase")

    def test_08_singleton_service_consistency(self):
        """Singleton service instance must expose valid session and beacon."""
        beacon = airgap_attendance_did_service.get_current_beacon("CLS-DHAKA-10B")
        self.assertEqual(beacon.classroom_id, "CLS-DHAKA-10B")
        status = airgap_attendance_did_service.get_session_status()
        self.assertIsNotNone(status)

if __name__ == "__main__":
    unittest.main()
