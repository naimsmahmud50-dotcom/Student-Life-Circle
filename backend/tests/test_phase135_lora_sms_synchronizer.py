"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Rural Resilience & Offline SMS/LoRa Exam Synchronizer
 * TOPIC:     Phase 135 Ultra-Compressed Binary Payloads & Offline Disaster Recovery
 * FILE:      backend/tests/test_phase135_lora_sms_synchronizer.py
 * PHASE:     Phase 135 - Offline LoRa & SMS-Bridge Exam Synchronizer
 * PURPOSE:   Automated test suite validating:
 *            1. Developer Architecture Note headers & file presence
 *            2. Strict Zero-Emoji compliance
 *            3. 100-MCQ dense bit-packing (38 bytes) and exact roundtrip fidelity
 *            4. CRC-16-CCITT calculation and bit-flip detection
 *            5. Offline HMAC-SHA256 signature and anti-tamper security
 *            6. Full 87-byte datagram serialization <= 140 byte budget constraint
 *            7. Hex PDU and Base85 SMS string encoding/decoding
 *            8. Gateway reception, auto-grading, and duplicate packet suppression
 *            9. Supabase migration 013 Row Level Security policies
 *            10. Frontend console markup and 3D tactile button styling
 * STANDARDS: Zero-Emoji, Disaster Resilient, Cryptographic Signatures, Low-Bandwidth
 */
