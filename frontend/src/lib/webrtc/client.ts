/**
 * ==============================================================================
 * DEVELOPER ARCHITECTURE NOTE (Phase 80 - Resilient WebSocket Client):
 * This client provides a robust, self-healing WebSocket connection manager for
 * the Student Life Circle frontend.
 * Key Architectural Features:
 * 1. Automatic Exponential Backoff Reconnection:
 *    - Base delay: 1,000ms; Max delay: 30,000ms; Factor: 1.5; Jitter: +/- 20%.
 *    - Automatically recovers from intermittent network dropouts without thundering herd.
 * 2. 30-Second Heartbeat Ping/Pong Keepalive:
 *    - Periodically transmits {"type": "ping", "client_time": Date.now()}.
 *    - Detects half-open TCP connections when pong is missing for over 10 seconds.
 * 3. Secure Handshake Query Binding:
 *    - Appends token parameter (?token=...) to the WebSocket handshake URL.
 * 4. Zero-Emoji Policy Enforced: All logs, error messages, and comments use clean text.
 * ==============================================================================
 */

import {
  WebSocketClientConfig,
  WebSocketConnectionStatus,
  PingPongMessage
} from "./types";

export class ResilientWebSocketClient {
  private config: Required<WebSocketClientConfig>;
  private socket: WebSocket | null = null;
  private status: WebSocketConnectionStatus = "CLOSED";
  private reconnectAttempts = 0;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private pongTimeoutTimer: NodeJS.Timeout | null = null;
  private isIntentionallyClosed = false;
  private lastMeasuredLatencyMs = 0;

  private messageListeners: Set<(data: any) => void> = new Set();
  private statusListeners: Set<(status: WebSocketConnectionStatus) => void> = new Set();
  private errorListeners: Set<(error: any) => void> = new Set();

  constructor(config: WebSocketClientConfig) {
    const defaultBaseUrl =
      typeof window !== "undefined"
        ? `${window.location.protocol === "https:" ? "wss:" : "ws:"}//${window.location.host}`
        : "ws://localhost:8000";

    this.config = {
      baseUrl: config.baseUrl || process.env.NEXT_PUBLIC_WS_URL || defaultBaseUrl,
      channelType: config.channelType,
      channelId: config.channelId,
      token: config.token,
      heartbeatIntervalMs: config.heartbeatIntervalMs || 30000, // 30s heartbeat
      pongTimeoutMs: config.pongTimeoutMs || 10000,
      baseReconnectDelayMs: config.baseReconnectDelayMs || 1000,
      maxReconnectDelayMs: config.maxReconnectDelayMs || 30000,
      backoffFactor: config.backoffFactor || 1.5,
      maxReconnectAttempts: config.maxReconnectAttempts || 10
    };
  }

  /**
   * Constructs the authenticated WebSocket connection URL.
   */
  public getEndpointUrl(): string {
    const base = this.config.baseUrl.replace(/\/$/, "");
    const encodedToken = encodeURIComponent(this.config.token);
    return `${base}/ws/${this.config.channelType}/${this.config.channelId}?token=${encodedToken}`;
  }

  /**
   * Establishes the WebSocket connection.
   */
  public connect(): void {
    if (typeof window === "undefined") {
      return; // Server-side rendering guard
    }

    if (this.socket && (this.socket.readyState === WebSocket.OPEN || this.socket.readyState === WebSocket.CONNECTING)) {
      return;
    }

    this.isIntentionallyClosed = false;
    this.setStatus("CONNECTING");

    try {
      const url = this.getEndpointUrl();
      this.socket = new WebSocket(url);

      this.socket.onopen = this.handleOpen.bind(this);
      this.socket.onmessage = this.handleMessage.bind(this);
      this.socket.onclose = this.handleClose.bind(this);
      this.socket.onerror = this.handleError.bind(this);
    } catch (err) {
      this.handleError(err);
      this.scheduleReconnect();
    }
  }

  /**
   * Gracefully terminates the WebSocket connection.
   */
  public disconnect(): void {
    this.isIntentionallyClosed = true;
    this.stopHeartbeat();
    this.clearReconnectTimer();

    if (this.socket) {
      this.setStatus("CLOSING");
      try {
        this.socket.close(1000, "CLIENT_DISCONNECTED_CLEANLY");
      } catch (e) {
        // Ignored during shutdown
      }
      this.socket = null;
    }
    this.setStatus("CLOSED");
  }

