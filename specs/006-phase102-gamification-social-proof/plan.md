<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Implementation Plan
TOPIC:     Technical Blueprint for Dignified Gamification & Verifiable Social Proof
FILE:      specs/006-phase102-gamification-social-proof/plan.md
PHASE:     Phase 102 - Dignified Gamification & Verifiable Social Proof
PURPOSE:   Architectural blueprint for Strava-caliber academic achievement,
           streak recovery modals, anti-burnout point capping, and cryptographic badges.
STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
-->

# Technical Plan: Phase 102 Dignified Gamification & Verifiable Social Proof

## 1. Architectural Architecture
- **Anti-Burnout Gamification Engine (`backend/app/services/gamification_service.py`)**:
  - Implements `GamificationEngine` singleton with thread-safe ledger.
  - Enforces `DAILY_XP_CAP = 500` to prevent binge-studying and dopamine fatigue.
  - Implements `recover_streak_with_drill(user_id)` allowing 1-click recovery if a review drill is completed.
  - Implements `award_mastery_badge(user_id, badge_id)` with cryptographic HMAC-SHA256 fingerprint.
- **Frontend Components**:
  - `StreakShieldModal.tsx`: Accessible dialog with warm amber glowing flame, empathetic copy, and recovery trigger.
  - `MasteryBadgeCard.tsx`: Micro-beveled card with specular top sheen, QR Code SVG link, and LinkedIn/Facebook share handlers.
  - `achievements.tsx`: Flagship Bento Grid showcasing Streak Velocity, Active Shields, Subject Masteries, and Milestone Timeline.
- **Verification Suite**:
  - `backend/tests/test_phase102_dignified_gamification.py`: Asserts daily XP capping, streak recovery logic, cryptographic badge verification, architecture note headers, and zero-emoji compliance.

## 2. Directory Layout & Key Files
- `frontend/src/components/gamification/StreakShieldModal.tsx`
- `frontend/src/components/gamification/MasteryBadgeCard.tsx`
- `frontend/src/pages/achievements.tsx`
- `backend/app/services/gamification_service.py`
- `backend/tests/test_phase102_dignified_gamification.py`
