# Feature Specification: 061-career-page-atmospheric-redesign

## 1. Executive Summary & Problem Statement
The Career Guideline & Job Hub (`frontend/src/pages/career.tsx`) features an elevated, atmospheric top hero banner (`CareerStatsHeader.tsx`) with warm amber sunburst lighting (`rgba(255, 178, 0, 0.45)` aura), large typographic watermark `CAREER`, frosted metric cards, and refined badge styling. However, the subsequent lower sections of the page (`CareerSearchFilterBar`, `CareerCategoryGrid`, `CareerJobBoard`, `CareerATSApplicationPipeline`, `GovtCircularsAndCareerGuide`, and the cryptographic skills/snapshot section) currently present a plain, flat border-and-white card aesthetic that lacks atmospheric depth and visual continuity.

The user has instructed:
"upore paray design ache kintu nicher para gula kono design nai tmr uchit akhn uporer design ar dharabahikotay nicher para gula design kora tbe design same copy kora jabena design thik rekhe halka kore aro sundor vabe design kore diba avabe full page design kore diben tbe ajonno apnr sokol skill kaje lagaite paren /design /swiper /motion /speckit /using-superpowers design ses kore tmi code chack diye fix kore felba jodi kno bug dhora pore r tmi path paicho onnno kno code a jhamela korba na jei path paicho sei path ai kaj korba do it"

## 2. Goals & Non-Goals
### Goals
1. **Atmospheric Aesthetic Continuity:** Elevate each lower section with custom radial lighting, subtle chromatic palettes, and ambient watermarks that harmonize with the hero without raw copy-pasting.
2. **Distinct Harmonic Themes:**
   - **Search & Filter Console (`CareerSearchFilterBar`):** Warm frosted ivory console with luminous focus states, tactile filter pills, and refined badge toggles.
   - **Job Categories Matrix (`CareerCategoryGrid`):** Fresh emerald/sage atmospheric container (`bg-[#F7FCF9] dark:bg-[#081816]`, watermark `SECTORS`, soft emerald aura), elevated frosted cards with icon glows, and smooth swiper/horizontal scroll feeling on mobile.
   - **Live Job Board (`CareerJobBoard`):** Oxford navy & ivory atmospheric feed (`bg-[#FAFBFD] dark:bg-[#0A1220]`, watermark `VACANCIES`), elevated job cards with tactile 3D apply buttons, salary badges with Bangladeshi currency styling, and enhanced metadata chips.
   - **ATS Application Pipeline (`CareerATSApplicationPipeline`):** Indigo/slate workspace atmosphere (`bg-[#F8FAFC] dark:bg-[#09111E]`, watermark `PIPELINE`), enhanced stepper dots, and glowing interview callout card.
   - **Government Circulars & Career Guides (`GovtCircularsAndCareerGuide`):** Deep pine & gold sealed gazette aesthetic, styled salary benchmarks table, numbered preparation roadmap cards, and interactive FAQ accordions.
   - **Verifiable Skills & Cryptographic CV Snapshot (`career.tsx`):** Oxford midnight digital ledger aesthetic (`bg-[#F9FAFB] dark:bg-[#070D18]`, watermark `VERIFIED`), glowing SHA-256 hash capsule, copy feedback, and interactive evidence cards.
3. **Strict Zero-Emoji Discipline:** Pure Lucide SVG icons only across all components.
4. **Strict Scope Lock:** Modify exclusively `frontend/src/pages/career.tsx` and files inside `frontend/src/components/career/`. Do not touch any other pages or buttons.
5. **Zero TypeScript Errors & 100% Test Pass:** Ensure zero compiler warnings and all tests pass.

### Non-Goals
- No backend API route modifications.
- No changes to tuition, live challenge, or other pages.
- No third-party heavy dependencies that break static export.

## 3. User Scenarios & Acceptance Criteria
- **Scenario 1:** The user visits `/career/` and scrolls through the page. Every section feels integrated, editorial, and atmospheric, matching the caliber of the top hero header.
- **Scenario 2:** The user switches between tabs (`jobs`, `pipeline`, `circulars`, `skills`). Each tab reveals a themed atmospheric section with tailored lighting and clear typographic watermarks.
- **Scenario 3:** The user filters by category or search term in the search bar. The search bar provides refined interactive feedback and tactile pill states.
- **Scenario 4:** Static export and test validation (`tsc --noEmit` and `node --test`) run with zero errors.
