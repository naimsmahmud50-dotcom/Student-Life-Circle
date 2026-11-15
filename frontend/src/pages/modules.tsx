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

import React, { useEffect } from 'react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { PageHeader } from '@/components/layout/PageHeader';
import { ModuleDirectory } from '@/modules/ModuleDirectory';
import { Layers } from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export default function ModulesPage() {
  const { t, locale } = useTranslation();
  const isBn = locale === 'bn';

  const title = isBn
    ? "৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি | অগ্রযাত্রা"
    : "69 Enterprise Modules Directory | Ogrojatra";
  const description = isBn
    ? "৬৯টি স্বয়ংক্রিয় এন্টারপ্রাইজ রিসার্চ, স্টেম ল্যাব, অফলাইন রেজিলিয়েন্স ও একাডেমি মডিউল হাব।"
    : "69 automated enterprise research, STEM labs, offline resilience and academic module directory.";

  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.title = title;
    }
  }, [title]);

  return (
    <div className="min-h-screen flex flex-col bg-[#FAFAF8] dark:bg-[#090D16] bg-academic-graph text-slate-900 dark:text-slate-100 font-sans transition-colors duration-200">
      <AppHead
        title={title}
        description={description}
        canonicalUrl="/modules"
        ogType="website"
      />

      <Navbar currentStage={isBn ? "এন্টারপ্রাইজ মডিউল ডিরেক্টরি" : "Enterprise Modules Directory"} />

      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
        <PageHeader
          category={isBn ? "এন্টারপ্রাইজ আর্কিটেকচার" : "Enterprise Architecture"}
          title={isBn ? "৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি" : "69 Enterprise Modules Directory"}
          subtitle={
            isBn
              ? "স্বয়ংক্রিয় এন্টারপ্রাইজ রিসার্চ, স্টেম ল্যাব, অফলাইন রেজিলিয়েন্স ও একাডেমি মডিউল হাব। শিক্ষার্থী কোর ভিউ এবং আর্কিটেক্ট ডিরেক্টরির মধ্যে তাৎক্ষণিক রূপান্তর।"
              : "Automated enterprise research, STEM labs, offline resilience and academic module hub. Instant toggle between student core and architect directory."
          }
          breadcrumbs={[
            { label: isBn ? 'নীড়পাতা' : 'Home', href: '/' },
            { label: isBn ? 'এন্টারপ্রাইজ আর্কিটেকচার' : 'Enterprise Architecture' }
          ]}
          stats={[
            { label: isBn ? 'শিক্ষার্থী কোর হাব' : 'Student Core Hub', value: isBn ? '৫টি মডিউল' : '5 Modules' },
            { label: isBn ? 'মোট মডিউল' : 'Total Modules', value: isBn ? '৬৯টি এন্টারপ্রাইজ' : '69 Enterprise', highlight: true },
            { label: isBn ? 'বান্ডেল লোডিং' : 'Bundle Loading', value: isBn ? 'অন-ডিমান্ড ডায়নামিক' : 'On-Demand Dynamic' },
            { label: isBn ? 'নিরাপত্তা স্ট্যান্ডার্ড' : 'Security Standard', value: 'ASVS L2' }
          ]}
        />

        <ModuleDirectory />
      </main>

      <Footer />
    </div>
  );
}
