# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 94 - W3C Web Push & VAPID RFC 8292 Service):
# This service implements the W3C Push API and RFC 8292 Voluntary Application
# Server Identification (VAPID) engine for the Student Life Circle platform.
# Architecture & Standards:
# 1. RFC 8292 VAPID Keypair Management:
#    - Generates and manages Elliptic Curve P-256 (prime256v1) keypairs.
#    - Exposes uncompressed 65-byte public keys in URL-safe base64 format without padding.
# 2. VAPID JWT Signing:
#    - Constructs ES256 signed JSON Web Tokens (aud, exp, sub) per push service endpoint origin.
#    - Assembles standard RFC 8292 Authorization headers (vapid t=<jwt>, k=<pub_key>).
# 3. Client Push Subscription Registry:
#    - Persists browser client push subscriptions (endpoint, p256dh, auth, user_id).
#    - Deduplicates subscriptions on endpoint URLs.
# 4. Scheduled Notification Dispatchers:
#    - Daily Quiz Ready: "আজকের কুইজ প্রস্তুত: এইচএসসি পদার্থবিজ্ঞান ৩য় অধ্যায়"
#    - Study Streak Retention: "আপনার ৫ দিনের স্টাডি স্ট্রিক ধরে রাখতে আজকের প্র্যাকটিস সম্পন্ন করুন!"
# 5. Strict Zero-Emoji Governance: All titles, bodies, and logs use formal technical text.
# ==============================================================================

import os
import time
import json
import base64
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from urllib.parse import urlparse

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature


