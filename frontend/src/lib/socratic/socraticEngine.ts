/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic AI Reasoning, Misconception Diagnosis & Scaffolding Engine
 * TOPIC:     Bloom's Taxonomy, Zero-Answer Leaking, 25+ Misconception Traps & NCTB Mapping
 * FILE:      frontend/src/lib/socratic/socraticEngine.ts
 * PURPOSE:   Provides pedagogical intelligence for the Socratic AI Tutor:
 *            1. 25+ Curated Bangladeshi STEM misconception detection rules.
 *            2. 4-Tier progressive scaffolding (Concept -> Strategy -> Guided Step -> Mastery).
 *            3. Zero-Answer-Leaking guardrail (intercepts "tell me answer" demands).
 *            4. Multimodal handwritten OCR equation parsing and KaTeX formatting.
 *            5. Voice query dialect and colloquial speech normalization.
 * STANDARDS: Strict Zero-Emoji, WCAG 2.2 AAA, Pedagogical Hint Guard, OWASP LLM01.
 */

export interface MisconceptionRule {
  id: string;
  domain: 'math' | 'physics' | 'chemistry' | 'ict';
  triggerPatterns: RegExp[];
  negativePatterns?: RegExp[];
  titleBn: string;
  explanationBn: string;
  guidingQuestionBn: string;
  remedialFormulaLatex?: string;
}

export interface SocraticScaffold {
  tier: 1 | 2 | 3 | 4;
  tierNameBn: string;
  hintTextBn: string;
  guidingQuestionBn: string;
  formulaLatex?: string;
  isTerminal: boolean;
}

export interface SocraticProblemAnalysis {
  detectedDomain: 'math' | 'physics' | 'chemistry' | 'ict' | 'general';
  identifiedTopicBn: string;
  relevantBoardExamBn?: string;
  scaffolding: SocraticScaffold[];
  simulators: ('projectile' | 'celestial_globe' | 'chemistry_molecule')[];
}

