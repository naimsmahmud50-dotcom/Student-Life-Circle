/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Bdjobs-Class Career & Employment Ecosystem Dataset
 * STANDARDS: UI/UX Pro Max, Pure Academic & Corporate Palette, Zero-Emoji, WCAG 2.2 AAA
 * ISOLATION: 100% Brand-Safe. Zero Bdjobs trademarks or scraped proprietary images.
 * PURPOSE:   Provides authentic Bangladeshi employment, government circulars,
 *            divisional taxonomy, and ATS tracking structures.
 */

export interface CareerCategory {
  id: string;
  nameBn: string;
  nameEn: string;
  jobCount: number;
  type: 'functional' | 'special_skill';
  iconName: string;
  description: string;
}

export interface CareerDivision {
  id: string;
  nameBn: string;
  nameEn: string;
  districts: string[];
}

export interface CareerJob {
  id: string;
  title: string;
  companyName: string;
  companyMonogram: string; // 2-letter corporate monogram
  monogramBg: string;      // Tailwind bg class
  monogramText: string;    // Tailwind text class
  companyIndustry: string;
  category: string;
  orgType: 'GOVT' | 'PRIVATE' | 'NGO' | 'MULTINATIONAL' | 'SEMI_GOVT';
  jobNature: 'FULL_TIME' | 'PART_TIME' | 'CONTRACTUAL' | 'INTERNSHIP' | 'FREELANCE';
  jobLevel: 'ENTRY' | 'MID' | 'SENIOR';
  vacancy: number;
  locationDistrict: string;
  locationDivision: string;
  minSalary: number;
  maxSalary: number;
  isSalaryNegotiable: boolean;
  deadline: string;        // Bengali readable date
  deadlineIso: string;     // ISO timestamp for urgency calculation
  publishedDate: string;
  experienceYears: string;
  educationRequirements: string[];
  responsibilities: string[];
  benefits: string[];
  isHotJob: boolean;
  isEarlyAccess: boolean;
  applicantsCount: number;
}

export interface GovtCircular {
  id: string;
  title: string;
  ministryOrDepartment: string;
  totalPosts: number;
  applicationDeadline: string;
  circularDate: string;
  gradePayScale: string;
  officialRef: string;
}

export interface SalaryBenchmark {
  industry: string;
  roleTitle: string;
  entryLevelSalary: string;
  midLevelSalary: string;
  seniorLevelSalary: string;
}

export interface CareerFaq {
  question: string;
  answer: string;
}

