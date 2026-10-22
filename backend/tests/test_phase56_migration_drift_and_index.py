"""
Unit tests for Phase 56: Production Schema Migration, Drift Guard & Index Optimizer.
"""

import unittest
from backend.app.services.schema_migration_engine_service import SchemaMigrationEngineService
from backend.app.services.schema_drift_detector_service import SchemaDriftDetectorService
from backend.app.services.index_optimizer_advisor_service import IndexOptimizerAdvisorService


class TestPhase56MigrationDriftAndIndex(unittest.TestCase):

    def setUp(self):
        self.migration_service = SchemaMigrationEngineService()
        self.drift_service = SchemaDriftDetectorService()
        self.index_service = IndexOptimizerAdvisorService()

    # --- T001: Schema Migration Engine Tests ---
    def test_safe_add_column_migration(self):
        res = self.migration_service.analyze_migration_safety(
            version_id="20261015_04",
            migration_name="add_student_bio",
            target_table="students",
            operation_type="ADD_COLUMN",
            column_definitions=[{"name": "bio", "type": "TEXT", "default": "''"}]
        )
        self.assertTrue(res["safe_to_apply"])
        self.assertEqual(res["safety_verdict"], "ZERO_DOWNTIME_APPROVED")
        self.assertIn("lock_timeout = '2s'", res["forward_sql"])
        self.assertIn("ALTER TABLE students ADD COLUMN IF NOT EXISTS bio TEXT DEFAULT ''", res["forward_sql"])
        self.assertIn("ALTER TABLE students DROP COLUMN IF EXISTS bio", res["rollback_sql"])

    def test_dangerous_drop_table_blocked(self):
        res = self.migration_service.analyze_migration_safety(
            version_id="20261015_05",
            migration_name="drop_quiz_table",
            target_table="quiz_attempts",
            operation_type="DROP_TABLE"
        )
        self.assertFalse(res["safe_to_apply"])
        self.assertEqual(res["safety_verdict"], "DANGEROUS_OPERATION_BLOCKED")
        self.assertEqual(res["risk_score"], 100)
        self.assertIn("DROP_TABLE_PROHIBITED", res["warnings"][0])

    def test_blocking_index_warned(self):
        res = self.migration_service.analyze_migration_safety(
            version_id="20261015_06",
            migration_name="raw_blocking_index",
            target_table="students",
            operation_type="CUSTOM",
            raw_ddl_forward="CREATE INDEX idx_student_email ON students(email);"
        )
        self.assertFalse(res["safe_to_apply"])
        self.assertTrue(any("BLOCKING_INDEX_LOCK" in w for w in res["warnings"]))

    def test_migration_history_ledger(self):
        history_before = self.migration_service.get_migration_history()
        count_before = len(history_before)

        apply_res = self.migration_service.apply_migration(
            version_id="20261015_07",
            migration_name="add_admission_weights_v2"
        )
        self.assertTrue(apply_res["applied"])
        history_after = self.migration_service.get_migration_history()
        self.assertEqual(len(history_after), count_before + 1)
        self.assertEqual(history_after[-1]["version_id"], "20261015_07")

    # --- T002: Schema Drift Detector Tests ---
    def test_schema_drift_detection_parity(self):
        declared = {
            "tables": {
                "transcripts": {
                    "columns": {"id": "UUID", "student_id": "VARCHAR", "gpa": "NUMERIC"},
                    "indexes": ["idx_transcripts_student"]
                }
            }
        }
        res = self.drift_service.detect_schema_drift("production", declared, declared)
        self.assertFalse(res["drift_detected"])
        self.assertEqual(res["parity_status"], "PARITY_SYNCHRONIZED")
        self.assertEqual(res["declared_manifest_digest"], res["live_manifest_digest"])
        self.assertEqual(len(res["drift_details"]), 0)

    def test_schema_drift_detection_missing_table_and_column(self):
        declared = {
            "tables": {
                "scholarships": {
                    "columns": {"id": "UUID", "amount": "NUMERIC", "grantee_id": "VARCHAR"},
                    "indexes": ["idx_scholarships_grantee"]
                }
            }
        }
        live = {"tables": {}}  # Table missing in live
        res = self.drift_service.detect_schema_drift("staging", declared, live)
        self.assertTrue(res["drift_detected"])
        self.assertEqual(res["parity_status"], "DRIFT_ALERT_REMEDIATION_REQUIRED")
        self.assertEqual(res["drift_details"][0]["drift_type"], "MISSING_TABLE")
        self.assertIn("CREATE TABLE IF NOT EXISTS scholarships", res["remediation_sql"])

    def test_schema_drift_detection_type_mutation(self):
        declared = {
            "tables": {
                "exams": {"columns": {"max_score": "INTEGER"}}
            }
        }
        live = {
            "tables": {
                "exams": {"columns": {"max_score": "VARCHAR"}}
            }
        }
        res = self.drift_service.detect_schema_drift("production", declared, live)
        self.assertTrue(res["drift_detected"])
        self.assertEqual(res["drift_details"][0]["drift_type"], "COLUMN_TYPE_MUTATION")

    # --- T003: Index Optimizer Advisor Tests ---
    def test_index_recommendation_high_selectivity(self):
        res = self.index_service.recommend_index(
            table_name="students",
            query_clause="department = 'CSE' AND batch = 2024",
            filter_columns=["department", "batch"],
            sort_columns=["created_at"],
            table_row_count=100000,
            estimated_matched_rows=150
        )
        self.assertEqual(res["index_type"], "COMPOSITE_BTREE_HIGH_SELECTIVITY")
        self.assertTrue(res["selectivity"] <= 0.01)
        self.assertIn("CREATE INDEX CONCURRENTLY IF NOT EXISTS", res["create_index_sql"])
        self.assertIn("idx_students_department_batch_created_at", res["recommended_index_name"])
        self.assertEqual(res["lock_safety"], "NON_BLOCKING_CONCURRENT")

    def test_index_recommendation_partial_filter(self):
        res = self.index_service.recommend_index(
            table_name="questions",
            query_clause="subject_id = 'math_01' AND status = 'published'",
            filter_columns=["subject_id"],
            sort_columns=[],
            table_row_count=50000,
            estimated_matched_rows=100
        )
        self.assertEqual(res["index_type"], "PARTIAL_FILTERED_BTREE")
        self.assertIn("WHERE status = 'published'", res["create_index_sql"])

    def test_index_redundancy_prefix_detection(self):
        mock_indexes = [
            {"name": "idx_a", "table": "users", "columns": ["email"]},
            {"name": "idx_b", "table": "users", "columns": ["email", "status"]},
            {"name": "idx_c", "table": "users", "columns": ["phone"]},
        ]
        res = self.index_service.scan_redundant_indexes(mock_indexes)
        self.assertEqual(res["total_indexes_scanned"], 3)
        self.assertEqual(res["redundant_indexes_found"], 1)
        self.assertEqual(res["redundancies"][0]["redundant_index"], "idx_a")
        self.assertEqual(res["redundancies"][0]["covered_by"], "idx_b")
        self.assertIn("DROP INDEX CONCURRENTLY IF EXISTS idx_a", res["redundancies"][0]["recommendation"])


if __name__ == "__main__":
    unittest.main()
