/**
 * ==============================================================================
 * DEVELOPER ARCHITECTURE NOTE (Phase 80 - WebSocket & WebRTC Types):
 * Defines strict TypeScript interfaces for real-time WebSocket communication,
 * heartbeat keepalives, live challenge synchronization, vector canvas delta sync,
 * and WebRTC peer-to-peer audio mesh signaling.
 * Zero-Emoji Policy Enforced: All comments and descriptions use clean technical text.
 * ==============================================================================
 */

export type WebSocketChannelType = "live-challenge" | "whiteboard" | "voice-mesh";

export type WebSocketConnectionStatus =
  | "CONNECTING"
  | "OPEN"
  | "CLOSING"
  | "CLOSED"
  | "RECONNECTING";

export interface PingPongMessage {
  type: "ping" | "pong";
  client_time?: number;
  server_time?: number;
  latency_ms?: number;
}

export interface LiveChallengeMessage {
  type:
    | "SYNC_COUNTDOWN"
    | "SUBMIT_ANSWER"
    | "GET_LEADERBOARD"
    | "LEADERBOARD_UPDATED"
    | "COUNTDOWN_SYNC_RESPONSE"
    | "ANSWER_CONFIRMED"
    | "LEADERBOARD_SNAPSHOT";
  room_id?: string;
  question_id?: string;
  selected_option?: string;
  is_correct?: boolean;
  score?: number;
  new_score?: number;
  server_time_ms?: number;
  remaining_ms?: number;
  duration_seconds?: number;
  leaderboard?: Array<{
    user_id: string;
    score: number;
    rank?: number;
  }>;
  last_answer_by?: string;
  timestamp_ms?: number;
}

export interface VectorStroke {
  id?: string;
  author_id?: string;
  tool_type: "pen" | "line" | "rect" | "circle" | "eraser";
  color: string;
  width: number;
  points: number[][];
  timestamp_ms?: number;
  is_erased?: boolean;
}

export interface LatexFormulaNode {
  id?: string;
  author_id?: string;
  latex_source: string;
  position_x: number;
  position_y: number;
  font_size: number;
  color?: string;
}

export interface WhiteboardDeltaMessage {
  type:
    | "DRAW_STROKE"
    | "ERASE_STROKE"
    | "PLACE_LATEX"
    | "STROKE_DELTA"
    | "LATEX_NODE_PLACED"
    | "GET_CANVAS_SNAPSHOT"
    | "CANVAS_SNAPSHOT"
    | "STROKE_ACCEPTED"
    | "LATEX_ACCEPTED";
  circle_id?: string;
  stroke?: VectorStroke;
  latex_node?: LatexFormulaNode;
  strokes?: VectorStroke[];
  formulas?: LatexFormulaNode[];
  strokes_count?: number;
  formulas_count?: number;
}

export interface WebRtcSignalPayload {
  sdp?: RTCSessionDescriptionInit;
  candidate?: RTCIceCandidateInit;
  audio_muted?: boolean;
  is_speaking?: boolean;
}

export interface VoiceMeshSignalMessage {
  type:
    | "SDP_OFFER"
    | "SDP_ANSWER"
    | "ICE_CANDIDATE"
    | "JOIN_MESH"
    | "LEAVE_MESH"
    | "VAD_ACTIVE"
    | "MUTE_STATE"
    | "SIGNAL_ROUTED";
  circle_id?: string;
  sender_user_id?: string;
  target_user_id?: string;
  payload?: WebRtcSignalPayload;
  timestamp_ms?: number;
}

export interface WebRtcPeerState {
  peer_id: string;
  user_id: string;
  audio_muted: boolean;
  is_speaking: boolean;
  connection_state: string;
  latency_ms: number;
}

export interface WebSocketClientConfig {
  baseUrl?: string;
  channelType: WebSocketChannelType;
  channelId: string;
  token: string;
  heartbeatIntervalMs?: number;
  pongTimeoutMs?: number;
  baseReconnectDelayMs?: number;
  maxReconnectDelayMs?: number;
  backoffFactor?: number;
  maxReconnectAttempts?: number;
}
