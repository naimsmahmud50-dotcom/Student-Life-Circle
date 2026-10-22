/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Guardian Trust Console Page
 * TOPIC:     Apple Health Caliber Guardian Portal & Tuition Escrow Host
 * FILE:      frontend/src/pages/guardian.tsx
 * PHASE:     Phase 108 - Guardian Trust Console & Child Digital Safety Portal
 * PURPOSE:   Provides parents and guardians with an empathetic, dignified home:
 *            1. Non-intrusive learning telemetry across linked children.
 *            2. ASVS L2 child privacy wall protection.
 *            3. Milestone tuition escrow review and OTP authorization.
 *            4. Integration with standard Navbar, Footer, and AppHead.
 * STANDARDS: ASVS L2 Minor Privacy Boundary, Zero-Intrusion Safeguards, Zero-Emoji, UI/UX Pro Max
 */

import React, { useState } from 'react';
import {
  ShieldCheck,
  Heart,
  Clock,
  Award,
  Wallet,
  Lock,
  Users,
  CheckCircle2,
  Sparkles,
  Info,
  Building2,
  Calendar
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { GuardianDashboard } from '@/components/guardian/GuardianDashboard';
import { TuitionEscrowApprovalCard } from '@/components/guardian/TuitionEscrowApprovalCard';

export default function GuardianPage() {
  const [activeTab, setActiveTab] = useState<'both' | 'progress' | 'escrow'>('both');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-bengali selection:bg-teal-500/30 selection:text-teal-200">
      <AppHead
        title="অভিভাবক ট্রাস্ট কনসোল ও শিশু ডিজিটাল নিরাপত্তা | অগ্রযাত্রা"
        description="সন্তানের পড়াশোনার সার্বিক অগ্রগতি ও মানসিক শান্তির সমন্বয়। গোপনীয়তা প্রাচীর (ASVS L2) ও নিরাপদ টিউশন ফি এসক্রো ব্যবস্থাপনা।"
      />
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
        {/* Top Hero Guidance Banner */}
        <section className="relative overflow-hidden rounded-3xl bg-slate-900/90 border border-teal-500/30 p-6 sm:p-8 shadow-2xl backdrop-blur-xl">
          <div className="absolute top-0 right-0 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20" />
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2.5 px-3 py-1.5 rounded-full bg-teal-950/80 border border-teal-500/40 text-teal-300 text-xs font-mono font-medium tracking-wide">
                <ShieldCheck className="w-3.5 h-3.5 text-teal-400" />
                <span>FAMILY TRUST & CHILD DIGITAL SAFETY CONSOLE</span>
              </div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-white font-sans">
                অভিভাবক ট্রাস্ট কনসোল ও শিশু ডিজিটাল নিরাপত্তা
              </h1>
              <p className="text-slate-300 text-sm sm:text-base max-w-3xl leading-relaxed">
                সন্তানের পড়াশোনায় পাশে থাকুন স্নেহে, উদ্বেগে নয়। এই কনসোলটি কোনো নজরদারি বা প্যানিক সৃষ্টি করে না;
                বরং সন্তানের সুস্থ মানসিক বিকাশ ও স্বচ্ছ টিউশন সম্মানী পরিশোধের একটি বিশ্বস্ত পারিবারিক মাধ্যম।
              </p>
            </div>

            {/* Safety Metrics Widgets */}
            <div className="flex flex-wrap md:flex-col gap-3 shrink-0">
              <div className="px-4 py-2.5 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex items-center gap-3">
                <Lock className="w-4 h-4 text-emerald-400" />
                <div>
                  <div className="text-[11px] text-slate-400 font-sans uppercase">শিশু গোপনীয়তা মান</div>
                  <div className="text-xs font-semibold text-emerald-300">ASVS L2 / COPPA সুরক্ষিত</div>
                </div>
              </div>
              <div className="px-4 py-2.5 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex items-center gap-3">
                <Wallet className="w-4 h-4 text-teal-400" />
                <div>
                  <div className="text-[11px] text-slate-400 font-sans uppercase">টিউশন ফি নিরাপত্তা</div>
                  <div className="text-xs font-semibold text-teal-300">১-ক্লিক ওটিপি এসক্রো রিলিজ</div>
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
                    ? 'bg-teal-700 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                সম্মিলিত ভিউ (অগ্রগতি + ফি রিলিজ)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('progress')}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                  activeTab === 'progress'
                    ? 'bg-teal-700 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                পড়াশোনার অগ্রগতি ও শিখন
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('escrow')}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                  activeTab === 'escrow'
                    ? 'bg-teal-700 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                টিউশন এসক্রো অনুমোদন
              </button>
            </div>
          </div>
        </section>

        {/* Dashboard & Escrow Grid */}
        <div className="space-y-8">
          {(activeTab === 'both' || activeTab === 'progress') && (
            <section className="space-y-3">
              <GuardianDashboard />
            </section>
          )}

          {(activeTab === 'both' || activeTab === 'escrow') && (
            <section className="space-y-3">
              <TuitionEscrowApprovalCard />
            </section>
          )}
        </div>

        {/* Child Digital Privacy Wall (ASVS L2) Guidance */}
        <section className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800 text-slate-300 space-y-4">
          <div className="flex items-center gap-2.5 text-teal-400 text-sm font-semibold">
            <Info className="w-4 h-4" />
            <span>অভিভাবক সচেতনতা ও শিশু নিরাপত্তা নীতিমালা (ASVS L2 / COPPA)</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-400 leading-relaxed font-sans">
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">১. নজরদারি নয়, উৎসাহ দিন</div>
              <p>
                শিক্ষার্থীর ব্যক্তিগত চিন্তা, সহপাঠী গ্রুপ চ্যাট বা খসড়া নোট অভিভাবকের কাছে গোপন রাখা হয়। এটি শিশুর আত্মবিশ্বাস ও
                স্বাধীন মেধা বিকাশে অত্যন্ত জরুরি।
              </p>
            </div>
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">২. সামগ্রিক অগ্রগতিতে আলোকপাত</div>
              <p>
                প্রতিটি ভুলের হিসাব না করে দেখুন সন্তান প্রতিদিনের রুটিন বজায় রাখছে কিনা এবং সাপ্তাহিক সময়ের সঠিক ব্যবহার করছে কিনা।
              </p>
            </div>
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">৩. নিরাপদ ও স্বচ্ছ এসক্রো সম্মানী</div>
              <p>
                গৃহশিক্ষকের ১২টি ক্লাস সম্পন্ন হওয়া এবং শিক্ষার্থীর সন্তুষ্টি নিশ্চিত করার পরেই কেবল ওটিপি দিয়ে ফি রিলিজ করবেন।
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
