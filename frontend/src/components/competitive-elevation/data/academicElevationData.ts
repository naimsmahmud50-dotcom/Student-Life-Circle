/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic Elevation Data Contract & Lexicon
 * TOPIC:     10MS Reverse Engineering Competitive Integration
 * FILE:      frontend/src/components/competitive-elevation/data/academicElevationData.ts
 * STANDARDS: Zero-Emoji, Pure Lucide Icon mapping, Original Scholar Monograms (Zero External Scraped Photos),
 *            WCAG 2.2 AAA Contrast, Bengali Typography Rigor
 */

export interface AcademicSubject {
  id: string;
  nameBn: string;
  code: string;
  iconName: 'Atom' | 'FlaskConical' | 'Calculator' | 'Dna' | 'BookOpen' | 'Globe' | 'Cpu' | 'TrendingUp' | 'ShieldCheck';
}

export interface AcademicBundle {
  id: string;
  categoryId: 'hsc_27' | 'hsc_28' | 'ssc_27' | 'admission_varsity' | 'admission_med_eng' | 'bcs_preli';
  titleBn: string;
  subtitleBn: string;
  badgeBn: string;
  badgeType: 'emerald' | 'gold' | 'crimson';
  subjects: AcademicSubject[];
  deliverablesBn: string[];
  mockTestsCount: number;
  liveLecturesCount: number;
  enrolledStudentsCount: number;
  targetUrl: string;
  actionTextBn: string;
}

export interface AcademicCategory {
  id: 'hsc_27' | 'hsc_28' | 'ssc_27' | 'admission_varsity' | 'admission_med_eng' | 'bcs_preli';
  labelBn: string;
  subLabelBn: string;
  badgeBn?: string;
}

export interface AchieverProfile {
  id: string;
  nameBn: string;
  institutionBn: string;
  milestoneBn: string;
  quoteBn: string;
  batchBn: string;
  initials: string;
  accentBg: string; // Tailwind color class for monogram circle
}

export interface AcademicPillarFeature {
  id: string;
  titleBn: string;
  subtitleBn: string;
  descriptionBn: string;
  reassuranceBn: string;
  badgeBn: string;
  iconName: 'Sparkles' | 'WifiOff' | 'Trophy' | 'BookMarked' | 'Headphones' | 'Layers';
  actionUrl: string;
  actionLabelBn: string;
}

export const ACADEMIC_CATEGORIES: AcademicCategory[] = [
  {
    id: 'hsc_27',
    labelBn: 'এইচএসসি ২০২৭',
    subLabelBn: 'একাদশ-দ্বাদশ অনলাইন ব্যাচ',
    badgeBn: 'ভর্তি চলছে',
  },
  {
    id: 'hsc_28',
    labelBn: 'এইচএসসি ২০২৮',
    subLabelBn: 'নতুন শিক্ষাক্রম ব্যাচ',
    badgeBn: 'নতুন সেশন',
  },
  {
    id: 'ssc_27',
    labelBn: 'এসএসসি ২০২৭',
    subLabelBn: 'দশম শ্রেণি শেষ মুহূর্তের প্রস্তুতি',
    badgeBn: 'মডেল টেস্ট',
  },
  {
    id: 'admission_varsity',
    labelBn: 'ভার্সিটি এডমিশন',
    subLabelBn: 'ক/খ/গ ইউনিট ও গুচ্ছ',
    badgeBn: 'এডমিশন ২০২৬',
  },
  {
    id: 'admission_med_eng',
    labelBn: 'মেডিকেল ও বুয়েট',
    subLabelBn: 'ইঞ্জিনিয়ারিং স্পেশাল',
  },
  {
    id: 'bcs_preli',
    labelBn: 'বিসিএস ও ক্যারিয়ার',
    subLabelBn: 'প্রিলি ও সরকারি ব্যাংক জবস',
  },
];

