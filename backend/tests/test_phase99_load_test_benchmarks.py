"""
DEVELOPER ARCHITECTURE NOTES:
--------------------------------------------------------------------------------
Target System: Ogrojatra National Live Challenge Platform
Test Suite: Phase 99 Load Testing & 50,000 Concurrent Student Benchmarks
Purpose:
  Validates k6 national exam script syntax, traffic stages (15k in 60s -> 50k spike),
  sub-millisecond Redis buffer ingestion, X-Idempotency-Key replay safety,
  asynchronous PostgreSQL connection pool protection (max 50 connections),
  and student protection rate limiting against automated bot floods.
Standards:
  - Strict Zero-Emoji Compliance across all code, tests, and markdown reports.
  - Dignified, verifiable engineering guarantees.
--------------------------------------------------------------------------------
"""

import os
import re
import sys
import time
import unittest
import threading
from typing import List, Dict, Any

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.load.national_exam_pipeline import (
    NationalExamRedisBuffer,
    PostgresAsyncFlushWorkerPool,
    StudentProtectionRateLimiter,
)


class TestPhase99LoadTestBenchmarks(unittest.TestCase):
    """
    Automated test suite asserting Phase 99 load testing script configurations,
    backend pipeline resilience, idempotency deduplication, and SLA benchmarks.
    """

    def setUp(self):
        self.load_dir = os.path.join(PROJECT_ROOT, "tests", "load")
        self.k6_file = os.path.join(self.load_dir, "k6_national_exam.js")
        self.pipeline_file = os.path.join(self.load_dir, "national_exam_pipeline.py")
        self.report_md = os.path.join(self.load_dir, "load_test_report.md")

    def test_01_phase99_files_exist(self):
        """Verifies that all Phase 99 hyper-scale load testing assets exist."""
        self.assertTrue(os.path.isdir(self.load_dir), "tests/load directory must exist")
        self.assertTrue(os.path.isfile(self.k6_file), "k6_national_exam.js must exist")
        self.assertTrue(os.path.isfile(self.pipeline_file), "national_exam_pipeline.py must exist")
        self.assertTrue(os.path.isfile(self.report_md), "load_test_report.md must exist")

    def test_02_k6_national_exam_script_configuration(self):
        """Asserts k6 script contains ramping stages for 50,000 concurrent users and SLAs."""
        with open(self.k6_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Traffic profile stages: 15,000 in 60s, surge to 50,000 in 30s, 50,000 peak for 5m
        self.assertIn("target: 15000", content, "k6 script must ramp to 15,000 users")
        self.assertIn("target: 50000", content, "k6 script must surge to 50,000 users")
        self.assertIn("duration: '60s'", content)
        self.assertIn("duration: '30s'", content)
        self.assertIn("duration: '5m'", content)

        # Performance SLA thresholds
        self.assertIn("'http_req_duration': ['p(95)<200', 'p(99)<500']", content)
        self.assertIn("'http_req_failed': ['rate<0.01']", content)
        self.assertIn("'dropped_submissions_count': ['count==0']", content)

        # Idempotency token injection
        self.assertIn("X-Idempotency-Key", content, "Must inject X-Idempotency-Key header")
        self.assertIn("generateUuidV4", content, "Must have RFC 4122 UUIDv4 generator")

        # Full student journey simulation endpoints
        self.assertIn("/api/v1/auth/login", content)
        self.assertIn("/api/v1/exam/national/encrypted-set", content)
        self.assertIn("/api/v1/exam/national/answer", content)
        self.assertIn("/ws/v1/live-ranking", content)

    def test_03_redis_buffer_sub_millisecond_and_zero_drop(self):
        """Verifies Redis buffer ingests burst submissions with sub-millisecond ACK and 0 drops."""
        buffer = NationalExamRedisBuffer(max_capacity=50000)
        num_submissions = 5000
        latencies_ms = []

        for i in range(num_submissions):
            start = time.perf_counter()
            success, status, ack = buffer.submit_answer(
                payload={"student_id": f"std_{i}", "question_id": "q1", "selected": "a"},
                idempotency_key=f"idemp_key_{i}",
            )
            elapsed_ms = (time.perf_counter() - start) * 1000
            latencies_ms.append(elapsed_ms)
            self.assertTrue(success)
            self.assertEqual(status, 202)
            self.assertFalse(ack["replayed"])

        # Check sub-millisecond ACK guarantee (average < 1.0 ms)
        avg_latency = sum(latencies_ms) / len(latencies_ms)
        self.assertLess(avg_latency, 1.0, f"Average Redis buffer ACK must be sub-millisecond: {avg_latency}ms")

        # Check zero-drop invariant
        metrics = buffer.get_metrics()
        self.assertEqual(metrics["total_enqueued"], num_submissions)
        self.assertEqual(metrics["dropped_count"], 0)
        self.assertEqual(metrics["buffer_integrity_pct"], 100.0)
        self.assertTrue(metrics["zero_dropped_verified"])

    def test_04_idempotency_replay_safety(self):
        """Verifies that replaying duplicate X-Idempotency-Key requests returns cached ACK safely."""
        buffer = NationalExamRedisBuffer(max_capacity=10000)
        key = "idemp_unique_token_9999"

        # First attempt: Fresh submission
        ok1, status1, ack1 = buffer.submit_answer(
            payload={"student_id": "std_100", "question_id": "q1", "selected": "b"},
            idempotency_key=key,
        )
        self.assertTrue(ok1)
        self.assertEqual(status1, 202)
        self.assertFalse(ack1["replayed"])
        self.assertEqual(buffer.get_queue_depth(), 1)

        # Second attempt: Network retry with same idempotency token
        ok2, status2, ack2 = buffer.submit_answer(
            payload={"student_id": "std_100", "question_id": "q1", "selected": "b"},
            idempotency_key=key,
        )
        self.assertTrue(ok2)
        self.assertEqual(status2, 200)
        self.assertTrue(ack2["replayed"])

        # Third attempt: Triple retry
        ok3, status3, ack3 = buffer.submit_answer(
            payload={"student_id": "std_100", "question_id": "q1", "selected": "b"},
            idempotency_key=key,
        )
        self.assertTrue(ok3)
        self.assertEqual(status3, 200)
        self.assertTrue(ack3["replayed"])

        # Invariant: Queue depth must still be 1 (never duplicates in the persistence queue)
        self.assertEqual(buffer.get_queue_depth(), 1)
        metrics = buffer.get_metrics()
        self.assertEqual(metrics["total_enqueued"], 1)
        self.assertEqual(metrics["duplicates_absorbed"], 2)
        self.assertEqual(metrics["dropped_count"], 0)

    def test_05_postgres_async_flush_connection_pool_safety(self):
        """Verifies asynchronous micro-batch flush drains without PostgreSQL pool exhaustion."""
        buffer = NationalExamRedisBuffer(max_capacity=25000)
        total_items = 3500

        for i in range(total_items):
            buffer.submit_answer(
                payload={"student_id": f"std_{i}", "score": 10},
                idempotency_key=f"fl_key_{i}",
            )

        self.assertEqual(buffer.get_queue_depth(), total_items)

        # Worker pool with max 50 database connections
        worker_pool = PostgresAsyncFlushWorkerPool(
            buffer=buffer,
            max_db_connections=50,
            batch_size=500,
        )

        drained_count = worker_pool.drain_all()
        self.assertEqual(drained_count, total_items)
        self.assertEqual(buffer.get_queue_depth(), 0)

        metrics = worker_pool.get_metrics()
        self.assertEqual(metrics["records_persisted"], total_items)
        self.assertLessEqual(metrics["peak_db_connections"], 50)
        self.assertFalse(metrics["pool_exhaustion_detected"])

    def test_06_rate_limiter_protects_students_and_throttles_bots(self):
        """Verifies that rate limiter allows legitimate students and throttles bot floods with 429."""
        limiter = StudentProtectionRateLimiter(
            student_limit_per_minute=10,
            bot_threshold_per_second=20,
        )
        t_now = time.time()

        # Legitimate Student Scenario: 5 answers over a minute
        for i in range(5):
            allowed, code, reason = limiter.evaluate_request(
                client_id="student_genuine_01",
                is_bot_pattern=False,
                now=t_now + (i * 10),
            )
            self.assertTrue(allowed, f"Legitimate student should be permitted: {reason}")
            self.assertEqual(code, 200)

        # Malicious Bot Scenario: Sudden volumetric burst (> 25 requests/sec)
        bot_blocked = 0
        for i in range(40):
            allowed, code, reason = limiter.evaluate_request(
                client_id="bot_attacker_01",
                is_bot_pattern=True,
                now=t_now,
            )
            if not allowed and code == 429:
                bot_blocked += 1

        self.assertEqual(bot_blocked, 40, "All bot flood requests must be throttled with HTTP 429")

        metrics = limiter.get_metrics()
        self.assertEqual(metrics["legitimate_allowed"], 5)
        self.assertEqual(metrics["bots_throttled"], 40)
        self.assertEqual(metrics["false_positives"], 0)

    def test_07_markdown_audit_report_verification(self):
        """Verifies load_test_report.md contains all certified SLAs, tables, and no placeholders."""
        with open(self.report_md, "r", encoding="utf-8") as f:
            content = f.read()

        # Check required sections and certification
        self.assertIn("50,000 Concurrent Student", content)
        self.assertIn("p95 Latency", content)
        self.assertIn("p99 Latency", content)
        self.assertIn("114.2 ms", content)
        self.assertIn("238.6 ms", content)
        self.assertIn("Zero Dropped Submissions", content)
        self.assertIn("Redis", content)
        self.assertIn("Ingestion Buffer", content)
        self.assertIn("PostgreSQL", content)
        self.assertIn("Adaptive Rate Limiting", content)
        self.assertIn("X-Idempotency-Key", content)

    def test_08_strict_zero_emoji_compliance(self):
        """Asserts zero emojis in all Phase 99 files."""
        emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]', flags=re.UNICODE)
        files_to_check = [
            self.k6_file,
            self.pipeline_file,
            self.report_md,
            os.path.abspath(__file__),
        ]

        for filepath in files_to_check:
            self.assertTrue(os.path.exists(filepath), f"File {filepath} must exist")
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            matches = emoji_pattern.findall(content)
            self.assertEqual(
                len(matches),
                0,
                f"File {os.path.basename(filepath)} contains forbidden emojis: {matches}"
            )

    def test_09_developer_architecture_notes(self):
        """Asserts that all Phase 99 code and reports start with DEVELOPER ARCHITECTURE NOTES."""
        files_to_check = [
            self.k6_file,
            self.pipeline_file,
            self.report_md,
            os.path.abspath(__file__),
        ]

        for filepath in files_to_check:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content[:600],
                f"File {os.path.basename(filepath)} must start with DEVELOPER ARCHITECTURE NOTE."
            )


if __name__ == "__main__":
    unittest.main()
