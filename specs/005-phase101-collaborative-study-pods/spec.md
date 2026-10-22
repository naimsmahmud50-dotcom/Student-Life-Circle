<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Feature Specification
TOPIC:     Phase 101 Real-Time Study Pods & Collaborative Whiteboard
FILE:      specs/005-phase101-collaborative-study-pods/spec.md
PHASE:     Phase 101 - Real-Time Study Pods & Collaborative Whiteboard
PURPOSE:   Establishes functional specifications for synchronized student study pods.
           Defines WebRTC audio mesh topology, real-time vector whiteboard delta broadcast,
           max 8 peers room capacity enforcement, and Apple Freeform caliber UI design.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
-->

# Specification: Phase 101 — Real-Time Study Pods & Collaborative Whiteboard

## Feature Directory
`specs/005-phase101-collaborative-study-pods`

## 1. Problem Statement
Self-directed study can often feel isolating for secondary and higher secondary students preparing for competitive board and university entrance exams. Students need an interactive, distraction-free digital space to solve physics, chemistry, and higher math problems together in small, intimate cohorts (2 to 8 peers) with real-time vector drawing, LaTeX formula rendering, and crystal-clear voice communication.

## 2. Goals & Non-Goals
### Goals:
- Build `CollaborativeWhiteboard.tsx` featuring HTML5 high-performance vector canvas, geometric shapes, freehand drawing, and KaTeX mathematical notation stamps.
- Synchronize whiteboard stroke deltas and LaTeX nodes in real time over WebSocket `/ws/whiteboard/{pod_id}` with Redis pub/sub.
- Build `StudyPodRoom.tsx` featuring dynamic 2-to-8 participant video/audio tiles, soft ambient emerald pulse active speaker ring, and a floating frosted glass control bar.
- Implement WebRTC P2P audio mesh signaling in `voiceMesh.ts` with automatic echo cancellation, noise suppression, and Web Audio API VAD.
- Implement backend `study_pods.py` API enforcing a strict maximum capacity limit of 8 peers per room.
- Maintain 100% Zero-Emoji compliance with Lucide-React SVG vectors and WCAG 2.2 AAA contrast.

### Non-Goals:
- Centralized SFU media server infrastructure (P2P full-mesh audio is used for sub-50ms rural latency).
- Public unauthenticated room joining.
