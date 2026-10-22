"""
========================================================================================
MODULE:    Phase 14 Automated Test Suite - Enterprise Security & Offline Sync
TOPIC:     Rate Limiting, Security Headers, ASVS L2 Minor Masking & PWA Batch Sync
FILE:      backend/tests/test_phase14_security_and_offline_sync.py
PURPOSE:   Verifies all enterprise security and offline network resilience features:
           1. Anti-Brute-Force Rate Limiting (5 auth limit, 60 save limit, retry-after).
           2. Defense-in-Depth Security Headers (CSP, HSTS, X-Frame-Options DENY).
           3. ASVS L2 Minor Data Masking (top-level and nested PII protection).
           4. PWA Offline Practice Bundle Builder (tamper-resistant question delivery).
           5. Batch Offline Answer Sync (idempotent replay and duplicate handling).
           6. Async REST API Router endpoints for offline sync and security policies.
AUDIENCE:  Security Compliance Engineers, QA Automation Leads & Autonomous Test Runners
STANDARDS: Zero-Emoji Microcopy, ASVS L2 Child Privacy, 100% Deterministic Testing
========================================================================================
"""

import asyncio
import unittest
from backend.app.core.rate_limiter import SlidingWindowRateLimiter
from backend.app.core.security_headers import SecurityHeadersManager
from backend.app.services.offline_sync_service import OfflineSyncService
from backend.app.services.quiz_engine import QuizEngineService
from backend.app.schemas.quiz_schema import QuizMode
from backend.app.schemas.security_and_offline_schema import (
    OfflineSyncBatchRequest,
    SecurityProfileSanitizeRequest
)
from backend.app.api.v1.router import (
    sync_offline_batch,
    get_offline_manifest,
    get_security_policy,
    sanitize_minor_profile
)


