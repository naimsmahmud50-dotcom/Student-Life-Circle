"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Ministry Accreditation & National Curriculum API Gateway
 * TOPIC:     Phase 131 National Education Board Webhook Clearinghouse & Ed25519 Signatures
 * FILE:      backend/integrations/education_board_gateway.py
 * PHASE:     Phase 131 - National Curriculum Accreditation API Gateway
 * PURPOSE:   Provides institutional clearinghouse interconnections with NCTB and 11
 *            National Education Boards using Ed25519 cryptographic non-repudiation,
 *            W3C Verifiable Credentials batch synchronization, IP whitelisting, and
 *            sliding-window rate limiting.
 * STANDARDS: Zero-Emoji, ASVS L2, Ed25519 Cryptographic Signatures, Rate Limiting
 */
"""

import binascii
import ipaddress
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519


class IPNotWhitelistedException(PermissionError):
    """Raised when an incoming board webhook request originates from an unverified IP address."""
    pass


class RateLimitExceededException(RuntimeError):
    """Raised when a board node exceeds its allotted API quota (60 req/min)."""
    pass


class InvalidSignatureException(ValueError):
    """Raised when Ed25519 digital signature fails mathematical verification or payload is tampered."""
    pass


class StaleWebhookTimestampException(ValueError):
    """Raised when webhook timestamp exceeds allowable drift window (anti-replay defense)."""
    pass


class BoardNodeType(str, Enum):
    NCTB = "NCTB"
    DHAKA = "DHAKA"
    CHITTAGONG = "CHITTAGONG"
    RAJSHAHI = "RAJSHAHI"
    COMILLA = "COMILLA"
    JESSORE = "JESSORE"
    BARISAL = "BARISAL"
    SYLHET = "SYLHET"
    DINAJPUR = "DINAJPUR"
    MYMENSINGH = "MYMENSINGH"
    MADRASAH = "MADRASAH"
    TECHNICAL = "TECHNICAL"


@dataclass
class EducationBoardNode:
    """Registered institutional education board node in the national clearinghouse."""
    id: str
    name_bn: str
    name_en: str
    board_type: BoardNodeType
    endpoint_url: str
    public_key_hex: str
    whitelisted_ips: List[str]
    rate_limit_rpm: int = 60
    is_active: bool = True


# Canonical Registry of 12 Education Boards & NCTB
BOARD_REGISTRY: Dict[BoardNodeType, EducationBoardNode] = {
    BoardNodeType.NCTB: EducationBoardNode(
        id="node_nctb_gov",
        name_bn="জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB)",
        name_en="National Curriculum and Textbook Board",
        board_type=BoardNodeType.NCTB,
        endpoint_url="https://gateway.nctb.gov.bd/v1/accreditation",
        public_key_hex="bb50199ece5cbc10648ed3ad08ce2fdb730b320306b93eddd714fd8ec5ba0838",
        whitelisted_ips=["103.48.16.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.DHAKA: EducationBoardNode(
        id="node_dhaka_board",
        name_bn="মাধ্যমিক ও উচ্চমাধ্যমিক শিক্ষা বোর্ড, ঢাকা",
        name_en="Board of Intermediate & Secondary Education, Dhaka",
        board_type=BoardNodeType.DHAKA,
        endpoint_url="https://api.dhakaeducationboard.gov.bd/webhook",
        public_key_hex="a8e55f98e837691d11e6c9824e9f2bdf6313d264b1c68424f8771c10b7c5c861",
        whitelisted_ips=["103.48.17.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.CHITTAGONG: EducationBoardNode(
        id="node_ctg_board",
        name_bn="মাধ্যমিক ও উচ্চমাধ্যমিক শিক্ষা বোর্ড, চট্টগ্রাম",
        name_en="Board of Intermediate & Secondary Education, Chattogram",
        board_type=BoardNodeType.CHITTAGONG,
        endpoint_url="https://api.bise-ctg.gov.bd/webhook",
        public_key_hex="12aedd17b501126a2c17fb2b53f47d141a194b9aed9319b43054446eddd0f7ea",
        whitelisted_ips=["103.48.18.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.RAJSHAHI: EducationBoardNode(
        id="node_rajshahi_board",
        name_bn="মাধ্যমিক ও উচ্চমাধ্যমিক শিক্ষা বোর্ড, রাজশাহী",
        name_en="Board of Intermediate & Secondary Education, Rajshahi",
        board_type=BoardNodeType.RAJSHAHI,
        endpoint_url="https://api.rajshahieducationboard.gov.bd/webhook",
        public_key_hex="0364edbf40f7b15479db7609f96f0b41aead1e751e2dca651cb099bdf14d1b01",
        whitelisted_ips=["103.48.19.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.SYLHET: EducationBoardNode(
        id="node_sylhet_board",
        name_bn="মাধ্যমিক ও উচ্চমাধ্যমিক শিক্ষা বোর্ড, সিলেট",
        name_en="Board of Intermediate & Secondary Education, Sylhet",
        board_type=BoardNodeType.SYLHET,
        endpoint_url="https://api.sylhetboard.gov.bd/webhook",
        public_key_hex="52b72296cd45889bec50a6fc4ee6a572bd8d98c7c0d64af87d99683bdca1850a",
        whitelisted_ips=["103.48.20.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.BARISAL: EducationBoardNode(
        id="node_barisal_board",
        name_bn="মাধ্যমিক ও উচ্চমাধ্যমিক শিক্ষা বোর্ড, বরিশাল",
        name_en="Board of Intermediate & Secondary Education, Barishal",
        board_type=BoardNodeType.BARISAL,
        endpoint_url="https://api.barisalboard.gov.bd/webhook",
        public_key_hex="8484e77942b2280c7a81e50b8c56641c5ec3fa0726bdfe291138d5dfccf057a7",
        whitelisted_ips=["103.48.21.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.COMILLA: EducationBoardNode(
        id="node_comilla_board",
        name_bn="মাধ্যমিক ও উচ্চমাধ্যমিক শিক্ষা বোর্ড, কুমিল্লা",
        name_en="Board of Intermediate & Secondary Education, Cumilla",
        board_type=BoardNodeType.COMILLA,
        endpoint_url="https://api.comillaboard.gov.bd/webhook",
        public_key_hex="370080a6eae9e8bb67a018e05bf5d19a4912d9ced5691358361ab46edbf4eb46",
        whitelisted_ips=["103.48.22.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.JESSORE: EducationBoardNode(
        id="node_jessore_board",
        name_bn="মাধ্যমিক ও উচ্চমাধ্যমিক শিক্ষা বোর্ড, যশোর",
        name_en="Board of Intermediate & Secondary Education, Jashore",
        board_type=BoardNodeType.JESSORE,
        endpoint_url="https://api.jessoreboard.gov.bd/webhook",
        public_key_hex="3813083e012230f1f416cec1bb6e53b28aa6fb2e0d6188630829486d0d4cb482",
        whitelisted_ips=["103.48.23.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.DINAJPUR: EducationBoardNode(
        id="node_dinajpur_board",
        name_bn="মাধ্যমিক ও উচ্চমাধ্যমিক শিক্ষা বোর্ড, দিনাজপুর",
        name_en="Board of Intermediate & Secondary Education, Dinajpur",
        board_type=BoardNodeType.DINAJPUR,
        endpoint_url="https://api.dinajpurbise.gov.bd/webhook",
        public_key_hex="e1ad1c7a10aa7e9ca26ea6bf3be1a552e983edcb4d14e3270b4f13251cd297b8",
        whitelisted_ips=["103.48.24.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.MYMENSINGH: EducationBoardNode(
        id="node_mymensingh_board",
        name_bn="মাধ্যমিক ও উচ্চমাধ্যমিক শিক্ষা বোর্ড, ময়মনসিংহ",
        name_en="Board of Intermediate & Secondary Education, Mymensingh",
        board_type=BoardNodeType.MYMENSINGH,
        endpoint_url="https://api.mymensinghboard.gov.bd/webhook",
        public_key_hex="88ec099a06419134d2131c0433bb0446b5c1e95fdb1ca669289472a01639c29f",
        whitelisted_ips=["103.48.25.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.MADRASAH: EducationBoardNode(
        id="node_madrasah_board",
        name_bn="বাংলাদেশ মাদ্রাসা শিক্ষা বোর্ড",
        name_en="Bangladesh Madrasah Education Board",
        board_type=BoardNodeType.MADRASAH,
        endpoint_url="https://api.bmeb.gov.bd/webhook",
        public_key_hex="aabb5dca0108e787a0e0a3330abc89d1a18d76a7b4fb39599e4b2debb66179b2",
        whitelisted_ips=["103.48.26.0/24", "127.0.0.1", "::1"]
    ),
    BoardNodeType.TECHNICAL: EducationBoardNode(
        id="node_technical_board",
        name_bn="বাংলাদেশ কারিগরি শিক্ষা বোর্ড (BTEB)",
        name_en="Bangladesh Technical Education Board",
        board_type=BoardNodeType.TECHNICAL,
        endpoint_url="https://api.bteb.gov.bd/webhook",
        public_key_hex="85fa31609ffc56f143ba9fc327abb943562466c4ac7a4639cb8f41522c25429c",
        whitelisted_ips=["103.48.27.0/24", "127.0.0.1", "::1"]
    ),
}


@dataclass
class W3CVerifiableCredential:
    """W3C Standard Verifiable Credential representation for curriculum and certificate sync."""
    context: List[str]
    id: str
    type: List[str]
    issuer: Dict[str, Any]
    issuance_date: str
    credential_subject: Dict[str, Any]
    proof: Dict[str, Any]

    def is_valid_structure(self) -> bool:
        """Validates adherence to W3C Verifiable Credentials Data Model v1.1."""
        has_context = "https://www.w3.org/2018/credentials/v1" in self.context
        has_type = "VerifiableCredential" in self.type
        has_id = bool(self.id and self.id.startswith("urn:"))
        has_issuer = bool(self.issuer and "id" in self.issuer)
        has_proof = bool(self.proof and self.proof.get("type") == "Ed25519Signature2020")
        return bool(has_context and has_type and has_id and has_issuer and has_proof)


@dataclass
class WebhookEvent:
    id: str
    source_board: BoardNodeType
    event_type: str
    payload: Dict[str, Any]
    signature_hex: str
    timestamp: float
    is_verified: bool
    processed_at: float = field(default_factory=time.time)


class Ed25519SignatureVerifier:
    """Cryptographic non-repudiation engine utilizing Ed25519 asymmetric signatures."""

    @classmethod
    def generate_keypair(cls) -> Tuple[ed25519.Ed25519PrivateKey, ed25519.Ed25519PublicKey, str, str]:
        """Generates a fresh Ed25519 keypair, returning private/public keys and hex encodings."""
        priv_key = ed25519.Ed25519PrivateKey.generate()
        pub_key = priv_key.public_key()
        priv_hex = binascii.hexlify(priv_key.private_bytes_raw()).decode("utf-8")
        pub_hex = binascii.hexlify(pub_key.public_bytes_raw()).decode("utf-8")
        return priv_key, pub_key, priv_hex, pub_hex

    @classmethod
    def sign_payload(cls, private_key: ed25519.Ed25519PrivateKey, payload_bytes: bytes) -> str:
        """Signs binary payload with private key and returns lowercase hexadecimal signature."""
        signature = private_key.sign(payload_bytes)
        return binascii.hexlify(signature).decode("utf-8")

    @classmethod
    def verify_signature(
        cls,
        public_key: ed25519.Ed25519PublicKey,
        signature_hex: str,
        payload_bytes: bytes
    ) -> bool:
        """
        Verifies mathematical authenticity of signature over binary payload.
        Returns True if valid; raises InvalidSignatureException if forged or corrupted.
        """
        try:
            sig_bytes = binascii.unhexlify(signature_hex)
            public_key.verify(sig_bytes, payload_bytes)
            return True
        except (InvalidSignature, binascii.Error, ValueError) as e:
            raise InvalidSignatureException(f"Ed25519 Signature Verification Failed: {e}")

    @classmethod
    def assert_fresh_timestamp(cls, timestamp_epoch: float, max_drift_seconds: float = 300.0) -> None:
        """Rejects webhook requests with timestamps older than 5 minutes to defeat replay attacks."""
        now = time.time()
        drift = abs(now - timestamp_epoch)
        if drift > max_drift_seconds:
            raise StaleWebhookTimestampException(
                f"Replay Attack Defense: Webhook timestamp drift ({drift:.1f}s) "
                f"exceeds tolerance of {max_drift_seconds}s."
            )


class SlidingWindowRateLimiter:
    """Sliding-window rate limiter enforcing 60 requests/minute per board node."""

    def __init__(self, window_seconds: float = 60.0):
        self.window_seconds = window_seconds
        # node_id -> list of timestamps
        self._history: Dict[str, List[float]] = {}

    def is_allowed(self, node_id: str, limit: int = 60) -> bool:
        """Determines if request is within rate limit; appends current timestamp if allowed."""
        now = time.time()
        window_start = now - self.window_seconds

        timestamps = self._history.get(node_id, [])
        # Prune older than window
        timestamps = [t for t in timestamps if t >= window_start]

        if len(timestamps) >= limit:
            self._history[node_id] = timestamps
            return False

        timestamps.append(now)
        self._history[node_id] = timestamps
        return True


class IPWhitelister:
    """ASVS L2 IP validation verifying incoming client IPs against board CIDR subnet ranges."""

    @classmethod
    def is_ip_whitelisted(cls, client_ip: str, whitelisted_cidrs: List[str]) -> bool:
        """Checks if client_ip belongs to any whitelisted IP or CIDR network block."""
        try:
            ip_obj = ipaddress.ip_address(client_ip)
            for cidr in whitelisted_cidrs:
                try:
                    if "/" in cidr:
                        net = ipaddress.ip_network(cidr, strict=False)
                        if ip_obj in net:
                            return True
                    else:
                        if ip_obj == ipaddress.ip_address(cidr):
                            return True
                except ValueError:
                    continue
        except ValueError:
            return False
        return False


class EducationBoardGateway:
    """
    Ministry of Education & National Curriculum Accreditation API Gateway & Clearinghouse.
    """

    def __init__(self):
        self.rate_limiter = SlidingWindowRateLimiter(window_seconds=60.0)

    def process_incoming_webhook(
        self,
        source_board: BoardNodeType,
        event_id: str,
        event_type: str,
        payload: Dict[str, Any],
        signature_hex: str,
        timestamp: float,
        client_ip: str,
        override_public_key: Optional[ed25519.Ed25519PublicKey] = None
    ) -> WebhookEvent:
        """
        Ingests, validates IP, rate limits, checks timestamp freshness, and verifies Ed25519 signature.
        """
        node = BOARD_REGISTRY.get(source_board)
        if not node or not node.is_active:
            raise KeyError(f"Education Board node '{source_board.value}' is unregistered or inactive.")

        # 1. IP Whitelisting Check
        if not IPWhitelister.is_ip_whitelisted(client_ip, node.whitelisted_ips):
            raise IPNotWhitelistedException(
                f"Security Firewall: Client IP '{client_ip}' is not authorized for board '{source_board.value}'."
            )

        # 2. Rate Limiting Check
        if not self.rate_limiter.is_allowed(node.id, limit=node.rate_limit_rpm):
            raise RateLimitExceededException(
                f"Rate Limit Exceeded: Board node '{source_board.value}' exceeded {node.rate_limit_rpm} req/min."
            )

        # 3. Anti-Replay Timestamp Check
        Ed25519SignatureVerifier.assert_fresh_timestamp(timestamp)

        # 4. Ed25519 Digital Signature Verification
        canonical_payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        signed_message = f"{event_type}|{timestamp:.4f}|".encode("utf-8") + canonical_payload_bytes

        if override_public_key:
            public_key = override_public_key
        else:
            pub_bytes = binascii.unhexlify(node.public_key_hex)
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)

        is_verified = Ed25519SignatureVerifier.verify_signature(
            public_key=public_key,
            signature_hex=signature_hex,
            payload_bytes=signed_message
        )

        return WebhookEvent(
            id=event_id,
            source_board=source_board,
            event_type=event_type,
            payload=payload,
            signature_hex=signature_hex,
            timestamp=timestamp,
            is_verified=is_verified
        )

    def dispatch_outgoing_webhook(
        self,
        target_board: BoardNodeType,
        event_type: str,
        payload: Dict[str, Any],
        private_key: ed25519.Ed25519PrivateKey
    ) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Signs and formats outgoing webhook transmission to education board node.
        """
        node = BOARD_REGISTRY.get(target_board)
        if not node:
            raise KeyError(f"Target board node '{target_board.value}' not found.")

        now = time.time()
        canonical_payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        signed_message = f"{event_type}|{now:.4f}|".encode("utf-8") + canonical_payload_bytes

        signature_hex = Ed25519SignatureVerifier.sign_payload(private_key, signed_message)

        headers = {
            "Content-Type": "application/json",
            "X-Board-Node-Id": node.id,
            "X-Event-Type": event_type,
            "X-Timestamp": f"{now:.4f}",
            "X-Ed25519-Signature": signature_hex,
        }
        return payload, headers

    def validate_w3c_credentials_batch(
        self,
        credentials_json: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validates a batch of W3C Verifiable Credentials against accreditation schemas.
        """
        valid_items: List[W3CVerifiableCredential] = []
        invalid_items: List[Dict[str, Any]] = []

        for item in credentials_json:
            vc = W3CVerifiableCredential(
                context=item.get("@context", []),
                id=item.get("id", ""),
                type=item.get("type", []),
                issuer=item.get("issuer", {}),
                issuance_date=item.get("issuanceDate", ""),
                credential_subject=item.get("credentialSubject", {}),
                proof=item.get("proof", {})
            )
            if vc.is_valid_structure():
                valid_items.append(vc)
            else:
                invalid_items.append(item)

        return {
            "total_received": len(credentials_json),
            "valid_count": len(valid_items),
            "invalid_count": len(invalid_items),
            "is_batch_valid": len(invalid_items) == 0,
            "valid_credentials": valid_items,
        }
