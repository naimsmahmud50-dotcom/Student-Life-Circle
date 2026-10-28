# Technical Plan: Live Challenge Hero - Exact Live MCQ Elevation

- **Feature Directory:** `specs/058-live-challenge-hero-exact-livemcq-elevation`
- **File to Elevate:**
  1. `frontend/src/components/live-challenge/LiveMcqHeroSection.tsx`
  2. `frontend/src/pages/live-challenge.tsx`
- **Design Inspiration:** Live MCQ Hero screenshot (`media_1793149966303_08d756b3.png`)

---

## 1. Visual Design Architecture

### 1.1 Cosmic Deep Canvas & Lighting System
- Canvas background:
  `bg-[#0A0E2A] bg-gradient-to-b from-[#090C22] via-[#0E153A] to-[#080B1E]`
- Angled subtle luminous streaks:
  SVG background overlay with light streaks angled at -70deg using semi-transparent white/cyan gradient bands.
- Luminous Core Aura:
  `radial-gradient(ellipse 65% 55% at 50% 35%, rgba(59, 130, 246, 0.25) 0%, rgba(99, 102, 241, 0.14) 40%, transparent 75%)`
- Floating Warm Golden Stardust:
  Subtle CSS particles positioned at key focal points with soft amber glow.

### 1.2 Peripheral Floating Elements
- **Floating Track Pills:**
  - `• BCS`: Positioned left (`bg-[#231E42]/80 border border-purple-500/30 text-purple-200`)
  - `• NTRCA`: Positioned bottom-left (`bg-[#231E42]/80 border border-purple-500/30 text-purple-200`)
  - `• Primary`: Positioned top-right (`bg-[#122A44]/80 border border-sky-500/30 text-sky-200`)
  - `• Bank`: Positioned mid-right (`bg-[#103430]/80 border border-emerald-500/30 text-emerald-200`)
  - `• BJS`: Positioned bottom-right (`bg-[#382F18]/80 border border-amber-500/30 text-amber-200`)
- **Educational Motifs:**
  - Mortarboard / Graduation cap with gold tassel on top-left
  - Open notebook line-art on bottom-left
  - Pencil / writing tool line-art on bottom-right

### 1.3 Central Hero Typography & Elements
- **Header Pill:** `• সঠিক প্রস্তুতি, সহজ প্রিলি` (`bg-[#1A2148]/90 border border-indigo-400/30 text-indigo-200`)
- **Headline:**
  - "ঘরে বসেই সকল প্রতিযোগিতামূলক" in clean white bold font
  - "চাকরির পূর্ণাঙ্গ প্রস্তুতি" in fiery orange-amber gradient (`from-[#FF5722] via-[#FF8A00] to-[#FFA000]`)
- **Subtitle:** Comprehensive candidate support text with `২৪ লাখ+` highlighted badge
- **Dual Pill CTAs:**
  - Button 1: Left Cyan-to-Cobalt gradient pill (`৪৫তম স্পেশাল বিসিএস / লাইভ অলিম্পিয়াড`)
  - Button 2: Right Orange-to-Coral gradient pill (`পরীক্ষা দিন`)
- **Active Exam Room Bar:** Server-authoritative timer, negative marking indicator, and rules modal button integrated cleanly without visual clutter.
- **App Platform Ecosystem:** "অ্যাপ ইনস্টল করুন" with Google Play, App Store, Windows, macOS, Web.

### 1.4 Bottom Docked Frosted Glass KPI Container
- Docked rounded container: `bg-[#0D1535]/85 backdrop-blur-xl border border-white/10 rounded-3xl p-6 sm:p-8 shadow-2xl`
- 4 Columns:
  1. Circular amber badge + `২৪ লাখ+` + `অ্যাপ ব্যবহারকারী`
  2. Circular amber badge + `৭.৫ লাখ+` + `আর্কাইভ MCQ (reference-সহ ব্যাখ্যা)`
  3. Circular amber badge + `৩০ হাজার+` + `প্রতিদিন গড় ব্যবহারকারী`
  4. Circular amber badge + `১০+` + `বছরের অভিজ্ঞতা`

---

## 2. Technical Quality & Verification Strategy

1. **Strict Zero-Emoji Policy:** Only Lucide SVGs allowed.
2. **TypeScript Integrity:** `tsc --noEmit` must pass with zero errors.
3. **Automated Testing:** Existing test suite must pass 45/45 tests.
4. **Security & Code Review:** Conduct Strix security sanity review on props, events, and inputs.
5. **Port Discipline:** Run on port 3002.