class TestPhase14SecurityAndOfflineSync(unittest.TestCase):
    """
    Automated verification of security boundaries, rate limiters, and offline sync.
    """

    def setUp(self):
        self.rate_limiter = SlidingWindowRateLimiter()
        self.security_headers = SecurityHeadersManager()
        self.quiz_engine = QuizEngineService()
        self.offline_sync = OfflineSyncService()

    # -------------------------------------------------------------------------
    # 1. Rate Limiting Tests
    # -------------------------------------------------------------------------
    def test_auth_rate_limiting_enforcement(self):
        client_ip = "192.168.1.105"

        # First 5 attempts succeed
        for i in range(5):
            allowed, remaining, retry_after = self.rate_limiter.check_auth_limit(client_ip)
            self.assertTrue(allowed, f"Attempt {i+1} should be permitted")
            self.assertEqual(retry_after, 0)

        # 6th attempt is throttled
        blocked, remaining, retry_after = self.rate_limiter.check_auth_limit(client_ip)
        self.assertFalse(blocked)
        self.assertEqual(remaining, 0)
        self.assertGreater(retry_after, 0)

        # Key reset works
        self.rate_limiter.reset_key(f"auth:{client_ip}")
        re_allowed, _, _ = self.rate_limiter.check_auth_limit(client_ip)
        self.assertTrue(re_allowed)

    def test_answer_save_rate_limiting(self):
        session_id = "att_test_rate_limit_01"

        # 60 saves allowed
        for i in range(60):
            allowed, _, _ = self.rate_limiter.check_answer_save_limit(session_id)
            self.assertTrue(allowed)

        # 61st save blocked
        blocked, _, retry_after = self.rate_limiter.check_answer_save_limit(session_id)
        self.assertFalse(blocked)
        self.assertGreater(retry_after, 0)

    # -------------------------------------------------------------------------
    # 2. Defense-in-Depth Security Headers & ASVS L2 Data Masking
    # -------------------------------------------------------------------------
    def test_production_security_headers(self):
        headers = self.security_headers.get_standard_headers()
        self.assertEqual(headers["X-Frame-Options"], "DENY")
        self.assertTrue(
            "max-age=63072000" in headers["Strict-Transport-Security"] or
            "max-age=31536000" in headers["Strict-Transport-Security"]
        )
        self.assertIn("default-src 'self'", headers["Content-Security-Policy"])

    def test_asvs_l2_minor_data_masking(self):
        minor_student = {
            "student_id": "std_minor_ashik_01",
            "name": "আশিকুর রহমান",
            "age": 14,
            "is_minor": True,
            "phone_number": "+8801711998877",
            "location": {
                "district": "Dhaka",
                "thana": "Mirpur",
                "address_line": "House 12, Road 4, Section 10"
            }
        }

        # Case A: Public / Unauthorized viewer -> Sensitive PII masked
        public_view = self.security_headers.sanitize_minor_profile_data(
            student_data=minor_student,
            requester_user_id="usr_stranger_01"
        )
        self.assertEqual(public_view["phone_number"], "[REDACTED_MINOR_PRIVACY_PROTECTED]")
        self.assertEqual(public_view["location"]["address_line"], "[REDACTED_MINOR_PRIVACY_PROTECTED]")
        self.assertEqual(public_view["location"]["district"], "Dhaka")  # Safe high-level kept
        self.assertEqual(public_view["_minor_privacy_view"], "REDACTED_ASVS_L2")
        self.assertTrue(public_view["is_profile_private"])

        # Case B: Authorized Linked Guardian -> Full access granted
        guardian_view = self.security_headers.sanitize_minor_profile_data(
            student_data=minor_student,
            requester_user_id="usr_parent_ashik",
            authorized_guardian_ids=["usr_parent_ashik"]
        )
        self.assertEqual(guardian_view["phone_number"], "+8801711998877")
        self.assertEqual(guardian_view["location"]["address_line"], "House 12, Road 4, Section 10")
        self.assertEqual(guardian_view["_minor_privacy_view"], "AUTHORIZED_FULL")

    # -------------------------------------------------------------------------
    # 3. PWA Offline Practice Bundle Builder
    # -------------------------------------------------------------------------
    def test_offline_practice_bundle_generation(self):
        bundle = self.offline_sync.generate_offline_bundle(
            class_grade=8,
            subject="গণিত",
            bundle_size=5
        )
        self.assertIn("bundle_g8_", bundle["bundle_id"])
        self.assertEqual(bundle["class_grade"], 8)
        self.assertEqual(bundle["offline_storage_policy"], "PWA_INDEXED_DB")
        self.assertGreater(len(bundle["questions"]), 0)

        # Anti-Cheating check: Options must NOT reveal is_correct flag
        first_q = bundle["questions"][0]
        for opt in first_q["options"]:
            self.assertNotIn("is_correct", opt)
            self.assertIn("text_bn", opt)

    # -------------------------------------------------------------------------
    # 4. Batch Offline Answer Sync with Idempotent Replay
    # -------------------------------------------------------------------------
    def test_batch_offline_sync_replay(self):
        student_id = "std_offline_tester_01"
        raw_questions = [
            {
                "id": "q_off_01",
                "stem_bn": "১ম গতি সূত্র কী?",
                "options": [
                    {"id": "opt_a", "option_key": "A", "option_text_bn": "জড়তার সূত্র", "is_correct": True},
                    {"id": "opt_b", "option_key": "B", "option_text_bn": "বলের পরিমাপ", "is_correct": False}
                ]
            }
        ]

        # Start attempt in global quiz_engine
        from backend.app.services.quiz_engine import quiz_engine
        attempt = quiz_engine.start_practice_attempt(
            user_id=student_id,
            blueprint_id="bp_off_01",
            mode=QuizMode.ANYTIME_PRACTICE,
            raw_questions=raw_questions
        )
        attempt_id = attempt.attempt_id

        buffered_queue = [
            {
                "question_version_id": "q_off_01",
                "selected_option_id": "opt_a",
                "idempotency_key": "idem_off_001",
                "time_taken_seconds": 12.5
            },
            # Duplicate retry of the same answer
            {
                "question_version_id": "q_off_01",
                "selected_option_id": "opt_a",
                "idempotency_key": "idem_off_001",
                "time_taken_seconds": 12.5
            }
        ]

        batch_result = self.offline_sync.process_offline_sync_batch(
            student_id=student_id,
            attempt_id=attempt_id,
            buffered_answers=buffered_queue
        )

        self.assertEqual(batch_result["total_submitted"], 2)
        self.assertEqual(batch_result["synced_count"], 1)
        self.assertEqual(batch_result["skipped_count"], 1)
        self.assertEqual(batch_result["results"][0]["status"], "SYNCED_SAVED")
        self.assertEqual(batch_result["results"][1]["status"], "DUPLICATE_IDEMPOTENT_SKIPPED")

    # -------------------------------------------------------------------------
    # 5. Router Endpoints Integration
    # -------------------------------------------------------------------------
    def test_router_phase14_endpoints(self):
        async def run_async():
            # 1. Manifest
            manifest = await get_offline_manifest(class_grade=8, subject="গণিত", bundle_size=5)
            self.assertIn("bundle_id", manifest)
            self.assertEqual(manifest["class_grade"], 8)

            # 2. Security Policy
            policy = await get_security_policy()
            self.assertEqual(policy["status"], "ACTIVE")
            self.assertEqual(policy["asvs_level"], "ASVS 4.0 Level 2")

            # 3. Sanitize Profile API
            san_req = SecurityProfileSanitizeRequest(
                student_profile={
                    "user_id": "std_minor_api_01",
                    "age": 13,
                    "phone_number": "+8801999888777",
                    "email": "ashik@example.com"
                },
                requester_user_id="usr_anonymous"
            )
            san_resp = await sanitize_minor_profile(san_req)
            self.assertEqual(san_resp["status"], "SUCCESS")
            self.assertEqual(
                san_resp["sanitized_profile"]["phone_number"],
                "[REDACTED_MINOR_PRIVACY_PROTECTED]"
            )

        asyncio.run(run_async())


if __name__ == "__main__":
    unittest.main()
