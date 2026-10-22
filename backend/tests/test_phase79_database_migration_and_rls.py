# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 79 - Database Migration & Supabase RLS Tests):
# Automated verification test suite for Phase 79: Live Database Migration & Supabase RLS Hardening.
# Verifies:
# 1. 001_core_supabase_schema.sql: DDL statements, tables, append-only trigger, and indices.
# 2. 002_rls_security_policies.sql: Zero-IDOR, tenant isolation, minor protection, audit immutability.
# 3. DatabaseSessionManager: Connection pool settings, async session execution, health diagnostics.
# 4. ORM Models: UserModel, ProfileModel, QuizAttemptModel, TuitionApplicationModel, AuditLogModel.
# 5. CacheService: Asynchronous Redis / LRU in-memory query cache, TTL expiry, pattern eviction.
# 6. LiveQueryService: Hot endpoint caching, Zero-IDOR blocking, minor profile masking, and audit logging.
# 7. Strict Zero-Emoji Policy: Enforces zero-emoji governance across all Phase 79 artifacts.
# ==============================================================================

import os
import unittest
import asyncio
from backend.app.db.session import DatabaseSessionManager, db_manager
from backend.app.db.models import (
    UserModel,
    ProfileModel,
    QuestionItemModel,
    QuizAttemptModel,
    TuitionApplicationModel,
    AuditLogModel
)
from backend.app.services.cache_service import CacheService
from backend.app.services.live_query_service import LiveQueryService


