"""
Atmospheric Climate Dynamics Service
====================================
Planetary energy balance, Arrhenius greenhouse gas radiative forcing,
Stefan-Boltzmann radiation equilibrium, and climate sensitivity analysis.

Mathematical Foundation:
- Solar Constant: S_0 ~ 1361 W/m^2
- Earth Energy Invariant: (S_0 * (1 - albedo)) / 4 = epsilon * sigma * T^4
- Stefan-Boltzmann Constant: sigma = 5.670374419e-8 W/(m^2 K^4)
- Arrhenius Radiative Forcing: Delta F = alpha * ln(C / C_0) where alpha ~ 5.35 W/m^2
- Equilibrium Climate Sensitivity: Delta T_eq = lambda_c * Delta F where lambda_c ~ 0.8 K/(W/m^2)

Zero external dependencies — pure Python standard library.
"""

import math
from typing import Any, Dict


class AtmosphericClimateModelingService:
    """Enterprise planetary climate dynamics and atmospheric simulation engine."""

    SOLAR_CONSTANT_S0 = 1361.0            # W/m^2 (Top of atmosphere solar irradiance)
    STEFAN_BOLTZMANN_SIGMA = 5.670374e-8  # W/(m^2 K^4)
    PRE_INDUSTRIAL_CO2_PPM = 280.0        # Reference pre-industrial baseline (ppm)
    ARRHENIUS_ALPHA = 5.35                # W/m^2 coefficient for CO2 forcing
    CLIMATE_SENSITIVITY_PARAM = 0.8       # K per (W/m^2) feedback factor

    @staticmethod
    def calculate_radiative_forcing(
        co2_concentration_ppm: float,
        ch4_concentration_ppb: float = 1900.0,
        n2o_concentration_ppb: float = 335.0,
        baseline_co2_ppm: float = 280.0,
    ) -> Dict[str, Any]:
        """
        Calculate instantaneous greenhouse radiative forcing:
        Delta F_CO2 = 5.35 * ln(C / C_0)
        """
        c = max(1.0, float(co2_concentration_ppm))
        c0 = max(1.0, float(baseline_co2_ppm))

        # Arrhenius logarithmic relation
        delta_f_co2 = AtmosphericClimateModelingService.ARRHENIUS_ALPHA * math.log(c / c0)

        # Simplified methane and nitrous oxide contributions
        delta_f_ch4 = 0.036 * (math.sqrt(max(1.0, ch4_concentration_ppb)) - math.sqrt(700.0))
        delta_f_n2o = 0.12 * (math.sqrt(max(1.0, n2o_concentration_ppb)) - math.sqrt(270.0))

        total_forcing = delta_f_co2 + max(0.0, delta_f_ch4) + max(0.0, delta_f_n2o)

        # Expected equilibrium temperature anomaly: Delta T = lambda * Delta F
        temp_anomaly_celsius = AtmosphericClimateModelingService.CLIMATE_SENSITIVITY_PARAM * total_forcing

        return {
            "co2_concentration_ppm": c,
            "baseline_co2_ppm": c0,
            "forcing_co2_w_m2": round(delta_f_co2, 3),
            "forcing_ch4_w_m2": round(max(0.0, delta_f_ch4), 3),
            "forcing_n2o_w_m2": round(max(0.0, delta_f_n2o), 3),
            "total_radiative_forcing_w_m2": round(total_forcing, 3),
            "equilibrium_warming_celsius": round(temp_anomaly_celsius, 2),
            "doubling_co2_warming_celsius": round(
                AtmosphericClimateModelingService.CLIMATE_SENSITIVITY_PARAM * AtmosphericClimateModelingService.ARRHENIUS_ALPHA * math.log(2.0),
                2
            ),
        }

    @staticmethod
    def solve_planetary_energy_balance(
        planetary_albedo: float = 0.30,
        effective_emissivity: float = 0.612,
        solar_irradiance: float = 1361.0,
        greenhouse_forcing_delta_f: float = 0.0,
    ) -> Dict[str, Any]:
        """
        Solve Stefan-Boltzmann planetary energy equilibrium:
        F_in = (S_0 * (1 - albedo)) / 4
        F_out = epsilon * sigma * T_surface^4 - Delta F
        => T_surface = ((F_in + Delta F) / (epsilon * sigma))^(1/4)
        """
        albedo = max(0.0, min(0.99, float(planetary_albedo)))
        eps = max(0.1, min(1.0, float(effective_emissivity)))
        s0 = max(100.0, float(solar_irradiance))
        df = float(greenhouse_forcing_delta_f)
        sigma = AtmosphericClimateModelingService.STEFAN_BOLTZMANN_SIGMA

        absorbed_solar_flux = (s0 * (1.0 - albedo)) / 4.0
        total_effective_flux = max(1.0, absorbed_solar_flux + df)

        # Bare rock equilibrium temperature (no greenhouse effect, eps=1)
        t_bare_rock_k = (absorbed_solar_flux / sigma) ** 0.25

        # Surface temperature with atmospheric greenhouse blanket
        t_surface_k = (total_effective_flux / (eps * sigma)) ** 0.25
        t_surface_c = t_surface_k - 273.15

        return {
            "planetary_albedo": albedo,
            "effective_emissivity": eps,
            "incident_solar_flux_w_m2": round(absorbed_solar_flux, 2),
            "total_effective_flux_w_m2": round(total_effective_flux, 2),
            "bare_rock_temp_kelvin": round(t_bare_rock_k, 2),
            "bare_rock_temp_celsius": round(t_bare_rock_k - 273.15, 2),
            "surface_temp_kelvin": round(t_surface_k, 2),
            "surface_temp_celsius": round(t_surface_c, 2),
            "natural_greenhouse_effect_k": round(t_surface_k - t_bare_rock_k, 2),
        }
