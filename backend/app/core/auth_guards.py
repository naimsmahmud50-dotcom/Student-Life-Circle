"""
========================================================================================
MODULE:    Enterprise Server-Side RBAC & Authentication Guard
TOPIC:     Strict 401 vs 403 HTTP Separation, Session Verification & Role Authorization
FILE:      backend/app/core/auth_guards.py
PURPOSE:   Enforces server-side authentication and role-based access control (RBAC).
           Protects sensitive administrative endpoints against unauthenticated access (401)
           and unauthorized/insufficient privileges (403). Client guards must never be
           the sole protection.
AUDIENCE:  FastAPI Routers, Integration Testers & Security Auditors
STANDARDS: OWASP ASVS L2, Zero-Trust Architecture, Clean Architecture
========================================================================================
"""

from typing import List, Optional, Dict, Any
from backend.app.core.fastapi_shim import Header, HTTPException, status
from backend.app.services.auth_service import auth_service
from backend.app.models.user import UserRoleEnum


def get_current_user_context(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    """
    Extracts Bearer token from authorization header, validates session,
    and returns verified user context dict containing user, profile, and roles.
    Raises HTTP 401 if missing, invalid, or expired.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="প্রবেশাধিকার অস্বীকৃত: অথরাইজেশন হেডার অনুপস্থিত (Authorization header required)."
        )

    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="প্রবেশাধিকার অস্বীকৃত: ইনভ্যালিড বিয়ারার টোকেন (Invalid bearer token format)."
        )

    user_context = auth_service.get_current_user_by_token(token)
    if not user_context:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="সেশন মেয়াদোত্তীর্ণ বা অকার্যকর (Invalid or expired session)."
        )

    return user_context


def require_roles(allowed_roles: List[UserRoleEnum]):
    """
    Factory creating a role-enforcement dependency.
    Raises 401 if unauthenticated, and 403 if authenticated user lacks required roles.
    """
    def role_checker(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
        user_context = get_current_user_context(authorization)
        user_roles = user_context.get("roles", [])

        # Check if user has any of the allowed roles
        allowed_values = [r.value if hasattr(r, "value") else str(r) for r in allowed_roles]
        has_permission = any(str(role).upper() in allowed_values for role in user_roles)

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"অননুমোদিত প্রবেশাধিকার: এই অপারেশনটির জন্য আবশ্যক রোল {allowed_values}। "
                    f"আপনার বর্তমান রোল: {user_roles} (Forbidden: insufficient privileges)."
                )
            )

        return user_context

    return role_checker


# Canonical pre-configured role dependencies
require_admin_or_reviewer = require_roles([UserRoleEnum.ADMIN, UserRoleEnum.SUBJECT_REVIEWER])
require_full_admin = require_roles([UserRoleEnum.ADMIN])
