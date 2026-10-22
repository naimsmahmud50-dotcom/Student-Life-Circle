/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Grand Public Production Launch & System Handover
 * TOPIC:     Phase 141 SEO, 64-District OpenGraph Engine, Production CI/CD & National Handover
 * FILE:      specs/044-phase141-grand-production-launch/tasks.md
 * PHASE:     Phase 141 - Grand Public Production Launch & Final Handover
 * PURPOSE:   Actionable, ordered tasks for Phase 141 implementation
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Full 64-District Support
 */

# Phase 141 Tasks: Grand Public Production Launch & Final Handover

- [x] **Task 1: 64-District Dataset & Dynamic OpenGraph Engine**
  - Implement `frontend/src/lib/districts.ts` with authentic data for all 64 districts (Bangla names, division, student counts, top streams).
  - Implement `frontend/src/pages/api/og.ts` delivering 1200x630 vector social cards with dark Oxford Navy styling, Bangla text, and edge caching.

- [x] **Task 2: SEO, Sitemap, Robots.txt & Structured Data**
  - Generate `frontend/public/sitemap.xml` with all 37 core application routes + district entry points.
  - Generate `frontend/public/robots.txt` with canonical sitemap pointer and protected route rules.
  - Create `frontend/src/components/seo/SEOHead.tsx` with canonical URLs, OpenGraph tags, Twitter cards, and JSON-LD schemas.

- [x] **Task 3: Production DevOps, CI/CD & Disaster Recovery**
  - Create `.github/workflows/production-deploy.yml` with automated test, build, and deploy steps.
  - Create `nginx/studentlifecircle.conf` with HTTPS, HTTP/2, HSTS, security headers, rate limiting, and caching.
  - Create `scripts/backup_database.sh` for automated encrypted database backups.
  - Create `scripts/rollback.sh` for instant release rollback.
  - Create `.env.production.example` documenting all production secrets.

- [x] **Task 4: Search Engine Indexing & Handover Operations Handbook**
  - Create `docs/seo/SEARCH_ENGINE_INDEXING_CHECKLIST.md` for Google Search Console and Bing Webmaster Tools.
  - Create `DEPLOYMENT_HANDBOOK.md` in repository root with architecture, incident runbooks, and maintenance guides.

- [x] **Task 5: Automated Test Suite & Pre-Launch Audit**
  - Implement `backend/tests/test_phase141_production_launch.py` covering:
    - Test 01: Mandatory Architecture Note headers.
    - Test 02: Strict Zero-Emoji compliance across all Phase 141 files.
    - Test 03: Complete 64-district dataset integrity and division coverage.
    - Test 04: OpenGraph SVG generation across sample districts.
    - Test 05: Sitemap XML syntax, route coverage, and canonical consistency.
    - Test 06: Robots.txt syntax and security disallow rules.
    - Test 07: JSON-LD structured data schema compliance.
    - Test 08: CI/CD workflow and deployment scripts validation.
    - Test 09: Production environment variable documentation.

- [x] **Task 6: Final Verification, Build, and Handover Artifact**
  - Run full repository test discovery (`python3 -m unittest discover -s backend/tests -p "test_*.py"`: 1,565 tests passing).
  - Run Zero-Emoji sweep (`python3 backend/scripts/run_zero_emoji_sweep.py`: 605 files certified).
  - Rebuild frontend (`npm run build`: 37/37 pages + dynamic `/api/og` compiled).
  - Generate `PHASE_141_PRODUCTION_LAUNCH_REPORT.md` artifact.
