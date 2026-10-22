"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Security Verification & Zero-Trust Audit Test Suite
TOPIC:     Phase 111 Supabase Security Hardening & Zero-Trust RLS Audit
FILE:      backend/tests/test_phase111_supabase_security_hardening.py
PHASE:     Phase 111 - Supabase Security Hardening & Zero-Trust RLS Audit
PURPOSE:   Automated unit, integration, and compliance tests verifying complete RLS
           lockdown, zero-trust token claims, PostgREST query hardening, storage
           MIME quarantine, 25-vector penetration audit, and strict zero-emoji mandate.
STANDARDS: Strix-Supabase Security Playbook, OWASP ASVS L2, Zero-IDOR, Strict Zero-Emoji
========================================================================================
"""

import json
import os
import re
import unittest
import uuid
from pathlib import Path

from backend.app.core.supabase_security_validator import (
    SupabaseSecurityValidator,
    InvalidTokenException,
    IDORViolationException,
    PostgRESTQueryViolationException,
)
from backend.app.services.storage_quarantine_service import (
    StorageQuarantineService,
    StorageSecurityException,
)
from backend.scripts.run_supabase_security_audit import SupabaseSecurityAuditRunner


class TestPhase111SupabaseSecurityHardening(unittest.TestCase):
    """
    Unit and integration test suite certifying Phase 111 Supabase Security Hardening.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.migration_path = cls.root_dir / "backend" / "migrations" / "003_hardened_supabase_rls.sql"
        cls.validator = SupabaseSecurityValidator()
        cls.storage = StorageQuarantineService()

    def test_01_sql_migration_rls_lockdown_and_immutability(self):
        """Verifies RLS enabled/forced, user_id policy bindings, and audit log immutability."""
        self.assertTrue(self.migration_path.exists(), "Migration SQL file must exist.")
        with open(self.migration_path, "r", encoding="utf-8") as f:
            sql = f.read()

        tables = [
            "users",
            "profiles",
            "student_profiles",
            "quiz_attempts",
            "tuition_escrow",
            "credentials",
            "audit_logs",
        ]

        for table in tables:
            enable_stmt = f"ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;"
            force_stmt = f"ALTER TABLE public.{table} FORCE ROW LEVEL SECURITY;"
            self.assertIn(enable_stmt, sql, f"Missing ENABLE RLS on {table}")
            self.assertIn(force_stmt, sql, f"Missing FORCE RLS on {table}")

        # Verify auth.uid() binding
        self.assertIn("auth.uid() = user_id", sql, "Policies must bind to auth.uid() = user_id")
        self.assertIn("auth.uid() = id", sql, "User policies must bind to auth.uid() = id")

        # Verify audit log immutability
        self.assertIn("REVOKE UPDATE, DELETE ON public.audit_logs FROM PUBLIC, authenticated, anon;", sql)
        self.assertIn("trg_enforce_strict_audit_log_immutability", sql)

    def test_02_supabase_security_validator_zero_trust_and_idor(self):
        """Verifies JWT claim verification, algorithm confusion defense, and IDOR prevention."""
        user_id = str(uuid.uuid4())
        foreign_id = str(uuid.uuid4())

        # 1. Valid token creation and validation
        token = self.validator.create_signed_token(sub=user_id, role="student")
        claims = self.validator.validate_token(token)
        self.assertEqual(claims["sub"], user_id)
        self.assertEqual(claims["role"], "student")
        self.assertEqual(claims["aud"], "authenticated")

        # 2. Reject algorithm none
        bad_token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTYiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJleHAiOjk5OTk5OTk5OTl9."
        with self.assertRaises(InvalidTokenException):
            self.validator.validate_token(bad_token)

        # 3. Reject expired token
        exp_token = self.validator.create_signed_token(sub=user_id, expires_in=-100)
        with self.assertRaises(InvalidTokenException):
            self.validator.validate_token(exp_token)

        # 4. Zero-Trust IDOR check: reject foreign user_id
        with self.assertRaises(IDORViolationException):
            self.validator.verify_user_binding(claims, requested_user_id=foreign_id)

        # Matching user_id passes
        self.assertTrue(self.validator.verify_user_binding(claims, requested_user_id=user_id))

        # 5. PostgREST Query Hardening: block count=exact on PII tables for students
        headers = {"Prefer": "count=exact"}
        params = {"status": "ACTIVE"}
        _, clean_headers = self.validator.sanitize_postgrest_query(
            params, headers=headers, table_name="users", user_role="student"
        )
        self.assertNotIn("count=exact", clean_headers.get("Prefer", ""))

        # 6. PostgREST Query Hardening: block wildcard enumeration
        with self.assertRaises(PostgRESTQueryViolationException):
            self.validator.sanitize_postgrest_query({"email.ilike": "%*"})

        # 7. PostgREST Query Hardening: block SQL injection
        with self.assertRaises(PostgRESTQueryViolationException):
            self.validator.sanitize_postgrest_query({"name": "admin'; DROP TABLE student_profiles; --"})

    def test_03_storage_quarantine_mime_sniffing_and_signed_urls(self):
        """Verifies storage private buckets, Stored XSS quarantine, and signed URL generation."""
        user_id = str(uuid.uuid4())

        # 1. Private bucket verification
        self.assertTrue(self.storage.is_private_bucket("student-documents"))
        self.assertTrue(self.storage.is_private_bucket("verified-cvs"))
        self.assertFalse(self.storage.is_private_bucket("public-avatars"))

        # 2. Path Traversal rejection
        with self.assertRaises(StorageSecurityException):
            self.storage.sanitize_file_path("../../etc/passwd")

        # 3. Stored XSS SVG quarantine
        svg_bytes = b"<svg xmlns='http://www.w3.org/2000/svg'><script>alert('xss')</script></svg>"
        res_svg = self.storage.inspect_upload(
            bucket="student-documents",
            file_name="award.svg",
            declared_mime="image/svg+xml",
            content=svg_bytes,
            uploader_user_id=user_id,
        )
        self.assertEqual(res_svg["status"], "QUARANTINED")
        self.assertIn("Prohibited MIME type", res_svg["reason"])

        # 4. Polyglot PNG with embedded script quarantine
        polyglot = b"\x89PNG\r\n\x1a\n<script>alert(1)</script>"
        res_poly = self.storage.inspect_upload(
            bucket="student-documents",
            file_name="photo.png",
            declared_mime="image/png",
            content=polyglot,
            uploader_user_id=user_id,
        )
        self.assertEqual(res_poly["status"], "QUARANTINED")
        self.assertIn("polyglot", res_poly["reason"])

        # 5. Clean PDF approval
        clean_pdf = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
        res_clean = self.storage.inspect_upload(
            bucket="student-documents",
            file_name="transcript.pdf",
            declared_mime="application/pdf",
            content=clean_pdf,
            uploader_user_id=user_id,
        )
        self.assertEqual(res_clean["status"], "APPROVED")

        # 6. Signed URL generation (900s TTL)
        signed = self.storage.generate_signed_url(
            bucket="student-documents",
            file_path="transcripts/semester1.pdf",
            user_id=user_id,
            ttl_seconds=900,
        )
        self.assertEqual(signed["ttl_seconds"], 900)
        self.assertEqual(signed["enforced_headers"]["X-Content-Type-Options"], "nosniff")
        self.assertIn("attachment", signed["enforced_headers"]["Content-Disposition"])

        # 7. Signed URL verification
        token_match = re.search(r"token=([a-f0-9]+)&expires=(\d+)&uid=([^&]+)&nonce=([a-f0-9]+)", signed["signed_url"])
        self.assertIsNotNone(token_match)
        token, expires_str, uid, nonce = token_match.groups()
        is_valid = self.storage.verify_signed_url(
            bucket="student-documents",
            file_path="transcripts/semester1.pdf",
            user_id=uid,
            expires_at=int(expires_str),
            nonce=nonce,
            provided_token=token,
        )
        self.assertTrue(is_valid, "Valid signed URL must verify successfully.")

        # Tampered token fails
        is_tampered = self.storage.verify_signed_url(
            bucket="student-documents",
            file_path="transcripts/semester1.pdf",
            user_id=uid,
            expires_at=int(expires_str),
            nonce=nonce,
            provided_token="tampered_token_hash_0000",
        )
        self.assertFalse(is_tampered, "Tampered token must fail verification.")

    def test_04_supabase_security_audit_scanner_execution(self):
        """Verifies the 25-vector penetration audit runner achieves 100% compliance."""
        runner = SupabaseSecurityAuditRunner()
        success = runner.run_all_audits()
        self.assertTrue(success, "All 25 penetration vectors must pass.")

        report_file = self.root_dir / "backend" / "reports" / "supabase-security-audit-report.json"
        self.assertTrue(report_file.exists(), "Audit report JSON must be generated.")

        with open(report_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["total_vectors_tested"], 25)
        self.assertEqual(data["failed_vectors"], 0)
        self.assertEqual(data["compliance_score"], 100.0)

    def test_05_developer_architecture_notes_and_strict_zero_emoji(self):
        """Asserts Developer Architecture Note headers and strict zero emoji compliance."""
        target_files = [
            self.root_dir / "backend" / "migrations" / "003_hardened_supabase_rls.sql",
            self.root_dir / "backend" / "app" / "core" / "supabase_security_validator.py",
            self.root_dir / "backend" / "app" / "services" / "storage_quarantine_service.py",
            self.root_dir / "backend" / "scripts" / "run_supabase_security_audit.py",
            Path(__file__).resolve(),
        ]

        # Emoji pattern
        emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff\U00002600-\U000027BF\U00002300-\U000023FF]"
        )

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check Developer Architecture Note
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"File {file_path.name} missing Developer Architecture Note header.",
            )

            # Check Zero Emojis
            matches = emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"File {file_path.name} violates strict Zero Emoji policy: found {matches}",
            )


if __name__ == "__main__":
    unittest.main()