// ---------------------------------------------------------------------------
// 1. Functional & Special Skills Categories (Mirroring Bdjobs Taxonomy)
// ---------------------------------------------------------------------------
export const CAREER_CATEGORIES: CareerCategory[] = [
  {
    id: "cat_it",
    nameBn: "আইটি ও সফটওয়্যার",
    nameEn: "IT & Telecommunication",
    jobCount: 1420,
    type: "functional",
    iconName: "Code",
    description: "ফুলস্ট্যাক, পাইথন, ফ্রন্টএন্ড, ক্লাউড আর্কিটেকচার ও ডেভঅপস"
  },
  {
    id: "cat_bank",
    nameBn: "ব্যাংক ও নন-ব্যাংক ফিন্যান্স",
    nameEn: "Bank & Non-Bank Fin",
    jobCount: 890,
    type: "functional",
    iconName: "Building2",
    description: "ম্যানেজমেন্ট ট্রেইনি, ক্রেডিট অ্যানালিস্ট ও জেনারেল ব্যাংকিং"
  },
  {
    id: "cat_engineering",
    nameBn: "ইঞ্জিনিয়ারিং ও আর্কিটেকচার",
    nameEn: "Engineer & Architect",
    jobCount: 760,
    type: "functional",
    iconName: "Compass",
    description: "সিভিল, ইলেকট্রিক্যাল, মেকানিক্যাল ও ইন্ডাস্ট্রিয়াল প্রোডাকশন"
  },
  {
    id: "cat_marketing",
    nameBn: "মার্কেটিং ও সেলস",
    nameEn: "Marketing & Sales",
    jobCount: 1150,
    type: "functional",
    iconName: "TrendingUp",
    description: "ব্র্যান্ডিং, ডিজিটাল গ্রোথ, বিজনেস ডেভেলপমেন্ট ও রিটেল"
  },
  {
    id: "cat_govt",
    nameBn: "সরকারি ও ক্যাডার সার্ভিস",
    nameEn: "Government & Cadre",
    jobCount: 520,
    type: "functional",
    iconName: "Award",
    description: "বিপিএসসি, স্বায়ত্তশাসিত প্রতিষ্ঠান ও মন্ত্রণালয়ের নিয়োগ বিজ্ঞপ্তি"
  },
  {
    id: "cat_ngo",
    nameBn: "এনজিও ও উন্নয়ন সংস্থা",
    nameEn: "NGO & Development",
    jobCount: 640,
    type: "functional",
    iconName: "Users",
    description: "ফিল্ড অপারেশন, প্রোগ্রাম মনিটরিং ও রিসার্চ কো-অর্ডিনেটর"
  },
  {
    id: "cat_pharma",
    nameBn: "মেডিকেল ও ফার্মাসিউটিক্যাল",
    nameEn: "Medical & Pharma",
    jobCount: 580,
    type: "functional",
    iconName: "Activity",
    description: "মেডিকেল প্রমোশন, কিউএ কেমিস্ট ও ক্লিনিক্যাল রিসার্চ"
  },
  {
    id: "cat_education",
    nameBn: "শিক্ষা ও প্রশিক্ষণ",
    nameEn: "Education & Training",
    jobCount: 490,
    type: "functional",
    iconName: "BookOpen",
    description: "বিশ্ববিদ্যালয় প্রভাষক, কলেজ শিক্ষক ও কর্পোরেট ট্রেইনার"
  },
  {
    id: "cat_skill_elec",
    nameBn: "ইলেকট্রিশিয়ান ও টেকনিশিয়ান",
    nameEn: "Electrician & Technician",
    jobCount: 410,
    type: "special_skill",
    iconName: "Zap",
    description: "ইন্ডাস্ট্রিয়াল ওয়্যারিং, এইচভিএসি মেইনটেন্যান্স ও পাওয়ার কন্ট্রোল"
  },
  {
    id: "cat_skill_garments",
    nameBn: "গার্মেন্টস ও টেক্সটাইল টেকনিশিয়ান",
    nameEn: "Garments & Textile",
    jobCount: 680,
    type: "special_skill",
    iconName: "Scissors",
    description: "প্যাটার্ন মেকিং, কোয়ালিটি অডিটর ও মার্চেন্ডাইজিং অ্যাসিস্ট্যান্ট"
  },
  {
    id: "cat_skill_driver",
    nameBn: "ড্রাইভার ও লজিস্টিকস রাইডার",
    nameEn: "Driver & Logistics",
    jobCount: 530,
    type: "special_skill",
    iconName: "Truck",
    description: "হেভি/লাইট লাইসেন্সধারী ড্রাইভার ও এক্সপ্রেস ডেলিভারি রাইডার"
  },
  {
    id: "cat_skill_chef",
    nameBn: "শেফ ও ক্যাটারিং সার্ভিস",
    nameEn: "Chef & Hospitality",
    jobCount: 380,
    type: "special_skill",
    iconName: "Utensils",
    description: "হোটেল রন্ধনশিল্পী, বেকারি স্পেশালিস্ট ও ফুড সেফটি সুপারভাইজার"
  }
];

