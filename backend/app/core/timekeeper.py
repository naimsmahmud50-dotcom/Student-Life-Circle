"""
========================================================================================
MODULE:    Server-Authoritative Timekeeper & Exam Clock Manager
TOPIC:     NTP Clock Synchronization, Session Window Validation & Anti-Tampering
FILE:      backend/app/core/timekeeper.py
PURPOSE:   Enforces server authority over all examination timers. Guarantees that
           students cannot cheat or extend test durations by modifying their local
           device clocks. Computes exact remaining seconds, validates active start
           windows, and flags abnormal client-timestamp deviations for audit.
AUDIENCE:  Developers, Exam Security Reviewers & AI Agents
STANDARDS: Server-Authoritative State, Anti-Cheat, High Concurrency
========================================================================================
"""

from datetime import datetime, timezone
from typing import Tuple, Dict, Any


class ServerTimekeeper:
    """
    Central timekeeper for high-stakes examinations and practice sets.
    Anchors all timing calculations to UTC timestamps derived strictly from the server.
    """

    @staticmethod
    def get_server_utc_now() -> datetime:
        """Returns the current trusted UTC timestamp from the server clock."""
        return datetime.now(timezone.utc)

    @staticmethod
    def get_server_iso_now() -> str:
        """Returns ISO 8601 formatted string for API responses."""
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def validate_session_window(
        cls,
        session_start: datetime,
        session_end: datetime,
        client_timestamp: float = None
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validates whether the current moment falls strictly within the live exam window.
        Detects significant client-server clock skew to alert students of potential desync.
        """
        now = cls.get_server_utc_now()

        # Ensure timezone awareness
        if session_start.tzinfo is None:
            session_start = session_start.replace(tzinfo=timezone.utc)
        if session_end.tzinfo is None:
            session_end = session_end.replace(tzinfo=timezone.utc)

        # Skew detection
        skew_warning = None
        if client_timestamp:
            client_dt = datetime.fromtimestamp(client_timestamp, tz=timezone.utc)
            skew_seconds = abs((now - client_dt).total_seconds())
            if skew_seconds > 5.0:
                skew_warning = f"Client clock skewed by {skew_seconds:.1f}s relative to server."

        if now < session_start:
            seconds_until_start = (session_start - now).total_seconds()
            return False, "SESSION_NOT_STARTED", {
                "server_time": now.isoformat(),
                "seconds_until_start": max(0, int(seconds_until_start)),
                "skew_warning": skew_warning
            }

        if now > session_end:
            return False, "SESSION_CLOSED", {
                "server_time": now.isoformat(),
                "closed_at": session_end.isoformat(),
                "skew_warning": skew_warning
            }

        remaining_seconds = (session_end - now).total_seconds()
        return True, "ACTIVE", {
            "server_time": now.isoformat(),
            "remaining_seconds": max(0, int(remaining_seconds)),
            "skew_warning": skew_warning
        }

    @classmethod
    def calculate_attempt_remaining_seconds(
        cls,
        expires_at: datetime
    ) -> int:
        """
        Calculates remaining seconds for an active individual attempt.
        Returns 0 if already expired.
        """
        now = cls.get_server_utc_now()
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        remaining = (expires_at - now).total_seconds()
        return max(0, int(remaining))

    @classmethod
    def is_attempt_expired(cls, expires_at: datetime) -> bool:
        """Checks if attempt is past the server deadline."""
        return cls.calculate_attempt_remaining_seconds(expires_at) <= 0