def b64url_encode(data: bytes) -> str:
    """Encodes bytes to URL-safe base64 string without trailing padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(data: str) -> bytes:
    """Decodes URL-safe base64 string adding padding if necessary."""
    rem = len(data) % 4
    if rem > 0:
        data += "=" * (4 - rem)
    return base64.urlsafe_b64decode(data.encode("ascii"))


class VAPIDKeyManager:
    """
    Manages RFC 8292 VAPID Elliptic Curve P-256 keypair and token signatures.
    """

    def __init__(
        self,
        private_key: Optional[ec.EllipticCurvePrivateKey] = None,
        contact_subject: str = "mailto:notifications@studentlifecircle.edu.bd"
    ):
        self.contact_subject = os.getenv("VAPID_CONTACT_SUB", contact_subject)

        # Generate or load EC P-256 private key
        if private_key:
            self._private_key = private_key
        else:
            self._private_key = ec.generate_private_key(ec.SECP256R1())

        self._public_key = self._private_key.public_key()

        # Cache uncompressed point format (65 bytes)
        raw_pub = self._public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        self.public_key_b64 = b64url_encode(raw_pub)

    def get_public_key(self) -> str:
        """Returns VAPID uncompressed public key in URL-safe base64 format."""
        return self.public_key_b64

    def build_vapid_headers(self, endpoint_url: str, ttl_seconds: int = 43200) -> Dict[str, str]:
        """
        Builds RFC 8292 VAPID Authorization and Crypto-Key headers for a target push endpoint.
        """
        parsed = urlparse(endpoint_url)
        audience = f"{parsed.scheme}://{parsed.netloc}"
        exp = int(time.time()) + ttl_seconds

        jwt_header = {"typ": "JWT", "alg": "ES256"}
        jwt_claims = {
            "aud": audience,
            "exp": exp,
            "sub": self.contact_subject
        }

        header_b64 = b64url_encode(json.dumps(jwt_header, separators=(",", ":")).encode("utf-8"))
        claims_b64 = b64url_encode(json.dumps(jwt_claims, separators=(",", ":")).encode("utf-8"))
        signing_input = f"{header_b64}.{claims_b64}".encode("ascii")

        # Sign using ES256 (ECDSA SHA-256)
        der_signature = self._private_key.sign(signing_input, ec.ECDSA(hashes.SHA256()))
        r, s = decode_dss_signature(der_signature)
        raw_signature = r.to_bytes(32, "big") + s.to_bytes(32, "big")
        signature_b64 = b64url_encode(raw_signature)

        jwt_token = f"{signing_input.decode('ascii')}.{signature_b64}"

        return {
            "Authorization": f"vapid t={jwt_token}, k={self.public_key_b64}",
            "Crypto-Key": f"p256ecdsa={self.public_key_b64}"
        }


class WebPushService:
    """
    W3C Web Push Notification engine managing subscriptions, VAPID token generation,
    and scheduled notifications across student devices.
    """

    def __init__(self, key_manager: Optional[VAPIDKeyManager] = None):
        self.key_manager = key_manager or VAPIDKeyManager()
        # Maps endpoint -> subscription record
        self._subscriptions: Dict[str, Dict[str, Any]] = {}
        # Maps user_id -> set of endpoints
        self._user_subscriptions: Dict[str, List[str]] = {}
        # Dispatched notification history log
        self._dispatch_history: List[Dict[str, Any]] = []

    def get_public_key(self) -> str:
        """Returns platform VAPID public key for frontend registration."""
        return self.key_manager.get_public_key()

    def subscribe(
        self,
        user_id: str,
        endpoint: str,
        p256dh: str,
        auth: str,
        user_agent: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Saves client push subscription parameters conforming to W3C Push API.
        """
        clean_user = (user_id or "STD_ANON").strip()
        clean_endpoint = (endpoint or "").strip()

        if not clean_endpoint.startswith("https://") and not clean_endpoint.startswith("http://localhost"):
            raise ValueError("Push subscription endpoint must be a secure HTTPS URL.")
        if not p256dh or not auth:
            raise ValueError("Push subscription requires client p256dh and auth keys.")

        record = {
            "subscription_id": f"sub_{uuid.uuid4().hex[:12]}",
            "user_id": clean_user,
            "endpoint": clean_endpoint,
            "keys": {
                "p256dh": p256dh.strip(),
                "auth": auth.strip()
            },
            "user_agent": user_agent or "Mozilla/5.0 Browser",
            "subscribed_at": datetime.now(timezone.utc).isoformat(),
            "is_active": True
        }

        self._subscriptions[clean_endpoint] = record

        if clean_user not in self._user_subscriptions:
            self._user_subscriptions[clean_user] = []
        if clean_endpoint not in self._user_subscriptions[clean_user]:
            self._user_subscriptions[clean_user].append(clean_endpoint)

        return {
            "status": "SUBSCRIBED",
            "subscription_id": record["subscription_id"],
            "user_id": clean_user,
            "endpoint": clean_endpoint,
            "subscribed_at": record["subscribed_at"]
        }

    def unsubscribe(self, endpoint: str) -> Dict[str, Any]:
        """Removes a client push subscription by endpoint."""
        clean_endpoint = (endpoint or "").strip()
        record = self._subscriptions.pop(clean_endpoint, None)
        if record:
            user_id = record["user_id"]
            if user_id in self._user_subscriptions:
                self._user_subscriptions[user_id] = [
                    ep for ep in self._user_subscriptions[user_id] if ep != clean_endpoint
                ]
            return {
                "status": "UNSUBSCRIBED",
                "endpoint": clean_endpoint,
                "user_id": user_id
            }

        return {
            "status": "NOT_FOUND",
            "endpoint": clean_endpoint
        }

    def get_user_subscriptions(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieves all active push subscriptions for a user."""
        endpoints = self._user_subscriptions.get(user_id, [])
        return [self._subscriptions[ep] for ep in endpoints if ep in self._subscriptions]

    def send_push_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        action_url: str = "/dashboard",
        tag: Optional[str] = None,
        icon: str = "/icons/icon-192x192.png",
        badge: str = "/icons/badge-72x72.png"
    ) -> Dict[str, Any]:
        """
        Constructs and dispatches Web Push payload to all active registered devices of user.
        """
        subscriptions = self.get_user_subscriptions(user_id)
        if not subscriptions:
            return {
                "status": "NO_ACTIVE_SUBSCRIPTION",
                "user_id": user_id,
                "dispatched_count": 0,
                "message": f"No active Web Push subscriptions found for user {user_id}."
            }

        payload_dict = {
            "title": title,
            "body": body,
            "icon": icon,
            "badge": badge,
            "tag": tag or f"slc-{uuid.uuid4().hex[:6]}",
            "data": {
                "url": action_url,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }

        dispatch_results = []
        for sub in subscriptions:
            endpoint = sub["endpoint"]
            vapid_headers = self.key_manager.build_vapid_headers(endpoint)

            delivery_record = {
                "notification_id": f"pnotif_{uuid.uuid4().hex[:12]}",
                "user_id": user_id,
                "endpoint": endpoint,
                "payload": payload_dict,
                "vapid_auth_header": vapid_headers["Authorization"],
                "dispatched_at": datetime.now(timezone.utc).isoformat(),
                "delivery_status": "DELIVERED_SIMULATED"
            }
            self._dispatch_history.append(delivery_record)
            dispatch_results.append(delivery_record)

        return {
            "status": "DISPATCHED",
            "user_id": user_id,
            "dispatched_count": len(dispatch_results),
            "payload": payload_dict,
            "deliveries": dispatch_results
        }

    # --------------------------------------------------------------------------
    # Scheduled Notification Templates (Authentic NCTB & Retention Workflows)
    # --------------------------------------------------------------------------

    def dispatch_daily_quiz_reminder(
        self,
        user_id: str,
        chapter: str = "এইচএসসি পদার্থবিজ্ঞান ৩য় অধ্যায়"
    ) -> Dict[str, Any]:
        """
        Dispatches daily quiz ready notification.
        Exact required Bengali text: 'আজকের কুইজ প্রস্তুত: এইচএসসি পদার্থবিজ্ঞান ৩য় অধ্যায়'
        """
        title = "আজকের কুইজ প্রস্তুত"
        body = f"আজকের কুইজ প্রস্তুত: {chapter}"
        action_url = "/quiz/practice?subject=physics&chapter=3"
        return self.send_push_notification(
            user_id=user_id,
            title=title,
            body=body,
            action_url=action_url,
            tag="daily-quiz-reminder"
        )

    def dispatch_streak_reminder(
        self,
        user_id: str,
        streak_days: int = 5
    ) -> Dict[str, Any]:
        """
        Dispatches study streak retention reminder.
        Exact required Bengali text: 'আপনার ৫ দিনের স্টাডি স্ট্রিক ধরে রাখতে আজকের প্র্যাকটিস সম্পন্ন করুন!'
        """
        title = "স্টাডি স্ট্রিক সতর্কতা"
        streak_bn = to_bengali_digits(streak_days)
        body = f"আপনার {streak_bn} দিনের স্টাডি স্ট্রিক ধরে রাখতে আজকের প্র্যাকটিস সম্পন্ন করুন!"
        action_url = "/dashboard/streak"
        return self.send_push_notification(
            user_id=user_id,
            title=title,
            body=body,
            action_url=action_url,
            tag="streak-retention-reminder"
        )


def to_bengali_digits(val: Any) -> str:
    """Converts ASCII digits to authentic Bengali numerals."""
    s = str(val)
    mapping = {"0": "০", "1": "১", "2": "২", "3": "৩", "4": "৪", "5": "৫", "6": "৬", "7": "৭", "8": "৮", "9": "৯"}
    return "".join(mapping.get(c, c) for c in s)


# Global Web Push Service Instance
web_push_service = WebPushService()

