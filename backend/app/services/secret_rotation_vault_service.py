import hashlib
import math
import re
import secrets
import time
from typing import Any, Dict, List, Optional, Set


class SecretRotationVaultService:
    """
    Dynamic Secret Rotation Vault & Client Bundle Entropy Leak Scanner.
    Enforces Strix Supabase Security Playbook zero-leak standards:
    - Scans client-side bundles and API payloads for exposed service_role keys.
    - Orchestrates zero-downtime dual-key rotation with overlapping grace windows.
    - Maintains cryptographic revocation blacklists.
    """

    # Signatures for high-risk exposed secrets in bundles or HTTP responses
    SECRET_REGEX_PATTERNS = [
        (
            r"sb_secret_[a-zA-Z0-9_\-]{24,}",
            "SUPABASE_SECRET_SERVICE_ROLE_KEY",
            "CRITICAL",
            "Exposed opaque Supabase secret key (sb_secret_...). Bypasses all Row Level Security policies.",
        ),
        (
            r"postgres(?:ql)?:\/\/[a-zA-Z0-9_\-\.]+:(?!\[)[^\s@:]+@[a-zA-Z0-9_\-\.]+",
            "DATABASE_CONNECTION_URI_WITH_PLAINTEXT_PASSWORD",
            "CRITICAL",
            "PostgreSQL direct connection string with plaintext password exposed in bundle.",
        ),
        (
            r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----",
            "ASYMMETRIC_PRIVATE_KEY_EXPOSURE",
            "CRITICAL",
            "Cryptographic private key PEM block detected in source code or response payload.",
        ),
        (
            r"whsec_[a-zA-Z0-9_\-]{24,}",
            "SVIX_WEBHOOK_SIGNING_SECRET",
            "HIGH",
            "Svix webhook signing secret exposed in client code.",
        ),
    ]

    def __init__(self):
        self._key_registry: Dict[str, Dict[str, Any]] = {}
        self._revocation_blacklist: Set[str] = set()
        self._seed_default_keys()

    def _seed_default_keys(self):
        """Initializes default master credentials."""
        now = int(time.time())
        self._key_registry["key_srv_active_01"] = {
            "key_id": "key_srv_active_01",
            "key_type": "service_role",
            "secret": f"sb_secret_prod_{secrets.token_hex(16)}",
            "status": "ACTIVE",
            "created_at": now - 86400,
            "grace_expires_at": None,
        }

    @staticmethod
    def _calculate_shannon_entropy(data: str) -> float:
        """Calculates Shannon entropy to detect high-randomness secret tokens."""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        freq = {c: data.count(c) for c in set(data)}
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy

    def scan_client_bundle_for_secrets(self, content_or_bundle: str) -> Dict[str, Any]:
        """
        Scans bundle scripts, HTML responses, or API payloads for exposed database keys and high-entropy secrets.
        """
        findings: List[Dict[str, Any]] = []

        # 1. Regex pattern matching
        for pattern, leak_type, severity, msg in self.SECRET_REGEX_PATTERNS:
            matches = re.findall(pattern, content_or_bundle)
            if matches:
                findings.append({
                    "leak_type": leak_type,
                    "severity": severity,
                    "occurrences": len(matches),
                    "sample": matches[0][:14] + "...",
                    "detail": msg,
                })

        # 2. Heuristic check: JWT token claiming service_role in public code
        jwt_matches = re.findall(r"eyJ[a-zA-Z0-9_\-]+\.eyJ[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-]+", content_or_bundle)
        for jwt_str in jwt_matches:
            if "service_role" in content_or_bundle and jwt_str in content_or_bundle:
                findings.append({
                    "leak_type": "EMBEDDED_SERVICE_ROLE_JWT",
                    "severity": "CRITICAL",
                    "occurrences": 1,
                    "sample": jwt_str[:20] + "...",
                    "detail": "Client script contains hardcoded JWT associated with service_role privilege.",
                })
                break

        # 3. High-entropy token detection (alphanumeric sequences > 36 chars with entropy > 4.5)
        tokens = re.findall(r"\b[A-Za-z0-9_\-]{36,64}\b", content_or_bundle)
        high_entropy_tokens = [t for t in tokens if self._calculate_shannon_entropy(t) > 4.5]
        if high_entropy_tokens and not findings:
            findings.append({
                "leak_type": "HIGH_ENTROPY_SUSPICIOUS_TOKEN",
                "severity": "MEDIUM",
                "occurrences": len(high_entropy_tokens),
                "sample": high_entropy_tokens[0][:12] + "...",
                "detail": f"High Shannon entropy string detected (> 4.5 bits/char); potential API secret.",
            })

        has_critical = any(f["severity"] == "CRITICAL" for f in findings)
        is_safe = len(findings) == 0

        return {
            "is_safe": is_safe,
            "has_critical_leak": has_critical,
            "total_leaks_found": len(findings),
            "findings": findings,
            "remediation": (
                "No leaked secrets detected. Client bundle is clean."
                if is_safe
                else "IMMEDIATE ACTION REQUIRED: Revoke compromised keys and remove secrets from client-facing assets."
            ),
        }

    def execute_zero_downtime_key_rotation(
        self, key_type: str = "service_role", grace_period_seconds: int = 300
    ) -> Dict[str, Any]:
        """
        Orchestrates dual-key zero-downtime rotation.
        Retires the previous key into a sliding grace period while issuing a fresh active key.
        """
        now = int(time.time())

        # Find existing active key
        previous_key_id = None
        for kid, kdata in self._key_registry.items():
            if kdata["key_type"] == key_type and kdata["status"] == "ACTIVE":
                kdata["status"] = "DEPRECATING"
                kdata["grace_expires_at"] = now + grace_period_seconds
                previous_key_id = kid
                break

        # Generate new active key
        new_key_id = f"key_{key_type}_{secrets.token_hex(4)}"
        new_secret = f"sb_secret_{secrets.token_hex(20)}"

        self._key_registry[new_key_id] = {
            "key_id": new_key_id,
            "key_type": key_type,
            "secret": new_secret,
            "status": "ACTIVE",
            "created_at": now,
            "grace_expires_at": None,
        }

        rotation_id = f"rot_{hashlib.sha256(f'{new_key_id}:{now}'.encode()).hexdigest()[:12]}"

        return {
            "rotation_id": rotation_id,
            "key_type": key_type,
            "active_key_id": new_key_id,
            "new_secret_masked": new_secret[:12] + "..." + new_secret[-4:],
            "deprecating_key_id": previous_key_id,
            "grace_period_seconds": grace_period_seconds,
            "status": "ROTATION_ACTIVE_IN_GRACE",
            "message": f"New key '{new_key_id}' activated. Previous key '{previous_key_id}' accepted for {grace_period_seconds}s grace window.",
        }

    def revoke_compromised_credential(self, key_id: str, reason: str) -> Dict[str, Any]:
        """
        Immediately invalidates a key and adds it to the cryptographic revocation blacklist.
        """
        now = int(time.time())
        self._revocation_blacklist.add(key_id)

        if key_id in self._key_registry:
            self._key_registry[key_id]["status"] = "REVOKED"
            self._key_registry[key_id]["revocation_reason"] = reason
            self._key_registry[key_id]["revoked_at"] = now

        return {
            "key_id": key_id,
            "status": "REVOKED_BLACKLISTED",
            "revoked_at": now,
            "reason": reason,
            "message": f"Credential '{key_id}' added to revocation blacklist. All subsequent authentications will fail.",
        }

    def is_key_valid(self, key_id: str) -> Dict[str, Any]:
        """
        Validates whether a key ID is usable or rejected.
        """
        now = int(time.time())
        if key_id in self._revocation_blacklist:
            return {"valid": False, "status": "REVOKED", "reason": "Key is blacklisted"}

        key_data = self._key_registry.get(key_id)
        if not key_data:
            return {"valid": False, "status": "NOT_FOUND", "reason": "Unrecognized key"}

        if key_data["status"] == "ACTIVE":
            return {"valid": True, "status": "ACTIVE", "reason": "Primary active key"}

        if key_data["status"] == "DEPRECATING":
            exp = key_data.get("grace_expires_at", 0)
            if now <= exp:
                return {"valid": True, "status": "DEPRECATING", "reason": f"In grace period (expires in {exp - now}s)"}
            else:
                return {"valid": False, "status": "EXPIRED", "reason": "Grace period expired"}

        return {"valid": False, "status": key_data["status"], "reason": "Inactive key"}
