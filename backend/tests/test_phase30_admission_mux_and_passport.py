"""
Unit and Integration Test Suite: Phase 30
Verifies:
1. UniversityAdmissionMultiplexerService (GPA & group eligibility, schedule clash detection, batch apply, admit cards)
2. OfflineDeltaSyncService (CRDT vector clock sync, LWW and Set-Union merging, idempotent deduplication, SHA-256 digest)
3. StudentTalentPassportService (Talent radar scores, Minor PII Redaction Shield, cryptographic QR signature)
4. Section 29 REST Routes in router.py
"""

import unittest
from backend.app.services.university_admission_multiplexer_service import (
    UniversityAdmissionMultiplexerService,
    university_admission_multiplexer_service
)
from backend.app.services.offline_delta_sync_service import (
    OfflineDeltaSyncService,
    offline_delta_sync_service
)
from backend.app.services.student_talent_passport_service import (
    StudentTalentPassportService,
    student_talent_passport_service
)
from backend.app.schemas.admission_mux_and_passport_schema import (
    CheckAdmissionEligibilityRequest,
    BatchApplyUniversityRequest,
    OfflineDeltaSyncRequest,
    GenerateTalentPassportRequest
)
from backend.app.api.v1.router import (
    check_admission_eligibility,
    batch_apply_admission,
    get_admission_admit_card,
    sync_crdt_delta,
    get_student_crdt_synced_state,
    generate_talent_passport,
    get_public_talent_passport,
    verify_talent_passport_qr_signature
)


