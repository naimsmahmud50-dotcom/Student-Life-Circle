/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Centralized Admission Counseling Page
 * TOPIC:     Gale-Shapley Stable Matching Studio & Seat Migration Hub
 * FILE:      frontend/src/pages/counseling.tsx
 * PHASE:     Phase 107 - Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
 * PURPOSE:   Provides candidates with an elite university guidance counseling room:
 *            1. Interactive preference stack builder with real-time probability meters.
 *            2. Multi-round migration cascade visualizer showing vacancy ripples.
 *            3. Transparent quota policies and automatic general spillover explanations.
 *            4. Integration with standard Navbar, Footer, and AppHead.
 * STANDARDS: Pareto-Optimal Deferred Acceptance, Quota Spillover Balancing, Zero-Emoji, UI/UX Pro Max
 */

import React, { useState } from 'react';
import {
  GraduationCap,
  Award,
  Compass,
  Layers,
  CheckCircle2,
  TrendingUp,
  Info,
  ShieldCheck,
  Building2,
  Sliders,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { AdmissionCounselingMatrix } from '@/components/admission/AdmissionCounselingMatrix';
import { MigrationCascadeVisualizer } from '@/components/admission/MigrationCascadeVisualizer';

export default function CounselingPage() {
  const [activeTab, setActiveTab] = useState<'both' | 'matrix' | 'migration'>('both');
  const [lastSavedMessage, setLastSavedMessage] = useState<string | null>(null);

  const handlePreferencesSaved = (preferences: string[], quota: string) => {
    setLastSavedMessage(`পছন্দক্রম সংরক্ষিত হয়েছে (${preferences.length}টি বিভাগ, কোটা: ${quota})`);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-bengali selection:bg-blue-500/30 selection:text-blue-200">
      <AppHead
        title="কেন্দ্রীয় ভর্তি কাউন্সেলিং ও গেলে-শ্যাপলি ম্যাচিং হাব | অগ্রযাত্রা"
        description="বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (BUET), ঢাকা বিশ্ববিদ্যালয় (DU), মেডিকেল ও গুচ্ছ ভর্তির মেধাভিত্তিক ও ঈর্ষামুক্ত কেন্দ্রীয় কাউন্সেলিং স্টুডিও।"
      />
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
        {/* Top Hero Guidance Banner */}
        <section className="relative overflow-hidden rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#24314A] p-6 sm:p-8 shadow-xs">
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2.5 px-3 py-1.5 rounded-full bg-blue-950/80 border border-blue-500/40 text-blue-300 text-xs font-mono font-medium tracking-wide">
                <Compass className="w-3.5 h-3.5 text-blue-400" />
                <span>CENTRALIZED MATCHING ENGINE: GALE-SHAPLEY DEFERRED ACCEPTANCE</span>
              </div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-white font-sans">
                কেন্দ্রীয় ভর্তি কাউন্সেলিং ও স্মার্ট মাইগ্রেশন হাব
              </h1>
              <p className="text-slate-300 text-sm sm:text-base max-w-3xl leading-relaxed">
                নোবেলজয়ী অর্থনীতিবিদদের উদ্ভাবিত ডেফার্ড অ্যাকসেপ্টেন্স (Gale-Shapley) মডেলের মাধ্যমে বুয়েট, ঢাবি, মেডিকেল ও গুচ্ছ
                ভর্তির আসন বণ্টন ব্যবস্থা। এটি শতভাগ স্থিতিশীল ও ঈর্ষামুক্ত (Envy-Free) মেধাভিত্তিক বরাদ্দ নিশ্চিত করে।
              </p>
            </div>

            {/* Platform Trust Highlights */}
            <div className="flex flex-wrap md:flex-col gap-3 shrink-0">
              <div className="px-4 py-2.5 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex items-center gap-3">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <div>
                  <div className="text-[11px] text-slate-400 font-sans uppercase">ম্যাচিং গ্যারান্টি</div>
                  <div className="text-xs font-semibold text-emerald-300">১০০% স্থিতিশীল ও ঈর্ষামুক্ত</div>
                </div>
              </div>
              <div className="px-4 py-2.5 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex items-center gap-3">
                <TrendingUp className="w-4 h-4 text-blue-400" />
                <div>
                  <div className="text-[11px] text-slate-400 font-sans uppercase">কোটা নীতি</div>
                  <div className="text-xs font-semibold text-blue-300">স্বয়ংক্রিয় সাধারণ স্পিল-ওভার</div>
                </div>
              </div>
            </div>
          </div>

          {/* Mode Switcher Tabs */}
          <div className="mt-8 pt-6 border-t border-slate-800 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-2 bg-slate-950/80 p-1.5 rounded-2xl border border-slate-800">
              <button
                type="button"
                onClick={() => setActiveTab('both')}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                  activeTab === 'both'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                সম্মিলিত ভিউ (ম্যাট্রিক্স + মাইগ্রেশন)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('matrix')}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                  activeTab === 'matrix'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                পছন্দক্রম ম্যাট্রিক্স
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('migration')}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                  activeTab === 'migration'
                    ? 'bg-blue-600 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                মাইগ্রেশন রিপল সিমুলেটর
              </button>
            </div>

            {lastSavedMessage && (
              <div className="text-xs text-emerald-400 font-sans flex items-center gap-2">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>{lastSavedMessage}</span>
              </div>
            )}
          </div>
        </section>

        {/* Counseling Studio Interactive Sections */}
        <div className="space-y-8">
          {(activeTab === 'both' || activeTab === 'matrix') && (
            <section className="space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-white flex items-center gap-2 font-sans">
                  <GraduationCap className="w-5 h-5 text-blue-400" />
                  <span>বিশ্ববিদ্যালয় পছন্দক্রম ও লাইভ সম্ভাবনা ম্যাট্রিক্স</span>
                </h2>
                <span className="text-xs text-slate-400 font-mono">STRATEGY-PROOF REORDER</span>
              </div>
              <AdmissionCounselingMatrix onSavePreferences={handlePreferencesSaved} />
            </section>
          )}

          {(activeTab === 'both' || activeTab === 'migration') && (
            <section className="space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-white flex items-center gap-2 font-sans">
                  <Layers className="w-5 h-5 text-blue-400" />
                  <span>আসন মাইগ্রেশন ক্যাসকেড ও পরবর্তী রাউন্ড কাটঅফ</span>
                </h2>
                <span className="text-xs text-slate-400 font-mono">3-STAGE VACANCY CASCADE</span>
              </div>
              <MigrationCascadeVisualizer />
            </section>
          )}
        </div>

        {/* Pedagogical Guidance & Matching Rules */}
        <section className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800 text-slate-300 space-y-4">
          <div className="flex items-center gap-2.5 text-blue-400 text-sm font-semibold">
            <Info className="w-4 h-4" />
            <span>শিক্ষার্থী নির্দেশিকা: গেলে-শ্যাপলি ম্যাচিং ও মাইগ্রেশন নীতি</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-400 leading-relaxed font-sans">
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">১. সত্যবাদী পছন্দক্রম নিরাপদ (Strategy-Proof)</div>
              <p>
                আপনার সত্যিকারের পছন্দের ক্রমানুসারেই সাজান। পছন্দের ১ নম্বরে আপনার স্বপ্নের বিভাগ দিলে যদি আসন না পান,
                তাতে ২ নম্বর বা ৩ নম্বর পছন্দের অগ্রাধিকার কখনোই ক্ষুণ্ন হবে না।
              </p>
            </div>
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">২. কোনো ব্লকিং পেয়ার নেই (Envy-Free)</div>
              <p>
                মেধা তালিকায় কোনো শিক্ষার্থী কম স্কোর নিয়ে আপনার পছন্দের বিভাগটিতে স্থান পাবে না। প্রতিটি বরাদ্দ
                সম্পূর্ণ স্বচ্ছ এবং গাণিতিকভাবে ন্যায়সংগত।
              </p>
            </div>
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">৩. কোটা শূন্য হলে মেধা তালিকায় রূপান্তর</div>
              <p>
                কোনো বিভাগে বিশেষ কোটায় উপযুক্ত প্রার্থী না পাওয়া গেলে আসন শূন্য ফেলে রাখা হয় না। স্বয়ংক্রিয়ভাবে
                সাধারণ মেধা তালিকায় তা স্পিল-ওভার হয়ে অপেক্ষমাণ শিক্ষার্থীদের দেওয়া হয়।
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
