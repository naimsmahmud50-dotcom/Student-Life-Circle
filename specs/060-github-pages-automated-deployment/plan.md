# Technical Plan: Automated GitHub Pages Deployment

- **Feature ID:** `060-github-pages-automated-deployment`
- **Domain:** DevOps / CI/CD / Static Site Generation / GitHub Pages
- **Target URL:** `https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/`
- **Repo Remote:** `https://github.com/naimsmahmud50-dotcom/Student-Life-Circle.git`
- **Zero-Emoji Discipline:** Strictly applied across all configuration, workflows, scripts, and documentation.

---

## 1. Architecture Overview

GitHub Pages hosts static files from a repository. For a project repository (not a `<user>.github.io` root user repository), the site is served under a subpath:
`https://<username>.github.io/<repository-name>/` -> `https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/`

To make Next.js 15 render seamlessly in this environment:
1. **Dynamic Base Path:** Next.js prepends `/Student-Life-Circle` to all internal routing, CSS, and JS chunks when exported for GitHub Pages, while preserving `''` for local development.
2. **Static Export Mode:** Next.js compiles all pages to pure static HTML, CSS, and JS into `frontend/out/`.
3. **Nojekyll Guard:** GitHub Pages runs Jekyll by default, which ignores directories starting with an underscore (such as `_next/`). Adding `out/.nojekyll` bypasses Jekyll processing and ensures all assets load properly.
4. **Deploy from Branch (`gh-pages`):** Deploying the compiled static assets directly to the `gh-pages` branch allows GitHub Pages to serve the live site immediately without requiring elevated OAuth `workflow` permissions that are restricted on standard developer tokens.

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

### Phase 2: Build & Deployment Automation
- Add `build:pages` and `deploy:pages` scripts to `frontend/package.json`.
- Create `scripts/deploy-gh-pages.sh` to compile static assets, inject `.nojekyll`, and push cleanly to `origin gh-pages`.

### Phase 3: Documentation & Repository Verification
- Update `README.md` with:
  - Official GitHub Pages live link
  - Deployment status and branch badge
  - Setup instructions
  - Complete zero-emoji cleanup

### Phase 4: Git Commit & Remote Verification
- Stage all changes.
- Commit with zero-emoji structured message.
- Push `main` to `origin main`.
- Push static export to `origin gh-pages`.