// ---------------------------------------------------------------------------
// 2. Bangladesh Divisions & Key Districts
// ---------------------------------------------------------------------------
export const BANGLADESH_DIVISIONS: CareerDivision[] = [
  {
    id: "all",
    nameBn: "সমগ্র বাংলাদেশ",
    nameEn: "All Bangladesh",
    districts: ["ঢাকা", "চট্টগ্রাম", "রাজশাহী", "খুলনা", "বরিশাল", "সিলেট", "রংপুর", "ময়মনসিংহ", "রিমোট / বাসা থেকে"]
  },
  {
    id: "dhaka",
    nameBn: "ঢাকা বিভাগ",
    nameEn: "Dhaka Division",
    districts: ["ঢাকা মহানগর", "গাজীপুর", "নারায়ণগঞ্জ", "সাভার", "টাঙ্গাইল", "নরসিংদী"]
  },
  {
    id: "chattogram",
    nameBn: "চট্টগ্রাম বিভাগ",
    nameEn: "Chattogram Division",
    districts: ["চট্টগ্রাম মহানগর", "কক্সবাজার", "কুমিল্লা", "ফেনী", "নোয়াখালী", "ব্রাহ্মণবাড়িয়া"]
  },
  {
    id: "rajshahi",
    nameBn: "রাজশাহী বিভাগ",
    nameEn: "Rajshahi Division",
    districts: ["রাজশাহী", "বগুড়া", "পাবনা", "সিরাজগঞ্জ", "নওগাঁ"]
  },
  {
    id: "khulna",
    nameBn: "খুলনা বিভাগ",
    nameEn: "Khulna Division",
    districts: ["খুলনা", "যশোর", "কুষ্টিয়া", "সাতক্ষীরা", "ঝিনাইদহ"]
  },
  {
    id: "sylhet",
    nameBn: "সিলেট বিভাগ",
    nameEn: "Sylhet Division",
    districts: ["সিলেট", "মৌলভীবাজার", "হবিগঞ্জ", "সুনামগঞ্জ"]
  },
  {
    id: "barishal",
    nameBn: "বরিশাল বিভাগ",
    nameEn: "Barishal Division",
    districts: ["বরিশাল", "পটুয়াখালী", "ভোলা", "পিরোজপুর"]
  },
  {
    id: "rangpur",
    nameBn: "রংপুর বিভাগ",
    nameEn: "Rangpur Division",
    districts: ["রংপুর", "দিনাজপুর", "কুড়িগ্রাম", "গাইবান্ধা"]
  },
  {
    id: "mymensingh",
    nameBn: "ময়মনসিংহ বিভাগ",
    nameEn: "Mymensingh Division",
    districts: ["ময়মনসিংহ", "জামালপুর", "নেত্রকোণা", "শেরপুর"]
  }
];

