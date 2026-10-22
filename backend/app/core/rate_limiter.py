"""
========================================================================================
MODULE:    Enterprise Sliding-Window Rate Limiter & Brute-Force Shield
TOPIC:     Request Throttling, DoS Protection & HTTP 429 Status Management
FILE:      backend/app/core/rate_limiter.py
PURPOSE:   Enforces NFR-004 rate-limiting and anti-brute-force defense-in-depth:
           - Authentication: Max 5 login attempts / min per client identifier.
           - Quiz Answer Saves: Max 60 saves / min per session to prevent flooding.
           - AI Generation Pipeline: Max 10 drafts / min per content creator.
           - General API Endpoints: Max 120 calls / min per IP.
           Uses an in-memory sliding window log algorithm with microsecond timestamps.
AUDIENCE:  Security Engineers, Infrastructure Architects & AI Agents
STANDARDS: OWASP ASVS 4.0 L2, RFC 6585 (HTTP 429), Zero-Emoji Microcopy
========================================================================================
"""

import time
from typing import Dict, List, Tuple, Any, Optional
from backend.app.core.timekeeper import ServerTimekeeper


class SlidingWindowRateLimiter:
    """
    Sliding-window request throttler with sub-second accuracy.
    """

    DEFAULT_LIMITS = {
        "auth": {"max_requests": 5, "window_seconds": 60},
        "answer_save": {"max_requests": 60, "window_seconds": 60},
        "quiz_submission": {"max_requests": 60, "window_seconds": 60},
        "ai_draft": {"max_requests": 10, "window_seconds": 60},
        "public_search": {"max_requests": 120, "window_seconds": 60},
        "general_api": {"max_requests": 120, "window_seconds": 60}
    }

    def __init__(self):
        # key -> list of float timestamps (epoch seconds)
        self._request_logs: Dict[str, List[float]] = {}
        self._blocked_counter: int = 0

    def check_rate_limit(
        self,
        key: str,
        limit: int,
        window_seconds: int = 60,
        consume: bool = True
    ) -> Tuple[bool, int, int]:
        """
        Evaluates whether a request identified by 'key' is permitted under the rate limit.
        
        Args:
            key: Unique tracking identifier (e.g., 'auth:ip_192.168.1.1' or 'save:att_123').
            limit: Maximum allowed requests within the sliding window.
            window_seconds: Duration of the sliding window in seconds (default: 60).
            consume: If True, records the request if permitted.

        Returns:
            Tuple of (is_allowed: bool, remaining_requests: int, retry_after_seconds: int)
        """
        now = time.time()
        cutoff = now - window_seconds

        # Clean expired timestamps outside the sliding window
        timestamps = self._request_logs.get(key, [])
        valid_timestamps = [t for t in timestamps if t > cutoff]
        self._request_logs[key] = valid_timestamps

        current_count = len(valid_timestamps)

        if current_count >= limit:
            self._blocked_counter += 1
            # Calculate oldest timestamp inside window to determine exact wait time
            oldest_timestamp = valid_timestamps[0] if valid_timestamps else now
            retry_after = max(1, int(oldest_timestamp + window_seconds - now) + 1)
            return False, 0, retry_after

        remaining = limit - current_count - (1 if consume else 0)

        if consume:
            valid_timestamps.append(now)

        return True, max(0, remaining), 0

    # -------------------------------------------------------------------------
    # Policy-Specific Helper Methods
    # -------------------------------------------------------------------------
    def check_auth_limit(self, identifier: str) -> Tuple[bool, int, int]:
        """Enforces max 5 login attempts per minute (Anti-Credential Stuffing)."""
        cfg = self.DEFAULT_LIMITS["auth"]
        return self.check_rate_limit(
            key=f"auth:{identifier}",
            limit=cfg["max_requests"],
            window_seconds=cfg["window_seconds"]
        )

    def check_answer_save_limit(self, session_id: str) -> Tuple[bool, int, int]:
        """Enforces max 60 answer saves per minute per quiz attempt session."""
        cfg = self.DEFAULT_LIMITS["answer_save"]
        return self.check_rate_limit(
            key=f"save:{session_id}",
            limit=cfg["max_requests"],
            window_seconds=cfg["window_seconds"]
        )

    def check_ai_draft_limit(self, user_id: str) -> Tuple[bool, int, int]:
        """Enforces max 10 AI question drafts per minute per editor."""
        cfg = self.DEFAULT_LIMITS["ai_draft"]
        return self.check_rate_limit(
            key=f"ai_draft:{user_id}",
            limit=cfg["max_requests"],
            window_seconds=cfg["window_seconds"]
        )

    def check_quiz_submit_limit(self, user_id: str) -> Tuple[bool, int, int]:
        """Enforces max 60 quiz submissions per minute per user."""
        cfg = self.DEFAULT_LIMITS["quiz_submission"]
        return self.check_rate_limit(
            key=f"quiz_submit:{user_id}",
            limit=cfg["max_requests"],
            window_seconds=cfg["window_seconds"]
        )

    def check_public_search_limit(self, identifier: str) -> Tuple[bool, int, int]:
        """Enforces max 120 search/directory queries per minute per IP."""
        cfg = self.DEFAULT_LIMITS["public_search"]
        return self.check_rate_limit(
            key=f"search:{identifier}",
            limit=cfg["max_requests"],
            window_seconds=cfg["window_seconds"]
        )

    def check_token_bucket(
        self,
        key: str,
        capacity: int = 60,
        fill_rate_per_sec: float = 1.0,
        cost: int = 1
    ) -> Tuple[bool, int, int]:
        """
        Token Bucket rate-limiting algorithm.
        Tokens regenerate continuously at fill_rate_per_sec up to capacity.
        Returns (is_allowed, remaining_tokens, retry_after_seconds).
        """
        now = time.time()
        if not hasattr(self, "_token_buckets"):
            self._token_buckets: Dict[str, Tuple[float, float]] = {}

        tokens, last_fill = self._token_buckets.get(key, (float(capacity), now))
        elapsed = max(0.0, now - last_fill)
        tokens = min(float(capacity), tokens + (elapsed * fill_rate_per_sec))

        if tokens >= cost:
            tokens -= cost
            self._token_buckets[key] = (tokens, now)
            return True, int(tokens), 0
        else:
            self._blocked_counter += 1
            deficit = cost - tokens
            retry_after = max(1, int(deficit / fill_rate_per_sec) + 1) if fill_rate_per_sec > 0 else 60
            self._token_buckets[key] = (tokens, now)
            return False, int(tokens), retry_after

    def reset_key(self, key: str) -> None:
        """Clears request history for a specific key (e.g. after successful MFA/captcha)."""
        self._request_logs.pop(key, None)

    def clear_all(self) -> None:
        """Clears all in-memory rate-limit buckets (useful for test suites)."""
        self._request_logs.clear()
        self._blocked_counter = 0

    def get_metrics(self) -> Dict[str, Any]:
        """Returns diagnostic metrics on rate-limiter activity."""
        return {
            "active_tracked_keys": len(self._request_logs),
            "total_throttled_requests": self._blocked_counter,
            "policy_limits": self.DEFAULT_LIMITS,
            "evaluated_at": ServerTimekeeper.get_server_iso_now()
        }


# Singleton export
rate_limiter = SlidingWindowRateLimiter()
