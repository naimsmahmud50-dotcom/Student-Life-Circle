/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: JobDetailModal.tsx
 * PURPOSE:   Bdjobs-Style Comprehensive Job Specification Modal & Drawer
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, WCAG 2.2 AAA
 */

import React from 'react';
import { 
  X, 
  Building2, 
  MapPin, 
  Calendar, 
  Clock, 
  Briefcase, 
  GraduationCap, 
  CheckCircle2, 
  Award, 
  Send, 
  ShieldCheck,
  Banknote,
  FileText,
  Users
} from 'lucide-react';
import { CareerJob } from './data/careerElevationData';
import { useTranslation } from '../../lib/i18n';

interface JobDetailModalProps {
  job: CareerJob | null;
  isOpen: boolean;
  onClose: () => void;
  onOpenApply: (job: CareerJob) => void;
}

export const JobDetailModal: React.FC<JobDetailModalProps> = ({
  job,
  isOpen,
  onClose,
  onOpenApply
}) => {
  const { isBengali } = useTranslation();

  if (!isOpen || !job) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4">
      <div 
        className="relative w-full max-w-3xl rounded-3xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden my-8"
        role="dialog"
        aria-modal="true"
      >
        
        {/* Modal Top Header */}
        <div className="p-6 sm:p-7 border-b border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 flex items-start justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className={`w-14 h-14 rounded-2xl ${job.monogramBg} ${job.monogramText} flex items-center justify-center text-lg font-black shrink-0 shadow-xs border border-white/20`}>
              {job.companyMonogram}
            </div>
            <div className="space-y-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-[#0A2540] text-amber-300">
                  {job.id}
                </span>
                {job.isHotJob && (
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800 dark:bg-rose-950/60 dark:text-rose-300 border border-rose-300">
                    {isBengali ? "হট জব (জরুরি)" : "Hot Job (Urgent)"}
                  </span>
                )}
                {job.isEarlyAccess && (
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-300">
                    {isBengali ? "আর্লি অ্যাক্সেস" : "Early Access"}
                  </span>
                )}
              </div>

              <h2 className="text-xl sm:text-2xl font-black text-slate-900 dark:text-white font-bengali">
                {isBengali ? job.title : (job.titleEn || job.title)}
              </h2>
              <p className="text-sm font-semibold text-slate-600 dark:text-slate-300 flex items-center gap-1.5 font-bengali">
                <Building2 className="w-4 h-4 text-[#0A2540] dark:text-amber-300" />
                <span>{isBengali ? job.companyName : (job.companyNameEn || job.companyName)}</span>
                <span className="text-slate-400">•</span>
                <span className="text-xs text-slate-500">
                  {isBengali ? job.companyIndustry : (job.companyIndustryEn || job.companyIndustry)}
                </span>
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Scrollable Body */}
        <div className="p-6 sm:p-7 space-y-6 max-h-[70vh] overflow-y-auto">
          
          {/* Quick Summary Grid (Bdjobs Style Summary Box) */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800 text-xs">
            <div className="space-y-1">
              <span className="text-slate-500 font-bengali">
                {isBengali ? "খালি পদ (Vacancy):" : "Vacancy:"}
              </span>
              <p className="font-bold text-slate-900 dark:text-white font-bengali">
                {isBengali ? `${job.vacancy} জন` : `${job.vacancy} Positions`}
              </p>
            </div>

            <div className="space-y-1">
              <span className="text-slate-500 font-bengali">
                {isBengali ? "চাকরির ধরন:" : "Job Nature:"}
              </span>
              <p className="font-bold text-slate-900 dark:text-white font-bengali">
                {job.jobNature === 'FULL_TIME'
                  ? (isBengali ? 'ফুল-টাইম' : 'Full-Time')
                  : job.jobNature === 'INTERNSHIP'
                  ? (isBengali ? 'ইন্টার্নশিপ' : 'Internship')
                  : (isBengali ? 'চুক্তিভিত্তিক' : 'Contractual')}
              </p>
            </div>

            <div className="space-y-1">
              <span className="text-slate-500 font-bengali">
                {isBengali ? "অভিজ্ঞতা:" : "Experience:"}
              </span>
              <p className="font-bold text-slate-900 dark:text-white font-bengali">
                {isBengali ? job.experienceYears : (job.experienceYearsEn || job.experienceYears)}
              </p>
            </div>

            <div className="space-y-1">
              <span className="text-slate-500 font-bengali">
                {isBengali ? "কর্মস্থল (Location):" : "Location:"}
              </span>
              <p className="font-bold text-slate-900 dark:text-white font-bengali flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-slate-400" />
                <span>{isBengali ? job.locationDistrict : (job.locationDistrictEn || job.locationDistrict)}</span>
              </p>
            </div>
          </div>

          {/* Salary & Benefits Highlight Bar */}
          <div className="p-4 rounded-2xl border-2 border-emerald-200 dark:border-emerald-800/60 bg-emerald-50/50 dark:bg-emerald-950/20 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <span className="text-xs text-emerald-800 dark:text-emerald-300 font-bengali font-bold flex items-center gap-1">
                <Banknote className="w-4 h-4" />
                <span>{isBengali ? "মাসিক বেতন কাঠামো:" : "Monthly Salary Scale:"}</span>
              </span>
              <div className="text-lg font-black text-slate-900 dark:text-white font-bengali mt-0.5">
                {isBengali
                  ? `${job.minSalary.toLocaleString('bn-BD')} - ${job.maxSalary.toLocaleString('bn-BD')} টাকা`
                  : `৳ ${job.minSalary.toLocaleString('en-US')} - ${job.maxSalary.toLocaleString('en-US')}`}
                {job.isSalaryNegotiable && (
                  <span className="text-xs font-normal text-slate-500 ml-1.5">
                    {isBengali ? "(আলোচনা সাপেক্ষ)" : "(Negotiable)"}
                  </span>
                )}
              </div>
            </div>

            <div className="text-right sm:border-l sm:border-emerald-200 dark:sm:border-emerald-800/60 sm:pl-4">
              <span className="text-xs text-rose-700 dark:text-rose-400 font-bengali font-bold flex items-center gap-1">
                <Clock className="w-3.5 h-3.5" />
                <span>{isBengali ? "আবেদনের শেষ তারিখ:" : "Application Deadline:"}</span>
              </span>
              <div className="text-sm font-bold text-slate-900 dark:text-white font-bengali mt-0.5">
                {isBengali ? job.deadline : (job.deadlineEn || job.deadline)}
              </div>
            </div>
          </div>

          {/* Educational Requirements */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-[#0A2540] dark:text-white flex items-center gap-2 font-bengali border-b border-slate-200 dark:border-slate-800 pb-2">
              <GraduationCap className="w-4 h-4 text-[#0A2540] dark:text-amber-300" />
              <span>{isBengali ? "শিক্ষাগত যোগ্যতা ও প্রয়োজনীয় ডিগ্রি" : "Educational Requirements & Degrees"}</span>
            </h3>
            <ul className="space-y-2">
              {(isBengali ? job.educationRequirements : (job.educationRequirementsEn || job.educationRequirements)).map((req, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-700 dark:text-slate-300 font-bengali leading-relaxed">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>{req}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Key Responsibilities */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-[#0A2540] dark:text-white flex items-center gap-2 font-bengali border-b border-slate-200 dark:border-slate-800 pb-2">
              <Briefcase className="w-4 h-4 text-[#0A2540] dark:text-amber-300" />
              <span>{isBengali ? "দায়িত্ব ও কাজের পরিধি (Responsibilities)" : "Key Responsibilities & Scope"}</span>
            </h3>
            <ul className="space-y-2">
              {(isBengali ? job.responsibilities : (job.responsibilitiesEn || job.responsibilities)).map((resp, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-700 dark:text-slate-300 font-bengali leading-relaxed">
                  <div className="w-1.5 h-1.5 rounded-full bg-[#0A2540] dark:bg-amber-400 shrink-0 mt-1.5" />
                  <span>{resp}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Compensation & Other Benefits */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-[#0A2540] dark:text-white flex items-center gap-2 font-bengali border-b border-slate-200 dark:border-slate-800 pb-2">
              <Award className="w-4 h-4 text-[#0A2540] dark:text-amber-300" />
              <span>{isBengali ? "সুবিধাসমূহ ও অন্যান্য সুযোগ-সুবিধা" : "Compensation & Other Benefits"}</span>
            </h3>
            <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {(isBengali ? job.benefits : (job.benefitsEn || job.benefits)).map((benefit, idx) => (
                <li key={idx} className="p-2.5 rounded-xl bg-[#FAFAF8] dark:bg-slate-950/40 border border-slate-200 dark:border-slate-800 text-xs text-slate-700 dark:text-slate-300 font-bengali flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>{benefit}</span>
                </li>
              ))}
            </ul>
          </div>

        </div>

        {/* Modal Sticky Bottom Action Footer */}
        <div className="p-4 sm:p-5 border-t border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 flex items-center justify-between gap-4">
          <div className="text-xs text-slate-500 font-bengali flex items-center gap-1.5">
            <Users className="w-3.5 h-3.5 text-slate-400" />
            <span>
              {isBengali
                ? `মোট ${job.applicantsCount} জন প্রার্থী আবেদন করেছেন`
                : `Total ${job.applicantsCount} candidates applied`}
            </span>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-2xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 text-slate-700 dark:text-slate-300 text-xs font-bold font-bengali transition cursor-pointer"
            >
              {isBengali ? "বন্ধ করুন" : "Close"}
            </button>

            <button
              onClick={() => {
                onClose();
                onOpenApply(job);
              }}
              className="px-6 py-2.5 rounded-2xl bg-[#0A2540] hover:bg-[#081c30] text-white font-bold font-bengali text-xs shadow-[0_4px_0_0_#071D33] active:translate-y-1 active:shadow-none transition flex items-center gap-2 cursor-pointer"
            >
              <Send className="w-3.5 h-3.5 text-amber-300" />
              <span>{isBengali ? "অনলাইনে আবেদন করুন (Apply Online)" : "Apply Online"}</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};
