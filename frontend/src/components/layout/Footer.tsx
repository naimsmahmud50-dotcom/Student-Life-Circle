/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Global Application Layout - Dignified Flagship Footer
 * TOPIC:     Master Academic UI & Bespoke Atmospheric Watermark Elevation
 * FILE:      frontend/src/components/layout/Footer.tsx
 * PURPOSE:   Elevates every button, card, background, and header to Cambridge/Oxford-grade
 *            academic editorial layout featuring 5 clean columns (About, Levels, Resources, Contact, Legal),
 *            warm sunshine linen canvas (#FFF6DD, dark:bg-[#070C18]), golden sunburst radial aura,
 *            giant typographic watermark (OGROJATRA), geometric dot matrix grid, authentic national
 *            payment rails (bKash, Nagad, SSLCommerz), and strict zero-emoji policy.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
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
  Trophy,
  Users,
  Briefcase,
  Sparkles,
  HelpCircle,
  Mail
} from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export interface FooterProps {
  theme?: 'light' | 'dark';
}

export const Footer: React.FC<FooterProps> = () => {
  const { t, isBengali } = useTranslation();

  return (
    <footer className="relative overflow-hidden w-full bg-[#FFF6DD]/95 dark:bg-[#070C18] text-[#5B5B5B] dark:text-slate-300 border-t border-amber-200/80 dark:border-[#262D3D] font-sans transition-colors duration-300">
      {/* -----------------------------------------------------------------------
          BACKGROUND ATMOSPHERICS: Dot Grid, Sunburst Aura, Giant Watermark
          ----------------------------------------------------------------------- */}
      {/* Subtle Academic Dot Matrix Grid */}
      <div
        className="absolute inset-0 pointer-events-none select-none z-0 opacity-40 dark:opacity-20"
        style={{
          backgroundImage: 'radial-gradient(rgba(243, 172, 8, 0.25) 1px, transparent 1px)',
          backgroundSize: '24px 24px'
        }}
        aria-hidden="true"
      />

      {/* Upward-Rising Golden Sunburst Radial Aura */}
      <div
        className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
        style={{
          height: '100%',
          minHeight: '420px',
          background:
            'radial-gradient(ellipse 75% 85% at 50% 100%, rgba(255, 178, 0, 0.42) 0%, rgba(243, 172, 8, 0.18) 50%, rgba(253, 215, 70, 0) 100%)'
        }}
        aria-hidden="true"
      />

      {/* Giant Typographic Watermark (OGROJATRA) */}
      <div
        className="absolute z-0 pointer-events-none select-none w-full bottom-8 md:bottom-12 left-0 flex justify-center overflow-hidden"
        aria-hidden="true"
      >
        <p
          className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(4rem,22vw,16rem)] uppercase tracking-wider select-none opacity-85"
          style={{
            lineHeight: 0.9,
            backgroundImage:
              'linear-gradient(to bottom, rgba(243, 172, 8, 0.22) 15%, rgba(253, 215, 70, 0.02) 100%)'
          }}
        >
          OGROJATRA
        </p>
      </div>

      {/* -----------------------------------------------------------------------
          TIER 1: Accreditation & Institutional Compliance Bar
          ----------------------------------------------------------------------- */}
      <div className="relative z-10 bg-[#FFF1C2]/90 dark:bg-[#0B132B]/90 backdrop-blur-md border-b border-amber-200/70 dark:border-amber-900/40 px-4 sm:px-6 lg:px-8 py-3.5">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 text-xs">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50/90 dark:bg-emerald-950/60 border border-emerald-300/70 dark:border-emerald-700/60 text-[#065F46] dark:text-emerald-300 font-semibold shadow-2xs">
            <ShieldCheck className="w-4 h-4 text-[#065F46] dark:text-emerald-400 shrink-0" />
            <span>
              {isBengali
                ? 'জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) কারিকুলাম মানদণ্ড ২০২৬ সমর্থিত'
                : 'National Curriculum & Textbook Board (NCTB) 2026 Aligned'}
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-3 text-xs">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/80 dark:bg-[#121B2D]/80 border border-amber-200/60 dark:border-slate-800 text-[#4A4740] dark:text-slate-300 shadow-2xs">
              <Lock className="w-3.5 h-3.5 text-[#1B2A4A] dark:text-sky-400 shrink-0" />
              <span>ISO 27001 সার্টিফাইড ডেটা ভল্ট</span>
            </span>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/80 dark:bg-[#121B2D]/80 border border-amber-200/60 dark:border-slate-800 text-[#4A4740] dark:text-slate-300 shadow-2xs">
              <Award className="w-3.5 h-3.5 text-[#ED8E22] dark:text-amber-400 shrink-0" />
              <span>OWASP ASVS L2 সিকিউরিটি আর্কিটেকচার</span>
            </span>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/80 dark:bg-[#121B2D]/80 border border-amber-200/60 dark:border-slate-800 text-[#4A4740] dark:text-slate-300 shadow-2xs">
              <CheckCircle2 className="w-3.5 h-3.5 text-[#065F46] dark:text-emerald-400 shrink-0" />
              <span>WCAG 2.2 AAA কমপ্লায়েন্ট</span>
            </span>
          </div>
        </div>
      </div>

      {/* -----------------------------------------------------------------------
          TIER 2: Main 5-Column Editorial Navigation Grid
          ----------------------------------------------------------------------- */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-8 lg:gap-6">
          
          {/* Column 1: Brand & Mission */}
          <div className="sm:col-span-2 lg:col-span-1 p-5 rounded-2xl bg-white/85 dark:bg-[#121B2D]/85 border border-amber-200/70 dark:border-[#262D3D] shadow-xs backdrop-blur-xs space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#0A2540] text-white flex items-center justify-center shadow-[0_3px_0_0_#051329] border border-amber-200/50 shrink-0">
                <GraduationCap className="w-5 h-5 text-[#ED8E22]" strokeWidth={1.75} />
              </div>
              <div>
                <span className="font-bold text-lg text-[#1A1A1A] dark:text-white tracking-tight font-bengali block">
                  অগ্রযাত্রা
                </span>
                <span className="block text-[11px] text-[#5B5B5B] dark:text-slate-400 font-medium font-sans">
                  Student Growth Platform
                </span>
              </div>
            </div>

            <p className="text-xs text-[#5B5B5B] dark:text-slate-400 leading-relaxed font-bengali">
              {isBengali
                ? 'একটি ইউনিফাইড প্রোফাইল, একটি দীর্ঘমেয়াদী শিক্ষাজীবন। মাধ্যমিক ও উচ্চ মাধ্যমিক স্তর থেকে বিশ্ববিদ্যালয় ভর্তি ও পেশাগত কর্মজীবন পর্যন্ত বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য বিশ্বস্ত প্ল্যাটফর্ম।'
                : "One unified profile for lifelong learning. Supporting students from secondary education through university entrance and professional career pathways."}
            </p>

            <div className="pt-1">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-300/60 dark:border-emerald-700/60 text-xs text-[#065F46] dark:text-emerald-300 font-semibold font-bengali shadow-2xs">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>অ্যাকাডেমিক স্বচ্ছতা নিশ্চিত</span>
              </span>
            </div>
          </div>

          {/* Column 2: Levels (শ্রেণি ও পর্যায়) */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#1A1A1A] dark:text-white font-sans flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-[#1B2A4A] dark:text-sky-400" strokeWidth={1.75} />
              <span>{isBengali ? 'শ্রেণি ও স্তর' : 'Levels'}</span>
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link
                  href="/learn?stage=SSC"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'এসএসসি (৯ম ও ১০ম)' : 'SSC Curriculum'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/learn?stage=HSC"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'এইচএসসি (বিজ্ঞান/মানবিক/ব্যবসায়)' : 'HSC Curriculum'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/admission"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি' : 'University Admission'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/career"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'ক্যারিয়ার ও স্কিল লেজার' : 'Career & Skills'}</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Resources (রিসোর্স ও পাঠ্যক্রম) */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#1A1A1A] dark:text-white font-sans flex items-center gap-2">
              <Compass className="w-4 h-4 text-[#065F46] dark:text-emerald-400" strokeWidth={1.75} />
              <span>{isBengali ? 'রিসোর্স' : 'Resources'}</span>
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link
                  href="/board-archives"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'বোর্ড প্রশ্ন ব্যাংক' : 'Board Question Bank'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/practice"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'অনুশীলন ও মডেল টেস্ট' : 'Adaptive Practice'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/live-challenge"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'লাইভ অলিম্পিয়াড চ্যালেঞ্জ' : 'Live Challenge'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/modules?category=stem-labs"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'স্টেম ল্যাব (stem-labs)' : 'STEM Labs'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/tuition"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'টিউশন ও ট্রাস্ট' : 'Tuition & Trust'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/verify"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'সনদ যাচাই (/verify)' : 'Certificate Verification'}</span>
                </Link>
              </li>
              <li>
                <Link
                  id="footer-global-socratic-trigger"
                  data-trigger="global-socratic-trigger"
                  href="/socratic/solver"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>{isBengali ? 'সক্রেটিক এআই টিউটর' : 'Socratic AI Tutor'}</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 4: Contact & Helpdesk */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#1A1A1A] dark:text-white font-sans flex items-center gap-2">
              <PhoneCall className="w-4 h-4 text-[#ED8E22] dark:text-amber-400" strokeWidth={1.75} />
              <span>{isBengali ? 'যোগাযোগ' : 'Contact'}</span>
            </h3>
            <div className="space-y-2.5 text-xs text-[#5B5B5B] dark:text-slate-400">
              <div className="flex items-center justify-between p-2 rounded-xl bg-white/70 dark:bg-[#121B2D]/70 border border-amber-200/50 dark:border-slate-800 shadow-2xs">
                <span>হটলাইন:</span>
                <span className="px-2 py-0.5 rounded-md bg-[#0A2540] text-white font-sans font-bold text-[11px]">১৬xxx (16xxx)</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-xl bg-white/70 dark:bg-[#121B2D]/70 border border-amber-200/50 dark:border-slate-800 shadow-2xs">
                <span>শিশু হেল্পলাইন:</span>
                <span className="px-2 py-0.5 rounded-md bg-emerald-700 text-white font-sans font-bold text-[11px]">১০৯৮ (1098)</span>
              </div>
              <div className="flex items-center justify-between p-2 rounded-xl bg-white/70 dark:bg-[#121B2D]/70 border border-amber-200/50 dark:border-slate-800 shadow-2xs">
                <span>জরুরি সেবা:</span>
                <span className="px-2 py-0.5 rounded-md bg-[#ED8E22] text-white font-sans font-bold text-[11px]">৯৯৯ (999)</span>
              </div>
              <div className="pt-1">
                <a
                  href="mailto:support@ogrojatra.edu.bd"
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/80 dark:bg-[#121B2D]/80 border border-amber-200/60 dark:border-slate-700 text-[#1B2A4A] dark:text-sky-400 hover:text-[#ED8E22] font-mono text-[11px] shadow-2xs transition-colors"
                >
                  <Mail className="w-3.5 h-3.5 text-[#ED8E22]" />
                  <span>support@ogrojatra.edu.bd</span>
                </a>
              </div>
            </div>
          </div>

          {/* Column 5: Governance & Legal */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#1A1A1A] dark:text-white font-sans flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-[#065F46] dark:text-emerald-400" strokeWidth={1.75} />
              <span>{isBengali ? 'নীতিমালা ও সুরক্ষা' : 'Legal & Safety'}</span>
            </h3>
            <ul className="space-y-2 text-xs">
              <li className="flex items-start gap-2 text-[#5B5B5B] dark:text-slate-400 py-1">
                <Lock className="w-3.5 h-3.5 text-[#1B2A4A] dark:text-sky-400 shrink-0 mt-0.5" />
                <span>{isBengali ? 'অপ্রাপ্তবয়স্কদের তথ্য সুরক্ষা' : 'Minor Data Protection'}</span>
              </li>
              <li className="flex items-start gap-2 text-[#5B5B5B] dark:text-slate-400 py-1">
                <HeartHandshake className="w-3.5 h-3.5 text-[#065F46] dark:text-emerald-400 shrink-0 mt-0.5" />
                <span>{isBengali ? 'সুরক্ষিত টিউশন ও এসক্রো সম্মতি' : 'Escrow Tuition Trust'}</span>
              </li>
              <li className="flex items-start gap-2 text-[#5B5B5B] dark:text-slate-400 py-1">
                <FileText className="w-3.5 h-3.5 text-[#787878] dark:text-slate-400 shrink-0 mt-0.5" />
                <span>{isBengali ? 'ব্যবহারের শর্তাবলী' : 'Terms of Service'}</span>
              </li>
            </ul>
          </div>

        </div>

        {/* ---------------------------------------------------------------------
            TIER 3: Verified National Payment Rails & Escrow Trust Badges
            --------------------------------------------------------------------- */}
        <div className="mt-10 p-5 sm:p-6 rounded-2xl bg-white/85 dark:bg-[#121B2D]/85 border border-amber-200/80 dark:border-[#262D3D] shadow-xs backdrop-blur-xs">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="text-center md:text-left">
              <h4 className="text-xs font-bold text-[#1A1A1A] dark:text-slate-200 font-sans flex items-center justify-center md:justify-start gap-1.5">
                <ShieldCheck className="w-4 h-4 text-[#065F46] dark:text-emerald-400" />
                <span>{isBengali ? 'যাচাইকৃত জাতীয় পেমেন্ট মাধ্যম ও এসক্রো ট্রাস্ট' : 'Verified National Payment Rails & Escrow'}</span>
              </h4>
              <p className="text-[11px] text-[#787878] dark:text-slate-400 mt-1">
                {isBengali
                  ? 'এনক্রিপ্টেড পেমেন্ট ও বাংলাদেশ ব্যাংক রেগুলেশন নির্দেশিত নিরাপত্তা'
                  : 'Encrypted transactions aligned with Bangladesh Bank regulations'}
              </p>
            </div>

            {/* Authentic Payment Rails Badges */}
            <div className="flex flex-wrap items-center justify-center gap-3">
              {/* bKash Official SVG Badge */}
              <div
                className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white dark:bg-[#0F172A] border border-amber-200/70 dark:border-slate-800 shadow-2xs hover:shadow-xs transition"
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
                <span className="text-[10px] font-mono text-slate-600 dark:text-slate-300 font-semibold">Verified</span>
              </div>

              {/* Nagad Official SVG Badge */}
              <div
                className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white dark:bg-[#0F172A] border border-amber-200/70 dark:border-slate-800 shadow-2xs hover:shadow-xs transition"
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
                <span className="text-[10px] font-mono text-slate-600 dark:text-slate-300 font-semibold">Verified</span>
              </div>

              {/* SSLCommerz Escrow Gateway */}
              <div
                className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white dark:bg-[#0F172A] border border-amber-200/70 dark:border-slate-800 shadow-2xs hover:shadow-xs transition"
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
                <span className="text-[10px] font-mono text-slate-600 dark:text-slate-300 font-semibold">PCI-DSS</span>
              </div>
            </div>
          </div>
        </div>

        {/* ---------------------------------------------------------------------
            TIER 4: Bottom Bar - Copyright, Digital Safety & Standards
            --------------------------------------------------------------------- */}
        <div className="mt-8 pt-6 border-t border-amber-200/70 dark:border-[#262D3D] flex flex-col sm:flex-row items-center justify-between text-xs text-[#6B655B] dark:text-slate-400 gap-4">
          <p className="text-center sm:text-left font-bengali">
            © ২০২৬ অগ্রযাত্রা (Student Life Circle). গণপ্রজাতন্ত্রী বাংলাদেশ সরকারের ডিজিটাল নিরাপত্তা আইন ও আন্তর্জাতিক ডেটা সুরক্ষা মানদণ্ড অনুযায়ী পরিচালিত।
          </p>

          <div className="flex flex-wrap items-center justify-center gap-3">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-300/60 text-[#065F46] dark:text-emerald-300 font-semibold shadow-2xs">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              WCAG 2.2 AAA
            </span>
            <span className="text-amber-300 dark:text-slate-700">•</span>
            <span className="px-2 py-0.5 rounded-md bg-white/70 dark:bg-slate-800/70 border border-amber-200/50 dark:border-slate-700 font-bengali">জিরো-ইমোজি পলিসি</span>
            <span className="text-amber-300 dark:text-slate-700">•</span>
            <span className="px-2 py-0.5 rounded-md bg-white/70 dark:bg-slate-800/70 border border-amber-200/50 dark:border-slate-700 font-bengali">বাংলা ও ইংরেজি সংস্করণ</span>
          </div>
        </div>

      </div>
    </footer>
  );
};