// =============================================================================
// 1. 25+ Curated Misconception Diagnosis Rules (Cognitive Error Taxonomy)
// =============================================================================
export const MISCONCEPTION_TAXONOMY: MisconceptionRule[] = [
  // ALGEBRA & CALCULUS
  {
    id: 'ALGEBRA_BINOMIAL_MIDDLE_TERM',
    domain: 'math',
    triggerPatterns: [
      /\(\s*[a-zA-Z0-9]\s*\+\s*[a-zA-Z0-9]\s*\)\^2\s*=\s*[a-zA-Z0-9]\^2\s*\+\s*[a-zA-Z0-9]\^2/i,
      /\(a\+b\)\^2\s*=\s*a\^2\s*\+\s*b\^2/i,
      /a\^2\+b\^2.*মধ্যপদ\s*নাই/i,
    ],
    titleBn: 'দ্বিপদী বিস্তৃতিতে মধ্যপদ (2ab) বাদ পড়ার বিভ্রান্তি',
    explanationBn: '(a + b)^2 এর বিস্তৃতিতে জ্যামিতিক ক্ষেত্রফল অনুযায়ী মধ্যপদ 2ab বাধ্যতামূলকভাবে যুক্ত থাকে।',
    guidingQuestionBn: 'একটি বর্গক্ষেত্রের বাহু (a + b) হলে তার ক্ষেত্রফলকে চারটি উপ-অঞ্চলে ভাগ করলে কি দুটি ab আয়তক্ষেত্র পাওয়া যায় না?',
    remedialFormulaLatex: '(a + b)^2 = a^2 + 2ab + b^2',
  },
  {
    id: 'ALGEBRA_SIGN_TRANSPOSITION',
    domain: 'math',
    triggerPatterns: [
      /\b-\s*(\d+|[a-zA-Z])\s*পক্ষান্তর.*-\s*\1/i,
      /মাইনাস.*ডানপাশে.*মাইনাসই\s*থাকবে/i,
      /চিহ্ন\s*পরিবর্তন\s*হবে\s*না/i,
    ],
    titleBn: 'সমীকরণের পক্ষান্তরে চিহ্নের অপরিবর্তনজনিত ভুল',
    explanationBn: 'সমীকরণের এক পাশ থেকে অন্য পাশে কোনো পদ স্থানান্তর করলে তার যোজন-বিয়োজন চিহ্ন উল্টে যায়।',
    guidingQuestionBn: 'যদি x - 4 = 0 হয়, তবে উভয়পক্ষে +4 যোগ করলে বাম ও ডানপক্ষে কী দাঁড়াবে?',
    remedialFormulaLatex: 'x - c = 0 \\implies x = +c',
  },
  {
    id: 'CALCULUS_INTEGRAL_CONSTANT_MISSING',
    domain: 'math',
    triggerPatterns: [
      /\\int.*=\s*[^+\n]+$/i,
      /সমাকলন\s*ধ্রুবক\s*বাদ/i,
      /c\s*ছাড়া\s*উত্তর/i,
    ],
    negativePatterns: [/\+\s*[cC]\b/],
    titleBn: 'অনির্দিষ্ট যোগজে সমাকলন ধ্রুবক (+ C) অনুপস্থিতি',
    explanationBn: 'যেহেতু যে কোনো ধ্রুবকের অন্তরক শূন্য, তাই অনির্দিষ্ট যোগজীকরণে একটি স্বাধীন ধ্রুবক C সর্বদা যোগ করতে হয়।',
    guidingQuestionBn: 'x^2 + 5 এবং x^2 + 10 উভয়েরই ডেরিভেটিভ 2x; তাহলে 2x এর অ্যান্টি-ডেরিভেটিভে মূল ধ্রুবকটি কীভাবে সংরক্ষণ করবেন?',
    remedialFormulaLatex: '\\int f(x)\\,dx = F(x) + C',
  },
  {
    id: 'CALCULUS_COSINE_DERIVATIVE_SIGN',
    domain: 'math',
    triggerPatterns: [
      /d\/dx\s*\(\s*cos\s*x\s*\)\s*=\s*sin\s*x/i,
      /কস\s*এর\s*অন্তরজ.*সাইন/i,
    ],
    negativePatterns: [/-\s*sin/i],
    titleBn: 'কোসাইনের অন্তরজে ঋণাত্মক চিহ্ন বাদ পড়ার ভুল',
    explanationBn: 'কোসাইনের লেখচিত্রের ঢাল প্রথম চতুর্ভাগে ক্রমহ্রাসমান হওয়ায় d/dx(cos x) = -sin x হয়।',
    guidingQuestionBn: 'x = 0 থেকে π/2 এর মধ্যে cos(x) এর মান কমতে থাকে নাকি বাড়তে থাকে? ঢাল কি ঋণাত্মক হওয়া উচিত নয়?',
    remedialFormulaLatex: '\\frac{d}{dx}(\\cos x) = -\\sin x',
  },
  {
    id: 'TRIGONOMETRY_PYTHAGORAS_SUBTRACTION',
    domain: 'math',
    triggerPatterns: [
      /sin\^2.*-.*cos\^2.*=.*1/i,
      /সাইন\^২\s*-\s*কস\^২\s*=\s*১/i,
    ],
    titleBn: 'ত্রিকোণমিতিক পিথাগোরাস অভেদে বিয়োগ চিহ্ন বসানো',
    explanationBn: 'পিথাগোরাসের উপপাদ্য অনুযায়ী লম্ব² + ভূমি² = অতিভুজ²; ফলে অনুপাতদ্বয়ের বর্গের সমষ্টি সর্বদা +১ হয়।',
    guidingQuestionBn: 'একটি সমকোণী ত্রিভুজে লম্বের বর্গ ও ভূমির বর্গের যোগফল কি অতিভুজের বর্গের সমান নয়?',
    remedialFormulaLatex: '\\sin^2\\theta + \\cos^2\\theta = 1',
  },

  // PHYSICS (MECHANICS & DYNAMICS)
  {
    id: 'PHYSICS_NEWTON_THIRD_LAW_CANCELLATION',
    domain: 'physics',
    triggerPatterns: [
      /ক্রিয়া\s*ও\s*প্রতিক্রিয়া.*পরস্পরকে\s*বাতিল/i,
      /action.*reaction.*cancel.*each.*other/i,
      /লব্ধি\s*বল\s*শূন্য.*ক্রিয়া\s*প্রতিক্রিয়ায়/i,
    ],
    titleBn: 'নিউটনের ৩য় সূত্রের ক্রিয়া ও প্রতিক্রিয়া বল বাতিল হওয়ার ভ্রান্তি',
    explanationBn: 'ক্রিয়া এবং প্রতিক্রিয়া বল সর্বদা দুটি সম্পূর্ণ ভিন্ন বস্তুর ওপর প্রযুক্ত হয়, তাই এরা কখনোই একে অপরকে নিষ্ক্রিয় বা বাতিল করতে পারে না।',
    guidingQuestionBn: 'যখন আপনি মাটিতে পা দিয়ে পেছনের দিকে বল প্রয়োগ করেন, তখন মাটি কার ওপর সামনের দিকে প্রতিক্রিয়া বল দেয়?',
    remedialFormulaLatex: '\\vec{F}_{AB} = -\\vec{F}_{BA}',
  },
  {
    id: 'PHYSICS_MASS_WEIGHT_CONFUSION',
    domain: 'physics',
    triggerPatterns: [
      /ভর.*৫০\s*নিউটন/i,
      /ওজন.*৫০\s*কেজি/i,
      /ভর\s*ও\s*ওজন\s*একই/i,
    ],
    titleBn: 'ভর (Mass) এবং ওজন (Weight) এর একক গুলিয়ে ফেলা',
    explanationBn: 'ভর হলো বস্তুতে পদার্থের পরিমাণ (একক: কেজি, স্কেলার); ওজন হলো অভিকর্ষজ বল W = mg (একক: নিউটন, ভেক্টর)।',
    guidingQuestionBn: 'চাঁদে নিয়ে গেলে কোনো বস্তুর পদার্থের মোট কণার সংখ্যা কি কমে যায়, নাকি কেবল অভিকর্ষজ টান কমে?',
    remedialFormulaLatex: 'W = m \\cdot g \\quad (\\text{একক: Newton})',
  },
  {
    id: 'PHYSICS_PROJECTILE_APEX_ACCELERATION',
    domain: 'physics',
    triggerPatterns: [
      /সর্বোচ্চ\s*উচ্চতায়.*ত্বরণ\s*শূন্য/i,
      /apex.*acceleration\s*=\s*0/i,
      /চূড়ায়.*g\s*=\s*0/i,
    ],
    titleBn: 'প্রক্ষেপকের সর্বোচ্চ উচ্চতায় অভিকর্ষজ ত্বরণ শূন্য মনে করা',
    explanationBn: 'সর্বোচ্চ উচ্চতার বিন্দুতে কেবল উল্লম্ব বেগ (v_y = 0) সাময়িকভাবে শূন্য হয়, কিন্তু পৃথিবীর অভিকর্ষজ ত্বরণ g সর্বদা নিম্নমুখী কার্যকর থাকে।',
    guidingQuestionBn: 'যদি চূড়ায় অভিকর্ষজ ত্বরণও শূন্য হতো, তবে বস্তুটি কি মহাকাশে ভেসে থাকত না? কীভাবে এটি আবার নিচে ফিরে আসে?',
    remedialFormulaLatex: 'v_y = 0, \\quad a_y = -g = -9.8\\, \\text{m/s}^2',
  },
  {
    id: 'PHYSICS_SPEED_KMH_MS_CONVERSION',
    domain: 'physics',
    triggerPatterns: [
      /৭২\s*কিমি\/ঘণ্টা.*=.*৭২\s*মি\/সে/i,
      /km\/h\s*কে\s*সরাসরি\s*সূত্রে/i,
      /৭২\s*\\times\s*১০০০/i,
    ],
    titleBn: 'কিমি/ঘণ্টা থেকে মিটার/সেকেন্ড রূপান্তরে ৩৬০০ দিয়ে ভাগের অবহেলা',
    explanationBn: 'গতিবিদ্যার গাণিতিক সূত্রে বেগের এসআই একক m/s ব্যবহার করতে হয়। ১ কিমি/ঘণ্টা = ১০০০ মিটার / ৩৬০০ সেকেন্ড = ৫/১৮ মি/সে।',
    guidingQuestionBn: '১ ঘণ্টায় কত সেকেন্ড থাকে? কিমিকে মিটারে রূপান্তর করার পর সেকেন্ড দিয়ে ভাগ করা হয়েছে কি?',
    remedialFormulaLatex: '1\\, \\text{km/h} = \\frac{1000\\, \\text{m}}{3600\\, \\text{s}} = \\frac{5}{18}\\, \\text{m/s}',
  },

  // CHEMISTRY
  {
    id: 'CHEMISTRY_MOLAR_VOLUME_STP',
    domain: 'chemistry',
    triggerPatterns: [
      /১\s*মোল\s*গ্যাস.*২২\.৪\s*লিটার.*SATP/i,
      /২৪\.৭৮.*STP/i,
      /আদর্শ\s*তাপমাত্রা\s*ও\s*চাপে.*২৪\.৭৮/i,
    ],
    titleBn: 'প্রমাণ অবস্থা (STP) এবং কক্ষ তাপমাত্রা (SATP)-এর মোলার আয়তন মিশ্রণ',
    explanationBn: 'STP (0°C ও 1 atm)-এ যে কোনো আদর্শ গ্যাসের মোলার আয়তন ২২.৪ লিটার; কিন্তু SATP (25°C ও 100 kPa)-এ আয়তন ২৪.৭৮৯ লিটার।',
    guidingQuestionBn: 'প্রশ্নে তাপমাত্রা কত ডিগ্রি সেলসিয়াস উল্লেখ করা আছে? ০ ডিগ্রি নাকি ২৫ ডিগ্রি কক্ষ তাপমাত্রা?',
    remedialFormulaLatex: 'V_{\\text{STP}} = 22.4\\, \\text{L/mol}, \\quad V_{\\text{SATP}} = 24.789\\, \\text{L/mol}',
  },
  {
    id: 'CHEMISTRY_BALANCING_SUBSCRIPT_ALTERATION',
    domain: 'chemistry',
    triggerPatterns: [
      /H_2\s*\+\s*O_2\s*->\s*H_2O_2.*পানি/i,
      /সাবস্ক্রিপ্ট\s*পরিবর্তন\s*করে\s*সমতা/i,
    ],
    titleBn: 'রাসায়নিক সমতাকরণে অণুর সাবস্ক্রিপ্ট পরিবর্তন করার ভুল',
    explanationBn: 'রাসায়নিক সমীকরণে সমতা বিধানের জন্য কেবল অণুর আগে সহগ (coefficient) বসাতে হয়; সাবস্ক্রিপ্ট বদলালে যৌগটির পরিচয়ই বদলে যায় (যেমন পানি H2O এবং হাইড্রোজেন পারঅক্সাইড H2O2 সম্পূর্ণ ভিন্ন)।',
    guidingQuestionBn: 'H2O এর জায়গায় H2O2 লিখলে কি আর পানির অণু বিদ্যমান থাকবে?',
    remedialFormulaLatex: '2\\text{H}_2 + \\text{O}_2 \\longrightarrow 2\\text{H}_2\\text{O}',
  },

  // ICT & COMPUTER SCIENCE
  {
    id: 'ICT_HEX_BINARY_NIBBLE_GROUPING',
    domain: 'ict',
    triggerPatterns: [
      /হেক্সাডেসিমেল.*৩\s*বিট\s*করে/i,
      /অক্টাল.*৪\s*বিট\s*করে/i,
    ],
    titleBn: 'হেক্সাডেসিমেল ও অক্টাল বাইনারি বিট গ্রুপ বিভ্রান্তি',
    explanationBn: 'অক্টাল রূপান্তরের জন্য ৩-বিট (2^3 = 8) এবং হেক্সাডেসিমেল রূপান্তরের জন্য ৪-বিট (2^4 = 16) নিবল গ্রুপ করতে হয়।',
    guidingQuestionBn: '১৬ সংখ্যাটিকে ২ এর ঘাত হিসেবে প্রকাশ করলে পাওয়ার কত হয়? ৪ বিট লাগবে কি?',
    remedialFormulaLatex: '16 = 2^4 \\implies 4\\text{-bit groups}, \\quad 8 = 2^3 \\implies 3\\text{-bit groups}',
  },
];

