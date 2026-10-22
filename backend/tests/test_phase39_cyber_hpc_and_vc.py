"""
Unit, integration, and security tests for Phase 39:
- Autonomous Cyber Range & Zero-Trust Defense Sandbox
- High-Performance Computing (HPC) Parallel Job Scheduler (Slurm + Amdahl Speedup)
- University Venture Capital Angel Syndicate & SAFE Cap Table Dilution Simulator
"""

import asyncio
import unittest

from backend.app.services.cyber_range_zero_trust_service import CyberRangeZeroTrustService
from backend.app.services.hpc_cluster_scheduler_service import HpcClusterSchedulerService
from backend.app.services.university_vc_syndicate_service import UniversityVcAngelSyndicateService

from backend.app.schemas.cyber_hpc_and_vc_schema import (
    ZeroTrustEvaluationRequest,
    ThreatDetectionRequest,
    HpcJobSubmitRequest,
    AmdahlSpeedupCalcRequest,
    SafeDilutionCalcRequest,
    AngelCommitmentRequest
)

from backend.app.api.v1.router import (
    evaluate_zero_trust_access,
    inspect_and_sanitize_payload_threat,
    submit_hpc_compute_job,
    calculate_amdahl_parallel_speedup,
    get_hpc_cluster_status,
    calculate_safe_cap_table_dilution,
    register_angel_syndicate_commitment,
    list_startup_syndicate_commitments
)


