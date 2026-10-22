/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Error Boundary & Status Fallback
 * TOPIC:     Human-Crafted 404 Not Found Page (Phase 100 Launch)
 * FILE:      frontend/src/pages/404.tsx
 * PHASE:     Phase 100 - Grand Public Launch
 * PURPOSE:   Provides an empathetic, prestigious student-first 404 error experience.
 *            Replaces cold robotic system errors with heartwarming guidance,
 *            3D tactile action buttons, and sub-pixel Hind Siliguri typography.
 * STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
 */

import React from 'react';
import Link from 'next/link';
import { Home, Compass, BookOpen, ArrowLeft, Search } from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';

export default function Custom404() {
  return (
    <>
      <AppHead
        title="পাতাটি পাওয়া যায়নি (৪০৪) | অগ্রযাত্রা"
        description="পাতাটি হয়তো ক্লাসরুম পরিবর্তন করেছে, চলো মূল পাতায় ফিরে যাই। বাংলাদেশের জাতীয় ডিজিটাল শিক্ষামূলক প্ল্যাটফর্ম অগ্রযাত্রা।"
        canonicalUrl="/404"
        ogType="website"
      />

      <div className="min-h-screen flex flex-col bg-slate-50/50 dark:bg-[#090D16] text-slate-900 dark:text-slate-100 font-sans selection:bg-blue-600 selection:text-white transition-colors duration-200">
        <Navbar currentStage="এইচএসসি বিজ্ঞান (HSC Science)" />

        <main className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-16 sm:py-24 relative overflow-hidden">
          {/* Subtle Atmospheric Ambient Lighting */}
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-blue-500/5 dark:bg-blue-500/10 blur-3xl pointer-events-none" />
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full bg-teal-500/5 dark:bg-teal-500/10 blur-3xl pointer-events-none" />

          <div className="max-w-2xl w-full text-center relative z-10 space-y-8">
            
            {/* Visual Decorative Vector Badge (Zero Emoji, 1.75px Stroke) */}
            <div className="inline-flex items-center justify-center p-4 rounded-3xl bg-blue-50 dark:bg-blue-950/60 border border-blue-200/80 dark:border-blue-800/80 text-blue-600 dark:text-blue-400 shadow-ambient mx-auto">
              <Compass className="w-12 h-12 animate-pulse" strokeWidth={1.75} />
            </div>

            {/* Display Numeral in Plus Jakarta Sans */}
            <div className="space-y-3">
              <span className="font-display font-black text-7xl sm:text-9xl tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-600 to-teal-600 dark:from-blue-400 dark:via-indigo-300 dark:to-teal-300 block select-none">
                404
              </span>
              
              {/* Heartwarming Human Bengali Microcopy in Hind Siliguri */}
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold font-bengali text-slate-900 dark:text-white leading-tight balance-text">
                পাতাটি হয়তো ক্লাসরুম পরিবর্তন করেছে, চলো মূল পাতায় ফিরে যাই
              </h1>

              <p className="text-sm sm:text-base text-slate-600 dark:text-slate-300 font-bengali leading-relaxed max-w-lg mx-auto editorial-measure">
                তুমি যে পাতাটি খুঁজছো তা সাময়িকভাবে সরিয়ে নেওয়া হয়েছে অথবা অন্য কোনো ঠিকানায় স্থানান্তর করা হয়েছে। তবে চিন্তার কিছু নেই, তোমার মেধার অগ্রযাত্রা অক্ষুণ্ণ রয়েছে।
              </p>
            </div>

            {/* 3D Tactile Action Button (Brilliant / Linear Physics) */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
              <Link
                href="/"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold font-bengali text-sm sm:text-base rounded-2xl shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none transition-all duration-150 min-h-[48px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
              >
                <Home className="w-5 h-5" strokeWidth={1.75} />
                <span>হোমপেজে ফিরে যাও</span>
              </Link>

              <Link
                href="/learn"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-3.5 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:text-blue-600 dark:hover:text-blue-400 border border-slate-200 dark:border-slate-800 font-semibold font-bengali text-sm rounded-2xl shadow-xs hover:-translate-y-0.5 active:scale-[0.98] transition-all duration-150 min-h-[48px]"
              >
                <BookOpen className="w-4 h-4" strokeWidth={1.75} />
                <span>পাঠ্যক্রম অন্বেষণ</span>
              </Link>
            </div>

            {/* Helpful Student Guidance */}
            <div className="pt-6 border-t border-slate-200/60 dark:border-slate-800/60 text-xs text-slate-500 dark:text-slate-400 font-bengali">
              <span>কোনো তথ্য খুঁজে পেতে সমস্যা হলে আমাদের ২৪/৭ সাপোর্ট অথবা সক্রেটিক টিউটরের সহায়তা নাও।</span>
            </div>

          </div>
        </main>

        <Footer />
      </div>
    </>
  );
}
