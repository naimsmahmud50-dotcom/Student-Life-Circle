/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Ogrojatra Platform Knowledge Graph & Feature Lexicon
 * TOPIC:     Site Omniscience, 42+ Route Capabilities & Academic Guidance Directory
 * FILE:      frontend/src/lib/socratic/platformKnowledge.ts
 * PURPOSE:   Provides complete structural and functional knowledge of all pages, tools,
 *            and services across the Ogrojatra Student Life Circle platform:
 *            1. 20 Primary educational & career services mapped with Bengali titles,
 *               routing paths, feature descriptions, and natural language trigger patterns.
 *            2. Enables Socratic AI Tutor to answer questions about site navigation,
 *               platform features, and where to find specific academic tools.
 * STANDARDS: Strict Zero-Emoji, WCAG 2.2 AAA, ASVS L2, Pure Academic Design
 */

export interface PlatformFeature {
  id: string;
  route: string;
  titleBn: string;
  category: 'academic' | 'exam' | 'career' | 'support' | 'admin' | 'tools';
  descriptionBn: string;
  howToUseBn: string;
  triggerPatterns: RegExp[];
}

export const PLATFORM_KNOWLEDGE_BASE: PlatformFeature[] = [
  // 1. Socratic Whiteboard Solver & Canvas
  {
    id: 'socratic_solver',
    route: '/socratic/solver',
    titleBn: 'সক্রেটিক হোয়াইটবোর্ড ও খাতা ওটিআর সলভার',
    category: 'academic',
    descriptionBn: 'ইন্টারঅ্যাক্টিভ এইচটিএমএল৫ পেপার ক্যানভাস, জ্যামিতিক কম্পাস ও রুলার, গণিত সংকেত প্যালেট এবং খাতার হস্তলিপি ছবি স্ক্যানার (OCR) সহ ধাপে ধাপে গাণিতিক যুক্তি সমাধানের ডিজিটাল ল্যাব।',
    howToUseBn: 'হোমপেজ বা মেনু থেকে "সক্রেটিক সলভার"-এ গিয়ে খাতার ছবি আপলোড করুন অথবা ক্যানভাসে পেন্সিল ও রুলার দিয়ে আঁকাআঁকি করে সমাধান করুন।',
    triggerPatterns: [
      /সক্রেটিক.*(সলভার|হোয়াইটবোর্ড|ক্যানভাস)/i,
      /খাতার\s*ছবি/i,
      /math\s*whiteboard/i,
      /socratic\s*solver/i,
      /হাতে\s*লেখা\s*অংক/i,
      /ocr\s*স্ক্যান/i,
      /whiteboard\s*(kothay|kivabe)/i,
      /ক্যানভাস\s*(কোথায়|কীভাবে)/i
    ]
  },

  // 2. Live Challenge 3D Arena
  {
    id: 'live_challenge',
    route: '/live-challenge',
    titleBn: 'লাইভ অ্যাকাডেমিক চ্যালেঞ্জ (৩ডি মাল্টিপ্লেয়ার এরেনা)',
    category: 'exam',
    descriptionBn: 'রিয়েল-টাইম ৩ডি অ্যাকাডেমিক অ্যারেনা যেখানে সারা বাংলাদেশের সহপাঠীদের সাথে একযোগে টাইমার ও লাইভ লিডারবোর্ডে কুইজ ও অলিম্পিয়াড প্রতিযোগিতা অনুষ্ঠিত হয়।',
    howToUseBn: 'মেনু থেকে "লাইভ চ্যালেঞ্জ" পেজে প্রবেশ করুন। রানিং বা আসন্ন চ্যালেঞ্জ সিলেক্ট করে "এরেনায় যোগ দিন" বাটনে ক্লিক করুন।',
    triggerPatterns: [
      /লাইভ\s*চ্যালেঞ্জ/i,
      /live\s*challenge/i,
      /৩ডি\s*প্রতিযোগিতা/i,
      /অন্যদের\s*সাথে\s*(প্রতিযোগিতা|যুদ্ধ|কুইজ|খেলব)/i,
      /লিডারবোর্ড/i,
      /মাল্টিপ্লেয়ার/i,
      /live\s*challenge\s*(ki|kothay|kivabe)/i,
      /challenge\s*(kothay|kivabe)/i
    ]
  },

  // 3. Admission Predictor
  {
    id: 'admission_predictor',
    route: '/admission/predictor',
    titleBn: 'বিশ্ববিদ্যালয় ভর্তি সম্ভাবনা ক্যালকুলেটর (Admission Predictor)',
    category: 'academic',
    descriptionBn: 'এসএসসি ও এইচএসসি জিপিএ এবং বিষয়ভিত্তিক নম্বর ইনপুট করে বুয়েট, ঢাকা বিশ্ববিদ্যালয়, মেডিকেল ও অন্যান্য পাবলিক বিশ্ববিদ্যালয়ে ভর্তি পরীক্ষা দেওয়ার যোগ্যতা ও সম্ভাবনা যাচাইয়ের নির্ভরযোগ্য টুল।',
    howToUseBn: 'মেনু থেকে "ভর্তি প্রস্তুতি" > "এডমিশন প্রেডিক্টর" পেজে যান। আপনার এসএসসি ও এইচএসসি ফলাফল ইনপুট করে "সম্ভাবনা হিসাব করুন" বাটনে চাপুন।',
    triggerPatterns: [
      /ভর্তি\s*(পরীক্ষা|সম্ভাবনা|প্রেডিক্টর|ক্যালকুলেটর)/i,
      /এডমিশন\s*(প্রেডিক্টর|সম্ভাবনা|পরীক্ষা|ক্যালকুলেটর)?/i,
      /admission\s*predictor/i,
      /বুয়েট.*ভর্তি.*যোগ্যতা/i,
      /মেডিকেল.*কাট\s*মার্ক/i,
      /ঢাবি.*ভর্তি/i,
      /ভর্তি\s*ক্যালকুলেটর/i,
      /buet\s*admission/i,
      /admission\s*predictor\s*(ki|kothay|kivabe)/i,
      /chance\s*pabo\s*kina/i
    ]
  },

  // 4. Board Archives (10-Year Question Bank)
  {
    id: 'board_archives',
    route: '/board-archives',
    titleBn: 'বিগত ১০ বছরের বোর্ড প্রশ্ন ও নির্ভুল সমাধান ব্যাংক',
    category: 'academic',
    descriptionBn: 'ঢাকা, চট্টগ্রাম, রাজশাহী, যশোর, সিলেটসহ সকল শিক্ষা বোর্ডের বিগত ১০ বছরের এসএসসি ও এইচএসসি পরীক্ষার প্রশ্নপত্র, অধ্যায়ভিত্তিক প্রশ্ন ও নির্ভুল সমাধান সমৃদ্ধ ডিজিটাল আর্কাইভ।',
    howToUseBn: 'মেনু থেকে "বোর্ড আর্কাইভস" পেজে গিয়ে আপনার বোর্ড, বছর ও বিষয় নির্বাচন করে প্রশ্ন ও সমাধান বিনামূল্যে ডাউনলোড বা অনলাইন স্ক্রিনে পড়ুন।',
    triggerPatterns: [
      /বিগত\s*(বছর|১০\s*বছর).*বোর্ড\s*প্রশ্ন/i,
      /বোর্ড\s*(প্রশ্ন|আর্কাইভ)/i,
      /board\s*(questions?|archives?)/i,
      /বোর্ডের\s*প্রশ্ন/i,
      /বিগত\s*বছরের\s*প্রশ্ন/i,
      /মডেল\s*টেস্ট/i,
      /question\s*bank/i,
      /প্রশ্ন\s*ব্যাংক/i,
      /board\s*questions?\s*(kothay|pabo)/i
    ]
  },

  // 5. Practice & Question Drill
  {
    id: 'practice',
    route: '/practice',
    titleBn: 'বিষয়ভিত্তিক ও অধ্যায়ভিত্তিক অনুশীলন কেন্দ্র (Practice Hub)',
    category: 'academic',
    descriptionBn: 'জাতীয় শিক্ষাক্রম (এনসিটিবি) অনুযায়ী প্রতিটি বিষয়ের প্রতিটি অধ্যায়ের শতভাগ এমসিকিউ, সৃজনশীল ও গাণিতিক সমস্যা অনুশীলনের স্বয়ংক্রিয় প্ল্যাটফর্ম।',
    howToUseBn: '"অনুশীলন" পেজে গিয়ে পদার্থ, রসায়ন, গণিত বা জীববিজ্ঞান বিষয় নির্বাচন করুন এবং পছন্দমতো অধ্যায় ক্লিক করে প্র্যাকটিস শুরু করুন।',
    triggerPatterns: [
      /অনুশীলন\s*কেন্দ্র/i,
      /practice\s*hub/i,
      /অধ্যায়ভিত্তিক\s*(অনুশীলন|এমসিকিউ)/i,
      /mcq\s*অনুশীলন/i,
      /কুইজ\s*অনুশীলন/i,
      /practice\s*(kothay|korbo)/i,
      /mcq\s*(kothay|practice)/i
    ]
  },

  // 6. Adaptive Exam (Computerized Adaptive Testing)
  {
    id: 'adaptive_exam',
    route: '/adaptive-exam',
    titleBn: 'অভিযোজিত পরীক্ষা (Adaptive Computerized Exam)',
    category: 'exam',
    descriptionBn: 'আইটেম রেসপন্স থিওরি (IRT) চালিত পরীক্ষা যেখানে শিক্ষার্থীর উত্তরের নির্ভুলতার ওপর ভিত্তি করে প্রশ্নের কাঠিন্যের মাত্রা স্বয়ংক্রিয়ভাবে পরিবর্তিত হয়।',
    howToUseBn: '"পরীক্ষা" মেনু থেকে "অভিযোজিত পরীক্ষা" বেছে নিয়ে পরীক্ষা শুরু করুন। এটি আপনার আসল মেধা স্তর নির্ণয় করে রিপোর্ট দেবে।',
    triggerPatterns: [
      /অ্যাডাপ্টিভ\s*পরীক্ষা/i,
      /adaptive\s*exam/i,
      /ক্যাট\s*পরীক্ষা/i,
      /মেধা\s*যাচাই/i,
      /আইআরটি/i,
      /irt\s*exam/i
    ]
  },

  // 7. National Olympiad Arena
  {
    id: 'olympiad_arena',
    route: '/olympiad/arena',
    titleBn: 'জাতীয় গণিত ও বিজ্ঞান অলিম্পিয়াড এরেনা',
    category: 'academic',
    descriptionBn: 'বাংলাদেশ গণিত অলিম্পিয়াড (BdMO), পদার্থবিজ্ঞান অলিম্পিয়াড (BdPhO) ও ইনফরমেটিক্স অলিম্পিয়াডের জাতীয় পর্যায়ের কঠিন ও চিন্তাশীল সমস্যা অনুশীলনের প্ল্যাটফর্ম।',
    howToUseBn: '"অলিম্পিয়াড এরেনা" পেজে প্রবেশ করে ক্যাটাগরি (প্রাইমারি, জুনিয়র, সেকেন্ডারি, হায়ার সেকেন্ডারি) অনুযায়ী সমস্যা সমাধান করুন।',
    triggerPatterns: [
      /অলিম্পিয়াড/i,
      /olympiad/i,
      /bdmo/i,
      /bdpho/i,
      /কঠিন\s*অংক\s*অনুশীলন/i,
      /math\s*olympiad/i
    ]
  },

  // 8. Caretutors-grade Tuition Marketplace
  {
    id: 'tuition',
    route: '/tuition',
    titleBn: 'যাচাইকৃত হোম ও অনলাইন টিউটরিং সংযোগ (Tuition Hub)',
    category: 'support',
    descriptionBn: 'বুয়েট, ঢাবি, মেডিকেল ও শীর্ষ বিশ্ববিদ্যালয়ের যাচাইকৃত শিক্ষক খুঁজে নেওয়ার এবং শিক্ষার্থীদের বিশ্বস্ত টিউশন পাওয়ার নিরাপদ এসক্রো ট্রাস্ট প্ল্যাটফর্ম।',
    howToUseBn: '"টিউশন" পেজে গিয়ে "টিউটর খুঁজুন" অথবা "টিউটর হতে আবেদন করুন" ফর্ম পূরণ করে সরাসরি অভিভাবক ও শিক্ষকদের সাথে যোগাযোগ করুন।',
    triggerPatterns: [
      /টিউশন/i,
      /হোম\s*টিউটর/i,
      /প্রাইভেট\s*শিক্ষক/i,
      /tuition/i,
      /tutor\s*(চাই|খুঁজছি|কই|কোথায়|পাব|dorkar)/i,
      /পড়ানো/i,
      /tuition\s*(kothay|pabo|chai)/i,
      /home\s*tutor\s*(kothay|chai)/i
    ]
  },

  // 9. Career Skill Radar
  {
    id: 'career_radar',
    route: '/career/radar',
    titleBn: 'ক্যারিয়ার স্কিল ম্যাপিং ও মার্কেট রাডার (Career Radar)',
    category: 'career',
    descriptionBn: 'বিডিজবস ও জাতীয় শ্রমবাজারের ডাটা অ্যানালিটিক্স অনুযায়ী শিক্ষার্থীর বর্তমান অ্যাকাডেমিক ব্যাকগ্রাউন্ড দিয়ে ভবিষ্যৎ সম্ভাবনাময় পেশার স্কিল গ্যাপ নিরূপণ।',
    howToUseBn: '"ক্যারিয়ার" > "স্কিল রাডার" পেজে আপনার বিষয় ও লক্ষ্য ইনপুট করে মার্কেট রেডি রাডার গ্রাফ পর্যবেক্ষণ করুন।',
    triggerPatterns: [
      /ক্যারিয়ার\s*রাডার/i,
      /career\s*radar/i,
      /ভবিষ্যৎ\s*(চাকরি|পেশা)/i,
      /স্কিল\s*গ্যাপ/i,
      /চাকরির\s*সুযোগ/i,
      /job\s*market/i
    ]
  },

  // 10. Student Dashboard
  {
    id: 'dashboard',
    route: '/dashboard',
    titleBn: 'শিক্ষার্থী সেন্ট্রাল ড্যাশবোর্ড',
    category: 'tools',
    descriptionBn: 'দৈনিক পড়ার স্ট্রিক, চলমান সিলেবাসের সমাপ্তির হার, দুর্বল অধ্যায়ের তালিকা ও সময় ব্যবস্থাপনার রুটিন সমন্বিত ব্যক্তিগত ড্যাশবোর্ড।',
    howToUseBn: 'লগইন করার পর যেকোনো সময় মেনু থেকে "ড্যাশবোর্ড"-এ ক্লিক করলেই আপনার সার্বিক অগ্রগতি এক নজরে দেখতে পাবেন।',
    triggerPatterns: [
      /ড্যাশবোর্ড/i,
      /dashboard/i,
      /আমার\s*অগ্রগতি/i,
      /পড়ার\s*স্ট্রিক/i,
      /প্রগ্রেস\s*রিপোর্ট/i,
      /study\s*streak/i
    ]
  },

  // 11. Interactive 3D Simulations Lab
  {
    id: 'simulations',
    route: '/simulations',
    titleBn: 'ইন্টারেক্টিভ ৩ডি স্টেম সিমুলেশন ল্যাব',
    category: 'academic',
    descriptionBn: 'পদার্থবিজ্ঞানের প্রাসের গতিপথ, রসায়নের অণুর সংকরণ ও বন্ধন কোণ, এবং জ্যোতির্বিজ্ঞানের মহাজাগতিক গ্লোব বাস্তবসম্মত ৩ডি ভিজ্যুয়ালাইজেশনের মাধ্যমে শেখার ল্যাব।',
    howToUseBn: '"৩ডি ল্যাব" পেজে গিয়ে প্রাস সিমুলেটরে কোণ ও বেগ পরিবর্তন করে ট্র্যাজেক্টরি পরীক্ষা করুন অথবা আণবিক ভিউয়ারে অণু ঘুরিয়ে বন্ধন কোণ মাপুন।',
    triggerPatterns: [
      /৩ডি\s*(ল্যাব|সিমুলেশন)/i,
      /simulation/i,
      /প্রাসের\s*সিমুলেটর/i,
      /অণুর\s*বন্ধন\s*কোণ/i,
      /ত্রিমাত্রিক\s*ভিজ্যুয়াল/i,
      /3d\s*(lab|simulation)/i
    ]
  },

  // 12. Scholarship Disbursement Portal
  {
    id: 'scholarship',
    route: '/scholarship/disbursement',
    titleBn: 'মেধাবৃত্তি ও শিক্ষা সহায়তা তহবিল',
    category: 'support',
    descriptionBn: 'মেধাবী ও অসচ্ছল শিক্ষার্থীদের জন্য শিক্ষা সহায়তা ও জাতীয় বৃত্তির আবেদন, ট্র্যাকিং এবং স্বচ্ছ বিতরণ পোর্টাল।',
    howToUseBn: '"শিক্ষাবৃত্তি" পেজে গিয়ে যোগ্যতা পরীক্ষা করুন এবং প্রয়োজনীয় তথ্য ও অ্যাকাডেমিক সার্টিফিকেট আপলোড করে বৃত্তির আবেদন সাবমিট করুন।',
    triggerPatterns: [
      /বৃত্তি/i,
      /স্কলারশিপ/i,
      /scholarship/i,
      /শিক্ষা\s*সাহায্য/i,
      /আর্থিক\s*সহায়তা/i,
      /scholarship\s*(kothay|kivabe)/i
    ]
  },

  // 13. Exam Routines Calendar
  {
    id: 'routines',
    route: '/routines',
    titleBn: 'জাতীয় শিক্ষা বোর্ড ও সেমিস্টার রুটিন ক্যালেন্ডার',
    category: 'academic',
    descriptionBn: 'সকল শিক্ষা বোর্ডের এসএসসি, এইচএসসি, কারিগরি ও মাদ্রাসা বোর্ডের সর্বশেষ পরীক্ষার রুটিন, সময়সূচি এবং রিভিশন ক্যালেন্ডার।',
    howToUseBn: '"রুটিন" পেজে গিয়ে আপনার পরীক্ষার স্তর (এসএসসি/এইচএসসি) নির্বাচন করে অফিসিয়াল পিডিএফ রুটিন ডাউনলোড বা প্রিন্ট করুন।',
    triggerPatterns: [
      /পরীক্ষার\s*রুটিন/i,
      /রুটিন\s*ক্যালেন্ডার/i,
      /routine/i,
      /সময়সূচি/i,
      /কবে\s*পরীক্ষা/i,
      /exam\s*routine/i,
      /routine\s*(kothay|pabo)/i
    ]
  },

  // 14. Mental Health Counseling
  {
    id: 'counseling',
    route: '/counseling',
    titleBn: 'শিক্ষার্থী মানসিক স্বাস্থ্য ও স্টাডি স্ট্রেস কাউন্সেলিং',
    category: 'support',
    descriptionBn: 'পড়াশোনার চাপ, পরীক্ষাভীতি, মনোযোগের ঘাটতি এবং ক্যারিয়ার দ্বিধা দূর করতে পেশাদার কাউন্সিলরদের গাইডলাইন ও মানসিক স্বাস্থ্য সহায়তা।',
    howToUseBn: '"কাউন্সেলিং" পেজে প্রবেশ করে আপনার সমস্যা জানিয়ে অভিজ্ঞ কাউন্সিলরের সাথে সেশনের অ্যাপয়েন্টমেন্ট বুক করুন।',
    triggerPatterns: [
      /কাউন্সেলিং/i,
      /পড়াশোনার\s*চাপ/i,
      /মানসিক\s*(স্বাস্থ্য|কষ্ট|টেনশন)/i,
      /মন\s*বসছে\s*না/i,
      /counseling/i,
      /counseling\s*(kothay|pabo)/i
    ]
  },

  // 15. Rural Offline Synchronizer
  {
    id: 'rural_sync',
    route: '/rural/synchronizer',
    titleBn: 'পল্লী ও অফলাইন স্টাডি সিংক্রোনাইজার',
    category: 'tools',
    descriptionBn: 'গ্রাম ও পাহাড়ি অঞ্চলের সীমিত ইন্টারনেটের শিক্ষার্থীদের জন্য এক ক্লিকে সম্পূর্ণ সপ্তাহের সিলেবাস ও প্রশ্ন অফলাইন মেমোরিতে সেভ করে রাখার প্রযুক্তি।',
    howToUseBn: 'ইন্টারনেট থাকাকালীন "অফলাইন সিংক্রোনাইজার" পেজে গিয়ে "অফলাইন বান্ডিল ডাউনলোড" বাটনে চাপুন; এরপর ইন্টারনেট ছাড়াও পড়তে পারবেন।',
    triggerPatterns: [
      /অফলাইন\s*(পড়া|মোড|সিংক)/i,
      /নেট\s*না\s*থাকলে/i,
      /ইন্টারনেট\s*ছাড়া/i,
      /offline\s*sync/i,
      /offline\s*mode/i,
      /গ্রামের\s*ইন্টারনেট/i
    ]
  },

  // 16. AI Viva & Practical Evaluator Lab
  {
    id: 'viva_evaluator',
    route: '/viva/evaluator',
    titleBn: 'এআই ভাইভা ও মৌখিক পরীক্ষা মূল্যায়ন ল্যাব',
    category: 'exam',
    descriptionBn: 'মেডিকেল, বিশ্ববিদ্যালয় ভর্তি ও বোর্ড ব্যবহারিক পরীক্ষার মৌখিক প্রশ্নের জন্য এআই দ্বারা পরিচালিত রিয়েল-টাইম ভাইভা সিমুলেশন এবং আত্মবিশ্বাস মূল্যায়ন ল্যাব।',
    howToUseBn: 'মেনু থেকে "ভাইভা মূল্যায়ন" পেজে যান। আপনার বিষয় সিলেক্ট করে মাইক্রোফোনের মাধ্যমে মৌখিক প্রশ্নের উত্তর দিন এবং তাৎক্ষণিক ফিডব্যাক পান।',
    triggerPatterns: [
      /ভাইভা/i,
      /viva(\s*evaluator|\s*exam)?/i,
      /মৌখিক\s*পরীক্ষা/i,
      /ব্যবহারিক\s*ভাইভা/i,
      /viva\s*(kothay|kivabe)/i
    ]
  },

  // 17. Peer Study Pod & Virtual Library
  {
    id: 'study_pod',
    route: '/study-pod',
    titleBn: 'ভার্চুয়াল স্টাডি পড ও সহপাঠী গ্রুপ ডিসকাশন',
    category: 'academic',
    descriptionBn: 'সহপাঠীদের সাথে একই সিলেবাসে ফোকাসড গ্রুপ স্টাডি, পোমোডোরো টাইমার ও পিয়ার ডিসকাশন রুম।',
    howToUseBn: '"স্টাডি পড" পেজে গিয়ে একটি নতুন পড তৈরি করুন অথবা বন্ধুদের দেওয়া পড কোড দিয়ে বিদ্যমান স্টাডি রুমে জয়েন করুন।',
    triggerPatterns: [
      /স্টাডি\s*পড/i,
      /study\s*pod/i,
      /গ্রুপ\s*স্টাডি/i,
      /বন্ধুদের\s*সাথে\s*পড়া/i,
      /group\s*study/i
    ]
  },

  // 18. Guardian & Parent-Teacher Coordination
  {
    id: 'guardian_ptc',
    route: '/guardian/ptc',
    titleBn: 'অভিভাবক ও শিক্ষক সমন্বয় পোর্টাল (PTC)',
    category: 'support',
    descriptionBn: 'সন্তানের পড়াশোনার অগ্রগতি, দৈনিক উপস্থিতি, পরীক্ষার ফলাফল এবং শিক্ষকদের সাথে সরাসরি মতামত বিনিময়ের ডিজিটাল অভিভাবক ড্যাশবোর্ড।',
    howToUseBn: '"অভিভাবক পোর্টাল"-এ প্রবেশ করে শিক্ষার্থীর স্টুডেন্ট আইডি লিঙ্ক করুন এবং সামগ্রিক অগ্রগতি পর্যবেক্ষণ করুন।',
    triggerPatterns: [
      /অভিভাবক/i,
      /guardian/i,
      /parent/i,
      /ptc/i,
      /শিক্ষক\s*অভিভাবক/i
    ]
  },

  // 19. Academic Resource Hub
  {
    id: 'academic_hub',
    route: '/academic-hub',
    titleBn: 'সেন্ট্রাল অ্যাকাডেমিক রিসোর্স হাব ও পাঠ্যক্রম',
    category: 'academic',
    descriptionBn: 'জাতীয় শিক্ষাক্রমের সকল শ্রেণির পাঠ্যবই, অধ্যায়ভিত্তিক লেকচার শিট, হ্যান্ডনোট এবং বিষয়ভিত্তিক পূর্ণাঙ্গ অ্যাকাডেমিক রিসোর্স ভাণ্ডার।',
    howToUseBn: '"অ্যাকাডেমিক হাব" পেজে যান এবং আপনার শ্রেণি ও বিষয় বেছে নিয়ে হ্যান্ডনোট ও স্টাডি মেটেরিয়াল সংগ্রহ করুন।',
    triggerPatterns: [
      /অ্যাকাডেমিক\s*হাব/i,
      /academic\s*hub/i,
      /লেকচার\s*শিট/i,
      /হ্যান্ডনোট/i,
      /পাঠ্যবই/i,
      /বই\s*কোথায়/i
    ]
  },

  // 20. Curriculum Lexicon & Formula Bank
  {
    id: 'curriculum_lexicon',
    route: '/curriculum/lexicon',
    titleBn: 'জাতীয় শিক্ষাক্রম পরিভাষা ও সূত্রকোষ (Curriculum Lexicon)',
    category: 'academic',
    descriptionBn: 'উচ্চতর গণিত, পদার্থ, রসায়ন ও জীববিজ্ঞানের সকল বৈজ্ঞানিক সূত্র, সংজ্ঞা, ধ্রুবকের মান ও ইংরেজি-বাংলা পারিভাষিক শব্দকোষ।',
    howToUseBn: '"শিক্ষাক্রম লেক্সিকন" পেজে যেকোনো বৈজ্ঞানিক শব্দ বা সূত্রের নাম লিখে সার্চ করুন এবং পূর্ণাঙ্গ প্রতিপাদন ও ব্যবহার দেখুন।',
    triggerPatterns: [
      /লেক্সিকন/i,
      /lexicon/i,
      /সূত্রকোষ/i,
      /সব\s*সূত্র/i,
      /formula\s*book/i,
      /পরিভাষা/i
    ]
  }
];

/**
 * Formats a comprehensive Bengali guidance response for a matched platform feature.
 */
export function formatPlatformFeatureResponse(feature: PlatformFeature): string {
  return (
    `[অগ্রযাত্রা প্ল্যাটফর্ম গাইড: ${feature.titleBn}]\n\n` +
    `পৃষ্ঠা লিঙ্ক: ${feature.route}\n` +
    `বিভাগ: ${feature.category.toUpperCase()}\n\n` +
    `বিবরণ:\n${feature.descriptionBn}\n\n` +
    `কীভাবে ব্যবহার করবেন:\n${feature.howToUseBn}\n\n` +
    `আপনি কি সরাসরি "${feature.titleBn}" পেজে যেতে চান? লিঙ্কটিতে ক্লিক করলেই আপনি সংশ্লিষ্ট পেজে পৌঁছে যাবেন।`
  );
}

/**
 * Searches the Platform Knowledge Base for features matching user query.
 */
export function findPlatformKnowledge(query: string): PlatformFeature | null {
  const text = query.trim();
  if (!text) return null;

  for (const feature of PLATFORM_KNOWLEDGE_BASE) {
    if (feature.triggerPatterns.some((pattern) => pattern.test(text))) {
      return feature;
    }
  }
  return null;
}
