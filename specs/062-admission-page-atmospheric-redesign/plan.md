# Implementation Plan: 062-admission-page-atmospheric-redesign

## 1. Architectural Strategy
We elevate `frontend/src/pages/admission.tsx` by introducing:
- A 4-metric admission telemetry bar at the base of the hero.
- An interactive master tab switcher (`activeTab: 'targets' | 'counseling' | 'migration' | 'strategy' | 'faqs'`).
- In `targets` tab:
  - Atmospheric Search & Filter Console with warm amber aura.
  - Atmospheric Blueprint Canvas with radial Oxford Navy aura and typographic watermark `BLUEPRINT`.
  - Elevated university target cards featuring institutional monograms (DU, BUET, DMC, GST), negative marking pills, cut-off probability progress bars, and tactile 3D action buttons.
- In `counseling` tab:
  - Atmospheric container with watermark `COUNSELING`, rendering the existing `AdmissionCounselingMatrix` component.
- In `migration` tab:
  - Atmospheric container with watermark `CASCADE`, rendering the existing `MigrationCascadeVisualizer` component.
- In `strategy` tab:
  - Atmospheric container with watermark `STRATEGY` containing negative marking penalty minimization tactics and subject weightage breakdown table.
- In `faqs` tab:
  - Atmospheric container with watermark `POLICIES` containing accordion for admission rules, second-timer policies, and calculator approvals.

## 2. Verification Protocol
1. TypeScript compilation: `npx tsc --noEmit` in `frontend/`.
2. Python Zero-Emoji audit on `frontend/src/pages/admission.tsx` and spec files.
3. Static page build: `npm --prefix frontend run build:pages`.
4. Git commit and GitHub Pages deployment script: `bash scripts/deploy-gh-pages.sh`.
