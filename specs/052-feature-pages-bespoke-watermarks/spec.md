# Feature Specification: Bespoke Feature Background Designs & Giant Typographic Watermarks

## Executive Summary
Following the acclaimed aesthetic of Ogrojatra's Homepage Hero (featuring warm linen canvas `#FFFCF6`, warm sunshine tint `#FFF6DD`, radial golden sunburst glows, and giant typographic watermark `OGROJATRA`), this specification outlines the deployment of differentiated, domain-tailored background designs and giant watermarks across all flagship feature pages:
1. `PageHeader.tsx`: Global support for bespoke typographic watermarks (`watermarkText`) and radial atmospheric glows (`glowGradient`).
2. `/board-archives`: Watermark `ARCHIVES` with heritage parchment golden aura.
3. `/socratic/solver`: Watermark `SOCRATIC` with intelligent neural amber aura and warm ivory cards.
4. `/live-challenge`: Watermark `CHALLENGE` with stadium golden amber arena glow.
5. `/tuition`: Watermark `TUITION` with trusted scholarly prestige aura.
6. `/practice`: Watermark `PRACTICE` with focused academic aura.
7. `/career`: Watermark `CAREER` with professional horizon amber aura.
8. `/admission`: Watermark `ADMISSION` with university prestige golden aura.

## Functional Requirements
- **FR-01:** Implement `watermarkText` and `glowGradient` in `PageHeader.tsx` with responsive clamp scaling (`clamp(3rem, 18vw, 15rem)`) and zero layout shift (`pointer-events-none select-none`).
- **FR-02:** Integrate bespoke atmospheric background container in `socratic/solver.tsx` matching the dual-mode tutor and whiteboard layout.
- **FR-03:** Integrate bespoke watermark and golden aura in `live-challenge.tsx` above or encompassing `LiveMcqHeroSection`.
- **FR-04:** Integrate bespoke watermark and golden aura in `tuition.tsx` header section.
- **FR-05:** Integrate bespoke watermark and golden aura in `career.tsx` / `CareerStatsHeader.tsx`.
- **FR-06:** Integrate bespoke watermark and golden aura in `admission.tsx` header section.
- **FR-07:** Preserve 100% of existing functionality, math KaTeX rendering, audio/voice inputs, 3D STEM slots, and APIs.
- **FR-08:** Strictly adhere to the zero-emoji policy across all code, comments, and copy.
- **FR-09:** Maintain strict port discipline on port 3002.
