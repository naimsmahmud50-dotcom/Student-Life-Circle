# Feature Specification: Dignified Global Footer Atmospheric Aesthetic & Watermark

## 1. Context & Objective
The user requested an elite, bespoke background design for the website's Footer section (as depicted in the user-provided screenshot `media_1793081550967_f78d49b0.png`). The current footer has a flat, muted `#FAF8F3` background that lacks the majestic warmth, depth, radial sunburst glow, and typographic watermarks established in the hero and flagship feature pages.

The objective is to transform the global institutional footer (`frontend/src/components/layout/Footer.tsx` and `frontend/src/components/goedu/GoEduFooter.tsx`) into an editorial masterpiece featuring:
- A warm sunshine/linen ambient canvas (`#FFF6DD` / `#FFFCF6`, dark: `#070C18`).
- A subtle geometric paper dot matrix grid (`radial-gradient(rgba(243, 172, 8, 0.14) 1px, transparent 1px)`).
- An upward-rising golden sunburst radial aura (`radial-gradient(ellipse 75% 85% at 50% 100%, ...)`).
- A giant typographic watermark (`OGROJATRA`) spanning across the background behind the editorial tiers.
- Frosted warm golden accreditation ribbon for Tier 1 compliance.
- Warm ivory card treatment for Brand & Mission, tactile micro-badges for hotline numbers, and a dedicated trust shelf for national payment rails (bKash, Nagad, SSLCommerz).
- Strict adherence to the zero-emoji policy, WCAG 2.2 AAA contrast, and responsive layout.

## 2. Functional Requirements
- **FR-01**: Root footer wrapper must have warm sunshine canvas with `relative overflow-hidden` containing the sunburst glow and typographic watermark layer in `z-0` without blocking clicks or text selection on content.
- **FR-02**: Giant typographic watermark text `OGROJATRA` rendered with clip-path gradient `linear-gradient(to bottom, rgba(243, 172, 8, 0.22) 15%, rgba(253, 215, 70, 0.02) 100%)` and responsive clamp size.
- **FR-03**: Tier 1 compliance bar elevated with warm golden frosted banner `bg-[#FFF1C2]/90 dark:bg-[#0B132B]/90`, subtle amber border, and crisp status pills.
- **FR-04**: Tier 2 editorial columns structured with `relative z-10`. Column 1 (Brand & Mission) elevated into a frosted warm ivory container with amber hairline border and emerald transparency pill.
- **FR-05**: Interactive navigation links in Columns 2, 3, 4, 5 enhanced with smooth hover transitions, golden amber hover colors (`hover:text-[#ED8E22]`), and subtle micro-indicator bullets.
- **FR-06**: Tier 3 payment rails wrapped in a dedicated frosted trust shelf `bg-white/85 dark:bg-[#121B2D]/85` with crisp verified merchant badges.
- **FR-07**: Tier 4 copyright bar aligned with warm amber divider and WCAG 2.2 AAA live status dot.
- **FR-08**: Secondary `GoEduFooter.tsx` also elevated with the warm sunshine canvas, sunburst aura, and watermark to maintain complete application-wide consistency.

## 3. Non-Functional & Security Constraints
- **Zero-Emoji Policy**: Absolutely zero emojis in code, markup, comments, or UI.
- **Security & XSS**: No raw `dangerouslySetInnerHTML`, sanitized SVG definitions, valid accessible attributes.
- **Accessibility**: Full WCAG 2.2 AAA compliance, aria-hidden on decorative watermark and glow elements, semantic landmarks.
- **Port Discipline**: Exclusively running on port 3002.
