<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Phase 106 Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
FILE:      specs/010-phase106-rural-emergency-bridge/tasks.md
PHASE:     Phase 106 - Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
PURPOSE:   Ordered task list tracking atomic implementation steps for binary packet
           packing, CRC16 verification, ToA radio modeling, DTN queue, UI instruments, and test validation.
STANDARDS: Delay-Tolerant Networking (DTN), CRC16 Frame Validation, Zero-Emoji, Field-Grade
-->

# Tasks: Phase 106 — Rural LoRaWAN Emergency Bridge & Solar Micro-Hub

## Tasks Ledger

- [x] Task 1: Implement LoRa Packet & DTN Service (`backend/app/services/lora_packet_service.py`)
  - Binary packet packing (<= 256 bytes) with Header, Sequence, Device ID, Payload, and CRC16 checksum
  - CRC16-CCITT checksum computation and frame verification
  - Delay-Tolerant Network (DTN) queue buffer with priority, TTL, and status lifecycle
  - Semtech LoRa Time-on-Air (ToA) calculation across SF7-SF12 and bandwidths
  - Battery consumption modeling (current drain, transmission energy in mWh)
- [x] Task 2: Implement Daylight-Readable Radio Studio (`frontend/src/components/emergency-mesh/LoRaRadioStudio.tsx`)
  - Daylight-readable high-contrast field instrument design (slate surfaces, crisp dials)
  - Frequency tuner (868.1 MHz, 868.3 MHz, 433.175 MHz, 915.0 MHz)
  - Tactile 3D button physics (`shadow-[0_4px_0_0_#0F766E] active:translate-y-1 active:shadow-none font-semibold rounded-2xl`)
  - Audio and RF transmission pulse visualizer
  - Pure Lucide vectors and 'Hind Siliguri' + 'Inter' typography
- [x] Task 3: Implement Solar Station Telemetry Component (`frontend/src/components/emergency-mesh/SolarStationTelemetry.tsx`)
  - Solar photovoltaic voltage, battery reserve percentage (12V / 24V), power watts, and temperature
  - Local village student mesh network node counts and signal RSSI (dBm)
  - Field-grade high-contrast layout, tabular metrics, Zero Emoji
- [x] Task 4: Mount Emergency Mesh REST API endpoints (`backend/app/api/v1/endpoints/emergency_mesh.py`)
  - `POST /api/v1/emergency/packet/send`
  - `GET /api/v1/emergency/station/status`
  - Include router in `backend/app/api/v1/router.py`
- [x] Task 5: Implement automated verification test suite (`backend/tests/test_phase106_lora_emergency_bridge.py`)
  - Binary packet packing and size boundary assertions (<= 256 bytes)
  - CRC16 validation and corrupt frame rejection
  - Time-on-Air (ToA) calculation across SF7 to SF12
  - Battery consumption modeling
  - DTN queue buffering and delivery lifecycle
  - REST API endpoint verification
  - Developer Architecture Note header validation and strict zero-emoji sweep
- [x] Task 6: Execute full regression test discovery (`python3 -m unittest discover -s backend/tests`) asserting 100% pass rate
