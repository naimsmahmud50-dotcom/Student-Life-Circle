"""
========================================================================================
MODULE:    Defense-in-Depth Security Headers & Minor Data Sanitization Filter
TOPIC:     HTTP Response Headers, CSP, Anti-Clickjacking & ASVS L2 Minor Privacy
FILE:      backend/app/core/security_headers.py
PURPOSE:   Enforces non-negotiable enterprise security standards:
           1. Injects hardened HTTP response headers (CSP, HSTS, X-Frame-Options DENY,
              X-Content-Type-Options nosniff, Referrer-Policy).
           2. ASVS L2 Minor Data Masking: Automatically redacts phone numbers, exact
              residential addresses, and private messaging channels for learners under 16,
              unless requested by verified guardians or compliance administrators.
AUDIENCE:  Security Compliance Engineers, Privacy Officers & AI Agents
STANDARDS: OWASP ASVS 4.0 L2, OWASP Secure Headers Guide, Zero-Emoji Spec
========================================================================================
"""

import copy
from typing import Dict, Any, List, Optional


class SecurityHeadersManager:
    """
    Manages defense-in-depth security headers and ASVS L2 child privacy data filters.
    """

    DEFAULT_SECURITY_HEADERS = {
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        ),
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
        "X-XSS-Protection": "1; mode=block"
    }

    @classmethod
    def get_standard_headers(cls) -> Dict[str, str]:
        """Returns the dictionary of hardened production HTTP response headers."""
        return copy.deepcopy(cls.DEFAULT_SECURITY_HEADERS)

    @classmethod
    def sanitize_minor_profile_data(
        cls,
        student_data: Dict[str, Any],
        requester_user_id: Optional[str] = None,
        requester_roles: Optional[List[str]] = None,
        authorized_guardian_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Sanitizes profile payload according to ASVS L2 child protection doctrine:
        - If student is a minor (<16 or is_minor flag True), sensitive PII (phone, exact address,
          unverified contact handles) is redacted with '[REDACTED_MINOR_PRIVACY_PROTECTED]'.
        - Exemption: Requester is the student themselves, their linked guardian, or an ADMIN.
        """
        data = copy.deepcopy(student_data)
        age = data.get("age", 18)
        is_minor = data.get("is_minor", age < 16)

        if not is_minor:
            return data

        # Check authorization exemptions
        student_id = data.get("student_id") or data.get("user_id")
        is_self = requester_user_id and requester_user_id == student_id
        is_admin = requester_roles and "ADMIN" in requester_roles
        is_linked_guardian = (
            requester_user_id and 
            authorized_guardian_ids and 
            requester_user_id in authorized_guardian_ids
        )

        if is_self or is_admin or is_linked_guardian:
            # Authorized to view full data
            data["_minor_privacy_view"] = "AUTHORIZED_FULL"
            return data

        # Redact sensitive fields for public / unauthorized viewers
        sensitive_fields = [
            "phone_number",
            "phone",
            "mobile",
            "email",
            "street_address",
            "residential_address",
            "guardian_phone",
            "chat_handle",
            "whatsapp_number"
        ]

        for field in sensitive_fields:
            if field in data:
                data[field] = "[REDACTED_MINOR_PRIVACY_PROTECTED]"

        # Recursively sanitize nested dictionaries (e.g. location, contact_info)
        nested_sensitive = {"address_line", "street", "house", "road", "phone", "mobile", "email"}
        for parent_key, parent_val in list(data.items()):
            if isinstance(parent_val, dict):
                nested_copy = copy.deepcopy(parent_val)
                for sub_key in list(nested_copy.keys()):
                    if sub_key.lower() in nested_sensitive:
                        nested_copy[sub_key] = "[REDACTED_MINOR_PRIVACY_PROTECTED]"
                data[parent_key] = nested_copy

        data["_minor_privacy_view"] = "REDACTED_ASVS_L2"
        data["is_profile_private"] = True
        return data


# Singleton export
security_headers = SecurityHeadersManager()
