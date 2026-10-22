"""
Strix Supabase Security Audit Suite:
Exhaustive verification of Row-Level Security (RLS), PostgREST injection defense,
Edge Function JWT audience binding, Storage security, and Realtime channel authorization.
Compliant with /strix-supabase playbook and ASVS Level 2 child safety guidelines.
"""

import unittest
from backend.app.services.supabase_security_service import SupabaseSecurityService
from backend.app.services.edge_function_boundary_service import EdgeFunctionBoundaryService
from backend.app.services.realtime_cryptographic_presence_service import RealtimeCryptographicPresenceService
from backend.app.services.postgres_rls_compliance_scanner_service import PostgresRlsComplianceScannerService
from backend.app.services.dynamic_data_masking_service import DynamicDataMaskingService
from backend.app.services.pg_graphql_shield_service import PgGraphqlShieldService
from backend.app.services.edge_function_zero_trust_gateway_service import EdgeFunctionZeroTrustGatewayService


class TestStrixSupabaseSecurityAudit(unittest.TestCase):

    def setUp(self):
        self.supabase_sec = SupabaseSecurityService()
        self.edge_sec = EdgeFunctionBoundaryService(secret_signing_key="audit_edge_secret_2026")
        self.realtime_sec = RealtimeCryptographicPresenceService(channel_signing_secret="audit_rt_secret_2026")
        self.rls_scanner = PostgresRlsComplianceScannerService()
        self.masking_sec = DynamicDataMaskingService()
        self.graphql_shield = PgGraphqlShieldService()
        self.zero_trust = EdgeFunctionZeroTrustGatewayService(secret_key="audit_zt_secret_2026")

    # =========================================================================
    # 1. Row-Level Security (RLS) Policy Tests
    # =========================================================================
    def test_rls_anon_access_denied_on_protected_tables(self):
        """Asserts unauthenticated anon caller is strictly denied on learner profiles."""
        res = self.supabase_sec.evaluate_rls_access(
            table_name="profiles",
            action="SELECT",
            caller_role="anon"
        )
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 401)

    def test_rls_authenticated_owner_allowed(self):
        """Asserts authenticated student can access their own application records."""
        res = self.supabase_sec.evaluate_rls_access(
            table_name="applications",
            action="UPDATE",
            caller_role="authenticated",
            caller_uid="usr_student_alice",
            caller_tenant_id="tenant_dhaka",
            target_owner_id="usr_student_alice",
            target_tenant_id="tenant_dhaka",
            client_payload_user_id="usr_student_alice"
        )
        self.assertEqual(res["verdict"], "ALLOWED")
        self.assertEqual(res["status_code"], 200)

    def test_rls_idor_and_cross_tenant_denied(self):
        """Asserts horizontal IDOR attempt across students is halted."""
        res = self.supabase_sec.evaluate_rls_access(
            table_name="escrow_vaults",
            action="SELECT",
            caller_role="authenticated",
            caller_uid="usr_student_attacker",
            target_owner_id="usr_student_victim"
        )
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)
        self.assertIn("IDOR_VIOLATION", res["reason"])

    def test_rls_client_payload_spoofing_denied(self):
        """Asserts client inserting foreign user_id in payload is blocked by RLS check."""
        res = self.supabase_sec.evaluate_rls_access(
            table_name="cv_snapshots",
            action="INSERT",
            caller_role="authenticated",
            caller_uid="usr_student_alice",
            client_payload_user_id="usr_impersonated_victim"
        )
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)

    # =========================================================================
    # 2. PostgREST Filter Injection & SQL Policy Generation Tests
    # =========================================================================
    def test_postgrest_injection_sanitization(self):
        """Asserts that dangerous or= clauses trying to bypass tenant filters are flagged."""
        malicious_query = {
            "select": "id,title",
            "or": "(tenant_id.eq.org_1,tenant_id.is.null)"
        }
        res = self.supabase_sec.sanitize_postgrest_query(malicious_query)
        self.assertFalse(res["is_safe"])
        self.assertGreaterEqual(res["threat_score"], 40)

    def test_postgrest_sql_generation(self):
        """Asserts compliant PostgreSQL RLS DDL generation with force row level security."""
        sql = self.supabase_sec.generate_secure_rls_sql("exam_submissions", "user_id", "tenant_id")
        self.assertIn("ENABLE ROW LEVEL SECURITY", sql)
        self.assertIn("FORCE ROW LEVEL SECURITY", sql)
        self.assertIn("auth.uid() = user_id", sql)

    # =========================================================================
    # 3. Edge Function JWT & Audience Validation Tests
    # =========================================================================
    def test_edge_jwt_token_verification(self):
        """Asserts that passing apikey alone without user Bearer token is rejected."""
        res = self.edge_sec.verify_edge_jwt_token(
            auth_header=None,
            apikey_header="sb_publishable_anon_demo_key_99"
        )
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["status_code"], 401)

    def test_edge_jwt_valid_bearer(self):
        """Asserts valid authenticated user token is accepted."""
        mock_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3JfMDEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIn0.signature_dummy"
        res = self.edge_sec.verify_edge_jwt_token(
            auth_header=f"Bearer {mock_jwt}",
            apikey_header=None
        )
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["status_code"], 200)

    # =========================================================================
    # 4. PostgreSQL Compliance Scanner Tests
    # =========================================================================
    def test_rls_compliance_scanner(self):
        """Asserts scanner flags tables lacking RLS and generates ALTER TABLE remediation."""
        table_schema = {
            "table_name": "bursary_ledgers",
            "rls_enabled": False,
            "policies": []
        }
        res = self.rls_scanner.scan_table_rls_compliance(table_schema)
        self.assertEqual(res["status"], "NON_COMPLIANT")
        self.assertTrue(any(v["code"] == "RLS_DISABLED" for v in res["violations"]))
        self.assertIn("ENABLE ROW LEVEL SECURITY", res["remediation_sql"])

    # =========================================================================
    # 5. Dynamic Data Masking & PII Protection Tests
    # =========================================================================
    def test_dynamic_data_masking_student_record(self):
        """Asserts student PII is masked when viewed by public or unauthorized roles."""
        record = {
            "full_name": "Tanvir Hassan",
            "email": "tanvir.hassan@example.com",
            "phone": "+8801712345678",
            "national_id": "19982692800123456",
            "gpa": "3.85"
        }
        res = self.masking_sec.mask_student_record(record, viewer_role="public")
        masked = res["masked_record"]
        self.assertNotIn("12345678", masked["phone"])
        self.assertIn("*", masked["phone"])
        self.assertNotIn("tanvir.hassan@", masked["email"])
        self.assertIn("*", masked["email"])
        self.assertIn("PHONE_PATTERN_MASKED", res["applied_rules"])
        self.assertIn("EMAIL_PATTERN_MASKED", res["applied_rules"])

    # =========================================================================
    # 6. GraphQL Query Depth & Introspection Shield Tests
    # =========================================================================
    def test_graphql_depth_shield(self):
        """Asserts that recursive deeply nested queries are halted."""
        deep_query = "{ a { b { c { d { e { f } } } } } }"
        res = self.graphql_shield.inspect_and_authorize_query(deep_query, caller_role="student")
        self.assertFalse(res["authorized"])
        self.assertTrue(any(v["code"] == "EXCESSIVE_QUERY_DEPTH" for v in res["violations"]))

    # =========================================================================
    # 7. Edge Zero-Trust Signature & Privilege Escalation Tests
    # =========================================================================
    def test_zero_trust_spoofed_service_role_defense(self):
        """Asserts that client injecting spoofed service_role header is blocked."""
        token = self.zero_trust.create_jwt(
            user_id="usr_attacker_999",
            role="student",
            tenant_id="univ_dhaka_01"
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "x-supabase-role": "service_role"  # Spoofed privilege escalation
        }
        result = self.zero_trust.verify_edge_request(headers)
        self.assertFalse(result["is_valid"])
        self.assertIn("PRIVILEGE_ESCALATION_BLOCKED", result["security_flags"])


if __name__ == "__main__":
    unittest.main()
