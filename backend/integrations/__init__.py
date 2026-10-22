"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Ministry Accreditation & National Curriculum API Gateway
 * TOPIC:     Phase 131 National Education Board Webhook Clearinghouse & Ed25519 Signatures
 * FILE:      backend/integrations/__init__.py
 * PHASE:     Phase 131 - National Curriculum Accreditation API Gateway
 * PURPOSE:   Exports the Education Board Gateway clearinghouse classes and cryptography.
 * STANDARDS: Zero-Emoji, ASVS L2, Ed25519 Cryptographic Signatures, Rate Limiting
 */
"""

from backend.integrations.education_board_gateway import (
    EducationBoardGateway,
    EducationBoardNode,
    BoardNodeType,
    W3CVerifiableCredential,
    WebhookEvent,
    Ed25519SignatureVerifier,
    IPNotWhitelistedException,
    RateLimitExceededException,
    InvalidSignatureException,
    BOARD_REGISTRY,
)

__all__ = [
    "EducationBoardGateway",
    "EducationBoardNode",
    "BoardNodeType",
    "W3CVerifiableCredential",
    "WebhookEvent",
    "Ed25519SignatureVerifier",
    "IPNotWhitelistedException",
    "RateLimitExceededException",
    "InvalidSignatureException",
    "BOARD_REGISTRY",
]