export const ACADEMIC_BUNDLES: AcademicBundle[] = [
  // HSC 2027
  {
    id: 'hsc27-science-bundle',
    categoryId: 'hsc_27',
    titleBn: 'এইচএসসি ২৭ বিজ্ঞান বান্ডেল',
    subtitleBn: 'পদার্থবিজ্ঞান, রসায়ন, উচ্চতর গণিত ও জীববিজ্ঞান সম্পূর্ণ প্রস্তুতি',
    badgeBn: 'সেরা পছন্দ',
    badgeType: 'emerald',
    subjects: [
      { id: 'phy', nameBn: 'পদার্থবিজ্ঞান ১ম ও ২য়', code: 'PHY-101', iconName: 'Atom' },
      { id: 'chem', nameBn: 'রসায়ন ১ম ও ২য়', code: 'CHE-102', iconName: 'FlaskConical' },
      { id: 'math', nameBn: 'উচ্চতর গণিত ১ম ও ২য়', code: 'MTH-103', iconName: 'Calculator' },
      { id: 'bio', nameBn: 'জীববিজ্ঞান ১ম ও ২য়', code: 'BIO-104', iconName: 'Dna' },
    ],
    deliverablesBn: [
      'সাপ্তাহিক ১০টি লাইভ মাস্টারক্লাস ও ডিসকাশন',
      'অধ্যায়ভিত্তিক মুদ্রিত লেকচার শিট ও স্মার্ট নোটস',
      'আনলিমিটেড MCQ প্র্যাকটিস ও সাপ্তাহিক মডেল টেস্ট',
      '২৪ ঘণ্টা ডাউট সলভের সার্বক্ষণিক সহায়তা',
    ],
    mockTestsCount: 65,
    liveLecturesCount: 120,
    enrolledStudentsCount: 18450,
    targetUrl: '/practice',
    actionTextBn: 'সিলেবাস ও পরীক্ষা শুরু করুন',
  },
  {
    id: 'hsc27-compulsory-bundle',
    categoryId: 'hsc_27',
    titleBn: 'বাংলা, ইংরেজি ও তথ্যপ্রযুক্তি বান্ডেল',
    subtitleBn: 'সকল বিভাগের শিক্ষার্থীদের জন্য আবশ্যিক তিন বিষয়ের পূর্ণাঙ্গ কোর্স',
    badgeBn: 'আবশ্যিক প্যাক',
    badgeType: 'gold',
    subjects: [
      { id: 'bangla', nameBn: 'বাংলা ১ম ও ২য় পত্র', code: 'BAN-101', iconName: 'BookOpen' },
      { id: 'english', nameBn: 'ইংরেজি ১ম ও ২য় পত্র', code: 'ENG-102', iconName: 'Globe' },
      { id: 'ict', nameBn: 'তথ্য ও যোগাযোগ প্রযুক্তি', code: 'ICT-103', iconName: 'Cpu' },
    ],
    deliverablesBn: [
      'ব্যাকরণ, ফ্রি হ্যান্ড রাইটিং ও সৃজনশীল কৌশল',
      'বোর্ড প্রশ্ন ও শীর্ষ কলেজের মডেল টেস্ট সমাধান',
      'ক্লাস মিস হলে সংরক্ষিত আর্কাইভ থেকে রিভিশন',
    ],
    mockTestsCount: 40,
    liveLecturesCount: 80,
    enrolledStudentsCount: 14200,
    targetUrl: '/practice',
    actionTextBn: 'মডেল টেস্টে অংশ নিন',
  },

  // HSC 2028
  {
    id: 'hsc28-science-bundle',
    categoryId: 'hsc_28',
    titleBn: 'এইচএসসি ২৮ বিজ্ঞান ভিত্তি ব্যাচ',
    subtitleBn: 'নতুন শিক্ষাক্রমের আলোকে কনসেপ্ট ক্লিয়ারিং ও সাপ্তাহিক অ্যাসেসমেন্ট',
    badgeBn: 'নতুন ব্যাচ',
    badgeType: 'emerald',
    subjects: [
      { id: 'phy28', nameBn: 'পদার্থবিজ্ঞান', code: 'PHY-28', iconName: 'Atom' },
      { id: 'chem28', nameBn: 'রসায়ন', code: 'CHE-28', iconName: 'FlaskConical' },
      { id: 'math28', nameBn: 'উচ্চতর গণিত', code: 'MTH-28', iconName: 'Calculator' },
      { id: 'bio28', nameBn: 'জীববিজ্ঞান', code: 'BIO-28', iconName: 'Dna' },
    ],
    deliverablesBn: [
      'নতুন সিলেবাসের প্রতিটি অধ্যায়ের কনসেপচুয়াল ক্লাস',
      'সাপ্তাহিক হোমওয়ার্ক ও প্র্যাকটিস পেপারস',
      'জাতীয় অলিম্পিয়াডের আদলে সাপ্তাহিক কুইজ প্রতিযোগিতা',
    ],
    mockTestsCount: 50,
    liveLecturesCount: 95,
    enrolledStudentsCount: 11200,
    targetUrl: '/practice',
    actionTextBn: 'ব্যাচে যোগ দিন',
  },

  // SSC 2027
  {
    id: 'ssc27-final-prep',
    categoryId: 'ssc_27',
    titleBn: 'এসএসসি ২৭ শেষ মুহূর্তের প্রস্তুতি ও টেস্ট পেপার সমাধান',
    subtitleBn: 'বোর্ড সেরা ৭০টি স্কুলের টেস্ট পেপার প্রশ্ন ও সাজেশনের নিখুঁত সমাধান',
    badgeBn: 'পরীক্ষা স্পেশাল',
    badgeType: 'crimson',
    subjects: [
      { id: 'ssc-sci', nameBn: 'পদার্থবিজ্ঞান, রসায়ন ও জীববিজ্ঞান', code: 'SSC-SCI', iconName: 'FlaskConical' },
      { id: 'ssc-gen', nameBn: 'সাধারণ গণিত ও উচ্চতর গণিত', code: 'SSC-MTH', iconName: 'Calculator' },
      { id: 'ssc-lang', nameBn: 'বাংলা, ইংরেজি ও বাংলাদেশ বিশ্বপরিচয়', code: 'SSC-HUM', iconName: 'BookOpen' },
    ],
    deliverablesBn: [
      'শীর্ষ স্কুলের টেস্ট পরীক্ষার প্রশ্ন পর্যালোচনা',
      'নেগেটিভ মার্কিং সহ ফুল লেংথ বোর্ড স্ট্যান্ডার্ড মডেল টেস্ট',
      'পরীক্ষার হলে সময় ব্যবস্থাপনার পরীক্ষিত কৌশল',
    ],
    mockTestsCount: 75,
    liveLecturesCount: 60,
    enrolledStudentsCount: 22800,
    targetUrl: '/live-challenge',
    actionTextBn: 'টেস্ট পেপার পরীক্ষা দিন',
  },

  // Admission Varsity
  {
    id: 'admission-a-unit',
    categoryId: 'admission_varsity',
    titleBn: 'ভার্সিটি ক ইউনিট + গুচ্ছ বিজ্ঞান ভর্তি প্রোগ্রাম',
    subtitleBn: 'ঢাকা বিশ্ববিদ্যালয় ও সকল প্রযুক্তি বিশ্ববিদ্যালয়ের কনসেপ্ট ও প্রশ্নব্যাংক',
    badgeBn: 'ভর্তি পরীক্ষা',
    badgeType: 'emerald',
    subjects: [
      { id: 'adm-phy', nameBn: 'এডমিশন পদার্থবিজ্ঞান', code: 'ADM-PHY', iconName: 'Atom' },
      { id: 'adm-chem', nameBn: 'এডমিশন রসায়ন', code: 'ADM-CHE', iconName: 'FlaskConical' },
      { id: 'adm-math', nameBn: 'এডমিশন উচ্চতর গণিত', code: 'ADM-MTH', iconName: 'Calculator' },
      { id: 'adm-bio', nameBn: 'এডমিশন জীববিজ্ঞান', code: 'ADM-BIO', iconName: 'Dna' },
    ],
    deliverablesBn: [
      'বিগত ২০ বছরের ঢাকা বিশ্ববিদ্যালয় ও গুচ্ছ প্রশ্ন বিশ্লেষণ',
      'দৈনিক প্র্যাকটিস এক্সাম ও রিয়েল-টাইম জাতীয় র‍্যাঙ্কিং',
      'নেগেটিভ মার্কিং সহ রিয়েল ওএমআর সিমুলেশন',
    ],
    mockTestsCount: 90,
    liveLecturesCount: 140,
    enrolledStudentsCount: 29500,
    targetUrl: '/admission',
    actionTextBn: 'এডমিশন টেস্ট দিন',
  },

  // Engineering & Medical
  {
    id: 'admission-eng-med',
    categoryId: 'admission_med_eng',
    titleBn: 'বুয়েট ইঞ্জিনিয়ারিং ও মেডিকেল সমন্বিত স্পেশাল',
    subtitleBn: 'গাণিতিক সমস্যার গভীর বিশ্লেষণ ও মেডিকেল তথ্যমূলক প্রশ্নব্যাংক',
    badgeBn: 'মেধা নিশ্চিতকরণ',
    badgeType: 'crimson',
    subjects: [
      { id: 'eng-math', nameBn: 'বুয়েট লিখিত গণিত ও মেকানিক্স', code: 'ENG-MTH', iconName: 'Calculator' },
      { id: 'med-gk', nameBn: 'মেডিকেল বায়োলজি, কেমিস্ট্রি ও জিকে', code: 'MED-BIO', iconName: 'Dna' },
    ],
    deliverablesBn: [
      'রিটেন ও এমসিকিউ উভয় ফরম্যাটের নিবিড় মডেল টেস্ট',
      'ক্যালকুলেটর শর্টকাট ও সময় বাঁচানোর নির্ভুল টেকনিক',
      'অলিম্পিয়াড স্ট্যান্ডার্ড জটিল সমস্যার সমাধান',
    ],
    mockTestsCount: 85,
    liveLecturesCount: 110,
    enrolledStudentsCount: 16700,
    targetUrl: '/live-challenge',
    actionTextBn: 'চ্যালেঞ্জে অংশ নিন',
  },

  // BCS & Career
  {
    id: 'bcs-preli-complete',
    categoryId: 'bcs_preli',
    titleBn: '৪৭তম বিসিএস প্রিলিমিনারি পূর্ণাঙ্গ কোর্স',
    subtitleBn: '২০০ নম্বরের সিলেবাস ভিত্তিক বিষয়ভিত্তিক কুইজ ও ১০ সেট ফাইনাল মডেল টেস্ট',
    badgeBn: 'ক্যারিয়ার প্যাক',
    badgeType: 'gold',
    subjects: [
      { id: 'bcs-bng', nameBn: 'বাংলা ভাষা ও সাহিত্য', code: 'BCS-01', iconName: 'BookOpen' },
      { id: 'bcs-eng', nameBn: 'ইংরেজি ভাষা ও ব্যাকরণ', code: 'BCS-02', iconName: 'Globe' },
      { id: 'bcs-gk', nameBn: 'বাংলাদেশ ও আন্তর্জাতিক বিষয়াবলি', code: 'BCS-03', iconName: 'ShieldCheck' },
      { id: 'bcs-sci', nameBn: 'সাধারণ বিজ্ঞান ও কম্পিউটার প্রযুক্তি', code: 'BCS-04', iconName: 'Cpu' },
    ],
    deliverablesBn: [
      '১০ম থেকে ৪৬তম বিসিএস প্রিলিমিনারি সমাধান ও পর্যালোচনা',
      'নেগেটিভ ০.৫০ মার্কিং সহ রিয়েল ওএমআর টাইমার টেস্ট',
      'সাপ্তাহিক কারেন্ট অ্যাফেয়ার্স ক্যাপসুল',
    ],
    mockTestsCount: 80,
    liveLecturesCount: 100,
    enrolledStudentsCount: 21300,
    targetUrl: '/career',
    actionTextBn: 'বিসিএস মডেল টেস্ট দিন',
  },
];

