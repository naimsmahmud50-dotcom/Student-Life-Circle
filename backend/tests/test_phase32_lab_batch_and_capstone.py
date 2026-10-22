"""
Unit and Integration Test Suite: Phase 32
Verifies:
1. VirtualScienceLabService (DC circuit simulator, geometric optics ray tracer, acid-base titration, automated lab reports)
2. CoachingBatchPoolService (micro-coaching batch creation, fractional 1/N escrow cost-splitting, attendance telemetry)
3. IndustryCapstoneService (corporate problem briefs, 3-stage milestone progression, PPO conversion tracker)
4. Section 31 REST Routes in router.py
"""

import unittest
from backend.app.services.virtual_science_lab_service import (
    VirtualScienceLabService,
    virtual_science_lab_service
)
from backend.app.services.coaching_batch_pool_service import (
    CoachingBatchPoolService,
    coaching_batch_pool_service
)
from backend.app.services.industry_capstone_service import (
    IndustryCapstoneService,
    industry_capstone_service
)
from backend.app.schemas.lab_batch_and_capstone_schema import (
    CircuitSimulationRequest,
    OpticsRayTraceRequest,
    TitrationSimulationRequest,
    LabReportSynthesisRequest,
    CreateCoachingBatchRequest,
    JoinBatchGuardianRequest,
    LogBatchSessionRequest,
    SubmitCapstoneMilestoneRequest
)
from backend.app.api.v1.router import (
    simulate_dc_circuit,
    trace_optics_ray,
    simulate_acid_base_titration,
    generate_lab_report,
    create_coaching_batch,
    join_coaching_batch,
    log_coaching_session,
    get_coaching_batch_details,
    list_coaching_batches,
    get_capstones_directory,
    get_capstone_details,
    submit_capstone_milestone
)


