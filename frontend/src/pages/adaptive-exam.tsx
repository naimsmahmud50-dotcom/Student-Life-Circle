/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Computerized Adaptive Testing Page
 * TOPIC:     AI Adaptive Examination & Dynamic CAT Tower Page
 * FILE:      frontend/src/pages/adaptive-exam.tsx
 * PHASE:     Phase 105 - AI Adaptive CAT Examination Tower
 * PURPOSE:   Provides an interactive page mounting the AdaptiveExamStudio and
 *            AbilityConvergenceGraph, guiding students through distraction-free
 *            3-PL IRT adaptive evaluation with KaTeX equations and tactile buttons.
 * STANDARDS: UI/UX Pro Max, IRT 3-PL Latent Ability Math, Zero-Emoji, Human-Centric
 */

import React from 'react';
import { Compass, Sparkles, ShieldCheck, Target } from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { AdaptiveExamStudio } from '@/components/adaptive-exam/AdaptiveExamStudio';

export default function AdaptiveExamPage() {
  return (
    <div className="min-h-screen bg-slate-50/50 dark:bg-[#0F172A] text-slate-900 dark:text-slate-100 flex flex-col font-sans transition-colors duration-200">
      <AppHead
        title="এআই অ্যাডাপ্টিভ পরীক্ষা | ডাইনামিক ক্যাট টাওয়ার | অগ্রযাত্রা"
        description="আইআরটি ৩-পিএল সাইকোমেট্রিক অ্যাডাপ্টিভ পরীক্ষা ও রিয়েল-টাইম সামর্থ্য অভিসরণ ট্র্যাকিং।"
        canonicalUrl="/adaptive-exam"
        ogType="website"
      />

      <Navbar currentStage="এইচএসসি বিজ্ঞান (HSC Science)" />

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 flex flex-col space-y-8">
        <AdaptiveExamStudio initialSubject="উচ্চতর গণিত ও পদার্থবিজ্ঞান" studentId="stu_ogro_live" />
      </main>

      <Footer />
    </div>
  );
}
