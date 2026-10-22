import unittest
from backend.app.services.connection_pooler_hygiene_service import ConnectionPoolerHygieneService
from backend.app.services.dynamic_data_masking_service import DynamicDataMaskingService
from backend.app.services.federated_fdw_security_service import FederatedFdwSecurityService


class TestPhase53PoolerMaskingAndFdw(unittest.TestCase):
    """
    Comprehensive Automated Unit Tests for Phase 53:
    - Connection Pooler Session State Hygiene
    - Role-Based Dynamic Data Masking & Inference Risk
    - Federated FDW Remote Server Security & Query Sanitizer
    """

    def setUp(self):
        self.pooler_service = ConnectionPoolerHygieneService()
        self.masking_service = DynamicDataMaskingService()
        self.fdw_service = FederatedFdwSecurityService()

    # --- Connection Pooler Hygiene Tests ---

    def test_01_pooler_hygiene_clean_session(self):
        clean_stmts = [
            "BEGIN;",
            "SET LOCAL search_path = public, campus_app;",
            "SELECT * FROM students WHERE id = 's_1001';",
            "COMMIT;"
        ]
        res = self.pooler_service.audit_session_hygiene(clean_stmts)
        self.assertTrue(res["is_hygienic"])
        self.assertEqual(res["violations_detected"], 0)
        self.assertEqual(res["risk_score"], 0.0)

    def test_02_pooler_hygiene_polluting_guc_and_patch(self):
        dirty_stmts = [
            "SET search_path = malicious_schema;",
            "LISTEN audit_channel;",
            "CREATE TEMP TABLE dirty_cache (val text);"
        ]
        res = self.pooler_service.audit_session_hygiene(dirty_stmts)
        self.assertFalse(res["is_hygienic"])
        self.assertGreaterEqual(res["violations_detected"], 3)
        self.assertGreaterEqual(res["risk_score"], 40.0)

        # Check automated localized patch
        patch = res["safe_sql_patch"]
        self.assertIn("SET LOCAL search_path = malicious_schema", patch)
        self.assertIn("ON COMMIT DROP", patch)

    def test_03_pooler_reset_guard_verification(self):
        clean_meta = {
            "reset_query": "DISCARD ALL;",
            "active_advisory_locks": 0,
            "has_temp_schemas": False,
            "gucs_restored": True
        }
        res_clean = self.pooler_service.verify_pool_reset_guard(clean_meta)
        self.assertTrue(res_clean["reset_verified"])
        self.assertEqual(res_clean["status"], "PRISTINE")

        dirty_meta = {
            "reset_query": "SELECT 1;",  # Missing DISCARD ALL
            "active_advisory_locks": 2,
            "has_temp_schemas": True,
            "gucs_restored": False
        }
        res_dirty = self.pooler_service.verify_pool_reset_guard(dirty_meta)
        self.assertFalse(res_dirty["reset_verified"])
        self.assertEqual(res_dirty["status"], "CONTAMINATED")
        self.assertGreaterEqual(len(res_dirty["issues"]), 3)

    def test_04_pooler_isolation_benchmark(self):
        bench = self.pooler_service.simulate_pool_isolation_benchmark(concurrent_tenants=5, total_transactions=30)
        self.assertEqual(bench["isolation_pass_rate"], 100.0)
        self.assertGreater(bench["prevented_contaminations"], 0)
        self.assertEqual(bench["benchmark_status"], "EXEMPLARY_ISOLATION")

    # --- Dynamic Data Masking Tests ---

    def test_05_dynamic_masking_student_role(self):
        raw_record = {
            "id": "std_101",
            "full_name": "Rahim Ahmed",
            "email": "rahim.ahmed@univ.edu",
            "phone": "+8801712345678",
            "national_id": "19952691234567890",
            "gpa": 3.88,
            "scholarship_amount": 25000.0
        }
        masked = self.masking_service.mask_student_record(raw_record, viewer_role="student")
        rec = masked["masked_record"]

        self.assertEqual(rec["email"], "r*********d@univ.edu")
        self.assertIn("****", rec["phone"])
        self.assertIn("******", rec["national_id"])
        self.assertEqual(rec["gpa"], "3.75 - 4.00 (First Class Honors)")
        self.assertEqual(rec["scholarship_amount"], "[REDACTED_FINANCIAL_AID]")
        self.assertTrue(masked["watermark"].startswith("wm_v53_"))

    def test_06_dynamic_masking_faculty_and_admin_roles(self):
        raw_record = {
            "id": "std_102",
            "full_name": "Karim Uddin",
            "email": "karim@univ.edu",
            "phone": "+8801812345678",
            "national_id": "19962691234567890",
            "gpa": 3.65,
            "scholarship_amount": 10000.0
        }
        # Faculty role: GPA and email are unmasked, phone and NID remain masked
        fac_res = self.masking_service.mask_student_record(raw_record, viewer_role="faculty")
        fac_rec = fac_res["masked_record"]
        self.assertEqual(fac_rec["email"], "karim@univ.edu")
        self.assertEqual(fac_rec["gpa"], 3.65)
        self.assertIn("****", fac_rec["phone"])

        # Dean role: everything unmasked
        dean_res = self.masking_service.mask_student_record(raw_record, viewer_role="academic_dean")
        dean_rec = dean_res["masked_record"]
        self.assertEqual(dean_rec["phone"], "+8801812345678")
        self.assertEqual(dean_rec["national_id"], "19962691234567890")
        self.assertEqual(dean_rec["scholarship_amount"], 10000.0)

    def test_07_masked_view_sql_and_inference_risk(self):
        sql = self.masking_service.generate_masked_view_sql(table_name="students", view_name="v_masked_students")
        self.assertIn("CREATE OR REPLACE VIEW public.v_masked_students", sql)
        self.assertIn("security_barrier = true", sql)
        self.assertIn("auth.role()", sql)

        dataset = [
            {"department": "CSE", "batch": "2024", "district": "Dhaka"},
            {"department": "CSE", "batch": "2024", "district": "Dhaka"},
            {"department": "EEE", "batch": "2023", "district": "Sylhet"},
        ]
        risk = self.masking_service.evaluate_inference_risk(dataset, masked_columns=["department", "batch", "district"])
        self.assertEqual(risk["records_evaluated"], 3)
        self.assertGreaterEqual(risk["re_identification_risk_percent"], 30.0)

    # --- Federated FDW Security Tests ---

    def test_08_fdw_server_definition_audit(self):
        compliant_cfg = {
            "server_name": "buet_academic_cluster",
            "options": {
                "host": "buet-db.internal",
                "port": "5432",
                "dbname": "credit_transfers",
                "sslmode": "require",
                "connect_timeout": "5"
            }
        }
        res_comp = self.fdw_service.audit_fdw_server_definition(compliant_cfg)
        self.assertTrue(res_comp["compliant"])
        self.assertEqual(res_comp["risk_score"], 0.0)

        insecure_cfg = {
            "server_name": "unencrypted_campus_node",
            "options": {
                "host": "untrusted.external.org",
                "sslmode": "disable",
                "connect_timeout": "30",
                "updatable": "true"
            }
        }
        res_insec = self.fdw_service.audit_fdw_server_definition(insecure_cfg)
        self.assertFalse(res_comp["compliant"] is False)
        self.assertFalse(res_insec["compliant"])
        self.assertGreaterEqual(res_insec["risk_score"], 50.0)

    def test_09_fdw_user_mappings_privilege_scan(self):
        mappings = [
            {
                "local_user": "anon",
                "remote_user": "remote_readonly",
                "server_name": "partner_univ_node"
            },
            {
                "local_user": "student",
                "remote_user": "postgres",  # Remote superuser overprivilege
                "server_name": "partner_univ_node"
            },
            {
                "local_user": "faculty",
                "remote_user": "academic_user",
                "server_name": "partner_univ_node",
                "options": {"password": "secret_in_plaintext"}
            }
        ]
        res = self.fdw_service.validate_user_mapping_permissions(mappings)
        self.assertFalse(res["is_secure"])
        self.assertEqual(res["violations_detected"], 3)
        hazards = [v["hazard"] for v in res["violations"]]
        self.assertIn("ANONYMOUS_ROLE_REMOTE_MAPPING", hazards)
        self.assertIn("REMOTE_SUPERUSER_OVERPRIVILEGE", hazards)
        self.assertIn("PLAINTEXT_PASSWORD_IN_MAPPING", hazards)

    def test_10_federated_query_sanitizer(self):
        valid_query = "SELECT student_id, course_code, grade FROM credit_transfer.transcripts WHERE approved = true;"
        res_valid = self.fdw_service.sanitize_federated_query(valid_query)
        self.assertTrue(res_valid["allowed"])
        self.assertEqual(res_valid["target_schema"], "credit_transfer")

        # Stacked SQL attack
        stacked_attack = "SELECT 1 FROM credit_transfer.transcripts; DROP TABLE public.users;"
        res_stacked = self.fdw_service.sanitize_federated_query(stacked_attack)
        self.assertFalse(res_stacked["allowed"])
        self.assertEqual(res_stacked["security_flag"], "STACKED_SQL_INJECTION_BLOCKED")

        # Schema traversal into pg_catalog
        catalog_attack = "SELECT usename, passwd FROM pg_catalog.pg_shadow;"
        res_catalog = self.fdw_service.sanitize_federated_query(catalog_attack)
        self.assertFalse(res_catalog["allowed"])
        self.assertEqual(res_catalog["security_flag"], "RESTRICTED_SCHEMA_TRAVERSAL_BLOCKED")


if __name__ == "__main__":
    unittest.main()