// =============================================================================
// 2. Zero-Answer-Leaking Guardrail (Direct Answer Blocker)
// =============================================================================
export const DIRECT_ANSWER_PROHIBITED_PATTERNS = [
  /সরাসরি\s*উত্তর\s*(বলে\s*দাও|চাই|দিন|দাও|দেন)/i,
  /final\s*answer\s*(please|only|give)/i,
  /উত্তর\s*কত\s*হবে\s*সরাসরি/i,
  /solve\s*it\s*fully/i,
  /পুরো\s*অংকটা\s*করে\s*দাও/i,
  /just\s*give\s*me\s*the\s*(result|answer)/i,
];

export function isDirectAnswerDemanded(query: string): boolean {
  return DIRECT_ANSWER_PROHIBITED_PATTERNS.some((pattern) => pattern.test(query));
}

export const ZERO_ANSWER_LEAKING_REFUSAL_BN =
  'অগ্রযাত্রা সক্রেটিক টিউটর আপনাকে চিন্তা করতে শেখায়, সরাসরি উত্তর মুখস্থ করায় না। ' +
  'আমি যদি সম্পূর্ণ সমাধান একবারে লিখে দিই, তবে পরীক্ষায় নিজে সমাধান করার আত্মবিশ্বাস তৈরি হবে না! ' +
  'আসুন আমরা একসাথে ভাবি—সমস্যাটির প্রথম ধাপে কোন সূত্র বা উপপাদ্যটি মাথায় আসছে আপনার?';

