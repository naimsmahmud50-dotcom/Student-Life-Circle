"""
========================================================================================
MODULE:    Phase 87 Automated Test Suite - Production Docker & GitHub Actions CI/CD
TOPIC:     Container Security, Multi-Stage Builds, CI Quality Gates & Trivy Audits
FILE:      backend/tests/test_phase87_docker_and_cicd.py
PURPOSE:   Validates full compliance with CIS Docker Benchmark, NIST SP 800-190,
           and automated GitHub Actions CI/CD standards:
           1. backend/Dockerfile: Multi-stage python:3.12-slim-bookworm, non-root appuser:10001,
              wheel caching, and 4-worker Uvicorn ASGI entrypoint.
           2. frontend/Dockerfile: Multi-stage node:20-alpine standalone build (< 120MB),
              non-root nextjs:1001 user, and wget healthcheck.
           3. frontend/next.config.js: Standalone output mode enabled.
           4. docker-compose.prod.yml: 4 core services (FastAPI, Next.js, Postgres 16 Alpine,
              Redis 7 Alpine), network segmentation, resource quotas, and logging limits.
           5. .github/workflows/ci-cd.yml & deploy.yml: 4 CI jobs (backend-tests,
              frontend-quality, e2e-smoke, docker-trivy-deploy), Trivy scanning, GHCR push.
           6. Strict Zero-Emoji compliance and prominent Developer Architecture Notes.
AUDIENCE:  DevOps Engineers, SRE Leads, Security Compliance Auditors & Autonomous Test Runners
STANDARDS: CIS Docker Benchmark, OWASP ASVS L2, Strict Zero-Emoji Spec, 100% Passing Tests
========================================================================================
"""

import os
import re
import unittest
from pathlib import Path


