# ==============================================================================
# File: backend/tests/test_phase51_presence_rls_and_anonymization.py
# Phase: 51 - Realtime Presence, RLS Compliance & Privacy Vault Tests
# Description: Verifies Realtime presence HMAC authentication, zombie session reaping,
#              PostgreSQL RLS static compliance scanning, and K-Anonymity /
#              differential privacy data masking.
# ==============================================================================

import unittest
import time
from backend.app.services.realtime_presence_integrity_service import RealtimePresenceIntegrityService
from backend.app.services.postgres_rls_compliance_scanner_service import PostgresRlsComplianceScannerService
from backend.app.services.database_anonymization_vault_service import DatabaseAnonymizationVaultService

class TestPhase51PresenceRlsAndAnonymization(unittest.TestCase):

    def setUp(self):
        self.presence_service = RealtimePresenceIntegrityService()
        self.rls_scanner = PostgresRlsComplianceScannerService()
        self.privacy_vault = DatabaseAnonymizationVaultService()

    # --------------------------------------------------------------------------
    # 1. Realtime Presence & Liveness Tests
    # --------------------------------------------------------------------------
    def test_presence_ticket_generate_and_authorized_join(self):
        ticket = self.presence_service.generate_presence_ticket(
            channel_name="room:study_circ_101",
            user_id="usr_stu_101",
            user_role="student",
            ttl_seconds=300
        )
        self.assertIn("presence_signature", ticket)
        self.assertEqual(len(ticket["presence_signature"]), 64)

        # Authorized Join
        join_res = self.presence_service.verify_and_join_presence(
            channel_name=ticket["channel_name"],
            user_id=ticket["user_id"],
            session_id=ticket["session_id"],
            user_role=ticket["user_role"],
            expires_at=ticket["expires_at"],
            signature=ticket["presence_signature"]
        )
        self.assertTrue(join_res["authorized"])
        self.assertEqual(join_res["active_peer_count"], 1)

    def test_presence_phantom_injection_and_tamper_defense(self):
        ticket = self.presence_service.generate_presence_ticket(
            channel_name="room:study_circ_101",
            user_id="usr_stu_101"
        )
        # Attempt to join with forged signature
        join_forged = self.presence_service.verify_and_join_presence(
            channel_name=ticket["channel_name"],
            user_id=ticket["user_id"],
            session_id=ticket["session_id"],
            user_role=ticket["user_role"],
            expires_at=ticket["expires_at"],
            signature="bad_forged_hex_signature_0000000000000000000000000000000000000000"
        )
        self.assertFalse(join_forged["authorized"])
        self.assertEqual(join_forged["error_code"], "PHANTOM_INJECTION_DETECTED")

    def test_presence_heartbeat_and_zombie_reaper(self):
        ticket = self.presence_service.generate_presence_ticket(
            channel_name="room:exam_proctor_501",
            user_id="usr_stu_88"
        )
        self.presence_service.verify_and_join_presence(
            channel_name=ticket["channel_name"],
            user_id=ticket["user_id"],
            session_id=ticket["session_id"],
            user_role=ticket["user_role"],
            expires_at=ticket["expires_at"],
            signature=ticket["presence_signature"]
        )
        # Verify active
        self.assertEqual(len(self.presence_service.list_active_peers(ticket["channel_name"])), 1)

        # Heartbeat update
        hb = self.presence_service.record_heartbeat(ticket["channel_name"], ticket["session_id"])
        self.assertTrue(hb)

        # Simulate timeout: reap zombies with max_idle_sec=0
        reaped = self.presence_service.reap_zombie_sessions(ticket["channel_name"], max_idle_sec=-1.0)
        self.assertIn(ticket["session_id"], reaped)
        self.assertEqual(len(self.presence_service.list_active_peers(ticket["channel_name"])), 0)

    # --------------------------------------------------------------------------
    # 2. PostgreSQL RLS Compliance Scanner Tests
    # --------------------------------------------------------------------------
    def test_rls_compliance_compliant_table(self):
        table_schema = {
            "table_name": "student_transcripts",
            "rls_enabled": True,
            "policies": [
                {"name": "sel_policy", "cmd": "SELECT", "using": "tenant_id = auth.jwt() ->> 'tenant_id'"},
                {"name": "ins_policy", "cmd": "INSERT", "with_check": "user_id = auth.uid()"},
                {"name": "upd_policy", "cmd": "UPDATE", "using": "user_id = auth.uid()"},
                {"name": "del_policy", "cmd": "DELETE", "using": "auth.jwt() ->> 'role' = 'admin'"}
            ]
        }
        res = self.rls_scanner.scan_table_rls_compliance(table_schema)
        self.assertEqual(res["status"], "COMPLIANT")
        self.assertGreaterEqual(res["compliance_score"], 85)
        self.assertEqual(len(res["violations"]), 0)

    def test_rls_compliance_disabled_table_and_remediation(self):
        table_schema = {
            "table_name": "bursary_ledgers",
            "rls_enabled": False,
            "policies": []
        }
        res = self.rls_scanner.scan_table_rls_compliance(table_schema)
        self.assertEqual(res["status"], "NON_COMPLIANT")
        self.assertTrue(any(v["code"] == "RLS_DISABLED" for v in res["violations"]))
        self.assertIn("ALTER TABLE bursary_ledgers ENABLE ROW LEVEL SECURITY", res["remediation_sql"])

    def test_security_definer_function_scan(self):
        # Insecure function
        insecure_func = {
            "function_name": "rpc_elevate_privilege",
            "security_type": "SECURITY DEFINER",
            "search_path_set": False
        }
        res_insec = self.rls_scanner.scan_function_security_definer(insecure_func)
        self.assertFalse(res_insec["is_secure"])
        self.assertTrue(any(v["code"] == "SEARCH_PATH_HIJACK_VULNERABILITY" for v in res_insec["violations"]))
        self.assertIn("SET search_path = ''", res_insec["remediation_sql"])

        # Secure function
        secure_func = {
            "function_name": "rpc_safe_sum",
            "security_type": "SECURITY DEFINER",
            "search_path_set": True
        }
        res_sec = self.rls_scanner.scan_function_security_definer(secure_func)
        self.assertTrue(res_sec["is_secure"])

    # --------------------------------------------------------------------------
    # 3. Privacy Vault & Anonymization Tests
    # --------------------------------------------------------------------------
    def test_pseudonymization_and_laplace_noise(self):
        p1 = self.privacy_vault.pseudonymize_identifier("19982692800123456", field_salt="nid")
        p2 = self.privacy_vault.pseudonymize_identifier("19982692800123456", field_salt="nid")
        # Must be deterministic
        self.assertEqual(p1, p2)
        self.assertTrue(p1.startswith("ps_"))

        # Different salt gives different pseudonym
        p_other = self.privacy_vault.pseudonymize_identifier("19982692800123456", field_salt="phone")
        self.assertNotEqual(p1, p_other)

        # Differential privacy noise injection
        dp_res = self.privacy_vault.inject_laplace_noise(true_value=3.85, sensitivity=0.1, epsilon=0.5)
        self.assertEqual(dp_res["true_value"], 3.85)
        self.assertIn("noisy_value", dp_res)
        self.assertEqual(dp_res["epsilon_budget"], 0.5)

    def test_k_anonymity_evaluation_and_dataset_masking(self):
        # Create dataset with k=6 for ('Dhaka', '2026')
        records = [
            {"student_id": f"stu_{i}", "district": "Dhaka", "year": "2026", "gpa": 3.8}
            for i in range(10)
        ]
        k_eval = self.privacy_vault.evaluate_k_anonymity(records, quasi_identifiers=["district", "year"])
        self.assertTrue(k_eval["is_k_anonymous"])
        self.assertEqual(k_eval["k_min_achieved"], 10)
        self.assertEqual(k_eval["status"], "APPROVED_FOR_PUBLIC_RELEASE")

        # Anonymize dataset
        anon_res = self.privacy_vault.anonymize_dataset(
            dataset=records,
            direct_identifiers=["student_id"],
            quasi_identifiers=["district", "year"]
        )
        self.assertEqual(anon_res["records_processed"], 10)
        self.assertTrue(anon_res["sanitized_sample"][0]["student_id"].startswith("ps_"))

if __name__ == "__main__":
    unittest.main()
