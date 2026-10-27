# Technical Plan: 050 - GoEdu Design Reverse Engineering & Platform Adaptation

## 1. Technical Architecture Overview
This plan implements the complete GoEdu design system into Ogrojatra (Student Life Circle), establishing a modular component suite in `frontend/src/components/goedu/` that mirrors `https://goedu.ac/` while integrating Ogrojatra's existing features (Socratic AI Tutor, Live Challenge, Admission Predictor, Tuition, Board Archives).

```
frontend/src/
├── components/
│   └── goedu/
│       ├── GoEduNavbar.tsx          # Floating pill header & mobile drawer
│       ├── GoEduHero.tsx            # Sunshine hero with watermark & AI search
│       ├── GoEduTrustProof.tsx      # Tri-card review matrix (Google, Trustpilot, FB)
│       ├── GoEduBundleSpotlight.tsx # 2.5rem ultra-rounded accelerator bundle
│       ├── GoEduCourseGrid.tsx      # Category pills & interactive course cards
│       ├── GoEduInstructors.tsx     # Mentor cards with credentials & ratings
│       ├── GoEduTrustFactors.tsx    # 4-pillar accreditation & trust grid
│       ├── GoEduAIBanner.tsx        # Interactive Socratic AI guidance CTA
│       └── GoEduFooter.tsx          # Comprehensive GoEdu-styled footer
├── data/
│   └── goeduData.ts                 # Real & adapted course data, bundles, instructors
└── pages/
    ├── index.tsx                    # Primary homepage adopting GoEdu design language
    └── courses.tsx                  # Dedicated courses catalog with GoEdu filters
```

---

## 2. Token Architecture & Theme Extensions

### Tailwind & CSS Classes Mapping
| Token | GoEdu Hex | Tailwind Class Mapping | Usage |
| :--- | :--- | :--- | :--- |
| **Canvas Light** | `#FFFCF6` | `bg-[#FFFCF6]` | Global page background |
| **Hero Sunshine** | `#FFF6DD` | `bg-[#FFF6DD]` | Hero background with radial golden glow |
| **Primary Accent** | `#ED8E22` | `bg-[#ED8E22] text-[#ED8E22]` | Primary buttons, active pill tabs, pulsating dots |
| **Primary Hover** | `#D47C1A` | `hover:bg-[#D47C1A]` | Hover state for buttons and links |
| **Sun Gold** | `#F3AC08` | `text-[#F3AC08] from-[#F3AC08]` | Star ratings, watermark text, gradients |
| **Deep Charcoal** | `#213130` | `text-[#213130]` | High-impact headings |
| **Slate Heading** | `#1E293B` | `text-[#1E293B]` | Subheadings, card titles |
| **Pill Container** | `#E7E7E7` | `bg-[#E7E7E7] dark:bg-gray-800` | Floating pill navigation background |
| **Trustpilot Green** | `#00B67A` | `bg-[#00B67A] text-[#00B67A]` | Trustpilot verified badge & stars |
| **Facebook Blue** | `#0066F5` | `text-[#0066F5]` | Facebook reviews badge |

---

## 3. Data Models & Contracts (`goeduData.ts`)

```typescript
export interface GoEduCourse {
  id: number;
  title: string;
  slug: string;
  category: string;
  categorySlug: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  thumbnail: string;
  instructor: {
    name: string;
    role: string;
    photo: string;
    institution: string;
  };
  price: number;
  discountPrice?: number;
  rating: number;
  ratingCount: number;
  totalStudents: number;
  durationMinutes: number;
  totalLessons: number;
  tags: string[];
  routeLink: string;
}

export interface GoEduBundle {
  id: number;
  title: string;
  subtitle: string;
  description: string;
  slug: string;
  tag: string;
  coursesCount: number;
  originalPrice: number;
  bundlePrice: number;
  thumbnail: string;
  highlights: string[];
  routeLink: string;
}

export interface GoEduInstructor {
  id: number;
  name: string;
  title: string;
  institution: string;
  photo: string;
  totalCourses: number;
  totalStudents: number;
  rating: number;
  bio: string;
}
```

---

## 4. Verification & Testing Strategy
1. **Component Testing**: Unit tests for `goeduData.ts` and component render trees.
2. **Type Safety**: Full pass with `tsc --noEmit`.
3. **Production Build**: Verify static export and server rendering with `npm run build`.
4. **Zero-Emoji Audit**: Automated scan guaranteeing 0 emoji unicode codepoints.
5. **Responsive Validation**: Test on mobile (320px), tablet (768px), and desktop (1280px+).
