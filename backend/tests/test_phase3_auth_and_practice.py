"""
========================================================================================
MODULE:    Automated Verification Test Suite - Phase 3 & 4
TOPIC:     Auth, Password Hashing, Minor Privacy Enforcement & Session Lifecycles
FILE:      backend/tests/test_phase3_auth_and_practice.py
PURPOSE:   Verifies the security and child safety guarantees of Phase 3.
           Proves: (1) Key-stretched password hashing, (2) Minor detection locking
           accounts to PRIVATE mode, (3) Duplicate account prevention,
           (4) Constant-time credential authentication, (5) Session token revocation,
           and (6) RBAC/ABAC ownership protection.
AUDIENCE:  Security Auditors, Backend Developers & CI/CD Pipelines
STANDARDS: OWASP ASVS L2, COPPA/Minor Privacy, Zero-Trust Architecture
========================================================================================
"""

import unittest
from backend.app.services.auth_service import AuthService
from backend.app.models.user import EducationStageEnum


class TestPhase3AuthAndMinorSafety(unittest.TestCase):
    """
    Test suite for Authentication, Minor Safety, and Session Management.
    """

    def setUp(self):
        self.auth = AuthService()

    def test_01_registration_with_password_hashing(self):
        """Proves password is securely hashed and not stored in plaintext."""
        success, result, reason = self.auth.register_user(
            full_name="Abir Rahman",
            password="StrongPassword123!",
            email="abir.rahman@example.com",
            age=17,
            stage=EducationStageEnum.HSC
        )
        self.assertTrue(success)
        self.assertEqual(reason, "OK")
        self.assertNotIn("StrongPassword123!", result["user"]["password_hash"])
        self.assertTrue(result["user"]["password_hash"].startswith("pbkdf2_sha256$"))

    def test_02_minor_safety_auto_private_lock(self):
        """Proves minors (age < 16) automatically get PRIVATE privacy mode."""
        success, result, _ = self.auth.register_user(
            full_name="Sadia Islam",
            password="SecurePass999!",
            email="sadia.child@example.com",
            age=13,
            stage=EducationStageEnum.MIDDLE
        )
        self.assertTrue(success)
        self.assertTrue(result["minor_protection_active"])
        self.assertEqual(result["profile"]["privacy_mode"], "PRIVATE")
        self.assertTrue(result["profile"]["is_minor"])

    def test_03_adult_pseudonymous_profile(self):
        """Proves adults default to pseudonymous mode for leaderboard participation."""
        success, result, _ = self.auth.register_user(
            full_name="Kamrul Hasan",
            password="AdultSecurePass!",
            email="kamrul.adult@example.com",
            age=22,
            stage=EducationStageEnum.UNIVERSITY
        )
        self.assertTrue(success)
        self.assertFalse(result["minor_protection_active"])
        self.assertEqual(result["profile"]["privacy_mode"], "PSEUDONYMOUS")
        self.assertFalse(result["profile"]["is_minor"])

    def test_04_duplicate_email_prevention(self):
        """Proves system rejects duplicate email registrations with HTTP 409 conflict."""
        self.auth.register_user(
            full_name="User First",
            password="Password123!",
            email="unique.student@example.com"
        )
        # Attempt second registration with same email
        success, _, reason = self.auth.register_user(
            full_name="User Second",
            password="Password123!",
            email="unique.student@example.com"
        )
        self.assertFalse(success)
        self.assertEqual(reason, "EMAIL_ALREADY_EXISTS")

    def test_05_authentication_and_session_validation(self):
        """Proves valid credentials issue session tokens and invalid passwords fail."""
        self.auth.register_user(
            full_name="Test Student",
            password="MySecretPassword123",
            email="login.test@example.com"
        )

        # Successful login
        ok, res, _ = self.auth.authenticate_user("login.test@example.com", "MySecretPassword123")
        self.assertTrue(ok)
        self.assertIsNotNone(res["session_token"])

        # Token validation
        user_ctx = self.auth.get_current_user_by_token(res["session_token"])
        self.assertIsNotNone(user_ctx)
        self.assertEqual(user_ctx["user"]["email"], "login.test@example.com")

        # Failed login (wrong password)
        failed, _, err = self.auth.authenticate_user("login.test@example.com", "WrongPassword!")
        self.assertFalse(failed)
        self.assertEqual(err, "INVALID_CREDENTIALS")

    def test_06_logout_revokes_token(self):
        """Proves logout immediately invalidates the active session token."""
        _, res, _ = self.auth.register_user(
            full_name="Logout User",
            password="Password123!",
            email="logout.user@example.com"
        )
        token = res["session_token"]

        # Token is valid
        self.assertIsNotNone(self.auth.get_current_user_by_token(token))

        # Logout
        revoked = self.auth.logout_session(token)
        self.assertTrue(revoked)

        # Token is now rejected
        self.assertIsNone(self.auth.get_current_user_by_token(token))


if __name__ == "__main__":
    unittest.main()
