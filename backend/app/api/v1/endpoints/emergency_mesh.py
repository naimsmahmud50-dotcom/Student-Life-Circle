"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Rural LoRaWAN Emergency Bridge & Solar Micro-Hub Endpoints
TOPIC:     LoRaWAN Packet Transmission, DTN Buffering & Solar Telemetry Delivery
FILE:      backend/app/api/v1/endpoints/emergency_mesh.py
PHASE:     Phase 106 - Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
PURPOSE:   Provides REST API endpoints for off-grid student exam answer ingestion,
           binary frame packing, Delay-Tolerant Network (DTN) queue management,
           and real-time solar micro-hub station telemetry interrogation.
STANDARDS: Delay-Tolerant Networking (DTN), CRC16 Frame Validation, Zero-Emoji, Field-Grade
"""

from typing import Any, Dict, List, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    HTTPException,
    JSONResponse,
    Query,
    status
)
from backend.app.services.lora_packet_service import lora_packet_service

router = APIRouter(prefix="/emergency", tags=["Rural LoRaWAN Emergency Bridge & Solar Micro-Hub"])


@router.post("/packet/send", status_code=status.HTTP_200_OK)
async def send_emergency_lora_packet(payload: Dict[str, Any]):
    """
    Ingests off-grid student exam answers or emergency alerts, packs a binary frame
    with CRC16 checksum, computes Time-on-Air (ToA), and buffers into the DTN queue.
    """
    device_id = payload.get("device_id")
    if not device_id or not str(device_id).strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'device_id' is required."
        )

    payload_type = int(payload.get("payload_type", 1))
    payload_text = payload.get("payload_text", "")
    payload_hex = payload.get("payload_hex", "")
    priority = int(payload.get("priority", 1))
    ttl_hours = int(payload.get("ttl_hours", 72))

    if payload_hex:
        try:
            raw_bytes = bytes.fromhex(payload_hex)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid hexadecimal payload format in 'payload_hex'."
            )
    elif payload_text:
        raw_bytes = payload_text.encode("utf-8")
    else:
        raw_bytes = b"EMPTY_PAYLOAD"

    entry = lora_packet_service.enqueue_dtn_packet(
        device_id=device_id.strip(),
        payload_type=payload_type,
        raw_payload=raw_bytes,
        priority=priority,
        ttl_hours=ttl_hours
    )

    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "success": True,
        "packet": entry,
        "message": "Packet successfully serialized with CRC16 and queued in Delay-Tolerant Network (DTN)."
    })


@router.get("/station/status", status_code=status.HTTP_200_OK)
async def get_solar_station_status(
    station_id: Optional[str] = Query(None, description="Identifier for remote solar micro-hub station")
):
    """
    Retrieves real-time solar photovoltaic generation (W), battery reserve (%),
    voltage (V), signal RSSI (dBm), and student mesh connections.
    """
    if not station_id:
        station_id = "SOLAR-CHAR-CHILMARI-01"

    status_data = lora_packet_service.get_solar_station_status(station_id)
    if not status_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solar station '{station_id}' was not found in off-grid telemetry registry."
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=status_data)


@router.get("/stations", status_code=status.HTTP_200_OK)
async def list_all_solar_stations():
    """Lists all active rural solar stations across Char and Haor disaster zones."""
    stations = lora_packet_service.list_solar_stations()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"stations": stations, "total": len(stations)})


@router.get("/dtn/queue", status_code=status.HTTP_200_OK)
async def list_dtn_pending_queue(status_filter: Optional[str] = Query(None, alias="status")):
    """Returns buffered delay-tolerant messages pending gateway handshake."""
    queue = lora_packet_service.list_dtn_queue(status=status_filter)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"queue": queue, "total": len(queue)})


@router.post("/dtn/ack/{packet_id}", status_code=status.HTTP_200_OK)
async def acknowledge_dtn_packet(packet_id: str):
    """Marks a buffered packet as acknowledged by cloud uplink gateway."""
    success = lora_packet_service.acknowledge_packet(packet_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Packet '{packet_id}' not found in DTN buffer."
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"success": True, "packet_id": packet_id})
