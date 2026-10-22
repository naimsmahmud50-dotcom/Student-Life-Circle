<!--
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Spec-Driven Development (SDD) Technical Plan
TOPIC:     Flagship Human-Centric Institutional Portal Architecture
FILE:      specs/025-human-flagship-portal/plan.md
PHASE:     Phase 121 / Feature 025 - Flagship Human-Centric Institutional Portal
PURPOSE:   Architectural blueprint for transitioning the platform from an internal
           cockpit mockup to a prestigious, client-ready national educational portal.
STANDARDS: UI/UX Pro Max, Swiss Style Minimalism, Pure Academic Palette, Zero-Emoji
-->

# Technical Architecture Plan: Flagship Human-Centric Institutional Portal

## 1. Architectural Strategy
We resolve the homepage clutter by establishing a clean separation between the **Public Enterprise Portal** and the **Protected Student Dashboard**:

```
                       [User Visits http://localhost:3000]
                                        │
                ┌───────────────────────┴───────────────────────┐
                ▼                                               ▼
    [Public Visitor / Client]                       [Authenticated Student]
                │                                               │
    frontend/src/pages/index.tsx                    frontend/src/pages/dashboard.tsx
    - Mission & Value Proposition                   - Personal Streak (7 Days)
    - 4 Core Academic Pathways                      - Daily Goal Ring (68%)
    - Interactive Feature Showcase                  - Next Recommended Practice
    - Board Archives & STEM Labs                    - Active Quizzes & Tasks
    - National Trust & Payment Rails                - Personal Performance Radar
    - Client / School Partnership CTA
```

## 2. Design System & Visual Hierarchy (`/ui-ux-pro-max`)

| Element | Specification | Rationale |
| :--- | :--- | :--- |
| **Design Pattern** | Feature-Rich Showcase | Proven structure for high credibility and conversion in EdTech. |
| **Visual Style** | Swiss Style & Minimalism | Generous whitespace, calm rhythm, no visual clutter or childish gamification. |
| **Primary Color** | Oxford Academic Navy (`#0A2540`) | Conveys dignity, prestige, and national authority. |
| **Background** | Clean Paper Ivory (`#FAFAF8` / `#FFFFFF`) | Natural paper reading comfort without stark white glare. |
| **Accent Colors** | Scholarly Gold (`#B45309`), Academic Emerald (`#065F46`) | Restrained semantic accents for badges and highlights. |
| **Buttons** | 3D Tactile Physics (`shadow-[0_4px_0_0_#051329]`) | Clear affordance, responsive push feedback on click. |
| **Typography** | Noto Sans Bengali (16px base, 1.6 line height) | Superior readability across mobile, tablet, and desktop. |
| **Icons** | Pure Lucide Vector SVG Icons | Strict zero-emoji compliance across all components. |

## 3. Structural Sections of `frontend/src/pages/index.tsx`

1. **Global Academic Header (`Navbar`)**:
   - Logo with Oxford Navy badge, Bengali title "অগ্রযাত্রা", and crisp navigation links.
   - Client-accessible links: "পাঠ্যক্রম", "বোর্ড প্রশ্ন ব্যাংক", "প্র্যাকটিস", "ভর্তি পরীক্ষা", "টিউশন", "ক্যারিয়ার".
   - Primary action: "ড্যাশবোর্ড প্রবেশ" pointing to `/dashboard`.

2. **Flagship Academic Hero**:
   - Dignified badge: "জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) মানদণ্ডে পরিচালিত".
   - Authoritative Headline: "বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বিক ডিজিটাল শিক্ষাজীবন".
   - Subtitle: "মাধ্যমিক ও উচ্চ মাধ্যমিক থেকে বিশ্ববিদ্যালয় ভর্তি এবং পেশাগত ক্যারিয়ার—সব বিষয়ের অধ্যায়ভিত্তিক শিখন, বিগত ১০ বছরের বোর্ড প্রশ্ন এবং ৩ডি ভার্চুয়াল বিজ্ঞান ল্যাব।"
   - Dual Call-to-Action Buttons:
     * Primary: "বিনামূল্যে পড়াশোনা শুরু করুন" (Oxford Navy 3D button).
     * Secondary: "বোর্ড প্রশ্ন ব্যাংক দেখুন" (Crisp paper outline with chevron).
   - Clean Platform Feature Radar: An interactive preview card demonstrating the platform's multi-stage curriculum and real-time national scale.

