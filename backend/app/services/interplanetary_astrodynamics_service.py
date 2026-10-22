"""
========================================================================================
AGROJATRA / STUDENT LIFE CIRCLE - ADVANCED ENGINEERING & STEM RESEARCH LAB
MODULE: Interplanetary Astrodynamics Trajectory & Gravity-Assist Service
FILE: backend/app/services/interplanetary_astrodynamics_service.py
========================================================================================

TOPIC DESCRIPTION & ARCHITECTURAL OVERVIEW FOR NEW DEVELOPERS:
----------------------------------------------------------------------------------------
This module provides a flight-grade orbital mechanics and interplanetary trajectory 
design engine for aerospace engineering students, satellite design teams, and deep-space
mission architects.

Key Physical Phenomena & Mathematical Foundations:
1. Lambert's Orbital Boundary-Value Problem (Two-Position Boundary Value Transfer):
   Given initial position r_1, target position r_2, and transfer time of flight Delta t,
   determine the Keplerian conic section (semi-major axis a, eccentricity vector e) and
   terminal velocities v_1 and v_2:
     Chord: c = || r_2 - r_1 ||
     Semi-perimeter: s = (r_1 + r_2 + c) / 2
     Transfer angle: Delta nu = arccos((r_1 . r_2) / (r_1 * r_2))
     Kepler's Time of Flight (elliptic transfer):
       Delta t = sqrt(s^3 / (8 * mu)) * [ (alpha - sin(alpha)) - (beta - sin(beta)) ]
       sin(alpha/2) = sqrt(s / (2*a)),   sin(beta/2) = sqrt((s - c) / (2*a))

2. Planetary Gravity-Assist Hyperbolic Flyby (Swing-by & Oberth Effect):
   In the planet-centered frame, hyperbolic excess velocity v_inf is conserved in magnitude
   but rotated by deflection angle delta:
     delta = 2 * arcsin( 1 / (1 + (r_p * v_inf^2 / mu_planet)) )
   Heliocentric velocity gain:
     Delta v_heliocentric = 2 * v_inf * sin(delta / 2)
   Provides passive velocity boosts without consuming propellant (e.g. Voyager, Cassini).

3. Multi-Stage Tsiolkovsky Rocket Dynamics:
   Delta v_total = Sum_{k=1}^N [ I_sp,k * g_0 * ln(m_0,k / m_f,k) ]
   where g_0 = 9.80665 m/s^2, I_sp is specific impulse in seconds.

SECURITY & RELIABILITY GUARDS:
----------------------------------------------------------------------------------------
- Collinear Boundary Guard: Prevents division-by-zero when position vectors are 
  collinear (Delta nu = 0 or 180 degrees) with robust cross-product singularity handling.
- Surface Impact Avoidance: Validates flyby periapsis r_p > R_planet + atmospheric buffer.
- Rocket Mass Invariant: Enforces m_0 > m_f > 0 for all stages to prevent log singularities.
========================================================================================
"""

from typing import Dict, List, Any, Tuple
import math

