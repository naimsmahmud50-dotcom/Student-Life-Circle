import React from 'react';
import Link from 'next/link';
import { GraduationCap, ShieldCheck, Mail, Phone, MapPin } from 'lucide-react';

export const GoEduFooter: React.FC = () => {
  return (
    <footer className="relative overflow-hidden w-full bg-[#FFF6DD]/95 dark:bg-[#070C18] border-t border-amber-200/80 dark:border-[#262D3D] transition-colors duration-300 pt-16 pb-12 font-sans">
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
          minHeight: '400px',
          background:
            'radial-gradient(ellipse 75% 85% at 50% 100%, rgba(255, 178, 0, 0.40) 0%, rgba(243, 172, 8, 0.16) 50%, rgba(253, 215, 70, 0) 100%)'
        }}
        aria-hidden="true"
      />

      {/* Giant Typographic Watermark (OGROJATRA EDU) */}
      <div
        className="absolute z-0 pointer-events-none select-none w-full bottom-8 left-0 flex justify-center overflow-hidden"
        aria-hidden="true"
      >
        <p
          className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[16vw] md:text-[clamp(3.5rem,18vw,14rem)] uppercase tracking-wider select-none opacity-85"
          style={{
            lineHeight: 0.9,
            backgroundImage:
              'linear-gradient(to bottom, rgba(243, 172, 8, 0.22) 15%, rgba(253, 215, 70, 0.02) 100%)'
          }}
        >
          OGROJATRA EDU
        </p>
      </div>

      <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 pb-12 border-b border-amber-200/70 dark:border-slate-800">
          {/* Brand & Accreditation Column */}
          <div className="lg:col-span-2 p-5 rounded-2xl bg-white/85 dark:bg-[#121B2D]/85 border border-amber-200/70 dark:border-[#262D3D] shadow-xs backdrop-blur-xs space-y-4">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-[#0A2540] flex items-center justify-center text-white shadow-[0_3px_0_0_#051329] border border-amber-200/50">
                <GraduationCap className="w-5 h-5 text-[#ED8E22]" aria-hidden="true" />
              </div>
              <span className="text-xl font-black text-[#213130] dark:text-white tracking-tight">
                অগ্রযাত্রা <span className="text-[#ED8E22] text-xs font-bold uppercase">Edu</span>
              </span>
            </Link>

            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 leading-relaxed max-w-sm font-bengali">
              বাংলাদেশের শিক্ষার্থীদের জন্য এনসিটিবি স্টেম কারিকুলাম, এডমিশন প্রেডিকশন এবং প্রফেশনাল স্কিলসের
              সমন্বিত লার্নিং প্ল্যাটফর্ম। জিইএসি স্ট্যান্ডার্ড অনুমোদিত পাঠ্যক্রম।
            </p>

            <div className="flex items-center gap-2 text-xs text-emerald-800 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/50 p-2.5 rounded-xl border border-emerald-300/60 dark:border-emerald-800/60 max-w-sm shadow-2xs">
              <ShieldCheck className="w-4 h-4 shrink-0 text-emerald-600 dark:text-emerald-400" aria-hidden="true" />
              <span className="font-semibold font-bengali">জিইএসি এক্রিডিটেড ও কোয়ালিটি অ্যাসিউরড সিলেবাস</span>
            </div>

            <div className="text-xs text-slate-600 dark:text-slate-400 space-y-2 pt-1">
              <div className="flex items-center gap-2">
                <Mail className="w-3.5 h-3.5 text-[#ED8E22]" aria-hidden="true" />
                <span className="font-mono">support@ogrojatra.edu.bd</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-3.5 h-3.5 text-[#ED8E22]" aria-hidden="true" />
                <span className="font-bengali">+৮৮০ ১৮১১-৪৫৮৮৩০ (সকাল ৯টা - রাত ৯টা)</span>
              </div>
            </div>
          </div>

          {/* Column 1: Learning Programs */}
          <div className="space-y-3">
            <h3 className="font-bold text-xs uppercase tracking-wider text-[#1A1A1A] dark:text-white font-sans">
              একাডেমিক প্রোগ্রাম
            </h3>
            <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-400">
              <li>
                <Link href="/courses" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>সকল অনলাইন কোর্স</span>
                </Link>
              </li>
              <li>
                <Link href="/courses?category=stem-math" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>উচ্চতর গণিত ও বিজ্ঞান</span>
                </Link>
              </li>
              <li>
                <Link href="/courses?category=ai-tech" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>এআই ও টেকনোলজি</span>
                </Link>
              </li>
              <li>
                <Link href="/admission/predictor" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>এডমিশন প্রেডিক্টর</span>
                </Link>
              </li>
              <li>
                <Link href="/board-archives" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>বিগত ১০ বছরের বোর্ড প্রশ্ন</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 2: Interactive Features */}
          <div className="space-y-3">
            <h3 className="font-bold text-xs uppercase tracking-wider text-[#1A1A1A] dark:text-white font-sans">
              ইন্টারেক্টিভ টুলস
            </h3>
            <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-400">
              <li>
                <Link href="/socratic/solver" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>সক্রেটিক এআই সলভার</span>
                </Link>
              </li>
              <li>
                <Link href="/live-challenge" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>লাইভ চ্যালেঞ্জ এরিনা</span>
                </Link>
              </li>
              <li>
                <Link href="/olympiad/arena" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>অলিম্পিয়াড এরিনা</span>
                </Link>
              </li>
              <li>
                <Link href="/tuition" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>হোম টিউটর ও টিউশন হাব</span>
                </Link>
              </li>
              <li>
                <Link href="/routines" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>মডেল টেস্ট ও রুটিন হাব</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 3: Platform & Career */}
          <div className="space-y-3">
            <h3 className="font-bold text-xs uppercase tracking-wider text-[#1A1A1A] dark:text-white font-sans">
              ক্যারিয়ার ও সাপোর্ট
            </h3>
            <ul className="space-y-2 text-xs text-slate-600 dark:text-slate-400">
              <li>
                <Link href="/career/radar" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>ক্যারিয়ার রাডার ও জবস</span>
                </Link>
              </li>
              <li>
                <Link href="/scholarship/disbursement" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>স্কলারশিপ বিতরণ</span>
                </Link>
              </li>
              <li>
                <Link href="/study-pod" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>স্টাডি পড ও গ্রুপ স্টাডি</span>
                </Link>
              </li>
              <li>
                <Link href="/viva/evaluator" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>ভাইভা ইভ্যালুয়েটর</span>
                </Link>
              </li>
              <li>
                <Link href="/guardian/ptc" className="hover:text-[#ED8E22] dark:hover:text-amber-400 transition-colors flex items-center gap-2 py-1 group">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-300 dark:bg-amber-600/70 group-hover:bg-[#ED8E22] transition-colors shrink-0"></span>
                  <span>অভিভাবক ড্যাশবোর্ড</span>
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-600 dark:text-slate-400 gap-4">
          <p className="font-bengali">© ২০২৬ অগ্রযাত্রা (Student Life Circle) ও গোএডু ডিজাইন সিস্টেম। সর্বস্বত্ব সংরক্ষিত।</p>
          <div className="flex items-center gap-4 text-xs font-bengali">
            <Link href="/" className="hover:text-[#ED8E22] transition-colors">
              গোপনীয়তা নীতি
            </Link>
            <span className="text-amber-300 dark:text-slate-700">•</span>
            <Link href="/" className="hover:text-[#ED8E22] transition-colors">
              ব্যবহারের শর্তাবলী
            </Link>
            <span className="text-amber-300 dark:text-slate-700">•</span>
            <Link href="/" className="hover:text-[#ED8E22] transition-colors">
              জিইএসি স্বীকৃতি
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};
