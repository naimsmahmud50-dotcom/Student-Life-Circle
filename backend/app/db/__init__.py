# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 79 - Database Package Init):
# Exposes the session manager, database health check, models, and session generators
# for the Student Life Circle database layer.
# Zero-Emoji Policy Enforced.
# ==============================================================================

from backend.app.db.session import (
    db_manager,
    get_async_session,
    DatabaseSessionManager,
    FallbackAsyncSession
)
from backend.app.db.models import (
    UserModel,
    ProfileModel,
    QuestionItemModel,
    QuizAttemptModel,
    TuitionApplicationModel,
    AuditLogModel
)

__all__ = [
    "db_manager",
    "get_async_session",
    "DatabaseSessionManager",
    "FallbackAsyncSession",
    "UserModel",
    "ProfileModel",
    "QuestionItemModel",
    "QuizAttemptModel",
    "TuitionApplicationModel",
    "AuditLogModel"
]
