# ==============================================================================
# File: backend/app/services/postgrest_query_hardener_service.py
# Phase: 49 - PostgREST Query Hardener & Parameter Pollution Shield
# Topic: Parameter Pollution Defense, Wildcard Poisoning Prevention, & Tenant Boundary
# Description: Sanitizes and hardens PostgREST filter parameters, blocks parameter
#              pollution attacks, stops unindexed leading wildcard mass-disclosure,
#              enforces tenant boundaries from JWT claims, and limits relation embed depth.
# ==============================================================================

import re
from typing import Dict, Any, List, Optional, Tuple

class PostgrestQueryHardenerService:
    """
    PostgREST Query Hardening & Parameter Pollution Defense Service.
    Protects Supabase endpoints from malicious filter chaining, parameter pollution,
    unanchored wildcard disclosure, cross-tenant leaks, and deep relation overfetching.
    """

    # Columns where leading wildcard searches (%keyword) are strictly prohibited
    SENSITIVE_SEARCH_COLUMNS = {
        "email", "phone", "nid", "national_id", "password_hash",
        "api_key", "secret_token", "bank_account", "bursary_account"
    }

    MAX_RELATION_EMBED_DEPTH = 2

    def __init__(self):
        self._stats = {
            "queries_analyzed": 0,
            "parameter_pollutions_blocked": 0,
            "wildcard_poisonings_blocked": 0,
            "cross_tenant_tampering_blocked": 0,
            "excessive_embed_depth_blocked": 0,
            "safe_queries_passed": 0
        }

    def inspect_and_harden_query(
        self,
        raw_query_params: Dict[str, Any],
        verified_jwt_claims: Dict[str, Any],
        table_name: str
    ) -> Dict[str, Any]:
        """
        Inspects incoming PostgREST query parameters against OWASP/Strix attack patterns.
        Returns a hardened parameter set or raises validation rejections.
        """
        self._stats["queries_analyzed"] += 1
        violations = []
        hardened_params = {}

        # 1. Parameter Pollution Check (duplicate parameter names passed as lists)
        for key, value in raw_query_params.items():
            if isinstance(value, list) and len(value) > 1:
                self._stats["parameter_pollutions_blocked"] += 1
                violations.append({
                    "code": "HTTP_PARAMETER_POLLUTION",
                    "severity": "HIGH",
                    "parameter": key,
                    "detail": f"Duplicate parameter '{key}' detected with {len(value)} conflicting values. Parameter pollution rejected."
                })
                # Harden by taking the first strict value or rejecting
                continue

            hardened_params[key] = value

        # 2. Inspect Filter Operators (Wildcard poisoning & illegal OR null combinations)
        for key, val in list(hardened_params.items()):
            str_val = str(val)

            # Check for unanchored wildcard on sensitive columns
            if key in self.SENSITIVE_SEARCH_COLUMNS or any(col in key for col in self.SENSITIVE_SEARCH_COLUMNS):
                if "%" in str_val or "*" in str_val:
                    # Check if wildcard is leading (%abc) or broad (%%)
                    if str_val.startswith("ilike.%") or str_val.startswith("like.%") or "%" in str_val[:8]:
                        self._stats["wildcard_poisonings_blocked"] += 1
                        violations.append({
                            "code": "UNANCHORED_WILDCARD_POISONING",
                            "severity": "MEDIUM",
                            "parameter": key,
                            "detail": f"Leading wildcard on sensitive column '{key}' prohibited. May cause full-table scan or mass data disclosure."
                        })

            # Check for RLS bypass via OR is.null chaining
            if key == "or" or "or=" in str_val:
                if "is.null" in str_val or "tenant_id.is.null" in str_val:
                    self._stats["parameter_pollutions_blocked"] += 1
                    violations.append({
                        "code": "SUSPICIOUS_OR_NULL_BYPASS",
                        "severity": "CRITICAL",
                        "parameter": key,
                        "detail": "Illegal 'or=(...is.null)' pattern detected. Known technique to bypass RLS tenant boundary."
                    })

        # 3. Tenant Boundary Enforcement
        verified_tenant = verified_jwt_claims.get("tenant_id") or verified_jwt_claims.get("app_metadata", {}).get("tenant_id")
        if not verified_tenant:
            verified_tenant = "inst_default"

        client_requested_tenant = hardened_params.get("institution_id") or hardened_params.get("tenant_id")
        if client_requested_tenant:
            # Strip operator like 'eq.inst_xyz'
            clean_client_tenant = str(client_requested_tenant).replace("eq.", "").strip()
            if clean_client_tenant != verified_tenant:
                self._stats["cross_tenant_tampering_blocked"] += 1
                violations.append({
                    "code": "CROSS_TENANT_TAMPERING",
                    "severity": "CRITICAL",
                    "parameter": "tenant_id",
                    "detail": f"Client attempted to query tenant '{clean_client_tenant}' while authenticated under tenant '{verified_tenant}'."
                })

        # Force enforce verified tenant in hardened params
        hardened_params["tenant_id"] = f"eq.{verified_tenant}"

        # 4. Relation Overfetch / Embed Depth Check
        select_clause = hardened_params.get("select", "*")
        embed_depth = self._calculate_embed_depth(str(select_clause))
        if embed_depth > self.MAX_RELATION_EMBED_DEPTH:
            self._stats["excessive_embed_depth_blocked"] += 1
            violations.append({
                "code": "EXCESSIVE_EMBED_DEPTH",
                "severity": "MEDIUM",
                "parameter": "select",
                "detail": f"Relation embed depth of {embed_depth} exceeds maximum allowable threshold ({self.MAX_RELATION_EMBED_DEPTH}). Potential resource exhaustion or RLS leak."
            })

        is_safe = len(violations) == 0
        if is_safe:
            self._stats["safe_queries_passed"] += 1

        return {
            "is_safe": is_safe,
            "table_name": table_name,
            "violations": violations,
            "hardened_params": hardened_params if is_safe else {},
            "embed_depth": embed_depth,
            "enforced_tenant_id": verified_tenant
        }

    def _calculate_embed_depth(self, select_clause: str) -> int:
        """Calculates nesting depth of parenthesis in PostgREST select embeds."""
        max_depth = 0
        current_depth = 0
        for char in select_clause:
            if char == "(":
                current_depth += 1
                if current_depth > max_depth:
                    max_depth = current_depth
            elif char == ")":
                if current_depth > 0:
                    current_depth -= 1
        return max_depth

    def get_security_metrics(self) -> Dict[str, Any]:
        """Returns statistics on queries analyzed and threats mitigated."""
        return {
            "stats": dict(self._stats),
            "max_embed_depth_allowed": self.MAX_RELATION_EMBED_DEPTH,
            "sensitive_search_columns_protected": sorted(list(self.SENSITIVE_SEARCH_COLUMNS))
        }
