"""
Unit tests for Phase 55: Zero-Knowledge Multi-Tenant Partitioning,
Row-Level Cryptographic Attestation & Cross-Region CDC Replication.
"""

import time
import unittest
from backend.app.services.zk_tenant_partition_service import ZeroKnowledgeTenantPartitionService
from backend.app.services.row_level_merkle_attestation_service import RowLevelAttestationMerkleService
from backend.app.services.cdc_replication_conflict_service import CdcReplicationConflictService


class TestPhase55TenantMerkleCdc(unittest.TestCase):

    def setUp(self):
        self.zk_service = ZeroKnowledgeTenantPartitionService()
        self.merkle_service = RowLevelAttestationMerkleService()
        self.cdc_service = CdcReplicationConflictService()

    # --- T001: Zero-Knowledge Multi-Tenant Partitioning Tests ---
    def test_tenant_partition_valid_route(self):
        res = self.zk_service.route_query(
            tenant_id="inst_buet",
            table_name="academic_records",
            query_filters={"semester": "Term-1"}
        )
        self.assertTrue(res["success"])
        self.assertEqual(res["target_partition_table"], "academic_records_part_inst_buet")
        self.assertTrue(res["pruning_boundary_enforced"])
        self.assertEqual(res["sanitized_filter"]["tenant_id"], "inst_buet")
        self.assertEqual(res["sanitized_filter"]["semester"], "Term-1")

    def test_tenant_partition_unregistered_tenant(self):
        res = self.zk_service.route_query(
            tenant_id="inst_unknown_university",
            table_name="students"
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["security_verdict"], "REJECTED_UNKNOWN_TENANT")

    def test_tenant_partition_signature_verification(self):
        valid_sig = self.zk_service.generate_tenant_proof("inst_du")
        res_valid = self.zk_service.validate_tenant_boundary("inst_du", auth_token_signature=valid_sig)
        self.assertTrue(res_valid["valid"])
        self.assertEqual(res_valid["security_verdict"], "VERIFIED_BOUNDARY_ACCEPTED")

        res_forged = self.zk_service.validate_tenant_boundary("inst_du", auth_token_signature="forged_signature_000")
        self.assertFalse(res_forged["valid"])
        self.assertEqual(res_forged["security_verdict"], "REJECTED_FORGED_SIGNATURE")

    def test_tenant_partition_escape_detection(self):
        # Union probe
        res1 = self.zk_service.detect_partition_escape_attempt("inst_buet", "SELECT * FROM academic_records UNION SELECT * FROM secret_passwords")
        self.assertTrue(res1["blocked"])
        self.assertEqual(res1["detected_vector"], "UNION_PARTITION_ESCAPE_ATTEMPT")

        # Wildcard probe
        res2 = self.zk_service.detect_partition_escape_attempt("inst_buet", "SELECT * FROM part_* WHERE 1=1")
        self.assertTrue(res2["blocked"])
        self.assertEqual(res2["detected_vector"], "WILDCARD_PARTITION_PROBE")

        # Cross-tenant discovery probe
        res3 = self.zk_service.detect_partition_escape_attempt("inst_buet", "SELECT * FROM academic_records WHERE tenant_id = 'inst_du'")
        self.assertTrue(res3["blocked"])
        self.assertEqual(res3["detected_vector"], "CROSS_TENANT_DISCOVERY_PROBE")

        # Clean query
        res4 = self.zk_service.detect_partition_escape_attempt("inst_buet", "department = 'CSE' AND batch = 2024")
        self.assertFalse(res4["blocked"])

    def test_partition_topology_coverage(self):
        topo = self.zk_service.get_partition_topology()
        self.assertEqual(topo["total_tenants"], 8)
        self.assertIn("students", topo["partitionable_entities"])
        inst_ids = [p["tenant_id"] for p in topo["partitions"]]
        self.assertIn("inst_buet", inst_ids)
        self.assertIn("inst_cadet", inst_ids)

    # --- T002: Row-Level Merkle Attestation Tests ---
    def test_row_attestation_canonical_seal(self):
        payload = {"student_id": "stu_buet_01", "gpa": 3.95, "degree": "B.Sc CSE"}
        attestation = self.merkle_service.generate_row_attestation(
            record_id="rec_001",
            tenant_id="inst_buet",
            entity_type="transcript",
            payload=payload
        )
        self.assertEqual(attestation["record_id"], "rec_001")
        self.assertEqual(attestation["attestation_status"], "CRYPTOGRAPHICALLY_SEALED")
        self.assertEqual(len(attestation["canonical_payload_digest"]), 64)
        self.assertEqual(len(attestation["hmac_signature"]), 64)

    def test_merkle_tree_construction_and_root(self):
        records = [
            {"id": "r1", "credits": 3, "grade": "A+"},
            {"id": "r2", "credits": 4, "grade": "A"},
            {"id": "r3", "credits": 3, "grade": "A-"},
        ]
        tree = self.merkle_service.build_merkle_tree("inst_buet", records)
        self.assertEqual(tree["total_leaves"], 3)
        self.assertTrue(tree["tree_depth"] >= 2)
        self.assertEqual(len(tree["merkle_root"]), 64)

    def test_merkle_proof_verification_valid_and_invalid(self):
        records = [
            {"id": "tx1", "val": 100},
            {"id": "tx2", "val": 200},
            {"id": "tx3", "val": 300},
            {"id": "tx4", "val": 400},
        ]
        tree = self.merkle_service.build_merkle_tree("inst_du", records)
        leaves = tree["leaf_hashes"]
        root = tree["merkle_root"]

        # Generate proof for index 1 (tx2)
        proof = self.merkle_service.generate_merkle_proof(1, leaves)
        self.assertTrue(len(proof) > 0)

        # Verify valid proof
        v_res = self.merkle_service.verify_merkle_proof(root, leaves[1], proof)
        self.assertTrue(v_res["is_valid"])
        self.assertEqual(v_res["verdict"], "PROOF_VERIFIED_VALID")

        # Verify invalid proof (tampered leaf)
        v_invalid = self.merkle_service.verify_merkle_proof(root, "0" * 64, proof)
        self.assertFalse(v_invalid["is_valid"])
        self.assertEqual(v_invalid["verdict"], "PROOF_INVALID_TAMPER_DETECTED")

    def test_row_tamper_detection_pinpoints_mutations(self):
        original_payload = {"student_id": "stu_99", "gpa": 3.80, "status": "enrolled"}
        attestation = self.merkle_service.generate_row_attestation(
            record_id="rec_99",
            tenant_id="inst_buet",
            entity_type="transcript",
            payload=original_payload
        )
        attestation["payload"] = original_payload

        # Untampered
        res_clean = self.merkle_service.detect_row_tampering(attestation, original_payload)
        self.assertFalse(res_clean["tampered"])
        self.assertEqual(res_clean["verdict"], "RECORD_PRISTINE_INTEGRITY")

        # Tampered GPA (e.g. fraudulent grade boost)
        tampered_payload = {"student_id": "stu_99", "gpa": 4.00, "status": "enrolled"}
        res_tampered = self.merkle_service.detect_row_tampering(attestation, tampered_payload)
        self.assertTrue(res_tampered["tampered"])
        self.assertEqual(res_tampered["verdict"], "CRITICAL_TAMPER_DETECTED")
        self.assertEqual(len(res_tampered["mutated_fields"]), 1)
        self.assertEqual(res_tampered["mutated_fields"][0]["field"], "gpa")
        self.assertEqual(res_tampered["mutated_fields"][0]["original_value"], 3.80)
        self.assertEqual(res_tampered["mutated_fields"][0]["tampered_value"], 4.00)

    # --- T003: Cross-Region CDC Replication Tests ---
    def test_cdc_event_processing_and_dlq(self):
        # Valid region
        res = self.cdc_service.decode_and_process_event(
            event_id="evt_01",
            region_origin="region_dhaka",
            table_name="students",
            operation="INSERT",
            row_data={"name": "Rahim"},
            vector_clock={"region_dhaka": 1},
            commit_lsn="16/3400A120"
        )
        self.assertEqual(res["status"], "APPLIED_REPLICATED")
        self.assertEqual(res["winning_region"], "region_dhaka")

        # Invalid region -> DLQ quarantine
        res_bad = self.cdc_service.decode_and_process_event(
            event_id="evt_02",
            region_origin="region_mars_colony",
            table_name="students",
            operation="INSERT",
            row_data={"name": "Unknown"},
            vector_clock={"region_mars": 1},
            commit_lsn="16/00000000"
        )
        self.assertEqual(res_bad["status"], "QUARANTINED_DLQ")
        self.assertEqual(len(self.cdc_service._dlq_quarantine), 1)

    def test_cdc_vector_clock_dominance(self):
        clock_a = {"region_dhaka": 2, "region_chittagong": 1}
        clock_b = {"region_dhaka": 1, "region_chittagong": 1}
        self.assertEqual(self.cdc_service.compare_vector_clocks(clock_a, clock_b), "A_GREATER")
        self.assertEqual(self.cdc_service.compare_vector_clocks(clock_b, clock_a), "B_GREATER")

        clock_c = {"region_dhaka": 2, "region_chittagong": 0}
        clock_d = {"region_dhaka": 1, "region_chittagong": 1}
        self.assertEqual(self.cdc_service.compare_vector_clocks(clock_c, clock_d), "CONCURRENT")

    def test_cdc_conflict_resolution_lww(self):
        local_rec = {
            "row_data": {"title": "Local Title"},
            "vector_clock": {"region_dhaka": 2, "region_chittagong": 0},
            "timestamp": 100.0,
            "region_origin": "region_dhaka"
        }
        incoming_evt = {
            "row_data": {"title": "Incoming Title"},
            "vector_clock": {"region_dhaka": 0, "region_chittagong": 2},
            "timestamp": 105.0,  # Later timestamp
            "region_origin": "region_chittagong"
        }
        res = self.cdc_service.resolve_replication_conflict(local_rec, incoming_evt)
        self.assertTrue(res["conflict_detected"])
        self.assertEqual(res["winner"], "INCOMING")
        self.assertEqual(res["active_data"]["title"], "Incoming Title")

    def test_cdc_replication_slot_lag_sla(self):
        lag_report = self.cdc_service.get_replication_slot_lag(
            slot_name="sub_chittagong_dr_slot",
            source_region="region_dhaka",
            target_region="region_chittagong",
            current_lsn="16/3400A120",
            confirmed_flush_lsn="16/3400A000"
        )
        self.assertIn("byte_lag", lag_report)
        self.assertIn("sla_status", lag_report)
        self.assertEqual(lag_report["sla_status"], "SLA_COMPLIANT_ACTIVE")


if __name__ == "__main__":
    unittest.main()
