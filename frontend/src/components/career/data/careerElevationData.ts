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
  descriptionEn?: string;
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
  titleEn?: string;
  companyName: string;
  companyNameEn?: string;
  companyMonogram: string; // 2-letter corporate monogram
  monogramBg: string;      // Tailwind bg class
  monogramText: string;    // Tailwind text class
  companyIndustry: string;
  companyIndustryEn?: string;
  category: string;
  orgType: 'GOVT' | 'PRIVATE' | 'NGO' | 'MULTINATIONAL' | 'SEMI_GOVT';
  jobNature: 'FULL_TIME' | 'PART_TIME' | 'CONTRACTUAL' | 'INTERNSHIP' | 'FREELANCE';
  jobLevel: 'ENTRY' | 'MID' | 'SENIOR';
  vacancy: number;
  locationDistrict: string;
  locationDistrictEn?: string;
  locationDivision: string;
  locationDivisionEn?: string;
  minSalary: number;
  maxSalary: number;
  isSalaryNegotiable: boolean;
  deadline: string;        // Bengali readable date
  deadlineEn?: string;
  deadlineIso: string;     // ISO timestamp for urgency calculation
  publishedDate: string;
  publishedDateEn?: string;
  experienceYears: string;
  experienceYearsEn?: string;
  educationRequirements: string[];
  educationRequirementsEn?: string[];
  responsibilities: string[];
  responsibilitiesEn?: string[];
  benefits: string[];
  benefitsEn?: string[];
  isHotJob: boolean;
  isEarlyAccess: boolean;
  applicantsCount: number;
}

export interface GovtCircular {
  id: string;
  title: string;
  titleEn?: string;
  ministryOrDepartment: string;
  ministryOrDepartmentEn?: string;
  totalPosts: number;
  applicationDeadline: string;
  applicationDeadlineEn?: string;
  circularDate: string;
  gradePayScale: string;
  gradePayScaleEn?: string;
  officialRef: string;
}

export interface SalaryBenchmark {
  industry: string;
  industryEn?: string;
  roleTitle: string;
  roleTitleEn?: string;
  entryLevelSalary: string;
  entryLevelSalaryEn?: string;
  midLevelSalary: string;
  midLevelSalaryEn?: string;
  seniorLevelSalary: string;
  seniorLevelSalaryEn?: string;
}