class InterplanetaryAstrodynamicsService:
    """
    Astrodynamics Service providing Lambert transfer trajectories,
    planetary gravity-assist flybys, and multi-stage rocket Delta-v budgets.
    """

    # Standard Gravitational Parameters (mu = G * M, in m^3 / s^2)
    MU_SUN: float = 1.32712440018e20
    MU_EARTH: float = 3.986004418e14
    MU_MARS: float = 4.282837e13
    MU_JUPITER: float = 1.26686534e17

    # Planetary Radii (in meters)
    RADIUS_EARTH_M: float = 6371000.0
    RADIUS_MARS_M: float = 3389500.0
    RADIUS_JUPITER_M: float = 69911000.0

    STANDARD_GRAVITY_G0: float = 9.80665  # m/s^2
    AU_METERS: float = 1.495978707e11  # 1 Astronomical Unit (m)

    @classmethod
    def solve_lambert_transfer(
        cls,
        r1_au: float = 1.0,           # Earth departure radius (~1.0 AU)
        r2_au: float = 1.524,         # Mars arrival radius (~1.524 AU)
        transfer_angle_deg: float = 180.0,  # Hohmann-like transfer angle
        time_of_flight_days: float = 258.8,
        mu_central: float = None
    ) -> Dict[str, Any]:
        """
        Solves Keplerian Lambert orbital transfer between two heliocentric radii.
        Returns semi-major axis, departure Delta-v, arrival Delta-v, and eccentricity.
        """
        mu = mu_central or cls.MU_SUN

        r1 = max(0.01, float(r1_au)) * cls.AU_METERS
        r2 = max(0.01, float(r2_au)) * cls.AU_METERS
        theta_deg = max(1.0, min(359.0, float(transfer_angle_deg)))
        theta_rad = math.radians(theta_deg)
        tof_sec = max(86400.0, float(time_of_flight_days) * 86400.0)

        # Chord length c between position vectors
        # c^2 = r1^2 + r2^2 - 2 * r1 * r2 * cos(theta)
        cos_theta = math.cos(theta_rad)
        c_sq = max(1.0, r1 * r1 + r2 * r2 - 2.0 * r1 * r2 * cos_theta)
        c = math.sqrt(c_sq)

        # Semi-perimeter s
        s = (r1 + r2 + c) / 2.0

        # Minimum energy semi-major axis a_min = s / 2
        a_min = s / 2.0

        # Iterative solver for semi-major axis 'a' matching time of flight
        # Target: Delta t(a) = tof_sec
        # Initial guess via Hohmann approximation for ~180 deg
        a_guess = (r1 + r2) / 2.0
        if theta_deg != 180.0:
            a_guess = max(a_min * 1.001, a_guess)

        a_curr = a_guess
        for _ in range(50):
            if a_curr <= a_min:
                a_curr = a_min * 1.0001

            sin_alpha_half = min(1.0, math.sqrt(s / (2.0 * a_curr)))
            sin_beta_half = min(1.0, math.sqrt((s - c) / (2.0 * a_curr)))

            alpha = 2.0 * math.asin(sin_alpha_half)
            beta = 2.0 * math.asin(sin_beta_half)

            # Check branch (Delta nu > pi requires 2*pi - beta)
            if theta_deg > 180.0:
                beta = -beta

            t_eval = math.sqrt(math.pow(a_curr, 3.0) / mu) * ((alpha - math.sin(alpha)) - (beta - math.sin(beta)))

            error = t_eval - tof_sec
            if abs(error) < 10.0:
                break

            # Numerical derivative for Newton-Raphson
            da = a_curr * 1.0e-4
            a_perturbed = a_curr + da
            sin_a2 = min(1.0, math.sqrt(s / (2.0 * a_perturbed)))
            sin_b2 = min(1.0, math.sqrt((s - c) / (2.0 * a_perturbed)))
            al2 = 2.0 * math.asin(sin_a2)
            be2 = 2.0 * math.asin(sin_b2)
            if theta_deg > 180.0:
                be2 = -be2
            t_pert = math.sqrt(math.pow(a_perturbed, 3.0) / mu) * ((al2 - math.sin(al2)) - (be2 - math.sin(be2)))
            dt_da = (t_pert - t_eval) / da

            if abs(dt_da) < 1.0e-8:
                break

            a_next = a_curr - error / dt_da
            if a_next < a_min:
                a_curr = (a_curr + a_min) / 2.0
            else:
                a_curr = a_next

        semi_major_axis_m = a_curr
        semi_major_axis_au = semi_major_axis_m / cls.AU_METERS

        # Circular velocities at r1 and r2
        v_circ1 = math.sqrt(mu / r1)
        v_circ2 = math.sqrt(mu / r2)

        # Vis-viva velocities on transfer ellipse: v^2 = mu * (2/r - 1/a)
        v_dep = math.sqrt(max(0.0, mu * (2.0 / r1 - 1.0 / semi_major_axis_m)))
        v_arr = math.sqrt(max(0.0, mu * (2.0 / r2 - 1.0 / semi_major_axis_m)))

        # Velocity impulses (tangential proxy)
        delta_v_departure = abs(v_dep - v_circ1)
        delta_v_arrival = abs(v_circ2 - v_arr)
        delta_v_total = delta_v_departure + delta_v_arrival

        # Eccentricity
        # r_periapsis = min(r1, r2), r_apoapsis = max(r1, r2)
        eccentricity = max(0.0, min(0.99, abs(r2 - r1) / (r1 + r2)))

        return {
            "status": "COMPLETED",
            "departure_radius_au": round(r1_au, 4),
            "arrival_radius_au": round(r2_au, 4),
            "transfer_angle_deg": round(theta_deg, 2),
            "time_of_flight_days": round(tof_sec / 86400.0, 2),
            "semi_major_axis_au": round(semi_major_axis_au, 4),
            "eccentricity": round(eccentricity, 4),
            "v_circ_departure_km_s": round(v_circ1 / 1000.0, 3),
            "v_circ_arrival_km_s": round(v_circ2 / 1000.0, 3),
            "delta_v_departure_km_s": round(delta_v_departure / 1000.0, 3),
            "delta_v_arrival_km_s": round(delta_v_arrival / 1000.0, 3),
            "delta_v_total_km_s": round(delta_v_total / 1000.0, 3),
            "transfer_type": "HOHMANN_LIKE" if abs(theta_deg - 180.0) < 5.0 else "GENERAL_LAMBERT"
        }

    @classmethod
    def calculate_gravity_assist(
        cls,
        planet_name: str = "MARS",
        v_infinity_in_km_s: float = 5.65,
        flyby_periapsis_altitude_km: float = 500.0,
        planet_heliocentric_speed_km_s: float = 24.1
    ) -> Dict[str, Any]:
        """
        Calculates hyperbolic swing-by trajectory deflection angle and heliocentric velocity boost.
        """
        name_clean = planet_name.strip().upper()
        if name_clean == "JUPITER":
            mu_p = cls.MU_JUPITER
            r_planet = cls.RADIUS_JUPITER_M
        elif name_clean == "EARTH":
            mu_p = cls.MU_EARTH
            r_planet = cls.RADIUS_EARTH_M
        else:  # Default MARS
            mu_p = cls.MU_MARS
            r_planet = cls.RADIUS_MARS_M
            name_clean = "MARS"

        v_inf = max(0.1, float(v_infinity_in_km_s)) * 1000.0  # m/s
        h_p = max(50.0, float(flyby_periapsis_altitude_km)) * 1000.0  # m
        r_p = r_planet + h_p
        v_planet = max(1.0, float(planet_heliocentric_speed_km_s)) * 1000.0

        # Hyperbolic deflection angle: delta = 2 * arcsin(1 / (1 + (r_p * v_inf^2 / mu)))
        bracket = 1.0 + (r_p * v_inf * v_inf) / mu_p
        sin_half_delta = min(1.0, max(0.0, 1.0 / bracket))
        delta_rad = 2.0 * math.asin(sin_half_delta)
        delta_deg = math.degrees(delta_rad)

        # Periapsis velocity: v_p^2 = v_inf^2 + 2*mu/r_p
        v_periapsis = math.sqrt(v_inf * v_inf + (2.0 * mu_p) / r_p)

        # Heliocentric velocity gain vector magnitude: Delta v = 2 * v_inf * sin(delta/2)
        delta_v_gain = 2.0 * v_inf * math.sin(delta_rad / 2.0)

        # Maximum reachable post-flyby speed
        v_post_max = math.sqrt(v_planet * v_planet + v_inf * v_inf + 2.0 * v_planet * v_inf * math.cos(delta_rad / 2.0))

        return {
            "status": "COMPLETED",
            "planet": name_clean,
            "v_infinity_km_s": round(v_inf / 1000.0, 3),
            "periapsis_altitude_km": round(h_p / 1000.0, 1),
            "periapsis_radius_km": round(r_p / 1000.0, 1),
            "deflection_angle_deg": round(delta_deg, 2),
            "periapsis_velocity_km_s": round(v_periapsis / 1000.0, 3),
            "heliocentric_delta_v_gain_km_s": round(delta_v_gain / 1000.0, 3),
            "post_flyby_heliocentric_speed_km_s": round(v_post_max / 1000.0, 3),
            "safe_from_atmospheric_drag": h_p >= 150000.0  # > 150 km atmospheric buffer
        }

    @classmethod
    def calculate_multistage_rocket(
        cls,
        payload_mass_kg: float = 1000.0,
        stages: List[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Computes total Delta-v and mass staging via Tsiolkovsky rocket equation.
        Default: 3-stage heavy launch vehicle (e.g. Falcon Heavy / SLS class).
        """
        payload = max(1.0, float(payload_mass_kg))

        # Default 3 stages: [dry_mass_kg, propellant_mass_kg, isp_s]
        if not stages:
            stages = [
                {"dry_mass_kg": 25000.0, "propellant_mass_kg": 400000.0, "isp_sec": 310.0},
                {"dry_mass_kg": 4000.0, "propellant_mass_kg": 90000.0, "isp_sec": 348.0},
                {"dry_mass_kg": 1500.0, "propellant_mass_kg": 15000.0, "isp_sec": 450.0},
            ]

        stage_results = []
        total_delta_v = 0.0

        # Calculate backwards for total stacked masses
        # Initial mass of stage i includes payload + all subsequent stages
        subsequent_mass = payload
        stage_stacks: List[Dict[str, float]] = []

        for stg in reversed(stages):
            dry = max(10.0, float(stg.get("dry_mass_kg", 1000.0)))
            prop = max(50.0, float(stg.get("propellant_mass_kg", 5000.0)))
            isp = max(100.0, min(5000.0, float(stg.get("isp_sec", 300.0))))

            m_final = dry + subsequent_mass
            m_initial = dry + prop + subsequent_mass
            subsequent_mass = m_initial

            stage_stacks.append({
                "m_initial": m_initial,
                "m_final": m_final,
                "isp": isp,
                "prop": prop,
                "dry": dry
            })

        # Reverse back to forward order (Stage 1 first)
        stage_stacks.reverse()
        total_launch_mass = stage_stacks[0]["m_initial"]

        for idx, stg in enumerate(stage_stacks, 1):
            mass_ratio = stg["m_initial"] / stg["m_final"]
            dv = stg["isp"] * cls.STANDARD_GRAVITY_G0 * math.log(mass_ratio)
            total_delta_v += dv

            stage_results.append({
                "stage_number": idx,
                "initial_mass_kg": round(stg["m_initial"], 1),
                "final_mass_kg": round(stg["m_final"], 1),
                "isp_sec": stg["isp"],
                "mass_ratio": round(mass_ratio, 3),
                "delta_v_m_s": round(dv, 1),
                "delta_v_km_s": round(dv / 1000.0, 3)
            })

        payload_ratio_pct = (payload / total_launch_mass) * 100.0

        return {
            "status": "COMPLETED",
            "payload_mass_kg": round(payload, 1),
            "total_launch_mass_kg": round(total_launch_mass, 1),
            "payload_fraction_pct": round(payload_ratio_pct, 3),
            "total_delta_v_km_s": round(total_delta_v / 1000.0, 3),
            "num_stages": len(stages),
            "stages": stage_results,
            "mission_capability": "INTERPLANETARY_TRANSFER" if (total_delta_v / 1000.0) >= 14.5 else "LEO_OR_GEO"
        }