export const ACADEMIC_PILLAR_FEATURES: AcademicPillarFeature[] = [
  {
    id: 'socratic-doubt-solve',
    titleBn: 'সার্বক্ষণিক ডাউট সলভ',
    subtitleBn: 'তোমার ২৪/৭ সক্রেটিক এআই স্টাডি পার্টনার',
    descriptionBn: 'পদার্থবিজ্ঞান, গণিত বা রসায়নের যেকোনো জটিল প্রশ্ন আটকে গেলে সাথে সাথে ধাপে ধাপে সমাধান ও গভীর ধারণা বুঝে নিন।',
    reassuranceBn: 'কখনোই পড়ার গতি থামবে না',
    badgeBn: '২৪x৭ সাপোর্ট',
    iconName: 'Sparkles',
    actionUrl: '/socratic',
    actionLabelBn: 'ডাউট সলভার চালু করুন',
  },
  {
    id: 'offline-pwa-vault',
    titleBn: 'পড়া চলবে ইন্টারনেট ছাড়াও',
    subtitleBn: 'অফলাইন পিডব্লিউএ ভল্ট ও প্র্যাকটিস ইঞ্জিন',
    descriptionBn: 'মোবাইল ডেটা বা ইন্টারনেট কানেকশন ছাড়াও লেকচার নোটস, ফর্মুলা শিট এবং সংরক্ষিত কুইজ নিরাপদে অনুশীলন করুন।',
    reassuranceBn: 'লোডশেডিং বা নেটওয়ার্কহীনতায় পড়াশোনা অক্ষত',
    badgeBn: 'জিরো ডেটা মোড',
    iconName: 'WifiOff',
    actionUrl: '/offline',
    actionLabelBn: 'অফলাইন ভল্ট দেখুন',
  },
  {
    id: 'national-live-challenge',
    titleBn: 'জাতীয় লাইভ অলিম্পিয়াড',
    subtitleBn: 'দেশসেরা শিক্ষার্থীদের সাথে রিয়েল-টাইম লড়াই',
    descriptionBn: 'প্রতি শুক্রবার রাতে নির্দিষ্ট সময়ে একই প্রশ্নে সারা দেশের হাজারো শিক্ষার্থীর সাথে নেগেটিভ মার্কিং সহ লাইভ চ্যালেঞ্জ।',
    reassuranceBn: 'সার্ভার সিঙ্কড নির্ভুল টাইমার ও জাতীয় র‍্যাঙ্কিং',
    badgeBn: 'লাইভ লড়াই',
    iconName: 'Trophy',
    actionUrl: '/live-challenge',
    actionLabelBn: 'লাইভ চ্যালেঞ্জে প্রবেশ করুন',
  },
  {
    id: 'printed-smart-materials',
    titleBn: 'অধ্যায়ভিত্তিক স্মার্ট নোটস ও প্রশ্নব্যাংক',
    subtitleBn: 'বিগত ১৫ বছরের বোর্ড ও শীর্ষ কলেজ প্রশ্ন',
    descriptionBn: 'প্রতিটি অধ্যায়ের গুরুত্বপূর্ণ সূত্র, দ্রুত সমাধানের কৌশল ও টাইপভিত্তিক প্রশ্নের সুশৃঙ্খল রিভিশন আর্কাইভ।',
    reassuranceBn: 'ক্লাস মিস করলেও আর্কাইভে সব সংরক্ষিত',
    badgeBn: 'রিভিশন রেডি',
    iconName: 'BookMarked',
    actionUrl: '/learn',
    actionLabelBn: 'নোটস ও শিট পড়ুন',
  },
];

