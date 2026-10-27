# Feature Specification: Deep Pine Emerald Concentric Rings Institutional Footer

## 1. Context & User Rationale
The user provided a visual reference image (`media_1793082461636_3d6cf2bd.png`) showcasing a deep pine emerald background design featuring:
- A deep forest emerald / pine teal canvas (`#071F1A` to `#0C2B24`).
- Ambient glowing mint/emerald radiance on the left.
- Large, elegant concentric geometric vector circular rings on the right.
- Explicit instruction: "aikhane manus r lekha betito tmi ciaile aita use korte paro ai design ta kintu sundor dekha jacche" (Excluding the human figure and the text, use this exact background aesthetic for the footer).

## 2. Design Architecture
- **Canvas Root**: `bg-[#071F1A]` with vertical and diagonal forest teal gradients (`from-[#071F1A] via-[#0C2B24] to-[#051713]`).
- **Horizon Boundary**: A hairline luminous mint-emerald gradient line (`bg-gradient-to-r from-transparent via-emerald-400 to-transparent h-[2px]`) at the top edge.
- **Ambient Radiant Lighting**:
  - Top-left glowing mint illumination: `radial-gradient(circle at 12% 25%, rgba(16, 185, 129, 0.35) 0%, rgba(13, 148, 136, 0.15) 45%, transparent 70%)`
  - Subtle right-side ambient emerald aura: `radial-gradient(circle at 85% 65%, rgba(5, 150, 105, 0.20) 0%, transparent 60%)`
- **Concentric Geometric Orbital Rings**:
  - Vector SVG layers containing large concentric circular arcs in varying stroke widths (24px to 48px) and emerald/teal opacities (15% to 28%), positioned on the right and intersecting seamlessly across the canvas without obstructing text or interactions.
- **Tier 1 (Accreditation Bar)**: Deep emerald frosted ribbon (`bg-[#0A241E]/90 border-b border-emerald-900/60 backdrop-blur-md`) with emerald NCTB 2026 badge and dark glass compliance chips.
- **Tier 2 (5-Column Navigation Grid)**:
  - Column 1 (Brand & Mission): Frosted deep-emerald glass container (`bg-[#0C2D25]/85 border border-emerald-600/30 shadow-2xl backdrop-blur-md`) with Oxford Navy shield and amber graduation cap.
  - Columns 2-5: Headings in `text-emerald-200`, links in `text-emerald-100/75 hover:text-white hover:translate-x-1` with interactive amber bullets.
  - Tactical hotline chips for 16xxx, 1098, 999.
- **Tier 3 (Verified Payment Rails)**: Dedicated frosted emerald trust shelf (`bg-[#0C2D25]/85 border border-emerald-600/35 shadow-2xl backdrop-blur-md`) with bKash, Nagad, and SSLCommerz badges.
- **Tier 4 (Copyright Bar)**: Hairline divider with live pulsing WCAG 2.2 AAA badge and zero-emoji policy statement.
- **Application Alignment**: Uniformly applied to `frontend/src/components/layout/Footer.tsx` and `frontend/src/components/goedu/GoEduFooter.tsx`.

## 3. Strict Non-Negotiables
- **Zero-Emoji Policy**: Zero emojis anywhere in code, markup, comments, or UI.
- **Security & Hardening**: Pure sanitized SVG vectors, no raw innerHTML, WCAG 2.2 AAA compliance.
- **Port Discipline**: Running exclusively on port 3002.
