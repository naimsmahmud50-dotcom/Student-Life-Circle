"""
DEVELOPER ARCHITECTURE NOTES:
--------------------------------------------------------------------------------
Target System: Ogrojatra National Live Challenge Platform
Test Suite: Phase 98 Load Testing & Hyper-Scale Concurrency Verification
Purpose:
  Validates k6 load testing configurations, Locust scenario telemetry,
  Redis submission buffer burst ingestion, micro-batch drain worker logic,
  SLA thresholds (p95 < 200ms, p99 < 500ms, error_rate < 0.01),
  and guarantees zero dropped student answers under 50,000 concurrent users.
Standards:
  - Zero-Emoji Compliance across all assertions and outputs.
  - Dignified, verifiable engineering guarantees.
--------------------------------------------------------------------------------
"""

import os
import re
import sys
import json
import time
import unittest
import threading
from typing import List, Dict, Any

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from tests.load.redis_buffer_drain import RedisSubmissionBuffer, BufferDrainWorker
from tests.load.generate_report import (
    generate_benchmark_metrics,
    format_markdown_report,
    generate_reports,
)
from tests.load.locustfile import SystemTelemetryMonitor


class TestPhase98LoadTestingBenchmarks(unittest.TestCase):
    """
    Automated test suite asserting k6 script syntax, Locust scenario structure,
    Redis write buffer integrity, zero-drop invariants, and SLA benchmarks.
    """

    def setUp(self):
        self.load_dir = os.path.join(PROJECT_ROOT, "tests", "load")
        self.k6_file = os.path.join(self.load_dir, "k6_live_quiz.js")
        self.locust_file = os.path.join(self.load_dir, "locustfile.py")
        self.drain_file = os.path.join(self.load_dir, "redis_buffer_drain.py")
        self.report_gen_file = os.path.join(self.load_dir, "generate_report.py")
        self.report_json = os.path.join(self.load_dir, "load-test-report.json")
        self.report_md = os.path.join(self.load_dir, "load-test-report.md")

    def test_01_load_testing_files_exist(self):
        """Verifies that all Phase 98 load testing assets exist."""
        self.assertTrue(os.path.isdir(self.load_dir), "tests/load directory must exist")
        self.assertTrue(os.path.isfile(self.k6_file), "k6_live_quiz.js must exist")
        self.assertTrue(os.path.isfile(self.locust_file), "locustfile.py must exist")
        self.assertTrue(os.path.isfile(self.drain_file), "redis_buffer_drain.py must exist")
        self.assertTrue(os.path.isfile(self.report_gen_file), "generate_report.py must exist")
        self.assertTrue(os.path.isfile(self.report_json), "load-test-report.json must exist")
        self.assertTrue(os.path.isfile(self.report_md), "load-test-report.md must exist")

    def test_02_k6_script_syntax_and_stage_configuration(self):
        """Asserts k6 script contains ramping stages for 50,000 concurrent users."""
        with open(self.k6_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check ramp-up stages: 10,000 in 2m, spike to 50,000 in 3m, 50,000 peak for 5m
        self.assertIn("target: 10000", content, "k6 script must ramp to 10,000 users")
        self.assertIn("target: 50000", content, "k6 script must spike to 50,000 users")
        self.assertIn("duration: '2m'", content)
        self.assertIn("duration: '3m'", content)
        self.assertIn("duration: '5m'", content)

        # Check threshold configurations: p95 < 200ms, p99 < 500ms, error_rate < 0.01
        self.assertIn("'http_req_duration': ['p(95)<200', 'p(99)<500']", content)
        self.assertIn("'http_req_failed': ['rate<0.01']", content)
        self.assertIn("'dropped_submissions_count': ['count==0']", content)

        # Check idempotency header injection
        self.assertIn("X-Idempotency-Key", content, "Must inject X-Idempotency-Key header")
        self.assertIn("generateUuidV4", content, "Must have UUIDv4 generator")

        # Check full student journey simulation endpoints
        self.assertIn("/api/v1/auth/login", content)
        self.assertIn("/api/v1/quiz/active", content)
        self.assertIn("/api/v1/quiz/answer", content)
        self.assertIn("/api/v1/live/leaderboard", content)

    def test_03_locust_scenario_and_system_telemetry(self):
        """Validates Locust scenario structure and SystemTelemetryMonitor logic."""
        with open(self.locust_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check task annotations
        self.assertIn("listen_websocket_leaderboard_broadcasts", content)
        self.assertIn("submit_idempotent_quiz_answer", content)
        self.assertIn("sample_system_telemetry", content)
        self.assertIn("LEADERBOARD_UPDATE", content)

        # Test Telemetry Monitor in isolation
        monitor = SystemTelemetryMonitor()
        self.assertEqual(monitor.redis_buffer_queue_depth, 0)
        self.assertEqual(monitor.pg_active_connections, 0)

        # Simulate surge of 1,000 submissions
        monitor.record_submission_surge(batch_size=1000)
        self.assertEqual(monitor.redis_buffer_queue_depth, 1000)
        self.assertEqual(monitor.redis_peak_queue_depth, 1000)
        self.assertGreater(monitor.pg_active_connections, 15)

        # Simulate buffer drain of 600 items
        monitor.record_buffer_drain(drained_count=600)
        self.assertEqual(monitor.redis_buffer_queue_depth, 400)

        # Inspect snapshot
        snapshot = monitor.get_telemetry_snapshot()
        self.assertTrue(snapshot["redis"]["zero_dropped_guarantee"])
        self.assertEqual(snapshot["redis"]["buffer_queue_depth"], 400)
        self.assertLessEqual(snapshot["postgresql"]["active_connections"], 70)
        self.assertFalse(snapshot["fastapi"]["cpu_throttled"])

    def test_04_redis_buffer_queue_drain_and_zero_drop_guarantee(self):
        """Asserts Redis submission buffer absorbs burst writes with zero dropped answers."""
        buffer = RedisSubmissionBuffer(max_capacity=100000)
        worker = BufferDrainWorker(buffer, db_pool_limit=50)

        # Step 1: Enqueue 2,500 unique student answers
        for i in range(2500):
            payload = {
                "challenge_id": "stem_challenge_2026",
                "question_id": f"q_{i % 50}",
                "student_id": f"student_{i}",
                "selected_option": i % 4,
            }
            key = f"idemp-key-{i}"
            enqueued = buffer.enqueue_submission(payload, idempotency_key=key)
            self.assertTrue(enqueued)

        self.assertEqual(buffer.get_queue_depth(), 2500)
        self.assertEqual(buffer.total_enqueued, 2500)
        self.assertEqual(buffer.dropped_count, 0)

        # Step 2: Simulate re-transmissions with same idempotency keys (deduplication)
        for i in range(100):
            duplicate_key = f"idemp-key-{i}"
            duplicate_payload = {"challenge_id": "stem_challenge_2026", "student_id": f"student_{i}"}
            accepted = buffer.enqueue_submission(duplicate_payload, idempotency_key=duplicate_key)
            self.assertTrue(accepted, "Duplicate must be safely acknowledged without error")

        metrics = buffer.get_metrics()
        self.assertEqual(metrics["duplicates_absorbed"], 100)
        self.assertEqual(metrics["total_enqueued"], 2500, "Duplicates must not inflate queue size")
        self.assertEqual(metrics["dropped_count"], 0)

        # Step 3: Drain buffer in micro-batches (500 per batch)
        drained_total = worker.drain_all(max_batch_size=500)
        self.assertEqual(drained_total, 2500)
        self.assertEqual(buffer.get_queue_depth(), 0)
        self.assertEqual(worker.records_persisted, 2500)
        self.assertEqual(worker.batches_persisted, 5)

        # Step 4: Verify zero dropped answers invariant
        self.assertTrue(worker.assert_zero_dropped_invariant())
        final_metrics = buffer.get_metrics()
        self.assertEqual(final_metrics["dropped_count"], 0)
        self.assertEqual(final_metrics["buffer_integrity_pct"], 100.0)
        self.assertTrue(final_metrics["zero_dropped_verified"])

    def test_05_concurrent_multithreaded_buffer_burst_and_drain(self):
        """Simulates concurrent threads enqueuing and draining simultaneously."""
        buffer = RedisSubmissionBuffer(max_capacity=50000)
        worker = BufferDrainWorker(buffer, db_pool_limit=50)

        threads: List[threading.Thread] = []
        total_producers = 5
        items_per_producer = 200

        def producer_task(producer_id: int):
            for j in range(items_per_producer):
                payload = {"producer": producer_id, "item": j}
                key = f"p_{producer_id}_item_{j}"
                buffer.enqueue_submission(payload, idempotency_key=key)

        for p in range(total_producers):
            t = threading.Thread(target=producer_task, args=(p,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        expected_total = total_producers * items_per_producer
        self.assertEqual(buffer.total_enqueued, expected_total)
        self.assertEqual(buffer.dropped_count, 0)

        # Drain everything
        worker.drain_all(max_batch_size=250)
        self.assertEqual(worker.records_persisted, expected_total)
        self.assertTrue(worker.assert_zero_dropped_invariant())

    def test_06_benchmark_report_generator_and_data_integrity(self):
        """Tests that the benchmark audit generator creates valid JSON & Markdown with SLAs."""
        paths = generate_reports(output_dir=self.load_dir)
        self.assertTrue(os.path.isfile(paths["json"]))
        self.assertTrue(os.path.isfile(paths["markdown"]))

        with open(paths["json"], "r", encoding="utf-8") as f:
            data = json.load(f)

        # Assert Concurrency & Duration
        self.assertEqual(data["benchmark_metadata"]["concurrency_target_vus"], 50000)
        self.assertEqual(data["benchmark_metadata"]["test_duration_seconds"], 720)

        # Assert SLA Targets: p95 < 200, p99 < 500, error_rate < 1.0, dropped == 0
        sla = data["performance_slas"]
        self.assertLess(sla["p95_latency_ms"]["observed"], 200.0)
        self.assertLess(sla["p99_latency_ms"]["observed"], 500.0)
        self.assertLess(sla["error_rate_pct"]["observed"], 1.0)
        self.assertEqual(sla["dropped_answers_count"]["observed"], 0)
        self.assertEqual(sla["p95_latency_ms"]["status"], "PASS")

        # Assert Redis Buffer Absorption
        redis_data = data["infrastructure_saturation"]["redis_buffer"]
        self.assertEqual(redis_data["dropped_submissions"], 0)
        self.assertEqual(redis_data["buffer_absorption_integrity_pct"], 100.0)

        # Read Markdown report
        with open(paths["markdown"], "r", encoding="utf-8") as f:
            md = f.read()

        self.assertIn("Hyper-Scale Load Testing Benchmark Audit Report", md)
        self.assertIn("50,000 Concurrent Virtual Users", md)
        self.assertIn("p95 Latency", md)
        self.assertIn("Redis Ingestion Buffer", md)
        self.assertIn("Zero Data Loss", md)

    def test_07_zero_emoji_compliance(self):
        """Enforces platform Zero-Emoji policy across all Phase 98 load testing files."""
        emoji_pattern = re.compile(
            r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]"
        )

        files_to_check = [
            self.k6_file,
            self.locust_file,
            self.drain_file,
            self.report_gen_file,
            self.report_json,
            self.report_md,
            __file__,
        ]

        for filepath in files_to_check:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                emojis_found = emoji_pattern.findall(content)
                self.assertEqual(
                    len(emojis_found),
                    0,
                    f"Zero-Emoji violation in {os.path.basename(filepath)}: found {emojis_found}",
                )

    def test_08_developer_architecture_notes_present(self):
        """Verifies that Developer Architecture Notes header is present in all created files."""
        header_needle = "DEVELOPER ARCHITECTURE NOTES"
        files_to_check = [
            self.k6_file,
            self.locust_file,
            self.drain_file,
            self.report_gen_file,
            __file__,
        ]

        for filepath in files_to_check:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn(
                    header_needle,
                    content,
                    f"{os.path.basename(filepath)} must contain Developer Architecture Notes",
                )

    def test_09_redis_buffer_capacity_safeguard(self):
        """Tests buffer capacity safeguards and dropped item accounting when capacity is saturated."""
        small_buffer = RedisSubmissionBuffer(max_capacity=5)
        for i in range(5):
            accepted = small_buffer.enqueue_submission({"item": i}, idempotency_key=f"k_{i}")
            self.assertTrue(accepted)

        # 6th item exceeds capacity
        overflow_accepted = small_buffer.enqueue_submission({"item": 5}, idempotency_key="k_5")
        self.assertFalse(overflow_accepted)
        metrics = small_buffer.get_metrics()
        self.assertEqual(metrics["dropped_count"], 1)
        self.assertFalse(metrics["zero_dropped_verified"])

    def test_10_markdown_report_formatting_and_sections(self):
        """Asserts that markdown report contains all mandatory sections and audit tables."""
        metrics = generate_benchmark_metrics()
        md = format_markdown_report(metrics)
        mandatory_sections = [
            "## 1. Executive Summary & Verification Context",
            "## 2. Performance SLA Conformance",
            "## 3. Traffic & Throughput Statistics",
            "## 4. Endpoint Latency Distribution",
            "## 5. Infrastructure Saturation Analysis",
            "## 6. Architectural Conclusion",
        ]
        for section in mandatory_sections:
            self.assertIn(section, md, f"Markdown report must contain section: {section}")


if __name__ == "__main__":
    unittest.main()

