/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      frontend/src/components/live-challenge/LiveMcqFaqAccordion.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Reverse-engineers and elevates Live MCQ's "faq" section. Provides
 *            interactive expandable accordion for high-stakes test rules, negative
 *            marking, server timer synchronization, offline resilience, and privacy.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React, { useState } from 'react';
import {
  HelpCircle,
  ChevronDown,
  ChevronUp,
  ShieldCheck,
  CheckCircle2
} from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

interface FaqItem {
  questionBn: string;
  questionEn: string;
  answerBn: string;
  answerEn: string;
}

const FAQS: FaqItem[] = [
  {
    questionBn: 'নতুন শিক্ষার্থী হিসেবে কীভাবে লাইভ পরীক্ষায় অংশগ্রহণ শুরু করবো?',
    questionEn: 'How do I start participating in live exams as a new student?',
    answerBn: 'প্রথমে হোমপেজ বা লাইভ চ্যালেঞ্জ লবি থেকে আপনার পরীক্ষার বিষয় বা ট্র্যাক নির্বাচন করুন। নির্ধারিত সময়ে "পরীক্ষায় অংশগ্রহণ করুন" বাটনে ক্লিক করে ডিজিটাল ওএমআর শিট অথবা স্ট্যান্ডার্ড ইন্টারফেসে লাইভ পরীক্ষা শুরু করতে পারবেন।',
    answerEn: 'First, select your examination track or subject from the homepage or Live Challenge lobby. At the scheduled time, click "Take Exam" to launch the test in either the Digital OMR Sheet mode or standard interface.'
  },
  {
    questionBn: 'লাইভ পরীক্ষার নির্দিষ্ট সময় মিস হয়ে গেলে পরবর্তীতে কি পরীক্ষা দেওয়া সম্ভব?',
    questionEn: 'Can I still take the exam if I miss the live examination slot?',
    answerBn: 'হ্যাঁ। কোনো কারণে নির্ধারিত লাইভ সময়ে যুক্ত হতে না পারলে, পরীক্ষাটি সরাসরি "১০ বছরের সেন্ট্রাল আর্কাইভ"-এ যুক্ত হয়ে যায়। আর্কাইভ থেকে আপনি যে কোনো সময় সেলফ-টেস্ট বা ওএমআর প্র্যাকটিস মোডে অংশ নিতে পারবেন।',
    answerEn: 'Yes. If you miss the live slot for any reason, the exam is immediately moved to the "10-Year Central Archive". You can take it anytime in self-paced or OMR practice mode with instant scoring.'
  },
  {
    questionBn: 'নেগেটিভ মার্কিং পদ্ধতি কীভাবে হিসাব করা হয়?',
    questionEn: 'How does the negative marking system work?',
    answerBn: 'প্রতিটি সঠিক উত্তরের জন্য পাবেন +১.০ নম্বর এবং প্রতিটি ভুল উত্তরের জন্য কাটা যাবে -০.২৫ নম্বর। কোনো প্রশ্নের উত্তর না দিলে কোনো নম্বর কর্তন করা হবে না। পরীক্ষা শেষে তাৎক্ষণিক গ্রস স্কোর, নেগেটিভ ডিডাকশন ও নেট স্কোর প্রদর্শিত হবে।',
    answerEn: 'Each correct answer awards +1.0 mark, and each incorrect answer deducts -0.25 mark. Unanswered questions carry no penalty. Detailed gross score, negative deductions, and net score are displayed instantly after completion.'
  },
  {
    questionBn: 'পরীক্ষার চলাকালীন ইন্টারনেট বিচ্ছিন্ন হয়ে গেলে আমার উত্তর কি মুছে যাবে?',
    questionEn: 'Will my answers be lost if my internet connection drops during the exam?',
    answerBn: 'একদমই না। আমাদের ক্লায়েন্ট-সাইড অফলাইন রেসিলিয়েন্ট মেমরি বাফারে আপনার প্রতিটি উত্তর স্থানীয়ভাবে সুরক্ষিত থাকে। পুনরায় ইন্টারনেট সংযোগ ফিরলেই মিলি-সেকেন্ড সিঙ্কে সার্ভারে উত্তর জমা হবে।',
    answerEn: 'Not at all. Our client-side offline resilient buffer securely saves every answer locally on your device. Once the internet connection is restored, answers are synced to the server with millisecond-level precision.'
  },
  {
    questionBn: 'পাবলিক লিডারবোর্ডে আমার ব্যক্তিগত তথ্য কি নিরাপদ?',
    questionEn: 'Is my personal information secure on the public leaderboard?',
    answerBn: 'সম্পূর্ণ নিরাপদ। লিডারবোর্ডে কোনো ফোন নম্বর বা ব্যক্তিগত নাম দেখানো হয় না; প্রার্থীর জন্য স্বয়ংক্রিয় ছদ্মনাম (Pseudonymous Handle) ব্যবহৃত হয়। এছাড়া চাইলে যে কোনো সময় এক ক্লিকে পাবলিক র‍্যাংকিং থেকে নিজেকে অপ্ট-আউট করতে পারবেন।',
    answerEn: 'Completely secure. No phone numbers or real full names are revealed on the leaderboard; an automated pseudonymous handle is assigned to each examinee. You can also opt out of public rankings at any time with one click.'
  },
  {
    questionBn: 'স্মার্টফোন এবং কম্পিউটার উভয় ডিভাইস থেকে কি একাউন্ট ব্যবহার করা যাবে?',
    questionEn: 'Can I use my account across both mobile devices and computers?',
    answerBn: 'হ্যাঁ। আপনার অগ্রযাত্রা একাউন্ট সম্পূর্ণ ক্লাউড-সিঙ্কড। মোবাইল, ট্যাবলেট বা কম্পিউটার—যেকোনো ডিভাইসের ব্রাউজার থেকে সরাসরি লগইন করে যেকোনো সময় সমান সুবিধায় প্রস্তুতি চালিয়ে যেতে পারবেন।',
    answerEn: 'Yes. Your Agrojatra account is fully cloud-synchronized. You can log in directly from any smartphone, tablet, or desktop browser and resume your preparation seamlessly.'
  }
];

