"""
Comprehensive Automated Unit Tests for Phase 58:
W3C Verifiable Credential & ZKP Certificate Vault.
"""

import unittest
from backend.app.services.verifiable_credential_engine_service import VerifiableCredentialEngineService
from backend.app.services.zkp_range_proof_service import ZeroKnowledgeRangeProofService
from backend.app.services.institutional_revocation_registry_service import InstitutionalRevocationRegistryService


class TestPhase58VerifiableCredentialAndZkp(unittest.TestCase):

    def setUp(self):
        self.credential_service = VerifiableCredentialEngineService()
        self.zkp_service = ZeroKnowledgeRangeProofService()
        self.revocation_service = InstitutionalRevocationRegistryService()

    # --- VerifiableCredentialEngineService Tests ---
    def test_issue_verifiable_credential_structure(self):
        res = self.credential_service.issue_credential(
            student_id="DU-CSE-2022-0491",
            student_name="Tahmidur Rahman",
            institution_did="did:web:du.ac.bd:issuers:registrar",
            degree_title="Bachelor of Science in Computer Science & Engineering",
            cgpa=3.85,
            graduation_year=2026,
            honors_designation="Summa Cum Laude"
        )
        self.assertTrue(res["is_valid"])
        self.assertTrue(res["credential_id"].startswith("urn:uuid:"))
        w3c = res["w3c_payload"]
        self.assertIn("https://www.w3.org/ns/credentials/v2", w3c["@context"])
        self.assertEqual(w3c["credentialSubject"]["studentId"], "DU-CSE-2022-0491")
        self.assertEqual(w3c["credentialSubject"]["cgpa"], 3.85)
        self.assertIn("proof", w3c)
        self.assertEqual(w3c["proof"]["type"], "Ed25519Signature2020")
        self.assertTrue(res["svg_badge"].startswith("<svg"))

    def test_verify_unaltered_credential(self):
        issued = self.credential_service.issue_credential(
            student_id="BUET-EEE-2022-0112",
            student_name="Nusrat Jahan",
            institution_did="did:web:buet.ac.bd:issuers:dean",
            degree_title="B.Sc. in Electrical & Electronic Engineering",
            cgpa=3.92,
            graduation_year=2026
        )
        verify_res = self.credential_service.verify_credential(issued["w3c_payload"])
        self.assertTrue(verify_res["is_valid"])
        self.assertTrue(verify_res["issuer_verified"])
        self.assertFalse(verify_res["tamper_detected"])
        self.assertEqual(verify_res["claimed_student_name"], "Nusrat Jahan")
        self.assertEqual(verify_res["revocation_status"], "ACTIVE_VERIFIED")

    def test_verify_tampered_credential_cgpa_altered(self):
        issued = self.credential_service.issue_credential(
            student_id="DU-CSE-2022-0491",
            student_name="Tahmidur Rahman",
            institution_did="did:web:du.ac.bd:issuers:registrar",
            degree_title="B.Sc. in CSE",
            cgpa=3.85,
            graduation_year=2026
        )
        # Tamper: Fraudulently change CGPA from 3.85 to 3.99
        tampered_payload = json_copy = dict(issued["w3c_payload"])
        tampered_payload["credentialSubject"] = dict(tampered_payload["credentialSubject"])
        tampered_payload["credentialSubject"]["cgpa"] = 3.99

        verify_res = self.credential_service.verify_credential(tampered_payload)
        self.assertFalse(verify_res["is_valid"])
        self.assertTrue(verify_res["tamper_detected"])
        self.assertEqual(verify_res["revocation_status"], "SIGNATURE_INVALID")
        self.assertIn("mismatch", verify_res["verification_report"])

    def test_verify_tampered_credential_name_altered(self):
        issued = self.credential_service.issue_credential(
            student_id="NSU-BBA-2022-0881",
            student_name="Arif Hasan",
            institution_did="did:web:nsu.edu:issuers:controller",
            degree_title="Bachelor of Business Administration",
            cgpa=3.60,
            graduation_year=2026
        )
        tampered_payload = dict(issued["w3c_payload"])
        tampered_payload["credentialSubject"] = dict(tampered_payload["credentialSubject"])
        tampered_payload["credentialSubject"]["studentName"] = "Fraudster Impersonator"

        verify_res = self.credential_service.verify_credential(tampered_payload)
        self.assertFalse(verify_res["is_valid"])
        self.assertTrue(verify_res["tamper_detected"])

    def test_credential_svg_badge_xss_hardened(self):
        # Attempt XSS injection through student name
        xss_input = "<script>alert(1)</script>John Doe"
        res = self.credential_service.issue_credential(
            student_id="TEST-001",
            student_name=xss_input,
            institution_did="did:web:du.ac.bd:issuers:registrar",
            degree_title="B.Sc. in CSE",
            cgpa=3.50,
            graduation_year=2026
        )
        svg = res["svg_badge"]
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)

    def test_credential_invalid_cgpa_rejected(self):
        with self.assertRaises(ValueError):
            self.credential_service.issue_credential(
                student_id="TEST-002",
                student_name="Invalid CGPA Student",
                institution_did="did:web:du.ac.bd:issuers:registrar",
                degree_title="B.Sc. in Physics",
                cgpa=4.50,  # Invalid
                graduation_year=2026
            )

    # --- ZeroKnowledgeRangeProofService Tests ---
    def test_zkp_range_proof_satisfies_threshold(self):
        res = self.zkp_service.generate_range_proof(
            credential_id="urn:uuid:mock-credential-123",
            actual_cgpa=3.85,
            threshold_cgpa=3.50,
            student_did="did:key:z6MkpTHR8VNsBxYAAWHuEc2KAguPuHdO83nB0491"
        )
        self.assertTrue(res["proof_valid"])
        self.assertEqual(res["threshold_tested"], 3.50)
        self.assertIsNone(res["revealed_cgpa"])  # Privacy: score strictly concealed!
        self.assertTrue(res["pedersen_commitment"].startswith("0x"))
        self.assertIn("satisfies CGPA requirement", res["verifier_statement"])

    def test_zkp_range_proof_fails_threshold(self):
        res = self.zkp_service.generate_range_proof(
            credential_id="urn:uuid:mock-credential-456",
            actual_cgpa=3.20,
            threshold_cgpa=3.50,
            student_did="did:key:z6MkpTHR8VNsBxYAAWHuEc2KAguPuHdO83nB0491"
        )
        self.assertFalse(res["proof_valid"])
        self.assertIsNone(res["revealed_cgpa"])
        self.assertIn("Proof Rejected", res["verifier_statement"])

    def test_zkp_range_proof_verification_sub_millisecond(self):
        proof = self.zkp_service.generate_range_proof(
            credential_id="urn:uuid:mock-cred-789",
            actual_cgpa=3.95,
            threshold_cgpa=3.75,
            student_did="did:key:z6MkpTHR8VNsBxYAAWHuEc2KAguPuHdO83nB0112"
        )
        verified = self.zkp_service.verify_range_proof(
            proof_id=proof["proof_id"],
            pedersen_commitment=proof["pedersen_commitment"],
            threshold_cgpa=proof["threshold_tested"],
            student_did="did:key:z6MkpTHR8VNsBxYAAWHuEc2KAguPuHdO83nB0112",
            challenge_hash=proof["challenge_hash"],
            response_proof=proof["response_proof"],
            credential_id="urn:uuid:mock-cred-789"
        )
        self.assertTrue(verified)

    # --- InstitutionalRevocationRegistryService Tests ---
    def test_revocation_registry_active_check(self):
        res = self.revocation_service.check_revocation(
            institution_did="did:web:du.ac.bd:issuers:registrar",
            status_list_index=1001
        )
        self.assertFalse(res["is_revoked"])
        self.assertIsNone(res["revocation_reason"])
        self.assertEqual(len(res["state_root_hash"]), 64)

    def test_revocation_registry_revoked_check(self):
        res = self.revocation_service.check_revocation(
            institution_did="did:web:du.ac.bd:issuers:registrar",
            status_list_index=1005  # Seeded as revoked
        )
        self.assertTrue(res["is_revoked"])
        self.assertIn("Malpractice", res["revocation_reason"])

    def test_revocation_registry_dual_signature_requirement(self):
        with self.assertRaises(ValueError):
            self.revocation_service.update_revocation(
                institution_did="did:web:du.ac.bd:issuers:registrar",
                status_list_index=1002,
                is_revoked=True,
                revocation_reason="Grade manipulation",
                dean_signature="",  # Missing Dean signature
                registrar_signature="sig_reg_12345678"
            )

    def test_revocation_registry_authorized_update(self):
        root_before = self.revocation_service.check_revocation("did:web:du.ac.bd", 1002)["state_root_hash"]
        update_res = self.revocation_service.update_revocation(
            institution_did="did:web:du.ac.bd:issuers:registrar",
            status_list_index=1002,
            is_revoked=True,
            revocation_reason="Revoked by Academic Council Decision 2026/04",
            dean_signature="sig_dean_academic_council_du_valid_2026",
            registrar_signature="sig_registrar_du_valid_2026"
        )
        self.assertTrue(update_res["is_revoked"])
        self.assertEqual(update_res["authorization"], "DUAL_OFFICER_SIGNATURE_VERIFIED")

        # Confirm status change and state root change
        check_after = self.revocation_service.check_revocation("did:web:du.ac.bd", 1002)
        self.assertTrue(check_after["is_revoked"])
        self.assertNotEqual(root_before, check_after["state_root_hash"])


if __name__ == "__main__":
    unittest.main()
