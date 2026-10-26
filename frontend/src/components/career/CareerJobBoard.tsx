/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: CareerJobBoard.tsx
 * PURPOSE:   Bdjobs-Style Live Job Feed with Filter Evaluation, Responsive Cards & Modal Triggers
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, WCAG 2.2 AAA
 */

import React, { useState, useMemo } from 'react';
import { 
  Building2, 
  MapPin, 
  Briefcase, 
  Clock, 
  Banknote, 
  Send, 
  Eye, 
  Sparkles,
  Users,
  AlertCircle,
  RotateCcw,
  GraduationCap
} from 'lucide-react';
import { CareerJob, VERIFIED_CAREER_JOBS } from './data/careerElevationData';
import { JobDetailModal } from './JobDetailModal';
import { JobApplyModal } from './JobApplyModal';

interface CareerJobBoardProps {
  searchQuery: string;
  selectedDivision: string;
  selectedCategory: string;
  selectedJobNature: string;
  selectedOrgType: string;
  isHotJobOnly: boolean;
  onClearFilters: () => void;
  sealedSnapshotHash: string;
  onApplicationSubmitted: (app: any) => void;
}

export const CareerJobBoard: React.FC<CareerJobBoardProps> = ({
  searchQuery,
  selectedDivision,
  selectedCategory,
  selectedJobNature,
  selectedOrgType,
  isHotJobOnly,
  onClearFilters,
  sealedSnapshotHash,
  onApplicationSubmitted
}) => {
  const [activeDetailJob, setActiveDetailJob] = useState<CareerJob | null>(null);
  const [activeApplyJob, setActiveApplyJob] = useState<CareerJob | null>(null);
  const [sortBy, setSortBy] = useState<'deadline' | 'salary' | 'recent'>('recent');

  // Filter & Sort Logic
  const filteredJobs = useMemo(() => {
    return VERIFIED_CAREER_JOBS.filter(job => {
      // Keyword matching
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase();
        const matchesTitle = job.title.toLowerCase().includes(query);
        const matchesCompany = job.companyName.toLowerCase().includes(query);
        const matchesIndustry = job.companyIndustry.toLowerCase().includes(query);
        const matchesReqs = job.educationRequirements.some(r => r.toLowerCase().includes(query));
        if (!matchesTitle && !matchesCompany && !matchesIndustry && !matchesReqs) return false;
      }

      // Division
      if (selectedDivision !== 'all') {
        if (job.locationDivision !== selectedDivision) return false;
      }

      // Category
      if (selectedCategory !== 'all') {
        if (job.category !== selectedCategory) return false;
      }

      // Job Nature
      if (selectedJobNature !== 'all') {
        if (job.jobNature !== selectedJobNature) return false;
      }

      // Org Type
      if (selectedOrgType !== 'all') {
        if (job.orgType !== selectedOrgType) return false;
      }

      // Hot Job
      if (isHotJobOnly) {
        if (!job.isHotJob) return false;
      }

      return true;
    }).sort((a, b) => {
      if (sortBy === 'deadline') {
        return new Date(a.deadlineIso).getTime() - new Date(b.deadlineIso).getTime();
      }
      if (sortBy === 'salary') {
        return b.maxSalary - a.maxSalary;
      }
      return b.applicantsCount - a.applicantsCount;
    });
  }, [searchQuery, selectedDivision, selectedCategory, selectedJobNature, selectedOrgType, isHotJobOnly, sortBy]);

  return (
    <div className="space-y-4">
      
      {/* Feed Control Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 px-2">
        <div className="text-xs sm:text-sm font-bold text-slate-700 dark:text-slate-300 font-bengali flex items-center gap-2">
          <Briefcase className="w-4 h-4 text-[#0A2540] dark:text-amber-300" />
          <span>মোট {filteredJobs.length} টি চাকরির বিজ্ঞপ্তি পাওয়া গেছে</span>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 font-bengali">সাজান:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-3 py-1.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-xs font-bengali text-slate-800 dark:text-slate-200 focus:outline-none cursor-pointer"
          >
            <option value="recent">জনপ্রিয়তা ও আবেদন সংখ্যা</option>
            <option value="deadline">আবেদনের শেষ তারিখ (নিকটবর্তী)</option>
            <option value="salary">সর্বোচ্চ মাসিক বেতন</option>
          </select>
        </div>
      </div>

      {/* Jobs Feed List */}
      {filteredJobs.length === 0 ? (
        <div className="rounded-3xl border-2 border-dashed border-slate-300 dark:border-slate-800 p-8 sm:p-12 text-center space-y-4 bg-white dark:bg-slate-900">
          <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 flex items-center justify-center mx-auto">
            <AlertCircle className="w-6 h-6" />
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-bold text-slate-900 dark:text-white font-bengali">
              কোনো চাকরির বিজ্ঞপ্তি পাওয়া যায়নি
            </h3>
            <p className="text-xs text-slate-500 font-bengali max-w-sm mx-auto">
              আপনার ফিল্টার মানদণ্ড পরিবর্তন করে অথবা রিসেট করে পুনরায় চেষ্টা করুন।
            </p>
          </div>
          <button
            onClick={onClearFilters}
            className="px-4 py-2 rounded-xl bg-[#0A2540] text-white text-xs font-bold font-bengali flex items-center gap-1.5 mx-auto cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>ফিল্টার রিসেট করুন</span>
          </button>
        </div>
      ) : (
        <div className="space-y-3.5">
          {filteredJobs.map((job) => (
            <div
              key={job.id}
              className="p-5 sm:p-6 rounded-3xl border-2 border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs hover:border-slate-300 dark:hover:border-slate-700 transition flex flex-col md:flex-row md:items-center justify-between gap-5"
            >
              
              {/* Left Column: Monogram & Job Identity */}
              <div className="flex items-start gap-4">
                <div className={`w-12 h-12 sm:w-14 sm:h-14 rounded-2xl ${job.monogramBg} ${job.monogramText} flex items-center justify-center text-base sm:text-lg font-black shrink-0 shadow-xs border border-white/20`}>
                  {job.companyMonogram}
                </div>

                <div className="space-y-1.5">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                      {job.id}
                    </span>

                    {job.isHotJob && (
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 border border-rose-200 dark:border-rose-800">
                        হট জব
                      </span>
                    )}

                    {job.orgType === 'GOVT' && (
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-amber-50 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
                        সরকারি
                      </span>
                    )}

                    {job.jobNature === 'INTERNSHIP' && (
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-bold bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
                        ইন্টার্নশিপ
                      </span>
                    )}
                  </div>

                  <h3 
                    onClick={() => setActiveDetailJob(job)}
                    className="text-base sm:text-lg font-black text-slate-900 dark:text-white font-bengali hover:text-[#0A2540] dark:hover:text-amber-300 transition-colors cursor-pointer"
                  >
                    {job.title}
                  </h3>

                  <p className="text-xs sm:text-sm font-semibold text-slate-700 dark:text-slate-300 flex flex-wrap items-center gap-2 font-bengali">
                    <span>{job.companyName}</span>
                    <span className="text-slate-400">•</span>
                    <span className="text-slate-500 font-normal flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" />
                      {job.locationDistrict}
                    </span>
                  </p>

                  {/* Metadata Chips */}
                  <div className="flex flex-wrap items-center gap-3 pt-1 text-xs text-slate-500 font-bengali">
                    <span className="flex items-center gap-1">
                      <Briefcase className="w-3.5 h-3.5 text-slate-400" />
                      <span>{job.experienceYears}</span>
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Users className="w-3.5 h-3.5 text-slate-400" />
                      <span>{job.vacancy} টি শূন্যপদ</span>
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1 text-rose-700 dark:text-rose-400 font-medium">
                      <Clock className="w-3.5 h-3.5" />
                      <span>শেষ তারিখ: {job.deadline}</span>
                    </span>
                  </div>
                </div>
              </div>

              {/* Right Column: Salary & CTAs */}
              <div className="flex md:flex-col items-center md:items-end justify-between md:justify-center gap-3 pt-3 md:pt-0 border-t md:border-t-0 border-slate-100 dark:border-slate-800 shrink-0">
                <div className="text-left md:text-right">
                  <div className="text-xs text-slate-500 font-bengali">মাসিক বেতন:</div>
                  <div className="text-sm sm:text-base font-black text-emerald-700 dark:text-emerald-400 font-bengali">
                    {job.minSalary.toLocaleString('bn-BD')} - {job.maxSalary.toLocaleString('bn-BD')} ৳
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    data-testid="detail-job-btn"
                    onClick={() => setActiveDetailJob(job)}
                    className="px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 text-slate-700 dark:text-slate-300 text-xs font-bold font-bengali transition flex items-center gap-1 cursor-pointer"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    <span>বিস্তারিত</span>
                  </button>

                  <button
                    data-testid="apply-job-btn"
                    onClick={() => setActiveApplyJob(job)}
                    className="px-4 py-2 rounded-xl bg-[#0A2540] hover:bg-[#081c30] text-white text-xs font-bold font-bengali shadow-sm active:translate-y-0.5 transition flex items-center gap-1 cursor-pointer"
                  >
                    <Send className="w-3.5 h-3.5 text-amber-300" />
                    <span>আবেদন</span>
                  </button>
                </div>
              </div>

            </div>
          ))}
        </div>
      )}

      {/* Modals */}
      <JobDetailModal
        job={activeDetailJob}
        isOpen={Boolean(activeDetailJob)}
        onClose={() => setActiveDetailJob(null)}
        onOpenApply={(job) => setActiveApplyJob(job)}
      />

      <JobApplyModal
        job={activeApplyJob}
        isOpen={Boolean(activeApplyJob)}
        onClose={() => setActiveApplyJob(null)}
        sealedSnapshotHash={sealedSnapshotHash}
        onApplicationSubmitted={onApplicationSubmitted}
      />

    </div>
  );
};
