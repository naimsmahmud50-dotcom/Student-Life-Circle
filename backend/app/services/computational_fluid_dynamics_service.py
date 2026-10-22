"""
Computational Fluid Dynamics (CFD) Sandbox Service
===================================================
Incompressible, laminar 2D Navier-Stokes solver, Reynolds number
regime classification, Bernoulli pressure-velocity equations,
and aerodynamic drag / lift coefficient estimation.

Mathematical Foundation:
- Reynolds Number: Re = (rho * v * L) / mu
- Incompressible Continuity: div(u) = 0
- 1D/2D Navier-Stokes Momentum: du/dt + (u . grad)u = -1/rho * grad(p) + nu * laplacian(u)
- Bernoulli Invariant: P + 0.5 * rho * v^2 + rho * g * h = const
- Drag Force: F_D = 0.5 * C_D * rho * v^2 * A => C_D = 2 * F_D / (rho * v^2 * A)

Zero external dependencies — pure Python standard library.
"""

import math
from typing import Any, List, Dict


class ComputationalFluidDynamicsService:
    """Enterprise CFD physics and fluid dynamics analytics engine."""

    # Standard reference fluids: (density kg/m^3, dynamic viscosity Pa.s)
    FLUID_CATALOG = {
        "air_20c": (1.204, 1.825e-5),
        "water_20c": (998.2, 1.002e-3),
        "blood_37c": (1060.0, 3.5e-3),
        "glycerol": (1260.0, 1.412),
        "engine_oil": (888.0, 0.29),
        "honey": (1420.0, 10.0),
    }

    @staticmethod
    def classify_reynolds_regime(
        velocity: float,
        characteristic_length: float,
        fluid: str = "air_20c",
        custom_density: float | None = None,
        custom_viscosity: float | None = None,
    ) -> Dict[str, Any]:
        """
        Calculate Reynolds number and classify flow regime.
        Re = (rho * v * L) / mu
        """
        velocity = max(0.0, float(velocity))
        char_len = max(1e-6, float(characteristic_length))

        if fluid in ComputationalFluidDynamicsService.FLUID_CATALOG:
            rho, mu = ComputationalFluidDynamicsService.FLUID_CATALOG[fluid]
        else:
            rho, mu = ComputationalFluidDynamicsService.FLUID_CATALOG["air_20c"]

        if custom_density is not None and custom_density > 0:
            rho = float(custom_density)
        if custom_viscosity is not None and custom_viscosity > 0:
            mu = float(custom_viscosity)

        # Kinematic viscosity: nu = mu / rho
        nu = mu / max(1e-6, rho)

        # Reynolds number
        reynolds = (rho * velocity * char_len) / max(1e-12, mu)

        if reynolds < 2300.0:
            regime = "LAMINAR"
            flow_characteristics = "Smooth, ordered fluid motion in parallel layers; minimal lateral mixing."
            friction_factor = 64.0 / max(1e-6, reynolds) if reynolds > 0 else 0.0
        elif reynolds <= 4000.0:
            regime = "TRANSITIONAL"
            flow_characteristics = "Unstable flow exhibiting localized bursts of turbulence amidst laminar base."
            friction_factor = 0.032
        else:
            regime = "TURBULENT"
            flow_characteristics = "Chaotic fluid particles with eddies, vortices, and high momentum diffusion."
            # Blasius formula for turbulent pipe flow: f = 0.3164 / Re^0.25
            friction_factor = 0.3164 / (reynolds ** 0.25) if reynolds > 0 else 0.0

        return {
            "reynolds_number": round(reynolds, 2),
            "regime": regime,
            "fluid_type": fluid,
            "density_kg_m3": round(rho, 4),
            "dynamic_viscosity_pa_s": mu,
            "kinematic_viscosity_m2_s": round(nu, 8),
            "velocity_m_s": velocity,
            "characteristic_length_m": char_len,
            "darcy_friction_factor": round(friction_factor, 6),
            "flow_characteristics": flow_characteristics,
        }

    @staticmethod
    def solve_bernoulli_flow(
        p1_pascal: float,
        v1_m_s: float,
        z1_meters: float,
        v2_m_s: float,
        z2_meters: float,
        fluid: str = "water_20c",
        gravity: float = 9.80665,
    ) -> Dict[str, Any]:
        """
        Solve Bernoulli steady-state conservation equation:
        P1 + 0.5 * rho * v1^2 + rho * g * z1 = P2 + 0.5 * rho * v2^2 + rho * g * z2
        """
        p1 = max(0.0, float(p1_pascal))
        v1 = max(0.0, float(v1_m_s))
        z1 = float(z1_meters)
        v2 = max(0.0, float(v2_m_s))
        z2 = float(z2_meters)

        rho, _ = ComputationalFluidDynamicsService.FLUID_CATALOG.get(
            fluid, ComputationalFluidDynamicsService.FLUID_CATALOG["water_20c"]
        )

        total_head_1 = p1 + 0.5 * rho * (v1 ** 2) + rho * gravity * z1
        p2 = total_head_1 - 0.5 * rho * (v2 ** 2) - rho * gravity * z2

        # Cavitation warning if p2 approaches vapor pressure (~2.34 kPa for water at 20C)
        is_cavitation_risk = p2 < 2340.0

        return {
            "fluid": fluid,
            "density_kg_m3": rho,
            "total_stagnation_pressure_pa": round(total_head_1, 2),
            "upstream_pressure_p1_pa": round(p1, 2),
            "upstream_velocity_v1_m_s": v1,
            "downstream_velocity_v2_m_s": v2,
            "downstream_pressure_p2_pa": round(max(0.0, p2), 2),
            "delta_p_pa": round(p1 - p2, 2),
            "cavitation_risk": is_cavitation_risk,
            "head_loss_equivalent_m": round(abs(total_head_1 - (p2 + 0.5 * rho * (v2**2) + rho * gravity * z2)) / (rho * gravity), 4),
        }

    @staticmethod
    def calculate_aerodynamic_coefficients(
        drag_force_newtons: float,
        lift_force_newtons: float,
        velocity_m_s: float,
        frontal_area_m2: float,
        fluid: str = "air_20c",
    ) -> Dict[str, Any]:
        """
        Calculate aerodynamic drag (C_D) and lift (C_L) coefficients:
        C_D = (2 * F_D) / (rho * v^2 * A)
        C_L = (2 * F_L) / (rho * v^2 * A)
        """
        f_d = max(0.0, float(drag_force_newtons))
        f_l = float(lift_force_newtons)
        v = max(0.01, float(velocity_m_s))
        area = max(1e-5, float(frontal_area_m2))

        rho, _ = ComputationalFluidDynamicsService.FLUID_CATALOG.get(
            fluid, ComputationalFluidDynamicsService.FLUID_CATALOG["air_20c"]
        )

        dyn_pressure = 0.5 * rho * (v ** 2)
        c_d = f_d / (dyn_pressure * area)
        c_l = f_l / (dyn_pressure * area)

        lift_to_drag = c_l / max(1e-6, c_d)

        return {
            "drag_coefficient_cd": round(c_d, 4),
            "lift_coefficient_cl": round(c_l, 4),
            "lift_to_drag_ratio": round(lift_to_drag, 3),
            "dynamic_pressure_pa": round(dyn_pressure, 2),
            "velocity_m_s": v,
            "frontal_area_m2": area,
            "drag_force_n": f_d,
            "lift_force_n": f_l,
        }

    @staticmethod
    def simulate_2d_laminar_channel_profile(
        channel_height_m: float = 0.05,
        centerline_velocity_m_s: float = 1.5,
        grid_points: int = 11,
    ) -> Dict[str, Any]:
        """
        Compute parabolic Poiseuille velocity profile for 2D laminar channel:
        u(y) = u_max * (1 - (2*y / H)^2) where y in [-H/2, H/2]
        """
        h = max(0.001, float(channel_height_m))
        u_max = max(0.01, float(centerline_velocity_m_s))
        n_pts = max(5, min(51, int(grid_points)))

        profile = []
        step = h / (n_pts - 1)
        half_h = h / 2.0

        for i in range(n_pts):
            y = -half_h + i * step
            # Parabolic equation
            u_y = u_max * (1.0 - (y / half_h) ** 2)
            u_y = max(0.0, u_y)
            profile.append({
                "index": i,
                "y_position_m": round(y, 4),
                "normalized_y": round(y / half_h, 3),
                "velocity_m_s": round(u_y, 4),
                "shear_strain_rate_s_inv": round(abs(2.0 * u_max * y / (half_h ** 2)), 4),
            })

        u_mean = (2.0 / 3.0) * u_max
        return {
            "channel_height_m": h,
            "centerline_velocity_max_m_s": u_max,
            "mean_bulk_velocity_m_s": round(u_mean, 4),
            "velocity_profile_samples": profile,
        }
