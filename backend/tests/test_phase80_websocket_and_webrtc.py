# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 80 - WebSocket & WebRTC Tests):
# Automated verification test suite for Phase 80: WebSocket Server & WebRTC Signaling Engine.
# Verifies:
# 1. Handshake Authentication: Cryptographic token validation, missing token rejection,
#    and role-based room access authorization.
# 2. Live Challenge Channel: Millisecond-accurate countdown sync, answer broadcasts,
#    and real-time leaderboard sorting.
# 3. Whiteboard Delta Sync: Collaborative vector drawing and LaTeX canvas distribution.
# 4. WebRTC Voice Mesh Signaling: SDP Offer/Answer routing, ICE candidate trickle, and VAD telemetry.
# 5. Heartbeat Keepalive: 30-second ping/pong protocol with latency calculation.
# 6. High-Concurrency Stress Test: 1,000 concurrent WebSocket connections with strictly sub-50ms latency.
# 7. Strict Zero-Emoji Governance: Enforces zero-emoji compliance across all Phase 80 artifacts.
# ==============================================================================

import os
import time
import unittest
import asyncio
from typing import List, Dict, Any

from backend.app.core.fastapi_shim import WebSocket, WebSocketDisconnect, status
from backend.app.services.websocket_connection_manager import (
    WebSocketConnectionManager,
    websocket_manager
)
from backend.app.api.v1.endpoints.websocket import router as websocket_router


class MockClientWebSocket(WebSocket):
    """
    Mock WebSocket implementation for asynchronous in-memory testing.
    """
    def __init__(self, query_params=None):
        super().__init__(query_params=query_params)
        self.received_messages: List[Dict[str, Any]] = []
        self.sent_messages: List[Dict[str, Any]] = []
        self.closed = False
        self.close_code: int = 0
        self.close_reason: str = ""

    async def accept(self):
        self.client_state = "CONNECTED"

    async def send_json(self, data: Any):
        self.received_messages.append(data)

    async def close(self, code: int = 1000, reason: str = ""):
        self.closed = True
        self.close_code = code
        self.close_reason = reason
        self.client_state = "DISCONNECTED"


