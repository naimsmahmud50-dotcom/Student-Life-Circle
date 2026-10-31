/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: CareerJobBoard.tsx
 * PURPOSE:   Bdjobs-Style Live Job Feed with Atmospheric Elevation, Tactile Cards & Modal Triggers
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
  GraduationCap,
  ArrowUpDown
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
    <div className="relative overflow-hidden rounded-3xl border border-slate-200/80 dark:border-[#262D3D] bg-[#FAFBFD]/90 dark:bg-[#0A1220]/90 p-6 sm:p-8 shadow-xs space-y-6">
      
      {/* Oxford Navy Atmospheric Glow Stop */}
      <div
        className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
        style={{
          height: '100%',
          minHeight: '260px',
          background:
            'radial-gradient(ellipse 65% 90% at 30% 100%, rgba(10, 37, 64, 0.12) 0%, rgba(10, 37, 64, 0.03) 45%, transparent 100%)'
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
              'linear-gradient(to bottom, rgba(10, 37, 64, 0.16) 15%, rgba(10, 37, 64, 0.01) 100%)'
          }}
        >
          VACANCIES
        </p>
      </div>

      {/* Feed Control Bar */}
      <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200/60 dark:border-slate-800 pb-4">
        <div className="flex items-center gap-2.5">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-white dark:bg-[#121B2D] text-[#0A2540] dark:text-blue-300 border border-slate-200 dark:border-slate-800 shadow-xs font-bengali">
            <Briefcase className="w-3.5 h-3.5 mr-1.5 text-[#ED8E22]" />
            লাইভ জব ফিড
          </span>
          <span className="text-xs sm:text-sm font-bold text-slate-700 dark:text-slate-300 font-bengali">
            মোট <strong className="text-slate-900 dark:text-white font-mono">{filteredJobs.length}</strong> টি সার্কুলার পাওয়া গেছে
          </span>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-500 font-bengali flex items-center gap-1">
            <ArrowUpDown className="w-3.5 h-3.5" />
            <span>সাজান:</span>
          </span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-3.5 py-1.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-xs font-bengali text-slate-800 dark:text-slate-200 focus:outline-none cursor-pointer shadow-xs transition"
          >
            <option value="recent">জনপ্রিয়তা ও আবেদন সংখ্যা</option>
            <option value="deadline">আবেদনের শেষ তারিখ (নিকটবর্তী)</option>
            <option value="salary">সর্বোচ্চ মাসিক বেতন</option>
          </select>
        </div>
      </div>

      {/* Jobs Feed List */}
      <div className="relative z-10">
        {filteredJobs.length === 0 ? (
          <div className="rounded-3xl border-2 border-dashed border-slate-300 dark:border-slate-800 p-8 sm:p-12 text-center space-y-4 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xs">
            <div className="w-14 h-14 rounded-2xl bg-amber-50 dark:bg-amber-950/40 text-amber-600 flex items-center justify-center mx-auto border border-amber-200/60">
              <AlertCircle className="w-7 h-7" />
            </div>
            <div className="space-y-1">
              <h3 className="text-base font-bold text-slate-900 dark:text-white font-bengali">
                কোনো চাকরির বিজ্ঞপ্তি পাওয়া যায়নি
              </h3>
              <p className="text-xs text-slate-500 font-bengali max-w-sm mx-auto leading-relaxed">
                আপনার দেওয়া ফিল্টার বা সার্চ শব্দের সাথে মিল পাওয়া যায়নি। ফিল্টার রিসেট করে পুনরায় অনুসন্ধান করুন।
              </p>
            </div>
            <button
              onClick={onClearFilters}
              className="px-5 py-2.5 rounded-2xl bg-[#0A2540] hover:bg-[#081c30] text-white text-xs font-bold font-bengali shadow-[0_4px_0_0_#071D33] active:translate-y-1 active:shadow-none transition flex items-center gap-1.5 mx-auto cursor-pointer"
            >
              <RotateCcw className="w-3.5 h-3.5 text-amber-300" />
              <span>ফিল্টার রিসেট করুন</span>
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredJobs.map((job) => (
              <div
                key={job.id}
                className="p-5 sm:p-6 rounded-3xl border border-slate-200/90 dark:border-[#232F45] bg-white/95 dark:bg-[#101A2C]/95 shadow-xs hover:border-amber-300 dark:hover:border-amber-500/50 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200 flex flex-col md:flex-row md:items-center justify-between gap-5 group"
              >
                
                {/* Left Column: Monogram & Job Identity */}
                <div className="flex items-start gap-4">
                  <div className={`w-13 h-13 sm:w-14 sm:h-14 rounded-2xl ${job.monogramBg} ${job.monogramText} flex items-center justify-center text-base sm:text-lg font-black shrink-0 shadow-xs border border-white/30 group-hover:scale-105 transition-transform`}>
                    {job.companyMonogram}
                  </div>

                  <div className="space-y-1.5">
                    <div className="flex flex-wrap items-center gap-1.5">
                      <span className="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                        {job.id}
                      </span>

                      {job.isHotJob && (
                        <span className="px-2.5 py-0.5 rounded-md text-[10px] font-bold bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300 border border-rose-200 dark:border-rose-800 flex items-center gap-1">
                          <Clock className="w-3 h-3 text-rose-600" />
                          হট জব
                        </span>
                      )}

                      {job.orgType === 'GOVT' && (
                        <span className="px-2.5 py-0.5 rounded-md text-[10px] font-bold bg-amber-50 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200 dark:border-amber-800 flex items-center gap-1">
                          <Building2 className="w-3 h-3 text-amber-600" />
                          সরকারি সার্কুলার
                        </span>
                      )}

                      {job.jobNature === 'INTERNSHIP' && (
                        <span className="px-2.5 py-0.5 rounded-md text-[10px] font-bold bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300 border border-blue-200 dark:border-blue-800 flex items-center gap-1">
                          <GraduationCap className="w-3 h-3 text-blue-600" />
                          ইন্টার্নশিপ
                        </span>
                      )}
                    </div>

                    <h3 
                      onClick={() => setActiveDetailJob(job)}
                      className="text-base sm:text-lg font-black text-slate-900 dark:text-white font-bengali group-hover:text-[#ED8E22] dark:group-hover:text-amber-300 transition-colors cursor-pointer"
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
                        <span>অভিজ্ঞতা: {job.experienceYears}</span>
                      </span>
                      <span>•</span>
                      <span className="flex items-center gap-1">
                        <Users className="w-3.5 h-3.5 text-slate-400" />
                        <span>{job.vacancy} টি পদ</span>
                      </span>
                      <span>•</span>
                      <span className="flex items-center gap-1 text-rose-700 dark:text-rose-400 font-medium">
                        <Clock className="w-3.5 h-3.5" />
                        <span>শেষ সময়: {job.deadline}</span>
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
                      className="px-3.5 py-2.5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 text-slate-700 dark:text-slate-300 text-xs font-bold font-bengali shadow-xs transition flex items-center gap-1.5 cursor-pointer"
                    >
                      <Eye className="w-3.5 h-3.5 text-slate-500" />
                      <span>বিস্তারিত</span>
                    </button>

                    <button
                      data-testid="apply-job-btn"
                      onClick={() => setActiveApplyJob(job)}
                      className="px-5 py-2.5 rounded-2xl bg-[#0A2540] hover:bg-[#081c30] text-white text-xs font-bold font-bengali shadow-[0_4px_0_0_#071D33] active:translate-y-1 active:shadow-none transition flex items-center gap-1.5 cursor-pointer"
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
      </div>

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
