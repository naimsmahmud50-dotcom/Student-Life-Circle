import unittest
from backend.app.services.disaster_recovery_pitr_simulator_service import DisasterRecoveryPitrSimulatorService
from backend.app.services.secret_rotation_vault_service import SecretRotationVaultService
from backend.app.services.wal_archive_integrity_service import WalArchiveIntegrityService


class TestPhase54PitrVaultAndWal(unittest.TestCase):
    """
    Comprehensive Automated Unit Tests for Phase 54:
    - Automated PITR Disaster Recovery & Consistency Checks
    - Dynamic Secret Rotation Vault & Entropy Leak Scanner
    - Write-Ahead Log (WAL) Archive Continuity & SLA Lag Validator
    """

    def setUp(self):
        self.pitr_service = DisasterRecoveryPitrSimulatorService()
        self.vault_service = SecretRotationVaultService()
        self.wal_service = WalArchiveIntegrityService()

    # --- PITR Disaster Recovery Tests ---

    def test_01_pitr_snapshot_creation(self):
        tables = {
            "students": {"count": 1000, "digest": "hash_abc1"},
            "transcripts": {"count": 5000, "digest": "hash_abc2"}
        }
        snap = self.pitr_service.create_pitr_snapshot(
            target_epoch=1729000000,
            snapshot_tag="test_pre_exam_release",
            table_manifests=tables
        )
        self.assertEqual(snap["status"], "VERIFIED_READY")
        self.assertTrue(snap["basebackup_lsn"].startswith("16/"))
        self.assertTrue(len(snap["manifest_digest"]) == 64)

    def test_02_pitr_recovery_drill_simulation(self):
        # Baseline snapshot exists in registry
        drill = self.pitr_service.simulate_recovery_drill(
            snapshot_id="snap_prod_base_001",
            disaster_scenario="accidental_drop_table"
        )
        self.assertTrue(drill["success"])
        self.assertEqual(drill["status"], "PITR_RESTORE_DRILL_PASSED")
        self.assertTrue(drill["rpo_compliant"])
        self.assertTrue(drill["rto_compliant"])
        self.assertLessEqual(drill["rpo_seconds"], 60)
        self.assertLessEqual(drill["rto_seconds"], 900)

    def test_03_pitr_restore_consistency_verification(self):
        orig = {
            "students": {"count": 14250, "digest": "d_101"},
            "transcripts": {"count": 98400, "digest": "d_102"}
        }
        # Matching restored dataset
        res_match = self.pitr_service.verify_restore_consistency(orig, orig)
        self.assertTrue(res_match["is_consistent"])
        self.assertEqual(res_match["data_loss_percentage"], 0.0)
        self.assertEqual(res_match["integrity_verdict"], "ZERO_DATA_LOSS_VERIFIED")

        # Corrupted / drifted restored dataset
        corrupted = {
            "students": {"count": 14250, "digest": "d_101"},
            "transcripts": {"count": 97000, "digest": "d_corrupt_diff"}  # 1400 records lost
        }
        res_drift = self.pitr_service.verify_restore_consistency(orig, corrupted)
        self.assertFalse(res_drift["is_consistent"])
        self.assertGreater(res_drift["data_loss_percentage"], 0.0)
        self.assertEqual(res_drift["integrity_verdict"], "INTEGRITY_DRIFT_DETECTED")

    # --- Secret Rotation Vault Tests ---

    def test_04_secret_leak_scanner_detection(self):
        leaked_bundle = """
        const config = {
          supabaseUrl: "https://demo.supabase.co",
          secretKey: "sb_secret_exposed_super_privilege_key_12345678",
          databaseUri: "postgresql://postgres:p@ssword123@db.internal:5432/campus"
        };
        """
        scan = self.vault_service.scan_client_bundle_for_secrets(leaked_bundle)
        self.assertFalse(scan["is_safe"])
        self.assertTrue(scan["has_critical_leak"])
        self.assertGreaterEqual(scan["total_leaks_found"], 2)

        types = [f["leak_type"] for f in scan["findings"]]
        self.assertIn("SUPABASE_SECRET_SERVICE_ROLE_KEY", types)
        self.assertIn("DATABASE_CONNECTION_URI_WITH_PLAINTEXT_PASSWORD", types)

    def test_05_secret_leak_scanner_clean_bundle(self):
        clean_bundle = """
        const config = {
          supabaseUrl: "https://demo.supabase.co",
          anonKey: "sb_publishable_client_token_safe_for_browsers"
        };
        console.log("Welcome to Student Life Circle");
        """
        scan = self.vault_service.scan_client_bundle_for_secrets(clean_bundle)
        self.assertTrue(scan["is_safe"])
        self.assertFalse(scan["has_critical_leak"])
        self.assertEqual(scan["total_leaks_found"], 0)

    def test_06_zero_downtime_key_rotation(self):
        rot = self.vault_service.execute_zero_downtime_key_rotation(
            key_type="service_role", grace_period_seconds=300
        )
        self.assertEqual(rot["status"], "ROTATION_ACTIVE_IN_GRACE")
        self.assertIsNotNone(rot["active_key_id"])
        self.assertIsNotNone(rot["deprecating_key_id"])

        # Active key must be valid
        val_active = self.vault_service.is_key_valid(rot["active_key_id"])
        self.assertTrue(val_active["valid"])
        self.assertEqual(val_active["status"], "ACTIVE")

        # Deprecating key must be valid within grace window
        val_deprecating = self.vault_service.is_key_valid(rot["deprecating_key_id"])
        self.assertTrue(val_deprecating["valid"])
        self.assertEqual(val_deprecating["status"], "DEPRECATING")

    def test_07_immediate_key_revocation(self):
        key_id = "key_srv_active_01"
        rev = self.vault_service.revoke_compromised_credential(key_id, reason="Exposed in public commit")
        self.assertEqual(rev["status"], "REVOKED_BLACKLISTED")

        val = self.vault_service.is_key_valid(key_id)
        self.assertFalse(val["valid"])
        self.assertEqual(val["status"], "REVOKED")

    # --- WAL Archive Integrity Tests ---

    def test_08_wal_archive_continuous_chain(self):
        # Seeded chain has 4 sequential segments
        ver = self.wal_service.verify_wal_chain_continuity()
        self.assertTrue(ver["is_continuous"])
        self.assertEqual(ver["missing_segments_count"], 0)
        self.assertEqual(ver["status"], "ARCHIVE_CHAIN_PRISTINE")

    def test_09_wal_archive_detects_gap(self):
        # Register segment 6 without segment 5 (gap)
        seg_6_name = self.wal_service.format_segment_name(timeline_id=1, log_id=0, seg_id=6)
        reg = self.wal_service.register_wal_segment(
            segment_name=seg_6_name,
            timeline_id=1,
            segment_number=6,
            checksum="chk_segment_6"
        )
        self.assertTrue(reg["accepted"])

        ver_broken = self.wal_service.verify_wal_chain_continuity()
        self.assertFalse(ver_broken["is_continuous"])
        self.assertGreater(ver_broken["missing_segments_count"], 0)
        self.assertEqual(ver_broken["status"], "ARCHIVE_CHAIN_BROKEN_GAPS_DETECTED")
        expected_missing = self.wal_service.format_segment_name(timeline_id=1, log_id=0, seg_id=5)
        self.assertIn(expected_missing, ver_broken["missing_segments"])

    def test_10_wal_archive_lag_and_sla(self):
        lag_res = self.wal_service.evaluate_archive_lag_and_sla(max_lag_seconds=600)
        self.assertTrue(lag_res["sla_met"])
        self.assertGreater(lag_res["total_archived_mb"], 0)
        self.assertEqual(lag_res["status"], "OPTIMAL_ARCHIVE_SLA")


if __name__ == "__main__":
    unittest.main()
