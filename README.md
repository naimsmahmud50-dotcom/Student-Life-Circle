# Student Life Circle (অগ্রযাত্রা)

> **Bangladesh's Premier Whole-Journey Learning, Career & Academic Growth Platform**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success?style=flat&logo=github)](https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/)
[![Deployment Branch](https://img.shields.io/badge/Deployment%20Branch-gh--pages-blue?style=flat&logo=git)](https://github.com/naimsmahmud50-dotcom/Student-Life-Circle/tree/gh-pages)

**Live Production URL:** [https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/](https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/)

Student Life Circle is an all-in-one educational and career growth ecosystem designed specifically for secondary, higher-secondary, and university students across Bangladesh. Featuring interactive NCTB curriculum learning, KaTeX-rendered practice quizzes, university admission guidance, verified tutoring dual-escrow, and career credentials.

---

## Live Deployment & GitHub Pages

This repository is published live on GitHub Pages directly from the `gh-pages` branch. The Next.js frontend is compiled into static HTML/CSS/JS with asset prefixing and `.nojekyll` protection to ensure seamless 24/7 client previews without requiring a local development server.

- **Production Live URL:** [https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/](https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/)
- **Deployment Branch:** [gh-pages](https://github.com/naimsmahmud50-dotcom/Student-Life-Circle/tree/gh-pages) (serves from `/` root)
- **Automated Deployment Script:** `scripts/deploy-gh-pages.sh`

---

## Core Architecture & Capabilities

1. **Interactive Learn Hub**: NCTB aligned chapter-by-chapter curriculum with interactive video player, notes, and circular progress tracking.
2. **Practice Quiz Arena**: KaTeX mathematical stem rendering, real-time timer countdowns, and instant explanatory feedback.
3. **University Admission Engine**: Departmental cut-off probability calculators, past admission test archives, and unit-wise preparation matrices.
4. **Verified Tuition Escrow**: Safe student-tutor marketplace with dual-party milestone protection and bKash/Nagad digital payment gateways.
5. **Career Ledger & Portfolio**: Cryptographically verifiable extracurricular credentials with automated PDF resume export.
6. **Socratic AI Tutor**: Real-time context-aware academic assistant offering step-by-step conceptual problem solving.

---

## Technology Stack

- **Frontend**: Next.js 15, React 19, TypeScript, Tailwind CSS, Lucide Icons, Motion, Swiper, KaTeX.
- **Backend**: FastAPI (Python 3.11), Uvicorn, PostgreSQL, Redis, Pydantic.
- **Testing & E2E**: Playwright, Jest, Vitest, Unittest.
- **Deployment & Telemetry**: GitHub Pages (`gh-pages`), Docker, Nginx, Cloudflare HTTP/3, Prometheus OpenMetrics.

---

## Getting Started

### 1. Frontend Setup (Local Development)
```bash
cd frontend
npm install
npm run dev
```

### 2. Frontend Static Export & Deploy to GitHub Pages
```bash
# Build static export locally into frontend/out
npm --prefix frontend run build:pages

# Build and push directly to GitHub Pages branch
npm --prefix frontend run deploy:pages
```

### 3. Backend Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

---

## License

Developed by **Mahmud Hasan** for the students of Bangladesh.  
Copyright (c) 2026 Student Life Circle. All Rights Reserved.
