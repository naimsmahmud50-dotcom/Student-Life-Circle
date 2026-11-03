# Technical Plan: Full-Site Bilingual (BN/EN) Internationalization Elevation

## 1. Architecture Overview & Data Flow

```
[ User Interaction ] ─── (Click 'BN' or 'EN' on Navbar/Footer)
        │
        ▼
[ I18nContext / useTranslation() ]
        │
        ├── Updates state: `locale = 'bn' | 'en'`, `isBengali = boolean`
        ├── Persists to `localStorage.setItem('slc_locale', locale)`
        ├── Writes HTTP Cookie: `NEXT_LOCALE`
        └── Re-renders subscribed React components instantaneously
                │
                ▼
      [ Flagship Landing Page (`index.tsx`) ]
        │
        ├── Evaluates `{isBengali ? 'বাংলা বার্তা' : 'English Message'}`
        ├── Translates numbers via `toBengaliDigits()` / `toEnglishDigits()`
        └── Preserves 100% of Tailwind CSS styling, responsive layout & physics
```

---

## 2. Implementation Strategy

### Component-Level Strategy in `frontend/src/pages/index.tsx`:
1. Use the existing `const { isBengali, t, formatNumber } = useTranslation();` hook.
2. For structured, multi-line blocks (such as the 4-in-1 comparison cards, the curated pathways, and the 3D lab descriptions), introduce clean, type-safe content lookup maps or inline dual-script expressions.
3. Keep all CSS class names (`className="..."`) exactly untouched.
4. Replace raw hardcoded Bengali strings with `{isBengali ? '<authentic_bengali>' : '<academic_english>'}`.
5. In countdown timer display, render formatted localized digits:
   ```tsx
   {isBengali ? toBengaliDigits(String(countdown.hours).padStart(2, '0')) : String(countdown.hours).padStart(2, '0')}
   ```

---

## 3. Section-by-Section Translation Mapping

1. **Hero & Top Badges**:
   - `জাতীয় শিক্ষাক্রম (NCTB) মানদণ্ডে পরিচালিত • ৬৪ জেলায় সমন্বিত` <-> `Aligned with National Curriculum (NCTB) • Integrated Across 64 Districts`
   - `৪টি প্রথাগত অ্যাপের একক বিকল্প • জাতীয় ডিজিটাল ক্যাম্পাস` <-> `Single Alternative to 4 Conventional Apps • National Digital Campus`
   - `স্বাগতম, ভবিষ্যৎ গড়ার অগ্রযাত্রায়` <-> `Welcome to the Journey of Shaping the Future`
   - `বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বিক ডিজিটাল ক্যাম্পাস` <-> `A Comprehensive Digital Campus for Every Student in Bangladesh`
   - `মাধ্যমিক (SSC ৯-১০)` <-> `Secondary (SSC 9-10)`
   - `উচ্চ মাধ্যমিক (HSC ১১-১২)` <-> `Higher Secondary (HSC 11-12)`
   - `বিশ্ববিদ্যালয় ভর্তি (Admission)` <-> `University Admission`
   - `টিউশন ও ক্যারিয়ার (Career)` <-> `Tuition & Career`
   - `পড়াশোনা শুরু করুন (Quick Resume)` <-> `Start Learning (Quick Resume)`
   - `বোর্ড প্রশ্ন ব্যাংক (২০১৫–২০২৫)` <-> `Board Question Bank (2015–2025)`
   - Trust strip items (NCTB curriculum, 10-year board questions, offline mesh sync, zero hidden fees).

2. **4-in-1 Platform Comparison**:
   - `৪টি ভিন্ন সাবস্ক্রিপশন নয় — অগ্রযাত্রায় সবই এক ছাতার নিচে` <-> `Not 4 Separate Subscriptions — Everything Under One Roof at Ogrojatra`
   - Cards: 10 Minute School, Live MCQ, Caretutors, Bdjobs alternatives.

3. **Academic Progress & Pedagogical Pillars**:
   - `আপনার শেখার অগ্রগতি ও ধারাবাহিকতা` <-> `Your Academic Progress & Consistency`
   - Daily goals, streak counters, mastery metrics.

4. **Curated Pathways (SSC, HSC, Admission, Career)**:
   - Pathway titles, syllabi completion badges, syllabus outlines.

5. **3D STEM Virtual Labs**:
   - Physics, Chemistry, KaTeX formula explanations, interactive lab launching triggers.

6. **Live Challenge & Socratic AI**:
   - Countdown timer labels, live participant metrics, Socratic AI modal triggers.

7. **W3C Certificate Showcase**:
   - Cryptographic verification badge, blockchain-grade hash, QR verification preview.

8. **Testimonials, Compliance Badges, & Final CTA**:
   - Student reviews, ISO 27001, OWASP ASVS L2, National Student Community CTA.

---

## 4. Verification & Testing Protocol
1. **Static Analysis & Typecheck**:
   - `cd frontend && npx tsc --noEmit` must return 0 errors.
2. **Backend Regression Testing**:
   - Run `python3 -m unittest backend/tests/test_phase98_2_flagship_home_dashboard.py` and `backend/tests/test_phase98_flagship_ui_elevation.py` to confirm zero test breakages.
3. **Strict Zero-Emoji Audit**:
   - Run python zero-emoji regex scanner across `frontend/src/pages/index.tsx`.
4. **Build & Live Verification**:
   - Run `bash scripts/deploy-gh-pages.sh --rebuild` and verify `HTTP 200` on GitHub Pages.
