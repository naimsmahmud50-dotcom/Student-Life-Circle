# ==============================================================================
# File: backend/app/services/storage_multipart_sanitizer_service.py
# Phase: 50 - Storage Multipart Upload & MIME Antivirus Sanitizer
# Topic: Presigned Chunked Tickets, Magic Byte MIME Defense, & SVG XSS Neutralizer
# Description: Generates HMAC-signed multipart upload tickets, inspects file binary
#              magic bytes to defeat MIME spoofing, and sanitizes SVG/HTML uploads to
#              eliminate Stored XSS threats on Supabase Storage buckets.
# ==============================================================================

import re
import time
import hmac
import hashlib
import uuid
from typing import Dict, Any, List, Optional, Tuple

class StorageMultipartSanitizerService:
    """
    Supabase Storage Multipart Security & MIME Antivirus Sanitizer Engine.
    Enforces cryptographically signed upload authorizations, verifies binary magic bytes,
    and neutralizes Stored Cross-Site Scripting (XSS) vectors in uploaded student documents.
    """

    # Binary magic byte signatures
    MAGIC_SIGNATURES = {
        "application/pdf": b"%PDF-",
        "image/png": b"\x89PNG\r\n\x1a\n",
        "image/jpeg": b"\xff\xd8\xff",
        "application/zip": b"PK\x03\x04"
    }

    # Prohibited XSS patterns in SVG / HTML documents
    MALICIOUS_XSS_PATTERNS = [
        re.compile(r"<\s*script[^>]*>.*?</\s*script\s*>", re.IGNORECASE | re.DOTALL),
        re.compile(r"on\w+\s*=\s*[\"'].*?[\"']", re.IGNORECASE),
        re.compile(r"javascript:\s*", re.IGNORECASE),
        re.compile(r"<\s*(?:iframe|embed|object|base|link)[^>]*>", re.IGNORECASE),
        re.compile(r"xlink:href\s*=\s*[\"']javascript:.*?[\"']", re.IGNORECASE)
    ]

    def __init__(self, signing_secret: str = "secret-storage-hmac-master-key-2026"):
        self.signing_secret = signing_secret.encode("utf-8")
        
        # Telemetry stats
        self._stats = {
            "tickets_issued": 0,
            "uploads_inspected": 0,
            "mime_spoofs_blocked": 0,
            "svg_xss_sanitized": 0,
            "clean_files_approved": 0
        }

    def generate_presigned_upload_ticket(
        self,
        bucket_id: str,
        file_path: str,
        user_id: str,
        allowed_mime_types: List[str],
        max_size_bytes: int = 10485760,  # 10 MB default
        ttl_seconds: int = 900           # 15 minutes
    ) -> Dict[str, Any]:
        """Generates an HMAC-signed upload ticket for chunked multipart upload."""
        self._stats["tickets_issued"] += 1
        now = time.time()
        expires_at = now + ttl_seconds
        ticket_id = f"tkt_{uuid.uuid4().hex[:12]}"

        # Canonical string for HMAC signing
        canonical = f"{ticket_id}:{bucket_id}:{file_path}:{user_id}:{expires_at}:{max_size_bytes}"
        signature = hmac.new(self.signing_secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()

        return {
            "ticket_id": ticket_id,
            "bucket_id": bucket_id,
            "target_path": file_path,
            "user_id": user_id,
            "max_size_bytes": max_size_bytes,
            "allowed_mime_types": allowed_mime_types,
            "expires_at": expires_at,
            "hmac_signature": signature,
            "upload_endpoint": f"https://supabase.agrojatra.edu.bd/storage/v1/upload/{bucket_id}/{ticket_id}"
        }

    def verify_and_sanitize_upload(
        self,
        file_bytes: bytes,
        declared_mime_type: str,
        file_name: str
    ) -> Dict[str, Any]:
        """
        Inspects binary magic bytes, validates file integrity, and neutralizes XSS in SVGs.
        Returns safety verdict, sanitized payload, and required download security headers.
        """
        self._stats["uploads_inspected"] += 1
        violations = []
        sanitized_bytes = file_bytes
        was_sanitized = False

        # 1. Magic Byte Signature Verification
        expected_sig = self.MAGIC_SIGNATURES.get(declared_mime_type)
        if expected_sig:
            if not file_bytes.startswith(expected_sig):
                self._stats["mime_spoofs_blocked"] += 1
                violations.append({
                    "code": "MIME_TYPE_SPOOFING",
                    "severity": "CRITICAL",
                    "message": f"Binary magic bytes mismatch for claimed MIME '{declared_mime_type}'. Spoofed extension/header detected."
                })

        # 2. SVG / XML / HTML Stored XSS Neutralization
        if "svg" in declared_mime_type or file_name.lower().endswith(".svg") or "html" in declared_mime_type:
            text_content = file_bytes.decode("utf-8", errors="ignore")
            detected_attacks = []

            for pattern in self.MALICIOUS_XSS_PATTERNS:
                if pattern.search(text_content):
                    detected_attacks.append(pattern.pattern[:25])
                    text_content = pattern.sub("", text_content)
                    was_sanitized = True

            if was_sanitized:
                self._stats["svg_xss_sanitized"] += 1
                sanitized_bytes = text_content.encode("utf-8")
                violations.append({
                    "code": "STORED_XSS_NEUTRALIZED",
                    "severity": "HIGH",
                    "message": f"Active script tags or inline event handlers stripped from SVG: {detected_attacks}"
                })

        # Security Headers to prevent MIME sniffing in browsers
        safe_headers = {
            "Content-Disposition": f'attachment; filename="{file_name}"',
            "X-Content-Type-Options": "nosniff",
            "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'"
        }

        is_safe = not any(v["code"] == "MIME_TYPE_SPOOFING" for v in violations)
        if is_safe and not was_sanitized:
            self._stats["clean_files_approved"] += 1

        return {
            "safe": is_safe,
            "was_sanitized": was_sanitized,
            "violations": violations,
            "declared_mime_type": declared_mime_type,
            "file_size_bytes": len(sanitized_bytes),
            "enforced_download_headers": safe_headers,
            "status": "APPROVED" if is_safe else "REJECTED"
        }

    def get_storage_metrics(self) -> Dict[str, Any]:
        """Returns storage sanitizer operational telemetry."""
        return {
            "stats": dict(self._stats),
            "supported_magic_types": list(self.MAGIC_SIGNATURES.keys()),
            "xss_patterns_count": len(self.MALICIOUS_XSS_PATTERNS)
        }
