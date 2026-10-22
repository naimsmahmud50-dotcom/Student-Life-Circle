"""
Unit, integration, and security tests for Phase 38:
- Post-Quantum Cryptography & Lattice Key Encapsulation (ML-KEM / Kyber-768)
- Smart Renewable Micro-Grid Dispatch Simulator (Solar PV + LiFePO4 BESS)
- Decentralized Carbon Offset Registry & Verifiable Green Certificate Ledger
"""

import asyncio
import unittest

from backend.app.services.post_quantum_cryptography_service import PostQuantumCryptographyService
from backend.app.services.smart_grid_renewable_service import SmartGridRenewableDispatchService
from backend.app.services.decentralized_carbon_offset_service import DecentralizedCarbonOffsetService

from backend.app.schemas.pqc_smartgrid_and_carbon_schema import (
    PqcKeyGenRequest,
    PqcEncapsulateRequest,
    PqcDecapsulateRequest,
    PqcQuantumSecurityAssessmentRequest,
    SolarPvCalcRequest,
    MicroGridDispatchRequest,
    CarbonOffsetMintRequest,
    CarbonOffsetRetireRequest
)

from backend.app.api.v1.router import (
    generate_pqc_keypair,
    encapsulate_pqc_shared_secret,
    decapsulate_pqc_shared_secret,
    benchmark_pqc_quantum_security,
    calculate_solar_power,
    simulate_microgrid_24h_dispatch,
    mint_carbon_offset_certificate,
    retire_carbon_offset_certificate,
    verify_carbon_offset_certificate,
    get_carbon_registry_summary
)


