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
  nameEn?: string;
  taglineBn: string;
  taglineEn?: string;
  iconName: 'BookOpen' | 'Globe' | 'GraduationCap' | 'Languages' | 'Palette' | 'HeartHandshake' | 'Atom' | 'Award';
  jobsCount: number;
}

export interface TuitionJob {
  id: string; // e.g. "TUI-9104"
  titleBn: string;
  titleEn?: string;
  category: 'bangla_medium' | 'english_version' | 'english_medium' | 'religious' | 'admission' | 'arts_lang' | 'special_child';
  classGradeBn: string;
  classGradeEn?: string;
  subjectsBn: string[];
  subjectsEn?: string[];
  mode: 'হোম টিউশন' | 'অনলাইন টিউশন' | 'গ্রুপ ব্যাচ';
  modeEn?: 'Home Tuition' | 'Online Tuition' | 'Group Batch';
  district: string;
  districtEn?: string;
  thana: string;
  thanaEn?: string;
  areaBn: string;
  areaEn?: string;
  daysPerWeek: number;
  salaryBn: string;
  salaryEn?: string;
  salaryAmount: number;
  genderPreferenceBn: 'পুরুষ টিউটর আবশ্যক' | 'মহিলা টিউটর আবশ্যক' | 'যেকোনো অভিজ্ঞ টিউটর';
  genderPreferenceEn?: string;
  tutorRequirementBn: string;
  tutorRequirementEn?: string;
  postedDateBn: string;
  postedDateEn?: string;
  applicantsCount: number;
  status: 'open' | 'shortlisting' | 'confirmed';
  escrowProtected: boolean;
}

export interface VerifiedTutor {
  id: string;
  nameBn: string;
  nameEn?: string;
  initialsBn: string;
  initialsEn?: string;
  accentBg: string;
  institutionBn: string;
  institutionEn?: string;
  departmentBn: string;
  departmentEn?: string;
  degreeLevelBn: string;
  degreeLevelEn?: string;
  sscBackgroundBn: string;
  sscBackgroundEn?: string;
  hscBackgroundBn: string;
  hscBackgroundEn?: string;
  preferredCategories: string[];
  preferredSubjects: string[];
  preferredSubjectsEn?: string[];
  preferredLocations: string[];
  preferredLocationsEn?: string[];
  experienceYearsBn: string;
  experienceYearsEn?: string;
  rating: number;
  totalReviews: number;
  tuitionsCompleted: number;
  expectedSalaryBn: string;
  expectedSalaryEn?: string;
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
  questionEn?: string;
  answerBn: string;
  answerEn?: string;
  category: 'guardian' | 'tutor';
}

