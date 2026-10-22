/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Error Boundary & Status Fallback
 * TOPIC:     Human-Crafted 500 Server Error Page (Phase 100 Launch)
 * FILE:      frontend/src/pages/500.tsx
 * PHASE:     Phase 100 - Grand Public Launch
 * PURPOSE:   Provides an empathetic, reassuring 500 internal server error page.
 *            Replaces generic system failures with warm human reassurance,
 *            3D tactile recovery buttons, and sub-pixel Hind Siliguri typography.
 * STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
 */

import React from 'react';
import Link from 'next/link';
import { Home, RefreshCw, AlertCircle, ShieldCheck } from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';

export default function Custom500() {
  const handleReload = () => {
    if (typeof window !== 'undefined') {
      window.location.reload();
    }
  };

  return (
    <>
      <AppHead
        title="সার্ভার সংযোগে বিঘ্ন (৫০০) | অগ্রযাত্রা"
        description="সার্ভারে সামান্য যান্ত্রিক গোলযোগ দেখা দিয়েছে, আমাদের কারিগরি দল বিষয়টি দেখছে। বাংলাদেশের জাতীয় ডিজিটাল শিক্ষামূলক প্ল্যাটফর্ম অগ্রযাত্রা।"
        canonicalUrl="/500"
        ogType="website"
      />

      <div className="min-h-screen flex flex-col bg-slate-50/50 dark:bg-[#090D16] text-slate-900 dark:text-slate-100 font-sans selection:bg-blue-600 selection:text-white transition-colors duration-200">
        <Navbar currentStage="এইচএসসি বিজ্ঞান (HSC Science)" />

        <main className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-16 sm:py-24 relative overflow-hidden">
          {/* Subtle Atmospheric Ambient Lighting */}
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-amber-500/5 dark:bg-amber-500/10 blur-3xl pointer-events-none" />
          <div className="absolute bottom-1/4 left-1/4 w-80 h-80 rounded-full bg-blue-500/5 dark:bg-blue-500/10 blur-3xl pointer-events-none" />

          <div className="max-w-2xl w-full text-center relative z-10 space-y-8">
            
            {/* Visual Decorative Vector Badge (Zero Emoji, 1.75px Stroke) */}
            <div className="inline-flex items-center justify-center p-4 rounded-3xl bg-amber-50 dark:bg-amber-950/60 border border-amber-200/80 dark:border-amber-800/80 text-amber-600 dark:text-amber-400 shadow-ambient mx-auto">
              <AlertCircle className="w-12 h-12 animate-pulse" strokeWidth={1.75} />
            </div>

            {/* Display Numeral in Plus Jakarta Sans */}
            <div className="space-y-3">
              <span className="font-display font-black text-7xl sm:text-9xl tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-orange-500 to-red-500 block select-none">
                500
              </span>
              
              {/* Heartwarming Human Bengali Microcopy in Hind Siliguri */}
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold font-bengali text-slate-900 dark:text-white leading-tight balance-text">
                সার্ভারে সামান্য যান্ত্রিক গোলযোগ দেখা দিয়েছে, আমাদের কারিগরি দল বিষয়টি দেখছে
              </h1>

              <p className="text-sm sm:text-base text-slate-600 dark:text-slate-300 font-bengali leading-relaxed max-w-lg mx-auto editorial-measure">
                আমরা স্বয়ংক্রিয়ভাবে ত্রুটির বিবরণ পেয়েছি এবং অতি দ্রুত তা স্বাভাবিক করার কাজ চলছে। তোমার যেকোনো সংরক্ষিত তথ্য বা পরীক্ষার খাতা সম্পূর্ণ নিরাপদ রয়েছে।
              </p>
            </div>

            {/* 3D Tactile Action Buttons (Brilliant / Linear Physics) */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
              <button
                type="button"
                onClick={handleReload}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold font-bengali text-sm sm:text-base rounded-2xl shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none transition-all duration-150 min-h-[48px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
              >
                <RefreshCw className="w-5 h-5" strokeWidth={1.75} />
                <span>পুনরায় চেষ্টা করুন</span>
              </button>

              <Link
                href="/"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 border border-slate-200 dark:border-slate-800 font-semibold font-bengali text-sm sm:text-base rounded-2xl shadow-xs hover:-translate-y-0.5 active:scale-[0.98] transition-all duration-150 min-h-[48px]"
              >
                <Home className="w-5 h-5" strokeWidth={1.75} />
                <span>হোমপেজে ফিরে যাও</span>
              </Link>
            </div>

            {/* Platform Security Assurance */}
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 dark:bg-slate-800/80 text-xs text-slate-600 dark:text-slate-400 font-bengali">
              <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" strokeWidth={1.75} />
              <span>আইএসও ২৭০০১ ও পোস্টগ্রিস এসকিউএল পিআইটিআর সুরক্ষিত ডাটাবেস</span>
            </div>

          </div>
        </main>

        <Footer />
      </div>
    </>
  );
}
