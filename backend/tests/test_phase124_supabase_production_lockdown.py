"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Security Verification & Production Lockdown Test Suite
TOPIC:     Phase 124 Supabase Production Security Lockdown & Strix Audit
FILE:      backend/tests/test_phase124_supabase_production_lockdown.py
PHASE:     Phase 124 - Supabase Production Security Lockdown & Strix Audit
PURPOSE:   Automated unit, integration, and compliance tests verifying 100% table RLS
           lockdown, direct auth.uid() policy bindings, zero-trust token claims,
           PostgREST query hardening, storage quarantine against Stored XSS, 25-vector
           penetration audit, and strict zero-emoji mandate.
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


class TestPhase124SupabaseProductionLockdown(unittest.TestCase):
    """
    Unit and integration test suite certifying Phase 124 Supabase Production Security Lockdown.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.migration_004_path = cls.root_dir / "backend" / "migrations" / "004_production_supabase_lockdown.sql"
        cls.validator_path = cls.root_dir / "backend" / "app" / "core" / "supabase_security_validator.py"
        cls.storage_path = cls.root_dir / "backend" / "app" / "services" / "storage_quarantine_service.py"
        cls.audit_script_path = cls.root_dir / "backend" / "scripts" / "run_supabase_security_audit.py"
        cls.test_file_path = Path(__file__)

        cls.validator = SupabaseSecurityValidator()
        cls.storage = StorageQuarantineService()

        cls.target_files = [
            cls.migration_004_path,
            cls.validator_path,
            cls.storage_path,
            cls.audit_script_path,
            cls.test_file_path,
        ]

    def test_01_developer_architecture_notes_presence(self):
        """Verifies Developer Architecture Note headers on all Phase 124 target files."""
        for file_path in self.target_files:
            self.assertTrue(file_path.exists(), f"Target file {file_path.name} must exist.")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"File {file_path.name} missing DEVELOPER ARCHITECTURE NOTE header."
            )
            self.assertIn(
                "Phase 124",
                content,
                f"File {file_path.name} missing Phase 124 reference in header."
            )

    def test_02_migration_004_rls_lockdown_and_immutability(self):
        """Verifies Migration 004 enforces ENABLE and FORCE RLS on 100% of tables and audit immutability."""
        self.assertTrue(self.migration_004_path.exists(), "Migration 004 file must exist.")
        sql = self.migration_004_path.read_text(encoding="utf-8")

        target_tables = [
            "users",
            "profiles",
            "student_profiles",
            "quiz_attempts",
            "tuition_escrow",
            "credentials",
            "audit_logs",
        ]

        for table in target_tables:
            enable_pattern = re.compile(rf"ALTER\s+TABLE\s+public\.{table}\s+ENABLE\s+ROW\s+LEVEL\s+SECURITY", re.IGNORECASE)
            force_pattern = re.compile(rf"ALTER\s+TABLE\s+public\.{table}\s+FORCE\s+ROW\s+LEVEL\s+SECURITY", re.IGNORECASE)
            self.assertTrue(bool(enable_pattern.search(sql)), f"Table {table} must ENABLE ROW LEVEL SECURITY.")
            self.assertTrue(bool(force_pattern.search(sql)), f"Table {table} must FORCE ROW LEVEL SECURITY.")

        # Check auth.uid() binding
        self.assertIn("auth.uid() = id", sql, "Users table must bind auth.uid() to id.")
        self.assertIn("auth.uid() = user_id", sql, "Target tables must bind auth.uid() to user_id.")

        # Check immutability
        self.assertIn("REVOKE UPDATE, DELETE ON public.audit_logs", sql)
        self.assertIn("trg_enforce_strict_audit_log_immutability", sql)

    def test_03_jwt_validation_algorithm_confusion_and_audience_pinning(self):
        """Verifies JWT claim verification, algorithm 'none' rejection, and audience pinning."""
        test_uid = str(uuid.uuid4())
        valid_token = self.validator.create_signed_token(sub=test_uid, role="student")
        payload = self.validator.validate_token(valid_token)
        self.assertEqual(payload["sub"], test_uid)
        self.assertEqual(payload["role"], "student")

        # Algorithm 'none' attack simulation
        header_b64 = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0"  # {"alg":"none","typ":"JWT"}
        payload_b64 = "eyJzdWIiOiIxMjM0NTYiLCJyb2xlIjoiYXV0aGVudGljYXRlZCJ9"
        unsigned_token = f"{header_b64}.{payload_b64}."
        with self.assertRaises(InvalidTokenException):
            self.validator.validate_token(unsigned_token)

        # Expired token simulation
        expired_token = self.validator.create_signed_token(sub=test_uid, expires_in=-10)
        with self.assertRaises(InvalidTokenException):
            self.validator.validate_token(expired_token)

        # Audience verification
        forged_aud_token = self.validator.create_signed_token(
            sub=test_uid, custom_claims={"aud": "unauthorized-external-party"}
        )
        with self.assertRaises(InvalidTokenException):
            self.validator.validate_token(forged_aud_token)

        # Pinned audience verification
        pinned_token = self.validator.create_signed_token(
            sub=test_uid, custom_claims={"aud": "ogrojatra-production-aud"}
        )
        pinned_payload = self.validator.validate_token(pinned_token)
        self.assertEqual(pinned_payload["aud"], "ogrojatra-production-aud")

    def test_04_idor_binding_defense(self):
        """Verifies strict auth.uid() binding blocking cross-user spoofing."""
        victim_uid = str(uuid.uuid4())
        attacker_uid = str(uuid.uuid4())
        attacker_claims = {"sub": attacker_uid, "role": "student"}

        # Attempting action on victim's record must raise IDORViolationException
        with self.assertRaises(IDORViolationException):
            self.validator.verify_user_binding(attacker_claims, requested_user_id=victim_uid)

        # Authorized action on own record must pass
        self.assertTrue(self.validator.verify_user_binding(attacker_claims, requested_user_id=attacker_uid))

    def test_05_postgrest_query_hardening_and_count_stripping(self):
        """Verifies PostgREST parameter pollution defense, count stripping, and SQL injection defense."""
        # 1. Stripping Prefer: count=exact on PII tables
        _, sanitized_headers = self.validator.sanitize_postgrest_query(
            params={},
            headers={"Prefer": "count=exact"},
            table_name="student_profiles",
            user_role="student",
        )
        self.assertEqual(sanitized_headers.get("Prefer"), "count=none")

        # 2. SQL injection blocking
        with self.assertRaises(PostgRESTQueryViolationException):
            self.validator.sanitize_postgrest_query(
                params={"name": "eq.Tanzim; DROP TABLE users;--"},
                table_name="student_profiles",
            )

        # 3. Unbounded wildcard ILIKE blocking
        with self.assertRaises(PostgRESTQueryViolationException):
            self.validator.sanitize_postgrest_query(
                params={"email.ilike": "%"},
                table_name="student_profiles",
            )

        # 4. Null byte parameter pollution blocking
        with self.assertRaises(PostgRESTQueryViolationException):
            self.validator.sanitize_postgrest_query(
                params={"user_id\x00malicious": "123"},
                table_name="student_profiles",
            )

    def test_06_storage_quarantine_signed_url_ttl_and_security_headers(self):
        """Verifies private storage buckets, 900s signed URL TTL, security headers, and MIME quarantine."""
        # 1. Private bucket classification
        self.assertTrue(self.storage.is_private_bucket("student-documents"))
        self.assertTrue(self.storage.is_private_bucket("verified-cvs"))
        self.assertFalse(self.storage.is_private_bucket("public-avatars"))

        # 2. Signed URL generation and headers
        test_uid = str(uuid.uuid4())
        signed = self.storage.generate_signed_url(
            bucket="student-documents",
            file_path=f"{test_uid}/transcript.pdf",
            user_id=test_uid,
            ttl_seconds=900,
        )
        self.assertEqual(signed["ttl_seconds"], 900)
        self.assertIn("signed_url", signed)
        self.assertEqual(signed["enforced_headers"]["X-Content-Type-Options"], "nosniff")
        self.assertIn("attachment", signed["enforced_headers"]["Content-Disposition"])

        # 3. Stored XSS SVG Quarantine
        malicious_svg = b"<svg xmlns='http://www.w3.org/2000/svg'><script>alert('XSS')</script></svg>"
        res = self.storage.inspect_upload(
            bucket="student-documents",
            file_name="avatar.svg",
            declared_mime="image/svg+xml",
            content=malicious_svg,
            uploader_user_id=test_uid,
        )
        self.assertEqual(res["status"], "QUARANTINED")

    def test_07_strix_25_vector_security_audit_execution(self):
        """Executes full 25-vector Strix security audit asserting 25 passed and 0 failed."""
        runner = SupabaseSecurityAuditRunner()
        success = runner.run_all_audits()
        self.assertTrue(success, "All 25 penetration vectors must pass.")

        report_file = self.root_dir / "backend" / "reports" / "supabase-security-audit-report.json"
        self.assertTrue(report_file.exists(), "Audit report JSON must exist.")

        with open(report_file, "r", encoding="utf-8") as f:
            report_data = json.load(f)

        self.assertEqual(report_data["total_vectors_tested"], 25)
        self.assertEqual(report_data["failed_vectors"], 0)
        self.assertEqual(report_data["compliance_score"], 100.0)

    def test_08_strict_zero_emoji_compliance(self):
        """Verifies zero emojis across all Phase 124 target files."""
        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|"
            r"[\u2600-\u27bf]|"
            r"[\u2300-\u23ff]|"
            r"[\u2b50-\u2b55]|"
            r"[\ufe00-\ufe0f]"
        )

        for file_path in self.target_files:
            content = file_path.read_text(encoding="utf-8")
            emojis = emoji_pattern.findall(content)
            self.assertEqual(
                emojis,
                [],
                f"Zero-Emoji policy violation in {file_path.name}: {emojis}"
            )


if __name__ == "__main__":
    unittest.main()