export const TUITION_CATEGORIES: TuitionCategoryInfo[] = [
  {
    id: 'all',
    nameBn: 'সকল ক্যাটাগরি',
    nameEn: 'All Categories',
    taglineBn: 'সারাদেশের সকল টিউশন ও টিউটর',
    taglineEn: 'All tuitions & tutors nationwide',
    iconName: 'GraduationCap',
    jobsCount: 1420,
  },
  {
    id: 'bangla_medium',
    nameBn: 'বাংলা মাধ্যম',
    nameEn: 'Bangla Medium',
    taglineBn: 'শ্রেণি ১-১২, এসএসসি ও এইচএসসি বোর্ড পাঠ্যক্রম',
    taglineEn: 'Class 1-12, SSC & HSC board curriculum',
    iconName: 'BookOpen',
    jobsCount: 680,
  },
  {
    id: 'english_version',
    nameBn: 'ইংলিশ ভার্সন',
    nameEn: 'English Version',
    taglineBn: 'এনসিটিবি পাঠ্যক্রমের ইংরেজি সংস্করণ',
    taglineEn: 'English version of NCTB curriculum',
    iconName: 'Globe',
    jobsCount: 340,
  },
  {
    id: 'english_medium',
    nameBn: 'ইংলিশ মিডিয়াম',
    nameEn: 'English Medium',
    taglineBn: 'ক্যামব্রিজ ও এডেক্সেল ও/এ লেভেল কারিকুলাম',
    taglineEn: 'Cambridge & Edexcel O/A Level curricula',
    iconName: 'Languages',
    jobsCount: 195,
  },
  {
    id: 'religious',
    nameBn: 'ধর্মীয় ও কুরআন শিক্ষা',
    nameEn: 'Religious & Quran',
    taglineBn: 'সহীহ কুরআন তিলাওয়াত, তাজবীদ ও আরবি শিক্ষা',
    taglineEn: 'Authentic Quran recitation, Tajweed & Arabic',
    iconName: 'Award',
    jobsCount: 85,
  },
  {
    id: 'admission',
    nameBn: 'ভর্তি পরীক্ষা প্রস্তুতি',
    nameEn: 'Admission Prep',
    taglineBn: 'বুয়েট, মেডিকেল, ঢাবি ক/খ/গ ইউনিট স্পেশাল',
    taglineEn: 'BUET, Medical, DU A/B/C units special',
    iconName: 'Atom',
    jobsCount: 72,
  },
  {
    id: 'arts_lang',
    nameBn: 'ভাষা ও স্কিলস',
    nameEn: 'Language & Skills',
    taglineBn: 'স্পোকেন ইংলিশ, আইইএলটিএস, ড্রয়িং ও মিউজিক',
    taglineEn: 'Spoken English, IELTS, drawing & music',
    iconName: 'Palette',
    jobsCount: 48,
  },
  {
    id: 'special_child',
    nameBn: 'স্পেশাল চাইল্ড কেয়ার',
    nameEn: 'Special Child Care',
    taglineBn: 'অটিজম, এডিএইচডি ও ব্যক্তিগত বিশেষ পরিচর্যা',
    taglineEn: 'Autism, ADHD & personalized special care',
    iconName: 'HeartHandshake',
    jobsCount: 24,
  },
];

