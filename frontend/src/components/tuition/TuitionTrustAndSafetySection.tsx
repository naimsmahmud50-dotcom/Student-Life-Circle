/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Tuition Trust, Safety & FAQ Ecosystem
 * TOPIC:     CareTutors-Style 4-Pillar Safety & Bilateral Trust Architecture
 * FILE:      frontend/src/components/tuition/TuitionTrustAndSafetySection.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, High Contrast, Accessible FAQ Accordion, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { TUITION_FAQS, TuitionFAQItem } from './data/tuitionElevationData';
import {
  ShieldCheck,
  FileCheck2,
  CalendarCheck2,
  Lock,
  CreditCard,
  ChevronDown,
  ChevronUp,
  HelpCircle,
  AlertCircle,
  BadgeCheck,
} from 'lucide-react';

interface TuitionTrustAndSafetySectionProps {
  className?: string;
}

export const TuitionTrustAndSafetySection: React.FC<TuitionTrustAndSafetySectionProps> = ({
  className = '',
}) => {
  const [openFaqId, setOpenFaqId] = useState<string>('faq-g1');
  const [activeFaqTab, setActiveFaqTab] = useState<'guardian' | 'tutor'>('guardian');

  const filteredFaqs = TUITION_FAQS.filter((f) => f.category === activeFaqTab);

  const toggleFaq = (id: string) => {
    setOpenFaqId(openFaqId === id ? '' : id);
  };

  return (
    <section
      className={`space-y-12 font-bengali ${className}`}
      aria-labelledby="trust-safety-heading"
    >
      {/* 4 Pillars Grid */}
      <div className="space-y-6">
        <div className="text-center max-w-2xl mx-auto px-4">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 uppercase tracking-wider">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>নিরাপদ ও নির্ভরযোগ্য টিউশন নেটওয়ার্ক</span>
          </span>
          <h3
            id="trust-safety-heading"
            className="mt-3 text-2xl sm:text-3xl font-bold font-serif text-slate-900 dark:text-white"
          >
            কেন অগ্রযাত্রা টিউশন মার্কেটপ্লেস সবচেয়ে বিশ্বস্ত?
          </h3>
          <p className="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-400">
            শিক্ষার্থী, অভিভাবক ও শিক্ষকদের শতভাগ নিরাপত্তা নিশ্চিত করার ৪ স্তরের সুরক্ষা ব্যবস্থা
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
          {/* Pillar 1 */}
          <div className="p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-700">
              <FileCheck2 className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white leading-snug">
              ১. জাতীয় পরিচয়পত্র ও সনদ যাচাই
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              প্রতিটি শিক্ষকের জাতীয় পরিচয়পত্র (NID) এবং বিশ্ববিদ্যালয় স্টুডেন্ট আইডি ও ট্রান্সক্রিপ্ট নিখুঁতভাবে যাচাই করে ভেরিফায়েড ব্যাজ দেওয়া হয়।
            </p>
          </div>

          {/* Pillar 2 */}
          <div className="p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
            <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 flex items-center justify-center text-blue-700">
              <CalendarCheck2 className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white leading-snug">
              ২. ২ দিনের ফ্রি ট্রায়াল ক্লাস
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              শিক্ষক ও শিক্ষার্থীর বোঝাপড়া যাচাইয়ের জন্য প্রথম ২ দিন বিনামূল্যে ট্রায়াল ক্লাস। শতভাগ সন্তুষ্ট হলেই কেবল টিউশন চুক্তি নিশ্চিত করবেন।
            </p>
          </div>

          {/* Pillar 3 */}
          <div className="p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
            <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800 flex items-center justify-center text-amber-700">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white leading-snug">
              ৩. ০ টাকা অগ্রিম ও নো-স্ক্যাম নীতি
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              অভিভাবকদের কাছ থেকে কোনো রেজিস্ট্রেশন চার্জ বা অগ্রিম ফি নেওয়া হয় না। কোনো ভুয়া মিডিয়া বা অগ্রিম কমিশনের ঝামেলামুক্ত।
            </p>
          </div>

          {/* Pillar 4 */}
          <div className="p-5 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-3">
            <div className="w-10 h-10 rounded-xl bg-purple-50 dark:bg-purple-950/60 border border-purple-200 dark:border-purple-800 flex items-center justify-center text-purple-700">
              <CreditCard className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white leading-snug">
              ৪. দ্বিপাক্ষিক সম্মতি ও এসক্রো ট্রাস্ট
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              উভয় পক্ষের সম্মতি ছাড়া নম্বর উন্মুক্ত নয়। এছাড়া মাসের বেতন এসক্রো মাইলস্টোন প্রোটেকশনে সম্পূর্ণ নিরাপদ থাকে।
            </p>
          </div>
        </div>
      </div>

      {/* FAQ Accordion Section */}
      <div className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-emerald-700" />
            <h4 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">
              সাধারণ জিজ্ঞাসা (FAQ)
            </h4>
          </div>

          {/* FAQ Switcher: Guardian vs Tutor */}
          <div className="flex gap-2">
            <button
              onClick={() => setActiveFaqTab('guardian')}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeFaqTab === 'guardian'
                  ? 'bg-[#0A2540] text-white'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300'
              }`}
            >
              অভিভাবকদের প্রশ্ন
            </button>
            <button
              onClick={() => setActiveFaqTab('tutor')}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeFaqTab === 'tutor'
                  ? 'bg-[#0A2540] text-white'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300'
              }`}
            >
              শিক্ষকদের প্রশ্ন
            </button>
          </div>
        </div>

        <div className="space-y-3">
          {filteredFaqs.map((faq) => {
            const isOpen = openFaqId === faq.id;
            return (
              <div
                key={faq.id}
                className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-[#FAF8F3]/60 dark:bg-slate-950/40 overflow-hidden"
              >
                <button
                  onClick={() => toggleFaq(faq.id)}
                  aria-expanded={isOpen}
                  className="w-full p-4 text-left flex items-center justify-between gap-3 text-xs sm:text-sm font-bold text-slate-800 dark:text-white hover:text-emerald-800 transition-colors"
                >
                  <span>{faq.questionBn}</span>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-slate-400 shrink-0" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                  )}
                </button>
                {isOpen && (
                  <div className="px-4 pb-4 text-xs text-slate-600 dark:text-slate-400 leading-relaxed border-t border-slate-100 dark:border-slate-800/60 pt-3">
                    {faq.answerBn}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