export const VERIFIED_ACHIEVERS: AchieverProfile[] = [
  {
    id: 'achiever-01',
    nameBn: 'রেদোয়ান আহমেদ',
    institutionBn: 'নটর ডেম কলেজ, ঢাকা',
    milestoneBn: 'বুয়েট ভর্তি মেধা তালিকায় ৯ম',
    quoteBn: 'অগ্রযাত্রার লাইভ চ্যালেঞ্জ ও নেগেটিভ মার্কিং যুক্ত প্র্যাকটিস আমার ভুল চিহ্নিত করতে সবচেয়ে বেশি সাহায্য করেছে। পরীক্ষার হলের ভয় একদম কেটে গিয়েছিল।',
    batchBn: 'এইচএসসি ২৪ ব্যাচ',
    initials: 'রা',
    accentBg: 'bg-emerald-800 text-emerald-100 border-emerald-600',
  },
  {
    id: 'achiever-02',
    nameBn: 'ফারজানা আক্তার তিশা',
    institutionBn: 'ভিকারুননিসা নূন স্কুল অ্যান্ড কলেজ',
    milestoneBn: 'ঢাকা বিশ্ববিদ্যালয় ক ইউনিট মেধা তালিকায় ৭ম',
    quoteBn: 'অফলাইনে নোটস ডাউনলোড করে রাখার সুবিধাটা গ্রামের বাড়ি যাওয়ার পর খুব কাজে দিয়েছিল। ইন্টারনেট না থাকলেও পড়া কখনও থেমে থাকেনি।',
    batchBn: 'এইচএসসি ২৪ ব্যাচ',
    initials: 'ফা',
    accentBg: 'bg-blue-900 text-blue-100 border-blue-700',
  },
  {
    id: 'achiever-03',
    nameBn: 'মাহমুদ তানভীর',
    institutionBn: 'রাজশাহী কলেজ, রাজশাহী',
    milestoneBn: 'মেডিকেল ভর্তি মেধা তালিকায় ১৪তম',
    quoteBn: 'প্রতিটি সাবজেক্টের চ্যাপ্টারওয়াইজ কুইজ এবং সার্বক্ষণিক সক্রেটিক ডাউট সলভের ব্যাখ্যাগুলো ছিল একেবারেই শিক্ষক সুলভ। অসংখ্য ধন্যবাদ অগ্রযাত্রা!',
    batchBn: 'এইচএসসি ২৪ ব্যাচ',
    initials: 'মা',
    accentBg: 'bg-amber-800 text-amber-100 border-amber-600',
  },
  {
    id: 'achiever-04',
    nameBn: 'জাহিদ হাসান সোহাগ',
    institutionBn: 'চট্টগ্রাম কলেজ, চট্টগ্রাম',
    milestoneBn: '৪৫তম বিসিএস প্রিলি উত্তীর্ণ',
    quoteBn: 'বিসিএস প্রিলির ২০০ নম্বরের সিলেবাসে সময় ব্যবস্থাপনা সবচেয়ে বড় চ্যালেঞ্জ। অগ্রযাত্রার ওএমআর টাইমার টেস্ট সেই আত্মবিশ্বাস এনে দিয়েছিল।',
    batchBn: 'বিসিএস প্রিলি ব্যাচ',
    initials: 'জা',
    accentBg: 'bg-slate-800 text-slate-100 border-slate-600',
  },
];
