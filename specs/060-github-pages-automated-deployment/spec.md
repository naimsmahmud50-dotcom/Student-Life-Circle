# Feature Specification: Automated GitHub Pages Deployment for Student Life Circle

- **Feature ID:** 060-github-pages-automated-deployment
- **Status:** In Progress
- **Primary Domain:** DevOps / CI/CD / Static Site Generation / GitHub Actions
- **Target URL:** `https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/`

---

## 1. Problem Statement & User Story
The user wants to host the Student Life Circle frontend directly on GitHub Pages without requiring external hosting services, ensuring clients and recruiters can visit the live project 24/7 directly via GitHub without keeping their local computer running.

### User Story:
> As a project owner, I want my Next.js web application to be automatically compiled into static assets and deployed to GitHub Pages whenever code is pushed to `main`, so that any visitor or client viewing my GitHub repository can immediately click the live URL to experience the application live.

---

## 2. Functional Requirements
1. **Dynamic Base Path & Asset Prefix:**
   - When building for GitHub Pages, `basePath` and `assetPrefix` must dynamically resolve to `/Student-Life-Circle` via environment variable `NEXT_PUBLIC_BASE_PATH`.
   - When building for local development or Vercel, `basePath` remains empty (`''`) to preserve root-level hosting compatibility.
2. **Static HTML Export Pipeline:**
   - Configure `next.config.js` to conditionally enable `output: 'export'` when `NEXT_EXPORT=true` or running in GitHub Actions.
   - Set `images: { unoptimized: true }` during export to prevent runtime Next.js image optimization failures on static hosting.
   - Enforce trailing slashes (`trailingSlash: true`) for clean URL routing across GitHub Pages subdirectories.
3. **Jekyll Bypass Guard (`.nojekyll`):**
   - Automatically inject a `.nojekyll` file into the root of `out/` to prevent GitHub's Jekyll engine from discarding `_next/` static JavaScript and CSS assets.
4. **Automated GitHub Actions Deployment Workflow:**
   - Create `.github/workflows/deploy-pages.yml` triggering on `push` to `main` branch.
   - Concurrency group `pages` with `cancel-in-progress: true` to prevent concurrent race conditions.
   - Permissions configured with `pages: write` and `id-token: write`.
   - Setup Node.js 20, install frontend dependencies (`npm ci`), run export build, and deploy via `actions/deploy-pages@v4`.
5. **Zero-Emoji Discipline:**
   - Pure Lucide SVG icons and strict zero-emoji compliance across all artifacts.

---

## 3. Acceptance Criteria
- [ ] `frontend/next.config.js` builds both in standalone mode and static export mode without breaking either.
- [ ] `npm --prefix frontend run build` with `NEXT_EXPORT=true` produces an `out/` directory containing all 44 HTML pages.
- [ ] `.nojekyll` exists in `out/`.
- [ ] `.github/workflows/deploy-pages.yml` is validated for YAML syntax and correct GitHub Actions schema.
- [ ] Changes committed and pushed to `main` on `origin`.
