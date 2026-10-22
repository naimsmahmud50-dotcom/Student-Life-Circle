/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Enterprise Modules Directory Page
 * TOPIC:     Phase 138 Unified Premium Design System & Sub-pages Elevation
 * FILE:      frontend/src/pages/modules.tsx
 * PHASE:     Phase 138 - Unified Premium Design for Sub-pages
 * PURPOSE:   Standardized academic enterprise directory page with flagship
 *            PageHeader, global Navbar & Footer, and zero-emoji design tokens.
 * STANDARDS: Zero-Emoji, Pure Academic Design, WCAG 2.2 AAA, UI/UX Pro Max
 */

import React from 'react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { PageHeader } from '@/components/layout/PageHeader';
import { ModuleDirectory } from '@/modules/ModuleDirectory';
import { Layers } from 'lucide-react';

export default function ModulesPage() {
  return (
    <div className="min-h-screen flex flex-col bg-[#FAFAF8] dark:bg-[#090D16] text-slate-900 dark:text-slate-100 font-sans transition-colors duration-200">
      <AppHead
        title="৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি | অগ্রযাত্রা"
        description="৬৯টি স্বয়ংক্রিয় এন্টারপ্রাইজ রিসার্চ, স্টেম ল্যাব, অফলাইন রেজিলিয়েন্স ও একাডেমি মডিউল হাব।"
        canonicalUrl="/modules"
        ogType="website"
      />

      <Navbar currentStage="এন্টারপ্রাইজ মডিউল ডিরেক্টরি" />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
        <PageHeader
          category="এন্টারপ্রাইজ আর্কিটেকচার"
          title="৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি"
          subtitle="স্বয়ংক্রিয় এন্টারপ্রাইজ রিসার্চ, স্টেম ল্যাব, অফলাইন রেজিলিয়েন্স ও একাডেমি মডিউল হাব। শিক্ষার্থী কোর ভিউ এবং আর্কিটেক্ট ডিরেক্টরির মধ্যে তাৎক্ষণিক রূপান্তর।"
          breadcrumbs={[
            { label: 'নীড়পাতা', href: '/' },
            { label: 'এন্টারপ্রাইজ আর্কিটেকচার' }
          ]}
          stats={[
            { label: 'শিক্ষার্থী কোর হাব', value: '৫টি মডিউল' },
            { label: 'মোট মডিউল', value: '৬৯টি এন্টারপ্রাইজ', highlight: true },
            { label: 'বান্ডেল লোডিং', value: 'অন-ডিমান্ড ডায়নামিক' },
            { label: 'নিরাপত্তা স্ট্যান্ডার্ড', value: 'ASVS L2' }
          ]}
        />

        <ModuleDirectory />
      </main>

      <Footer />
    </div>
  );
}