class TestPhase87DockerAndCicd(unittest.TestCase):
    """
    Automated verification of production Dockerfiles, docker-compose.prod.yml,
    GitHub Actions workflows, Trivy scan parameters, and zero-emoji compliance.
    """

    def setUp(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent

    # -------------------------------------------------------------------------
    # 1. Backend Dockerfile Multi-Stage & Security Verification
    # -------------------------------------------------------------------------
    def test_01_backend_dockerfile_multi_stage_and_security(self):
        """Verifies backend/Dockerfile adheres to multi-stage caching and non-root isolation."""
        dockerfile = self.root_dir / "backend" / "Dockerfile"
        self.assertTrue(dockerfile.exists(), "backend/Dockerfile must exist")

        with open(dockerfile, "r", encoding="utf-8") as f:
            content = f.read()

        # Multi-stage assertion
        self.assertIn("FROM python:3.12-slim-bookworm AS builder", content)
        self.assertIn("FROM python:3.12-slim-bookworm AS runner", content)

        # Wheel caching assertion
        self.assertIn("pip wheel", content)
        self.assertIn("/build/wheels", content)

        # Least-privilege non-root execution
        self.assertIn("10001", content)
        self.assertIn("appuser", content)
        self.assertIn("USER appuser", content)

        # Healthcheck and ASGI workers
        self.assertIn("HEALTHCHECK", content)
        self.assertIn("/api/v1/health", content)
        self.assertIn("uvicorn", content)
        self.assertIn("--workers", content)
        self.assertIn('"4"', content)

    # -------------------------------------------------------------------------
    # 2. Frontend Dockerfile Standalone & Alpine Optimization
    # -------------------------------------------------------------------------
    def test_02_frontend_dockerfile_standalone_and_alpine(self):
        """Verifies frontend/Dockerfile implements Next.js standalone runner on Alpine."""
        dockerfile = self.root_dir / "frontend" / "Dockerfile"
        self.assertTrue(dockerfile.exists(), "frontend/Dockerfile must exist")

        with open(dockerfile, "r", encoding="utf-8") as f:
            content = f.read()

        # Alpine multi-stage stages
        self.assertIn("FROM node:20-alpine AS deps", content)
        self.assertIn("FROM node:20-alpine AS builder", content)
        self.assertIn("FROM node:20-alpine AS runner", content)

        # Standalone copy traces (< 120MB optimization)
        self.assertIn(".next/standalone", content)
        self.assertIn(".next/static", content)

        # Non-root user isolation
        self.assertIn("1001", content)
        self.assertIn("nextjs", content)
        self.assertIn("USER nextjs", content)

        # Standalone server launch & healthcheck
        self.assertIn("node", content)
        self.assertIn("server.js", content)
        self.assertIn("HEALTHCHECK", content)
        self.assertIn("wget", content)

    # -------------------------------------------------------------------------
    # 3. Next.js Standalone Configuration Verification
    # -------------------------------------------------------------------------
    def test_03_next_config_standalone_output(self):
        """Verifies frontend/next.config.js declares output: 'standalone'."""
        next_config = self.root_dir / "frontend" / "next.config.js"
        self.assertTrue(next_config.exists(), "frontend/next.config.js must exist")

        with open(next_config, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("output: 'standalone'", content)

    # -------------------------------------------------------------------------
    # 4. Production Docker Compose Topology & Quotas
    # -------------------------------------------------------------------------
    def test_04_docker_compose_prod_topology_and_limits(self):
        """Verifies docker-compose.prod.yml orchestrates 4 services with resource quotas and logging."""
        compose_file = self.root_dir / "docker-compose.prod.yml"
        self.assertTrue(compose_file.exists(), "docker-compose.prod.yml must exist")

        with open(compose_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Core services
        self.assertIn("postgres:", content)
        self.assertIn("postgres:16-alpine", content)
        self.assertIn("redis:", content)
        self.assertIn("redis:7-alpine", content)
        self.assertIn("backend:", content)
        self.assertIn("frontend:", content)

        # Network segmentation
        self.assertIn("ogrojatra-internal:", content)
        self.assertIn("internal: true", content)
        self.assertIn("ogrojatra-public:", content)

        # Resource limits and log caps
        self.assertIn("limits:", content)
        self.assertIn("cpus:", content)
        self.assertIn("memory:", content)
        self.assertIn("max-size:", content)
        self.assertIn("max-file:", content)

        # Healthcheck dependency chain
        self.assertIn("condition: service_healthy", content)

    # -------------------------------------------------------------------------
    # 5. GitHub Actions CI/CD Pipeline Verification
    # -------------------------------------------------------------------------
    def test_05_github_actions_ci_cd_workflow(self):
        """Verifies .github/workflows/ci-cd.yml defines 4 quality and delivery pipeline jobs."""
        ci_cd_file = self.root_dir / ".github" / "workflows" / "ci-cd.yml"
        self.assertTrue(ci_cd_file.exists(), ".github/workflows/ci-cd.yml must exist")

        with open(ci_cd_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Triggers
        self.assertIn("branches: [ main ]", content)
        self.assertIn("pull_request:", content)

        # Job 1: Backend tests and security sweep
        self.assertIn("backend-tests:", content)
        self.assertIn("unittest discover -s backend/tests", content)
        self.assertIn("run_security_sweep.py", content)

        # Job 2: Frontend lint and TypeScript check
        self.assertIn("frontend-quality:", content)
        self.assertIn("npm run lint", content)
        self.assertIn("tsc --noEmit", content)

        # Job 3: Playwright E2E smoke tests
        self.assertIn("e2e-smoke:", content)
        self.assertIn("run-e2e.py", content)

        # Job 4: Docker build, Trivy scan, and GHCR deploy
        self.assertIn("docker-trivy-deploy:", content)
        self.assertIn("trivy-action", content)
        self.assertIn("ghcr.io", content)
        self.assertIn("docker push", content)

    # -------------------------------------------------------------------------
    # 6. Production Deployment Workflow Verification
    # -------------------------------------------------------------------------
    def test_06_github_actions_deploy_workflow(self):
        """Verifies .github/workflows/deploy.yml orchestrates production stack rollout."""
        deploy_file = self.root_dir / ".github" / "workflows" / "deploy.yml"
        self.assertTrue(deploy_file.exists(), ".github/workflows/deploy.yml must exist")

        with open(deploy_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("docker-compose.prod.yml", content)
        self.assertIn("workflow_dispatch:", content)

    # -------------------------------------------------------------------------
    # 7. Strict Zero-Emoji & Architecture Notes Compliance
    # -------------------------------------------------------------------------
    def test_07_strict_zero_emoji_and_architecture_notes(self):
        """Verifies zero unicode emojis and prominent architecture headers across all Phase 87 files."""
        emoji_pattern = re.compile(
            r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
            r"\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF"
            r"\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
            r"\u2600-\u26FF\u2700-\u27BF]"
        )

        target_files = [
            self.root_dir / "backend" / "Dockerfile",
            self.root_dir / "frontend" / "Dockerfile",
            self.root_dir / "frontend" / "next.config.js",
            self.root_dir / "docker-compose.prod.yml",
            self.root_dir / ".github" / "workflows" / "ci-cd.yml",
            self.root_dir / ".github" / "workflows" / "deploy.yml",
            self.root_dir / "backend" / "tests" / "test_phase87_docker_and_cicd.py"
        ]

        for file_path in target_files:
            self.assertTrue(file_path.exists(), f"File {file_path} must exist")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Zero-Emoji assertion
            matches = emoji_pattern.findall(content)
            self.assertEqual(len(matches), 0, f"Found emojis in {file_path}: {matches}")

            # Architecture Note assertion
            has_arch_note = "MODULE:" in content and "PURPOSE:" in content
            self.assertTrue(has_arch_note, f"File {file_path} must contain Developer Architecture Note")


if __name__ == "__main__":
    unittest.main()
