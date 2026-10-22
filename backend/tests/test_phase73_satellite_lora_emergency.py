"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Test Suite: Autonomous Satellite USSD & LoRa Long-Range Emergency Gateway
FILE:      backend/tests/test_phase73_satellite_lora_emergency.py
PURPOSE:   Comprehensive unit and integration test suite validating:
           1. 160-character USSD state machine transitions, menu flows, quiz prompts,
              and strict GSM 7-bit character budget compliance.
           2. Compact binary LoRaWAN packet frame encoding, CRC16 attestation,
              Spreading Factor (SF7 vs SF12) airtime scaling, and link budget math.
           3. Delay-Tolerant Networking (DTN) store-and-forward queue staging.
           4. Off-grid solar station photovoltaic and battery telemetry integrity.
           5. Section 72 REST API router endpoints.
STANDARDS: 100% assertions coverage, zero emojis, ASVS L2 compliance.
========================================================================================
"""

import asyncio
import unittest

from backend.app.schemas.satellite_lora_emergency_schema import (
    UssdSessionStateEnum,
    LoraSpreadingFactorEnum,
    TransmissionMediumEnum,
    UssdMenuRequest,
    LoraPacketEncodeRequest,
)
from backend.app.services.satellite_lora_emergency_service import (
    SatelliteLoraEmergencyService,
    compute_crc16_ccitt,
    satellite_lora_emergency_service
)
from backend.app.api.v1.router import (
    handle_ussd_menu_session_endpoint,
    encode_lora_packet_frame_endpoint,
    enqueue_dtn_mutation_endpoint,
    list_remote_solar_stations_endpoint,
    get_satellite_lora_status_endpoint
)


class TestSatelliteLoraEmergencyGateway(unittest.TestCase):
    """
    Test cases asserting the accuracy, physical radio telemetry, and USSD state machine
    for off-grid riverine Char schools and disaster-resilient educational infrastructure.
    """

    def setUp(self):
        self.service = SatelliteLoraEmergencyService()

    def test_ussd_initial_session_and_char_boundary(self):
        """Verify initial USSD dial (*999#) returns valid menu <= 160 characters."""
        req = UssdMenuRequest(
            session_id="SESS-001",
            phone_number_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            user_input="*999#",
            current_state=UssdSessionStateEnum.INITIAL
        )
        resp = self.service.handle_ussd_session(req)
        self.assertEqual(resp.next_state, UssdSessionStateEnum.MENU_NAV)
        self.assertFalse(resp.should_close_session)
        self.assertLessEqual(resp.char_count, 160)
        self.assertGreaterEqual(resp.char_budget_remaining, 0)
        self.assertIn("Agrojatra Micro-Learn", resp.display_text)

    def test_ussd_menu_navigation_to_quiz(self):
        """Verify navigation from root menu into MCQ quiz prompt."""
        req = UssdMenuRequest(
            session_id="SESS-002",
            phone_number_hash="hash-123",
            user_input="1",
            current_state=UssdSessionStateEnum.MENU_NAV
        )
        resp = self.service.handle_ussd_session(req)
        self.assertEqual(resp.next_state, UssdSessionStateEnum.QUESTION_PROMPT)
        self.assertLessEqual(resp.char_count, 160)
        self.assertIn("Farad", resp.display_text)

    def test_ussd_quiz_answer_evaluation_correct(self):
        """Verify answering Farad (option 2) awards marks in 160-char payload."""
        req = UssdMenuRequest(
            session_id="SESS-003",
            phone_number_hash="hash-123",
            user_input="2",
            current_state=UssdSessionStateEnum.QUESTION_PROMPT
        )
        resp = self.service.handle_ussd_session(req)
        self.assertEqual(resp.next_state, UssdSessionStateEnum.SCORE_SUMMARY)
        self.assertIn("Correct", resp.display_text)
        self.assertLessEqual(resp.char_count, 160)

    def test_ussd_quiz_answer_evaluation_incorrect(self):
        """Verify incorrect option returns constructive review advice."""
        req = UssdMenuRequest(
            session_id="SESS-004",
            phone_number_hash="hash-123",
            user_input="1",
            current_state=UssdSessionStateEnum.QUESTION_PROMPT
        )
        resp = self.service.handle_ussd_session(req)
        self.assertIn("Incorrect", resp.display_text)
        self.assertEqual(resp.next_state, UssdSessionStateEnum.SCORE_SUMMARY)

    def test_ussd_session_exit_and_termination(self):
        """Verify hash input gracefully closes the session."""
        req = UssdMenuRequest(
            session_id="SESS-005",
            phone_number_hash="hash-123",
            user_input="#",
            current_state=UssdSessionStateEnum.SCORE_SUMMARY
        )
        resp = self.service.handle_ussd_session(req)
        self.assertTrue(resp.should_close_session)
        self.assertEqual(resp.next_state, UssdSessionStateEnum.TERMINATED)

    def test_lora_packet_encoding_and_crc16(self):
        """Verify binary packet framing starts with 0x7E and includes verified CRC16."""
        req = LoraPacketEncodeRequest(
            station_id="STN-CHAR-01",
            student_did="did:agro:student:char01948",
            quiz_id="QUIZ-PHYS-001",
            selected_option_index=2,
            spreading_factor=LoraSpreadingFactorEnum.SF9,
            bandwidth_khz=125.0
        )
        resp = self.service.encode_lora_packet(req)
        self.assertTrue(resp.raw_payload_hex.startswith("7E"))
        self.assertGreater(resp.payload_bytes_len, 8)
        self.assertEqual(len(resp.crc16_checksum), 4)

        # Verify CRC matches payload bytes
        packet_bytes = bytes.fromhex(resp.raw_payload_hex)
        computed_crc = compute_crc16_ccitt(packet_bytes[:-2])
        self.assertEqual(resp.crc16_checksum, computed_crc)

    def test_lora_spreading_factor_time_on_air_scaling(self):
        """Verify higher spreading factors yield longer airtime but greater link budget."""
        req_sf7 = LoraPacketEncodeRequest(
            station_id="STN-CHAR-01",
            student_did="did:agro:student:test",
            quiz_id="Q-1",
            selected_option_index=1,
            spreading_factor=LoraSpreadingFactorEnum.SF7
        )
        req_sf12 = LoraPacketEncodeRequest(
            station_id="STN-CHAR-01",
            student_did="did:agro:student:test",
            quiz_id="Q-1",
            selected_option_index=1,
            spreading_factor=LoraSpreadingFactorEnum.SF12
        )
        resp_sf7 = self.service.encode_lora_packet(req_sf7)
        resp_sf12 = self.service.encode_lora_packet(req_sf12)

        self.assertLess(resp_sf7.estimated_time_on_air_ms, resp_sf12.estimated_time_on_air_ms)
        self.assertLess(resp_sf7.link_budget_dbm, resp_sf12.link_budget_dbm)

    def test_dtn_queue_buffering_and_backlog(self):
        """Verify delay-tolerant store-and-forward queue buffering."""
        item = self.service.enqueue_dtn_mutation(
            station_id="STN-CHAR-01",
            payload_type="ATTENDANCE_PUNCH",
            data={"did": "did:agro:123", "punch_epoch": 1729000000}
        )
        self.assertTrue(item.item_id.startswith("DTN-"))
        self.assertEqual(item.station_id, "STN-CHAR-01")
        self.assertFalse(item.is_delivered)

    def test_remote_solar_stations_telemetry(self):
        """Verify 5 remote off-grid solar stations have nominal voltages and battery levels."""
        stations = self.service.get_remote_stations()
        self.assertEqual(len(stations), 5)
        for stn in stations:
            self.assertGreater(stn.battery_level_percent, 50.0)
            self.assertGreater(stn.battery_voltage_volts, 12.0)
            self.assertGreater(stn.solar_pv_input_watts, 20.0)

    def test_rest_api_endpoints(self):
        """Verify Section 72 REST API endpoints return 200 OK responses."""
        ussd_req = UssdMenuRequest(
            session_id="SESS-API-01",
            phone_number_hash="hash-api",
            user_input="*999#",
            current_state=UssdSessionStateEnum.INITIAL
        )
        ussd_resp = asyncio.run(handle_ussd_menu_session_endpoint(ussd_req))
        self.assertEqual(ussd_resp.session_id, "SESS-API-01")

        lora_req = LoraPacketEncodeRequest(
            station_id="STN-WET-02",
            student_did="did:agro:student:haor01",
            quiz_id="Q-HAOR-1",
            selected_option_index=3,
            spreading_factor=LoraSpreadingFactorEnum.SF8
        )
        lora_resp = asyncio.run(encode_lora_packet_frame_endpoint(lora_req))
        self.assertEqual(lora_resp.station_id, "STN-WET-02")

        dtn_item = asyncio.run(enqueue_dtn_mutation_endpoint(station_id="STN-ISL-03"))
        self.assertEqual(dtn_item.station_id, "STN-ISL-03")

        stations = asyncio.run(list_remote_solar_stations_endpoint())
        self.assertGreaterEqual(len(stations), 5)

        status_resp = asyncio.run(get_satellite_lora_status_endpoint())
        self.assertTrue(status_resp.operational)
        self.assertGreater(status_resp.active_remote_stations, 0)


if __name__ == "__main__":
    unittest.main()
