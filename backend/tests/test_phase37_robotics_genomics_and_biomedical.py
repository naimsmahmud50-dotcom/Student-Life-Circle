"""
Unit, Integration, and Security Test Suite: Phase 37
Verifies:
1. EdgeRoboticsDroneSimulatorService (PID attitude dynamics, thrust-to-weight, battery endurance kinetics)
2. GenomicBioinformaticsService (Needleman-Wunsch & Smith-Waterman sequence alignment, CRISPR sgRNA scanner)
3. BiomedicalDiagnosticSandboxService (Confusion matrix, sensitivity/specificity, ROC-AUC curve generation)
4. Section 36 REST Routes in router.py
"""

import unittest
from backend.app.services.edge_robotics_drone_service import (
    EdgeRoboticsDroneSimulatorService,
    edge_robotics_drone_service
)
from backend.app.services.genomic_bioinformatics_service import (
    GenomicBioinformaticsService,
    genomic_bioinformatics_service
)
from backend.app.services.biomedical_diagnostic_service import (
    BiomedicalDiagnosticSandboxService,
    biomedical_diagnostic_service
)
from backend.app.schemas.robotics_genomics_and_biomedical_schema import (
    DronePidSimRequest,
    DroneEnduranceRequest,
    SequenceAlignRequest,
    CrisprGuideScanRequest,
    DiagnosticConfusionMatrixRequest,
    DiagnosticRocCurveRequest
)
from backend.app.api.v1.router import (
    simulate_drone_pid_loop,
    calculate_drone_endurance,
    align_genomic_sequences,
    scan_crispr_guide_rnas,
    evaluate_diagnostic_confusion_matrix,
    tune_diagnostic_threshold_and_roc
)


