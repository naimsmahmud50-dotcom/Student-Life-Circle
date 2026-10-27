export interface GoEduInstructor {
  id: number;
  name: string;
  role: string;
  institution: string;
  photo: string;
  totalCourses: number;
  totalStudents: number;
  rating: number;
  bio: string;
}

export interface GoEduCourse {
  id: number;
  title: string;
  bengaliTitle: string;
  slug: string;
  category: string;
  categorySlug: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  levelBengali: string;
  thumbnail: string;
  instructor: GoEduInstructor;
  price: number;
  discountPrice?: number;
  rating: number;
  ratingCount: number;
  totalStudents: number;
  durationMinutes: number;
  totalLessons: number;
  tags: string[];
  routeLink: string;
  isPopular?: boolean;
  isAccredited?: boolean;
}

export interface GoEduBundle {
  id: number;
  title: string;
  bengaliTitle: string;
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

export interface GoEduCategory {
  id: string;
  name: string;
  bengaliName: string;
  count: number;
}

export const GOEDU_CATEGORIES: GoEduCategory[] = [
  { id: 'all', name: 'All Categories', bengaliName: 'সব কোর্স', count: 287 },
  { id: 'ai-tech', name: 'Artificial Intelligence & Tech', bengaliName: 'এআই ও প্রযুক্তি', count: 48 },
  { id: 'stem-math', name: 'Higher Math & Science', bengaliName: 'উচ্চতর গণিত ও বিজ্ঞান', count: 64 },
  { id: 'admission', name: 'University Admission & Test Prep', bengaliName: 'এডমিশন ও মডেল টেস্ট', count: 52 },
  { id: 'career-skills', name: 'Employability & Business Skills', bengaliName: 'ক্যারিয়ার ও ফ্রিল্যান্সিং', count: 75 },
  { id: 'software-web', name: 'Software & Web Development', bengaliName: 'সফটওয়্যার ও ওয়েব', count: 48 },
];

export const GOEDU_INSTRUCTORS: GoEduInstructor[] = [
  {
    id: 1,
    name: 'Sayma Suraiya',
    role: 'Assistant Professor & Applied Math Specialist',
    institution: 'Daffodil International University',
    photo: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80',
    totalCourses: 4,
    totalStudents: 12450,
    rating: 4.9,
    bio: 'Specialist in quantitative analysis, calculus with business applications, and curriculum moderation.'
  },
  {
    id: 2,
    name: 'Dr. Tanvir Ahmed',
    role: 'Lead AI Researcher & Faculty Member',
    institution: 'Institute of Information Technology, DU',
    photo: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80',
    totalCourses: 6,
    totalStudents: 18900,
    rating: 4.95,
    bio: 'Pioneer in Bengali Natural Language Processing, computer vision, and machine learning architectures.'
  },
  {
    id: 3,
    name: 'Fariha Rahman',
    role: 'Senior Academic Coordinator & Olympiad Mentor',
    institution: 'Ogrojatra Academic Research Cell',
    photo: 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=400&q=80',
    totalCourses: 5,
    totalStudents: 14200,
    rating: 4.88,
    bio: 'Dedicated mentor for Math Olympiad, physics problem-solving, and HSC board examination analytics.'
  },
  {
    id: 4,
    name: 'Mahmudur Rahman',
    role: 'Full Stack Architect & Industry Consultant',
    institution: 'Tech Bangladesh & GEAC Evaluator',
    photo: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=400&q=80',
    totalCourses: 8,
    totalStudents: 22100,
    rating: 4.92,
    bio: 'Industry practitioner guiding university students into high-growth software engineering careers.'
  }
];

export const GOEDU_COURSES: GoEduCourse[] = [
  {
    id: 1,
    title: 'Differential Calculus with Business & STEM Applications',
    bengaliTitle: 'ডিফারেনশিয়াল ক্যালকুলাস: থিওরি, গ্রাফ ও বাস্তব প্রয়োগ',
    slug: 'differential-calculus-applications',
    category: 'Higher Math & Science',
    categorySlug: 'stem-math',
    level: 'Beginner',
    levelBengali: 'প্রাথমিক থেকে মধ্যম',
    thumbnail: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=800&q=80',
    instructor: GOEDU_INSTRUCTORS[0],
    price: 1200,
    discountPrice: 500,
    rating: 4.9,
    ratingCount: 382,
    totalStudents: 3410,
    durationMinutes: 420,
    totalLessons: 24,
    tags: ['Differential Calculus', 'Business Mathematics', 'Marginal Analysis', 'NCTB STEM'],
    routeLink: '/socratic/solver?topic=calculus',
    isPopular: true,
    isAccredited: true
  },
  {
    id: 2,
    title: 'Generative AI & LLM Prompt Engineering for Students',
    bengaliTitle: 'জেনারেটিভ এআই ও প্রম্পট ইঞ্জিনিয়ারিং মাস্টারক্লাস',
    slug: 'generative-ai-prompt-engineering',
    category: 'Artificial Intelligence & Tech',
    categorySlug: 'ai-tech',
    level: 'Intermediate',
    levelBengali: 'মধ্যবর্তী পর্যায়',
    thumbnail: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80',
    instructor: GOEDU_INSTRUCTORS[1],
    price: 1500,
    discountPrice: 650,
    rating: 4.96,
    ratingCount: 520,
    totalStudents: 4890,
    durationMinutes: 540,
    totalLessons: 32,
    tags: ['Generative AI', 'Prompt Engineering', 'Productivity', 'Python'],
    routeLink: '/academic-hub',
    isPopular: true,
    isAccredited: true
  },
  {
    id: 3,
    title: 'HSC Physics Mechanics & Projectile Dynamics Arena',
    bengaliTitle: 'এইচএসসি পদার্থবিজ্ঞান ১ম পত্র: গতিবিদ্যা ও প্রক্ষেপক সিমুলেশন',
    slug: 'hsc-physics-mechanics-projectile',
    category: 'Higher Math & Science',
    categorySlug: 'stem-math',
    level: 'Intermediate',
    levelBengali: 'এইচএসসি স্পেশাল',
    thumbnail: 'https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?auto=format&fit=crop&w=800&q=80',
    instructor: GOEDU_INSTRUCTORS[2],
    price: 1000,
    discountPrice: 450,
    rating: 4.88,
    ratingCount: 412,
    totalStudents: 5120,
    durationMinutes: 380,
    totalLessons: 20,
    tags: ['Physics 1st Paper', 'Projectile Motion', 'Vector Mechanics', 'Board Exams'],
    routeLink: '/socratic/solver?topic=physics',
    isPopular: true,
    isAccredited: true
  },
  {
    id: 4,
    title: 'University Admission Mission 100: Math & Physics Mocks',
    bengaliTitle: 'বিশ্ববিদ্যালয় ভর্তি মিশন ১০০: ইঞ্জিনিয়ারিং ও ভার্সিটি ক ইউনিট',
    slug: 'university-admission-mission-100',
    category: 'University Admission & Test Prep',
    categorySlug: 'admission',
    level: 'Advanced',
    levelBengali: 'এডভান্সড এডমিশন',
    thumbnail: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=800&q=80',
    instructor: GOEDU_INSTRUCTORS[2],
    price: 2500,
    discountPrice: 990,
    rating: 4.94,
    ratingCount: 780,
    totalStudents: 8200,
    durationMinutes: 720,
    totalLessons: 45,
    tags: ['BUET', 'Dhaka University', 'Admission Predictor', 'Live MCQ'],
    routeLink: '/admission/predictor',
    isPopular: true,
    isAccredited: true
  },
  {
    id: 5,
    title: 'Modern Full-Stack Web Architecture with React & Next.js',
    bengaliTitle: 'মডার্ন ফুল-স্ট্যাক ওয়েব আর্কিটেকচার: রিয়েক্ট ও নেক্সট.জেএস',
    slug: 'modern-fullstack-web-architecture',
    category: 'Software & Web Development',
    categorySlug: 'software-web',
    level: 'Beginner',
    levelBengali: 'বিগিনার থেকে প্রফেশনাল',
    thumbnail: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80',
    instructor: GOEDU_INSTRUCTORS[3],
    price: 1800,
    discountPrice: 750,
    rating: 4.91,
    ratingCount: 295,
    totalStudents: 2980,
    durationMinutes: 600,
    totalLessons: 36,
    tags: ['React', 'Next.js', 'Tailwind CSS', 'TypeScript', 'API Integration'],
    routeLink: '/career/radar',
    isPopular: false,
    isAccredited: true
  },
  {
    id: 6,
    title: 'HSC ICT Boolean Algebra, Logic Gates & Number Systems',
    bengaliTitle: 'এইচএসসি আইসিটি: বুলিয়ান অ্যালজেব্রা, লজিক গেট ও সংখ্যা পদ্ধতি',
    slug: 'hsc-ict-boolean-algebra-logic-gates',
    category: 'Higher Math & Science',
    categorySlug: 'stem-math',
    level: 'Beginner',
    levelBengali: 'এইচএসসি ও বোর্ড এক্সাম',
    thumbnail: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80',
    instructor: GOEDU_INSTRUCTORS[1],
    price: 900,
    discountPrice: 400,
    rating: 4.93,
    ratingCount: 340,
    totalStudents: 4190,
    durationMinutes: 320,
    totalLessons: 18,
    tags: ['ICT', 'Boolean Algebra', 'De Morgan Theorem', 'Logic Gates'],
    routeLink: '/socratic/solver?topic=ict',
    isPopular: true,
    isAccredited: true
  },
  {
    id: 7,
    title: 'Professional Communication & Career Readiness for Bangladeshi Graduates',
    bengaliTitle: 'প্রফেশনাল কমিউনিকেশন, সিভি বিল্ডিং ও কর্পোরেট প্রস্তুতি',
    slug: 'professional-communication-career-readiness',
    category: 'Employability & Business Skills',
    categorySlug: 'career-skills',
    level: 'Beginner',
    levelBengali: 'ক্যারিয়ার প্রস্তুতি',
    thumbnail: 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=800&q=80',
    instructor: GOEDU_INSTRUCTORS[3],
    price: 800,
    discountPrice: 350,
    rating: 4.87,
    ratingCount: 210,
    totalStudents: 3120,
    durationMinutes: 240,
    totalLessons: 14,
    tags: ['Career Growth', 'Interview Skills', 'CV Building', 'Communication'],
    routeLink: '/career/radar',
    isPopular: false,
    isAccredited: true
  },
  {
    id: 8,
    title: 'HSC Chemistry Stoichiometry & Chemical Bonding Essentials',
    bengaliTitle: 'এইচএসসি রসায়ন ১ম ও ২য় পত্র: স্টয়কিওমেট্রি ও রাসায়নিক বন্ধন',
    slug: 'hsc-chemistry-stoichiometry-bonding',
    category: 'Higher Math & Science',
    categorySlug: 'stem-math',
    level: 'Intermediate',
    levelBengali: 'এইচএসসি ও এডমিশন',
    thumbnail: 'https://images.unsplash.com/photo-1603126857599-f6e157fa2fe6?auto=format&fit=crop&w=800&q=80',
    instructor: GOEDU_INSTRUCTORS[2],
    price: 1100,
    discountPrice: 480,
    rating: 4.89,
    ratingCount: 315,
    totalStudents: 3740,
    durationMinutes: 360,
    totalLessons: 22,
    tags: ['Chemistry 1st Paper', 'Stoichiometry', 'Molar Volume', 'Periodic Table'],
    routeLink: '/socratic/solver?topic=chemistry',
    isPopular: true,
    isAccredited: true
  }
];

export const GOEDU_BUNDLES: GoEduBundle[] = [
  {
    id: 1,
    title: 'The AI Advantage Accelerator Course Bundle',
    bengaliTitle: 'এআই এডভান্টেজ এক্সিলারেটর বান্ডেল: প্রযুক্তি ও প্রডাক্টিভিটি',
    subtitle: 'Master practical AI for income generation, academic research, and career acceleration.',
    description: 'AI is transforming the way students and professionals work, earn, and build academic careers. This bundle covers LLMs, Prompt Engineering, Automation, and Python workflows.',
    slug: 'the-ai-advantage-accelerator-bundle',
    tag: 'Featured Bundle',
    coursesCount: 5,
    originalPrice: 4500,
    bundlePrice: 1490,
    thumbnail: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=1200&q=80',
    highlights: [
      '৫টি প্রফেশনাল ও জিইএসি সার্টিফাইড কোর্স',
      'প্রম্পট ইঞ্জিনিয়ারিং ও অটোমেশন প্রজেক্টস',
      '২৪/৭ সক্রেটিক এআই টিউটর সহায়তা',
      'আজীবন এক্সেস ও রিভিশন ম্যাটেরিয়ালস'
    ],
    routeLink: '/academic-hub?bundle=ai-advantage'
  },
  {
    id: 2,
    title: 'HSC STEM Complete Mastery & Board Exam Fighter Bundle',
    bengaliTitle: 'এইচএসসি স্টেম কমপ্লিট মাস্টারি ও বোর্ড প্রশ্ন সমাধান বান্ডেল',
    subtitle: 'Full NCTB syllabus coverage for Higher Math, Physics, Chemistry, and ICT.',
    description: 'Designed specifically for HSC candidates aiming for A+ in science. Includes past 10 years board paper solutions, 3D interactive physics simulations, and live challenge arena access.',
    slug: 'hsc-stem-mastery-bundle',
    tag: 'Board Special',
    coursesCount: 6,
    originalPrice: 5200,
    bundlePrice: 1750,
    thumbnail: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80',
    highlights: [
      'উচ্চতর গণিত, পদার্থবিজ্ঞান, রসায়ন ও আইসিটি সম্পূর্ণ কভারেজ',
      'বিগত ১০ বছরের বোর্ড প্রশ্ন সমাধান ও ব্যাখ্যা',
      'সক্রেটিক ইন্টারেক্টিভ হোয়াইটবোর্ড সলভার',
      'লাইভ চ্যালেঞ্জ কুইজ এরিনা ফ্রি এক্সেস'
    ],
    routeLink: '/board-archives'
  }
];

export const GOEDU_TRUST_FACTORS = [
  {
    id: 'accreditation',
    title: 'GEAC ও আন্তর্জাতিক স্বীকৃতি',
    description: 'সকল কোর্স অভিজ্ঞ একাডেমিশিয়ান এবং ইন্ড্রাস্ট্রি বিশেষজ্ঞদের দ্বারা যাচাইকৃত ও অনুমোদিত।'
  },
  {
    id: 'socratic-ai',
    title: '২৪/৭ সক্রেটিক এআই টিউটর',
    description: 'মুখস্থ নয়—সক্রেটিক ডায়লগের মাধ্যমে ধাপে ধাপে জটিল গাণিতিক ও বৈজ্ঞানিক সমস্যা সমাধান।'
  },
  {
    id: 'lifetime-access',
    title: 'আজীবন এক্সেস ও আপডেট',
    description: 'একবার এনরোল করলেই লেকচার নোটস, কুইজ এবং ভবিষ্যৎ আপডেটে কোনো অতিরিক্ত ফি নেই।'
  },
  {
    id: 'career-placement',
    title: 'সার্টিফিকেট ও ক্যারিয়ার রাডার',
    description: 'কোর্স সমাপ্তির পর ভেরিফায়েড সার্টিফিকেট এবং জব মার্কেটের ক্যারিয়ার ম্যাপিং সহায়তা।'
  }
];

export function getCoursesByCategory(categorySlug: string): GoEduCourse[] {
  if (!categorySlug || categorySlug === 'all') {
    return GOEDU_COURSES;
  }
  return GOEDU_COURSES.filter(course => course.categorySlug === categorySlug);
}

export function searchGoEduCourses(query: string): GoEduCourse[] {
  if (!query || !query.trim()) {
    return GOEDU_COURSES;
  }
  const clean = query.trim().toLowerCase();
  return GOEDU_COURSES.filter(course =>
    course.title.toLowerCase().includes(clean) ||
    course.bengaliTitle.toLowerCase().includes(clean) ||
    course.category.toLowerCase().includes(clean) ||
    course.tags.some(t => t.toLowerCase().includes(clean)) ||
    course.instructor.name.toLowerCase().includes(clean)
  );
}
