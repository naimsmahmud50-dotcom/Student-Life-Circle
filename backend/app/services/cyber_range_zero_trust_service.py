"""
Autonomous Cyber Range & Zero-Trust Defense Sandbox Service.
Implements NIST SP 800-207 Zero-Trust Architecture:
- Continuous Dynamic Trust Scoring (0-100) based on Device, IP, MFA, and Geo-Velocity
- Multi-Vector Threat Detection (SQLi, XSS, Path Traversal, JWT Alg=None)
- Automated Payload Sanitization and Forensic Audit Logging
"""

import hashlib
import html
import re
import time
from typing import Dict, Any, List, Optional, Tuple


class CyberRangeZeroTrustService:
    """
    Zero-Trust Continuous Verification and Cyber Threat Defense Sandbox.
    Enforces 'Never Trust, Always Verify' across student sessions and API payloads.
    """

    # Signature heuristics for injection attacks
    SQLI_PATTERNS = [
        re.compile(r"(\bunion\b.*\bselect\b)", re.IGNORECASE),
        re.compile(r"(\bor\b\s+['\"0-9a-z]+\s*=\s*['\"0-9a-z]+)", re.IGNORECASE),
        re.compile(r"(--|#|/\*).*", re.IGNORECASE),
        re.compile(r"(\bdrop\b\s+\btable\b)", re.IGNORECASE),
        re.compile(r"(\bselect\b.*\bfrom\b)", re.IGNORECASE),
        re.compile(r"(\bsleep\s*\(\s*\d+\s*\))", re.IGNORECASE)
    ]

    XSS_PATTERNS = [
        re.compile(r"<\s*script[^>]*>", re.IGNORECASE),
        re.compile(r"javascript\s*:", re.IGNORECASE),
        re.compile(r"on(load|error|click|mouseover)\s*=", re.IGNORECASE),
        re.compile(r"<\s*img[^>]+src=[^>]+onerror=", re.IGNORECASE),
        re.compile(r"<\s*svg[^>]*onload=", re.IGNORECASE)
    ]

    PATH_TRAVERSAL_PATTERNS = [
        re.compile(r"\.\./|\.\.\\"),
        re.compile(r"%2e%2e%2f|%2e%2e/", re.IGNORECASE)
    ]

    JWT_VULN_PATTERNS = [
        re.compile(r'"alg"\s*:\s*"none"', re.IGNORECASE),
        re.compile(r'"alg"\s*:\s*""', re.IGNORECASE)
    ]

    _incident_forensics_log: List[Dict[str, Any]] = []

    @classmethod
    def evaluate_zero_trust_access(
        cls,
        student_id: str,
        device_fingerprint: str,
        ip_address: str = "127.0.0.1",
        mfa_authenticated: bool = True,
        geo_velocity_kmh: float = 0.0,
        payload_sample: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Continuously calculates trust score (0 - 100) and issues dynamic access verdict.
        """
        clean_id = (student_id or "").strip()
        if not clean_id:
            raise ValueError("Student ID is required for Zero-Trust evaluation")

        trust_score = 100.0
        anomaly_flags: List[str] = []
        risk_factors: Dict[str, float] = {}

        # 1. MFA Evaluation
        if not mfa_authenticated:
            trust_score -= 35.0
            anomaly_flags.append("MFA_NOT_PRESENT")
            risk_factors["mfa_penalty"] = 35.0

        # 2. Geo-Velocity / Impossible Travel Anomaly
        velocity = max(0.0, float(geo_velocity_kmh))
        if velocity > 800.0:  # Faster than commercial jet airliner
            trust_score -= 45.0
            anomaly_flags.append("IMPOSSIBLE_TRAVEL_SPEED_EXCEEDED")
            risk_factors["geo_velocity_penalty"] = 45.0
        elif velocity > 120.0:
            trust_score -= 15.0
            anomaly_flags.append("ELEVATED_TRANSIT_VELOCITY")
            risk_factors["geo_velocity_penalty"] = 15.0

        # 3. Device Posture Entropy Check
        if not device_fingerprint or len(device_fingerprint) < 16:
            trust_score -= 20.0
            anomaly_flags.append("LOW_ENTROPY_UNVERIFIED_DEVICE")
            risk_factors["device_penalty"] = 20.0

        # 4. IP Risk Assessment
        if ip_address.startswith("10.0.") or ip_address.startswith("192.168.") or ip_address in ("127.0.0.1", "::1"):
            risk_factors["ip_reputation"] = 0.0  # Trusted internal/loopback
        elif ip_address.startswith("198.51.100."):  # Testnet threat IP simulation
            trust_score -= 30.0
            anomaly_flags.append("SUSPICIOUS_PROXY_OR_TOR_EXIT_NODE")
            risk_factors["ip_penalty"] = 30.0

        # 5. Active Payload Threat Inspection
        payload_malicious = False
        if payload_sample:
            threat_eval = cls.inspect_and_sanitize_payload(payload_sample, "BODY")
            if threat_eval["is_malicious"]:
                payload_malicious = True
                trust_score -= 50.0
                anomaly_flags.extend([f"THREAT_DETECTED:{t}" for t in threat_eval["attack_types"]])
                risk_factors["payload_threat_penalty"] = 50.0

        # Bound trust score strictly between 0.0 and 100.0
        final_trust_score = max(0.0, min(100.0, trust_score))

        # Dynamic Policy Decision Matrix
        if final_trust_score >= 80.0:
            decision = "ALLOW"
            access_granted = True
            threat_level = "LOW"
        elif final_trust_score >= 50.0:
            decision = "CHALLENGE_STEP_UP_MFA"
            access_granted = False
            threat_level = "MEDIUM"
        else:
            decision = "DENY"
            access_granted = False
            threat_level = "CRITICAL" if payload_malicious else "HIGH"

        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # Record high/critical risk forensic event
        if final_trust_score < 70.0:
            cls.record_incident(
                student_id=clean_id,
                threat_level=threat_level,
                decision=decision,
                anomaly_flags=anomaly_flags,
                ip_address=ip_address
            )

        return {
            "student_id": clean_id,
            "trust_score": round(final_trust_score, 1),
            "access_granted": access_granted,
            "decision": decision,
            "threat_level": threat_level,
            "anomaly_flags": anomaly_flags,
            "risk_factors": risk_factors,
            "verification_timestamp": timestamp
        }

    @classmethod
    def inspect_and_sanitize_payload(cls, payload_text: str, context_type: str = "QUERY") -> Dict[str, Any]:
        """
        Scans payload string for web injection threats and returns sanitized output.
        """
        if payload_text is None:
            return {
                "is_malicious": False,
                "attack_types": [],
                "sanitized_output": "",
                "risk_score": 0.0,
                "detection_signature": "CLEAN"
            }

        text = str(payload_text)
        detected_attacks: List[str] = []

        # Check SQL Injection
        for pattern in cls.SQLI_PATTERNS:
            if pattern.search(text):
                detected_attacks.append("SQL_INJECTION")
                break

        # Check XSS
        for pattern in cls.XSS_PATTERNS:
            if pattern.search(text):
                detected_attacks.append("CROSS_SITE_SCRIPTING")
                break

        # Check Path Traversal
        for pattern in cls.PATH_TRAVERSAL_PATTERNS:
            if pattern.search(text):
                detected_attacks.append("PATH_TRAVERSAL")
                break

        # Check JWT None Algorithm
        for pattern in cls.JWT_VULN_PATTERNS:
            if pattern.search(text):
                detected_attacks.append("JWT_ALGORITHM_NONE_FORGERY")
                break

        is_malicious = len(detected_attacks) > 0
        risk_score = round(min(1.0, len(detected_attacks) * 0.45), 2) if is_malicious else 0.0

        # Perform defensive HTML entity sanitization
        sanitized = html.escape(text)

        signature = "THREAT:" + "+".join(detected_attacks) if is_malicious else "CLEAN_PAYLOAD"

        return {
            "is_malicious": is_malicious,
            "attack_types": detected_attacks,
            "sanitized_output": sanitized,
            "risk_score": risk_score,
            "detection_signature": signature
        }

    @classmethod
    def record_incident(
        cls,
        student_id: str,
        threat_level: str,
        decision: str,
        anomaly_flags: List[str],
        ip_address: str
    ) -> Dict[str, Any]:
        """
        Appends an immutable forensic event to the in-memory telemetry log.
        """
        ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        raw_hash = hashlib.sha256(f"{student_id}:{ts}:{threat_level}:{ip_address}".encode("utf-8")).hexdigest()
        event_id = f"INCIDENT-{raw_hash[:12].upper()}"

        record = {
            "event_id": event_id,
            "student_id": student_id,
            "threat_level": threat_level,
            "decision": decision,
            "anomaly_flags": anomaly_flags,
            "ip_address": ip_address,
            "timestamp": ts,
            "forensic_hash": raw_hash
        }
        cls._incident_forensics_log.append(record)
        return record

    @classmethod
    def get_forensics_log(cls, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns recent forensics security incidents."""
        return cls._incident_forensics_log[-limit:]

    @classmethod
    def reset_forensics_for_testing(cls) -> None:
        """Helper for test isolation."""
        cls._incident_forensics_log.clear()
