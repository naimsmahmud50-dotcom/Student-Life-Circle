# Feature Specification: 062-admission-page-atmospheric-redesign

## 1. Executive Summary & Problem Statement
The University Admission Preparation Hub (`frontend/src/pages/admission.tsx`) features a dignified, atmospheric top hero banner with warm amber sunburst lighting (`rgba(255, 178, 0, 0.45)` aura), large typographic watermark `ADMISSION`, badge pills, and a cut-off forecaster CTA banner. However, the subsequent lower sections of the page currently consist of plain, unstyled filter buttons and raw white blueprint cards with flat borders and no atmospheric canvas, lighting, or visual storytelling.

The user has instructed:
"prothom paray design ache baki para gula design nai akhn tmr kaj holo tmi path khuje paciho onno kno path a jhamela na kore akdom jei path tmi khuje paich sei path ar design ta tmi nicher para gula uporer sathe thik rekhe design kore felo tbe mne rekho akdom copy paste design jate na hoy akkhere obossoi sotorko thakba best design diba ,, design korar time tmi tmr sokol skill jmn /design /ui-styling /ui-ux-pro-max joto designing skilll ache sob skill kaje lagiye kaj suru kore dibe akta bisoy note kore felo tmk jei path dewya hoilo sei path betito proyojon chara onno kno path a hat diba na onno kno code nosto korba na tmi mne rakhba tmr kaj jeita dewya hoiche sudhu sei kaj ta tmi kroba onno kothaw onno code a jhamela korba na.."

## 2. Goals & Non-Goals
### Goals
1. **Atmospheric Aesthetic Continuity:** Elevate the lower sections of `frontend/src/pages/admission.tsx` with bespoke radial lighting, thematic typographic watermarks, frosted glass containers, tactile 3D buttons, and institutional insignia without making a duplicate copy of the hero.
2. **Distinct Themed Sections:**
   - **Interactive Platform Metric Counter Bar:** 4 frosted metric cards showcasing admission clusters, total seats, verified mocks, and negative marking simulator.
   - **Master Admission Hub Tab Controller:** Seamless switcher between `targets` (University Blueprints & Mocks), `counseling` (Gale-Shapley Stable Matching Matrix), `migration` (Multi-round Seat Reallocation Cascade), `strategy` (Negative Marking Minimization & Subject Weightage), and `faqs` (Admission Policies & Rules).
   - **University Search & Multi-Vector Filter Console:** Frosted ivory and amber console with glowing focus ring, university category chips with item counts, and tactile active states.
   - **Live University Blueprint Feed (`BLUEPRINT`):** Oxford Navy and ivory atmospheric canvas, ambient watermark `BLUEPRINT`, bespoke university monograms (DU, BUET, DMC, GST), Burgundy crimson negative marking pills, animated cut-off probability bars, and 3D tactile buttons (`ডায়াগনস্টিক টেস্ট` & `মডেল টেস্ট দিন`).
   - **Integrated Admission Counseling Matrix (`COUNSELING`):** Interactive preference stack builder with Pareto-optimal deferred acceptance.
   - **Integrated Migration Cascade Visualizer (`CASCADE`):** Cross-admission seat ripple simulation showing vacancy promotions.
   - **Negative Marking Strategy & Guidelines (`STRATEGY`):** 4 strategic cards on penalty minimization, pacing algorithms, subject weightages, and calculator rules.
   - **Admission FAQ Accordion (`POLICIES`):** Accordion covering second-timer rules, non-programmable calculator lists, and quota verifications.
3. **Strict Zero-Emoji Discipline:** Pure Lucide SVG icons only. No emoji characters anywhere in code, commits, or responses.
4. **Strict Scope Lock:** Modify exclusively `frontend/src/pages/admission.tsx`. Do not touch any other pages or buttons.
5. **Zero TypeScript Errors & 100% Production Build:** Ensure `npx tsc --noEmit` and `npm --prefix frontend run build:pages` succeed with zero errors.

### Non-Goals
- No backend API route modifications.
- No modifications to files outside `frontend/src/pages/admission.tsx`.
