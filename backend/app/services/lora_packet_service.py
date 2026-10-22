"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
TOPIC:     Binary Packet Packing, CRC16 Checksum & Delay-Tolerant Networking (DTN)
FILE:      backend/app/services/lora_packet_service.py
PHASE:     Phase 106 - Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
PURPOSE:   Encodes student exam answers into ultra-compact binary frames (<= 256 bytes),
           computes CRC16 validation checksums, models Semtech LoRa Time-on-Air (ToA)
           and battery consumption, and manages off-grid DTN store-and-forward queues.
STANDARDS: Delay-Tolerant Networking (DTN), CRC16 Frame Validation, Zero-Emoji, Field-Grade
"""

import math
import struct
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


def compute_crc16(data: bytes) -> int:
    """
    Computes CRC-16-CCITT (polynomial 0x1021, initial value 0xFFFF).
    Returns 16-bit unsigned integer checksum.
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


class LoraPacketService:
    """
    Field-Grade LoRaWAN Packet Engineering & Delay-Tolerant Networking (DTN) Service.
    """

    MAX_FRAME_SIZE = 256
    SYNC_BYTE = 0x7E

    # Payload Types
    TYPE_EXAM_ANSWER = 0x01
    TYPE_STUDENT_PRESENCE = 0x02
    TYPE_SOLAR_TELEMETRY = 0x03
    TYPE_SOS_ALERT = 0x04

    def __init__(self) -> None:
        self._dtn_queue: Dict[str, Dict[str, Any]] = {}
        self._sequence_counter = 1
        self._solar_stations: Dict[str, Dict[str, Any]] = {
            "SOLAR-CHAR-CHILMARI-01": {
                "station_id": "SOLAR-CHAR-CHILMARI-01",
                "location_name": "চিলমারী ব্রহ্মপুত্র চরে স্থাপিত সোলার মাইক্রো-হাব",
                "region": "কুড়িগ্রাম (Kurigram)",
                "battery_voltage_v": 13.25,
                "battery_soc_percent": 94.0,
                "solar_irradiance_wm2": 720.0,
                "pv_power_w": 88.5,
                "load_power_w": 14.2,
                "system_temperature_c": 28.5,
                "connected_student_nodes": 18,
                "channel_frequency_mhz": 868.1,
                "signal_rssi_dbm": -96.0,
                "snr_db": 7.5,
                "gateway_online": True,
                "last_handshake": datetime.now(timezone.utc).isoformat(),
            },
            "SOLAR-HAOR-SUNAMGANJ-02": {
                "station_id": "SOLAR-HAOR-SUNAMGANJ-02",
                "location_name": "তাহিরপুর হাওর জরুরি শিক্ষা সম্প্রচার স্টেশন",
                "region": "সুনামগঞ্জ (Sunamganj)",
                "battery_voltage_v": 12.80,
                "battery_soc_percent": 82.5,
                "solar_irradiance_wm2": 610.0,
                "pv_power_w": 72.0,
                "load_power_w": 16.0,
                "system_temperature_c": 26.0,
                "connected_student_nodes": 12,
                "channel_frequency_mhz": 868.3,
                "signal_rssi_dbm": -104.0,
                "snr_db": 4.2,
                "gateway_online": False,  # Off-grid DTN buffering mode
                "last_handshake": datetime.now(timezone.utc).isoformat(),
            }
        }

    # --------------------------------------------------------------------------
    # 1. Binary Frame Serialization & CRC16 Verification
    # --------------------------------------------------------------------------

    def pack_frame(
        self,
        device_id: str,
        payload_type: int,
        payload_data: bytes,
        sequence_num: Optional[int] = None
    ) -> bytes:
        """
        Packs a compact binary LoRa frame (<= 256 bytes) with CRC16 checksum.
        Format:
        [Sync: 1B] [Seq: 2B] [DeviceID: 8B] [Type: 1B] [Len: 1B] [Payload: NB] [CRC16: 2B]
        """
        if sequence_num is None:
            sequence_num = self._sequence_counter
            self._sequence_counter = (self._sequence_counter + 1) & 0xFFFF

        # Truncate or pad device ID to exact 8 bytes
        dev_bytes = device_id.encode("utf-8")[:8].ljust(8, b"\x00")
        payload_len = len(payload_data)

        # Header + Device + Type + Len = 1 + 2 + 8 + 1 + 1 = 13 bytes. Plus 2 bytes CRC16 = 15 bytes overhead.
        max_payload = self.MAX_FRAME_SIZE - 15
        if payload_len > max_payload:
            payload_data = payload_data[:max_payload]
            payload_len = max_payload

        # Header payload without CRC16
        header = struct.pack(">BH8sBB", self.SYNC_BYTE, sequence_num, dev_bytes, payload_type, payload_len)
        data_to_checksum = header + payload_data

        checksum = compute_crc16(data_to_checksum)
        full_frame = data_to_checksum + struct.pack(">H", checksum)

        assert len(full_frame) <= self.MAX_FRAME_SIZE, f"Frame size {len(full_frame)} exceeds 256 bytes"
        return full_frame

    def unpack_frame(self, frame: bytes) -> Dict[str, Any]:
        """
        Deserializes a LoRa binary frame, asserts sync byte, and verifies CRC16 checksum.
        """
        if len(frame) < 15:
            return {"valid": False, "error": "Frame too short (minimum 15 bytes required)"}

        if len(frame) > self.MAX_FRAME_SIZE:
            return {"valid": False, "error": f"Frame exceeds maximum size ({len(frame)} > 256 bytes)"}

        # Check sync byte
        if frame[0] != self.SYNC_BYTE:
            return {"valid": False, "error": f"Invalid sync byte 0x{frame[0]:02X} (expected 0x{self.SYNC_BYTE:02X})"}

        # Extract checksum from last 2 bytes
        received_crc = struct.unpack(">H", frame[-2:])[0]
        payload_to_verify = frame[:-2]
        computed_crc = compute_crc16(payload_to_verify)

        if received_crc != computed_crc:
            return {
                "valid": False,
                "error": f"CRC16 mismatch: received 0x{received_crc:04X}, computed 0x{computed_crc:04X}"
            }

        # Unpack header fields
        sync, seq, dev_bytes, payload_type, payload_len = struct.unpack(">BH8sBB", frame[:13])
        device_id = dev_bytes.decode("utf-8", errors="ignore").rstrip("\x00")
        actual_payload = frame[13:-2]

        return {
            "valid": True,
            "sequence_number": seq,
            "device_id": device_id,
            "payload_type": payload_type,
            "payload_length": len(actual_payload),
            "payload_bytes": actual_payload,
            "crc16_hex": f"0x{received_crc:04X}",
            "frame_size_bytes": len(frame)
        }

    # --------------------------------------------------------------------------
    # 2. Time-on-Air (ToA) & Radio Energy Physical Math
    # --------------------------------------------------------------------------

    @staticmethod
    def calculate_time_on_air(
        payload_bytes: int,
        spreading_factor: int = 7,
        bandwidth_hz: int = 125000,
        coding_rate: int = 1,
        preamble_length: int = 8,
        explicit_header: bool = True,
        low_data_rate_opt: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Computes exact Semtech LoRa Time-on-Air (ToA) in milliseconds.
        Formulas:
        T_sym = 2^SF / BW
        T_preamble = (N_preamble + 4.25) * T_sym
        Payload_symbols = 8 + max(ceil((8*PL - 4*SF + 28 + 16 - 20*H) / (4*(SF - 2*DE))) * (CR + 4), 0)
        """
        sf = max(7, min(12, spreading_factor))
        bw = float(bandwidth_hz)
        cr = max(1, min(4, coding_rate))
        n_preamble = float(preamble_length)

        # Symbol duration in seconds
        t_sym = (2.0 ** sf) / bw

        # Auto-enable Low Data Rate Optimization if symbol duration > 16ms
        if low_data_rate_opt is None:
            low_data_rate_opt = (t_sym > 0.016)
        de = 1 if low_data_rate_opt else 0
        h = 0 if explicit_header else 1

        # Preamble duration
        t_preamble = (n_preamble + 4.25) * t_sym

        # Payload symbols calculation
        numerator = 8.0 * payload_bytes - 4.0 * sf + 28.0 + 16.0 - 20.0 * h
        denominator = 4.0 * (sf - 2.0 * de)

        if denominator <= 0:
            denominator = 1.0

        terms = math.ceil(max(0.0, numerator) / denominator) * (cr + 4)
        n_payload = 8.0 + max(0.0, terms)
        t_payload = n_payload * t_sym

        # Total Time on Air in milliseconds
        total_toa_sec = t_preamble + t_payload
        total_toa_ms = round(total_toa_sec * 1000.0, 2)

        return {
            "spreading_factor": sf,
            "bandwidth_khz": bw / 1000.0,
            "payload_bytes": payload_bytes,
            "symbol_duration_ms": round(t_sym * 1000.0, 3),
            "preamble_duration_ms": round(t_preamble * 1000.0, 2),
            "payload_duration_ms": round(t_payload * 1000.0, 2),
            "time_on_air_ms": total_toa_ms,
            "low_data_rate_opt": low_data_rate_opt
        }

    @staticmethod
    def calculate_energy_consumption(
        time_on_air_ms: float,
        supply_voltage_v: float = 3.3,
        tx_current_ma: float = 120.0
    ) -> Dict[str, Any]:
        """
        Models energy consumption in milliwatt-hours (mWh) and battery longevity.
        Energy (mWh) = (V * I_tx * ToA_sec) / 3600
        """
        toa_sec = time_on_air_ms / 1000.0
        power_mw = supply_voltage_v * tx_current_ma
        energy_mwh = (power_mw * toa_sec) / 3600.0

        # Packets per 1000 mAh single cell battery
        total_battery_mwh = supply_voltage_v * 1000.0
        packets_per_charge = int(total_battery_mwh / max(energy_mwh, 0.00001))

        return {
            "supply_voltage_v": supply_voltage_v,
            "tx_current_ma": tx_current_ma,
            "power_mw": round(power_mw, 2),
            "energy_per_packet_mwh": round(energy_mwh, 5),
            "packets_per_1000mah_battery": packets_per_charge
        }

    # --------------------------------------------------------------------------
    # 3. Delay-Tolerant Networking (DTN) Queue
    # --------------------------------------------------------------------------

    def enqueue_dtn_packet(
        self,
        device_id: str,
        payload_type: int,
        raw_payload: bytes,
        priority: int = 1,
        ttl_hours: int = 72
    ) -> Dict[str, Any]:
        """
        Buffers a student submission in the off-grid DTN store-and-forward queue.
        """
        packet_id = f"pkt_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc).isoformat()

        frame = self.pack_frame(device_id, payload_type, raw_payload)
        toa_info = self.calculate_time_on_air(len(frame))

        entry: Dict[str, Any] = {
            "packet_id": packet_id,
            "device_id": device_id,
            "payload_type": payload_type,
            "priority": priority,
            "enqueued_at": now,
            "ttl_hours": ttl_hours,
            "status": "QUEUED",
            "frame_bytes_len": len(frame),
            "time_on_air_ms": toa_info["time_on_air_ms"],
            "raw_frame_hex": frame.hex(),
            "retry_count": 0,
        }
        self._dtn_queue[packet_id] = entry
        return entry

    def list_dtn_queue(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists pending or forwarded DTN packets."""
        items = list(self._dtn_queue.values())
        if status:
            items = [it for it in items if it["status"] == status]
        return sorted(items, key=lambda x: (-x["priority"], x["enqueued_at"]))

    def acknowledge_packet(self, packet_id: str) -> bool:
        """Marks a packet as successfully uplinked to central cloud."""
        if packet_id in self._dtn_queue:
            self._dtn_queue[packet_id]["status"] = "ACKNOWLEDGED"
            self._dtn_queue[packet_id]["delivered_at"] = datetime.now(timezone.utc).isoformat()
            return True
        return False

    # --------------------------------------------------------------------------
    # 4. Solar Station Health & Telemetry
    # --------------------------------------------------------------------------

    def get_solar_station_status(self, station_id: str) -> Optional[Dict[str, Any]]:
        """Returns physical solar station battery, voltage, and mesh load telemetry."""
        station = self._solar_stations.get(station_id)
        if not station:
            return None

        # Count pending DTN packets for this hub
        station_copy = dict(station)
        pending = len([p for p in self._dtn_queue.values() if p["status"] == "QUEUED"])
        station_copy["dtn_pending_packets"] = pending
        return station_copy

    def list_solar_stations(self) -> List[Dict[str, Any]]:
        """Returns all registered off-grid rural solar stations."""
        return [self.get_solar_station_status(sid) for sid in self._solar_stations.keys()]

    def reset_for_testing(self) -> None:
        """Clears stored DTN packets for test isolation."""
        self._dtn_queue.clear()
        self._sequence_counter = 1


# Global Singleton Service
lora_packet_service = LoraPacketService()
