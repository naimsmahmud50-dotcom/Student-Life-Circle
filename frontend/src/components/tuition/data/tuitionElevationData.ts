/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Tuition Marketplace Data Contracts & Verified Datasets
 * TOPIC:     CareTutors Reverse Engineering Elevation
 * FILE:      frontend/src/components/tuition/data/tuitionElevationData.ts
 * STANDARDS: Zero-Emoji, Pure Lucide Icon mapping, Original Scholar Monograms (Zero External Scraped Photos),
 *            WCAG 2.2 AAA Contrast, Bengali Typography Rigor
 */

export interface TuitionCategoryInfo {
  id: 'all' | 'bangla_medium' | 'english_version' | 'english_medium' | 'religious' | 'admission' | 'arts_lang' | 'special_child';
  nameBn: string;
  taglineBn: string;
  iconName: 'BookOpen' | 'Globe' | 'GraduationCap' | 'Languages' | 'Palette' | 'HeartHandshake' | 'Atom' | 'Award';
  jobsCount: number;
}

export interface TuitionJob {
  id: string; // e.g. "TUI-9104"
  titleBn: string;
  category: 'bangla_medium' | 'english_version' | 'english_medium' | 'religious' | 'admission' | 'arts_lang' | 'special_child';
  classGradeBn: string;
  subjectsBn: string[];
  mode: 'হোম টিউশন' | 'অনলাইন টিউশন' | 'গ্রুপ ব্যাচ';
  district: string;
  thana: string;
  areaBn: string;
  daysPerWeek: number;
  salaryBn: string;
  salaryAmount: number;
  genderPreferenceBn: 'পুরুষ টিউটর আবশ্যক' | 'মহিলা টিউটর আবশ্যক' | 'যেকোনো অভিজ্ঞ টিউটর';
  tutorRequirementBn: string;
  postedDateBn: string;
  applicantsCount: number;
  status: 'open' | 'shortlisting' | 'confirmed';
  escrowProtected: boolean;
}

export interface VerifiedTutor {
  id: string;
  nameBn: string;
  initialsBn: string;
  accentBg: string;
  institutionBn: string;
  departmentBn: string;
  degreeLevelBn: string;
  sscBackgroundBn: string;
  hscBackgroundBn: string;
  preferredCategories: string[];
  preferredSubjects: string[];
  preferredLocations: string[];
  experienceYearsBn: string;
  rating: number;
  totalReviews: number;
  tuitionsCompleted: number;
  expectedSalaryBn: string;
  verificationStatus: {
    nidVerified: boolean;
    academicIdVerified: boolean;
    backgroundChecked: boolean;
  };
}

export interface TuitionSalaryFormula {
  district: string;
  medium: string;
  classGroup: 'primary' | 'lower_secondary' | 'secondary_ssc' | 'higher_hsc' | 'admission';
  daysPerWeek: number;
  minSalary: number;
  maxSalary: number;
}

export interface TuitionFAQItem {
  id: string;
  questionBn: string;
  answerBn: string;
  category: 'guardian' | 'tutor';
}

