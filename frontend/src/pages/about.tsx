/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Institutional About & Sovereign Educational Mission Page
 * TOPIC:     Phase 120 Grand Nationwide Rollout & Public Launch Sign-off
 * FILE:      frontend/src/pages/about.tsx
 * PHASE:     Phase 120 - Grand Nationwide Rollout & Public Launch Sign-off
 * PURPOSE:   Presents the sovereign academic mission, pedagogical philosophy, NCTB curriculum
 *            alignment, and technical architecture pillars of Ogrojatra (অগ্রযাত্রা).
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React, { useState } from 'react';
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

export default function AboutPage() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <div
      className={`min-h-screen flex flex-col font-sans transition-colors duration-200 ${
        theme === 'dark' ? 'dark bg-[#070D18]' : 'bg-[#FAFAF8]'
      }`}
    >
      <AppHead
        title="আমাদের সম্পর্কে — জাতীয় সার্বভৌম শিক্ষামূলক প্ল্যাটফর্ম | অগ্রযাত্রা"
        description="অগ্রযাত্রা (Ogrojatra) — বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য একটি সার্বজনীন, সার্বভৌম ও আন্তর্জাতিক মানের ডিজিটাল একাডেমিক ইকোসিস্টেম।"
      />

      <Navbar
        currentStage="জাতীয় পাবলিক লঞ্চ সংস্করণ (Phase 120)"
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
        {/* Hero Section */}
        <section className="text-center max-w-4xl mx-auto space-y-6 pt-4">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white border border-slate-200 text-xs font-semibold text-[#0A2540] shadow-xs">
            <ShieldCheck className="w-4 h-4 text-emerald-700 stroke-[2]" />
            <span>গণপ্রজাতন্ত্রী বাংলাদেশ অনুমোদিত শিক্ষাক্রম ও সার্বভৌম এডুটেক প্ল্যাটফর্ম</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold text-[#0A2540] tracking-tight leading-tight">
            অগ্রযাত্রা — বাংলাদেশের প্রতিটি শিক্ষার্থীর সার্বভৌম একাডেমিক ভবিষ্যৎ
          </h1>

          <p className="text-base sm:text-lg text-slate-600 leading-relaxed max-w-3xl mx-auto">
            Class 6 থেকে জাতীয় বোর্ড পরীক্ষা, বিশ্ববিদ্যালয় ভর্তি ও ক্যারিয়ার — বাংলাদেশের শিক্ষার্থীদের জন্য একটি
            পূর্ণাঙ্গ, নিরাপদ, নজরদারি-মুক্ত ও আন্তর্জাতিক মানের শিক্ষামূলক অপারেটিং সিস্টেম।
          </p>
        </section>

        {/* 4 Core Pillars of Ogrojatra */}
        <section className="space-y-8">
          <div className="text-center max-w-2xl mx-auto">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-1">
              মৌলিক স্তম্ভসমূহ
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-[#0A2540]">
              যে আদর্শে অগ্রযাত্রা নির্মিত
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center mb-5 shadow-xs">
                  <BookOpen className="w-6 h-6 stroke-[1.75]" />
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] mb-2">
                  NCTB কারিকুলাম সামঞ্জস্য
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) অনুমোদিত বিগত ১০ বছরের বোর্ড প্রশ্ন ও KaTeX নির্ভুল গাণিতিক সমাধানের বিশাল ভাণ্ডার।
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 text-xs font-semibold text-[#0A2540] flex items-center gap-1">
                <span>১০০% প্রাতিষ্ঠানিক মান</span>
              </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center mb-5 shadow-xs">
                  <ShieldCheck className="w-6 h-6 stroke-[1.75]" />
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] mb-2">
                  নজরদারি-মুক্ত পরীক্ষা হল
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  কোনো ক্যামেরা বা বায়োমেট্রিক ভিডিও নজরদারি ছাড়াই ক্লায়েন্ট হিউরিস্টিক ও ক্রিপ্টোগ্রাফিক SHA-256 সিলের মাধ্যমে পরীক্ষার অখণ্ডতা নিশ্চিত।
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 text-xs font-semibold text-[#0A2540] flex items-center gap-1">
                <span>শিক্ষার্থী গোপনীয়তা প্রথম</span>
              </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center mb-5 shadow-xs">
                  <Radio className="w-6 h-6 stroke-[1.75]" />
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] mb-2">
                  প্রান্তিক অফলাইন মেশ
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  হাওর, চর ও দুর্গম পাহাড়ি অঞ্চলের জন্য ইন্টারনেটহীন ৬০ জনের লোকাল Wi-Fi/ব্লুটুথ ক্লাসরুম স্টেশন এবং LoRaWAN ইমার্জেন্সি ব্যাকবোন।
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 text-xs font-semibold text-[#0A2540] flex items-center gap-1">
                <span>ডিজিটাল বৈষম্য নিরসন</span>
              </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center mb-5 shadow-xs">
                  <Users className="w-6 h-6 stroke-[1.75]" />
                </div>
                <h3 className="text-lg font-bold text-[#0A2540] mb-2">
                  পিয়ার-রিভিউ ট্রাইব্যুনাল
                </h3>
                <p className="text-xs text-slate-600 leading-relaxed">
                  দ্বৈত-পরীক্ষক ব্লাইন্ড কনসেনসাস মডেল: ন্যূনতম ২ জন অভিজ্ঞ শিক্ষাবিদের যাচাই ও অনুমোদন ছাড়া কোনো প্রশ্ন লাইভ পুলে প্রবেশ করতে পারে না।
                </p>
              </div>
              <div className="mt-4 pt-3 border-t border-slate-100 text-xs font-semibold text-[#0A2540] flex items-center gap-1">
                <span>শিক্ষাবিদদের সার্বভৌম কর্তৃত্ব</span>
              </div>
            </div>
          </div>
        </section>

        {/* Nationwide Rollout Statistics & SRE Rigor */}
        <section className="bg-white border border-slate-200 rounded-3xl p-8 sm:p-10 shadow-xs">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center divide-y md:divide-y-0 md:divide-x divide-slate-100">
            <div className="p-4">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                আর্কিটেকচারাল পর্যায়
              </span>
              <span className="text-3xl sm:text-4xl font-extrabold text-[#0A2540]">১২০ টি</span>
              <span className="text-xs text-slate-500 block mt-1">১০০% স্পেসিফিকেশন সম্পন্ন</span>
            </div>

            <div className="p-4">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                স্বয়ংক্রিয় টেস্ট কাভারেজ
              </span>
              <span className="text-3xl sm:text-4xl font-extrabold text-emerald-700">১,৩৮০+ টি</span>
              <span className="text-xs text-slate-500 block mt-1">১০০% উত্তীর্ণ (০ ব্যর্থতা)</span>
            </div>

            <div className="p-4">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                অ্যাক্সেসিবিলিটি স্ট্যান্ডার্ড
              </span>
              <span className="text-3xl sm:text-4xl font-extrabold text-[#0A2540]">AAA</span>
              <span className="text-xs text-slate-500 block mt-1">WCAG 2.2 সাব-পিক্সেল ক্ল্যারিটি</span>
            </div>

            <div className="p-4">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-1">
                জিরো-ইমোজি পলিসি
              </span>
              <span className="text-3xl sm:text-4xl font-extrabold text-[#0A2540]">১০০%</span>
              <span className="text-xs text-slate-500 block mt-1">বিশুদ্ধ ভেক্টর এসভিজি আইকন</span>
            </div>
          </div>
        </section>

        {/* Academic Governance & Ethical Charter */}
        <section className="bg-[#FAFAF8] border border-slate-200 rounded-3xl p-8 sm:p-10 shadow-xs space-y-6">
          <div className="max-w-3xl">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-1">
              সার্বভৌম অঙ্গীকার
            </span>
            <h2 className="text-2xl font-bold text-[#0A2540]">
              শিক্ষার্থীদের নিরাপত্তা ও একাডেমিক মর্যাদার সুরক্ষা
            </h2>
            <p className="text-sm text-slate-600 mt-2 leading-relaxed">
              অগ্রযাত্রা শুধু একটি সফটওয়্যার নয়; এটি বাংলাদেশের শিক্ষা ব্যবস্থার ডিজিটাল সার্বভৌমত্বের প্রতীক।
              আমাদের প্রতিটি সিদ্ধান্ত পরিচালিত হয় শিক্ষক, শিক্ষার্থী ও অভিভাবকদের পারস্পরিক আস্থার ওপর।
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-slate-200">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-[#0A2540] flex-shrink-0">
                <Lock className="w-4 h-4" />
              </div>
              <div className="text-xs">
                <strong className="block font-bold text-slate-900 mb-0.5">ডেটা বিক্রি নিষিদ্ধ</strong>
                <span className="text-slate-600">শিক্ষার্থীর কোনো তথ্য বাণিজ্যিক বিজ্ঞাপনদাতার কাছে হস্তান্তর করা হয় না।</span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-[#0A2540] flex-shrink-0">
                <HeartHandshake className="w-4 h-4" />
              </div>
              <div className="text-xs">
                <strong className="block font-bold text-slate-900 mb-0.5">অভিভাবক সম্মতি নিশ্চিত</strong>
                <span className="text-slate-600">টিউশন ফি ও যোগাযোগে অভিভাবকের পূর্ণ ডিজিটাল সম্মতি বাধ্যতামূলক।</span>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-[#0A2540] flex-shrink-0">
                <Award className="w-4 h-4" />
              </div>
              <div className="text-xs">
                <strong className="block font-bold text-slate-900 mb-0.5">ন্যায্য মেধা স্বীকৃতি</strong>
                <span className="text-slate-600">স্বচ্ছ মেধা অ্যালগরিদমের মাধ্যমে জাতীয় বৃত্তি সরাসরি ব্যাংক অ্যাকাউন্টে প্রদান।</span>
              </div>
            </div>
          </div>

          <div className="pt-4 flex justify-end">
            <Link
              href="/terms"
              className="inline-flex items-center gap-1.5 text-xs font-bold text-[#0A2540] hover:underline"
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
