"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Ministry Accreditation & National Curriculum API Gateway
 * TOPIC:     Phase 131 National Education Board Webhook Clearinghouse & Ed25519 Signatures
 * FILE:      backend/tests/test_phase131_board_gateway.py
 * PHASE:     Phase 131 - National Curriculum Accreditation API Gateway
 * PURPOSE:   Automated test suite validating:
 *            1. Developer Architecture Note headers & file presence
 *            2. Ed25519 cryptographic keypair generation, signing, and verification
 *            3. Webhook tamper detection & signature forgery defense
 *            4. Anti-replay timestamp drift protection
 *            5. ASVS L2 IP whitelisting & subnet CIDR verification
 *            6. Sliding-window rate limiting (60 req/min)
 *            7. W3C Verifiable Credentials batch schema validation
 *            8. Supabase migration 009 Row Level Security policies
 *            9. Frontend clearinghouse dashboard styling, 3D buttons, and Zero-Emoji compliance
 * STANDARDS: Zero-Emoji, ASVS L2, Ed25519 Cryptographic Signatures, Rate Limiting
 */
"""

import binascii
import json
import os
import re
import time
import unittest
from pathlib import Path

from backend.integrations.education_board_gateway import (
    BOARD_REGISTRY,
    BoardNodeType,
    EducationBoardGateway,
    EducationBoardNode,
    Ed25519SignatureVerifier,
    IPNotWhitelistedException,
    IPWhitelister,
    InvalidSignatureException,
    RateLimitExceededException,
    SlidingWindowRateLimiter,
    StaleWebhookTimestampException,
    W3CVerifiableCredential,
    WebhookEvent,
)

# Strict Zero-Emoji Regex covering all standard Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase131BoardGateway(unittest.TestCase):
    """
    Automated verification test suite for Phase 131 Ministry Accreditation & Board API Gateway.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.integrations_init = cls.root_dir / "backend" / "integrations" / "__init__.py"
        cls.gateway_py = cls.root_dir / "backend" / "integrations" / "education_board_gateway.py"
        cls.migration_sql = cls.root_dir / "backend" / "migrations" / "009_education_board_gateway_rls.sql"
        cls.gateway_tsx = cls.root_dir / "frontend" / "src" / "pages" / "governance" / "board-gateway.tsx"
        cls.test_py = cls.root_dir / "backend" / "tests" / "test_phase131_board_gateway.py"

    def test_01_all_phase131_files_exist_with_developer_headers(self):
        """Validates that all Phase 131 core files exist and possess mandatory Developer Architecture Note headers."""
        target_files = [
            self.integrations_init,
            self.gateway_py,
            self.migration_sql,
            self.gateway_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Missing required Phase 131 file: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE:", content, f"Missing Architecture header in {file_path}")
            self.assertIn("Phase 131", content, f"Missing Phase 131 reference in {file_path}")
            self.assertIn("Ministry Accreditation & National Curriculum API Gateway", content, f"Missing module in {file_path}")

    def test_02_zero_emoji_compliance(self):
        """Strictly enforces zero emoji in all created Phase 131 code and migration files."""
        target_files = [
            self.integrations_init,
            self.gateway_py,
            self.migration_sql,
            self.gateway_tsx,
            self.test_py,
        ]

        for file_path in target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(len(matches), 0, f"Emoji violations detected in {file_path}: {matches}")

    def test_03_board_registry_integrity(self):
        """Validates canonical registration of NCTB and all 11 national education boards."""
        self.assertGreaterEqual(len(BOARD_REGISTRY), 12)
        expected_boards = [
            BoardNodeType.NCTB,
            BoardNodeType.DHAKA,
            BoardNodeType.CHITTAGONG,
            BoardNodeType.RAJSHAHI,
            BoardNodeType.COMILLA,
            BoardNodeType.JESSORE,
            BoardNodeType.BARISAL,
            BoardNodeType.SYLHET,
            BoardNodeType.DINAJPUR,
            BoardNodeType.MYMENSINGH,
            BoardNodeType.MADRASAH,
            BoardNodeType.TECHNICAL,
        ]

        for board_type in expected_boards:
            self.assertIn(board_type, BOARD_REGISTRY)
            node = BOARD_REGISTRY[board_type]
            self.assertTrue(node.is_active)
            self.assertTrue(node.name_bn)
            self.assertTrue(node.name_en)
            self.assertTrue(node.endpoint_url.startswith("https://"))
            self.assertEqual(node.rate_limit_rpm, 60)
            self.assertGreaterEqual(len(node.whitelisted_ips), 1)
            # Public key hex should be 64 characters (32 bytes)
            self.assertEqual(len(node.public_key_hex), 64)

    def test_04_ed25519_keypair_generation_and_signing(self):
        """Validates Ed25519 cryptographic keypair generation, payload signing, and verification."""
        priv_key, pub_key, priv_hex, pub_hex = Ed25519SignatureVerifier.generate_keypair()

        self.assertEqual(len(priv_hex), 64)
        self.assertEqual(len(pub_hex), 64)

        test_payload = b"NCTB_CURRICULUM_ACCREDITATION_PAYLOAD_2026"
        signature_hex = Ed25519SignatureVerifier.sign_payload(priv_key, test_payload)

        self.assertEqual(len(signature_hex), 128)  # Ed25519 signatures are 64 bytes = 128 hex chars

        # Verification must succeed with valid key and payload
        is_valid = Ed25519SignatureVerifier.verify_signature(pub_key, signature_hex, test_payload)
        self.assertTrue(is_valid)

    def test_05_ed25519_tampered_payload_and_forgery_defense(self):
        """Confirms that tampered payloads or forged signatures raise InvalidSignatureException."""
        priv_key, pub_key, _, _ = Ed25519SignatureVerifier.generate_keypair()
        _, foreign_pub_key, _, _ = Ed25519SignatureVerifier.generate_keypair()

        original_payload = b"SUBJECT_PHYSICS_GRADE_12_ACC_OK"
        signature_hex = Ed25519SignatureVerifier.sign_payload(priv_key, original_payload)

        # 1. Tampered payload
        tampered_payload = b"SUBJECT_PHYSICS_GRADE_12_ACC_FORGED"
        with self.assertRaises(InvalidSignatureException):
            Ed25519SignatureVerifier.verify_signature(pub_key, signature_hex, tampered_payload)

        # 2. Corrupted signature hex
        corrupted_sig = "a" * 128
        with self.assertRaises(InvalidSignatureException):
            Ed25519SignatureVerifier.verify_signature(pub_key, corrupted_sig, original_payload)

        # 3. Mismatched public key
        with self.assertRaises(InvalidSignatureException):
            Ed25519SignatureVerifier.verify_signature(foreign_pub_key, signature_hex, original_payload)

    def test_06_anti_replay_timestamp_defense(self):
        """Enforces rejection of webhook requests exceeding the allowable clock drift window."""
        now = time.time()

        # Fresh timestamp within 300s
        Ed25519SignatureVerifier.assert_fresh_timestamp(now)
        Ed25519SignatureVerifier.assert_fresh_timestamp(now - 120)

        # Stale timestamp (> 300s old)
        stale_time = now - 350
        with self.assertRaises(StaleWebhookTimestampException):
            Ed25519SignatureVerifier.assert_fresh_timestamp(stale_time, max_drift_seconds=300.0)

        # Future timestamp (> 300s in future)
        future_time = now + 400
        with self.assertRaises(StaleWebhookTimestampException):
            Ed25519SignatureVerifier.assert_fresh_timestamp(future_time, max_drift_seconds=300.0)

    def test_07_ip_whitelisting_and_cidr_matching(self):
        """Verifies ASVS L2 IP address whitelisting with exact and CIDR subnet evaluation."""
        whitelisted = ["103.48.16.0/24", "192.168.1.10", "127.0.0.1", "::1"]

        # Valid IPs
        self.assertTrue(IPWhitelister.is_ip_whitelisted("103.48.16.1", whitelisted))
        self.assertTrue(IPWhitelister.is_ip_whitelisted("103.48.16.254", whitelisted))
        self.assertTrue(IPWhitelister.is_ip_whitelisted("192.168.1.10", whitelisted))
        self.assertTrue(IPWhitelister.is_ip_whitelisted("127.0.0.1", whitelisted))
        self.assertTrue(IPWhitelister.is_ip_whitelisted("::1", whitelisted))

        # Unauthorized IPs
        self.assertFalse(IPWhitelister.is_ip_whitelisted("103.48.17.1", whitelisted))
        self.assertFalse(IPWhitelister.is_ip_whitelisted("192.168.1.11", whitelisted))
        self.assertFalse(IPWhitelister.is_ip_whitelisted("8.8.8.8", whitelisted))
        self.assertFalse(IPWhitelister.is_ip_whitelisted("invalid_ip_string", whitelisted))

    def test_08_sliding_window_rate_limiter(self):
        """Tests rate limiter quota exhaustion (60 requests per minute)."""
        limiter = SlidingWindowRateLimiter(window_seconds=60.0)
        node_id = "test_node_dhaka"

        # First 60 requests should pass
        for i in range(60):
            allowed = limiter.is_allowed(node_id, limit=60)
            self.assertTrue(allowed, f"Request #{i+1} should be allowed")

        # 61st request in the same window must be rejected
        self.assertFalse(limiter.is_allowed(node_id, limit=60))

    def test_09_incoming_webhook_processing_e2e(self):
        """Tests complete end-to-end incoming webhook ingestion, verification, and rejection paths."""
        gateway = EducationBoardGateway()

        priv_key, pub_key, _, pub_hex = Ed25519SignatureVerifier.generate_keypair()

        payload = {
            "curriculum_version": "NCTB-2026-V4",
            "subject_code": "PHY-101",
            "accreditation_status": "ACCREDITED",
            "authorized_by": "National Curriculum Board Director"
        }
        event_type = "CURRICULUM_ACCREDITATION_PUBLISHED"
        now = time.time()

        canonical_payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        signed_message = f"{event_type}|{now:.4f}|".encode("utf-8") + canonical_payload_bytes
        sig_hex = Ed25519SignatureVerifier.sign_payload(priv_key, signed_message)

        # 1. Successful incoming webhook with override public key
        event = gateway.process_incoming_webhook(
            source_board=BoardNodeType.NCTB,
            event_id="evt_test_001",
            event_type=event_type,
            payload=payload,
            signature_hex=sig_hex,
            timestamp=now,
            client_ip="127.0.0.1",
            override_public_key=pub_key
        )
        self.assertIsInstance(event, WebhookEvent)
        self.assertTrue(event.is_verified)
        self.assertEqual(event.source_board, BoardNodeType.NCTB)

        # 2. Rejection on unauthorized IP
        with self.assertRaises(IPNotWhitelistedException):
            gateway.process_incoming_webhook(
                source_board=BoardNodeType.NCTB,
                event_id="evt_test_002",
                event_type=event_type,
                payload=payload,
                signature_hex=sig_hex,
                timestamp=now,
                client_ip="198.51.100.25",
                override_public_key=pub_key
            )

        # 3. Rejection on stale timestamp
        with self.assertRaises(StaleWebhookTimestampException):
            gateway.process_incoming_webhook(
                source_board=BoardNodeType.NCTB,
                event_id="evt_test_003",
                event_type=event_type,
                payload=payload,
                signature_hex=sig_hex,
                timestamp=now - 600,
                client_ip="127.0.0.1",
                override_public_key=pub_key
            )

    def test_10_outgoing_webhook_dispatch(self):
        """Tests outgoing webhook signing and dispatch header generation."""
        gateway = EducationBoardGateway()
        priv_key, pub_key, _, _ = Ed25519SignatureVerifier.generate_keypair()

        payload = {"status": "STUDENT_CREDENTIAL_VERIFIED", "student_roll": "104928"}
        event_type = "CREDENTIAL_VERIFICATION_BROADCAST"

        dispatched_payload, headers = gateway.dispatch_outgoing_webhook(
            target_board=BoardNodeType.DHAKA,
            event_type=event_type,
            payload=payload,
            private_key=priv_key
        )

        self.assertEqual(dispatched_payload, payload)
        self.assertEqual(headers["X-Board-Node-Id"], "node_dhaka_board")
        self.assertEqual(headers["X-Event-Type"], event_type)
        self.assertIn("X-Ed25519-Signature", headers)
        self.assertEqual(len(headers["X-Ed25519-Signature"]), 128)

    def test_11_w3c_verifiable_credential_batch_validation(self):
        """Tests schema compliance of W3C Verifiable Credentials for curriculum and certificate sync."""
        gateway = EducationBoardGateway()

        valid_vc = {
            "@context": ["https://www.w3.org/2018/credentials/v1"],
            "id": "urn:uuid:bd-nctb-curriculum-2026-phy",
            "type": ["VerifiableCredential", "CurriculumAccreditationCredential"],
            "issuer": {"id": "did:bdgov:nctb:accreditation"},
            "issuanceDate": "2026-10-20T10:00:00Z",
            "credentialSubject": {
                "id": "did:bdgov:curriculum:hsc-physics",
                "gradeLevel": "Grade 11-12",
                "syllabusStandard": "National Curriculum 2026"
            },
            "proof": {
                "type": "Ed25519Signature2020",
                "created": "2026-10-20T10:00:00Z",
                "proofPurpose": "assertionMethod",
                "verificationMethod": "did:bdgov:nctb:accreditation#key-1",
                "jws": "eyJhbGciOiJFZERTQ..."
            }
        }

        invalid_vc = {
            "title": "Invalid Non-W3C Credential",
            "missing_fields": True
        }

        batch = [valid_vc, invalid_vc]
        res = gateway.validate_w3c_credentials_batch(batch)

        self.assertEqual(res["total_received"], 2)
        self.assertEqual(res["valid_count"], 1)
        self.assertEqual(res["invalid_count"], 1)
        self.assertFalse(res["is_batch_valid"])
        self.assertEqual(len(res["valid_credentials"]), 1)
        self.assertEqual(res["valid_credentials"][0].id, "urn:uuid:bd-nctb-curriculum-2026-phy")

    def test_12_supabase_migration_009_rls_integrity(self):
        """Verifies migration 009 creates required clearinghouse tables and enforces 100% RLS."""
        sql_content = self.migration_sql.read_text(encoding="utf-8")

        required_tables = [
            "board_accreditation_nodes",
            "board_webhook_events",
            "verifiable_credentials_batch",
            "gateway_audit_logs",
        ]

        for tbl in required_tables:
            has_table = f"CREATE TABLE IF NOT EXISTS public.{tbl}" in sql_content or f"CREATE TABLE IF NOT EXISTS {tbl}" in sql_content
            self.assertTrue(has_table, f"Missing table creation for {tbl}")
            has_rls = f"ALTER TABLE public.{tbl} ENABLE ROW LEVEL SECURITY;" in sql_content or f"ALTER TABLE {tbl} ENABLE ROW LEVEL SECURITY;" in sql_content
            self.assertTrue(has_rls, f"Missing RLS enablement for {tbl}")

        # Confirm service role bypass policy is specified
        self.assertIn("CREATE POLICY", sql_content)
        self.assertIn("service_role", sql_content)

    def test_13_frontend_clearinghouse_page_styling_and_icons(self):
        """Verifies frontend board-gateway page implements pure academic styling and Lucide icons."""
        tsx_content = self.gateway_tsx.read_text(encoding="utf-8")

        # Academic color palette & 3D tactile buttons
        self.assertTrue(
            "bg-[#0A2540]" in tsx_content or "bg-navy-900" in tsx_content or "from-[#0A2540]" in tsx_content,
            "Missing Oxford Academic Navy styling"
        )
        self.assertTrue("shadow-[0_4px_0_0" in tsx_content, "Missing 3D tactile button styling")

        # Lucide vector icons
        expected_icons = ["ShieldCheck", "Building2", "FileCheck", "CheckCircle2", "Activity", "Server", "Terminal"]
        for icon in expected_icons:
            self.assertIn(icon, tsx_content, f"Missing expected Lucide icon: {icon}")


if __name__ == "__main__":
    unittest.main()
