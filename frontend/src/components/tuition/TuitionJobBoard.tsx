/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Tuition Job Board
 * TOPIC:     CareTutors-Style Filterable Job Board for Tutors
 * FILE:      frontend/src/components/tuition/TuitionJobBoard.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, High Contrast, Tactile Buttons, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { TuitionJob, TUITION_JOBS } from './data/tuitionElevationData';
import {
  Search,
  Filter,
  MapPin,
  Calendar,
  CreditCard,
  UserCheck,
  CheckCircle2,
  Users,
  Clock,
  Send,
  X,
  ShieldCheck,
  Briefcase,
  AlertCircle,
  Lock,
} from 'lucide-react';

interface TuitionJobBoardProps {
  className?: string;
  initialCategory?: string;
  onRequestTutorClick?: () => void;
}

export const TuitionJobBoard: React.FC<TuitionJobBoardProps> = ({
  className = '',
  initialCategory = 'all',
  onRequestTutorClick,
}) => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedDistrict, setSelectedDistrict] = useState<string>('ALL');
  const [selectedCategory, setSelectedCategory] = useState<string>(initialCategory);
  const [selectedMode, setSelectedMode] = useState<string>('ALL');

  // Apply Modal state
  const [applyingJob, setApplyingJob] = useState<TuitionJob | null>(null);
  const [coverNote, setCoverNote] = useState<string>('');
  const [tutorPhone, setTutorPhone] = useState<string>('');
  const [appliedJobs, setAppliedJobs] = useState<string[]>([]);
  const [applySuccessMessage, setApplySuccessMessage] = useState<string | null>(null);

  const filteredJobs = TUITION_JOBS.filter((job) => {
    const matchesSearch =
      searchQuery === '' ||
      job.titleBn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.subjectsBn.some((s) => s.toLowerCase().includes(searchQuery.toLowerCase())) ||
      job.areaBn.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.thana.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesDistrict = selectedDistrict === 'ALL' || job.district === selectedDistrict;
    const matchesCategory = selectedCategory === 'all' || job.category === selectedCategory;
    const matchesMode = selectedMode === 'ALL' || job.mode === selectedMode;

    return matchesSearch && matchesDistrict && matchesCategory && matchesMode;
  });

  const handleApplySubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!applyingJob) return;

    setAppliedJobs([...appliedJobs, applyingJob.id]);
    setApplySuccessMessage(`দ্বিপাক্ষিক সম্মতির অনুরোধ সফলভাবে পাঠানো হয়েছে। অভিভাবক জব ${applyingJob.id}-এ সম্মতি দিলে সরাসরি যোগাযোগ উন্মুক্ত হবে।`);

    setTimeout(() => {
      setApplySuccessMessage(null);
      setApplyingJob(null);
      setCoverNote('');
      setTutorPhone('');
    }, 2500);
  };

  return (
    <div className={`space-y-6 ${className}`} aria-labelledby="job-board-heading">
      {/* Search & Filter Bar */}
      <div className="p-4 sm:p-5 rounded-3xl border border-amber-200/70 dark:border-[#262D3D] bg-white dark:bg-[#121B2D] shadow-xs space-y-3 font-bengali">
        <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
          <div className="relative w-full sm:w-80">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="বিষয়, শ্রেণি বা এলাকা দিয়ে খুঁজুন..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs text-slate-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#0A2540]"
            />
          </div>

          <div className="flex flex-wrap gap-2 w-full sm:w-auto items-center">
            {/* District Filter */}
            <select
              value={selectedDistrict}
              onChange={(e) => setSelectedDistrict(e.target.value)}
              aria-label="জেলা নির্বাচন করুন"
              className="flex-1 sm:flex-initial p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
            >
              <option value="ALL">সকল জেলা</option>
              <option value="ঢাকা">ঢাকা</option>
              <option value="চট্টগ্রাম">চট্টগ্রাম</option>
              <option value="রাজশাহী">রাজশাহী</option>
            </select>

            {/* Mode Filter */}
            <select
              value={selectedMode}
              onChange={(e) => setSelectedMode(e.target.value)}
              aria-label="টিউশন মোড নির্বাচন করুন"
              className="flex-1 sm:flex-initial p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
            >
              <option value="ALL">সকল মোড</option>
              <option value="হোম টিউশন">হোম টিউশন</option>
              <option value="অনলাইন টিউশন">অনলাইন টিউশন</option>
            </select>

            {onRequestTutorClick && (
              <button
                onClick={onRequestTutorClick}
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-emerald-800 hover:bg-emerald-900 active:bg-emerald-950 text-white font-bold text-xs shadow-sm transition-all whitespace-nowrap cursor-pointer"
              >
                + রিকোয়ারমেন্ট পোস্ট করুন
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Jobs Listing Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredJobs.length > 0 ? (
          filteredJobs.map((job) => {
            const isApplied = appliedJobs.includes(job.id);
            return (
              <article
                key={job.id}
                className="flex flex-col justify-between bg-white dark:bg-[#121B2D] rounded-3xl border border-amber-200/70 dark:border-[#262D3D] p-5 sm:p-6 shadow-xs hover:border-[#ED8E22]/60 hover:shadow-md transition-all duration-200 space-y-4"
              >
                <div className="space-y-3 font-bengali">
                  {/* Top Bar: Job ID, Status & Date */}
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-mono font-bold text-slate-700 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 px-2.5 py-0.5 rounded-md border border-slate-200 dark:border-slate-700">
                      {job.id}
                    </span>
                    <span
                      className={`font-semibold px-2 py-0.5 rounded-full text-[11px] ${
                        job.status === 'open'
                          ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                          : job.status === 'shortlisting'
                          ? 'bg-amber-100 text-amber-800 border border-amber-300'
                          : 'bg-slate-100 text-slate-600 border border-slate-300'
                      }`}
                    >
                      {job.status === 'open' ? 'আবেদন চলছে' : job.status === 'shortlisting' ? 'বাছাই চলছে' : 'নিশ্চিতকৃত'}
                    </span>
                  </div>

                  {/* Title & Grade */}
                  <div>
                    <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white leading-snug">
                      {job.titleBn}
                    </h3>
                    <div className="text-xs font-semibold text-emerald-800 dark:text-emerald-400 mt-0.5">
                      {job.classGradeBn}
                    </div>
                  </div>

                  {/* Subjects Badges */}
                  <div className="flex flex-wrap gap-1.5 pt-1">
                    {job.subjectsBn.map((sub, idx) => (
                      <span
                        key={idx}
                        className="text-[11px] font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 px-2 py-0.5 rounded-md border border-slate-200 dark:border-slate-700"
                      >
                        {sub}
                      </span>
                    ))}
                  </div>

                  {/* Location & Days Matrix */}
                  <div className="p-3.5 rounded-2xl bg-[#FAF8F3] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 text-xs space-y-1.5">
                    <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-400">
                      <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span className="truncate">{job.areaBn}, {job.district} ({job.mode})</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-400">
                      <Calendar className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span>সপ্তাহে {job.daysPerWeek} দিন</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-400">
                      <UserCheck className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                      <span>{job.genderPreferenceBn}</span>
                    </div>
                  </div>

                  {/* Tutor Requirement Note */}
                  <p className="text-xs text-slate-600 dark:text-slate-400 italic line-clamp-2">
                    &ldquo;{job.tutorRequirementBn}&rdquo;
                  </p>

                  {/* Masked Contact Shield */}
                  <div className="flex items-center justify-between text-xs pt-2 border-t border-slate-100 dark:border-slate-800">
                    <span className="text-slate-500 font-bengali">যোগাযোগ:</span>
                    <span className="font-mono text-slate-700 dark:text-slate-300 font-bold">
                      ০১৭*** (দ্বিপাক্ষিক লক)
                    </span>
                  </div>
                </div>

                {/* Footer: Salary & Action Button */}
                <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 font-bengali">
                  <div>
                    <div className="text-[11px] text-slate-500 font-medium">মাসিক পারিশ্রমিক</div>
                    <div className="text-sm font-bold font-mono text-emerald-800 dark:text-emerald-400 leading-tight">
                      {job.salaryBn}
                    </div>
                  </div>

                  {isApplied ? (
                    <span className="inline-flex items-center justify-center gap-1 text-xs font-bold text-emerald-700 bg-emerald-50 px-4 py-3 rounded-2xl border border-emerald-200">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>আবেদনকৃত</span>
                    </span>
                  ) : (
                    <button
                      onClick={() => setApplyingJob(job)}
                      disabled={job.status === 'confirmed'}
                      aria-label="দ্বিপাক্ষিক সম্মতির আবেদন করুন"
                      className="w-full sm:w-auto px-5 py-3 rounded-2xl bg-[#0A2540] hover:bg-[#081c30] text-white text-xs font-bold transition-all shadow-[0_3px_0_0_#071D33] active:translate-y-0.5 active:shadow-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0A2540] disabled:opacity-50 cursor-pointer flex items-center justify-center gap-1.5"
                    >
                      <Lock className="w-3.5 h-3.5 text-amber-300 shrink-0" />
                      <span>দ্বিপাক্ষিক সম্মতির আবেদন করুন</span>
                    </button>
                  )}
                </div>
              </article>
            );
          })
        ) : (
          <div className="col-span-full py-12 text-center bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 font-bengali">
            <Briefcase className="w-10 h-10 text-slate-300 mx-auto mb-3" />
            <h4 className="text-base font-bold text-slate-800 dark:text-white">
              এই ফিল্টারে কোনো টিউশন জব খুঁজে পাওয়া যায়নি
            </h4>
            <p className="text-xs text-slate-500 mt-1">
              অন্য কোনো জেলা বা বিষয় নির্বাচন করে পুনরায় চেষ্টা করুন।
            </p>
          </div>
        )}
      </div>

      {/* Apply Modal */}
      {applyingJob && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="apply-modal-title"
          className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/70 backdrop-blur-xs animate-in fade-in duration-150"
        >
          <div className="relative w-full max-w-lg bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl p-6 font-bengali space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <div>
                <span className="text-[11px] font-mono font-bold text-slate-500">{applyingJob.id}</span>
                <h3 id="apply-modal-title" className="text-base font-bold text-slate-900 dark:text-white">
                  দ্বিপাক্ষিক যোগাযোগ সম্মতি
                </h3>
              </div>
              <button
                onClick={() => setApplyingJob(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {applySuccessMessage ? (
              <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-300 text-emerald-800 text-xs font-bold text-center">
                {applySuccessMessage}
              </div>
            ) : (
              <form onSubmit={handleApplySubmit} className="space-y-4 text-xs">
                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-1">
                  <div className="font-bold text-slate-800 dark:text-white">{applyingJob.titleBn}</div>
                  <div className="text-slate-500">পারিশ্রমিক: <strong className="text-emerald-700">{applyingJob.salaryBn}</strong> | এলাকা: {applyingJob.areaBn}</div>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                    আপনার মোবাইল নম্বর (ভেরিফায়েড অ্যাকাউন্ট):
                  </label>
                  <input
                    type="tel"
                    value={tutorPhone}
                    onChange={(e) => setTutorPhone(e.target.value)}
                    placeholder="০১৭১১******"
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white font-mono"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                    অভিভাবকের উদ্দেশ্যে সংক্ষিপ্ত বার্তা / অভিজ্ঞতা:
                  </label>
                  <textarea
                    rows={3}
                    value={coverNote}
                    onChange={(e) => setCoverNote(e.target.value)}
                    placeholder="আপনার বিশ্ববিদ্যালয়, বিভাগ এবং এই বিষয়ে পূর্বে পড়ানোর অভিজ্ঞতা লিখুন..."
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white"
                  />
                </div>

                <div className="p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-amber-800 dark:text-amber-300 text-xs flex items-start gap-2.5">
                  <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-amber-600" />
                  <div>
                    <span className="font-semibold block mb-0.5">দ্বিপাক্ষিক অনুমোদন নীতি:</span>
                    গোপনীয়তা নীতিমালার আওতায় উভয় পক্ষ সম্মতি প্রদান না করা পর্যন্ত সরাসরি ফোন নম্বর উন্মুক্ত হয় না। ২ দিনের ফ্রি ট্রায়াল ক্লাসে সম্মত থাকতে হবে।
                  </div>
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setApplyingJob(null)}
                    className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold"
                  >
                    বাতিল
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-2.5 rounded-2xl bg-[#0A2540] hover:bg-[#081c30] text-white font-bold flex items-center gap-1.5 cursor-pointer shadow-sm"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>সম্মতি নিশ্চিত করুন</span>
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
