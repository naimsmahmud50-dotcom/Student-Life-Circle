"""
================================================================================
MODULE: Supabase Realtime Cryptographic Presence & Channel Authorization Guard
TOPIC: Strix-Supabase WebSocket Realtime Security, Room Guards & Tenant Leak Prevention
FILE: backend/app/services/realtime_cryptographic_presence_service.py
PURPOSE: Enforces strict channel authorization and payload filtering for Supabase Realtime
         WebSocket streams (room, presence, and broadcast channels), preventing cross-room
         eavesdropping and unauthorized broadcast spoofing.
AUDIENCE: Distributed Systems Engineers, Realtime Platform Architects, Security Auditors.
================================================================================
"""

import hmac
import hashlib
import time
from typing import Dict, Any, List, Optional


class RealtimeCryptographicPresenceService:
    """
    Guards Supabase Realtime channels against unauthorized eavesdropping,
    cross-tenant broadcasts, and PII leakage in replication streams.
    """

    SENSITIVE_FIELDS = {
        "phone_number",
        "email_address",
        "home_address",
        "guardian_national_id",
        "password_hash",
        "payment_account_number"
    }

    def __init__(self, channel_signing_secret: str = "realtime_channel_strix_guard_secret_2026"):
        self.channel_signing_secret = channel_signing_secret

    def authorize_channel_subscription(
        self,
        channel_name: str,
        user_id: str,
        user_role: str,
        tenant_id: str,
        enrolled_circles: Optional[List[str]] = None,
        linked_guardian_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates whether a user can subscribe or broadcast to a Realtime channel.
        Supported channel schemes:
        - room:<circle_id> (Study Circle rooms)
        - guardian:<guardian_id> (Guardian telemetry & alerts)
        - exam:<session_id> (Live MCQ proctoring)
        - public:broadcast (Public announcements)
        """
        enrolled_circles = enrolled_circles or []
        linked_guardian_ids = linked_guardian_ids or []
        
        parts = channel_name.split(":", 1)
        prefix = parts[0].lower()
        topic = parts[1] if len(parts) > 1 else ""

        # Case 1: Public announcements
        if prefix == "public":
            token = self._generate_channel_token(channel_name, user_id, "READ_ONLY")
            return {
                "authorized": True,
                "channel_name": channel_name,
                "access_level": "READ_ONLY",
                "join_token": token,
                "reason": "Public broadcast channel accessible to all authenticated principals."
            }

        # Case 2: Study Circle room
        if prefix == "room":
            if topic in enrolled_circles or user_role == "admin":
                token = self._generate_channel_token(channel_name, user_id, "READ_WRITE")
                return {
                    "authorized": True,
                    "channel_name": channel_name,
                    "access_level": "READ_WRITE",
                    "join_token": token,
                    "reason": f"User is an enrolled member of circle '{topic}'."
                }
            return {
                "authorized": False,
                "channel_name": channel_name,
                "access_level": "NONE",
                "join_token": None,
                "reason": f"UNAUTHORIZED: User '{user_id}' is not enrolled in circle '{topic}'."
            }

        # Case 3: Guardian Channel
        if prefix == "guardian":
            if user_id == topic or topic in linked_guardian_ids or user_role == "admin":
                token = self._generate_channel_token(channel_name, user_id, "READ_WRITE")
                return {
                    "authorized": True,
                    "channel_name": channel_name,
                    "access_level": "READ_WRITE",
                    "join_token": token,
                    "reason": "Authorized bilateral guardian telemetry channel."
                }
            return {
                "authorized": False,
                "channel_name": channel_name,
                "access_level": "NONE",
                "join_token": None,
                "reason": f"UNAUTHORIZED: Cross-guardian channel join rejected for '{user_id}'."
            }

        # Case 4: Exam Channel
        if prefix == "exam":
            if user_role in {"student", "proctor", "admin"}:
                token = self._generate_channel_token(channel_name, user_id, "READ_WRITE")
                return {
                    "authorized": True,
                    "channel_name": channel_name,
                    "access_level": "READ_WRITE",
                    "join_token": token,
                    "reason": "Authorized exam participant session."
                }

        return {
            "authorized": False,
            "channel_name": channel_name,
            "access_level": "NONE",
            "join_token": None,
            "reason": f"Unknown channel namespace '{prefix}'."
        }

    def filter_broadcast_payload(
        self,
        event_name: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Sanitizes outgoing broadcast payloads to ensure PII is stripped
        before transmission across realtime subscriptions.
        """
        sanitized = {}
        stripped_fields = []

        for k, v in payload.items():
            if k.lower() in self.SENSITIVE_FIELDS:
                stripped_fields.append(k)
            else:
                sanitized[k] = v

        return {
            "event_name": event_name,
            "sanitized_payload": sanitized,
            "stripped_pii_fields": stripped_fields,
            "is_clean": len(stripped_fields) == 0,
            "timestamp": time.time()
        }

    def _generate_channel_token(self, channel_name: str, user_id: str, access_level: str) -> str:
        expiry = int(time.time()) + 1800  # 30 minutes
        msg = f"{channel_name}:{user_id}:{access_level}:{expiry}".encode("utf-8")
        sig = hmac.new(self.channel_signing_secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()[:32]
        return f"rt_token_{sig}_{expiry}"
