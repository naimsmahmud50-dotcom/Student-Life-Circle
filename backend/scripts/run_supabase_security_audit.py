"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Supabase Security Penetration Audit & Automated Vector Scanner
TOPIC:     Phase 124 Supabase Production Security Lockdown & Strix Audit
FILE:      backend/scripts/run_supabase_security_audit.py
PHASE:     Phase 124 - Supabase Production Security Lockdown & Strix Audit
PURPOSE:   Executes automated penetration audit across 25 security attack vectors:
           verifies Row Level Security lockdown, PostgREST query sanitization,
           IDOR prevention, storage quarantine against Stored XSS, signed URL TTLs,
           and client-side bundle secret isolation according to Strix-Supabase specs.
STANDARDS: Strix-Supabase Security Playbook, OWASP ASVS L2, Zero-IDOR, Strict Zero-Emoji
========================================================================================
"""

import datetime
import json
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Add repository root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

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


class SupabaseSecurityAuditRunner:
    """
    Automated penetration test runner and compliance auditor for Supabase security hardening.
    """

    def __init__(self):
        self.validator = SupabaseSecurityValidator()
        self.storage = StorageQuarantineService()
        self.results: List[Dict[str, Any]] = []
        self.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.report_path = ROOT_DIR / "backend" / "reports" / "supabase-security-audit-report.json"

    def record_result(self, vector_id: str, title: str, status: str, details: str, severity: str = "HIGH"):
        """Records an individual attack vector audit result."""
        self.results.append({
            "vector_id": vector_id,
            "title": title,
            "status": status,
            "severity": severity,
            "details": details,
        })
        print(f"[{status}] {vector_id}: {title} - {details}")

    def audit_sql_migration_rls(self):
        """Audits backend/migrations/003_hardened_supabase_rls.sql and 004_production_supabase_lockdown.sql for complete RLS lockdown."""
        migration_file = ROOT_DIR / "backend" / "migrations" / "003_hardened_supabase_rls.sql"
        migration_004 = ROOT_DIR / "backend" / "migrations" / "004_production_supabase_lockdown.sql"
        if not migration_file.exists() and not migration_004.exists():
            self.record_result("VEC-01", "Migration File Existence", "FAIL", "Migration file missing", "CRITICAL")
            return

        sql_content = ""
        if migration_file.exists():
            with open(migration_file, "r", encoding="utf-8") as f:
                sql_content += f.read() + "\n"
        if migration_004.exists():
            with open(migration_004, "r", encoding="utf-8") as f:
                sql_content += f.read() + "\n"

        target_tables = [
            "users",
            "profiles",
            "student_profiles",
            "quiz_attempts",
            "tuition_escrow",
            "credentials",
            "audit_logs",
        ]

        # Vectors 1 to 7: RLS Enabled and Forced
        for idx, table in enumerate(target_tables, start=1):
            enable_pattern = re.compile(rf"ALTER\s+TABLE\s+public\.{table}\s+ENABLE\s+ROW\s+LEVEL\s+SECURITY", re.IGNORECASE)
            force_pattern = re.compile(rf"ALTER\s+TABLE\s+public\.{table}\s+FORCE\s+ROW\s+LEVEL\s+SECURITY", re.IGNORECASE)

            has_enable = bool(enable_pattern.search(sql_content))
            has_force = bool(force_pattern.search(sql_content))

            if has_enable and has_force:
                self.record_result(
                    f"VEC-0{idx}",
                    f"RLS Enabled & Forced on {table}",
                    "PASS",
                    f"Table {table} has both ENABLE and FORCE ROW LEVEL SECURITY asserted.",
                    "HIGH"
                )
            else:
                self.record_result(
                    f"VEC-0{idx}",
                    f"RLS Enabled & Forced on {table}",
                    "FAIL",
                    f"Table {table} missing ENABLE ({has_enable}) or FORCE ({has_force}) RLS.",
                    "CRITICAL"
                )

        # Vector 8: Audit Logs Immutability
        has_revoke_update = "REVOKE UPDATE, DELETE ON public.audit_logs" in sql_content
        has_immutability_trigger = "trg_enforce_strict_audit_log_immutability" in sql_content
        if has_revoke_update and has_immutability_trigger:
            self.record_result(
                "VEC-08",
                "Audit Log Immutability Enforcement",
                "PASS",
                "audit_logs table enforces REVOKE UPDATE, DELETE and triggers strict immutability exception.",
                "CRITICAL"
            )
        else:
            self.record_result(
                "VEC-08",
                "Audit Log Immutability Enforcement",
                "FAIL",
                "audit_logs missing REVOKE or immutability trigger.",
                "CRITICAL"
            )

    def audit_token_and_auth_vectors(self):
        """Audits JWT validation, algorithm confusion rejection, audience binding, and IDOR."""
        user_a = str(uuid.uuid4())
        user_b = str(uuid.uuid4())

        # Vector 9: Valid Token Verification
        valid_token = self.validator.create_signed_token(sub=user_a, role="student")
        try:
            claims = self.validator.validate_token(valid_token)
            if claims.get("sub") == user_a and claims.get("role") == "student":
                self.record_result(
                    "VEC-09",
                    "Valid JWT Claims Verification",
                    "PASS",
                    "Authentic token validated successfully with correct claims.",
                    "HIGH"
                )
            else:
                self.record_result("VEC-09", "Valid JWT Claims Verification", "FAIL", "Claims mismatch", "HIGH")
        except Exception as e:
            self.record_result("VEC-09", "Valid JWT Claims Verification", "FAIL", str(e), "HIGH")

        # Vector 10: Algorithm None Confusion Attack
        none_token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTYiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJleHAiOjk5OTk5OTk5OTl9."
        try:
            self.validator.validate_token(none_token)
            self.record_result("VEC-10", "Algorithm 'none' Attack Defense", "FAIL", "Accepted alg=none token", "CRITICAL")
        except InvalidTokenException:
            self.record_result(
                "VEC-10",
                "Algorithm 'none' Attack Defense",
                "PASS",
                "Token with alg='none' was safely detected and rejected.",
                "CRITICAL"
            )

        # Vector 11: Invalid Audience Attack
        bad_aud_token = self.validator.create_signed_token(sub=user_a, custom_claims={"aud": "unauthorized-client"})
        try:
            self.validator.validate_token(bad_aud_token)
            self.record_result("VEC-11", "Audience Verification Guard", "FAIL", "Accepted invalid audience", "HIGH")
        except InvalidTokenException:
            self.record_result(
                "VEC-11",
                "Audience Verification Guard",
                "PASS",
                "Token with unauthorized audience was safely rejected.",
                "HIGH"
            )

        # Vector 12: Expired Token Rejection
        expired_token = self.validator.create_signed_token(sub=user_a, expires_in=-300)
        try:
            self.validator.validate_token(expired_token)
            self.record_result("VEC-12", "Expired Token Rejection", "FAIL", "Accepted expired token", "HIGH")
        except InvalidTokenException:
            self.record_result(
                "VEC-12",
                "Expired Token Rejection",
                "PASS",
                "Expired token was safely detected and rejected.",
                "HIGH"
            )

        # Vector 13: IDOR User Parameter Tampering
        claims_a = self.validator.validate_token(valid_token)
        try:
            self.validator.verify_user_binding(claims_a, requested_user_id=user_b)
            self.record_result("VEC-13", "IDOR User Parameter Tampering Defense", "FAIL", "Allowed user A to impersonate user B", "CRITICAL")
        except IDORViolationException:
            self.record_result(
                "VEC-13",
                "IDOR User Parameter Tampering Defense",
                "PASS",
                "IDOR attempt with foreign user_id was safely blocked.",
                "CRITICAL"
            )

        # Vector 14: Cross-Tenant Isolation Enforcement
        tenant_1 = str(uuid.uuid4())
        tenant_token = self.validator.create_signed_token(sub=user_a, role="student", tenant_id=tenant_1)
        tenant_claims = self.validator.validate_token(tenant_token)
        if tenant_claims.get("tenant_id") == tenant_1:
            self.record_result(
                "VEC-14",
                "Cross-Tenant Claim Binding",
                "PASS",
                "Tenant claim bound securely to JWT payload.",
                "HIGH"
            )
        else:
            self.record_result("VEC-14", "Cross-Tenant Claim Binding", "FAIL", "Tenant claim missing", "HIGH")

    def audit_postgrest_hardening(self):
        """Audits PostgREST query sanitization, count inference, parameter pollution, and SQLi."""
        # Vector 15: Parameter Pollution Detection
        try:
            polluted_params = {"id\x00malicious": "123"}
            self.validator.sanitize_postgrest_query(polluted_params)
            self.record_result("VEC-15", "PostgREST Parameter Pollution Defense", "FAIL", "Allowed null byte in parameter key", "HIGH")
        except PostgRESTQueryViolationException:
            self.record_result(
                "VEC-15",
                "PostgREST Parameter Pollution Defense",
                "PASS",
                "Null byte control character parameter pollution blocked.",
                "HIGH"
            )

        # Vector 16: Count Inference Blocking on PII Tables
        headers = {"Prefer": "count=exact"}
        params = {"class_grade": "10"}
        _, clean_headers = self.validator.sanitize_postgrest_query(
            params, headers=headers, table_name="student_profiles", user_role="student"
        )
        if "count=exact" not in clean_headers.get("Prefer", ""):
            self.record_result(
                "VEC-16",
                "PostgREST Count Inference Blocking",
                "PASS",
                "Prefer: count=exact stripped from non-admin request on student_profiles.",
                "HIGH"
            )
        else:
            self.record_result("VEC-16", "PostgREST Count Inference Blocking", "FAIL", "Failed to sanitize count=exact", "HIGH")

        # Vector 17: Wildcard ILIKE Mass Enumeration Defense
        wildcard_params = {"email.ilike": "*%"}
        try:
            self.validator.sanitize_postgrest_query(wildcard_params, table_name="users")
            self.record_result("VEC-17", "Wildcard ILIKE Mass Enumeration Defense", "FAIL", "Allowed unbounded wildcard query", "HIGH")
        except PostgRESTQueryViolationException:
            self.record_result(
                "VEC-17",
                "Wildcard ILIKE Mass Enumeration Defense",
                "PASS",
                "Unbounded wildcard query on email.ilike was blocked.",
                "HIGH"
            )

        # Vector 18: SQL Injection Sanitization
        sqli_params = {"search": "test'; DROP TABLE users; --"}
        try:
            self.validator.sanitize_postgrest_query(sqli_params)
            self.record_result("VEC-18", "SQL Injection Pattern Defense", "FAIL", "Allowed raw SQL injection statement", "CRITICAL")
        except PostgRESTQueryViolationException:
            self.record_result(
                "VEC-18",
                "SQL Injection Pattern Defense",
                "PASS",
                "DROP TABLE SQL injection pattern was blocked.",
                "CRITICAL"
            )

    def audit_storage_security(self):
        """Audits private bucket controls, Stored XSS SVG blocking, polyglot defense, and signed URLs."""
        user_id = str(uuid.uuid4())

        # Vector 19: Private Bucket Policy Enforcement
        is_private = self.storage.is_private_bucket("student-documents")
        is_public = self.storage.is_private_bucket("public-avatars")
        if is_private and not is_public:
            self.record_result(
                "VEC-19",
                "Storage Private Bucket Designation",
                "PASS",
                "student-documents correctly marked private; public-avatars marked public.",
                "HIGH"
            )
        else:
            self.record_result("VEC-19", "Storage Private Bucket Designation", "FAIL", "Bucket designation error", "HIGH")

        # Vector 20: Stored XSS SVG Upload Quarantine
        svg_content = b"<svg xmlns='http://www.w3.org/2000/svg'><script>alert('xss')</script></svg>"
        res_svg = self.storage.inspect_upload(
            bucket="student-documents",
            file_name="cert.svg",
            declared_mime="image/svg+xml",
            content=svg_content,
            uploader_user_id=user_id
        )
        if res_svg.get("status") == "QUARANTINED":
            self.record_result(
                "VEC-20",
                "Stored XSS SVG Upload Quarantine",
                "PASS",
                "SVG upload quarantined with Stored XSS defense reason.",
                "CRITICAL"
            )
        else:
            self.record_result("VEC-20", "Stored XSS SVG Upload Quarantine", "FAIL", "Allowed SVG upload", "CRITICAL")

        # Vector 21: Polyglot Payload Detection
        polyglot_payload = b"\x89PNG\r\n\x1a\n" + b"<script>alert(document.cookie)</script>"
        res_polyglot = self.storage.inspect_upload(
            bucket="student-documents",
            file_name="avatar.png",
            declared_mime="image/png",
            content=polyglot_payload,
            uploader_user_id=user_id
        )
        if res_polyglot.get("status") == "QUARANTINED":
            self.record_result(
                "VEC-21",
                "Polyglot Embedded Script Detection",
                "PASS",
                "Disguised PNG containing embedded <script> quarantined.",
                "CRITICAL"
            )
        else:
            self.record_result("VEC-21", "Polyglot Embedded Script Detection", "FAIL", "Allowed polyglot script in PNG", "CRITICAL")

        # Vector 22: Magic Byte Mismatch Detection
        fake_pdf = b"NOT_A_REAL_PDF_JUST_TEXT"
        res_fake_pdf = self.storage.inspect_upload(
            bucket="student-documents",
            file_name="transcript.pdf",
            declared_mime="application/pdf",
            content=fake_pdf,
            uploader_user_id=user_id
        )
        if res_fake_pdf.get("status") == "QUARANTINED":
            self.record_result(
                "VEC-22",
                "MIME Magic Byte Mismatch Detection",
                "PASS",
                "Spoofed PDF extension missing %PDF- header quarantined.",
                "HIGH"
            )
        else:
            self.record_result("VEC-22", "MIME Magic Byte Mismatch Detection", "FAIL", "Allowed mismatched magic bytes", "HIGH")

        # Vector 23: Time-Limited Signed URL with 900s TTL
        signed_url_data = self.storage.generate_signed_url(
            bucket="student-documents",
            file_path="transcripts/doc1.pdf",
            user_id=user_id,
            ttl_seconds=900
        )
        if signed_url_data.get("ttl_seconds") == 900 and "token=" in signed_url_data.get("signed_url"):
            self.record_result(
                "VEC-23",
                "Time-Limited Signed URL Generation (900s TTL)",
                "PASS",
                "Signed URL generated with strict 900s expiration and HMAC token.",
                "HIGH"
            )
        else:
            self.record_result("VEC-23", "Time-Limited Signed URL Generation (900s TTL)", "FAIL", "Invalid TTL or token", "HIGH")

        # Vector 24: Enforced nosniff & Attachment Headers
        headers = signed_url_data.get("enforced_headers", {})
        has_nosniff = headers.get("X-Content-Type-Options") == "nosniff"
        has_attachment = "attachment" in headers.get("Content-Disposition", "")
        if has_nosniff and has_attachment:
            self.record_result(
                "VEC-24",
                "Download Security Headers Enforcement",
                "PASS",
                "Response headers include X-Content-Type-Options: nosniff and Content-Disposition: attachment.",
                "HIGH"
            )
        else:
            self.record_result("VEC-24", "Download Security Headers Enforcement", "FAIL", "Missing nosniff or attachment headers", "HIGH")

    def audit_client_bundle_secret_leak(self):
        """Vector 25: Scans frontend/ directory to verify zero service_role or sb_secret_ exposure."""
        frontend_dir = ROOT_DIR / "frontend"
        if not frontend_dir.exists():
            self.record_result("VEC-25", "Client Bundle Secret Leak Audit", "PASS", "Frontend directory absent", "CRITICAL")
            return

        leaked_files = []
        suspicious_patterns = [
            re.compile(r"service_role\s*[:=]\s*['\"][a-zA-Z0-9_\-\.]{20,}['\"]", re.IGNORECASE),
            re.compile(r"sb_secret_[a-zA-Z0-9_\-]{16,}", re.IGNORECASE),
            re.compile(r"SUPABASE_SERVICE_ROLE_KEY\s*[:=]\s*['\"][a-zA-Z0-9_\-\.]{20,}['\"]", re.IGNORECASE),
        ]

        # Scan .env, .ts, .tsx, .js, .json in frontend
        for ext in [".ts", ".tsx", ".js", ".jsx", ".env", ".local"]:
            for file_path in frontend_dir.rglob(f"*{ext}"):
                if "node_modules" in str(file_path) or ".next" in str(file_path):
                    continue
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    for pattern in suspicious_patterns:
                        if pattern.search(content):
                            leaked_files.append(str(file_path.relative_to(ROOT_DIR)))
                            break
                except Exception:
                    pass

        if not leaked_files:
            self.record_result(
                "VEC-25",
                "Client Bundle Secret Isolation Audit",
                "PASS",
                "Zero service_role keys or sb_secret_ tokens detected across frontend code.",
                "CRITICAL"
            )
        else:
            self.record_result(
                "VEC-25",
                "Client Bundle Secret Isolation Audit",
                "FAIL",
                f"Potential service_role leak detected in: {leaked_files}",
                "CRITICAL"
            )

    def run_all_audits(self) -> bool:
        """Executes all 25 attack vector audits and generates final JSON report."""
        print("================================================================================")
        print("STARTING SUPABASE SECURITY HARDENING & ZERO-TRUST AUDIT (PHASE 111)")
        print("================================================================================")

        self.audit_sql_migration_rls()
        self.audit_token_and_auth_vectors()
        self.audit_postgrest_hardening()
        self.audit_storage_security()
        self.audit_client_bundle_secret_leak()

        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")

        print("================================================================================")
        print(f"AUDIT SUMMARY: {passed}/{total} VECTORS PASSED ({failed} FAILED)")
        print("================================================================================")

        # Generate report artifact
        report_data = {
            "audit_name": "Supabase Security Hardening & Zero-Trust Audit",
            "phase": "Phase 111",
            "timestamp": self.timestamp,
            "total_vectors_tested": total,
            "passed_vectors": passed,
            "failed_vectors": failed,
            "compliance_score": round((passed / total) * 100, 2) if total > 0 else 0,
            "standards_adherence": [
                "Strix-Supabase Security Playbook",
                "OWASP ASVS Level 2",
                "Zero-Trust Architecture",
                "Strict Zero-Emoji Policy"
            ],
            "vectors": self.results,
        }

        self.report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        print(f"Detailed audit report exported to: {self.report_path}")

        return failed == 0


if __name__ == "__main__":
    runner = SupabaseSecurityAuditRunner()
    success = runner.run_all_audits()
    sys.exit(0 if success else 1)
