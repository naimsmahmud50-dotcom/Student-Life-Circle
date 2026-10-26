/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Institutional Terms of Service & Privacy Charter Page
 * TOPIC:     Phase 120 Grand Nationwide Rollout & Public Launch Sign-off
 * FILE:      frontend/src/pages/terms.tsx
 * PHASE:     Phase 120 - Grand Nationwide Rollout & Public Launch Sign-off
 * PURPOSE:   Presents the formal scholarly terms of service, student data sovereignty
 *            guarantees, zero-video proctoring privacy charter, and guardian trust protections.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  ShieldCheck,
  Scale,
  FileText,
  CheckCircle2,
  Lock,
  BookOpen,
  Users,
  Award,
  AlertCircle,
  ArrowLeft,
  GraduationCap
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';

export default function TermsPage() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <div
      className={`min-h-screen flex flex-col font-sans transition-colors duration-200 bg-academic-paper-grain ${
        theme === 'dark' ? 'dark bg-[#070D18]' : 'bg-[#FAFAF8]'
      }`}
    >
      <AppHead
        title="প্রাতিষ্ঠানিক ব্যবহারের নীতিমালা ও গোপনীয়তা সনদ | অগ্রযাত্রা"
        description="অগ্রযাত্রা প্ল্যাটফর্মের প্রাতিষ্ঠানিক ব্যবহারের শর্তাবলী, শিক্ষার্থী ডেটা সার্বভৌমত্ব ও নজরদারি-মুক্ত পরীক্ষা নীতি।"
      />

      <Navbar
        currentStage="জাতীয় পাবলিক লঞ্চ সংস্করণ (Phase 120)"
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8 relative z-10">
        {/* Header Bar */}
        <div className="space-y-4">
          <Link
            href="/about"
            className="btn-tactile-outline inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold text-[#1B2A4A] dark:text-[#A8B7D8] transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>আমাদের সম্পর্কে ফিরে যান</span>
          </Link>

          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#F5F2EB] dark:bg-[#162032] border border-[#E2DDD3] dark:border-[#263147] text-xs font-bold text-[#0A2540] dark:text-[#E8EFF8] shadow-paper-xs">
            <Scale className="w-3.5 h-3.5 text-emerald-800 dark:text-emerald-400" />
            <span>আইনগত ও প্রাতিষ্ঠানিক সনদ • সংস্করণ ২০২৬.১</span>
          </div>

          <h1 className="text-2xl sm:text-4xl font-extrabold text-[#0A2540] dark:text-[#E8EFF8] tracking-tight font-serif-bn">
            অগ্রযাত্রা প্রাতিষ্ঠানিক ব্যবহারের নীতিমালা ও শিক্ষার্থী অধিকার সনদ
          </h1>
          <p className="text-xs sm:text-sm text-[#5A687D] dark:text-[#94A3B8]">
            সর্বশেষ পরিমার্জন: অক্টোবর ২০২৬ • কার্যকর এলাকা: গণপ্রজাতন্ত্রী বাংলাদেশ
          </p>
        </div>

        {/* Content Clauses Card */}
        <article className="bg-[#FDFCF9] dark:bg-[#111827] border border-[#E5E2DA] dark:border-[#263147] rounded-2xl p-6 sm:p-10 shadow-paper-md space-y-8 text-sm leading-relaxed text-[#2D3748] dark:text-[#CBD5E1] relative overflow-hidden notebook-margin-accent">
          {/* Preamble */}
          <div className="p-5 rounded-xl bg-[#F6F5F0] dark:bg-[#151D2A] border-l-4 border-emerald-700 dark:border-emerald-500 space-y-2">
            <h2 className="text-xs font-bold tracking-widest text-emerald-800 dark:text-emerald-400 uppercase font-mono">
              প্রস্তাবনা (Preamble)
            </h2>
            <p className="text-sm font-medium text-[#1B2A4A] dark:text-[#E2E8F0] leading-relaxed">
              অগ্রযাত্রা প্ল্যাটফর্ম বাংলাদেশের প্রতিটি শিক্ষার্থী, শিক্ষক এবং অভিভাবকের সাংবিধানিক শিক্ষার অধিকার ও
              ডিজিটাল মর্যাদার প্রতি দায়বদ্ধ। এই নীতিমালা প্ল্যাটফর্মের প্রতিটি প্রযুক্তিগত ও আইনি মিথস্ক্রিয়া পরিচালনা করে।
            </p>
          </div>

          {/* Clause 1 */}
          <section className="space-y-3 pt-2 border-t border-[#E5E2DA] dark:border-[#263147]/60">
            <div className="flex items-center gap-2 text-xs font-bold tracking-widest text-emerald-800 dark:text-emerald-400 uppercase font-mono">
              <span>ধারা ০১</span>
              <span className="w-8 h-px bg-emerald-700/30 dark:bg-emerald-400/30"></span>
            </div>
            <h3 className="text-base font-bold text-[#0A2540] dark:text-[#E8EFF8] font-serif-bn flex items-center gap-2">
              <Lock className="w-4 h-4 text-emerald-700 dark:text-emerald-400 flex-shrink-0" />
              <span>শিক্ষার্থী ডেটা সার্বভৌমত্ব ও ব্যক্তিগত সুরক্ষা</span>
            </h3>
            <p>
              ১.১. শিক্ষার্থীর নাম, রোল, পরীক্ষা ফলাফল এবং প্রাতিষ্ঠানিক পরিচয় জাতীয় সার্বভৌম ডেটা হিসাবে গণ্য।
              কোনো অবস্থাতেই এই তথ্য বাণিজ্যিক বিজ্ঞাপনদাতা, বহিরাগত এআই কর্পোরেশন বা তৃতীয় পক্ষের কাছে বিক্রি বা বিনিময় করা হবে না।
            </p>
            <p>
              ১.২. শিক্ষার্থী বা তার অভিভাবক যেকোনো সময় নিজস্ব প্রোফাইলের সম্পূর্ণ ডেটা এক্সপোর্ট অথবা স্থায়ীভাবে মুছে ফেলার
              আইনগত অধিকার সংরক্ষণ করেন।
            </p>
          </section>

          {/* Clause 2 */}
          <section className="space-y-3 pt-6 border-t border-[#E5E2DA] dark:border-[#263147]/60">
            <div className="flex items-center gap-2 text-xs font-bold tracking-widest text-emerald-800 dark:text-emerald-400 uppercase font-mono">
              <span>ধারা ০২</span>
              <span className="w-8 h-px bg-emerald-700/30 dark:bg-emerald-400/30"></span>
            </div>
            <h3 className="text-base font-bold text-[#0A2540] dark:text-[#E8EFF8] font-serif-bn flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-700 dark:text-emerald-400 flex-shrink-0" />
              <span>নজরদারি-মুক্ত পরীক্ষা অখণ্ডতা ও প্রক্টরিং নিশ্চয়তা</span>
            </h3>
            <p>
              ২.১. অগ্রযাত্রা কখনোই শিক্ষার্থীর মুখমণ্ডলের ভিডিও রেকর্ডিং, চোখের পলক পর্যবেক্ষণ (Eye-tracking) বা ব্যক্তিগত কক্ষের
              ভিডিও ধারণ করে না।
            </p>
            <p>
              ২.২. পরীক্ষা সততা বজায় রাখতে কেবল অ-আক্রমণাত্মক ব্রাউজার ইভেন্ট (ট্যাব পরিবর্তন, উইন্ডো ব্লার সময়কাল) পরিমাপ করা হয়
              এবং প্রতিটি জমা দেওয়া উত্তরপত্র অপরিবর্তনীয় SHA-256 ক্রিপ্টোগ্রাফিক হ্যাশ সিলের মাধ্যমে সুরক্ষিত থাকে।
            </p>
          </section>

          {/* Clause 3 */}
          <section className="space-y-3 pt-6 border-t border-[#E5E2DA] dark:border-[#263147]/60">
            <div className="flex items-center gap-2 text-xs font-bold tracking-widest text-emerald-800 dark:text-emerald-400 uppercase font-mono">
              <span>ধারা ০৩</span>
              <span className="w-8 h-px bg-emerald-700/30 dark:bg-emerald-400/30"></span>
            </div>
            <h3 className="text-base font-bold text-[#0A2540] dark:text-[#E8EFF8] font-serif-bn flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-700 dark:text-emerald-400 flex-shrink-0" />
              <span>টিউশন ফি এসক্রো সুরক্ষা ও অভিভাবক ট্রাস্ট</span>
            </h3>
            <p>
              ৩.১. টিউশন ব্যবস্থার ক্ষেত্রে সমস্ত আর্থিক লেনদেন অগ্রযাত্রা সিকিউর এসক্রো ভল্টে সংরক্ষিত থাকে। শিক্ষক কর্তৃক
              পাঠদান সম্পন্ন এবং অভিভাবকের ডিজিটাল ট্রাস্ট কনসোলে অনুমোদন ব্যতিরেকে কোনো অর্থ ছাড় করা হয় না।
            </p>
            <p>
              ৩.২. অপ্রাপ্তবয়স্ক শিক্ষার্থীর যেকোনো টিউশন বুকিং ও ডেটা শেয়ারিংয়ে অভিভাবকের ওটিপি (OTP) ও লিখিত ডিজিটাল সম্মতি বাধ্যতামূলক।
            </p>
          </section>

          {/* Clause 4 */}
          <section className="space-y-3 pt-6 border-t border-[#E5E2DA] dark:border-[#263147]/60">
            <div className="flex items-center gap-2 text-xs font-bold tracking-widest text-emerald-800 dark:text-emerald-400 uppercase font-mono">
              <span>ধারা ০৪</span>
              <span className="w-8 h-px bg-emerald-700/30 dark:bg-emerald-400/30"></span>
            </div>
            <h3 className="text-base font-bold text-[#0A2540] dark:text-[#E8EFF8] font-serif-bn flex items-center gap-2">
              <Award className="w-4 h-4 text-emerald-700 dark:text-emerald-400 flex-shrink-0" />
              <span>মেধা বৃত্তি ও নিরপেক্ষ ট্রাইব্যুনাল সালিশি</span>
            </h3>
            <p>
              ৪.১. জাতীয় মেধা বৃত্তি বণ্টন ১০০% গাণিতিক যোগ্যতা এবং যাচাইকৃত প্রাতিষ্ঠানিক স্কোরের ভিত্তিতে স্বয়ংক্রিয়ভাবে পরিচালিত হয়।
              কোনো রাজনৈতিক বা আর্থিক পক্ষপাতিত্বের সুযোগ নেই।
            </p>
            <p>
              ৪.২. যেকোনো পরীক্ষার ফলাফল বা গ্রেডিং নিয়ে অসন্তোষ দেখা দিলে নিরপেক্ষ জুরি ও শিক্ষাবিদদের সমন্বয়ে গঠিত একাডেমিক
              সালিশি ট্রাইব্যুনাল কর্তৃক স্বচ্ছ পুনঃমূল্যায়ন নিশ্চিত করা হয়।
            </p>
          </section>

          {/* Clause 5 */}
          <section className="space-y-3 pt-6 border-t border-[#E5E2DA] dark:border-[#263147]/60">
            <div className="flex items-center gap-2 text-xs font-bold tracking-widest text-emerald-800 dark:text-emerald-400 uppercase font-mono">
              <span>ধারা ০৫</span>
              <span className="w-8 h-px bg-emerald-700/30 dark:bg-emerald-400/30"></span>
            </div>
            <h3 className="text-base font-bold text-[#0A2540] dark:text-[#E8EFF8] font-serif-bn flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-emerald-700 dark:text-emerald-400 flex-shrink-0" />
              <span>অফলাইন পিয়ার-টু-পিয়ার শিক্ষাক্রম সমতা</span>
            </h3>
            <p>
              ৫.১. বাংলাদেশের প্রত্যন্ত চরাঞ্চল, হাওর ও পাহাড়ি অঞ্চলের যেসকল শিক্ষার্থীর নিয়মিত ইন্টারনেট সুবিধা নেই,
              তাদের জন্য অফলাইন মেশ স্টেশনের মাধ্যমে পূর্ণ শিক্ষাক্রম ও পরীক্ষা গ্রহণের ব্যবস্থা নিশ্চিত করা হয়েছে।
            </p>
            <p>
              ৫.২. অফলাইন ও অনলাইন শিক্ষার্থীদের মেধা মূল্যায়নে কোনো বৈষম্য করা হবে না।
            </p>
          </section>
        </article>
      </main>

      <Footer theme={theme} />
    </div>
  );
}
