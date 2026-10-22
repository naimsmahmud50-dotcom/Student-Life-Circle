"""
Gravitational Wave Interferometry (LIGO/Virgo) Service
======================================================
Compact Binary Coalescence (CBC) general relativity kinematics,
chirp mass calculation, frequency evolution trajectory (TaylorT1 0PN),
strain amplitude, and matched-filter Signal-to-Noise Ratio (SNR).

Mathematical Foundation:
- Solar Mass M_sun: 1.98847e30 kg
- Gravitational Constant G: 6.67430e-11 m^3 / (kg s^2)
- Speed of Light c: 299792458.0 m/s
- Chirp Mass: M_chirp = (m1 * m2)^(3/5) / (m1 + m2)^(1/5)
- Symmetric Mass Ratio: eta = (m1 * m2) / (m1 + m2)^2
- Frequency Derivative: df/dt = (96/5) * pi^(8/3) * (G * M_chirp / c^3)^(5/3) * f^(11/3)
- Time to Merger: tau_merge = (5 / 256) * (G * M_chirp / c^3)^(-5/3) * (pi * f)^(-8/3)
- Characteristic Strain: h_0 ~ (4 / D_L) * (G * M_chirp / c^2) * ((pi * G * M_chirp * f) / c^3)^(2/3)

Zero external dependencies — pure Python standard library.
"""

import math
from typing import Any, Dict, List


