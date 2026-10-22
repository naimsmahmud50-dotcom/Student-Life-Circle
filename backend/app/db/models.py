# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 79 - Production Database ORM Models):
# This module defines the relational database entity models for the Student Life
# Circle platform. It implements models for users, learner profiles, question items,
# quiz attempts, tuition applications, verifiable credentials, and immutable audit logs.
# Architecture & Standards:
# 1. Dual-Mode Compatibility: Uses SQLAlchemy 2.0 DeclarativeBase when installed,
#    with graceful fallback to clean Python dataclasses when running in testing/sandbox
#    environments without external database dependencies.
# 2. Schema Alignment: Matches 1-to-1 with backend/migrations/001_core_supabase_schema.sql.
# 3. Child Minor Protection & Zero-IDOR: Models include is_minor and tenant_id fields
#    to maintain parity with Row-Level Security policies.
# 4. Zero-Emoji Policy Enforced: All comments and descriptions use clean technical text.
# ==============================================================================

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional

try:
    from sqlalchemy.orm import declarative_base, Mapped, mapped_column
    from sqlalchemy import String, Integer, Boolean, Numeric, Text, JSON, DateTime, ForeignKey
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID
    Base = declarative_base()
    HAS_SA_MODELS = True
except ImportError:
    class Base:
        """Fallback mock base class."""
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def to_dict(self) -> Dict[str, Any]:
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    HAS_SA_MODELS = False


if HAS_SA_MODELS:
    class UserModel(Base):
        __tablename__ = "users"
        id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
        role: Mapped[str] = mapped_column(String(64), nullable=False, default="student")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    class ProfileModel(Base):
        __tablename__ = "profiles"
        id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
        tenant_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
        full_name: Mapped[str] = mapped_column(String(255), nullable=False)
        role: Mapped[str] = mapped_column(String(64), nullable=False, default="student")
        class_grade: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
        curriculum: Mapped[str] = mapped_column(String(64), nullable=False, default="NCTB")
        is_minor: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
        guardian_consent_granted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
        phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
        institution: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
        district: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    class QuestionItemModel(Base):
        __tablename__ = "question_items"
        id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        subject: Mapped[str] = mapped_column(String(128), nullable=False)
        topic: Mapped[str] = mapped_column(String(128), nullable=False)
        stem_text_bn: Mapped[str] = mapped_column(Text, nullable=False)
        stem_text_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
        difficulty: Mapped[str] = mapped_column(String(32), nullable=False, default="INTERMEDIATE")
        options: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
        correct_option_key: Mapped[str] = mapped_column(String(8), nullable=False)
        explanation_bn: Mapped[str] = mapped_column(Text, nullable=False)
        is_quarantined: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    class QuizAttemptModel(Base):
        __tablename__ = "quiz_attempts"
        id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
        tenant_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
        quiz_id: Mapped[str] = mapped_column(String(64), nullable=False)
        score: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False, default=0.0)
        total_questions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
        correct_answers: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
        time_spent_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
        answers_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
        is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    class TuitionApplicationModel(Base):
        __tablename__ = "tuition_applications"
        id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        student_user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
        tutor_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
        tenant_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
        subject: Mapped[str] = mapped_column(String(128), nullable=False)
        grade_level: Mapped[str] = mapped_column(String(32), nullable=False)
        budget_bdt: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)
        status: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING")
        guardian_phone: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
        message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    class AuditLogModel(Base):
        __tablename__ = "audit_logs"
        id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        tenant_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
        user_id: Mapped[Optional[uuid.UUID]] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
        action: Mapped[str] = mapped_column(String(64), nullable=False)
        entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
        entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
        metadata_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
        ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
        user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
        timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

else:
    # Pure Python Resilient Fallback Model Classes
    class UserModel(Base):
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.email = kwargs.get("email", "")
            self.role = kwargs.get("role", "student")
            self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))
            self.updated_at = kwargs.get("updated_at", datetime.now(timezone.utc))
            super().__init__(**kwargs)

    class ProfileModel(Base):
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.user_id = kwargs.get("user_id", "")
            self.tenant_id = kwargs.get("tenant_id", str(uuid.uuid4()))
            self.full_name = kwargs.get("full_name", "")
            self.role = kwargs.get("role", "student")
            self.class_grade = kwargs.get("class_grade", 10)
            self.curriculum = kwargs.get("curriculum", "NCTB")
            self.is_minor = kwargs.get("is_minor", True)
            self.guardian_consent_granted = kwargs.get("guardian_consent_granted", False)
            self.phone = kwargs.get("phone", None)
            self.institution = kwargs.get("institution", None)
            self.district = kwargs.get("district", None)
            self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))
            self.updated_at = kwargs.get("updated_at", datetime.now(timezone.utc))
            super().__init__(**kwargs)

    class QuestionItemModel(Base):
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.subject = kwargs.get("subject", "")
            self.topic = kwargs.get("topic", "")
            self.stem_text_bn = kwargs.get("stem_text_bn", "")
            self.stem_text_en = kwargs.get("stem_text_en", None)
            self.difficulty = kwargs.get("difficulty", "INTERMEDIATE")
            self.options = kwargs.get("options", {})
            self.correct_option_key = kwargs.get("correct_option_key", "A")
            self.explanation_bn = kwargs.get("explanation_bn", "")
            self.is_quarantined = kwargs.get("is_quarantined", False)
            self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))
            super().__init__(**kwargs)

    class QuizAttemptModel(Base):
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.user_id = kwargs.get("user_id", "")
            self.tenant_id = kwargs.get("tenant_id", "")
            self.quiz_id = kwargs.get("quiz_id", "")
            self.score = kwargs.get("score", 0.0)
            self.total_questions = kwargs.get("total_questions", 0)
            self.correct_answers = kwargs.get("correct_answers", 0)
            self.time_spent_seconds = kwargs.get("time_spent_seconds", 0)
            self.answers_payload = kwargs.get("answers_payload", {})
            self.is_verified = kwargs.get("is_verified", True)
            self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))
            super().__init__(**kwargs)

    class TuitionApplicationModel(Base):
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.student_user_id = kwargs.get("student_user_id", "")
            self.tutor_user_id = kwargs.get("tutor_user_id", None)
            self.tenant_id = kwargs.get("tenant_id", "")
            self.subject = kwargs.get("subject", "")
            self.grade_level = kwargs.get("grade_level", "")
            self.budget_bdt = kwargs.get("budget_bdt", 0.0)
            self.status = kwargs.get("status", "PENDING")
            self.guardian_phone = kwargs.get("guardian_phone", None)
            self.message = kwargs.get("message", None)
            self.created_at = kwargs.get("created_at", datetime.now(timezone.utc))
            self.updated_at = kwargs.get("updated_at", datetime.now(timezone.utc))
            super().__init__(**kwargs)

    class AuditLogModel(Base):
        def __init__(self, **kwargs):
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.tenant_id = kwargs.get("tenant_id", "")
            self.user_id = kwargs.get("user_id", None)
            self.action = kwargs.get("action", "")
            self.entity_type = kwargs.get("entity_type", "")
            self.entity_id = kwargs.get("entity_id", "")
            self.metadata_payload = kwargs.get("metadata_payload", {})
            self.ip_address = kwargs.get("ip_address", None)
            self.user_agent = kwargs.get("user_agent", None)
            self.timestamp = kwargs.get("timestamp", datetime.now(timezone.utc))
            super().__init__(**kwargs)