// ---------------------------------------------------------------------------
// 3. Realistic Verified Job Listings (Master-Class Bdjobs Depth)
// ---------------------------------------------------------------------------
export const VERIFIED_CAREER_JOBS: CareerJob[] = [
  {
    id: "JOB-BD-2026-001",
    title: "জুনিয়র সফটওয়্যার ইঞ্জিনিয়ার (Python / FastAPI)",
    companyName: "ব্রেনস্টেশন ২৩ (BrainStation 23)",
    companyMonogram: "BS",
    monogramBg: "bg-blue-900",
    monogramText: "text-blue-100",
    companyIndustry: "Software & Technology",
    category: "cat_it",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 4,
    locationDistrict: "ঢাকা মহানগর",
    locationDivision: "dhaka",
    minSalary: 35000,
    maxSalary: 55000,
    isSalaryNegotiable: false,
    deadline: "৩০ নভেম্বর ২০২৬",
    deadlineIso: "2026-11-30T23:59:59Z",
    publishedDate: "২০ অক্টোবর ২০২৬",
    experienceYears: "০ - ১ বছর (ফ্রেশার স্বাগতম)",
    educationRequirements: [
      "কম্পিউটার সায়েন্স ও ইঞ্জিনিয়ারিং (CSE) অথবা সমমানের বিষয়ে স্নাতক/বিএসসি ডিগ্রি।",
      "ন্যূনতম সিজিপিএ ৩.০০ (৪.০০ এর স্কেলে)।"
    ],
    responsibilities: [
      "উচ্চ কর্মক্ষমতাসম্পন্ন রেস্টফুল এপিআই ডিজাইন ও ফাস্টএপিআই দিয়ে বাস্তবায়ন।",
      "পোস্টগ্রেসকিউএল ডাটাবেজ অপ্টিমাইজেশন ও জটিল কোয়েরি প্রোফাইলিং।",
      "ডকারাইজেশন ও সিআই/সিডি অটোমেশন পাইপলাইনে সক্রিয় অবদান রাখা।",
      "টিম মেম্বারদের কোড রিভিউ ও টেস্ট-ড্রিভেন ডেভেলপমেন্ট চর্চা বজায় রাখা।"
    ],
    benefits: [
      "বছরে ২টি উৎসব বোনাস (মূল বেতনের সমপরিমাণ)।",
      "প্রভিডেন্ট ফান্ড ও গ্র্যাচুইটি পলিসি সুবিধা।",
      "অফিসিয়াল লাঞ্চ ও স্ন্যাকস কমপ্লিমেন্টারি।",
      "বার্ষিক পারফরম্যান্স ও স্কিল ইনক্রিমেন্ট।"
    ],
    isHotJob: true,
    isEarlyAccess: true,
    applicantsCount: 142
  },
  {
    id: "JOB-BD-2026-002",
    title: "ম্যানেজমেন্ট ট্রেইনি অফিসার (MTO - 2026)",
    companyName: "ইস্টার্ন ব্যাংক লিমিটেড (EBL)",
    companyMonogram: "EB",
    monogramBg: "bg-emerald-900",
    monogramText: "text-emerald-100",
    companyIndustry: "Banking & Financial Institutions",
    category: "cat_bank",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 15,
    locationDistrict: "ঢাকা মহানগর",
    locationDivision: "dhaka",
    minSalary: 65000,
    maxSalary: 75000,
    isSalaryNegotiable: false,
    deadline: "১৫ নভেম্বর ২০২৬",
    deadlineIso: "2026-11-15T23:59:59Z",
    publishedDate: "১৮ অক্টোবর ২০২৬",
    experienceYears: "অভিজ্ঞতার প্রয়োজন নেই (নতুন স্নাতকদের জন্য)",
    educationRequirements: [
      "যেকোনো স্বীকৃত বিশ্ববিদ্যালয় থেকে ফিন্যান্স, ব্যাংকিং, ইকোনমিক্স বা ব্যবসায় প্রশাসনে বিবিএ/এমবিএ।",
      "এসএসসি ও এইচএসসিতে ন্যূনতম জিপিএ ৪.৫০ এবং স্নাতক পর্যায়ে ৩.২০।"
    ],
    responsibilities: [
      "শাখা ব্যাংকিং, ক্রেডিট অ্যানালাইসিস ও ট্রেড সার্ভিসের বিভিন্ন ডেস্ক পরিচালনা।",
      "রিটেইল ও করপোরেট ক্লায়েন্টদের ফাইন্যান্সিয়াল পোর্টফোলিও মূল্যায়ন।",
      "১ বছর সফল প্রশিক্ষণ শেষে সিনিয়র প্রিন্সিপাল অফিসার ধাপে স্থায়ীকরণ।"
    ],
    benefits: [
      "প্রবেশনারি মেয়াদে মাসিক আকর্ষণীয় প্রশিক্ষণ ভাতা।",
      "গ্রুপ হেলথ ও লাইফ ইন্স্যুরেন্স প্যাকেজ।",
      "বাৎসরিক ব্যাংকিং প্রফিট শেয়ারিং বোনাস।"
    ],
    isHotJob: true,
    isEarlyAccess: false,
    applicantsCount: 389
  },
  {
    id: "JOB-BD-2026-003",
    title: "অ্যাসিস্ট্যান্ট ডিরেক্টর (জেনারেল) - সার্কুলার ২০২৬",
    companyName: "বাংলাদেশ ব্যাংক (কেন্দ্রীয় ব্যাংক)",
    companyMonogram: "BB",
    monogramBg: "bg-amber-900",
    monogramText: "text-amber-100",
    companyIndustry: "Central Banking & Regulatory",
    category: "cat_govt",
    orgType: "GOVT",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 100,
    locationDistrict: "ঢাকা মহানগর",
    locationDivision: "dhaka",
    minSalary: 42000,
    maxSalary: 53060,
    isSalaryNegotiable: false,
    deadline: "০৫ ডিসেম্বর ২০২৬",
    deadlineIso: "2026-12-05T23:59:59Z",
    publishedDate: "২৫ অক্টোবর ২০২৬",
    experienceYears: "অভিজ্ঞতা বাধ্যতামূলক নয়",
    educationRequirements: [
      "যেকোনো বিষয়ে ৪ বছর মেয়াদী স্নাতক/স্নাতকোত্তর ডিগ্রি (ন্যূনতম ২য় শ্রেণি বা সমমান)।",
      "শিক্ষা জীবনে কোনো তৃতীয় বিভাগ গ্রহণযোগ্য নয়।"
    ],
    responsibilities: [
      "মুদ্রানীতি প্রণয়ন, বৈদেশিক মুদ্রার রিজার্ভ পর্যবেক্ষণ ও ব্যাংক নিয়ন্ত্রণ।",
      "ব্যাংকিং পরিদর্শন ও পরিদর্শন প্রতিবেদনের ভিত্তিতে সুপারভাইজরি একশন গ্রহণ।"
    ],
    benefits: [
      "জাতীয় বেতন স্কেল ২০১৫ অনুযায়ী ৯ম গ্রেডের পূর্ণ সুবিধাদি।",
      "সরকারি আবাসন ও সুদমুক্ত হোম লোন স্কিম।",
      "উচ্চশিক্ষার জন্য বৈদেশিক স্কলারশিপ প্রোগ্রাম।"
    ],
    isHotJob: false,
    isEarlyAccess: false,
    applicantsCount: 12500
  },
  {
    id: "JOB-BD-2026-004",
    title: "প্রোগ্রাম অফিসার (কমিউনিটি এডুকেশন)",
    companyName: "ব্র্যাক (BRAC International)",
    companyMonogram: "BR",
    monogramBg: "bg-pink-900",
    monogramText: "text-pink-100",
    companyIndustry: "Non-Government Organization",
    category: "cat_ngo",
    orgType: "NGO",
    jobNature: "FULL_TIME",
    jobLevel: "MID",
    vacancy: 6,
    locationDistrict: "বগুড়া",
    locationDivision: "rajshahi",
    minSalary: 40000,
    maxSalary: 48000,
    isSalaryNegotiable: true,
    deadline: "২৫ নভেম্বর ২০২৬",
    deadlineIso: "2026-11-25T23:59:59Z",
    publishedDate: "২২ অক্টোবর ২০২৬",
    experienceYears: "১ - ৩ বছর",
    educationRequirements: [
      "সমাজবিজ্ঞান, সমাজকল্যাণ, বা শিক্ষা বিষয়ে স্নাতক/মাস্টার্স।"
    ],
    responsibilities: [
      "তৃণমূল পর্যায়ে প্রাথমিক ও উপানুষ্ঠানিক শিক্ষা প্রকল্প বাস্তবায়ন।",
      "স্থানীয় অভিভাবক ও শিক্ষকদের সাথে সমন্বয় সভা পরিচালনা এবং ডেটা এন্ট্রি।"
    ],
    benefits: [
      "মোবাইল ও যাতায়াত ভাতা।",
      "বার্ষিক স্বাস্থ্য বীমা ও প্রভিডেন্ট ফান্ড।"
    ],
    isHotJob: false,
    isEarlyAccess: true,
    applicantsCount: 94
  },
  {
    id: "JOB-BD-2026-005",
    title: "কোয়ালিটি কন্ট্রোল কেমিস্ট (QC Chemist)",
    companyName: "স্কয়ার ফার্মাসিউটিক্যালস পিএলসি",
    companyMonogram: "SQ",
    monogramBg: "bg-slate-900",
    monogramText: "text-slate-100",
    companyIndustry: "Pharmaceutical & Healthcare",
    category: "cat_pharma",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 5,
    locationDistrict: "পাবনা",
    locationDivision: "rajshahi",
    minSalary: 38000,
    maxSalary: 45000,
    isSalaryNegotiable: false,
    deadline: "২০ নভেম্বর ২০২৬",
    deadlineIso: "2026-11-20T23:59:59Z",
    publishedDate: "১৯ অক্টোবর ২০২৬",
    experienceYears: "০ - ২ বছর",
    educationRequirements: [
      "রসায়ন / ফলিত রসায়নে বিএসসি বা এমএসসি।"
    ],
    responsibilities: [
      "এইচপিএলসি এবং ইউভি স্পেকট্রোফোটোমেট্রি দ্বারা ড্রাগ স্যাম্পল পরীক্ষা।",
      "জিএমপি ও স্ট্যান্ডার্ড অপারেটিং প্রসিডিউর (SOP) শতভাগ বজায় রাখা।"
    ],
    benefits: [
      "কোম্পানির নিজস্ব ট্রান্সপোর্ট ও ক্যাফেটেরিয়া সুবিধা।",
      "বছরে ৩টি বোনাস (২টি উৎসব + ১টি প্রফিট বোনাস)।"
    ],
    isHotJob: true,
    isEarlyAccess: false,
    applicantsCount: 167
  },
  {
    id: "JOB-BD-2026-006",
    title: "ইন্টার্ন - ফ্রন্টএন্ড ডেভেলপার (Next.js / React)",
    companyName: "চালডাল লিমিটেড (Chaldal)",
    companyMonogram: "CD",
    monogramBg: "bg-orange-900",
    monogramText: "text-orange-100",
    companyIndustry: "E-Commerce & Tech",
    category: "cat_it",
    orgType: "PRIVATE",
    jobNature: "INTERNSHIP",
    jobLevel: "ENTRY",
    vacancy: 3,
    locationDistrict: "রিমোট / বাসা থেকে",
    locationDivision: "dhaka",
    minSalary: 18000,
    maxSalary: 25000,
    isSalaryNegotiable: false,
    deadline: "১০ নভেম্বর ২০২৬",
    deadlineIso: "2026-11-10T23:59:59Z",
    publishedDate: "২১ অক্টোবর ২০২৬",
    experienceYears: "ফ্রেশার বা ফাইনাল ইয়ার শিক্ষার্থী",
    educationRequirements: [
      "সিএসই বা রিলেটেড বিষয়ের আন্ডারগ্র্যাজুয়েট শিক্ষার্থী বা সদ্য পাসকৃত।"
    ],
    responsibilities: [
      "টেইলউইন্ড সিএসএস ও টাইপস্ক্রিপ্ট দিয়ে আধুনিক রেসপনসিভ ইউআই তৈরি।",
      "কম্পোনেন্ট লেভেল অপ্টিমাইজেশন ও পারফরম্যান্স মেট্রিক নিরীক্ষা।"
    ],
    benefits: [
      "সফল ইন্টার্নশিপ শেষে ফুল-টাইম নিয়োগের সুযোগ।",
      "আন্তর্জাতিক মেন্টরদের সরাসরি দিকনির্দেশনা।"
    ],
    isHotJob: true,
    isEarlyAccess: true,
    applicantsCount: 218
  },
  {
    id: "JOB-BD-2026-007",
    title: "ইন্ডাস্ট্রিয়াল সিনিয়র ইলেকট্রিশিয়ান",
    companyName: "ওয়ালটন হাই-টেক ইন্ডাস্ট্রিজ পিএলসি",
    companyMonogram: "WL",
    monogramBg: "bg-indigo-900",
    monogramText: "text-indigo-100",
    companyIndustry: "Electronics Manufacturing",
    category: "cat_skill_elec",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "MID",
    vacancy: 8,
    locationDistrict: "গাজীপুর",
    locationDivision: "dhaka",
    minSalary: 28000,
    maxSalary: 36000,
    isSalaryNegotiable: true,
    deadline: "২৮ নভেম্বর ২০২৬",
    deadlineIso: "2026-11-28T23:59:59Z",
    publishedDate: "১৭ অক্টোবর ২০২৬",
    experienceYears: "২ - ৪ বছর",
    educationRequirements: [
      "বাংলাদেশ কারিগরি শিক্ষা বোর্ডের ডিপ্লোমা ইন ইলেকট্রিক্যাল বা ভোকেশনাল সার্টিফিকেট।"
    ],
    responsibilities: [
      "উৎপাদন লাইনের ট্রান্সফর্মার, প্যানেল বোর্ড ও পিএলসি মোটর মেরামত।",
      "প্রিভেন্টিভ মেইনটেন্যান্স চেকশিট অনুযায়ী নিয়মিত যন্ত্রাংশ টেস্ট করা।"
    ],
    benefits: [
      "কোম্পানি ডরমিটরি ও সাবসিডিযুক্ত খাবার।",
      "ওভারটাইম ভাতা ও বার্ষিক ইনক্রিমেন্ট।"
    ],
    isHotJob: false,
    isEarlyAccess: false,
    applicantsCount: 62
  },
  {
    id: "JOB-BD-2026-008",
    title: "অ্যাসিস্ট্যান্ট ইঞ্জিনিয়ার (সিভিল)",
    companyName: "মেঘনা গ্রুপ অব ইন্ডাস্ট্রিজ (MGI)",
    companyMonogram: "MG",
    monogramBg: "bg-teal-900",
    monogramText: "text-teal-100",
    companyIndustry: "Conglomerate & Heavy Industry",
    category: "cat_engineering",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 4,
    locationDistrict: "নারায়ণগঞ্জ",
    locationDivision: "dhaka",
    minSalary: 38000,
    maxSalary: 45000,
    isSalaryNegotiable: false,
    deadline: "২২ নভেম্বর ২০২৬",
    deadlineIso: "2026-11-22T23:59:59Z",
    publishedDate: "১৬ অক্টোবর ২০২৬",
    experienceYears: "১ - ২ বছর",
    educationRequirements: [
      "বিএসসি ইন সিভিল ইঞ্জিনিয়ারিং (বুয়েট/কুয়েট/রুয়েট/চুয়েট অগ্রাধিকার)।"
    ],
    responsibilities: [
      "ইন্ডাস্ট্রিয়াল প্ল্যান্ট ও ওয়্যারহাউস নির্মাণ কাজের সরাসরি সাইট তদারকি।",
      "অটোক্যাড ড্রয়িং যাচাই ও ম্যাটেরিয়াল কোয়ালিটি টেস্টিং নিশ্চিতকরণ।"
    ],
    benefits: [
      "সাইট ট্রাভেল অ্যালাউন্স ও স্বাস্থ্য সুরক্ষা সরঞ্জাম।",
      "বার্ষিক বোনাস ও প্রভিডেন্ট ফান্ড।"
    ],
    isHotJob: false,
    isEarlyAccess: true,
    applicantsCount: 81
  }
];

