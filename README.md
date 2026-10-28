# Student Life Circle (অগ্রযাত্রা)

> **Bangladesh's Premier Whole-Journey Learning, Career & Academic Growth Platform**

[![GitHub Pages Deployment](https://github.com/naimsmahmud50-dotcom/Student-Life-Circle/actions/workflows/deploy-pages.yml/badge.svg)](https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success?style=flat&logo=github)](https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/)

**Live Production Preview:** [https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/](https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/)

Student Life Circle is an all-in-one educational and career growth ecosystem designed specifically for secondary, higher-secondary, and university students across Bangladesh. Featuring interactive NCTB curriculum learning, KaTeX-rendered practice quizzes, university admission guidance, verified tutoring dual-escrow, and career credentials.

---

## Live Deployment & GitHub Pages

This repository is configured with an automated Continuous Deployment (CD) pipeline via GitHub Actions. Whenever changes are merged or pushed to the `main` branch, the Next.js frontend is automatically compiled into static HTML/CSS/JS with asset prefixing and published directly to GitHub Pages.

- **Production URL:** [https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/](https://naimsmahmud50-dotcom.github.io/Student-Life-Circle/)
- **CI/CD Workflow:** [.github/workflows/deploy-pages.yml](.github/workflows/deploy-pages.yml)
- **Deployment Status:** Real-time status visible via the badge above or under the GitHub repository Actions tab.

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
- **Deployment & Telemetry**: GitHub Actions (GitHub Pages), Docker, Nginx, Cloudflare HTTP/3, Prometheus OpenMetrics.

---

## Getting Started

### 1. Frontend Setup (Local Development)
```bash
cd frontend
npm install
npm run dev
```

### 2. Frontend Static Export (GitHub Pages Build)
```bash
cd frontend
npm run build:pages
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