export interface CareerFaq {
  question: string;
  questionEn?: string;
  answer: string;
  answerEn?: string;
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
    description: "ফুলস্ট্যাক, পাইথন, ফ্রন্টএন্ড, ক্লাউড আর্কিটেকচার ও ডেভঅপস",
    descriptionEn: "Full Stack, Python, Frontend, Cloud Architecture & DevOps"
  },
  {
    id: "cat_bank",
    nameBn: "ব্যাংক ও নন-ব্যাংক ফিন্যান্স",
    nameEn: "Bank & Non-Bank Fin",
    jobCount: 890,
    type: "functional",
    iconName: "Building2",
    description: "ম্যানেজমেন্ট ট্রেইনি, ক্রেডিট অ্যানালিস্ট ও জেনারেল ব্যাংকিং",
    descriptionEn: "Management Trainee, Credit Analyst & General Banking"
  },
  {
    id: "cat_engineering",
    nameBn: "ইঞ্জিনিয়ারিং ও আর্কিটেকচার",
    nameEn: "Engineer & Architect",
    jobCount: 760,
    type: "functional",
    iconName: "Compass",
    description: "সিভিল, ইলেকট্রিক্যাল, মেকানিক্যাল ও ইন্ডাস্ট্রিয়াল প্রোডাকশন",
    descriptionEn: "Civil, Electrical, Mechanical & Industrial Production"
  },
  {
    id: "cat_marketing",
    nameBn: "মার্কেটিং ও সেলস",
    nameEn: "Marketing & Sales",
    jobCount: 1150,
    type: "functional",
    iconName: "TrendingUp",
    description: "ব্র্যান্ডিং, ডিজিটাল গ্রোথ, বিজনেস ডেভেলপমেন্ট ও রিটেল",
    descriptionEn: "Branding, Digital Growth, Business Development & Retail"
  },
  {
    id: "cat_govt",
    nameBn: "সরকারি ও ক্যাডার সার্ভিস",
    nameEn: "Government & Cadre",
    jobCount: 520,
    type: "functional",
    iconName: "Award",
    description: "বিপিএসসি, স্বায়ত্তশাসিত প্রতিষ্ঠান ও মন্ত্রণালয়ের নিয়োগ বিজ্ঞপ্তি",
    descriptionEn: "BPSC, Autonomous Institutions & Ministry Career Notices"
  },
  {
    id: "cat_ngo",
    nameBn: "এনজিও ও উন্নয়ন সংস্থা",
    nameEn: "NGO & Development",
    jobCount: 640,
    type: "functional",
    iconName: "Users",
    description: "ফিল্ড অপারেশন, প্রোগ্রাম মনিটরিং ও রিসার্চ কো-অর্ডিনেটর",
    descriptionEn: "Field Operations, Program Monitoring & Research Coordination"
  },
  {
    id: "cat_pharma",
    nameBn: "মেডিকেল ও ফার্মাসিউটিক্যাল",
    nameEn: "Medical & Pharma",
    jobCount: 580,
    type: "functional",
    iconName: "Activity",
    description: "মেডিকেল প্রমোশন, কিউএ কেমিস্ট ও ক্লিনিক্যাল রিসার্চ",
    descriptionEn: "Medical Promotion, QA Chemist & Clinical Research"
  },
  {
    id: "cat_education",
    nameBn: "শিক্ষা ও প্রশিক্ষণ",
    nameEn: "Education & Training",
    jobCount: 490,
    type: "functional",
    iconName: "BookOpen",
    description: "বিশ্ববিদ্যালয় প্রভাষক, কলেজ শিক্ষক ও কর্পোরেট ট্রেইনার",
    descriptionEn: "University Lecturers, College Faculty & Corporate Trainers"
  },
  {
    id: "cat_skill_elec",
    nameBn: "ইলেকট্রিশিয়ান ও টেকনিশিয়ান",
    nameEn: "Electrician & Technician",
    jobCount: 410,
    type: "special_skill",
    iconName: "Zap",
    description: "ইন্ডাস্ট্রিয়াল ওয়্যারিং, এইচভিএসি মেইনটেন্যান্স ও পাওয়ার কন্ট্রোল",
    descriptionEn: "Industrial Wiring, HVAC Maintenance & Power Control"
  },
  {
    id: "cat_skill_garments",
    nameBn: "গার্মেন্টস ও টেক্সটাইল টেকনিশিয়ান",
    nameEn: "Garments & Textile",
    jobCount: 680,
    type: "special_skill",
    iconName: "Scissors",
    description: "প্যাটার্ন মেকিং, কোয়ালিটি অডিটর ও মার্চেন্ডাইজিং অ্যাসিস্ট্যান্ট",
    descriptionEn: "Pattern Making, Quality Auditor & Merchandising Assistant"
  },
  {
    id: "cat_skill_driver",
    nameBn: "ড্রাইভার ও লজিস্টিকস রাইডার",
    nameEn: "Driver & Logistics",
    jobCount: 530,
    type: "special_skill",
    iconName: "Truck",
    description: "হেভি/লাইট লাইসেন্সধারী ড্রাইভার ও এক্সপ্রেস ডেলিভারি রাইডার",
    descriptionEn: "Heavy/Light Licensed Drivers & Express Delivery Couriers"
  },
  {
    id: "cat_skill_chef",
    nameBn: "শেফ ও ক্যাটারিং সার্ভিস",
    nameEn: "Chef & Hospitality",
    jobCount: 380,
    type: "special_skill",
    iconName: "Utensils",
    description: "হোটেল রন্ধনশিল্পী, বেকারি স্পেশালিস্ট ও ফুড সেফটি সুপারভাইজার",
    descriptionEn: "Culinary Artists, Bakery Specialists & Food Safety Leads"
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
    titleEn: "Junior Software Engineer (Python / FastAPI)",
    companyName: "ব্রেনস্টেশন ২৩ (BrainStation 23)",
    companyNameEn: "BrainStation 23",
    companyMonogram: "BS",
    monogramBg: "bg-blue-900",
    monogramText: "text-blue-100",
    companyIndustry: "Software & Technology",
    companyIndustryEn: "Software & Technology",
    category: "cat_it",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 4,
    locationDistrict: "ঢাকা মহানগর",
    locationDistrictEn: "Dhaka Metro",
    locationDivision: "dhaka",
    locationDivisionEn: "Dhaka",
    minSalary: 35000,
    maxSalary: 55000,
    isSalaryNegotiable: false,
    deadline: "৩০ নভেম্বর ২০২৬",
    deadlineEn: "30 November 2026",
    deadlineIso: "2026-11-30T23:59:59Z",
    publishedDate: "২০ অক্টোবর ২০২৬",
    publishedDateEn: "20 October 2026",
    experienceYears: "০ - ১ বছর (ফ্রেশার স্বাগতম)",
    experienceYearsEn: "0 - 1 Year (Freshers Welcome)",
    educationRequirements: [
      "কম্পিউটার সায়েন্স ও ইঞ্জিনিয়ারিং (CSE) অথবা সমমানের বিষয়ে স্নাতক/বিএসসি ডিগ্রি।",
      "ন্যূনতম সিজিপিএ ৩.০০ (৪.০০ এর স্কেলে)।"
    ],
    educationRequirementsEn: [
      "Bachelor's / BSc in Computer Science & Engineering (CSE) or equivalent discipline.",
      "Minimum CGPA 3.00 on a 4.00 scale."
    ],
    responsibilities: [
      "উচ্চ কর্মক্ষমতাসম্পন্ন রেস্টফুল এপিআই ডিজাইন ও ফাস্টএপিআই দিয়ে বাস্তবায়ন।",
      "পোস্টগ্রেসকিউএল ডাটাবেজ অপ্টিমাইজেশন ও জটিল কোয়েরি প্রোফাইলিং।",
      "ডকারাইজেশন ও সিআই/সিডি অটোমেশন পাইপলাইনে সক্রিয় অবদান রাখা।",
      "টিম মেম্বারদের কোড রিভিউ ও টেস্ট-ড্রিভেন ডেভেলপমেন্ট চর্চা বজায় রাখা।"
    ],
    responsibilitiesEn: [
      "Design and implement high-performance RESTful APIs using FastAPI.",
      "PostgreSQL database query optimization and schema profiling.",
      "Active contribution to Dockerization and CI/CD automation pipelines.",
      "Participate in peer code reviews and maintain Test-Driven Development (TDD) hygiene."
    ],
    benefits: [
      "বছরে ২টি উৎসব বোনাস (মূল বেতনের সমপরিমাণ)।",
      "প্রভিডেন্ট ফান্ড ও গ্র্যাচুইটি পলিসি সুবিধা।",
      "অফিসিয়াল লাঞ্চ ও স্ನ್ಯাকস কমপ্লিমেন্টারি।",
      "বার্ষিক পারফরম্যান্স ও স্কিল ইনক্রিমেন্ট।"
    ],
    benefitsEn: [
      "2 Festival Bonuses per year (equal to basic salary).",
      "Provident fund and gratuity policy benefits.",
      "Complimentary office lunch and evening refreshments.",
      "Annual performance and merit-based skill increments."
    ],
    isHotJob: true,
    isEarlyAccess: true,
    applicantsCount: 142
  },
  {
    id: "JOB-BD-2026-002",
    title: "ম্যানেজমেন্ট ট্রেইনি অফিসার (MTO - 2026)",
    titleEn: "Management Trainee Officer (MTO - 2026)",
    companyName: "ইস্টার্ন ব্যাংক লিমিটেড (EBL)",
    companyNameEn: "Eastern Bank Limited (EBL)",
    companyMonogram: "EB",
    monogramBg: "bg-emerald-900",
    monogramText: "text-emerald-100",
    companyIndustry: "Banking & Financial Institutions",
    companyIndustryEn: "Banking & Financial Institutions",
    category: "cat_bank",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 15,
    locationDistrict: "ঢাকা মহানগর",
    locationDistrictEn: "Dhaka Metro",
    locationDivision: "dhaka",
    locationDivisionEn: "Dhaka",
    minSalary: 65000,
    maxSalary: 75000,
    isSalaryNegotiable: false,
    deadline: "১৫ নভেম্বর ২০২৬",
    deadlineEn: "15 November 2026",
    deadlineIso: "2026-11-15T23:59:59Z",
    publishedDate: "১৮ অক্টোবর ২০২৬",
    publishedDateEn: "18 October 2026",
    experienceYears: "অভিজ্ঞতার প্রয়োজন নেই (নতুন স্নাতকদের জন্য)",
    experienceYearsEn: "No prior experience required (Fresh graduates)",
    educationRequirements: [
      "যেকোনো স্বীকৃত বিশ্ববিদ্যালয় থেকে ফিন্যান্স, ব্যাংকিং, ইকোনমিক্স বা ব্যবসায় প্রশাসনে বিবিএ/এমবিএ।",
      "এসএসসি ও এইচএসসিতে ন্যূনতম জিপিএ ৪.৫০ এবং স্নাতক পর্যায়ে ৩.২০।"
    ],
    educationRequirementsEn: [
      "BBA / MBA in Finance, Banking, Economics, or Business Administration from an accredited university.",
      "Minimum GPA 4.50 in SSC/HSC and CGPA 3.20 at undergraduate level."
    ],
    responsibilities: [
      "শাখা ব্যাংকিং, ক্রেডিট অ্যানালাইসিস ও ট্রেড সার্ভিসের বিভিন্ন ডেস্ক পরিচালনা।",
      "রিটেইল ও করপোরেট ক্লায়েন্টদের ফাইন্যান্সিয়াল পোর্টফোলিও মূল্যায়ন।",
      "১ বছর সফল প্রশিক্ষণ শেষে সিনিয়র প্রিন্সিপাল অফিসার ধাপে স্থায়ীকরণ।"
    ],
    responsibilitiesEn: [
      "Rotational management across branch banking, credit risk, and trade services desks.",
      "Financial portfolio appraisal for retail and commercial corporate clients.",
      "Confirmation into Senior Principal Officer rank following 1-year structured track."
    ],
    benefits: [
      "প্রবেশনারি মেয়াদে মাসিক আকর্ষণীয় প্রশিক্ষণ ভাতা।",
      "গ্রুপ হেলথ ও লাইফ ইন্স্যুরেন্স প্যাকেজ।",
      "বাৎসরিক ব্যাংকিং প্রফিট শেয়ারিং বোনাস।"
    ],
    benefitsEn: [
      "Lucrative monthly stipend during probationary training period.",
      "Comprehensive group health and life insurance coverage.",
      "Annual banking profit-sharing dividends and performance bonuses."
    ],
    isHotJob: true,
    isEarlyAccess: false,
    applicantsCount: 389
  },
  {
    id: "JOB-BD-2026-003",
    title: "অ্যাসিস্ট্যান্ট ডিরেক্টর (জেনারেল) - সার্কুলার ২০২৬",
    titleEn: "Assistant Director (General) - Circular 2026",
    companyName: "বাংলাদেশ ব্যাংক (কেন্দ্রীয় ব্যাংক)",
    companyNameEn: "Bangladesh Bank (Central Bank)",
    companyMonogram: "BB",
    monogramBg: "bg-amber-900",
    monogramText: "text-amber-100",
    companyIndustry: "Central Banking & Regulatory",
    companyIndustryEn: "Central Banking & Regulatory",
    category: "cat_govt",
    orgType: "GOVT",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 100,
    locationDistrict: "ঢাকা মহানগর",
    locationDistrictEn: "Dhaka Metro",
    locationDivision: "dhaka",
    locationDivisionEn: "Dhaka",
    minSalary: 42000,
    maxSalary: 53060,
    isSalaryNegotiable: false,
    deadline: "০৫ ডিসেম্বর ২০২৬",
    deadlineEn: "05 December 2026",
    deadlineIso: "2026-12-05T23:59:59Z",
    publishedDate: "২৫ অক্টোবর ২০২৬",
    publishedDateEn: "25 October 2026",
    experienceYears: "অভিজ্ঞতা বাধ্যতামূলক নয়",
    experienceYearsEn: "No prior experience required",
    educationRequirements: [
      "যেকোনো বিষয়ে ৪ বছর মেয়াদী স্নাতক/স্নাতকোত্তর ডিগ্রি (ন্যূনতম ২য় শ্রেণি বা সমমান)।",
      "শিক্ষা জীবনে কোনো তৃতীয় বিভাগ গ্রহণযোগ্য নয়।"
    ],
    educationRequirementsEn: [
      "4-year Bachelor's / Master's degree in any discipline (minimum 2nd class or equivalent).",
      "No 3rd division/class in academic lifecycle."
    ],
    responsibilities: [
      "মুদ্রানীতি প্রণয়ন, বৈদেশিক মুদ্রার রিজার্ভ পর্যবেক্ষণ ও ব্যাংক নিয়ন্ত্রণ।",
      "ব্যাংকিং পরিদর্শন ও পরিদর্শন প্রতিবেদনের ভিত্তিতে সুপারভাইজরি একশন গ্রহণ।"
    ],
    responsibilitiesEn: [
      "Formulation of monetary policy, FX reserve surveillance, and scheduled bank oversight.",
      "Regulatory bank inspection and implementation of risk supervisory directives."
    ],
    benefits: [
      "জাতীয় বেতন স্কেল ২০১৫ অনুযায়ী ৯ম গ্রেডের পূর্ণ সুবিধাদি।",
      "সরকারি আবাসন ও সুদমুক্ত হোম লোন স্কিম।",
      "উচ্চশিক্ষার জন্য বৈদেশিক স্কলারশিপ প্রোগ্রাম।"
    ],
    benefitsEn: [
      "Full 9th Grade benefits under National Pay Scale 2015.",
      "Government residential quarters and interest-free home building finance.",
      "Sponsored overseas postgraduate scholarships."
    ],
    isHotJob: false,
    isEarlyAccess: false,
    applicantsCount: 12500
  },
  {
    id: "JOB-BD-2026-004",
    title: "প্রোগ্রাম অফিসার (কমিউনিটি এডুকেশন)",
    titleEn: "Program Officer (Community Education)",
    companyName: "ব্র্যাক (BRAC International)",
    companyNameEn: "BRAC International",
    companyMonogram: "BR",
    monogramBg: "bg-pink-900",
    monogramText: "text-pink-100",
    companyIndustry: "Non-Government Organization",
    companyIndustryEn: "Non-Government Organization",
    category: "cat_ngo",
    orgType: "NGO",
    jobNature: "FULL_TIME",
    jobLevel: "MID",
    vacancy: 6,
    locationDistrict: "বগুড়া",
    locationDistrictEn: "Bogura",
    locationDivision: "rajshahi",
    locationDivisionEn: "Rajshahi",
    minSalary: 40000,
    maxSalary: 48000,
    isSalaryNegotiable: true,
    deadline: "২৫ নভেম্বর ২০২৬",
    deadlineEn: "25 November 2026",
    deadlineIso: "2026-11-25T23:59:59Z",
    publishedDate: "২২ অক্টোবর ২০২৬",
    publishedDateEn: "22 October 2026",
    experienceYears: "১ - ৩ বছর",
    experienceYearsEn: "1 - 3 Years",
    educationRequirements: [
      "সমাজবিজ্ঞান, সমাজকল্যাণ, বা শিক্ষা বিষয়ে স্নাতক/মাস্টার্স।"
    ],
    educationRequirementsEn: [
      "Bachelor's / Master's in Sociology, Social Work, Education, or relevant field."
    ],
    responsibilities: [
      "তৃণমূল পর্যায়ে প্রাথমিক ও উপানুষ্ঠানিক শিক্ষা প্রকল্প বাস্তবায়ন।",
      "স্থানীয় অভিভাবক ও শিক্ষকদের সাথে সমন্বয় সভা পরিচালনা এবং ডেটা এন্ট্রি।"
    ],
    responsibilitiesEn: [
      "Field-level execution of primary and non-formal community learning initiatives.",
      "Facilitate stakeholder meetings with guardians/teachers and maintain M&E data entry."
    ],
    benefits: [
      "মোবাইল ও যাতায়াত ভাতা।",
      "বার্ষিক স্বাস্থ্য বীমা ও প্রভিডেন্ট ফান্ড।"
    ],
    benefitsEn: [
      "Official mobile and conveyance allowances.",
      "Annual health insurance policy and contributory provident fund."
    ],
    isHotJob: false,
    isEarlyAccess: true,
    applicantsCount: 94
  },
  {
    id: "JOB-BD-2026-005",
    title: "কোয়ালিটি কন্ট্রোল কেমিস্ট (QC Chemist)",
    titleEn: "Quality Control Chemist (QC Chemist)",
    companyName: "স্কয়ার ফার্মাসিউটিক্যালস পিএলসি",
    companyNameEn: "Square Pharmaceuticals PLC",
    companyMonogram: "SQ",
    monogramBg: "bg-slate-900",
    monogramText: "text-slate-100",
    companyIndustry: "Pharmaceutical & Healthcare",
    companyIndustryEn: "Pharmaceutical & Healthcare",
    category: "cat_pharma",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 5,
    locationDistrict: "পাবনা",
    locationDistrictEn: "Pabna",
    locationDivision: "rajshahi",
    locationDivisionEn: "Rajshahi",
    minSalary: 38000,
    maxSalary: 45000,
    isSalaryNegotiable: false,
    deadline: "২০ নভেম্বর ২০২৬",
    deadlineEn: "20 November 2026",
    deadlineIso: "2026-11-20T23:59:59Z",
    publishedDate: "১৯ অক্টোবর ২০২৬",
    publishedDateEn: "19 October 2026",
    experienceYears: "০ - ২ বছর",
    experienceYearsEn: "0 - 2 Years",
    educationRequirements: [
      "রসায়ন / ফলিত রসায়নে বিএসসি বা এমএসসি।"
    ],
    educationRequirementsEn: [
      "BSc or MSc in Chemistry / Applied Chemistry."
    ],
    responsibilities: [
      "এইচপিএলসি এবং ইউভি স্পেকট্রোফোটোমেট্রি দ্বারা ড্রাগ স্যাম্পল পরীক্ষা।",
      "জিএমপি ও স্ট্যান্ডার্ড অপারেটিং প্রসিডিউর (SOP) শতভাগ বজায় রাখা।"
    ],
    responsibilitiesEn: [
      "Assay of active pharmaceutical ingredients via HPLC and UV spectrophotometry.",
      "Strict compliance with cGMP guidelines and standard operating procedures (SOP)."
    ],
    benefits: [
      "কোম্পানির নিজস্ব ট্রান্সপোর্ট ও ক্যাফেটেরিয়া সুবিধা।",
      "বছরে ৩টি বোনাস (২টি উৎসব + ১টি প্রফিট বোনাস)।"
    ],
    benefitsEn: [
      "Dedicated company transport and subsidized cafeteria meals.",
      "3 Annual bonuses (2 Festival + 1 WPPF Profit Sharing bonus)."
    ],
    isHotJob: true,
    isEarlyAccess: false,
    applicantsCount: 167
  },
  {
    id: "JOB-BD-2026-006",
    title: "ইন্টার্ন - ফ্রন্টএন্ড ডেভেলপার (Next.js / React)",
    titleEn: "Frontend Developer Intern (Next.js / React)",
    companyName: "চালডাল লিমিটেড (Chaldal)",
    companyNameEn: "Chaldal Limited",
    companyMonogram: "CD",
    monogramBg: "bg-orange-900",
    monogramText: "text-orange-100",
    companyIndustry: "E-Commerce & Tech",
    companyIndustryEn: "E-Commerce & Tech",
    category: "cat_it",
    orgType: "PRIVATE",
    jobNature: "INTERNSHIP",
    jobLevel: "ENTRY",
    vacancy: 3,
    locationDistrict: "রিমোট / বাসা থেকে",
    locationDistrictEn: "Remote / Work From Home",
    locationDivision: "dhaka",
    locationDivisionEn: "Dhaka",
    minSalary: 18000,
    maxSalary: 25000,
    isSalaryNegotiable: false,
    deadline: "১০ নভেম্বর ২০২৬",
    deadlineEn: "10 November 2026",
    deadlineIso: "2026-11-10T23:59:59Z",
    publishedDate: "২১ অক্টোবর ২০২৬",
    publishedDateEn: "21 October 2026",
    experienceYears: "ফ্রেশার বা ফাইনাল ইয়ার শিক্ষার্থী",
    experienceYearsEn: "Fresh graduates or Final-year students",
    educationRequirements: [
      "সিএসই বা রিলেটেড বিষয়ের আন্ডারগ্র্যাজুয়েট শিক্ষার্থী বা সদ্য পাসকৃত।"
    ],
    educationRequirementsEn: [
      "Undergraduate or fresh graduate in CSE, Software Engineering, or related fields."
    ],
    responsibilities: [
      "টেইলউইন্ড সিএসএস ও টাইপস্ক্রিপ্ট দিয়ে আধুনিক রেসপনসিভ ইউআই তৈরি।",
      "কম্পোনেন্ট লেভেল অপ্টিমাইজেশন ও পারফরম্যান্স মেট্রিক নিরীক্ষা।"
    ],
    responsibilitiesEn: [
      "Build modern responsive user interfaces using Tailwind CSS and TypeScript.",
      "Component-level code optimization, state hygiene, and Lighthouse performance checks."
    ],
    benefits: [
      "সফল ইন্টার্নশিপ শেষে ফুল-টাইম নিয়োগের সুযোগ।",
      "আন্তর্জাতিক মেন্টরদের সরাসরি দিকনির্দেশনা।"
    ],
    benefitsEn: [
      "Direct pathway to full-time engineering hire upon completion.",
      "1-on-1 engineering mentorship from senior staff."
    ],
    isHotJob: true,
    isEarlyAccess: true,
    applicantsCount: 218
  },
  {
    id: "JOB-BD-2026-007",
    title: "ইন্ডাস্ট্রিয়াল সিনিয়র ইলেকট্রিশিয়ান",
    titleEn: "Senior Industrial Electrician",
    companyName: "ওয়ালটন হাই-টেক ইন্ডাস্ট্রিজ পিএলসি",
    companyNameEn: "Walton Hi-Tech Industries PLC",
    companyMonogram: "WL",
    monogramBg: "bg-indigo-900",
    monogramText: "text-indigo-100",
    companyIndustry: "Electronics Manufacturing",
    companyIndustryEn: "Electronics Manufacturing",
    category: "cat_skill_elec",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "MID",
    vacancy: 8,
    locationDistrict: "গাজীপুর",
    locationDistrictEn: "Gazipur",
    locationDivision: "dhaka",
    locationDivisionEn: "Dhaka",
    minSalary: 28000,
    maxSalary: 36000,
    isSalaryNegotiable: true,
    deadline: "২৮ নভেম্বর ২০২৬",
    deadlineEn: "28 November 2026",
    deadlineIso: "2026-11-28T23:59:59Z",
    publishedDate: "১৭ অক্টোবর ২০২৬",
    publishedDateEn: "17 October 2026",
    experienceYears: "২ - ৪ বছর",
    experienceYearsEn: "2 - 4 Years",
    educationRequirements: [
      "বাংলাদেশ কারিগরি শিক্ষা বোর্ডের ডিপ্লোমা ইন ইলেকট্রিক্যাল বা ভোকেশনাল সার্টিফিকেট।"
    ],
    educationRequirementsEn: [
      "Diploma in Electrical Engineering or BTEB vocational trade certificate."
    ],
    responsibilities: [
      "উৎপাদন লাইনের ট্রান্সফর্মার, প্যানেল বোর্ড ও পিএলসি মোটর মেরামত।",
      "প্রিভেন্টিভ মেইনটেন্যান্স চেকশিট অনুযায়ী নিয়মিত যন্ত্রাংশ টেস্ট করা।"
    ],
    responsibilitiesEn: [
      "Preventive maintenance of substation transformers, switchgear, and PLC motor drives.",
      "Perform diagnostic testing as per industrial engineering maintenance protocol."
    ],
    benefits: [
      "কোম্পানি ডরমিটরি ও সাবসিডিযুক্ত খাবার।",
      "ওভারটাইম ভাতা ও বার্ষিক ইনক্রিমেন্ট।"
    ],
    benefitsEn: [
      "Subsidized company housing and canteen facilities.",
      "Standard overtime compensation and annual wage increments."
    ],
    isHotJob: false,
    isEarlyAccess: false,
    applicantsCount: 62
  },
  {
    id: "JOB-BD-2026-008",
    title: "অ্যাসিস্ট্যান্ট ইঞ্জিনিয়ার (সিভিল)",
    titleEn: "Assistant Engineer (Civil)",
    companyName: "মেঘনা গ্রুপ অব ইন্ডাস্ট্রিজ (MGI)",
    companyNameEn: "Meghna Group of Industries (MGI)",
    companyMonogram: "MG",
    monogramBg: "bg-teal-900",
    monogramText: "text-teal-100",
    companyIndustry: "Conglomerate & Heavy Industry",
    companyIndustryEn: "Conglomerate & Heavy Industry",
    category: "cat_engineering",
    orgType: "PRIVATE",
    jobNature: "FULL_TIME",
    jobLevel: "ENTRY",
    vacancy: 4,
    locationDistrict: "নারায়ণগঞ্জ",
    locationDistrictEn: "Narayanganj",
    locationDivision: "dhaka",
    locationDivisionEn: "Dhaka",
    minSalary: 38000,
    maxSalary: 45000,
    isSalaryNegotiable: false,
    deadline: "২২ নভেম্বর ২০২৬",
    deadlineEn: "22 November 2026",
    deadlineIso: "2026-11-22T23:59:59Z",
    publishedDate: "১৬ অক্টোবর ২০২৬",
    publishedDateEn: "16 October 2026",
    experienceYears: "১ - ২ বছর",
    experienceYearsEn: "1 - 2 Years",
    educationRequirements: [
      "বিএসসি ইন সিভিল ইঞ্জিনিয়ারিং (বুয়েট/কুয়েট/রুয়েট/চুয়েট অগ্রাধিকার)।"
    ],
    educationRequirementsEn: [
      "BSc in Civil Engineering (Graduates from BUET/KUET/RUET/CUET prioritized)."
    ],
    responsibilities: [
      "ইন্ডাস্ট্রিয়াল প্ল্যান্ট ও ওয়্যারহাউস নির্মাণ কাজের সরাসরি সাইট তদারকি।",
      "অটোক্যাড ড্রয়িং যাচাই ও ম্যাটেরিয়াল কোয়ালিটি টেস্টিং নিশ্চিতকরণ।"
    ],
    responsibilitiesEn: [
      "On-site civil execution and QA inspection for heavy industrial plants and warehouses.",
      "Verification of architectural AutoCAD schematics and structural strength testing."
    ],
    benefits: [
      "সাইট ট্রাভেল অ্যালাউন্স ও স্বাস্থ্য সুরক্ষা সরঞ্জাম।",
      "বার্ষিক বোনাস ও প্রভিডেন্ট ফান্ড।"
    ],
    benefitsEn: [
      "Site travel allowance and specialized personal protective equipment.",
      "Annual festive bonuses and contributory provident fund."
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
    titleEn: "48th BCS (Special) Examination Circular 2026",
    ministryOrDepartment: "বাংলাদেশ সরকারি কর্ম কমিশন (BPSC)",
    ministryOrDepartmentEn: "Bangladesh Public Service Commission (BPSC)",
    totalPosts: 3120,
    applicationDeadline: "১৫ ডিসেম্বর ২০২৬",
    applicationDeadlineEn: "15 December 2026",
    circularDate: "০১ অক্টোবর ২০২৬",
    gradePayScale: "জাতীয় বেতন স্কেল ২০১৫, ৯ম গ্রেড (২২,০০০ - ৫৩,০৬০ টাকা)",
    gradePayScaleEn: "National Pay Scale 2015, Grade 9 (BDT 22,000 - 53,060)",
    officialRef: "bpsc.gov.bd/circular/48-special"
  },
  {
    id: "GOVT-BB-AD-26",
    title: "সহকারী পরিচালক (রিসার্চ ও জেনারেল) সার্কুলার",
    titleEn: "Assistant Director (Research & General) Circular",
    ministryOrDepartment: "বাংলাদেশ ব্যাংক ব্যাংকার্স সিলেকশন কমিটি",
    ministryOrDepartmentEn: "Bangladesh Bank Bankers Selection Committee",
    totalPosts: 125,
    applicationDeadline: "১০ ডিসেম্বর ২০২৬",
    applicationDeadlineEn: "10 December 2026",
    circularDate: "০৫ অক্টোবর ২০২৬",
    gradePayScale: "জাতীয় বেতন স্কেল ২০১৫, ৯ম গ্রেড",
    gradePayScaleEn: "National Pay Scale 2015, Grade 9",
    officialRef: "erecruitment.bb.org.bd"
  },
  {
    id: "GOVT-RAIL-26",
    title: "উপ-সহকারী প্রকৌশলী ও স্টেশন মাস্টার নিয়োগ",
    titleEn: "Sub-Assistant Engineer & Station Master Recruitment",
    ministryOrDepartment: "বাংলাদেশ রেলওয়ে (BR)",
    ministryOrDepartmentEn: "Bangladesh Railway (BR)",
    totalPosts: 450,
    applicationDeadline: "২৮ নভেম্বর ২০২৬",
    applicationDeadlineEn: "28 November 2026",
    circularDate: "১২ অক্টোবর ২০২৬",
    gradePayScale: "জাতীয় বেতন স্কেল ২০১৫, ১০ম গ্রেড (১৬,০০০ - ৩৮,৬৪০ টাকা)",
    gradePayScaleEn: "National Pay Scale 2015, Grade 10 (BDT 16,000 - 38,640)",
    officialRef: "railway.gov.bd"
  },
  {
    id: "GOVT-BIMAN-26",
    title: "অ্যাসিস্ট্যান্ট ম্যানেজার (আইটি ও অপারেশনস)",
    titleEn: "Assistant Manager (IT & Operations)",
    ministryOrDepartment: "বিমান বাংলাদেশ এয়ারলাইন্স পিএলসি",
    ministryOrDepartmentEn: "Biman Bangladesh Airlines PLC",
    totalPosts: 35,
    applicationDeadline: "৩০ নভেম্বর ২০২৬",
    applicationDeadlineEn: "30 November 2026",
    circularDate: "১৫ অক্টোবর ২০২৬",
    gradePayScale: "বিমান নিজস্ব গ্রেড-৬ (২২,০০০ - ৫৩,০৬০ টাকা)",
    gradePayScaleEn: "Biman Grade 6 (BDT 22,000 - 53,060)",
    officialRef: "biman.org.bd/jobs"
  }
];

