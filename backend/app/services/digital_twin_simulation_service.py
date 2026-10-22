"""
Digital Twin Simulation Engine Service
=======================================
Parametric digital twin state modeling with predictive maintenance
anomaly detection via Mahalanobis distance, Monte Carlo reliability
estimation, and sensor drift calibration.

Mathematical Foundation:
- Mahalanobis Distance: D_M = sqrt((x - mu)^T * Sigma^-1 * (x - mu))
- Exponential Reliability: R(t) = e^(-lambda * t)
- Monte Carlo MTTF: E[T] = (1 / N) * sum(T_i)
- Sensor Drift: x_calibrated = x_raw - drift_rate * elapsed_hours

Zero external dependencies — pure Python standard library.
"""

import math
import random
from typing import Any


class DigitalTwinSimulationService:
    """Enterprise digital twin simulation engine for predictive maintenance."""

    # Default sensor parameter bounds (name -> (min_normal, max_normal, unit))
    SENSOR_PROFILES = {
        "temperature": (18.0, 85.0, "C"),
        "pressure": (95.0, 115.0, "kPa"),
        "rpm": (800.0, 3600.0, "RPM"),
        "vibration": (0.01, 4.5, "mm/s"),
        "humidity": (20.0, 80.0, "%RH"),
        "voltage": (210.0, 240.0, "V"),
    }

    # Failure rate lambda (per 1000 hours) by component class
    FAILURE_RATES = {
        "motor": 0.0008,
        "pump": 0.0012,
        "bearing": 0.0020,
        "transformer": 0.0005,
        "compressor": 0.0015,
        "default": 0.0010,
    }

    @staticmethod
    def simulate_twin_state(
        sensors: dict[str, float] | None = None,
        noise_sigma: float = 0.05,
    ) -> dict[str, Any]:
        """
        Generate or validate a digital twin state snapshot with optional noise.

        Parameters
        ----------
        sensors : dict or None
            Mapping of sensor_name -> current_value. If None, generates defaults.
        noise_sigma : float
            Gaussian noise standard deviation as fraction of range (0-1).

        Returns
        -------
        dict with sensor readings, status flags, and timestamp metadata.
        """
        noise_sigma = max(0.0, min(1.0, noise_sigma))
        state: dict[str, Any] = {}

        if sensors is None:
            sensors = {}
            for name, (lo, hi, _) in DigitalTwinSimulationService.SENSOR_PROFILES.items():
                mid = (lo + hi) / 2.0
                span = hi - lo
                noise = random.gauss(0, noise_sigma * span)
                sensors[name] = round(mid + noise, 4)

        readings = []
        for name, value in sensors.items():
            profile = DigitalTwinSimulationService.SENSOR_PROFILES.get(name)
            if profile:
                lo, hi, unit = profile
                in_range = lo <= value <= hi
                pct = ((value - lo) / max(0.01, hi - lo)) * 100.0
            else:
                lo, hi, unit = 0.0, 100.0, "unit"
                in_range = True
                pct = 50.0

            readings.append({
                "sensor": name,
                "value": round(float(value), 4),
                "unit": unit,
                "normal_range": [lo, hi],
                "in_range": in_range,
                "utilization_pct": round(max(0.0, min(100.0, pct)), 2),
            })

        anomalies = [r for r in readings if not r["in_range"]]
        state["readings"] = readings
        state["total_sensors"] = len(readings)
        state["anomaly_count"] = len(anomalies)
        state["health_status"] = "HEALTHY" if len(anomalies) == 0 else "DEGRADED" if len(anomalies) <= 2 else "CRITICAL"
        return state

    @staticmethod
    def mahalanobis_anomaly_score(
        observation: list[float],
        mean_vector: list[float],
        covariance_matrix: list[list[float]],
    ) -> dict[str, Any]:
        """
        Compute Mahalanobis distance for multivariate anomaly detection.

        D_M = sqrt((x - mu)^T * Sigma^-1 * (x - mu))

        For a 2x2 covariance matrix, we compute the inverse analytically.
        For larger matrices, we use a simplified diagonal approximation
        to remain dependency-free.

        Parameters
        ----------
        observation : list of float
            Current sensor observation vector.
        mean_vector : list of float
            Historical mean vector (same dimensionality).
        covariance_matrix : list of list of float
            Covariance matrix (NxN).

        Returns
        -------
        dict with distance, threshold, and anomaly flag.
        """
        n = len(observation)
        if n != len(mean_vector):
            return {"error": "Dimension mismatch between observation and mean vector", "distance": -1.0}
        if len(covariance_matrix) != n:
            return {"error": "Covariance matrix dimension mismatch", "distance": -1.0}

        # Compute deviation vector
        diff = [observation[i] - mean_vector[i] for i in range(n)]

        if n == 1:
            var = max(1e-10, covariance_matrix[0][0])
            d_sq = (diff[0] ** 2) / var
        elif n == 2:
            # Analytical 2x2 inverse
            a, b = covariance_matrix[0][0], covariance_matrix[0][1]
            c, d = covariance_matrix[1][0], covariance_matrix[1][1]
            det = a * d - b * c
            det = max(abs(det), 1e-10) * (1 if det >= 0 else -1)
            inv = [[d / det, -b / det], [-c / det, a / det]]
            # (x-mu)^T * Sigma^-1 * (x-mu)
            temp = [sum(inv[i][j] * diff[j] for j in range(2)) for i in range(2)]
            d_sq = sum(diff[i] * temp[i] for i in range(2))
        else:
            # Diagonal approximation for larger dims
            d_sq = 0.0
            for i in range(n):
                var = max(1e-10, covariance_matrix[i][i])
                d_sq += (diff[i] ** 2) / var

        d_sq = max(0.0, d_sq)
        distance = math.sqrt(d_sq)

        # Chi-squared threshold approximation for n degrees of freedom at 95%
        # Using Wilson-Hilferty approximation: chi2_alpha ~ n * (1 - 2/(9n) + z_alpha * sqrt(2/(9n)))^3
        z_95 = 1.645
        wh = 1.0 - 2.0 / (9.0 * max(1, n)) + z_95 * math.sqrt(2.0 / (9.0 * max(1, n)))
        threshold = math.sqrt(max(1.0, n * (wh ** 3)))

        return {
            "mahalanobis_distance": round(distance, 6),
            "threshold_95pct": round(threshold, 6),
            "is_anomaly": distance > threshold,
            "dimensions": n,
            "severity": "CRITICAL" if distance > threshold * 1.5 else "WARNING" if distance > threshold else "NORMAL",
        }

    @staticmethod
    def calibrate_sensor_drift(
        raw_value: float,
        drift_rate_per_hour: float,
        elapsed_hours: float,
        reference_value: float | None = None,
    ) -> dict[str, Any]:
        """
        Calibrate a sensor reading by removing estimated drift.

        x_calibrated = x_raw - drift_rate * elapsed_hours

        Parameters
        ----------
        raw_value : float
            Current raw sensor reading.
        drift_rate_per_hour : float
            Estimated drift rate (units per hour).
        elapsed_hours : float
            Hours since last calibration.
        reference_value : float or None
            Known reference value for accuracy assessment.

        Returns
        -------
        dict with calibrated value, drift amount, and accuracy.
        """
        elapsed_hours = max(0.0, elapsed_hours)
        drift_amount = drift_rate_per_hour * elapsed_hours
        calibrated = raw_value - drift_amount

        result: dict[str, Any] = {
            "raw_value": round(raw_value, 6),
            "drift_rate_per_hour": drift_rate_per_hour,
            "elapsed_hours": elapsed_hours,
            "estimated_drift": round(drift_amount, 6),
            "calibrated_value": round(calibrated, 6),
        }

        if reference_value is not None:
            error = abs(calibrated - reference_value)
            pct_error = (error / max(abs(reference_value), 1e-10)) * 100.0
            result["reference_value"] = reference_value
            result["absolute_error"] = round(error, 6)
            result["percent_error"] = round(pct_error, 4)
            result["calibration_quality"] = "EXCELLENT" if pct_error < 1.0 else "GOOD" if pct_error < 5.0 else "FAIR" if pct_error < 10.0 else "POOR"

        return result

    @staticmethod
    def monte_carlo_reliability(
        component_class: str = "default",
        mission_hours: float = 1000.0,
        simulations: int = 1000,
        seed: int | None = None,
    ) -> dict[str, Any]:
        """
        Monte Carlo reliability estimation using exponential failure model.

        R(t) = e^(-lambda * t)
        MTTF = 1 / lambda

        Parameters
        ----------
        component_class : str
            Component type for failure rate lookup.
        mission_hours : float
            Duration of the mission in hours.
        simulations : int
            Number of Monte Carlo simulation runs (capped at 10000).
        seed : int or None
            Random seed for reproducibility.

        Returns
        -------
        dict with analytical and simulated reliability metrics.
        """
        lam = DigitalTwinSimulationService.FAILURE_RATES.get(
            component_class,
            DigitalTwinSimulationService.FAILURE_RATES["default"],
        )
        mission_hours = max(1.0, mission_hours)
        simulations = max(10, min(10000, simulations))

        if seed is not None:
            rng = random.Random(seed)
        else:
            rng = random.Random()

        # Analytical reliability
        analytical_reliability = math.exp(-lam * mission_hours)
        mttf = 1.0 / max(lam, 1e-12)

        # Monte Carlo simulation: generate failure times from exponential distribution
        failures_before_mission = 0
        failure_times = []
        for _ in range(simulations):
            u = max(1e-15, rng.random())
            t_fail = -math.log(u) / max(lam, 1e-12)
            failure_times.append(t_fail)
            if t_fail <= mission_hours:
                failures_before_mission += 1

        simulated_reliability = 1.0 - (failures_before_mission / simulations)
        simulated_mttf = sum(failure_times) / simulations

        return {
            "component_class": component_class,
            "failure_rate_lambda": lam,
            "mission_hours": mission_hours,
            "simulations": simulations,
            "analytical_reliability": round(analytical_reliability, 6),
            "analytical_mttf_hours": round(mttf, 2),
            "simulated_reliability": round(simulated_reliability, 6),
            "simulated_mttf_hours": round(simulated_mttf, 2),
            "failures_in_mission": failures_before_mission,
            "confidence": "HIGH" if simulations >= 500 else "MEDIUM" if simulations >= 100 else "LOW",
        }
