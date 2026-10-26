"""
========================================================================================
MODULE:    Core Configuration & Environment Management
TOPIC:     App Settings, Security Secrets, Database & Redis Connection Specs
FILE:      backend/app/core/config.py
PURPOSE:   Centralized application settings. Supports both Pydantic Settings and
           standard library fallback for zero-dependency portability across any
           Python 3.12+ environment. Manages PostgreSQL connection strings, Redis,
           JWT signing secrets, token expirations, and CORS allowlists.
AUDIENCE:  Developers, DevOps Engineers & AI Agents
STANDARDS: 12-Factor App, OWASP ASVS L2, Python 3.12+ Strict Typing
========================================================================================
"""

import os
from typing import List, Union

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from pydantic import field_validator

    class Settings(BaseSettings):
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=True,
            extra="ignore"
        )
        PROJECT_NAME: str = "Student Growth Platform (অগ্রযাত্রা)"
        VERSION: str = "2.0.0"
        API_V1_STR: str = "/api/v1"
        ENVIRONMENT: str = "development"
        DEBUG: bool = False
        SECRET_KEY: str = "super_secure_secret_key_change_in_production_min_32_bytes_long"
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
        DATABASE_URL: str = "postgresql+asyncpg://student_admin:student_secure_password@localhost:5432/student_growth_platform"
        REDIS_URL: str = "redis://localhost:6379/0"
        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://studentlifecircle.com",
            "https://ogrojatra.edu.bd"
        ]
        FEATURE_EXAM_ROUTINE: bool = False
        FEATURE_STUDY_ARCHIVE: bool = False
        FEATURE_CIRCULAR_ALERT: bool = False

    settings = Settings()

except ImportError:
    # Zero-dependency Fallback for Python Standard Library
    class Settings:
        PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Student Growth Platform (অগ্রযাত্রা)")
        VERSION: str = "2.0.0"
        API_V1_STR: str = "/api/v1"
        ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
        SECRET_KEY: str = os.getenv("SECRET_KEY", "super_secure_secret_key_change_in_production_min_32_bytes_long")
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", str(60 * 24)))
        DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://student_admin:student_secure_password@localhost:5432/student_growth_platform")
        REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        BACKEND_CORS_ORIGINS: List[str] = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "https://studentlifecircle.com",
            "https://ogrojatra.edu.bd"
        ]
        FEATURE_EXAM_ROUTINE: bool = os.getenv("FEATURE_EXAM_ROUTINE", "False").lower() == "true"
        FEATURE_STUDY_ARCHIVE: bool = os.getenv("FEATURE_STUDY_ARCHIVE", "False").lower() == "true"
        FEATURE_CIRCULAR_ALERT: bool = os.getenv("FEATURE_CIRCULAR_ALERT", "False").lower() == "true"

    settings = Settings()
