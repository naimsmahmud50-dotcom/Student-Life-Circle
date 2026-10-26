# Plan: CareTutors-Inspired Tuition Marketplace Technical Architecture

## 1. Architecture & Component Hierarchy

To maintain complete **Scope Lock** and maintain codebase hygiene, all newly elevated tuition modules will be created under:
`frontend/src/components/tuition/`

```text
frontend/src/components/tuition/
├── data/
│   └── tuitionElevationData.ts        # Typed datasets for jobs, tutors, salary rules & FAQs
├── TutorRequestWizardModal.tsx        # 4-step wizard modal for guardians
├── TuitionJobBoard.tsx                # Filterable live tuition job board with apply modal
├── VerifiedTutorDirectory.tsx         # Directory of verified tutors with consent unlock
├── TuitionSalaryCalculator.tsx        # Interactive salary calculator
├── TuitionTrustAndSafetySection.tsx   # 4-Pillar trust, 2-day trial & escrow explanation
├── TuitionCategoryPills.tsx           # Category navigation pills
├── TuitionStatsHeader.tsx             # Live stats bar (Tutors, Jobs, Rating, Zero Scam)
└── __tests__/
    └── tuitionElevation.test.mjs      # Unit test suite verifying logic & sanitization
```

Master integration point:
- `frontend/src/pages/tuition.tsx`: Hosts the elevated experience via structured tabs, maintaining backward compatibility with `apiClient.getTuitionListings` and bilateral consent handling.

---

## 2. Technical Contracts & Data Schemas

### 2.1 Tuition Job Schema
```typescript
export interface TuitionJob {
  id: string; // e.g. "TUI-9104"
  titleBn: string;
  category: 'bangla_medium' | 'english_version' | 'english_medium' | 'religious' | 'admission' | 'arts_lang' | 'special_child';
  classGradeBn: string; // e.g. "১০ম শ্রেণি (এসএসসি ২৭)"
  subjectsBn: string[]; // e.g. ["পদার্থবিজ্ঞান", "রসায়ন", "উচ্চতর গণিত"]
  mode: 'হোম টিউশন' | 'অনলাইন টিউশন' | 'গ্রুপ ব্যাচ';
  district: string; // e.g. "ঢাকা"
  thana: string; // e.g. "ধানমন্ডি"
  addressDetailsBn: string; // e.g. "ধানমন্ডি ২৭, রোড ৮/এ"
  daysPerWeek: number; // e.g. 3
  salaryBn: string; // e.g. "৮,০০০ - ১০,০০০ টাকা/মাস"
  salaryAmount: number;
  genderPreferenceBn: 'পুরুষ টিউটর আবশ্যক' | 'মহিলা টিউটর আবশ্যক' | 'যেকোনো';
  tutorRequirementBn: string; // e.g. "বুয়েট বা ঢাকা বিশ্ববিদ্যালয়ের বিজ্ঞান বিভাগের অভিজ্ঞ টিউটর অগ্রাধিকার"
  postedDateBn: string;
  applicantsCount: number;
  status: 'open' | 'shortlisting' | 'confirmed';
}
```

### 2.2 Verified Tutor Schema
```typescript
export interface VerifiedTutor {
  id: string; // e.g. "TUT-408"
  nameBn: string;
  initialsBn: string;
  accentBg: string;
  institutionBn: string; // e.g. "বুয়েট"
  departmentBn: string; // e.g. "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)"
  degreeLevelBn: string; // e.g. "স্নাতক (৩য় বর্ষ)"
  sscBackgroundBn: string; // e.g. "নটর ডেম কলেজ (জিপিএ ৫.০০)"
  preferredCategories: string[];
  preferredSubjects: string[];
  preferredLocations: string[];
  experienceYearsBn: string; // e.g. "৩+ বছর"
  rating: number; // e.g. 4.9
  totalReviews: number;
  tuitionsCompleted: number;
  expectedSalaryBn: string; // e.g. "৮,০০০ - ১২,০০০ টাকা/মাস"
  verificationStatus: {
    nidVerified: boolean;
    academicIdVerified: boolean;
    backgroundChecked: boolean;
  };
}
```

---

## 3. Security, Input Sanitization & Strix Audit Rules

1. **XSS Protection:** All user inputs from the Guardian Request Wizard (phone, address, instructions) are strictly escaped and sanitized via React JSX. No raw HTML injection.
2. **Phone Number Privacy:** Phone numbers on the job board and tutor profiles are masked (`০১৭*** (দ্বিপাক্ষিক লক)`). Direct contacts are only unlocked upon bilateral consent confirmation.
3. **Zero Advance Scam Architecture:** The UI clearly enforces that no advance commission or security deposit is required prior to tutor appointment and completion of 2-day free trial classes.
4. **Zero Unicode Emojis:** Strict adherence to project rules. All iconography uses `lucide-react`.
5. **WCAG 2.2 AAA Contrast & Keyboard Access:** Full tab order, aria dialog attributes, ESC key closure, and high-contrast labels.
