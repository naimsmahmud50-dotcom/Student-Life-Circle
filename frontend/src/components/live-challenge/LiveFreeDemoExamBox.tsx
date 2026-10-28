/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ 2D Elevation & Free Demo Diagnostic Box
 * FILE:      frontend/src/components/live-challenge/LiveFreeDemoExamBox.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Reverse-engineers and elevates Live MCQ's "dxb" (Demo Exam Box) section:
 *            instant diagnostic entry, 20 curated questions, 15m timer, -0.25 negative marking,
 *            editorial typography, and live interactive sample question with Socratic explanation.
 * STANDARDS: Zero-Emoji, Zero-AI Vibe, WCAG 2.2 AAA Contrast, Human Craftsmanship
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Sparkles,
  Clock,
  HelpCircle,
  AlertTriangle,
  ArrowRight,
  CheckCircle2
} from 'lucide-react';

export function LiveFreeDemoExamBox() {
  const [isDiagnosticStarted, setIsDiagnosticStarted] = useState<boolean>(false);

  return (
    <div id="demo-exam" className="relative overflow-hidden rounded-3xl bg-[#07192F]/90 backdrop-blur-md text-white p-8 sm:p-12 border border-cyan-500/25 shadow-2xl">
      {/* Refined Architectural Hairline Grid */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden select-none" aria-hidden="true">
        <div
          className="absolute inset-0 opacity-[0.04]"
          style={{
            backgroundImage:
              'radial-gradient(circle, #ffffff 1px, transparent 1px), linear-gradient(to right, rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.05) 1px, transparent 1px)',
            backgroundSize: '32px 32px, 64px 64px, 64px 64px'
          }}
        />
        <div className="absolute inset-2 border border-white/5 rounded-2xl pointer-events-none" />
      </div>

      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        
        {/* Left Column: Copy & Specs */}
        <div className="lg:col-span-7 space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#0A2540]/80 border border-cyan-500/30 text-xs font-bold font-bengali text-amber-300">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" />
            <span>সরাসরি মেধা যাচাই • কোনো রেজিস্ট্রেশন ছাড়াই</span>
          </div>

          <div className="space-y-3">
            <h2 className="text-2xl sm:text-4xl font-bold text-white font-serif tracking-tight">
              <span className="text-amber-400 font-serif">
                ফ্রি ডেমো
              </span>{' '}
              এক্সাম দিন
            </h2>

            <p className="text-sm text-slate-300 font-bengali leading-[1.8] max-w-xl">
              ফ্রি ডেমো পরীক্ষা দিয়ে নিজের প্রস্তুতি যাচাই করুন। কুইজ শেষে জানুন কোন বিষয়ে আপনি এগিয়ে, আর কোথায় দরকার আরও ধারাবাহিক প্রস্তুতি।
            </p>
          </div>

          {/* Specs List */}
          <ul className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2">
            <li className="p-3.5 rounded-xl bg-[#0A2540]/80 border border-cyan-500/25">
              <div className="text-xl sm:text-2xl font-black font-mono text-amber-300 flex items-baseline gap-1">
                ২০ <span className="text-xs font-bengali text-slate-300 font-normal">টি</span>
              </div>
              <div className="text-xs text-slate-300 font-bengali mt-0.5">
                বাছাইকৃত প্রশ্ন
              </div>
            </li>

            <li className="p-3.5 rounded-xl bg-[#0A2540]/80 border border-cyan-500/25">
              <div className="text-xl sm:text-2xl font-black font-mono text-sky-300 flex items-baseline gap-1">
                ১৫ <span className="text-xs font-bengali text-slate-300 font-normal">মিনিট</span>
              </div>
              <div className="text-xs text-slate-300 font-bengali mt-0.5">
                নির্ধারিত সময়
              </div>
            </li>

            <li className="p-3.5 rounded-xl bg-[#0A2540]/80 border border-rose-500/40 col-span-2 sm:col-span-1">
              <div className="text-xl sm:text-2xl font-black font-mono text-rose-300">
                -০.২৫
              </div>
              <div className="text-xs text-rose-300 font-bengali mt-0.5">
                নেগেটিভ মার্কিং
              </div>
            </li>
          </ul>

          {/* Action Trigger */}
          <div className="pt-2 flex flex-wrap items-center gap-4">
            <Link
              href="/practice?demo=standard"
              className="px-8 py-3.5 rounded-2xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold font-bengali text-sm shadow-[0_4px_0_0_#B45309] active:translate-y-1 active:shadow-none transition flex items-center justify-center gap-2"
            >
              <span>ডেমো পরীক্ষা শুরু করুন</span>
              <ArrowRight className="w-4 h-4 text-slate-950" />
            </Link>

            <span className="text-xs font-bengali text-slate-300 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>তাৎক্ষণিক ফলাফল ও বিস্তারিত ব্যাখ্যা</span>
            </span>
          </div>
        </div>

        {/* Right Column: Live Diagnostic Preview Box */}
        <div className="lg:col-span-5 p-6 rounded-2xl bg-[#061426]/95 border border-cyan-500/30 shadow-2xl space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-cyan-500/20">
            <span className="text-xs font-mono text-amber-300 font-bold uppercase">
              নমুনা প্রশ্ন ০১ • এইচএসসি পদার্থবিজ্ঞান
            </span>
            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-300 border border-emerald-500/40">
              সঠিক উত্তর: +১.০
            </span>
          </div>

          <div className="space-y-3">
            <p className="text-sm font-bengali text-white leading-relaxed">
              একটি সরল দোলকের কার্যকর দৈর্ঘ্য দ্বিগুণ করা হলে তার দোলনকালের কী পরিবর্তন ঘটবে?
            </p>

            <div className="space-y-2 text-xs font-bengali">
              <div className="p-2.5 rounded-xl bg-[#0A2540]/80 border border-cyan-500/20 text-slate-300 flex items-center gap-2.5 hover:bg-[#0E3559] cursor-pointer transition">
                <span className="w-5 h-5 rounded-full border border-white/30 flex items-center justify-center text-[11px] font-mono">ক</span>
                <span>দোলনকাল অপরিবর্তিত থাকবে</span>
              </div>
              <div className="p-2.5 rounded-xl bg-[#063B2C] border border-[#059669] text-emerald-200 flex items-center gap-2.5 font-bold">
                <span className="w-5 h-5 rounded-full bg-emerald-400 text-slate-950 flex items-center justify-center text-[11px] font-mono font-bold">খ</span>
                <span>দোলনকাল √২ গুণ বৃদ্ধি পাবে (সঠিক)</span>
              </div>
              <div className="p-2.5 rounded-xl bg-[#0A2540]/80 border border-cyan-500/20 text-slate-300 flex items-center gap-2.5 hover:bg-[#0E3559] cursor-pointer transition">
                <span className="w-5 h-5 rounded-full border border-white/30 flex items-center justify-center text-[11px] font-mono">গ</span>
                <span>দোলনকাল অর্ধেক হবে</span>
              </div>
            </div>

            <div className="p-3 rounded-xl bg-[#0A2540]/90 border border-cyan-500/25 text-[11px] text-slate-300 font-bengali leading-relaxed">
              <strong className="text-amber-300 font-mono">ব্যাখ্যা (T = 2π√(L/g)):</strong> দোলনকাল কার্যকর দৈর্ঘ্যের বর্গমূলের সমানুপাতিক। সুতরাং L দ্বিগুণ হলে T পরিবর্তিত হয়ে √২ গুণ হবে।
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