class TestPhase37RoboticsGenomicsAndBiomedical(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.drone_service = EdgeRoboticsDroneSimulatorService()
        self.genomics_service = GenomicBioinformaticsService()
        self.biomed_service = BiomedicalDiagnosticSandboxService()

    # -------------------------------------------------------------------------
    # 1. EdgeRoboticsDroneSimulatorService Tests
    # -------------------------------------------------------------------------

    def test_simulate_pid_stable(self):
        req = DronePidSimRequest(
            kp=1.2,
            ki=0.05,
            kd=0.35,
            target_angle_deg=15.0,
            initial_angle_deg=0.0,
            dt_seconds=0.02,
            steps=80
        )
        res = self.drone_service.simulate_pid_attitude(req)
        self.assertTrue(res.is_stable)
        self.assertLess(res.steady_state_error_deg, 1.5)
        self.assertGreater(len(res.trajectory_sample), 5)
        self.assertIn("damped", res.status_summary.lower())

    def test_simulate_pid_extreme_overshoot(self):
        req = DronePidSimRequest(
            kp=3.5,
            ki=0.5,
            kd=0.01,  # Low damping causing overshoot
            target_angle_deg=20.0,
            initial_angle_deg=0.0
        )
        res = self.drone_service.simulate_pid_attitude(req)
        self.assertGreater(res.overshoot_pct, 10.0)

    def test_calculate_endurance_standard_quad(self):
        req = DroneEnduranceRequest(
            mass_kg=1.45,
            rotor_count=4,
            battery_capacity_mah=5200.0,
            battery_voltage_v=14.8,
            hover_efficiency_g_per_w=8.2
        )
        res = self.drone_service.calculate_endurance(req)
        self.assertGreater(res.total_weight_n, 14.0)
        self.assertGreater(res.hover_power_watts, 150.0)
        self.assertGreater(res.battery_energy_wh, 70.0)
        self.assertGreater(res.hover_time_minutes, 18.0)
        self.assertEqual(res.flight_readiness, "MISSION_READY")

    def test_calculate_endurance_overweight(self):
        req = DroneEnduranceRequest(
            mass_kg=8.5,
            rotor_count=4,
            battery_capacity_mah=3000.0,
            battery_voltage_v=11.1,
            hover_efficiency_g_per_w=3.0
        )
        res = self.drone_service.calculate_endurance(req)
        self.assertLess(res.hover_time_minutes, 10.0)
        self.assertEqual(res.flight_readiness, "DANGEROUSLY_OVERWEIGHT")

    def test_calculate_endurance_clamped_extremes(self):
        req = DroneEnduranceRequest(
            mass_kg=-5.0,  # Clamped to >= 0.2
            rotor_count=1,  # Clamped to >= 3
            battery_capacity_mah=50.0,  # Clamped to >= 500
            battery_voltage_v=1.0,  # Clamped to >= 3.7
            hover_efficiency_g_per_w=0.5  # Clamped to >= 2.5
        )
        res = self.drone_service.calculate_endurance(req)
        self.assertGreater(res.hover_time_minutes, 0.0)

    # -------------------------------------------------------------------------
    # 2. GenomicBioinformaticsService Tests
    # -------------------------------------------------------------------------

    def test_align_sequences_global_exact(self):
        req = SequenceAlignRequest(
            sequence_a="ATGCGATCGATC",
            sequence_b="ATGCGATCGATC",
            alignment_type="GLOBAL"
        )
        res = self.genomics_service.align_sequences(req)
        self.assertEqual(res.alignment_type, "GLOBAL")
        self.assertEqual(res.identity_pct, 100.0)
        self.assertEqual(res.mismatches, 0)
        self.assertEqual(res.gaps, 0)

    def test_align_sequences_global_mismatch_and_gap(self):
        req = SequenceAlignRequest(
            sequence_a="ATGCGTAC",
            sequence_b="ATACGTAC",
            alignment_type="GLOBAL"
        )
        res = self.genomics_service.align_sequences(req)
        self.assertGreater(res.identity_pct, 80.0)
        self.assertEqual(res.mismatches, 1)

    def test_align_sequences_local_subsequence(self):
        req = SequenceAlignRequest(
            sequence_a="GGGGATGCGTACGGGG",
            sequence_b="CCCCATGCGTACCCCC",
            alignment_type="LOCAL"
        )
        res = self.genomics_service.align_sequences(req)
        self.assertEqual(res.alignment_type, "LOCAL")
        self.assertIn("ATGCGTAC", res.aligned_seq_a)

    def test_align_sequences_bounded_dos_protection(self):
        enormous_seq = "ATGC" * 1000  # 4,000 nt
        req = SequenceAlignRequest(sequence_a=enormous_seq, sequence_b=enormous_seq)
        res = self.genomics_service.align_sequences(req)
        self.assertLessEqual(len(res.aligned_seq_a), self.genomics_service.MAX_ALIGNMENT_LEN)

    def test_scan_crispr_guides_standard(self):
        # Target with 20nt + AGG PAM
        dna = "ATGCGTACCGGATCGATCGAAGGTCGATCGG"
        req = CrisprGuideScanRequest(target_dna_sequence=dna)
        res = self.genomics_service.scan_crispr_guides(req)
        self.assertGreater(res.target_length_nt, 25)
        self.assertIn("U", res.transcribed_mrna)
        self.assertGreater(res.melting_temperature_c, 50.0)
        self.assertGreaterEqual(res.guide_count, 1)
        self.assertEqual(len(res.guides[0]["protospacer_20nt"]), 20)
        self.assertTrue(res.guides[0]["pam_motif"].endswith("GG"))

    def test_scan_crispr_guides_short_fallback(self):
        req = CrisprGuideScanRequest(target_dna_sequence="ATGC")
        res = self.genomics_service.scan_crispr_guides(req)
        self.assertGreaterEqual(res.target_length_nt, 23)

    # -------------------------------------------------------------------------
    # 3. BiomedicalDiagnosticSandboxService Tests
    # -------------------------------------------------------------------------

    def test_evaluate_confusion_matrix_standard(self):
        req = DiagnosticConfusionMatrixRequest(
            true_positives=185,
            false_positives=15,
            true_negatives=280,
            false_negatives=20
        )
        res = self.biomed_service.evaluate_confusion_matrix(req)
        self.assertEqual(res.total_samples, 500)
        self.assertGreaterEqual(res.sensitivity_tpr, 0.90)  # 185 / 205 = 0.902
        self.assertGreaterEqual(res.specificity_tnr, 0.94)  # 280 / 295 = 0.949
        self.assertGreaterEqual(res.f1_score, 0.90)
        self.assertEqual(res.diagnostic_tier, "CLINICALLY_VALIDATED")

    def test_evaluate_confusion_matrix_zero_division_protection(self):
        req = DiagnosticConfusionMatrixRequest(
            true_positives=0,
            false_positives=0,
            true_negatives=0,
            false_negatives=0
        )
        res = self.biomed_service.evaluate_confusion_matrix(req)
        self.assertGreater(res.total_samples, 0)
        self.assertIsInstance(res.sensitivity_tpr, float)

    def test_generate_roc_curve_trapezoidal_auc(self):
        req = DiagnosticRocCurveRequest(
            disease_name="Pulmonary Tuberculosis (Chest X-Ray)",
            current_threshold=0.50
        )
        res = self.biomed_service.generate_roc_curve(req)
        self.assertEqual(res.disease_name, "Pulmonary Tuberculosis (Chest X-Ray)")
        self.assertGreaterEqual(res.auc_roc, 0.88)
        self.assertLessEqual(res.auc_roc, 1.0)
        self.assertEqual(len(res.curve_points), 11)
        self.assertIn("Youden", res.clinical_recommendation)

    def test_generate_roc_curve_threshold_tuning(self):
        req_sens = DiagnosticRocCurveRequest(current_threshold=0.20)
        res_sens = self.biomed_service.generate_roc_curve(req_sens)
        self.assertGreater(res_sens.operating_point_sensitivity, 0.95)
        self.assertIn("Rule-Out", res_sens.clinical_recommendation)

        req_spec = DiagnosticRocCurveRequest(current_threshold=0.80)
        res_spec = self.biomed_service.generate_roc_curve(req_spec)
        self.assertGreater(res_spec.operating_point_specificity, 0.95)
        self.assertIn("Rule-In", res_spec.clinical_recommendation)

    # -------------------------------------------------------------------------
    # 4. Section 36 REST Router Tests (Async Integration)
    # -------------------------------------------------------------------------

    async def test_api_drone_pid_simulate(self):
        req = DronePidSimRequest(target_angle_deg=10.0)
        res = await simulate_drone_pid_loop(req)
        self.assertTrue(res.is_stable)

    async def test_api_drone_endurance_calculate(self):
        req = DroneEnduranceRequest(mass_kg=1.5)
        res = await calculate_drone_endurance(req)
        self.assertIn(res.flight_readiness, ["MISSION_READY", "SUB_OPTIMAL", "DANGEROUSLY_OVERWEIGHT"])

    async def test_api_genomics_sequence_align(self):
        req = SequenceAlignRequest(sequence_a="ATGC", sequence_b="ATGC")
        res = await align_genomic_sequences(req)
        self.assertEqual(res.identity_pct, 100.0)

    async def test_api_genomics_crispr_scan(self):
        req = CrisprGuideScanRequest(target_dna_sequence="ATGCGTACCGGATCGATCGATCGGATCGAATCGATCGG")
        res = await scan_crispr_guide_rnas(req)
        self.assertGreater(res.guide_count, 0)

    async def test_api_biomedical_evaluate_roc(self):
        req = DiagnosticConfusionMatrixRequest(true_positives=100, false_positives=10, true_negatives=100, false_negatives=10)
        res = await evaluate_diagnostic_confusion_matrix(req)
        self.assertGreater(res.f1_score, 0.85)

    async def test_api_biomedical_threshold_tune(self):
        req = DiagnosticRocCurveRequest(current_threshold=0.50)
        res = await tune_diagnostic_threshold_and_roc(req)
        self.assertGreater(res.auc_roc, 0.85)


if __name__ == '__main__':
    unittest.main()
