"""
Phase 57: Adaptive Bitrate (ABR) Advisor Service.
Computes Exponential Moving Average (EMA) throughput, applies hysteresis damping,
and monitors client buffer occupancy to prevent video stalls on unstable mobile connections.
"""

from typing import Dict, Any, Optional


class AdaptiveBitrateAdvisorService:
    """
    ABR decision engine implementing smoothed throughput estimation,
    hysteresis-guarded ladder transitions, and buffer starvation alarms.
    """

    # Resolution ladder thresholds in kbps
    BITRATE_THRESHOLDS = [
        {"resolution": "1080p", "min_kbps": 3500.0, "nominal_kbps": 4200.0},
        {"resolution": "720p", "min_kbps": 1500.0, "nominal_kbps": 1800.0},
        {"resolution": "360p", "min_kbps": 400.0, "nominal_kbps": 480.0},
        {"resolution": "240p", "min_kbps": 200.0, "nominal_kbps": 240.0},
        {"resolution": "144p", "min_kbps": 0.0, "nominal_kbps": 96.0}
    ]

    # EMA smoothing coefficient (0.0 < alpha <= 1.0)
    EMA_ALPHA = 0.35

    def __init__(self):
        # In-memory history for smoothing simulation: {session_id: last_smoothed_kbps}
        self._session_cache: Dict[str, float] = {}

    def advise_bitrate(
        self,
        measured_throughput_kbps: float,
        current_resolution: str = "360p",
        buffer_occupancy_seconds: float = 10.0,
        device_pixel_ratio: float = 1.0,
        is_metered_connection: bool = False,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates network speed, buffer state, and metered constraints to select
        optimal playback resolution without oscillation.
        """
        measured_kbps = max(10.0, float(measured_throughput_kbps))
        buffer_sec = max(0.0, float(buffer_occupancy_seconds))

        # 1. Smooth throughput using Exponential Moving Average
        cache_key = session_id or "default_session"
        prev_smoothed = self._session_cache.get(cache_key, measured_kbps)
        smoothed_kbps = round(
            (self.EMA_ALPHA * measured_kbps) + ((1.0 - self.EMA_ALPHA) * prev_smoothed),
            2
        )
        self._session_cache[cache_key] = smoothed_kbps

        # 2. Buffer Health & Stall Risk assessment
        buffer_health, stall_risk = self.calculate_buffer_health(buffer_sec)

        # 3. Determine ideal resolution from smoothed throughput
        target_resolution = "144p"
        for tier in self.BITRATE_THRESHOLDS:
            if smoothed_kbps >= tier["min_kbps"]:
                target_resolution = tier["resolution"]
                break

        # Metered connection cap (Data Saver mode caps at 360p)
        if is_metered_connection and target_resolution in ("720p", "1080p"):
            target_resolution = "360p"

        # 4. Hysteresis Damping to prevent rapid oscillation
        ladder_order = ["144p", "240p", "360p", "720p", "1080p"]
        curr_idx = ladder_order.index(current_resolution) if current_resolution in ladder_order else 2
        targ_idx = ladder_order.index(target_resolution) if target_resolution in ladder_order else 2

        hysteresis_applied = False
        final_resolution = current_resolution
        action_msg = "Maintain current playback profile."

        # Case A: Emergency Downgrade due to buffer starvation
        if buffer_sec < 3.5 and curr_idx > 0:
            final_resolution = ladder_order[max(0, curr_idx - 1)]
            action_msg = "Emergency downscale to avoid buffer stall."
        # Case B: Standard Downgrade when bandwidth drops
        elif targ_idx < curr_idx:
            final_resolution = target_resolution
            action_msg = f"Network bandwidth degraded. Downscaling from {current_resolution} to {final_resolution}."
        # Case C: Upgrade requires headroom (hysteresis) and healthy buffer
        elif targ_idx > curr_idx:
            # Require at least 20% throughput headroom and 8s buffer to upgrade
            target_tier = next(t for t in self.BITRATE_THRESHOLDS if t["resolution"] == target_resolution)
            required_upgrade_headroom = target_tier["min_kbps"] * 1.20

            if smoothed_kbps >= required_upgrade_headroom and buffer_sec >= 8.0:
                final_resolution = target_resolution
                action_msg = f"Throughput sustained with healthy buffer. Upgrading to {final_resolution}."
            else:
                final_resolution = current_resolution
                hysteresis_applied = True
                action_msg = f"Hysteresis active: upgrade to {target_resolution} deferred until headroom/buffer stabilizes."
        else:
            final_resolution = current_resolution
            action_msg = f"Stable throughput on {final_resolution}."

        is_switching = final_resolution != current_resolution

        return {
            "measured_throughput_kbps": measured_kbps,
            "smoothed_throughput_kbps": smoothed_kbps,
            "current_resolution": current_resolution,
            "recommended_resolution": final_resolution,
            "is_switching_resolution": is_switching,
            "buffer_health_status": buffer_health,
            "stall_risk_percentage": stall_risk,
            "hysteresis_applied": hysteresis_applied,
            "advisor_action": action_msg
        }

    def calculate_buffer_health(self, buffer_seconds: float) -> tuple:
        """
        Returns (buffer_status_str, stall_risk_percentage).
        """
        if buffer_seconds >= 15.0:
            return ("OPTIMAL_BUFFER", 2.0)
        elif buffer_seconds >= 8.0:
            return ("STABLE_BUFFER", 12.0)
        elif buffer_seconds >= 3.5:
            return ("DEPLETING_BUFFER", 45.0)
        else:
            return ("CRITICAL_STARVATION", 92.0)