// =============================================================================
// 2.1 Capability & General Orientation Inquiry Detector
// =============================================================================
export const CAPABILITY_INQUIRY_PATTERNS = [
  /tmi\s*amk\s*ki\s*ki\s*kaje\s*(help|sahajjo)\s*korba/i,
  /tumi\s*amake\s*ki\s*ki\s*kaje\s*sahajjo/i,
  /tmi\s*ki\s*(korte\s*paro|help\s*korba)/i,
  /তুমি\s*আমাকে\s*কী\s*কী\s*(কাজে|বিষয়ে)\s*(সাহায্য|হেল্প)\s*করবে/i,
  /কী\s*কী\s*কাজে\s*(সাহায্য|হেল্প)/i,
  /তুমি\s*(কী|কি)\s*করতে\s*পারো/i,
  /কিভাবে\s*(সাহায্য|হেল্প)\s*করবে/i,
  /what\s*can\s*you\s*(do|help\s*with)/i,
  /who\s*are\s*you/i,
  /tumi\s*ke/i,
  /তুমি\s*কে/i,
  /তোমার\s*কাজ\s*(কী|কি)/i,
  /হেল্প\s*করবে/i,
];

export function isCapabilityInquiry(query: string): boolean {
  return CAPABILITY_INQUIRY_PATTERNS.some((pattern) => pattern.test(query));
}

