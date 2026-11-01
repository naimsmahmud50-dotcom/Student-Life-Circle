# Task Breakdown: Footer Contact Actions, Button Interactivity & Typography Elevation

## Task Status Checklist

- [x] Task 1: Audit and overhaul the Contact Action Center in `Footer.tsx`
  - Convert hotline into a clickable, tactile `tel:` action card preserving `১৬xxx` test invariant.
  - Convert child helpline (`১০৯৮`) and emergency (`৯৯৯`) into clickable `tel:` links with emergency styling.
  - Convert email support into an elegant, tactile card with `font-sans font-medium` (no `font-mono`).

- [x] Task 2: Make dead links and buttons fully interactive
  - Convert Legal & Safety items (`অপ্রাপ্তবয়স্কদের তথ্য সুরক্ষা`, `সুরক্ষিত টিউশন ও এসক্রো সম্মতি`, `ব্যবহারের শর্তাবলী`) to working Next.js `<Link>` elements.
  - Make Tier 4 bottom badges interactive (`বাংলা ও ইংরেজি সংস্করণ`, `জিরো-ইমোজি পলিসি`, `WCAG 2.2 AAA`).
  - Add interactive tooltips/hover states to accreditation and payment seals.

- [x] Task 3: Overhaul typography across all footer sections
  - Remove all `font-mono` on Bengali text to prevent jagged fallback glyphs.
  - Apply `font-bengali font-semibold` and `tracking-normal leading-relaxed` across Bengali labels, headings, and descriptions.
  - Use clean `font-sans font-bold` for numeric chips.

- [x] Task 4: Static analysis, unit tests and zero-emoji verification
  - Run `npx tsc --noEmit` to verify 0 TypeScript errors.
  - Run `backend/tests/test_phase98_1_app_shell_and_footer.py` (ensure 10/10 pass).
  - Run zero-emoji scanner on `Footer.tsx` and spec files.
  - Run `npm --prefix frontend run build:pages` to verify all 44 routes build cleanly.

- [x] Task 5: Commit, push to `main`, and deploy to GitHub Pages
  - Commit changes with zero-emoji message.
  - Push to `origin main`.
  - Deploy to GitHub Pages via deployment script.
  - Report final status to user.
