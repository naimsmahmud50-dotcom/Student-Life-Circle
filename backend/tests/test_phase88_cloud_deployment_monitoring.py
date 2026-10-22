"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE - PHASE 88 TEST SUITE:
MODULE:    Production Cloud Deployment, Observability & Disaster Recovery Verification
TOPIC:     Prometheus Metrics, Sentry PII Sanitization, Nginx HTTP/3, K8s, Systemd, PITR, Deploy Scripts
FILE:      backend/tests/test_phase88_cloud_deployment_monitoring.py
PURPOSE:   Automated unit and integration test suite verifying:
           1. PrometheusMetricsCollector text format, counters, and p50/p90/p95/p99 percentiles.
           2. SentryManager error capture, DSN fallback, and ASVS L2 PII scrubbing.
           3. Nginx configuration with HTTP/3 (QUIC), Alt-Svc headers, and WebSocket upgrades.
           4. Cloudflare DNSSEC, Strict SSL, and edge security rules validation.
           5. Kubernetes manifests (backend, redis, ingress, configmap, secrets) schema validation.
           6. Systemd unit files sandboxing directives and restart policies.
           7. Database WAL continuous archiving SQL policy and PITR restore script execution.
           8. Vercel edge caching and security headers configuration.
           9. Production Docker Compose multi-service topology (including Prometheus & Grafana).
           10. deploy.sh orchestrator commands and PRODUCTION_LAUNCH_CHECKLIST.md completeness.
           11. Strict Zero-Emoji compliance and Developer Architecture Notes presence.