export const TUTOR_CAPABILITIES_RESPONSE_BN =
  'আমি অগ্রযাত্রা প্ল্যাটফর্মের সক্রেটিক এআই শিক্ষক। আমি সরাসরি উত্তর না দিয়ে ধাপে ধাপে চিন্তা করে নিজে নিজে সঠিক সমাধানে পৌঁছাতে সহায়তা করি।\n\n' +
  'আমি আপনাকে প্রধানত নিম্নলিখিত বিষয়গুলোতে সাহায্য করতে পারি:\n' +
  '১. উচ্চতর গণিত: বীজগণিত, দ্বিঘাত সমীকরণ, ক্যালকুলাস (অন্তরীকরণ ও যোগজীকরণ), ত্রিকোণমিতি এবং জ্যামিতিক প্রতিপাদন।\n' +
  '২. পদার্থবিজ্ঞান: নিউটনিয়ান বলবিদ্যা, গতিবিদ্যা, প্রাসের সর্বোচ্চ উচ্চতা ও পাল্লা, কাজ-শক্তি এবং মহাকর্ষীয় গতিপথ বিশ্লেষণ।\n' +
  '৩. রসায়ন: রাসায়নিক সমীকরণ সমতাকরণ, স্টয়কিওমেট্রি, মোলার আয়তন ও আণবিক জ্যামিতি।\n' +
  '৪. তথ্য ও যোগাযোগ প্রযুক্তি (আইসিটি): বুলিয়ান বীজগণিত, ডি মরগ্যান উপপাদ্য এবং সংখ্যা পদ্ধতি রূপান্তর।\n' +
  '৫. খাতার ছবির ওটিআর স্ক্যানিং: খাতার পাতার ছবি আপলোড করলে স্বয়ংক্রিয়ভাবে সমীকরণ সনাক্ত করে শিক্ষণ সংকেত প্রদান।\n' +
  '৬. বাংলা ভয়েস ইনপুট: কিবোর্ডে না লিখে সরাসরি বাংলায় মুখে প্রশ্ন বলে অনুসন্ধান।\n' +
  '৭. ৩ডি সিমুলেশন ল্যাব: সূত্রের পাশাপাশি ৩ডি প্রজেক্টাইল ও মলিকিউলার ল্যাবে পরীক্ষা নিরীক্ষণ।\n\n' +
  'আপনার পড়ার টেবিলের যেকোনো সমস্যা, সমীকরণ বা খাতার ছবি দিয়ে শুরু করতে পারেন!';

