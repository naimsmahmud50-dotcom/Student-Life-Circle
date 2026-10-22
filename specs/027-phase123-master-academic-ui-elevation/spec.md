<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Specification
TOPIC:     Master Academic UI & Pro Tactile Button Elevation Specification
FILE:      specs/027-phase123-master-academic-ui-elevation/spec.md
PHASE:     Phase 123 - Master Academic UI & Pro Tactile Button Elevation
PURPOSE:   Functional & technical specifications for Duolingo/Brilliant-grade 3D physical press
           buttons, pure Oxford academic color palette, and complete elimination of AI vibe.
STANDARDS: UI/UX Pro Max, Pure Academic Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
-->

# Specification: Feature 027 — Phase 123 Master Academic UI & Pro Tactile Button Elevation

## 1. Problem Statement & Mission
Educational platforms require visceral tactile feedback, dignity, and visual stability. The presence of generic AI artifacts—such as translucent neon cyan halos, glowing purple/indigo drop-shadows, and flat, mushy button states—degrades student trust and institutional authority. Phase 123 elevates Ogrojatra to Duolingo/Brilliant-grade tactile button physics combined with Oxford and Cambridge scholarly typography and palette.

## 2. Requirements & Design Tokens

### A. Pure Academic Color Palette
- **Deep Oxford Academic Navy**: `#0A2540` / `#0F2942` (Primary brand, deep scholarly contrast, anchor elements).
- **Pure Paper White & Warm Scholarly Ivory**: `#FFFFFF` (Surface) & `#FAFAF8` (App background canvas).
- **Academic Forest Green**: `#065F46` / Depth `#033829` or `#044332` (Mastery success, correct answers, verified credentials).
- **Scholar Gold**: `#B45309` (Academic honors, Olympiad distinctions, focus streaks).
- **Burgundy Crimson**: `#991B1B` / Depth `#5B1010` (Negative marking alerts, critical warnings, strict security).

### B. Pro Tactile 3D Physical Buttons
1. **Primary Action (Oxford Navy 3D)**:
   - Base: `#0A2540`
   - Bottom Ledge: `shadow-[0_4px_0_0_#051329]`
   - Hover: `hover:bg-[#0E3357]`
   - Press State: `active:translate-y-1 active:shadow-none`
   - Ergonomics: `rounded-2xl font-semibold transition-all duration-140`
2. **Secondary / Quiz Option (Pure Paper White 3D)**:
   - Base: `bg-white text-slate-800`
   - Border: `border border-slate-300`
   - Shadow & Press: `shadow-sm active:translate-y-0.5 rounded-2xl`
   - Hover: `hover:bg-slate-50`
3. **Mastery Success Button (Academic Forest Green 3D)**:
   - Base: `bg-[#065F46] text-white`
   - Bottom Ledge: `shadow-[0_4px_0_0_#033829]` (or `shadow-[0_4px_0_0_#044332]`)
   - Press State: `active:translate-y-1 active:shadow-none`
   - Hover: `hover:bg-[#087858]`

### C. Typography Standards
- Bengali body & headings: `Hind Siliguri` (with comfortable line-height 1.75).
- Latin display titles: `Plus Jakarta Sans`.
- Numbers, dates, scores, timers: `Inter` (with `tabular-nums`).

### D. Zero AI Vibe & Zero Emoji
- Strictly no glowing neon shadows (`glow-blue`, `glow-teal`, etc.).
- Strictly no purple/indigo neon gradient cards.
- 100% vector SVG icons from `lucide-react` with 1.75px stroke width.
- Zero Unicode emoji glyphs anywhere in frontend or backend.
