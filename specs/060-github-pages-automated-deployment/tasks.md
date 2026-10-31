# Tasks: Automated GitHub Pages Deployment

- **Feature ID:** `060-github-pages-automated-deployment`
- **Domain:** DevOps / CI/CD / Static Site Generation / GitHub Pages
- **Status:** Completed
- **Zero-Emoji Discipline:** Strictly applied across all tasks and artifacts.

---

## Task Matrix

- [x] **Task 1: Specification & Planning**
  - [x] Create `specs/060-github-pages-automated-deployment/spec.md`
  - [x] Create `specs/060-github-pages-automated-deployment/plan.md`
  - [x] Create `specs/060-github-pages-automated-deployment/tasks.md`

- [x] **Task 2: Dynamic Next.js Configuration (`frontend/next.config.js`)**
  - [x] Implement conditional `isExport` detection via `process.env.NEXT_EXPORT === 'true' || process.env.GITHUB_ACTIONS === 'true'`.
  - [x] Implement dynamic `basePath` and `assetPrefix` resolving to `process.env.NEXT_PUBLIC_BASE_PATH || ''`.
  - [x] Configure `output: isExport ? 'export' : 'standalone'`.
  - [x] Configure `trailingSlash: isExport ? true : false`.
  - [x] Configure `images.unoptimized: isExport ? true : false`.
  - [x] Guard `headers()` so it is only present in non-export mode.

- [x] **Task 3: Export Scripts in `frontend/package.json`**
  - [x] Add `"build:pages": "NEXT_PUBLIC_BASE_PATH=/Student-Life-Circle NEXT_EXPORT=true next build && touch out/.nojekyll"` to `frontend/package.json`.
  - [x] Add `"deploy:pages": "npm run build:pages && bash ../scripts/deploy-gh-pages.sh"` to `frontend/package.json`.

- [x] **Task 4: Deployment Automation Script (`scripts/deploy-gh-pages.sh`)**
  - [x] Create `scripts/deploy-gh-pages.sh` to stage static build with `.nojekyll` and push to `origin gh-pages`.
  - [x] Make script executable (`chmod +x scripts/deploy-gh-pages.sh`).

- [x] **Task 5: Repository README.md Update**
  - [x] Add deployment badges and live URL to `README.md`.
  - [x] Remove all legacy emojis to adhere to the strict Zero-Emoji policy.

- [x] **Task 6: Local Validation & Asset Verification**
  - [x] Execute `npm --prefix frontend run build:pages` locally.
  - [x] Verify `frontend/out/.nojekyll` exists.
  - [x] Verify `frontend/out/index.html` references `/Student-Life-Circle/_next/static/...`.
  - [x] Test standard build or development to ensure zero regressions for non-export modes.

- [x] **Task 7: Git Commit, Push & Remote Deployment**
  - [x] Stage all modified and new files.
  - [x] Commit with structured zero-emoji message.
  - [x] Push `main` to `origin main`.
  - [x] Push static export to `origin gh-pages`.

- [x] **Task 8: GitHub Repository Homepage Link & Topics Integration**
  - [x] Update repository homepage URL to `https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/` via `gh repo edit`.
  - [x] Enrich repository topics (`nextjs`, `react`, `fastapi`, `education`, `learning-platform`, `bangladesh`, `github-pages`, `tailwindcss`, `typescript`).
  - [x] Verify link display on GitHub repository About sidebar.

