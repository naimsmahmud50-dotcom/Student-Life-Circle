# ==============================================================================
# File: backend/tests/test_phase49_jwks_query_hardener_and_cdc.py
# Phase: 49 - Supabase Edge JWKS, Query Hardener & Database CDC Audit Tests
# Description: Verifies asymmetric JWKS rotation, JTI anti-replay caching,
#              auth.uid identity binding, PostgREST query hardening, and
#              tamper-evident CDC Merkle chain integrity.
# ==============================================================================

import unittest
import time
from backend.app.services.edge_distributed_replay_service import EdgeDistributedReplayService
from backend.app.services.postgrest_query_hardener_service import PostgrestQueryHardenerService
from backend.app.services.database_cdc_audit_engine_service import DatabaseCDCAuditEngineService

class TestPhase49SupabaseJwksQueryHardenerAndCdc(unittest.TestCase):

    def setUp(self):
        self.edge_service = EdgeDistributedReplayService(
            expected_issuer="https://supabase.agrojatra.edu.bd/auth/v1",
            expected_aud="authenticated"
        )
        self.hardener_service = PostgrestQueryHardenerService()
        self.cdc_service = DatabaseCDCAuditEngineService()

    # --------------------------------------------------------------------------
    # 1. Edge Distributed Replay & JWKS Tests
    # --------------------------------------------------------------------------
    def test_jwks_rotation_and_retrieval(self):
        jwks = self.edge_service.get_jwks()
        self.assertIn("keys", jwks)
        self.assertGreaterEqual(len(jwks["keys"]), 2)

        rot_res = self.edge_service.rotate_signing_key("key-2026-q4-edge", "RS256")
        self.assertTrue(rot_res["rotated_successfully"])
        self.assertEqual(rot_res["active_kid"], "key-2026-q4-edge")

        # Verify new key is in JWKS
        updated_jwks = self.edge_service.get_jwks()
        kids = [k["kid"] for k in updated_jwks["keys"]]
        self.assertIn("key-2026-q4-edge", kids)

    def test_edge_token_valid_and_replay_defense(self):
        now = time.time()
        header = {"alg": "RS256", "kid": "key-prod-2026-a"}
        payload = {
            "iss": "https://supabase.agrojatra.edu.bd/auth/v1",
            "aud": "authenticated",
            "sub": "usr_stu_994101",
            "jti": "jti_nonce_uuid_771992",
            "exp": now + 3600,
            "role": "authenticated",
            "app_metadata": {"tenant_id": "inst_du_dhaka"}
        }

        # First verification must succeed
        res1 = self.edge_service.verify_edge_token(header, payload)
        self.assertTrue(res1["valid"])
        self.assertEqual(res1["server_uid"], "usr_stu_994101")
        self.assertEqual(res1["tenant_id"], "inst_du_dhaka")

        # Second verification with SAME JTI must be blocked as replay attack
        res2 = self.edge_service.verify_edge_token(header, payload)
        self.assertFalse(res2["valid"])
        self.assertEqual(res2["error_code"], "REPLAY_ATTACK_DETECTED")

    def test_edge_token_algorithm_confusion_and_identity_mismatch(self):
        now = time.time()
        # Insecure algorithm downgrade
        header_insecure = {"alg": "HS256", "kid": "key-prod-2026-a"}
        payload = {
            "iss": "https://supabase.agrojatra.edu.bd/auth/v1",
            "aud": "authenticated",
            "sub": "usr_stu_994101",
            "jti": "jti_unique_112233",
            "exp": now + 3600
        }
        res_alg = self.edge_service.verify_edge_token(header_insecure, payload)
        self.assertFalse(res_alg["valid"])
        self.assertEqual(res_alg["error_code"], "ALGORITHM_CONFUSION_REJECTED")

        # Identity spoofing attempt (client requested user ID does not match JWT sub)
        header_secure = {"alg": "RS256", "kid": "key-prod-2026-a"}
        res_spoof = self.edge_service.verify_edge_token(
            header_secure, payload, client_supplied_user_id="usr_victim_100200"
        )
        self.assertFalse(res_spoof["valid"])
        self.assertEqual(res_spoof["error_code"], "IDENTITY_MISMATCH")

    # --------------------------------------------------------------------------
    # 2. PostgREST Query Hardening Tests
    # --------------------------------------------------------------------------
    def test_postgrest_query_hardening_safe_and_tenant_enforcement(self):
        raw_params = {
            "student_id": "eq.stu_8820",
            "select": "id,course_name,grade",
            "order": "created_at.desc"
        }
        jwt_claims = {"tenant_id": "inst_buet_dhaka", "sub": "usr_stu_8820"}
        
        result = self.hardener_service.inspect_and_harden_query(raw_params, jwt_claims, "grades")
        self.assertTrue(result["is_safe"])
        self.assertEqual(len(result["violations"]), 0)
        self.assertEqual(result["hardened_params"]["tenant_id"], "eq.inst_buet_dhaka")

    def test_postgrest_query_hardening_detects_violations(self):
        # 1. Parameter pollution
        polluted_params = {
            "student_id": ["eq.stu_1", "eq.stu_2"],
            "select": "*"
        }
        jwt = {"tenant_id": "inst_buet_dhaka"}
        res_poll = self.hardener_service.inspect_and_harden_query(polluted_params, jwt, "grades")
        self.assertFalse(res_poll["is_safe"])
        self.assertTrue(any(v["code"] == "HTTP_PARAMETER_POLLUTION" for v in res_poll["violations"]))

        # 2. Wildcard poisoning on sensitive column
        wildcard_params = {
            "email": "ilike.%gmail.com",
            "select": "*"
        }
        res_wild = self.hardener_service.inspect_and_harden_query(wildcard_params, jwt, "profiles")
        self.assertFalse(res_wild["is_safe"])
        self.assertTrue(any(v["code"] == "UNANCHORED_WILDCARD_POISONING" for v in res_wild["violations"]))

        # 3. Cross-tenant tampering
        cross_tenant_params = {
            "institution_id": "eq.inst_ru_rajshahi",
            "select": "*"
        }
        res_cross = self.hardener_service.inspect_and_harden_query(cross_tenant_params, jwt, "attendance")
        self.assertFalse(res_cross["is_safe"])
        self.assertTrue(any(v["code"] == "CROSS_TENANT_TAMPERING" for v in res_cross["violations"]))

        # 4. Excessive embed depth
        deep_embed_params = {
            "select": "id,profiles(name,department(faculty(campus(building(room))))))"
        }
        res_depth = self.hardener_service.inspect_and_harden_query(deep_embed_params, jwt, "students")
        self.assertFalse(res_depth["is_safe"])
        self.assertTrue(any(v["code"] == "EXCESSIVE_EMBED_DEPTH" for v in res_depth["violations"]))

    # --------------------------------------------------------------------------
    # 3. Database CDC & Tamper-Evident Merkle Chain Tests
    # --------------------------------------------------------------------------
    def test_cdc_wal_ingest_and_cryptographic_integrity(self):
        # Ingest 3 WAL events
        e1 = self.cdc_service.ingest_wal_event(
            event_type="INSERT",
            table_name="student_transcripts",
            record_id="rec_9001",
            record_data={"student_id": "stu_01", "cgpa": 3.92, "nid": "1998542199801", "phone": "01711223344"},
            actor_id="registrar_office"
        )
        self.assertTrue(e1["success"])
        self.assertEqual(e1["sequence_index"], 0)

        e2 = self.cdc_service.ingest_wal_event(
            event_type="UPDATE",
            table_name="student_transcripts",
            record_id="rec_9001",
            record_data={"student_id": "stu_01", "cgpa": 3.95, "nid": "1998542199801", "phone": "01711223344"},
            actor_id="registrar_office"
        )
        self.assertEqual(e2["sequence_index"], 1)

        # Integrity verification must pass
        integrity = self.cdc_service.verify_audit_integrity()
        self.assertTrue(integrity["chain_valid"])
        self.assertEqual(integrity["total_blocks_verified"], 2)

        # Tamper simulation: mutate historical record
        self.cdc_service._audit_log[0]["payload"]["cgpa"] = 4.00
        tamper_res = self.cdc_service.verify_audit_integrity()
        self.assertFalse(tamper_res["chain_valid"])
        self.assertEqual(tamper_res["tamper_detected_at_index"], 0)

    def test_realtime_broadcast_authorization_and_pii_scrubbing(self):
        self.cdc_service.ingest_wal_event(
            event_type="INSERT",
            table_name="bursary_disbursements",
            record_id="bursary_rec_77",
            record_data={
                "student_id": "stu_authorized_user",
                "amount_bdt": 12500,
                "nid": "550012349876",
                "phone": "01819998877",
                "bursary_account": "1002998844"
            },
            actor_id="finance_dept"
        )
        trail = self.cdc_service.get_audit_trail()
        entry = trail[0]

        # Authorized student sees scrubbed PII
        broadcast = self.cdc_service.prepare_realtime_broadcast_payload(
            event_entry=entry,
            subscriber_user_id="stu_authorized_user",
            subscriber_role="student"
        )
        self.assertIsNotNone(broadcast)
        self.assertTrue(broadcast["broadcast_authorized"])
        # Check PII redaction
        self.assertIn("***-****-", broadcast["data"]["nid"])
        self.assertIn("+880-17****-", broadcast["data"]["phone"])
        self.assertIn("ACC-****-", broadcast["data"]["bursary_account"])

        # Unauthorized student cannot receive event
        unauth_broadcast = self.cdc_service.prepare_realtime_broadcast_payload(
            event_entry=entry,
            subscriber_user_id="stu_eavesdropper",
            subscriber_role="student"
        )
        self.assertIsNone(unauth_broadcast)

if __name__ == "__main__":
    unittest.main()