// ---------------------------------------------------------------------------
// 4. Official Bangladesh Government Circular Archives (বিসিএস ও সরকারি চাকরি)
// ---------------------------------------------------------------------------
export const GOVT_CIRCULAR_ARCHIVES: GovtCircular[] = [
  {
    id: "GOVT-PSC-48",
    title: "৪৮তম বিসিএস (বিশেষ) পরীক্ষা সার্কুলার ২০২৬",
    ministryOrDepartment: "বাংলাদেশ সরকারি কর্ম কমিশন (BPSC)",
    totalPosts: 3120,
    applicationDeadline: "১৫ ডিসেম্বর ২০২৬",
    circularDate: "০১ অক্টোবর ২০২৬",
    gradePayScale: "জাতীয় বেতন স্কেল ২০১৫, ৯ম গ্রেড (২২,০০০ - ৫৩,০৬০ টাকা)",
    officialRef: "bpsc.gov.bd/circular/48-special"
  },
  {
    id: "GOVT-BB-AD-26",
    title: "সহকারী পরিচালক (রিসার্চ ও জেনারেল) সার্কুলার",
    ministryOrDepartment: "বাংলাদেশ ব্যাংক ব্যাংকার্স সিলেকশন কমিটি",
    totalPosts: 125,
    applicationDeadline: "১০ ডিসেম্বর ২০২৬",
    circularDate: "০৫ অক্টোবর ২০২৬",
    gradePayScale: "জাতীয় বেতন স্কেল ২০১৫, ৯ম গ্রেড",
    officialRef: "erecruitment.bb.org.bd"
  },
  {
    id: "GOVT-RAIL-26",
    title: "উপ-সহকারী প্রকৌশলী ও স্টেশন মাস্টার নিয়োগ",
    ministryOrDepartment: "বাংলাদেশ রেলওয়ে (BR)",
    totalPosts: 450,
    applicationDeadline: "২৮ নভেম্বর ২০২৬",
    circularDate: "১২ অক্টোবর ২০২৬",
    gradePayScale: "জাতীয় বেতন স্কেল ২০১৫, ১০ম গ্রেড (১৬,০০০ - ৩৮,৬৪০ টাকা)",
    officialRef: "railway.gov.bd"
  },
  {
    id: "GOVT-BIMAN-26",
    title: "অ্যাসিস্ট্যান্ট ম্যানেজার (আইটি ও অপারেশনস)",
    ministryOrDepartment: "বিমান বাংলাদেশ এয়ারলাইন্স পিএলসি",
    totalPosts: 35,
    applicationDeadline: "৩০ নভেম্বর ২০২৬",
    circularDate: "১৫ অক্টোবর ২০২৬",
    gradePayScale: "বিমান নিজস্ব গ্রেড-৬ (২২,০০০ - ৫৩,০৬০ টাকা)",
    officialRef: "biman.org.bd/jobs"
  }
];

