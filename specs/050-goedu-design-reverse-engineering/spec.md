# Feature Specification: 050 - GoEdu Design Reverse Engineering & Platform Adaptation

## 1. Executive Summary & Objective
Reverse engineer the design language, visual tokens, layout architecture, and user experience of `https://goedu.ac/` (GoEdu - GEAC-accredited online learning platform) and adapt it comprehensively into the "Ogrojatra" (Student Life Circle) platform.

The goal is to infuse Ogrojatra with GoEdu's signature warm, modern, high-trust educational aesthetic (warm linen `#FFFCF6`, sunshine hero `#FFF6DD`, vibrant amber `#ED8E22`, pill navigation, giant watermark typography, tri-card trust matrix, and interactive AI recommendation) while seamlessly integrating Ogrojatra's existing academic capabilities (Socratic AI Tutor, Live Challenge, Admission Predictor, Tuition Marketplace, and Board Archives).

---

## 2. Reverse-Engineered Design System (GoEdu DNA)

### 2.1 Color Tokens
- **Canvas Base (Light)**: `#FFFCF6` (Warm linen sand)
- **Hero Canvas (Light)**: `#FFF6DD` (Sunshine amber-cream) with radial golden sunburst `radial-gradient(ellipse 65% 90% at 50% 100%, rgba(255, 178, 0, 0.75) 0%, rgba(243, 172, 8, 0.4) 45%, rgba(253, 215, 70, 0) 100%)`
- **Canvas Base (Dark)**: `#111827` (Tailwind `gray-900`), Cards: `#1F2937` (`gray-800`), Borders: `#374151` (`gray-700`)
- **Primary Brand Accent**: `#ED8E22` (Warm Amber Orange)
  - Hover: `#D47C1A`
  - Active: `#B86612`
  - Subtle Tint: `#FFFBEB` (`amber-50`)
- **Secondary Accent (Sun Gold)**: `#F3AC08` / `#FBBC05` (Stars, badges, watermark typography)
- **Deep Headings & Slate**: `#213130` (Dark Forest Charcoal) / `#1E293B` (Slate-800)
- **Body & Secondary Text**: `#4B5563` (`gray-600`), Dark Mode: `#D1D5DB` (`gray-300`)
- **Floating Pill Container**: `#E7E7E7` (Light warm gray container for pill navigation)
- **Trust Badge Brand Colors**:
  - Google Reviews: Multi-color logo (`#4285F4`, `#EA4335`, `#FBBC05`, `#34A853`)
  - Trustpilot Verified: `#00B67A` (Emerald green badge, rating stars, and container)
  - Facebook Reviews: `#0066F5` (Facebook vibrant blue, 100% recommended)

### 2.2 Typography & Spacing Language
- **Latin Headings**: `Lexend`, `Lexend Deca` (Geometric, clean, modern)
- **Bengali Headings & Body**: `Noto Sans Bengali`, `Hind Siliguri` (Readable, dignified)
- **Pill Navigation & Badges**: `Work Sans` (Crisp, semi-bold 14px)
- **Metrics & Numbers**: `Inter`, `Geist Sans`
- **Hero Typographic Watermark**: Giant background text `text-[26vw] md:text-[clamp(4rem,30.5vw,30rem)] font-black text-transparent bg-clip-text bg-gradient-to-b from-[#F3AC08] to-transparent pointer-events-none select-none`

### 2.3 Component Radius & Elevation
- **Pills**: `rounded-full` (Nav items, badges, search bar, buttons)
- **Hero Feature Container**: `rounded-[2.5rem]` (40px)
- **Cards (Courses, Mentors, Reviews)**: `rounded-2xl` (16px) with soft border (`border-gray-100 dark:border-gray-800`) and elevated shadow (`shadow-md hover:shadow-xl transition-all duration-300 hover:-translate-y-1`)
- **Search Bar**: `rounded-full bg-white/95 dark:bg-gray-900/95 shadow-md border border-gray-200 dark:border-gray-700`

---

## 3. User Stories

### US-001: Modern GoEdu Floating Pill Navigation
**As a** student or visitor browsing Ogrojatra,  
**I want** a sleek floating pill header that pins smoothly with logo, segmented category navigation, search, cart, and profile/login,  
**So that** I experience a clean, modern, and uncluttered browsing experience identical to GoEdu.

### US-002: Signature Sunshine Hero with Typographic Watermark & AI Recommendation
**As a** learner landing on the homepage,  
**I want** a warm sunshine hero section (`#FFF6DD`) featuring the pulsating badge, bold asymmetric headline, giant watermark branding, and an intelligent pill search bar with a "Let AI Recommend" button,  
**So that** I feel instantly welcomed and can quickly find relevant courses or launch the Socratic AI Tutor.

### US-003: Tri-Card Social Proof & Learner Trust Matrix
**As a** prospective student or guardian,  
**I want** to see verified trust indicators (Google Reviews, Trustpilot 5-Star score, and Facebook 100% recommendation),  
**So that** I have immediate confidence in the platform's credibility and educational outcomes.

### US-004: In-Demand Course & Subject Grid
**As a** student seeking academic and professional mastery,  
**I want** an interactive course grid featuring category tabs (AI & Tech, Higher Math, Physics, Admission & Skills), high-fidelity course cards with level indicators, lesson count, duration, instructor avatar, ratings, and pricing badges,  
**So that** I can explore learning modules with clarity and ease.

### US-005: Featured Accelerator Bundle Spotlight
**As a** motivated learner,  
**I want** a dedicated spotlight card (`rounded-[2.5rem]`) highlighting comprehensive bundles (e.g., HSC STEM Masterclass, University Admission Accelerator, AI Advantage),  
**So that** I can enroll in structured milestone-oriented learning packages.

### US-006: Expert Instructors & Trust Factors
**As a** learner,  
**I want** to see featured instructor profiles with verified credentials, along with a 4-pillar trust section explaining accreditation, lifetime access, and AI guidance,  
**So that** I understand why thousands of Bangladeshi students trust Ogrojatra.

---

## 4. Acceptance Criteria
1. **Design Fidelity**: Visual styling matches GoEdu's layout structure, colors (`#FFFCF6`, `#FFF6DD`, `#ED8E22`), pill navigation, rounded cards, and typography.
2. **Zero-Emoji Compliance**: Absolute zero emojis anywhere in UI, buttons, tabs, or badges. Semantic SVG icons (Lucide) used exclusively.
3. **Responsive Execution**: Fully responsive at 320px, 768px, 1280px, and 1920px. Mobile drawer smoothly mimics GoEdu mobile menu.
4. **Dark Mode Support**: Seamless toggle between GoEdu warm cream (`#FFFCF6`) and slate dark mode (`#111827` / `#1F2937`).
5. **No Business Logic Disruption**: All Ogrojatra features (`/socratic/solver`, `/live-challenge`, `/admission/predictor`, `/tuition`, `/board-archives`) remain linked, functional, and enhanced.
6. **Performance & A11y**: WCAG AA contrast ratio (4.5:1), keyboard focus rings, `aria-label` attributes on icon-only buttons, and zero CLS.
