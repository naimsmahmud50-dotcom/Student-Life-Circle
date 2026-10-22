# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 82 Test Suite):
# Automated Verification Test Suite for SMS OTP & Guardian Consent Gateway:
# 1. Bangladeshi SMS Aggregators (Greenweb, Teletalk, Elitbuzz, Twilio, Mock).
# 2. Bangla Unicode Detection & Multi-Part Character Calculation.
# 3. Cryptographic 6-Digit OTP Generation, SHA-256 Hash-at-Rest, and 180s TTL.
# 4. Anti-SMS-Bombing Rate Limiter (Max 3 OTP requests / 15 minutes).
# 5. OTP Verification, Replay Prevention, and Failed Attempt Lockout.
# 6. Minor Student Guardian Consent Flow, 1-Click Verification, and Profile Lockdown.
# 7. Complete REST Endpoints and Append-Only Audit Logging.
# 8. Strict Zero-Emoji Compliance across all code, logs, and frontend components.
# ==============================================================================

import unittest
import asyncio
import time
import os
import re

from backend.app.services.sms.adapters import (
    is_bangla_unicode,
    calculate_sms_parts,
    normalize_bd_phone,
    mask_phone_for_logging,
    GreenwebSMSAdapter,
    TeletalkSMSAdapter,
    ElitbuzzSMSAdapter,
    TwilioSMSAdapter,
    MockSMSAdapter
)
from backend.app.services.sms.sms_gateway_service import (
    SMSGatewayService,
    sms_gateway_service,
    MAX_OTP_PER_15_MINUTES,
    RATE_LIMIT_WINDOW_SECONDS
)
from backend.app.services.sms.otp_service import (
    OTPService,
    otp_service,
    OTP_TTL_SECONDS
)
from backend.app.services.sms.guardian_consent_service import (
    GuardianConsentService,
    guardian_consent_service
)
from backend.app.api.v1.endpoints.auth_otp import (
    send_sms_otp_endpoint,
    verify_sms_otp_endpoint,
    request_guardian_consent_endpoint,
    verify_guardian_consent_token_endpoint,
    grant_guardian_consent_endpoint,
    revoke_guardian_consent_endpoint,
    get_student_privacy_status_endpoint,
    get_sms_audit_logs_endpoint
)
from backend.app.core.fastapi_shim import HTTPException