// ---------------------------------------------------------------------------
// 5. Bangladesh Industry Salary Insights & Benchmarks
// ---------------------------------------------------------------------------
export const SALARY_BENCHMARKS: SalaryBenchmark[] = [
  {
    industry: "সফটওয়্যার ও আইটি (Tech)",
    roleTitle: "সফটওয়্যার ইঞ্জিনিয়ার (Full Stack)",
    entryLevelSalary: "৩৫,০০০ - ৫৫,০০০ টাকা",
    midLevelSalary: "৭০,০০০ - ১,৩০,০০০ টাকা",
    seniorLevelSalary: "১,৮০,০০০ - ৩,০০,০০০+ টাকা"
  },
  {
    industry: "ব্যাংকিং ও ফিন্যান্সিয়াল",
    roleTitle: "ম্যানেজমেন্ট ট্রেইনি / অফিসার",
    entryLevelSalary: "৫০,০০০ - ৭০,০০০ টাকা",
    midLevelSalary: "৮০,০০০ - ১,৪০,০০০ টাকা",
    seniorLevelSalary: "১,৬০,০০০ - ২,৫০,০০০+ টাকা"
  },
  {
    industry: "ফার্মাসিউটিক্যালস",
    roleTitle: "কিউসি কেমিস্ট / প্রোডাক্ট অফিসার",
    entryLevelSalary: "৩০,০০০ - ৪২,০০০ টাকা",
    midLevelSalary: "৫৫,০০০ - ৮৫,০০০ টাকা",
    seniorLevelSalary: "১,১০,০০০ - ১,৯০,০০০ টাকা"
  },
  {
    industry: "এনজিও ও উন্নয়ন সংস্থা",
    roleTitle: "প্রজেক্ট কো-অর্ডিনেটর",
    entryLevelSalary: "৩৫,০০০ - ৫০,০০০ টাকা",
    midLevelSalary: "৬৫,০০০ - ১,১০,০০০ টাকা",
    seniorLevelSalary: "১,৪০,০০০ - ২,২০,০০০ টাকা"
  },
  {
    industry: "টেক্সটাইল ও ম্যানুফ্যাকচারিং",
    roleTitle: "ইন্ডাস্ট্রিয়াল ইঞ্জিনিয়ার / মার্চেন্ডাইজার",
    entryLevelSalary: "২৫,০০০ - ৩৮,০০০ টাকা",
    midLevelSalary: "৫০,০০০ - ৯০,০০০ টাকা",
    seniorLevelSalary: "১,২০,০০০ - ২,০০,০০০ টাকা"
  }
];

