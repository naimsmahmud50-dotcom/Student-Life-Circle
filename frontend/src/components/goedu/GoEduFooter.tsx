import React from 'react';
import Link from 'next/link';
import { GraduationCap, ShieldCheck, Mail, Phone, MapPin } from 'lucide-react';

export const GoEduFooter: React.FC = () => {
  return (
    <footer className="relative overflow-hidden w-full bg-[#071F1A] text-emerald-100 font-sans transition-colors duration-300 pt-16 pb-12">
      {/* -----------------------------------------------------------------------
          HORIZON BOUNDARY: Luminous Mint-Emerald Transition Line
          ----------------------------------------------------------------------- */}
      <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-emerald-400 to-transparent opacity-85 z-20" />

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

      <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 pb-12 border-b border-emerald-900/60">
          {/* Brand & Accreditation Column in Frosted Emerald Card */}
          <div className="lg:col-span-2 p-6 rounded-2xl bg-[#0C2E25]/85 border border-emerald-600/35 shadow-2xl backdrop-blur-md space-y-4">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-[#061F1A] flex items-center justify-center text-white shadow-[0_3px_0_0_#031410] border border-emerald-400/40">
                <GraduationCap className="w-5 h-5 text-[#ED8E22]" aria-hidden="true" />
              </div>
              <span className="text-xl font-black text-white tracking-tight">
                অগ্রযাত্রা <span className="text-[#ED8E22] text-xs font-bold uppercase">Edu</span>
              </span>
            </Link>

            <p className="text-xs sm:text-sm text-emerald-100/80 leading-relaxed max-w-sm font-bengali">
              বাংলাদেশের শিক্ষার্থীদের জন্য এনসিটিবি স্টেম কারিকুলাম, এডমিশন প্রেডিকশন এবং প্রফেশনাল স্কিলসের
              সমন্বিত লার্নিং প্ল্যাটফর্ম। জিইএসি স্ট্যান্ডার্ড অনুমোদিত পাঠ্যক্রম।
            </p>

            <div className="flex items-center gap-2 text-xs text-emerald-300 bg-emerald-500/15 p-2.5 rounded-xl border border-emerald-400/40 max-w-sm shadow-xs">
              <ShieldCheck className="w-4 h-4 shrink-0 text-emerald-400" aria-hidden="true" />
              <span className="font-semibold font-bengali">জিইএসি এক্রিডিটেড ও কোয়ালিটি অ্যাসিউরড সিলেবাস</span>
            </div>

            <div className="text-xs text-emerald-100/80 space-y-2 pt-1">
              <div className="flex items-center gap-2">
                <Mail className="w-3.5 h-3.5 text-[#ED8E22]" aria-hidden="true" />
                <span className="font-mono text-emerald-200">support@ogrojatra.edu.bd</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-3.5 h-3.5 text-[#ED8E22]" aria-hidden="true" />
                <span className="font-bengali text-emerald-200">+৮৮০ ১৮১১-৪৫৮৮৩০ (সকাল ৯টা - রাত ৯টা)</span>
              </div>
            </div>
          </div>

          {/* Column 1: Learning Programs */}
          <div className="space-y-3">
            <h3 className="font-bold text-xs uppercase tracking-wider text-emerald-200 font-sans">
              একাডেমিক প্রোগ্রাম
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/courses" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>সকল অনলাইন কোর্স</span>
                </Link>
              </li>
              <li>
                <Link href="/courses?category=stem-math" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>উচ্চতর গণিত ও বিজ্ঞান</span>
                </Link>
              </li>
              <li>
                <Link href="/courses?category=ai-tech" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>এআই ও টেকনোলজি</span>
                </Link>
              </li>
              <li>
                <Link href="/admission/predictor" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>এডমিশন প্রেডিক্টর</span>
                </Link>
              </li>
              <li>
                <Link href="/board-archives" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>বিগত ১০ বছরের বোর্ড প্রশ্ন</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 2: Interactive Features */}
          <div className="space-y-3">
            <h3 className="font-bold text-xs uppercase tracking-wider text-emerald-200 font-sans">
              ইন্টারেক্টিভ টুলস
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/socratic/solver" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>সক্রেটিক এআই সলভার</span>
                </Link>
              </li>
              <li>
                <Link href="/live-challenge" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>লাইভ চ্যালেঞ্জ এরিনা</span>
                </Link>
              </li>
              <li>
                <Link href="/olympiad/arena" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>অলিম্পিয়াড এরিনা</span>
                </Link>
              </li>
              <li>
                <Link href="/tuition" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>হোম টিউটর ও টিউশন হাব</span>
                </Link>
              </li>
              <li>
                <Link href="/routines" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>মডেল টেস্ট ও রুটিন হাব</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Platform & Career */}
          <div className="space-y-3">
            <h3 className="font-bold text-xs uppercase tracking-wider text-emerald-200 font-sans">
              ক্যারিয়ার ও সাপোর্ট
            </h3>
            <ul className="space-y-2 text-xs">
              <li>
                <Link href="/career/radar" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>ক্যারিয়ার রাডার ও জবস</span>
                </Link>
              </li>
              <li>
                <Link href="/scholarship/disbursement" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>স্কলারশিপ বিতরণ</span>
                </Link>
              </li>
              <li>
                <Link href="/study-pod" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>স্টাডি পড ও গ্রুপ স্টাডি</span>
                </Link>
              </li>
              <li>
                <Link href="/viva/evaluator" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>ভাইভা ইভ্যালুয়েটর</span>
                </Link>
              </li>
              <li>
                <Link href="/guardian/ptc" className="text-emerald-100/75 hover:text-white hover:translate-x-1 transition-all flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-700/60 group-hover:bg-[#ED8E22] group-hover:scale-125 transition-all shrink-0"></span>
                  <span>অভিভাবক ড্যাশবোর্ড</span>
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-emerald-200/70 gap-4">
          <p className="font-bengali">© ২০২৬ অগ্রযাত্রা (Student Life Circle) ও গোএডু ডিজাইন সিস্টেম। সর্বস্বত্ব সংরক্ষিত।</p>
          <div className="flex items-center gap-4 text-xs font-bengali">
            <Link href="/" className="hover:text-white transition-colors">
              গোপনীয়তা নীতি
            </Link>
            <span className="text-emerald-800">•</span>
            <Link href="/" className="hover:text-white transition-colors">
              ব্যবহারের শর্তাবলী
            </Link>
            <span className="text-emerald-800">•</span>
            <Link href="/" className="hover:text-white transition-colors">
              জিইএসি স্বীকৃতি
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};
