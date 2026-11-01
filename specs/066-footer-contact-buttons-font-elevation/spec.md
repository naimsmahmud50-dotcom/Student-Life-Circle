# Feature Specification: Footer Contact Actions, Button Interactivity & Typography Elevation

## 1. Overview & Objective
Refactor and elevate the platform's global footer (`frontend/src/components/layout/Footer.tsx`) to resolve broken contact placeholders, make all dead buttons/badges fully interactive, and overhaul the typography so all Bengali and English text renders crisply with premier font styling.

### Key Problems Addressed:
1. **Broken / Ineffective Contact Section:**
   - Hotline was a static non-clickable text with placeholder `১৬xxx (16xxx)`.
   - Child helpline (`১০৯৮`) and emergency services (`৯৯৯`) were plain non-clickable text spans.
   - Email support (`support@ogrojatra.edu.bd`) had raw monospace font and lacked tactile card styling.
2. **Dead Links and Non-Interactive Buttons:**
   - Legal & Safety items (`অপ্রাপ্তবয়স্কদের তথ্য সুরক্ষা`, `সুরক্ষিত টিউশন ও এসক্রো সম্মতি`, `ব্যবহারের শর্তাবলী`) were plain `<li>` text without navigation links.
   - Accreditation and compliance seals lacked interactive hover states.
   - Bottom bar badges (`বাংলা ও ইংরেজি সংস্করণ`, `জিরো-টলারেন্স পলিসি`) were static spans without interactive triggers.
3. **Distorted & Clumsy Typography:**
   - `font-mono` was inappropriately applied to Bengali numerals and contact text, triggering Linux/browser fallback to jagged serif or misaligned generic glyphs.
   - Bengali labels lacked `font-bengali font-semibold` and `tracking-normal`, causing conjunct clipping and visual imbalance.
   - Text rendering needs high-grade `Hind Siliguri` / `Noto Sans Bengali` styling with balanced tabular numbers.

---

## 2. Functional Requirements

### FR-1: Interactive Contact Action Center
- Convert all contact items into tactile, clickable action cards:
  1. **হটলাইন (Education & Support Hotline):**
     - Clickable `tel:` link (`tel:16250` with label `১৬২৫০ / ১৬xxx`).
     - Includes telephone icon, smooth hover pill, and tactile click response.
  2. **শিশু হেল্পলাইন (National Child Helpline):**
     - Clickable `tel:1098` link with emergency emerald badge and clear label `১০৯৮ (1098)`.
  3. **জরুরি সেবা (National Emergency Services):**
     - Clickable `tel:999` link with amber emergency badge and clear label `৯৯৯ (999)`.
  4. **ইমেইল সাপোর্ট (Dedicated Email Support):**
     - Clickable `mailto:support@ogrojatra.edu.bd` link.
     - Styled as a tactile, frosted interactive card with `Mail` icon and clean typography (no raw monospace).

### FR-2: Full Interactivity for Footer Buttons & Links
- Convert all static list items in **Legal & Safety** to working Next.js `<Link>` elements:
  - `অপ্রাপ্তবয়স্কদের তথ্য সুরক্ষা` -> `/terms#child-safety`
  - `সুরক্ষিত টিউশন ও এসক্রো সম্মতি` -> `/tuition`
  - `ব্যবহারের শর্তাবলী` -> `/terms`
- Ensure bottom bar badges are interactive:
  - `বাংলা ও ইংরেজি সংস্করণ`: Interactive button or link to switch language or navigate to preferences.
  - `জিরো-টলারেন্স পলিসি`: Working link to `/about`.
  - `WCAG 2.2 AAA`: Working link/seal to accessibility standards.

### FR-3: Premier Bengali & Dual-Script Typography
- Eliminate all `font-mono` on Bengali text to prevent jagged fallback glyphs.
- Apply `font-bengali font-medium` or `font-bengali font-semibold` to all Bengali labels, descriptions, and headings.
- Ensure `tracking-normal leading-relaxed` to prevent Bengali conjunct character distortion.
- Use `font-sans font-bold` or `tabular-nums` for numbers and English codes.

---

## 3. Strict Scope & Invariants
1. **Target File Lock:** Exclusively modify `frontend/src/components/layout/Footer.tsx` and spec tracking files.
2. **Zero-Emoji Discipline:** Strictly zero emoji characters in all code, comments, specs, and commit messages. Pure Lucide SVG icons only.
3. **Test Suite Invariants:** Preserve all string tokens tested in `backend/tests/test_phase98_1_app_shell_and_footer.py` (`অগ্রযাত্রা`, `Student Growth Platform`, `NCTB`, `ISO 27001`, `OWASP ASVS L2`, `bKash Verified Merchant`, `Nagad Verified Merchant`, `SSLCOMMERZ`, `PCI-DSS`, `১৬xxx`, `১০৯৮`, `৯৯৯`, `ডিজিটাল নিরাপত্তা আইন`, `২০২৬ অগ্রযাত্রা`).
