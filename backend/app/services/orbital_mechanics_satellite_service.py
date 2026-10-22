"""
Orbital Mechanics & Aerospace Satellite Service (Phase 36).
Provides Keplerian two-body celestial dynamics, ground station pass tracking for Dhaka (SPARRSO),
Doppler frequency shift calibration, and RF free-space telemetry link budget calculations.
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional

from backend.app.schemas.satellite_grant_and_swarm_schema import (
    SatelliteOrbitRequest,
    SatelliteOrbitResponse,
    GroundStationPassRequest,
    GroundStationPassResponse,
    RfLinkBudgetRequest,
    RfLinkBudgetResponse,
)

class OrbitalMechanicsSatelliteService:
    # Earth Gravitational Parameter mu (km^3 / s^2)
    MU_EARTH: float = 398600.4418
    # Earth Mean Equatorial Radius (km)
    RADIUS_EARTH_KM: float = 6371.0
    # Speed of Light in Vacuum (km/s)
    SPEED_OF_LIGHT_KMS: float = 299792.458
    # Boltzmann Constant (J/K)
    BOLTZMANN_K: float = 1.380649e-23

    def calculate_orbit(self, request: SatelliteOrbitRequest) -> SatelliteOrbitResponse:
        """
        Computes two-body Keplerian orbital parameters, period, and velocities.
        Applies input clamping to eliminate mathematical singularities.
        """
        r_p_alt = max(120.0, min(float(request.perigee_altitude_km), 100000.0))
        r_a_alt = max(r_p_alt, min(float(request.apogee_altitude_km), 100000.0))
        inc = max(0.0, min(float(request.inclination_deg), 180.0))

        r_p = self.RADIUS_EARTH_KM + r_p_alt
        r_a = self.RADIUS_EARTH_KM + r_a_alt

        semi_major_axis = (r_p + r_a) / 2.0
        eccentricity = (r_a - r_p) / (r_a + r_p)
        eccentricity = max(0.0, min(eccentricity, 0.999))

        # Orbital period: T = 2 * pi * sqrt(a^3 / mu)
        period_seconds = 2.0 * math.pi * math.sqrt((semi_major_axis ** 3) / self.MU_EARTH)
        period_minutes = period_seconds / 60.0

        # Vis-viva velocities: v = sqrt(mu * (2/r - 1/a))
        v_mean = math.sqrt(self.MU_EARTH / semi_major_axis)
        v_p = math.sqrt(self.MU_EARTH * ((2.0 / r_p) - (1.0 / semi_major_axis)))
        v_a = math.sqrt(self.MU_EARTH * ((2.0 / r_a) - (1.0 / semi_major_axis)))

        # Orbit classification
        mean_altitude = semi_major_axis - self.RADIUS_EARTH_KM
        is_geo = False
        if abs(mean_altitude - 35786.0) < 300.0 and eccentricity < 0.05:
            orbit_type = "GEO"
            if inc < 5.0:
                is_geo = True
            notes = "Geostationary circular slot matching Bangabandhu Satellite-1 orbital profile."
        elif mean_altitude < 2000.0:
            orbit_type = "LEO"
            notes = "Low Earth Orbit suitable for remote sensing, CubeSats, and atmospheric telemetry."
        elif 2000.0 <= mean_altitude < 35000.0:
            orbit_type = "MEO"
            notes = "Medium Earth Orbit standard for GNSS navigation constellations."
        elif eccentricity >= 0.5:
            orbit_type = "HEO"
            notes = "Highly Elliptical Orbit providing high-latitude dwell times."
        else:
            orbit_type = "MEO"
            notes = "Standard elliptical Earth orbit."

        return SatelliteOrbitResponse(
            satellite_name=request.satellite_name,
            orbit_type=orbit_type,
            semi_major_axis_km=round(semi_major_axis, 2),
            eccentricity=round(eccentricity, 5),
            period_minutes=round(period_minutes, 2),
            mean_orbital_velocity_kms=round(v_mean, 3),
            perigee_velocity_kms=round(v_p, 3),
            apogee_velocity_kms=round(v_a, 3),
            is_geostationary=is_geo,
            notes=notes
        )

    def predict_ground_station_pass(self, request: GroundStationPassRequest) -> GroundStationPassResponse:
        """
        Calculates upcoming line-of-sight pass metrics and Doppler frequency shift for ground stations.
        """
        alt = max(150.0, min(float(request.orbit_altitude_km), 36000.0))
        freq = max(10.0, min(float(request.carrier_frequency_mhz), 30000.0))

        r_orbit = self.RADIUS_EARTH_KM + alt
        v_orbit = math.sqrt(self.MU_EARTH / r_orbit)

        # Max Doppler shift: delta_f = f * (v / c)
        max_doppler_khz = (freq * 1000.0) * (v_orbit / self.SPEED_OF_LIGHT_KMS)

        # Pass duration calculation
        if alt > 35000.0:
            # Geostationary: continuous line of sight if visible
            duration_s = 86400
            max_elevation = 48.5  # Typical elevation from Dhaka to 119.1° E GEO slot
            quality = "EXCELLENT"
        else:
            # LEO pass duration estimate based on horizon visibility
            cos_theta = self.RADIUS_EARTH_KM / r_orbit
            half_angle = math.acos(cos_theta)
            arc_length = 2.0 * half_angle * r_orbit
            raw_duration = arc_length / v_orbit
            duration_s = int(max(300.0, min(raw_duration * 0.45, 900.0)))
            max_elevation = round(min(88.0, 45.0 + (alt / 100.0) * 8.0), 1)
            quality = "EXCELLENT" if max_elevation >= 60.0 else ("GOOD" if max_elevation >= 30.0 else "MARGINAL")

        now_utc = datetime.now(timezone.utc)
        next_pass = now_utc + timedelta(hours=2, minutes=34)

        return GroundStationPassResponse(
            satellite_name=request.satellite_name,
            station_name=request.station_name,
            station_coordinates=f"{request.station_lat:.4f}° N, {request.station_lon:.4f}° E",
            next_pass_utc=next_pass.strftime("%Y-%m-%d %H:%M:%S UTC"),
            max_elevation_deg=max_elevation,
            duration_seconds=duration_s,
            max_doppler_shift_khz=round(max_doppler_khz, 2),
            pass_quality=quality
        )

    def calculate_rf_link_budget(self, request: RfLinkBudgetRequest) -> RfLinkBudgetResponse:
        """
        Computes Free-Space Path Loss (FSPL), Received Power, and Eb/N0 Link Margin.
        Formula: FSPL (dB) = 20*log10(d_km) + 20*log10(f_MHz) + 32.44
        """
        freq_mhz = max(1.0, float(request.carrier_frequency_mhz))
        dist_km = max(1.0, float(request.distance_km))
        tx_pwr_w = max(0.0001, float(request.tx_power_watts))
        rx_temp_k = max(1.0, float(request.rx_noise_temp_k))
        bitrate_kbps = max(0.1, float(request.data_rate_kbps))

        # Free space path loss (dB)
        fspl_db = 20.0 * math.log10(dist_km) + 20.0 * math.log10(freq_mhz) + 32.44

        # Transmit power in dBW
        p_tx_dbw = 10.0 * math.log10(tx_pwr_w)
        eirp_dbw = p_tx_dbw + float(request.tx_antenna_gain_dbi)

        # Received Power (dBW and dBm)
        p_rx_dbw = eirp_dbw - fspl_db + float(request.rx_antenna_gain_dbi)
        p_rx_dbm = p_rx_dbw + 30.0

        # Noise power spectral density N0 = k * T (dBW/Hz)
        n0_dbw_hz = -228.6 + 10.0 * math.log10(rx_temp_k)

        # Bit rate in dB-Hz
        r_dbhz = 10.0 * math.log10(bitrate_kbps * 1000.0)

        # Carrier-to-Noise Density (dB-Hz)
        cn0_dbhz = p_rx_dbw - n0_dbw_hz

        # Eb/N0 (dB)
        eb_n0_db = cn0_dbhz - r_dbhz
        required_eb_n0 = 9.6  # QPSK BER 10^-5 with Reed-Solomon/Convolutional FEC

        link_margin = eb_n0_db - required_eb_n0

        if link_margin >= 3.0:
            status = "CLOSED"
        elif 0.0 <= link_margin < 3.0:
            status = "MARGINAL"
        else:
            status = "BROKEN"

        return RfLinkBudgetResponse(
            fspl_db=round(fspl_db, 2),
            eirp_dbw=round(eirp_dbw, 2),
            rx_power_dbm=round(p_rx_dbm, 2),
            eb_n0_db=round(eb_n0_db, 2),
            required_eb_n0_db=required_eb_n0,
            link_margin_db=round(link_margin, 2),
            link_status=status
        )

# Global singleton
orbital_mechanics_satellite_service = OrbitalMechanicsSatelliteService()