class TestPhase39CyberHpcAndVc(unittest.TestCase):

    def setUp(self):
        CyberRangeZeroTrustService.reset_forensics_for_testing()
        HpcClusterSchedulerService.reset_queue_for_testing()
        UniversityVcAngelSyndicateService.reset_syndicate_for_testing()

    # -------------------------------------------------------------------------
    # 1. Zero-Trust Cyber Range & Threat Detection Tests
    # -------------------------------------------------------------------------

    def test_zero_trust_pristine_session(self):
        eval_res = CyberRangeZeroTrustService.evaluate_zero_trust_access(
            student_id="STU-PRISTINE-01",
            device_fingerprint="sha256-device-posture-trusted-hardware",
            ip_address="127.0.0.1",
            mfa_authenticated=True,
            geo_velocity_kmh=0.0
        )
        self.assertEqual(eval_res["trust_score"], 100.0)
        self.assertTrue(eval_res["access_granted"])
        self.assertEqual(eval_res["decision"], "ALLOW")
        self.assertEqual(eval_res["threat_level"], "LOW")
        self.assertEqual(len(eval_res["anomaly_flags"]), 0)

    def test_zero_trust_mfa_missing_penalty(self):
        eval_res = CyberRangeZeroTrustService.evaluate_zero_trust_access(
            student_id="STU-NO-MFA",
            device_fingerprint="sha256-device-posture-trusted-hardware",
            mfa_authenticated=False
        )
        self.assertEqual(eval_res["trust_score"], 65.0)
        self.assertFalse(eval_res["access_granted"])
        self.assertEqual(eval_res["decision"], "CHALLENGE_STEP_UP_MFA")
        self.assertIn("MFA_NOT_PRESENT", eval_res["anomaly_flags"])

    def test_zero_trust_impossible_travel_anomaly(self):
        eval_res = CyberRangeZeroTrustService.evaluate_zero_trust_access(
            student_id="STU-TRAVEL-ANOMALY",
            device_fingerprint="sha256-device-posture-trusted-hardware",
            geo_velocity_kmh=1200.0
        )
        self.assertLess(eval_res["trust_score"], 60.0)
        self.assertIn("IMPOSSIBLE_TRAVEL_SPEED_EXCEEDED", eval_res["anomaly_flags"])

    def test_zero_trust_sql_injection_detection_and_denial(self):
        eval_res = CyberRangeZeroTrustService.evaluate_zero_trust_access(
            student_id="STU-ATTACKER-SQLI",
            device_fingerprint="short-device",
            payload_sample="' UNION SELECT username, password_hash FROM admin_users--"
        )
        self.assertEqual(eval_res["decision"], "DENY")
        self.assertFalse(eval_res["access_granted"])
        self.assertTrue(any("THREAT_DETECTED:SQL_INJECTION" in flag for flag in eval_res["anomaly_flags"]))

    def test_payload_threat_scanner_xss_and_sanitization(self):
        xss_payload = "<script>alert('XSS-Exploit')</script>"
        res = CyberRangeZeroTrustService.inspect_and_sanitize_payload(xss_payload, "BODY")

        self.assertTrue(res["is_malicious"])
        self.assertIn("CROSS_SITE_SCRIPTING", res["attack_types"])
        self.assertIn("&lt;script&gt;", res["sanitized_output"])
        self.assertNotIn("<script>", res["sanitized_output"])

    def test_payload_threat_scanner_path_traversal_and_jwt_none(self):
        traversal = "../../etc/passwd"
        res_trav = CyberRangeZeroTrustService.inspect_and_sanitize_payload(traversal)
        self.assertTrue(res_trav["is_malicious"])
        self.assertIn("PATH_TRAVERSAL", res_trav["attack_types"])

        jwt_none = '{"alg": "none", "typ": "JWT"}'
        res_jwt = CyberRangeZeroTrustService.inspect_and_sanitize_payload(jwt_none)
        self.assertTrue(res_jwt["is_malicious"])
        self.assertIn("JWT_ALGORITHM_NONE_FORGERY", res_jwt["attack_types"])

    def test_forensics_incident_logging(self):
        CyberRangeZeroTrustService.evaluate_zero_trust_access(
            student_id="STU-ROGUE-01",
            device_fingerprint="bad-device",
            mfa_authenticated=False,
            geo_velocity_kmh=1500.0
        )
        logs = CyberRangeZeroTrustService.get_forensics_log()
        self.assertGreaterEqual(len(logs), 1)
        self.assertEqual(logs[-1]["student_id"], "STU-ROGUE-01")
        self.assertTrue(logs[-1]["event_id"].startswith("INCIDENT-"))

    # -------------------------------------------------------------------------
    # 2. HPC Parallel Scheduler & Amdahl Speedup Tests
    # -------------------------------------------------------------------------

    def test_amdahl_speedup_calculation(self):
        res = HpcClusterSchedulerService.calculate_amdahl_speedup(parallel_fraction=0.95)
        self.assertEqual(res["parallel_fraction"], 0.95)
        self.assertEqual(res["serial_fraction"], 0.05)
        self.assertEqual(res["theoretical_max_speedup"], 20.0)

        # 16 processors speedup check
        proc_16 = [item for item in res["speedup_curve"] if item["processors"] == 16][0]
        self.assertAlmostEqual(proc_16["speedup"], 9.143, places=2)

    def test_amdahl_gustafson_scaling_comparison(self):
        res = HpcClusterSchedulerService.calculate_amdahl_speedup(parallel_fraction=0.90)
        amdahl_64 = [item for item in res["speedup_curve"] if item["processors"] == 64][0]["speedup"]
        gustafson_64 = [item for item in res["gustafson_scaled_speedup"] if item["processors"] == 64][0]["scaled_speedup"]

        # Gustafson weak scaling should exceed Amdahl strong scaling limit
        self.assertGreater(gustafson_64, amdahl_64)

    def test_amdahl_edge_case_zero_parallel(self):
        res = HpcClusterSchedulerService.calculate_amdahl_speedup(parallel_fraction=0.0)
        self.assertEqual(res["theoretical_max_speedup"], 1.0)
        for item in res["speedup_curve"]:
            self.assertEqual(item["speedup"], 1.0)

    def test_hpc_job_submission_h100(self):
        job = HpcClusterSchedulerService.submit_hpc_job(
            job_name="Genome-Transformer-Large",
            student_id="STU-BIO-01",
            gpu_type="NVIDIA_H100",
            gpu_count=8,
            vram_gb_requested=640.0,
            walltime_minutes=180
        )
        self.assertTrue(job["job_id"].startswith("HPC-JOB-"))
        self.assertEqual(job["gpu_count"], 8)
        self.assertEqual(job["tflops_allocated"], 8 * 989.0)
        self.assertEqual(job["allocated_nodes"], 1)
        self.assertEqual(job["queue_state"], "RUNNING")

    def test_hpc_queue_backfilling_and_wait_estimation(self):
        # Fill queue with 5 jobs
        for i in range(5):
            HpcClusterSchedulerService.submit_hpc_job(
                job_name=f"Job-{i}",
                student_id=f"STU-{i}",
                gpu_count=2
            )
        queue = HpcClusterSchedulerService.list_queue_jobs()
        self.assertEqual(len(queue), 5)
        # 5th job should be PENDING with non-zero estimated wait
        self.assertEqual(queue[4]["queue_state"], "PENDING")
        self.assertGreater(queue[4]["estimated_wait_seconds"], 0)

    def test_hpc_cluster_status_aggregation(self):
        HpcClusterSchedulerService.submit_hpc_job(
            job_name="Vision-SSL-Pretrain",
            student_id="STU-AI-01",
            gpu_count=4
        )
        status = HpcClusterSchedulerService.get_cluster_status()
        self.assertGreater(status["total_cluster_gpus"], 100)
        self.assertEqual(status["allocated_gpus"], 4)
        self.assertGreater(status["active_compute_tflops"], 0.0)

    # -------------------------------------------------------------------------
    # 3. University VC Angel Syndicate & SAFE Dilution Tests
    # -------------------------------------------------------------------------

    def test_safe_dilution_post_money_yc_standard(self):
        res = UniversityVcAngelSyndicateService.calculate_safe_dilution(
            startup_name="EdTech AI Labs",
            safe_type="POST_MONEY_SAFE",
            investment_amount_usd=150000.0,
            valuation_cap_usd=3000000.0,
            existing_founder_shares=8000000
        )
        self.assertEqual(res["investor_equity_pct"], 5.0)
        self.assertEqual(res["founder_equity_pct"], 95.0)
        self.assertEqual(res["post_money_valuation_usd"], 3000000.0)
        self.assertEqual(res["new_shares_issued"], 421053)
        self.assertEqual(res["total_post_shares"], 8421053)

    def test_safe_dilution_pre_money_comparison(self):
        res = UniversityVcAngelSyndicateService.calculate_safe_dilution(
            startup_name="AgroDrone Robotics",
            safe_type="PRE_MONEY_SAFE",
            investment_amount_usd=200000.0,
            valuation_cap_usd=2000000.0,
            existing_founder_shares=8000000
        )
        self.assertAlmostEqual(res["investor_equity_pct"], 9.09, places=1)
        self.assertEqual(res["post_money_valuation_usd"], 2200000.0)

    def test_safe_dilution_zero_or_negative_inputs_rejected(self):
        with self.assertRaises(ValueError):
            UniversityVcAngelSyndicateService.calculate_safe_dilution(valuation_cap_usd=0.0)

        with self.assertRaises(ValueError):
            UniversityVcAngelSyndicateService.calculate_safe_dilution(investment_amount_usd=-500.0)

        with self.assertRaises(ValueError):
            UniversityVcAngelSyndicateService.calculate_safe_dilution(existing_founder_shares=0)

    def test_angel_commitment_registration_and_progress(self):
        c1 = UniversityVcAngelSyndicateService.register_angel_commitment(
            startup_name="NanoSilicon",
            student_founder_id="STU-FOUNDER-01",
            target_raise_usd=200000.0,
            investor_name="Angel Fund Alpha",
            commitment_amount_usd=50000.0
        )
        self.assertEqual(c1["total_committed_usd"], 50000.0)
        self.assertEqual(c1["funding_progress_pct"], 25.0)
        self.assertEqual(c1["status"], "COMMITTED")
        self.assertTrue(c1["escrow_lock_seal"].startswith("ESCROW-SEAL-"))

        # Second commitment bringing to 100% target
        c2 = UniversityVcAngelSyndicateService.register_angel_commitment(
            startup_name="NanoSilicon",
            student_founder_id="STU-FOUNDER-01",
            target_raise_usd=200000.0,
            investor_name="Venture Syndicate Beta",
            commitment_amount_usd=150000.0
        )
        self.assertEqual(c2["total_committed_usd"], 200000.0)
        self.assertEqual(c2["funding_progress_pct"], 100.0)
        self.assertEqual(c2["status"], "FULLY_SUBSCRIBED")

    def test_angel_commitment_listing(self):
        UniversityVcAngelSyndicateService.register_angel_commitment(
            startup_name="BioCRISPR",
            student_founder_id="STU-GEN-01",
            commitment_amount_usd=30000.0
        )
        commitments = UniversityVcAngelSyndicateService.list_startup_commitments("BioCRISPR")
        self.assertEqual(len(commitments), 1)
        self.assertEqual(commitments[0]["startup_name"], "BioCRISPR")

    # -------------------------------------------------------------------------
    # 4. Asynchronous REST Endpoints Integration Tests
    # -------------------------------------------------------------------------

    def test_api_v1_zero_trust_endpoints(self):
        async def run_async():
            zt_res = await evaluate_zero_trust_access(ZeroTrustEvaluationRequest(
                student_id="STU-API-ZT",
                device_fingerprint="device-fingerprint-posture-valid-1234"
            ))
            self.assertEqual(zt_res["decision"], "ALLOW")

            threat_res = await inspect_and_sanitize_payload_threat(ThreatDetectionRequest(
                payload_text="1 OR '1'='1' --",
                context_type="QUERY"
            ))
            self.assertTrue(threat_res["is_malicious"])
            self.assertIn("SQL_INJECTION", threat_res["attack_types"])

        asyncio.run(run_async())

    def test_api_v1_hpc_endpoints(self):
        async def run_async():
            job_res = await submit_hpc_compute_job(HpcJobSubmitRequest(
                job_name="Distributed-PPO-RL",
                student_id="STU-API-HPC",
                gpu_count=4
            ))
            self.assertTrue(job_res["job_id"].startswith("HPC-JOB-"))

            amd_res = await calculate_amdahl_parallel_speedup(AmdahlSpeedupCalcRequest(
                parallel_fraction=0.96
            ))
            self.assertEqual(amd_res["theoretical_max_speedup"], 25.0)

            status_res = await get_hpc_cluster_status()
            self.assertGreater(status_res["total_cluster_gpus"], 0)

        asyncio.run(run_async())

    def test_api_v1_vc_endpoints(self):
        async def run_async():
            safe_res = await calculate_safe_cap_table_dilution(SafeDilutionCalcRequest(
                startup_name="MedVision AI",
                investment_amount_usd=250000.0,
                valuation_cap_usd=5000000.0
            ))
            self.assertEqual(safe_res["investor_equity_pct"], 5.0)

            commit_res = await register_angel_syndicate_commitment(AngelCommitmentRequest(
                startup_name="MedVision AI",
                student_founder_id="STU-MED-01",
                commitment_amount_usd=100000.0
            ))
            self.assertTrue(commit_res["commitment_id"].startswith("VC-COMMIT-"))

            list_res = await list_startup_syndicate_commitments("MedVision AI")
            self.assertEqual(len(list_res), 1)

        asyncio.run(run_async())


if __name__ == "__main__":
    unittest.main()
