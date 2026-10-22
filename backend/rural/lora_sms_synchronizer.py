"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Rural Resilience & Offline SMS/LoRa Exam Synchronizer
 * TOPIC:     Phase 135 Ultra-Compressed Binary Payloads & Offline Disaster Recovery
 * FILE:      backend/rural/lora_sms_synchronizer.py
 * PHASE:     Phase 135 - Offline LoRa & SMS-Bridge Exam Synchronizer
 * PURPOSE:   Provides bit-level MCQ answer compression (100 questions in <= 140 bytes),
 *            CRC-16 validation, offline cryptographic signature authentication,
 *            and LoRa/SMS multi-channel reconciliation for grid-outage resilience.
 * STANDARDS: Zero-Emoji, Disaster Resilient, Cryptographic Signatures, Low-Bandwidth
 */
"""

import base64
import binascii
import hashlib
import hmac
import struct
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class MCQOption(int, Enum):
    UNANSWERED = 0
    A = 1
    B = 2
    C = 3
    D = 4


class TransmissionChannel(str, Enum):
    LORA_MESH = "LORA_MESH"
    GSM_SMS = "GSM_SMS"


class PacketExceedsMTUException(ValueError):
    """Raised when encoded datagram exceeds the 140-byte MTU limit."""
    pass


class InvalidDatagramSizeException(ValueError):
    """Raised when datagram size is malformed or invalid."""
    pass


class CorruptedPacketChecksumException(ValueError):
    """Raised when CRC-16 checksum verification fails due to transmission noise."""
    pass


class TamperedOfflineSignatureException(PermissionError):
    """Raised when cryptographic signature does not match device private secret."""
    pass


MAGIC_BYTE = 0xBD  # 189 in decimal: Bangladesh Datagram Identifier
PROTOCOL_VERSION = 0x01
MAX_ALLOWED_PACKET_BYTES = 140


class CRCCalculator:
    """CRC-16-CCITT implementation for bit-level radio packet corruption detection."""

    POLYNOMIAL = 0x1021
    INITIAL_VALUE = 0xFFFF

    @classmethod
    def calculate_crc16(cls, data: bytes) -> int:
        crc = cls.INITIAL_VALUE
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = ((crc << 1) ^ cls.POLYNOMIAL) & 0xFFFF
                else:
                    crc = (crc << 1) & 0xFFFF
        return crc

    @classmethod
    def calculate(cls, data: bytes) -> int:
        return cls.calculate_crc16(data)

    @classmethod
    def verify_crc16(cls, data: bytes, expected_crc: int) -> bool:
        return cls.calculate_crc16(data) == expected_crc

    @classmethod
    def verify(cls, data: bytes, expected_crc: int) -> bool:
        return cls.verify_crc16(data, expected_crc)


class DenseBitPacker:
    """
    Compresses 100 MCQ responses into dense 3-bit tokens.
    100 questions * 3 bits = 300 bits = 37.5 bytes -> 38 bytes padded.
    """

    @classmethod
    def pack_100_mcqs(cls, answers: List[MCQOption]) -> bytes:
        if len(answers) != 100:
            raise ValueError(f"Expected exactly 100 MCQ answers, received {len(answers)}")

        # 300 bits total -> 38 bytes
        bit_buffer = 0
        bit_count = 0
        byte_chunks = bytearray()

        for opt in answers:
            # 3 bits per answer (values 0..4 fit in 3 bits: 000 to 100)
            val = opt.value & 0x07
            bit_buffer = (bit_buffer << 3) | val
            bit_count += 3

            while bit_count >= 8:
                shift = bit_count - 8
                byte_val = (bit_buffer >> shift) & 0xFF
                byte_chunks.append(byte_val)
                bit_count -= 8
                bit_buffer &= (1 << bit_count) - 1

        if bit_count > 0:
            # Pad remaining bits to complete final byte
            byte_val = (bit_buffer << (8 - bit_count)) & 0xFF
            byte_chunks.append(byte_val)

        return bytes(byte_chunks)

    @classmethod
    def pack(cls, answers: List[MCQOption]) -> bytes:
        return cls.pack_100_mcqs(answers)

    @classmethod
    def unpack_100_mcqs(cls, payload: bytes, total_questions: int = 100) -> List[MCQOption]:
        if len(payload) < 38:
            raise ValueError(f"Invalid answer payload size: {len(payload)} bytes. Required at least 38 bytes.")

        bit_buffer = 0
        bit_count = 0
        byte_index = 0
        answers: List[MCQOption] = []

        while len(answers) < total_questions:
            while bit_count < 3 and byte_index < len(payload):
                bit_buffer = (bit_buffer << 8) | payload[byte_index]
                bit_count += 8
                byte_index += 1

            if bit_count < 3:
                break

            shift = bit_count - 3
            val = (bit_buffer >> shift) & 0x07
            bit_count -= 3
            bit_buffer &= (1 << bit_count) - 1

            # Validate enum bounds
            if val > 4:
                val = 0
            answers.append(MCQOption(val))

        # Fill remaining with UNANSWERED if incomplete
        while len(answers) < total_questions:
            answers.append(MCQOption.UNANSWERED)

        return answers

    @classmethod
    def unpack(cls, payload: bytes, total_questions: int = 100) -> List[MCQOption]:
        return cls.unpack_100_mcqs(payload, total_questions)


class OfflineSignatureEngine:
    """Cryptographic signing engine securing offline exam packets before radio broadcast."""

    DEFAULT_TEST_SECRET = b"OGROJATRA_DISASTER_RECOVERY_KEY_2026"

    @classmethod
    def sign_payload(cls, binary_envelope: bytes, device_secret: Union[bytes, str] = DEFAULT_TEST_SECRET) -> bytes:
        """Computes 32-byte HMAC-SHA256 signature tag."""
        if isinstance(device_secret, str):
            device_secret = device_secret.encode("utf-8")
        return hmac.new(device_secret, binary_envelope, hashlib.sha256).digest()

    @classmethod
    def sign(cls, header: bytes, answers: Optional[bytes] = None, secret: Union[bytes, str] = DEFAULT_TEST_SECRET) -> bytes:
        data = header + (answers if answers is not None else b"")
        return cls.sign_payload(data, secret)

    @classmethod
    def verify_signature(
        cls,
        binary_envelope: bytes,
        signature_tag: bytes,
        device_secret: Union[bytes, str] = DEFAULT_TEST_SECRET
    ) -> bool:
        if isinstance(device_secret, str):
            device_secret = device_secret.encode("utf-8")
        expected = cls.sign_payload(binary_envelope, device_secret)
        if not hmac.compare_digest(expected, signature_tag):
            raise TamperedOfflineSignatureException("Offline signature mismatch: Packet altered or invalid device key.")
        return True

    @classmethod
    def verify(
        cls,
        header: bytes,
        answers: Optional[bytes] = None,
        signature: Optional[bytes] = None,
        secret: Union[bytes, str] = DEFAULT_TEST_SECRET
    ) -> bool:
        if signature is not None and answers is not None:
            data = header + answers
            sig_to_check = signature
        else:
            data = header
            sig_to_check = answers if answers is not None else b""
        try:
            return cls.verify_signature(data, sig_to_check, secret)
        except TamperedOfflineSignatureException:
            return False


@dataclass
class PacketHeader:
    magic: int = MAGIC_BYTE
    version: int = PROTOCOL_VERSION
    channel: TransmissionChannel = TransmissionChannel.LORA_MESH
    student_roll_hash: int = 0      # 4 bytes uint32
    exam_id_hash: int = 0           # 4 bytes uint32
    submission_epoch: int = 0       # 4 bytes uint32 timestamp


@dataclass
class BinaryExamDatagram:
    header: PacketHeader
    answers_payload: bytes          # 38 bytes
    signature_tag: bytes            # 32 bytes
    crc16: int                      # 2 bytes uint16
    total_bytes: int = 0
    student_id: str = ""
    exam_id: str = ""
    sequence_num: int = 1

    @property
    def answers(self) -> List[MCQOption]:
        return DenseBitPacker.unpack_100_mcqs(self.answers_payload, total_questions=100)

    @classmethod
    def create(
        cls,
        student_id: Optional[str] = None,
        exam_id: Optional[str] = None,
        answers: Optional[List[MCQOption]] = None,
        secret_key: Optional[Union[bytes, str]] = None,
        channel: Union[TransmissionChannel, str] = TransmissionChannel.LORA_MESH,
        sequence_num: int = 1,
        submission_epoch: Optional[int] = None,
        student_roll: Optional[str] = None,
        device_secret: Optional[Union[bytes, str]] = None,
    ) -> "BinaryExamDatagram":
        resolved_student = student_id if student_id is not None else (student_roll if student_roll is not None else "STU-UNKNOWN")
        resolved_exam = exam_id if exam_id is not None else "EXAM-UNKNOWN"
        resolved_secret = secret_key if secret_key is not None else (device_secret if device_secret is not None else OfflineSignatureEngine.DEFAULT_TEST_SECRET)
        if isinstance(resolved_secret, str):
            resolved_secret = resolved_secret.encode("utf-8")
        if isinstance(channel, str):
            channel = TransmissionChannel.LORA_MESH if "LORA" in channel.upper() else TransmissionChannel.GSM_SMS

        answers_list = answers if answers is not None else [MCQOption.UNANSWERED] * 100

        # 1. Hashes for header
        s_hash = struct.unpack(">I", hashlib.sha256(resolved_student.encode()).digest()[:4])[0]
        e_hash = struct.unpack(">I", hashlib.sha256(resolved_exam.encode()).digest()[:4])[0]
        epoch = submission_epoch if submission_epoch is not None else int(time.time())

        header = PacketHeader(
            magic=MAGIC_BYTE,
            version=PROTOCOL_VERSION,
            channel=channel,
            student_roll_hash=s_hash,
            exam_id_hash=e_hash,
            submission_epoch=epoch,
        )

        # 2. Pack 100 MCQs
        answers_bytes = DenseBitPacker.pack_100_mcqs(answers_list)

        # 3. Channel byte
        ch_byte = 0x01 if channel == TransmissionChannel.LORA_MESH else 0x02

        # 4. Construct envelope for signing (Header + Answers)
        envelope = struct.pack(
            ">BBBIII",
            header.magic,
            header.version,
            ch_byte,
            header.student_roll_hash,
            header.exam_id_hash,
            header.submission_epoch,
        ) + answers_bytes

        # 5. Sign envelope
        signature = OfflineSignatureEngine.sign_payload(envelope, resolved_secret)

        # 6. Calculate CRC-16 over (Envelope + Signature)
        payload_with_sig = envelope + signature
        crc = CRCCalculator.calculate_crc16(payload_with_sig)

        total_size = len(payload_with_sig) + 2
        if total_size > MAX_ALLOWED_PACKET_BYTES:
            raise PacketExceedsMTUException(
                f"Packet size {total_size} bytes exceeds maximum allowed MTU of {MAX_ALLOWED_PACKET_BYTES} bytes."
            )

        return cls(
            header=header,
            answers_payload=answers_bytes,
            signature_tag=signature,
            crc16=crc,
            total_bytes=total_size,
            student_id=resolved_student,
            exam_id=resolved_exam,
            sequence_num=sequence_num,
        )

    def serialize_bytes(self) -> bytes:
        ch_byte = 0x01 if self.header.channel == TransmissionChannel.LORA_MESH else 0x02
        envelope = struct.pack(
            ">BBBIII",
            self.header.magic,
            self.header.version,
            ch_byte,
            self.header.student_roll_hash,
            self.header.exam_id_hash,
            self.header.submission_epoch,
        ) + self.answers_payload + self.signature_tag + struct.pack(">H", self.crc16)
        return envelope

    def to_bytes(self) -> bytes:
        return self.serialize_bytes()

    def to_hex_pdu(self) -> str:
        return binascii.hexlify(self.serialize_bytes()).decode("utf-8").upper()

    def to_base85_sms(self) -> str:
        return base64.b85encode(self.serialize_bytes()).decode("utf-8")

    @classmethod
    def parse_bytes(cls, raw: bytes, device_secret: Union[bytes, str] = OfflineSignatureEngine.DEFAULT_TEST_SECRET) -> "BinaryExamDatagram":
        if isinstance(device_secret, str):
            device_secret = device_secret.encode("utf-8")

        if len(raw) < 87:
            raise ValueError(f"Packet too short: {len(raw)} bytes.")
        if len(raw) > MAX_ALLOWED_PACKET_BYTES:
            raise PacketExceedsMTUException(f"Packet size {len(raw)} exceeds {MAX_ALLOWED_PACKET_BYTES} bytes.")

        # Extract CRC
        payload_body = raw[:-2]
        expected_crc = struct.unpack(">H", raw[-2:])[0]
        actual_crc = CRCCalculator.calculate_crc16(payload_body)
        if expected_crc != actual_crc:
            raise CorruptedPacketChecksumException(
                f"CRC-16 mismatch: expected {hex(expected_crc)}, got {hex(actual_crc)}. Data corrupted in transit."
            )

        # Unpack header
        header_len = 1 + 1 + 1 + 4 + 4 + 4  # 15 bytes
        magic, ver, ch_byte, s_hash, e_hash, epoch = struct.unpack(">BBBIII", payload_body[:header_len])
        if magic != MAGIC_BYTE:
            raise ValueError(f"Invalid magic byte: {hex(magic)}, expected {hex(MAGIC_BYTE)}.")

        channel = TransmissionChannel.LORA_MESH if ch_byte == 0x01 else TransmissionChannel.GSM_SMS

        # Answers payload is 38 bytes
        answers_bytes = payload_body[header_len:header_len + 38]

        # Signature tag is 32 bytes
        sig_tag = payload_body[header_len + 38:header_len + 38 + 32]

        # Verify offline signature
        envelope = payload_body[:header_len + 38]
        OfflineSignatureEngine.verify_signature(envelope, sig_tag, device_secret)

        header = PacketHeader(
            magic=magic,
            version=ver,
            channel=channel,
            student_roll_hash=s_hash,
            exam_id_hash=e_hash,
            submission_epoch=epoch,
        )

        return cls(
            header=header,
            answers_payload=answers_bytes,
            signature_tag=sig_tag,
            crc16=actual_crc,
            total_bytes=len(raw),
            student_id="",
            exam_id="",
            sequence_num=1,
        )

    @classmethod
    def from_bytes(cls, raw: bytes, expected_secret_key: Union[bytes, str] = OfflineSignatureEngine.DEFAULT_TEST_SECRET) -> "BinaryExamDatagram":
        return cls.parse_bytes(raw, expected_secret_key)

    @classmethod
    def from_hex_pdu(cls, hex_str: str, expected_secret_key: Union[bytes, str] = OfflineSignatureEngine.DEFAULT_TEST_SECRET) -> "BinaryExamDatagram":
        raw = binascii.unhexlify(hex_str.strip())
        return cls.from_bytes(raw, expected_secret_key)

    @classmethod
    def from_base85_sms(cls, b85_str: str, expected_secret_key: Union[bytes, str] = OfflineSignatureEngine.DEFAULT_TEST_SECRET) -> "BinaryExamDatagram":
        raw = base64.b85decode(b85_str.strip().encode("utf-8"))
        return cls.from_bytes(raw, expected_secret_key)


@dataclass
class ReconciledExamResult:
    student_roll: str
    exam_id: str
    total_questions: int
    attempted_count: int
    correct_count: int
    incorrect_count: int
    score: float
    percentage: float
    channel: TransmissionChannel
    transmission_bytes: int
    reconciled_at: float = field(default_factory=time.time)


@dataclass
class ReconciledAnswerSheet:
    packet_id: str
    student_id: str
    exam_id: str
    transport_channel: str
    answered_count: int
    score: float
    grade: str
    is_duplicate: bool
    signature_verified: bool
    answers_summary: Dict[str, Any]
    reconciled_at: float = field(default_factory=time.time)


class LoRaSMSSynchronizerService:
    """
    Central server clearinghouse receiving radio and SMS datagrams from rural stations,
    deduplicating multi-path packets, and scoring answers.
    """

    def __init__(self, gateway_node_id: str = "GW-SUNDARBAN-01", device_secret: Union[bytes, str] = OfflineSignatureEngine.DEFAULT_TEST_SECRET):
        self.gateway_node_id = gateway_node_id
        if isinstance(device_secret, str):
            device_secret = device_secret.encode("utf-8")
        self.device_secret = device_secret
        # packet_hash -> BinaryExamDatagram
        self._received_packets: Dict[str, BinaryExamDatagram] = {}
        # exam_id -> answer_key
        self._exam_answer_keys: Dict[str, List[MCQOption]] = {}
        self.duplicate_count: int = 0

    def register_exam_answer_key(self, exam_id: str, key: List[MCQOption]) -> None:
        if len(key) != 100:
            raise ValueError("Official answer key must contain exactly 100 questions.")
        self._exam_answer_keys[exam_id] = key

    def reconcile_packet(
        self,
        datagram_bytes: bytes,
        answer_key: Optional[List[MCQOption]] = None,
        expected_secret_key: Union[bytes, str] = OfflineSignatureEngine.DEFAULT_TEST_SECRET,
        transport_channel: str = "LORA_MESH",
        rssi_dbm: float = -92.0,
        snr_db: float = 8.5,
    ) -> ReconciledAnswerSheet:
        """
        Ingests datagram bytes, verifies signature and CRC, grades answers, and checks for duplicates.
        """
        packet_hash = hashlib.sha256(datagram_bytes).hexdigest()
        is_duplicate = packet_hash in self._received_packets
        if is_duplicate:
            self.duplicate_count += 1

        datagram = BinaryExamDatagram.from_bytes(datagram_bytes, expected_secret_key)
        self._received_packets[packet_hash] = datagram

        unpacked = DenseBitPacker.unpack_100_mcqs(datagram.answers_payload, 100)
        resolved_key = answer_key if answer_key is not None else [MCQOption((i % 4) + 1) for i in range(100)]

        correct = 0
        incorrect = 0
        answered = 0

        for given, expected in zip(unpacked, resolved_key):
            if given != MCQOption.UNANSWERED:
                answered += 1
                if given == expected:
                    correct += 1
                else:
                    incorrect += 1

        score = float(correct)
        if score >= 80:
            grade = "A+"
        elif score >= 70:
            grade = "A"
        elif score >= 60:
            grade = "A-"
        elif score >= 50:
            grade = "B"
        elif score >= 40:
            grade = "C"
        elif score >= 33:
            grade = "D"
        else:
            grade = "F"

        packet_id = f"PKT-{transport_channel[:4]}-{packet_hash[:6].upper()}"

        return ReconciledAnswerSheet(
            packet_id=packet_id,
            student_id=datagram.student_id or "STU-RURAL",
            exam_id=datagram.exam_id or "EXAM-RURAL",
            transport_channel=transport_channel,
            answered_count=answered,
            score=score,
            grade=grade,
            is_duplicate=is_duplicate,
            signature_verified=True,
            answers_summary={
                "total_questions": 100,
                "answered_count": answered,
                "correct_count": correct,
                "incorrect_count": incorrect,
                "rssi_dbm": rssi_dbm,
                "snr_db": snr_db,
            }
        )

    def receive_and_reconcile_packet(
        self,
        raw_packet_bytes: bytes,
        student_roll: str,
        exam_id: str
    ) -> Tuple[bool, ReconciledExamResult, str]:
        """
        Receives packet, performs deduplication, decodes answers, and computes exam grade.
        """
        packet_hash = hashlib.sha256(raw_packet_bytes).hexdigest()
        is_duplicate = packet_hash in self._received_packets
        if is_duplicate:
            self.duplicate_count += 1

        datagram = BinaryExamDatagram.parse_bytes(raw_packet_bytes, self.device_secret)
        self._received_packets[packet_hash] = datagram

        # Extract 100 answers
        unpacked_answers = DenseBitPacker.unpack_100_mcqs(datagram.answers_payload, total_questions=100)

        # Grade against registered answer key or default benchmark
        answer_key = self._exam_answer_keys.get(exam_id)
        if not answer_key:
            answer_key = [MCQOption((i % 4) + 1) for i in range(100)]

        correct = 0
        incorrect = 0
        attempted = 0

        for given, expected in zip(unpacked_answers, answer_key):
            if given != MCQOption.UNANSWERED:
                attempted += 1
                if given == expected:
                    correct += 1
                else:
                    incorrect += 1

        score = float(correct)
        percentage = (score / 100.0) * 100.0

        result = ReconciledExamResult(
            student_roll=student_roll,
            exam_id=exam_id,
            total_questions=100,
            attempted_count=attempted,
            correct_count=correct,
            incorrect_count=incorrect,
            score=score,
            percentage=percentage,
            channel=datagram.header.channel,
            transmission_bytes=datagram.total_bytes,
        )

        status_msg = "ডুপ্লিকেট প্যাকেট সনাক্ত (পূর্বেই সিঙ্ক হয়েছে)" if is_duplicate else "সফলভাবে ডিকোড ও সিঙ্ক সম্পন্ন"
        return is_duplicate, result, status_msg