export const TUITION_CATEGORIES: TuitionCategoryInfo[] = [
  {
    id: 'all',
    nameBn: 'সকল ক্যাটাগরি',
    taglineBn: 'সারাদেশের সকল টিউশন ও টিউটর',
    iconName: 'GraduationCap',
    jobsCount: 1420,
  },
  {
    id: 'bangla_medium',
    nameBn: 'বাংলা মাধ্যম',
    taglineBn: 'শ্রেণি ১-১২, এসএসসি ও এইচএসসি বোর্ড পাঠ্যক্রম',
    iconName: 'BookOpen',
    jobsCount: 680,
  },
  {
    id: 'english_version',
    nameBn: 'ইংলিশ ভার্সন',
    taglineBn: 'এনসিটিবি পাঠ্যক্রমের ইংরেজি সংস্করণ',
    iconName: 'Globe',
    jobsCount: 340,
  },
  {
    id: 'english_medium',
    nameBn: 'ইংলিশ মিডিয়াম',
    taglineBn: 'ক্যামব্রিজ ও এডেক্সেল ও/এ লেভেল কারিকুলাম',
    iconName: 'Languages',
    jobsCount: 195,
  },
  {
    id: 'religious',
    nameBn: 'ধর্মীয় ও কুরআন শিক্ষা',
    taglineBn: 'সহীহ কুরআন তিলাওয়াত, তাজবীদ ও আরবি শিক্ষা',
    iconName: 'Award',
    jobsCount: 85,
  },
  {
    id: 'admission',
    nameBn: 'ভর্তি পরীক্ষা প্রস্তুতি',
    taglineBn: 'বুয়েট, মেডিকেল, ঢাবি ক/খ/গ ইউনিট স্পেশাল',
    iconName: 'Atom',
    jobsCount: 72,
  },
  {
    id: 'arts_lang',
    nameBn: 'ভাষা ও স্কিলস',
    taglineBn: 'স্পোকেন ইংলিশ, আইইএলটিএস, ড্রয়িং ও মিউজিক',
    iconName: 'Palette',
    jobsCount: 48,
  },
  {
    id: 'special_child',
    nameBn: 'স্পেশাল চাইল্ড কেয়ার',
    taglineBn: 'অটিজম, এডিএইচডি ও ব্যক্তিগত বিশেষ পরিচর্যা',
    iconName: 'HeartHandshake',
    jobsCount: 24,
  },
];

