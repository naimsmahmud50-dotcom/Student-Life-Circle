"""
Neuromorphic Spiking Neural Network (SNN) Service
==================================================
Biomimetic Leaky Integrate-and-Fire (LIF) neuron dynamics, action
potential spike emission, and Spike-Timing-Dependent Plasticity (STDP)
Hebbian synaptic learning.

Mathematical Foundation:
- LIF Membrane Equation: tau_m * (dV / dt) = -(V - V_rest) + R_m * I(t)
- Threshold Condition: If V(t) >= V_thresh -> Spike = 1, V(t) = V_reset for t_ref
- STDP Synaptic Adaptation:
  For Delta t = t_post - t_pre:
    Delta w = A_+ * exp(-Delta t / tau_+)  if Delta t > 0 (LTP: Potentiation)
    Delta w = -A_- * exp(Delta t / tau_-)   if Delta t < 0 (LTD: Depression)

Zero external dependencies — pure Python standard library.
"""

import math
from typing import Any, Dict, List, Optional


class NeuromorphicSpikingNetworkService:
    """Enterprise neuromorphic SNN and synaptic plasticity engine."""

    V_REST_DEFAULT = -70.0      # Resting potential (mV)
    V_RESET_DEFAULT = -75.0     # Reset potential after spike (mV)
    V_THRESH_DEFAULT = -55.0    # Action potential trigger threshold (mV)
    TAU_M_DEFAULT = 20.0        # Membrane time constant (ms)
    R_M_DEFAULT = 10.0          # Membrane resistance (MOhm)
    T_REFRACTORY_DEFAULT = 2.0  # Absolute refractory period (ms)

    # STDP Canonical Parameters (Bi & Poo 1998)
    A_PLUS = 0.010              # Maximum potentiation rate
    A_MINUS = 0.012             # Maximum depression rate
    TAU_PLUS = 20.0             # STDP LTP decay window (ms)
    TAU_MINUS = 20.0            # STDP LTD decay window (ms)

    @staticmethod
    def simulate_lif_neuron(
        current_injections_na: List[float],
        dt_ms: float = 0.5,
        v_rest_mv: float = -70.0,
        v_thresh_mv: float = -55.0,
        v_reset_mv: float = -75.0,
        tau_m_ms: float = 20.0,
        r_m_mohm: float = 10.0,
        refractory_period_ms: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Simulate membrane voltage evolution of a single Leaky Integrate-and-Fire neuron.
        """
        dt = max(0.01, min(2.0, float(dt_ms)))
        tau_m = max(1.0, float(tau_m_ms))
        r_m = max(0.1, float(r_m_mohm))
        t_ref = max(0.0, float(refractory_period_ms))

        v = v_rest_mv
        time_elapsed = 0.0
        refractory_timer = 0.0

        traces_v = []
        spike_times_ms = []

        for i, i_inj in enumerate(current_injections_na):
            t_curr = i * dt
            if refractory_timer > 0.0:
                # Inside refractory period: voltage clamped to reset
                v = v_reset_mv
                refractory_timer -= dt
                spiked = False
            else:
                # Euler forward integration of LIF differential equation:
                # dV = (-(V - V_rest) + R_m * I) * (dt / tau_m)
                dv = (-(v - v_rest_mv) + r_m * i_inj) * (dt / tau_m)
                v += dv

                if v >= v_thresh_mv:
                    spiked = True
                    spike_times_ms.append(round(t_curr, 2))
                    v = v_reset_mv
                    refractory_timer = t_ref
                else:
                    spiked = False

            traces_v.append({
                "time_ms": round(t_curr, 2),
                "voltage_mv": round(v, 2),
                "current_na": round(i_inj, 2),
                "spiked": spiked,
            })

        total_sim_time_ms = len(current_injections_na) * dt
        firing_rate_hz = (len(spike_times_ms) / (total_sim_time_ms / 1000.0)) if total_sim_time_ms > 0 else 0.0

        return {
            "total_sim_time_ms": round(total_sim_time_ms, 2),
            "total_spikes": len(spike_times_ms),
            "firing_rate_hz": round(firing_rate_hz, 2),
            "spike_times_ms": spike_times_ms,
            "voltage_trace": traces_v,
            "neuron_regime": "REPETITIVE_FIRING" if firing_rate_hz > 5.0 else ("PHASIC_FIRING" if len(spike_times_ms) > 0 else "QUIESCENT_SUBTHRESHOLD"),
        }

    @staticmethod
    def calculate_stdp_synaptic_plasticity(
        initial_weight: float,
        pre_spike_times_ms: List[float],
        post_spike_times_ms: List[float],
        a_plus: float = 0.010,
        a_minus: float = 0.012,
        tau_plus_ms: float = 20.0,
        tau_minus_ms: float = 20.0,
        w_min: float = 0.0,
        w_max: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Compute synaptic weight updates via Spike-Timing-Dependent Plasticity (STDP).
        Pairs all causal and acausal spike interactions.
        """
        w = max(w_min, min(w_max, float(initial_weight)))
        weight_history = [w]
        total_ltp_events = 0
        total_ltd_events = 0
        net_delta_w = 0.0

        for t_pre in pre_spike_times_ms:
            for t_post in post_spike_times_ms:
                delta_t = t_post - t_pre

                # Bound delta_t to window of +/- 100 ms
                if 0.0 < delta_t <= 100.0:
                    # Pre before post => Causal => Long-Term Potentiation (LTP)
                    dw = a_plus * math.exp(-delta_t / max(1.0, tau_plus_ms))
                    w = min(w_max, w + dw)
                    net_delta_w += dw
                    total_ltp_events += 1
                elif -100.0 <= delta_t < 0.0:
                    # Post before pre => Acausal => Long-Term Depression (LTD)
                    dw = -a_minus * math.exp(delta_t / max(1.0, tau_minus_ms))
                    w = max(w_min, w + dw)
                    net_delta_w += dw
                    total_ltd_events += 1

                weight_history.append(round(w, 4))

        return {
            "initial_weight": initial_weight,
            "final_weight": round(w, 4),
            "net_weight_change": round(net_delta_w, 4),
            "total_ltp_events": total_ltp_events,
            "total_ltd_events": total_ltd_events,
            "plasticity_outcome": "POTENTIATED" if w > initial_weight else ("DEPRESSED" if w < initial_weight else "UNCHANGED"),
            "weight_history_samples": weight_history[:20],
        }
