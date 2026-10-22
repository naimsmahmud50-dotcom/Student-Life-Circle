"""
================================================================================
TEST SUITE: Phase 61 Enterprise Supabase Production Cockpit & Live Console
STANDARDS: OWASP ASVS 4.0 Level 2, Strix-Supabase Security Playbook
PURPOSE: Comprehensive unit test coverage for RLS simulation, storage quarantine,
         edge telemetry, and cryptographic migration integrity.
================================================================================
"""

import unittest
from backend.app.services.supabase_production_cockpit_service import SupabaseProductionCockpitService


class TestSupabaseProductionCockpit(unittest.TestCase):

    def setUp(self):
        self.service = SupabaseProductionCockpitService()
        self.tenant_a = "11111111-1111-1111-1111-111111111111"
        self.tenant_b = "22222222-2222-2222-2222-222222222222"
        self.user_alice = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        self.user_bob = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"

    # --------------------------------------------------------------------------
    # 1. RLS Role & Origin Tests
    # --------------------------------------------------------------------------
    def test_service_role_browser_origin_critical_denial(self):
        res = self.service.simulate_rls_policy({
            "table_name": "profiles",
            "action": "SELECT",
            "caller_role": "service_role",
            "is_browser_origin": True
        })
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)
        self.assertEqual(res["threat_level"], "CRITICAL")
        self.assertIn("CRITICAL_KEY_EXPOSURE", res["reason"])

    def test_service_role_server_bypass(self):
        res = self.service.simulate_rls_policy({
            "table_name": "profiles",
            "action": "SELECT",
            "caller_role": "service_role",
            "is_browser_origin": False
        })
        self.assertEqual(res["verdict"], "ALLOWED")
        self.assertEqual(res["status_code"], 200)
        self.assertEqual(res["threat_level"], "NONE")

    def test_anon_direct_profile_access_denied(self):
        res = self.service.simulate_rls_policy({
            "table_name": "profiles",
            "action": "SELECT",
            "caller_role": "anon"
        })
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 401)

    def test_anon_published_question_bank_allowed(self):
        res = self.service.simulate_rls_policy({
            "table_name": "question_items",
            "action": "SELECT",
            "caller_role": "anon"
        })
        self.assertEqual(res["verdict"], "ALLOWED")
        self.assertEqual(res["status_code"], 200)

    def test_anon_verifiable_credentials_allowed(self):
        res = self.service.simulate_rls_policy({
            "table_name": "verifiable_credentials",
            "action": "SELECT",
            "caller_role": "anon"
        })
        self.assertEqual(res["verdict"], "ALLOWED")
        self.assertEqual(res["status_code"], 200)

    # --------------------------------------------------------------------------
    # 2. Spoofing & Tenant Isolation Tests
    # --------------------------------------------------------------------------
    def test_payload_user_id_spoofing_denied(self):
        res = self.service.simulate_rls_policy({
            "table_name": "profiles",
            "action": "UPDATE",
            "caller_role": "student",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a,
            "target_owner_id": self.user_alice,
            "target_tenant_id": self.tenant_a,
            "client_payload_user_id": self.user_bob
        })
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)
        self.assertEqual(res["threat_level"], "HIGH")
        self.assertIn("spoofing", res["reason"].lower())

    def test_tenant_boundary_isolation_enforced(self):
        res = self.service.simulate_rls_policy({
            "table_name": "exam_submissions",
            "action": "SELECT",
            "caller_role": "student",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a,
            "target_owner_id": self.user_alice,
            "target_tenant_id": self.tenant_b
        })
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)
        self.assertEqual(res["applied_policy"], "TENANT_ISOLATION_GUARD")

    # --------------------------------------------------------------------------
    # 3. Table-Specific Authorization & IDOR Tests
    # --------------------------------------------------------------------------
    def test_profile_idor_violation(self):
        res = self.service.simulate_rls_policy({
            "table_name": "profiles",
            "action": "UPDATE",
            "caller_role": "student",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a,
            "target_owner_id": self.user_bob,
            "target_tenant_id": self.tenant_a
        })
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)
        self.assertIn("IDOR", res["reason"])

    def test_profile_own_update_allowed(self):
        res = self.service.simulate_rls_policy({
            "table_name": "profiles",
            "action": "UPDATE",
            "caller_role": "student",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a,
            "target_owner_id": self.user_alice,
            "target_tenant_id": self.tenant_a
        })
        self.assertEqual(res["verdict"], "ALLOWED")
        self.assertEqual(res["status_code"], 200)

    def test_student_question_mutation_denied(self):
        res = self.service.simulate_rls_policy({
            "table_name": "question_items",
            "action": "INSERT",
            "caller_role": "student",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a
        })
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)

    def test_educator_question_mutation_allowed(self):
        res = self.service.simulate_rls_policy({
            "table_name": "question_items",
            "action": "INSERT",
            "caller_role": "educator",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a
        })
        self.assertEqual(res["verdict"], "ALLOWED")
        self.assertEqual(res["status_code"], 200)

    def test_student_exam_submission_immutable(self):
        res = self.service.simulate_rls_policy({
            "table_name": "exam_submissions",
            "action": "UPDATE",
            "caller_role": "student",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a
        })
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)
        self.assertIn("IMMUTABILITY", res["reason"])

    def test_student_peer_exam_idor_denied(self):
        res = self.service.simulate_rls_policy({
            "table_name": "exam_submissions",
            "action": "SELECT",
            "caller_role": "student",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a,
            "target_owner_id": self.user_bob,
            "target_tenant_id": self.tenant_a
        })
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)
        self.assertIn("peer", res["reason"])

    def test_escrow_settlement_restricted(self):
        # Student cannot update escrow vault
        res = self.service.simulate_rls_policy({
            "table_name": "escrow_vaults",
            "action": "UPDATE",
            "caller_role": "student",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a
        })
        self.assertEqual(res["verdict"], "DENIED")
        self.assertEqual(res["status_code"], 403)

        # Admin can update escrow vault
        res_admin = self.service.simulate_rls_policy({
            "table_name": "escrow_vaults",
            "action": "UPDATE",
            "caller_role": "institutional_admin",
            "caller_uid": self.user_alice,
            "caller_tenant_id": self.tenant_a
        })
        self.assertEqual(res_admin["verdict"], "ALLOWED")
        self.assertEqual(res_admin["status_code"], 200)

    # --------------------------------------------------------------------------
    # 4. Storage Quarantine & Anti-Malware Tests
    # --------------------------------------------------------------------------
    def test_storage_quarantine_executable(self):
        res = self.service.audit_storage_upload({
            "bucket_id": "student-docs",
            "file_name": "malicious.exe",
            "file_size_bytes": 1024,
            "declared_mime_type": "application/octet-stream",
            "file_hex_magic": "4d5a9000",
            "is_public_bucket": False
        })
        self.assertTrue(res["is_quarantined"])
        self.assertEqual(res["security_verdict"], "QUARANTINED")
        self.assertEqual(res["detected_mime_type"], "application/x-dosexec")

    def test_storage_mime_spoofing_quarantine(self):
        res = self.service.audit_storage_upload({
            "bucket_id": "profile-photos",
            "file_name": "avatar.png",
            "file_size_bytes": 2048,
            "declared_mime_type": "image/png",
            "file_hex_magic": "3c73766720786d",  # <svg xm... (SVG vector with possible XSS script)
            "is_public_bucket": False
        })
        self.assertTrue(res["is_quarantined"])
        self.assertEqual(res["security_verdict"], "QUARANTINED")
        self.assertEqual(res["risk_assessment"], "HIGH_EXPLOIT_CAMOUFLAGE")

    def test_storage_public_bucket_private_data_blocked(self):
        res = self.service.audit_storage_upload({
            "bucket_id": "student-credentials",
            "file_name": "diploma.pdf",
            "file_size_bytes": 50000,
            "declared_mime_type": "application/pdf",
            "file_hex_magic": "255044462d312e",
            "is_public_bucket": True
        })
        self.assertTrue(res["is_quarantined"])
        self.assertEqual(res["security_verdict"], "BLOCKED_PUBLIC_LEAK")
        self.assertEqual(res["risk_assessment"], "CRITICAL_PII_EXPOSURE")

    def test_storage_clean_upload_approved(self):
        res = self.service.audit_storage_upload({
            "bucket_id": "assignments",
            "file_name": "homework.pdf",
            "file_size_bytes": 35000,
            "declared_mime_type": "application/pdf",
            "file_hex_magic": "255044462d312e34",
            "is_public_bucket": False
        })
        self.assertFalse(res["is_quarantined"])
        self.assertEqual(res["security_verdict"], "APPROVED_SECURE")
        self.assertEqual(res["detected_mime_type"], "application/pdf")
        self.assertIn("attachment", res["disposition_header"])

    # --------------------------------------------------------------------------
    # 5. Edge Telemetry & Migration Verification Tests
    # --------------------------------------------------------------------------
    def test_edge_telemetry_metrics(self):
        res = self.service.get_edge_telemetry()
        self.assertIn("PGBOUNCER", res["connection_pool_status"])
        self.assertGreaterEqual(res["active_connections"], 0)
        self.assertGreater(res["zero_trust_jwt_binding_rate"], 99.0)
        self.assertGreater(len(res["active_edge_regions"]), 0)

    def test_migration_status_cryptographic_verification(self):
        res = self.service.get_migrations_status()
        self.assertGreaterEqual(res["total_migrations"], 2)
        self.assertEqual(res["overall_integrity"], "CRYPTOGRAPHICALLY_VERIFIED")
        
        # Verify both 001 and 002 files are present with sha256 checksums
        filenames = [m["file_name"] for m in res["migrations"]]
        self.assertIn("001_core_supabase_schema.sql", filenames)
        self.assertIn("002_rls_security_policies.sql", filenames)
        for m in res["migrations"]:
            self.assertEqual(len(m["sha256_checksum"]), 64)
            self.assertEqual(m["applied_status"], "APPLIED_AND_SYNCHRONIZED")


if __name__ == "__main__":
    unittest.main()
