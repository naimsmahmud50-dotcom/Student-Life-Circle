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
import { useTranslation, toBengaliDigits } from '@/lib/i18n';

export default function AboutPage() {
  const { language } = useTranslation();
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    document.title = language === 'bn'
      ? 'আমাদের সম্পর্কে — জাতীয় সার্বভৌম শিক্ষামূলক প্ল্যাটফর্ম | অগ্রযাত্রা'
      : 'About Us — Sovereign National Educational Platform | Ogrojatra';
  }, [language]);

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
    <div className="min-h-screen flex flex-col font-sans bg-[var(--color-paper-ground)] bg-[#FAFAF8] text-[var(--color-ink-primary)] bg-academic-paper-grain transition-colors duration-150">
      <AppHead
        title={
          language === 'bn'
            ? 'আমাদের সম্পর্কে — জাতীয় সার্বভৌম শিক্ষামূলক প্ল্যাটফর্ম | অগ্রযাত্রা'
            : 'About Us — Sovereign National Educational Platform | Ogrojatra'
        }
        description={
          language === 'bn'
            ? 'অগ্রযাত্রা (Ogrojatra) — বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বজনীন, সার্বভৌম ও আন্তর্জাতিক মানের ডিজিটাল একাডেমিক ইকোসিস্টেম।'
            : 'Ogrojatra — A universal, sovereign, and world-class digital academic ecosystem for every student in Bangladesh.'
        }
        canonicalUrl="/about"
        ogType="website"
      />

      <Navbar
        currentStage={language === 'bn' ? 'জাতীয় পাবলিক লঞ্চ সংস্করণ' : 'National Public Launch Edition'}
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
            <span>
              {language === 'bn'
                ? 'গণপ্রজাতন্ত্রী বাংলাদেশ অনুমোদিত শিক্ষাক্রম ও সার্বভৌম এডুটেক প্ল্যাটফর্ম'
                : 'Curriculum Approved in Bangladesh & Sovereign EdTech Platform'}
            </span>
          </div>

          <div className="space-y-4">
            <span className="eyebrow-label block">
              {language === 'bn' ? 'প্রাতিষ্ঠানিক পরিচিতি ও শিক্ষাদর্শন' : 'Institutional Overview & Pedagogy'}
            </span>
            <h1 className="text-3xl sm:text-5xl lg:text-[46px] font-bold text-[#0A2540] dark:text-[#F5F2EB] tracking-tight leading-[1.25] font-serif-bn">
              {language === 'bn'
                ? 'অগ্রযাত্রা — বাংলাদেশের প্রতিটি শিক্ষার্থীর সার্বভৌম একাডেমিক ভবিষ্যৎ'
                : 'Ogrojatra — Sovereign Academic Future for Every Student in Bangladesh'}
            </h1>
            <p className="text-base sm:text-lg text-[#525252] dark:text-[#A3A8B5] leading-[1.78] max-w-3xl font-sans">
              {language === 'bn'
                ? '৬ষ্ঠ শ্রেণি থেকে জাতীয় বোর্ড পরীক্ষা, বিশ্ববিদ্যালয় ভর্তি ও পেশাগত ক্যারিয়ার — বাংলাদেশের শিক্ষার্থীদের জন্য একটি পূর্ণাঙ্গ, নিরাপদ, নজরদারি-মুক্ত ও আন্তর্জাতিক মানের শিক্ষামূলক অপারেটিং সিস্টেম।'
                : 'From Grade 6 to National Board Exams, University Admissions, and Professional Careers — a comprehensive, secure, surveillance-free, and world-class educational operating system for students in Bangladesh.'}
            </p>
          </div>
        </section>

        {/* ===================================================================
            SECTION 2: 4 CORE INSTITUTIONAL PILLARS (Intentional Asymmetry)
            =================================================================== */}
        <section className="space-y-8">
          <div className="border-b border-[#E5E2DA] dark:border-[#263147] pb-4 flex flex-col sm:flex-row sm:items-end justify-between gap-2">
            <div>
              <span className="eyebrow-label block mb-1">
                {language === 'bn' ? 'মৌলিক স্তম্ভসমূহ' : 'Core Architectural Pillars'}
              </span>
              <h2 className="text-2xl sm:text-3xl font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                {language === 'bn' ? 'যে আদর্শে অগ্রযাত্রা নির্মিত' : 'Foundational Principles of Ogrojatra'}
              </h2>
            </div>
            <span className="text-xs text-[#737373] dark:text-[#7D8494] font-medium font-sans">
              {language === 'bn' ? 'চারটি সার্বভৌম একাডেমিক ভিত্তি' : 'Four Sovereign Academic Foundations'}
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
                  <span className="text-xs font-mono font-bold text-[#737373] dark:text-[#7D8494]">
                    {language === 'bn' ? 'অধ্যায় ০১' : 'Chapter 01'}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                  {language === 'bn' ? 'NCTB কারিকুলাম সামঞ্জস্য ও বোর্ড প্রশ্ন' : 'NCTB Curriculum Alignment & Board Papers'}
                </h3>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.7]">
                  {language === 'bn'
                    ? 'জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) অনুমোদিত বিগত ১০ বছরের বোর্ড প্রশ্ন এবং KaTeX নির্ভুল গাণিতিক সমাধানের সুবিশাল ডিজিটাল ভাণ্ডার।'
                    : 'A comprehensive digital archive of past 10 years board examination papers authorized by NCTB with precision KaTeX mathematical explanations.'}
                </p>
              </div>
              <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#263147] text-xs font-semibold text-[#065F46] dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>{language === 'bn' ? '১০০% প্রাতিষ্ঠানিক সিলেবাস কভারেজ' : '100% Institutional Syllabus Coverage'}</span>
              </div>
            </div>

            {/* Pillar 2 */}
            <div className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#171E2C] p-6 sm:p-7 shadow-[0_3px_0_0_#D1CDC4,0_1px_3px_rgba(10,37,64,0.05)] dark:shadow-[0_3px_0_0_#1F283A] flex flex-col justify-between space-y-5 transition-all hover:-translate-y-0.5">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-11 h-11 rounded-lg bg-[#065F46] text-white flex items-center justify-center shadow-[0_2px_0_0_#033829]">
                    <ShieldCheck className="w-5 h-5 stroke-[1.75]" />
                  </div>
                  <span className="text-xs font-mono font-bold text-[#737373] dark:text-[#7D8494]">
                    {language === 'bn' ? 'অধ্যায় ০২' : 'Chapter 02'}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                  {language === 'bn' ? 'নজরদারি-মুক্ত পরীক্ষা হল ও গোপনীয়তা' : 'Surveillance-Free Exam Hall & Privacy'}
                </h3>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.7]">
                  {language === 'bn'
                    ? 'কোনো ব্যক্তিগত ক্যামেরা নজরদারি ছাড়াই ক্লায়েন্ট সাইড হিউরিস্টিক এবং ক্রিপ্টোগ্রাফিক SHA-256 সিলের মাধ্যমে পরীক্ষার নিরপেক্ষ অখণ্ডতা বজায় রাখা হয়।'
                    : 'Exam integrity is preserved through client-side heuristics and cryptographic SHA-256 seals without intrusive camera or audio surveillance.'}
                </p>
              </div>
              <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#263147] text-xs font-semibold text-[#065F46] dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>{language === 'bn' ? 'শিক্ষার্থী গোপনীয়তা ও অধিকার প্রথম' : 'Student Privacy & Dignity First'}</span>
              </div>
            </div>

            {/* Pillar 3 */}
            <div className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#171E2C] p-6 sm:p-7 shadow-[0_3px_0_0_#D1CDC4,0_1px_3px_rgba(10,37,64,0.05)] dark:shadow-[0_3px_0_0_#1F283A] flex flex-col justify-between space-y-5 transition-all hover:-translate-y-0.5">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-11 h-11 rounded-lg bg-[#B45309] text-white flex items-center justify-center shadow-[0_2px_0_0_#78350F]">
                    <Radio className="w-5 h-5 stroke-[1.75]" />
                  </div>
                  <span className="text-xs font-mono font-bold text-[#737373] dark:text-[#7D8494]">
                    {language === 'bn' ? 'অধ্যায় ০৩' : 'Chapter 03'}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                  {language === 'bn' ? 'প্রান্তিক অফলাইন মেশ' : 'Marginal Offline Mesh'}
                </h3>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.7]">
                  {language === 'bn'
                    ? 'হাওর, চর ও পাহাড়ি দুর্গম অঞ্চলের জন্য ইন্টারনেটহীন ৬০ জনের লোকাল Wi-Fi/ব্লুটুথ ক্লাসরুম স্টেশন এবং LoRaWAN ইমার্জেন্সি ব্যাকবোন সিঙ্ক সুবিধা।'
                    : 'Local Wi-Fi/Bluetooth classroom stations for up to 60 learners and LoRaWAN emergency sync designed for remote haor, char, and hill-tract regions.'}
                </p>
              </div>
              <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#263147] text-xs font-semibold text-[#B45309] dark:text-amber-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>{language === 'bn' ? '৬৪ জেলায় ডিজিটাল বৈষম্য নিরসন' : 'Bridging Digital Divide Across 64 Districts'}</span>
              </div>
            </div>

            {/* Pillar 4 */}
            <div className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#171E2C] p-6 sm:p-7 shadow-[0_3px_0_0_#D1CDC4,0_1px_3px_rgba(10,37,64,0.05)] dark:shadow-[0_3px_0_0_#1F283A] flex flex-col justify-between space-y-5 transition-all hover:-translate-y-0.5">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-11 h-11 rounded-lg bg-[#0A2540] text-white flex items-center justify-center shadow-[0_2px_0_0_#051329]">
                    <Users className="w-5 h-5 stroke-[1.75]" />
                  </div>
                  <span className="text-xs font-mono font-bold text-[#737373] dark:text-[#7D8494]">
                    {language === 'bn' ? 'অধ্যায় ০৪' : 'Chapter 04'}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
                  {language === 'bn' ? 'শিক্ষাবিদ পিয়ার-রিভিউ ট্রাইব্যুনাল' : 'Academic Peer-Review Tribunal'}
                </h3>
                <p className="text-xs sm:text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.7]">
                  {language === 'bn'
                    ? 'দ্বৈত-পরীক্ষক ব্লাইন্ড কনসেনসাস মডেল: ন্যূনতম ২ জন অভিজ্ঞ শিক্ষাবিদের যাচাই ও আনুষ্ঠানিক সিল ছাড়া কোনো প্রশ্ন লাইভ পুলে প্রবেশ করতে পারে না।'
                    : 'Dual-examiner blind consensus model: no question enters the live pool without verification and official seals from at least 2 vetted educators.'}
                </p>
              </div>
              <div className="pt-3 border-t border-[#E5E2DA] dark:border-[#263147] text-xs font-semibold text-[#065F46] dark:text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>{language === 'bn' ? 'শিক্ষাবিদদের সার্বভৌম সম্পাদকীয় মানদণ্ড' : 'Sovereign Editorial Standard of Educators'}</span>
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
                {language === 'bn' ? 'আর্কিটেকচারাল পর্যায়' : 'Architectural Phases'}
              </span>
              <span className="text-3xl sm:text-4xl font-bold text-[#0A2540] dark:text-[#F5F2EB] tabular-nums">
                {language === 'bn' ? '১২০ টি' : '120'}
              </span>
              <span className="text-xs text-[#525252] dark:text-[#A3A8B5] block mt-1">
                {language === 'bn' ? '১০০% স্পেসিফিকেশন সম্পন্ন' : '100% Specifications Complete'}
              </span>
            </div>

            <div className="p-3 pt-6 md:pt-3">
              <span className="text-xs font-semibold text-[#737373] dark:text-[#7D8494] uppercase tracking-wider block mb-1">
                {language === 'bn' ? 'স্বয়ংক্রিয় টেস্ট কাভারেজ' : 'Automated Test Coverage'}
              </span>
              <span className="text-3xl sm:text-4xl font-bold text-[#065F46] dark:text-emerald-400 tabular-nums">
                {language === 'bn' ? '১,৩৮০+' : '1,380+'}
              </span>
              <span className="text-xs text-[#525252] dark:text-[#A3A8B5] block mt-1">
                {language === 'bn' ? '১০০% উত্তীর্ণ (০ ব্যর্থতা)' : '100% Passing (0 Failures)'}
              </span>
            </div>

            <div className="p-3 pt-6 md:pt-3">
              <span className="text-xs font-semibold text-[#737373] dark:text-[#7D8494] uppercase tracking-wider block mb-1">
                {language === 'bn' ? 'অ্যাক্সেসিবিলিটি স্ট্যান্ডার্ড' : 'Accessibility Standard'}
              </span>
              <span className="text-3xl sm:text-4xl font-bold text-[#0A2540] dark:text-[#F5F2EB]">AAA</span>
              <span className="text-xs text-[#525252] dark:text-[#A3A8B5] block mt-1">
                {language === 'bn' ? 'WCAG 2.2 সাব-পিক্সেল ক্ল্যারিটি' : 'WCAG 2.2 Sub-Pixel Clarity'}
              </span>
            </div>

            <div className="p-3 pt-6 md:pt-3">
              <span className="text-xs font-semibold text-[#737373] dark:text-[#7D8494] uppercase tracking-wider block mb-1">
                {language === 'bn' ? 'জিরো-ইমোজি পলিসি' : 'Zero-Emoji Policy'}
              </span>
              <span className="text-3xl sm:text-4xl font-bold text-[#0A2540] dark:text-[#F5F2EB]">
                {language === 'bn' ? '১০০%' : '100%'}
              </span>
              <span className="text-xs text-[#525252] dark:text-[#A3A8B5] block mt-1">
                {language === 'bn' ? 'বিশুদ্ধ ভেক্টর এসভিজি আইকন' : 'Pure Vector SVG Icons'}
              </span>
            </div>
          </div>
        </section>

        {/* ===================================================================
            SECTION 4: ETHICAL CHARTER & STUDENT PROTECTIONS
            =================================================================== */}
        <section className="rounded-lg border border-[#E5E2DA] dark:border-[#263147] bg-[#FAF8F3] dark:bg-[#1E2738] p-8 sm:p-10 shadow-sm space-y-6 notebook-margin-accent">
          <div className="max-w-3xl space-y-2">
            <span className="eyebrow-label block">
              {language === 'bn' ? 'সার্বভৌম নৈতিক অঙ্গীকার' : 'Sovereign Ethical Charter'}
            </span>
            <h2 className="text-2xl font-bold text-[#0A2540] dark:text-[#F5F2EB] font-serif-bn">
              {language === 'bn'
                ? 'শিক্ষার্থীদের ব্যক্তিগত নিরাপত্তা ও একাডেমিক মর্যাদার সুরক্ষা'
                : 'Safeguarding Student Privacy & Academic Dignity'}
            </h2>
            <p className="text-sm text-[#525252] dark:text-[#A3A8B5] leading-[1.75]">
              {language === 'bn'
                ? 'অগ্রযাত্রা শুধু একটি ডিজিটাল সফটওয়্যার নয়; এটি বাংলাদেশের শিক্ষা ব্যবস্থার সার্বভৌমত্বের প্রতীক। আমাদের প্রতিটি সিদ্ধান্ত পরিচালিত হয় শিক্ষক, শিক্ষার্থী ও অভিভাবকদের পারস্পরিক আস্থার ওপর।'
                : 'Ogrojatra is not just software; it is a symbol of educational sovereignty in Bangladesh. Every decision is guided by mutual trust among teachers, students, and guardians.'}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5 pt-4 border-t border-[#E5E2DA] dark:border-[#263147]">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-[#FDFCF9] dark:bg-[#171E2C] border border-[#E5E2DA] dark:border-[#263147] flex items-center justify-center text-[#0A2540] dark:text-[#F5F2EB] shrink-0 shadow-xs">
                <Lock className="w-4 h-4" />
              </div>
              <div className="text-xs space-y-1">
                <strong className="block font-bold text-[#1A1A1A] dark:text-[#F5F2EB]">
                  {language === 'bn' ? 'ডেটা বিক্রি নিষিদ্ধ' : 'Data Monetization Prohibited'}
                </strong>
                <span className="text-[#525252] dark:text-[#A3A8B5] leading-relaxed block">
                  {language === 'bn'
                    ? 'শিক্ষার্থীর কোনো তথ্য বাণিজ্যিক বিজ্ঞাপনদাতার কাছে হস্তান্তর করা হয় না।'
                    : 'No student data is ever sold or transferred to commercial advertisers.'}
                </span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-[#FDFCF9] dark:bg-[#171E2C] border border-[#E5E2DA] dark:border-[#263147] flex items-center justify-center text-[#0A2540] dark:text-[#F5F2EB] shrink-0 shadow-xs">
                <HeartHandshake className="w-4 h-4" />
              </div>
              <div className="text-xs space-y-1">
                <strong className="block font-bold text-[#1A1A1A] dark:text-[#F5F2EB]">
                  {language === 'bn' ? 'অভিভাবক সম্মতি নিশ্চিত' : 'Verified Guardian Consent'}
                </strong>
                <span className="text-[#525252] dark:text-[#A3A8B5] leading-relaxed block">
                  {language === 'bn'
                    ? 'টিউশন ফি ও যোগাযোগে অভিভাবকের পূর্ণ ডিজিটাল সম্মতি বাধ্যতামূলক।'
                    : 'Mandatory digital parental consent for all tuition transactions and communications.'}
                </span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-lg bg-[#FDFCF9] dark:bg-[#171E2C] border border-[#E5E2DA] dark:border-[#263147] flex items-center justify-center text-[#0A2540] dark:text-[#F5F2EB] shrink-0 shadow-xs">
                <Award className="w-4 h-4" />
              </div>
              <div className="text-xs space-y-1">
                <strong className="block font-bold text-[#1A1A1A] dark:text-[#F5F2EB]">
                  {language === 'bn' ? 'ন্যায্য মেধা স্বীকৃতি' : 'Merit-Based Recognition'}
                </strong>
                <span className="text-[#525252] dark:text-[#A3A8B5] leading-relaxed block">
                  {language === 'bn'
                    ? 'স্বচ্ছ মেধা অ্যালগরিদমের মাধ্যমে জাতীয় বৃত্তি সরাসরি ব্যাংক অ্যাকাউন্টে প্রদান।'
                    : 'Transparent merit algorithms routing national scholarship stipends directly to student bank accounts.'}
                </span>
              </div>
            </div>
          </div>

          <div className="pt-4 flex justify-end">
            <Link
              href="/terms"
              className="btn-tactile-primary px-6 py-2.5 text-xs font-semibold rounded-lg text-white gap-2 inline-flex items-center"
            >
              <span>
                {language === 'bn'
                  ? 'প্রাতিষ্ঠানিক ব্যবহারের নীতিমালা ও গোপনীয়তা সনদ পড়ুন'
                  : 'Read Institutional Terms of Service & Privacy Charter'}
              </span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </section>
      </main>

      <Footer theme={theme} />
    </div>
  );
}
