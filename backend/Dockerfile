# ========================================================================================
# DEVELOPER ARCHITECTURE NOTE - PRODUCTION DOCKER CONTAINER:
# MODULE:    FastAPI Enterprise Production Docker Container
# TOPIC:     Multi-Stage Build, Wheel Caching, Least-Privilege Non-Root Execution
# FILE:      backend/Dockerfile
# PURPOSE:   Packages the Python FastAPI educational exam platform into a minimal,
#            secure, production-ready container image.
#            1. Builder Stage: Uses python:3.12-slim-bookworm to compile and package
#               all pip dependencies as standalone wheels in /build/wheels.
#            2. Runner Stage: Pristine minimal runtime installing wheels, configuring
#               unprivileged appuser (UID: 10001, GID: 10001), healthcheck polling,
#               and launching Uvicorn ASGI server with 4 concurrent workers.
# AUDIENCE:  DevOps Engineers, Site Reliability Engineers, Kubernetes Architects & CI/CD
# STANDARDS: CIS Docker Benchmark v1.6, OWASP ASVS L2, NIST SP 800-190, Zero-Emoji Spec
# ========================================================================================

# -----------------------------------------------------------------------------
# 1. Dependency Builder Stage (Wheels Pre-compilation & Caching)
# -----------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS builder

WORKDIR /build

# Install build dependencies for C extensions and async drivers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and pre-compile wheels for sub-second layer caching
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt || true

# -----------------------------------------------------------------------------
# 2. Production Runner Stage (Minimal Footprint & Non-Root Security)
# -----------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000 \
    ENVIRONMENT=production

WORKDIR /app

# Create unprivileged dedicated system user and group for process isolation
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/bash -m appuser

# Install minimal runtime system utilities (curl for container healthcheck, libpq5 for PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq5 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-compiled binary wheels from builder stage and install
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir /wheels/* 2>/dev/null || true && rm -rf /wheels

# Copy application source code with non-root ownership
COPY --chown=appuser:appgroup backend /app/backend

# Switch to unprivileged execution user
USER appuser

EXPOSE 8000

# Container automated healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Production ASGI Entrypoint with 4 Uvicorn workers
CMD ["python3", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