// ---------------------------------------------------------------------------
// 5. Bangladesh Industry Salary Insights & Benchmarks
// ---------------------------------------------------------------------------
export const SALARY_BENCHMARKS: SalaryBenchmark[] = [
  {
    industry: "সফটওয়্যার ও আইটি (Tech)",
    industryEn: "Software & Technology (Tech)",
    roleTitle: "সফটওয়্যার ইঞ্জিনিয়ার (Full Stack)",
    roleTitleEn: "Software Engineer (Full Stack)",
    entryLevelSalary: "৩৫,০০০ - ৫৫,০০০ টাকা",
    entryLevelSalaryEn: "BDT 35,000 - 55,000",
    midLevelSalary: "৭০,০০০ - ১,৩০,০০০ টাকা",
    midLevelSalaryEn: "BDT 70,000 - 130,000",
    seniorLevelSalary: "১,৮০,০০০ - ৩,০০,০০০+ টাকা",
    seniorLevelSalaryEn: "BDT 180,000 - 300,000+"
  },
  {
    industry: "ব্যাংকিং ও ফিন্যান্সিয়াল",
    industryEn: "Banking & Financial Institutions",
    roleTitle: "ম্যানেজমেন্ট ট্রেইনি / অফিসার",
    roleTitleEn: "Management Trainee / Officer",
    entryLevelSalary: "৫০,০০০ - ৭০,০০০ টাকা",
    entryLevelSalaryEn: "BDT 50,000 - 70,000",
    midLevelSalary: "৮০,০০০ - ১,৪০,০০০ টাকা",
    midLevelSalaryEn: "BDT 80,000 - 140,000",
    seniorLevelSalary: "১,৬০,০০০ - ২,৫০,০০০+ টাকা",
    seniorLevelSalaryEn: "BDT 160,000 - 250,000+"
  },
  {
    industry: "ফার্মাসিউটিক্যালস",
    industryEn: "Pharmaceuticals",
    roleTitle: "কিউসি কেমিস্ট / প্রোডাক্ট অফিসার",
    roleTitleEn: "QC Chemist / Product Officer",
    entryLevelSalary: "৩০,০০০ - ৪২,০০০ টাকা",
    entryLevelSalaryEn: "BDT 30,000 - 42,000",
    midLevelSalary: "৫৫,০০০ - ৮৫,০০০ টাকা",
    midLevelSalaryEn: "BDT 55,000 - 85,000",
    seniorLevelSalary: "১,১০,০০০ - ১,৯০,০০০ টাকা",
    seniorLevelSalaryEn: "BDT 110,000 - 190,000"
  },
  {
    industry: "এনজিও ও উন্নয়ন সংস্থা",
    industryEn: "NGO & Development Sector",
    roleTitle: "প্রজেক্ট কো-অর্ডিনেটর",
    roleTitleEn: "Project Coordinator",
    entryLevelSalary: "৩৫,০০০ - ৫০,০০০ টাকা",
    entryLevelSalaryEn: "BDT 35,000 - 50,000",
    midLevelSalary: "৬৫,০০০ - ১,১০,০০০ টাকা",
    midLevelSalaryEn: "BDT 65,000 - 110,000",
    seniorLevelSalary: "১,৪০,০০০ - ২,২০,০০০ টাকা",
    seniorLevelSalaryEn: "BDT 140,000 - 220,000"
  },
  {
    industry: "টেক্সটাইল ও ম্যানুফ্যাকচারিং",
    industryEn: "Textile & Manufacturing",
    roleTitle: "ইন্ডাস্ট্রিয়াল ইঞ্জিনিয়ার / মার্চেন্ডাইজার",
    roleTitleEn: "Industrial Engineer / Merchandiser",
    entryLevelSalary: "২৫,০০০ - ৩৮,০০০ টাকা",
    entryLevelSalaryEn: "BDT 25,000 - 38,000",
    midLevelSalary: "৫০,০০০ - ৯০,০০০ টাকা",
    midLevelSalaryEn: "BDT 50,000 - 90,000",
    seniorLevelSalary: "১,২০,০০০ - ২,০০,০০০ টাকা",
    seniorLevelSalaryEn: "BDT 120,000 - 200,000"
  }
];

