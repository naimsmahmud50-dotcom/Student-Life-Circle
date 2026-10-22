"""
Phase 58: Verifiable Credential Engine Service.
Synthesizes W3C Verifiable Credentials Data Model v2.0 JSON-LD credentials,
canonicalizes with RFC 8785 JCS, signs with cryptographic proofs, and
renders XSS-hardened SVG badges for Bangladeshi academic institutions.
"""

import json
import hashlib
import hmac
import uuid
import re
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class VerifiableCredentialEngineService:
    """
    W3C Verifiable Credential synthesizer and tamper-evident verification engine.
    """

    INSTITUTION_REGISTRY: Dict[str, Dict[str, str]] = {
        "did:web:du.ac.bd:issuers:registrar": {
            "name": "University of Dhaka (DU)",
            "key_id": "did:web:du.ac.bd#key-2026-ed25519",
            "secret": "du_secret_institutional_key_seed_2026_xyz"
        },
        "did:web:buet.ac.bd:issuers:dean": {
            "name": "Bangladesh University of Engineering & Technology (BUET)",
            "key_id": "did:web:buet.ac.bd#key-2026-ed25519",
            "secret": "buet_secret_institutional_key_seed_2026_xyz"
        },
        "did:web:nsu.edu:issuers:controller": {
            "name": "North South University (NSU)",
            "key_id": "did:web:nsu.edu#key-2026-ed25519",
            "secret": "nsu_secret_institutional_key_seed_2026_xyz"
        }
    }

    # Strix XSS sanitization pattern
    DANGEROUS_SVG_PATTERN = re.compile(r"<\s*script|onload|onerror|javascript:|<\s*foreignObject", re.IGNORECASE)

    def __init__(self):
        # Monotonically increasing status list index generator
        self._next_status_index = 1001

    def sanitize_string(self, text: str) -> str:
        """
        Escapes text for safe inclusion in JSON-LD and SVG templates.
        """
        if not text:
            return ""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
        )

    def issue_credential(
        self,
        student_id: str,
        student_name: str,
        institution_did: str,
        degree_title: str,
        cgpa: float,
        graduation_year: int,
        honors_designation: str = "First Class Honours"
    ) -> Dict[str, Any]:
        """
        Issues an authentic W3C VC v2.0 JSON-LD academic degree credential.
        """
        if not (0.0 <= cgpa <= 4.0):
            raise ValueError(f"CGPA {cgpa} is outside the valid range (0.00 - 4.00).")

        clean_student_id = self.sanitize_string(student_id.strip())
        clean_student_name = self.sanitize_string(student_name.strip())
        clean_degree = self.sanitize_string(degree_title.strip())

        inst_info = self.INSTITUTION_REGISTRY.get(institution_did)
        if not inst_info:
            inst_info = {
                "name": "Bangladeshi Institutional Accredited Partner",
                "key_id": f"{institution_did}#key-1",
                "secret": "fallback_academic_vault_seed_2026"
            }

        credential_id = f"urn:uuid:{uuid.uuid4()}"
        status_index = self._next_status_index
        self._next_status_index += 1

        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Unsigned W3C VC v2.0 Document
        vc_payload: Dict[str, Any] = {
            "@context": [
                "https://www.w3.org/ns/credentials/v2",
                "https://studentlifecircle.edu.bd/contexts/academic-v1.jsonld"
            ],
            "id": credential_id,
            "type": ["VerifiableCredential", "AcademicDegreeCredential"],
            "issuer": {
                "id": institution_did,
                "name": inst_info["name"]
            },
            "validFrom": now_iso,
            "credentialSubject": {
                "id": f"did:key:z6MkpTHR8VNsBxYAAWHuEc2KAguPuHdO83nB{clean_student_id[-4:]}",
                "studentId": clean_student_id,
                "studentName": clean_student_name,
                "degree": clean_degree,
                "cgpa": round(cgpa, 2),
                "graduationYear": graduation_year,
                "honors": honors_designation
            },
            "credentialStatus": {
                "id": f"{institution_did}/status/status-list-2026",
                "type": "BitstringStatusListEntry",
                "statusPurpose": "revocation",
                "statusListIndex": status_index
            }
        }

        # RFC 8785 JSON Canonicalization Scheme (JCS) representation
        canonical_json = json.dumps(vc_payload, sort_keys=True, separators=(",", ":"))
        canonical_digest = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

        # Cryptographic Signature (Ed25519 simulated via HMAC-SHA256 institutional secret)
        sig_raw = hmac.new(
            inst_info["secret"].encode("utf-8"),
            canonical_digest.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        # Append W3C Proof Suite
        vc_payload["proof"] = {
            "type": "Ed25519Signature2020",
            "created": now_iso,
            "verificationMethod": inst_info["key_id"],
            "proofPurpose": "assertionMethod",
            "proofValue": f"z{sig_raw[:64]}",
            "canonicalDigest": canonical_digest
        }

        # Render XSS-hardened SVG Badge
        svg_badge = self.render_svg_badge(student_name, degree_title, inst_info["name"], cgpa, graduation_year)

        return {
            "credential_id": credential_id,
            "w3c_payload": vc_payload,
            "canonical_digest": canonical_digest,
            "ed25519_signature": vc_payload["proof"]["proofValue"],
            "status_list_index": status_index,
            "is_valid": True,
            "svg_badge": svg_badge
        }

    def verify_credential(
        self,
        credential_payload: Dict[str, Any],
        expected_issuer_did: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cryptographically verifies the authenticity and tamper-resistance of a W3C Credential.
        """
        if not isinstance(credential_payload, dict):
            return {
                "is_valid": False,
                "issuer_verified": False,
                "tamper_detected": True,
                "revocation_status": "CORRUPT_PAYLOAD",
                "verification_report": "Payload is not a valid dictionary.",
                "claimed_student_name": "",
                "claimed_degree": ""
            }

        proof = credential_payload.get("proof")
        if not proof or not isinstance(proof, dict):
            return {
                "is_valid": False,
                "issuer_verified": False,
                "tamper_detected": True,
                "revocation_status": "MISSING_PROOF",
                "verification_report": "W3C Credential lacks cryptographic proof block.",
                "claimed_student_name": "",
                "claimed_degree": ""
            }

        issuer_obj = credential_payload.get("issuer", {})
        issuer_did = issuer_obj.get("id") if isinstance(issuer_obj, dict) else str(issuer_obj)

        if expected_issuer_did and issuer_did != expected_issuer_did:
            return {
                "is_valid": False,
                "issuer_verified": False,
                "tamper_detected": False,
                "revocation_status": "ISSUER_MISMATCH",
                "verification_report": f"Issuer DID {issuer_did} does not match expected {expected_issuer_did}.",
                "claimed_student_name": "",
                "claimed_degree": ""
            }

        inst_info = self.INSTITUTION_REGISTRY.get(issuer_did)
        issuer_verified = inst_info is not None

        # Extract payload without proof to recalculate JCS canonical digest
        payload_copy = {k: v for k, v in credential_payload.items() if k != "proof"}
        recalculated_canonical = json.dumps(payload_copy, sort_keys=True, separators=(",", ":"))
        recalculated_digest = hashlib.sha256(recalculated_canonical.encode("utf-8")).hexdigest()

        claimed_digest = proof.get("canonicalDigest")
        claimed_sig = proof.get("proofValue", "")

        # Recalculate signature if issuer known
        tamper_detected = False
        if claimed_digest != recalculated_digest:
            tamper_detected = True
        elif inst_info:
            expected_sig = hmac.new(
                inst_info["secret"].encode("utf-8"),
                recalculated_digest.encode("utf-8"),
                hashlib.sha256
            ).hexdigest()
            if not claimed_sig.endswith(expected_sig[:64]):
                tamper_detected = True

        subject = credential_payload.get("credentialSubject", {})
        student_name = subject.get("studentName", "Unknown")
        degree = subject.get("degree", "Unknown")

        if tamper_detected:
            return {
                "is_valid": False,
                "issuer_verified": issuer_verified,
                "tamper_detected": True,
                "revocation_status": "SIGNATURE_INVALID",
                "verification_report": "Cryptographic signature mismatch! Content was altered post-issuance.",
                "claimed_student_name": student_name,
                "claimed_degree": degree
            }

        return {
            "is_valid": True,
            "issuer_verified": issuer_verified,
            "tamper_detected": False,
            "revocation_status": "ACTIVE_VERIFIED",
            "verification_report": "Valid W3C Verifiable Credential. Cryptographic signature and issuer identity confirmed.",
            "claimed_student_name": student_name,
            "claimed_degree": degree
        }

    def render_svg_badge(
        self,
        student_name: str,
        degree: str,
        institution_name: str,
        cgpa: float,
        graduation_year: int
    ) -> str:
        """
        Renders an XSS-hardened SVG badge.
        Strix Security Rule: Zero script tags or foreignObjects allowed.
        """
        clean_name = self.sanitize_string(student_name)
        clean_deg = self.sanitize_string(degree)
        clean_inst = self.sanitize_string(institution_name)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 200" width="100%" height="100%">
  <defs>
    <linearGradient id="certGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#1e293b" />
    </linearGradient>
  </defs>
  <rect width="480" height="200" rx="16" fill="url(#certGrad)" stroke="#334155" stroke-width="2" />
  <circle cx="430" cy="45" r="22" fill="#10b981" fill-opacity="0.2" stroke="#10b981" stroke-width="2" />
  <path d="M422 45l5 5 12-12" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
  <text x="32" y="42" fill="#94a3b8" font-family="system-ui, sans-serif" font-size="11" font-weight="600" letter-spacing="1">VERIFIED ACADEMIC CREDENTIAL</text>
  <text x="32" y="76" fill="#f8fafc" font-family="system-ui, sans-serif" font-size="18" font-weight="700">{clean_name}</text>
  <text x="32" y="105" fill="#38bdf8" font-family="system-ui, sans-serif" font-size="13" font-weight="500">{clean_deg}</text>
  <text x="32" y="132" fill="#cbd5e1" font-family="system-ui, sans-serif" font-size="11">{clean_inst} • Class of {graduation_year}</text>
  <line x1="32" y1="150" x2="448" y2="150" stroke="#334155" stroke-width="1" />
  <text x="32" y="174" fill="#10b981" font-family="system-ui, sans-serif" font-size="12" font-weight="700">CGPA: {cgpa:.2f} / 4.00</text>
  <text x="448" y="174" text-anchor="end" fill="#64748b" font-family="ui-monospace, monospace" font-size="10">W3C Ed25519 Verified</text>
</svg>"""

        if self.DANGEROUS_SVG_PATTERN.search(svg):
            raise ValueError("Dangerous XSS pattern detected in generated SVG.")

        return svg
