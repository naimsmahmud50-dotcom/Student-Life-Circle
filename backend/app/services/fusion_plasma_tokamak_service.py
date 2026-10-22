"""
Fusion Plasma Tokamak Physics Service
======================================
Magnetohydrodynamic (MHD) plasma confinement modeling, Lawson criterion
triple product evaluation, tokamak safety factor (Kruskal-Shafranov limit),
and fusion power gain Q-factor estimation.

Mathematical Foundation:
- Lawson Criterion: Triple Product n * tau_E * T >= 3.0e21 keV s m^-3 (D-T ignition)
- Kinetic Pressure: p = 2 * n * k_B * T
- Magnetic Beta: beta = (2 * mu_0 * p) / B^2
- Safety Factor: q(r) = (r * B_toroidal) / (R_major * B_poloidal)
- Kruskal-Shafranov Limit: q_edge > 2.0 (kink instability suppression)
- Fusion Gain Factor: Q = P_fusion / P_external_heating (Q >= 1 breakeven, Q >= 10 burning)

Zero external dependencies — pure Python standard library.
"""

import math
from typing import Any, Dict


class FusionPlasmaTokamakService:
    """Enterprise tokamak plasma physics and thermonuclear fusion engine."""

    MU_0 = 4.0 * math.pi * 1e-7         # Vacuum permeability (H/m)
    BOLTZMANN_K_EV = 8.617333262e-5     # eV / Kelvin
    LAWSON_IGNITION_TRIPLE_PRODUCT = 3.0e21  # m^-3 * s * keV (D-T ignition threshold)
    BREAKEVEN_TRIPLE_PRODUCT = 5.0e20        # m^-3 * s * keV (Q = 1 breakeven)

    @staticmethod
    def evaluate_lawson_criterion(
        plasma_density_m3: float,
        energy_confinement_time_s: float,
        plasma_temperature_kev: float,
        external_heating_power_mw: float = 50.0,
    ) -> Dict[str, Any]:
        """
        Evaluate thermonuclear fusion ignition viability via the Lawson Triple Product:
        LTP = n * tau_E * T
        """
        n = max(1e18, float(plasma_density_m3))
        tau = max(0.01, float(energy_confinement_time_s))
        t_kev = max(0.1, float(plasma_temperature_kev))
        p_ext = max(0.1, float(external_heating_power_mw))

        # Triple product: n * tau_E * T (keV s m^-3)
        triple_product = n * tau * t_kev

        # Fusion gain factor Q estimation
        # Empirical scaling: Q ~ 5 * (LTP / 5e20)^1.5 when below ignition
        if triple_product >= FusionPlasmaTokamakService.LAWSON_IGNITION_TRIPLE_PRODUCT:
            fusion_gain_q = 999.0  # Self-sustaining ignition
            regime = "SELF_SUSTAINING_IGNITION"
        elif triple_product >= FusionPlasmaTokamakService.BREAKEVEN_TRIPLE_PRODUCT:
            ratio = triple_product / FusionPlasmaTokamakService.BREAKEVEN_TRIPLE_PRODUCT
            fusion_gain_q = min(50.0, 1.0 + 9.0 * (ratio ** 1.8))
            regime = "BURNING_PLASMA" if fusion_gain_q >= 10.0 else "SCIENTIFIC_BREAKEVEN"
        else:
            ratio = triple_product / FusionPlasmaTokamakService.BREAKEVEN_TRIPLE_PRODUCT
            fusion_gain_q = max(0.01, ratio ** 1.5)
            regime = "SUB_BREAKEVEN"

        # Estimated fusion power output in MW
        fusion_power_mw = p_ext * fusion_gain_q if fusion_gain_q < 999.0 else 500.0

        fraction_of_ignition = min(1.0, triple_product / FusionPlasmaTokamakService.LAWSON_IGNITION_TRIPLE_PRODUCT)

        return {
            "plasma_density_m3": n,
            "energy_confinement_time_s": tau,
            "plasma_temperature_kev": t_kev,
            "triple_product_kev_s_m3": triple_product,
            "ignition_threshold_target": FusionPlasmaTokamakService.LAWSON_IGNITION_TRIPLE_PRODUCT,
            "fraction_of_ignition_pct": round(fraction_of_ignition * 100.0, 2),
            "fusion_gain_factor_q": round(fusion_gain_q, 2),
            "external_heating_mw": p_ext,
            "estimated_fusion_power_mw": round(fusion_power_mw, 2),
            "plasma_regime": regime,
            "ignition_achieved": regime == "SELF_SUSTAINING_IGNITION",
        }

    @staticmethod
    def calculate_tokamak_mhd_stability(
        major_radius_r_m: float,
        minor_radius_a_m: float,
        toroidal_field_bt_tesla: float,
        plasma_current_ip_ma: float,
        plasma_density_m3: float = 1.0e20,
        plasma_temperature_kev: float = 15.0,
        elongation_kappa: float = 1.7,
    ) -> Dict[str, Any]:
        """
        Calculate magnetic confinement efficiency (Beta) and edge safety factor q(a)
        to prevent disruptive MHD kink instabilities (Kruskal-Shafranov limit).
        """
        r_major = max(0.5, float(major_radius_r_m))
        r_minor = max(0.1, float(minor_radius_a_m))
        b_t = max(0.1, float(toroidal_field_bt_tesla))
        i_p = max(0.01, float(plasma_current_ip_ma))  # in Mega-Amperes (MA)
        kappa = max(1.0, float(elongation_kappa))

        # Aspect ratio A = R / a
        aspect_ratio = r_major / r_minor

        # Poloidal magnetic field at edge: B_p ~ (mu_0 * I_p) / (2 * pi * a)
        i_p_amps = i_p * 1e6
        b_p = (FusionPlasmaTokamakService.MU_0 * i_p_amps) / (2.0 * math.pi * r_minor)

        # Cylindrical safety factor with D-shape elongation: q_edge = q_cyl * (1 + kappa^2)/2
        q_cyl = (r_minor * b_t) / (r_major * max(1e-6, b_p))
        q_edge = q_cyl * ((1.0 + kappa * kappa) / 2.0)

        # Kinetic pressure: p = 2 * n * k_B * T (converting keV to Joules: 1 keV = 1.60218e-16 J)
        n = max(1e18, float(plasma_density_m3))
        t_joules = max(0.1, float(plasma_temperature_kev)) * 1.602176634e-16
        kinetic_pressure_pa = 2.0 * n * t_joules

        # Magnetic pressure: p_mag = B^2 / (2 * mu_0)
        magnetic_pressure_pa = (b_t ** 2) / (2.0 * FusionPlasmaTokamakService.MU_0)

        # Total beta: beta = p / p_mag
        beta_total = kinetic_pressure_pa / max(1e-6, magnetic_pressure_pa)
        beta_pct = beta_total * 100.0

        # Troyon beta limit: beta_N ~ 2.8 * (I_p / (a * B_t))
        troyon_normalized_beta = beta_pct / (i_p / (r_minor * b_t)) if (r_minor * b_t) > 0 else 0.0

        # Kruskal-Shafranov stability: q_edge must be > 2.0
        is_mhd_stable = q_edge >= 2.0 and troyon_normalized_beta <= 3.5

        return {
            "major_radius_m": r_major,
            "minor_radius_m": r_minor,
            "aspect_ratio": round(aspect_ratio, 2),
            "toroidal_field_tesla": b_t,
            "poloidal_field_tesla": round(b_p, 4),
            "safety_factor_q_edge": round(q_edge, 3),
            "kruskal_shafranov_limit": 2.0,
            "kinetic_pressure_kpa": round(kinetic_pressure_pa / 1000.0, 2),
            "magnetic_pressure_mpa": round(magnetic_pressure_pa / 1e6, 2),
            "plasma_beta_pct": round(beta_pct, 3),
            "troyon_normalized_beta": round(troyon_normalized_beta, 2),
            "is_mhd_stable": is_mhd_stable,
            "instability_risk": "NONE (STABLE)" if is_mhd_stable else ("KINK_INSTABILITY_RISK" if q_edge < 2.0 else "BALLOONING_BETA_LIMIT_EXCEEDED"),
        }
