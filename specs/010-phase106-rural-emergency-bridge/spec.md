<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Feature Specification
TOPIC:     Phase 106 Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
FILE:      specs/010-phase106-rural-emergency-bridge/spec.md
PHASE:     Phase 106 - Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
PURPOSE:   Establishes functional specifications for off-grid Delay-Tolerant Networking (DTN),
           compact binary LoRaWAN radio frame packing (<= 256 bytes), CRC16 frame validation,
           physical Time-on-Air (ToA) modeling, and solar photovoltaic micro-hub telemetry.
STANDARDS: Delay-Tolerant Networking (DTN), CRC16 Frame Validation, Zero-Emoji, Field-Grade
-->

# Specification: Phase 106 — Rural LoRaWAN Emergency Bridge & Solar Micro-Hub

## Feature Directory
`specs/010-phase106-rural-emergency-bridge`

## 1. Problem Statement
In isolated riverine islands (Char areas), flood-prone haors (Sunamganj, Netrokona), and coastal delta belts of Bangladesh, seasonal monsoons, cyclones, and grid outages regularly sever cellular 4G/3G towers and mains electricity for days or weeks. When connectivity collapses, students are cut off from national exams, model test submissions, and emergency educational broadcasts. 

To bridge this educational chasm without relying on commercial telecom grids, "Student Life Circle (অগ্রযাত্রা)" requires an autonomous off-grid emergency bridge. Combining license-free sub-GHz LoRaWAN radio (868 MHz / 433 MHz) with solar-powered micro-hubs and Delay-Tolerant Networking (DTN) store-and-forward queues, students can submit exam responses through low-power transceivers, buffered until a solar hub establishes a gateway handshake.

## 2. Goals & User Stories

### US1: Ultra-Compact Binary Payload Packing & CRC16 Verification (P1)
- As an embedded radio engineer, I want student exam submissions and emergency telemetry packed into ultra-dense binary frames (<= 256 bytes) with CRC16-CCITT checksums to guarantee transmission integrity over noisy sub-GHz channels.
- Acceptance Criteria:
  - Binary packet structure: Header (1 byte), Sequence (2 bytes), Student/Device Hash (8 bytes), Payload Type (1 byte), Payload Data (variable), CRC16 (2 bytes).
  - Total frame size strictly <= 256 bytes (LoRa physical payload maximum).
  - Deterministic CRC16 calculation and verification. Reject corrupt frames.

### US2: Physical Time-on-Air (ToA) & Battery Energy Modeling (P1)
- As a field operations technician, I need precise Semtech LoRa Time-on-Air (ToA) calculations and battery drain modeling across Spreading Factors (SF7 to SF12) and Bandwidths (125 kHz, 250 kHz, 500 kHz).
- Acceptance Criteria:
  - Calculate symbol duration $T_{sym} = 2^{SF} / BW$.
  - Calculate preamble duration $T_{preamble} = (N_{preamble} + 4.25) \cdot T_{sym}$.
  - Compute payload symbol count and transmission time $ToA$.
  - Model energy consumed per transmission $E = V \cdot I_{tx} \cdot ToA$ in milliwatt-hours (mWh).

### US3: Delay-Tolerant Networking (DTN) Store-and-Forward Queue (P1)
- As a student in an isolated Char school, I want my submitted exam answers safely queued on local flash/memory and forwarded automatically as soon as a solar micro-hub gateway establishes an uplink.
- Acceptance Criteria:
  - In-memory/persistent DTN queue with TTL (Time-to-Live), priority levels, and ACK confirmation.
  - Automatic status transitions: `QUEUED` -> `TRANSMITTING` -> `ACKNOWLEDGED`.

### US4: Daylight-Readable LoRa Radio Studio & Solar Station UI (P1)
- As a teacher in a rural disaster shelter, I need daylight-readable, dependable field instruments to configure frequencies, send packets, and inspect solar battery status.
- Acceptance Criteria:
  - `frontend/src/components/emergency-mesh/LoRaRadioStudio.tsx`: 868MHz frequency selector, RF transmission trigger, and packet pulse visualizer.
  - Tactile 3D button depth (`shadow-[0_4px_0_0_#0F766E] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`).
  - `frontend/src/components/emergency-mesh/SolarStationTelemetry.tsx`: Battery voltage (12V/24V), solar irradiance, generation watts, student node counts.
  - Strict Zero-Emoji policy; Lucide SVG vectors only (`Radio`, `Battery`, `Sun`, `Signal`, `AlertTriangle`).
  - 'Hind Siliguri' typography for Bengali field copy, 'Inter' tabular numbers for voltages and RSSI metrics.

### US5: REST API Endpoints & Verification Suite (P1)
- As a client device, I need endpoints to transmit packets and inspect solar station telemetry.
- Acceptance Criteria:
  - `POST /api/v1/emergency/packet/send`: Ingests exam response or telemetry, serializes to binary, enqueues to DTN.
  - `GET /api/v1/emergency/station/status`: Returns real-time solar station voltage, battery percentage, and mesh topology.
  - Automated test suite `backend/tests/test_phase106_lora_emergency_bridge.py` passing 100%.