// ---------------------------------------------------------------------------
// 6. Professional Career & Resume FAQs
// ---------------------------------------------------------------------------
export const CAREER_PORTAL_FAQS: CareerFaq[] = [
  {
    question: "অগ্রযাত্রা ক্যারিয়ার হাবে আবেদন করার সুবিধা কী এবং সিলগালা সিভি স্ন্যাপশট কী?",
    answer: "অগ্রযাত্রা প্ল্যাটফর্মে আপনার প্রতিটি একাডেমিক স্কোর, অলিম্পিয়াড ব্যাজ এবং গিটহাব কোড ক্রিপ্টোগ্রাফিকভাবে সংরক্ষিত থাকে। আবেদন করার সময় একটি অনন্য SHA-256 সিলগালা সিভি স্ন্যাপশট তৈরি হয়, যাতে নিয়োগকারী শতভাগ নিশ্চিত হতে পারেন যে আবেদনকারী পরবর্তীতে তথ্য পরিবর্তন করেননি।"
  },
  {
    question: "ফ্রেশার বা বিশ্ববিদ্যালয়ের শিক্ষার্থীরা কীভাবে ইন্টার্নশিপের সুযোগ পেতে পারে?",
    answer: "আমাদের ফিল্টারে 'ফ্রেশার ও ইন্টার্নশিপ' মোড চালু করলেই অভিজ্ঞতাহীন প্রার্থীর উপযোগী সকল টেক, এনজিও ও করপোরেট ইন্টার্নশিপ তালিকাভুক্ত হবে। প্রজেক্ট ডেমো ও স্কিল প্রমাণপত্র থাকলে শিক্ষার্থীরা অগ্রাধিকার পায়।"
  },
  {
    question: "সরকারি চাকরির সার্কুলারে কি সরাসরি এই প্ল্যাটফর্ম থেকে আবেদন করা যায়?",
    answer: "সরকারি সার্কুলার সেকশনে বিপিএসসি, বাংলাদেশ ব্যাংক ও মন্ত্রণালয়ের অনুমোদিত গেজেট এবং সরাসরি অফিসিয়াল আবেদন লিংক (যেমন: teletalk / bpsc.gov.bd) সংযুক্ত থাকে যাতে প্রার্থীরা ভুয়া বিজ্ঞপ্তি থেকে সুরক্ষিত থাকেন।"
  },
  {
    question: "নিয়োগকারী প্রতিষ্ঠান কীভাবে অগ্রযাত্রায় চাকরির বিজ্ঞাপন প্রকাশ করতে পারে?",
    answer: "নিয়োগকর্তারা 'পোস্ট এ জব' ৪-ধাপের উইজার্ডের মাধ্যমে খুব সহজেই তাদের প্রতিষ্ঠানের বিস্তারিত পদবি, প্রয়োজনীয় যোগ্যতা ও বেতন কাঠামো নির্ধারণ করে তাৎক্ষণিক চাকরি পোস্ট করতে পারেন।"
  }
];
