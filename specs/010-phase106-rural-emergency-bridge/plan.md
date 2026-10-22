<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Implementation Plan
TOPIC:     Phase 106 Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
FILE:      specs/010-phase106-rural-emergency-bridge/plan.md
PHASE:     Phase 106 - Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
PURPOSE:   Architectural blueprint detailing technical steps for binary packet framing,
           CRC16 validation, Time-on-Air radio physical modeling, DTN queue buffering,
           daylight-readable field instrument UI components, REST endpoints, and test verification.
STANDARDS: Delay-Tolerant Networking (DTN), CRC16 Frame Validation, Zero-Emoji, Field-Grade
-->

# Implementation Plan: Phase 106 — Rural LoRaWAN Emergency Bridge & Solar Micro-Hub

## 1. System Architecture

```
+-------------------------------------------------------------+
|             Off-Grid Char / Haor Student Transceiver         |
|  - Student Exam Answers (MCQ / Numerical)                   |
|  - Packed into binary frame <= 256 bytes with CRC16         |
|  - LoRa PHY: 868.1 MHz, SF7-SF12, BW 125 kHz                |
+------------------------------+------------------------------+
                               |
                   (Sub-GHz Radio Transmission)
                               |
                               v
+-------------------------------------------------------------+
|            Solar Micro-Hub & Gateway Node                   |
|  - 100W Monocrystalline PV Panel + 12.8V LiFePO4 Battery    |
|  - SolarStationTelemetry.tsx: Real-time Volts, Watts, RSSI  |
|  - Delay-Tolerant Network (DTN) Store-and-Forward Queue     |
+------------------------------+------------------------------+
                               |
              (Periodic Satellite / Cellular Handshake)
                               |
                               v
+-------------------------------------------------------------+
|             Ogrojatra Cloud & National Exam Core            |
|  - Ingests verified binary packets via REST endpoints       |
|  - POST /api/v1/emergency/packet/send                       |
|  - GET  /api/v1/emergency/station/status                    |
+-------------------------------------------------------------+
```

## 2. Radio Physical Math & Binary Frame Structure

### A. Frame Structure (Max 256 Bytes)
```
+--------+----------+---------------+--------------+-------------------+----------+
| Header | Seq No   | Device ID     | Payload Type | Encoded Payload   | CRC-16   |
| 1 byte | 2 bytes  | 8 bytes       | 1 byte       | N bytes (<= 242)  | 2 bytes  |
+--------+----------+---------------+--------------+-------------------+----------+
```
Total overhead: $1 + 2 + 8 + 1 + 2 = 14$ bytes. Maximum user payload: 242 bytes.

### B. Time-on-Air (ToA) Physical Formulas
$$T_{sym} = \frac{2^{SF}}{BW}$$
$$T_{preamble} = (N_{preamble} + 4.25) \cdot T_{sym}$$
$$Payload_{symbols} = 8 + \max\left( \left\lceil \frac{8 \cdot PL - 4 \cdot SF + 28 + 16 - 20H}{4(SF - 2DE)} \right\rceil \cdot (CR + 4), 0 \right)$$
$$ToA = T_{preamble} + Payload_{symbols} \cdot T_{sym}$$

---

## 3. Implementation Steps & Targets
1. `backend/app/services/lora_packet_service.py`: Binary serialization, CRC16 checksum, Semtech LoRa ToA calculation, battery drain estimation, and DTN store-and-forward queue.
2. `frontend/src/components/emergency-mesh/LoRaRadioStudio.tsx`: Field-grade daylight-readable instrument with frequency dial, 3D tactile buttons (`shadow-[0_4px_0_0_#0F766E]`), and transmission pulse visualizer.
3. `frontend/src/components/emergency-mesh/SolarStationTelemetry.tsx`: Solar panel power telemetry, battery percentage, student mesh nodes, Inter tabular metrics.
4. `backend/app/api/v1/endpoints/emergency_mesh.py`: Fast REST endpoints for packet dispatch and station health inquiry.
5. `backend/tests/test_phase106_lora_emergency_bridge.py`: Automated tests asserting binary frames, CRC16 verification, ToA values, DTN queue, zero emoji, and architecture note headers.
6. Platform regression pass asserting 1,308+ passing tests.