"""

import os
import re
import unittest
from pathlib import Path

from backend.rural.lora_sms_synchronizer import (
    BinaryExamDatagram,
    CRCCalculator,
    CorruptedPacketChecksumException,
    DenseBitPacker,
    InvalidDatagramSizeException,
    LoRaSMSSynchronizerService,
    MCQOption,
    OfflineSignatureEngine,
    ReconciledAnswerSheet,
    TamperedOfflineSignatureException,
)

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase135LoRaSMSSynchronizer(unittest.TestCase):
    """
    Automated verification suite for Phase 135 Offline LoRa & SMS-Bridge Rural Exam Synchronizer.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.rural_init = cls.root_dir / "backend" / "rural" / "__init__.py"
        cls.sync_py = cls.root_dir / "backend" / "rural" / "lora_sms_synchronizer.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "013_offline_lora_mesh_rls.sql"
        cls.synchronizer_tsx = cls.root_dir / "frontend" / "src" / "pages" / "rural" / "synchronizer.tsx"
        cls.test_py = cls.root_dir / "backend" / "tests" / "test_phase135_lora_sms_synchronizer.py"

    def test_01_all_phase135_files_exist_with_developer_headers(self):
        """Validates that all Phase 135 core files exist and possess mandatory Developer Architecture Note headers."""
        target_files = [
            self.rural_init,
            self.sync_py,
            self.migration_sql,
            self.synchronizer_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Missing required Phase 135 file: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE:", content, f"Missing Architecture header in {file_path}")
            self.assertIn("Phase 135", content, f"Missing Phase 135 reference in {file_path}")
            self.assertIn("Rural Resilience & Offline SMS/LoRa Exam Synchronizer", content, f"Missing module in {file_path}")

    def test_02_zero_emoji_compliance(self):
        """Strictly enforces zero emoji in all created Phase 135 code and migration files."""
        target_files = [
            self.rural_init,
            self.sync_py,
            self.migration_sql,
            self.synchronizer_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(len(matches), 0, f"Emoji violations detected in {file_path}: {matches}")

    def test_03_dense_bit_packing_100_mcqs_size_and_limits(self):
        """Validates that 100 MCQs pack into exactly 38 bytes and enforces bounds."""
        answers = [MCQOption.A] * 100
        packed = DenseBitPacker.pack(answers)
        self.assertEqual(len(packed), 38, f"Expected 38 bytes for 100 questions, got {len(packed)}")

        # Enforce exactly 100 questions
        with self.assertRaises(ValueError):
            DenseBitPacker.pack([MCQOption.A] * 99)

        with self.assertRaises(ValueError):
            DenseBitPacker.pack([MCQOption.A] * 101)

    def test_04_exact_bitwise_roundtrip_fidelity(self):
        """Verifies 100% roundtrip fidelity across all MCQ options (Unanswered, A, B, C, D)."""
        test_patterns = [
            [MCQOption.UNANSWERED] * 100,
            [MCQOption.A] * 100,
            [MCQOption.B] * 100,
            [MCQOption.C] * 100,
            [MCQOption.D] * 100,
            # Pattern with rotating options
            [MCQOption(i % 5) for i in range(100)],
            # Alternating choices
            [MCQOption.A if i % 2 == 0 else MCQOption.D for i in range(100)],
        ]

        for pattern in test_patterns:
            packed = DenseBitPacker.pack(pattern)
            self.assertEqual(len(packed), 38)
            unpacked = DenseBitPacker.unpack(packed, total_questions=100)
            self.assertEqual(pattern, unpacked, "Bit-packing roundtrip failed to reproduce exact MCQ sequence")

    def test_05_crc16_checksum_calculation_and_bit_flip_detection(self):
        """Validates CRC-16-CCITT checksum computation and detection of single bit-flips."""
        data = b"STUDENT_LIFE_CIRCLE_PHASE_135_RESILIENCE"
        crc = CRCCalculator.calculate(data)
        self.assertIsInstance(crc, int)
        self.assertTrue(0 <= crc <= 0xFFFF)

        # Verification on unaltered payload
        self.assertTrue(CRCCalculator.verify(data, crc))

        # Single bit-flip simulation
        corrupted_data = bytearray(data)
        corrupted_data[0] ^= 0x01
        self.assertFalse(CRCCalculator.verify(bytes(corrupted_data), crc))

    def test_06_offline_hmac_sha256_cryptographic_signature_tamper_detection(self):
        """Verifies offline HMAC-SHA256 signature generation and detects tampering."""
        secret = "RURAL_OFFLINE_SECRET_KEY_2026"
        header = b"BAP1_TEST_HEADER"
        answers = b"\x01" * 38

        sig = OfflineSignatureEngine.sign(header, answers, secret)
        self.assertEqual(len(sig), 32, "Signature must be 32 bytes (256 bits)")

        # Verify authentic signature
        self.assertTrue(OfflineSignatureEngine.verify(header, answers, sig, secret))

        # Tampered answers must fail verification
        tampered_answers = bytearray(answers)
        tampered_answers[5] ^= 0xFF
        self.assertFalse(OfflineSignatureEngine.verify(header, bytes(tampered_answers), sig, secret))

        # Wrong secret key must fail verification
        self.assertFalse(OfflineSignatureEngine.verify(header, answers, sig, "WRONG_SECRET_KEY"))

    def test_07_full_datagram_packing_and_140_byte_budget(self):
        """Verifies full datagram size fits strictly within 140-byte constraint (actual 87 bytes)."""
        answers = [MCQOption((i % 4) + 1) for i in range(100)]
        student_id = "STU-RURAL-88102"
        exam_id = "EXAM-HSC-PHY-2026"
        secret = "SECURE_OFFLINE_DEVICE_SALT"

        datagram = BinaryExamDatagram.create(
            student_id=student_id,
            exam_id=exam_id,
            answers=answers,
            secret_key=secret,
            sequence_num=1,
        )

        serialized = datagram.to_bytes()
        # Budget check: <= 140 bytes GSM SMS PDU / LoRa MTU
        self.assertLessEqual(len(serialized), 140, "Datagram exceeds 140-byte GSM SMS / LoRa MTU limit")
        self.assertEqual(len(serialized), 87, f"Expected 87 bytes total, got {len(serialized)}")

        # Deserialization & field verification
        reconstructed = BinaryExamDatagram.from_bytes(serialized, expected_secret_key=secret)
        self.assertEqual(reconstructed.header.student_roll_hash, datagram.header.student_roll_hash)
        self.assertEqual(reconstructed.header.exam_id_hash, datagram.header.exam_id_hash)
        self.assertEqual(reconstructed.answers, answers)

        # Hex PDU representation
        hex_pdu = datagram.to_hex_pdu()
        self.assertEqual(len(hex_pdu), 87 * 2)  # 174 hex characters
        from_hex = BinaryExamDatagram.from_hex_pdu(hex_pdu, expected_secret_key=secret)
        self.assertEqual(from_hex.header.student_roll_hash, datagram.header.student_roll_hash)

        # Base85 SMS representation (fits inside single 160-char SMS)
        base85_str = datagram.to_base85_sms()
        self.assertLessEqual(len(base85_str), 160, "Base85 string exceeds 160-character GSM SMS limit")
        from_base85 = BinaryExamDatagram.from_base85_sms(base85_str, expected_secret_key=secret)
        self.assertEqual(from_base85.header.exam_id_hash, datagram.header.exam_id_hash)

    def test_08_corrupted_checksum_raises_exception(self):
        """Verifies that corrupted packet checksum raises CorruptedPacketChecksumException."""
        answers = [MCQOption.A] * 100
        datagram = BinaryExamDatagram.create("STU-1", "EXAM-1", answers, "SECRET")
        serialized = bytearray(datagram.to_bytes())

        # Corrupt CRC byte
        serialized[-1] ^= 0xFF

        with self.assertRaises(CorruptedPacketChecksumException):
            BinaryExamDatagram.from_bytes(bytes(serialized), expected_secret_key="SECRET")

    def test_09_tampered_signature_raises_exception(self):
        """Verifies that tampered signature raises TamperedOfflineSignatureException."""
        answers = [MCQOption.A] * 100
        datagram = BinaryExamDatagram.create("STU-1", "EXAM-1", answers, "SECRET")
        serialized = bytearray(datagram.to_bytes())

        # Corrupt a signature byte (offset 15 + 38 = 53 to 85)
        serialized[60] ^= 0x55

        # Recalculate CRC on corrupted payload so CRC passes but signature fails
        payload_without_crc = serialized[:-2]
        new_crc = CRCCalculator.calculate(bytes(payload_without_crc))
        serialized[-2] = (new_crc >> 8) & 0xFF
        serialized[-1] = new_crc & 0xFF

        with self.assertRaises(TamperedOfflineSignatureException):
            BinaryExamDatagram.from_bytes(bytes(serialized), expected_secret_key="SECRET")

    def test_10_gateway_reconciliation_scoring_and_deduplication(self):
        """Verifies gateway packet ingestion, auto-scoring against answer key, and duplicate suppression."""
        service = LoRaSMSSynchronizerService(gateway_node_id="GW-SUNDARBAN-01")

        # Answer key: 100 questions where correct answer is (i % 4) + 1
        answer_key = [MCQOption((i % 4) + 1) for i in range(100)]
        secret = "SHARED_EXAM_SECRET"

        # Student 1 answered all 100 correctly
        student_answers = list(answer_key)
        datagram = BinaryExamDatagram.create("STU-PERFECT", "EXAM-HSC-PHY-2026", student_answers, secret)

        result = service.reconcile_packet(
            datagram_bytes=datagram.to_bytes(),
            answer_key=answer_key,
            expected_secret_key=secret,
            transport_channel="LORA_MESH",
            rssi_dbm=-92.0,
            snr_db=8.5,
        )

        self.assertFalse(result.is_duplicate)
        self.assertTrue(result.signature_verified)
        self.assertEqual(result.score, 100.0)
        self.assertEqual(result.grade, "A+")
        self.assertEqual(result.answers_summary["correct_count"], 100)
        self.assertEqual(result.answers_summary["incorrect_count"], 0)

        # Duplicate ingestion of the same packet
        duplicate_result = service.reconcile_packet(
            datagram_bytes=datagram.to_bytes(),
            answer_key=answer_key,
            expected_secret_key=secret,
            transport_channel="GSM_SMS_PDU",
        )

        self.assertTrue(duplicate_result.is_duplicate)
        self.assertEqual(service.duplicate_count, 1)

    def test_11_migration_013_supabase_rls_security(self):
        """Verifies that migration 013 enables and forces RLS on all 4 tables with zero-IDOR policies."""
        sql_content = self.migration_sql.read_text(encoding="utf-8")
        required_tables = [
            "lora_gateway_nodes",
            "rural_exam_packets",
            "offline_signed_answer_sheets",
            "reconciliation_audit_logs",
        ]

        for table in required_tables:
            self.assertIn(f"ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;", sql_content)
            self.assertIn(f"ALTER TABLE public.{table} FORCE ROW LEVEL SECURITY;", sql_content)

        # Verify tenant isolation and service_role clauses
        self.assertIn("auth.uid()", sql_content)
        self.assertIn("service_role", sql_content)

    def test_12_frontend_rural_synchronizer_markup_and_tactile_styling(self):
        """Verifies frontend console contains required BAP-140 inspection, 3D tactile buttons, and Lucide icons."""
        tsx_content = self.synchronizer_tsx.read_text(encoding="utf-8")
        self.assertIn("BAP-140", tsx_content)
        self.assertIn("CRC-16-CCITT", tsx_content)
        self.assertIn("shadow-[0_4px_0_0_#051329] active:translate-y-1", tsx_content)
        self.assertIn("GATEWAY_NODES", tsx_content)
        self.assertIn("Base85", tsx_content)
        self.assertIn("toBengaliDigits", tsx_content)


if __name__ == "__main__":
    unittest.main()
