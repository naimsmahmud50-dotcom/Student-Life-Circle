"""
Autonomous Micro-Robotics Swarm Intelligence Service
=====================================================
Distributed multi-agent coordination based on Reynolds Boids algorithm,
artificial potential fields for obstacle avoidance, and battery
duty-cycle consensus optimization.

Mathematical Foundation:
- Separation Force: F_sep = - sum_j (r_ij / |r_ij|^2) for |r_ij| < d_sep
- Alignment Force: F_ali = (1 / N) * sum_j v_j - v_i
- Cohesion Force: F_coh = (1 / N) * sum_j r_j - r_i
- Repulsive Potential Field: U_rep = 0.5 * eta * (1/d - 1/d0)^2 for d < d0
- Net Agent Steering: a_i = w_s * F_sep + w_a * F_ali + w_c * F_coh + F_rep

Zero external dependencies — pure Python standard library.
"""

import math
from typing import Any, Dict, List


class AutonomousMicroRoboticsSwarmService:
    """Enterprise multi-agent micro-robotics swarm simulator."""

    @staticmethod
    def simulate_swarm_step(
        agents: List[Dict[str, Any]],
        target_waypoint: List[float] | None = None,
        obstacles: List[List[float]] | None = None,
        dt_seconds: float = 0.1,
        weight_separation: float = 1.5,
        weight_alignment: float = 1.0,
        weight_cohesion: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Advance swarm kinematic state by dt seconds under Reynolds flocking forces
        and obstacle potential fields.
        """
        if not agents:
            # Generate default 5-drone triangular formation
            agents = [
                {"id": "agent_0", "x": 0.0, "y": 0.0, "vx": 1.0, "vy": 0.5, "battery_pct": 98.0},
                {"id": "agent_1", "x": -2.0, "y": -2.0, "vx": 1.0, "vy": 0.5, "battery_pct": 95.0},
                {"id": "agent_2", "x": 2.0, "y": -2.0, "vx": 1.0, "vy": 0.5, "battery_pct": 96.0},
                {"id": "agent_3", "x": -4.0, "y": -4.0, "vx": 1.0, "vy": 0.5, "battery_pct": 92.0},
                {"id": "agent_4", "x": 4.0, "y": -4.0, "vx": 1.0, "vy": 0.5, "battery_pct": 94.0},
            ]

        target = target_waypoint if target_waypoint else [25.0, 30.0]
        obs_list = obstacles if obstacles else [[10.0, 15.0], [18.0, 22.0]]
        dt = max(0.01, min(1.0, float(dt_seconds)))

        updated_agents = []
        n = len(agents)

        # Swarm centroid
        cx = sum(a["x"] for a in agents) / n
        cy = sum(a["y"] for a in agents) / n

        # Swarm mean velocity
        cvx = sum(a["vx"] for a in agents) / n
        cvy = sum(a["vy"] for a in agents) / n

        for a in agents:
            ax = a["x"]
            ay = a["y"]
            avx = a["vx"]
            avy = a["vy"]
            batt = a.get("battery_pct", 100.0)

            # 1. Separation force
            f_sep_x, f_sep_y = 0.0, 0.0
            for other in agents:
                if other["id"] == a["id"]:
                    continue
                dx = ax - other["x"]
                dy = ay - other["y"]
                dist = math.sqrt(dx * dx + dy * dy)
                if 0.001 < dist < 3.0:
                    f_sep_x += dx / (dist * dist)
                    f_sep_y += dy / (dist * dist)

            # 2. Alignment force
            f_ali_x = cvx - avx
            f_ali_y = cvy - avy

            # 3. Cohesion force
            f_coh_x = cx - ax
            f_coh_y = cy - ay

            # 4. Target attraction force
            t_dx = target[0] - ax
            t_dy = target[1] - ay
            t_dist = max(0.01, math.sqrt(t_dx * t_dx + t_dy * t_dy))
            f_tgt_x = 0.8 * (t_dx / t_dist)
            f_tgt_y = 0.8 * (t_dy / t_dist)

            # 5. Obstacle repulsive field
            f_rep_x, f_rep_y = 0.0, 0.0
            d0 = 4.0  # Obstacle influence distance
            for obs in obs_list:
                ox = ax - obs[0]
                oy = ay - obs[1]
                o_dist = max(0.01, math.sqrt(ox * ox + oy * oy))
                if o_dist < d0:
                    rep_mag = 2.0 * (1.0 / o_dist - 1.0 / d0) / (o_dist * o_dist)
                    f_rep_x += rep_mag * (ox / o_dist)
                    f_rep_y += rep_mag * (oy / o_dist)

            # Net acceleration
            acc_x = weight_separation * f_sep_x + weight_alignment * f_ali_x + weight_cohesion * f_coh_x + f_tgt_x + f_rep_x
            acc_y = weight_separation * f_sep_y + weight_alignment * f_ali_y + weight_cohesion * f_coh_y + f_tgt_y + f_rep_y

            # Limit max speed
            new_vx = avx + acc_x * dt
            new_vy = avy + acc_y * dt
            speed = math.sqrt(new_vx * new_vx + new_vy * new_vy)
            max_speed = 3.5
            if speed > max_speed:
                new_vx = (new_vx / speed) * max_speed
                new_vy = (new_vy / speed) * max_speed

            new_x = ax + new_vx * dt
            new_y = ay + new_vy * dt

            # Battery discharge proportional to speed plus baseline idle drain
            batt_drain = (0.05 * speed + 0.02) * dt
            new_batt = max(0.0, batt - batt_drain)

            updated_agents.append({
                "id": a["id"],
                "x": round(new_x, 3),
                "y": round(new_y, 3),
                "vx": round(new_vx, 3),
                "vy": round(new_vy, 3),
                "speed_m_s": round(speed, 2),
                "battery_pct": round(new_batt, 3),
            })

        # Formation dispersion metric (mean distance to centroid)
        dispersion = sum(
            math.sqrt((a["x"] - cx)**2 + (a["y"] - cy)**2) for a in updated_agents
        ) / n

        return {
            "swarm_size": n,
            "centroid": [round(cx, 3), round(cy, 3)],
            "target_waypoint": target,
            "swarm_dispersion_radius_m": round(dispersion, 3),
            "updated_agents": updated_agents,
            "swarm_status": "FLOCKING_NOMINAL" if dispersion < 10.0 else "DISPERSED",
        }
