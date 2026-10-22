import json
import time
import unittest
from backend.app.services.edge_function_zero_trust_gateway_service import EdgeFunctionZeroTrustGatewayService
from backend.app.services.database_webhook_replay_guard_service import DatabaseWebhookReplayGuardService
from backend.app.services.postgrest_audit_trail_engine_service import PostgrestAuditTrailEngineService


class TestPhase52EdgeGatewayWebhookAndAudit(unittest.TestCase):
    """
    Comprehensive Automated Unit Tests for Phase 52:
    - Edge Function Zero-Trust Gateway
    - Database Webhook Replay Guard
    - PostgREST Hash-Chained Audit Trail & Anomaly Engine
    """

    def setUp(self):
        self.gateway = EdgeFunctionZeroTrustGatewayService(secret_key="test-edge-secret-key-2026")
        self.webhook_guard = DatabaseWebhookReplayGuardService(secret="whsec_test_webhook_secret_key_2026")
        self.audit_engine = PostgrestAuditTrailEngineService()

    # --- Edge Function Zero-Trust Gateway Tests ---

    def test_01_edge_gateway_valid_jwt_verification(self):
        token = self.gateway.create_jwt(
            user_id="usr_prof_101",
            role="faculty",
            tenant_id="univ_dhaka_01",
            audience="authenticated",
            expires_in=3600
        )
        headers = {"Authorization": f"Bearer {token}"}
        result = self.gateway.verify_edge_request(headers)

        self.assertTrue(result["is_valid"])
        self.assertEqual(result["user_id"], "usr_prof_101")
        self.assertEqual(result["role"], "faculty")
        self.assertEqual(result["tenant_id"], "univ_dhaka_01")
        self.assertNotIn("PRIVILEGE_ESCALATION_BLOCKED", result["security_flags"])

    def test_02_edge_gateway_signature_tamper_rejection(self):
        token = self.gateway.create_jwt(
            user_id="usr_student_202",
            role="student",
            tenant_id="univ_dhaka_01"
        )
        # Tamper with the token body
        parts = token.split(".")
        tampered_token = f"{parts[0]}.{parts[1]}xyz.{parts[2]}"
        headers = {"Authorization": f"Bearer {tampered_token}"}
        result = self.gateway.verify_edge_request(headers)

        self.assertFalse(result["is_valid"])
        self.assertIn("INVALID_CRYPTOGRAPHIC_SIGNATURE", result["security_flags"])

    def test_03_edge_gateway_spoofed_service_role_header_defense(self):
        """Tests that client injecting x-supabase-role: service_role with normal token is rejected."""
        token = self.gateway.create_jwt(
            user_id="usr_attacker_999",
            role="student",
            tenant_id="univ_dhaka_01"
        )
        headers = {
            "Authorization": f"Bearer {token}",
            "x-supabase-role": "service_role"  # Header spoofing attack
        }
        result = self.gateway.verify_edge_request(headers)

        self.assertFalse(result["is_valid"])
        self.assertIn("SPOOFED_SERVICE_ROLE_HEADER_DETECTED", result["security_flags"])
        self.assertIn("PRIVILEGE_ESCALATION_BLOCKED", result["security_flags"])

    def test_04_edge_gateway_tenant_isolation_and_rbac(self):
        claims = {
            "sub": "usr_dean_01",
            "role": "academic_dean",
            "app_metadata": {"tenant_id": "buet_univ_02"}
        }
        # Check tenant isolation
        iso_pass = self.gateway.enforce_tenant_isolation(claims, target_tenant_id="buet_univ_02")
        self.assertTrue(iso_pass["isolated"])

        iso_fail = self.gateway.enforce_tenant_isolation(claims, target_tenant_id="du_univ_01")
        self.assertFalse(iso_fail["isolated"])
        self.assertIn("Tenant boundary violation", iso_fail["message"])

        # Check RBAC Action Authorization
        verdict_allowed = self.gateway.evaluate_edge_action_policy(
            user_role="academic_dean",
            function_name="finalize_course_grades",
            requested_action="approve"
        )
        self.assertTrue(verdict_allowed["allowed"])
        self.assertTrue(verdict_allowed["verdict_signature"].startswith("sig_v1_"))

        verdict_denied = self.gateway.evaluate_edge_action_policy(
            user_role="student",
            function_name="finalize_course_grades",
            requested_action="approve"
        )
        self.assertFalse(verdict_denied["allowed"])

    # --- Database Webhook Replay Guard Tests ---

    def test_05_webhook_valid_signature_and_attestation(self):
        msg_id = "msg_evt_001_success"
        ts = int(time.time())
        payload = json.dumps({"event": "STUDENT_ENROLLED", "student_id": "s_1001", "course": "CSE-101"})
        sig = self.webhook_guard.sign_test_webhook(msg_id, ts, payload)

        headers = {
            "webhook-id": msg_id,
            "webhook-timestamp": str(ts),
            "webhook-signature": sig
        }

        verify_res = self.webhook_guard.verify_webhook_signature(headers, payload.encode("utf-8"))
        self.assertTrue(verify_res["verified"])
        self.assertIsNone(verify_res["error_code"])

        # Attestation
        receipt = self.webhook_guard.attest_and_record_event(
            event_type="INSERT",
            table_name="student_enrollments",
            record_id="s_1001",
            payload={"student_id": "s_1001", "course": "CSE-101"}
        )
        self.assertEqual(receipt["status"], "ATTESTED_VALID")
        self.assertTrue(receipt["attestation_signature"].startswith("att_v1_"))

    def test_06_webhook_anti_replay_and_duplicate_rejection(self):
        msg_id = "msg_evt_002_replay"
        ts = int(time.time())
        payload = "test_payload_data"
        sig = self.webhook_guard.sign_test_webhook(msg_id, ts, payload)

        headers = {
            "webhook-id": msg_id,
            "webhook-timestamp": str(ts),
            "webhook-signature": sig
        }

        # First delivery passes
        res1 = self.webhook_guard.verify_webhook_signature(headers, payload.encode("utf-8"))
        self.assertTrue(res1["verified"])

        # Immediate replay attack with identical msg_id must fail
        res2 = self.webhook_guard.verify_webhook_signature(headers, payload.encode("utf-8"))
        self.assertFalse(res2["verified"])
        self.assertEqual(res2["error_code"], "DUPLICATE_MESSAGE_REPLAY")

    def test_07_webhook_expired_timestamp_rejection(self):
        msg_id = "msg_evt_003_expired"
        old_ts = int(time.time()) - 400  # 400s old > 300s max age
        payload = "expired_payload_data"
        sig = self.webhook_guard.sign_test_webhook(msg_id, old_ts, payload)

        headers = {
            "webhook-id": msg_id,
            "webhook-timestamp": str(old_ts),
            "webhook-signature": sig
        }

        res = self.webhook_guard.verify_webhook_signature(headers, payload.encode("utf-8"))
        self.assertFalse(res["verified"])
        self.assertEqual(res["error_code"], "REPLAY_WINDOW_EXPIRED")

    # --- PostgREST Hash-Chained Audit Trail Tests ---

    def test_08_audit_chain_integrity_and_recording(self):
        # Initial seeded chain should verify successfully
        init_verify = self.audit_engine.verify_audit_chain_integrity()
        self.assertTrue(init_verify["is_valid"])
        self.assertGreaterEqual(init_verify["total_entries"], 3)

        # Record new entry
        entry = self.audit_engine.record_audit_event(
            actor_id="usr_audit_lead",
            actor_role="lead_proctor",
            action="RPC_EXEC",
            schema_name="public",
            target_entity="fn_verify_room_integrity",
            metadata={"room_id": "hall_3", "proctors": 4}
        )
        self.assertIn("entry_hash", entry)
        self.assertIn("prev_hash", entry)

        # Re-verify chain
        post_verify = self.audit_engine.verify_audit_chain_integrity()
        self.assertTrue(post_verify["is_valid"])
        self.assertEqual(post_verify["chain_head_hash"], entry["entry_hash"])

    def test_09_audit_chain_tamper_detection(self):
        """Simulates an attacker tampering with an audit block payload."""
        # Tamper with an internal entry in memory
        target_entry = self.audit_engine._audit_chain[1]
        original_actor = target_entry["actor_id"]
        target_entry["actor_id"] = "hacked_actor"

        tamper_verify = self.audit_engine.verify_audit_chain_integrity()
        self.assertFalse(tamper_verify["is_valid"])
        self.assertEqual(tamper_verify["broken_index"], 1)
        self.assertIn("tampering detected", tamper_verify["reason"].lower())

        # Restore
        target_entry["actor_id"] = original_actor

    def test_10_audit_anomaly_detection_mass_deletion_and_rpc_abuse(self):
        engine = PostgrestAuditTrailEngineService()
        now = int(time.time())

        # Simulate 6 fast deletions by rogue actor
        for i in range(6):
            engine.record_audit_event(
                actor_id="rogue_user_13",
                actor_role="student",
                action="ROW_DELETE",
                schema_name="public",
                target_entity=f"quiz_submissions_{i}",
                metadata={"record_id": str(i)},
                timestamp=now - (i * 2)
            )

        # Simulate unauthorized execution of dangerous SECURITY DEFINER RPC
        engine.record_audit_event(
            actor_id="rogue_user_13",
            actor_role="student",
            action="RPC_EXEC",
            schema_name="public",
            target_entity="fn_admin_wipe",
            metadata={"target_table": "transcripts"},
            timestamp=now - 5
        )

        anomalies_report = engine.detect_audit_anomalies(time_window_seconds=300)
        self.assertIn(anomalies_report["threat_level"], ["HIGH", "CRITICAL"])
        self.assertGreaterEqual(anomalies_report["anomalies_detected"], 2)

        types = [a["type"] for a in anomalies_report["anomalies"]]
        self.assertIn("MASS_DELETION_BURST", types)
        self.assertIn("PRIVILEGED_RPC_ABUSE_ATTEMPT", types)


if __name__ == "__main__":
    unittest.main()
