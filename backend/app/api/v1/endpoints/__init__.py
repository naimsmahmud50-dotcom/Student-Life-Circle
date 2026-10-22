# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 82 - API Endpoints Init):
# Exports modular routers for WebSocket, Payments, and SMS OTP / Guardian Consent.
# Zero-Emoji Policy Enforced.
# ==============================================================================

from backend.app.api.v1.endpoints.websocket import router as websocket_router
from backend.app.api.v1.endpoints.payments import router as payments_router
from backend.app.api.v1.endpoints.auth_otp import router as auth_otp_router
from backend.app.api.v1.endpoints.study_pods import router as study_pods_router
from backend.app.api.v1.endpoints.grading import router as grading_router

__all__ = ["websocket_router", "payments_router", "auth_otp_router", "study_pods_router", "grading_router"]