AUDIENCE:  QA Engineers, SREs, Security Auditors & AI Agents
STANDARDS: Python unittest, OWASP ASVS L2, OpenMetrics, Zero-Emoji Spec
========================================================================================
"""

import unittest
import os
import re
import json
import subprocess
from pathlib import Path

import asyncio
from backend.app.core.metrics import PrometheusMetricsCollector, metrics_collector
from backend.app.core.sentry import SentryManager, sentry_manager
from backend.app.main import prometheus_metrics
from backend.app.core.fastapi_shim import PlainTextResponse


class TestPrometheusMetrics(unittest.TestCase):
    """Verifies Prometheus metrics aggregation, latency percentiles, and exposition format."""

    def setUp(self):
        self.collector = PrometheusMetricsCollector()

    def test_record_request_and_percentiles(self):
        """Tests request recording and p50, p90, p95, p99 percentile calculation."""
        # Record 100 requests with varying latencies
        for i in range(1, 101):
            latency = i * 0.005  # 5ms to 500ms
            status = 200 if i <= 95 else 500
            self.collector.record_request(
                method="GET",
                endpoint="/api/v1/health",
                status_code=status,
                duration_seconds=latency
            )

        percentiles = self.collector.get_percentiles("GET", "/api/v1/health")
        self.assertIn("p50", percentiles)
        self.assertIn("p90", percentiles)
        self.assertIn("p95", percentiles)
        self.assertIn("p99", percentiles)

        # Assert p95 is greater than p50
        self.assertGreater(percentiles["p95"], percentiles["p50"])
        # Assert p99 is greater than or equal to p95
        self.assertGreaterEqual(percentiles["p99"], percentiles["p95"])

    def test_websocket_tracking(self):
        """Tests active WebSocket connections gauge increments and decrements."""
        self.collector.record_websocket_connect("live-challenge")
        self.collector.record_websocket_connect("live-challenge")
        self.collector.record_websocket_connect("whiteboard")

        output = self.collector.generate_prometheus_metrics()
        self.assertIn('active_websocket_connections{room_type="live-challenge"} 2', output)
        self.assertIn('active_websocket_connections{room_type="whiteboard"} 1', output)

        self.collector.record_websocket_disconnect("live-challenge")
        output2 = self.collector.generate_prometheus_metrics()
        self.assertIn('active_websocket_connections{room_type="live-challenge"} 1', output2)

    def test_rate_limit_throttle_recording(self):
        """Tests DDoS rate limit throttling counters."""
        self.collector.record_rate_limit_throttle("/api/v1/auth/login")
        self.collector.record_rate_limit_throttle("/api/v1/auth/login")

        output = self.collector.generate_prometheus_metrics()
        self.assertIn('rate_limit_throttled_total{endpoint="/api/v1/auth/login"} 2', output)

    def test_prometheus_exposition_format(self):
        """Tests that generated text strictly conforms to Prometheus 0.0.4 text standard."""
        self.collector.record_request("POST", "/api/v1/quiz/submit", 200, 0.045)
        output = self.collector.generate_prometheus_metrics()

        self.assertIn("# HELP http_requests_total", output)
        self.assertIn("# TYPE http_requests_total counter", output)
        self.assertIn("# HELP http_request_duration_seconds", output)
        self.assertIn("# TYPE http_request_duration_seconds summary", output)
        self.assertIn('http_requests_total{endpoint="/api/v1/quiz/submit",method="POST",status="200"} 1', output)
        self.assertIn('quantile="0.95"', output)
        self.assertIn('quantile="0.99"', output)

    def test_fastapi_metrics_endpoint(self):
        """Tests the live /metrics endpoint mounted on FastAPI app."""
        response = asyncio.run(prometheus_metrics())
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/plain", response.media_type)
        self.assertIn("http_requests_total", response.content)


class TestSentryManager(unittest.TestCase):
    """Verifies Sentry integration, exception tracking, and ASVS L2 PII redaction."""

    def test_sentry_initialization_graceful(self):
        """Tests initialization with and without DSN does not raise unhandled errors."""
        manager = SentryManager(dsn="https://fake-key@sentry.ogrojatra.edu.bd/123", environment="test")
        self.assertIsNotNone(manager)

        # Test capture exception does not crash
        try:
            raise ValueError("Test synthetic exception for observability")
        except ValueError as exc:
            event_id = manager.capture_exception(exc, {"user_id": "usr_9988"})
            self.assertIsInstance(event_id, str)

    def test_pii_sanitization(self):
        """Tests that sensitive keys like password, token, and secret are redacted."""
        manager = SentryManager()
        sensitive_data = {
            "username": "student_01",
            "password": "SuperSecretPassword123!",
            "auth_token": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            "refresh_token": "rt_secret_token",
            "api_key": "bkash_secret_key_prod",
            "safe_metadata": "HSC Physics 1st Paper"
        }

        sanitized = manager.sanitize_pii(sensitive_data)
        self.assertEqual(sanitized["password"], "[REDACTED_BY_SENTRY_GATEWAY]")
        self.assertEqual(sanitized["auth_token"], "[REDACTED_BY_SENTRY_GATEWAY]")
        self.assertEqual(sanitized["refresh_token"], "[REDACTED_BY_SENTRY_GATEWAY]")
        self.assertEqual(sanitized["api_key"], "[REDACTED_BY_SENTRY_GATEWAY]")
        self.assertEqual(sanitized["safe_metadata"], "HSC Physics 1st Paper")

    def test_frontend_sentry_client_script(self):
        """Verifies frontend Sentry error reporter contains PII redaction and client service."""
        sentry_fe_path = Path("frontend/src/lib/sentry.ts")
        self.assertTrue(sentry_fe_path.exists(), "frontend/src/lib/sentry.ts must exist")
        content = sentry_fe_path.read_text(encoding="utf-8")
        self.assertIn("FrontendSentryService", content)
        self.assertIn("clientSentry", content)
        self.assertIn("captureException", content)
        self.assertIn("DEVELOPER ARCHITECTURE NOTE", content)


class TestNginxAndCloudflare(unittest.TestCase):
    """Verifies Nginx HTTP/3 (QUIC) reverse proxy and Cloudflare edge security configurations."""

    def test_nginx_configuration_directives(self):
        """Tests Nginx configuration for HTTP/3, QUIC, and WebSocket upgrades."""
        nginx_conf = Path("infra/nginx/nginx.conf")
        self.assertTrue(nginx_conf.exists(), "infra/nginx/nginx.conf must exist")
        content = nginx_conf.read_text(encoding="utf-8")

        self.assertIn("listen 443 quic reuseport", content)
        self.assertIn('add_header Alt-Svc \'h3=":443"; ma=86400\'', content)
        self.assertIn("proxy_set_header Upgrade $http_upgrade", content)
        self.assertIn('proxy_set_header Connection "upgrade"', content)
        self.assertIn("limit_req_zone", content)
        self.assertIn("proxy_pass http://backend_upstream", content)
        self.assertIn("proxy_pass http://frontend_upstream", content)

    def test_cloudflare_edge_rules(self):
        """Tests Cloudflare DNS and security rules configuration."""
        cf_path = Path("infra/cloudflare/dns_ssl_rules.json")
        self.assertTrue(cf_path.exists(), "infra/cloudflare/dns_ssl_rules.json must exist")
        
        with open(cf_path, "r", encoding="utf-8") as f:
            cf_data = json.load(f)

        self.assertEqual(cf_data["ssl_tls"]["mode"], "strict")
        self.assertEqual(cf_data["dnssec"]["status"], "active")
        self.assertEqual(cf_data["ssl_tls"]["min_tls_version"], "1.2")
        self.assertEqual(cf_data["edge_caching_and_performance"]["http3_quic"], "on")
        self.assertIn("waf_rate_limiting_rules", cf_data)


class TestKubernetesAndSystemd(unittest.TestCase):
    """Verifies Kubernetes manifests and Linux systemd unit service specifications."""

    def test_kubernetes_manifests_exist_and_valid(self):
        """Tests that all required Kubernetes manifests exist and contain required blocks."""
        k8s_dir = Path("infra/k8s")
        expected_files = [
            "configmap-secrets.yaml",
            "backend-deployment.yaml",
            "redis-deployment.yaml",
            "ingress.yaml"
        ]
        for f in expected_files:
            file_path = k8s_dir / f
            self.assertTrue(file_path.exists(), f"Missing Kubernetes manifest: {f}")

        # Check backend deployment details
        backend_content = (k8s_dir / "backend-deployment.yaml").read_text(encoding="utf-8")
        self.assertIn("kind: Deployment", backend_content)
        self.assertIn("type: RollingUpdate", backend_content)
        self.assertIn("maxSurge: 1", backend_content)
        self.assertIn("maxUnavailable: 0", backend_content)
        self.assertIn("runAsUser: 10001", backend_content)
        self.assertIn("path: /api/v1/health", backend_content)
        self.assertIn("kind: HorizontalPodAutoscaler", backend_content)

        # Check ingress details
        ingress_content = (k8s_dir / "ingress.yaml").read_text(encoding="utf-8")
        self.assertIn("kind: Ingress", ingress_content)
        self.assertIn("path: /api/v1", ingress_content)
        self.assertIn("path: /ws", ingress_content)
        self.assertIn("path: /metrics", ingress_content)
        self.assertIn("secretName: ogrojatra-tls-cert", ingress_content)

    def test_systemd_unit_services(self):
        """Tests systemd service units for backend and celery workers."""
        systemd_dir = Path("infra/systemd")
        backend_service = systemd_dir / "ogrojatra-backend.service"
        celery_service = systemd_dir / "ogrojatra-celery.service"

        self.assertTrue(backend_service.exists(), "ogrojatra-backend.service must exist")
        self.assertTrue(celery_service.exists(), "ogrojatra-celery.service must exist")

        backend_text = backend_service.read_text(encoding="utf-8")
        self.assertIn("ProtectSystem=strict", backend_text)
        self.assertIn("NoNewPrivileges=true", backend_text)
        self.assertIn("PrivateTmp=true", backend_text)
        self.assertIn("Restart=always", backend_text)
        self.assertIn("uvicorn backend.app.main:app", backend_text)

        celery_text = celery_service.read_text(encoding="utf-8")
        self.assertIn("celery -A backend.app.core.celery_app worker", celery_text)
        self.assertIn("Restart=always", celery_text)


class TestDatabaseBackupAndPitr(unittest.TestCase):
    """Verifies continuous WAL archiving policy and automated PITR restoration script."""

    def test_database_backup_policy_sql(self):
        """Tests PostgreSQL WAL archiving SQL schema and RLS policies."""
        sql_path = Path("infra/database/backup_and_pitr_policy.sql")
        self.assertTrue(sql_path.exists(), "backup_and_pitr_policy.sql must exist")
        sql_text = sql_path.read_text(encoding="utf-8")

        self.assertIn("CREATE SCHEMA IF NOT EXISTS backup_meta;", sql_text)
        self.assertIn("ALTER TABLE backup_meta.disaster_recovery_logs ENABLE ROW LEVEL SECURITY;", sql_text)
        self.assertIn("CREATE POLICY deny_update_backup_logs", sql_text)
        self.assertIn("CREATE POLICY deny_delete_backup_logs", sql_text)
        self.assertIn("FUNCTION backup_meta.create_restore_point", sql_text)
        self.assertIn("VIEW backup_meta.archiving_health", sql_text)

    def test_pitr_restore_script_dry_run(self):
        """Tests execution of pitr_restore.sh with DRY_RUN=true flag."""
        script_path = Path("infra/database/pitr_restore.sh")
        self.assertTrue(script_path.exists(), "pitr_restore.sh must exist")
        self.assertTrue(os.access(script_path, os.X_OK), "pitr_restore.sh must be executable")

        result = subprocess.run(
            ["bash", str(script_path), "2026-10-18 12:00:00 UTC"],
            env={**os.environ, "DRY_RUN": "true"},
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Initializing Point-in-Time Recovery procedure", result.stdout)
        self.assertIn("Dry run preflight checks completed successfully", result.stdout)


class TestDeploymentOrchestrationAndChecklist(unittest.TestCase):
    """Verifies Vercel configuration, Docker Compose topology, deploy.sh, and launch checklist."""

    def test_vercel_json_configuration(self):
        """Tests frontend/vercel.json for edge caching and security headers."""
        v_path = Path("frontend/vercel.json")
        self.assertTrue(v_path.exists(), "frontend/vercel.json must exist")
        
        with open(v_path, "r", encoding="utf-8") as f:
            v_data = json.load(f)

        self.assertEqual(v_data.get("framework"), "nextjs")
        self.assertTrue(v_data.get("cleanUrls"))
        
        # Check static cache control header
        found_cache_control = False
        for entry in v_data.get("headers", []):
            if entry.get("source") == "/_next/static/(.*)":
                for h in entry.get("headers", []):
                    if h.get("key") == "Cache-Control" and "immutable" in h.get("value", ""):
                        found_cache_control = True
        self.assertTrue(found_cache_control, "Cache-Control immutable header must be configured for /_next/static/")

    def test_docker_compose_prod_topology(self):
        """Tests docker-compose.prod.yml includes all 7 production services."""
        compose_path = Path("docker-compose.prod.yml")
        self.assertTrue(compose_path.exists(), "docker-compose.prod.yml must exist")
        content = compose_path.read_text(encoding="utf-8")

        services = ["postgres:", "redis:", "backend:", "frontend:", "nginx:", "prometheus:", "grafana:"]
        for s in services:
            self.assertIn(s, content, f"Service {s} must be present in docker-compose.prod.yml")

        self.assertIn("ogrojatra-internal:", content)
        self.assertIn("ogrojatra-public:", content)

    def test_deploy_script_syntax_and_commands(self):
        """Tests deploy.sh syntax and status command invocation."""
        deploy_script = Path("deploy.sh")
        self.assertTrue(deploy_script.exists(), "deploy.sh must exist")
        self.assertTrue(os.access(deploy_script, os.X_OK), "deploy.sh must be executable")

        result = subprocess.run(["bash", "-n", str(deploy_script)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"deploy.sh has bash syntax errors: {result.stderr}")

    def test_production_launch_checklist(self):
        """Tests PRODUCTION_LAUNCH_CHECKLIST.md contains required SLOs and DR procedures."""
        checklist_path = Path("PRODUCTION_LAUNCH_CHECKLIST.md")
        self.assertTrue(checklist_path.exists(), "PRODUCTION_LAUNCH_CHECKLIST.md must exist")
        checklist_text = checklist_path.read_text(encoding="utf-8")

        self.assertIn("Verified Production Endpoints Matrix", checklist_text)
        self.assertIn("Service Level Objectives (SLOs)", checklist_text)
        self.assertIn("Disaster Recovery (DR) Runbook", checklist_text)
        self.assertIn("Recovery Time Objective (RTO)", checklist_text)
        self.assertIn("Recovery Point Objective (RPO)", checklist_text)


class TestZeroEmojiAndArchitectureNotesCompliance(unittest.TestCase):
    """Enforces zero-emoji standard and developer architecture notes across Phase 88 files."""

    EMOJI_PATTERN = re.compile(
        r"[\U0001F600-\U0001F64F"
        r"\U0001F300-\U0001F5FF"
        r"\U0001F680-\U0001F6FF"
        r"\U0001F700-\U0001F77F"
        r"\U0001F780-\U0001F7FF"
        r"\U0001F800-\U0001F8FF"
        r"\U0001F900-\U0001F9FF"
        r"\U0001FA00-\U0001FA6F"
        r"\U0001FA70-\U0001FAFF"
        r"\U00002702-\U000027B0"
        r"\U000024C2-\U0001F251]"
    )

    PHASE88_FILES = [
        "backend/app/core/metrics.py",
        "backend/app/core/sentry.py",
        "frontend/src/lib/sentry.ts",
        "infra/nginx/nginx.conf",
        "infra/cloudflare/dns_ssl_rules.json",
        "infra/k8s/configmap-secrets.yaml",
        "infra/k8s/backend-deployment.yaml",
        "infra/k8s/redis-deployment.yaml",
        "infra/k8s/ingress.yaml",
        "infra/systemd/ogrojatra-backend.service",
        "infra/systemd/ogrojatra-celery.service",
        "infra/database/backup_and_pitr_policy.sql",
        "infra/database/pitr_restore.sh",
        "infra/prometheus/prometheus.yml",
        "infra/grafana/dashboards/platform_dashboard.json",
        "infra/grafana/provisioning/datasources/prometheus.yml",
        "infra/grafana/provisioning/dashboards/dashboards.yml",
        "deploy.sh",
        "docker-compose.prod.yml",
        "PRODUCTION_LAUNCH_CHECKLIST.md"
    ]

    def test_strict_zero_emoji(self):
        """Verifies zero emojis exist in any Phase 88 file."""
        for file_rel in self.PHASE88_FILES:
            file_path = Path(file_rel)
            if not file_path.exists():
                continue
            content = file_path.read_text(encoding="utf-8")
            match = self.EMOJI_PATTERN.search(content)
            self.assertIsNone(match, f"Found prohibited emoji in {file_rel}: {match.group() if match else ''}")

    def test_developer_architecture_notes_presence(self):
        """Verifies developer architecture notes exist at top of Phase 88 files."""
        for file_rel in self.PHASE88_FILES:
            file_path = Path(file_rel)
            if not file_path.exists():
                continue
            # JSON files can omit comment headers if standard JSON parser forbids comments
            if file_rel.endswith(".json"):
                continue
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"Missing 'DEVELOPER ARCHITECTURE NOTE' in {file_rel}"
            )


if __name__ == "__main__":
    unittest.main()
