# Bug Assessment: UI Language Architecture Standardization (English UI Chrome with Dynamic Question Language)

## 1. Problem Description
The user reported an architectural mismatch regarding language localization across the web application:
- **Reported Issue**: The platform's UI chrome (navigation tabs 1-19, header bar, buttons, action controls, metric cards, status badges, forms, and tables) was authored in Bengali.
- **Architectural Mandate**: 
  1. The entire platform interface (navigation, dashboards, tabs, buttons, KPI metrics, modal dialogues, filters, settings) MUST be in international, crisp, professional English (`/ui-ux-pro-max` standard).
  2. Only the academic quiz questions, problem stems, mathematical equations, and answer options should adapt dynamically according to the student's chosen curriculum/language (e.g. NCTB Bengali Medium vs English Version / Edexcel / Cambridge).
  3. The quiz testing engine must feature a live Question Language / Medium Switcher (`English | Bengali`) allowing students to switch question content without changing the English system interface.

---

## 2. Root Cause Analysis
1. Early prototype iterations conflated student demographics (learners in Bangladesh) with UI language, incorrectly translating system chrome, buttons, and navigation into Bengali.
2. In reality, modern national and international platforms (e.g., Shikho, 10 Minute School, LeetCode, HackerRank, Coursera, Codeforces) preserve all UI controls, timers, submit buttons, status pills, and scorecards in English, while allowing educational content (STEM or literature questions) to adapt to the student's language/curriculum.

---

## 3. Remediation Strategy
1. **System UI Chrome Refactoring (English Only)**:
   - Change HTML `<html lang="en">` and update `<title>` to `Agrojatra | Student Life Circle - Enterprise Growth Platform`.
   - Update developer notes and architecture highlights banner to English.
   - Refactor all 19 navigation tabs to standard English labels.
   - Refactor all buttons ("Submit Answer", "Start Sprint", "Quarantine Item", "Verify HMAC", "Grant Bilateral Consent", "Export Ledger", "Book Session", "Reset", "Filter") to English.
   - Refactor all metric cards, badges, table columns, tooltips, and status indicators across all 19 tabs to English.
   - Update all dynamic JavaScript DOM mutations, toasts, status badges, and alert strings to English.
2. **Academic Question / Quiz Content Dynamic Language Selector**:
   - Introduce a prominent Question Medium Switcher (`English | Bengali`) in the Practice Engine, Live Olympiad, Admission Hub, and CAT Exam tabs.
   - When **English** is selected (Default/Recommended): Problem stems, questions, and options are displayed in English.
   - When **Bengali** is selected: Problem stems and options adapt to the NCTB Bengali curriculum, while all surrounding buttons, timers, submit controls, and scorecards remain strictly in English.
3. **Typography & Styling**:
   - Update Tailwind font family to `Inter, Plus Jakarta Sans, system-ui, sans-serif` with Bengali Unicode fallback.
   - Retain dual-theme obsidian dark mode (`#0B0F19`) and clean light mode (`#F8FAFC`).
   - Strictly adhere to zero-emoji policy with Lucide SVG icons.
4. **Synchronize Files**:
   - Apply changes to `preview.html` and mirror to `interactive_preview.html`.
   - Verify backend unit tests (141/141 passing).
