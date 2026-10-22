"""
Virtual Science Laboratory Service for Agrojatra Platform.
Provides high-fidelity physics and chemistry simulation engines:
1. DC Electrical Circuit Simulator (Ohm's & Kirchhoff's laws, short-circuit guard).
2. Geometric Optics Ray Tracer (Convex/Concave thin lens formula, focal singularity handler).
3. Acid-Base Titration Curve Calculator (Equivalence point, pH curve, indicator chromophoric transitions).
4. Automated Lab Report Synthesizer with relative percentage error validation.
"""

import math
import uuid
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class VirtualScienceLabService:
    def __init__(self):
        pass

    def simulate_circuit(
        self,
        circuit_id: str,
        source_voltage: float,
        configuration: str = "SERIES",
        components: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Simulates DC circuit behavior using Ohm's and Kirchhoff's circuit laws.
        Protects against divide-by-zero on short circuits with a 0.001 Ohm floor.
        """
        if not components:
            # Default component set: 2 series resistors
            components = [
                {"id": "R1", "type": "RESISTOR", "value": 10.0},
                {"id": "R2", "type": "RESISTOR", "value": 20.0},
            ]

        # Sanitize component resistance values
        sanitized_components = []
        for c in components:
            val = float(c.get("value", 10.0))
            if val < 0:
                val = 0.0
            sanitized_components.append({
                "id": str(c.get("id", f"C-{uuid.uuid4().hex[:4]}")),
                "type": str(c.get("type", "RESISTOR")).upper(),
                "value": val,
            })

        config_upper = configuration.strip().upper()
        if config_upper not in ["SERIES", "PARALLEL"]:
            config_upper = "SERIES"

        is_short_circuit = False

        if config_upper == "SERIES":
            raw_total_r = sum(c["value"] for c in sanitized_components)
            if raw_total_r < 0.05:
                is_short_circuit = True
            total_resistance = max(raw_total_r, 0.001)
            total_current = source_voltage / total_resistance
            total_power = source_voltage * total_current

            # Component telemetry
            telemetry = []
            for c in sanitized_components:
                c_val = c["value"]
                v_drop = total_current * c_val
                p_disp = (total_current ** 2) * c_val
                telemetry.append({
                    "id": c["id"],
                    "type": c["type"],
                    "resistance_ohms": round(c_val, 4),
                    "voltage_drop_volts": round(v_drop, 4),
                    "current_amps": round(total_current, 4),
                    "power_watts": round(p_disp, 4),
                })
        else:  # PARALLEL
            conductance_sum = 0.0
            has_zero_resistor = False
            for c in sanitized_components:
                c_val = c["value"]
                if c_val < 0.05:
                    has_zero_resistor = True
                    conductance_sum += 1.0 / 0.001
                else:
                    conductance_sum += 1.0 / c_val

            if has_zero_resistor or conductance_sum > 1000.0:
                is_short_circuit = True

            total_resistance = 1.0 / conductance_sum if conductance_sum > 0 else 0.001
            total_resistance = max(total_resistance, 0.001)
            total_current = source_voltage / total_resistance
            total_power = source_voltage * total_current

            telemetry = []
            for c in sanitized_components:
                c_val = max(c["value"], 0.001)
                i_branch = source_voltage / c_val
                p_branch = source_voltage * i_branch
                telemetry.append({
                    "id": c["id"],
                    "type": c["type"],
                    "resistance_ohms": round(c["value"], 4),
                    "voltage_drop_volts": round(source_voltage, 4),
                    "current_amps": round(i_branch, 4),
                    "power_watts": round(p_branch, 4),
                })

        return {
            "circuit_id": circuit_id,
            "source_voltage": round(source_voltage, 2),
            "configuration": config_upper,
            "total_resistance": round(total_resistance, 4),
            "total_current": round(total_current, 4),
            "total_power": round(total_power, 4),
            "component_telemetry": telemetry,
            "is_short_circuit_safe": not is_short_circuit,
            "execution_status": "WARNING_SHORT_CIRCUIT" if is_short_circuit else "SUCCESS",
        }

    def trace_optics_rays(
        self,
        lens_type: str = "CONVEX",
        focal_length_cm: float = 15.0,
        object_distance_cm: float = 30.0,
        object_height_cm: float = 5.0,
    ) -> Dict[str, Any]:
        """
        Calculates thin lens optical ray tracer using Gaussian lens equation:
        1/f = 1/v + 1/u => v = (f * u) / (u - f)
        Object distance u > 0 (placed to the left of the lens).
        Convex lens: f > 0
        Concave lens: f < 0
        """
        l_type = lens_type.strip().upper()
        if l_type not in ["CONVEX", "CONCAVE"]:
            l_type = "CONVEX"

        f = abs(focal_length_cm) if l_type == "CONVEX" else -abs(focal_length_cm)
        u = abs(object_distance_cm)
        h_o = float(object_height_cm)

        # Check if object is at focus for convex lens
        if l_type == "CONVEX" and abs(u - f) < 1e-4:
            return {
                "lens_type": l_type,
                "focal_length_cm": round(f, 2),
                "object_distance_cm": round(u, 2),
                "object_height_cm": round(h_o, 2),
                "image_distance_cm": None,
                "image_height_cm": None,
                "magnification": None,
                "image_nature": "AT_INFINITY",
                "ray_coordinates": {
                    "object_tip": [-u, h_o],
                    "lens_center": [0, 0],
                    "focus_right": [f, 0],
                    "focus_left": [-f, 0],
                    "ray1_lens_hit": [0, h_o],
                    "ray2_optical_center": [0, 0],
                },
                "is_at_focus": True,
            }

        # Thin lens formula: 1/v = 1/f - 1/u => v = (f * u) / (u - f)
        # Note: In Cartesian coordinates where object is at -u:
        # 1/v - 1/(-u) = 1/f => 1/v + 1/u = 1/f => 1/v = 1/f - 1/u
        v = (f * u) / (u - f)
        m = -v / u
        h_i = m * h_o

        if l_type == "CONVEX":
            if u > f:
                nature = "REAL_INVERTED"
            else:
                nature = "VIRTUAL_UPRIGHT"
        else:
            nature = "VIRTUAL_UPRIGHT"

        return {
            "lens_type": l_type,
            "focal_length_cm": round(f, 2),
            "object_distance_cm": round(u, 2),
            "object_height_cm": round(h_o, 2),
            "image_distance_cm": round(v, 3),
            "image_height_cm": round(h_i, 3),
            "magnification": round(m, 3),
            "image_nature": nature,
            "ray_coordinates": {
                "object_tip": [-u, h_o],
                "image_tip": [round(v, 2), round(h_i, 2)],
                "lens_center": [0, 0],
                "focus_right": [round(f, 2), 0],
                "focus_left": [round(-f, 2), 0],
                "ray1_lens_hit": [0, h_o],
                "ray2_optical_center": [0, 0],
            },
            "is_at_focus": False,
        }

    def simulate_acid_base_titration(
        self,
        analyte: str = "HCl",
        titrant: str = "NaOH",
        analyte_volume_ml: float = 25.0,
        analyte_molarity: float = 0.1,
        titrant_molarity: float = 0.1,
        indicator: str = "PHENOLPHTHALEIN",
    ) -> Dict[str, Any]:
        """
        Calculates analytical strong acid - strong base titration curve and indicator color transition.
        Equivalence volume: V_eq = (M_a * V_a) / M_b
        """
        ind = indicator.strip().upper()
        if ind not in ["PHENOLPHTHALEIN", "METHYL_ORANGE"]:
            ind = "PHENOLPHTHALEIN"

        v_a = max(analyte_volume_ml, 1.0)
        m_a = max(analyte_molarity, 0.001)
        m_b = max(titrant_molarity, 0.001)

        v_eq = (m_a * v_a) / m_b
        max_v = round(v_eq * 2.0, 1)

        # Generate 21 sample volume points from 0 to 2*v_eq
        step = max_v / 20.0
        curve = []

        initial_ph = round(-math.log10(m_a), 2)

        for i in range(21):
            v_b = round(i * step, 2)
            if v_b < v_eq - 0.01:
                # Excess Acid
                mol_acid_left = (m_a * v_a) - (m_b * v_b)
                total_vol = v_a + v_b
                conc_h = mol_acid_left / total_vol
                ph = -math.log10(max(conc_h, 1e-14))
            elif abs(v_b - v_eq) <= 0.01:
                # Equivalence Point
                ph = 7.0
            else:
                # Excess Base
                mol_base_excess = (m_b * v_b) - (m_a * v_a)
                total_vol = v_a + v_b
                conc_oh = mol_base_excess / total_vol
                poh = -math.log10(max(conc_oh, 1e-14))
                ph = 14.0 - poh

            ph = min(max(ph, 0.0), 14.0)

            # Chromophoric color calculation
            if ind == "PHENOLPHTHALEIN":
                if ph < 8.2:
                    color = "COLORLESS"
                elif ph <= 10.0:
                    color = "FAINT_PINK"
                else:
                    color = "MAGENTA_PINK"
            else:  # METHYL_ORANGE
                if ph < 3.1:
                    color = "RED"
                elif ph <= 4.4:
                    color = "ORANGE"
                else:
                    color = "YELLOW"

            curve.append({
                "volume_added_ml": round(v_b, 2),
                "ph": round(ph, 2),
                "color_state": color,
            })

        final_ph = curve[-1]["ph"]

        return {
            "analyte": analyte,
            "titrant": titrant,
            "equivalence_volume_ml": round(v_eq, 2),
            "equivalence_ph": 7.0,
            "indicator": ind,
            "titration_curve": curve,
            "initial_ph": initial_ph,
            "final_ph": final_ph,
            "status": "COMPLETED",
        }

    def generate_lab_report(
        self,
        lab_type: str,
        student_id: str,
        experimental_value: float,
        theoretical_value: float,
        observations: str = "",
    ) -> Dict[str, Any]:
        """
        Synthesizes automated scientific laboratory reports with calculated relative percentage error.
        """
        if theoretical_value == 0:
            rel_error_pct = 0.0
        else:
            rel_error_pct = abs((experimental_value - theoretical_value) / theoretical_value) * 100.0

        report_id = f"RPT-{uuid.uuid4().hex[:8].upper()}"
        now_iso = datetime.now(timezone.utc).isoformat()

        # Generate cryptographic verification stamp
        raw_stamp = f"{report_id}:{student_id}:{lab_type}:{rel_error_pct:.2f}:{now_iso}"
        verif_hash = hashlib.sha256(raw_stamp.encode()).hexdigest()[:16].upper()

        if rel_error_pct <= 5.0:
            eval_note = "High experimental precision within acceptable national science standards (<5% margin)."
        elif rel_error_pct <= 15.0:
            eval_note = "Moderate experimental deviation (5%-15% margin); calibration recommended."
        else:
            eval_note = "Significant deviation (>15% margin); environmental apparatus leakage or parallax error suspected."

        conclusion = (
            f"Experimental result: {experimental_value} vs Theoretical baseline: {theoretical_value}. "
            f"Calculated relative discrepancy: {rel_error_pct:.2f}%. {eval_note}"
        )
        if observations:
            conclusion += f" Student Observation Note: {observations}"

        return {
            "report_id": report_id,
            "lab_type": lab_type,
            "student_id": student_id,
            "experimental_value": round(experimental_value, 4),
            "theoretical_value": round(theoretical_value, 4),
            "relative_error_pct": round(rel_error_pct, 2),
            "conclusion": conclusion,
            "verification_stamp": f"AGR-LAB-{verif_hash}",
            "generated_at": now_iso,
        }


virtual_science_lab_service = VirtualScienceLabService()
