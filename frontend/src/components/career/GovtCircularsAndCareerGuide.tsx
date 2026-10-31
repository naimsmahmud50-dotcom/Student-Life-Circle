/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: GovtCircularsAndCareerGuide.tsx
 * PURPOSE:   Bdjobs-Style Official Government Circulars, Salary Insights & Career Preparation Hub
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { 
  Award, 
  ExternalLink, 
  Calendar, 
  Clock, 
  Building2, 
  ChevronDown, 
  ChevronUp, 
  FileText, 
  TrendingUp, 
  ShieldCheck, 
  BookOpen,
  Briefcase,
  CheckCircle2,
  Sparkles,
  HelpCircle
} from 'lucide-react';
import { 
  GOVT_CIRCULAR_ARCHIVES, 
  SALARY_BENCHMARKS, 
  CAREER_PORTAL_FAQS 
} from './data/careerElevationData';

export const GovtCircularsAndCareerGuide: React.FC = () => {
  const [openFaqIndex, setOpenFaqIndex] = useState<number | null>(0);

  const toggleFaq = (idx: number) => {
    setOpenFaqIndex(openFaqIndex === idx ? null : idx);
  };

  return (
    <div className="space-y-8">
      
      {/* 1. Official Government Circulars Grid with Gazette Atmosphere */}
      <div className="relative overflow-hidden rounded-3xl border border-amber-200/70 dark:border-amber-950/70 bg-[#FFFDF5]/90 dark:bg-[#0E131E]/90 p-6 sm:p-8 shadow-xs space-y-6">
        
        {/* Soft Golden Gazette Halo */}
        <div
          className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
          style={{
            height: '100%',
            minHeight: '260px',
            background:
              'radial-gradient(ellipse 65% 90% at 20% 100%, rgba(245, 158, 11, 0.14) 0%, rgba(245, 158, 11, 0.03) 50%, transparent 100%)'
          }}
          aria-hidden="true"
        />

        {/* Ambient Typographic Watermark */}
        <div
          className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
          aria-hidden="true"
        >
          <p
            className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,18vw,12rem)] uppercase tracking-wider select-none opacity-85"
            style={{
              lineHeight: 0.95,
              backgroundImage:
                'linear-gradient(to bottom, rgba(245, 158, 11, 0.20) 15%, rgba(245, 158, 11, 0.01) 100%)'
            }}
          >
            GAZETTE
          </p>
        </div>

        {/* Header */}
        <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-amber-200/60 dark:border-slate-800 pb-5">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-amber-100/90 dark:bg-amber-950/60 text-amber-900 dark:text-amber-300 border border-amber-300/80 dark:border-amber-800 shadow-xs font-bengali">
                <Award className="w-3.5 h-3.5 mr-1 text-amber-600 dark:text-amber-400" />
                জাতীয় সরকারি গেজেট ও বিপিএসসি সার্কুলার
              </span>
            </div>

            <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#1E293B] dark:text-[#F8FAFC]">
              সরকারি ও ক্যাডার সার্ভিস নিয়োগ বিজ্ঞপ্তি (Official Circulars)
            </h2>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
              বাংলাদেশ সরকারি কর্ম কমিশন (BPSC), বাংলাদেশ ব্যাংক ও মন্ত্রণালয় সমূহের অনুমোদিত সার্কুলার
            </p>
          </div>

          <span className="px-3.5 py-1.5 rounded-2xl text-xs font-mono font-bold bg-white dark:bg-[#121B2D] text-amber-900 dark:text-amber-300 border border-amber-200/80 dark:border-amber-900/60 shadow-xs self-start sm:self-auto">
            ৪টি অ্যাক্টিভ গেজেট
          </span>
        </div>

        {/* Circular Cards Grid */}
        <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 gap-4">
          {GOVT_CIRCULAR_ARCHIVES.map((circ) => (
            <div
              key={circ.id}
              className="p-5 sm:p-6 rounded-2xl border border-amber-200/70 dark:border-slate-800 bg-white/95 dark:bg-[#111A2C]/95 flex flex-col justify-between space-y-4 hover:border-amber-400 dark:hover:border-amber-600 hover:shadow-md transition-all duration-200 group"
            >
              <div className="space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="px-2.5 py-0.5 rounded-md text-[10px] font-mono font-bold bg-amber-100 dark:bg-amber-950/80 text-amber-900 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                    {circ.id}
                  </span>
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    মোট পদ: <strong className="text-amber-900 dark:text-amber-300 font-mono text-sm">{circ.totalPosts.toLocaleString('bn-BD')}</strong> টি
                  </span>
                </div>

                <h3 className="font-bold text-base text-slate-900 dark:text-white font-bengali group-hover:text-amber-700 dark:group-hover:text-amber-300 transition-colors">
                  {circ.title}
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali flex items-center gap-1.5">
                  <Building2 className="w-3.5 h-3.5 text-slate-400" />
                  <span>{circ.ministryOrDepartment}</span>
                </p>

                <div className="p-3 rounded-xl bg-amber-50/60 dark:bg-slate-900/80 border border-amber-200/50 dark:border-slate-800 text-xs font-bengali space-y-1.5">
                  <div className="text-slate-700 dark:text-slate-300 font-medium">বেতন স্কেল: {circ.gradePayScale}</div>
                  <div className="text-rose-700 dark:text-rose-400 font-bold flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-rose-600" />
                    <span>শেষ তারিখ: {circ.applicationDeadline}</span>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between text-xs font-bold text-amber-800 dark:text-amber-300 font-bengali">
                <span>অফিসিয়াল গেজেট ও আবেদন লিংক:</span>
                <span className="font-mono text-[11px] text-slate-500 hover:text-amber-700 dark:hover:text-amber-300 flex items-center gap-1">
                  <span>{circ.officialRef}</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 2. Bangladesh Industry Salary Insights & Benchmarks */}
      <div className="relative overflow-hidden rounded-3xl border border-emerald-200/70 dark:border-emerald-950/70 bg-[#F4FAF6]/90 dark:bg-[#071714]/90 p-6 sm:p-8 shadow-xs space-y-6">
        
        {/* Emerald Atmospheric Halo */}
        <div
          className="absolute top-0 right-0 w-full pointer-events-none select-none z-0"
          style={{
            height: '100%',
            minHeight: '260px',
            background:
              'radial-gradient(ellipse 65% 90% at 80% 0%, rgba(16, 185, 129, 0.12) 0%, rgba(16, 185, 129, 0.02) 50%, transparent 100%)'
          }}
          aria-hidden="true"
        />

        <div className="relative z-10 border-b border-emerald-200/60 dark:border-emerald-900/60 pb-5 space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100/90 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300/80 dark:border-emerald-800 shadow-xs font-bengali">
              <TrendingUp className="w-3.5 h-3.5 mr-1 text-emerald-600 dark:text-emerald-400" />
              মার্কেট ডেটা নির্দেশিকা
            </span>
          </div>

          <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#0B251F] dark:text-[#E8F8F4]">
            শিল্প ও পদবি ভেদে গড় বেতন নির্দেশিকা (Salary Insights)
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
            বাংলাদেশের শীর্ষস্থানীয় কর্মক্ষেত্রে এন্ট্রি, মিড ও সিনিয়র লেভেলের বর্তমান মার্কেট রেট ও বেঞ্চমার্ক
          </p>
        </div>

        <div className="relative z-10 overflow-x-auto rounded-2xl border border-emerald-200/70 dark:border-emerald-900/60 bg-white/95 dark:bg-[#0B1E1A]/95 shadow-xs">
          <table className="w-full text-left text-xs font-bengali border-collapse">
            <thead>
              <tr className="border-b border-emerald-200/60 dark:border-emerald-900/60 bg-emerald-50/80 dark:bg-[#071714] text-slate-700 dark:text-slate-200">
                <th className="p-4 font-bold">সেক্টর ও পদবি</th>
                <th className="p-4 font-bold">এন্ট্রি-লেভেল / ফ্রেশার</th>
                <th className="p-4 font-bold">মিড-লেভেল (২-৪ বছর)</th>
                <th className="p-4 font-bold">সিনিয়র / লিড লেভেল</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-emerald-100/60 dark:divide-emerald-900/40">
              {SALARY_BENCHMARKS.map((item, idx) => (
                <tr key={idx} className="hover:bg-emerald-50/40 dark:hover:bg-emerald-950/30 transition">
                  <td className="p-4 font-bold text-slate-900 dark:text-white">
                    <div className="text-sm">{item.roleTitle}</div>
                    <div className="text-[11px] text-emerald-700 dark:text-emerald-400 font-normal">{item.industry}</div>
                  </td>
                  <td className="p-4 text-slate-700 dark:text-slate-300 font-medium">
                    {item.entryLevelSalary}
                  </td>
                  <td className="p-4 text-emerald-700 dark:text-emerald-400 font-bold">
                    {item.midLevelSalary}
                  </td>
                  <td className="p-4 text-[#0A2540] dark:text-amber-300 font-black">
                    {item.seniorLevelSalary}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 3. Career & Interview Preparation Tips */}
      <div className="relative overflow-hidden rounded-3xl border border-indigo-200/70 dark:border-indigo-950/70 bg-[#F8FAFD]/90 dark:bg-[#09111E]/90 p-6 sm:p-8 shadow-xs space-y-6">
        
        <div className="relative z-10 border-b border-indigo-200/60 dark:border-indigo-900/60 pb-5 space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-indigo-100/90 dark:bg-indigo-950/60 text-indigo-900 dark:text-indigo-300 border border-indigo-300/80 dark:border-indigo-800 shadow-xs font-bengali">
              <BookOpen className="w-3.5 h-3.5 mr-1 text-indigo-600 dark:text-indigo-400" />
              প্রস্তুতি রোডম্যাপ
            </span>
          </div>

          <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#0A1A3A] dark:text-[#EEF2FF]">
            ইন্টারভিউ প্রস্তুতি ও প্রফেশনাল ক্যারিয়ার গাইডলাইন
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
            করপোরেট এইচআর ও টেকনিক্যাল বোর্ডে সাফল্য অর্জনের পরীক্ষিত কৌশল
          </p>
        </div>

        <div className="relative z-10 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#0F172A]/95 border border-indigo-100/90 dark:border-indigo-900/50 shadow-xs space-y-2 hover:shadow-md transition">
            <span className="text-xs font-bold text-[#0A2540] dark:text-amber-300 font-bengali flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>১. এভিডেন্স-বেসড পোর্টফোলিও</span>
            </span>
            <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
              শুধুমাত্র মুখে দাবি করার পরিবর্তে আপনার করা বাস্তব প্রজেক্টের লাইভ লিঙ্ক বা গিটহাব রিপোজিটরি যুক্ত করুন। নিয়োগকর্তা প্রমাণ পেলে ৮৫% বেশি গুরুত্ব দেন।
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#0F172A]/95 border border-indigo-100/90 dark:border-indigo-900/50 shadow-xs space-y-2 hover:shadow-md transition">
            <span className="text-xs font-bold text-[#0A2540] dark:text-amber-300 font-bengali flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>২. এটিএস-ফ্রেন্ডলি সিভি ফরম্যাট</span>
            </span>
            <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
              জটিল ফ্যান্সি ডিজাইন বাদ দিয়ে স্ট্যান্ডার্ড এক বা দুই পৃষ্ঠার পরিষ্কার ফরম্যাট ব্যবহার করুন যাতে স্ক্রিনিং অ্যালগরিদম সহজেই আপনার তথ্য পড়তে পারে।
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#0F172A]/95 border border-indigo-100/90 dark:border-indigo-900/50 shadow-xs space-y-2 hover:shadow-md transition">
            <span className="text-xs font-bold text-[#0A2540] dark:text-amber-300 font-bengali flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>৩. বিহেভিয়োরাল ও টেকনিক্যাল ভাইভা</span>
            </span>
            <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
              STAR (Situation, Task, Action, Result) মেথডে যেকোনো প্রশ্নের গুছিয়ে উত্তর দিন। কোম্পানির সাম্প্রতিক অর্জন ও কার্যক্রম সম্পর্কে ধারণা রাখুন।
            </p>
          </div>
        </div>
      </div>

      {/* 4. FAQ Accordion with Atmospheric Elevation */}
      <div className="relative overflow-hidden rounded-3xl border border-slate-200/80 dark:border-[#262D3D] bg-white/95 dark:bg-[#0B0F19]/95 p-6 sm:p-8 shadow-xs space-y-6">
        
        <div className="relative z-10 border-b border-slate-200/60 dark:border-slate-800 pb-5 space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-white dark:bg-[#121B2D] text-emerald-800 dark:text-emerald-300 border border-slate-200 dark:border-slate-800 shadow-xs font-bengali">
              <HelpCircle className="w-3.5 h-3.5 mr-1 text-emerald-600" />
              সহায়তা ও নিরাপত্তা
            </span>
          </div>

          <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#0A2540] dark:text-white">
            সচরাচর জিজ্ঞাসিত প্রশ্নাবলী (FAQ)
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
            আবেদন প্রক্রিয়া, সিলগালা সিভি স্ন্যাপশট ও নিয়োগ সুরক্ষা সম্পর্কিত তথ্যাদি
          </p>
        </div>

        <div className="relative z-10 space-y-3">
          {CAREER_PORTAL_FAQS.map((faq, idx) => {
            const isOpen = openFaqIndex === idx;
            return (
              <div
                key={idx}
                className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 overflow-hidden transition-all"
              >
                <button
                  onClick={() => toggleFaq(idx)}
                  className="w-full p-4 sm:p-5 text-left flex items-center justify-between gap-4 font-bold text-xs sm:text-sm text-slate-900 dark:text-white font-bengali hover:text-[#0A2540] dark:hover:text-amber-300 transition cursor-pointer"
                >
                  <span>{faq.question}</span>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-[#ED8E22] shrink-0" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                  )}
                </button>

                {isOpen && (
                  <div className="px-4 sm:px-5 pb-5 text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed border-t border-slate-200/60 dark:border-slate-800 pt-3.5">
                    {faq.answer}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
};
