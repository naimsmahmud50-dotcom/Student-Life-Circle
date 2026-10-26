/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: JobApplyModal.tsx
 * PURPOSE:   Bdjobs-Style Online Application Flow with Sealed Cryptographic CV Snapshot
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { 
  X, 
  Send, 
  Lock, 
  ShieldCheck, 
  CheckCircle2, 
  FileText, 
  Building2, 
  Banknote,
  Hash,
  AlertCircle
} from 'lucide-react';
import { CareerJob } from './data/careerElevationData';

interface JobApplyModalProps {
  job: CareerJob | null;
  isOpen: boolean;
  onClose: () => void;
  sealedSnapshotHash: string;
  onApplicationSubmitted: (application: {
    jobId: string;
    companyName: string;
    role: string;
    appliedDate: string;
    stage: 'APPLIED' | 'VIEWED' | 'SHORTLISTED' | 'INTERVIEW' | 'OFFER';
    cvSnapshotId: string;
    expectedSalary: number;
    trackingId: string;
  }) => void;
}

export const JobApplyModal: React.FC<JobApplyModalProps> = ({
  job,
  isOpen,
  onClose,
  sealedSnapshotHash,
  onApplicationSubmitted
}) => {
  const [expectedSalary, setExpectedSalary] = useState<string>('40000');
  const [coverNote, setCoverNote] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [submittedData, setSubmittedData] = useState<{ trackingId: string } | null>(null);

  if (!isOpen || !job) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    setTimeout(() => {
      const trackingId = `OGRO-APP-${Math.floor(10000 + Math.random() * 90000)}`;
      setSubmittedData({ trackingId });
      setIsSubmitting(false);
    }, 200);
  };

  const handleFinish = () => {
    if (submittedData && job) {
      onApplicationSubmitted({
        jobId: job.id,
        companyName: job.companyName,
        role: job.title,
        appliedDate: "২৬ অক্টোবর ২০২৬",
        stage: 'APPLIED',
        cvSnapshotId: sealedSnapshotHash,
        expectedSalary: Number(expectedSalary) || job.minSalary,
        trackingId: submittedData.trackingId
      });
    }
    setSubmittedData(null);
    onClose();
  };

  const handleClose = () => {
    setSubmittedData(null);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4">
      <div 
        className="relative w-full max-w-xl rounded-3xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden my-8"
        role="dialog"
        aria-modal="true"
      >
        
        {/* Header */}
        <div className="p-6 border-b border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-[#0A2540] text-amber-300">
                অনলাইন আবেদন ফর্ম
              </span>
              <span className="text-xs text-slate-500 font-mono font-bold">
                {job.id}
              </span>
            </div>
            <h2 className="text-lg font-black text-slate-900 dark:text-white font-bengali">
              {job.title}
            </h2>
            <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali mt-0.5">
              {job.companyName}
            </p>
          </div>

          <button
            onClick={handleClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {submittedData ? (
          /* Success Screen */
          <div className="p-6 sm:p-8 text-center space-y-4">
            <div className="w-16 h-16 rounded-full bg-emerald-100 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 flex items-center justify-center mx-auto border-2 border-emerald-300 dark:border-emerald-700">
              <CheckCircle2 className="w-8 h-8" />
            </div>

            <h3 className="text-xl font-black text-slate-900 dark:text-white font-bengali">
              আবেদন সফলভাবে গৃহীত হয়েছে!
            </h3>
            
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 font-bengali max-w-md mx-auto leading-relaxed">
              আপনার সিলগালা ক্রিপ্টোগ্রাফিক সিভি স্ন্যাপশট নিয়োগকারী প্রতিষ্ঠান <strong>{job.companyName}</strong>-এর এইচআর ড্যাশবোর্ডে তালিকাভুক্ত হয়েছে।
            </p>

            <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 max-w-sm mx-auto text-left space-y-1.5">
              <div className="flex items-center justify-between text-xs font-bengali">
                <span className="text-slate-500">অ্যাপ্লিকেশন ট্র্যাকিং আইডি:</span>
                <span className="font-mono font-bold text-[#0A2540] dark:text-amber-300">{submittedData.trackingId}</span>
              </div>
              <div className="flex items-center justify-between text-xs font-bengali">
                <span className="text-slate-500">সিভি স্ন্যাপশট হ্যাশ:</span>
                <span className="font-mono text-[11px] text-slate-600 dark:text-slate-400 truncate max-w-[150px]">{sealedSnapshotHash}</span>
              </div>
            </div>

            <button
              onClick={handleFinish}
              className="mt-4 px-6 py-2.5 rounded-2xl bg-[#0A2540] hover:bg-[#081c30] text-white font-bold font-bengali text-xs shadow-sm cursor-pointer"
            >
              সম্পন্ন করুন
            </button>
          </div>
        ) : (
          /* Application Form */
          <form onSubmit={handleSubmit} className="p-6 space-y-5">
            
            {/* Sealed CV Snapshot Verification Notice */}
            <div className="p-4 rounded-2xl bg-emerald-50/60 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/80 flex items-start gap-3">
              <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
              <div className="space-y-1 text-xs">
                <span className="font-bold text-emerald-900 dark:text-emerald-300 font-bengali">
                  সিলগালা ক্রিপ্টোগ্রাফিক সিভি স্ন্যাপশট সংযুক্ত
                </span>
                <p className="text-slate-600 dark:text-slate-400 font-bengali leading-relaxed">
                  আপনার বর্তমান ভেরিফায়েড প্রফেশনাল প্রোফাইল ও একাডেমিক স্কোর হ্যাশ আকারে লক থাকবে।
                </p>
                <div className="font-mono text-[11px] font-bold text-emerald-800 dark:text-emerald-400 bg-white dark:bg-slate-900 px-2 py-0.5 rounded border border-emerald-300 dark:border-emerald-800 inline-block">
                  {sealedSnapshotHash}
                </div>
              </div>
            </div>

            {/* Expected Salary Input */}
            <div className="space-y-1.5">
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                মাসিক প্রত্যাশিত পারিশ্রমিক / বেতন (টাকায়):
              </label>
              <div className="relative">
                <Banknote className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                <input
                  type="number"
                  value={expectedSalary}
                  onChange={(e) => setExpectedSalary(e.target.value)}
                  placeholder="যেমন: ৪০০০"
                  className="w-full pl-10 pr-4 py-2.5 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950 border border-slate-300 dark:border-slate-700 text-xs sm:text-sm font-bengali text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0A2540]"
                />
              </div>
              <p className="text-[11px] text-slate-500 font-bengali">
                বিজ্ঞাপিত বেতন স্কেল: {job.minSalary.toLocaleString('bn-BD')} - {job.maxSalary.toLocaleString('bn-BD')} টাকা
              </p>
            </div>

            {/* Priority Note / Cover Letter */}
            <div className="space-y-1.5">
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                সংক্ষিপ্ত কভার নোট / আবেদন বার্তা (ঐচ্ছিক):
              </label>
              <textarea
                rows={3}
                value={coverNote}
                onChange={(e) => setCoverNote(e.target.value)}
                placeholder="নিয়োগকর্তার উদ্দেশে আপনার প্রাসঙ্গিক অভিজ্ঞতা বা শিক্ষাগত বিশেষত্ব উল্লেখ করুন..."
                className="w-full p-3 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950 border border-slate-300 dark:border-slate-700 text-xs sm:text-sm font-bengali text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0A2540]"
              />
            </div>

            {/* Footer Buttons */}
            <div className="pt-2 border-t border-slate-200 dark:border-slate-800 flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={handleClose}
                className="px-4 py-2.5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 text-slate-700 dark:text-slate-300 text-xs font-bold font-bengali transition cursor-pointer"
              >
                বাতিল করুন
              </button>

              <button
                type="submit"
                disabled={isSubmitting}
                className="px-6 py-2.5 rounded-2xl bg-[#0A2540] hover:bg-[#081c30] text-white font-bold font-bengali text-xs shadow-[0_4px_0_0_#071D33] active:translate-y-1 active:shadow-none transition flex items-center gap-2 cursor-pointer"
              >
                <Send className="w-3.5 h-3.5 text-amber-300" />
                <span>{isSubmitting ? "আবেদন জমা হচ্ছে..." : "আবেদন নিশ্চিত করুন"}</span>
              </button>
            </div>

          </form>
        )}

      </div>
    </div>
  );
};