export const TUITION_JOBS: TuitionJob[] = [
  {
    id: 'TUI-9101',
    titleBn: '১০ম শ্রেণির পদার্থবিজ্ঞান ও উচ্চতর গণিত টিউশন',
    titleEn: 'Class 10 Physics & Higher Math Tuition',
    category: 'bangla_medium',
    classGradeBn: '১০ম শ্রেণি (এসএসসি ২০২৭)',
    classGradeEn: 'Class 10 (SSC 2027)',
    subjectsBn: ['পদার্থবিজ্ঞান', 'উচ্চতর গণিত', 'রসায়ন'],
    subjectsEn: ['Physics', 'Higher Math', 'Chemistry'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'ধানমন্ডি',
    areaBn: 'ঢাকা, ধানমন্ডি (রোড ৮/এ)',
    areaEn: 'Dhaka, Dhanmondi (Road 8/A)',
    daysPerWeek: 3,
    salaryBn: '৮,০০০ - ১০,০০০ টাকা/মাস',
    salaryEn: 'BDT 8,000 - 10,000/Month',
    salaryAmount: 9000,
    genderPreferenceBn: 'পুরুষ টিউটর আবশ্যক',
    genderPreferenceEn: 'Male Tutor Required',
    tutorRequirementBn: 'বুয়েট (ECE) বা ঢাকা বিশ্ববিদ্যালয়ের নিয়মিত শিক্ষার্থী অগ্রাধিকার পাবেন। টেস্ট পেপার সমাধানে পারদর্শী হতে হবে।',
    tutorRequirementEn: 'BUET (ECE) or Dhaka University regular students will get preference. Must be skilled in test paper problem solving.',
    postedDateBn: '২৪ অক্টোবর ২০২৬',
    postedDateEn: '24 October 2026',
    applicantsCount: 4,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9102',
    titleBn: 'এইচএসসি ১ম বর্ষের কেমিস্ট্রি ও বায়োলজি টিউশন',
    titleEn: 'HSC 1st Year Chemistry & Biology Tuition',
    category: 'english_version',
    classGradeBn: 'একাদশ শ্রেণি (এইচএসসি ২০২৭)',
    classGradeEn: 'Class 11 (HSC 2027)',
    subjectsBn: ['রসায়ন ১ম পত্র', 'জীববিজ্ঞান ১ম পত্র'],
    subjectsEn: ['Chemistry 1st Paper', 'Biology 1st Paper'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'উত্তরা',
    areaBn: 'উত্তরা সেক্টর ৭, রবীন্দ্র সরণি',
    areaEn: 'Uttara Sector 7, Rabindra Sarani',
    daysPerWeek: 3,
    salaryBn: '১০,০০০ - ১২,০০০ টাকা/মাস',
    salaryEn: 'BDT 10,000 - 12,000/Month',
    salaryAmount: 11000,
    genderPreferenceBn: 'মহিলা টিউটর আবশ্যক',
    genderPreferenceEn: 'Female Tutor Required',
    tutorRequirementBn: 'মেডিকেল কলেজ বা ঢাবি বায়োকেমিস্ট্রির অভিজ্ঞ মহিলা টিউটর প্রয়োজন। শিক্ষার্থীকে কনসেপচুয়াল ধারণা বুঝিয়ে পড়াতে হবে।',
    tutorRequirementEn: 'Experienced female tutor from Medical College or DU Biochemistry required. Must teach with strong conceptual foundation.',
    postedDateBn: '২৫ অক্টোবর ২০২৬',
    postedDateEn: '25 October 2026',
    applicantsCount: 6,
    status: 'shortlisting',
    escrowProtected: true,
  },
  {
    id: 'TUI-9103',
    titleBn: 'ও-লেভেল ফিজিক্স ও কেমব্রিজ ম্যাথমেটিক্স টিউশন',
    titleEn: 'O-Level Physics & Cambridge Mathematics Tuition',
    category: 'english_medium',
    classGradeBn: 'O-Level (Class 10)',
    classGradeEn: 'O-Level (Class 10)',
    subjectsBn: ['Physics (5054)', 'Mathematics (4024)'],
    subjectsEn: ['Physics (5054)', 'Mathematics (4024)'],
    mode: 'অনলাইন টিউশন',
    district: 'ঢাকা',
    thana: 'গুলশান',
    areaBn: 'গুলশান ২ (অনলাইন জুম ক্লাস)',
    areaEn: 'Gulshan 2 (Online Zoom Class)',
    daysPerWeek: 4,
    salaryBn: '১২,০০০ - ১৫,০০০ টাকা/মাস',
    salaryEn: 'BDT 12,000 - 15,000/Month',
    salaryAmount: 13500,
    genderPreferenceBn: 'যেকোনো অভিজ্ঞ টিউটর',
    genderPreferenceEn: 'Any Experienced Tutor',
    tutorRequirementBn: 'ক্যামব্রিজ পাঠ্যক্রমে ও/এ লেভেল উত্তীর্ণ এবং বিগত ২+ বছর ইংলিশ মিডিয়াম পড়ানোর বাস্তব অভিজ্ঞতা থাকতে হবে।',
    tutorRequirementEn: 'Must have passed O/A Level under Cambridge curriculum with 2+ years of real English medium tutoring experience.',
    postedDateBn: '২৫ অক্টোবর ২০২৬',
    postedDateEn: '25 October 2026',
    applicantsCount: 3,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9104',
    titleBn: '৮ম শ্রেণির বিজ্ঞান, গণিত ও আইসিটি টিউশন',
    titleEn: 'Class 8 Science, Math & ICT Tuition',
    category: 'bangla_medium',
    classGradeBn: '৮ম শ্রেণি (নতুন শিক্ষাক্রম)',
    classGradeEn: 'Class 8 (New Curriculum)',
    subjectsBn: ['বিজ্ঞান', 'গণিত', 'তথ্যপ্রযুক্তি'],
    subjectsEn: ['Science', 'Mathematics', 'ICT'],
    mode: 'হোম টিউশন',
    district: 'চট্টগ্রাম',
    thana: 'পাঁচলাইশ',
    areaBn: 'পাঁচলাইশ আবাসিক এলাকা',
    areaEn: 'Panchlaish Residential Area',
    daysPerWeek: 3,
    salaryBn: '৭,০০০ - ৮,৫০০ টাকা/মাস',
    salaryEn: 'BDT 7,000 - 8,500/Month',
    salaryAmount: 7500,
    genderPreferenceBn: 'যেকোনো অভিজ্ঞ টিউটর',
    genderPreferenceEn: 'Any Experienced Tutor',
    tutorRequirementBn: 'চট্টগ্রাম বিশ্ববিদ্যালয় বা চুয়েটের দায়িত্বশীল শিক্ষার্থী। নতুন শিক্ষাক্রমের অ্যাক্টিভিটি ভিত্তিক পড়াশোনায় দক্ষ।',
    tutorRequirementEn: 'Responsible student from Chittagong University or CUET. Skilled in activity-based learning under the new curriculum.',
    postedDateBn: '২৩ অক্টোবর ২০২৬',
    postedDateEn: '23 October 2026',
    applicantsCount: 5,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9105',
    titleBn: 'বুয়েট ভর্তি প্রস্তুতি গণিত স্পেশাল টিউশন',
    titleEn: 'BUET Admission Prep Math Special Tuition',
    category: 'admission',
    classGradeBn: 'এডমিশন পরীক্ষার্থী (২০২৬)',
    classGradeEn: 'Admission Candidate (2026)',
    subjectsBn: ['ক্যালকুলাস', 'মেকানিক্স', 'ভেক্টর গণিত'],
    subjectsEn: ['Calculus', 'Mechanics', 'Vector Math'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'মিরপুর',
    areaBn: 'মিরপুর ডিওএইচএস',
    areaEn: 'Mirpur DOHS',
    daysPerWeek: 2,
    salaryBn: '১০,০০০ টাকা/মাস',
    salaryEn: 'BDT 10,000/Month',
    salaryAmount: 10000,
    genderPreferenceBn: 'পুরুষ টিউটর আবশ্যক',
    genderPreferenceEn: 'Male Tutor Required',
    tutorRequirementBn: 'শুধুমাত্র বুয়েটের ৩য় বা ৪র্থ বর্ষের প্রকৌশল বিভাগের শিক্ষার্থী যাদের এডমিশন পড়ানোর পূর্ব অভিজ্ঞতা আছে।',
    tutorRequirementEn: 'Only 3rd or 4th year BUET engineering students with prior admission tutoring experience.',
    postedDateBn: '২৬ অক্টোবর ২০২৬',
    postedDateEn: '26 October 2026',
    applicantsCount: 2,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9106',
    titleBn: 'সহীহ কুরআন ও তাজবীদ শিক্ষা (শিশুদের জন্য)',
    titleEn: 'Authentic Quran & Tajweed Learning (For Kids)',
    category: 'religious',
    classGradeBn: '৪র্থ শ্রেণি ও কেজি',
    classGradeEn: 'Class 4 & KG',
    subjectsBn: ['কুরআনুল কারীম', 'তাজবীদ', 'দৈনন্দিন দোয়া ও মাসয়ালা'],
    subjectsEn: ['Holy Quran', 'Tajweed', 'Daily Dua & Masail'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'মোহাম্মদপুর',
    areaBn: 'মোহাম্মদপুর জাপান গার্ডেন সিটি',
    areaEn: 'Mohammadpur Japan Garden City',
    daysPerWeek: 4,
    salaryBn: '৬,০০০ - ৭,৫০০ টাকা/মাস',
    salaryEn: 'BDT 6,000 - 7,500/Month',
    salaryAmount: 6500,
    genderPreferenceBn: 'মহিলা টিউটর আবশ্যক',
    genderPreferenceEn: 'Female Tutor Required',
    tutorRequirementBn: 'হাফেজা বা কওমি/আলিয়া মাদরাসা ব্যাকগ্রাউন্ডের অভিজ্ঞ শিক্ষিকা। ধৈর্যশীল আচরণ আবশ্যক।',
    tutorRequirementEn: 'Hafiza or experienced teacher with Qawmi/Alia madrasah background. Patient behavior essential.',
    postedDateBn: '২১ অক্টোবর ২০২৬',
    postedDateEn: '21 October 2026',
    applicantsCount: 7,
    status: 'confirmed',
    escrowProtected: true,
  },
  {
    id: 'TUI-9107',
    titleBn: 'আইইএলটিএস (IELTS) স্পিকিং ও রাইটিং মেন্টরশিপ',
    titleEn: 'IELTS Speaking & Writing Mentorship',
    category: 'arts_lang',
    classGradeBn: 'উচ্চশিক্ষা ও স্কিলস শিক্ষার্থী',
    classGradeEn: 'Higher Ed & Skills Student',
    subjectsBn: ['IELTS Academic', 'Spoken English', 'Essay Writing'],
    subjectsEn: ['IELTS Academic', 'Spoken English', 'Essay Writing'],
    mode: 'অনলাইন টিউশন',
    district: 'ঢাকা',
    thana: 'বনানী',
    areaBn: 'বনানী (অনলাইন গুগল মিট সেশন)',
    areaEn: 'Banani (Online Google Meet Session)',
    daysPerWeek: 3,
    salaryBn: '১২,০০০ - ১৪,০০০ টাকা/মাস',
    salaryEn: 'BDT 12,000 - 14,000/Month',
    salaryAmount: 13000,
    genderPreferenceBn: 'যেকোনো অভিজ্ঞ টিউটর',
    genderPreferenceEn: 'Any Experienced Tutor',
    tutorRequirementBn: 'আইইএলটিএস স্কোর ৮.০+ অথবা ঢাবি ইংরেজি বিভাগের অভিজ্ঞ প্রশিক্ষক প্রয়োজন। ব্যান্ড স্কোর ৭.৫ অর্জনে সহায়তা করতে হবে।',
    tutorRequirementEn: 'IELTS score 8.0+ or experienced educator from DU English Department required. Goal: achieve band 7.5.',
    postedDateBn: '২৬ অক্টোবর ২০২৬',
    postedDateEn: '26 October 2026',
    applicantsCount: 5,
    status: 'open',
    escrowProtected: true,
  },
  {
    id: 'TUI-9108',
    titleBn: 'অটিজম ও স্পেশাল চাইল্ড আর্লি লার্নিং কেয়ার',
    titleEn: 'Autism & Special Child Early Learning Care',
    category: 'special_child',
    classGradeBn: 'স্পেশাল কেয়ার (বয়স ৮ বছর)',
    classGradeEn: 'Special Care (Age 8)',
    subjectsBn: ['স্পিচ থেরাপি বেসিক', 'আচরণগত শিক্ষা', 'হস্তলিখন ও বর্ণপরিচয়'],
    subjectsEn: ['Speech Therapy Basics', 'Behavioral Education', 'Handwriting & Phonics'],
    mode: 'হোম টিউশন',
    district: 'ঢাকা',
    thana: 'উত্তরা',
    areaBn: 'উত্তরা সেক্টর ১১',
    areaEn: 'Uttara Sector 11',
    daysPerWeek: 4,
    salaryBn: '১৫,০০০ টাকা/মাস',
    salaryEn: 'BDT 15,000/Month',
    salaryAmount: 15000,
    genderPreferenceBn: 'মহিলা টিউটর আবশ্যক',
    genderPreferenceEn: 'Female Tutor Required',
    tutorRequirementBn: 'স্পেশাল এডুকেশন বা চাইল্ড ডেভেলপমেন্টে প্রশিক্ষণপ্রাপ্ত সহনশীল ও যত্নবান শিক্ষিকা অগ্রাধিকার পাবেন।',
    tutorRequirementEn: 'Trained, patient and attentive teacher in Special Education or Child Development preferred.',
    postedDateBn: '২৭ অক্টোবর ২০২৬',
    postedDateEn: '27 October 2026',
    applicantsCount: 3,
    status: 'open',
    escrowProtected: true,
  },
];

export const VERIFIED_TUTORS: VerifiedTutor[] = [
  {
    id: 'TUT-401',
    nameBn: 'তানভীর হাসান সৌরভ',
    nameEn: 'Tanvir Hasan Sourav',
    initialsBn: 'তা',
    initialsEn: 'TH',
    accentBg: 'bg-emerald-800 text-emerald-100 border-emerald-600',
    institutionBn: 'বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (BUET)',
    institutionEn: 'Bangladesh University of Engineering and Technology (BUET)',
    departmentBn: 'ইলেকট্রিক্যাল অ্যান্ড ইলেকট্রনিক ইঞ্জিনিয়ারিং (EEE)',
    departmentEn: 'Electrical and Electronic Engineering (EEE)',
    degreeLevelBn: 'স্নাতক (৪র্থ বর্ষ)',
    degreeLevelEn: 'Undergraduate (4th Year)',
    sscBackgroundBn: 'নটর ডেম কলেজ, ঢাকা (জিপিএ ৫.০০)',
    hscBackgroundBn: 'নটর ডেম কলেজ, ঢাকা (জিপিএ ৫.০০)',
    preferredCategories: ['bangla_medium', 'english_version', 'admission'],
    preferredSubjects: ['পদার্থবিজ্ঞান', 'উচ্চতর গণিত', 'আইসিটি'],
    preferredSubjectsEn: ['Physics', 'Higher Math', 'ICT'],
    preferredLocations: ['ধানমন্ডি', 'লালমাটিয়া', 'মোহাম্মদপুর', 'ফার্মগেট'],
    preferredLocationsEn: ['Dhanmondi', 'Lalmatia', 'Mohammadpur', 'Farmgate'],
    experienceYearsBn: '৪+ বছর',
    experienceYearsEn: '4+ Years',
    rating: 4.95,
    totalReviews: 48,
    tuitionsCompleted: 26,
    expectedSalaryBn: '৯,০০০ - ১২,০০০ টাকা/মাস',
    expectedSalaryEn: 'BDT 9,000 - 12,000/Month',
    verificationStatus: {
      nidVerified: true,
      academicIdVerified: true,
      backgroundChecked: true,
    },
  },
  {
    id: 'TUT-402',
    nameBn: 'নুসরাত জাহান মিম',
    nameEn: 'Nusrat Jahan Mim',
    initialsBn: 'নু',
    initialsEn: 'NJ',
    accentBg: 'bg-blue-900 text-blue-100 border-blue-700',
    institutionBn: 'ঢাকা মেডিকেল কলেজ (DMC)',
    institutionEn: 'Dhaka Medical College (DMC)',
    departmentBn: 'এমবিবিএস (৪র্থ বর্ষ)',
    departmentEn: 'MBBS (4th Year)',
    degreeLevelBn: 'মেডিকেল শিক্ষার্থী',
    degreeLevelEn: 'Medical Student',
    sscBackgroundBn: 'ভিকারুননিসা নূন স্কুল অ্যান্ড কলেজ (জিপিএ ৫.০০)',
    hscBackgroundBn: 'ভিকারুননিসা নূন কলেজ (জিপিএ ৫.০০)',
    preferredCategories: ['bangla_medium', 'english_version'],
    preferredSubjects: ['জীববিজ্ঞান', 'রসায়ন', 'সাধারণ বিজ্ঞান'],
    preferredSubjectsEn: ['Biology', 'Chemistry', 'General Science'],
    preferredLocations: ['উত্তরা', 'মিরপুর', 'খিলগাঁও', 'বসুন্ধরা'],
    preferredLocationsEn: ['Uttara', 'Mirpur', 'Khilgaon', 'Bashundhara'],
    experienceYearsBn: '৩+ বছর',
    experienceYearsEn: '3+ Years',
    rating: 4.9,
    totalReviews: 34,
    tuitionsCompleted: 19,
    expectedSalaryBn: '৮,৫০০ - ১১,০০০ টাকা/মাস',
    expectedSalaryEn: 'BDT 8,500 - 11,000/Month',
    verificationStatus: {
      nidVerified: true,
      academicIdVerified: true,
      backgroundChecked: true,
    },
  },
  {
    id: 'TUT-403',
    nameBn: 'সায়মন সাদিক',
    nameEn: 'Saymon Sadik',
    initialsBn: 'সা',
    initialsEn: 'SS',
    accentBg: 'bg-amber-800 text-amber-100 border-amber-600',
    institutionBn: 'ঢাকা বিশ্ববিদ্যালয় (DU)',
    institutionEn: 'University of Dhaka (DU)',
    departmentBn: 'ফলিত গণিত ও পরিসংখ্যান',
    departmentEn: 'Applied Mathematics & Statistics',
    degreeLevelBn: 'স্নাতকোত্তর (মাস্টার্স)',
    degreeLevelEn: 'Postgraduate (Masters)',
    sscBackgroundBn: 'রাজশাহী কলেজিয়েট স্কুল (জিপিএ ৫.০০)',
    hscBackgroundBn: 'রাজশাহী কলেজ (জিপিএ ৫.০০)',
    preferredCategories: ['bangla_medium', 'english_medium'],
    preferredSubjects: ['সাধারণ গণিত', 'উচ্চতর গণিত', 'পরিসংখ্যান'],
    preferredSubjectsEn: ['General Math', 'Higher Math', 'Statistics'],
    preferredLocations: ['ধানমন্ডি', 'আজিমপুর', 'শান্তিনগর', 'অনলাইন'],
    preferredLocationsEn: ['Dhanmondi', 'Azimpur', 'Shantinagar', 'Online'],
    experienceYearsBn: '৫+ বছর',
    experienceYearsEn: '5+ Years',
    rating: 5.0,
    totalReviews: 62,
    tuitionsCompleted: 41,
    expectedSalaryBn: '৮,০০০ - ১০,৫০০ টাকা/মাস',
    expectedSalaryEn: 'BDT 8,000 - 10,500/Month',
    verificationStatus: {
      nidVerified: true,
      academicIdVerified: true,
      backgroundChecked: true,
    },
  },
  {
    id: 'TUT-404',
    nameBn: 'ফাতিহা তাসনিম',
    nameEn: 'Fatiha Tasnim',
    initialsBn: 'ফা',
    initialsEn: 'FT',
    accentBg: 'bg-slate-800 text-slate-100 border-slate-600',
    institutionBn: 'নর্থ সাউথ বিশ্ববিদ্যালয় (NSU)',
    institutionEn: 'North South University (NSU)',
    departmentBn: 'বিবিএ (ফাইন্যান্স ও ইকোনমিক্স)',
    departmentEn: 'BBA (Finance & Economics)',
    degreeLevelBn: 'স্নাতক (শেষ বর্ষ)',
    degreeLevelEn: 'Undergraduate (Final Year)',
    sscBackgroundBn: 'সেন্ট ফ্রান্সিস জেভিয়ার্স গ্রিন হেরাল্ড (O-Level)',
    hscBackgroundBn: 'মাস্টারমাইন্ড স্কুল (A-Level)',
    preferredCategories: ['english_medium', 'arts_lang'],
    preferredSubjects: ['Economics', 'Business Studies', 'Spoken English'],
    preferredSubjectsEn: ['Economics', 'Business Studies', 'Spoken English'],
    preferredLocations: ['গুলশান', 'বনানী', 'বারিধারা', 'বসুন্ধরা'],
    preferredLocationsEn: ['Gulshan', 'Banani', 'Baridhara', 'Bashundhara'],
    experienceYearsBn: '৩+ বছর',
    experienceYearsEn: '3+ Years',
    rating: 4.85,
    totalReviews: 29,
    tuitionsCompleted: 15,
    expectedSalaryBn: '১০,০০০ - ১৫,০০০ টাকা/মাস',
    expectedSalaryEn: 'BDT 10,000 - 15,000/Month',
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
    questionEn: 'What happens after submitting a tutor requirement as a parent/guardian?',
    answerBn: 'আপনার রিকোয়ারমেন্ট জমা দেওয়ার ২৪ থেকে ৪৮ ঘণ্টার মধ্যে আমাদের অ্যালগরিদম ও অ্যাকাডেমিক টিম আপনার চাহিদামাফিক ৩ থেকে ৫ জন যাচাইকৃত শীর্ষ শিক্ষকের প্রোফাইল পাঠায়। আপনি তাদের শিক্ষাগত যোগ্যতা দেখে পছন্দের শিক্ষককে বাছাই করতে পারেন।',
    answerEn: 'Within 24 to 48 hours of submission, our matching engine recommends profiles of 3 to 5 verified top scholars. You can review their credentials and select your preferred tutor.',
  },
  {
    id: 'faq-g2',
    category: 'guardian',
    questionBn: '২ দিনের ফ্রি ট্রায়াল ক্লাসের নিয়ম কী?',
    questionEn: 'How does the 2-day free trial class work?',
    answerBn: 'বাছাইকৃত শিক্ষক প্রথমে ২ দিন বিনামূল্যে ট্রায়াল ক্লাস করাবেন। যদি শিক্ষক ও শিক্ষার্থীর বোঝাপড়া শতভাগ সন্তোষজনক হয়, কেবল তখনই আপনি নিয়মিত টিউশন কনফার্ম করবেন। সন্তুষ্ট না হলে কোনো ফি ছাড়াই বিকল্প শিক্ষক নেওয়া যাবে।',
    answerEn: 'The selected tutor conducts 2 complimentary trial sessions. If mutual satisfaction is achieved, you proceed to regular sessions. Otherwise, you may choose an alternate tutor with zero obligation.',
  },
  {
    id: 'faq-g3',
    category: 'guardian',
    questionBn: 'অভিভাবককে কি কোনো অগ্রিম রেজিস্ট্রেশন ফি দিতে হবে?',
    questionEn: 'Do guardians need to pay any upfront registration fees?',
    answerBn: 'একেবারেই না। অগ্রযাত্রায় শিক্ষক খোঁজা ও ট্রায়াল নেওয়া সম্পূর্ণ বিনামূল্যে। অভিভাবকের কাছ থেকে কোনো প্রকার অগ্রিম কমিশন বা হিডেন চার্জ নেওয়া হয় না।',
    answerEn: 'Absolutely not. Searching for tutors and conducting trial classes on Agrjatra is 100% free with zero upfront commissions or hidden charges.',
  },
  {
    id: 'faq-t1',
    category: 'tutor',
    questionBn: 'একজন শিক্ষক কীভাবে অগ্রযাত্রায় ভেরিফায়েড টিউটর হতে পারেন?',
    questionEn: 'How can an educator become a verified tutor on Agrjatra?',
    answerBn: 'প্রোফাইল তৈরি করে আপনার জাতীয় পরিচয়পত্র (NID) এবং বিশ্ববিদ্যালয়ের স্টুডেন্ট আইডি কার্ড বা ডিগ্রি সনদের কপি আপলোড করতে হবে। আমাদের ভেরিফিকেশন টিম উভয় নথি যাচাই শেষে আপনার অ্যাকাউন্টে ভেরিফায়েড ব্যাজ প্রদান করবে।',
    answerEn: 'Create a scholar profile and upload your National ID (NID) along with university student ID or degree transcript. Our verification team grants the verified badge upon manual review.',
  },
  {
    id: 'faq-t2',
    category: 'tutor',
    questionBn: 'টিউশনের মাসিক পারিশ্রমিক পাওয়ার সুরক্ষা কী?',
    questionEn: 'What safeguards exist for educators to receive their monthly remuneration?',
    answerBn: 'আমরা সুরক্ষিত এসক্রো মাইলস্টোন সিস্টেম সমর্থন করি, যেখানে মাসের শুরুতে টিউশন ফি অভিভাবক প্ল্যাটফর্মে নিরাপদ জমা রাখেন এবং মাস শেষে ক্লাস সফলভাবে শেষ হলে শিক্ষককে তা সরাসরি ট্রান্সফার করা হয়।',
    answerEn: 'We support a protected escrow milestone architecture where tuition fees are held safely at the beginning of each cycle and released directly to the educator upon completion.',
  },
];
