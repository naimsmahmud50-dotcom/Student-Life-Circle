import re
from typing import Any, Dict, List, Optional


class FederatedFdwSecurityService:
    """
    Security Validator and Query Sanitizer for PostgreSQL Foreign Data Wrappers (postgres_fdw).
    Protects inter-university credit transfer federations, education board linkages,
    and remote database user mappings from credential exposure and schema traversal attacks.
    """

    ALLOWED_SSL_MODES = ["require", "verify-ca", "verify-full"]
    DISALLOWED_REMOTE_USERS = ["postgres", "root", "superuser", "admin", "rds_superuser"]
    RESTRICTED_SCHEMAS = ["pg_catalog", "information_schema", "pg_toast", "vault", "auth"]

    def __init__(self):
        pass

    def audit_fdw_server_definition(self, server_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Audits a postgres_fdw FOREIGN SERVER configuration for transport encryption and timeouts.
        """
        server_name = server_config.get("server_name", "foreign_server")
        options = server_config.get("options", {})
        findings: List[Dict[str, str]] = []

        # 1. SSL Mode Check
        sslmode = options.get("sslmode", "").lower()
        if not sslmode or sslmode not in self.ALLOWED_SSL_MODES:
            findings.append({
                "issue": "INSECURE_OR_MISSING_SSL_MODE",
                "severity": "CRITICAL",
                "detail": f"Server '{server_name}' uses sslmode='{sslmode or 'none'}'. Must enforce 'require', 'verify-ca', or 'verify-full'.",
            })

        # 2. Connection Timeout Check
        try:
            timeout = int(options.get("connect_timeout", 0))
            if timeout <= 0 or timeout > 10:
                findings.append({
                    "issue": "MISSING_OR_EXCESSIVE_CONNECT_TIMEOUT",
                    "severity": "MEDIUM",
                    "detail": f"Connect timeout is {timeout}s. Recommended bounded range: 3s - 10s to prevent connection pool exhaustion.",
                })
        except ValueError:
            findings.append({
                "issue": "INVALID_CONNECT_TIMEOUT",
                "severity": "MEDIUM",
                "detail": "Connect timeout must be an integer number of seconds.",
            })

        # 3. Updatable Remote Data Check
        updatable = str(options.get("updatable", "false")).lower()
        if updatable == "true":
            findings.append({
                "issue": "REMOTE_MUTATION_PERMITTED",
                "severity": "HIGH",
                "detail": "Foreign server allows remote writes. Ensure strict transactional audit logging is enforced.",
            })

        compliant = len([f for f in findings if f["severity"] == "CRITICAL"]) == 0
        risk_score = 0.0
        for f in findings:
            if f["severity"] == "CRITICAL":
                risk_score += 50.0
            elif f["severity"] == "HIGH":
                risk_score += 25.0
            else:
                risk_score += 10.0
        risk_score = min(risk_score, 100.0)

        hardened_options = dict(options)
        hardened_options["sslmode"] = "verify-full" if "verify-full" in sslmode else "require"
        hardened_options["connect_timeout"] = "5"

        return {
            "server_name": server_name,
            "compliant": compliant,
            "risk_score": risk_score,
            "findings_count": len(findings),
            "findings": findings,
            "hardened_options": hardened_options,
        }

    def validate_user_mapping_permissions(
        self, user_mappings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Scans FDW user mappings for privilege escalation hazards (e.g., mapping public/students to remote superusers).
        """
        violations: List[Dict[str, Any]] = []

        for m in user_mappings:
            local_user = m.get("local_user", "").lower()
            remote_user = m.get("remote_user", "").lower()
            server_name = m.get("server_name", "remote_cluster")
            has_plaintext_password = "password" in m.get("options", {})

            # Hazard 1: Anonymous or Public role mapped to remote server
            if local_user in ["public", "anon", "unauthenticated"]:
                violations.append({
                    "hazard": "ANONYMOUS_ROLE_REMOTE_MAPPING",
                    "severity": "CRITICAL",
                    "local_user": local_user,
                    "remote_user": remote_user,
                    "detail": f"Role '{local_user}' has a foreign data wrapper mapping to '{server_name}'. Public clients can trigger remote network requests.",
                })

            # Hazard 2: Local student/unprivileged mapped to remote superuser
            if remote_user in self.DISALLOWED_REMOTE_USERS and local_user not in ["service_role", "dba_admin"]:
                violations.append({
                    "hazard": "REMOTE_SUPERUSER_OVERPRIVILEGE",
                    "severity": "CRITICAL",
                    "local_user": local_user,
                    "remote_user": remote_user,
                    "detail": f"Local role '{local_user}' is mapped to high-privileged remote user '{remote_user}' on '{server_name}'.",
                })

            # Hazard 3: Plaintext password in options dictionary
            if has_plaintext_password:
                violations.append({
                    "hazard": "PLAINTEXT_PASSWORD_IN_MAPPING",
                    "severity": "HIGH",
                    "local_user": local_user,
                    "remote_user": remote_user,
                    "detail": "Plaintext password embedded in USER MAPPING options. Use external token or secret vault.",
                })

        is_secure = len(violations) == 0

        return {
            "is_secure": is_secure,
            "total_mappings_analyzed": len(user_mappings),
            "violations_detected": len(violations),
            "violations": violations,
            "status": "APPROVED" if is_secure else "PRIVILEGE_VIOLATIONS_FOUND",
        }

    def sanitize_federated_query(
        self, remote_sql: str, allowed_schemas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Sanitizes cross-campus federated queries to prevent remote schema hopping and stacked query injection.
        """
        schemas = allowed_schemas or ["academics", "credit_transfer", "public"]
        cleaned = remote_sql.strip()

        # Check for stacked SQL injection (; followed by mutation)
        if re.search(r";\s*(DROP|ALTER|TRUNCATE|DELETE|INSERT|UPDATE|GRANT)\b", cleaned, re.IGNORECASE):
            return {
                "allowed": False,
                "sanitized_sql": "",
                "rejection_reason": "Stacked SQL query injection attempt detected",
                "security_flag": "STACKED_SQL_INJECTION_BLOCKED",
            }

        # Check for restricted schema access
        for restricted in self.RESTRICTED_SCHEMAS:
            if re.search(rf"\b{restricted}\.", cleaned, re.IGNORECASE):
                return {
                    "allowed": False,
                    "sanitized_sql": "",
                    "rejection_reason": f"Access to restricted internal schema '{restricted}' forbidden in federated context",
                    "security_flag": "RESTRICTED_SCHEMA_TRAVERSAL_BLOCKED",
                }

        # Verify query targets permitted schemas
        schema_matched = False
        target_schema = "unknown"
        for s in schemas:
            if re.search(rf"\b{s}\.", cleaned, re.IGNORECASE):
                schema_matched = True
                target_schema = s
                break

        if not schema_matched:
            return {
                "allowed": False,
                "sanitized_sql": "",
                "rejection_reason": f"Target table does not belong to allowed federated schemas: {schemas}",
                "security_flag": "UNAUTHORIZED_SCHEMA_ACCESS",
            }

        return {
            "allowed": True,
            "sanitized_sql": cleaned,
            "target_schema": target_schema,
            "rejection_reason": None,
            "security_flag": "FEDERATED_QUERY_VERIFIED",
        }
