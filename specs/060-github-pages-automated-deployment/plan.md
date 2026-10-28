# Technical Plan: Automated GitHub Pages Deployment

- **Feature ID:** `060-github-pages-automated-deployment`
- **Domain:** DevOps / CI/CD / Static Site Generation / GitHub Actions
- **Target URL:** `https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/`
- **Repo Remote:** `https://github.com/naimsmahmud50-dotcom/Student-Life-Circle.git`
- **Zero-Emoji Discipline:** Strictly applied across all configuration, workflows, scripts, and documentation.

---

## 1. Architecture Overview

GitHub Pages hosts static files from a repository. For a project repository (not a `<user>.github.io` root user repository), the site is served under a subpath:
`https://<username>.github.io/<repository-name>/` -> `https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/`

To make Next.js 15 render seamlessly in this environment:
1. **Dynamic Base Path:** Next.js must prepend `/Student-Life-Circle` to all internal routing, CSS, and JS chunks when exported for GitHub Pages, while preserving `''` for local development.
2. **Static Export Mode:** Next.js compiles all pages to pure static HTML, CSS, and JS into `frontend/out/`.
3. **Nojekyll Guard:** GitHub Pages runs Jekyll by default, which ignores directories starting with an underscore (such as `_next/`). Adding `out/.nojekyll` bypasses Jekyll processing and ensures all assets load properly.
4. **GitHub Actions Workflow:** A dedicated workflow triggers on every push to `main`, builds the frontend, and publishes the static artifacts directly to GitHub Pages via the official `actions/deploy-pages@v4`.

---

## 2. Configuration Matrix

| Environment | NEXT_EXPORT | NEXT_PUBLIC_BASE_PATH | output | basePath | images.unoptimized |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Local Dev | false | "" | undefined | "" | false |
| Local Build / Docker | false | "" | "standalone" | "" | false |
| GitHub Pages Export | true | "/Student-Life-Circle" | "export" | "/Student-Life-Circle" | true |

---

## 3. Implementation Phases

### Phase 1: Next.js Configuration Refinement
- Update `frontend/next.config.js` with conditional `isExport` and dynamic `basePath`.
- Ensure `headers()` is only defined when not in static export mode to avoid Next.js warnings.
- Set `trailingSlash: true` when exporting to ensure clean navigation across static subfolders.

### Phase 2: Build Scripts & Tooling
- Add `build:pages` script to `frontend/package.json`:
  `NEXT_PUBLIC_BASE_PATH=/Student-Life-Circle NEXT_EXPORT=true next build && touch out/.nojekyll`
- Validate local execution of `npm --prefix frontend run build:pages`.

### Phase 3: GitHub Actions CI/CD Pipeline
- Create `.github/workflows/deploy-pages.yml` with:
  - Branch filter: `main`
  - Concurrency group `pages`
  - Permissions: `contents: read`, `pages: write`, `id-token: write`
  - Node 20 setup, `npm ci`, `build:pages`
  - `actions/upload-pages-artifact@v3` targeting `frontend/out`
  - `actions/deploy-pages@v4`

### Phase 4: Documentation & Repository Verification
- Update `README.md` with:
  - Official GitHub Pages live link
  - Deployment status badge
  - Setup instructions
  - Complete zero-emoji cleanup
- Run static export verification and ensure asset URLs contain `/Student-Life-Circle/`.

### Phase 5: Git Commit & Push
- Stage all changes.
- Commit with zero-emoji structured message.
- Push to `origin main`.
- Provide exact user guidance for GitHub Repository Settings (Pages Source: GitHub Actions).