3. **National Scale & Trust Strip**:
   - 4 Verifiable National Metrics:
     * ১০ বছরের আসল বোর্ড প্রশ্ন (২০১৫–২০২৫)
     * ১০০% জাতীয় শিক্ষাক্রম (NCTB) মানদণ্ড
     * ৬৪ জেলার শিক্ষার্থীদের জন্য অফলাইন ও অনলাইন সুবিধা
     * ০% ভিডিও নজরদারি • সর্বোচ্চ শিক্ষার্থী ডেটা গোপনীয়তা

4. **The 4 Core Educational Pathways**:
   - Card 1: **মাধ্যমিক স্তর (SSC ৯-১০)**: সাধারণ গণিত, উচ্চতর গণিত, পদার্থ ও রসায়ন।
   - Card 2: **উচ্চ মাধ্যমিক (HSC ১১-১২)**: পদার্থবিজ্ঞান, রসায়ন, জীববিজ্ঞান ও গণিত।
   - Card 3: **বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি (Admission)**: বুয়েট, ঢাকা বিশ্ববিদ্যালয় ও মেডিকেল মক টেস্ট।
   - Card 4: **পেশাগত ক্যারিয়ার ও টিউশন (Career & Tuition)**: দ্বিপাক্ষিক এসক্রো এবং যাচাইকৃত স্কিল রেকর্ড।

5. **Interactive Flagship Capabilities Showcase**:
   - Tabbed or Bento showcase highlighting:
     * **অফিসিয়াল এনসিটিবি বোর্ড প্রশ্ন ব্যাংক**: বিগত ১০ বছরের প্রশ্ন ও KaTeX সমীকরণ ভিউয়ার।
     * **৩ডি স্টেম ভার্চুয়াল বিজ্ঞান ল্যাব**: প্রক্ষেপক গতি ও আণবিক জ্যামিতি সরাসরি ব্রাউজারে সিমুলেশন।
     * **ডিজিটাল এক্সাম হল ও শান্ত প্রক্টরিং**: পরীক্ষাভীতি দূর করতে শান্ত, গোপনীয়তা-সুরক্ষিত পরিবেশ।
     * **সক্রেটিক এআই টিউটর**: সরাসরি উত্তর নয়, চিন্তার বিকাশ ও ধারণাগত পথপ্রদর্শন।
     * **জাতীয় মেধা বৃত্তি ও স্বচ্ছ এসক্রো**: আর্থিক অস্বচ্ছতা দূর করে স্বয়ংক্রিয় মেধা অনুদান।

6. **Institutional Accreditation & Payment Rails**:
   - bKash Verified Merchant, Nagad Verified Merchant, SSLCommerz PCI-DSS gateway.
   - W3C Cryptographic Proof-of-Skill verification.

7. **Closing High-Impact Call to Action & Footer**:
   - Clear, dignified invitation for students, parents, and institutions to get started.
   - Comprehensive institutional footer with compliance links, hotline, and contact info.

## 4. Implementation Steps
1. Create `frontend/src/pages/dashboard.tsx` to preserve all personal student dashboard capabilities.
2. Re-architect `frontend/src/pages/index.tsx` with the new Flagship Public Portal structure.
3. Verify Next.js build compilation (`npx next build`).
4. Execute zero-emoji sweep (`run_zero_emoji_sweep.py`).
5. Verify live server response at `http://localhost:3000`.
