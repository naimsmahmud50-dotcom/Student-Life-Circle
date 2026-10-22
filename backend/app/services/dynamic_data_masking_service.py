import hashlib
import json
import re
import time
from typing import Any, Dict, List, Optional


class DynamicDataMaskingService:
    """
    Role-Based Dynamic Data Masking & Redaction Service for Student Information Systems.
    Complies with FERPA, GDPR, and Bangladesh Data Protection Act.
    Applies contextual masking across student, faculty, and administrative perspectives.
    """

    ROLE_PERMISSIONS = {
        "student": {
            "mask_email": True,
            "mask_phone": True,
            "mask_national_id": True,
            "mask_gpa": True,
            "mask_financials": True,
        },
        "public": {
            "mask_email": True,
            "mask_phone": True,
            "mask_national_id": True,
            "mask_gpa": True,
            "mask_financials": True,
        },
        "faculty": {
            "mask_email": False,
            "mask_phone": True,
            "mask_national_id": True,
            "mask_gpa": False,
            "mask_financials": True,
        },
        "bursar": {
            "mask_email": False,
            "mask_phone": False,
            "mask_national_id": False,
            "mask_gpa": True,
            "mask_financials": False,
        },
        "academic_dean": {
            "mask_email": False,
            "mask_phone": False,
            "mask_national_id": False,
            "mask_gpa": False,
            "mask_financials": False,
        },
        "registrar": {
            "mask_email": False,
            "mask_phone": False,
            "mask_national_id": False,
            "mask_gpa": False,
            "mask_financials": False,
        },
        "service_role": {
            "mask_email": False,
            "mask_phone": False,
            "mask_national_id": False,
            "mask_gpa": False,
            "mask_financials": False,
        },
    }

    def __init__(self):
        pass

    @staticmethod
    def _mask_email(email: str) -> str:
        if not email or "@" not in email:
            return "******@masked.domain"
        name, domain = email.split("@", 1)
        if len(name) <= 2:
            masked_name = name[0] + "*"
        else:
            masked_name = name[0] + ("*" * (len(name) - 2)) + name[-1]
        return f"{masked_name}@{domain}"

    @staticmethod
    def _mask_phone(phone: str) -> str:
        if not phone or len(phone) < 7:
            return "+8801*******"
        prefix = phone[:6]
        suffix = phone[-3:]
        stars = "*" * (len(phone) - 9 if len(phone) > 9 else 4)
        return f"{prefix}{stars}{suffix}"

    @staticmethod
    def _mask_national_id(nid: str) -> str:
        if not nid or len(nid) < 8:
            return "**********"
        return nid[:4] + ("*" * (len(nid) - 8)) + nid[-4:]

    @staticmethod
    def _mask_gpa(gpa_val: Any) -> str:
        try:
            val = float(gpa_val)
            if val >= 3.75:
                return "3.75 - 4.00 (First Class Honors)"
            elif val >= 3.50:
                return "3.50 - 3.74 (Upper Second Class)"
            elif val >= 3.00:
                return "3.00 - 3.49 (Second Class)"
            else:
                return "Below 3.00"
        except (ValueError, TypeError):
            return "GPA_MASKED"

    def mask_student_record(
        self,
        record: Dict[str, Any],
        viewer_role: str,
        masking_policy: Optional[Dict[str, bool]] = None,
    ) -> Dict[str, Any]:
        """
        Transforms sensitive fields in a student record according to the viewer's role.
        """
        role_rules = masking_policy or self.ROLE_PERMISSIONS.get(
            viewer_role.lower(), self.ROLE_PERMISSIONS["public"]
        )

        masked = dict(record)
        applied_rules: List[str] = []

        if role_rules.get("mask_email") and "email" in masked:
            masked["email"] = self._mask_email(str(masked["email"]))
            applied_rules.append("EMAIL_PATTERN_MASKED")

        if role_rules.get("mask_phone") and "phone" in masked:
            masked["phone"] = self._mask_phone(str(masked["phone"]))
            applied_rules.append("PHONE_PATTERN_MASKED")

        if role_rules.get("mask_national_id") and "national_id" in masked:
            masked["national_id"] = self._mask_national_id(str(masked["national_id"]))
            applied_rules.append("NID_SURROUNDING_MASKED")

        if role_rules.get("mask_gpa") and "gpa" in masked:
            masked["gpa"] = self._mask_gpa(masked["gpa"])
            applied_rules.append("GPA_TIER_GENERALIZED")

        if role_rules.get("mask_financials"):
            for fin_field in ["scholarship_amount", "bursary_stipend", "tuition_due"]:
                if fin_field in masked:
                    masked[fin_field] = "[REDACTED_FINANCIAL_AID]"
                    applied_rules.append(f"{fin_field.upper()}_REDACTED")

        now = int(time.time())
        watermark = f"wm_v53_{hashlib.sha256(f'{viewer_role}:{now}'.encode()).hexdigest()[:12]}"

        return {
            "masked_record": masked,
            "viewer_role": viewer_role,
            "applied_rules": applied_rules,
            "redaction_count": len(applied_rules),
            "watermark": watermark,
        }

    def generate_masked_view_sql(
        self,
        table_name: str = "students",
        view_name: Optional[str] = None,
        column_rules: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Generates production-grade PostgreSQL dynamic masking view SQL statements.
        Uses auth.role() and auth.uid() context to evaluate runtime unmasking.
        """
        v_name = view_name or f"v_masked_{table_name}"
        rules = column_rules or {
            "email": "CASE WHEN auth.role() IN ('academic_dean', 'registrar', 'service_role') THEN email ELSE regexp_replace(email, '(?<=.).(?=.*@)', '*', 'g') END",
            "phone": "CASE WHEN auth.role() IN ('academic_dean', 'bursar', 'registrar') THEN phone ELSE overlay(phone placing '****' from 7 for 4) END",
            "national_id": "CASE WHEN auth.role() IN ('academic_dean', 'registrar', 'service_role') THEN national_id ELSE overlay(national_id placing '******' from 5 for 6) END",
            "gpa": "CASE WHEN auth.role() IN ('faculty', 'academic_dean', 'registrar') THEN gpa::text ELSE CASE WHEN gpa >= 3.5 THEN 'Honor Roll (>= 3.50)' ELSE 'Standard (< 3.50)' END END",
        }

        col_expressions = [f"  id", f"  full_name"]
        for col, expr in rules.items():
            col_expressions.append(f"  ({expr}) AS {col}")

        cols_sql = ",\n".join(col_expressions)
        sql = f"""-- Dynamic Masking View for table '{table_name}'
-- Complies with Strix Supabase Security Playbook & FERPA Rules
CREATE OR REPLACE VIEW public.{v_name} WITH (security_barrier = true) AS
SELECT
{cols_sql}
FROM public.{table_name};

GRANT SELECT ON public.{v_name} TO authenticated, anon;
"""
        return sql

    def evaluate_inference_risk(
        self, dataset: List[Dict[str, Any]], masked_columns: List[str]
    ) -> Dict[str, Any]:
        """
        Evaluates re-identification and linkage inference risk across a masked dataset.
        """
        if not dataset:
            return {
                "records_evaluated": 0,
                "re_identification_risk": 0.0,
                "risk_rating": "MINIMAL",
                "unique_rows": 0,
                "findings": ["Empty dataset passed"],
            }

        # Count quasi-identifier frequency combinations
        signatures: Dict[str, int] = {}
        for r in dataset:
            sig_parts = [str(r.get(col, "")) for col in masked_columns]
            sig = ":".join(sig_parts)
            signatures[sig] = signatures.get(sig, 0) + 1

        total = len(dataset)
        uniques = sum(1 for count in signatures.values() if count == 1)
        risk_pct = round((uniques / total) * 100.0, 2)

        risk_rating = "LOW"
        if risk_pct > 50.0:
            risk_rating = "HIGH"
        elif risk_pct > 20.0:
            risk_rating = "MEDIUM"

        return {
            "records_evaluated": total,
            "unique_quasi_tuples": len(signatures),
            "uniques_count": uniques,
            "re_identification_risk_percent": risk_pct,
            "risk_rating": risk_rating,
            "findings": [
                f"{uniques} out of {total} records possess unique quasi-identifier combinations.",
                f"Linkage attack resistance rating: {risk_rating} (risk: {risk_pct}%).",
            ],
        }
