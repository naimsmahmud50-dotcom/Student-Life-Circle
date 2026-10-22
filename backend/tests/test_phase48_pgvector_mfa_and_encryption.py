"""
================================================================================
TEST SUITE: Phase 48 - pgvector, MFA Passkeys & Envelope Field Encryption
STANDARDS: OWASP ASVS L2, Strix-Supabase Security Playbook, FIDO2/WebAuthn
FILE: backend/tests/test_phase48_pgvector_mfa_and_encryption.py
================================================================================
"""

import unittest
import time
from backend.app.services.supabase_pgvector_service import SupabasePgvectorService
from backend.app.services.supabase_mfa_passkey_service import SupabaseMfaPasskeyService
from backend.app.services.supabase_field_encryption_service import SupabaseFieldEncryptionService


class TestPhase48PgvectorMfaAndEncryption(unittest.TestCase):
    def setUp(self):
        self.vector_service = SupabasePgvectorService()
        self.mfa_service = SupabaseMfaPasskeyService()
        self.crypto_service = SupabaseFieldEncryptionService()

    # =========================================================================
    # 1. pgvector & AI Syllabus Grounding Tests
    # =========================================================================
    def test_vector_cosine_and_l2_metrics(self):
        vec_a = [1.0, 0.0, 0.0]
        vec_b = [1.0, 0.0, 0.0]
        vec_c = [0.0, 1.0, 0.0]
        vec_d = [-1.0, 0.0, 0.0]

        # Identical vectors
        self.assertAlmostEqual(self.vector_service.cosine_similarity(vec_a, vec_b), 1.0, places=4)
        self.assertAlmostEqual(self.vector_service.l2_distance(vec_a, vec_b), 0.0, places=4)

        # Orthogonal vectors
        self.assertAlmostEqual(self.vector_service.cosine_similarity(vec_a, vec_c), 0.0, places=4)

        # Opposite vectors
        self.assertAlmostEqual(self.vector_service.cosine_similarity(vec_a, vec_d), -1.0, places=4)

    def test_vector_rls_cross_tenant_isolation(self):
        query = [0.5, 0.5, 0.707]
        corpus = [
            {"id": "doc_1", "title": "Syllabus Physics", "embedding": [0.5, 0.5, 0.707], "tenant_id": "org_dhaka", "is_public": False},
            {"id": "doc_2", "title": "Secret Exam Questions", "embedding": [0.5, 0.5, 0.707], "tenant_id": "org_chittagong", "is_public": False},
            {"id": "doc_3", "title": "Public NCTB Class 10", "embedding": [0.49, 0.51, 0.707], "tenant_id": "org_chittagong", "is_public": True}
        ]

        # Student from org_dhaka should NOT see doc_2 (org_chittagong private)
        res = self.vector_service.search_semantic_knowledge(
            query_vector=query,
            corpus=corpus,
            caller_tenant_id="org_dhaka",
            caller_role="authenticated"
        )

        doc_ids = [r["id"] for r in res["results"]]
        self.assertIn("doc_1", doc_ids)
        self.assertIn("doc_3", doc_ids)
        self.assertNotIn("doc_2", doc_ids)
        self.assertEqual(res["cross_tenant_leaks_prevented"], 1)

    def test_ai_syllabus_grounding_verification(self):
        syllabus_chunk = [0.2, 0.4, 0.8, 0.1]
        
        # Grounded AI response
        grounded_resp = [0.21, 0.39, 0.79, 0.11]
        eval_ok = self.vector_service.evaluate_ai_grounding(grounded_resp, [syllabus_chunk], grounding_threshold=0.82)
        self.assertTrue(eval_ok["is_grounded"])
        self.assertEqual(eval_ok["verdict"], "VERIFIED_SYLLABUS_GROUNDED")

        # Hallucinated response
        hallucinated_resp = [-0.9, 0.1, -0.2, 0.8]
        eval_bad = self.vector_service.evaluate_ai_grounding(hallucinated_resp, [syllabus_chunk], grounding_threshold=0.82)
        self.assertFalse(eval_bad["is_grounded"])
        self.assertEqual(eval_bad["verdict"], "POTENTIAL_HALLUCINATION_DETECTED")

    # =========================================================================
    # 2. GoTrue MFA & WebAuthn Passkeys Tests
    # =========================================================================
    def test_totp_enrollment_and_verification(self):
        enroll = self.mfa_service.enroll_totp_factor("usr_student_mfa_01")
        self.assertIn("otpauth://totp", enroll["otpauth_uri"])
        self.assertEqual(len(enroll["backup_recovery_codes_plaintext"]), 8)

        secret_hex = enroll["secret_hex"]
        current_code = enroll["current_time_step_code"]

        # Valid verification elevates session to AAL2
        verify_res = self.mfa_service.verify_totp_token(secret_hex, current_code)
        self.assertTrue(verify_res["is_valid"])
        self.assertEqual(verify_res["current_aal"], "aal2")

        # Invalid verification remains at AAL1
        bad_res = self.mfa_service.verify_totp_token(secret_hex, "000000")
        self.assertFalse(bad_res["is_valid"])
        self.assertEqual(bad_res["current_aal"], "aal1")

    def test_passkey_challenge_and_origin_binding(self):
        challenge_data = self.mfa_service.generate_passkey_challenge("usr_99", "student@agrojatra.edu.bd")
        self.assertEqual(challenge_data["rp"]["id"], "agrojatra.edu.bd")

        # Case A: Correct origin and RP ID succeeds
        verify_ok = self.mfa_service.verify_passkey_response(
            challenge=challenge_data["challenge"],
            client_origin="https://agrojatra.edu.bd",
            client_rp_id="agrojatra.edu.bd",
            credential_id="cred_fido2_key_01",
            signature="sig_hardware_crypto"
        )
        self.assertTrue(verify_ok["verified"])
        self.assertEqual(verify_ok["aal"], "aal2")

        # Case B: Origin mismatch (Phishing attempt) rejected
        verify_phish = self.mfa_service.verify_passkey_response(
            challenge=challenge_data["challenge"],
            client_origin="https://evil-phishing-agrojatra.com",
            client_rp_id="agrojatra.edu.bd",
            credential_id="cred_fido2_key_01",
            signature="sig_hardware_crypto"
        )
        self.assertFalse(verify_phish["verified"])
        self.assertIn("ORIGIN_MISMATCH", verify_phish["reason"])

    # =========================================================================
    # 3. Database Field Envelope Encryption Tests
    # =========================================================================
    def test_envelope_encryption_roundtrip(self):
        secret_pii = "Student National ID: 19952692800123456"
        context = "guardian_verification_table"

        enc = self.crypto_service.envelope_encrypt(secret_pii, associated_data=context)
        self.assertIsNotNone(enc["ciphertext_hex"])
        self.assertIsNotNone(enc["encrypted_dek_hex"])
        self.assertIsNotNone(enc["blind_index_hex"])

        # Decrypt
        dec = self.crypto_service.envelope_decrypt(
            ciphertext_hex=enc["ciphertext_hex"],
            data_nonce_hex=enc["data_nonce_hex"],
            encrypted_dek_hex=enc["encrypted_dek_hex"],
            dek_nonce_hex=enc["dek_nonce_hex"],
            associated_data=context
        )
        self.assertTrue(dec["success"])
        self.assertEqual(dec["plaintext"], secret_pii)

    def test_blind_index_deterministic_match(self):
        pii = "bkash_wallet_01711223344"
        idx1 = self.crypto_service.compute_blind_index(pii)
        idx2 = self.crypto_service.compute_blind_index(pii)
        idx_diff = self.crypto_service.compute_blind_index("bkash_wallet_01899887766")

        self.assertEqual(idx1, idx2)
        self.assertNotEqual(idx1, idx_diff)


if __name__ == "__main__":
    unittest.main()
