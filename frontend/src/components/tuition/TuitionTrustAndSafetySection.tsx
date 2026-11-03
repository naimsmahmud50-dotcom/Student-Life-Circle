/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Tuition Trust, Safety & FAQ Ecosystem
 * TOPIC:     CareTutors-Style 4-Pillar Safety & Bilateral Trust Architecture
 * FILE:      frontend/src/components/tuition/TuitionTrustAndSafetySection.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, High Contrast, Accessible FAQ Accordion, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { useTranslation } from '../../lib/i18n';
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
  const { isBengali } = useTranslation();
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
            <span>{isBengali ? "নিরাপদ ও নির্ভরযোগ্য টিউশন নেটওয়ার্ক" : "Safe & Trustworthy Tuition Network"}</span>
          </span>
          <h3
            id="trust-safety-heading"
            className="mt-3 text-2xl sm:text-3xl font-bold font-serif text-slate-900 dark:text-white"
          >
            {isBengali ? "কেন অগ্রযাত্রা টিউশন মার্কেটপ্লেস সবচেয়ে বিশ্বস্ত?" : "Why Agragoti Tuition Marketplace Is Bangladesh's Most Trusted?"}
          </h3>
          <p className="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-400">
            {isBengali
              ? "শিক্ষার্থী, অভিভাবক ও শিক্ষকদের শতভাগ নিরাপত্তা নিশ্চিত করার ৪ স্তরের সুরক্ষা ব্যবস্থা"
              : "A 4-tier security framework ensuring 100% protection for students, parents, and educators"}
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
          {/* Pillar 1 */}
          <div className="p-5 rounded-3xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-700">
              <FileCheck2 className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white leading-snug">
              {isBengali ? "১. জাতীয় পরিচয়পত্র ও সনদ যাচাই" : "1. NID & Degree Verification"}
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              {isBengali
                ? "প্রতিটি শিক্ষকের জাতীয় পরিচয়পত্র (NID) এবং বিশ্ববিদ্যালয় স্টুডেন্ট আইডি ও ট্রান্সক্রিপ্ট নিখুঁতভাবে যাচাই করে ভেরিফায়েড ব্যাজ দেওয়া হয়।"
                : "Every educator's National ID (NID), student ID card, and academic transcripts are rigorously authenticated before badge issuance."}
            </p>
          </div>

          {/* Pillar 2 */}
          <div className="p-5 rounded-3xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 flex items-center justify-center text-blue-700">
              <CalendarCheck2 className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white leading-snug">
              {isBengali ? "২. ২ দিনের ফ্রি ট্রায়াল ক্লাস" : "2. 2-Day Free Trial Sessions"}
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              {isBengali
                ? "শিক্ষক ও শিক্ষার্থীর বোঝাপড়া যাচাইয়ের জন্য প্রথম ২ দিন বিনামূল্যে ট্রায়াল ক্লাস। শতভাগ সন্তুষ্ট হলেই কেবল টিউশন চুক্তি নিশ্চিত করবেন।"
                : "2 complimentary trial sessions to evaluate pedagogy and student comfort. Finalize tuition agreement only when 100% satisfied."}
            </p>
          </div>

          {/* Pillar 3 */}
          <div className="p-5 rounded-3xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800 flex items-center justify-center text-amber-700">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white leading-snug">
              {isBengali ? "৩. ০ টাকা অগ্রিম ও নো-স্ক্যাম নীতি" : "3. BDT 0 Advance Fee & Zero Scam"}
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              {isBengali
                ? "অভিভাবকদের কাছ থেকে কোনো রেজিস্ট্রেশন চার্জ বা অগ্রিম ফি নেওয়া হয় না। কোনো ভুয়া মিডিয়া বা অগ্রিম কমিশনের ঝামেলামুক্ত।"
                : "Zero registration charges or advance fees for guardians. Free from unregulated middlemen or upfront commission deductions."}
            </p>
          </div>

          {/* Pillar 4 */}
          <div className="p-5 rounded-3xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-purple-50 dark:bg-purple-950/60 border border-purple-200 dark:border-purple-800 flex items-center justify-center text-purple-700">
              <CreditCard className="w-5 h-5" />
            </div>
            <h4 className="font-bold text-sm sm:text-base text-slate-900 dark:text-white leading-snug">
              {isBengali ? "৪. দ্বিপাক্ষিক সম্মতি ও এসক্রো ট্রাস্ট" : "4. Bilateral Consent & Escrow Trust"}
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              {isBengali
                ? "উভয় পক্ষের সম্মতি ছাড়া নম্বর উন্মুক্ত নয়। এছাড়া মাসের বেতন এসক্রো মাইলস্টোন প্রোটেকশনে সম্পূর্ণ নিরাপদ থাকে।"
                : "Direct contact numbers remain masked until mutual consent is verified. Monthly honorarium is safeguarded via escrow milestones."}
            </p>
          </div>
        </div>
      </div>

      {/* FAQ Accordion Section */}
      <div className="p-6 sm:p-8 rounded-3xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-emerald-700" />
            <h4 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">
              {isBengali ? "সাধারণ জিজ্ঞাসা (FAQ)" : "Frequently Asked Questions (FAQ)"}
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
              {isBengali ? "অভিভাবকদের প্রশ্ন" : "Parent Questions"}
            </button>
            <button
              onClick={() => setActiveFaqTab('tutor')}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                activeFaqTab === 'tutor'
                  ? 'bg-[#0A2540] text-white'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300'
              }`}
            >
              {isBengali ? "শিক্ষকদের প্রশ্ন" : "Tutor Questions"}
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
                  <span>{isBengali ? faq.questionBn : (faq.questionEn || faq.questionBn)}</span>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-slate-400 shrink-0" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                  )}
                </button>
                {isOpen && (
                  <div className="px-4 pb-4 text-xs text-slate-600 dark:text-slate-400 leading-relaxed border-t border-slate-100 dark:border-slate-800/60 pt-3">
                    {isBengali ? faq.answerBn : (faq.answerEn || faq.answerBn)}
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
