/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Next.js Page: /routines
 * TOPIC:     200-Day BCS & Admission Routine Calendar Hub with Feature Gating
 * FILE:      frontend/src/pages/routines/index.tsx
 * PURPOSE:   Provides top-level isolated page route for the Exam Routine Hub.
 *            Enforces runtime feature gating; renders Coming Soon banner if flag is false.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA Contrast
 * ========================================================================================
 */

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import Link from 'next/link';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Calendar, ShieldCheck, ArrowRight, Lock, CheckCircle2 } from 'lucide-react';
import { useFeatureFlags, isFeatureEnabled } from '@/config/featureFlags';

// Dynamic lazy import to preserve bundle budget (<25 KB initial chunk)
const ExamRoutineHub = dynamic(
  () => import('@/modules/exam-routine').then((mod) => mod.ExamRoutineHub),
  {
    ssr: true,
    loading: () => (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="flex flex-col items-center gap-3">
          <Calendar className="h-8 w-8 text-emerald-600 animate-pulse" />
          <span className="text-xs font-serif text-slate-500">পরীক্ষার রুটিন লোড হচ্ছে...</span>
        </div>
      </div>
    ),
  }
);

export default function RoutinesPage() {
  const flags = useFeatureFlags();
  const [previewEnabled, setPreviewEnabled] = useState<boolean>(false);

  const isEnabled = flags.examRoutine || previewEnabled;

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      <AppHead
        title="পরীক্ষার রুটিন ও মেগা মডেল টেস্ট শিডিউল | অগ্রযাত্রা"
        description="৪৭তম বিসিএস প্রিলিমিনারি ২০০ দিনের দৈনিক রুটিন এবং বিশ্ববিদ্যালয় ভর্তি মেগা মডেল টেস্ট শিডিউল ক্যালেন্ডার।"
      />
      <Navbar />

      <main className="flex-1">
        {isEnabled ? (
          <ExamRoutineHub />
        ) : (
          <div className="mx-auto max-w-4xl px-4 py-20 text-center">
            <div className="mx-auto max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900 space-y-5">
              <div className="mx-auto inline-flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600 dark:bg-emerald-950/50 dark:text-emerald-400">
                <Calendar className="h-6 w-6" />
              </div>

              <div className="space-y-2">
                <h1 className="text-xl font-serif font-bold text-slate-900 dark:text-slate-100">
                  শীঘ্রই আসছে: লাইভ এমসিকিউ ও মডেল টেস্ট রুটিন হাব
                </h1>
                <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  ৪৭তম বিসিএস এবং বিশ্ববিদ্যালয় ভর্তি পরীক্ষার্থীদের জন্য ২০০ দিনের সুবিন্যস্ত দৈনিক রুটিন ও মেগা মডেল টেস্ট শিডিউল চূড়ান্ত নিরীক্ষায় রয়েছে।
                </p>
              </div>

              <div className="rounded-lg bg-slate-50 p-4 text-left text-xs space-y-2 dark:bg-slate-800/60">
                <div className="flex items-center gap-2 font-semibold text-slate-700 dark:text-slate-300">
                  <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                  <span>আসন্ন প্রধান বৈশিষ্ঠ্যসমূহ:</span>
                </div>
                <ul className="list-disc list-inside space-y-1 text-slate-500 dark:text-slate-400 pl-1">
                  <li>২০০ দিনের সমন্বিত দৈনিক সিলেবাস রোডম্যাপ</li>
                  <li>প্রতি শুক্রবার দেশব্যাপী মেগা মডেল টেস্ট ও লাইভ কাউন্টডাউন</li>
                  <li>নেগেটিভ মার্কিং পেনাল্টি নিরীক্ষা ও মেধা পারসেন্টাইল প্রজেকশন</li>
                </ul>
              </div>

              {/* Developer / QA Preview Toggle */}
              <div className="pt-2 border-t border-slate-100 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setPreviewEnabled(true)}
                  className="inline-flex items-center gap-1.5 text-xs text-emerald-600 hover:text-emerald-500 font-semibold"
                >
                  <Lock className="h-3 w-3" />
                  <span>স্টেজিং প্রিভিউ সক্রিয় করুন (Quality Review Mode)</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
