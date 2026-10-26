/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic Excellence Hub & Course Bundles
 * TOPIC:     10MS Competitive Elevation Dedicated Showcase Page
 * FILE:      frontend/src/pages/academic-hub.tsx
 * STANDARDS: Zero-Emoji, Production Grade, Scope Lock, WCAG 2.2 AAA
 */

import React from 'react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { CompetitiveElevationSection } from '@/components/competitive-elevation';

export default function AcademicHubPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#FAF8F3] dark:bg-[#0A1120] text-slate-900 dark:text-slate-100 transition-colors duration-200">
      <AppHead
        title="অ্যাকাডেমিক কোর্স ও ব্যাচ হাব | অগ্রযাত্রা"
        description="এক জায়গায় স্কুল, কলেজ ও প্রতিযোগিতামূলক পরীক্ষার পূর্ণাঙ্গ প্রস্তুতি। লাইভ ক্লাস, আনলিমিটেড ওএমআর মডেল টেস্ট ও ২৪ ঘণ্টা ডাউট সলভ।"
      />

      <Navbar />

      <main className="flex-1 py-6 sm:py-10">
        <CompetitiveElevationSection defaultCategoryId="hsc_27" />
      </main>

      <Footer />
    </div>
  );
}