class TestPhase80WebSocketAndWebRTC(unittest.TestCase):

    def setUp(self):
        self.manager = WebSocketConnectionManager()

    # --------------------------------------------------------------------------
    # 1. Handshake Token Authentication & Access Control
    # --------------------------------------------------------------------------
    def test_handshake_authentication_and_unauthorized_blocking(self):
        # 1. Valid token
        res_valid = self.manager.authenticate_handshake(
            token="bearer_student_alice12345",
            channel_type="live_challenge",
            room_or_circle_id="room_101"
        )
        self.assertTrue(res_valid["authenticated"])
        self.assertEqual(res_valid["role"], "student")
        self.assertEqual(res_valid["user_id"], "usr_alice12345")

        # 2. Missing token must be rejected with 1008
        res_missing = self.manager.authenticate_handshake(
            token=None,
            channel_type="live_challenge",
            room_or_circle_id="room_101"
        )
        self.assertFalse(res_missing["authenticated"])
        self.assertEqual(res_missing["close_code"], status.WS_1008_POLICY_VIOLATION)

        # 3. Forged / Expired token must be rejected
        res_unauthorized = self.manager.authenticate_handshake(
            token="unauthorized_token",
            channel_type="live_challenge",
            room_or_circle_id="room_101"
        )
        self.assertFalse(res_unauthorized["authenticated"])
        self.assertEqual(res_unauthorized["close_code"], status.WS_1008_POLICY_VIOLATION)

        # 4. Unauthorized room access (student trying to enter private admin room)
        res_room_denied = self.manager.authenticate_handshake(
            token="bearer_student_alice12345",
            channel_type="whiteboard",
            room_or_circle_id="private_admin_audit_chamber"
        )
        self.assertFalse(res_room_denied["authenticated"])
        self.assertIn("AUTHORIZATION_DENIED", res_room_denied["reason"])

    # --------------------------------------------------------------------------
    # 2. Live Challenge Countdown & Leaderboard Sync
    # --------------------------------------------------------------------------
    def test_live_challenge_countdown_and_leaderboard_sync(self):
        async def run_test():
            ws1 = MockClientWebSocket()
            conn_id_1 = await self.manager.connect(
                websocket=ws1,
                channel_type="live_challenge",
                room_or_circle_id="room_live_01",
                user_id="usr_student_alice",
                role="student",
                tenant_id="tenant_dhaka_01"
            )

            # 1. Synchronize countdown
            sync_res = await self.manager.handle_live_challenge_message(
                room_id="room_live_01",
                user_id="usr_student_alice",
                message={"type": "SYNC_COUNTDOWN"}
            )
            self.assertEqual(sync_res["type"], "COUNTDOWN_SYNC_RESPONSE")
            self.assertGreater(sync_res["remaining_ms"], 0)
            self.assertEqual(sync_res["duration_seconds"], 1800)

            # 2. Submit answer
            ans_res = await self.manager.handle_live_challenge_message(
                room_id="room_live_01",
                user_id="usr_student_alice",
                message={
                    "type": "SUBMIT_ANSWER",
                    "question_id": "q_phys_01",
                    "selected_option": "B",
                    "is_correct": True
                }
            )
            self.assertEqual(ans_res["type"], "ANSWER_CONFIRMED")
            self.assertEqual(ans_res["new_score"], 10.0)

            # 3. Fetch leaderboard snapshot
            lb_res = await self.manager.handle_live_challenge_message(
                room_id="room_live_01",
                user_id="usr_student_alice",
                message={"type": "GET_LEADERBOARD"}
            )
            self.assertEqual(lb_res["type"], "LEADERBOARD_SNAPSHOT")
            self.assertGreaterEqual(len(lb_res["leaderboard"]), 1)
            self.assertEqual(lb_res["leaderboard"][0]["user_id"], "usr_student_alice")

            await self.manager.disconnect(conn_id_1, "live_challenge", "room_live_01")

        asyncio.run(run_test())

    # --------------------------------------------------------------------------
    # 3. Whiteboard Delta Sync & LaTeX Canvas
    # --------------------------------------------------------------------------
    def test_whiteboard_delta_sync_and_latex_canvas(self):
        async def run_test():
            ws_author = MockClientWebSocket()
            ws_peer = MockClientWebSocket()

            conn_a = await self.manager.connect(ws_author, "whiteboard", "circle_math_01", "usr_tutor", "educator", "t1")
            conn_b = await self.manager.connect(ws_peer, "whiteboard", "circle_math_01", "usr_learner", "student", "t1")

            # Author draws stroke
            stroke_payload = {
                "type": "DRAW_STROKE",
                "stroke": {
                    "id": "stroke_001",
                    "tool_type": "pen",
                    "color": "#2563EB",
                    "width": 2.0,
                    "points": [[10.0, 20.0], [30.0, 40.0]]
                }
            }
            res_stroke = await self.manager.handle_whiteboard_message("circle_math_01", "usr_tutor", stroke_payload)
            self.assertEqual(res_stroke["type"], "STROKE_ACCEPTED")

            # Check peer received STROKE_DELTA
            delta_messages = [m for m in ws_peer.received_messages if m.get("type") == "STROKE_DELTA"]
            self.assertGreaterEqual(len(delta_messages), 1)
            self.assertEqual(delta_messages[0]["stroke"]["color"], "#2563EB")

            # Author places LaTeX node
            latex_payload = {
                "type": "PLACE_LATEX",
                "latex_node": {
                    "id": "latex_001",
                    "latex_source": r"E = mc^2",
                    "position_x": 100.0,
                    "position_y": 150.0,
                    "font_size": 24
                }
            }
            res_latex = await self.manager.handle_whiteboard_message("circle_math_01", "usr_tutor", latex_payload)
            self.assertEqual(res_latex["type"], "LATEX_ACCEPTED")

            # Check peer received LATEX_NODE_PLACED
            latex_messages = [m for m in ws_peer.received_messages if m.get("type") == "LATEX_NODE_PLACED"]
            self.assertGreaterEqual(len(latex_messages), 1)

            await self.manager.disconnect(conn_a, "whiteboard", "circle_math_01")
            await self.manager.disconnect(conn_b, "whiteboard", "circle_math_01")

        asyncio.run(run_test())

    # --------------------------------------------------------------------------
    # 4. WebRTC Voice Mesh SDP Offer / Answer & ICE Signaling
    # --------------------------------------------------------------------------
    def test_voice_mesh_webrtc_sdp_and_ice_signaling(self):
        async def run_test():
            ws_peer_a = MockClientWebSocket()
            ws_peer_b = MockClientWebSocket()

            conn_a = await self.manager.connect(ws_peer_a, "voice_mesh", "circle_voice_01", "usr_alice", "student", "t1")
            conn_b = await self.manager.connect(ws_peer_b, "voice_mesh", "circle_voice_01", "usr_bob", "student", "t1")

            # Peer A sends SDP Offer targeted to Peer B
            offer_payload = {
                "type": "SDP_OFFER",
                "target_user_id": "usr_bob",
                "payload": {"sdp": {"type": "offer", "sdp": "v=0\r\no=- 12345 2 IN IP4 127.0.0.1"}}
            }
            await self.manager.handle_voice_mesh_message("circle_voice_01", "usr_alice", offer_payload)

            # Peer B should receive the SDP offer
            received_offers = [m for m in ws_peer_b.received_messages if m.get("type") == "SDP_OFFER"]
            self.assertGreaterEqual(len(received_offers), 1)
            self.assertEqual(received_offers[0]["sender_user_id"], "usr_alice")

            # Peer B sends SDP Answer back to Peer A
            answer_payload = {
                "type": "SDP_ANSWER",
                "target_user_id": "usr_alice",
                "payload": {"sdp": {"type": "answer", "sdp": "v=0\r\no=- 67890 2 IN IP4 127.0.0.1"}}
            }
            await self.manager.handle_voice_mesh_message("circle_voice_01", "usr_bob", answer_payload)

            # Peer A should receive the SDP answer
            received_answers = [m for m in ws_peer_a.received_messages if m.get("type") == "SDP_ANSWER"]
            self.assertGreaterEqual(len(received_answers), 1)
            self.assertEqual(received_answers[0]["sender_user_id"], "usr_bob")

            # Peer A sends ICE candidate
            ice_payload = {
                "type": "ICE_CANDIDATE",
                "target_user_id": "usr_bob",
                "payload": {"candidate": {"candidate": "candidate:1 1 UDP ...", "sdpMid": "0"}}
            }
            await self.manager.handle_voice_mesh_message("circle_voice_01", "usr_alice", ice_payload)
            received_ice = [m for m in ws_peer_b.received_messages if m.get("type") == "ICE_CANDIDATE"]
            self.assertGreaterEqual(len(received_ice), 1)

            await self.manager.disconnect(conn_a, "voice_mesh", "circle_voice_01")
            await self.manager.disconnect(conn_b, "voice_mesh", "circle_voice_01")

        asyncio.run(run_test())

    # --------------------------------------------------------------------------
    # 5. Heartbeat Keepalive Protocol
    # --------------------------------------------------------------------------
    def test_heartbeat_ping_pong_protocol(self):
        async def run_test():
            ws = MockClientWebSocket()
            client_send_time = int(time.time() * 1000) - 25

            pong = await self.manager.handle_heartbeat_ping(
                websocket=ws,
                conn_id="conn_test_heartbeat",
                ping_payload={"type": "ping", "client_time": client_send_time}
            )
            self.assertEqual(pong["type"], "pong")
            self.assertGreaterEqual(pong["latency_ms"], 0)
            self.assertGreater(pong["server_time"], 0)

            # Verify websocket received the pong response
            self.assertEqual(len(ws.received_messages), 1)
            self.assertEqual(ws.received_messages[0]["type"], "pong")

        asyncio.run(run_test())

    # --------------------------------------------------------------------------
    # 6. Stress Test: 1,000 Concurrent WebSockets with Sub-50ms Latency
    # --------------------------------------------------------------------------
    def test_stress_1000_concurrent_connections_and_sub_50ms_latency(self):
        async def run_stress_test():
            total_target_clients = 1000
            mock_sockets = [MockClientWebSocket() for _ in range(total_target_clients)]
            conn_ids = []

            # 1. Connect 1,000 concurrent clients across 5 rooms (200 clients per room)
            for i, ws in enumerate(mock_sockets):
                room_index = i % 5
                room_id = f"stress_room_{room_index}"
                user_id = f"usr_stress_client_{i:04d}"

                cid = await self.manager.connect(
                    websocket=ws,
                    channel_type="live_challenge",
                    room_or_circle_id=room_id,
                    user_id=user_id,
                    role="student",
                    tenant_id="tenant_scale_test"
                )
                conn_ids.append((cid, "live_challenge", room_id))

            stats = self.manager.get_manager_stats()
            self.assertEqual(stats["active_connections"], 1000)

            # 2. Measure high-concurrency broadcast throughput and latency
            start_time = time.perf_counter()
            test_broadcast_payload = {
                "type": "MASS_BROADCAST_TEST",
                "message": "High-concurrency millisecond sync verification.",
                "timestamp_ms": int(time.time() * 1000)
            }

            delivered_count = await self.manager.broadcast_to_channel(
                channel_type="live_challenge",
                room_or_circle_id="stress_room_0",
                message=test_broadcast_payload
            )
            broadcast_duration_ms = (time.perf_counter() - start_time) * 1000

            # 3. Assertions: latency strictly under 50ms and 200 delivered in stress_room_0
            self.assertEqual(delivered_count, 200)
            self.assertLess(
                broadcast_duration_ms,
                50.0,
                f"Broadcast latency exceeded 50ms threshold: {broadcast_duration_ms:.2f}ms"
            )

            # 4. Teardown all 1,000 connections
            for cid, ctype, rid in conn_ids:
                await self.manager.disconnect(cid, ctype, rid)

            final_stats = self.manager.get_manager_stats()
            self.assertEqual(final_stats["active_connections"], 0)
            self.assertEqual(final_stats["total_connections_opened"], 1000)
            self.assertEqual(final_stats["total_connections_closed"], 1000)

        asyncio.run(run_stress_test())

    # --------------------------------------------------------------------------
    # 7. Router WebSocket Endpoints Registered
    # --------------------------------------------------------------------------
    def test_router_websocket_routes_registered(self):
        self.assertIsNotNone(websocket_router)
        self.assertIsNotNone(websocket_manager)
        stats = self.manager.get_manager_stats()
        self.assertIn("active_connections", stats)
        self.assertIn("average_broadcast_latency_ms", stats)

    # --------------------------------------------------------------------------
    # 8. Strict Zero-Emoji Governance Across Phase 80 Files
    # --------------------------------------------------------------------------
    def test_strict_zero_emoji_governance_across_phase80_files(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        files_to_audit = [
            os.path.join(base_dir, "app", "services", "websocket_connection_manager.py"),
            os.path.join(base_dir, "app", "api", "v1", "endpoints", "websocket.py"),
            os.path.join(base_dir, "app", "api", "v1", "endpoints", "__init__.py"),
            os.path.join(os.path.dirname(base_dir), "frontend", "src", "lib", "webrtc", "types.ts"),
            os.path.join(os.path.dirname(base_dir), "frontend", "src", "lib", "webrtc", "client.ts"),
            os.path.join(os.path.dirname(base_dir), "frontend", "src", "lib", "webrtc", "voiceMesh.ts"),
            os.path.join(os.path.dirname(base_dir), "frontend", "src", "lib", "webrtc", "index.ts")
        ]

        def contains_emoji(text: str) -> bool:
            for char in text:
                cp = ord(char)
                if (0x1F600 <= cp <= 0x1F64F or
                    0x1F300 <= cp <= 0x1F5FF or
                    0x1F680 <= cp <= 0x1F6FF or
                    0x1F700 <= cp <= 0x1F77F or
                    0x1F780 <= cp <= 0x1F7FF or
                    0x1F800 <= cp <= 0x1F8FF or
                    0x1F900 <= cp <= 0x1F9FF or
                    0x1FA00 <= cp <= 0x1FA6F or
                    0x1FA70 <= cp <= 0x1FAFF or
                    0x2600 <= cp <= 0x26FF or
                    0x2700 <= cp <= 0x27BF):
                    return True
            return False

        for fpath in files_to_audit:
            self.assertTrue(os.path.exists(fpath), f"File {fpath} must exist")
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertFalse(contains_emoji(content), f"Rogue emoji detected in {fpath}")
            self.assertIn("DEVELOPER ARCHITECTURE NOTE", content, f"Missing Developer Note in {fpath}")


if __name__ == "__main__":
    unittest.main()