export function LiveMcqFaqAccordion() {
  const { isBengali } = useTranslation();
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const toggle = (idx: number) => {
    setOpenIndex(openIndex === idx ? null : idx);
  };

  return (
    <div className="space-y-6">
      <div className="text-center space-y-3 max-w-2xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-slate-100 dark:bg-[#151D2C] border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 text-xs font-bold font-bengali">
          <HelpCircle className="w-3.5 h-3.5 text-sky-500 dark:text-sky-400" />
          <span>{isBengali ? 'সচরাচর জিজ্ঞাসা • FAQ' : 'Frequently Asked Questions • FAQ'}</span>
        </div>

        <h2 className="text-xl sm:text-3xl font-bold text-slate-900 dark:text-white font-serif tracking-tight">
          {isBengali ? (
            <>
              পরীক্ষা সংক্রান্ত সকল প্রশ্নের{' '}
              <span className="text-sky-600 dark:text-sky-400 font-serif">
                নির্ভরযোগ্য উত্তর
              </span>
            </>
          ) : (
            <>
              Authoritative Answers to{' '}
              <span className="text-sky-600 dark:text-sky-400 font-serif">
                All Examination Questions
              </span>
            </>
          )}
        </h2>

        <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
          {isBengali 
            ? 'যা জানতে চান, এখানে পেয়ে যাবেন। নিয়মাবলী বুঝে নিয়ে নিশ্চিন্তে পরীক্ষায় অংশ নিন।' 
            : 'Everything you need to know. Understand the rules and participate in exams with complete confidence.'}
        </p>
      </div>

      <div className="max-w-3xl mx-auto space-y-3">
        {FAQS.map((faq, index) => {
          const isOpen = openIndex === index;

          return (
            <div
              key={index}
              className={`rounded-2xl bg-white/95 dark:bg-[#131A26]/90 border backdrop-blur-md overflow-hidden transition shadow-xl ${
                isOpen
                  ? 'border-sky-500/40 dark:border-sky-400/40'
                  : 'border-slate-200/80 dark:border-slate-800/80'
              }`}
            >
              <button
                type="button"
                onClick={() => toggle(index)}
                className="w-full p-5 text-left flex items-center justify-between gap-4 hover:bg-slate-50 dark:hover:bg-slate-800/40 transition cursor-pointer"
                aria-expanded={isOpen}
              >
                <span className="text-sm sm:text-base font-bold font-bengali text-slate-900 dark:text-white flex items-center gap-2.5">
                  <span className="w-6 h-6 rounded-lg bg-sky-500/10 dark:bg-sky-500/20 text-sky-600 dark:text-sky-400 text-xs font-mono font-bold flex items-center justify-center shrink-0 border border-sky-500/30">
                    Q{index + 1}
                  </span>
                  <span>{isBengali ? faq.questionBn : faq.questionEn}</span>
                </span>
                {isOpen ? (
                  <ChevronUp className="w-5 h-5 text-sky-500 dark:text-sky-400 shrink-0" />
                ) : (
                  <ChevronDown className="w-5 h-5 text-slate-400 shrink-0" />
                )}
              </button>

              {isOpen && (
                <div className="px-5 pb-5 pt-3 text-xs sm:text-sm text-slate-700 dark:text-slate-200 font-bengali leading-relaxed border-t border-slate-200/50 dark:border-slate-800/80 bg-slate-50/50 dark:bg-[#0B1019]/60">
                  {isBengali ? faq.answerBn : faq.answerEn}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
