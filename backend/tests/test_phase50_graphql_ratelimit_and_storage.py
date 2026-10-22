# ==============================================================================
# File: backend/tests/test_phase50_graphql_ratelimit_and_storage.py
# Phase: 50 - Supabase GraphQL Shield, Edge Rate Limiter & Storage Sanitizer Tests
# Description: Verifies AST complexity limits, introspection controls, cyclic
#              recursion defense, multi-tier token bucket rate limiting, and
#              magic byte MIME verification & SVG XSS sanitization.
# ==============================================================================

import unittest
import time
from backend.app.services.pg_graphql_shield_service import PgGraphqlShieldService
from backend.app.services.edge_distributed_rate_limiter_service import EdgeDistributedRateLimiterService
from backend.app.services.storage_multipart_sanitizer_service import StorageMultipartSanitizerService

class TestPhase50GraphqlRateLimitAndStorage(unittest.TestCase):

    def setUp(self):
        self.graphql_shield = PgGraphqlShieldService()
        self.rate_limiter = EdgeDistributedRateLimiterService()
        self.storage_sanitizer = StorageMultipartSanitizerService()

    # --------------------------------------------------------------------------
    # 1. pg_graphql Shield Tests
    # --------------------------------------------------------------------------
    def test_graphql_valid_query_approved(self):
        query = """
        query GetStudentGrades {
            student(id: "stu_101") {
                name
                grades(limit: 5) {
                    course_name
                    grade_point
                }
            }
        }
        """
        res = self.graphql_shield.inspect_and_authorize_query(query, caller_role="student")
        self.assertTrue(res["authorized"])
        self.assertEqual(res["status"], "APPROVED")
        self.assertLessEqual(res["calculated_depth"], 4)

    def test_graphql_introspection_shield(self):
        query = "{ __schema { types { name } } }"
        # Anon role must be blocked
        res_anon = self.graphql_shield.inspect_and_authorize_query(query, caller_role="anon")
        self.assertFalse(res_anon["authorized"])
        self.assertTrue(any(v["code"] == "INTROSPECTION_UNAUTHORIZED" for v in res_anon["violations"]))

        # Admin role must be allowed
        res_admin = self.graphql_shield.inspect_and_authorize_query(query, caller_role="admin")
        self.assertTrue(res_admin["authorized"])

    def test_graphql_depth_and_recursion_defense(self):
        # 1. Excessive depth (> 4 levels)
        deep_query = "{ a { b { c { d { e { f } } } } } }"
        res_depth = self.graphql_shield.inspect_and_authorize_query(deep_query, caller_role="student")
        self.assertFalse(res_depth["authorized"])
        self.assertTrue(any(v["code"] == "EXCESSIVE_QUERY_DEPTH" for v in res_depth["violations"]))

        # 2. Cyclic recursion
        cyclic_query = "{ user { posts { user { posts { id } } } } }"
        res_cyclic = self.graphql_shield.inspect_and_authorize_query(cyclic_query, caller_role="student")
        self.assertFalse(res_cyclic["authorized"])
        self.assertTrue(any(v["code"] == "CYCLIC_RECURSION_DETECTED" for v in res_cyclic["violations"]))

    def test_graphql_restricted_fields_and_parity_audit(self):
        query_leak = "{ student { name password_hash internal_risk_score } }"
        res_leak = self.graphql_shield.inspect_and_authorize_query(query_leak, caller_role="student")
        self.assertFalse(res_leak["authorized"])
        self.assertTrue(any(v["code"] == "RESTRICTED_FIELD_ACCESS" for v in res_leak["violations"]))

        # Parity audit
        parity = self.graphql_shield.audit_postgrest_graphql_parity(
            table_name="student_profiles",
            postgrest_allowed_columns=["id", "name", "email", "batch"],
            graphql_type_fields=["id", "name", "email", "batch", "internal_risk_score"]
        )
        self.assertTrue(parity["has_parity_risk"])
        self.assertIn("internal_risk_score", parity["graphql_overexposed_fields"])

    # --------------------------------------------------------------------------
    # 2. Edge Distributed Rate Limiter Tests
    # --------------------------------------------------------------------------
    def test_rate_limiter_allow_and_throttle(self):
        client_ip = "192.168.10.45"
        # First request must be allowed
        res1 = self.rate_limiter.check_rate_limit(client_ip=client_ip, endpoint="/rest/v1/data")
        self.assertTrue(res1["allowed"])
        self.assertGreater(res1["remaining_tokens"], 0)

        # Exhaust tokens with large custom cost
        res_exhaust = self.rate_limiter.check_rate_limit(client_ip=client_ip, custom_cost=100)
        self.assertFalse(res_exhaust["allowed"])
        self.assertEqual(res_exhaust["reason"], "RATE_LIMIT_EXCEEDED")
        self.assertGreater(res_exhaust["retry_after_seconds"], 0)

    def test_rate_limiter_penalty_box_and_reset(self):
        client_ip = "10.0.0.99"
        # Trigger 5 consecutive breaches
        for _ in range(5):
            self.rate_limiter.check_rate_limit(client_ip=client_ip, custom_cost=100)

        # 6th request must hit penalty box
        res_penalized = self.rate_limiter.check_rate_limit(client_ip=client_ip, custom_cost=1)
        self.assertFalse(res_penalized["allowed"])
        self.assertEqual(res_penalized["reason"], "CLIENT_TEMPORARILY_BLOCKED")
        self.assertTrue(res_penalized["penalty_active"])

        # Reset client unbans them
        client_key = f"ip:{client_ip}"
        self.rate_limiter.reset_client(client_key)
        res_after_reset = self.rate_limiter.check_rate_limit(client_ip=client_ip, custom_cost=1)
        self.assertTrue(res_after_reset["allowed"])
        self.assertFalse(res_after_reset["penalty_active"])

    # --------------------------------------------------------------------------
    # 3. Storage Multipart Sanitizer & Antivirus Tests
    # --------------------------------------------------------------------------
    def test_storage_presigned_ticket_generation(self):
        ticket = self.storage_sanitizer.generate_presigned_upload_ticket(
            bucket_id="student_transcripts",
            file_path="2026/fall/transcript_stu_101.pdf",
            user_id="usr_stu_101",
            allowed_mime_types=["application/pdf"]
        )
        self.assertIn("ticket_id", ticket)
        self.assertIn("hmac_signature", ticket)
        self.assertEqual(len(ticket["hmac_signature"]), 64)
        self.assertGreater(ticket["expires_at"], time.time())

    def test_storage_magic_byte_verification_and_xss_sanitization(self):
        # 1. Valid PDF with magic bytes %PDF-
        valid_pdf = b"%PDF-1.7\nAcademic Transcript Content..."
        res_pdf = self.storage_sanitizer.verify_and_sanitize_upload(
            file_bytes=valid_pdf,
            declared_mime_type="application/pdf",
            file_name="transcript.pdf"
        )
        self.assertTrue(res_pdf["safe"])
        self.assertEqual(res_pdf["status"], "APPROVED")

        # 2. Spoofed PDF (declared application/pdf but arbitrary malicious shell script)
        spoofed_pdf = b"#!/bin/bash\nrm -rf /"
        res_spoof = self.storage_sanitizer.verify_and_sanitize_upload(
            file_bytes=spoofed_pdf,
            declared_mime_type="application/pdf",
            file_name="fake.pdf"
        )
        self.assertFalse(res_spoof["safe"])
        self.assertTrue(any(v["code"] == "MIME_TYPE_SPOOFING" for v in res_spoof["violations"]))

        # 3. Malicious SVG with embedded script
        malicious_svg = b'<svg xmlns="http://www.w3.org/2000/svg"><circle cx="10" cy="10" r="5"/><script>alert("XSS")</script></svg>'
        res_svg = self.storage_sanitizer.verify_and_sanitize_upload(
            file_bytes=malicious_svg,
            declared_mime_type="image/svg+xml",
            file_name="avatar.svg"
        )
        self.assertTrue(res_svg["safe"])  # Approved because XSS was successfully neutralized
        self.assertTrue(res_svg["was_sanitized"])
        self.assertTrue(any(v["code"] == "STORED_XSS_NEUTRALIZED" for v in res_svg["violations"]))
        # Verify nosniff header
        self.assertEqual(res_svg["enforced_download_headers"]["X-Content-Type-Options"], "nosniff")

if __name__ == "__main__":
    unittest.main()
