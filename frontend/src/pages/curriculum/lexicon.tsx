/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Bilingual Curriculum Engine & NCTB Terminology Lexicon
 * TOPIC:     Phase 136 Instant Medium Switcher & Contextual Academic Terminology
 * FILE:      frontend/src/pages/curriculum/lexicon.tsx
 * PHASE:     Phase 136 - Dual-Curriculum Bilingual Terminology Switcher
 * PURPOSE:   Provides interactive bilingual NCTB terminology exploration,
 *            side-by-side dual-column curriculum viewing, and 1-click exam paper
 *            localization between Bangla Medium and English Version tracks.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Pure Academic Design, NCTB Aligned
 */

import React, { useState, useMemo } from 'react';
import Link from 'next/link';
import {
  BookOpen,
  Languages,
  Columns,
  Layers,
  Search,
  FileText,
  CheckCircle2,
  ArrowRightLeft,
  Sparkles,
  GraduationCap,
  Bookmark,
  Compass,
  Check,
  Copy,
  Sliders,
  HelpCircle,
  ChevronRight,
  ExternalLink
} from 'lucide-react';
import { AppHead } from '../../components/layout/Head';
import { Navbar } from '../../components/layout/Navbar';
import { Footer } from '../../components/layout/Footer';
import { toBengaliDigits } from '../../lib/i18n';

type AcademicMedium = 'BANGLA' | 'ENGLISH_VERSION' | 'BILINGUAL_DUAL' | 'INLINE_ANNOTATED';
type SubjectFilter = 'ALL' | 'PHYSICS' | 'CHEMISTRY' | 'HIGHER_MATH' | 'BIOLOGY';

interface LexiconItem {
  id: string;
  termEn: string;
  termBn: string;
  phoneticEn: string;
  phoneticBn: string;
  subject: SubjectFilter;
  subjectBn: string;
  gradeTier: 'SSC' | 'HSC';
  nctbCode: string;
  definitionEn: string;
  definitionBn: string;
  formula?: string;
}