class TestPhase79DatabaseMigrationAndRLS(unittest.TestCase):

    def setUp(self):
        self.migrations_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "migrations"
        )
        self.cache_service = CacheService()
        self.live_query_service = LiveQueryService()

    # --------------------------------------------------------------------------
    # 1. DDL Schema Verification
    # --------------------------------------------------------------------------
    def test_migration_001_ddl_syntax_and_tables(self):
        file_path = os.path.join(self.migrations_dir, "001_core_supabase_schema.sql")
        self.assertTrue(os.path.exists(file_path), "001_core_supabase_schema.sql must exist")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check required tables
        required_tables = [
            "public.users",
            "public.profiles",
            "public.question_items",
            "public.quiz_attempts",
            "public.exam_submissions",
            "public.tuition_applications",
            "public.escrow_vaults",
            "public.verifiable_credentials",
            "public.audit_logs"
        ]
        for tbl in required_tables:
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {tbl}", content, f"Missing table {tbl}")

        # Check append-only immutability trigger
        self.assertIn("reject_audit_log_mutation()", content)
        self.assertIn("trg_prevent_audit_log_mutation", content)
        self.assertIn("BEFORE UPDATE OR DELETE ON public.audit_logs", content)

        # Check required indices
        self.assertIn("idx_profiles_user_tenant", content)
        self.assertIn("idx_profiles_minor_privacy", content)
        self.assertIn("idx_quiz_attempts_user", content)
        self.assertIn("idx_audit_logs_tenant_ts", content)

    # --------------------------------------------------------------------------
    # 2. RLS Security Policies Verification
    # --------------------------------------------------------------------------
    def test_migration_002_rls_policies_coverage(self):
        file_path = os.path.join(self.migrations_dir, "002_rls_security_policies.sql")
        self.assertTrue(os.path.exists(file_path), "002_rls_security_policies.sql must exist")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check RLS enabled and forced on key tables
        tables = [
            "public.users",
            "public.profiles",
            "public.question_items",
            "public.quiz_attempts",
            "public.exam_submissions",
            "public.tuition_applications",
            "public.escrow_vaults",
            "public.verifiable_credentials",
            "public.audit_logs"
        ]
        for tbl in tables:
            self.assertIn(f"ALTER TABLE {tbl} ENABLE ROW LEVEL SECURITY", content)
            self.assertIn(f"ALTER TABLE {tbl} FORCE ROW LEVEL SECURITY", content)

        # Child minor protection check
        self.assertIn("is_minor = TRUE", content)
        self.assertIn("guardian_consent_granted = TRUE", content)

        # Audit logs immutability check
        self.assertIn("REVOKE UPDATE, DELETE ON public.audit_logs", content)
        self.assertIn("audit_logs_append_only_insert", content)

    # --------------------------------------------------------------------------
    # 3. Database Session Manager & Health Check
    # --------------------------------------------------------------------------
    def test_database_session_manager_and_health_check(self):
        async def run_check():
            health = await db_manager.check_database_health()
            self.assertIn(health["status"], ("HEALTHY", "DEGRADED"))
            self.assertIn("latency_ms", health)
            self.assertIn("pool", health)
            self.assertEqual(health["pool"]["configured_pool_size"], 10)
            self.assertEqual(health["pool"]["configured_max_overflow"], 20)

            # Test session checkout
            sessions_count = 0
            async for session in db_manager.get_session():
                self.assertTrue(hasattr(session, "execute"))
                self.assertTrue(hasattr(session, "commit"))
                self.assertTrue(hasattr(session, "rollback"))
                res = await session.execute("SELECT 1")
                self.assertIsNotNone(res)
                sessions_count += 1
                break
            self.assertEqual(sessions_count, 1)

        asyncio.run(run_check())

    # --------------------------------------------------------------------------
    # 4. ORM Models Schema Parity
    # --------------------------------------------------------------------------
    def test_db_orm_models_schema_parity(self):
        user = UserModel(email="student@nctb.gov.bd", role="student")
        self.assertEqual(user.email, "student@nctb.gov.bd")

        profile = ProfileModel(
            user_id=user.id,
            full_name="Fatima Begum",
            is_minor=True,
            guardian_consent_granted=False
        )
        self.assertTrue(profile.is_minor)
        self.assertFalse(profile.guardian_consent_granted)

        quiz_attempt = QuizAttemptModel(
            user_id=user.id,
            tenant_id="tenant_chittagong",
            quiz_id="quiz_phys_01",
            score=85.0
        )
        self.assertEqual(quiz_attempt.score, 85.0)

        audit_log = AuditLogModel(
            tenant_id="tenant_chittagong",
            user_id=user.id,
            action="LOGIN_ATTEMPT",
            entity_type="users",
            entity_id=str(user.id)
        )
        self.assertEqual(audit_log.action, "LOGIN_ATTEMPT")

    # --------------------------------------------------------------------------
    # 5. Redis / In-Memory Query Cache Service
    # --------------------------------------------------------------------------
    def test_redis_query_cache_service_and_ttl(self):
        async def run_cache_test():
            await self.cache_service.flush_all()

            # Set and Get
            await self.cache_service.set("test_key_1", {"data": "verified_content"}, ttl=10)
            val = await self.cache_service.get("test_key_1")
            self.assertEqual(val, {"data": "verified_content"})

            # Delete pattern
            await self.cache_service.set("question_bank:hsc:01", {"id": 1}, ttl=10)
            await self.cache_service.set("question_bank:hsc:02", {"id": 2}, ttl=10)
            deleted_count = await self.cache_service.delete_pattern("question_bank:*")
            self.assertEqual(deleted_count, 2)

            # Telemetry stats
            stats = self.cache_service.get_stats()
            self.assertGreaterEqual(stats["hits"], 1)
            self.assertIn("backend", stats)

        asyncio.run(run_cache_test())

    # --------------------------------------------------------------------------
    # 6. Live Query Hot Endpoints Caching
    # --------------------------------------------------------------------------
    def test_live_query_hot_endpoints_caching(self):
        async def run_hot_endpoints_test():
            # First fetch (cache miss)
            questions_1 = await self.live_query_service.get_hot_question_bank()
            self.assertGreater(len(questions_1), 0)

            # Second fetch (cache hit)
            questions_2 = await self.live_query_service.get_hot_question_bank()
            self.assertEqual(len(questions_1), len(questions_2))

            # Admission circulars
            circulars = await self.live_query_service.get_admission_circulars()
            self.assertGreaterEqual(len(circulars), 3)

        asyncio.run(run_hot_endpoints_test())

    # --------------------------------------------------------------------------
    # 7. Zero-IDOR Quiz and Tuition Enforcement
    # --------------------------------------------------------------------------
    def test_zero_idor_quiz_and_tuition_enforcement(self):
        async def run_idor_test():
            # 1. Valid user submitting their own attempt
            valid_jwt = {"sub": "usr_student_alice", "role": "student", "tenant_id": "tenant_dhaka_01"}
            res = await self.live_query_service.record_quiz_attempt(
                user_id="usr_student_alice",
                tenant_id="tenant_dhaka_01",
                caller_jwt=valid_jwt,
                attempt_data={"quiz_id": "bp_du_unit_a", "score": 92.5}
            )
            self.assertEqual(res["verdict"], "RECORDED")
            self.assertEqual(res["status_code"], 201)

            # 2. Spoofed IDOR attempt: Bob tries to submit quiz for Alice
            attacker_jwt = {"sub": "usr_student_bob", "role": "student", "tenant_id": "tenant_dhaka_01"}
            res_idor = await self.live_query_service.record_quiz_attempt(
                user_id="usr_student_alice",
                tenant_id="tenant_dhaka_01",
                caller_jwt=attacker_jwt,
                attempt_data={"quiz_id": "bp_du_unit_a", "score": 10.0}
            )
            self.assertEqual(res_idor["verdict"], "DENIED")
            self.assertEqual(res_idor["error"], "ZERO_IDOR_VIOLATION")
            self.assertEqual(res_idor["status_code"], 403)

            # 3. Spoofed Tuition Application: Bob tries to create application for Alice
            res_tuition_idor = await self.live_query_service.create_tuition_application(
                student_user_id="usr_student_alice",
                tenant_id="tenant_dhaka_01",
                caller_jwt=attacker_jwt,
                application_data={"subject": "Physics"}
            )
            self.assertEqual(res_tuition_idor["verdict"], "DENIED")
            self.assertEqual(res_tuition_idor["status_code"], 403)

        asyncio.run(run_idor_test())

    # --------------------------------------------------------------------------
    # 8. Under-16 Minor Profile Masking Protection
    # --------------------------------------------------------------------------
    def test_under_16_minor_profile_masking(self):
        async def run_minor_masking_test():
            minor_id = "usr_minor_student_01"

            # 1. Minor accessing their own profile (Full profile returned)
            self_jwt = {"sub": minor_id, "role": "student", "tenant_id": "tenant_dhaka_01"}
            res_self = await self.live_query_service.get_learner_profile(minor_id, self_jwt)
            self.assertFalse(res_self["is_masked"])
            self.assertEqual(res_self["profile"]["phone"], "+8801700000001")

            # 2. Unverified general adult viewing minor (Sensitive fields masked)
            adult_jwt = {"sub": "usr_stranger_adult", "role": "student", "tenant_id": "tenant_dhaka_01"}
            res_masked = await self.live_query_service.get_learner_profile(minor_id, adult_jwt)
            self.assertTrue(res_masked["is_masked"])
            self.assertEqual(res_masked["profile"]["phone"], "[MASKED_UNDER_16_PROTECTION]")
            self.assertEqual(res_masked["profile"]["institution"], "[MASKED_UNDER_16_PROTECTION]")

            # 3. Verified institutional admin viewing minor (Full profile returned)
            admin_jwt = {"sub": "usr_admin", "role": "institutional_admin", "tenant_id": "tenant_dhaka_01"}
            res_admin = await self.live_query_service.get_learner_profile(minor_id, admin_jwt)
            self.assertFalse(res_admin["is_masked"])
            self.assertEqual(res_admin["profile"]["phone"], "+8801700000001")

        asyncio.run(run_minor_masking_test())

    # --------------------------------------------------------------------------
    # 9. Audit Log Immutability & Mutation Rejection
    # --------------------------------------------------------------------------
    def test_audit_log_append_only_and_mutation_rejection(self):
        async def run_audit_test():
            jwt = {"sub": "usr_admin", "role": "institutional_admin", "tenant_id": "tenant_dhaka_01"}

            # Simulated UPDATE attempt must be strictly rejected
            update_res = await self.live_query_service.attempt_audit_log_mutation("log_123", "UPDATE", jwt)
            self.assertEqual(update_res["verdict"], "MUTATION_PROHIBITED")
            self.assertEqual(update_res["error"], "AUDIT_LOG_IMMUTABLE")
            self.assertEqual(update_res["status_code"], 403)

            # Simulated DELETE attempt must be strictly rejected
            delete_res = await self.live_query_service.attempt_audit_log_mutation("log_123", "DELETE", jwt)
            self.assertEqual(delete_res["verdict"], "MUTATION_PROHIBITED")
            self.assertEqual(delete_res["status_code"], 403)

        asyncio.run(run_audit_test())

    # --------------------------------------------------------------------------
    # 10. Strict Zero-Emoji Governance
    # --------------------------------------------------------------------------
    def test_strict_zero_emoji_governance_across_phase79_files(self):
        files_to_check = [
            os.path.join(self.migrations_dir, "001_core_supabase_schema.sql"),
            os.path.join(self.migrations_dir, "002_rls_security_policies.sql"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "db", "session.py"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "db", "models.py"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "services", "cache_service.py"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "services", "live_query_service.py")
        ]

        def contains_emoji(text: str) -> bool:
            for char in text:
                cp = ord(char)
                if (0x1F600 <= cp <= 0x1F64F or
                    0x1F300 <= cp <= 0x1F5FF or
                    0x1F680 <= cp <= 0x1F6FF or
                    0x1F700 <= cp <= 0x1F77F or
                    0x1F780 <= cp <= 0x1F7FF or
                    0x1F800 <= cp <= 0x1F8FF or
                    0x1F900 <= cp <= 0x1F9FF or
                    0x1FA00 <= cp <= 0x1FA6F or
                    0x1FA70 <= cp <= 0x1FAFF or
                    0x2600 <= cp <= 0x26FF or
                    0x2700 <= cp <= 0x27BF):
                    return True
            return False

        for file_path in files_to_check:
            self.assertTrue(os.path.exists(file_path), f"File {file_path} must exist")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertFalse(contains_emoji(content), f"Emoji violation detected in {file_path}")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE", content, f"Missing Developer Note in {file_path}")


if __name__ == "__main__":
    unittest.main()