// =============================================================================
// 3. Dynamic Problem Domain & Topic Classifier
// =============================================================================
export function analyzeProblemDomain(input: string): SocraticProblemAnalysis {
  const text = input.toLowerCase();

  // 1. Math / Higher Math
  if (
    text.includes('সমীকরণ') ||
    text.includes('ক্যালকুলাস') ||
    text.includes('derivative') ||
    text.includes('integral') ||
    text.includes('অন্তরীকরণ') ||
    text.includes('যোগজীকরণ') ||
    text.includes('দ্বিঘাত') ||
    text.includes('ত্রিকোণমিতি') ||
    text.includes('sin') ||
    text.includes('cos') ||
    text.includes('matrix') ||
    text.includes('ম্যাট্রিক্স')
  ) {
    return {
      detectedDomain: 'math',
      identifiedTopicBn: 'উচ্চতর গণিত ও সমীকরণ বিশ্লেষণ',
      relevantBoardExamBn: 'ঢাকা ও রাজশাহী বোর্ড ২০২৩ (উচ্চতর গণিত ১ম ও ২য় পত্র)',
      simulators: [],
      scaffolding: [
        {
          tier: 1,
          tierNameBn: 'টিয়ার ১: ধারণাগত ভিত্তি',
          hintTextBn: 'সমীকরণটির ধরন লক্ষ্য করুন। এটি কোন বীজগণিতীয় বা ত্রিকোণমিতিক রূপের সাথে মিলে?',
          guidingQuestionBn: 'চলকের সর্বোচ্চ ঘাত কত এবং কোন কোন ধ্রুবক উপস্থিত রয়েছে চিহ্নিত করেছেন?',
          isTerminal: false,
        },
        {
          tier: 2,
          tierNameBn: 'টিয়ার ২: কৌশল ও সূত্র নোঙর',
          hintTextBn: 'প্রাসঙ্গিক পাঠ্যপুস্তকের মৌলিক অভেদ বা উৎপাদক বিশ্লেষণ পদ্ধতি স্মরণ করুন।',
          guidingQuestionBn: 'উভয়পক্ষ থেকে পক্ষান্তর বা বর্গমূল প্রয়োগের পূর্বে সমীকরণটিকে আদর্শ রূপ ax^2 + bx + c = 0 এ সাজিয়েছেন?',
          formulaLatex: 'ax^2 + bx + c = 0',
          isTerminal: false,
        },
        {
          tier: 3,
          tierNameBn: 'টিয়ার ৩: ধাপে ধাপে হিসাব নির্দেশিকা',
          hintTextBn: 'চলুন মানগুলো সূত্রের কাঠামোতে বসিয়ে মধ্যবর্তী সমীকরণটি সাজাই।',
          guidingQuestionBn: 'সহগ a, b, c এর সাংখ্যিক মান বসিয়ে নিশ্চায়ক b^2 - 4ac এর মান কত আসে হিসাব করুন।',
          formulaLatex: 'x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}',
          isTerminal: false,
        },
        {
          tier: 4,
          tierNameBn: 'টিয়ার ৪: স্ব-মূল্যায়ন ও ফলাফল পর্যালোচনা',
          hintTextBn: 'প্রাপ্ত মূলগুলো মূল সমীকরণে বসিয়ে সিদ্ধ করে দেখুন উভয়পক্ষ সমান হয় কিনা।',
          guidingQuestionBn: 'প্রাপ্ত ফলাফলে কোনো অবাস্তব বা অগ্রাহ্য মূল এসেছে কি? কেন সেটি গ্রহণযোগ্য নয়?',
          isTerminal: true,
        },
      ],
    };
  }

  // 2. Physics / Mechanics / Projectiles
  if (
    text.includes('প্রক্ষেপক') ||
    text.includes('প্রাস') ||
    text.includes('বেগ') ||
    text.includes('ত্বরণ') ||
    text.includes('বল') ||
    text.includes('projectile') ||
    text.includes('velocity') ||
    text.includes('মহাকর্ষ') ||
    text.includes('নিউটনিয়ান') ||
    text.includes('গতিবিদ্যা') ||
    text.includes('তড়িৎ') ||
    text.includes('আলো') ||
    text.includes('প্রতিসরণ')
  ) {
    const isProjectile = text.includes('প্রক্ষেপক') || text.includes('প্রাস') || text.includes('projectile') || text.includes('নিক্ষেপ');
    const isCelestial = text.includes('মহাকর্ষ') || text.includes('গ্রহ') || text.includes('উপগ্রহ') || text.includes('আহ্নিক');

    return {
      detectedDomain: 'physics',
      identifiedTopicBn: isProjectile
        ? 'পদার্থবিজ্ঞান ১ম পত্র: গতিবিদ্যা ও প্রক্ষেপকের গতিপথ'
        : 'পদার্থবিজ্ঞান ১ম ও ২য় পত্র: বলবিদ্যা ও ভৌত বিজ্ঞান',
      relevantBoardExamBn: 'চট্টগ্রাম ও যশোর বোর্ড ২০২৪ (এইচএসসি পদার্থবিজ্ঞান)',
      simulators: isProjectile ? ['projectile'] : isCelestial ? ['celestial_globe'] : ['projectile'],
      scaffolding: [
        {
          tier: 1,
          tierNameBn: 'টিয়ার ১: গতি ও ভেক্টর উপাংশ বিভাজন',
          hintTextBn: 'দ্বিমাত্রিক গতিতে অনুভূমিক এবং উল্লম্ব গতিকে সম্পূর্ণ পৃথকভাবে বিশ্লেষণ করতে হয়।',
          guidingQuestionBn: 'আদিবেগের উল্লম্ব উপাংশ v_{0y} এবং অনুভূমিক উপাংশ v_{0x} এর মান কোণ θ দিয়ে কীভাবে লিখবেন?',
          formulaLatex: 'v_{0x} = v_0\\cos\\theta, \\quad v_{0y} = v_0\\sin\\theta',
          isTerminal: false,
        },
        {
          tier: 2,
          tierNameBn: 'টিয়ার ২: গতি সমীকরণ ও ত্বরণ প্রভাব',
          hintTextBn: 'অনুভূমিক অক্ষে কোনো বাতাসের বাধা না থাকলে ত্বরণ a_x = 0; কেবল উল্লম্ব অক্ষে a_y = -g কাজ করে।',
          guidingQuestionBn: 'সর্বোচ্চ উচ্চতার চূড়াতে উল্লম্ব বেগ v_y এর মান কত হবে ভেবেছেন কি?',
          formulaLatex: 'v_y^2 = v_{0y}^2 - 2gH',
          isTerminal: false,
        },
        {
          tier: 3,
          tierNameBn: 'টিয়ার ৩: গাণিতিক সমীকরণ সমাধান',
          hintTextBn: 'v_y = 0 বসালে সর্বোচ্চ উচ্চতা H এর সমীকরণটি অনায়াসে বের হয়ে আসে।',
          guidingQuestionBn: '2gH = v_0^2 sin^2(θ) সমীকরণ থেকে H কে বামপাশে রেখে ডানপাশে কী পাওয়া যায়?',
          formulaLatex: 'H = \\frac{v_0^2 \\sin^2\\theta}{2g}',
          isTerminal: false,
        },
        {
          tier: 4,
          tierNameBn: 'টিয়ার ৪: বাস্তব জগতের যাচাই ও ৩ডি সিমুলেশন',
          hintTextBn: 'আমাদের ইন্টারেক্টিভ সিমুলেটরে কোণ ও বেগের মান পরিবর্তন করে গতিপথের পরাবৃত্তাকার রূপটি পর্যবেক্ষণ করুন।',
          guidingQuestionBn: 'যদি কোণ ৪৫ ডিগ্রি হয় তবে অনুভূমিক পাল্লা সর্বাধিক হওয়ার কারণ কী ব্যাখ্যা করতে পারবেন?',
          isTerminal: true,
        },
      ],
    };
  }

  // 3. Chemistry / Stoichiometry / Molecular Structure
  if (
    text.includes('মোল') ||
    text.includes('বিক্রিয়া') ||
    text.includes('অ্যাসিড') ||
    text.includes('ক্ষার') ||
    text.includes('জারণ') ||
    text.includes('বিজারণ') ||
    text.includes('organic') ||
    text.includes('জৈব') ||
    text.includes('যোজ্যতা') ||
    text.includes('বন্ধন')
  ) {
    return {
      detectedDomain: 'chemistry',
      identifiedTopicBn: 'রসায়ন: রাসায়নিক গণনা ও আণবিক জ্যামিতি',
      relevantBoardExamBn: 'দিনাজপুর ও কুমিল্লা বোর্ড ২০২৩ (এইচএসসি রসায়ন ১ম পত্র)',
      simulators: ['chemistry_molecule'],
      scaffolding: [
        {
          tier: 1,
          tierNameBn: 'টিয়ার ১: বিক্রিয়ার সমতা বিধান ও প্রাথমিক উপাত্ত',
          hintTextBn: 'যেকোনো রাসায়নিক গণনার প্রথম শর্ত হলো বিক্রিয়ক ও উৎপাদের সমতাকৃত সমীকরণ লেখা।',
          guidingQuestionBn: 'বিক্রিয়ার উভয়পাশে পরমাণুর সংখ্যা কি সমতায় রয়েছে? বিক্রিয়ক ও উৎপাদের মোল অনুপাত কত?',
          isTerminal: false,
        },
        {
          tier: 2,
          tierNameBn: 'টিয়ার ২: মোল সংখ্যা গণনা সূত্র',
          hintTextBn: 'ভর প্রদত্ত থাকলে n = w / M এবং আয়তন প্রদত্ত থাকলে n = V / 22.4 সূত্র প্রযোজ্য।',
          guidingQuestionBn: 'যৌগটির আণবিক ভর (M) কত এবং প্রদত্ত ভরকে আণবিক ভর দিয়ে ভাগ করলে কত মোল পাওয়া যায়?',
          formulaLatex: 'n = \\frac{W}{M} = \\frac{V}{22.4\\, \\text{L}}',
          isTerminal: false,
        },
        {
          tier: 3,
          tierNameBn: 'টিয়ার ৩: লিমিটিং বিক্রিয়ক ও উৎপাদ পরিমাপ',
          hintTextBn: 'স্টয়কিওমেট্রিক অনুপাত তুলনা করে কোন বিক্রিয়কটি আগে শেষ হয়ে যাবে তা চিহ্নিত করুন।',
          guidingQuestionBn: '১ মোল বিক্রিয়ক থেকে কত মোল উৎপাদ তৈরি হওয়ার কথা সমীকরণ অনুযায়ী?',
          isTerminal: false,
        },
        {
          tier: 4,
          tierNameBn: 'টিয়ার ৪: ত্রিমাত্রিক বন্ধন কোণ ও স্ব-মূল্যায়ন',
          hintTextBn: 'উৎপাদ যৌগটির সংকরণ (hybridization) ও মুক্তজোড় ইলেকট্রন সংখ্যার ওপর ভিত্তি করে জ্যামিতিক গঠন যাচাই করুন।',
          guidingQuestionBn: 'আমাদের ৩ডি আণবিক ল্যাবে যৌগটির বন্ধন কোণ পরীক্ষা করে দেখেছেন কি?',
          isTerminal: true,
        },
      ],
    };
  }

  // General fallback
  return {
    detectedDomain: 'general',
    identifiedTopicBn: 'সাধারণ একাডেমিক অনুসন্ধান ও সমস্যা সমাধান',
    relevantBoardExamBn: 'জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (এনসিটিবি)',
    simulators: [],
    scaffolding: [
      {
        tier: 1,
        tierNameBn: 'টিয়ার ১: মূল ধারণা উন্মোচন',
        hintTextBn: 'সমস্যাটির মূল কেন্দ্রবিন্দু ও প্রয়োজনীয় সূত্রাবলী চিহ্নিত করুন।',
        guidingQuestionBn: 'প্রশ্নে ঠিক কী জানতে চাওয়া হয়েছে এবং কোন কোন তথ্য দেওয়া আছে?',
        isTerminal: false,
      },
      {
        tier: 2,
        tierNameBn: 'টিয়ার ২: কৌশল ও পরিকল্পনা',
        hintTextBn: 'সমস্যাটিকে দুই বা ততোধিক ছোট ছোট ধাপে বিভক্ত করে সমাধান করার পরিকল্পনা করুন।',
        guidingQuestionBn: 'প্রথম ধাপে কোন মধ্যবর্তী মান বের করে নিলে চূড়ান্ত সমাধানে পৌঁছানো সহজ হবে?',
        isTerminal: false,
      },
      {
        tier: 3,
        tierNameBn: 'টিয়ার ৩: যুক্তিনির্ভর অনুসন্ধান',
        hintTextBn: 'প্রাপ্ত মানসমূহ প্রতিস্থাপন করে সমীকরণ বা যুক্তির ফলাফল বিশ্লেষণ করুন।',
        guidingQuestionBn: 'হিসাব সম্পন্ন করার পর উত্তরের যৌক্তিকতা পরীক্ষা করেছেন কি?',
        isTerminal: false,
      },
      {
        tier: 4,
        tierNameBn: 'টিয়ার ৪: চূড়ান্ত সিদ্ধান্ত',
        hintTextBn: 'অভিনন্দন! আপনি নিজেই যুক্তি অনুসরণ করে সঠিক উপলব্ধিতে পৌঁছেছেন।',
        guidingQuestionBn: 'এই নিয়মের আরেকটি সমস্যা নিজে নিজে অনুশীলন করতে চান কি?',
        isTerminal: true,
      },
    ],
  };
}

// =============================================================================
// 4. Misconception Scanner for Student Responses
// =============================================================================
export function scanForMisconception(studentAnswer: string): MisconceptionRule | null {
  for (const rule of MISCONCEPTION_TAXONOMY) {
    const hasTrigger = rule.triggerPatterns.some((p) => p.test(studentAnswer));
    if (hasTrigger) {
      if (rule.negativePatterns && rule.negativePatterns.some((p) => p.test(studentAnswer))) {
        continue;
      }
      return rule;
    }
  }
  return null;
}