const BENCHMARK_LEXICON_DATA: LexiconItem[] = [
  {
    id: 'LEX-PHY-001',
    termEn: 'Kinematics',
    termBn: 'গতিবিদ্যা',
    phoneticEn: '/ˌkɪn.əˈmæt.ɪks/',
    phoneticBn: 'গতিবিদ্যা',
    subject: 'PHYSICS',
    subjectBn: 'পদার্থবিজ্ঞান',
    gradeTier: 'HSC',
    nctbCode: 'NCTB-PHY-C02-KINEMATICS',
    definitionEn: 'Branch of classical mechanics that describes the motion of points, bodies, and systems of bodies without considering the forces that cause them to move.',
    definitionBn: 'বলবিদ্যার যে শাখায় গতির কারণ বা বলের প্রভাব বিবেচনা না করে কেবল বস্তুর অবস্থান, সরণ, দ্রুতি, বেগ ও ত্বরণ নিয়ে সুশৃঙ্খল আলোচনা করা হয়।',
    formula: 'v = u + at, \\quad s = ut + \\frac{1}{2}at^2'
  },
  {
    id: 'LEX-PHY-002',
    termEn: 'Periodic Motion',
    termBn: 'পর্যায়বৃত্ত গতি',
    phoneticEn: '/ˌpɪr.iˈɑː.dɪk ˈmoʊ.ʃən/',
    phoneticBn: 'পর্যায়বৃত্ত গতি',
    subject: 'PHYSICS',
    subjectBn: 'পদার্থবিজ্ঞান',
    gradeTier: 'HSC',
    nctbCode: 'NCTB-PHY-C08-PERIODIC',
    definitionEn: 'Motion repeated in equal intervals of time, where a particle passes through a specific point in a definite direction at fixed periods.',
    definitionBn: 'কোনো গতিশীল কণার গতি যদি এমন হয় যে এটি এর গতিপথের কোনো নির্দিষ্ট বিন্দুকে নির্দিষ্ট সময় পর পর একই দিক থেকে অতিক্রম করে।',
    formula: 'T = 2\\pi \\sqrt{\\frac{L}{g}}'
  },
  {
    id: 'LEX-CHE-001',
    termEn: 'Periodic Table',
    termBn: 'পর্যায় সারণি',
    phoneticEn: '/ˌpɪr.iˈɑː.dɪk ˈteɪ.bəl/',
    phoneticBn: 'পর্যায় সারণি',
    subject: 'CHEMISTRY',
    subjectBn: 'রসায়ন',
    gradeTier: 'SSC',
    nctbCode: 'NCTB-CHE-C04-PERIODIC',
    definitionEn: 'Tabular display of chemical elements arranged by atomic number, electron configuration, and recurring chemical properties.',
    definitionBn: 'মৌলসমূহের ভৌত ও রাসায়নিক ধর্মের পর্যায়ক্রমিক পুনরাবৃত্তি প্রদর্শনকারী পারমাণবিক সংখ্যার ভিত্তিতে বিন্যস্ত আন্তর্জাতিক সারণি।',
    formula: 'Group 1 to 18, Period 1 to 7'
  },
  {
    id: 'LEX-CHE-002',
    termEn: 'Acid-Base Equilibrium',
    termBn: 'অম্ল-ক্ষারক সাম্যাবস্থা',
    phoneticEn: '/ˈæs.ɪd beɪs ˌiː.kwəˈlɪb.ri.əm/',
    phoneticBn: 'অম্ল-ক্ষারক সাম্যাবস্থা',
    subject: 'CHEMISTRY',
    subjectBn: 'রসায়ন',
    gradeTier: 'HSC',
    nctbCode: 'NCTB-CHE-C05-ACID-BASE',
    definitionEn: 'State of chemical balance in a solution involving proton donation and acceptance according to Brønsted–Lowry theory.',
    definitionBn: 'ব্রনস্টেড-লাউরি মতবাদ অনুসারে জলীয় দ্রবণে প্রোটন দান ও গ্রহণের গতিশীল রাসায়নিক ভারসাম্য অবস্থা।',
    formula: '\\text{pH} = -\\log[H^+]'
  },
  {
    id: 'LEX-MAT-001',
    termEn: 'Differentiation',
    termBn: 'অন্তরীকরণ',
    phoneticEn: '/ˌdɪf.əˌrɛn.ʃiˈeɪ.ʃən/',
    phoneticBn: 'অন্তরীকরণ',
    subject: 'HIGHER_MATH',
    subjectBn: 'উচ্চতর গণিত',
    gradeTier: 'HSC',
    nctbCode: 'NCTB-MAT-C09-CALCULUS',
    definitionEn: 'Mathematical process of calculating the instantaneous rate of change of a function with respect to one of its variables.',
    definitionBn: 'কোনো ফাংশনের স্বাধীন চলকের অতি ক্ষুদ্র পরিবর্তনের সাপেক্ষে অধীন চলকের পরিবর্তনের তাৎক্ষণিক হার নির্ণয়ের গাণিতিক প্রক্রিয়া।',
    formula: '\\frac{df}{dx} = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}'
  },
  {
    id: 'LEX-MAT-002',
    termEn: 'Trigonometric Ratio',
    termBn: 'ত্রিকোণমিতিক অনুপাত',
    phoneticEn: '/ˌtrɪɡ.ə.nəˈmɛt.rɪk ˈreɪ.ʃi.oʊ/',
    phoneticBn: 'ত্রিকোণমিতিক অনুপাত',
    subject: 'HIGHER_MATH',
    subjectBn: 'উচ্চতর গণিত',
    gradeTier: 'SSC',
    nctbCode: 'NCTB-MAT-C08-TRIGONOMETRY',
    definitionEn: 'Ratios of sides of a right-angled triangle with respect to its acute angles (sine, cosine, tangent).',
    definitionBn: 'সমকোণী ত্রিভুজের সূক্ষ্মকোণের সাপেক্ষে বাহুগুলোর মধ্যকার নির্দিষ্ট অনুপাত (সাইন, কোসাইন, ট্যানজেন্ট ইত্যাদি)।',
    formula: '\\sin^2\\theta + \\cos^2\\theta = 1'
  },
  {
    id: 'LEX-BIO-001',
    termEn: 'Photosynthesis',
    termBn: 'সালোকসংশ্লেষণ',
    phoneticEn: '/ˌfoʊ.toʊˈsɪn.θə.sɪs/',
    phoneticBn: 'সালোকসংশ্লেষণ',
    subject: 'BIOLOGY',
    subjectBn: 'জীববিজ্ঞান',
    gradeTier: 'SSC',
    nctbCode: 'NCTB-BIO-C04-BIOENERGETICS',
    definitionEn: 'Biological process by which green plants transform light energy into chemical energy in the form of glucose.',
    definitionBn: 'যে শারীরবৃত্তীয় প্রক্রিয়ায় সবুজ উদ্ভিদ সূর্যালোক ও ক্লোরোফিলের উপস্থিতিতে পানি ও কার্বন ডাই-অক্সাইড থেকে শর্করা জাতীয় খাদ্য তৈরি করে।',
    formula: '6CO_2 + 12H_2O \\rightarrow C_6H_{12}O_6 + 6O_2 + 6H_2O'
  }
];

