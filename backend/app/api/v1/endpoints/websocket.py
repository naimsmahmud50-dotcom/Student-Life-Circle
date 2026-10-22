# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 80 - FastAPI WebSocket Endpoints):
# This module defines the production WebSocket endpoints for the Student Life Circle platform.
# Channels:
# 1. /ws/live-challenge/{room_id}: Real-time leaderboard updates, concurrent answer broadcasts,
#    and millisecond-accurate countdown synchronization for live challenges.
# 2. /ws/whiteboard/{circle_id}: Low-latency delta sync for collaborative vector drawing & LaTeX canvas.
# 3. /ws/voice-mesh/{circle_id}: Lightweight SDP offer/answer signaling for peer-to-peer WebRTC audio mesh.
# Security & Standards:
# - Enforces token authentication during handshake (?token=jwt_token). Blocks unauthorized requests.
# - Heartbeat ping/pong (every 30s) and automatic graceful teardown on WebSocketDisconnect.
# - REST diagnostic endpoint /api/v1/websocket/status for connection metrics and health tracking.
# - Strict Zero-Emoji Policy Enforced: All docstrings, schemas, and logs use clean technical English.
# ==============================================================================

from typing import Dict, Any, Optional
from backend.app.core.fastapi_shim import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    Query,
    HTTPException,
    status
)
from backend.app.services.websocket_connection_manager import (
    websocket_manager,
    WebSocketConnectionManager
)

router = APIRouter(prefix="/ws", tags=["WebSockets & Real-Time Signaling"])


# =============================================================================
# 1. Live Challenge Real-Time WebSocket Channel
# =============================================================================
@router.websocket("/live-challenge/{room_id}")
async def websocket_live_challenge(
    websocket: WebSocket,
    room_id: str,
    token: Optional[str] = Query(None)
):
    """
    WebSocket channel for live competitive challenges:
    - Real-time leaderboard updates
    - Concurrent answer broadcasts
    - Millisecond-accurate countdown synchronization
    """
    # 1. Authenticate Handshake Token
    auth_result = websocket_manager.authenticate_handshake(token, "live_challenge", room_id)
    if not auth_result.get("authenticated", False):
        await websocket.close(
            code=auth_result.get("close_code", status.WS_1008_POLICY_VIOLATION),
            reason=auth_result.get("reason", "HANDSHAKE_DENIED")
        )
        return

    user_id = auth_result["user_id"]
    role = auth_result["role"]
    tenant_id = auth_result["tenant_id"]

    # 2. Accept & Register Connection
    conn_id = await websocket_manager.connect(
        websocket=websocket,
        channel_type="live_challenge",
        room_or_circle_id=room_id,
        user_id=user_id,
        role=role,
        tenant_id=tenant_id
    )

    try:
        while True:
            data = await websocket.receive_json()

            # Handle Heartbeat Keepalive
            if data.get("type") == "ping":
                await websocket_manager.handle_heartbeat_ping(websocket, conn_id, data)
                continue

            # Route Domain Message
            response = await websocket_manager.handle_live_challenge_message(room_id, user_id, data)
            await websocket.send_json(response)

    except WebSocketDisconnect:
        await websocket_manager.disconnect(conn_id, "live_challenge", room_id)
    except Exception:
        await websocket_manager.disconnect(conn_id, "live_challenge", room_id)


# =============================================================================
# 2. Collaborative Whiteboard & LaTeX Canvas Channel
# =============================================================================
@router.websocket("/whiteboard/{circle_id}")
async def websocket_whiteboard(
    websocket: WebSocket,
    circle_id: str,
    token: Optional[str] = Query(None)
):
    """
    WebSocket channel for collaborative whiteboard sessions:
    - Low-latency vector drawing delta sync
    - Mathematical LaTeX node positioning and updates
    """
    auth_result = websocket_manager.authenticate_handshake(token, "whiteboard", circle_id)
    if not auth_result.get("authenticated", False):
        await websocket.close(
            code=auth_result.get("close_code", status.WS_1008_POLICY_VIOLATION),
            reason=auth_result.get("reason", "HANDSHAKE_DENIED")
        )
        return

    user_id = auth_result["user_id"]
    role = auth_result["role"]
    tenant_id = auth_result["tenant_id"]

    conn_id = await websocket_manager.connect(
        websocket=websocket,
        channel_type="whiteboard",
        room_or_circle_id=circle_id,
        user_id=user_id,
        role=role,
        tenant_id=tenant_id
    )

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "ping":
                await websocket_manager.handle_heartbeat_ping(websocket, conn_id, data)
                continue

            response = await websocket_manager.handle_whiteboard_message(circle_id, user_id, data)
            await websocket.send_json(response)

    except WebSocketDisconnect:
        await websocket_manager.disconnect(conn_id, "whiteboard", circle_id)
    except Exception:
        await websocket_manager.disconnect(conn_id, "whiteboard", circle_id)


# =============================================================================
# 3. WebRTC Peer Voice Mesh Signaling Channel
# =============================================================================
@router.websocket("/voice-mesh/{circle_id}")
async def websocket_voice_mesh(
    websocket: WebSocket,
    circle_id: str,
    token: Optional[str] = Query(None)
):
    """
    WebSocket channel for P2P WebRTC audio mesh signaling:
    - Lightweight SDP Offer / Answer exchange
    - ICE candidate trickle routing
    - Voice Activity Detection (VAD) and mute state notifications
    """
    auth_result = websocket_manager.authenticate_handshake(token, "voice_mesh", circle_id)
    if not auth_result.get("authenticated", False):
        await websocket.close(
            code=auth_result.get("close_code", status.WS_1008_POLICY_VIOLATION),
            reason=auth_result.get("reason", "HANDSHAKE_DENIED")
        )
        return

    user_id = auth_result["user_id"]
    role = auth_result["role"]
    tenant_id = auth_result["tenant_id"]

    conn_id = await websocket_manager.connect(
        websocket=websocket,
        channel_type="voice_mesh",
        room_or_circle_id=circle_id,
        user_id=user_id,
        role=role,
        tenant_id=tenant_id
    )

    try:
        while True:
            data = await websocket.receive_json()

            if data.get("type") == "ping":
                await websocket_manager.handle_heartbeat_ping(websocket, conn_id, data)
                continue

            response = await websocket_manager.handle_voice_mesh_message(circle_id, user_id, data)
            await websocket.send_json(response)

    except WebSocketDisconnect:
        await websocket_manager.disconnect(conn_id, "voice_mesh", circle_id)
    except Exception:
        await websocket_manager.disconnect(conn_id, "voice_mesh", circle_id)


# =============================================================================
# 4. REST Diagnostic & Health Monitoring Routes
# =============================================================================
@router.get("/status")
async def get_websocket_cluster_status():
    """
    Diagnostic status endpoint returning active connection pool stats,
    channel counts, broadcast latency benchmarks, and Pub/Sub cluster state.
    """
    return websocket_manager.get_manager_stats()


@router.post("/broadcast")
async def trigger_server_authoritative_broadcast(payload: Dict[str, Any]):
    """
    Allows server-side workers to push authoritative broadcasts to connected clients.
    """
    channel_type = payload.get("channel_type", "live_challenge")
    target_id = payload.get("target_id", "default")
    message = payload.get("message", {})

    delivered = await websocket_manager.broadcast_to_channel(channel_type, target_id, message)
    return {
        "status": "DELIVERED",
        "channel_type": channel_type,
        "target_id": target_id,
        "delivered_connections": delivered
    }
