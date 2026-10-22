"""
Edge AI Robotics & Drone Simulator Service (Phase 37).
Provides discrete PID attitude loop simulation for quadcopter pitch/roll stabilization,
thrust-to-weight ratio dynamics, and LiPo battery hover endurance kinetics.
"""

import math
from typing import Dict, Any, List

from backend.app.schemas.robotics_genomics_and_biomedical_schema import (
    DronePidSimRequest,
    DronePidSimResponse,
    DroneEnduranceRequest,
    DroneEnduranceResponse,
)

class EdgeRoboticsDroneSimulatorService:
    GRAVITY_G: float = 9.80665
    MOMENT_OF_INERTIA: float = 0.025  # kg * m^2 for typical 5-inch / 10-inch drone frame
    AERODYNAMIC_DAMPING: float = 0.08

    def simulate_pid_attitude(self, request: DronePidSimRequest) -> DronePidSimResponse:
        """
        Simulates closed-loop quadcopter attitude control using discrete PID.
        Governing equation: tau = Kp*e + Ki*integral(e*dt) + Kd*(de/dt)
        Angular dynamics: d2_theta/dt2 = (tau - c * d_theta) / I
        """
        kp = max(0.0, float(request.kp))
        ki = max(0.0, float(request.ki))
        kd = max(0.0, float(request.kd))
        target_deg = float(request.target_angle_deg)
        current_deg = float(request.initial_angle_deg)
        dt = max(0.005, min(float(request.dt_seconds), 0.1))
        steps = max(20, min(int(request.steps), 300))

        integral_error = 0.0
        prev_error = target_deg - current_deg
        angular_velocity = 0.0  # deg/s

        max_angle = current_deg
        trajectory = []
        settling_step = None
        target_tolerance = max(0.5, abs(target_deg) * 0.05) if target_deg != 0 else 0.5

        for step in range(steps):
            error = target_deg - current_deg
            integral_error += error * dt
            # Anti-windup clamping on integral
            integral_error = max(-50.0, min(integral_error, 50.0))

            derivative_error = (error - prev_error) / dt
            prev_error = error

            # PID torque command
            tau = (kp * error) + (ki * integral_error) + (kd * derivative_error)

            # Angular acceleration
            alpha = (tau - (self.AERODYNAMIC_DAMPING * angular_velocity)) / self.MOMENT_OF_INERTIA
            angular_velocity += alpha * dt
            current_deg += angular_velocity * dt

            if abs(current_deg) > abs(max_angle):
                max_angle = current_deg

            # Check settling condition
            if abs(error) <= target_tolerance:
                if settling_step is None:
                    settling_step = step
            else:
                settling_step = None

            if step % max(1, steps // 10) == 0 or step == steps - 1:
                trajectory.append({
                    "time_s": round(step * dt, 3),
                    "angle_deg": round(current_deg, 2),
                    "error_deg": round(error, 2),
                    "torque_nm": round(tau, 3)
                })

        settling_time_s = round(settling_step * dt, 2) if settling_step else round(steps * dt, 2)
        target_baseline = abs(target_deg) if target_deg != 0 else 1.0
        overshoot = max(0.0, ((abs(max_angle) - abs(target_deg)) / target_baseline) * 100.0) if abs(max_angle) > abs(target_deg) else 0.0
        steady_state_error = abs(target_deg - current_deg)

        is_stable = steady_state_error <= 1.5 and not math.isnan(current_deg) and not math.isinf(current_deg)

        if is_stable and overshoot < 15.0:
            summary = "Critically damped loop: Fast rise time with minimal overshoot."
        elif is_stable:
            summary = f"Stable with {overshoot:.1f}% oscillatory overshoot. Consider increasing Kd damping."
        else:
            summary = "Underdamped or unstable loop: Steady-state error exceeded tolerance."

        return DronePidSimResponse(
            settling_time_seconds=settling_time_s,
            overshoot_pct=round(overshoot, 1),
            steady_state_error_deg=round(steady_state_error, 2),
            is_stable=is_stable,
            status_summary=summary,
            trajectory_sample=trajectory
        )

    def calculate_endurance(self, request: DroneEnduranceRequest) -> DroneEnduranceResponse:
        """
        Calculates hover power kinetics, thrust-to-weight ratio, and flight endurance in minutes.
        """
        mass = max(0.2, min(float(request.mass_kg), 50.0))
        rotors = max(3, min(int(request.rotor_count), 12))
        capacity = max(500.0, min(float(request.battery_capacity_mah), 100000.0))
        voltage = max(3.7, min(float(request.battery_voltage_v), 60.0))
        efficiency = max(2.5, min(float(request.hover_efficiency_g_per_w), 20.0))

        weight_n = mass * self.GRAVITY_G
        mass_grams = mass * 1000.0

        # Hover power in Watts = Total mass in grams / (grams per Watt efficiency)
        hover_power_watts = mass_grams / efficiency

        # Total battery energy in Watt-Hours (Wh) = (Capacity in mAh * V) / 1000
        battery_energy_wh = (capacity * voltage) / 1000.0

        # Safe 80% Depth-of-Discharge (DoD) to protect LiPo cells from over-discharge
        usable_energy_wh = battery_energy_wh * 0.80

        # Hover endurance time in minutes = (Usable Energy / Hover Power) * 60
        hover_time_minutes = (usable_energy_wh / hover_power_watts) * 60.0

        # Nominal thrust-to-weight ratio for standard brushless motors at 100% duty cycle
        # Standard configuration targets 2.1 to 2.5 TWR for agile authority
        twr = 2.25

        if hover_time_minutes >= 20.0:
            readiness = "MISSION_READY"
        elif hover_time_minutes >= 10.0:
            readiness = "SUB_OPTIMAL"
        else:
            readiness = "DANGEROUSLY_OVERWEIGHT"

        return DroneEnduranceResponse(
            total_weight_n=round(weight_n, 2),
            hover_power_watts=round(hover_power_watts, 2),
            battery_energy_wh=round(battery_energy_wh, 2),
            hover_time_minutes=round(hover_time_minutes, 1),
            thrust_to_weight_ratio=twr,
            flight_readiness=readiness
        )

# Global singleton
edge_robotics_drone_service = EdgeRoboticsDroneSimulatorService()
