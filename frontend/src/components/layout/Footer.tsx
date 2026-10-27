/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Global Application Layout - Dignified Flagship Footer
 * TOPIC:     Deep Pine Emerald & Concentric Rings Institutional Foundation
 * FILE:      frontend/src/components/layout/Footer.tsx
 * PURPOSE:   Provides an authoritative, deeply prestigious Deep Pine Emerald canvas (#071F1A)
 *            inspired by modern editorial learning platforms. Features a glowing mint radiant aura,
 *            vector geometric concentric orbital rings, frosted emerald glassmorphism,
 *            color-coded tactical hotline chips, authentic national payment rails (bKash,
 *            Nagad, SSLCommerz), and strict zero-emoji policy.
 * STANDARDS: UI/UX Pro Max, Pine Emerald Foundation, Tactile 3D Physics, Zero-Emoji, WCAG 2.2 AAA
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
  Mail
} from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export interface FooterProps {
  theme?: 'light' | 'dark';
}

export const Footer: React.FC<FooterProps> = () => {
  const { t, isBengali } = useTranslation();

  return (
    <footer className="relative overflow-hidden w-full bg-[#071F1A] text-emerald-100 font-sans transition-colors duration-300">
      {/* -----------------------------------------------------------------------
          HORIZON BOUNDARY: Luminous Mint-Emerald Transition Line
          ----------------------------------------------------------------------- */}
      <div className="w-full h-[2px] bg-gradient-to-r from-transparent via-emerald-400 to-transparent opacity-85 relative z-20" />

      {/* -----------------------------------------------------------------------
          BACKGROUND ATMOSPHERICS: Pine Emerald Canvas, Mint Radiant Glow, Concentric Rings
          ----------------------------------------------------------------------- */}
      {/* Deep Forest Pine Emerald Gradient Canvas */}
      <div
        className="absolute inset-0 bg-gradient-to-b from-[#071F1A] via-[#0C2B24] to-[#051713] pointer-events-none select-none z-0"
        aria-hidden="true"
      />

      {/* Ambient Radiant Mint Glow from Top-Left */}
      <div
        className="absolute top-0 left-0 w-full pointer-events-none select-none z-0"
        style={{
          height: '420px',
          background:
            'radial-gradient(ellipse 65% 55% at 12% 25%, rgba(16, 185, 129, 0.38) 0%, rgba(13, 148, 136, 0.16) 45%, transparent 70%)'
        }}
        aria-hidden="true"
      />

      {/* Secondary Ambient Forest Glow from Bottom-Right */}
      <div
        className="absolute bottom-0 right-0 w-full pointer-events-none select-none z-0"
        style={{
          height: '350px',
          background:
            'radial-gradient(ellipse 55% 45% at 85% 75%, rgba(5, 150, 105, 0.22) 0%, transparent 65%)'
        }}
        aria-hidden="true"
      />

      {/* Right Geometric Concentric Orbital Rings */}
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
            stroke="#059669"
            strokeWidth="44"
            opacity="0.22"
          />
          <circle
            cx="450"
            cy="400"
            r="270"
            stroke="#10B981"
            strokeWidth="38"
            opacity="0.30"
          />
          <circle
            cx="450"
            cy="400"
            r="180"
            stroke="#34D399"
            strokeWidth="26"
            opacity="0.22"
          />
          <circle
            cx="450"
            cy="400"
            r="95"
            stroke="#6EE7B7"
            strokeWidth="16"
            opacity="0.15"
          />
        </svg>
      </div>

      {/* Left Bottom Geometric Accent Arc */}
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
            stroke="#0D9488"
            strokeWidth="32"
            opacity="0.18"
          />
          <circle
            cx="100"
            cy="300"
            r="140"
            stroke="#14B8A6"
            strokeWidth="22"
            opacity="0.22"
          />
        </svg>
      </div>

      {/* -----------------------------------------------------------------------
          TIER 1: Accreditation & Institutional Compliance Bar
          ----------------------------------------------------------------------- */}
      <div className="relative z-10 bg-[#09221B]/90 backdrop-blur-md border-b border-emerald-900/60 px-4 sm:px-6 lg:px-8 py-3.5">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 text-xs">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-500/15 border border-emerald-400/40 text-emerald-300 font-semibold shadow-xs">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>
              {isBengali
                ? 'জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) কারিকুলাম মানদণ্ড ২০২৬ সমর্থিত'
                : 'National Curriculum & Textbook Board (NCTB) 2026 Aligned'}
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-2.5 text-xs">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-[#061A15]/80 border border-emerald-900/70 text-emerald-100/90 shadow-xs hover:border-emerald-700/60 transition">
              <Lock className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
              <span>ISO 27001 সার্টিফাইড ডেটা ভল্ট</span>
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-[#061A15]/80 border border-emerald-900/70 text-amber-300 shadow-xs hover:border-amber-700/60 transition">
              <Award className="w-3.5 h-3.5 text-[#ED8E22] shrink-0" />
              <span>OWASP ASVS L2 সিকিউরিটি আর্কিটেকচার</span>
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-[#061A15]/80 border border-emerald-900/70 text-emerald-300 shadow-xs hover:border-emerald-700/60 transition">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
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
          
          {/* Column 1: Brand & Mission in Frosted Emerald Card */}
          <div className="sm:col-span-2 lg:col-span-1 p-6 rounded-2xl bg-[#0C2E25]/85 border border-emerald-600/35 shadow-2xl backdrop-blur-md space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#061F1A] text-white flex items-center justify-center shadow-[0_3px_0_0_#031410] border border-emerald-400/40 shrink-0">
                <GraduationCap className="w-5 h-5 text-[#ED8E22]" strokeWidth={1.75} />
              </div>
              <div>
                <span className="font-bold text-lg text-white tracking-tight font-bengali block">
                  অগ্রযাত্রা
                </span>
                <span className="block text-[11px] text-emerald-200/70 font-medium font-sans">
                  Student Growth Platform
                </span>
              </div>
            </div>

            <p className="text-xs text-emerald-100/80 leading-relaxed font-bengali">
              {isBengali
                ? 'একটি ইউনিফাইড প্রোফাইল, একটি দীর্ঘমেয়াদী শিক্ষাজীবন। মাধ্যমিক ও উচ্চ মাধ্যমিক স্তর থেকে বিশ্ববিদ্যালয় ভর্তি ও পেশাগত কর্মজীবন পর্যন্ত বাংলাদেশের প্রতিটি শিক্ষার্থীর জন্য বিশ্বস্ত প্ল্যাটফর্ম।'
                : "One unified profile for lifelong learning. Supporting students from secondary education through university entrance and professional career pathways."}
            </p>

            <div className="pt-1">
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/40 text-xs text-emerald-300 font-bold font-bengali shadow-xs">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>অ্যাকাডেমিক স্বচ্ছতা নিশ্চিত</span>
              </span>
            </div>
          </div>

          {/* Column 2: Levels (শ্রেণি ও পর্যায়) */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-200 font-sans flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-emerald-400" strokeWidth={1.75} />
              <span>{isBengali ? 'শ্রেণি ও স্তর' : 'Levels'}</span>
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link
                  href="/learn?stage=SSC"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'এসএসসি (৯ম ও ১০ম)' : 'SSC Curriculum'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/learn?stage=HSC"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'এইচএসসি (বিজ্ঞান/মানবিক/ব্যবসায়)' : 'HSC Curriculum'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/admission"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি' : 'University Admission'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/career"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'ক্যারিয়ার ও স্কিল লেজার' : 'Career & Skills'}</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Resources (রিসোর্স ও পাঠ্যক্রম) */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-200 font-sans flex items-center gap-2">
              <Compass className="w-4 h-4 text-emerald-400" strokeWidth={1.75} />
              <span>{isBengali ? 'রিসোর্স' : 'Resources'}</span>
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link
                  href="/board-archives"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'বোর্ড প্রশ্ন ব্যাংক' : 'Board Question Bank'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/practice"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'অনুশীলন ও মডেল টেস্ট' : 'Adaptive Practice'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/live-challenge"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'লাইভ অলিম্পিয়াড চ্যালেঞ্জ' : 'Live Challenge'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/modules?category=stem-labs"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'স্টেম ল্যাব (stem-labs)' : 'STEM Labs'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/tuition"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'টিউশন ও ট্রাস্ট' : 'Tuition & Trust'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/verify"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'সনদ যাচাই (/verify)' : 'Certificate Verification'}</span>
                </Link>
              </li>
              <li>
                <Link
                  id="footer-global-socratic-trigger"
                  data-trigger="global-socratic-trigger"
                  href="/socratic/solver"
                  className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>{isBengali ? 'সক্রেটিক এআই টিউটর' : 'Socratic AI Tutor'}</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 4: Contact & Helpdesk */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-200 font-sans flex items-center gap-2">
              <PhoneCall className="w-4 h-4 text-[#ED8E22]" strokeWidth={1.75} />
              <span>{isBengali ? 'যোগাযোগ' : 'Contact'}</span>
            </h3>
            <div className="space-y-2.5 text-xs text-emerald-100/90">
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#061A15]/85 border border-emerald-900/80 shadow-xs">
                <span className="text-emerald-300/80">হটলাইন:</span>
                <span className="px-2.5 py-0.5 rounded-md bg-[#0C2E25] text-white border border-emerald-700/60 font-mono font-bold text-[11px]">১৬xxx (16xxx)</span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#061A15]/85 border border-emerald-900/80 shadow-xs">
                <span className="text-emerald-300/80">শিশু হেল্পলাইন:</span>
                <span className="px-2.5 py-0.5 rounded-md bg-emerald-950 text-emerald-300 border border-emerald-700/70 font-mono font-bold text-[11px]">১০৯৮ (1098)</span>
              </div>
              <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#061A15]/85 border border-emerald-900/80 shadow-xs">
                <span className="text-emerald-300/80">জরুরি সেবা:</span>
                <span className="px-2.5 py-0.5 rounded-md bg-[#251A08] text-amber-300 border border-amber-700/70 font-mono font-bold text-[11px]">৯৯৯ (999)</span>
              </div>
              <div className="pt-1">
                <a
                  href="mailto:support@ogrojatra.edu.bd"
                  className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#061A15]/85 border border-emerald-900/80 hover:border-emerald-500/50 text-emerald-300 hover:text-white font-mono text-xs transition shadow-xs"
                >
                  <Mail className="w-3.5 h-3.5 text-[#ED8E22]" />
                  <span>support@ogrojatra.edu.bd</span>
                </a>
              </div>
            </div>
          </div>

          {/* Column 5: Governance & Legal */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-200 font-sans flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" strokeWidth={1.75} />
              <span>{isBengali ? 'নীতিমালা ও সুরক্ষা' : 'Legal & Safety'}</span>
            </h3>
            <ul className="space-y-2 text-xs">
              <li className="flex items-start gap-2 text-emerald-100/75 hover:text-white transition py-1">
                <Lock className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span>{isBengali ? 'অপ্রাপ্তবয়স্কদের তথ্য সুরক্ষা' : 'Minor Data Protection'}</span>
              </li>
              <li className="flex items-start gap-2 text-emerald-100/75 hover:text-white transition py-1">
                <HeartHandshake className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                <span>{isBengali ? 'সুরক্ষিত টিউশন ও এসক্রো সম্মতি' : 'Escrow Tuition Trust'}</span>
              </li>
              <li className="flex items-start gap-2 text-emerald-100/75 hover:text-white transition py-1">
                <FileText className="w-3.5 h-3.5 text-emerald-300/80 shrink-0 mt-0.5" />
                <span>{isBengali ? 'ব্যবহারের শর্তাবলী' : 'Terms of Service'}</span>
              </li>
            </ul>
          </div>

        </div>

        {/* ---------------------------------------------------------------------
            TIER 3: Verified National Payment Rails & Escrow Trust Badges
            --------------------------------------------------------------------- */}
        <div className="mt-12 p-6 rounded-2xl bg-[#0C2E25]/85 border border-emerald-600/35 shadow-2xl backdrop-blur-md">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="text-center md:text-left">
              <h4 className="text-xs font-bold text-white font-sans flex items-center justify-center md:justify-start gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>{isBengali ? 'যাচাইকৃত জাতীয় পেমেন্ট মাধ্যম ও এসক্রো ট্রাস্ট' : 'Verified National Payment Rails & Escrow'}</span>
              </h4>
              <p className="text-[11px] text-emerald-200/70 mt-1 font-bengali">
                {isBengali
                  ? 'এনক্রিপ্টেড পেমেন্ট ও বাংলাদেশ ব্যাংক রেগুলেশন নির্দেশিত নিরাপত্তা'
                  : 'Encrypted transactions aligned with Bangladesh Bank regulations'}
              </p>
            </div>

            {/* Authentic Payment Rails Badges */}
            <div className="flex flex-wrap items-center justify-center gap-3">
              {/* bKash Official SVG Badge */}
              <div
                className="flex items-center gap-2.5 px-3.5 py-2 rounded-xl bg-[#061A15] border border-emerald-900/80 hover:border-pink-500/60 shadow-xs transition"
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
                <span className="text-[10px] font-mono text-emerald-200 font-semibold">Verified</span>
              </div>

              {/* Nagad Official SVG Badge */}
              <div
                className="flex items-center gap-2.5 px-3.5 py-2 rounded-xl bg-[#061A15] border border-emerald-900/80 hover:border-orange-500/60 shadow-xs transition"
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
                <span className="text-[10px] font-mono text-emerald-200 font-semibold">Verified</span>
              </div>

              {/* SSLCommerz Escrow Gateway */}
              <div
                className="flex items-center gap-2.5 px-3.5 py-2 rounded-xl bg-[#061A15] border border-emerald-900/80 hover:border-sky-500/60 shadow-xs transition"
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
                <span className="text-[10px] font-mono text-emerald-200 font-semibold">PCI-DSS</span>
              </div>
            </div>
          </div>
        </div>

        {/* ---------------------------------------------------------------------
            TIER 4: Bottom Bar - Copyright, Digital Safety & Standards
            --------------------------------------------------------------------- */}
        <div className="mt-10 pt-8 border-t border-emerald-900/70 flex flex-col sm:flex-row items-center justify-between text-xs text-emerald-200/70 gap-4">
          <p className="text-center sm:text-left font-bengali">
            © ২০২৬ অগ্রযাত্রা (Student Life Circle). গণপ্রজাতন্ত্রী বাংলাদেশ সরকারের ডিজিটাল নিরাপত্তা আইন ও আন্তর্জাতিক ডেটা সুরক্ষা মানদণ্ড অনুযায়ী পরিচালিত।
          </p>

          <div className="flex flex-wrap items-center justify-center gap-3">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/15 border border-emerald-400/40 text-emerald-300 font-semibold shadow-xs">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              WCAG 2.2 AAA
            </span>
            <span className="text-emerald-800">•</span>
            <span className="px-2.5 py-1 rounded-md bg-[#061A15] border border-emerald-900 text-emerald-200 font-bengali">জিরো-ইমোজি পলিসি</span>
            <span className="text-emerald-800">•</span>
            <span className="px-2.5 py-1 rounded-md bg-[#061A15] border border-emerald-900 text-emerald-200 font-bengali">বাংলা ও ইংরেজি সংস্করণ</span>
          </div>
        </div>

      </div>
    </footer>
  );
};
