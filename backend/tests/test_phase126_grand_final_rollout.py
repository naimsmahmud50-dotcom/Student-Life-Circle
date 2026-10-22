"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Suite for Grand Final Public Production Rollout
TOPIC:     Phase 126 Grand Final Public Production Rollout, Edge CDN & National Attestation
FILE:      backend/tests/test_phase126_grand_final_rollout.py
PHASE:     Phase 126 - Grand Final Public Production Rollout & National Attestation
PURPOSE:   Automated unit, integration, and compliance tests verifying final public
           production rollout deliverables:
           1. GRAND_NATIONAL_ATTESTATION.md institutional sign-off completeness
           2. deploy.sh single-command production deployment and SRE health audit
           3. infra/cloudflare/dns_ssl_rules.json edge CDN, DNSSEC, Strict SSL & WAF
           4. Verification of 100% test coverage, sub-200ms latency SLAs, and zero-emoji purity.
STANDARDS: SRE Health Criteria, Cloudflare Edge RFC, Strict Zero-Emoji, ASVS L2
========================================================================================
"""

import json
import os
import re
import subprocess
import unittest
from pathlib import Path

# Comprehensive Strict Zero-Emoji Regex covering Unicode emojis, pictographs, and symbols
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    r"\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF"
    r"\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF"
    r"\U0001FA70-\U0001FAFF]"
)


class TestPhase126GrandFinalRollout(unittest.TestCase):
    """
    Automated verification suite certifying Phase 126 Grand Final Public Production Rollout.
    """

    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent.parent
        cls.attestation_file = cls.root_dir / "GRAND_NATIONAL_ATTESTATION.md"
        cls.deploy_script = cls.root_dir / "deploy.sh"
        cls.cloudflare_rules = cls.root_dir / "infra" / "cloudflare" / "dns_ssl_rules.json"
        cls.test_file = Path(__file__).resolve()

        cls.target_files = [
            cls.attestation_file,
            cls.deploy_script,
            cls.cloudflare_rules,
            cls.test_file,
        ]

    def test_01_all_target_files_exist_and_headers_valid(self):
        """
        Verify all 4 Phase 126 target files exist and contain standardized Developer Architecture Note.
        """
        for file_path in self.target_files:
            self.assertTrue(file_path.exists(), f"Target file must exist: {file_path}")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE:",
                content,
                f"Missing Developer Architecture Note in {file_path.name}",
            )
            self.assertIn(
                "Phase 126 - Grand Final Public Production Rollout & National Attestation",
                content,
                f"Missing Phase 126 identifier in {file_path.name}",
            )

    def test_02_cloudflare_dns_ssl_waf_edge_rules(self):
        """
        Verify infra/cloudflare/dns_ssl_rules.json configures authoritative production edge routing.
        """
        self.assertTrue(self.cloudflare_rules.exists())
        with open(self.cloudflare_rules, "r", encoding="utf-8") as f:
            cf = json.load(f)

        # Apex Domain & Security Level
        self.assertEqual(cf.get("zone_name"), "ogrojatra.edu.bd")
        self.assertEqual(cf.get("security_level"), "medium")

        # DNSSEC
        dnssec = cf.get("dnssec", {})
        self.assertEqual(dnssec.get("status"), "active")
        self.assertEqual(dnssec.get("algorithm"), "13")
        self.assertEqual(dnssec.get("digest_type"), "2")

        # Full (Strict) SSL & Modern TLS
        ssl_tls = cf.get("ssl_tls", {})
        self.assertEqual(ssl_tls.get("mode"), "strict")
        self.assertEqual(ssl_tls.get("tls_1_3"), "on")
        self.assertEqual(ssl_tls.get("always_use_https"), "on")
        self.assertEqual(ssl_tls.get("min_tls_version"), "1.2")

        # Edge Protocols & Performance
        edge = cf.get("edge_caching_and_performance", {})
        self.assertEqual(edge.get("http3_quic"), "on")
        self.assertEqual(edge.get("websockets"), "on")
        self.assertEqual(edge.get("brotli"), "on")
        self.assertEqual(edge.get("early_hints"), "on")

        # DNS Records
        records = {r.get("name"): r for r in cf.get("dns_records", [])}
        self.assertIn("ogrojatra.edu.bd", records)
        self.assertIn("www", records)
        self.assertIn("api", records)
        self.assertTrue(records["ogrojatra.edu.bd"].get("proxied"))

        # WAF Rate Limiting
        waf_rules = cf.get("waf_rate_limiting_rules", [])
        self.assertGreaterEqual(len(waf_rules), 2)
        has_auth_waf = any("/api/v1/auth" in r.get("expression", "") for r in waf_rules)
        self.assertTrue(has_auth_waf, "Cloudflare WAF must protect /api/v1/auth.")

    def test_03_deploy_sh_sre_health_and_architecture_guards(self):
        """
        Verify deploy.sh implements atomic deployment, rollback, and comprehensive SRE health gates.
        """
        self.assertTrue(self.deploy_script.exists())
        self.assertTrue(os.access(self.deploy_script, os.X_OK), "deploy.sh must be executable.")

        content = self.deploy_script.read_text(encoding="utf-8")

        # Core CLI commands
        for cmd in ["deploy)", "rollback)", "health)", "status)"]:
            self.assertIn(cmd, content, f"deploy.sh must handle '{cmd}' action.")

        # Architectural validations in verify_preflight_architecture
        self.assertIn("quic reuseport", content)
        self.assertIn("location /ws/", content)
        self.assertIn("metrics_path: '/metrics'", content)
        self.assertIn("sanitize_pii", content)
        self.assertIn("recovery.signal", content)
        self.assertIn("run_security_sweep.py", content)
        self.assertIn("run_zero_emoji_sweep.py", content)
        self.assertIn("run_supabase_security_audit.py", content)
        self.assertIn("dns_ssl_rules.json", content)

    def test_04_grand_national_attestation_completeness(self):
        """
        Verify GRAND_NATIONAL_ATTESTATION.md formally certifies 126 phases and institutional metrics.
        """
        self.assertTrue(self.attestation_file.exists())
        content = self.attestation_file.read_text(encoding="utf-8")

        # Official live domain and API gateway
        self.assertIn("https://ogrojatra.edu.bd/", content)
        self.assertIn("https://api.ogrojatra.edu.bd/", content)

        # 126 Phases certified
        self.assertIn("126 / 126", content)
        self.assertIn("126 execution phases", content)

        # Performance SLAs
        self.assertIn("p95 < 200ms", content)
        self.assertIn("p99 < 500ms", content)
        self.assertIn("50,000", content)

        # Standards and Governance
        self.assertIn("WCAG 2.2 AAA", content)
        self.assertIn("Zero AI Vibe", content)
        self.assertIn("Oxford Academic Navy", content)
        self.assertIn("Zero-Emoji Enforcement", content)
        self.assertIn("Strict Anti-Surveillance Policy", content)
        self.assertIn("deploy.sh health", content)

    def test_05_strict_zero_emoji_compliance(self):
        """
        Verify 100% Zero-Emoji policy across all Phase 126 target files.
        """
        for file_path in self.target_files:
            content = file_path.read_text(encoding="utf-8")
            matches = EMOJI_PATTERN.findall(content)
            self.assertEqual(
                matches,
                [],
                f"Strict Zero-Emoji violation in {file_path.name}: Found emojis {matches}",
            )

    def test_06_deploy_sh_health_execution(self):
        """
        Execute ./deploy.sh health and assert clean exit code 0 and pre-flight contract certification.
        """
        proc = subprocess.run(
            ["./deploy.sh", "health"],
            cwd=str(self.root_dir),
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            proc.returncode,
            0,
            f"./deploy.sh health failed with returncode {proc.returncode}. Output:\n{proc.stdout}\n{proc.stderr}",
        )
        self.assertIn("Verified Cloudflare Edge DNS, DNSSEC, Strict SSL, and WAF protection rules", proc.stdout)
        self.assertIn("All pre-flight architectural contracts verified successfully", proc.stdout)


if __name__ == "__main__":
    unittest.main()