class TestPhase82SmsOtpAndGuardianConsent(unittest.IsolatedAsyncioTestCase):
    """
    Test suite asserting Bangladeshi SMS Gateway, Cryptographic OTP,
    Anti-SMS-Bombing Rate Limits, and Minor Guardian Consent Gateway.
    """

    async def asyncSetUp(self):
        # Reset mock adapter and in-memory caches
        sms_gateway_service.clear_audit_records()
        otp_service.clear_audit_records()
        guardian_consent_service.clear_audit_records()

    async def test_01_bangla_unicode_detection_and_parts(self):
        """Validates Bangla Unicode detection and SMS billable parts calculation."""
        english_text = "Your verification code is 123456."
        self.assertFalse(is_bangla_unicode(english_text))
        gsm_calc = calculate_sms_parts(english_text)
        self.assertEqual(gsm_calc["encoding"], "GSM_7BIT")
        self.assertEqual(gsm_calc["parts"], 1)

        bangla_text = "স্টুডেন্ট লাইফ সার্কেল ভেরিফিকেশন কোড: ১২৩৪৫৬।"
        self.assertTrue(is_bangla_unicode(bangla_text))
        unicode_calc = calculate_sms_parts(bangla_text)
        self.assertEqual(unicode_calc["encoding"], "UNICODE")
        self.assertEqual(unicode_calc["parts"], 1)

        long_bangla = "স্টুডেন্ট লাইফ সার্কেল প্ল্যাটফর্ম " * 5  # > 70 characters
        long_calc = calculate_sms_parts(long_bangla)
        self.assertEqual(long_calc["encoding"], "UNICODE")
        self.assertGreater(long_calc["parts"], 1)

    async def test_02_phone_normalization_and_masking(self):
        """Validates Bangladeshi phone number normalization and privacy masking."""
        self.assertEqual(normalize_bd_phone("01712345678"), "8801712345678")
        self.assertEqual(normalize_bd_phone("+8801812345678"), "8801812345678")
        self.assertEqual(normalize_bd_phone("8801912345678"), "8801912345678")
        self.assertEqual(normalize_bd_phone("015-1234-5678"), "8801512345678")

        masked = mask_phone_for_logging("01712345678")
        self.assertTrue(masked.startswith("88017"))
        self.assertTrue(masked.endswith("5678"))
        self.assertIn("****", masked)

    async def test_03_bangladeshi_sms_adapters(self):
        """Validates all aggregator adapters (Greenweb, Teletalk, Elitbuzz, Twilio, Mock)."""
        gw = GreenwebSMSAdapter()
        gw_res = await gw.send_sms("01711111111", "Test Greenweb", is_masked=True)
        self.assertTrue(gw_res["success"])
        self.assertEqual(gw_res["provider"], "greenweb")
        self.assertEqual(gw_res["sender_id"], "StudentLife")

        tt = TeletalkSMSAdapter()
        tt_res = await tt.send_sms("01511111111", "Test Teletalk", is_masked=False)
        self.assertTrue(tt_res["success"])
        self.assertEqual(tt_res["provider"], "teletalk")

        eb = ElitbuzzSMSAdapter()
        eb_res = await eb.send_sms("01811111111", "Test Elitbuzz")
        self.assertTrue(eb_res["success"])
        self.assertEqual(eb_res["provider"], "elitbuzz")

        tw = TwilioSMSAdapter()
        tw_res = await tw.send_sms("01911111111", "Test Twilio")
        self.assertTrue(tw_res["success"])
        self.assertEqual(tw_res["provider"], "twilio")

        mock = MockSMSAdapter()
        mock_res = await mock.send_sms("01722222222", "Test Mock")
        self.assertTrue(mock_res["success"])
        self.assertEqual(len(mock.sent_messages), 1)

    async def test_04_sms_gateway_failover_mechanism(self):
        """Validates automatic provider failover when primary aggregator fails."""
        gateway = SMSGatewayService(use_mock=False)
        failing_mock = MockSMSAdapter(should_fail=True)
        failing_mock.name = "failing_primary"
        working_mock = MockSMSAdapter(should_fail=False)
        working_mock.name = "working_backup"

        gateway.register_adapter(failing_mock)
        gateway.register_adapter(working_mock)
        gateway.set_fallback_order(["failing_primary", "working_backup"])

        res = await gateway.send_sms("01733333333", "Failover verification")
        self.assertTrue(res["success"])
        self.assertEqual(res["provider"], "working_backup")

    async def test_05_anti_sms_bombing_rate_limiter(self):
        """Asserts maximum 3 OTP requests per phone number per 15 minutes."""
        test_phone = "01744444444"
        gateway = SMSGatewayService(use_mock=True)

        # 1st request -> Allowed
        allowed1, count1, _ = await gateway.check_and_increment_rate_limit(test_phone)
        self.assertTrue(allowed1)
        self.assertEqual(count1, 1)

        # 2nd request -> Allowed
        allowed2, count2, _ = await gateway.check_and_increment_rate_limit(test_phone)
        self.assertTrue(allowed2)
        self.assertEqual(count2, 2)

        # 3rd request -> Allowed
        allowed3, count3, _ = await gateway.check_and_increment_rate_limit(test_phone)
        self.assertTrue(allowed3)
        self.assertEqual(count3, 3)

        # 4th request within 15 minutes -> BLOCKED
        allowed4, count4, retry_after = await gateway.check_and_increment_rate_limit(test_phone)
        self.assertFalse(allowed4)
        self.assertGreaterEqual(retry_after, 1)

    async def test_06_cryptographic_otp_lifecycle_and_verification(self):
        """Asserts cryptographic 6-digit OTP generation, SHA-256 hashing, and single-use purge."""
        test_phone = "01755555555"

        # Generate and send OTP
        res = await otp_service.generate_and_send_otp(
            phone=test_phone,
            purpose="LOGIN",
            user_id="usr_test_01",
            return_raw_for_testing=True
        )
        self.assertTrue(res["success"])
        raw_otp = res["raw_otp_testing_only"]
        self.assertEqual(len(raw_otp), 6)
        self.assertTrue(raw_otp.isdigit())

        # Test incorrect OTP submission
        bad_verif = await otp_service.verify_otp(phone=test_phone, otp="000000", purpose="LOGIN")
        self.assertFalse(bad_verif["verified"])
        self.assertEqual(bad_verif["error"], "INVALID_OTP")
        self.assertEqual(bad_verif["attempts_remaining"], 2)

        # Test correct OTP submission
        good_verif = await otp_service.verify_otp(phone=test_phone, otp=raw_otp, purpose="LOGIN")
        self.assertTrue(good_verif["verified"])
        self.assertEqual(good_verif["user_id"], "usr_test_01")

        # Replay attempt with same OTP -> MUST FAIL (single-use purge)
        replay_verif = await otp_service.verify_otp(phone=test_phone, otp=raw_otp, purpose="LOGIN")
        self.assertFalse(replay_verif["verified"])
        self.assertEqual(replay_verif["error"], "OTP_EXPIRED_OR_INVALID")

    async def test_07_guardian_consent_minor_flow(self):
        """Asserts minor student (<16) guardian consent request, SMS dispatch, approval, and revocation."""
        student_id = "student_minor_101"
        student_name = "Sakib Hasan"
        guardian_phone = "01766666666"

        # 1. Initial Privacy Status -> Locked to private mode
        init_status = guardian_consent_service.get_student_privacy_status(student_id)
        self.assertTrue(init_status["is_minor"])
        self.assertFalse(init_status["guardian_consent_granted"])
        self.assertFalse(init_status["can_receive_public_messages"])

        # 2. Request Guardian Consent
        req_res = await guardian_consent_service.request_guardian_consent(
            student_id=student_id,
            student_name=student_name,
            guardian_phone=guardian_phone,
            student_age=14
        )
        self.assertTrue(req_res["success"])
        self.assertEqual(req_res["status"], "PENDING")
        token = req_res["consent_token"]
        self.assertIsNotNone(token)

        # 3. Verify Token
        token_verif = await guardian_consent_service.verify_consent_token(token)
        self.assertTrue(token_verif["valid"])
        self.assertEqual(token_verif["student_name"], student_name)

        # 4. Guardian affirmative approval
        grant_res = await guardian_consent_service.grant_consent(
            token=token,
            relationship="FATHER",
            guardian_name="Abdul Hasan"
        )
        self.assertTrue(grant_res["success"])
        self.assertEqual(grant_res["status"], "APPROVED")

        # 5. Check Privacy Status after approval -> Unlocked
        post_status = guardian_consent_service.get_student_privacy_status(student_id)
        self.assertTrue(post_status["guardian_consent_granted"])
        self.assertTrue(post_status["can_receive_public_messages"])
        self.assertEqual(post_status["relationship"], "FATHER")

        # 6. Guardian Revocation -> Re-locks profile
        revoke_res = await guardian_consent_service.revoke_consent(
            student_id=student_id,
            guardian_phone=guardian_phone,
            reason="Safety reassessment"
        )
        self.assertTrue(revoke_res["success"])
        revoked_status = guardian_consent_service.get_student_privacy_status(student_id)
        self.assertFalse(revoked_status["guardian_consent_granted"])
        self.assertFalse(revoked_status["can_receive_public_messages"])

    async def test_08_rest_endpoints_integration(self):
        """Asserts all FastAPI endpoints for OTP and Guardian Consent."""
        phone = "01777777777"

        # Endpoint 1: Send OTP
        send_res = await send_sms_otp_endpoint({"phone": phone, "purpose": "TEST", "test_mode": True})
        self.assertTrue(send_res["success"])
        test_otp = send_res.get("raw_otp_testing_only")

        # Endpoint 2: Verify OTP
        verify_res = await verify_sms_otp_endpoint({"phone": phone, "otp": test_otp, "purpose": "TEST"})
        self.assertTrue(verify_res["verified"])

        # Endpoint 3: Request Guardian Consent
        consent_req = await request_guardian_consent_endpoint({
            "student_id": "student_endpoint_01",
            "student_name": "Nafisa Rahman",
            "guardian_phone": "01788888888",
            "student_age": 13
        })
        self.assertTrue(consent_req["success"])
        token = consent_req["consent_token"]

        # Endpoint 4: Verify Consent Token
        token_info = await verify_guardian_consent_token_endpoint(token=token)
        self.assertTrue(token_info["valid"])

        # Endpoint 5: Grant Consent
        grant_info = await grant_guardian_consent_endpoint({
            "token": token,
            "relationship": "MOTHER"
        })
        self.assertTrue(grant_info["success"])

        # Endpoint 6: Check Student Privacy Status
        status_info = await get_student_privacy_status_endpoint("student_endpoint_01")
        self.assertTrue(status_info["guardian_consent_granted"])

        # Endpoint 7: Audit Logs
        audit_res = await get_sms_audit_logs_endpoint(limit=20)
        self.assertEqual(audit_res["status"], "SUCCESS")
        self.assertIn("counts", audit_res)

    def test_09_zero_emoji_governance(self):
        """Scans all Phase 82 backend and frontend files to enforce strict ZERO-EMOJI policy."""
        files_to_check = [
            "backend/app/services/sms/adapters.py",
            "backend/app/services/sms/sms_gateway_service.py",
            "backend/app/services/sms/otp_service.py",
            "backend/app/services/sms/guardian_consent_service.py",
            "backend/app/services/sms/__init__.py",
            "backend/app/api/v1/endpoints/auth_otp.py",
            "frontend/src/components/auth/OtpVerificationModal.tsx",
            "frontend/src/components/auth/GuardianConsentCard.tsx",
            "frontend/src/components/auth/index.ts"
        ]

        # Common unicode emoji regex range
        emoji_pattern = re.compile(
            r'[\U00010000-\U0010ffff]|'  # Astral planes (surrogate pairs)
            r'[\u2600-\u26FF\u2700-\u27BF]'  # Miscellaneous symbols & dingbats
        )

        for rel_path in files_to_check:
            abs_path = os.path.join(os.getcwd(), rel_path)
            if not os.path.exists(abs_path):
                continue
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
                matches = emoji_pattern.findall(content)
                self.assertEqual(
                    len(matches), 
                    0, 
                    f"Zero-emoji policy violation in {rel_path}: {matches}"
                )


if __name__ == "__main__":
    unittest.main()
