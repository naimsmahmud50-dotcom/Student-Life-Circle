"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Rural Resilience & Offline SMS/LoRa Exam Synchronizer
 * TOPIC:     Phase 135 Ultra-Compressed Binary Payloads & Offline Disaster Recovery
 * FILE:      backend/rural/__init__.py
 * PHASE:     Phase 135 - Offline LoRa & SMS-Bridge Exam Synchronizer
 * PURPOSE:   Exposes rural offline exam datagram models, bit-packing codecs,
 *            cryptographic offline signature verifiers, and multi-channel reconcilers.
 * STANDARDS: Zero-Emoji, Disaster Resilient, Cryptographic Signatures, Low-Bandwidth
 */
"""

from .lora_sms_synchronizer import (
    MCQOption,
    TransmissionChannel,
    PacketHeader,
    BinaryExamDatagram,
    ReconciledExamResult,
    ReconciledAnswerSheet,
    DenseBitPacker,
    CRCCalculator,
    OfflineSignatureEngine,
    PacketExceedsMTUException,
    InvalidDatagramSizeException,
    CorruptedPacketChecksumException,
    TamperedOfflineSignatureException,
    LoRaSMSSynchronizerService,
)

__all__ = [
    "MCQOption",
    "TransmissionChannel",
    "PacketHeader",
    "BinaryExamDatagram",
    "ReconciledExamResult",
    "ReconciledAnswerSheet",
    "DenseBitPacker",
    "CRCCalculator",
    "OfflineSignatureEngine",
    "PacketExceedsMTUException",
    "InvalidDatagramSizeException",
    "CorruptedPacketChecksumException",
    "TamperedOfflineSignatureException",
    "LoRaSMSSynchronizerService",
]