export const TUITION_JOBS: TuitionJob[] = [
  {
    id: 'TUI-9101',
    titleBn: '১০ম শ্রেণির পদার্থবিজ্ঞান ও উচ্চতর গণিত টিউশন',
    category: 'bangla_medium',
    classGradeBn: '১০ম শ্রেণি (এসএসসি ২০২৭)',
    subjectsBn: ['পদার্থবিজ্ঞান', 'উচ্চতর গণিত', 'রসায়ন'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'ধানমন্ডি',
    areaBn: 'ঢাকা, ধানমন্ডি (রোড ৮/এ)',
    daysPerWeek: 3,
    salaryBn: '৮,০০০ - ১০,০০০ টাকা/মাস',
    salaryAmount: 9000,
    genderPreferenceBn: 'পুরুষ টিউটর আবশ্যক',
    tutorRequirementBn: 'বুয়েট (ECE) বা ঢাকা বিশ্ববিদ্যালয়ের নিয়মিত শিক্ষার্থী অগ্রাধিকার পাবেন। টেস্ট পেপার সমাধানে পারদর্শী হতে হবে।',
    postedDateBn: '২৪ অক্টোবর ২০২৬',
    applicantsCount: 4,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9102',
    titleBn: 'এইচএসসি ১ম বর্ষের কেমিস্ট্রি ও বায়োলজি টিউশন',
    category: 'english_version',
    classGradeBn: 'একাদশ শ্রেণি (এইচএসসি ২০২৭)',
    subjectsBn: ['রসায়ন ১ম পত্র', 'জীববিজ্ঞান ১ম পত্র'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'উত্তরা',
    areaBn: 'উত্তরা সেক্টর ৭, রবীন্দ্র সরণি',
    daysPerWeek: 3,
    salaryBn: '১০,০০০ - ১২,০০০ টাকা/মাস',
    salaryAmount: 11000,
    genderPreferenceBn: 'মহিলা টিউটর আবশ্যক',
    tutorRequirementBn: 'মেডিকেল কলেজ বা ঢাবি বায়োকেমিস্ট্রির অভিজ্ঞ মহিলা টিউটর প্রয়োজন। শিক্ষার্থীকে কনসেপচুয়াল ধারণা বুঝিয়ে পড়াতে হবে।',
    postedDateBn: '২৫ অক্টোবর ২০২৬',
    applicantsCount: 6,
    status: 'shortlisting',
    escrowProtected: true,
  },
  {
    id: 'TUI-9103',
    titleBn: 'ও-লেভেল ফিজিক্স ও কেমব্রিজ ম্যাথমেটিক্স টিউশন',
    category: 'english_medium',
    classGradeBn: 'O-Level (Class 10)',
    subjectsBn: ['Physics (5054)', 'Mathematics (4024)'],
    mode: 'অনলাইন টিউশন',
    district: 'ঢাকা',
    thana: 'গুলশান',
    areaBn: 'গুলশান ২ (অনলাইন জুম ক্লাস)',
    daysPerWeek: 4,
    salaryBn: '১২,০০০ - ১৫,০০০ টাকা/মাস',
    salaryAmount: 13500,
    genderPreferenceBn: 'যেকোনো অভিজ্ঞ টিউটর',
    tutorRequirementBn: 'ক্যামব্রিজ পাঠ্যক্রমে ও/এ লেভেল উত্তীর্ণ এবং বিগত ২+ বছর ইংলিশ মিডিয়াম পড়ানোর বাস্তব অভিজ্ঞতা থাকতে হবে।',
    postedDateBn: '২৫ অক্টোবর ২০২৬',
    applicantsCount: 3,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9104',
    titleBn: '৮ম শ্রেণির বিজ্ঞান, গণিত ও আইসিটি টিউশন',
    category: 'bangla_medium',
    classGradeBn: '৮ম শ্রেণি (নতুন শিক্ষাক্রম)',
    subjectsBn: ['বিজ্ঞান', 'গণিত', 'তথ্যপ্রযুক্তি'],
    mode: 'হোম টিউশন',
    district: 'চট্টগ্রাম',
    thana: 'পাঁচলাইশ',
    areaBn: 'পাঁচলাইশ আবাসিক এলাকা',
    daysPerWeek: 3,
    salaryBn: '৭,০০০ - ৮,৫০০ টাকা/মাস',
    salaryAmount: 7500,
    genderPreferenceBn: 'যেকোনো অভিজ্ঞ টিউটর',
    tutorRequirementBn: 'চট্টগ্রাম বিশ্ববিদ্যালয় বা চুয়েটের দায়িত্বশীল শিক্ষার্থী। নতুন শিক্ষাক্রমের অ্যাক্টিভিটি ভিত্তিক পড়াশোনায় দক্ষ।',
    postedDateBn: '২৩ অক্টোবর ২০২৬',
    applicantsCount: 5,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9105',
    titleBn: 'বুয়েট ভর্তি প্রস্তুতি গণিত স্পেশাল টিউশন',
    category: 'admission',
    classGradeBn: 'এডমিশন পরীক্ষার্থী (২০২৬)',
    subjectsBn: ['ক্যালকুলাস', 'মেকানিক্স', 'ভেক্টর গণিত'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'মিরপুর',
    areaBn: 'মিরপুর ডিওএইচএস',
    daysPerWeek: 2,
    salaryBn: '১০,০০০ টাকা/মাস',
    salaryAmount: 10000,
    genderPreferenceBn: 'পুরুষ টিউটর আবশ্যক',
    tutorRequirementBn: 'শুধুমাত্র বুয়েটের ৩য় বা ৪র্থ বর্ষের প্রকৌশল বিভাগের শিক্ষার্থী যাদের এডমিশন পড়ানোর পূর্ব অভিজ্ঞতা আছে।',
    postedDateBn: '২৬ অক্টোবর ২০২৬',
    applicantsCount: 2,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9106',
    titleBn: 'সহীহ কুরআন ও তাজবীদ শিক্ষা (শিশুদের জন্য)',
    category: 'religious',
    classGradeBn: '৪র্থ শ্রেণি ও কেজি',
    subjectsBn: ['কুরআনুল কারীম', 'তাজবীদ', 'দৈনন্দিন দোয়া ও মাসয়ালা'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'মোহাম্মদপুর',
    areaBn: 'মোহাম্মদপুর জাপান গার্ডেন সিটি',
    daysPerWeek: 4,
    salaryBn: '৬,০০০ - ৭,৫০০ টাকা/মাস',
    salaryAmount: 6500,
    genderPreferenceBn: 'মহিলা টিউটর আবশ্যক',
    tutorRequirementBn: 'হাফেজা বা কওমি/আলিয়া মাদরাসা ব্যাকগ্রাউন্ডের অভিজ্ঞ শিক্ষিকা। ধৈর্যশীল আচরণ আবশ্যক।',
    postedDateBn: '২১ অক্টোবর ২০২৬',
    applicantsCount: 7,
    status: 'confirmed',
    escrowProtected: true,
  },
  {
    id: 'TUI-9107',
    titleBn: 'আইইএলটিএস (IELTS) স্পিকিং ও রাইটিং মেন্টরশিপ',
    category: 'arts_lang',
    classGradeBn: 'উচ্চশিক্ষা ও স্কিলস শিক্ষার্থী',
    subjectsBn: ['IELTS Academic', 'Spoken English', 'Essay Writing'],
    mode: 'অনলাইন টিউশন',
    district: 'ঢাকা',
    thana: 'বনানী',
    areaBn: 'বনানী (অনলাইন গুগল মিট সেশন)',
    daysPerWeek: 3,
    salaryBn: '১২,০০০ - ১৪,০০০ টাকা/মাস',
    salaryAmount: 13000,
    genderPreferenceBn: 'যেকোনো অভিজ্ঞ টিউটর',
    tutorRequirementBn: 'আইইএলটিএস স্কোর ৮.০+ অথবা ঢাবি ইংরেজি বিভাগের অভিজ্ঞ প্রশিক্ষক প্রয়োজন। ব্যান্ড স্কোর ৭.৫ অর্জনে সহায়তা করতে হবে।',
    postedDateBn: '২৬ অক্টোবর ২০২৬',
    applicantsCount: 5,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9108',
    titleBn: 'অটিজম ও স্পেশাল চাইল্ড আর্লি লার্নিং কেয়ার',
    category: 'special_child',
    classGradeBn: 'স্পেশাল কেয়ার (বয়স ৮ বছর)',
    subjectsBn: ['স্পিচ থেরাপি বেসিক', 'আচরণগত শিক্ষা', 'হস্তলিখন ও বর্ণপরিচয়'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'উত্তরা',
    areaBn: 'উত্তরা সেক্টর ১১',
    daysPerWeek: 4,
    salaryBn: '১৫,০০০ টাকা/মাস',
    salaryAmount: 15000,
    genderPreferenceBn: 'মহিলা টিউটর আবশ্যক',
    tutorRequirementBn: 'স্পেশাল এডুকেশন বা চাইল্ড ডেভেলপমেন্টে প্রশিক্ষণপ্রাপ্ত সহনশীল ও যত্নবান শিক্ষিকা অগ্রাধিকার পাবেন।',
    postedDateBn: '২৭ অক্টোবর ২০২৬',
    applicantsCount: 3,
    status: 'open',
    escrowProtected: true,
  },
];

export const VERIFIED_TUTORS: VerifiedTutor[] = [
  {
    id: 'TUT-401',
    nameBn: 'তানভীর হাসান সৌরভ',
    initialsBn: 'তা',
    accentBg: 'bg-emerald-800 text-emerald-100 border-emerald-600',
    institutionBn: 'বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (BUET)',
    departmentBn: 'ইলেকট্রিক্যাল অ্যান্ড ইলেকট্রনিক ইঞ্জিনিয়ারিং (EEE)',
    degreeLevelBn: 'স্নাতক (৪র্থ বর্ষ)',
    sscBackgroundBn: 'নটর ডেম কলেজ, ঢাকা (জিপিএ ৫.০০)',
    hscBackgroundBn: 'নটর ডেম কলেজ, ঢাকা (জিপিএ ৫.০০)',
    preferredCategories: ['bangla_medium', 'english_version', 'admission'],
    preferredSubjects: ['পদার্থবিজ্ঞান', 'উচ্চতর গণিত', 'আইসিটি'],
    preferredLocations: ['ধানমন্ডি', 'লালমাটিয়া', 'মোহাম্মদপুর', 'ফার্মগেট'],
    experienceYearsBn: '৪+ বছর',
    rating: 4.95,
    totalReviews: 48,
    tuitionsCompleted: 26,
    expectedSalaryBn: '৯,০০০ - ১২,০০০ টাকা/মাস',
    verificationStatus: {
      nidVerified: true,
      academicIdVerified: true,
      backgroundChecked: true,
    },
  },
  {
    id: 'TUT-402',
    nameBn: 'নুসরাত জাহান মিম',
    initialsBn: 'নু',
    accentBg: 'bg-blue-900 text-blue-100 border-blue-700',
    institutionBn: 'ঢাকা মেডিকেল কলেজ (DMC)',
    departmentBn: 'এমবিবিএস (৪র্থ বর্ষ)',
    degreeLevelBn: 'মেডিকেল শিক্ষার্থী',
    sscBackgroundBn: 'ভিকারুননিসা নূন স্কুল অ্যান্ড কলেজ (জিপিএ ৫.০০)',
    hscBackgroundBn: 'ভিকারুননিসা নূন কলেজ (জিপিএ ৫.০০)',
    preferredCategories: ['bangla_medium', 'english_version'],
    preferredSubjects: ['জীববিজ্ঞান', 'রসায়ন', 'সাধারণ বিজ্ঞান'],
    preferredLocations: ['উত্তরা', 'মিরপুর', 'খিলগাঁও', 'বসুন্ধরা'],
    experienceYearsBn: '৩+ বছর',
    rating: 4.9,
    totalReviews: 34,
    tuitionsCompleted: 19,
    expectedSalaryBn: '৮,৫০০ - ১১,০০০ টাকা/মাস',
    verificationStatus: {
      nidVerified: true,
      academicIdVerified: true,
      backgroundChecked: true,
    },
  },
  {
    id: 'TUT-403',
    nameBn: 'সায়মন সাদিক',
    initialsBn: 'সা',
    accentBg: 'bg-amber-800 text-amber-100 border-amber-600',
    institutionBn: 'ঢাকা বিশ্ববিদ্যালয় (DU)',
    departmentBn: 'ফলিত গণিত ও পরিসংখ্যান',
    degreeLevelBn: 'স্নাতকোত্তর (মাস্টার্স)',
    sscBackgroundBn: 'রাজশাহী কলেজিয়েট স্কুল (জিপিএ ৫.০০)',
    hscBackgroundBn: 'রাজশাহী কলেজ (জিপিএ ৫.০০)',
    preferredCategories: ['bangla_medium', 'english_medium'],
    preferredSubjects: ['সাধারণ গণিত', 'উচ্চতর গণিত', 'পরিসংখ্যান'],
    preferredLocations: ['ধানমন্ডি', 'আজিমপুর', 'শান্তিনগর', 'অনলাইন'],
    experienceYearsBn: '৫+ বছর',
    rating: 5.0,
    totalReviews: 62,
    tuitionsCompleted: 41,
    expectedSalaryBn: '৮,০০০ - ১০,৫০০ টাকা/মাস',
    verificationStatus: {
      nidVerified: true,
      academicIdVerified: true,
      backgroundChecked: true,
    },
  },
  {
    id: 'TUT-404',
    nameBn: 'ফাতিহা তাসনিম',
    initialsBn: 'ফা',
    accentBg: 'bg-slate-800 text-slate-100 border-slate-600',
    institutionBn: 'নর্থ সাউথ বিশ্ববিদ্যালয় (NSU)',
    departmentBn: 'বিবিএ (ফাইন্যান্স ও ইকোনমিক্স)',
    degreeLevelBn: 'স্নাতক (শেষ বর্ষ)',
    sscBackgroundBn: 'সেন্ট ফ্রান্সিস জেভিয়ার্স গ্রিন হেরাল্ড (O-Level)',
    hscBackgroundBn: 'মাস্টারমাইন্ড স্কুল (A-Level)',
    preferredCategories: ['english_medium', 'arts_lang'],
    preferredSubjects: ['Economics', 'Business Studies', 'Spoken English'],
    preferredLocations: ['গুলশান', 'বনানী', 'বারিধারা', 'বসুন্ধরা'],
    experienceYearsBn: '৩+ বছর',
    rating: 4.85,
    totalReviews: 29,
    tuitionsCompleted: 15,
    expectedSalaryBn: '১০,০০০ - ১৫,০০০ টাকা/মাস',
    verificationStatus: {
      nidVerified: true,
      academicIdVerified: true,
      backgroundChecked: true,
    },
  },
];

export const SALARY_BENCHMARKS: TuitionSalaryFormula[] = [
  // Dhaka - Bangla Medium
  { district: 'ঢাকা', medium: 'বাংলা মাধ্যম', classGroup: 'primary', daysPerWeek: 3, minSalary: 4500, maxSalary: 6000 },
  { district: 'ঢাকা', medium: 'বাংলা মাধ্যম', classGroup: 'lower_secondary', daysPerWeek: 3, minSalary: 6000, maxSalary: 8000 },
  { district: 'ঢাকা', medium: 'বাংলা মাধ্যম', classGroup: 'secondary_ssc', daysPerWeek: 3, minSalary: 7500, maxSalary: 10000 },
  { district: 'ঢাকা', medium: 'বাংলা মাধ্যম', classGroup: 'higher_hsc', daysPerWeek: 3, minSalary: 9000, maxSalary: 12000 },
  { district: 'ঢাকা', medium: 'বাংলা মাধ্যম', classGroup: 'admission', daysPerWeek: 3, minSalary: 10000, maxSalary: 15000 },

  // Dhaka - English Version
  { district: 'ঢাকা', medium: 'ইংলিশ ভার্সন', classGroup: 'primary', daysPerWeek: 3, minSalary: 6000, maxSalary: 8000 },
  { district: 'ঢাকা', medium: 'ইংলিশ ভার্সন', classGroup: 'lower_secondary', daysPerWeek: 3, minSalary: 7500, maxSalary: 10000 },
  { district: 'ঢাকা', medium: 'ইংলিশ ভার্সন', classGroup: 'secondary_ssc', daysPerWeek: 3, minSalary: 9000, maxSalary: 12500 },
  { district: 'ঢাকা', medium: 'ইংলিশ ভার্সন', classGroup: 'higher_hsc', daysPerWeek: 3, minSalary: 11000, maxSalary: 15000 },

  // Dhaka - English Medium
  { district: 'ঢাকা', medium: 'ইংলিশ মিডিয়াম', classGroup: 'primary', daysPerWeek: 3, minSalary: 8000, maxSalary: 11000 },
  { district: 'ঢাকা', medium: 'ইংলিশ মিডিয়াম', classGroup: 'secondary_ssc', daysPerWeek: 3, minSalary: 12000, maxSalary: 16000 },
  { district: 'ঢাকা', medium: 'ইংলিশ মিডিয়াম', classGroup: 'higher_hsc', daysPerWeek: 3, minSalary: 15000, maxSalary: 22000 },

  // Outside Dhaka (Chittagong, Rajshahi, etc.)
  { district: 'অন্যান্য জেলা', medium: 'বাংলা মাধ্যম', classGroup: 'primary', daysPerWeek: 3, minSalary: 3500, maxSalary: 5000 },
  { district: 'অন্যান্য জেলা', medium: 'বাংলা মাধ্যম', classGroup: 'secondary_ssc', daysPerWeek: 3, minSalary: 5500, maxSalary: 7500 },
  { district: 'অন্যান্য জেলা', medium: 'বাংলা মাধ্যম', classGroup: 'higher_hsc', daysPerWeek: 3, minSalary: 7000, maxSalary: 9500 },
];

export const TUITION_FAQS: TuitionFAQItem[] = [
  {
    id: 'faq-g1',
    category: 'guardian',
    questionBn: 'অভিভাবক হিসেবে টিউটর রিকোয়ারমেন্ট দেওয়ার পর কী ঘটে?',
    answerBn: 'আপনার রিকোয়ারমেন্ট জমা দেওয়ার ২৪ থেকে ৪৮ ঘণ্টার মধ্যে আমাদের অ্যালগরিদম ও অ্যাকাডেমিক টিম আপনার চাহিদামাফিক ৩ থেকে ৫ জন যাচাইকৃত শীর্ষ শিক্ষকের প্রোফাইল পাঠায়। আপনি তাদের শিক্ষাগত যোগ্যতা দেখে পছন্দের শিক্ষককে বাছাই করতে পারেন।',
  },
  {
    id: 'faq-g2',
    category: 'guardian',
    questionBn: '২ দিনের ফ্রি ট্রায়াল ক্লাসের নিয়ম কী?',
    answerBn: 'বাছাইকৃত শিক্ষক প্রথমে ২ দিন বিনামূল্যে ট্রায়াল ক্লাস করাবেন। যদি শিক্ষক ও শিক্ষার্থীর বোঝাপড়া শতভাগ সন্তোষজনক হয়, কেবল তখনই আপনি নিয়মিত টিউশন কনফার্ম করবেন। সন্তুষ্ট না হলে কোনো ফি ছাড়াই বিকল্প শিক্ষক নেওয়া যাবে।',
  },
  {
    id: 'faq-g3',
    category: 'guardian',
    questionBn: 'অভিভাবককে কি কোনো অগ্রিম রেজিস্ট্রেশন ফি দিতে হবে?',
    answerBn: 'একেবারেই না। অগ্রযাত্রায় শিক্ষক খোঁজা ও ট্রায়াল নেওয়া সম্পূর্ণ বিনামূল্যে। অভিভাবকের কাছ থেকে কোনো প্রকার অগ্রিম কমিশন বা হিডেন চার্জ নেওয়া হয় না।',
  },
  {
    id: 'faq-t1',
    category: 'tutor',
    questionBn: 'একজন শিক্ষক কীভাবে অগ্রযাত্রায় ভেরিফায়েড টিউটর হতে পারেন?',
    answerBn: 'প্রোফাইল তৈরি করে আপনার জাতীয় পরিচয়পত্র (NID) এবং বিশ্ববিদ্যালয়ের স্টুডেন্ট আইডি কার্ড বা ডিগ্রি সনদের কপি আপলোড করতে হবে। আমাদের ভেরিফিকেশন টিম উভয় নথি যাচাই শেষে আপনার অ্যাকাউন্টে ভেরিফায়েড ব্যাজ প্রদান করবে।',
  },
  {
    id: 'faq-t2',
    category: 'tutor',
    questionBn: 'টিউশনের মাসিক পারিশ্রমিক পাওয়ার সুরক্ষা কী?',
    answerBn: 'আমরা সুরক্ষিত এসক্রো মাইলস্টোন সিস্টেম সমর্থন করি, যেখানে মাসের শুরুতে টিউশন ফি অভিভাবক প্ল্যাটফর্মে নিরাপদ জমা রাখেন এবং মাস শেষে ক্লাস সফলভাবে শেষ হলে শিক্ষককে তা সরাসরি ট্রান্সফার করা হয়।',
  },
];
