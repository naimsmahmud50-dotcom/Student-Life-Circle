"""
================================================================================
MODULE: Supabase Security & Row-Level Security (RLS) Policy Engine
TOPIC: Strix-Supabase Security Architecture, PostgREST Filter Defense & Tenant Isolation
FILE: backend/app/services/supabase_security_service.py
PURPOSE: Comprehensive verification and policy compilation for Supabase databases,
         enforcing OWASP ASVS L2, zero-IDOR, tenant boundary integrity, and preventing
         PostgREST parameter pollution, wildcard search leaks, and leaked service_role keys.
AUDIENCE: Cloud Security Engineers, Database Administrators, Backend Architects.
================================================================================
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class SupabaseSecurityService:
    """
    Core security evaluation engine for Supabase Row-Level Security (RLS) policies,
    PostgREST query sanitization, and database tenant isolation.
    """

    PUBLIC_TABLES = {"public_curricula", "public_institutions", "public_exam_notices"}
    
    PROTECTED_TABLES = {
        "profiles",
        "applications",
        "scholarships",
        "escrow_vaults",
        "exam_submissions",
        "cv_snapshots",
        "guardian_consents",
        "study_circle_notes",
        "bounty_tribunal_claims"
    }

    def evaluate_rls_access(
        self,
        table_name: str,
        action: str,
        caller_role: str,
        caller_uid: Optional[str] = None,
        caller_tenant_id: Optional[str] = None,
        target_owner_id: Optional[str] = None,
        target_tenant_id: Optional[str] = None,
        client_payload_user_id: Optional[str] = None,
        is_browser_origin: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates whether a database request complies with strict Row-Level Security.
        Adheres to Strix-Supabase defense rules:
        - Never trust client-supplied user_id or tenant_id over server JWT.
        - Service role keys must never be accepted from browser origins.
        - Cross-tenant and cross-user data access is categorically denied.
        """
        action = action.upper().strip()
        table_name = table_name.lower().strip()
        
        # Rule 1: Leaked service_role check
        if caller_role == "service_role":
            if is_browser_origin:
                return {
                    "verdict": "DENIED",
                    "status_code": 403,
                    "reason": "CRITICAL_KEY_EXPOSURE: service_role key invocation detected from browser client. Immediate revocation recommended.",
                    "applied_policy": "NO_BROWSER_SERVICE_ROLE",
                    "threat_level": "CRITICAL"
                }
            return {
                "verdict": "ALLOWED",
                "status_code": 200,
                "reason": "Service role bypass granted for internal backend server process only.",
                "applied_policy": "BYPASS_RLS_INTERNAL",
                "threat_level": "NONE"
            }

        # Rule 2: Unauthenticated anon role
        if caller_role == "anon":
            if table_name in self.PUBLIC_TABLES and action == "SELECT":
                return {
                    "verdict": "ALLOWED",
                    "status_code": 200,
                    "reason": f"Public table '{table_name}' allows unauthenticated SELECT.",
                    "applied_policy": f"anon_read_{table_name}",
                    "threat_level": "LOW"
                }
            return {
                "verdict": "DENIED",
                "status_code": 401,
                "reason": f"Table '{table_name}' requires authenticated session with valid JWT.",
                "applied_policy": "DEFAULT_DENY_UNAUTHENTICATED",
                "threat_level": "MEDIUM"
            }

        # Rule 3: Authenticated user checks
        if caller_role == "authenticated":
            if not caller_uid:
                return {
                    "verdict": "DENIED",
                    "status_code": 401,
                    "reason": "JWT missing 'sub' (auth.uid()) claim.",
                    "applied_policy": "INVALID_JWT_CLAIMS",
                    "threat_level": "HIGH"
                }

            # Check client payload manipulation (Mass Assignment / Spoofing)
            if client_payload_user_id and client_payload_user_id != caller_uid:
                return {
                    "verdict": "DENIED",
                    "status_code": 403,
                    "reason": "POLICY_VIOLATION: Client payload user_id does not match server auth.uid(). Server context is authoritative.",
                    "applied_policy": "DENY_USER_ID_OVERRIDE",
                    "threat_level": "HIGH"
                }

            # Check tenant isolation
            if caller_tenant_id and target_tenant_id and caller_tenant_id != target_tenant_id:
                return {
                    "verdict": "DENIED",
                    "status_code": 403,
                    "reason": "TENANT_ISOLATION_VIOLATION: Cross-tenant data boundary breach prevented.",
                    "applied_policy": "TENANT_ISOLATION_GUARD",
                    "threat_level": "HIGH"
                }

            # Check record owner isolation (IDOR protection)
            if target_owner_id and target_owner_id != caller_uid:
                return {
                    "verdict": "DENIED",
                    "status_code": 403,
                    "reason": "IDOR_VIOLATION: auth.uid() does not match record owner id.",
                    "applied_policy": f"{table_name}_owner_only",
                    "threat_level": "HIGH"
                }

            return {
                "verdict": "ALLOWED",
                "status_code": 200,
                "reason": f"Access granted for user '{caller_uid}' on table '{table_name}' for action '{action}'.",
                "applied_policy": f"{table_name}_authenticated_{action.lower()}",
                "threat_level": "NONE"
            }

        return {
            "verdict": "DENIED",
            "status_code": 403,
            "reason": f"Unrecognized or unauthorized role: '{caller_role}'.",
            "applied_policy": "UNKNOWN_ROLE_DENIED",
            "threat_level": "MEDIUM"
        }

    def sanitize_postgrest_query(
        self,
        query_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Sanitizes PostgREST query parameters against injection patterns:
        - Detects 'or=' filter bypass attempting to match NULL or wildcard tenants.
        - Detects unanchored 'ilike' queries on sensitive fields.
        - Flags excessive relation embedding (GraphQL/PostgREST overfetch).
        """
        anomalies = []
        threat_score = 0
        sanitized_params = {}

        for key, val in query_params.items():
            str_val = str(val).strip()

            # Check 1: 'or=' injection pattern (e.g., or=(tenant_id.eq.org,tenant_id.is.null))
            if key == "or" or "or=" in str_val:
                if re.search(r"\.is\.null|\.neq\.|\.gt\.0", str_val, re.IGNORECASE):
                    anomalies.append(f"Suspicious OR-filter condition: '{str_val}' potential boundary bypass.")
                    threat_score += 45
                    continue  # Strip hazardous filter

            # Check 2: Unanchored wildcards on sensitive columns
            if "ilike" in str_val or "like" in str_val:
                if str_val.startswith("*") or str_val.startswith("%") or str_val == "*":
                    anomalies.append(f"Unanchored wildcard query on parameter '{key}': '{str_val}' may cause table scan disclosure.")
                    threat_score += 30
                    str_val = re.sub(r"^[%*]+", "", str_val)

            # Check 3: Deep nested resource embedding
            if key == "select":
                depth = str_val.count("(")
                if depth >= 3:
                    anomalies.append(f"High relation embedding depth ({depth} levels): potential PostgREST overfetch/DoS vector.")
                    threat_score += 25

            sanitized_params[key] = str_val

        is_safe = threat_score < 30
        return {
            "is_safe": is_safe,
            "threat_score": min(100, threat_score),
            "anomalies": anomalies,
            "sanitized_params": sanitized_params,
            "recommended_action": "PERMIT" if is_safe else "REJECT_OR_FILTER"
        }

    def generate_secure_rls_sql(
        self,
        table_name: str,
        owner_column: str = "user_id",
        tenant_column: Optional[str] = "tenant_id"
    ) -> str:
        """
        Generates robust, production-grade PostgreSQL SQL statements enabling RLS,
        FORCE RLS, and strict policies for SELECT, INSERT, UPDATE, and DELETE.
        """
        table_name = re.sub(r"[^a-zA-Z0-9_]", "", table_name.lower())
        owner_col = re.sub(r"[^a-zA-Z0-9_]", "", owner_column.lower())
        
        tenant_clause = ""
        if tenant_column:
            tenant_col = re.sub(r"[^a-zA-Z0-9_]", "", tenant_column.lower())
            tenant_clause = f" AND {tenant_col} = (auth.jwt() ->> 'tenant_id')::uuid"

        sql = f"""-- =============================================================================
-- AUTOMATED STRIX-SUPABASE RLS POLICY GENERATION
-- TABLE: {table_name}
-- GENERATED: {datetime.now(timezone.utc).isoformat()}
-- STANDARDS: OWASP ASVS L2, Zero-IDOR, Multi-Tenant Boundary Isolation
-- =============================================================================

-- 1. Enable Row Level Security and enforce for table owner as well
ALTER TABLE public.{table_name} ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.{table_name} FORCE ROW LEVEL SECURITY;

-- 2. Revoke default public grants
REVOKE ALL ON public.{table_name} FROM PUBLIC;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.{table_name} TO authenticated;

-- 3. Policy: SELECT (Owner & Tenant Bound)
CREATE POLICY {table_name}_select_policy ON public.{table_name}
    FOR SELECT
    TO authenticated
    USING (
        auth.uid() = {owner_col}{tenant_clause}
    );

-- 4. Policy: INSERT (Enforce Caller Ownership)
CREATE POLICY {table_name}_insert_policy ON public.{table_name}
    FOR INSERT
    TO authenticated
    WITH CHECK (
        auth.uid() = {owner_col}{tenant_clause}
    );

-- 5. Policy: UPDATE (Owner & Tenant Bound)
CREATE POLICY {table_name}_update_policy ON public.{table_name}
    FOR UPDATE
    TO authenticated
    USING (
        auth.uid() = {owner_col}{tenant_clause}
    )
    WITH CHECK (
        auth.uid() = {owner_col}{tenant_clause}
    );

-- 6. Policy: DELETE (Owner & Tenant Bound)
CREATE POLICY {table_name}_delete_policy ON public.{table_name}
    FOR DELETE
    TO authenticated
    USING (
        auth.uid() = {owner_col}{tenant_clause}
    );
"""
        return sql
