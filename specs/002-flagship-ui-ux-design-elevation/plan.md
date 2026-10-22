# Architectural Plan: Flagship UI/UX Elevation & Design Unification

## Architecture & Implementation Blueprint

### 1. Global Shell & Layout Synchronization
- **File**: `frontend/src/pages/_app.tsx`
  - Injects `I18nProvider` from `@/lib/i18n` at the root so language switching is instantaneous across all routes.
  - Injects floating `SocraticTutorDrawer` launcher (accessible bottom-right FAB) across every view.
- **File**: `frontend/src/components/layout/Footer.tsx`
  - Creates a dignified, responsive platform footer with NCTB curriculum accreditation badges, verified payment logos (bKash, Nagad), and privacy/legal links.

### 2. Flagship Dashboard Transformation (`frontend/src/pages/index.tsx`)
- Replaces legacy prototype code with a cohesive, world-class Student Growth Dashboard:
  - **Hero & Context**: Dynamic greeting, current stage pill, quick resume CTA.
  - **Telemetry Metric Grid**: 4 key academic indicators (Study Streak, Questions Solved, Accuracy Rate, Percentile Rank).
  - **Journey Pathways**: Visual cards for Secondary (SSC), Higher Secondary (HSC), Admission Hub, Tuition Marketplace, Career Milestones.
  - **3D STEM Virtual Labs Showcase**: Interactive preview cards with direct launch buttons for Projectile Simulator and Molecular Viewer.
  - **Live Challenge Spotlight**: Real-time challenge card with live timer, participant badge, and instant join CTA.
  - **Proof-of-Skill Showcase**: Displays official W3C Certificate preview with QR code and 1-click social sharing.
  - **Payment & Trust Bar**: Official bKash and Nagad verified badges.

### 3. Sub-Page Layout Elevation
- **`frontend/src/pages/learn.tsx`**: Uses unified `Navbar`, visual progress meters, and direct chapter links.
- **`frontend/src/pages/practice.tsx`**: Unified navigation, KaTeX mathematical formulas, and Socratic hint integration.
- **`frontend/src/pages/live-challenge.tsx`**: Real-time lobby styling, sub-second leaderboard, and exam timer.
- **`frontend/src/pages/admission.tsx`**: Authentic admission blueprints (BUET, DU Ka, Medical) with negative marking indicators.

### 4. Verification & Testing Strategy
- All 1,190 backend unit/integration tests must remain 100% passing.
- Automated tests in `backend/tests/test_phase98_flagship_ui_elevation.py` validating component integration, layout shell, zero emojis, and WCAG AAA contrast.