class TestPhase32LabBatchAndCapstone(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.lab_service = VirtualScienceLabService()
        self.coaching_service = CoachingBatchPoolService()
        self.capstone_service = IndustryCapstoneService()

    # -------------------------------------------------------------------------
    # 1. VirtualScienceLabService Tests
    # -------------------------------------------------------------------------

    def test_circuit_series_simulation(self):
        """Asserts Ohm's & Kirchhoff's laws for series circuit calculations."""
        components = [
            {"id": "R1", "type": "RESISTOR", "value": 10.0},
            {"id": "R2", "type": "RESISTOR", "value": 20.0},
        ]
        res = self.lab_service.simulate_circuit(
            circuit_id="test-series-01",
            source_voltage=12.0,
            configuration="SERIES",
            components=components
        )
        self.assertEqual(res["circuit_id"], "test-series-01")
        self.assertEqual(res["configuration"], "SERIES")
        self.assertEqual(res["total_resistance"], 30.0)
        self.assertAlmostEqual(res["total_current"], 0.4, places=2)
        self.assertAlmostEqual(res["total_power"], 4.8, places=2)
        self.assertTrue(res["is_short_circuit_safe"])
        self.assertEqual(len(res["component_telemetry"]), 2)
        self.assertAlmostEqual(res["component_telemetry"][0]["voltage_drop_volts"], 4.0, places=2)
        self.assertAlmostEqual(res["component_telemetry"][1]["voltage_drop_volts"], 8.0, places=2)

    def test_circuit_parallel_simulation(self):
        """Asserts parallel circuit conductance and branch currents."""
        components = [
            {"id": "R1", "type": "RESISTOR", "value": 10.0},
            {"id": "R2", "type": "RESISTOR", "value": 10.0},
        ]
        res = self.lab_service.simulate_circuit(
            circuit_id="test-parallel-01",
            source_voltage=12.0,
            configuration="PARALLEL",
            components=components
        )
        self.assertEqual(res["configuration"], "PARALLEL")
        self.assertAlmostEqual(res["total_resistance"], 5.0, places=2)
        self.assertAlmostEqual(res["total_current"], 2.4, places=2)
        self.assertTrue(res["is_short_circuit_safe"])

    def test_circuit_short_circuit_protection(self):
        """Asserts zero-resistance short-circuit safety guard avoids ZeroDivisionError."""
        components = [
            {"id": "R1", "type": "RESISTOR", "value": 0.0},
        ]
        res = self.lab_service.simulate_circuit(
            circuit_id="test-short-01",
            source_voltage=12.0,
            configuration="SERIES",
            components=components
        )
        self.assertFalse(res["is_short_circuit_safe"])
        self.assertEqual(res["execution_status"], "WARNING_SHORT_CIRCUIT")
        self.assertGreater(res["total_current"], 0.0)

    def test_optics_convex_real_inverted(self):
        """Asserts convex lens real and inverted image formation when u > f."""
        res = self.lab_service.trace_optics_rays(
            lens_type="CONVEX",
            focal_length_cm=15.0,
            object_distance_cm=30.0,
            object_height_cm=5.0
        )
        self.assertEqual(res["lens_type"], "CONVEX")
        self.assertAlmostEqual(res["image_distance_cm"], 30.0, places=1)
        self.assertAlmostEqual(res["magnification"], -1.0, places=1)
        self.assertEqual(res["image_nature"], "REAL_INVERTED")
        self.assertFalse(res["is_at_focus"])

    def test_optics_convex_virtual_magnified(self):
        """Asserts convex lens virtual upright image formation when u < f."""
        res = self.lab_service.trace_optics_rays(
            lens_type="CONVEX",
            focal_length_cm=15.0,
            object_distance_cm=10.0,
            object_height_cm=5.0
        )
        self.assertAlmostEqual(res["image_distance_cm"], -30.0, places=1)
        self.assertAlmostEqual(res["magnification"], 3.0, places=1)
        self.assertEqual(res["image_nature"], "VIRTUAL_UPRIGHT")
        self.assertFalse(res["is_at_focus"])

    def test_optics_convex_at_focus_singularity(self):
        """Asserts object placed at focus safely reports AT_INFINITY without error."""
        res = self.lab_service.trace_optics_rays(
            lens_type="CONVEX",
            focal_length_cm=15.0,
            object_distance_cm=15.0,
            object_height_cm=5.0
        )
        self.assertTrue(res["is_at_focus"])
        self.assertIsNone(res["image_distance_cm"])
        self.assertEqual(res["image_nature"], "AT_INFINITY")

    def test_optics_concave_virtual_diminished(self):
        """Asserts concave lens produces virtual upright diminished image."""
        res = self.lab_service.trace_optics_rays(
            lens_type="CONCAVE",
            focal_length_cm=15.0,
            object_distance_cm=30.0,
            object_height_cm=6.0
        )
        self.assertEqual(res["lens_type"], "CONCAVE")
        self.assertAlmostEqual(res["image_distance_cm"], -10.0, places=1)
        self.assertAlmostEqual(res["magnification"], 0.333, places=2)
        self.assertEqual(res["image_nature"], "VIRTUAL_UPRIGHT")

    def test_titration_curve_and_equivalence(self):
        """Asserts analytical acid-base titration calculation and equivalence volume."""
        res = self.lab_service.simulate_acid_base_titration(
            analyte="HCl",
            titrant="NaOH",
            analyte_volume_ml=25.0,
            analyte_molarity=0.1,
            titrant_molarity=0.1,
            indicator="PHENOLPHTHALEIN"
        )
        self.assertEqual(res["equivalence_volume_ml"], 25.0)
        self.assertEqual(res["equivalence_ph"], 7.0)
        self.assertLess(res["initial_ph"], 2.0)
        self.assertGreater(res["final_ph"], 11.5)
        self.assertEqual(len(res["titration_curve"]), 21)

    def test_titration_indicator_chromophoric_transition(self):
        """Asserts indicator color change calculation for methyl orange and phenolphthalein."""
        res_ph = self.lab_service.simulate_acid_base_titration(
            indicator="PHENOLPHTHALEIN"
        )
        self.assertEqual(res_ph["titration_curve"][0]["color_state"], "COLORLESS")
        self.assertEqual(res_ph["titration_curve"][-1]["color_state"], "MAGENTA_PINK")

        res_mo = self.lab_service.simulate_acid_base_titration(
            indicator="METHYL_ORANGE"
        )
        self.assertEqual(res_mo["titration_curve"][0]["color_state"], "RED")
        self.assertEqual(res_mo["titration_curve"][-1]["color_state"], "YELLOW")

    def test_generate_lab_report_synthesis(self):
        """Asserts automated report generation with relative percentage error and verification stamp."""
        res = self.lab_service.generate_lab_report(
            lab_type="DC_OHMS_LAW",
            student_id="std-001",
            experimental_value=9.85,
            theoretical_value=10.0,
            observations="Minor resistance from test lead clips."
        )
        self.assertEqual(res["lab_type"], "DC_OHMS_LAW")
        self.assertEqual(res["relative_error_pct"], 1.5)
        self.assertTrue(res["verification_stamp"].startswith("AGR-LAB-"))
        self.assertIn("High experimental precision", res["conclusion"])

    # -------------------------------------------------------------------------
    # 2. CoachingBatchPoolService Tests
    # -------------------------------------------------------------------------

    def test_create_coaching_batch(self):
        """Asserts creating a micro-coaching batch assigns initial 100% share to lead guardian."""
        batch = self.coaching_service.create_batch(
            batch_title="Mirpur HSC 2026 Math Batch",
            subject="Higher Mathematics",
            lead_guardian_id="g-101",
            total_monthly_fee_bdt=6000.0,
            max_capacity=4
        )
        self.assertTrue(batch["batch_id"].startswith("BATCH-"))
        self.assertEqual(batch["current_guardians"], 1)
        self.assertEqual(batch["cost_per_guardian_bdt"], 6000.0)
        self.assertEqual(len(batch["guardian_shares"]), 1)

    def test_join_guardian_dynamic_split(self):
        """Asserts joining a guardian dynamically updates fractional cost-split."""
        batch = self.coaching_service.create_batch(
            batch_title="Sylhet Chemistry Circle",
            subject="Organic Chemistry",
            lead_guardian_id="g-201",
            total_monthly_fee_bdt=6000.0,
            max_capacity=3
        )
        joined = self.coaching_service.join_guardian(
            batch_id=batch["batch_id"],
            guardian_id="g-202",
            guardian_name="Salma Khatun",
            student_name="Nabil Ahmed"
        )
        self.assertEqual(joined["current_guardians"], 2)
        self.assertEqual(joined["cost_per_guardian_bdt"], 3000.0)

    def test_exact_escrow_cent_reconciliation(self):
        """Asserts zero rounding drift leak when fee is divided by 3."""
        batch = self.coaching_service.create_batch(
            batch_title="Chittagong Physics Squad",
            subject="Physics II",
            lead_guardian_id="g-301",
            total_monthly_fee_bdt=5000.0,
            max_capacity=3
        )
        self.coaching_service.join_guardian(batch["batch_id"], "g-302", "Parent 2", "Student 2")
        self.coaching_service.join_guardian(batch["batch_id"], "g-303", "Parent 3", "Student 3")

        details = self.coaching_service.get_batch_details(batch["batch_id"])
        total_allocated = sum(s["allocated_amount_bdt"] for s in details["guardian_shares"])
        self.assertEqual(round(total_allocated, 2), 5000.0)

    def test_batch_capacity_overflow(self):
        """Asserts joining beyond max_capacity raises ValueError."""
        batch = self.coaching_service.create_batch(
            batch_title="Compact Biology Batch",
            subject="Botany",
            lead_guardian_id="g-401",
            total_monthly_fee_bdt=4000.0,
            max_capacity=2
        )
        self.coaching_service.join_guardian(batch["batch_id"], "g-402", "Parent 2", "Student 2")
        with self.assertRaises(ValueError):
            self.coaching_service.join_guardian(batch["batch_id"], "g-403", "Parent 3", "Student 3")

    def test_duplicate_guardian_prevented(self):
        """Asserts duplicate enrollment with same guardian_id raises ValueError."""
        batch = self.coaching_service.create_batch(
            batch_title="Test Batch",
            subject="English",
            lead_guardian_id="g-501",
            total_monthly_fee_bdt=3000.0
        )
        with self.assertRaises(ValueError):
            self.coaching_service.join_guardian(batch["batch_id"], "g-501", "Duplicate Parent", "Student")

    def test_log_session_attendance_telemetry(self):
        """Asserts session attendance logging and percentage calculation."""
        batch = self.coaching_service.create_batch(
            batch_title="Session Test Batch",
            subject="ICT",
            lead_guardian_id="g-601",
            total_monthly_fee_bdt=3000.0
        )
        self.coaching_service.join_guardian(batch["batch_id"], "g-602", "Parent 2", "Student 2")
        session = self.coaching_service.log_session_attendance(
            batch_id=batch["batch_id"],
            session_topic="Python Functions & Recursion",
            attendees=["g-601", "g-602"],
            duration_minutes=90,
            mentor_notes="Both students finished recursion exercises."
        )
        self.assertEqual(session["attendee_count"], 2)
        self.assertEqual(session["attendance_pct"], 100.0)

    # -------------------------------------------------------------------------
    # 3. IndustryCapstoneService Tests
    # -------------------------------------------------------------------------

    def test_capstone_directory_and_details(self):
        """Asserts directory lists verified corporate capstones and retrieves by ID."""
        directory = self.capstone_service.get_capstone_directory()
        self.assertGreaterEqual(directory["total"], 3)
        cap = self.capstone_service.get_capstone_by_id("CAP-BKASH-01")
        self.assertEqual(cap["corporate_partner"], "bKash FinTech Ltd.")
        self.assertTrue(cap["ppo_opportunity"])

    def test_milestone_url_validation(self):
        """Asserts invalid protocol URLs are rejected to prevent SSRF and protocol smuggling."""
        with self.assertRaises(ValueError):
            self.capstone_service.submit_milestone(
                capstone_id="CAP-BKASH-01",
                student_id="std-sec-01",
                student_name="Security Tester",
                milestone_stage="ARCHITECTURE_PROPOSAL",
                deliverables_url="javascript:alert(1)",
                executive_summary="Malicious injection attempt"
            )

    def test_milestone_progression_enforcement(self):
        """Asserts stage progression cannot skip ARCHITECTURE_PROPOSAL."""
        with self.assertRaises(ValueError):
            self.capstone_service.submit_milestone(
                capstone_id="CAP-BKASH-01",
                student_id="std-jump-01",
                student_name="Jumper Student",
                milestone_stage="PROTOTYPE_DEMO",
                deliverables_url="https://github.com/test/demo",
                executive_summary="Skipped architecture"
            )

    def test_milestone_full_lifecycle_and_ppo(self):
        """Asserts full 3-stage progression unlocks PPO eligibility upon high final score."""
        student_id = "std-capstone-star"
        cap_id = "CAP-BKASH-01"

        # Stage 1
        m1 = self.capstone_service.submit_milestone(
            capstone_id=cap_id,
            student_id=student_id,
            student_name="Star Student",
            milestone_stage="ARCHITECTURE_PROPOSAL",
            deliverables_url="https://github.com/star/arch",
            executive_summary="Event-driven architecture proposal"
        )
        self.assertEqual(m1["status"], "APPROVED")
        self.assertFalse(m1["ppo_eligible"])

        # Stage 2
        m2 = self.capstone_service.submit_milestone(
            capstone_id=cap_id,
            student_id=student_id,
            student_name="Star Student",
            milestone_stage="PROTOTYPE_DEMO",
            deliverables_url="https://github.com/star/proto",
            executive_summary="Async prototype demo"
        )
        self.assertEqual(m2["status"], "APPROVED")
        self.assertFalse(m2["ppo_eligible"])

        # Stage 3
        m3 = self.capstone_service.submit_milestone(
            capstone_id=cap_id,
            student_id=student_id,
            student_name="Star Student",
            milestone_stage="FINAL_DELIVERABLES",
            deliverables_url="https://github.com/star/final",
            executive_summary="Final production deliverables"
        )
        self.assertEqual(m3["status"], "APPROVED")
        self.assertTrue(m3["ppo_eligible"])
        self.assertGreaterEqual(m3["score"], 85.0)

    # -------------------------------------------------------------------------
    # 4. Section 31 REST Routes Tests
    # -------------------------------------------------------------------------

    async def test_api_simulate_circuit(self):
        """Asserts POST /lab/circuit/simulate endpoint returns valid telemetry."""
        req = CircuitSimulationRequest(
            circuit_id="api-ckt-01",
            source_voltage=9.0,
            configuration="SERIES",
            components=[{"id": "R1", "type": "RESISTOR", "value": 18.0}]
        )
        res = await simulate_dc_circuit(payload=req)
        self.assertEqual(res["circuit_id"], "api-ckt-01")
        self.assertEqual(res["total_resistance"], 18.0)
        self.assertEqual(res["total_current"], 0.5)

    async def test_api_trace_optics_ray(self):
        """Asserts POST /lab/optics/ray-trace endpoint returns optical rays."""
        req = OpticsRayTraceRequest(
            lens_type="CONVEX",
            focal_length_cm=20.0,
            object_distance_cm=40.0,
            object_height_cm=4.0
        )
        res = await trace_optics_ray(payload=req)
        self.assertEqual(res["image_nature"], "REAL_INVERTED")
        self.assertEqual(res["image_distance_cm"], 40.0)

    async def test_api_simulate_titration(self):
        """Asserts POST /lab/titration/simulate endpoint returns pH curve."""
        req = TitrationSimulationRequest(
            analyte="HCl",
            titrant="NaOH",
            analyte_volume_ml=20.0,
            analyte_molarity=0.1,
            titrant_molarity=0.1
        )
        res = await simulate_acid_base_titration(payload=req)
        self.assertEqual(res["equivalence_volume_ml"], 20.0)
        self.assertEqual(res["status"], "COMPLETED")

    async def test_api_generate_lab_report(self):
        """Asserts POST /lab/report/generate returns synthesis report."""
        req = LabReportSynthesisRequest(
            lab_type="TITRATION_PH",
            student_id="std-api-01",
            experimental_value=20.2,
            theoretical_value=20.0,
            observations="Slight drop overshoot at burette stopcock."
        )
        res = await generate_lab_report(payload=req)
        self.assertEqual(res["lab_type"], "TITRATION_PH")
        self.assertAlmostEqual(res["relative_error_pct"], 1.0, places=1)

    async def test_api_coaching_batch_endpoints(self):
        """Asserts POST /coaching/batch/create, join, log-session, and detail retrieval."""
        create_req = CreateCoachingBatchRequest(
            batch_title="API Micro Batch",
            subject="ICT & Coding",
            lead_guardian_id="g-api-01",
            total_monthly_fee_bdt=4500.0,
            max_capacity=3
        )
        batch = await create_coaching_batch(payload=create_req)
        batch_id = batch["batch_id"]

        join_req = JoinBatchGuardianRequest(
            guardian_id="g-api-02",
            guardian_name="API Guardian 2",
            student_name="Student 2"
        )
        joined = await join_coaching_batch(batch_id=batch_id, payload=join_req)
        self.assertEqual(joined["current_guardians"], 2)

        session_req = LogBatchSessionRequest(
            session_topic="Python Variables",
            attendees=["g-api-01", "g-api-02"],
            duration_minutes=60
        )
        ses = await log_coaching_session(batch_id=batch_id, payload=session_req)
        self.assertEqual(ses["attendance_pct"], 100.0)

        details = await get_coaching_batch_details(batch_id=batch_id)
        self.assertEqual(details["batch_id"], batch_id)

        all_batches = await list_coaching_batches()
        self.assertGreaterEqual(len(all_batches), 1)

    async def test_api_capstone_endpoints(self):
        """Asserts GET /capstones/directory, details, and milestone submission."""
        directory = await get_capstones_directory()
        self.assertGreaterEqual(directory["total"], 3)

        first_id = directory["capstones"][0]["capstone_id"]
        detail = await get_capstone_details(capstone_id=first_id)
        self.assertEqual(detail["capstone_id"], first_id)

        submit_req = SubmitCapstoneMilestoneRequest(
            student_id="std-api-capstone",
            student_name="API Capstone Student",
            milestone_stage="ARCHITECTURE_PROPOSAL",
            deliverables_url="https://github.com/capstone/arch",
            executive_summary="Architecture proposal summary"
        )
        sub = await submit_capstone_milestone(capstone_id=first_id, payload=submit_req)
        self.assertEqual(sub["status"], "APPROVED")


if __name__ == "__main__":
    unittest.main()
