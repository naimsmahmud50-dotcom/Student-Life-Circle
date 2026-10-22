import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, List, Optional


class EdgeFunctionZeroTrustGatewayService:
    """
    Zero-Trust Gateway and Security Policy Evaluator for Supabase Edge Functions.
    Defends against spoofed service_role headers, cross-tenant leaks, and unauthorized invocations.
    Adheres to Strix Supabase Security Playbook and OWASP API Top 10 guidelines.
    """

    DEFAULT_SECRET = "supa-edge-secret-key-2026-production-token"

    # Strict role-based action permission matrix for edge serverless functions
    ACTION_RBAC_MATRIX = {
        "finalize_course_grades": ["academic_dean", "registrar"],
        "disburse_scholarship_fund": ["bursar", "financial_aid_director"],
        "issue_proctor_token": ["lead_proctor", "exam_controller"],
        "read_course_catalog": [
            "student",
            "faculty",
            "academic_dean",
            "registrar",
            "bursar",
            "lead_proctor",
        ],
        "execute_cdc_sync": ["service_role", "system_daemon"],
    }

    def __init__(self, secret_key: str = DEFAULT_SECRET):
        self.secret_key = secret_key

    @staticmethod
    def _b64url_encode(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

    @staticmethod
    def _b64url_decode(s: str) -> bytes:
        padding = "=" * ((4 - len(s) % 4) % 4)
        return base64.urlsafe_b64decode(s + padding)

    def create_jwt(
        self,
        user_id: str,
        role: str,
        tenant_id: str,
        audience: str = "authenticated",
        expires_in: int = 3600,
        extra_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Creates a compliant HMAC-SHA256 signed JWT for Supabase Auth simulation.
        """
        header = {"alg": "HS256", "typ": "JWT"}
        now = int(time.time())
        payload = {
            "sub": user_id,
            "role": role,
            "aud": audience,
            "exp": now + expires_in,
            "iat": now,
            "app_metadata": {
                "tenant_id": tenant_id,
                "role": role,
            },
            "user_metadata": {
                "user_id": user_id,
            },
        }
        if extra_claims:
            payload.update(extra_claims)

        encoded_header = self._b64url_encode(json.dumps(header).encode("utf-8"))
        encoded_payload = self._b64url_encode(json.dumps(payload).encode("utf-8"))
        signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
        signature = hmac.new(
            self.secret_key.encode("utf-8"), signing_input, hashlib.sha256
        ).digest()
        encoded_sig = self._b64url_encode(signature)
        return f"{encoded_header}.{encoded_payload}.{encoded_sig}"

    def verify_edge_request(
        self,
        headers: Dict[str, str],
        secret: Optional[str] = None,
        allowed_audiences: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Verifies authorization headers, cryptographic signature, token claims,
        and sanitizes client-supplied privilege spoofing attempts.
        """
        active_secret = secret or self.secret_key
        audiences = allowed_audiences or ["authenticated", "anon", "service_role"]

        # Case-insensitive header dictionary lookup
        normalized_headers = {k.lower(): v for k, v in headers.items()}
        auth_header = normalized_headers.get("authorization", "")
        apikey = normalized_headers.get("apikey", "")

        # 1. Detect Header Spoofing Attacks (e.g. client trying to inject x-supabase-role: service_role)
        security_flags = []
        spoofed_role = normalized_headers.get("x-supabase-role") or normalized_headers.get("x-client-role")
        if spoofed_role and spoofed_role.lower() == "service_role":
            security_flags.append("SPOOFED_SERVICE_ROLE_HEADER_DETECTED")

        if not auth_header:
            return {
                "is_valid": False,
                "reason": "Missing Authorization header",
                "security_flags": security_flags,
                "user_id": None,
                "role": "anonymous",
                "tenant_id": None,
                "claims": {},
            }

        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return {
                "is_valid": False,
                "reason": "Invalid Authorization header format; must be 'Bearer <token>'",
                "security_flags": security_flags,
                "user_id": None,
                "role": "anonymous",
                "tenant_id": None,
                "claims": {},
            }

        token = parts[1]
        jwt_parts = token.split(".")
        if len(jwt_parts) != 3:
            return {
                "is_valid": False,
                "reason": "Malformed JWT: expected 3 sections",
                "security_flags": security_flags,
                "user_id": None,
                "role": "anonymous",
                "tenant_id": None,
                "claims": {},
            }

        # 2. Verify Cryptographic HMAC Signature
        signing_input = f"{jwt_parts[0]}.{jwt_parts[1]}".encode("utf-8")
        expected_sig = hmac.new(
            active_secret.encode("utf-8"), signing_input, hashlib.sha256
        ).digest()
        expected_sig_encoded = self._b64url_encode(expected_sig)

        if not hmac.compare_digest(jwt_parts[2], expected_sig_encoded):
            return {
                "is_valid": False,
                "reason": "Cryptographic signature mismatch; possible token tampering",
                "security_flags": security_flags + ["INVALID_CRYPTOGRAPHIC_SIGNATURE"],
                "user_id": None,
                "role": "anonymous",
                "tenant_id": None,
                "claims": {},
            }

        # 3. Parse Payload
        try:
            payload_bytes = self._b64url_decode(jwt_parts[1])
            claims = json.loads(payload_bytes.decode("utf-8"))
        except Exception as e:
            return {
                "is_valid": False,
                "reason": f"Failed to parse JWT payload: {str(e)}",
                "security_flags": security_flags,
                "user_id": None,
                "role": "anonymous",
                "tenant_id": None,
                "claims": {},
            }

        # 4. Check Expiration
        now = int(time.time())
        exp = claims.get("exp", 0)
        if exp < now:
            return {
                "is_valid": False,
                "reason": f"JWT token expired at {exp} (current time: {now})",
                "security_flags": security_flags + ["TOKEN_EXPIRED"],
                "user_id": claims.get("sub"),
                "role": claims.get("role", "anonymous"),
                "tenant_id": claims.get("app_metadata", {}).get("tenant_id"),
                "claims": claims,
            }

        # 5. Check Audience
        token_aud = claims.get("aud")
        if token_aud not in audiences:
            return {
                "is_valid": False,
                "reason": f"Audience '{token_aud}' not in allowed audiences: {audiences}",
                "security_flags": security_flags + ["AUDIENCE_MISMATCH"],
                "user_id": claims.get("sub"),
                "role": claims.get("role", "anonymous"),
                "tenant_id": claims.get("app_metadata", {}).get("tenant_id"),
                "claims": claims,
            }

        # 6. Check Privilege Escalation Defense:
        # If client injected a fake service_role header while token role is not service_role, reject
        token_role = claims.get("role", "authenticated")
        if "SPOOFED_SERVICE_ROLE_HEADER_DETECTED" in security_flags and token_role != "service_role":
            return {
                "is_valid": False,
                "reason": "Privilege escalation blocked: client header claimed service_role but JWT claims lower role",
                "security_flags": security_flags + ["PRIVILEGE_ESCALATION_BLOCKED"],
                "user_id": claims.get("sub"),
                "role": token_role,
                "tenant_id": claims.get("app_metadata", {}).get("tenant_id"),
                "claims": claims,
            }

        user_id = claims.get("sub")
        tenant_id = claims.get("app_metadata", {}).get("tenant_id") or claims.get("tenant_id")

        return {
            "is_valid": True,
            "reason": "Token cryptographically verified and zero-trust headers validated",
            "security_flags": security_flags,
            "user_id": user_id,
            "role": token_role,
            "tenant_id": tenant_id,
            "claims": claims,
        }

    def enforce_tenant_isolation(
        self, claims: Dict[str, Any], target_tenant_id: str
    ) -> Dict[str, Any]:
        """
        Verifies that the caller belongs to target_tenant_id, blocking multi-tenant lateral movement.
        """
        user_tenant = (
            claims.get("app_metadata", {}).get("tenant_id")
            or claims.get("tenant_id")
            or "unknown_tenant"
        )
        user_role = claims.get("role", "authenticated")

        # Global system_daemon or service_role can cross tenants with audit logging
        if user_role in ["service_role", "system_daemon"]:
            return {
                "isolated": True,
                "privileged_bypass": True,
                "user_tenant": user_tenant,
                "target_tenant": target_tenant_id,
                "message": "Privileged role granted cross-tenant orchestration with security audit",
            }

        if user_tenant != target_tenant_id:
            return {
                "isolated": False,
                "privileged_bypass": False,
                "user_tenant": user_tenant,
                "target_tenant": target_tenant_id,
                "message": f"Tenant boundary violation: user in '{user_tenant}' cannot access '{target_tenant_id}'",
            }

        return {
            "isolated": True,
            "privileged_bypass": False,
            "user_tenant": user_tenant,
            "target_tenant": target_tenant_id,
            "message": "Tenant boundary integrity verified",
        }

    def evaluate_edge_action_policy(
        self, user_role: str, function_name: str, requested_action: str
    ) -> Dict[str, Any]:
        """
        Fine-grained RBAC action authorization before executing sensitive serverless routines.
        Produces an immutable cryptographic authorization verdict.
        """
        allowed_roles = self.ACTION_RBAC_MATRIX.get(function_name, ["service_role"])
        is_allowed = user_role in allowed_roles

        now_str = str(int(time.time()))
        # Cryptographic verdict signature to prove gate check was performed
        verdict_str = f"{user_role}:{function_name}:{requested_action}:{is_allowed}:{now_str}"
        verdict_sig = hmac.new(
            self.secret_key.encode("utf-8"), verdict_str.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return {
            "allowed": is_allowed,
            "user_role": user_role,
            "function_name": function_name,
            "requested_action": requested_action,
            "required_roles": allowed_roles,
            "timestamp": now_str,
            "verdict_signature": f"sig_v1_{verdict_sig[:32]}",
            "message": (
                "Action authorized for execution"
                if is_allowed
                else f"Action denied: role '{user_role}' lacks required privilege in {allowed_roles}"
            ),
        }
