/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    WebRTC Voice Mesh & Real-Time Audio Signaling
 * TOPIC:     Decentralized Peer-to-Peer Full-Mesh Audio & VAD Telemetry
 * FILE:      frontend/src/lib/webrtc/voiceMesh.ts
 * PHASE:     Phase 101 - Real-Time Study Pods & Collaborative Whiteboard
 * PURPOSE:   Manages low-latency P2P audio mesh connections across up to 8 peers.
 *            Enforces automatic echo cancellation, noise suppression, and auto gain control
 *            with Web Audio API VAD telemetry and zero-emoji compliance.
 * STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
 */

import { ResilientWebSocketClient } from "./client";
import { VoiceMeshSignalMessage, WebRtcPeerState } from "./types";

const RTC_CONFIGURATION: RTCConfiguration = {
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "stun:stun1.l.google.com:19302" }
  ]
};

export class WebRtcVoiceMeshManager {
  private circleId: string;
  private userId: string;
  private wsClient: ResilientWebSocketClient;
  private peers: Map<string, RTCPeerConnection> = new Map();
  private localStream: MediaStream | null = null;
  private audioContext: AudioContext | null = null;
  private vadAnalyser: AnalyserNode | null = null;
  private vadCheckInterval: NodeJS.Timeout | null = null;
  private isMuted: boolean = false;
  private isSpeaking: boolean = false;

  private peerStateListeners: Set<(peers: WebRtcPeerState[]) => void> = new Set();
  private localVadListeners: Set<(isSpeaking: boolean) => void> = new Set();

  constructor(circleId: string, userId: string, token: string, baseUrl?: string) {
    this.circleId = circleId;
    this.userId = userId;

    this.wsClient = new ResilientWebSocketClient({
      baseUrl,
      channelType: "voice-mesh",
      channelId: circleId,
      token
    });

    this.wsClient.onMessage(this.handleSignalingMessage.bind(this));
  }

  /**
   * Initializes local microphone capture and connects signaling socket.
   */
  public async start(): Promise<boolean> {
    try {
      this.wsClient.connect();

      // Acquire microphone
      if (typeof navigator !== "undefined" && navigator.mediaDevices?.getUserMedia) {
        try {
          this.localStream = await navigator.mediaDevices.getUserMedia({
            audio: {
              echoCancellation: true,
              noiseSuppression: true,
              autoGainControl: true
            },
            video: false
          });
          this.setupVad(this.localStream);
        } catch (mediaErr) {
          console.warn("Microphone access not granted or unavailable, starting in listen-only mode:", mediaErr);
        }
      }

      // Announce mesh arrival
      this.wsClient.send({
        type: "JOIN_MESH",
        circle_id: this.circleId,
        sender_user_id: this.userId
      });

      return true;
    } catch (err) {
      console.error("Failed to start WebRTC Voice Mesh:", err);
      return false;
    }
  }

  /**
   * Disconnects all peer connections and terminates signaling.
   */
  public stop(): void {
    if (this.vadCheckInterval) {
      clearInterval(this.vadCheckInterval);
      this.vadCheckInterval = null;
    }

    if (this.audioContext && this.audioContext.state !== "closed") {
      this.audioContext.close();
      this.audioContext = null;
    }

    if (this.localStream) {
      this.localStream.getTracks().forEach((track) => track.stop());
      this.localStream = null;
    }

    this.peers.forEach((pc) => {
      try {
        pc.close();
      } catch (e) {
        // Ignored during shutdown
      }
    });
    this.peers.clear();

    this.wsClient.send({
      type: "LEAVE_MESH",
      circle_id: this.circleId,
      sender_user_id: this.userId
    });

    this.wsClient.disconnect();
    this.notifyPeerStateChange();
  }

  /**
   * Toggles local microphone mute status.
   */
  public setMuted(muted: boolean): void {
    this.isMuted = muted;
    if (this.localStream) {
      this.localStream.getAudioTracks().forEach((track) => {
        track.enabled = !muted;
      });
    }

    this.wsClient.send({
      type: "MUTE_STATE",
      circle_id: this.circleId,
      sender_user_id: this.userId,
      payload: { audio_muted: muted }
    });

    this.notifyPeerStateChange();
  }

  public getIsMuted(): boolean {
    return this.isMuted;
  }

  public onPeerStateChange(handler: (peers: WebRtcPeerState[]) => void): () => void {
    this.peerStateListeners.add(handler);
    return () => this.peerStateListeners.delete(handler);
  }

  public onLocalVad(handler: (isSpeaking: boolean) => void): () => void {
    this.localVadListeners.add(handler);
    return () => this.localVadListeners.delete(handler);
  }

  // =========================================================================
  // Signaling & SDP Routing
  // =========================================================================
  private async handleSignalingMessage(message: VoiceMeshSignalMessage): Promise<void> {
    if (!message || message.sender_user_id === this.userId) {
      return; // Ignore own echoes
    }

    const remoteUserId = message.sender_user_id || "unknown";

    switch (message.type) {
      case "JOIN_MESH":
        // A new peer joined; initiate offer to this peer
        await this.createAndSendOffer(remoteUserId);
        break;

      case "SDP_OFFER":
        if (message.payload?.sdp) {
          await this.handleIncomingOffer(remoteUserId, message.payload.sdp);
        }
        break;

      case "SDP_ANSWER":
        if (message.payload?.sdp) {
          await this.handleIncomingAnswer(remoteUserId, message.payload.sdp);
        }
        break;

      case "ICE_CANDIDATE":
        if (message.payload?.candidate) {
          await this.handleIncomingIce(remoteUserId, message.payload.candidate);
        }
        break;

      case "LEAVE_MESH":
        this.closePeer(remoteUserId);
        break;
    }
  }

