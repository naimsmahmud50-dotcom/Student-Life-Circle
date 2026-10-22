"""
Schema Drift Detector Service (Phase 56).
Computes SHA-256 cryptographic fingerprints of database schemas,
detects live catalog drift, and synthesizes auto-reconciliation DDL.
"""

import hashlib
import json
from typing import Dict, Any, List, Optional


class SchemaDriftDetectorService:
    """
    Guarantees environment parity between declared code schemas and live database states.
    Identifies missing constraints, unmanaged tables, and mutated column types.
    """

    @classmethod
    def _canonical_json(cls, data: Any) -> str:
        """Serializes schema dictionary deterministically with sorted keys."""
        return json.dumps(data, sort_keys=True, separators=(",", ":"))

    @classmethod
    def calculate_manifest_digest(cls, schema: Dict[str, Any]) -> str:
        """Computes SHA-256 digest of a schema manifest."""
        canonical_str = cls._canonical_json(schema)
        return hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

    @classmethod
    def detect_schema_drift(
        cls,
        environment_name: str,
        declared_schema: Dict[str, Any],
        live_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compares declared schema against live catalog metadata,
        pinpoints specific differences, and generates reconciliation SQL.
        """
        declared_digest = cls.calculate_manifest_digest(declared_schema)
        live_digest = cls.calculate_manifest_digest(live_schema)

        drift_details: List[Dict[str, Any]] = []
        remediation_statements: List[str] = ["SET lock_timeout = '2s';"]

        decl_tables = declared_schema.get("tables", {})
        live_tables = live_schema.get("tables", {})

        # 1. Missing tables in live
        for tbl_name, tbl_spec in decl_tables.items():
            if tbl_name not in live_tables:
                drift_details.append({
                    "drift_type": "MISSING_TABLE",
                    "table": tbl_name,
                    "description": f"Table '{tbl_name}' is declared in specification but missing in live database."
                })
                cols = ", ".join([f"{col} {typ}" for col, typ in tbl_spec.get("columns", {}).items()])
                remediation_statements.append(f"CREATE TABLE IF NOT EXISTS {tbl_name} ({cols});")
            else:
                # 2. Column-level discrepancies
                decl_cols = tbl_spec.get("columns", {})
                live_cols = live_tables[tbl_name].get("columns", {})

                for col_name, col_type in decl_cols.items():
                    if col_name not in live_cols:
                        drift_details.append({
                            "drift_type": "MISSING_COLUMN",
                            "table": tbl_name,
                            "column": col_name,
                            "description": f"Column '{col_name}' ({col_type}) missing in live table '{tbl_name}'."
                        })
                        remediation_statements.append(
                            f"ALTER TABLE {tbl_name} ADD COLUMN IF NOT EXISTS {col_name} {col_type};"
                        )
                    elif live_cols[col_name].upper() != col_type.upper():
                        drift_details.append({
                            "drift_type": "COLUMN_TYPE_MUTATION",
                            "table": tbl_name,
                            "column": col_name,
                            "expected_type": col_type,
                            "live_type": live_cols[col_name],
                            "description": f"Type mismatch for '{tbl_name}.{col_name}': expected {col_type}, found {live_cols[col_name]}."
                        })

                # 3. Missing indexes
                decl_indexes = tbl_spec.get("indexes", [])
                live_indexes = live_tables[tbl_name].get("indexes", [])
                for idx in decl_indexes:
                    if idx not in live_indexes:
                        drift_details.append({
                            "drift_type": "MISSING_INDEX",
                            "table": tbl_name,
                            "index": idx,
                            "description": f"Index '{idx}' declared on '{tbl_name}' is missing in live catalog."
                        })
                        remediation_statements.append(
                            f"CREATE INDEX CONCURRENTLY IF NOT EXISTS {idx} ON {tbl_name} (id);"
                        )

        # 4. Rogue / unmanaged tables in live
        for tbl_name in live_tables:
            if tbl_name not in decl_tables:
                drift_details.append({
                    "drift_type": "UNMANAGED_ROGUE_TABLE",
                    "table": tbl_name,
                    "description": f"Table '{tbl_name}' exists in live database but is not registered in declared schemas."
                })

        drift_detected = len(drift_details) > 0
        parity_status = "DRIFT_ALERT_REMEDIATION_REQUIRED" if drift_detected else "PARITY_SYNCHRONIZED"

        remediation_sql = "\n".join(remediation_statements) if drift_detected else "-- NO REMEDIATION NEEDED (SCHEMA IN PARITY)"

        return {
            "environment_name": environment_name,
            "drift_detected": drift_detected,
            "declared_manifest_digest": declared_digest,
            "live_manifest_digest": live_digest,
            "drift_details": drift_details,
            "remediation_sql": remediation_sql,
            "parity_status": parity_status
        }
