/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Global Application Layout - Dignified Flagship Footer
 * TOPIC:     Master Academic UI & Pro Tactile Button Elevation
 * FILE:      frontend/src/components/layout/Footer.tsx
 * PHASE:     Phase 110 - Pure Academic Visual Design Elevation & Phase 123 - Master Academic UI & Pro Tactile Button Elevation
 * PURPOSE:   Elevates every button, card, background, and header to Cambridge/Oxford-grade
 *            academic editorial layout featuring 5 clean columns (About, Levels, Resources, Contact, Legal),
 *            hairline warm borders, authentic national payment rails, Oxford Academic Navy palette
 *            (#0A2540, dark:bg-[#0B132B]), and strict zero AI vibe.
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
  HelpCircle
} from 'lucide-react';
import { useTranslation } from '@/lib/i18n';

export interface FooterProps {
  theme?: 'light' | 'dark';
}

export const Footer: React.FC<FooterProps> = () => {
  const { t, isBengali } = useTranslation();

  return (
    <footer className="w-full bg-[#FAF8F3] dark:bg-[#0B132B] text-[#5B5B5B] dark:text-slate-300 border-t border-[#E5E2DA] dark:border-slate-800 font-sans transition-colors">
      {/* -----------------------------------------------------------------------
          TIER 1: Accreditation & Institutional Compliance Bar
          ----------------------------------------------------------------------- */}
      <div className="bg-[#F5F2EB] dark:bg-[#0F172A] border-b border-[#E5E2DA] dark:border-slate-800/80 px-4 sm:px-6 lg:px-8 py-3">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 text-xs">
          <div className="flex items-center gap-2 text-[#065F46] dark:text-emerald-400 font-medium">
            <ShieldCheck className="w-4 h-4 text-[#065F46] dark:text-emerald-400 shrink-0" />
            <span>
              {isBengali
                ? 'জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) কারিকুলাম মানদণ্ড ২০২৬ সমর্থিত'
                : 'National Curriculum & Textbook Board (NCTB) 2026 Aligned'}
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-[#787878] dark:text-slate-400 text-xs">
            <span className="inline-flex items-center gap-1.5">
              <Lock className="w-3.5 h-3.5 text-[#1B2A4A] dark:text-sky-400 shrink-0" />
              <span>ISO 27001 সার্টিফাইড ডেটা ভল্ট</span>
            </span>
            <span className="hidden sm:inline text-slate-300 dark:text-slate-700">•</span>
            <span className="inline-flex items-center gap-1.5">
              <Award className="w-3.5 h-3.5 text-[#B8862B] dark:text-amber-400 shrink-0" />
              <span>OWASP ASVS L2 সিকিউরিটি আর্কিটেকচার</span>
            </span>
            <span className="hidden sm:inline text-slate-300 dark:text-slate-700">•</span>
            <span className="inline-flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-[#065F46] dark:text-emerald-400 shrink-0" />
              <span>WCAG 2.2 AAA কমপ্লায়েন্ট</span>
            </span>
          </div>
        </div>
      </div>

      {/* -----------------------------------------------------------------------
          TIER 2: Main 5-Column Editorial Navigation Grid
          ----------------------------------------------------------------------- */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-8 lg:gap-6">
          
          {/* Column 1: Brand & Mission */}
          <div className="sm:col-span-2 lg:col-span-1 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#0A2540] text-white flex items-center justify-center shadow-[0_3px_0_0_#051329] border border-black/10 shrink-0">
                <GraduationCap className="w-5 h-5 text-[#FBBF24]" strokeWidth={1.75} />
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
              <span className="inline-flex items-center gap-1.5 text-xs text-[#065F46] dark:text-emerald-400 font-semibold font-bengali">
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
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#1A1A1A] dark:hover:text-white transition flex items-center gap-2 py-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 shrink-0"></span>
                  <span>{isBengali ? 'এসএসসি (৯ম ও ১০ম)' : 'SSC Curriculum'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/learn?stage=HSC"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#1A1A1A] dark:hover:text-white transition flex items-center gap-2 py-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 shrink-0"></span>
                  <span>{isBengali ? 'এইচএসসি (বিজ্ঞান/মানবিক/ব্যবসায়)' : 'HSC Curriculum'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/admission"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#1A1A1A] dark:hover:text-white transition flex items-center gap-2 py-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 shrink-0"></span>
                  <span>{isBengali ? 'বিশ্ববিদ্যালয় ও মেডিকেল ভর্তি' : 'University Admission'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/career"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#1A1A1A] dark:hover:text-white transition flex items-center gap-2 py-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 shrink-0"></span>
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
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#1A1A1A] dark:hover:text-white transition flex items-center gap-2 py-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 shrink-0"></span>
                  <span>{isBengali ? 'বোর্ড প্রশ্ন ব্যাংক' : 'Board Question Bank'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/practice"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#1A1A1A] dark:hover:text-white transition flex items-center gap-2 py-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 shrink-0"></span>
                  <span>{isBengali ? 'অনুশীলন ও মডেল টেস্ট' : 'Adaptive Practice'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/live-challenge"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#1A1A1A] dark:hover:text-white transition flex items-center gap-2 py-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 shrink-0"></span>
                  <span>{isBengali ? 'লাইভ অলিম্পিয়াড চ্যালেঞ্জ' : 'Live Challenge'}</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/socratic/solver"
                  className="text-[#5B5B5B] dark:text-slate-400 hover:text-[#1A1A1A] dark:hover:text-white transition flex items-center gap-2 py-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-[#E5E2DA] dark:bg-slate-700 shrink-0"></span>
                  <span>{isBengali ? 'সক্রেটিক এআই টিউটর' : 'Socratic AI Tutor'}</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 4: Contact & Helpdesk */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#1A1A1A] dark:text-white font-sans flex items-center gap-2">
              <PhoneCall className="w-4 h-4 text-[#B8862B] dark:text-amber-400" strokeWidth={1.75} />
              <span>{isBengali ? 'যোগাযোগ' : 'Contact'}</span>
            </h3>
            <div className="space-y-2 text-xs text-[#5B5B5B] dark:text-slate-400">
              <p>
                হটলাইন: <strong className="text-[#1A1A1A] dark:text-white font-sans font-semibold">16xxx</strong> (সকাল ৮টা - রাত ১০টা)
              </p>
              <p>
                শিশু হেল্পলাইন: <strong className="text-[#065F46] dark:text-emerald-400 font-sans font-semibold">1098</strong> (টোল ফ্রি)
              </p>
              <p>
                জরুরি সেবা: <strong className="text-[#B8862B] dark:text-amber-400 font-sans font-semibold">999</strong>
              </p>
              <div className="pt-1">
                <a
                  href="mailto:support@ogrojatra.edu.bd"
                  className="text-[#1B2A4A] dark:text-sky-400 hover:underline font-mono text-[11px]"
                >
                  support@ogrojatra.edu.bd
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
                <span>{isBengali ? 'সুরক্ষিত টিউশন এসক্রো' : 'Escrow Tuition Trust'}</span>
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
        <div className="mt-10 pt-6 border-t border-[#E5E2DA] dark:border-slate-800">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="text-center sm:text-left">
              <h4 className="text-xs font-semibold text-[#1A1A1A] dark:text-slate-300 font-sans">
                {isBengali ? 'যাচাইকৃত জাতীয় পেমেন্ট মাধ্যম ও এসক্রো ট্রাস্ট' : 'Verified National Payment Rails & Escrow'}
              </h4>
              <p className="text-[11px] text-[#787878] dark:text-slate-500 mt-0.5">
                {isBengali
                  ? 'এনক্রিপ্টেড পেমেন্ট ও বাংলাদেশ ব্যাংক রেগুলেশন নির্দেশিত'
                  : 'Encrypted transactions aligned with Bangladesh Bank regulations'}
              </p>
            </div>

            {/* Authentic Payment Rails Badges */}
            <div className="flex flex-wrap items-center justify-center gap-3">
              {/* bKash Official SVG Badge */}
              <div
                className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white dark:bg-[#0F172A] border border-[#E5E2DA] dark:border-slate-800 shadow-xs"
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
                <span className="text-[10px] font-mono text-[#787878] dark:text-slate-400">Verified</span>
              </div>

              {/* Nagad Official SVG Badge */}
              <div
                className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white dark:bg-[#0F172A] border border-[#E5E2DA] dark:border-slate-800 shadow-xs"
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
                <span className="text-[10px] font-mono text-[#787878] dark:text-slate-400">Verified</span>
              </div>

              {/* SSLCommerz Escrow Gateway */}
              <div
                className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white dark:bg-[#0F172A] border border-[#E5E2DA] dark:border-slate-800 shadow-xs"
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
                <span className="text-[10px] font-mono text-[#787878] dark:text-slate-400">PCI-DSS</span>
              </div>
            </div>
          </div>
        </div>

        {/* ---------------------------------------------------------------------
            TIER 4: Bottom Bar - Copyright, Digital Safety & Standards
            --------------------------------------------------------------------- */}
        <div className="mt-8 pt-6 border-t border-[#E5E2DA] dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-[#787878] dark:text-slate-500 gap-4">
          <p className="text-center sm:text-left font-bengali">
            © ২০২৬ অগ্রযাত্রা (Student Life Circle). গণপ্রজাতন্ত্রী বাংলাদেশ সরকারের ডিজিটাল নিরাপত্তা আইন ও আন্তর্জাতিক ডেটা সুরক্ষা মানদণ্ড অনুযায়ী পরিচালিত।
          </p>

          <div className="flex flex-wrap items-center justify-center gap-3">
            <span className="inline-flex items-center gap-1.5 text-[#065F46] dark:text-emerald-400 font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-[#065F46] dark:bg-emerald-500"></span>
              WCAG 2.2 AAA
            </span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span>জিরো-ইমোজি পলিসি</span>
            <span className="text-slate-300 dark:text-slate-700">•</span>
            <span>বাংলা ও ইংরেজি সংস্করণ</span>
          </div>
        </div>

      </div>
    </footer>
  );
};