interface ExamQuestion {
  id: string;
  subjectBn: string;
  subjectEn: string;
  promptBn: string;
  promptEn: string;
  optionsBn: string[];
  optionsEn: string[];
  correctIndex: number;
  explanationBn: string;
  explanationEn: string;
  keyTerms: { bn: string; en: string }[];
}

const BENCHMARK_EXAM_QUESTIONS: ExamQuestion[] = [
  {
    id: 'Q-01',
    subjectBn: 'পদার্থবিজ্ঞান (গতিবিদ্যা)',
    subjectEn: 'Physics (Kinematics)',
    promptBn: 'গতিবিদ্যা অনুসারে, কোনো বস্তুর সমত্বরণে যাত্রার ক্ষেত্রে নিচের কোন সমীকরণটি সঠিক নয়?',
    promptEn: 'According to Kinematics, which of the following equations is incorrect for a body moving with uniform acceleration?',
    optionsBn: [
      'v = u + at',
      's = ut + (1/2)at^2',
      'v^2 = u^2 + 2as',
      's = (u + v)t^2'
    ],
    optionsEn: [
      'v = u + at',
      's = ut + (1/2)at^2',
      'v^2 = u^2 + 2as',
      's = (u + v)t^2'
    ],
    correctIndex: 3,
    explanationBn: 'সঠিক দূরত্বের সূত্র হলো s = ((u + v) / 2) * t, অতএব s = (u + v)t^2 সমীকরণটি ত্রুটিপূর্ণ।',
    explanationEn: 'The correct formula for distance is s = ((u + v) / 2) * t; therefore, s = (u + v)t^2 is incorrect.',
    keyTerms: [{ bn: 'গতিবিদ্যা', en: 'Kinematics' }, { bn: 'সমত্বরণ', en: 'Uniform Acceleration' }]
  },
  {
    id: 'Q-02',
    subjectBn: 'রসায়ন (পর্যায় সারণি)',
    subjectEn: 'Chemistry (Periodic Table)',
    promptBn: 'আধুনিক পর্যায় সারণিতে পর্যায় বৃত্তাকার ধর্মের মধ্যে নিচের কোনটির মান বাম থেকে ডানে হ্রাস পায়?',
    promptEn: 'In the modern Periodic Table, which of the following periodic properties decreases from left to right across a period?',
    optionsBn: [
      'পারমাণবিক ব্যাসার্ধ (Atomic Radius)',
      'আয়নীকরণ শক্তি (Ionization Energy)',
      'ইলেকট্রন আসক্তি (Electron Affinity)',
      'তড়িৎ ঋণাত্মকতা (Electronegativity)'
    ],
    optionsEn: [
      'Atomic Radius',
      'Ionization Energy',
      'Electron Affinity',
      'Electronegativity'
    ],
    correctIndex: 0,
    explanationBn: 'একই পর্যায়ে বাম থেকে ডানে প্রোটন সংখ্যা বৃদ্ধি পাওয়ায় নিউক্লিয়াসের আকর্ষণ বৃদ্ধি পায়, ফলে পারমাণবিক ব্যাসার্ধ হ্রাস পায়।',
    explanationEn: 'Across a period from left to right, increasing nuclear effective charge attracts electrons more tightly, decreasing the atomic radius.',
    keyTerms: [{ bn: 'পর্যায় সারণি', en: 'Periodic Table' }, { bn: 'পারমাণবিক ব্যাসার্ধ', en: 'Atomic Radius' }]
  },
  {
    id: 'Q-03',
    subjectBn: 'উচ্চতর গণিত (অন্তরীকরণ)',
    subjectEn: 'Higher Math (Differentiation)',
    promptBn: 'অন্তরীকরণ প্রক্রিয়ায় d/dx (sin x) এর মান কত?',
    promptEn: 'In the mathematical process of Differentiation, what is the derivative d/dx (sin x)?',
    optionsBn: [
      '- cos x',
      'cos x',
      'tan x',
      '- sin x'
    ],
    optionsEn: [
      '- cos x',
      'cos x',
      'tan x',
      '- sin x'
    ],
    correctIndex: 1,
    explanationBn: 'ক্যালকুলাসের স্ট্যান্ডার্ড সূত্র অনুসারে d/dx (sin x) = cos x।',
    explanationEn: 'By standard differentiation principles in calculus, d/dx (sin x) = cos x.',
    keyTerms: [{ bn: 'অন্তরীকরণ', en: 'Differentiation' }]
  }
];

