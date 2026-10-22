# ==============================================================================
# File: backend/app/services/pg_graphql_shield_service.py
# Phase: 50 - Supabase GraphQL (pg_graphql) Schema Shield & Complexity Limiter
# Topic: Schema Introspection Guard, AST Query Complexity, & RLS Parity Auditor
# Description: Evaluates incoming GraphQL queries against denial-of-service recursion,
#              calculates AST complexity, enforces schema introspection access controls,
#              and audits parity between PostgREST and pg_graphql resolver fields.
# ==============================================================================

import re
from typing import Dict, Any, List, Optional, Tuple, Set

class PgGraphqlShieldService:
    """
    pg_graphql Schema Shield & Complexity Defense Engine.
    Guards Supabase GraphQL endpoints against resource exhaustion, unauthorized
    schema harvesting via introspection, and field-level RLS parity drift.
    """

    MAX_QUERY_DEPTH = 4
    MAX_COMPLEXITY_SCORE = 50

    # Restricted columns that must never be exposed via GraphQL resolvers
    RESTRICTED_COLUMNS: Set[str] = {
        "password_hash", "two_factor_secret", "internal_risk_score",
        "api_secret_key", "recovery_seeds", "encryption_dek"
    }

    def __init__(self):
        self._stats = {
            "queries_inspected": 0,
            "introspections_blocked": 0,
            "excessive_depth_blocked": 0,
            "high_complexity_blocked": 0,
            "cyclic_recursions_blocked": 0,
            "restricted_fields_blocked": 0,
            "safe_queries_authorized": 0
        }

    def inspect_and_authorize_query(
        self,
        query: str,
        caller_role: str = "anon",
        caller_user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Inspects GraphQL query for security violations, introspection abuse,
        depth limits, computational complexity, and cyclic recursion.
        """
        self._stats["queries_inspected"] += 1
        violations = []

        # 1. Introspection Authorization Check
        if "__schema" in query or "__type" in query:
            if caller_role not in ("admin", "developer"):
                self._stats["introspections_blocked"] += 1
                violations.append({
                    "code": "INTROSPECTION_UNAUTHORIZED",
                    "severity": "HIGH",
                    "message": "Full schema introspection is restricted to administrative and developer roles."
                })

        # 2. Query Depth Calculation
        depth = self._calculate_query_depth(query)
        if depth > self.MAX_QUERY_DEPTH:
            self._stats["excessive_depth_blocked"] += 1
            violations.append({
                "code": "EXCESSIVE_QUERY_DEPTH",
                "severity": "HIGH",
                "message": f"Query depth of {depth} exceeds allowable threshold ({self.MAX_QUERY_DEPTH}). Potential nested DoS."
            })

        # 3. Query Complexity Calculation
        complexity = self._calculate_complexity_score(query)
        if complexity > self.MAX_COMPLEXITY_SCORE:
            self._stats["high_complexity_blocked"] += 1
            violations.append({
                "code": "COMPLEXITY_LIMIT_EXCEEDED",
                "severity": "HIGH",
                "message": f"Query complexity score of {complexity} exceeds maximum allowable budget ({self.MAX_COMPLEXITY_SCORE})."
            })

        # 4. Cyclic Recursion Detection
        cyclic_pattern = self._detect_cyclic_recursion(query)
        if cyclic_pattern:
            self._stats["cyclic_recursions_blocked"] += 1
            violations.append({
                "code": "CYCLIC_RECURSION_DETECTED",
                "severity": "CRITICAL",
                "message": f"Cyclic recursive resolver chain detected: '{cyclic_pattern}'. Attack mitigation applied."
            })

        # 5. Restricted Field Access Check
        found_restricted = self._check_restricted_fields(query)
        if found_restricted:
            self._stats["restricted_fields_blocked"] += 1
            violations.append({
                "code": "RESTRICTED_FIELD_ACCESS",
                "severity": "CRITICAL",
                "message": f"Query attempts to fetch restricted sensitive fields: {', '.join(found_restricted)}. RLS parity protection enforced."
            })

        is_authorized = len(violations) == 0
        if is_authorized:
            self._stats["safe_queries_authorized"] += 1

        return {
            "authorized": is_authorized,
            "caller_role": caller_role,
            "calculated_depth": depth,
            "max_allowable_depth": self.MAX_QUERY_DEPTH,
            "complexity_score": complexity,
            "max_complexity_budget": self.MAX_COMPLEXITY_SCORE,
            "violations": violations,
            "status": "APPROVED" if is_authorized else "REJECTED"
        }

    def _calculate_query_depth(self, query: str) -> int:
        """Calculates nesting depth based on balanced curly braces."""
        max_depth = 0
        current_depth = 0
        for char in query:
            if char == "{":
                current_depth += 1
                if current_depth > max_depth:
                    max_depth = current_depth
            elif char == "}":
                if current_depth > 0:
                    current_depth -= 1
        return max_depth

    def _calculate_complexity_score(self, query: str) -> int:
        """
        Estimates AST node complexity score.
        Each field adds 1 point; list arguments (first, last, limit) multiply complexity.
        """
        score = 0
        clean_query = re.sub(r'#.*', '', query)
        # Count words that resemble field names
        tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', clean_query)
        ignored = {"query", "mutation", "subscription", "fragment", "on", "first", "last", "limit", "offset"}
        fields = [t for t in tokens if t not in ignored]
        score += len(fields)

        # Multipliers for pagination/list queries
        multipliers = re.findall(r'(?:first|last|limit):\s*(\d+)', clean_query)
        for m in multipliers:
            val = int(m)
            score += min(val, 25)

        return score

    def _detect_cyclic_recursion(self, query: str) -> Optional[str]:
        """Detects repeated entity relationship sequences indicating circular queries."""
        tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', query)
        for i in range(len(tokens) - 3):
            sub = tokens[i:i+2]
            rest = tokens[i+2:]
            if len(rest) >= 2 and rest[0] == sub[0] and rest[1] == sub[1]:
                return f"{sub[0]} -> {sub[1]} -> {sub[0]} -> {sub[1]}"
        return None

    def _check_restricted_fields(self, query: str) -> List[str]:
        """Identifies any forbidden or secret columns inside query."""
        found = []
        tokens = set(re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', query.lower()))
        for restricted in self.RESTRICTED_COLUMNS:
            if restricted in tokens:
                found.append(restricted)
        return found

    def audit_postgrest_graphql_parity(
        self,
        table_name: str,
        postgrest_allowed_columns: List[str],
        graphql_type_fields: List[str]
    ) -> Dict[str, Any]:
        """
        Audits field-level parity between PostgREST RLS exposed columns
        and pg_graphql schema types to identify potential data leak differentials.
        """
        pg_set = set(postgrest_allowed_columns)
        gql_set = set(graphql_type_fields)

        # Fields in GraphQL but missing from PostgREST permitted set
        graphql_overexposure = list(gql_set - pg_set)
        # Fields in PostgREST but not modeled in GraphQL
        postgrest_only = list(pg_set - gql_set)

        has_parity_risk = len(graphql_overexposure) > 0

        return {
            "table_name": table_name,
            "has_parity_risk": has_parity_risk,
            "graphql_overexposed_fields": graphql_overexposure,
            "postgrest_only_fields": postgrest_only,
            "recommendation": "Synchronize pg_graphql view bindings to prevent resolver RLS bypass." if has_parity_risk else "Parity verified."
        }

    def get_security_metrics(self) -> Dict[str, Any]:
        """Returns GraphQL shield metrics and mitigation counts."""
        return {
            "stats": dict(self._stats),
            "max_depth_threshold": self.MAX_QUERY_DEPTH,
            "max_complexity_threshold": self.MAX_COMPLEXITY_SCORE,
            "restricted_field_count": len(self.RESTRICTED_COLUMNS)
        }
