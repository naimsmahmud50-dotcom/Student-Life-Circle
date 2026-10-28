# Feature Specification: Automated GitHub Pages Deployment for Student Life Circle

- **Feature ID:** 060-github-pages-automated-deployment
- **Status:** Completed
- **Primary Domain:** DevOps / CI/CD / Static Site Generation / GitHub Pages
- **Target URL:** `https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/`
- **Deployment Branch:** `gh-pages`

---

## 1. Problem Statement & User Story
The user wants to host the Student Life Circle frontend directly on GitHub Pages without requiring external hosting services, ensuring clients and recruiters can visit the live project 24/7 directly via GitHub without keeping their local computer running.

### User Story:
> As a project owner, I want my Next.js web application to be compiled into static assets and deployed to GitHub Pages, so that any visitor or client viewing my GitHub repository can immediately click the live URL to experience the application live without external cloud dependencies.

---

## 2. Functional Requirements
1. **Dynamic Base Path & Asset Prefix:**
   - When building for GitHub Pages, `basePath` and `assetPrefix` dynamically resolve to `/Student-Life-Circle` via environment variable `NEXT_PUBLIC_BASE_PATH`.
   - When building for local development or Vercel, `basePath` remains empty (`''`) to preserve root-level hosting compatibility.
2. **Static HTML Export Pipeline:**
   - Configure `next.config.js` to conditionally enable `output: 'export'` when `NEXT_EXPORT=true` or running in CI.
   - Set `images: { unoptimized: true }` during export to prevent runtime Next.js image optimization failures on static hosting.
   - Enforce trailing slashes (`trailingSlash: true`) for clean URL routing across GitHub Pages subdirectories.
3. **Jekyll Bypass Guard (`.nojekyll`):**
   - Automatically inject a `.nojekyll` file into the root of `out/` to prevent GitHub's Jekyll engine from discarding `_next/` static JavaScript and CSS assets.
4. **Deploy from Branch Architecture (`gh-pages`):**
   - To bypass GitHub OAuth App scope limitations (where standard Git tokens lack elevated `workflow` permissions needed to push `.github/workflows/`), static build artifacts are deployed directly to the dedicated `gh-pages` branch.
   - GitHub Pages serves the `gh-pages` branch at root (`/`).
   - One-command automated deployment script provided via `scripts/deploy-gh-pages.sh` and `npm --prefix frontend run deploy:pages`.
5. **Zero-Emoji Discipline:**
   - Pure Lucide SVG icons and strict zero-emoji compliance across all configuration, code, and documentation.

---

## 3. Acceptance Criteria
- [x] `frontend/next.config.js` builds both in standalone mode and static export mode without breaking either.
- [x] `npm --prefix frontend run build:pages` produces an `out/` directory containing all 44 HTML pages.
- [x] `.nojekyll` exists in `out/`.
- [x] Static assets reference `/Student-Life-Circle/_next/static/...`.
- [x] `gh-pages` branch created and pushed to `origin`.
- [x] `main` branch updated and pushed to `origin`.
- [x] README.md updated with live URL and badge.
