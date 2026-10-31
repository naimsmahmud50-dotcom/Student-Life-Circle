/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: CareerATSApplicationPipeline.tsx
 * PURPOSE:   Bdjobs-Style Applicant Tracking System (ATS) Pipeline with Atmospheric Elevation
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, WCAG 2.2 AAA
 * INVARIANTS: Preserves 'SHORTLISTED' string and 'cvSnapshotId' for backend compatibility.
 */

import React from 'react';
import { 
  Building2, 
  Calendar, 
  Clock, 
  CheckCircle2, 
  ShieldCheck, 
  ArrowRight, 
  ExternalLink,
  Users,
  Video,
  FileCheck,
  AlertCircle,
  GitCommit
} from 'lucide-react';

export interface ApplicationItem {
  jobId: string;
  companyName: string;
  role: string;
  appliedDate: string;
  stage: 'APPLIED' | 'VIEWED' | 'SHORTLISTED' | 'INTERVIEW' | 'OFFER';
  cvSnapshotId: string;
  interviewDetails?: {
    date: string;
    time: string;
    type: 'ONLINE_VIVA' | 'IN_PERSON';
    locationOrLink: string;
  };
}

interface CareerATSApplicationPipelineProps {
  applications: ApplicationItem[];
  onOpenCvSnapshot: (hash: string) => void;
}

