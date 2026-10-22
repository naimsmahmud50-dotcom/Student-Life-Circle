"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Automated Verification Test Suite
TOPIC:     Phase 106 Rural LoRaWAN Emergency Bridge & Solar Micro-Hub Tests
FILE:      backend/tests/test_phase106_lora_emergency_bridge.py
PHASE:     Phase 106 - Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
PURPOSE:   Asserts binary packet packing (<= 256 bytes), CRC16 checksum validation,
           Semtech LoRa Time-on-Air (ToA) physics, DTN store-and-forward queueing,
           solar telemetry interrogation, REST API routes, and strict zero-emoji governance.
STANDARDS: Delay-Tolerant Networking (DTN), CRC16 Frame Validation, Zero-Emoji, Field-Grade
"""

import asyncio
import json
import os
import unittest
from pathlib import Path

from backend.app.services.lora_packet_service import (
    LoraPacketService,
    compute_crc16,
    lora_packet_service
)
from backend.app.api.v1.endpoints.emergency_mesh import (
    send_emergency_lora_packet,
    get_solar_station_status,
    list_all_solar_stations,
    list_dtn_pending_queue,
    acknowledge_dtn_packet
)
from backend.app.core.fastapi_shim import HTTPException


def is_emoji_char(char: str) -> bool:
    """Detects whether a character is a decorative unicode emoji."""
    code = ord(char)
    return (
        0x1F600 <= code <= 0x1F64F or
        0x1F300 <= code <= 0x1F5FF or
        0x1F680 <= code <= 0x1F6FF or
        0x1F900 <= code <= 0x1F9FF or
        0x1FA70 <= code <= 0x1FAFF or
        0x2600 <= code <= 0x26FF or
        0x2700 <= code <= 0x27BF
    )


def contains_emoji(text: str) -> bool:
    """Returns True if string contains any decorative unicode emoji."""
    return any(is_emoji_char(c) for c in text)


class TestPhase106LoraEmergencyBridge(unittest.TestCase):
    """
    Automated verification suite for Phase 106 Rural LoRaWAN Emergency Bridge & Solar Micro-Hub.
    """

    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parent.parent.parent
        cls.service_path = cls.repo_root / "backend" / "app" / "services" / "lora_packet_service.py"
        cls.endpoint_path = cls.repo_root / "backend" / "app" / "api" / "v1" / "endpoints" / "emergency_mesh.py"
        cls.studio_path = cls.repo_root / "frontend" / "src" / "components" / "emergency-mesh" / "LoRaRadioStudio.tsx"
        cls.solar_path = cls.repo_root / "frontend" / "src" / "components" / "emergency-mesh" / "SolarStationTelemetry.tsx"
        cls.page_path = cls.repo_root / "frontend" / "src" / "pages" / "emergency-mesh.tsx"
        cls.tasks_path = cls.repo_root / "specs" / "010-phase106-rural-emergency-bridge" / "tasks.md"

    def setUp(self):
        lora_packet_service.reset_for_testing()

    def test_01_crc16_computation_and_integrity(self):
        """Verifies CRC16-CCITT checksum computation and single-bit sensitivity."""
        sample_data = b"STUDENT_EXAM_ANSWER_Q1_A_Q2_C"
        crc1 = compute_crc16(sample_data)
        crc2 = compute_crc16(sample_data)
        self.assertEqual(crc1, crc2)
        self.assertIsInstance(crc1, int)
        self.assertTrue(0 <= crc1 <= 0xFFFF)

        # Single bit alteration must produce completely different checksum
        corrupted = bytearray(sample_data)
        corrupted[0] ^= 0x01
        crc_corrupted = compute_crc16(bytes(corrupted))
        self.assertNotEqual(crc1, crc_corrupted)

    def test_02_binary_frame_packing_and_256_byte_boundary(self):
        """Asserts binary frame packing strictly respects <= 256 bytes and header protocol."""
        svc = LoraPacketService()

        # Test small payload
        frame_small = svc.pack_frame("DEV-0001", LoraPacketService.TYPE_EXAM_ANSWER, b"ANS_A_B_C")
        self.assertLessEqual(len(frame_small), 256)
        self.assertEqual(frame_small[0], 0x7E)  # Sync byte

        unpacked = svc.unpack_frame(frame_small)
        self.assertTrue(unpacked["valid"])
        self.assertEqual(unpacked["device_id"], "DEV-0001")
        self.assertEqual(unpacked["payload_type"], LoraPacketService.TYPE_EXAM_ANSWER)
        self.assertEqual(unpacked["payload_bytes"], b"ANS_A_B_C")

        # Test maximum boundary payload (241 bytes payload + 15 bytes overhead = 256 bytes)
        large_payload = b"X" * 300  # Intentionally oversized
        frame_large = svc.pack_frame("STU-CHIL", LoraPacketService.TYPE_EXAM_ANSWER, large_payload)
        self.assertEqual(len(frame_large), 256)

        unpacked_large = svc.unpack_frame(frame_large)
        self.assertTrue(unpacked_large["valid"])
        self.assertEqual(unpacked_large["payload_length"], 241)
        self.assertEqual(len(unpacked_large["payload_bytes"]), 241)

    def test_03_corrupt_frame_detection_and_tamper_rejection(self):
        """Verifies corrupted or truncated frames are strictly rejected."""
        svc = LoraPacketService()
        valid_frame = svc.pack_frame("DEV-TEST", LoraPacketService.TYPE_SOS_ALERT, b"NEED_POWER")

        # Case 1: Corrupt sync byte
        bad_sync = bytearray(valid_frame)
        bad_sync[0] = 0x00
        res1 = svc.unpack_frame(bytes(bad_sync))
        self.assertFalse(res1["valid"])
        self.assertIn("Invalid sync byte", res1["error"])

        # Case 2: Bit flip in payload triggers CRC16 failure
        bad_payload = bytearray(valid_frame)
        bad_payload[14] ^= 0xFF
        res2 = svc.unpack_frame(bytes(bad_payload))
        self.assertFalse(res2["valid"])
        self.assertIn("CRC16 mismatch", res2["error"])

        # Case 3: Truncated frame (< 15 bytes)
        res3 = svc.unpack_frame(valid_frame[:10])
        self.assertFalse(res3["valid"])
        self.assertIn("Frame too short", res3["error"])

    def test_04_semtech_lora_time_on_air_physics_and_scaling(self):
        """Validates Semtech LoRa Time-on-Air (ToA) mathematical formula across SF7 to SF12."""
        payload_size = 50
        toa_sf7 = LoraPacketService.calculate_time_on_air(payload_size, spreading_factor=7)
        toa_sf8 = LoraPacketService.calculate_time_on_air(payload_size, spreading_factor=8)
        toa_sf9 = LoraPacketService.calculate_time_on_air(payload_size, spreading_factor=9)
        toa_sf10 = LoraPacketService.calculate_time_on_air(payload_size, spreading_factor=10)
        toa_sf11 = LoraPacketService.calculate_time_on_air(payload_size, spreading_factor=11)
        toa_sf12 = LoraPacketService.calculate_time_on_air(payload_size, spreading_factor=12)

        # Monotonic increase in airtime with spreading factor
        self.assertLess(toa_sf7["time_on_air_ms"], toa_sf8["time_on_air_ms"])
        self.assertLess(toa_sf8["time_on_air_ms"], toa_sf9["time_on_air_ms"])
        self.assertLess(toa_sf9["time_on_air_ms"], toa_sf10["time_on_air_ms"])
        self.assertLess(toa_sf10["time_on_air_ms"], toa_sf11["time_on_air_ms"])
        self.assertLess(toa_sf11["time_on_air_ms"], toa_sf12["time_on_air_ms"])

        # Low Data Rate Optimization check (triggered when symbol duration > 16ms)
        self.assertFalse(toa_sf7["low_data_rate_opt"])
        self.assertTrue(toa_sf12["low_data_rate_opt"])

    def test_05_battery_consumption_modeling(self):
        """Verifies power and battery longevity calculations."""
        toa_info = LoraPacketService.calculate_time_on_air(30, spreading_factor=7)
        energy_sf7 = LoraPacketService.calculate_energy_consumption(toa_info["time_on_air_ms"])

        toa_info_sf12 = LoraPacketService.calculate_time_on_air(30, spreading_factor=12)
        energy_sf12 = LoraPacketService.calculate_energy_consumption(toa_info_sf12["time_on_air_ms"])

        self.assertGreater(energy_sf12["energy_per_packet_mwh"], energy_sf7["energy_per_packet_mwh"])
        self.assertLess(energy_sf12["packets_per_1000mah_battery"], energy_sf7["packets_per_1000mah_battery"])
        self.assertGreater(energy_sf7["packets_per_1000mah_battery"], 10000)

    def test_06_dtn_queue_buffering_and_acknowledgement_lifecycle(self):
        """Verifies off-grid DTN queue buffer, priority sorting, and ACK transitions."""
        p1 = lora_packet_service.enqueue_dtn_packet("DEV-A", 1, b"Answer 1", priority=1)
        p2 = lora_packet_service.enqueue_dtn_packet("DEV-B", 4, b"Emergency Alert", priority=5)

        queue = lora_packet_service.list_dtn_queue()
        self.assertEqual(len(queue), 2)
        # Priority 5 must come before priority 1
        self.assertEqual(queue[0]["packet_id"], p2["packet_id"])
        self.assertEqual(queue[1]["packet_id"], p1["packet_id"])

        # Acknowledge packet p1
        ack_success = lora_packet_service.acknowledge_packet(p1["packet_id"])
        self.assertTrue(ack_success)

        queued_only = lora_packet_service.list_dtn_queue(status="QUEUED")
        self.assertEqual(len(queued_only), 1)
        self.assertEqual(queued_only[0]["packet_id"], p2["packet_id"])

        ack_only = lora_packet_service.list_dtn_queue(status="ACKNOWLEDGED")
        self.assertEqual(len(ack_only), 1)
        self.assertEqual(ack_only[0]["packet_id"], p1["packet_id"])

        # Acknowledge non-existent packet
        self.assertFalse(lora_packet_service.acknowledge_packet("nonexistent_id"))

    def test_07_solar_station_telemetry_and_node_load(self):
        """Verifies solar station telemetry interrogation and pending queue linkage."""
        chilmari = lora_packet_service.get_solar_station_status("SOLAR-CHAR-CHILMARI-01")
        self.assertIsNotNone(chilmari)
        self.assertEqual(chilmari["station_id"], "SOLAR-CHAR-CHILMARI-01")
        self.assertGreater(chilmari["battery_voltage_v"], 12.0)
        self.assertGreater(chilmari["solar_irradiance_wm2"], 500.0)
        self.assertEqual(chilmari["dtn_pending_packets"], 0)

        # Enqueue packet and re-check pending count
        lora_packet_service.enqueue_dtn_packet("DEV-NODE-99", 1, b"Payload")
        updated = lora_packet_service.get_solar_station_status("SOLAR-CHAR-CHILMARI-01")
        self.assertEqual(updated["dtn_pending_packets"], 1)

        # Non-existent station
        self.assertIsNone(lora_packet_service.get_solar_station_status("UNKNOWN_STATION"))

    async def _test_async_endpoints(self):
        """Helper to run async endpoint unit tests."""
        def extract_content(res):
            if hasattr(res, "body"):
                return json.loads(res.body.decode("utf-8"))
            return getattr(res, "content", {})

        # Test 1: Send packet with text
        res = await send_emergency_lora_packet({
            "device_id": "STU-8821",
            "payload_type": 1,
            "payload_text": "EXAM_ANS:1A,2C,3D",
            "priority": 2
        })
        self.assertEqual(res.status_code, 200)
        data = extract_content(res)
        self.assertTrue(data["success"])
        self.assertIn("packet_id", data["packet"])
        packet_id = data["packet"]["packet_id"]

        # Test 2: Missing device_id raises 400
        with self.assertRaises(HTTPException) as cm:
            await send_emergency_lora_packet({"device_id": ""})
        self.assertEqual(cm.exception.status_code, 400)

        # Test 3: Invalid hex raises 400
        with self.assertRaises(HTTPException) as cm:
            await send_emergency_lora_packet({"device_id": "DEV-01", "payload_hex": "NOT_HEX_XYZ"})
        self.assertEqual(cm.exception.status_code, 400)

        # Test 4: Station status
        stat_res = await get_solar_station_status(station_id="SOLAR-CHAR-CHILMARI-01")
        self.assertEqual(stat_res.status_code, 200)
        stat_data = extract_content(stat_res)
        self.assertEqual(stat_data["station_id"], "SOLAR-CHAR-CHILMARI-01")

        # Test 5: Station status not found
        with self.assertRaises(HTTPException) as cm:
            await get_solar_station_status(station_id="NON_EXISTENT")
        self.assertEqual(cm.exception.status_code, 404)

        # Test 6: List stations
        stations_res = await list_all_solar_stations()
        self.assertEqual(stations_res.status_code, 200)
        stations_data = extract_content(stations_res)
        self.assertGreaterEqual(stations_data["total"], 2)

        # Test 7: List DTN queue
        queue_res = await list_dtn_pending_queue(status_filter=None)
        self.assertEqual(queue_res.status_code, 200)
        queue_data = extract_content(queue_res)
        self.assertGreaterEqual(queue_data["total"], 1)

        # Test 8: Acknowledge DTN packet
        ack_res = await acknowledge_dtn_packet(packet_id)
        self.assertEqual(ack_res.status_code, 200)

        # Test 9: Acknowledge non-existent DTN packet raises 404
        with self.assertRaises(HTTPException) as cm:
            await acknowledge_dtn_packet("invalid_pkt_id_999")
        self.assertEqual(cm.exception.status_code, 404)

    def test_08_rest_api_endpoints_send_telemetry_ack(self):
        """Verifies Phase 106 REST API endpoints through direct async invocation."""
        asyncio.run(self._test_async_endpoints())

    def test_09_developer_architecture_note_and_strict_zero_emoji(self):
        """Verifies Developer Architecture Note headers and strict zero-emoji governance across Phase 106 files."""
        phase106_files = [
            self.service_path,
            self.endpoint_path,
            self.studio_path,
            self.solar_path,
            self.page_path,
            self.tasks_path,
            Path(__file__)
        ]

        for file_path in phase106_files:
            self.assertTrue(file_path.exists(), f"File does not exist: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"Missing Developer Architecture Note in {file_path.name}"
            )
            self.assertIn(
                "Phase 106",
                content,
                f"Missing Phase 106 reference in {file_path.name}"
            )
            self.assertFalse(
                contains_emoji(content),
                f"Strict Zero-Emoji violation detected in {file_path.name}"
            )


if __name__ == "__main__":
    unittest.main()
