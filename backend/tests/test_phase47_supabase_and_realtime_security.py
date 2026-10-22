"""
================================================================================
TEST SUITE: Phase 47 - Supabase Security, RLS Policy Engine & Realtime Guards
STANDARDS: OWASP ASVS L2, Strix-Supabase Security Playbook, Zero-IDOR Architecture
FILE: backend/tests/test_phase47_supabase_and_realtime_security.py
================================================================================
"""

import unittest
from backend.app.services.supabase_security_service import SupabaseSecurityService
from backend.app.services.edge_function_boundary_service import EdgeFunctionBoundaryService
from backend.app.services.realtime_cryptographic_presence_service import RealtimeCryptographicPresenceService


class TestPhase47SupabaseAndRealtimeSecurity(unittest.TestCase):
    def setUp(self):
        self.supabase_sec = SupabaseSecurityService()
        self.edge_sec = EdgeFunctionBoundaryService(secret_signing_key="test_signing_key_47")
        self.realtime_sec = RealtimeCryptographicPresenceService(channel_signing_secret="test_realtime_secret_47")

    # =========================================================================
    # 1. Row-Level Security (RLS) Policy Tests
    # =========================================================================
    def test_rls_anon_public_table_permitted(self):
        result = self.supabase_sec.evaluate_rls_access(
            table_name="public_curricula",
            action="SELECT",
            caller_role="anon"
        )
        self.assertEqual(result["verdict"], "ALLOWED")
        self.assertEqual(result["status_code"], 200)

    def test_rls_anon_protected_table_denied(self):
        result = self.supabase_sec.evaluate_rls_access(
            table_name="profiles",
            action="SELECT",
            caller_role="anon"
        )
        self.assertEqual(result["verdict"], "DENIED")
        self.assertEqual(result["status_code"], 401)

    def test_rls_browser_service_role_leaked_key_rejected(self):
        result = self.supabase_sec.evaluate_rls_access(
            table_name="scholarships",
            action="SELECT",
            caller_role="service_role",
            is_browser_origin=True
        )
        self.assertEqual(result["verdict"], "DENIED")
        self.assertEqual(result["status_code"], 403)
        self.assertEqual(result["threat_level"], "CRITICAL")

    def test_rls_authenticated_owner_allowed(self):
        result = self.supabase_sec.evaluate_rls_access(
            table_name="applications",
            action="UPDATE",
            caller_role="authenticated",
            caller_uid="usr_student_01",
            caller_tenant_id="tenant_dhaka",
            target_owner_id="usr_student_01",
            target_tenant_id="tenant_dhaka",
            client_payload_user_id="usr_student_01"
        )
        self.assertEqual(result["verdict"], "ALLOWED")
        self.assertEqual(result["status_code"], 200)

    def test_rls_authenticated_idor_denied(self):
        result = self.supabase_sec.evaluate_rls_access(
            table_name="escrow_vaults",
            action="SELECT",
            caller_role="authenticated",
            caller_uid="usr_student_attacker",
            target_owner_id="usr_student_victim"
        )
        self.assertEqual(result["verdict"], "DENIED")
        self.assertEqual(result["status_code"], 403)
        self.assertIn("IDOR_VIOLATION", result["reason"])

    def test_rls_client_payload_spoofing_denied(self):
        result = self.supabase_sec.evaluate_rls_access(
            table_name="cv_snapshots",
            action="INSERT",
            caller_role="authenticated",
            caller_uid="usr_student_01",
            client_payload_user_id="usr_impersonated_victim"
        )
        self.assertEqual(result["verdict"], "DENIED")
        self.assertEqual(result["status_code"], 403)
        self.assertIn("POLICY_VIOLATION", result["reason"])

    def test_rls_cross_tenant_breach_denied(self):
        result = self.supabase_sec.evaluate_rls_access(
            table_name="exam_submissions",
            action="SELECT",
            caller_role="authenticated",
            caller_uid="usr_student_01",
            caller_tenant_id="tenant_chittagong",
            target_owner_id="usr_student_01",
            target_tenant_id="tenant_dhaka"
        )
        self.assertEqual(result["verdict"], "DENIED")
        self.assertEqual(result["status_code"], 403)
        self.assertIn("TENANT_ISOLATION_VIOLATION", result["reason"])

    # =========================================================================
    # 2. PostgREST Query Sanitization & SQL Generation Tests
    # =========================================================================
    def test_postgrest_sanitize_or_filter_injection(self):
        raw_query = {
            "select": "id,title",
            "or": "(tenant_id.eq.org_1,tenant_id.is.null)"
        }
        res = self.supabase_sec.sanitize_postgrest_query(raw_query)
        self.assertFalse(res["is_safe"])
        self.assertGreaterEqual(res["threat_score"], 40)
        self.assertTrue(any("or" in a.lower() for a in res["anomalies"]))

    def test_postgrest_sql_generation(self):
        sql = self.supabase_sec.generate_secure_rls_sql("exam_submissions", "user_id", "tenant_id")
        self.assertIn("ALTER TABLE public.exam_submissions ENABLE ROW LEVEL SECURITY;", sql)
        self.assertIn("FORCE ROW LEVEL SECURITY;", sql)
        self.assertIn("auth.uid() = user_id", sql)
        self.assertIn("(auth.jwt() ->> 'tenant_id')::uuid", sql)

    # =========================================================================
    # 3. RPC Function Audit & Edge JWT Tests
    # =========================================================================
    def test_rpc_audit_vulnerable_security_definer(self):
        vulnerable_sql = """
        CREATE OR REPLACE FUNCTION admin_disburse_scholarship(p_user_id uuid, p_amount numeric)
        RETURNS void LANGUAGE plpgsql SECURITY DEFINER AS $$
        BEGIN
            UPDATE accounts SET balance = balance + p_amount WHERE id = p_user_id;
        END;
        $$;
        """
        audit = self.edge_sec.audit_rpc_function("admin_disburse_scholarship", vulnerable_sql, "SECURITY DEFINER")
        self.assertFalse(audit["is_compliant"])
        self.assertLess(audit["safety_score"], 60)
        self.assertTrue(len(audit["vulnerabilities"]) >= 2)
        self.assertIn("search_path", audit["remediation_sql"])

    def test_rpc_audit_hardened_invoker(self):
        safe_sql = """
        CREATE OR REPLACE FUNCTION get_my_study_stats()
        RETURNS jsonb LANGUAGE plpgsql SECURITY INVOKER SET search_path = public AS $$
        BEGIN
            IF auth.uid() IS NULL THEN RAISE EXCEPTION 'Unauthenticated'; END IF;
            RETURN jsonb_build_object('user', auth.uid());
        END;
        $$;
        """
        audit = self.edge_sec.audit_rpc_function("get_my_study_stats", safe_sql, "SECURITY INVOKER")
        self.assertTrue(audit["is_compliant"])
        self.assertEqual(audit["safety_score"], 100)

    def test_edge_jwt_apikey_only_rejected(self):
        res = self.edge_sec.verify_edge_jwt_token(
            auth_header=None,
            apikey_header="sb_publishable_anon_demo_key_99"
        )
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["status_code"], 401)
        self.assertIn("PASSING_APIKEY_ONLY_IS_INSUFFICIENT", res["reason"])

    def test_edge_jwt_valid_bearer_accepted(self):
        mock_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3JfMDEiLCJhdWQiOiJhdXRoZW50aWNhdGVkIn0.signature_dummy"
        res = self.edge_sec.verify_edge_jwt_token(auth_header=f"Bearer {mock_jwt}", apikey_header=None)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["status_code"], 200)

    # =========================================================================
    # 4. Storage Signed URLs & Realtime Channel Guard Tests
    # =========================================================================
    def test_storage_signed_url_anti_sniff_headers(self):
        res = self.edge_sec.generate_storage_signed_url(
            bucket_id="cv_vault",
            file_path="user_123/cv.html",  # Dangerous HTML type
            user_id="user_123",
            ttl_seconds=300,
            content_type="text/html"
        )
        self.assertTrue(res["is_private"])
        self.assertIn("token=", res["signed_url"])
        self.assertEqual(res["response_headers"]["X-Content-Type-Options"], "nosniff")
        self.assertIn("attachment", res["response_headers"]["Content-Disposition"])

    def test_realtime_channel_authorization(self):
        # Case A: Enrolled room member
        res_ok = self.realtime_sec.authorize_channel_subscription(
            channel_name="room:circle_physics_101",
            user_id="usr_student_alpha",
            user_role="student",
            tenant_id="tenant_01",
            enrolled_circles=["circle_physics_101"]
        )
        self.assertTrue(res_ok["authorized"])
        self.assertIsNotNone(res_ok["join_token"])

        # Case B: Cross-room intrusion denied
        res_denied = self.realtime_sec.authorize_channel_subscription(
            channel_name="room:circle_advanced_robotics",
            user_id="usr_student_alpha",
            user_role="student",
            tenant_id="tenant_01",
            enrolled_circles=["circle_physics_101"]
        )
        self.assertFalse(res_denied["authorized"])
        self.assertIsNone(res_denied["join_token"])

    def test_realtime_payload_pii_filtering(self):
        event_payload = {
            "student_name": "Rahim",
            "score": 94.5,
            "phone_number": "+8801700000000",
            "home_address": "Dhanmondi, Dhaka"
        }
        res = self.realtime_sec.filter_broadcast_payload("live_mcq_update", event_payload)
        self.assertNotIn("phone_number", res["sanitized_payload"])
        self.assertNotIn("home_address", res["sanitized_payload"])
        self.assertIn("student_name", res["sanitized_payload"])
        self.assertEqual(len(res["stripped_pii_fields"]), 2)


if __name__ == "__main__":
    unittest.main()
