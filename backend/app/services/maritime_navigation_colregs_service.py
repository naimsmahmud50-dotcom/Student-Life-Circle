"""
Autonomous Maritime Navigation (COLREGs AIS) Service
=====================================================
Automated AIS tracking, Closest Point of Approach (DCPA & TCPA) calculation,
and IMO COLREGs (Rules 13, 14, 15) collision avoidance protocol.

Mathematical Foundation:
- Relative Position: r_rel = r_target - r_own
- Relative Velocity: v_rel = v_target - v_own
- Time to Closest Point of Approach (TCPA):
  TCPA = - (r_rel . v_rel) / |v_rel|^2
- Distance at Closest Point of Approach (DCPA):
  DCPA = |r_rel + v_rel * TCPA|
- COLREGs Situations:
  - Rule 14 (Head-On): Relative bearing ~ 0° or 180° (+/- 10°). Evasive action: Turn to starboard.
  - Rule 15 (Crossing): Target approaching from starboard (0° - 112.5°). Give-way vessel must alter course to pass astern.
  - Rule 13 (Overtaking): Target approaching from > 112.5° abaft beam. Overtaking vessel keeps clear.

Zero external dependencies — pure Python standard library.
"""

import math
from typing import Any, Dict, List


class MaritimeNavigationColregsService:
    """Enterprise maritime autonomous surface ship (MASS) collision avoidance engine."""

    NM_TO_KM = 1.852             # Nautical miles to kilometers
    KNOTS_TO_MS = 0.514444       # Knots to meters/second
    DEFAULT_SAFETY_DCPA_NM = 1.0 # Minimum safe passing distance in NM
    DEFAULT_SAFETY_TCPA_MIN = 12.0 # Minimum safe collision warning horizon in minutes

    @staticmethod
    def calculate_closest_point_of_approach(
        own_x_nm: float,
        own_y_nm: float,
        own_speed_knots: float,
        own_course_deg: float,
        target_x_nm: float,
        target_y_nm: float,
        target_speed_knots: float,
        target_course_deg: float,
    ) -> Dict[str, Any]:
        """
        Calculate Distance to CPA (DCPA) and Time to CPA (TCPA) in nautical miles and minutes.
        """
        # Convert courses to math angles (0 deg = North = +y, 90 deg = East = +x)
        theta_own = math.radians(own_course_deg)
        theta_tgt = math.radians(target_course_deg)

        # Velocity components (knots)
        vx_own = own_speed_knots * math.sin(theta_own)
        vy_own = own_speed_knots * math.cos(theta_own)

        vx_tgt = target_speed_knots * math.sin(theta_tgt)
        vy_tgt = target_speed_knots * math.cos(theta_tgt)

        # Relative position (target relative to own)
        rx = target_x_nm - own_x_nm
        ry = target_y_nm - own_y_nm
        current_range_nm = math.sqrt(rx * rx + ry * ry)

        # Relative velocity
        vx_rel = vx_tgt - vx_own
        vy_rel = vy_tgt - vy_own
        v_rel_sq = vx_rel * vx_rel + vy_rel * vy_rel

        # TCPA calculation (hours)
        if v_rel_sq < 1e-6:
            # Parallel courses at identical speeds
            tcpa_hours = 0.0
            dcpa_nm = current_range_nm
        else:
            tcpa_hours = -(rx * vx_rel + ry * vy_rel) / v_rel_sq
            # Position at CPA
            cpa_x = rx + vx_rel * tcpa_hours
            cpa_y = ry + vy_rel * tcpa_hours
            dcpa_nm = math.sqrt(cpa_x * cpa_x + cpa_y * cpa_y)

        tcpa_minutes = tcpa_hours * 60.0

        # Relative bearing from own ship to target (0 - 360 deg)
        abs_bearing = (math.degrees(math.atan2(rx, ry)) + 360.0) % 360.0
        rel_bearing = (abs_bearing - own_course_deg + 360.0) % 360.0

        # Assess COLREGs collision risk
        is_diverging = tcpa_minutes < 0.0
        collision_risk = (
            not is_diverging
            and tcpa_minutes <= MaritimeNavigationColregsService.DEFAULT_SAFETY_TCPA_MIN
            and dcpa_nm <= MaritimeNavigationColregsService.DEFAULT_SAFETY_DCPA_NM
        )

        # COLREGs Rule classification
        # Course difference
        course_diff = abs((target_course_deg - own_course_deg + 180.0) % 360.0 - 180.0)

        if is_diverging:
            situation = "DIVERGING_SAFE"
            action = "MAINTAIN_COURSE_AND_SPEED"
            own_vessel_role = "STAND_ON"
        elif course_diff >= 170.0 and (rel_bearing <= 10.0 or rel_bearing >= 350.0):
            situation = "COLREGS_RULE_14_HEAD_ON"
            action = "ALTER_COURSE_TO_STARBOARD"
            own_vessel_role = "GIVE_WAY"
        elif rel_bearing > 112.5 and rel_bearing < 247.5:
            situation = "COLREGS_RULE_13_OVERTAKING"
            action = "OVERTAKING_VESSEL_KEEP_CLEAR"
            own_vessel_role = "GIVE_WAY"
        elif rel_bearing > 0.0 and rel_bearing <= 112.5:
            situation = "COLREGS_RULE_15_CROSSING_GIVE_WAY"
            action = "ALTER_COURSE_TO_STARBOARD_PASS_ASTERN"
            own_vessel_role = "GIVE_WAY"
        else:
            situation = "COLREGS_RULE_15_CROSSING_STAND_ON"
            action = "MAINTAIN_COURSE_AND_SPEED_STAND_ON"
            own_vessel_role = "STAND_ON"

        return {
            "current_range_nm": round(current_range_nm, 3),
            "relative_bearing_deg": round(rel_bearing, 1),
            "dcpa_nm": round(dcpa_nm, 3),
            "tcpa_minutes": round(tcpa_minutes, 1),
            "is_diverging": is_diverging,
            "collision_risk": collision_risk,
            "colregs_situation": situation,
            "own_vessel_role": own_vessel_role,
            "recommended_evasive_action": action,
        }