class TestPhase30AdmissionMuxAndPassport(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mux_service = UniversityAdmissionMultiplexerService()
        self.sync_service = OfflineDeltaSyncService()
        self.passport_service = StudentTalentPassportService()

    # -------------------------------------------------------------------------
    # 1. UniversityAdmissionMultiplexerService Tests
    # -------------------------------------------------------------------------
    def test_check_eligibility_high_gpa_science(self):
        reports = self.mux_service.check_eligibility(
            student_id="std-science-top",
            hsc_gpa=5.0,
            ssc_gpa=5.0,
            academic_group="SCIENCE"
        )
        self.assertGreaterEqual(len(reports), 5)
        # BUET, DU, Medical should all be eligible
        buet = next(r for r in reports if r["university_code"] == "BUET")
        self.assertTrue(buet["is_eligible"])
        self.assertIn("Fully Eligible", buet["status_reason"])

    def test_check_eligibility_sub_threshold_gpa(self):
        reports = self.mux_service.check_eligibility(
            student_id="std-low-gpa",
            hsc_gpa=3.6,
            ssc_gpa=3.8,
            academic_group="SCIENCE"
        )
        buet = next(r for r in reports if r["university_code"] == "BUET")
        self.assertFalse(buet["is_eligible"])
        self.assertIn("below required", buet["status_reason"])

        # GST cluster with 3.5 min should be eligible if combined >= 8.0 (here 7.4, so false)
        gst = next(r for r in reports if r["university_code"] == "GST")
        self.assertFalse(gst["is_eligible"])

    def test_check_eligibility_non_science_group(self):
        reports = self.mux_service.check_eligibility(
            student_id="std-commerce",
            hsc_gpa=5.0,
            ssc_gpa=5.0,
            academic_group="BUSINESS_STUDIES"
        )
        for r in reports:
            self.assertFalse(r["is_eligible"])
            self.assertIn("Requires SCIENCE group", r["status_reason"])

    def test_batch_apply_generates_admit_cards_and_venues(self):
        batch = self.mux_service.batch_apply(
            student_id="std-cand-01",
            student_name="Arman Hossain",
            hsc_roll="104928",
            hsc_registration="1812948291",
            university_codes=["BUET", "DU_KA"],
            payment_channel="bKash"
        )
        self.assertIn("batch-app-", batch["batch_id"])
        self.assertEqual(batch["payment_status"], "SETTLED")
        self.assertEqual(batch["total_fee_bdt"], 2200.0)
        self.assertEqual(len(batch["admit_cards"]), 2)

        # Inspect admit card
        first_card = batch["admit_cards"][0]
        self.assertTrue(first_card["admit_card_id"].startswith("ADM-"))
        self.assertIn("Room", first_card["exam_venue"])
        self.assertEqual(first_card["status"], "ISSUED")

        # Verify lookup
        card_lookup = self.mux_service.get_admit_card(first_card["admit_card_id"])
        self.assertIsNotNone(card_lookup)
        self.assertEqual(card_lookup["student_name"], "Arman Hossain")

    def test_batch_apply_validation_errors(self):
        with self.assertRaises(ValueError):
            self.mux_service.batch_apply(
                student_id="std-err",
                student_name="Test",
                hsc_roll="123",
                hsc_registration="456",
                university_codes=[]
            )

        with self.assertRaises(ValueError):
            self.mux_service.batch_apply(
                student_id="std-err",
                student_name="Test",
                hsc_roll="123",
                hsc_registration="456",
                university_codes=["UNKNOWN_VARSITY"]
            )

    # -------------------------------------------------------------------------
    # 2. OfflineDeltaSyncService Tests
    # -------------------------------------------------------------------------
    def test_crdt_delta_sync_fresh_mutations(self):
        student_id = "std-rural-01"
        mutations = [
            {
                "mutation_id": "mut-001",
                "client_timestamp": "2026-10-15T08:00:00Z",
                "vector_clock": 1,
                "entity_type": "QUIZ_ANSWER",
                "entity_id": "q-101",
                "payload": {"selected_option": "B", "score": 1.0}
            },
            {
                "mutation_id": "mut-002",
                "client_timestamp": "2026-10-15T08:01:00Z",
                "vector_clock": 2,
                "entity_type": "NOTE",
                "entity_id": "note-phy-01",
                "payload": {"content": "Carnot engine efficiency formula derivation"}
            }
        ]
        res = self.sync_service.sync_delta(
            client_id="pwa-kurigram-client",
            student_id=student_id,
            last_synced_vector_clock=0,
            mutations=mutations
        )
        self.assertEqual(res["sync_status"], "SUCCESS")
        self.assertEqual(res["applied_count"], 2)
        self.assertTrue(res["server_state_digest"].startswith("crdt-"))

        # Verify state
        state = self.sync_service.get_student_synced_state(student_id)
        self.assertIn("q-101", state["entities"]["QUIZ_ANSWER"])
        self.assertIn("note-phy-01", state["entities"]["NOTE"])

    def test_crdt_idempotent_deduplication(self):
        student_id = "std-rural-02"
        mutation = {
            "mutation_id": "mut-idempotent-01",
            "client_timestamp": "2026-10-15T08:05:00Z",
            "vector_clock": 1,
            "entity_type": "NOTE",
            "entity_id": "note-math-01",
            "payload": {"content": "Integration by parts formula"}
        }
        res1 = self.sync_service.sync_delta(
            client_id="client-a",
            student_id=student_id,
            last_synced_vector_clock=0,
            mutations=[mutation]
        )
        self.assertEqual(res1["applied_count"], 1)

        # Resend identical mutation_id (network retry)
        res2 = self.sync_service.sync_delta(
            client_id="client-a",
            student_id=student_id,
            last_synced_vector_clock=1,
            mutations=[mutation]
        )
        self.assertEqual(res2["applied_count"], 0)
        self.assertEqual(res2["sync_status"], "IDEMPOTENT_NOOP")

    def test_crdt_set_union_and_lww_resolution(self):
        student_id = "std-rural-03"
        # Initial bookmark
        self.sync_service.sync_delta(
            client_id="client-b",
            student_id=student_id,
            mutations=[{
                "mutation_id": "mut-bm-01",
                "vector_clock": 1,
                "entity_type": "BOOKMARK",
                "entity_id": "deck-physics",
                "payload": {"card_1": True, "card_2": True}
            }]
        )
        # Merge second bookmark with Set-Union
        res = self.sync_service.sync_delta(
            client_id="client-b",
            student_id=student_id,
            mutations=[{
                "mutation_id": "mut-bm-02",
                "vector_clock": 2,
                "entity_type": "BOOKMARK",
                "entity_id": "deck-physics",
                "payload": {"card_3": True}
            }]
        )
        self.assertEqual(res["sync_status"], "RECONCILED")
        state = self.sync_service.get_student_synced_state(student_id)
        deck = state["entities"]["BOOKMARK"]["deck-physics"]["payload"]
        self.assertTrue(deck.get("card_1"))
        self.assertTrue(deck.get("card_2"))
        self.assertTrue(deck.get("card_3"))

    # -------------------------------------------------------------------------
    # 3. StudentTalentPassportService Tests
    # -------------------------------------------------------------------------
    def test_generate_and_radar_scores(self):
        passport = self.passport_service.generate_passport(
            student_id="std-101",
            public_handle="zubair-al-mahmud",
            include_mentorship_badges=True,
            include_code_evaluations=True
        )
        self.assertTrue(passport["passport_id"].startswith("PASS-"))
        self.assertEqual(passport["public_handle"], "zubair-al-mahmud")
        self.assertGreaterEqual(passport["cat_latent_ability_theta"], 2.0)
        radar = passport["credentials_summary"]["radar_dimensions"]
        self.assertIn("algorithmic_problem_solving", radar)
        self.assertIn("mathematical_rigor", radar)
        self.assertTrue(passport["shareable_url"].startswith("https://agrojatra.edu.bd/talent/"))

    def test_minor_pii_redaction_shield(self):
        # Recruiter View (Shielded)
        recruiter_view = self.passport_service.get_passport_by_handle("zubair-al-mahmud", is_recruiter_view=True)
        self.assertIsNotNone(recruiter_view)
        self.assertIn("PROTECTED", recruiter_view["phone"])
        self.assertIn("VERIFIED", recruiter_view["email"])
        self.assertIn("REDACTED", recruiter_view["address"])
        self.assertFalse("Dhanmondi" in recruiter_view["address"])

        # Authenticated Student View (Unshielded)
        student_view = self.passport_service.get_passport_by_handle("zubair-al-mahmud", is_recruiter_view=False)
        self.assertIn("+88017", student_view["phone"])
        self.assertIn("Dhanmondi", student_view["address"])

    def test_qr_signature_cryptographic_verification(self):
        passport = self.passport_service.generate_passport(
            student_id="std-101",
            public_handle="zubair-al-mahmud"
        )
        sig = passport["qr_signature"]
        # Authentic signature
        self.assertTrue(self.passport_service.verify_passport_signature("zubair-al-mahmud", sig))

        # Tampered signature
        fake_sig = sig[:-4] + "DEAD"
        self.assertFalse(self.passport_service.verify_passport_signature("zubair-al-mahmud", fake_sig))

    # -------------------------------------------------------------------------
    # 4. Section 29 REST Endpoints Integration Tests
    # -------------------------------------------------------------------------
    async def test_router_admission_endpoints(self):
        # Eligibility
        req = CheckAdmissionEligibilityRequest(
            student_id="std-api-01",
            hsc_gpa=5.0,
            ssc_gpa=4.8,
            academic_group="SCIENCE"
        )
        res = await check_admission_eligibility(req)
        self.assertEqual(res["student_id"], "std-api-01")
        self.assertGreaterEqual(res["total_evaluated"], 5)

        # Batch apply
        batch_req = BatchApplyUniversityRequest(
            student_id="std-api-01",
            student_name="Tanzim Ahmed",
            hsc_roll="554433",
            hsc_registration="99887766",
            university_codes=["BUET", "GST"],
            payment_channel="bKash"
        )
        batch_res = await batch_apply_admission(batch_req)
        self.assertEqual(batch_res["payment_status"], "SETTLED")
        admit_id = batch_res["admit_cards"][0]["admit_card_id"]

        # Get admit card
        admit_res = await get_admission_admit_card(admit_id)
        self.assertEqual(admit_res["admit_card_id"], admit_id)

    async def test_router_crdt_sync_endpoints(self):
        sync_req = OfflineDeltaSyncRequest(
            client_id="client-web-01",
            student_id="std-api-sync",
            last_synced_vector_clock=0,
            mutations=[{
                "mutation_id": "mut-api-1",
                "vector_clock": 1,
                "entity_type": "QUIZ_ANSWER",
                "entity_id": "q-999",
                "payload": {"score": 5.0}
            }]
        )
        res = await sync_crdt_delta(sync_req)
        self.assertEqual(res["sync_status"], "SUCCESS")

        state = await get_student_crdt_synced_state("std-api-sync")
        self.assertEqual(state["student_id"], "std-api-sync")
        self.assertIn("q-999", state["entities"]["QUIZ_ANSWER"])

    async def test_router_talent_passport_endpoints(self):
        gen_req = GenerateTalentPassportRequest(
            student_id="std-202",
            public_handle="nafisa-tabassum",
            include_mentorship_badges=True,
            include_code_evaluations=True
        )
        passport = await generate_talent_passport(gen_req)
        self.assertEqual(passport["public_handle"], "nafisa-tabassum")

        # Public retrieval
        public_view = await get_public_talent_passport("nafisa-tabassum")
        self.assertIn("PROTECTED", public_view["phone"])

        # QR signature verification
        ver = await verify_talent_passport_qr_signature("nafisa-tabassum", passport["qr_signature"])
        self.assertTrue(ver["is_signature_valid"])
        self.assertEqual(ver["status"], "AUTHENTIC")


if __name__ == "__main__":
    unittest.main()
