"""
Interactive Semiconductor Physics & Quantum Mechanics Sandbox Service
Calculates PN junction depletion dynamics, built-in potential, electric field profiles,
and 1D Quantum Well discrete eigen-energies and wavefunctions.
"""

import math
from typing import Dict, List, Any


# Physical Constants in SI / Semiconductor Units
Q_E = 1.602176634e-19       # Elementary charge (C)
K_B = 1.380649e-23          # Boltzmann constant (J/K)
EPSILON_0_CM = 8.8541878e-14 # Vacuum permittivity (F/cm)
EPSILON_0_M = 8.8541878e-12  # Vacuum permittivity (F/m)
H_PLANCK = 6.62607015e-34    # Planck constant (J*s)
M_ELECTRON_0 = 9.1093837e-31 # Electron rest mass (kg)
C_LIGHT = 2.99792458e8       # Speed of light (m/s)

MATERIAL_CONSTANTS = {
    "SILICON": {
        "eps_r": 11.7,
        "n_i_300": 1.5e10,  # cm^-3
        "bandgap_300": 1.12 # eV
    },
    "GERMANIUM": {
        "eps_r": 16.0,
        "n_i_300": 2.4e13,
        "bandgap_300": 0.66
    },
    "GALLIUM_ARSENIDE": {
        "eps_r": 12.9,
        "n_i_300": 2.1e6,
        "bandgap_300": 1.42
    }
}


class SemiconductorQuantumSandboxService:
    """Enterprise semiconductor band structure and quantum wave solver."""

    def simulate_pn_junction(
        self,
        semiconductor_material: str = "SILICON",
        acceptor_doping_na_cm3: float = 1e16,
        donor_doping_nd_cm3: float = 1e16,
        reverse_bias_voltage_v: float = 0.0,
        temperature_kelvin: float = 300.0
    ) -> Dict[str, Any]:
        """
        Simulates abrupt PN junction depletion region dynamics, avoiding all singularities.
        """
        mat_key = semiconductor_material.upper().strip()
        if mat_key not in MATERIAL_CONSTANTS:
            mat_key = "SILICON"

        mat = MATERIAL_CONSTANTS[mat_key]
        t_k = max(100.0, min(float(temperature_kelvin), 600.0))
        n_a = max(1e13, min(float(acceptor_doping_na_cm3), 1e20))
        n_d = max(1e13, min(float(donor_doping_nd_cm3), 1e20))
        v_r = max(0.0, min(float(reverse_bias_voltage_v), 100.0))

        v_thermal = (K_B * t_k) / Q_E
        n_i = mat["n_i_300"] * ((t_k / 300.0) ** 1.5)

        # Built-in Potential V_bi
        v_bi = v_thermal * math.log((n_a * n_d) / (n_i ** 2))
        v_bi = max(0.1, min(v_bi, mat["bandgap_300"]))

        v_total = v_bi + v_r
        eps_s = mat["eps_r"] * EPSILON_0_CM

        # Depletion Width W (cm) -> convert to micrometers (um)
        w_cm = math.sqrt((2.0 * eps_s / Q_E) * ((1.0 / n_a) + (1.0 / n_d)) * v_total)
        w_um = w_cm * 1e4

        x_p_cm = w_cm * (n_d / (n_a + n_d))
        x_n_cm = w_cm * (n_a / (n_a + n_d))

        x_p_um = x_p_cm * 1e4
        x_n_um = x_n_cm * 1e4

        # Peak Electric Field E_max (V/cm) -> convert to kV/cm
        e_max_v_cm = (2.0 * v_total) / w_cm
        e_max_kv_cm = e_max_v_cm / 1e3

        # Junction Capacitance C_j (F/cm^2) -> convert to pF/cm^2
        c_j_f_cm2 = eps_s / w_cm
        c_j_pf_cm2 = c_j_f_cm2 * 1e12

        # Generate spatial electric field profile
        profile = []
        num_points = 21
        step = w_um / (num_points - 1)
        for i in range(num_points):
            x = -x_p_um + (i * step)
            if x < 0:
                # In P-side: linear rise from 0 at -x_p to -E_max at 0
                field = -e_max_kv_cm * ((x + x_p_um) / max(0.001, x_p_um))
            else:
                # In N-side: linear decay from -E_max at 0 to 0 at +x_n
                field = -e_max_kv_cm * ((x_n_um - x) / max(0.001, x_n_um))
            profile.append({"position_um": round(x, 4), "electric_field_kv_cm": round(field, 2)})

        return {
            "material": mat_key,
            "built_in_potential_v": round(v_bi, 3),
            "depletion_width_um": round(w_um, 3),
            "x_p_depletion_um": round(x_p_um, 3),
            "x_n_depletion_um": round(x_n_um, 3),
            "peak_electric_field_kv_cm": round(e_max_kv_cm, 2),
            "junction_capacitance_pf_cm2": round(c_j_pf_cm2, 2),
            "bandgap_ev": mat["bandgap_300"],
            "spatial_electric_field_profile": profile
        }

    def simulate_quantum_well(
        self,
        well_width_nm: float = 5.0,
        particle_mass_ratio: float = 0.067,
        state_levels: int = 3
    ) -> Dict[str, Any]:
        """
        Solves 1D infinite/finite quantum well eigen-energies and wavefunction modes.
        """
        l_nm = max(0.5, min(float(well_width_nm), 100.0))
        l_m = l_nm * 1e-9
        m_ratio = max(0.01, min(float(particle_mass_ratio), 10.0))
        m_eff = m_ratio * M_ELECTRON_0
        n_states = max(1, min(int(state_levels), 5))

        # E_1 = h^2 / (8 * m * L^2)
        e_1_joules = (H_PLANCK ** 2) / (8.0 * m_eff * (l_m ** 2))
        e_1_ev = e_1_joules / Q_E

        energy_levels = []
        for n in range(1, n_states + 1):
            e_n_ev = (n ** 2) * e_1_ev
            # Transition wavelength to next level (if applicable)
            if n > 1:
                delta_e_j = (e_n_ev - ((n - 1) ** 2 * e_1_ev)) * Q_E
                wl_nm = ((H_PLANCK * C_LIGHT) / delta_e_j) * 1e9 if delta_e_j > 0 else 0.0
            else:
                wl_nm = 0.0

            energy_levels.append({
                "level_n": n,
                "energy_ev": round(e_n_ev, 4),
                "wavelength_nm": round(wl_nm, 2)
            })

        # Generate Wavefunction psi_1(x), psi_2(x) spatial profiles across well
        wave_samples = []
        pts = 25
        for i in range(pts):
            x = (i / (pts - 1)) * l_nm
            psi_1 = math.sin(1 * math.pi * (x / l_nm))
            psi_2 = math.sin(2 * math.pi * (x / l_nm))
            wave_samples.append({
                "x_nm": round(x, 2),
                "psi_1": round(psi_1, 4),
                "prob_density_1": round(psi_1 ** 2, 4),
                "psi_2": round(psi_2, 4),
                "prob_density_2": round(psi_2 ** 2, 4)
            })

        return {
            "well_width_nm": l_nm,
            "effective_mass_kg": m_eff,
            "energy_levels": energy_levels,
            "wavefunction_samples": wave_samples
        }


# Export singleton instance
semiconductor_quantum_sandbox_service = SemiconductorQuantumSandboxService()
