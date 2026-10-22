/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Error Boundary & Status Fallback
 * TOPIC:     Human-Crafted 404 Not Found Page (Modern Academic Editorial Standard)
 * FILE:      frontend/src/pages/404.tsx
 * PHASE:     Phase 100 - Grand Public Launch
 * PURPOSE:   Provides an empathetic, prestigious student-first 404 error experience.
 *            Replaces cold robotic system errors with heartwarming guidance,
 *            3D tactile action buttons, and sub-pixel Hind Siliguri typography.
 * STANDARDS: Modern Academic Editorial, UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
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

      <div className="min-h-screen flex flex-col bg-[#FAF8F3] dark:bg-[#0B132B] text-[#1A1A1A] dark:text-[#F8FAFC] font-sans selection:bg-[#1B2A4A] selection:text-white transition-colors duration-200">
        <Navbar currentStage="এইচএসসি বিজ্ঞান (HSC Science)" />

        <main className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 py-16 sm:py-24 relative overflow-hidden">
          <div className="max-w-2xl w-full text-center relative z-10 space-y-6">
            
            {/* Visual Decorative Vector Badge (Zero Emoji, 1.75px Stroke) */}
            <div className="inline-flex items-center justify-center p-4 rounded-2xl bg-[#EEF2F6] dark:bg-[#152035] border border-[#D5DEE8] dark:border-[#263554] text-[#1B2A4A] dark:text-[#A8B7D8] mx-auto">
              <Compass className="w-10 h-10" strokeWidth={1.75} />
            </div>

            {/* Display Numeral in Plus Jakarta Sans */}
            <div className="space-y-3">
              <span className="font-display font-bold text-7xl sm:text-8xl tracking-tight text-[#1B2A4A] dark:text-[#A8B7D8] block select-none">
                404
              </span>
              
              {/* Heartwarming Human Bengali Microcopy in Hind Siliguri */}
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-serif font-bold font-bengali text-[#1B2A4A] dark:text-white leading-tight balance-text">
                পাতাটি হয়তো ক্লাসরুম পরিবর্তন করেছে, চলো মূল পাতায় ফিরে যাই
              </h1>

              <p className="text-sm sm:text-base text-[#5B5B5B] dark:text-slate-300 font-bengali leading-relaxed max-w-lg mx-auto editorial-measure">
                তুমি যে পাতাটি খুঁজছো তা সাময়িকভাবে সরিয়ে নেওয়া হয়েছে অথবা অন্য কোনো ঠিকানায় স্থানান্তর করা হয়েছে। তবে চিন্তার কিছু নেই, তোমার মেধার অগ্রযাত্রা অক্ষুণ্ণ রয়েছে।
              </p>
            </div>

            {/* 3D Tactile Action Button */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
              <Link
                href="/"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-6 py-3.5 bg-[#1B2A4A] hover:bg-[#132038] text-white font-semibold font-bengali text-sm sm:text-base rounded-2xl shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none transition-all duration-150 min-h-[48px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#1B2A4A] focus-visible:ring-offset-2"
              >
                <Home className="w-5 h-5" strokeWidth={1.75} />
                <span>হোমপেজে ফিরে যাও</span>
              </Link>

              <Link
                href="/learn"
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-3.5 bg-white dark:bg-[#121B2D] text-[#1A1A1A] dark:text-slate-300 hover:text-[#1B2A4A] dark:hover:text-white border border-[#E5E2DA] dark:border-[#263145] font-semibold font-bengali text-sm rounded-2xl shadow-xs active:translate-y-0.5 transition-all duration-150 min-h-[48px]"
              >
                <BookOpen className="w-4 h-4" strokeWidth={1.75} />
                <span>পাঠ্যক্রম অন্বেষণ</span>
              </Link>
            </div>

            {/* Helpful Student Guidance */}
            <div className="pt-6 border-t border-[#E5E2DA] dark:border-slate-800 text-xs text-[#5B5B5B] dark:text-slate-400 font-bengali">
              <span>কোনো তথ্য খুঁজে পেতে সমস্যা হলে আমাদের সহায়তা কেন্দ্রে যোগাযোগ করতে পারেন।</span>
            </div>

          </div>
        </main>

        <Footer />
      </div>
    </>
  );
}
