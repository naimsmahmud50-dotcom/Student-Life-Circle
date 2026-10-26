/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Institutional About & Sovereign Educational Mission Page
 * TOPIC:     Bengal Academic Editorial Monograph & Sovereign Pedagogy
 * FILE:      frontend/src/pages/about.tsx
 * PURPOSE:   Presents the sovereign academic mission, pedagogical philosophy, NCTB curriculum
 *            alignment, and technical architecture pillars of Ogrojatra (অগ্রযাত্রা).
 *            Elevated to authentic paper grain background, Noto Serif Bengali monograph headings,
 *            intentional asymmetrical editorial chapters, and tactile 3D cards.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  GraduationCap,
  BookOpen,
  ShieldCheck,
  Award,
  Compass,
  Users,
  Radio,
  FileCheck2,
  CheckCircle2,
  Cpu,
  Layers,
  Globe,
  ArrowRight,
  School,
  Lock,
  HeartHandshake
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { Badge, Button } from '@/components/ui';

export default function AboutPage() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const isDark = document.documentElement.classList.contains('dark');
      setTheme(isDark ? 'dark' : 'light');
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    if (typeof document !== 'undefined') {
      if (newTheme === 'dark') {
        document.documentElement.classList.add('dark');
        localStorage.setItem('slc_theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('slc_theme', 'light');
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col font-sans bg-[var(--color-paper-ground)] text-[var(--color-ink-primary)] bg-academic-paper-grain transition-colors duration-150">
      <AppHead
        title="আমাদের সম্পর্কে — জাতীয় সার্বভৌম শিক্ষামূলক প্ল্যাটফর্ম | অগ্রযাত্রা"
        description="অগ্রযাত্রা (Ogrojatra) — বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বজনীন, সার্বভৌম ও আন্তর্জাতিক মানের ডিজিটাল একাডেমিক ইকোসিস্টেম।"
        canonicalUrl="/about"
        ogType="website"
      />

      <Navbar
        currentStage="জাতীয় পাবলিক লঞ্চ সংস্করণ"
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-16 space-y-16">
        
        {/* ===================================================================
            SECTION 1: EDITORIAL MONOGRAPH HERO
            =================================================================== */}
        <section className="space-y-6 pt-2 max-w-4xl">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg bg-[#FDFCF9] dark:bg-[#171E2C] border border-[#E5E2DA] dark:border-[#263147] text-xs font-semibold text-[#525252] dark:text-[#A3A8B5] shadow-xs">
            <ShieldCheck className="w-4 h-4 text-[#065F46] dark:text-emerald-400 stroke-[2] shrink-0" />
            <span>গণপ্রজাতন্ত্রী বাংলাদেশ অনুমোদিত শিক্ষাক্রম ও সার্বভৌম এডুটেক প্ল্যাটফর্ম</span>
          </div>

          <div className="space-y-4">
            <span className="eyebrow-label block">প্রাতিষ্ঠানিক পরিচিতি ও শিক্ষাদর্শন</span>
            <h1 className="text-3xl sm:text-5xl lg:text-[46px] font-bold text-[#0A2540] dark:text-[#F5F2EB] tracking-tight leading-[1.25] font-serif-bn">
              অগ্রযাত্রা — বাংলাদেশের প্রতিটি শিক্ষার্থীর সার্বভৌম একাডেমিক ভবিষ্যৎ
            </h1>
            <p className="text-base sm:text-lg text-[#525252] dark:text-[#A3A8B5] leading-[1.78] max-w-3xl font-sans">
              ৬ষ্ঠ শ্রেণি থেকে জাতীয় বোর্ড পরীক্ষা, বিশ্ববিদ্যালয় ভর্তি ও পেশাগত ক্যারিয়ার — বাংলাদেশের শিক্ষার্থীদের জন্য একটি
              পূর্ণাঙ্গ, নিরাপদ, নজরদারি-মুক্ত ও আন্তর্জাতিক মানের শিক্ষামূলক অপারেটিং সিস্টেম।
            </p>
          </div>
        </section>

        {/* ===================================================================
            SECTION 2: 4 CORE INSTITUTIONAL PILLARS (Intentional Asymmetry)
            =================================================================== */}
        <section className="space-y-8">
          <div className="border-b border-[#E5E2DA] dark:border-[#263147] pb-4 flex flex-col sm:flex-row sm:items-end justify-between gap-2">
            <div>
              <span className="eyebrow-label block mb-1">মৌলিক স্তম্ভসমূহ</span>
              <h2 className="text-2xl sm:text-3xl font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                যে আদর্শে অগ্রযাত্রা নির্মিত
              </h2>
            </div>
            <span className="text-xs text-[#737373] dark:text-[#7D8494] font-medium font-sans">
              চারটি সার্বভৌম একাডেমিক ভিত্তি
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Pillar 1 */}
            <div className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#171E2C] p-6 sm:p-7 shadow-[0_3px_0_0_#D1CDC4,0_1px_3px_rgba(10,37,64,0.05)] dark:shadow-[0_3px_0_0_#1F283A] flex flex-col justify-between space-y-5 transition-all hover:-translate-y-0.5">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-11 h-11 rounded-lg bg-[#0A2540] text-white flex items-center justify-center shadow-[0_2px_0_0_#051329]">
                    <BookOpen className="w-5 h-5 stroke-[1.75]" />
                  </div>
                  <span className="text-xs font-mono font-bold text-[#737373] dark:text-[#7D8494]">অধ্যায় ০১</span>
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                  NCTB কারিকুলাম সামঞ্জস্য ও বোর্ড প্রশ্ন
                </h3>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.7]">
                  জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) অনুমোদিত বিগত ১০ বছরের বোর্ড প্রশ্ন এবং KaTeX নির্ভুল গাণিতিক সমাধানের সুবিশাল ডিজিটাল ভাণ্ডার।
                </p>
              </div>
              <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#263147] text-xs font-semibold text-[#065F46] dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>১০০% প্রাতিষ্ঠানিক সিলেবাস কভারেজ</span>
              </div>
            </div>

            {/* Pillar 2 */}
            <div className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#171E2C] p-6 sm:p-7 shadow-[0_3px_0_0_#D1CDC4,0_1px_3px_rgba(10,37,64,0.05)] dark:shadow-[0_3px_0_0_#1F283A] flex flex-col justify-between space-y-5 transition-all hover:-translate-y-0.5">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-11 h-11 rounded-lg bg-[#065F46] text-white flex items-center justify-center shadow-[0_2px_0_0_#033829]">
                    <ShieldCheck className="w-5 h-5 stroke-[1.75]" />
                  </div>
                  <span className="text-xs font-mono font-bold text-[#737373] dark:text-[#7D8494]">অধ্যায় ০২</span>
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                  নজরদারি-মুক্ত পরীক্ষা হল ও গোপনীয়তা
                </h3>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.7]">
                  কোনো ব্যক্তিগত ক্যামেরা নজরদারি ছাড়াই ক্লায়েন্ট সাইড হিউরিস্টিক এবং ক্রিপ্টোগ্রাফিক SHA-256 সিলের মাধ্যমে পরীক্ষার নিরপেক্ষ অখণ্ডতা বজায় রাখা হয়।
                </p>
              </div>
              <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#263147] text-xs font-semibold text-[#065F46] dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>শিক্ষার্থী গোপনীয়তা ও অধিকার প্রথম</span>
              </div>
            </div>

            {/* Pillar 3 */}
            <div className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#171E2C] p-6 sm:p-7 shadow-[0_3px_0_0_#D1CDC4,0_1px_3px_rgba(10,37,64,0.05)] dark:shadow-[0_3px_0_0_#1F283A] flex flex-col justify-between space-y-5 transition-all hover:-translate-y-0.5">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-11 h-11 rounded-lg bg-[#B45309] text-white flex items-center justify-center shadow-[0_2px_0_0_#78350F]">
                    <Radio className="w-5 h-5 stroke-[1.75]" />
                  </div>
                  <span className="text-xs font-mono font-bold text-[#737373] dark:text-[#7D8494]">অধ্যায় ০৩</span>
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                  প্রান্তিক অফলাইন রেজিলিয়েন্স মেশ
                </h3>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.7]">
                  হাওর, চর ও পাহাড়ি দুর্গম অঞ্চলের জন্য ইন্টারনেটহীন ৬০ জনের লোকাল Wi-Fi/ব্লুটুথ ক্লাসরুম স্টেশন এবং LoRaWAN ইমার্জেন্সি ব্যাকবোন সিঙ্ক সুবিধা।
                </p>
              </div>
              <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#263147] text-xs font-semibold text-[#B45309] dark:text-amber-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>৬৪ জেলায় ডিজিটাল বৈষম্য নিরসন</span>
              </div>
            </div>

            {/* Pillar 4 */}
            <div className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#171E2C] p-6 sm:p-7 shadow-[0_3px_0_0_#D1CDC4,0_1px_3px_rgba(10,37,64,0.05)] dark:shadow-[0_3px_0_0_#1F283A] flex flex-col justify-between space-y-5 transition-all hover:-translate-y-0.5">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-11 h-11 rounded-lg bg-[#0A2540] text-white flex items-center justify-center shadow-[0_2px_0_0_#051329]">
                    <Users className="w-5 h-5 stroke-[1.75]" />
                  </div>
                  <span className="text-xs font-mono font-bold text-[#737373] dark:text-[#7D8494]">অধ্যায় ০৪</span>
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                  শিক্ষাবিদ পিয়ার-রিভিউ ট্রাইব্যুনাল
                </h3>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.7]">
                  দ্বৈত-পরীক্ষক ব্লাইন্ড কনসেনসাস মডেল: ন্যূনতম ২ জন অভিজ্ঞ শিক্ষাবিদের যাচাই ও আনুষ্ঠানিক সিল ছাড়া কোনো প্রশ্ন লাইভ পুলে প্রবেশ করতে পারে না।
                </p>
              </div>
              <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#263147] text-xs font-semibold text-[#065F46] dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>শিক্ষাবিদদের সার্বভৌম সম্পাদকীয় মানদণ্ড</span>
              </div>
            </div>
          </div>
        </section>

        {/* ===================================================================
            SECTION 3: NATIONWIDE SRE RIGOR & METRICS
            =================================================================== */}
        <section className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#171E2C] p-8 sm:p-10 shadow-sm">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center divide-y md:divide-y-0 md:divide-x divide-[#E5E2DA] dark:divide-[#263147]">
            <div className="p-3">
              <span className="text-xs font-semibold text-[#737373] dark:text-[#7D8494] uppercase tracking-wider block mb-1">
                আর্কিটেকচারাল পর্যায়
              </span>
              <span className="text-3xl sm:text-4xl font-bold text-[#0A2540] dark:text-[#F5F2EB] tabular-nums">১২০টি</span>
              <span className="text-xs text-[#525252] dark:text-[#A3A8B5] block mt-1">১০০% স্পেসিফিকেশন সম্পন্ন</span>
            </div>

            <div className="p-3 pt-6 md:pt-3">
              <span className="text-xs font-semibold text-[#737373] dark:text-[#7D8494] uppercase tracking-wider block mb-1">
                স্বয়ংক্রিয় টেস্ট কাভারেজ
              </span>
              <span className="text-3xl sm:text-4xl font-bold text-[#065F46] dark:text-emerald-400 tabular-nums">১,৩৮০+</span>
              <span className="text-xs text-[#525252] dark:text-[#A3A8B5] block mt-1">১০০% উত্তীর্ণ (০ ব্যর্থতা)</span>
            </div>

            <div className="p-3 pt-6 md:pt-3">
              <span className="text-xs font-semibold text-[#737373] dark:text-[#7D8494] uppercase tracking-wider block mb-1">
                অ্যাক্সেসিবিলিটি স্ট্যান্ডার্ড
              </span>
              <span className="text-3xl sm:text-4xl font-bold text-[#0A2540] dark:text-[#F5F2EB]">AAA</span>
              <span className="text-xs text-[#525252] dark:text-[#A3A8B5] block mt-1">WCAG 2.2 সাব-পিক্সেল ক্ল্যারিটি</span>
            </div>

            <div className="p-3 pt-6 md:pt-3">
              <span className="text-xs font-semibold text-[#737373] dark:text-[#7D8494] uppercase tracking-wider block mb-1">
                জিরো-ইমোজি পলিসি
              </span>
              <span className="text-3xl sm:text-4xl font-bold text-[#0A2540] dark:text-[#F5F2EB]">১০০%</span>
              <span className="text-xs text-[#525252] dark:text-[#A3A8B5] block mt-1">বিশুদ্ধ ভেক্টর এসভিজি আইকন</span>
            </div>
          </div>
        </section>

        {/* ===================================================================
            SECTION 4: ETHICAL CHARTER & STUDENT PROTECTIONS
            =================================================================== */}
        <section className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FAF8F3] dark:bg-[#1E2738] p-8 sm:p-10 shadow-sm space-y-6 notebook-margin-accent">
          <div className="max-w-3xl space-y-2">
            <span className="eyebrow-label block">সার্বভৌম নৈতিক অঙ্গীকার</span>
            <h2 className="text-2xl font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
              শিক্ষার্থীদের ব্যক্তিগত নিরাপত্তা ও একাডেমিক মর্যাদার সুরক্ষা
            </h2>
            <p className="text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.75]">
              অগ্রযাত্রা শুধু একটি ডিজিটাল সফটওয়্যার নয়; এটি বাংলাদেশের শিক্ষা ব্যবস্থার সার্বভৌমত্বের প্রতীক।
              আমাদের প্রতিটি সিদ্ধান্ত পরিচালিত হয় শিক্ষক, শিক্ষার্থী ও অভিভাবকদের পারস্পরিক আস্থার ওপর।
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 pt-4 border-t border-[#E5E2DA] dark:border-[#263147]">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-[#FDFCF9] dark:bg-[#171E2C] border border-[#E5E2DA] dark:border-[#263147] flex items-center justify-center text-[#0A2540] dark:text-[#F5F2EB] shrink-0 shadow-xs">
                <Lock className="w-4 h-4" />
              </div>
              <div className="text-xs space-y-1">
                <strong className="block font-bold text-[#1A1A1A] dark:text-[#F5F2EB]">ডেটা বিক্রি নিষিদ্ধ</strong>
                <span className="text-[#525252] dark:text-[#A3A8B5] leading-relaxed block">শিক্ষার্থীর কোনো তথ্য বাণিজ্যিক বিজ্ঞাপনদাতার কাছে হস্তান্তর করা হয় না।</span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-[#FDFCF9] dark:bg-[#171E2C] border border-[#E5E2DA] dark:border-[#263147] flex items-center justify-center text-[#0A2540] dark:text-[#F5F2EB] shrink-0 shadow-xs">
                <HeartHandshake className="w-4 h-4" />
              </div>
              <div className="text-xs space-y-1">
                <strong className="block font-bold text-[#1A1A1A] dark:text-[#F5F2EB]">অভিভাবক সম্মতি নিশ্চিত</strong>
                <span className="text-[#525252] dark:text-[#A3A8B5] leading-relaxed block">টিউশন ফি ও যোগাযোগে অভিভাবকের পূর্ণ ডিজিটাল সম্মতি বাধ্যতামূলক।</span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-[#FDFCF9] dark:bg-[#171E2C] border border-[#E5E2DA] dark:border-[#263147] flex items-center justify-center text-[#0A2540] dark:text-[#F5F2EB] shrink-0 shadow-xs">
                <Award className="w-4 h-4" />
              </div>
              <div className="text-xs space-y-1">
                <strong className="block font-bold text-[#1A1A1A] dark:text-[#F5F2EB]">ন্যায্য মেধা স্বীকৃতি</strong>
                <span className="text-[#525252] dark:text-[#A3A8B5] leading-relaxed block">স্বচ্ছ মেধা অ্যালগরিদমের মাধ্যমে জাতীয় বৃত্তি সরাসরি ব্যাংক অ্যাকাউন্টে প্রদান।</span>
              </div>
            </div>
          </div>

          <div className="pt-4 flex justify-end">
            <Link
              href="/terms"
              className="btn-tactile-primary px-6 py-2.5 text-xs font-semibold rounded-lg text-white gap-2 inline-flex items-center"
            >
              <span>প্রাতিষ্ঠানিক ব্যবহারের নীতিমালা ও গোপনীয়তা সনদ পড়ুন</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </section>
      </main>

      <Footer theme={theme} />
    </div>
  );
}
