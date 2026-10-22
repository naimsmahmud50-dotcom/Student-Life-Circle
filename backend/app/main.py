"""
========================================================================================
MODULE:    FastAPI Application Factory & ASGI Entrypoint
TOPIC:     Server Lifecycle, CORS Middleware, Security Headers & Router Wiring
FILE:      backend/app/main.py
PURPOSE:   The primary entrypoint for the Student Growth Platform backend. Configures
           FastAPI with Swagger/OpenAPI documentation, registers CORS allowlists,
           attaches request tracing IDs, mounts versioned API routers, and enforces
           OWASP-recommended security headers.
AUDIENCE:  Developers, DevOps, Uvicorn ASGI Runner & AI Agents
STANDARDS: ASGI Standard, OWASP ASVS L2, Clean Architecture
========================================================================================
"""

from backend.app.core.fastapi_shim import FastAPI, Request, CORSMiddleware, JSONResponse, PlainTextResponse
import time
import secrets

from backend.app.core.config import settings
from backend.app.api.v1.router import api_router
from backend.app.core.metrics import metrics_collector
from backend.app.core.sentry import sentry_manager

# Initialize Sentry APM and exception monitoring
sentry_manager.init_sentry()

# -----------------------------------------------------------------------------
# FastAPI Application Initialization
# -----------------------------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "World-class educational companion and exam platform backend for Bangladesh. "
        "Enforces server-authoritative quiz timers, idempotent answer recording, "
        "minor safety guardrails, and single-click question quarantine operations."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# -----------------------------------------------------------------------------
# CORS Middleware Configuration
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Server-Time"],
)


from backend.app.core.middleware import SecurityHeadersMiddleware, DistributedRateLimiterMiddleware
from backend.app.core.security_headers import security_headers
from backend.app.core.rate_limiter import rate_limiter

# -----------------------------------------------------------------------------
# Security Headers & Distributed Rate Limiter Middleware
# -----------------------------------------------------------------------------
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(DistributedRateLimiterMiddleware)


@app.middleware("http")
async def add_security_headers_and_trace_id(request: Request, call_next):
    """
    Attaches unique X-Request-ID for distributed tracing, measures latency,
    evaluates rate limits, and sets OWASP-recommended HTTP security headers.
    """
    request_id = request.headers.get("X-Request-ID", f"req_{secrets.token_hex(8)}")
    start_time = time.time()

    # Rate limiting pre-check
    path = str(request.url.path) if hasattr(request, "url") and hasattr(request.url, "path") else str(getattr(request, "url", "/"))
    client_ip = "127.0.0.1"
    if hasattr(request, "client") and request.client and hasattr(request.client, "host"):
        client_ip = request.client.host

    limiter_mw = DistributedRateLimiterMiddleware(limiter=rate_limiter)
    user_id = limiter_mw._extract_user_id(request, fallback_ip=client_ip)
    is_allowed, remaining, retry_after = limiter_mw.evaluate_request(path, client_ip, user_id)

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

    process_time = (time.time() - start_time) * 1000.0
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    response.headers["X-RateLimit-Remaining"] = str(remaining)

    # Ingress full ASVS L2 / NIST security headers
    for h_key, h_val in security_headers.get_standard_headers().items():
        response.headers[h_key] = h_val

    # Record Prometheus metrics
    metrics_collector.record_request(
        method=request.method if hasattr(request, "method") else "GET",
        endpoint=path,
        status_code=getattr(response, "status_code", 200),
        duration_seconds=process_time / 1000.0
    )

    return response


# -----------------------------------------------------------------------------
# Mount API Routers
# -----------------------------------------------------------------------------
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
async def root():
    """Welcoming landing endpoint for the API service."""
    return {
        "platform": settings.PROJECT_NAME,
        "tagline": "একটি প্রোফাইল। একটি দীর্ঘযাত্রা।",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
        "status": "online"
    }


@app.get("/metrics", tags=["Monitoring"])
async def prometheus_metrics():
    """
    Exposes real-time Prometheus metrics for scrapers and Grafana dashboards.
    Conforms to OpenMetrics / Prometheus exposition 0.0.4 text format.
    """
    content = metrics_collector.generate_prometheus_metrics()
    return PlainTextResponse(content=content, media_type="text/plain; version=0.0.4; charset=utf-8")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
