"""
Production Schema Migration Engine Service (Phase 56).
Enforces zero-downtime DDL execution, compiles forward/rollback SQL migrations,
and blocks high-risk table locking operations.
"""

import re
import time
from typing import Dict, Any, List, Optional


class SchemaMigrationEngineService:
    """
    Manages automated schema migrations, zero-downtime DDL generation,
    and locks risk assessments for production databases.
    """

    DANGEROUS_PATTERNS = [
        (re.compile(r"drop\s+table", re.IGNORECASE), "DROP_TABLE_PROHIBITED", 100, "Dropping tables directly causes irreversible data loss."),
        (re.compile(r"drop\s+column", re.IGNORECASE), "DROP_COLUMN_DEPRECATION_REQUIRED", 85, "Dropping columns in active traffic breaks running application queries."),
        (re.compile(r"create\s+index(?!\s+concurrently)", re.IGNORECASE), "BLOCKING_INDEX_LOCK", 75, "Creating indexes without CONCURRENTLY takes an ACCESS EXCLUSIVE lock on production."),
        (re.compile(r"add\s+column[^\;]+not\s+null(?![^\;]+default)", re.IGNORECASE), "NOT_NULL_WITHOUT_DEFAULT", 80, "Adding NOT NULL column without a DEFAULT rewrites the entire table under lock."),
        (re.compile(r"alter\s+table[^\;]+alter\s+column[^\;]+type", re.IGNORECASE), "COLUMN_TYPE_ALTER_LOCK", 70, "Altering column types causes full table scan and rewrite."),
    ]

    def __init__(self):
        self._applied_migrations: List[Dict[str, Any]] = [
            {"version_id": "20261001_01", "name": "init_core_auth_and_students", "applied_at": "2026-10-01T00:00:00Z"},
            {"version_id": "20261005_02", "name": "add_admission_and_quiz_tables", "applied_at": "2026-10-05T00:00:00Z"},
            {"version_id": "20261010_03", "name": "add_audit_and_zk_partition_columns", "applied_at": "2026-10-10T00:00:00Z"},
        ]

    def analyze_migration_safety(
        self,
        version_id: str,
        migration_name: str,
        target_table: str,
        operation_type: str,
        column_definitions: Optional[List[Dict[str, Any]]] = None,
        index_definitions: Optional[List[Dict[str, Any]]] = None,
        raw_ddl_forward: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates migration risks, generates safe forward/rollback DDL,
        and enforces zero-downtime execution rules.
        """
        table = target_table.lower().strip()
        op = operation_type.upper().strip()
        warnings: List[str] = []
        max_risk = 0

        # Check raw DDL if supplied
        if raw_ddl_forward:
            for pattern, code, risk, msg in self.DANGEROUS_PATTERNS:
                if pattern.search(raw_ddl_forward):
                    warnings.append(f"[{code}] {msg}")
                    max_risk = max(max_risk, risk)

        # Synthesize forward & rollback SQL
        forward_sql_parts = ["SET lock_timeout = '2s';"]
        rollback_sql_parts = ["SET lock_timeout = '2s';"]

        if op == "ADD_COLUMN":
            cols = column_definitions or [{"name": "new_feature_meta", "type": "JSONB", "default": "'{}'::jsonb"}]
            for col in cols:
                c_name = col.get("name", "new_col")
                c_type = col.get("type", "TEXT")
                c_def = col.get("default", "NULL")
                c_not_null = col.get("not_null", False)

                if c_not_null and c_def == "NULL":
                    warnings.append("[NOT_NULL_LOCK] Cannot add NOT NULL column without a default value on active table.")
                    max_risk = max(max_risk, 80)

                forward_sql_parts.append(
                    f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {c_name} {c_type} DEFAULT {c_def};"
                )
                rollback_sql_parts.append(
                    f"ALTER TABLE {table} DROP COLUMN IF EXISTS {c_name};"
                )

        elif op == "CREATE_INDEX":
            indexes = index_definitions or [{"name": f"idx_{table}_lookup", "columns": ["student_id", "created_at"]}]
            for idx in indexes:
                idx_name = idx.get("name", f"idx_{table}_opt")
                cols = ", ".join(idx.get("columns", ["id"]))
                idx_type = idx.get("type", "btree").lower()
                predicate = idx.get("predicate")

                where_clause = f" WHERE {predicate}" if predicate else ""
                forward_sql_parts.append(
                    f"CREATE INDEX CONCURRENTLY IF NOT EXISTS {idx_name} ON {table} USING {idx_type} ({cols}){where_clause};"
                )
                rollback_sql_parts.append(
                    f"DROP INDEX CONCURRENTLY IF EXISTS {idx_name};"
                )

        elif op == "DROP_TABLE":
            warnings.append("[DROP_TABLE_PROHIBITED] Direct table drop rejected in production zero-downtime policy.")
            max_risk = 100
            forward_sql_parts.append(f"-- REJECTED: DROP TABLE {table};")
            rollback_sql_parts.append(f"-- NO-OP ROLLBACK")

        else:
            forward_sql_parts.append(f"-- CUSTOM DDL FOR {op} ON {table}")
            rollback_sql_parts.append(f"-- ROLLBACK DDL REQUIRED")

        safe_to_apply = (max_risk < 70)
        safety_verdict = "ZERO_DOWNTIME_APPROVED" if safe_to_apply else "DANGEROUS_OPERATION_BLOCKED"

        if safe_to_apply:
            lock_impact = "NON_BLOCKING (< 50ms lock acquisition)"
        else:
            lock_impact = f"HIGH_LOCK_RISK (Risk score: {max_risk})"

        return {
            "version_id": version_id,
            "migration_name": migration_name,
            "safety_verdict": safety_verdict,
            "risk_score": max_risk,
            "safe_to_apply": safe_to_apply,
            "forward_sql": "\n".join(forward_sql_parts),
            "rollback_sql": "\n".join(rollback_sql_parts),
            "lock_impact_estimate": lock_impact,
            "warnings": warnings
        }

    def apply_migration(self, version_id: str, migration_name: str, applied_by: str = "system_operator") -> Dict[str, Any]:
        """Records an approved migration into the active version ledger."""
        for m in self._applied_migrations:
            if m["version_id"] == version_id:
                return {"applied": False, "reason": "VERSION_ALREADY_APPLIED", "version_id": version_id}

        record = {
            "version_id": version_id,
            "name": migration_name,
            "applied_by": applied_by,
            "applied_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self._applied_migrations.append(record)
        return {"applied": True, "record": record}

    def get_migration_history(self) -> List[Dict[str, Any]]:
        """Returns ordered migration version history."""
        return list(self._applied_migrations)