  /**
   * Transmits a JSON payload over the WebSocket connection.
   */
  public send(payload: any): boolean {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      return false;
    }
    try {
      const dataStr = typeof payload === "string" ? payload : JSON.stringify(payload);
      this.socket.send(dataStr);
      return true;
    } catch (err) {
      this.notifyError(err);
      return false;
    }
  }

  public getStatus(): WebSocketConnectionStatus {
    return this.status;
  }

  public getLatency(): number {
    return this.lastMeasuredLatencyMs;
  }

  public onMessage(handler: (data: any) => void): () => void {
    this.messageListeners.add(handler);
    return () => this.messageListeners.delete(handler);
  }

  public onStatusChange(handler: (status: WebSocketConnectionStatus) => void): () => void {
    this.statusListeners.add(handler);
    return () => this.statusListeners.delete(handler);
  }

  public onError(handler: (error: any) => void): () => void {
    this.errorListeners.add(handler);
    return () => this.errorListeners.delete(handler);
  }

  // =========================================================================
  // Internal Event Handlers
  // =========================================================================
  private handleOpen(): void {
    this.reconnectAttempts = 0;
    this.clearReconnectTimer();
    this.setStatus("OPEN");
    this.startHeartbeat();
  }

  private handleMessage(event: MessageEvent): void {
    try {
      const parsed = JSON.parse(event.data);

      // Heartbeat Pong Handling
      if (parsed && parsed.type === "pong") {
        this.handlePong(parsed as PingPongMessage);
        return;
      }

      this.messageListeners.forEach((fn) => {
        try {
          fn(parsed);
        } catch (err) {
          console.error("Error in WebSocket message listener:", err);
        }
      });
    } catch (err) {
      // Non-JSON message passthrough
      this.messageListeners.forEach((fn) => fn(event.data));
    }
  }

  private handleClose(event: CloseEvent): void {
    this.stopHeartbeat();
    this.socket = null;

    if (!this.isIntentionallyClosed) {
      this.setStatus("CLOSED");
      this.scheduleReconnect();
    } else {
      this.setStatus("CLOSED");
    }
  }

  private handleError(error: any): void {
    this.notifyError(error);
  }

  private setStatus(newStatus: WebSocketConnectionStatus): void {
    this.status = newStatus;
    this.statusListeners.forEach((fn) => {
      try {
        fn(newStatus);
      } catch (err) {
        console.error("Error in WebSocket status listener:", err);
      }
    });
  }

  private notifyError(err: any): void {
    this.errorListeners.forEach((fn) => {
      try {
        fn(err);
      } catch (e) {
        console.error("Error in WebSocket error listener:", e);
      }
    });
  }

  // =========================================================================
  // Heartbeat Protocol (30s Cycle)
  // =========================================================================
  private startHeartbeat(): void {
    this.stopHeartbeat();
    this.heartbeatTimer = setInterval(() => {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        const pingMsg: PingPongMessage = {
          type: "ping",
          client_time: Date.now()
        };
        this.send(pingMsg);

        // Schedule pong timeout
        this.pongTimeoutTimer = setTimeout(() => {
          // Half-open connection detected, forcefully trigger reconnect
          if (this.socket) {
            try {
              this.socket.close(4000, "HEARTBEAT_TIMEOUT");
            } catch (e) {
              // Ignore
            }
          }
        }, this.config.pongTimeoutMs);
      }
    }, this.config.heartbeatIntervalMs);
  }

  private handlePong(pong: PingPongMessage): void {
    if (this.pongTimeoutTimer) {
      clearTimeout(this.pongTimeoutTimer);
      this.pongTimeoutTimer = null;
    }
    if (pong.client_time) {
      this.lastMeasuredLatencyMs = Math.max(0, Date.now() - pong.client_time);
    }
  }

  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
    if (this.pongTimeoutTimer) {
      clearTimeout(this.pongTimeoutTimer);
      this.pongTimeoutTimer = null;
    }
  }

  // =========================================================================
  // Exponential Backoff Reconnection Logic
  // =========================================================================
  private scheduleReconnect(): void {
    if (this.isIntentionallyClosed || this.reconnectAttempts >= this.config.maxReconnectAttempts) {
      return;
    }

    this.clearReconnectTimer();
    this.setStatus("RECONNECTING");

    // delay = min(base * (factor ^ attempts), max) with 20% jitter
    const exponentialDelay =
      this.config.baseReconnectDelayMs * Math.pow(this.config.backoffFactor, this.reconnectAttempts);
    const cappedDelay = Math.min(exponentialDelay, this.config.maxReconnectDelayMs);
    const jitter = cappedDelay * 0.2 * (Math.random() * 2 - 1);
    const finalDelay = Math.max(500, Math.floor(cappedDelay + jitter));

    this.reconnectAttempts++;
    this.reconnectTimer = setTimeout(() => {
      this.connect();
    }, finalDelay);
  }

  private clearReconnectTimer(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }
}