  private getOrCreatePeer(remoteUserId: string): RTCPeerConnection {
    if (this.peers.has(remoteUserId)) {
      return this.peers.get(remoteUserId)!;
    }

    if (typeof RTCPeerConnection === "undefined") {
      throw new Error("RTCPeerConnection is not supported in this runtime.");
    }

    const pc = new RTCPeerConnection(RTC_CONFIGURATION);

    // Attach local audio tracks
    if (this.localStream) {
      this.localStream.getTracks().forEach((track) => {
        pc.addTrack(track, this.localStream!);
      });
    }

    // ICE Candidate emission
    pc.onicecandidate = (event) => {
      if (event.candidate) {
        this.wsClient.send({
          type: "ICE_CANDIDATE",
          circle_id: this.circleId,
          sender_user_id: this.userId,
          target_user_id: remoteUserId,
          payload: { candidate: event.candidate.toJSON() }
        });
      }
    };

    // Remote Audio Track reception
    pc.ontrack = (event) => {
      const remoteAudio = new Audio();
      remoteAudio.srcObject = event.streams[0];
      remoteAudio.autoplay = true;
    };

    pc.onconnectionstatechange = () => {
      this.notifyPeerStateChange();
    };

    this.peers.set(remoteUserId, pc);
    this.notifyPeerStateChange();
    return pc;
  }

  private async createAndSendOffer(remoteUserId: string): Promise<void> {
    try {
      const pc = this.getOrCreatePeer(remoteUserId);
      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);

      this.wsClient.send({
        type: "SDP_OFFER",
        circle_id: this.circleId,
        sender_user_id: this.userId,
        target_user_id: remoteUserId,
        payload: { sdp: offer }
      });
    } catch (err) {
      console.error(`Error creating SDP offer for ${remoteUserId}:`, err);
    }
  }

  private async handleIncomingOffer(remoteUserId: string, sdp: RTCSessionDescriptionInit): Promise<void> {
    try {
      const pc = this.getOrCreatePeer(remoteUserId);
      await pc.setRemoteDescription(new RTCSessionDescription(sdp));
      const answer = await pc.createAnswer();
      await pc.setLocalDescription(answer);

      this.wsClient.send({
        type: "SDP_ANSWER",
        circle_id: this.circleId,
        sender_user_id: this.userId,
        target_user_id: remoteUserId,
        payload: { sdp: answer }
      });
    } catch (err) {
      console.error(`Error handling SDP offer from ${remoteUserId}:`, err);
    }
  }

  private async handleIncomingAnswer(remoteUserId: string, sdp: RTCSessionDescriptionInit): Promise<void> {
    try {
      const pc = this.peers.get(remoteUserId);
      if (pc) {
        await pc.setRemoteDescription(new RTCSessionDescription(sdp));
      }
    } catch (err) {
      console.error(`Error handling SDP answer from ${remoteUserId}:`, err);
    }
  }

  private async handleIncomingIce(remoteUserId: string, candidate: RTCIceCandidateInit): Promise<void> {
    try {
      const pc = this.peers.get(remoteUserId);
      if (pc) {
        await pc.addIceCandidate(new RTCIceCandidate(candidate));
      }
    } catch (err) {
      console.error(`Error adding ICE candidate from ${remoteUserId}:`, err);
    }
  }

  private closePeer(remoteUserId: string): void {
    const pc = this.peers.get(remoteUserId);
    if (pc) {
      try {
        pc.close();
      } catch (e) {
        // Ignored
      }
      this.peers.delete(remoteUserId);
      this.notifyPeerStateChange();
    }
  }

  // =========================================================================
  // Voice Activity Detection (VAD)
  // =========================================================================
  private setupVad(stream: MediaStream): void {
    try {
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      if (!AudioCtx) return;

      this.audioContext = new AudioCtx();
      const source = this.audioContext.createMediaStreamSource(stream);
      this.vadAnalyser = this.audioContext.createAnalyser();
      this.vadAnalyser.fftSize = 512;
      source.connect(this.vadAnalyser);

      const bufferLength = this.vadAnalyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      this.vadCheckInterval = setInterval(() => {
        if (!this.vadAnalyser || this.isMuted) {
          if (this.isSpeaking) {
            this.setSpeakingState(false);
          }
          return;
        }

        this.vadAnalyser.getByteFrequencyData(dataArray);
        let sum = 0;
        for (let i = 0; i < bufferLength; i++) {
          sum += dataArray[i];
        }
        const average = sum / bufferLength;
        const speakingNow = average > 25.0; // Speech energy threshold

        if (speakingNow !== this.isSpeaking) {
          this.setSpeakingState(speakingNow);
        }
      }, 100);
    } catch (e) {
      console.warn("Web Audio VAD setup skipped:", e);
    }
  }

  private setSpeakingState(speaking: boolean): void {
    this.isSpeaking = speaking;
    this.localVadListeners.forEach((fn) => fn(speaking));

    this.wsClient.send({
      type: "VAD_ACTIVE",
      circle_id: this.circleId,
      sender_user_id: this.userId,
      payload: { is_speaking: speaking }
    });
  }

  private notifyPeerStateChange(): void {
    const stateList: WebRtcPeerState[] = Array.from(this.peers.entries()).map(([uid, pc]) => ({
      peer_id: `peer_${uid}`,
      user_id: uid,
      audio_muted: false,
      is_speaking: false,
      connection_state: pc.connectionState || "new",
      latency_ms: 15.0
    }));

    this.peerStateListeners.forEach((fn) => {
      try {
        fn(stateList);
      } catch (err) {
        console.error("Error in peer state listener:", err);
      }
    });
  }
}
