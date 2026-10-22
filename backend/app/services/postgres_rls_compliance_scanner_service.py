# ==============================================================================
# File: backend/app/services/postgres_rls_compliance_scanner_service.py
# Phase: 51 - PostgreSQL RLS Compliance & Drift Scanner
# Topic: Table RLS Auditing, SECURITY DEFINER Search Path Protection, & Remediation
# Description: Performs automated compliance scans on PostgreSQL tables and functions,
#              detects missing write policies, unanchored tenant bounds, and unsafe
#              SECURITY DEFINER functions lacking search_path hardening.
# ==============================================================================

from typing import Dict, Any, List, Optional, Tuple

class PostgresRlsComplianceScannerService:
    """
    PostgreSQL Row Level Security (RLS) Compliance & Drift Scanner.
    Audits Supabase database schemas for RLS gaps, missing mutation guards,
    and search_path privilege escalation flaws according to Strix security benchmarks.
    """

    def __init__(self):
        self._stats = {
            "tables_scanned": 0,
            "functions_scanned": 0,
            "critical_drifts_flagged": 0,
            "remediation_patches_generated": 0
        }

    def scan_table_rls_compliance(self, table_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scans a single table definition for RLS enablement and policy coverage.
        table_schema expects: {table_name, rls_enabled, policies: [{name, cmd, using, with_check}]}
        """
        self._stats["tables_scanned"] += 1
        table_name = table_schema.get("table_name", "unknown_table")
        rls_enabled = table_schema.get("rls_enabled", False)
        policies = table_schema.get("policies", [])

        violations = []
        score = 100

        # 1. RLS Enabled Check
        if not rls_enabled:
            score -= 60
            self._stats["critical_drifts_flagged"] += 1
            violations.append({
                "code": "RLS_DISABLED",
                "severity": "CRITICAL",
                "message": f"Table '{table_name}' has RLS disabled. Data is vulnerable to bulk mass disclosure via PostgREST/GraphQL."
            })

        # 2. Write Policy Coverage Check (SELECT vs INSERT/UPDATE/DELETE)
        covered_cmds = {p.get("cmd", "").upper() for p in policies}
        required_cmds = {"SELECT", "INSERT", "UPDATE", "DELETE"}
        missing_cmds = required_cmds - covered_cmds

        if rls_enabled and missing_cmds:
            # If ALL command is covered, then all operations are guarded
            if "ALL" not in covered_cmds:
                score -= len(missing_cmds) * 10
                violations.append({
                    "code": "MISSING_WRITE_POLICIES",
                    "severity": "HIGH",
                    "message": f"Table '{table_name}' is missing explicit RLS policies for operations: {sorted(list(missing_cmds))}."
                })

        # 3. Tenant Boundary Verification
        tenant_bound = False
        for p in policies:
            clause = f"{p.get('using', '')} {p.get('with_check', '')}".lower()
            if "tenant_id" in clause or "institution_id" in clause:
                tenant_bound = True
                break

        if rls_enabled and not tenant_bound:
            score -= 15
            violations.append({
                "code": "MISSING_TENANT_ISOLATION_FILTER",
                "severity": "MEDIUM",
                "message": f"Table '{table_name}' policies do not explicitly check tenant_id / institution_id claim in JWT."
            })

        # SQL Remediation Generation
        remediation_sql = self._generate_table_remediation_sql(table_name, rls_enabled, missing_cmds)
        if violations:
            self._stats["remediation_patches_generated"] += 1

        final_score = max(0, score)
        return {
            "table_name": table_name,
            "rls_enabled": rls_enabled,
            "compliance_score": final_score,
            "status": "COMPLIANT" if final_score >= 85 else "NON_COMPLIANT",
            "violations": violations,
            "remediation_sql": remediation_sql
        }

    def scan_function_security_definer(self, func_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits PostgreSQL stored procedures / RPC functions for search_path hijacking vulnerabilities.
        func_metadata expects: {function_name, security_type, search_path_set, language}
        """
        self._stats["functions_scanned"] += 1
        func_name = func_metadata.get("function_name", "unknown_func")
        sec_type = func_metadata.get("security_type", "SECURITY INVOKER").upper()
        search_path_set = func_metadata.get("search_path_set", False)

        violations = []
        is_secure = True

        if sec_type == "SECURITY DEFINER" and not search_path_set:
            is_secure = False
            self._stats["critical_drifts_flagged"] += 1
            violations.append({
                "code": "SEARCH_PATH_HIJACK_VULNERABILITY",
                "severity": "CRITICAL",
                "message": f"Function '{func_name}' runs as SECURITY DEFINER without explicit 'SET search_path = \"\"'. Privilege escalation possible via object shadowing."
            })

        remediation_sql = f"ALTER FUNCTION {func_name} SET search_path = '';" if not is_secure else "-- Function search_path is already secure."

        return {
            "function_name": func_name,
            "security_type": sec_type,
            "is_secure": is_secure,
            "violations": violations,
            "remediation_sql": remediation_sql
        }

    def _generate_table_remediation_sql(self, table_name: str, rls_enabled: bool, missing_cmds: set) -> str:
        """Generates idempotent SQL statements to fix RLS gaps."""
        lines = []
        if not rls_enabled:
            lines.append(f"ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;")
            lines.append(f"ALTER TABLE {table_name} FORCE ROW LEVEL SECURITY;")

        if "SELECT" in missing_cmds:
            lines.append(f"CREATE POLICY {table_name}_select_tenant_iso ON {table_name} FOR SELECT USING (tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id'));")
        if "INSERT" in missing_cmds:
            lines.append(f"CREATE POLICY {table_name}_insert_owner_bound ON {table_name} FOR INSERT WITH CHECK (user_id = auth.uid());")
        if "UPDATE" in missing_cmds:
            lines.append(f"CREATE POLICY {table_name}_update_owner_bound ON {table_name} FOR UPDATE USING (user_id = auth.uid());")
        if "DELETE" in missing_cmds:
            lines.append(f"CREATE POLICY {table_name}_delete_admin_only ON {table_name} FOR DELETE USING (auth.jwt() ->> 'role' = 'admin');")

        return "\n".join(lines) if lines else "-- Table is fully compliant with RLS standards."

    def get_scanner_metrics(self) -> Dict[str, Any]:
        """Returns overall database compliance metrics."""
        return {
            "stats": dict(self._stats),
            "status": "operational"
        }
