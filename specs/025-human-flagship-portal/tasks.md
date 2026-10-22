<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Tasks Ledger
TOPIC:     Flagship Human-Centric Institutional Portal Implementation Checklist
FILE:      specs/025-human-flagship-portal/tasks.md
PHASE:     Phase 121 / Feature 025 - Flagship Human-Centric Institutional Portal
PURPOSE:   Actionable, ordered checklist for building the client-ready flagship landing
           page and cleanly separating the student dashboard.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
-->

# Tasks: Feature 025 — Flagship Human-Centric Institutional Portal

## Tasks Ledger

- [x] Task 1: Preserve Student Dashboard in `frontend/src/pages/dashboard.tsx`
  - Move personalized learning cockpit (streak counter, goal ring, active quiz reminders) to `/dashboard`
  - Maintain student profile controls and stage selections
- [x] Task 2: Re-Architect Flagship Landing Page in `frontend/src/pages/index.tsx`
  - Build prestigious Hero section with national authority, value proposition, and dual high-contrast CTAs
  - Implement National Scale & Trust Strip (4 core metrics)
  - Implement 4 Core Educational Pathway Cards (SSC, HSC, Admission, Career)
  - Implement Interactive Flagship Feature Showcase (NCTB Archives, Exam Hall, STEM Labs, AI Tutor, Scholarships)
  - Implement Institutional Trust & Verified Payment Rails (bKash, Nagad, SSLCommerz, W3C)
  - Implement High-Impact Closing CTA section
  - Ensure strict zero-emoji compliance (pure Lucide SVGs) and Oxford Academic Navy typography
- [x] Task 3: Update Global Header Navigation (`frontend/src/components/layout/Navbar.tsx`)
  - Add clean CTA button linking directly to `/dashboard` ("ড্যাশবোর্ড")
  - Retain all curriculum, board archives, and practice navigation links
- [x] Task 4: Compile & Verify Next.js Production Build
  - Execute `npx next build` and verify 0 TypeScript/ESLint errors
  - Confirm all 26+ static pages compile successfully
- [x] Task 5: Execute Strict Zero-Emoji & Security Sweeps
  - Run `python3 backend/scripts/run_zero_emoji_sweep.py`
  - Assert 0 violations across all files
- [x] Task 6: Verify Live Production Server on Port 3000
  - Restart Next.js server on port 3000
  - Confirm HTTP 200 OK and clean visual layout
