/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Global Application Layout - Dignified Flagship Footer
 * TOPIC:     Harmonious Warm Slate & Refined Geometric Foundation
 * FILE:      frontend/src/components/layout/Footer.tsx
 * PURPOSE:   Provides a dignified, harmonious, and softly illuminated footer canvas
 *            (light: warm sand-parchment #FAF7F0, dark: refined midnight slate #0D1524)
 *            that seamlessly integrates with the rest of the application. Features delicate,
 *            lightweight astronomical orbital hairlines, frosted glass containers, tactical
 *            hotline chips, verified national payment rails (bKash, Nagad, SSLCommerz), and
 *            strict zero-emoji policy.
 * STANDARDS: UI/UX Pro Max, Academic Editorial Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
 */

import React from 'react';
import Link from 'next/link';
import {
  GraduationCap,
  ShieldCheck,
  Lock,
  Award,
  HeartHandshake,
  FileText,
  PhoneCall,
  CheckCircle2,
  BookOpen,
  Compass,
  Mail,
  Globe
} from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export interface FooterProps {
  theme?: 'light' | 'dark';
}

export const Footer: React.FC<FooterProps> = () => {
  const { t, isBengali, toggleLocale } = useTranslation();

  return (
    <footer className="relative overflow-hidden w-full bg-[#FAF7F0] dark:bg-[#0D1524] text-slate-700 dark:text-slate-300 font-sans transition-colors duration-300">
      {/* -----------------------------------------------------------------------
          HORIZON BOUNDARY: Delicate Warm Amber Transition Hairline
          ----------------------------------------------------------------------- */}
      <div className="w-full h-[1px] bg-gradient-to-r from-transparent via-amber-400/50 dark:via-amber-500/30 to-transparent relative z-20" />

      {/* -----------------------------------------------------------------------
          BACKGROUND ATMOSPHERICS: Soft Harmonious Canvas & Delicate Radiant Glows
          ----------------------------------------------------------------------- */}
      {/* Soft Multi-Layered Atmosphere Gradient */}
      <div
        className="absolute inset-0 bg-gradient-to-b from-[#FAF7F0] via-[#F6F1E5] to-[#EFE7D4] dark:from-[#111A2E] dark:via-[#0D1524] dark:to-[#080D17] pointer-events-none select-none z-0"
        aria-hidden="true"
      />

      {/* Ambient Radiant Warm Glow from Top-Left */}
      <div
        className="absolute top-0 left-0 w-full pointer-events-none select-none z-0"
        style={{
          height: '420px',
          background:
            'radial-gradient(ellipse 65% 55% at 15% 20%, rgba(237, 142, 34, 0.08) 0%, rgba(56, 189, 248, 0.03) 45%, transparent 70%)'
        }}
        aria-hidden="true"
      />

      {/* Secondary Soft Amber Aura from Bottom-Right */}
      <div
        className="absolute bottom-0 right-0 w-full pointer-events-none select-none z-0"
        style={{
          height: '350px',
          background:
            'radial-gradient(ellipse 55% 45% at 85% 75%, rgba(237, 142, 34, 0.06) 0%, transparent 65%)'
        }}
        aria-hidden="true"
      />

      {/* Right Geometric Concentric Orbital Rings (Delicate, Lightweight Hairlines) */}
      <div
        className="absolute -right-24 md:-right-12 -top-20 md:-top-32 w-[480px] sm:w-[620px] md:w-[780px] h-[480px] sm:h-[620px] md:h-[780px] pointer-events-none select-none z-0"
        aria-hidden="true"
      >
        <svg
          viewBox="0 0 800 800"
          fill="none"
          className="w-full h-full"
          xmlns="http://www.w3.org/2000/svg"
          role="presentation"
        >
          <circle
            cx="450"
            cy="400"
            r="370"
            stroke="#ED8E22"
            strokeWidth="1.5"
            opacity="0.10"
            strokeDasharray="4 6"
          />
          <circle
            cx="450"
            cy="400"
            r="270"
            stroke="#38BDF8"
            strokeWidth="1.5"
            opacity="0.12"
          />
          <circle
            cx="450"
            cy="400"
            r="180"
            stroke="#ED8E22"
            strokeWidth="1.5"
            opacity="0.14"
          />
          <circle
            cx="450"
            cy="400"
            r="95"
            stroke="#10B981"
            strokeWidth="1.5"
            opacity="0.12"
          />
        </svg>
      </div>

      {/* Left Bottom Geometric Accent Arc (Refined Blueprint Hairlines) */}
      <div
        className="absolute -left-20 -bottom-24 w-[360px] md:w-[460px] h-[360px] md:h-[460px] pointer-events-none select-none z-0"
        aria-hidden="true"
      >
        <svg
          viewBox="0 0 400 400"
          fill="none"
          className="w-full h-full"
          xmlns="http://www.w3.org/2000/svg"
          role="presentation"
        >
          <circle
            cx="100"
            cy="300"
            r="220"
            stroke="#ED8E22"
            strokeWidth="1.5"
            opacity="0.10"
          />
          <circle
            cx="100"
            cy="300"
            r="140"
            stroke="#38BDF8"
            strokeWidth="1.5"
            opacity="0.10"
          />
        </svg>
      </div>

      {/* -----------------------------------------------------------------------
          TIER 1: Accreditation & Institutional Compliance Bar
          ----------------------------------------------------------------------- */}
      <div className="relative z-10 bg-white/70 dark:bg-[#111A2E]/70 backdrop-blur-md border-b border-amber-200/50 dark:border-slate-800/80 px-4 sm:px-6 lg:px-8 py-3.5">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 text-xs">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 dark:bg-amber-400/10 border border-amber-400/30 text-amber-900 dark:text-amber-200 font-semibold font-bengali tracking-normal shadow-xs">
            <ShieldCheck className="w-4 h-4 text-[#ED8E22] shrink-0" />
            <span>
              {isBengali
                ? 'জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) কারিকুলাম মানদণ্ড ২০২৬ সমর্থিত'
                : 'National Curriculum & Textbook Board (NCTB) 2026 Aligned'}
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2.5 text-xs">
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/90 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/60 text-slate-800 dark:text-slate-200 font-bengali font-semibold shadow-xs hover:border-emerald-400/60 hover:bg-emerald-50/40 dark:hover:bg-slate-800 transition cursor-default">
              <Lock className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
              <span>ISO 27001 সার্টিফাইড ডেটা ভল্ট</span>
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/90 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/60 text-amber-900 dark:text-amber-300 font-bengali font-semibold shadow-xs hover:border-amber-400/60 hover:bg-amber-50/40 dark:hover:bg-slate-800 transition cursor-default">
              <Award className="w-3.5 h-3.5 text-[#ED8E22] shrink-0" />
              <span>OWASP ASVS L2 সিকিউরিটি আর্কিটেকচার</span>
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/90 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/60 text-emerald-900 dark:text-emerald-300 font-bengali font-semibold shadow-xs hover:border-emerald-400/60 hover:bg-emerald-50/40 dark:hover:bg-slate-800 transition cursor-default">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
              <span>WCAG 2.2 AAA কমপ্লায়েন্ট</span>
            </span>
          </div>
        </div>
      </div>

      {/* -----------------------------------------------------------------------
          TIER 2: Main 5-Column Editorial Navigation Grid
          ----------------------------------------------------------------------- */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-8 lg:gap-6">
          
          {/* Column 1: Brand & Mission in Frosted Slate Card */}
          <div className="sm:col-span-2 lg:col-span-1 p-6 rounded-2xl bg-white/85 dark:bg-[#152136]/75 border border-amber-200/60 dark:border-slate-700/60 shadow-lg backdrop-blur-md space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#1B2A4A] dark:bg-[#0B132B] text-white flex items-center justify-center shadow-[0_3px_0_0_#0F172A] border border-amber-400/30 shrink-0">
                <GraduationCap className="w-5 h-5 text-[#ED8E22]" strokeWidth={1.75} />
              </div>
              <div>
                <span className="font-bold text-lg text-slate-900 dark:text-white tracking-tight font-bengali block">
                  অগ্রযাত্রা
                </span>
                <span className="block text-[11px] text-slate-500 dark:text-slate-400 font-medium font-sans">
                  Student Growth Platform
                </span>
              </div>
            </div>

            <p className="text-xs text-slate-600 dark:text-slate-300 leading-relaxed font-bengali">
              {isBengali
                ? 'একটি ইউনিফাইড প্রোফাইল, একটি দীর্ঘমেয়াদী শিক্ষাজীবন। মাধ্যমিক ও উচ্চ মাধ্যমিক স্তর থেকে বিশ্ববিদ্যালয় ভর্তি ও পেশাগত কর্মজীবন পর্যন্ত বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য বিশ্বস্ত প্ল্যাটফর্ম।'
                : "One unified profile for lifelong learning. Supporting students from secondary education through university entrance and professional career pathways."}
            </p>

            <div className="pt-1">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 dark:bg-emerald-400/10 border border-emerald-400/30 text-xs text-emerald-800 dark:text-emerald-300 font-bold font-bengali shadow-xs">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                <span>অ্যাকাডেমিক স্বচ্ছতা নিশ্চিত</span>
              </span>
            </div>
          </div>

          {/* Column 2: Levels (শ্রেণি ও পর্যায়) */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100 font-sans flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-[#ED8E22]" strokeWidth={1.75} />
              <span className="font-bengali font-bold">{isBengali ? 'শ্রেণি ও স্তর' : 'Levels'}</span>
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link
                  href="/learn?stage=SSC"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'এসএসসি (৯ম ও ১০ম)' : 'SSC Curriculum'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/learn?stage=HSC"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'এইচএসসি (বিজ্ঞান/মানবিক/ব্যবসায়)' : 'HSC Curriculum'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/admission"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি' : 'University Admission'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/career"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'ক্যারিয়ার ও স্কিল লেজার' : 'Career & Skills'}</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Resources (রিসোর্স ও পাঠ্যক্রম) */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100 font-sans flex items-center gap-2">
              <Compass className="w-4 h-4 text-[#ED8E22]" strokeWidth={1.75} />
              <span className="font-bengali font-bold">{isBengali ? 'রিসোর্স' : 'Resources'}</span>
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link
                  href="/board-archives"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'বোর্ড প্রশ্ন ব্যাংক' : 'Board Question Bank'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/practice"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'অনুশীলন ও মডেল টেস্ট' : 'Adaptive Practice'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/live-challenge"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'লাইভ অলিম্পিয়াড চ্যালেঞ্জ' : 'Live Challenge'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/modules?category=stem-labs"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'স্টেম ল্যাব (stem-labs)' : 'STEM Labs'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/tuition"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'টিউশন ও ট্রাস্ট' : 'Tuition & Trust'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/verify"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'সনদ যাচাই (/verify)' : 'Certificate Verification'}</span>
                </Link>
              </li>
              <li>
                <Link
                  id="footer-global-socratic-trigger"
                  data-trigger="global-socratic-trigger"
                  href="/socratic/solver"
                  className="text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all flex items-center gap-2 py-1 group font-bengali font-medium"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'সক্রেটিক এআই টিউটর' : 'Socratic AI Tutor'}</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 4: Contact & Helpdesk */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100 font-sans flex items-center gap-2">
              <PhoneCall className="w-4 h-4 text-[#ED8E22]" strokeWidth={1.75} />
              <span className="font-bengali font-bold">{isBengali ? 'যোগাযোগ ও সাপোর্ট' : 'Contact & Support'}</span>
            </h3>
            <div className="space-y-2 text-xs text-slate-700 dark:text-slate-300">
              <a
                href="tel:16250"
                title={isBengali ? 'অফিসিয়াল হটলাইনে কল করুন: ১৬xxx' : 'Call Support Hotline: 16xxx'}
                className="flex items-center justify-between p-2.5 rounded-xl bg-white/90 dark:bg-[#152136]/90 border border-slate-200/80 dark:border-slate-700/60 hover:border-[#ED8E22] hover:bg-amber-500/5 shadow-xs transition-all active:scale-[0.98] group"
              >
                <div className="flex items-center gap-2">
                  <PhoneCall className="w-3.5 h-3.5 text-[#ED8E22] group-hover:scale-110 transition-transform shrink-0" />
                  <span className="font-bengali font-semibold text-xs text-slate-700 dark:text-slate-300">
                    {isBengali ? 'হটলাইন:' : 'Hotline:'}
                  </span>
                </div>
                <span className="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-300 dark:border-slate-600 font-sans font-bold text-[11px] tracking-wide group-hover:border-[#ED8E22] shadow-xs">
                  ১৬xxx (16xxx)
                </span>
              </a>

              <a
                href="tel:1098"
                title={isBengali ? 'শিশু হেল্পলাইনে ফ্রি কল করুন: ১০৯৮' : 'Call Free Child Helpline: 1098'}
                className="flex items-center justify-between p-2.5 rounded-xl bg-white/90 dark:bg-[#152136]/90 border border-slate-200/80 dark:border-slate-700/60 hover:border-emerald-500 hover:bg-emerald-50/20 shadow-xs transition-all active:scale-[0.98] group"
              >
                <div className="flex items-center gap-2">
                  <HeartHandshake className="w-3.5 h-3.5 text-emerald-500 group-hover:scale-110 transition-transform shrink-0" />
                  <span className="font-bengali font-semibold text-xs text-slate-700 dark:text-slate-300">
                    {isBengali ? 'শিশু হেল্পলাইন:' : 'Child Helpline:'}
                  </span>
                </div>
                <span className="px-2.5 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-700/60 font-sans font-bold text-[11px] tracking-wide group-hover:border-emerald-500 shadow-xs">
                  ১০৯৮ (1098)
                </span>
              </a>

              <a
                href="tel:999"
                title={isBengali ? 'জরুরি সেবা ৯৯৯ এ কল করুন' : 'Call Emergency Services: 999'}
                className="flex items-center justify-between p-2.5 rounded-xl bg-white/90 dark:bg-[#152136]/90 border border-slate-200/80 dark:border-slate-700/60 hover:border-amber-500 hover:bg-amber-50/20 shadow-xs transition-all active:scale-[0.98] group"
              >
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-3.5 h-3.5 text-amber-500 group-hover:scale-110 transition-transform shrink-0" />
                  <span className="font-bengali font-semibold text-xs text-slate-700 dark:text-slate-300">
                    {isBengali ? 'জরুরি সেবা:' : 'Emergency:'}
                  </span>
                </div>
                <span className="px-2.5 py-0.5 rounded-md bg-amber-50 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-700/60 font-sans font-bold text-[11px] tracking-wide group-hover:border-amber-500 shadow-xs">
                  ৯৯৯ (999)
                </span>
              </a>

              <div className="pt-1">
                <a
                  href="mailto:support@ogrojatra.edu.bd"
                  title={isBengali ? 'ইমেইল পাঠাতে ক্লিক করুন' : 'Send an Email to Support'}
                  className="w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl bg-white/90 dark:bg-[#152136]/90 border border-slate-200/80 dark:border-slate-700/60 hover:border-[#ED8E22] hover:bg-amber-500/5 text-slate-700 dark:text-slate-300 hover:text-[#ED8E22] font-sans font-medium text-xs transition-all shadow-xs active:scale-[0.98] group"
                >
                  <Mail className="w-4 h-4 text-[#ED8E22] group-hover:scale-110 transition-transform shrink-0" />
                  <span className="font-sans font-semibold text-slate-800 dark:text-slate-200 group-hover:text-[#ED8E22] truncate text-xs">
                    support@ogrojatra.edu.bd
                  </span>
                </a>
              </div>
            </div>
          </div>

          {/* Column 5: Governance & Legal */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900 dark:text-slate-100 font-sans flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-[#ED8E22]" strokeWidth={1.75} />
              <span className="font-bengali font-bold">{isBengali ? 'নীতিমালা ও সুরক্ষা' : 'Legal & Safety'}</span>
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link
                  href="/terms"
                  className="flex items-start gap-2 text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all py-1 font-bengali font-medium group"
                >
                  <Lock className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5 group-hover:scale-110 transition-transform" />
                  <span>{isBengali ? 'অপ্রাপ্তবয়স্কদের তথ্য সুরক্ষা' : 'Minor Data Protection'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/tuition"
                  className="flex items-start gap-2 text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all py-1 font-bengali font-medium group"
                >
                  <HeartHandshake className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5 group-hover:scale-110 transition-transform" />
                  <span>{isBengali ? 'সুরক্ষিত টিউশন ও এসক্রো সম্মতি' : 'Escrow Tuition Trust'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/terms"
                  className="flex items-start gap-2 text-slate-600 dark:text-slate-300 hover:text-[#ED8E22] dark:hover:text-[#ED8E22] hover:translate-x-1 transition-all py-1 font-bengali font-medium group"
                >
                  <FileText className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5 group-hover:text-[#ED8E22] group-hover:scale-110 transition-all" />
                  <span>{isBengali ? 'ব্যবহারের শর্তাবলী' : 'Terms of Service'}</span>
                </Link>
              </li>
            </ul>
          </div>

        </div>

        {/* ---------------------------------------------------------------------
            TIER 3: Verified National Payment Rails & Escrow Trust Badges
            --------------------------------------------------------------------- */}
        <div className="mt-12 p-6 rounded-2xl bg-white/85 dark:bg-[#152136]/75 border border-amber-200/60 dark:border-slate-700/60 shadow-lg backdrop-blur-md">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="text-center md:text-left">
              <h4 className="text-xs font-bold text-slate-900 dark:text-white font-sans flex items-center justify-center md:justify-start gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-500" />
                <span>{isBengali ? 'যাচাইকৃত জাতীয় পেমেন্ট মাধ্যম ও এসক্রো ট্রাস্ট' : 'Verified National Payment Rails & Escrow'}</span>
              </h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1 font-bengali">
                {isBengali
                  ? 'এনক্রিপ্টেড পেমেন্ট ও বাংলাদেশ ব্যাংক রেগুলেশন নির্দেশিত নিরাপত্তা'
                  : 'Encrypted transactions aligned with Bangladesh Bank regulations'}
              </p>
            </div>

            {/* Authentic Payment Rails Badges */}
            <div className="flex flex-wrap items-center justify-center gap-3">
              {/* bKash Official SVG Badge */}
              <div
                className="group flex items-center gap-2.5 px-3.5 py-2 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-pink-500/60 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all cursor-default"
                title="bKash Direct Verified Merchant"
              >
                <svg
                  viewBox="0 0 100 40"
                  className="h-5 w-auto"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  role="img"
                  aria-label="bKash Verified Merchant"
                >
                  <rect width="100" height="40" rx="6" fill="#D12053" />
                  <path d="M22 8L34 20L28 26L18 16L22 8Z" fill="#FFFFFF" />
                  <path d="M34 20L44 14L38 32L30 24L34 20Z" fill="#F2F2F2" />
                  <text x="48" y="25" fill="#FFFFFF" fontFamily="sans-serif" fontWeight="bold" fontSize="13" letterSpacing="0.5">
                    bKash
                  </text>
                </svg>
                <span className="text-[10px] font-sans font-bold tracking-wider uppercase text-slate-600 dark:text-slate-300">Verified</span>
              </div>

              {/* Nagad Official SVG Badge */}
              <div
                className="group flex items-center gap-2.5 px-3.5 py-2 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-orange-500/60 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all cursor-default"
                title="Nagad Direct Verified Merchant"
              >
                <svg
                  viewBox="0 0 100 40"
                  className="h-5 w-auto"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  role="img"
                  aria-label="Nagad Verified Merchant"
                >
                  <rect width="100" height="40" rx="6" fill="#F7941D" />
                  <circle cx="24" cy="20" r="10" fill="#E41E26" />
                  <path d="M20 14L28 20L20 26V14Z" fill="#FFFFFF" />
                  <text x="42" y="25" fill="#FFFFFF" fontFamily="sans-serif" fontWeight="bold" fontSize="13" letterSpacing="0.5">
                    Nagad
                  </text>
                </svg>
                <span className="text-[10px] font-sans font-bold tracking-wider uppercase text-slate-600 dark:text-slate-300">Verified</span>
              </div>

              {/* SSLCommerz Escrow Gateway */}
              <div
                className="group flex items-center gap-2.5 px-3.5 py-2 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 hover:border-sky-500/60 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all cursor-default"
                title="SSLCommerz PCI-DSS Compliant Payment Gateway"
              >
                <svg
                  viewBox="0 0 110 40"
                  className="h-5 w-auto"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  role="img"
                  aria-label="SSLCommerz Secured"
                >
                  <rect width="110" height="40" rx="6" fill="#006699" />
                  <path d="M18 13C18 10.79 19.79 9 22 9C24.21 9 26 10.79 26 13V16H18V13ZM15 16V29H29V16H15Z" fill="#FFFFFF" />
                  <text x="35" y="25" fill="#FFFFFF" fontFamily="sans-serif" fontWeight="bold" fontSize="11">
                    SSLCOMMERZ
                  </text>
                </svg>
                <span className="text-[10px] font-sans font-bold tracking-wider uppercase text-slate-600 dark:text-slate-300">PCI-DSS</span>
              </div>
            </div>
          </div>
        </div>

        {/* ---------------------------------------------------------------------
            TIER 4: Bottom Bar - Copyright, Digital Safety & Standards
            --------------------------------------------------------------------- */}
        <div className="mt-10 pt-8 border-t border-slate-200/80 dark:border-slate-800/80 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 dark:text-slate-400 gap-4">
          <p className="text-center sm:text-left font-bengali font-normal">
            © ২০২৬ অগ্রযাত্রা (Student Life Circle). গণপ্রজাতন্ত্রী বাংলাদেশ সরকারের ডিজিটাল নিরাপত্তা আইন ও আন্তর্জাতিক ডেটা সুরক্ষা মানদণ্ড অনুযায়ী পরিচালিত।
          </p>

          <div className="flex flex-wrap items-center justify-center gap-3">
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-500/10 dark:bg-emerald-400/10 border border-emerald-400/30 text-emerald-800 dark:text-emerald-300 font-sans font-bold text-[11px] shadow-xs">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              WCAG 2.2 AAA
            </span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <Link
              href="/about"
              className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-white/90 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 hover:border-emerald-500/50 hover:text-emerald-600 dark:hover:text-emerald-400 transition-all font-bengali font-semibold shadow-2xs hover:shadow-xs active:scale-95"
              title="জিরো-ইমোজি পলিসি ও প্ল্যাটফর্ম পরিচিতি"
            >
              <span>জিরো-ইমোজি পলিসি</span>
            </Link>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <button
              type="button"
              onClick={toggleLocale}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/90 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 hover:border-[#ED8E22] hover:text-[#ED8E22] dark:hover:text-[#ED8E22] transition-all font-bengali font-semibold shadow-2xs hover:shadow-xs cursor-pointer active:scale-95"
              title={isBengali ? 'ইংরেজি সংস্করণে সুইচ করুন' : 'Switch to Bengali version'}
            >
              <Globe className="w-3.5 h-3.5 text-[#ED8E22]" />
              <span>বাংলা ও ইংরেজি সংস্করণ</span>
            </button>
          </div>
        </div>

      </div>
    </footer>
  );
};
