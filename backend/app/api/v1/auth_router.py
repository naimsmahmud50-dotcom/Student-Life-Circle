"""
========================================================================================
MODULE:    Authentication & User Session Router
TOPIC:     Registration, Login, Token Revocation & Current Profile Endpoints
FILE:      backend/app/api/v1/auth_router.py
PURPOSE:   Exposes REST endpoints for user authentication and session management.
           Handles progressive onboarding, email/phone authentication, minor privacy
           enforcement, and token-based identity resolution.
AUDIENCE:  Frontend Engineers, Integration Testers & AI Agents
STANDARDS: REST OpenAPI 3.1, OWASP ASVS L2, Zero-Trust Access
========================================================================================
"""

from typing import Optional
from backend.app.core.fastapi_shim import APIRouter, Header, HTTPException, status
from backend.app.services.auth_service import auth_service
from backend.app.models.user import EducationStageEnum
from backend.app.schemas.quiz_schema import BaseDTO

def Field(default=..., **kwargs):
    return default

auth_router = APIRouter()


class RegisterRequest(BaseDTO):
    full_name: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    stage: EducationStageEnum = EducationStageEnum.MIDDLE
    class_grade: Optional[int] = None
    medium: str = "BANGLA"
    target_exam: Optional[str] = None


class LoginRequest(BaseDTO):
    identifier: str
    password: str


@auth_router.post("/register", status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def register(payload: RegisterRequest):
    """
    Registers a new student, guardian, or tutor account.
    Applies automatic minor privacy protection if age < 16.
    """
    success, result, reason = auth_service.register_user(
        full_name=payload.full_name,
        password=payload.password,
        email=payload.email,
        phone=payload.phone,
        age=payload.age,
        stage=payload.stage,
        class_grade=payload.class_grade,
        medium=payload.medium,
        target_exam=payload.target_exam
    )

    if not success:
        if reason in ("EMAIL_ALREADY_EXISTS", "PHONE_ALREADY_EXISTS"):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email or phone already registered.")
        elif reason == "PASSWORD_TOO_SHORT":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=reason)

    return {
        "success": True,
        "message": "রেজিস্ট্রেশন সফল হয়েছে।",
        "data": result
    }


@auth_router.post("/login", tags=["Authentication"])
async def login(payload: LoginRequest):
    """
    Authenticates user and returns session credentials.
    """
    success, result, reason = auth_service.authenticate_user(
        identifier=payload.identifier,
        password=payload.password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ভুল ইমেইল/ফোন বা পাসওয়ার্ড।"
        )

    return {
        "success": True,
        "message": "লগইন সফল হয়েছে।",
        "data": result
    }


@auth_router.get("/me", tags=["Authentication"])
async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Returns current active user profile based on bearer token.
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header required.")

    token = authorization.replace("Bearer ", "").strip()
    user_context = auth_service.get_current_user_by_token(token)

    if not user_context:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session.")

    return {
        "success": True,
        "data": user_context
    }


@auth_router.post("/logout", tags=["Authentication"])
async def logout(authorization: Optional[str] = Header(None)):
    """
    Revokes current session token.
    """
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        auth_service.logout_session(token)

    return {
        "success": True,
        "message": "লগআউট সফল হয়েছে।"
    }
