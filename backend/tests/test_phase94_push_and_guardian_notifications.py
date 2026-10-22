# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 94 - Unit & Integration Test Suite):
# Comprehensive test suite validating W3C Web Push API, RFC 8292 VAPID Keypairs,
# Scheduled Retention Notifications, Service Worker Push Handlers, and Guardian
# Weekly Academic Digest Bot with Child Safety & Privacy Enforcement.
# Standards:
# 1. W3C Push API & RFC 8292 VAPID (EC P-256 / ES256).
# 2. Child Safety & Privacy: Strict non-disclosure of private notes.
# 3. Scheduled Reminders: Exact required Bengali texts verified.
# 4. Strict Zero-Emoji compliance across all files.
# ==============================================================================

import unittest
import time
import os
import re
import json
import uuid
import base64

from backend.app.services.notifications.web_push_service import (
    web_push_service,
    WebPushService,
    VAPIDKeyManager,
    b64url_decode
)
from backend.app.services.notifications.guardian_bot_service import (
    guardian_bot_service,
    GuardianMessagingBotService,
    WeeklyAcademicSummary,
    GuardianNotVerifiedError,
    GuardianPrivacyViolationError
)
from backend.app.api.v1.endpoints.push import (
    get_vapid_public_key,
    subscribe_push_client,
    unsubscribe_push_client,
    send_direct_push_notification,
    trigger_daily_quiz_reminder,
    trigger_streak_retention_reminder,
    trigger_guardian_weekly_digest
)


