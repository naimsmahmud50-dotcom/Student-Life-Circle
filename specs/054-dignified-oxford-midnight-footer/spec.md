# Feature Specification: Dignified Oxford Midnight Institutional Footer

## 1. Problem Statement & User Rationale
The previous iteration applied the exact same warm sunshine yellow palette (`#FFF6DD`), sunburst glow, and giant watermark to the Footer as the hero headers. The user rightly observed that repeating the identical visual treatment everywhere makes the platform feel repetitive and devoid of visual variety ("sob jaygay same design thakle ki valo dekha jabe?").

A world-class academic and national platform requires a distinct, authoritative foundation. The footer must serve as the solid, dignified anchor of the entire platform, creating dramatic visual contrast with the warm sunshine pages above.

## 2. Design Vision: The Oxford Midnight Foundation
- **Canvas**: Deep Oxford Midnight Navy (`#060D1A` to `#0B192E`), evoking institutional authority, timeless gravitas, and national trust.
- **Horizon Line (Top Boundary)**: A hairline luminous gold-amber accent horizon (`bg-gradient-to-r from-transparent via-[#ED8E22] to-transparent h-[2px]`) providing a luxurious transition between the warm content above and the deep midnight footer.
- **Atmospheric Celestial Matrix**: A subtle celestial starlight dot grid (`radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px)`) with an ambient deep sapphire-cyan aurora glow (`radial-gradient(ellipse 65% 45% at 50% 0%, rgba(30, 58, 138, 0.30) 0%, transparent 100%)`).
- **Watermark Treatment**: Replaced the bright yellow watermark with an ultra-subtle, dignified architectural outline watermark `NATIONAL TRUST REPOSITORY` in `text-white/[0.025]`, ensuring zero visual clutter.
- **Tier 1 (Accreditation Bar)**: Deep indigo-navy frosted bar (`bg-[#0A1628]/95 border-b border-slate-800/80`) with glowing emerald NCTB 2026 badge and dark glass security chips.
- **Tier 2 (Editorial Columns)**:
  - Column 1 (Brand & Mission): Deep dark-glass frosted card (`bg-[#0D1D35]/80 border border-slate-700/60 shadow-xl backdrop-blur-md`) with Oxford Navy shield and amber graduation cap.
  - Columns 2-5: Crisp white headings with amber accent lines, high-contrast slate text (`text-slate-300`), luminescent hover states (`hover:text-white hover:translate-x-1`), and interactive amber bullets.
  - Contact hotline cards: Color-coded dark glass tactile chips for 16xxx, 1098, 999.
- **Tier 3 (Payment Rails)**: Dedicated dark glass trust platform (`bg-[#0D1D35]/90 border border-slate-700/70 shadow-xl`) with high-contrast official SVG badges for bKash, Nagad, and SSLCommerz.
- **Tier 4 (Copyright Bar)**: Deep slate divider with animated pulse WCAG 2.2 AAA badge and zero-emoji compliance indicator.
- **Application Alignment**: Applied to both `frontend/src/components/layout/Footer.tsx` and `frontend/src/components/goedu/GoEduFooter.tsx`.

## 3. Strict Non-Negotiables
- **Zero-Emoji Policy**: Absolutely zero emojis across code, markup, comments, and UI.
- **Security & Strix Hardening**: 100% sanitized SVGs, zero unsafe scripts or innerHTML, valid accessible attributes, WCAG 2.2 AAA contrast standards.
- **Port Discipline**: Exclusively running on port 3002.
