/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: CareerATSApplicationPipeline.tsx
 * PURPOSE:   Bdjobs-Style Applicant Tracking System (ATS) Pipeline & Interview Scheduler
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, WCAG 2.2 AAA
 * INVARIANTS: Preserves 'SHORTLISTED' string and 'cvSnapshotId' for Phase 77/98 backend tests.
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
  AlertCircle
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
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-purple-100 text-purple-900 dark:bg-purple-950/60 dark:text-purple-300 border border-purple-300">
            OFFER (চাকরির প্রস্তাব)
          </span>
        );
      case 'INTERVIEW':
        return (
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-amber-100 text-amber-900 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-300 animate-pulse">
            INTERVIEW (সাক্ষাৎকার নির্ধারিত)
          </span>
        );
      case 'SHORTLISTED':
        return (
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-emerald-100 text-emerald-900 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-300">
            SHORTLISTED (বাছাইকৃত)
          </span>
        );
      case 'VIEWED':
        return (
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-blue-100 text-blue-900 dark:bg-blue-950/60 dark:text-blue-300 border border-blue-300">
            VIEWED (সিভি পর্যালোচিত)
          </span>
        );
      default:
        return (
          <span className="px-3 py-1 rounded-full text-xs font-bold font-mono bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
            APPLIED (আবেদন জমাকৃত)
          </span>
        );
    }
  };

  const stagesList = ['APPLIED', 'VIEWED', 'SHORTLISTED', 'INTERVIEW', 'OFFER'];

  return (
    <div className="rounded-3xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-7 shadow-sm space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <h2 className="text-lg font-bold flex items-center gap-2 font-bengali text-[#0A2540] dark:text-white">
            <Users className="w-5 h-5 text-[#0A2540] dark:text-amber-300" />
            <span>চাকরির আবেদন পাইপলাইন (Application Tracking Pipeline)</span>
          </h2>
          <p className="text-xs text-slate-500 font-bengali mt-1">
            শীর্ষ প্রযুক্তি কোম্পানিতে জমাকৃত সিভি স্ন্যাপশট ও স্ট্যাটাস ট্র্যাকিং
          </p>
        </div>

        <div className="text-xs text-slate-500 font-bengali">
          মোট সক্রিয় আবেদন: <strong className="text-slate-900 dark:text-white font-mono">{applications.length}</strong>
        </div>
      </div>

      {/* Applications List */}
      <div className="space-y-4">
        {applications.map((app) => {
          const currentStageIndex = stagesList.indexOf(app.stage);

          return (
            <div
              key={app.jobId}
              className="p-5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 space-y-4"
            >
              {/* Top Row: Company & Stage */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div className="flex items-start gap-3.5">
                  <div className="w-11 h-11 rounded-xl bg-[#0A2540] text-white flex items-center justify-center font-bold shrink-0">
                    <Building2 className="w-5 h-5 text-amber-300" />
                  </div>
                  <div>
                    <h3 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white font-bengali">
                      {app.companyName}
                    </h3>
                    <p className="text-xs text-slate-500 font-bengali">
                      {app.role} • আবেদন: {app.appliedDate}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {getStageBadge(app.stage)}
                  <span className="text-xs font-mono text-slate-500 bg-white dark:bg-slate-900 px-2.5 py-1 rounded border border-slate-200 dark:border-slate-800">
                    ID: {app.cvSnapshotId}
                  </span>
                </div>
              </div>

              {/* Progress Steps Indicator */}
              <div className="grid grid-cols-5 gap-1.5 pt-2">
                {stagesList.map((st, idx) => {
                  const isCompleted = idx <= currentStageIndex;
                  const isCurrent = idx === currentStageIndex;

                  return (
                    <div key={st} className="space-y-1 text-center">
                      <div
                        className={`h-2 rounded-full transition-all ${
                          isCompleted
                            ? 'bg-[#0A2540] dark:bg-amber-400'
                            : 'bg-slate-200 dark:bg-slate-800'
                        }`}
                      />
                      <span className={`text-[10px] font-mono block ${isCurrent ? 'font-bold text-[#0A2540] dark:text-amber-300' : 'text-slate-400'}`}>
                        {st}
                      </span>
                    </div>
                  );
                })}
              </div>

              {/* Interview Box (If in interview stage) */}
              {app.stage === 'INTERVIEW' && (
                <div className="p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 flex items-center justify-between gap-3 text-xs">
                  <div className="flex items-center gap-2.5 text-amber-900 dark:text-amber-200 font-bengali">
                    <Video className="w-4 h-4 text-amber-600 shrink-0" />
                    <span>
                      সাক্ষাৎকার আহ্বান: <strong>২৮ অক্টোবর ২০২৬, সকাল ১১:০০টা</strong> (গুগল মিট অনলাইন ভাইভা)
                    </span>
                  </div>
                  <button className="px-3 py-1 rounded-lg bg-amber-600 text-white font-bold font-bengali hover:bg-amber-700 transition cursor-pointer">
                    মিটিং লিংক
                  </button>
                </div>
              )}

              {/* Bottom Row: Verifiable CV Snapshot Hash */}
              <div className="pt-2 border-t border-slate-200/60 dark:border-slate-800/60 flex items-center justify-between text-xs text-slate-500 font-bengali">
                <span className="flex items-center gap-1.5">
                  <FileCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>সিলগালা ক্রিপ্টোগ্রাফিক সিভি স্ন্যাপশট সংযুক্ত</span>
                </span>
                <button
                  onClick={() => onOpenCvSnapshot(app.cvSnapshotId)}
                  className="font-mono text-xs text-[#0A2540] dark:text-amber-300 hover:underline flex items-center gap-1"
                >
                  <span>যাচাই করুন</span>
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
