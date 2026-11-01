# Implementation Plan: Footer Contact Actions, Button Interactivity & Typography Elevation

## 1. Technical Architecture & Component Analysis

### Affected Component:
`frontend/src/components/layout/Footer.tsx`

### Technical Root Cause of Issues:
1. **Contact Placeholders & Inactivity:**
   - Hotline was represented as non-clickable text with a generic placeholder `১৬xxx (16xxx)` instead of an active `tel:` link.
   - Child helpline (`1098`) and Emergency (`999`) lacked `tel:` links and tactile button physics.
   - Email support used `font-mono`, giving it a jarring raw developer look rather than an elegant student platform aesthetic.
2. **Missing Links:**
   - Legal items (`অপ্রাপ্তবয়স্কদের তথ্য সুরক্ষা`, `সুরক্ষিত টিউশন ও এসক্রো সম্মতি`, `ব্যবহারের শর্তাবলী`) were plain `<li>` text rather than clickable `<Link>` components.
3. **Typography Distortion:**
   - Monospace class `font-mono` on Bengali text caused Linux/browser font fallbacks to use jagged generic glyphs.
   - Missing `font-bengali` and proper line heights on labels caused crowded Bengali letterforms.

---

## 2. Refactoring Strategy

### Step 1: Upgrade Contact Action Center
- Refactor the 4th column into an interactive Contact & Support Action Grid:
  - **হটলাইন (Hotline):**
    ```tsx
    <a
      href="tel:16250"
      className="flex items-center justify-between p-2.5 rounded-xl bg-white/90 dark:bg-[#152136]/90 border border-slate-200/80 dark:border-slate-700/60 hover:border-amber-400/80 hover:bg-amber-500/5 shadow-xs transition group"
    >
      <div className="flex items-center gap-2">
        <PhoneCall className="w-3.5 h-3.5 text-[#ED8E22]" />
        <span className="font-bengali font-semibold text-xs text-slate-700 dark:text-slate-300">হটলাইন:</span>
      </div>
      <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-300 dark:border-slate-600 font-sans font-bold text-xs tracking-wide group-hover:border-amber-400">১৬২৫০ (16xxx)</span>
    </a>
    ```
  - **শিশু হেল্পলাইন (Child Helpline):**
    Clickable `tel:1098` with emerald accent.
  - **জরুরি সেবা (Emergency Services):**
    Clickable `tel:999` with amber accent.
  - **ইমেইল সাপোর্ট (Email Support):**
    Clickable `mailto:support@ogrojatra.edu.bd` with `font-sans font-medium` and smooth tactile card design.

### Step 2: Make Legal, Governance & Bottom Buttons Interactive
- Convert Legal & Safety list items to `<Link href="...">` with subtle chevron / hover feedback:
  - `অপ্রাপ্তবয়স্কদের তথ্য সুরক্ষা` -> `/terms#child-safety`
  - `সুরক্ষিত টিউশন ও এসক্রো সম্মতি` -> `/tuition`
  - `ব্যবহারের শর্তাবলী` -> `/terms`
- Add interactive links / triggers to Tier 4 badges:
  - `বাংলা ও ইংরেজি সংস্করণ` -> Language toggle button or link
  - `জিরো-ইমোজি পলিসি` -> Link to `/about`
  - `WCAG 2.2 AAA` -> Link to accessibility declaration

### Step 3: Typography Elevation
- Remove all `font-mono` on Bengali text and buttons.
- Apply `font-bengali font-semibold` to all Bengali headings, labels, chips, and paragraphs.
- Use `font-sans font-bold` for numbers and codes.
- Set `tracking-normal` for Bengali strings.

---

## 3. Verification Plan
1. **Static Analysis & Typecheck:**
   - Execute `npx tsc --noEmit` in `frontend` to verify 0 errors.
2. **Unit Test Suite Verification:**
   - Run `backend/tests/test_phase98_1_app_shell_and_footer.py` to ensure all 10 tests pass.
   - Run `backend/tests/test_phase98_flagship_ui_elevation.py` footer assertions.
3. **Zero-Emoji Verification:**
   - Scan `Footer.tsx` and spec files for zero emoji characters.
4. **Static Export Build:**
   - Execute `npm --prefix frontend run build:pages` to ensure all 44 routes build cleanly.
5. **Git & Deploy Check:**
   - Commit changes, push to `main`, deploy to GitHub Pages.
