<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Implementation Plan
TOPIC:     Technical Architecture for Study Pods & Collaborative Whiteboard
FILE:      specs/005-phase101-collaborative-study-pods/plan.md
PHASE:     Phase 101 - Real-Time Study Pods & Collaborative Whiteboard
PURPOSE:   Architectural blueprint for HTML5 whiteboard canvas with KaTeX math rendering,
           WebRTC voice mesh manager, dynamic participant grid, and backend capacity controls.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
-->

# Technical Plan: Phase 101 Study Pods & Collaborative Whiteboard

## 1. Architecture Overview
- **Whiteboard Engine**: HTML5 Canvas with vector path serialization, stroke smoothing, and KaTeX overlay stamps.
- **Signaling Layer**: Resilient WebSocket client connecting to `/ws/whiteboard/{pod_id}` and `/ws/voice-mesh/{pod_id}`.
- **Voice Mesh**: Full-mesh WebRTC `RTCPeerConnection` for up to 8 peers with `getUserMedia` audio constraints (echoCancellation, noiseSuppression, autoGainControl) and `AudioContext` energy-based Voice Activity Detection (VAD).
- **Study Pod Room UI**: Responsive CSS Grid adjusting seamlessly from 2 to 8 participant tiles, soft ambient emerald pulse ring around the speaking participant's avatar, and floating frosted glass bottom control pill (`backdrop-blur-xl bg-white/80 dark:bg-slate-900/80`).
- **Backend API & Capacity Guard**: `study_pods.py` enforcing strict capacity limit (`len(members) <= 8`) and broadcasting delta messages.

## 2. Component Specifications
1. `CollaborativeWhiteboard.tsx`:
   - State: tool (`pen`, `eraser`, `rectangle`, `circle`, `latex`), strokeColor, strokeWidth, strokes list, latexNodes list.
   - Canvas: Pointer events with coordinate normalization and retina display scaling (`window.devicePixelRatio`).
   - Floating toolbar: Pill bar with tactile tool buttons (`active:scale-95`, `shadow-sm`).
2. `StudyPodRoom.tsx`:
   - State: participants (2-8), isMuted, isCameraOn, isScreenSharing, isHandRaised, activeSpeakerId.
   - Grid layout: responsive `grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`.
   - Floating control bar: Lucide SVG icons (Mic, Video, Share2, Hand, LogOut) with tactile push states.
3. `voiceMesh.ts`:
   - Enforce Web Audio API VAD, echo cancellation, noise suppression, and full Phase 101 architecture note header.
4. `study_pods.py`:
   - In-memory thread-safe room registry with max capacity 8 enforcement, delta history, and telemetry.
5. `test_phase101_study_pods_and_whiteboard.py`:
   - Automated tests for capacity limit, delta broadcast, audio telemetry, and architecture notes.
