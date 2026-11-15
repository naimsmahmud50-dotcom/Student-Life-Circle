/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Official NCTB Board Question Archives Page
 * TOPIC:     Phase 138 Unified Premium Design System & Sub-pages Elevation
 * FILE:      frontend/src/pages/board-archives.tsx
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Standardized academic board question archive page with flagship
 *            PageHeader, breadcrumbs, NCTB seal, and zero-emoji design tokens.
 * STANDARDS: Zero-Emoji, Pure Academic Design, WCAG 2.2 AAA, UI/UX Pro Max
 */

import React, { useEffect } from 'react';
import {
  Award,
  BookOpen,
  CheckCircle,
  FileText,
  Printer,
  ChevronRight,
  ShieldCheck,
  Download,
  WifiOff
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { PageHeader } from '@/components/layout/PageHeader';
import {
  BoardQuestionArchiveViewer,
  BoardQuestionItem
} from '@/components/curriculum/BoardQuestionArchiveViewer';
import { saveMultipleBoardQuestions } from '@/lib/offline/offline-papers-store';
import { useTranslation, toBengaliDigits } from '@/lib/i18n';

// Import authentic board seed dataset
import rawBoardQuestions from '@/data/nctb_board_past_papers_2015_2025.json';

export default function BoardArchivesPage() {
  const { language } = useTranslation();
  const questions = rawBoardQuestions as BoardQuestionItem[];

  useEffect(() => {
    document.title = language === 'bn'
      ? 'অফিসিয়াল এনসিটিবি বোর্ড প্রশ্ন আর্কাইভ (২০১৫-২০২৫) | অগ্রযাত্রা'
      : 'Official NCTB Board Question Archives (2015-2025) | Ogrojatra';
  }, [language]);

  // Automatically seed and sync board questions to IndexedDB for offline access
  useEffect(() => {
    saveMultipleBoardQuestions(questions).catch((err) => {
      console.warn('[Offline Paper Vault] Sync non-fatal warning:', err);
    });
  }, [questions]);

  return (
    <div className="min-h-screen flex flex-col bg-[#FAFAF8] dark:bg-[#090D16] text-[#213130] dark:text-[#F5F2EB] font-sans transition-colors duration-300">
      <AppHead
        title={
          language === 'bn'
            ? 'অফিসিয়াল এনসিটিবি বোর্ড প্রশ্ন আর্কাইভ (২০১৫-২০২৫) | অগ্রযাত্রা'
            : 'Official NCTB Board Question Archives (2015-2025) | Ogrojatra'
        }
        description={
          language === 'bn'
            ? 'বাংলাদেশ জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) অনুমোদিত এসএসসি ও এইচএসসি বিগত ১০ বছরের বোর্ড প্রশ্ন ও KaTeX গাণিতিক সমাধান ব্যাংক।'
            : 'Official NCTB approved past 10 years SSC & HSC board examination questions and verified KaTeX mathematical solutions.'
        }
        canonicalUrl="/board-archives"
      />

      <Navbar currentStage={language === 'bn' ? 'বোর্ড পরীক্ষা প্রস্তুতি (SSC & HSC)' : 'Board Exam Preparation (SSC & HSC)'} />

      {/* Unified Flagship Editorial PageHeader with ARCHIVES Watermark */}
      <PageHeader
        watermarkText="ARCHIVES"
        category={language === 'bn' ? 'এনসিটিবি অনুমোদিত অফিসিয়াল প্রশ্ন ব্যাংক' : 'Official NCTB Approved Question Bank'}
        title={language === 'bn' ? 'অফিসিয়াল বোর্ড প্রশ্ন ও গাণিতিক সমাধান আর্কাইভ' : 'Official Board Exam Questions & Math Solutions Archive'}
        subtitle={
          language === 'bn'
            ? '২০১৫ থেকে ২০২৫ সালের ঢাকা, চট্টগ্রাম, রাজশাহী সহ সকল শিক্ষাবোর্ডের পদার্থবিজ্ঞান, রসায়ন, উচ্চতর গণিত, জীববিজ্ঞান ও আইসিটি পরীক্ষার সৃজনশীল ও বহুনির্বাচনি প্রশ্নপত্রের নির্ভরযোগ্য KaTeX সমাধান।'
            : 'Authentic Creative (CQ) and Multiple Choice (MCQ) board papers from 2015 to 2025 across Dhaka, Chittagong, Rajshahi and all boards with verified KaTeX mathematical solutions for Physics, Chemistry, Math, Biology, and ICT.'
        }
        breadcrumbs={[
          { label: language === 'bn' ? 'নীড়পাতা' : 'Home', href: '/' },
          { label: language === 'bn' ? 'পাঠ্যক্রম' : 'Curriculum', href: '/learn' },
          { label: language === 'bn' ? 'অফিসিয়াল বোর্ড আর্কাইভ' : 'Official Board Archives' }
        ]}
        stats={[
          { label: language === 'bn' ? 'শিক্ষাবোর্ড কভারেজ' : 'Board Coverage', value: language === 'bn' ? '১০টি বোর্ড' : '10 Boards' },
          { label: language === 'bn' ? 'সংরক্ষিত সময়কাল' : 'Recorded Span', value: language === 'bn' ? '২০১৫ — ২০২৫' : '2015 — 2025' },
          { label: language === 'bn' ? 'গাণিতিক নির্ভুলতা' : 'Math Precision', value: language === 'bn' ? '১০০% KaTeX' : '100% KaTeX', highlight: true },
          { label: language === 'bn' ? 'সমাধান পদ্ধতি' : 'Solution Rubric', value: language === 'bn' ? '৪ স্তরীয় রুব্রিক্স' : '4-Tier Rubrics' }
        ]}
        action={
          <button
            type="button"
            onClick={() => {
              if (typeof window !== 'undefined') window.print();
            }}
            className="print:hidden inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#ED8E22] hover:bg-[#D47C1A] text-white font-bold text-xs font-bengali shadow-[0_4px_0_0_#D47C1A] active:translate-y-1 active:shadow-none transition-all duration-150"
          >
            <Printer className="w-4 h-4 text-amber-200" />
            <span>{language === 'bn' ? 'প্রশ্নপত্র প্রিন্ট ভিউ' : 'Print Question Paper'}</span>
          </button>
        }
      />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
        {/* Question Archive Viewer Component */}
        <BoardQuestionArchiveViewer initialQuestions={questions} />

        {/* Academic Integrity & Study Tips Section */}
        <section className="print:hidden mt-12 bg-[#FFF9EB]/70 dark:bg-[#121B2D] p-6 sm:p-8 rounded-3xl border border-amber-200/80 dark:border-[#262D3D] shadow-xs space-y-5">
          <div className="flex items-center gap-2.5 text-[#213130] dark:text-[#F5F2EB] font-bold font-bengali text-base">
            <ShieldCheck className="w-5 h-5 text-[#ED8E22]" />
            <span>{language === 'bn' ? 'বোর্ড পরীক্ষার জন্য প্রস্তুতি নির্দেশিকা ও নির্ভুলতা নিশ্চয়তা' : 'Board Examination Study Guidelines & Precision Assurance'}</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-bengali text-[#525252] dark:text-slate-400 leading-relaxed">
            <div className="p-5 rounded-2xl bg-white dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-2">
              <strong className="text-[#1B2A4A] dark:text-white block font-semibold text-sm">
                {language === 'bn' ? '১. পরীক্ষা মোডে সময় মেনে অনুশীলন' : '1. Timed Practice in Exam Mode'}
              </strong>
              <p>
                {language === 'bn'
                  ? 'পরীক্ষা মোড চালু করে উত্তর না দেখে পূর্ণাঙ্গ উদ্দীপক সমাধান করুন। নির্দিষ্ট সময়ের মধ্যে সৃজনশীল প্রশ্নের (ক, খ, গ, ঘ) উত্তর লেখার অভ্যাস বোর্ড পরীক্ষায় সেরা ফলাফল নিশ্চিত করে।'
                  : 'Enable Exam Mode to solve stems without looking at solutions beforehand. Practicing timed answers for CQ parts (A, B, C, D) guarantees optimal exam results.'}
              </p>
            </div>
            <div className="p-5 rounded-2xl bg-white dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-2">
              <strong className="text-[#1B2A4A] dark:text-white block font-semibold text-sm">
                {language === 'bn' ? '২. KaTeX সূত্রের নির্ভুল প্রতিপাদন' : '2. Precision KaTeX Formula Derivations'}
              </strong>
              <p>
                {language === 'bn'
                  ? 'অগ্রযাত্রা প্ল্যাটফর্মের প্রতিটি গাণিতিক সমাধান উচ্চ রেজোলিউশনের সাব-পিক্সেল KaTeX ফরম্যাটে উপস্থাপিত, যা কোনো প্রতীক বা ভগ্নাংশ বিকৃত হতে দেয় না।'
                  : 'Every mathematical solution on Ogrojatra is typeset in high-resolution sub-pixel KaTeX format, preventing any symbol or fractional distortion.'}
              </p>
            </div>
            <div className="p-5 rounded-2xl bg-white dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-2">
              <strong className="text-[#1B2A4A] dark:text-white block font-semibold text-sm">
                {language === 'bn' ? '৩. অফিসিয়াল প্রিন্ট প্রিভিউ' : '3. Official Print Preview'}
              </strong>
              <p>
                {language === 'bn'
                  ? 'পরীক্ষার আগে অফলাইন অনুশীলনের জন্য "প্রশ্নপত্র প্রিন্ট ভিউ" বোতামে ক্লিক করে পরিচ্ছন্ন A4 ফরম্যাটে প্রশ্নপত্র প্রিন্ট বা PDF সংরক্ষণ করতে পারবেন।'
                  : 'Click the "Print Question Paper" button for clean A4 formatted printouts or PDF saves for distraction-free offline study prior to examinations.'}
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