class GravitationalWaveInterferometryService:
    """Enterprise gravitational wave physics and CBC signal processing engine."""

    M_SUN_KG = 1.98847e30             # Solar mass in kg
    G_CONST = 6.67430e-11             # Newton gravitational constant (m^3 / kg s^2)
    C_LIGHT = 299792458.0             # Speed of light (m/s)
    MPC_TO_METERS = 3.085677581e22    # 1 Megaparsec in meters

    # Geometric conversion factor: (G * M_sun) / c^3 ~ 4.92549e-6 seconds
    T_SUN_SEC = (G_CONST * M_SUN_KG) / (C_LIGHT ** 3)

    @staticmethod
    def calculate_binary_chirp_parameters(
        m1_solar_masses: float,
        m2_solar_masses: float,
        luminosity_distance_mpc: float = 410.0,
        initial_frequency_hz: float = 30.0,
    ) -> Dict[str, Any]:
        """
        Calculate chirp mass, symmetric mass ratio, time to merger, and peak strain amplitude.
        """
        m1 = max(0.1, float(m1_solar_masses))
        m2 = max(0.1, float(m2_solar_masses))
        d_mpc = max(1.0, float(luminosity_distance_mpc))
        f0 = max(10.0, min(1000.0, float(initial_frequency_hz)))

        total_mass = m1 + m2
        # Chirp mass: M = (m1 * m2)^(3/5) / (m1 + m2)^(1/5)
        chirp_mass = ((m1 * m2) ** 0.6) / (total_mass ** 0.2)
        # Symmetric mass ratio: eta = (m1 * m2) / (m1 + m2)^2
        eta = (m1 * m2) / (total_mass ** 2)

        # Chirp mass in seconds: G * M_chirp / c^3
        m_sec = chirp_mass * GravitationalWaveInterferometryService.T_SUN_SEC

        # Time to merger from initial frequency f0:
        # tau = (5 / 256) * m_sec^(-5/3) * (pi * f0)^(-8/3)
        coeff = 5.0 / 256.0
        time_to_merger_s = coeff * (m_sec ** (-5.0 / 3.0)) * ((math.pi * f0) ** (-8.0 / 3.0))

        # Inspiral-Merger transition frequency (ISCO: Innermost Stable Circular Orbit):
        # f_ISCO = c^3 / (6^(3/2) * pi * G * M_total) ~ 4397 Hz / (M_total in M_sun)
        f_isco_hz = 4397.0 / total_mass

        # Distance in meters
        d_m = d_mpc * GravitationalWaveInterferometryService.MPC_TO_METERS

        # Peak strain amplitude at ISCO:
        # h_peak ~ (4 / d_m) * (G * M_chirp / c^2) * (pi * G * M_chirp * f_isco / c^3)^(2/3)
        geom_radius = (GravitationalWaveInterferometryService.G_CONST * chirp_mass * GravitationalWaveInterferometryService.M_SUN_KG) / (GravitationalWaveInterferometryService.C_LIGHT ** 2)
        v_c = (math.pi * m_sec * f_isco_hz) ** (2.0 / 3.0)
        h_peak = (4.0 / d_m) * geom_radius * v_c

        # Signal-to-Noise Ratio (SNR) proxy against Advanced LIGO noise floor (h_noise ~ 1e-23 at 100 Hz)
        snr_proxy = min(100.0, (h_peak / 1.0e-23) * math.sqrt(time_to_merger_s * 100.0))

        # Binary type classification
        if m1 >= 5.0 and m2 >= 5.0:
            classification = "BINARY_BLACK_HOLE_BBH"
        elif m1 < 3.0 and m2 < 3.0:
            classification = "BINARY_NEUTRON_STAR_BNS"
        else:
            classification = "NEUTRON_STAR_BLACK_HOLE_NSBH"

        return {
            "mass_1_msun": m1,
            "mass_2_msun": m2,
            "total_mass_msun": round(total_mass, 2),
            "chirp_mass_msun": round(chirp_mass, 3),
            "symmetric_mass_ratio_eta": round(eta, 4),
            "luminosity_distance_mpc": d_mpc,
            "initial_frequency_hz": f0,
            "time_to_merger_seconds": round(time_to_merger_s, 3),
            "isco_frequency_hz": round(f_isco_hz, 1),
            "peak_strain_amplitude_h": h_peak,
            "matched_filter_snr": round(snr_proxy, 1),
            "binary_classification": classification,
            "detection_confidence": "HIGH_CONFIDENCE_DETECTION" if snr_proxy >= 8.0 else "SUB_THRESHOLD_CANDIDATE",
        }

    @staticmethod
    def generate_chirp_waveform_samples(
        chirp_mass_msun: float,
        duration_seconds: float = 0.5,
        sampling_rate_hz: float = 2048.0,
    ) -> Dict[str, Any]:
        """
        Synthesize gravitational wave chirp waveform h(t) leading up to merger.
        f(t) = (1/pi) * ((5/256) / (tau_c - t))^(3/8) * (G*M/c^3)^(-5/8)
        """
        mc = max(1.0, float(chirp_mass_msun))
        t_dur = max(0.1, min(2.0, float(duration_seconds)))
        fs = max(512.0, min(4096.0, float(sampling_rate_hz)))
        num_samples = int(t_dur * fs)
        dt = 1.0 / fs

        m_sec = mc * GravitationalWaveInterferometryService.T_SUN_SEC
        t_merger = t_dur  # Merger occurs at the end of the duration window

        waveform = []
        phase = 0.0

        for i in range(num_samples):
            t = i * dt
            tau = max(1e-4, t_merger - t)

            # 0PN instantaneous frequency
            freq_inst = (1.0 / math.pi) * (((5.0 / 256.0) / tau) ** (3.0 / 8.0)) * (m_sec ** (-5.0 / 8.0))
            freq_inst = min(1500.0, freq_inst)  # Clamp to reasonable detector band

            phase += 2.0 * math.pi * freq_inst * dt
            amplitude = (1.0 / tau) ** (0.25) * 1e-21
            h_t = amplitude * math.cos(phase)

            if i % (num_samples // 20) == 0:  # Sample down for payload efficiency
                waveform.append({
                    "time_ms": round(t * 1000.0, 1),
                    "frequency_hz": round(freq_inst, 1),
                    "strain_normalized": round(h_t * 1e21, 3),
                })

        return {
            "chirp_mass_msun": mc,
            "duration_seconds": t_dur,
            "samples_count": len(waveform),
            "waveform_samples": waveform,
        }
