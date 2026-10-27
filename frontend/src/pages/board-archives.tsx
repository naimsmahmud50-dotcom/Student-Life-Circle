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

// Import authentic board seed dataset
import rawBoardQuestions from '@/data/nctb_board_past_papers_2015_2025.json';

export default function BoardArchivesPage() {
  const questions = rawBoardQuestions as BoardQuestionItem[];

  // Automatically seed and sync board questions to IndexedDB for offline access
  useEffect(() => {
    saveMultipleBoardQuestions(questions).catch((err) => {
      console.warn('[Offline Paper Vault] Sync non-fatal warning:', err);
    });
  }, [questions]);

  return (
    <div className="min-h-screen flex flex-col bg-[#FFFCF6] dark:bg-[#0B0F19] text-[#213130] dark:text-[#F5F2EB] font-sans transition-colors duration-300">
      <AppHead
        title="অফিসিয়াল এনসিটিবি বোর্ড প্রশ্ন আর্কাইভ (২০১৫-২০২৫) | অগ্রযাত্রা"
        description="বাংলাদেশ জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) অনুমোদিত এসএসসি ও এইচএসসি বিগত ১০ বছরের বোর্ড প্রশ্ন ও KaTeX গাণিতিক সমাধান ব্যাংক।"
        canonicalUrl="/board-archives"
      />

      <Navbar currentStage="বোর্ড পরীক্ষা প্রস্তুতি (SSC & HSC)" />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
        {/* Unified Flagship Editorial PageHeader */}
        <PageHeader
          category="এনসিটিবি অনুমোদিত অফিসিয়াল প্রশ্ন ব্যাংক"
          title="অফিসিয়াল বোর্ড প্রশ্ন ও গাণিতিক সমাধান আর্কাইভ"
          subtitle="২০১৫ থেকে ২০২৫ সালের ঢাকা, চট্টগ্রাম, রাজশাহী সহ সকল শিক্ষাবোর্ডের পদার্থবিজ্ঞান, রসায়ন, উচ্চতর গণিত, জীববিজ্ঞান ও আইসিটি পরীক্ষার সৃজনশীল ও বহুনির্বাচনি প্রশ্নপত্রের নির্ভরযোগ্য KaTeX সমাধান।"
          breadcrumbs={[
            { label: 'নীড়পাতা', href: '/' },
            { label: 'পাঠ্যক্রম', href: '/learn' },
            { label: 'অফিসিয়াল বোর্ড আর্কাইভ' }
          ]}
          stats={[
            { label: 'শিক্ষাবোর্ড কভারেজ', value: '১০টি বোর্ড' },
            { label: 'সংরক্ষিত সময়কাল', value: '২০১৫ — ২০২৫' },
            { label: 'গাণিতিক নির্ভুলতা', value: '১০০% KaTeX', highlight: true },
            { label: 'সমাধান পদ্ধতি', value: '৪ স্তরীয় রুব্রিক্স' }
          ]}
          action={
            <button
              type="button"
              onClick={() => {
                if (typeof window !== 'undefined') window.print();
              }}
              className="print:hidden inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#ED8E22] hover:bg-[#D47C1A] text-white font-bold text-xs font-bengali shadow-md active:scale-95 transition-all duration-150"
            >
              <Printer className="w-4 h-4 text-amber-200" />
              <span>প্রশ্নপত্র প্রিন্ট ভিউ</span>
            </button>
          }
        />

        {/* Question Archive Viewer Component */}
        <BoardQuestionArchiveViewer initialQuestions={questions} />

        {/* Academic Integrity & Study Tips Section */}
        <section className="print:hidden mt-12 bg-[#FFF9EB]/70 dark:bg-[#121B2D] p-6 sm:p-8 rounded-3xl border border-amber-200/80 dark:border-[#262D3D] shadow-xs space-y-5">
          <div className="flex items-center gap-2.5 text-[#213130] dark:text-[#F5F2EB] font-bold font-bengali text-base">
            <ShieldCheck className="w-5 h-5 text-[#ED8E22]" />
            <span>বোর্ড পরীক্ষার জন্য প্রস্তুতি নির্দেশিকা ও নির্ভুলতা নিশ্চয়তা</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-bengali text-[#525252] dark:text-slate-400 leading-relaxed">
            <div className="p-5 rounded-2xl bg-white dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-2">
              <strong className="text-[#1B2A4A] dark:text-white block font-semibold text-sm">
                ১. পরীক্ষা মোডে সময় মেনে অনুশীলন
              </strong>
              <p>
                পরীক্ষা মোড চালু করে উত্তর না দেখে পূর্ণাঙ্গ উদ্দীপক সমাধান করুন। নির্দিষ্ট সময়ের মধ্যে সৃজনশীল প্রশ্নের (ক, খ, গ, ঘ) উত্তর লেখার অভ্যাস বোর্ড পরীক্ষায় সেরা ফলাফল নিশ্চিত করে।
              </p>
            </div>
            <div className="p-5 rounded-2xl bg-white dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-2">
              <strong className="text-[#1B2A4A] dark:text-white block font-semibold text-sm">
                ২. KaTeX সূত্রের নির্ভুল প্রতিপাদন
              </strong>
              <p>
                অগ্রযাত্রা প্ল্যাটফর্মের প্রতিটি গাণিতিক সমাধান উচ্চ রেজোলিউশনের সাব-পিক্সেল KaTeX ফরম্যাটে উপস্থাপিত, যা কোনো প্রতীক বা ভগ্নাংশ বিকৃত হতে দেয় না।
              </p>
            </div>
            <div className="p-5 rounded-2xl bg-white dark:bg-[#0E1526] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-2">
              <strong className="text-[#1B2A4A] dark:text-white block font-semibold text-sm">
                ৩. অফিসিয়াল প্রিন্ট প্রিভিউ
              </strong>
              <p>
                পরীক্ষার আগে অফলাইন অনুশীলনের জন্য &quot;প্রশ্নপত্র প্রিন্ট ভিউ&quot; বোতামে ক্লিক করে পরিচ্ছন্ন A4 ফরম্যাটে প্রশ্নপত্র প্রিন্ট বা PDF সংরক্ষণ করতে পারবেন।
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