class TestPhase38PqcSmartGridAndCarbon(unittest.TestCase):

    def setUp(self):
        DecentralizedCarbonOffsetService.reset_ledger_for_testing()

    # -------------------------------------------------------------------------
    # 1. Post-Quantum Cryptography (ML-KEM-768) Tests
    # -------------------------------------------------------------------------

    def test_pqc_keygen_nist_parameters(self):
        kp = PostQuantumCryptographyService.generate_keypair()
        self.assertEqual(kp["algorithm"], "ML-KEM-768")
        self.assertEqual(kp["security_level_nist"], 3)
        self.assertEqual(kp["classical_security_bits"], 192)
        self.assertEqual(kp["quantum_security_bits"], 180)
        self.assertEqual(kp["dimension_k"], 3)
        self.assertEqual(kp["modulus_q"], 3329)
        self.assertEqual(kp["degree_n"], 256)
        self.assertTrue(kp["public_key_fingerprint"].startswith("PQC-KEM768-"))
        self.assertTrue(len(kp["public_key_hex"]) > 100)
        self.assertTrue(len(kp["secret_key_hex"]) > 100)

    def test_pqc_deterministic_keygen_with_seed(self):
        kp1 = PostQuantumCryptographyService.generate_keypair(seed="reproducible-seed-abc")
        kp2 = PostQuantumCryptographyService.generate_keypair(seed="reproducible-seed-abc")
        kp3 = PostQuantumCryptographyService.generate_keypair(seed="different-seed-xyz")

        self.assertEqual(kp1["public_key_hex"], kp2["public_key_hex"])
        self.assertEqual(kp1["secret_key_hex"], kp2["secret_key_hex"])
        self.assertNotEqual(kp1["public_key_hex"], kp3["public_key_hex"])

    def test_pqc_encapsulation_success(self):
        kp = PostQuantumCryptographyService.generate_keypair(seed="encap-test-seed")
        enc = PostQuantumCryptographyService.encapsulate(kp["public_key_hex"])

        self.assertEqual(enc["algorithm"], "ML-KEM-768")
        self.assertEqual(enc["status"], "ENCAPSULATION_SUCCESS")
        self.assertEqual(enc["shared_secret_bits"], 256)
        self.assertTrue(enc["ciphertext_fingerprint"].startswith("CT-KEM768-"))
        self.assertEqual(len(enc["shared_secret_hex"]), 64)

    def test_pqc_decapsulation_roundtrip_and_constant_time(self):
        kp = PostQuantumCryptographyService.generate_keypair(seed="roundtrip-seed-456")
        enc = PostQuantumCryptographyService.encapsulate(kp["public_key_hex"], message_seed="msg-seed-fixed")
        decap = PostQuantumCryptographyService.decapsulate(kp["secret_key_hex"], enc["ciphertext_hex"])

        self.assertTrue(decap["is_valid"])
        self.assertTrue(decap["constant_time_verified"])
        self.assertEqual(decap["status"], "DECAPSULATION_SUCCESS")
        self.assertTrue(len(decap["recovered_shared_secret_hex"]) > 0)

    def test_pqc_invalid_key_or_ciphertext_handling(self):
        with self.assertRaises(ValueError):
            PostQuantumCryptographyService.encapsulate("")

        with self.assertRaises(ValueError):
            PostQuantumCryptographyService.encapsulate("short")

        with self.assertRaises(ValueError):
            PostQuantumCryptographyService.decapsulate("", "abcd")

    def test_pqc_quantum_security_benchmarks(self):
        bench_kyber = PostQuantumCryptographyService.analyze_quantum_security("ML-KEM-768")
        self.assertFalse(bench_kyber["shor_vulnerable"])
        self.assertFalse(bench_kyber["grover_vulnerable"])
        self.assertEqual(bench_kyber["classical_security_bits"], 192)

        bench_rsa = PostQuantumCryptographyService.analyze_quantum_security("RSA-2048")
        self.assertTrue(bench_rsa["shor_vulnerable"])
        self.assertEqual(bench_rsa["quantum_security_bits"], 0)

        bench_ecc = PostQuantumCryptographyService.analyze_quantum_security("ECC-SECP256R1")
        self.assertTrue(bench_ecc["shor_vulnerable"])
        self.assertEqual(bench_ecc["quantum_security_bits"], 0)

    # -------------------------------------------------------------------------
    # 2. Smart Grid Renewable Dispatch Tests
    # -------------------------------------------------------------------------

    def test_solar_pv_output_normal_conditions(self):
        res = SmartGridRenewableDispatchService.calculate_solar_pv_output(
            array_area_m2=200.0,
            efficiency=0.20,
            irradiance_w_per_m2=800.0,
            ambient_temp_c=25.0
        )
        self.assertGreater(res["ac_power_kw"], 0.0)
        self.assertGreater(res["cell_temperature_c"], 25.0)
        self.assertGreater(res["hourly_energy_kwh"], 0.0)

    def test_solar_pv_output_extreme_temperature_derating(self):
        res = SmartGridRenewableDispatchService.calculate_solar_pv_output(
            array_area_m2=250.0,
            efficiency=0.21,
            irradiance_w_per_m2=950.0,
            ambient_temp_c=55.0
        )
        self.assertGreater(res["ac_power_kw"], 0.0)
        self.assertGreater(res["thermal_derating_pct"], 0.0)
        self.assertLessEqual(res["thermal_derating_pct"], 50.0)

    def test_solar_pv_zero_irradiance_night(self):
        res = SmartGridRenewableDispatchService.calculate_solar_pv_output(
            array_area_m2=300.0,
            irradiance_w_per_m2=0.0
        )
        self.assertEqual(res["dc_power_kw"], 0.0)
        self.assertEqual(res["ac_power_kw"], 0.0)
        self.assertEqual(res["hourly_energy_kwh"], 0.0)

    def test_smart_grid_24h_dispatch_default_profile(self):
        dispatch = SmartGridRenewableDispatchService.simulate_microgrid_dispatch()
        self.assertEqual(len(dispatch["hourly_dispatch"]), 24)
        self.assertGreater(dispatch["total_load_kwh"], 1000.0)
        self.assertGreater(dispatch["total_solar_generated_kwh"], 100.0)
        self.assertGreater(dispatch["total_battery_charged_kwh"], 0.0)
        self.assertGreater(dispatch["total_battery_discharged_kwh"], 0.0)
        self.assertGreater(dispatch["peak_shaving_reduction_pct"], 0.0)
        self.assertGreater(dispatch["daily_savings_bdt"], 500.0)

    def test_smart_grid_dispatch_soc_limits_respected(self):
        dispatch = SmartGridRenewableDispatchService.simulate_microgrid_dispatch(
            battery_capacity_kwh=100.0,
            battery_initial_soc=0.50
        )
        for hour in dispatch["hourly_dispatch"]:
            soc = hour["battery_soc_pct"]
            self.assertGreaterEqual(soc, 15.0)
            self.assertLessEqual(soc, 95.0)

    def test_smart_grid_dispatch_financial_savings(self):
        dispatch = SmartGridRenewableDispatchService.simulate_microgrid_dispatch()
        self.assertLess(
            dispatch["daily_cost_with_microgrid_bdt"],
            dispatch["daily_baseline_cost_no_microgrid_bdt"]
        )
        self.assertAlmostEqual(
            dispatch["daily_savings_bdt"],
            dispatch["daily_baseline_cost_no_microgrid_bdt"] - dispatch["daily_cost_with_microgrid_bdt"],
            places=1
        )

    # -------------------------------------------------------------------------
    # 3. Decentralized Carbon Offset Registry Tests
    # -------------------------------------------------------------------------

    def test_carbon_avoided_emissions_calculation(self):
        tco2e = DecentralizedCarbonOffsetService.calculate_avoided_emissions(1000.0, 0.635)
        self.assertEqual(tco2e, 0.635)

        tco2e_zero = DecentralizedCarbonOffsetService.calculate_avoided_emissions(0.0)
        self.assertEqual(tco2e_zero, 0.0)

    def test_carbon_certificate_minting_and_hashing(self):
        cert = DecentralizedCarbonOffsetService.mint_certificate(
            student_id="STU-CAMPUS-01",
            project_name="Dormitory Rooftop Solar",
            renewable_energy_kwh=2500.0
        )
        self.assertTrue(cert["certificate_id"].startswith("CERT-CARBON-"))
        self.assertEqual(cert["owner_id"], "STU-CAMPUS-01")
        self.assertEqual(cert["renewable_energy_kwh"], 2500.0)
        self.assertGreater(cert["tco2e_avoided"], 1.0)
        self.assertEqual(cert["status"], "ACTIVE")
        self.assertFalse(cert["is_retired"])
        self.assertTrue(cert["verification_seal"].startswith("SEAL-"))
        self.assertEqual(len(cert["certificate_hash"]), 64)

    def test_carbon_certificate_hash_continuity(self):
        cert1 = DecentralizedCarbonOffsetService.mint_certificate("STU-1", "Project 1", 1000.0)
        cert2 = DecentralizedCarbonOffsetService.mint_certificate("STU-2", "Project 2", 2000.0)

        self.assertEqual(cert1["previous_block_hash"], DecentralizedCarbonOffsetService.GENESIS_BLOCK_HASH)
        self.assertEqual(cert2["previous_block_hash"], cert1["certificate_hash"])

    def test_carbon_certificate_verification_authentic(self):
        cert = DecentralizedCarbonOffsetService.mint_certificate("STU-VERIFY-01", "Lab Solar Microgrid", 1200.0)
        ver = DecentralizedCarbonOffsetService.verify_certificate(cert["certificate_id"])

        self.assertTrue(ver["is_found"])
        self.assertTrue(ver["is_authentic"])
        self.assertFalse(ver["is_retired"])
        self.assertEqual(ver["status"], "ACTIVE")

    def test_carbon_certificate_retirement_lifecycle(self):
        cert = DecentralizedCarbonOffsetService.mint_certificate("STU-RET-01", "Solar Carport Array", 3000.0)
        rcpt = DecentralizedCarbonOffsetService.retire_certificate(
            certificate_id=cert["certificate_id"],
            student_id="STU-RET-01",
            beneficiary_name="Annual Science Fair 2026",
            retirement_reason="Zero-Emission Exhibition Offset"
        )

        self.assertTrue(rcpt["success"])
        self.assertEqual(rcpt["status"], "RETIRED")
        self.assertTrue(rcpt["retirement_receipt_hash"].startswith("RCPT-"))

        # Verify through public verification endpoint
        ver = DecentralizedCarbonOffsetService.verify_certificate(cert["certificate_id"])
        self.assertTrue(ver["is_retired"])
        self.assertEqual(ver["status"], "RETIRED")
        self.assertEqual(ver["retirement_receipt"], rcpt["retirement_receipt_hash"])

    def test_carbon_anti_double_spend_enforcement(self):
        cert = DecentralizedCarbonOffsetService.mint_certificate("STU-DOUBLE-01", "Library Solar Bank", 800.0)
        DecentralizedCarbonOffsetService.retire_certificate(
            certificate_id=cert["certificate_id"],
            student_id="STU-DOUBLE-01",
            beneficiary_name="Event Alpha",
            retirement_reason="Legitimate First Claim"
        )

        # Attempting second retirement must raise ValueError
        with self.assertRaises(ValueError):
            DecentralizedCarbonOffsetService.retire_certificate(
                certificate_id=cert["certificate_id"],
                student_id="STU-DOUBLE-01",
                beneficiary_name="Event Beta",
                retirement_reason="Fraudulent Double-Claim"
            )

    def test_carbon_unauthorized_retirement_rejected(self):
        cert = DecentralizedCarbonOffsetService.mint_certificate("STU-OWNER-TRUE", "Community Biogas", 650.0)
        with self.assertRaises(PermissionError):
            DecentralizedCarbonOffsetService.retire_certificate(
                certificate_id=cert["certificate_id"],
                student_id="STU-IMPOSTOR-FALSE",
                beneficiary_name="Unauthorized Event",
                retirement_reason="Unauthorized Attempt"
            )

    def test_carbon_invalid_inputs_rejected(self):
        with self.assertRaises(ValueError):
            DecentralizedCarbonOffsetService.mint_certificate("", "Project", 100.0)

        with self.assertRaises(ValueError):
            DecentralizedCarbonOffsetService.mint_certificate("STU-01", "", 100.0)

        with self.assertRaises(ValueError):
            DecentralizedCarbonOffsetService.mint_certificate("STU-01", "Project", 0.0)

        with self.assertRaises(ValueError):
            DecentralizedCarbonOffsetService.mint_certificate("STU-01", "Project", -50.0)

        with self.assertRaises(KeyError):
            DecentralizedCarbonOffsetService.retire_certificate("NON-EXISTENT-ID", "STU-01", "Beneficiary", "Reason")

    def test_carbon_summary_aggregation(self):
        DecentralizedCarbonOffsetService.mint_certificate("STU-A", "Proj 1", 1000.0)
        c2 = DecentralizedCarbonOffsetService.mint_certificate("STU-B", "Proj 2", 2000.0)
        DecentralizedCarbonOffsetService.retire_certificate(c2["certificate_id"], "STU-B", "Fair", "Reason")

        summary = DecentralizedCarbonOffsetService.get_ledger_summary()
        self.assertEqual(summary["total_certificates_minted"], 2)
        self.assertEqual(summary["active_offsets_count"], 1)
        self.assertEqual(summary["retired_offsets_count"], 1)
        self.assertEqual(summary["total_renewable_energy_kwh"], 3000.0)
        self.assertGreater(summary["total_tco2e_avoided"], 1.5)

    # -------------------------------------------------------------------------
    # 4. Asynchronous REST Endpoint Integration Tests
    # -------------------------------------------------------------------------

    def test_api_v1_pqc_endpoints(self):
        async def run_async():
            kp_res = await generate_pqc_keypair(PqcKeyGenRequest(seed="api-pqc-seed"))
            self.assertEqual(kp_res["algorithm"], "ML-KEM-768")

            enc_res = await encapsulate_pqc_shared_secret(PqcEncapsulateRequest(
                public_key_hex=kp_res["public_key_hex"]
            ))
            self.assertEqual(enc_res["status"], "ENCAPSULATION_SUCCESS")

            decap_res = await decapsulate_pqc_shared_secret(PqcDecapsulateRequest(
                secret_key_hex=kp_res["secret_key_hex"],
                ciphertext_hex=enc_res["ciphertext_hex"]
            ))
            self.assertTrue(decap_res["is_valid"])

            bench_res = await benchmark_pqc_quantum_security(PqcQuantumSecurityAssessmentRequest(
                algorithm="ML-KEM-768"
            ))
            self.assertFalse(bench_res["shor_vulnerable"])

        asyncio.run(run_async())

    def test_api_v1_smart_grid_endpoints(self):
        async def run_async():
            solar_res = await calculate_solar_power(SolarPvCalcRequest(
                array_area_m2=200.0,
                irradiance_w_per_m2=800.0
            ))
            self.assertGreater(solar_res["ac_power_kw"], 0.0)

            dispatch_res = await simulate_microgrid_24h_dispatch(MicroGridDispatchRequest(
                solar_area_m2=250.0,
                battery_capacity_kwh=100.0
            ))
            self.assertGreater(dispatch_res["total_solar_generated_kwh"], 0.0)
            self.assertGreater(dispatch_res["daily_savings_bdt"], 0.0)

        asyncio.run(run_async())

    def test_api_v1_carbon_endpoints(self):
        async def run_async():
            mint_res = await mint_carbon_offset_certificate(CarbonOffsetMintRequest(
                student_id="STU-API-01",
                project_name="Campus Solar Initiative",
                renewable_energy_kwh=1500.0
            ))
            self.assertTrue(mint_res["certificate_id"].startswith("CERT-CARBON-"))

            ver_res = await verify_carbon_offset_certificate(mint_res["certificate_id"])
            self.assertTrue(ver_res["is_authentic"])

            ret_res = await retire_carbon_offset_certificate(CarbonOffsetRetireRequest(
                certificate_id=mint_res["certificate_id"],
                student_id="STU-API-01",
                beneficiary_name="Campus Conclave",
                retirement_reason="Green Event Offset"
            ))
            self.assertTrue(ret_res["success"])

            summary_res = await get_carbon_registry_summary()
            self.assertGreaterEqual(summary_res["total_certificates_minted"], 1)

        asyncio.run(run_async())


if __name__ == "__main__":
    unittest.main()
