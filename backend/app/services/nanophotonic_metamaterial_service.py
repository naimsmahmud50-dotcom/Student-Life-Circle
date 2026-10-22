"""
Nanophotonics Metamaterial Simulation Service
=============================================
Drude-Lorentz electromagnetic dispersion modeling, double-negative (DNG)
left-handed metamaterials, Veselago superlens evanescent amplification,
and negative Snell's Law refraction.

Mathematical Foundation:
- Drude Permittivity: Re(epsilon) = 1 - omega_p^2 / (omega^2 + gamma_e^2)
- Lorentz Permeability: Re(mu) = 1 - (F * omega^2 * (omega^2 - omega_0^2)) / ((omega^2 - omega_0^2)^2 + (gamma_m * omega)^2)
- Double-Negative (DNG) Condition: Re(epsilon) < 0 and Re(mu) < 0
  => Refractive Index n = -sqrt(|Re(epsilon)| * |Re(mu)|)
- Negative Snell's Law: n_1 * sin(theta_1) = n_2 * sin(theta_2)
- Evanescent Wave Factor: T = exp(|k_z| * d) where k_z = sqrt(k_x^2 - k_0^2)

Zero external dependencies — pure Python standard library.
"""

import math
from typing import Any, Dict


class NanophotonicMetamaterialService:
    """Enterprise nanophotonics and metamaterial optics simulation engine."""

    SPEED_OF_LIGHT = 299792458.0  # m/s

    @staticmethod
    def calculate_optical_dispersion(
        frequency_thz: float,
        plasma_frequency_thz: float = 120.0,
        resonance_frequency_thz: float = 100.0,
        electron_damping_thz: float = 2.0,
        magnetic_damping_thz: float = 3.0,
        magnetic_oscillator_strength: float = 0.55,
    ) -> Dict[str, Any]:
        """
        Calculate effective permittivity epsilon(omega), permeability mu(omega),
        and refractive index n(omega) across Drude-Lorentz metamaterial structures.
        """
        w = max(0.1, float(frequency_thz))
        w_p = max(0.1, float(plasma_frequency_thz))
        w_0 = max(0.1, float(resonance_frequency_thz))
        g_e = max(0.01, float(electron_damping_thz))
        g_m = max(0.01, float(magnetic_damping_thz))
        f_mag = max(0.0, min(1.0, float(magnetic_oscillator_strength)))

        # 1. Drude electrical permittivity: Re(epsilon)
        denom_e = (w ** 2) + (g_e ** 2)
        re_eps = 1.0 - (w_p ** 2) / denom_e

        # 2. Lorentz magnetic permeability: Re(mu)
        w_diff = (w ** 2) - (w_0 ** 2)
        denom_m = (w_diff ** 2) + ((g_m * w) ** 2)
        re_mu = 1.0 - (f_mag * (w ** 2) * w_diff) / max(1e-6, denom_m)

        # 3. Refractive index evaluation
        is_dng = (re_eps < 0.0) and (re_mu < 0.0)
        is_plasmonic = (re_eps < 0.0) and (re_mu > 0.0)
        is_magnetic = (re_eps > 0.0) and (re_mu < 0.0)

        if is_dng:
            # Veselago negative index of refraction
            n_eff = -math.sqrt(abs(re_eps) * abs(re_mu))
            medium_regime = "LEFT_HANDED_METAMATERIAL_DNG"
        elif is_plasmonic:
            n_eff = 0.0  # Evanescent / opaque
            medium_regime = "PLASMONIC_OPAQUE_EPSILON_NEGATIVE"
        elif is_magnetic:
            n_eff = 0.0  # Magnetic opaque
            medium_regime = "MAGNETIC_OPAQUE_MU_NEGATIVE"
        else:
            n_eff = math.sqrt(max(0.01, re_eps * re_mu))
            medium_regime = "CONVENTIONAL_DIELECTRIC_RIGHT_HANDED"

        return {
            "frequency_thz": w,
            "permittivity_re_eps": round(re_eps, 4),
            "permeability_re_mu": round(re_mu, 4),
            "refractive_index_n": round(n_eff, 4),
            "is_negative_index": is_dng,
            "medium_classification": medium_regime,
            "impedance_eta": round(math.sqrt(abs(re_mu) / max(1e-4, abs(re_eps))), 4),
        }

    @staticmethod
    def simulate_negative_refraction_ray(
        incident_angle_deg: float,
        n1_incident: float = 1.0,
        n2_metamaterial: float = -1.5,
        slab_thickness_nm: float = 150.0,
        wavelength_nm: float = 632.8,
    ) -> Dict[str, Any]:
        """
        Simulate refraction angle across metamaterial interface using generalized Snell's Law
        and compute Veselago superlens sub-wavelength focus position.
        """
        theta_1_deg = max(0.0, min(89.0, float(incident_angle_deg)))
        theta_1_rad = math.radians(theta_1_deg)
        n1 = float(n1_incident)
        n2 = float(n2_metamaterial)
        d_nm = max(10.0, float(slab_thickness_nm))
        lambda_nm = max(100.0, float(wavelength_nm))

        # Snell's Law: sin(theta_2) = (n1 / n2) * sin(theta_1)
        sin_theta_1 = math.sin(theta_1_rad)
        sin_theta_2 = (n1 / n2) * sin_theta_1 if abs(n2) > 1e-4 else 0.0

        is_tir = abs(sin_theta_2) > 1.0  # Total Internal Reflection

        if is_tir:
            refraction_angle_deg = 0.0
            lateral_shift_nm = 0.0
        else:
            # Preserve negative sign when n2 is negative
            if n2 < 0.0:
                refraction_angle_rad = -math.asin(abs(sin_theta_2))
            else:
                refraction_angle_rad = math.asin(sin_theta_2)

            refraction_angle_deg = math.degrees(refraction_angle_rad)
            # Lateral ray displacement through slab: Delta x = d * tan(theta_2)
            lateral_shift_nm = d_nm * math.tan(refraction_angle_rad)

        # Evanescent wave amplification factor for high-k components (sub-wavelength resolution)
        k0 = 2.0 * math.pi / lambda_nm
        kx_sub = 2.0 * k0  # Sub-wavelength spatial frequency
        kz_sub = math.sqrt(max(0.0, kx_sub ** 2 - k0 ** 2))
        evanescent_amplification = math.exp(min(20.0, kz_sub * d_nm))

        return {
            "incident_angle_deg": theta_1_deg,
            "refraction_angle_deg": round(refraction_angle_deg, 2),
            "refractive_index_n1": n1,
            "refractive_index_n2": n2,
            "slab_thickness_nm": d_nm,
            "lateral_shift_nm": round(lateral_shift_nm, 2),
            "total_internal_reflection": is_tir,
            "is_negative_refraction": refraction_angle_deg < 0.0,
            "evanescent_amplification_gain": round(evanescent_amplification, 2),
            "sub_diffraction_resolution_nm": round(lambda_nm / (2.0 * max(1.0, abs(n2))), 1),
        }