// ---------------------------------------------------------------------------
// 6. Professional Career & Resume FAQs
// ---------------------------------------------------------------------------
export const CAREER_PORTAL_FAQS: CareerFaq[] = [
  {
    question: "অগ্রযাত্রা ক্যারিয়ার হাবে আবেদন করার সুবিধা কী এবং সিলগালা সিভি স্ন্যাপশট কী?",
    questionEn: "What are the benefits of applying via Agragoti Career Hub and what is a Sealed CV Snapshot?",
    answer: "অগ্রযাত্রা প্ল্যাটফর্মে আপনার প্রতিটি একাডেমিক স্কোর, অলিম্পিয়াড ব্যাজ এবং গিটহাব কোড ক্রিপ্টোগ্রাফিকভাবে সংরক্ষিত থাকে। আবেদন করার সময় একটি অনন্য SHA-256 সিলগালা সিভি স্ন্যাপশট তৈরি হয়, যাতে নিয়োগকারী শতভাগ নিশ্চিত হতে পারেন যে আবেদনকারী পরবর্তীতে তথ্য পরিবর্তন করেননি।",
    answerEn: "Every verified academic milestone, olympiad badge, and GitHub code artifact on Agragoti is cryptographically recorded. During application submission, a unique immutable SHA-256 sealed CV snapshot is created, guaranteeing recruiters that submitted credentials remain untampered."
  },
  {
    question: "ফ্রেশার বা বিশ্ববিদ্যালয়ের শিক্ষার্থীরা কীভাবে ইন্টার্নশিপের সুযোগ পেতে পারে?",
    questionEn: "How can university students and fresh graduates secure internship opportunities?",
    answer: "আমাদের ফিল্টারে 'ফ্রেশার ও ইন্টার্নশিপ' মোড চালু করলেই অভিজ্ঞতাহীন প্রার্থীর উপযোগী সকল টেক, এনজিও ও করপোরেট ইন্টার্নশিপ তালিকাভুক্ত হবে। প্রজেক্ট ডেমো ও স্কিল প্রমাণপত্র থাকলে শিক্ষার্থীরা অগ্রাধিকার পায়।",
    answerEn: "Activating the 'Fresher & Internship' filter instantly isolates tech, NGO, and corporate internships tailored for candidates without prior work history. Evidence-backed projects and verified skill proofs grant highest interview priority."
  },
  {
    question: "সরকারি চাকরির সার্কুলারে কি সরাসরি এই প্ল্যাটফর্ম থেকে আবেদন করা যায়?",
    questionEn: "Can candidates apply directly to government job circulars from this portal?",
    answer: "সরকারি সার্কুলার সেকশনে বিপিএসসি, বাংলাদেশ ব্যাংক ও মন্ত্রণালয়ের অনুমোদিত গেজেট এবং সরাসরি অফিসিয়াল আবেদন লিংক (যেমন: teletalk / bpsc.gov.bd) সংযুক্ত থাকে যাতে প্রার্থীরা ভুয়া বিজ্ঞপ্তি থেকে সুরক্ষিত থাকেন।",
    answerEn: "The government circulars archive provides authentic gazette notifications from BPSC, Bangladesh Bank, and ministries with direct links to official recruitment portals (e.g., teletalk / bpsc.gov.bd) protecting applicants from fraudulent notices."
  },
  {
    question: "নিয়োগকারী প্রতিষ্ঠান কীভাবে অগ্রযাত্রায় চাকরির বিজ্ঞাপন প্রকাশ করতে পারে?",
    questionEn: "How can recruiting organizations post job circulars on Agragoti?",
    answer: "নিয়োগকর্তারা 'পোস্ট এ জব' ৪-ধাপের উইজার্ডের মাধ্যমে খুব সহজেই তাদের প্রতিষ্ঠানের বিস্তারিত পদবি, প্রয়োজনীয় যোগ্যতা ও বেতন কাঠামো নির্ধারণ করে তাৎক্ষণিক চাকরি পোস্ট করতে পারেন।",
    answerEn: "Employers can publish openings seamlessly via the 4-step 'Post a Job' wizard by specifying role requirements, compensation frameworks, and candidate eligibility criteria."
  }
];
