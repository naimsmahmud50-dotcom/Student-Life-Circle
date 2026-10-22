# Security Fix Plan: Phase 36 Orbital Mechanics, Global Grants & Swarm Study Pods

**Date:** 2026-10-15  
**Engine:** `/speckit-bug-fix`

## Implemented Hardening Measures

1. **Domain Clamping in `OrbitalMechanicsSatelliteService`**:
   - `dist_km = max(1.0, float(request.distance_km))`
   - `freq_mhz = max(1.0, float(request.carrier_frequency_mhz))`
   - `tx_pwr_w = max(0.0001, float(request.tx_power_watts))`
   - `rx_temp_k = max(1.0, float(request.rx_noise_temp_k))`
   - `bitrate_kbps = max(0.1, float(request.data_rate_kbps))`
   - `eccentricity = max(0.0, min(eccentricity, 0.999))`
   - Guarantees $0 \le e < 1.0$ (eliminates parabolic/hyperbolic divergence).

2. **Sanitization in `GlobalResearchGrantService`**:
   - Robust tokenization via `\b[a-zA-Z]{2,}\b` eliminates XSS payloads.
   - Word count underflow checks for payloads $< 30$ words returning structured advisory feedback rather than failing with division-by-zero errors.
   - Overhead rate clamped to $[0.0, 65.0]\%$.

3. **Multi-Agent Session Isolation**:
   - Cryptographically random session IDs using `uuid.uuid4().hex[:10].upper()`.
   - Default fallbacks for empty query strings.
