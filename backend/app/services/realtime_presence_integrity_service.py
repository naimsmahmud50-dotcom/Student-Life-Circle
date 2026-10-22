# ==============================================================================
# File: backend/app/services/realtime_presence_integrity_service.py
# Phase: 51 - Supabase Realtime Presence Integrity & Ghost Session Reaper
# Topic: Presence HMAC Authentication, Phantom Peer Defense & Zombie Reaper
# Description: Validates Realtime WebSocket presence subscriptions using ephemeral
#              HMAC session signatures, blocks phantom peer injection, and runs
#              an automated heartbeat zombie reaper to prevent ghost participants.
# ==============================================================================

import time
import hmac
import hashlib
import uuid
from typing import Dict, Any, List, Optional, Tuple

class RealtimePresenceIntegrityService:
    """
    Supabase Realtime Presence Integrity & Anti-Phantom Session Guard.
    Secures broadcast and presence channels across collaborative study rooms
    and proctored online exams, purging stale disconnected zombie participants.
    """

    HEARTBEAT_TIMEOUT_SEC = 30.0

    def __init__(self, signing_secret: str = "realtime-presence-hmac-secret-2026"):
        self.signing_secret = signing_secret.encode("utf-8")
        
        # In-memory channel registry: {channel_name: {session_id: peer_dict}}
        self._channels: Dict[str, Dict[str, Any]] = {}
        
        # Telemetry & Security Metrics
        self._stats = {
            "presence_joins_authorized": 0,
            "phantom_injections_blocked": 0,
            "heartbeats_recorded": 0,
            "zombies_reaped": 0
        }

    def generate_presence_ticket(
        self,
        channel_name: str,
        user_id: str,
        user_role: str = "student",
        ttl_seconds: int = 300
    ) -> Dict[str, Any]:
        """Generates an authorized presence join ticket with ephemeral HMAC signature."""
        now = time.time()
        expires_at = now + ttl_seconds
        session_id = f"sess_{uuid.uuid4().hex[:12]}"

        canonical = f"{channel_name}:{user_id}:{session_id}:{user_role}:{expires_at}"
        signature = hmac.new(self.signing_secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()

        return {
            "channel_name": channel_name,
            "user_id": user_id,
            "user_role": user_role,
            "session_id": session_id,
            "expires_at": expires_at,
            "presence_signature": signature,
            "issued_at": now
        }

    def verify_and_join_presence(
        self,
        channel_name: str,
        user_id: str,
        session_id: str,
        user_role: str,
        expires_at: float,
        signature: str,
        client_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Validates presence ticket signature against channel context.
        Rejects phantom peer injections and registers authenticated participant.
        """
        now = time.time()

        # 1. Expiration Check
        if expires_at < now:
            self._stats["phantom_injections_blocked"] += 1
            return {
                "authorized": False,
                "error_code": "TICKET_EXPIRED",
                "message": "Presence ticket has expired. Please re-authenticate."
            }

        # 2. Cryptographic Signature Validation
        canonical = f"{channel_name}:{user_id}:{session_id}:{user_role}:{expires_at}"
        expected_sig = hmac.new(self.signing_secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            self._stats["phantom_injections_blocked"] += 1
            return {
                "authorized": False,
                "error_code": "PHANTOM_INJECTION_DETECTED",
                "message": "Invalid presence signature. Potential phantom peer or session hijacking attack."
            }

        # 3. Register Active Peer in Channel
        if channel_name not in self._channels:
            self._channels[channel_name] = {}

        peer_entry = {
            "session_id": session_id,
            "user_id": user_id,
            "user_role": user_role,
            "joined_at": now,
            "last_heartbeat": now,
            "client_metadata": client_metadata or {}
        }
        self._channels[channel_name][session_id] = peer_entry
        self._stats["presence_joins_authorized"] += 1

        return {
            "authorized": True,
            "channel_name": channel_name,
            "session_id": session_id,
            "active_peer_count": len(self._channels[channel_name]),
            "message": "Presence successfully registered and synchronized."
        }

    def record_heartbeat(self, channel_name: str, session_id: str) -> bool:
        """Records a keepalive heartbeat from an active connected peer."""
        now = time.time()
        channel = self._channels.get(channel_name)
        if channel and session_id in channel:
            channel[session_id]["last_heartbeat"] = now
            self._stats["heartbeats_recorded"] += 1
            return True
        return False

    def reap_zombie_sessions(self, channel_name: str, max_idle_sec: Optional[float] = None) -> List[str]:
        """
        Detects and purges ghost sessions that ceased heartbeating.
        Prevents lingering disconnected avatars in proctored rooms.
        """
        now = time.time()
        timeout = max_idle_sec or self.HEARTBEAT_TIMEOUT_SEC
        reaped_sessions = []

        channel = self._channels.get(channel_name)
        if not channel:
            return []

        expired = [sid for sid, peer in channel.items() if now - peer["last_heartbeat"] > timeout]
        for sid in expired:
            del channel[sid]
            reaped_sessions.append(sid)
            self._stats["zombies_reaped"] += 1

        return reaped_sessions

    def list_active_peers(self, channel_name: str) -> List[Dict[str, Any]]:
        """Returns list of currently active verified participants."""
        channel = self._channels.get(channel_name, {})
        return list(channel.values())

    def get_service_metrics(self) -> Dict[str, Any]:
        """Returns presence security operational metrics."""
        total_peers = sum(len(c) for c in self._channels.values())
        return {
            "stats": dict(self._stats),
            "total_active_channels": len(self._channels),
            "total_connected_peers": total_peers,
            "heartbeat_timeout_sec": self.HEARTBEAT_TIMEOUT_SEC
        }
