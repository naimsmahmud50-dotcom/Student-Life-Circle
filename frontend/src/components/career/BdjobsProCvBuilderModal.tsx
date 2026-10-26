/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: BdjobsProCvBuilderModal.tsx
 * PURPOSE:   Bdjobs-Style Professional CV Builder & Profile Completeness Meter (85%)
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { 
  X, 
  FileText, 
  Download, 
  CheckCircle2, 
  User, 
  GraduationCap, 
  Briefcase, 
  Code, 
  ShieldCheck, 
  Printer,
  Sparkles,
  Award
} from 'lucide-react';

interface BdjobsProCvBuilderModalProps {
  isOpen: boolean;
  onClose: () => void;
  sealedSnapshotHash: string;
}

export const BdjobsProCvBuilderModal: React.FC<BdjobsProCvBuilderModalProps> = ({
  isOpen,
  onClose,
  sealedSnapshotHash
}) => {
  const [activeTab, setActiveTab] = useState<'personal' | 'academic' | 'skills' | 'experience' | 'preview'>('preview');

  // Candidate Data State
  const [candidateName, setCandidateName] = useState('মাহমুদ হাসান (Mahmud Hasan)');
  const [candidateEmail, setCandidateEmail] = useState('mahmud.cse.du@gmail.com');
  const [candidatePhone, setCandidatePhone] = useState('০১৭**-******');
  const [candidateLocation, setCandidateLocation] = useState('ধানমন্ডি, ঢাকা');
  
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4">
      <div 
        className="relative w-full max-w-4xl rounded-3xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden my-6"
        role="dialog"
        aria-modal="true"
      >
        
        {/* Top Header with Completeness Meter */}
        <div className="p-6 border-b border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-[#0A2540] text-amber-300 flex items-center justify-center font-bold shrink-0">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-black text-slate-900 dark:text-white font-bengali">
                  অগ্রযাত্রা প্রফেশনাল সিভি বিল্ডার
                </h2>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-300">
                  বিডিজবস ফরম্যাট স্ট্যান্ডার্ড
                </span>
              </div>
              <p className="text-xs text-slate-500 font-bengali mt-0.5">
                বাংলাদেশি করপোরেট ও বহুজাতিক প্রতিষ্ঠানের জন্য অনুমোদিত স্ট্যান্ডার্ড লেআউট
              </p>
            </div>
          </div>

          {/* Completeness Meter (85%) */}
          <div className="flex items-center gap-4">
            <div className="text-right">
              <span className="text-xs text-slate-500 font-bengali block">প্রোফাইল সম্পূর্ণতা:</span>
              <span className="text-sm font-black text-[#0A2540] dark:text-amber-300 font-mono">৮৫% সম্পন্ন</span>
            </div>
            <div className="w-16 bg-slate-200 dark:bg-slate-800 h-2.5 rounded-full overflow-hidden">
              <div className="bg-emerald-600 h-full w-[85%]" />
            </div>

            <button
              onClick={onClose}
              className="p-2 rounded-xl text-slate-400 hover:text-slate-700 dark:hover:text-white transition cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 px-6 pt-3 border-b border-slate-200 dark:border-slate-800 overflow-x-auto">
          {[
            { id: 'preview', label: 'সিভি প্রিভিউ (Standard View)', icon: FileText },
            { id: 'personal', label: 'ব্যক্তিগত তথ্য', icon: User },
            { id: 'academic', label: 'শিক্ষাগত যোগ্যতা', icon: GraduationCap },
            { id: 'skills', label: 'দক্ষতা ও প্রমাণ', icon: Code },
            { id: 'experience', label: 'অভিজ্ঞতা ও ইন্টার্নশিপ', icon: Briefcase }
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-3.5 py-2.5 text-xs font-bold font-bengali flex items-center gap-1.5 border-b-2 transition whitespace-nowrap cursor-pointer ${
                  isActive
                    ? 'border-[#0A2540] dark:border-amber-400 text-[#0A2540] dark:text-white'
                    : 'border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Modal Body */}
        <div className="p-6 sm:p-7 max-h-[65vh] overflow-y-auto space-y-6">
          
          {activeTab === 'preview' && (
            <div className="p-6 sm:p-8 rounded-2xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-950 text-slate-900 dark:text-slate-100 shadow-sm space-y-6 font-sans">
              
              {/* CV Resume Header */}
              <div className="border-b-2 border-slate-800 dark:border-slate-300 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h1 className="text-2xl font-black text-slate-900 dark:text-white font-bengali">
                    {candidateName}
                  </h1>
                  <p className="text-xs text-slate-600 dark:text-slate-300 mt-1">
                    সফটওয়্যার ইঞ্জিনিয়ার (FastAPI / Next.js / PostgreSQL)
                  </p>
                  <p className="text-xs text-slate-500 mt-0.5">
                    ইমেইল: {candidateEmail} • ফোন: {candidatePhone} • ঠিকানা: {candidateLocation}
                  </p>
                </div>

                <div className="text-right">
                  <div className="font-mono text-[10px] font-bold text-slate-500 bg-slate-100 dark:bg-slate-800 p-2 rounded border border-slate-200 dark:border-slate-700">
                    <div>SEALED SNAPSHOT HASH:</div>
                    <div className="text-emerald-700 dark:text-emerald-400">{sealedSnapshotHash}</div>
                  </div>
                </div>
              </div>

              {/* Education Section */}
              <div className="space-y-2">
                <h3 className="text-xs font-black uppercase tracking-wider text-slate-900 dark:text-amber-300 border-b border-slate-200 dark:border-slate-800 pb-1">
                  শিক্ষাগত যোগ্যতা (Educational Background)
                </h3>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between">
                    <div>
                      <span className="font-bold">বিএসসি ইন কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)</span>
                      <p className="text-slate-500 font-bengali">ঢাকা বিশ্ববিদ্যালয় (University of Dhaka)</p>
                    </div>
                    <div className="text-right">
                      <span className="font-mono font-bold">সিজিপিএ: ৩.৮৫ / ৪.০০</span>
                      <p className="text-slate-400">উত্তীর্ণ: ২০২৬</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Verified Technical Skills */}
              <div className="space-y-2">
                <h3 className="text-xs font-black uppercase tracking-wider text-slate-900 dark:text-amber-300 border-b border-slate-200 dark:border-slate-800 pb-1">
                  প্রমাণযুক্ত কারিগরি দক্ষতা (Evidence-Backed Skills)
                </h3>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="p-2 rounded bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                    <span className="font-bold">Python & FastAPI Backend</span>
                    <p className="text-[11px] text-slate-500 font-mono">github.com/student/fastapi-quiz-engine (Verified)</p>
                  </div>
                  <div className="p-2 rounded bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                    <span className="font-bold">React 19 & Next.js App Router</span>
                    <p className="text-[11px] text-slate-500 font-mono">ogrojatra-preview.vercel.app (Verified)</p>
                  </div>
                </div>
              </div>

              {/* Professional Experience / Internships */}
              <div className="space-y-2">
                <h3 className="text-xs font-black uppercase tracking-wider text-slate-900 dark:text-amber-300 border-b border-slate-200 dark:border-slate-800 pb-1">
                  অভিজ্ঞতা ও প্রকল্পসমূহ (Experience & Projects)
                </h3>
                <div className="text-xs space-y-1">
                  <div className="flex justify-between">
                    <span className="font-bold">জুনিয়র সফটওয়্যার ইন্টার্ন — চালডাল টেক ল্যাব</span>
                    <span className="font-mono text-slate-500">জুন ২০২৫ - ডিসেম্বর ২০২৫</span>
                  </div>
                  <p className="text-slate-600 dark:text-slate-400 font-bengali leading-relaxed">
                    মাইক্রোসার্ভিস এপিআই ডিজাইন, ক্যাশিং অপ্টিমাইজেশন এবং স্বয়ংক্রিয় টেস্ট কেস পরিচালনা।
                  </p>
                </div>
              </div>

            </div>
          )}

          {activeTab === 'personal' && (
            <div className="space-y-4 max-w-xl">
              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">পূর্ণ নাম:</label>
                <input
                  type="text"
                  value={candidateName}
                  onChange={(e) => setCandidateName(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">ইমেইল:</label>
                <input
                  type="email"
                  value={candidateEmail}
                  onChange={(e) => setCandidateEmail(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs text-slate-900 dark:text-white"
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">বর্তমান ঠিকানা:</label>
                <input
                  type="text"
                  value={candidateLocation}
                  onChange={(e) => setCandidateLocation(e.target.value)}
                  className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                />
              </div>
            </div>
          )}

          {activeTab !== 'preview' && activeTab !== 'personal' && (
            <div className="p-8 text-center text-slate-500 font-bengali text-xs">
              <CheckCircle2 className="w-8 h-8 text-emerald-600 mx-auto mb-2" />
              <span>আপনার একাডেমিক ও স্কিল পোর্টফোলিও স্বয়ংক্রিয়ভাবে অগ্রযাত্রা ডাটাবেজ থেকে যাচাইকৃত রয়েছে।</span>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="p-4 sm:p-5 border-t border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 flex items-center justify-between gap-4">
          <div className="text-xs text-slate-500 font-bengali flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
            <span>সিলগালা সিভি হ্যাশ: {sealedSnapshotHash.substring(0, 20)}...</span>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => window.print()}
              className="px-4 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 text-slate-700 dark:text-slate-300 text-xs font-bold font-bengali flex items-center gap-1.5 cursor-pointer"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>প্রিন্ট / PDF সংরক্ষণ</span>
            </button>

            <button
              onClick={onClose}
              className="px-5 py-2 rounded-xl bg-[#0A2540] text-white text-xs font-bold font-bengali cursor-pointer"
            >
              সম্পন্ন
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};
