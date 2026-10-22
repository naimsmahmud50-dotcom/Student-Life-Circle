"""
========================================================================================
MODULE:    FastAPI Enterprise Security & Distributed Rate Limiter Middleware
TOPIC:     OWASP ASVS L2 Defense-in-Depth, Security Headers & RFC 6585 Throttling
FILE:      backend/app/core/middleware.py
PURPOSE:   Provides enterprise middleware layers for the FastAPI ASGI application:
           1. SecurityHeadersMiddleware: Enforces strict Content-Security-Policy (CSP),
              X-Content-Type-Options: nosniff, X-Frame-Options: DENY,
              Strict-Transport-Security: max-age=63072000; includeSubDomains; preload,
              Referrer-Policy: strict-origin-when-cross-origin,
              Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(),
              and X-XSS-Protection: 1; mode=block. Also attaches distributed tracing
              X-Request-ID and X-Process-Time-Ms headers.
           2. DistributedRateLimiterMiddleware: Enforces multi-tier rate limiting:
              - Auth endpoints: 5 attempts/min per IP
              - Quiz submissions: 60 requests/min per user
              - Public search/directory: 120 requests/min per IP
              Throttled requests receive RFC 6585 HTTP 429 Too Many Requests with
              a mandatory Retry-After header.
AUDIENCE:  Security Compliance Engineers, DevOps & AI Agents
STANDARDS: OWASP ASVS 4.0 L2, NIST SP 800-53, RFC 6585, Strict Zero-Emoji Spec
========================================================================================
"""

import time
import secrets
from typing import Dict, Any, Optional, Callable
from backend.app.core.fastapi_shim import Request, JSONResponse, BaseHTTPMiddleware, status
from backend.app.core.security_headers import security_headers, SecurityHeadersManager
from backend.app.core.rate_limiter import rate_limiter, SlidingWindowRateLimiter


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    ASGI middleware enforcing OWASP ASVS Level 2 defense-in-depth security headers
    and distributed request tracing identifiers.
    """

    def __init__(self, app=None):
        super().__init__(app=app)
        self.headers_manager = security_headers

    async def dispatch(self, request: Request, call_next: Callable):
        request_id = request.headers.get("X-Request-ID") if hasattr(request, "headers") else None
        if not request_id:
            request_id = f"req_{secrets.token_hex(8)}"

        start_time = time.time()
        response = await call_next(request)
        process_time_ms = (time.time() - start_time) * 1000.0

        standard_headers = self.headers_manager.get_standard_headers()
        for header_key, header_val in standard_headers.items():
            response.headers[header_key] = header_val

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = f"{process_time_ms:.2f}"

        return response


class DistributedRateLimiterMiddleware(BaseHTTPMiddleware):
    """
    ASGI middleware enforcing multi-tier request rate limiting via Redis token bucket
    and sliding window algorithms. Returns RFC 6585 HTTP 429 when limits are exceeded.
    """

    def __init__(self, app=None, limiter: Optional[SlidingWindowRateLimiter] = None):
        super().__init__(app=app)
        self.limiter = limiter or rate_limiter

    def _extract_client_ip(self, request: Request) -> str:
        """Extracts the true client IP from forwarded headers or direct connection."""
        if hasattr(request, "headers") and request.headers:
            x_forwarded = request.headers.get("X-Forwarded-For")
            if x_forwarded:
                return x_forwarded.split(",")[0].strip()
            x_real_ip = request.headers.get("X-Real-IP")
            if x_real_ip:
                return x_real_ip.strip()

        if hasattr(request, "client") and request.client:
            if hasattr(request.client, "host"):
                return request.client.host
            elif isinstance(request.client, (tuple, list)) and len(request.client) > 0:
                return str(request.client[0])

        return "127.0.0.1"

    def _extract_user_id(self, request: Request, fallback_ip: str) -> str:
        """Extracts authenticated user identifier or falls back to client IP."""
        if hasattr(request, "headers") and request.headers:
            user_id = request.headers.get("x-user-id") or request.headers.get("X-User-ID")
            if user_id:
                return user_id

        # Check query string params if available
        if hasattr(request, "query_params") and request.query_params:
            user_id = request.query_params.get("user_id")
            if user_id:
                return user_id

        return fallback_ip

    def evaluate_request(self, path: str, client_ip: str, user_id: str) -> tuple[bool, int, int]:
        """
        Determines the applicable rate limit policy based on endpoint path and evaluates quota.
        Returns (is_allowed, remaining, retry_after).
        """
        clean_path = path.lower()

        # 1. Authentication Endpoints: 5 attempts / min per IP
        if "/auth" in clean_path or "/otp" in clean_path:
            return self.limiter.check_auth_limit(identifier=client_ip)

        # 2. Quiz Submission & Answer Save Endpoints: 60 requests / min per user
        if "/quiz-attempts" in clean_path and ("/submit" in clean_path or "/answers" in clean_path):
            return self.limiter.check_quiz_submit_limit(user_id=user_id)

        # 3. Public Search & Directory Endpoints: 120 requests / min per IP
        if "/search" in clean_path or clean_path.endswith("/jobs") or "/tuition" in clean_path:
            return self.limiter.check_public_search_limit(identifier=client_ip)

        # 4. General API Endpoints: 120 requests / min per IP
        return self.limiter.check_rate_limit(key=f"gen:{client_ip}", limit=120, window_seconds=60)

    async def dispatch(self, request: Request, call_next: Callable):
        path = str(request.url.path) if hasattr(request, "url") and hasattr(request.url, "path") else str(request.url)
        client_ip = self._extract_client_ip(request)
        user_id = self._extract_user_id(request, fallback_ip=client_ip)

        is_allowed, remaining, retry_after = self.evaluate_request(path=path, client_ip=client_ip, user_id=user_id)

        if not is_allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Rate limit exceeded. Please wait before retrying.",
                    "error_code": "RATE_LIMIT_EXCEEDED",
                    "retry_after": retry_after,
                    "status_code": 429
                },
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": "Throttled",
                    "X-RateLimit-Remaining": "0"
                }
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
