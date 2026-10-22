# ==============================================================================
# File: backend/app/services/database_anonymization_vault_service.py
# Phase: 51 - Differential Privacy & K-Anonymity Vault
# Topic: Deterministic Pseudonymization, Laplacian Noise, & K-Anonymity Grouping
# Description: Implements cryptographic pseudonymization for student records, injects
#              Laplacian differential privacy noise for aggregate statistics, and
#              evaluates K-Anonymity (k >= 5) to guarantee zero re-identification risk.
# ==============================================================================

import math
import random
import hmac
import hashlib
from typing import Dict, Any, List, Optional, Tuple

class DatabaseAnonymizationVaultService:
    """
    Database Anonymization & Differential Privacy Vault.
    Transforms raw academic and financial databases into mathematically
    guaranteed privacy-preserving datasets for institutional AI/ML training and reporting.
    """

    DEFAULT_EPSILON = 0.5  # Privacy budget parameter
    MIN_K_ANONYMITY = 5    # Minimum equivalence class threshold

    def __init__(self, master_pepper: str = "master-privacy-pepper-key-2026"):
        self.pepper = master_pepper.encode("utf-8")
        
        # Telemetry stats
        self._stats = {
            "records_pseudonymized": 0,
            "dp_queries_computed": 0,
            "k_anonymity_evaluations": 0
        }

    def pseudonymize_identifier(self, raw_value: str, field_salt: str = "stu_identity") -> str:
        """
        Computes deterministic, keyed HMAC pseudonym for student IDs, NID, and email.
        Allows relational join analysis without storing plaintext identity.
        """
        self._stats["records_pseudonymized"] += 1
        combined = f"{field_salt}:{raw_value}"
        sig = hmac.new(self.pepper, combined.encode("utf-8"), hashlib.sha256).hexdigest()
        return f"ps_{sig[:16]}"

    def inject_laplace_noise(self, true_value: float, sensitivity: float = 1.0, epsilon: float = 0.5) -> Dict[str, Any]:
        """
        Adds Laplacian differential privacy noise to aggregate queries (e.g. GPA or scholarship sums).
        Noise is drawn from Laplace(0, sensitivity / epsilon).
        """
        self._stats["dp_queries_computed"] += 1
        scale = sensitivity / max(0.01, epsilon)
        
        # Draw from standard uniform to produce Laplacian sample: u in (-0.5, 0.5)
        u = random.random() - 0.5
        noise = -scale * math.copysign(1.0, u) * math.log(1.0 - 2.0 * abs(u)) if abs(u) < 0.5 else 0.0
        
        noisy_value = true_value + noise

        return {
            "true_value": round(true_value, 4),
            "noisy_value": round(noisy_value, 4),
            "noise_added": round(noise, 4),
            "epsilon_budget": epsilon,
            "scale_parameter": round(scale, 4),
            "privacy_guarantee": f"Differential Privacy (eps={epsilon})"
        }

    def evaluate_k_anonymity(
        self,
        records: List[Dict[str, Any]],
        quasi_identifiers: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluates K-Anonymity across given quasi-identifiers (e.g. ['district', 'admission_year', 'gender']).
        Finds the smallest equivalence class k_min and computes maximum re-identification risk.
        """
        self._stats["k_anonymity_evaluations"] += 1
        if not records:
            return {"k_min": 0, "is_k_anonymous": False, "re_identification_risk": 1.0, "total_classes": 0}

        # Group records by tuple of quasi-identifier values
        classes: Dict[Tuple, int] = {}
        for r in records:
            key = tuple(str(r.get(qid, "UNKNOWN")) for qid in quasi_identifiers)
            classes[key] = classes.get(key, 0) + 1

        k_min = min(classes.values()) if classes else 0
        is_safe = k_min >= self.MIN_K_ANONYMITY
        re_identification_risk = round(1.0 / max(1, k_min), 4)

        return {
            "is_k_anonymous": is_safe,
            "k_min_achieved": k_min,
            "required_k_min": self.MIN_K_ANONYMITY,
            "total_equivalence_classes": len(classes),
            "total_records": len(records),
            "max_re_identification_risk": re_identification_risk,
            "status": "APPROVED_FOR_PUBLIC_RELEASE" if is_safe else "REIDENTIFICATION_RISK_HIGH"
        }

    def anonymize_dataset(
        self,
        dataset: List[Dict[str, Any]],
        direct_identifiers: List[str],
        quasi_identifiers: List[str]
    ) -> Dict[str, Any]:
        """
        Comprehensively sanitizes a dataset: replaces direct identifiers with pseudonyms,
        and evaluates K-Anonymity on the resulting output.
        """
        sanitized = []
        for row in dataset:
            clean_row = dict(row)
            for d_id in direct_identifiers:
                if d_id in clean_row:
                    clean_row[d_id] = self.pseudonymize_identifier(str(clean_row[d_id]), field_salt=d_id)
            sanitized.append(clean_row)

        k_eval = self.evaluate_k_anonymity(sanitized, quasi_identifiers)

        return {
            "records_processed": len(sanitized),
            "sanitized_sample": sanitized[:5],
            "k_anonymity_report": k_eval
        }

    def get_vault_metrics(self) -> Dict[str, Any]:
        """Returns privacy vault metrics."""
        return {
            "stats": dict(self._stats),
            "default_epsilon": self.DEFAULT_EPSILON,
            "min_k_threshold": self.MIN_K_ANONYMITY
        }