export default function CurriculumLexiconPage() {
  const [activeMedium, setActiveMedium] = useState<AcademicMedium>('BANGLA');
  const [selectedSubject, setSelectedSubject] = useState<SubjectFilter>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [showExplanation, setShowExplanation] = useState<Record<string, boolean>>({});
  const [copiedId, setCopiedId] = useState<string | null>(null);

  // Filtered Lexicon Entries
  const filteredLexicon = useMemo(() => {
    return BENCHMARK_LEXICON_DATA.filter((item) => {
      const matchSubj = selectedSubject === 'ALL' || item.subject === selectedSubject;
      if (!matchSubj) return false;
      if (!searchQuery.trim()) return true;

      const q = searchQuery.toLowerCase().trim();
      return (
        item.termEn.toLowerCase().includes(q) ||
        item.termBn.includes(q) ||
        item.nctbCode.toLowerCase().includes(q) ||
        item.definitionEn.toLowerCase().includes(q) ||
        item.definitionBn.includes(q)
      );
    });
  }, [selectedSubject, searchQuery]);

  const handleCopyTerm = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const toggleExplanation = (qId: string) => {
    setShowExplanation((prev) => ({ ...prev, [qId]: !prev[qId] }));
  };

  return (
    <>
      <AppHead
        title="দ্বিভাষিক এনসিটিবি কারিকুলাম ও পরিভাষা লেক্সিকন | স্টুডেন্ট লাইফ সার্কেল"
        description="এনসিটিবি বিজ্ঞান ও গণিত বিষয়ের শতভাগ নির্ভুল বাংলা মাধ্যম ও ইংলিশ ভার্সন দ্বিভাষিক পরিভাষা অভিধান এবং রিয়েল-টাইম প্রশ্নপত্র লোকালাইজেশন প্ল্যাটফর্ম।"
      />

      <div className="min-h-screen bg-[#F8FAFC] text-slate-800 flex flex-col font-sans">
        <Navbar />

        <main className="flex-grow py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
          {/* Breadcrumb Navigation */}
          <div className="mb-6">
            <div className="flex items-center gap-2 text-xs text-slate-500 mb-2">
              <Link href="/" className="hover:text-[#0A2540] transition-colors">হোম</Link>
              <span>/</span>
              <span className="text-[#0A2540] font-semibold">এনসিটিবি পাঠ্যক্রম রূপান্তর</span>
              <span>/</span>
              <span className="text-slate-400">দ্বিভাষিক লেক্সিকন ও মাধ্যম সুইচ (Phase 136)</span>
            </div>

            {/* Academic Journal Top Banner */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[#0A2540] text-white p-6 rounded-xl shadow-sm border border-slate-700">
              <div className="space-y-1">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 bg-emerald-500/20 text-emerald-400 rounded border border-emerald-500/30">
                    <Languages className="w-5 h-5" />
                  </div>
                  <h1 className="text-xl sm:text-2xl font-bold tracking-tight">
                    দ্বিভাষিক কারিকুলাম ও এনসিটিবি পরিভাষা লেক্সিকন
                  </h1>
                </div>
                <p className="text-xs text-slate-300 max-w-3xl">
                  বাংলা মাধ্যম (Bangla Medium) ও ইংলিশ ভার্সন (English Version) শিক্ষার্থীদের জন্য বিজ্ঞান ও গণিত বিষয়ের স্ট্যান্ডার্ড পারিভাষিক ম্যাপিং, সাইড-বাই-সাইড প্রশ্নপত্র প্রিভিউ ও কনটেক্সচুয়াল ডেফিনিশন।
                </p>
              </div>

              {/* Status Badge */}
              <div className="flex items-center gap-3 bg-[#051329] px-4 py-2.5 rounded-lg border border-emerald-500/40">
                <div className="p-1.5 bg-emerald-500/20 rounded-full text-emerald-400">
                  <BookOpen className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-[10px] text-emerald-400 font-bold uppercase tracking-wider">
                    এনসিটিবি স্ট্যান্ডার্ড: একাদশ-দ্বাদশ ও নবম-দশম
                  </div>
                  <div className="text-xs font-mono text-slate-200">
                    লেক্সিকন ভাণ্ডার: {toBengaliDigits(BENCHMARK_LEXICON_DATA.length)}টি প্রমিত পরিভাষা
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Medium Switcher Control Bar */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm mb-8">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <Sliders className="w-4 h-4 text-[#B45309]" />
                <span className="text-xs font-bold text-[#0A2540] uppercase tracking-wide">
                  প্রশ্নপত্র প্রদর্শন মোড নির্বাচন করুন (Medium Switcher):
                </span>
              </div>

              {/* 3D Physical Tactile Push Switcher */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button
                  type="button"
                  onClick={() => setActiveMedium('BANGLA')}
                  className={`py-2 px-3 text-xs font-bold rounded transition-all flex items-center justify-center gap-1.5 ${
                    activeMedium === 'BANGLA'
                      ? 'bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] translate-y-0.5'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }`}
                >
                  <BookOpen className="w-3.5 h-3.5" />
                  <span>বাংলা মাধ্যম</span>
                </button>

                <button
                  type="button"
                  onClick={() => setActiveMedium('ENGLISH_VERSION')}
                  className={`py-2 px-3 text-xs font-bold rounded transition-all flex items-center justify-center gap-1.5 ${
                    activeMedium === 'ENGLISH_VERSION'
                      ? 'bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] translate-y-0.5'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }`}
                >
                  <Languages className="w-3.5 h-3.5" />
                  <span>English Version</span>
                </button>

                <button
                  type="button"
                  onClick={() => setActiveMedium('BILINGUAL_DUAL')}
                  className={`py-2 px-3 text-xs font-bold rounded transition-all flex items-center justify-center gap-1.5 ${
                    activeMedium === 'BILINGUAL_DUAL'
                      ? 'bg-[#065F46] text-white shadow-[0_4px_0_0_#044231] translate-y-0.5'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }`}
                >
                  <Columns className="w-3.5 h-3.5" />
                  <span>সাইড-বাই-সাইড</span>
                </button>

                <button
                  type="button"
                  onClick={() => setActiveMedium('INLINE_ANNOTATED')}
                  className={`py-2 px-3 text-xs font-bold rounded transition-all flex items-center justify-center gap-1.5 ${
                    activeMedium === 'INLINE_ANNOTATED'
                      ? 'bg-[#B45309] text-white shadow-[0_4px_0_0_#78350f] translate-y-0.5'
                      : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                  }`}
                >
                  <Layers className="w-3.5 h-3.5" />
                  <span>ইনলাইন টীকা</span>
                </button>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-10">
            {/* Left Column: Live Exam Paper Localization Switcher (7 cols) */}
            <div className="lg:col-span-7 space-y-6">
              <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
                <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
                  <div>
                    <h2 className="text-base font-bold text-[#0A2540] flex items-center gap-2">
                      <FileText className="w-4 h-4 text-[#B45309]" />
                      <span>লাইভ প্রশ্নপত্র লোকালাইজেশন প্রিভিউ</span>
                    </h2>
                    <p className="text-xs text-slate-500 mt-0.5">
                      নির্বাচিত মাধ্যম: <strong className="text-[#0A2540]">
                        {activeMedium === 'BANGLA' && 'বাংলা মাধ্যম (Pure Bengali)'}
                        {activeMedium === 'ENGLISH_VERSION' && 'English Version (Pure English)'}
                        {activeMedium === 'BILINGUAL_DUAL' && 'দ্বিভাষিক সমান্তরাল কলাম (Side-by-Side Parallel)'}
                        {activeMedium === 'INLINE_ANNOTATED' && 'ইনলাইন পারিভাষিক টীকাযুক্ত (Annotated Gloss)'}
                      </strong>
                    </p>
                  </div>

                  <span className="text-[11px] bg-slate-100 border border-slate-200 text-slate-600 px-2 py-1 rounded font-mono">
                    HSC/SSC বোর্ড ফরম্যাট
                  </span>
                </div>

                {/* Exam Questions Render Engine */}
                <div className="space-y-6">
                  {BENCHMARK_EXAM_QUESTIONS.map((q, qIndex) => {
                    const isDual = activeMedium === 'BILINGUAL_DUAL';
                    const isEn = activeMedium === 'ENGLISH_VERSION';
                    const isInline = activeMedium === 'INLINE_ANNOTATED';
                    const showExp = showExplanation[q.id];

                    return (
                      <div
                        key={q.id}
                        className="p-4 bg-slate-50/70 border border-slate-200 rounded-lg hover:border-slate-300 transition-all space-y-3"
                      >
                        {/* Question Header & Subject */}
                        <div className="flex items-center justify-between text-xs">
                          <span className="font-bold text-[#0A2540] flex items-center gap-1.5 font-mono">
                            <span className="w-5 h-5 bg-[#0A2540] text-white rounded-full flex items-center justify-center text-[11px]">
                              {toBengaliDigits(qIndex + 1)}
                            </span>
                            <span>{isEn ? q.subjectEn : q.subjectBn}</span>
                          </span>

                          {/* Terminology Tags */}
                          <div className="flex items-center gap-1.5 flex-wrap">
                            {q.keyTerms.map((term, tIdx) => (
                              <span
                                key={tIdx}
                                className="text-[10px] bg-emerald-50 text-emerald-800 border border-emerald-300 px-2 py-0.5 rounded font-mono"
                              >
                                {term.bn} ↔ {term.en}
                              </span>
                            ))}
                          </div>
                        </div>

                        {/* Question Prompt Body */}
                        {isDual ? (
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-white p-3.5 rounded border border-slate-200">
                            {/* Bengali Left Column */}
                            <div className="border-r md:border-r border-slate-200 pr-3 space-y-3 font-['Hind_Siliguri',sans-serif]">
                              <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wide">
                                বাংলা মাধ্যম
                              </div>
                              <p className="text-sm font-semibold text-slate-800 leading-relaxed">
                                {q.promptBn}
                              </p>
                              <div className="space-y-1.5 pt-1">
                                {q.optionsBn.map((opt, oIdx) => (
                                  <div
                                    key={oIdx}
                                    className={`text-xs p-2 rounded border flex items-center gap-2 ${
                                      oIdx === q.correctIndex && showExp
                                        ? 'bg-emerald-50 border-emerald-400 text-emerald-900 font-bold'
                                        : 'bg-slate-50 border-slate-200 text-slate-700'
                                    }`}
                                  >
                                    <span className="font-mono text-slate-400">({['ক', 'খ', 'গ', 'ঘ'][oIdx]})</span>
                                    <span>{opt}</span>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* English Right Column */}
                            <div className="pl-1 space-y-3 font-['Inter',sans-serif]">
                              <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wide">
                                English Version
                              </div>
                              <p className="text-sm font-semibold text-slate-800 leading-relaxed">
                                {q.promptEn}
                              </p>
                              <div className="space-y-1.5 pt-1">
                                {q.optionsEn.map((opt, oIdx) => (
                                  <div
                                    key={oIdx}
                                    className={`text-xs p-2 rounded border flex items-center gap-2 ${
                                      oIdx === q.correctIndex && showExp
                                        ? 'bg-emerald-50 border-emerald-400 text-emerald-900 font-bold'
                                        : 'bg-slate-50 border-slate-200 text-slate-700'
                                    }`}
                                  >
                                    <span className="font-mono text-slate-400">({['A', 'B', 'C', 'D'][oIdx]})</span>
                                    <span>{opt}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                        ) : (
                          /* Single Column View (Bangla / English / Inline Gloss) */
                          <div className="bg-white p-3.5 rounded border border-slate-200 space-y-3">
                            <p className="text-sm font-semibold text-slate-800 leading-relaxed">
                              {isEn
                                ? q.promptEn
                                : isInline
                                ? (
                                    <span>
                                      {q.promptBn.split(' ').map((word, wIdx) => {
                                        const matched = q.keyTerms.find((t) => word.includes(t.bn));
                                        if (matched) {
                                          return (
                                            <span key={wIdx}>
                                              <span className="text-[#0A2540] font-bold underline decoration-emerald-500 decoration-2">
                                                {word}
                                              </span>{' '}
                                              <span className="text-[10px] bg-emerald-100 text-emerald-800 px-1 py-0.5 rounded font-mono font-normal">
                                                ({matched.en})
                                              </span>{' '}
                                            </span>
                                          );
                                        }
                                        return word + ' ';
                                      })}
                                    </span>
                                  )
                                : q.promptBn}
                            </p>

                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                              {(isEn ? q.optionsEn : q.optionsBn).map((opt, oIdx) => (
                                <div
                                  key={oIdx}
                                  className={`text-xs p-2.5 rounded border flex items-center gap-2 ${
                                    oIdx === q.correctIndex && showExp
                                      ? 'bg-emerald-50 border-emerald-400 text-emerald-900 font-bold'
                                      : 'bg-slate-50 border-slate-200 text-slate-700'
                                  }`}
                                >
                                  <span className="font-mono text-slate-400">
                                    {isEn ? `(${['A', 'B', 'C', 'D'][oIdx]})` : `(${['ক', 'খ', 'গ', 'ঘ'][oIdx]})`}
                                  </span>
                                  <span>{opt}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Explanation Toggle & Content */}
                        <div className="flex items-center justify-between pt-1">
                          <button
                            type="button"
                            onClick={() => toggleExplanation(q.id)}
                            className="text-xs font-semibold text-[#0A2540] hover:text-emerald-700 transition-colors flex items-center gap-1"
                          >
                            <HelpCircle className="w-3.5 h-3.5" />
                            <span>{showExp ? 'ব্যাখ্যা লুকান' : 'সঠিক উত্তরের ব্যাখ্যা দেখুন'}</span>
                          </button>

                          {showExp && (
                            <span className="text-xs text-emerald-700 font-bold font-mono">
                              সঠিক বিকল্প: {isEn ? ['A', 'B', 'C', 'D'][q.correctIndex] : ['ক', 'খ', 'গ', 'ঘ'][q.correctIndex]}
                            </span>
                          )}
                        </div>

                        {showExp && (
                          <div className="p-3 bg-emerald-50/70 border border-emerald-200 rounded text-xs text-emerald-900 space-y-1">
                            <span className="font-bold block">কনসেপচুয়াল সমাধান:</span>
                            <p>{isEn ? q.explanationEn : q.explanationBn}</p>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Right Column: Searchable NCTB STEM Lexicon Explorer (5 cols) */}
            <div className="lg:col-span-5 space-y-6">
              <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
                <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                  <div className="flex items-center gap-2">
                    <Bookmark className="w-4 h-4 text-[#B45309]" />
                    <h3 className="text-sm font-bold text-[#0A2540]">
                      এনসিটিবি পারিভাষিক লেক্সিকন ভাণ্ডার
                    </h3>
                  </div>
                  <span className="text-[11px] text-slate-500 font-mono">
                    {toBengaliDigits(filteredLexicon.length)}টি ফলাফল
                  </span>
                </div>

                {/* Search Input */}
                <div className="relative">
                  <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="শব্দ খুঁজুন (যেমন: গতিবিদ্যা, Kinematics, পর্যায় সারণি)..."
                    className="w-full pl-9 pr-3 py-2 text-xs bg-slate-50 border border-slate-300 rounded focus:outline-none focus:ring-1 focus:ring-[#0A2540] text-slate-800"
                  />
                </div>

                {/* Subject Filter Pills */}
                <div className="flex items-center gap-1.5 flex-wrap">
                  {(
                    [
                      { id: 'ALL', label: 'সকল বিষয়' },
                      { id: 'PHYSICS', label: 'পদার্থবিজ্ঞান' },
                      { id: 'CHEMISTRY', label: 'রসায়ন' },
                      { id: 'HIGHER_MATH', label: 'উচ্চতর গণিত' },
                      { id: 'BIOLOGY', label: 'জীববিজ্ঞান' }
                    ] as { id: SubjectFilter; label: string }[]
                  ).map((s) => (
                    <button
                      key={s.id}
                      type="button"
                      onClick={() => setSelectedSubject(s.id)}
                      className={`text-[11px] font-semibold px-2.5 py-1 rounded transition-colors ${
                        selectedSubject === s.id
                          ? 'bg-[#0A2540] text-white shadow-xs'
                          : 'bg-slate-100 hover:bg-slate-200 text-slate-600'
                      }`}
                    >
                      {s.label}
                    </button>
                  ))}
                </div>

                {/* Lexicon Term Cards List */}
                <div className="max-h-[560px] overflow-y-auto space-y-3 pr-1">
                  {filteredLexicon.length === 0 ? (
                    <div className="text-center py-8 text-xs text-slate-500">
                      কোনো পরিভাষা খুঁজে পাওয়া যায়নি।
                    </div>
                  ) : (
                    filteredLexicon.map((term) => (
                      <div
                        key={term.id}
                        className="p-3.5 bg-slate-50 border border-slate-200 rounded-lg hover:border-slate-300 transition-all space-y-2 text-xs"
                      >
                        {/* Term Title & Copy Action */}
                        <div className="flex items-start justify-between gap-2">
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-sm text-[#0A2540] font-['Hind_Siliguri',sans-serif]">
                                {term.termBn}
                              </span>
                              <span className="text-slate-400">↔</span>
                              <span className="font-bold text-sm text-slate-900 font-['Inter',sans-serif]">
                                {term.termEn}
                              </span>
                            </div>
                            <div className="text-[10px] text-slate-400 font-mono mt-0.5">
                              উচ্চারণ: {term.phoneticEn}
                            </div>
                          </div>

                          <button
                            type="button"
                            onClick={() => handleCopyTerm(`${term.termBn} (${term.termEn})`, term.id)}
                            className="text-slate-400 hover:text-slate-700 transition-colors p-1"
                            title="কপি করুন"
                          >
                            {copiedId === term.id ? (
                              <Check className="w-3.5 h-3.5 text-emerald-600" />
                            ) : (
                              <Copy className="w-3.5 h-3.5" />
                            )}
                          </button>
                        </div>

                        {/* Subject & NCTB Code Badges */}
                        <div className="flex items-center gap-2 flex-wrap text-[10px]">
                          <span className="bg-slate-200 text-slate-700 px-1.5 py-0.5 rounded font-semibold">
                            {term.subjectBn}
                          </span>
                          <span className="bg-blue-50 text-blue-700 border border-blue-200 px-1.5 py-0.5 rounded font-mono">
                            {term.gradeTier}
                          </span>
                          <span className="bg-amber-50 text-amber-800 border border-amber-200 px-1.5 py-0.5 rounded font-mono">
                            {term.nctbCode}
                          </span>
                        </div>

                        {/* Formula if applicable */}
                        {term.formula && (
                          <div className="p-2 bg-slate-900 text-slate-100 rounded font-mono text-[11px] overflow-x-auto">
                            {term.formula}
                          </div>
                        )}

                        {/* Definitions */}
                        <div className="space-y-1.5 pt-1 text-[11px] text-slate-600 border-t border-slate-200/60">
                          <div>
                            <span className="font-bold text-slate-700 block">বাংলা সংজ্ঞা:</span>
                            <p className="leading-relaxed font-['Hind_Siliguri',sans-serif]">{term.definitionBn}</p>
                          </div>
                          <div>
                            <span className="font-bold text-slate-700 block">English Definition:</span>
                            <p className="leading-relaxed font-['Inter',sans-serif]">{term.definitionEn}</p>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>
        </main>

        <Footer />
      </div>
    </>
  );
}