class TestPhase94PushAndGuardianNotifications(unittest.IsolatedAsyncioTestCase):
    """
    Test suite for Phase 94: Web Push (VAPID) & Guardian Messaging Bot.
    """

    def setUp(self):
        # Fresh isolated push service instance for clean testing
        self.key_manager = VAPIDKeyManager()
        self.push_service = WebPushService(self.key_manager)
        self.bot_service = GuardianMessagingBotService()

    def test_01_vapid_key_generation_and_rfc8292_format(self):
        """Verifies VAPID uncompressed P-256 public key structure and RFC 8292 formatting."""
        pub_key = self.key_manager.get_public_key()
        self.assertEqual(len(pub_key), 87)

        # Decode raw uncompressed point
        raw_bytes = b64url_decode(pub_key)
        self.assertEqual(len(raw_bytes), 65)
        # First byte must be 0x04 for uncompressed EC point
        self.assertEqual(raw_bytes[0], 0x04)

    def test_02_vapid_jwt_and_authorization_headers(self):
        """Verifies RFC 8292 Authorization headers (vapid t=JWT, k=PubKey)."""
        endpoint = "https://fcm.googleapis.com/fcm/send/sub_device_token_001"
        headers = self.key_manager.build_vapid_headers(endpoint)

        self.assertIn("Authorization", headers)
        self.assertIn("Crypto-Key", headers)

        auth_val = headers["Authorization"]
        self.assertTrue(auth_val.startswith("vapid t="))
        self.assertIn(", k=", auth_val)

        # Extract JWT
        jwt_token = auth_val.split("t=")[1].split(",")[0]
        parts = jwt_token.split(".")
        self.assertEqual(len(parts), 3)

        # Inspect Header and Claims
        header = json.loads(b64url_decode(parts[0]).decode("utf-8"))
        claims = json.loads(b64url_decode(parts[1]).decode("utf-8"))

        self.assertEqual(header["alg"], "ES256")
        self.assertEqual(header["typ"], "JWT")
        self.assertEqual(claims["aud"], "https://fcm.googleapis.com")
        self.assertGreater(claims["exp"], time.time())
        self.assertTrue(claims["sub"].startswith("mailto:"))

    def test_03_web_push_subscription_management(self):
        """Verifies client subscription registration, deduplication, and removal."""
        user_id = "STD_USER_PUSH_01"
        endpoint = "https://updates.push.services.mozilla.com/wpush/v2/test_ep_01"
        p256dh = "BCv7k_example_p256dh_key_base64_string_here"
        auth = "example_auth_secret_key"

        # Subscribe
        sub_res = self.push_service.subscribe(
            user_id=user_id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
            user_agent="Firefox/124.0"
        )
        self.assertEqual(sub_res["status"], "SUBSCRIBED")
        self.assertEqual(sub_res["user_id"], user_id)

        # Verify active subscription
        subs = self.push_service.get_user_subscriptions(user_id)
        self.assertEqual(len(subs), 1)
        self.assertEqual(subs[0]["endpoint"], endpoint)

        # Re-subscribing identical endpoint deduplicates
        self.push_service.subscribe(user_id=user_id, endpoint=endpoint, p256dh=p256dh, auth=auth)
        self.assertEqual(len(self.push_service.get_user_subscriptions(user_id)), 1)

        # Unsubscribe
        unsub_res = self.push_service.unsubscribe(endpoint)
        self.assertEqual(unsub_res["status"], "UNSUBSCRIBED")
        self.assertEqual(len(self.push_service.get_user_subscriptions(user_id)), 0)

    def test_04_direct_push_notification_dispatch(self):
        """Verifies push notification dispatching to active subscriber devices."""
        user_id = "STD_USER_PUSH_02"
        endpoint = "https://fcm.googleapis.com/fcm/send/test_ep_02"
        self.push_service.subscribe(
            user_id=user_id,
            endpoint=endpoint,
            p256dh="key123",
            auth="auth123"
        )

        dispatch_res = self.push_service.send_push_notification(
            user_id=user_id,
            title="লাইভ টেস্ট অ্যালার্ট",
            body="আপনার আজকের রুটিন প্রস্তুত",
            action_url="/schedule"
        )
        self.assertEqual(dispatch_res["status"], "DISPATCHED")
        self.assertEqual(dispatch_res["dispatched_count"], 1)
        self.assertEqual(dispatch_res["payload"]["title"], "লাইভ টেস্ট অ্যালার্ট")
        self.assertEqual(dispatch_res["payload"]["data"]["url"], "/schedule")

    def test_05_scheduled_daily_quiz_reminder_exact_text(self):
        """Verifies daily quiz ready notification with authentic Bengali curriculum text."""
        user_id = "STD_DAILY_QUIZ_USER"
        endpoint = "https://fcm.googleapis.com/fcm/send/test_ep_03"
        self.push_service.subscribe(user_id=user_id, endpoint=endpoint, p256dh="k1", auth="a1")

        res = self.push_service.dispatch_daily_quiz_reminder(
            user_id=user_id,
            chapter="এইচএসসি পদার্থবিজ্ঞান ৩য় অধ্যায়"
        )
        self.assertEqual(res["status"], "DISPATCHED")
        # Assert required exact text
        self.assertEqual(res["payload"]["body"], "আজকের কুইজ প্রস্তুত: এইচএসসি পদার্থবিজ্ঞান ৩য় অধ্যায়")
        self.assertIn("/quiz/practice", res["payload"]["data"]["url"])

    def test_06_scheduled_streak_retention_reminder_exact_text(self):
        """Verifies 5-day study streak retention reminder with exact Bengali text."""
        user_id = "STD_STREAK_USER"
        endpoint = "https://fcm.googleapis.com/fcm/send/test_ep_04"
        self.push_service.subscribe(user_id=user_id, endpoint=endpoint, p256dh="k2", auth="a2")

        res = self.push_service.dispatch_streak_reminder(
            user_id=user_id,
            streak_days=5
        )
        self.assertEqual(res["status"], "DISPATCHED")
        # Assert required exact text
        self.assertEqual(
            res["payload"]["body"],
            "আপনার ৫ দিনের স্টাডি স্ট্রিক ধরে রাখতে আজকের প্র্যাকটিস সম্পন্ন করুন!"
        )
        self.assertEqual(res["payload"]["data"]["url"], "/dashboard/streak")

    def test_07_guardian_weekly_academic_digest_compilation(self):
        """Verifies compilation of weekly academic metrics (study hours, questions, accuracy)."""
        summary = self.bot_service.build_weekly_academic_summary(
            student_id="STD_2026_091",
            student_name="রহিম আহমেদ",
            guardian_id="GRD_VERIFIED_01"
        )
        self.assertEqual(summary.student_name, "রহিম আহমেদ")
        self.assertEqual(summary.total_study_hours, 14.5)
        self.assertEqual(summary.questions_solved, 185)
        self.assertEqual(summary.accuracy_percentage, 84.5)
        self.assertEqual(len(summary.top_mastery_topics), 3)
        self.assertEqual(summary.top_mastery_topics[0]["topic"], "নিউটনিয়ান বলবিদ্যা")

    def test_08_whatsapp_message_formatting_and_zero_emoji(self):
        """Verifies WhatsApp Business API payload formatting, dignified tone, and zero emojis."""
        summary = self.bot_service.build_weekly_academic_summary(
            student_id="STD_2026_091",
            student_name="রহিম আহমেদ",
            guardian_id="GRD_VERIFIED_01"
        )
        wa_payload = self.bot_service.format_whatsapp_digest(summary)

        self.assertEqual(wa_payload["messaging_product"], "whatsapp")
        self.assertEqual(wa_payload["to"], "+8801712345678")
        body_text = wa_payload["text"]["body"]

        # Assert mandatory sections
        self.assertIn("[অগ্রযাত্রা অভিভাবক সাপ্তাহিক রিপোর্ট]", body_text)
        self.assertIn("মোট অধ্যয়নের সময়: ১৪.৫ ঘণ্টা", body_text)
        self.assertIn("সমাধানকৃত প্রশ্ন: ১৮৫টি", body_text)
        self.assertIn("সামগ্রিক নির্ভুলতা: ৮৪.৫%", body_text)
        self.assertIn("নিউটনিয়ান বলবিদ্যা", body_text)
        self.assertIn("শিশু সুরক্ষা ও গোপনীয়তা বিজ্ঞপ্তি:", body_text)

    def test_09_telegram_message_formatting(self):
        """Verifies Telegram Bot API sendMessage markdown formatting."""
        summary = self.bot_service.build_weekly_academic_summary(
            student_id="STD_2026_091",
            student_name="রহিম আহমেদ",
            guardian_id="GRD_VERIFIED_01"
        )
        tg_payload = self.bot_service.format_telegram_digest(summary, chat_id="tg_12345")

        self.assertEqual(tg_payload["chat_id"], "tg_12345")
        self.assertEqual(tg_payload["parse_mode"], "Markdown")
        self.assertIn("অগ্রযাত্রা অভিভাবক সাপ্তাহিক রিপোর্ট", tg_payload["text"])
        self.assertIn("১৪.৫", tg_payload["text"])

    def test_10_child_safety_and_privacy_enforcement(self):
        """Asserts unverified guardians are rejected and private notes are never leaked."""
        # Unverified guardian rejection
        with self.assertRaises(GuardianNotVerifiedError):
            self.bot_service.dispatch_weekly_digest(
                guardian_id="GRD_UNVERIFIED_99",
                student_id="STD_2026_999",
                channel="WHATSAPP"
            )

        # Mismatched student rejection
        with self.assertRaises(GuardianPrivacyViolationError):
            self.bot_service.dispatch_weekly_digest(
                guardian_id="GRD_VERIFIED_01",
                student_id="STD_DIFFERENT_STUDENT",
                channel="WHATSAPP"
            )

        # Verified guardian succeeds and privacy compliance flag is recorded
        dispatch_res = self.bot_service.dispatch_weekly_digest(
            guardian_id="GRD_VERIFIED_01",
            student_id="STD_2026_091",
            channel="WHATSAPP"
        )
        self.assertEqual(dispatch_res["status"], "DISPATCHED")
        body = dispatch_res["payload"]["text"]["body"]
        # Ensure private student notes / chats are NEVER included
        self.assertNotIn("personal_notes", body)
        self.assertNotIn("chat_history", body)

    async def test_11_push_rest_api_endpoints(self):
        """Verifies REST API endpoints for VAPID key, subscribe, scheduled alerts, and guardian digest."""
        # 1. VAPID public key
        key_res = await get_vapid_public_key()
        self.assertEqual(key_res["status"], "SUCCESS")
        self.assertEqual(len(key_res["vapid_public_key"]), 87)

        # 2. Subscribe endpoint
        endpoint = "https://fcm.googleapis.com/fcm/send/api_test_01"
        sub_res = await subscribe_push_client({
            "user_id": "STD_API_USER",
            "endpoint": endpoint,
            "keys": {"p256dh": "dummy_p256", "auth": "dummy_auth"}
        })
        self.assertEqual(sub_res["status"], "SUBSCRIBED")

        # 3. Scheduled Daily Quiz Endpoint
        daily_res = await trigger_daily_quiz_reminder({
            "user_id": "STD_API_USER",
            "chapter": "এইচএসসি পদার্থবিজ্ঞান ৩য় অধ্যায়"
        })
        self.assertEqual(daily_res["status"], "DISPATCHED")

        # 4. Scheduled Streak Reminder Endpoint
        streak_res = await trigger_streak_retention_reminder({
            "user_id": "STD_API_USER",
            "streak_days": 5
        })
        self.assertEqual(streak_res["status"], "DISPATCHED")

        # 5. Guardian Digest Endpoint
        guardian_res = await trigger_guardian_weekly_digest({
            "guardian_id": "GRD_VERIFIED_01",
            "student_id": "STD_2026_091",
            "channel": "WHATSAPP"
        })
        self.assertEqual(guardian_res["status"], "DISPATCHED")

        # 6. Unsubscribe endpoint
        unsub_res = await unsubscribe_push_client({"endpoint": endpoint})
        self.assertEqual(unsub_res["status"], "UNSUBSCRIBED")

    def test_12_service_worker_push_event_handlers(self):
        """Asserts frontend/public/sw.js contains push and notificationclick event listeners."""
        sw_path = "frontend/public/sw.js"
        self.assertTrue(os.path.exists(sw_path))

        with open(sw_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("self.addEventListener('push'", content)
        self.assertIn("self.addEventListener('notificationclick'", content)
        self.assertIn("showNotification", content)
        self.assertIn("openWindow", content)
        self.assertIn("DEVELOPER ARCHITECTURE NOTE (Phase 94", content)

    def test_13_zero_emoji_compliance_across_phase94_files(self):
        """Verifies strict Zero-Emoji compliance across all Phase 94 files."""
        emoji_pattern = re.compile(
            "[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u3030\u303d\u3297\u3299]"
        )

        phase94_files = [
            "backend/app/services/notifications/web_push_service.py",
            "backend/app/services/notifications/guardian_bot_service.py",
            "backend/app/services/notifications/__init__.py",
            "backend/app/api/v1/endpoints/push.py",
            "frontend/public/sw.js",
            "backend/tests/test_phase94_push_and_guardian_notifications.py"
        ]

        for path in phase94_files:
            self.assertTrue(os.path.exists(path), f"File missing: {path}")
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                matches = emoji_pattern.findall(text)
                self.assertEqual(
                    matches, [],
                    f"Found unauthorized emojis in {path}: {matches}"
                )

    def test_14_developer_architecture_notes_presence(self):
        """Verifies every Phase 94 file contains prominent Developer Architecture Notes."""
        files = [
            "backend/app/services/notifications/web_push_service.py",
            "backend/app/services/notifications/guardian_bot_service.py",
            "backend/app/services/notifications/__init__.py",
            "backend/app/api/v1/endpoints/push.py",
            "frontend/public/sw.js",
            "backend/tests/test_phase94_push_and_guardian_notifications.py"
        ]

        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                self.assertIn(
                    "DEVELOPER ARCHITECTURE NOTE",
                    text,
                    f"Missing DEVELOPER ARCHITECTURE NOTE in {path}"
                )


if __name__ == "__main__":
    unittest.main()
