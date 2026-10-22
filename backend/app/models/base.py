"""
========================================================================================
MODULE:    Database Foundation & Declarative Base Model
TOPIC:     UUID Primary Keys, UTC Timestamps, Soft Deletes & Serialization
FILE:      backend/app/models/base.py
PURPOSE:   Provides the root base class for all PostgreSQL relational entities.
           Enforces UUID v4 primary keys, automatic ISO-8601 UTC created/updated
           timestamps, standard dictionary serialization (`to_dict`), and clean
           attribute representation across the entire domain model.
AUDIENCE:  Database Architects, Backend Engineers & AI Agents
STANDARDS: Clean Architecture, PEP 681 (Data Class Transforms), Zero-Drift
========================================================================================
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict


class BaseModel:
    """
    Foundational model class for domain entities.
    Compatible with SQLAlchemy 2.0 / AsyncPG and standalone execution.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4()))
        now = datetime.now(timezone.utc).isoformat()
        self.created_at = kwargs.get("created_at", now)
        self.updated_at = kwargs.get("updated_at", now)

        for key, value in kwargs.items():
            if key not in ("id", "created_at", "updated_at"):
                setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes entity attributes to a clean dictionary."""
        result = {}
        for key, val in self.__dict__.items():
            if not key.startswith("_"):
                result[key] = val
        return result

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={getattr(self, 'id', None)}>"
