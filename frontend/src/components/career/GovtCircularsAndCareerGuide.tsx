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
  Briefcase
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
      
      {/* 1. Official Government Circulars Grid */}
      <div className="rounded-3xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-7 shadow-sm space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 dark:border-slate-800 pb-4">
          <div>
            <h2 className="text-lg font-bold flex items-center gap-2 font-bengali text-[#0A2540] dark:text-white">
              <Award className="w-5 h-5 text-amber-600 dark:text-amber-400" />
              <span>সরকারি ও ক্যাডার সার্ভিস নিয়োগ বিজ্ঞপ্তি (Official Circulars)</span>
            </h2>
            <p className="text-xs text-slate-500 font-bengali mt-1">
              বাংলাদেশ সরকারি কর্ম কমিশন (BPSC), বাংলাদেশ ব্যাংক ও মন্ত্রণালয় সমূহের অনুমোদিত সার্কুলার
            </p>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-amber-50 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
            ৪টি অ্যাক্টিভ গেজেট
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {GOVT_CIRCULAR_ARCHIVES.map((circ) => (
            <div
              key={circ.id}
              className="p-5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/40 flex flex-col justify-between space-y-4 hover:border-slate-300 transition"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-100 dark:bg-amber-950/80 text-amber-900 dark:text-amber-300">
                    {circ.id}
                  </span>
                  <span className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    মোট পদ: {circ.totalPosts.toLocaleString('bn-BD')} টি
                  </span>
                </div>

                <h3 className="font-bold text-sm text-slate-900 dark:text-white font-bengali">
                  {circ.title}
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali">
                  {circ.ministryOrDepartment}
                </p>

                <div className="p-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-[11px] font-bengali space-y-1">
                  <div className="text-slate-500">বেতন স্কেল: {circ.gradePayScale}</div>
                  <div className="text-rose-600 dark:text-rose-400 font-semibold flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    <span>শেষ তারিখ: {circ.applicationDeadline}</span>
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t border-slate-200/60 dark:border-slate-800/60 flex items-center justify-between text-xs font-semibold text-[#0A2540] dark:text-amber-300 font-bengali">
                <span>অফিসিয়াল গেজেট ও আবেদন লিংক:</span>
                <span className="font-mono text-[11px] text-slate-500 flex items-center gap-1">
                  <span>{circ.officialRef}</span>
                  <ExternalLink className="w-3 h-3" />
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 2. Bangladesh Industry Salary Insights & Benchmarks */}
      <div className="rounded-3xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-7 shadow-sm space-y-5">
        <div className="border-b border-slate-200 dark:border-slate-800 pb-4">
          <h2 className="text-lg font-bold flex items-center gap-2 font-bengali text-[#0A2540] dark:text-white">
            <TrendingUp className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            <span>শিল্প ও পদবি ভেদে গড় বেতন নির্দেশিকা (Salary Insights)</span>
          </h2>
          <p className="text-xs text-slate-500 font-bengali mt-1">
            বাংলাদেশের শীর্ষস্থানীয় কর্মক্ষেত্রে এন্ট্রি, মিড ও সিনিয়র লেভেলের বর্তমান মার্কেট রেট
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-bengali border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 text-slate-600 dark:text-slate-300">
                <th className="p-3 font-bold">সেক্টর ও পদবি</th>
                <th className="p-3 font-bold">এন্ট্রি-লেভেল / ফ্রেশার</th>
                <th className="p-3 font-bold">মিড-লেভেল (২-৪ বছর)</th>
                <th className="p-3 font-bold">সিনিয়র / লিড লেভেল</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {SALARY_BENCHMARKS.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-800/40 transition">
                  <td className="p-3 font-bold text-slate-900 dark:text-white">
                    <div>{item.roleTitle}</div>
                    <div className="text-[11px] text-slate-500 font-normal">{item.industry}</div>
                  </td>
                  <td className="p-3 text-slate-700 dark:text-slate-300 font-medium">
                    {item.entryLevelSalary}
                  </td>
                  <td className="p-3 text-emerald-700 dark:text-emerald-400 font-bold">
                    {item.midLevelSalary}
                  </td>
                  <td className="p-3 text-[#0A2540] dark:text-amber-300 font-black">
                    {item.seniorLevelSalary}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 3. Career & Interview Preparation Tips */}
      <div className="rounded-3xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-7 shadow-sm space-y-4">
        <div className="border-b border-slate-200 dark:border-slate-800 pb-4">
          <h2 className="text-lg font-bold flex items-center gap-2 font-bengali text-[#0A2540] dark:text-white">
            <BookOpen className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <span>ইন্টারভিউ প্রস্তুতি ও প্রফেশনাল ক্যারিয়ার গাইডলাইন</span>
          </h2>
          <p className="text-xs text-slate-500 font-bengali mt-1">
            করপোরেট এইচআর ও টেকনিক্যাল বোর্ডে সাফল্য অর্জনের পরীক্ষিত কৌশল
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800 space-y-2">
            <span className="text-xs font-bold text-[#0A2540] dark:text-amber-300 font-bengali block">
              ১. এভিডেন্স-বেসড পোর্টফোলিও
            </span>
            <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed">
              শুধুমাত্র মুখে দাবি করার পরিবর্তে আপনার করা বাস্তব প্রজেক্টের লাইভ লিঙ্ক বা গিটহাব রিপোজিটরি যুক্ত করুন। নিয়োগকর্তা প্রমাণ পেলে ৮৫% বেশি গুরুত্ব দেন।
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800 space-y-2">
            <span className="text-xs font-bold text-[#0A2540] dark:text-amber-300 font-bengali block">
              ২. এটিএস-ফ্রেন্ডলি সিভি ফরম্যাট
            </span>
            <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed">
              জটিল ফ্যান্সি ডিজাইন বাদ দিয়ে স্ট্যান্ডার্ড এক বা দুই পৃষ্ঠার পরিষ্কার ফরম্যাট ব্যবহার করুন যাতে স্ক্রিনিং অ্যালগরিদম সহজেই আপনার তথ্য পড়তে পারে।
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800 space-y-2">
            <span className="text-xs font-bold text-[#0A2540] dark:text-amber-300 font-bengali block">
              ৩. বিহেভিয়োরাল ও টেকনিক্যাল ভাইভা
            </span>
            <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed">
              STAR (Situation, Task, Action, Result) মেথডে যেকোনো প্রশ্নের গুছিয়ে উত্তর দিন। কোম্পানির সাম্প্রতিক অর্জন ও কার্যক্রম সম্পর্কে ধারণা রাখুন।
            </p>
          </div>
        </div>
      </div>

      {/* 4. FAQ Accordion */}
      <div className="rounded-3xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-7 shadow-sm space-y-4">
        <div className="border-b border-slate-200 dark:border-slate-800 pb-4">
          <h2 className="text-lg font-bold flex items-center gap-2 font-bengali text-[#0A2540] dark:text-white">
            <ShieldCheck className="w-5 h-5 text-emerald-600" />
            <span>সচরাচর জিজ্ঞাসিত প্রশ্নাবলী (FAQ)</span>
          </h2>
          <p className="text-xs text-slate-500 font-bengali mt-1">
            আবেদন প্রক্রিয়া, সিলগালা সিভি স্ন্যাপশট ও নিয়োগ সুরক্ষা সম্পর্কিত তথ্যাদি
          </p>
        </div>

        <div className="space-y-3">
          {CAREER_PORTAL_FAQS.map((faq, idx) => {
            const isOpen = openFaqIndex === idx;
            return (
              <div
                key={idx}
                className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/40 overflow-hidden"
              >
                <button
                  onClick={() => toggleFaq(idx)}
                  className="w-full p-4 text-left flex items-center justify-between gap-4 font-bold text-xs sm:text-sm text-slate-900 dark:text-white font-bengali hover:text-[#0A2540] dark:hover:text-amber-300 transition cursor-pointer"
                >
                  <span>{faq.question}</span>
                  {isOpen ? (
                    <ChevronUp className="w-4 h-4 text-slate-400 shrink-0" />
                  ) : (
                    <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                  )}
                </button>

                {isOpen && (
                  <div className="px-4 pb-4 text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed border-t border-slate-100 dark:border-slate-800 pt-3">
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