export const CareerATSApplicationPipeline: React.FC<CareerATSApplicationPipelineProps> = ({
  applications,
  onOpenCvSnapshot
}) => {
  const getStageBadge = (stage: ApplicationItem['stage']) => {
    switch (stage) {
      case 'OFFER':
        return (
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-purple-100 text-purple-900 dark:bg-purple-950/70 dark:text-purple-300 border border-purple-300 dark:border-purple-800 shadow-xs">
            OFFER (চাকরির প্রস্তাব)
          </span>
        );
      case 'INTERVIEW':
        return (
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-amber-100 text-amber-900 dark:bg-amber-950/70 dark:text-amber-300 border border-amber-300 dark:border-amber-700 shadow-xs animate-pulse">
            INTERVIEW (সাক্ষাৎকার নির্ধারিত)
          </span>
        );
      case 'SHORTLISTED':
        return (
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-emerald-100 text-emerald-900 dark:bg-emerald-950/70 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 shadow-xs">
            SHORTLISTED (বাছাইকৃত)
          </span>
        );
      case 'VIEWED':
        return (
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-blue-100 text-blue-900 dark:bg-blue-950/70 dark:text-blue-300 border border-blue-300 dark:border-blue-800 shadow-xs">
            VIEWED (সিভি পর্যালোচিত)
          </span>
        );
      default:
        return (
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700 shadow-xs">
            APPLIED (আবেদন জমাকৃত)
          </span>
        );
    }
  };

  const stagesList = ['APPLIED', 'VIEWED', 'SHORTLISTED', 'INTERVIEW', 'OFFER'];

  return (
    <div className="relative overflow-hidden rounded-3xl border border-indigo-200/60 dark:border-indigo-950/70 bg-[#F8FAFD]/90 dark:bg-[#09111E]/90 p-6 sm:p-8 shadow-xs space-y-6">
      
      {/* Indigo Atmospheric Halo */}
      <div
        className="absolute bottom-0 right-0 w-full pointer-events-none select-none z-0"
        style={{
          height: '100%',
          minHeight: '260px',
          background:
            'radial-gradient(ellipse 65% 90% at 75% 100%, rgba(99, 102, 241, 0.14) 0%, rgba(99, 102, 241, 0.03) 50%, transparent 100%)'
        }}
        aria-hidden="true"
      />

      {/* Atmospheric Typographic Watermark */}
      <div
        className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
        aria-hidden="true"
      >
        <p
          className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,18vw,12rem)] uppercase tracking-wider select-none opacity-85"
          style={{
            lineHeight: 0.95,
            backgroundImage:
              'linear-gradient(to bottom, rgba(99, 102, 241, 0.18) 15%, rgba(99, 102, 241, 0.01) 100%)'
          }}
        >
          PIPELINE
        </p>
      </div>

      {/* Header */}
      <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-indigo-200/60 dark:border-indigo-900/60 pb-5">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-indigo-100/90 dark:bg-indigo-950/60 text-indigo-900 dark:text-indigo-300 border border-indigo-300/80 dark:border-indigo-800 shadow-xs font-bengali">
              <Users className="w-3.5 h-3.5 mr-1 text-indigo-600 dark:text-indigo-400" />
              অ্যাপ্লিকেশন ট্র্যাকিং সিস্টেম
            </span>
          </div>

          <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#0A1A3A] dark:text-[#EEF2FF]">
            চাকরির আবেদন পাইপলাইন (Application Tracking Pipeline)
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
            শীর্ষ প্রযুক্তি কোম্পানিতে জমাকৃত সিভি স্ন্যাপশট, স্টেজ আপডেট ও ভাইভা শিডিউল ট্র্যাকিং
          </p>
        </div>

        <div className="px-3.5 py-1.5 rounded-2xl bg-white dark:bg-[#121B2D] border border-indigo-200/70 dark:border-indigo-900/70 shadow-xs text-xs text-slate-600 dark:text-slate-300 font-bengali">
          মোট সক্রিয় আবেদন: <strong className="text-indigo-900 dark:text-amber-300 font-mono text-sm ml-1">{applications.length}</strong>
        </div>
      </div>

      {/* Applications List */}
      <div className="relative z-10 space-y-4">
        {applications.map((app) => {
          const currentStageIndex = stagesList.indexOf(app.stage);

          return (
            <div
              key={app.jobId}
              className="p-5 sm:p-6 rounded-2xl border border-indigo-100/90 dark:border-indigo-900/50 bg-white/95 dark:bg-[#0F172A]/95 shadow-xs hover:border-indigo-300 dark:hover:border-indigo-700 hover:shadow-md transition-all duration-200 space-y-4"
            >
              {/* Top Row: Company & Stage */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-start gap-3.5">
                  <div className="w-12 h-12 rounded-xl bg-[#0A2540] text-white flex items-center justify-center font-bold shrink-0 shadow-xs border border-white/20">
                    <Building2 className="w-5 h-5 text-amber-300" />
                  </div>
                  <div className="space-y-0.5">
                    <h3 className="text-base font-bold text-slate-900 dark:text-white font-bengali">
                      {app.companyName}
                    </h3>
                    <p className="text-xs text-slate-500 font-bengali">
                      {app.role} • আবেদন: {app.appliedDate}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {getStageBadge(app.stage)}
                  <span className="text-xs font-mono font-semibold text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-900 px-3 py-1 rounded-xl border border-slate-200 dark:border-slate-800 shadow-xs">
                    ID: {app.cvSnapshotId}
                  </span>
                </div>
              </div>

              {/* Progress Steps Indicator */}
              <div className="grid grid-cols-5 gap-2 pt-2">
                {stagesList.map((st, idx) => {
                  const isCompleted = idx <= currentStageIndex;
                  const isCurrent = idx === currentStageIndex;

                  return (
                    <div key={st} className="space-y-1.5 text-center">
                      <div
                        className={`h-2.5 rounded-full transition-all ${
                          isCompleted
                            ? 'bg-[#0A2540] dark:bg-amber-400 shadow-xs'
                            : 'bg-slate-200 dark:bg-slate-800'
                        }`}
                      />
                      <span className={`text-[10px] font-mono block ${isCurrent ? 'font-black text-[#0A2540] dark:text-amber-300' : 'text-slate-400 font-medium'}`}>
                        {st}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* Interview Box (If in interview stage) */}
              {app.stage === 'INTERVIEW' && (
                <div className="p-4 rounded-2xl bg-amber-50/90 dark:bg-amber-950/50 border border-amber-200 dark:border-amber-800/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs shadow-xs">
                  <div className="flex items-center gap-3 text-amber-950 dark:text-amber-200 font-bengali">
                    <div className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-700 dark:text-amber-300 flex items-center justify-center shrink-0">
                      <Video className="w-4 h-4" />
                    </div>
                    <div>
                      <span className="font-semibold block">সাক্ষাৎকার আহ্বান সূচি:</span>
                      <strong className="text-amber-900 dark:text-amber-300">২৮ অক্টোবর ২০২৬, সকাল ১১:০০টা</strong> (গুগল মিট অনলাইন ভাইভা)
                    </div>
                  </div>
                  <button className="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-bold font-bengali shadow-xs active:translate-y-0.5 transition cursor-pointer self-start sm:self-auto">
                    মিটিং লিংক খুলুন
                  </button>
                </div>
              )}

              {/* Bottom Row: Verifiable CV Snapshot Hash */}
              <div className="pt-3 border-t border-slate-200/60 dark:border-slate-800/60 flex items-center justify-between text-xs text-slate-500 font-bengali">
                <span className="flex items-center gap-1.5">
                  <FileCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>সিলগালা ক্রিপ্টোগ্রাফিক সিভি স্ন্যাপশট সংরক্ষিত</span>
                </span>
                <button
                  onClick={() => onOpenCvSnapshot(app.cvSnapshotId)}
                  className="font-mono text-xs text-[#0A2540] dark:text-amber-300 hover:underline flex items-center gap-1 cursor-pointer font-bold"
                >
                  <span>যাচাই ও প্রিভিউ</span>
                  <ExternalLink className="w-3 h-3" />
                </button>
              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
};
