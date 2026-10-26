/**
 * DEVELOPER ARCHITECTURE NOTE:
 * COMPONENT: EmployerJobPostingWizardModal.tsx
 * PURPOSE:   Bdjobs-Style 4-Step Job Posting Wizard for Corporate & Institution Recruiters
 * STANDARDS: Zero-Emoji, UI/UX Pro Max, Academic Oxford Navy, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { 
  X, 
  PlusCircle, 
  Building2, 
  Briefcase, 
  GraduationCap, 
  Banknote, 
  CheckCircle2, 
  ArrowRight, 
  ArrowLeft,
  Calendar,
  MapPin,
  ShieldCheck,
  Check
} from 'lucide-react';
import { CareerJob, CAREER_CATEGORIES } from './data/careerElevationData';

interface EmployerJobPostingWizardModalProps {
  isOpen: boolean;
  onClose: () => void;
  onJobCreated: (newJob: CareerJob) => void;
}

export const EmployerJobPostingWizardModal: React.FC<EmployerJobPostingWizardModalProps> = ({
  isOpen,
  onClose,
  onJobCreated
}) => {
  const [step, setStep] = useState<number>(1);
  const [isSuccess, setIsSuccess] = useState<boolean>(false);

  // Form State
  const [companyName, setCompanyName] = useState('');
  const [companyIndustry, setCompanyIndustry] = useState('Software & IT');
  const [locationDistrict, setLocationDistrict] = useState('ঢাকা মহানগর');
  const [jobTitle, setJobTitle] = useState('');
  const [category, setCategory] = useState('cat_it');
  const [jobNature, setJobNature] = useState<'FULL_TIME' | 'INTERNSHIP' | 'CONTRACTUAL'>('FULL_TIME');
  const [vacancy, setVacancy] = useState<number>(2);
  const [experienceYears, setExperienceYears] = useState('০ - ১ বছর');
  const [educationReq, setEducationReq] = useState('সিএসই বা সংশ্লিষ্ট বিষয়ে স্নাতক');
  const [responsibilitiesText, setResponsibilitiesText] = useState('এপিআই ডেভেলপমেন্ট ও ডাটাবেজ অপ্টিমাইজেশন');
  const [minSalary, setMinSalary] = useState<number>(35000);
  const [maxSalary, setMaxSalary] = useState<number>(50000);
  const [deadline, setDeadline] = useState('৩০ ডিসেম্বর ২০২৬');

  if (!isOpen) return null;

  const handleNext = () => {
    if (step < 4) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const handlePublish = (e: React.FormEvent) => {
    e.preventDefault();

    const createdJob: CareerJob = {
      id: `JOB-BD-2026-${Math.floor(100 + Math.random() * 900)}`,
      title: jobTitle || 'সফটওয়্যার ইঞ্জিনিয়ার',
      companyName: companyName || 'অগ্রযাত্রা পার্টনার এন্টারপ্রাইজ',
      companyMonogram: (companyName || 'OG').substring(0, 2).toUpperCase(),
      monogramBg: 'bg-[#0A2540]',
      monogramText: 'text-amber-300',
      companyIndustry,
      category,
      orgType: 'PRIVATE',
      jobNature,
      jobLevel: 'ENTRY',
      vacancy,
      locationDistrict,
      locationDivision: 'dhaka',
      minSalary,
      maxSalary,
      isSalaryNegotiable: false,
      deadline,
      deadlineIso: '2026-12-30T23:59:59Z',
      publishedDate: 'আজ প্রকাশিত',
      experienceYears,
      educationRequirements: [educationReq],
      responsibilities: responsibilitiesText.split('\n').filter(Boolean),
      benefits: ['উৎসব বোনাস', 'প্রভিডেন্ট ফান্ড', 'লাঞ্চ সুবিধা'],
      isHotJob: true,
      isEarlyAccess: false,
      applicantsCount: 0
    };

    onJobCreated(createdJob);
    setIsSuccess(true);
  };

  const handleClose = () => {
    setIsSuccess(false);
    setStep(1);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4">
      <div 
        className="relative w-full max-w-2xl rounded-3xl bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden my-6"
        role="dialog"
        aria-modal="true"
      >
        
        {/* Header */}
        <div className="p-6 border-b border-slate-200 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#0A2540] text-amber-300 flex items-center justify-center font-bold">
              <PlusCircle className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-black text-slate-900 dark:text-white font-bengali">
                পোস্ট এ জব (নিয়োগকর্তা ড্যাশবোর্ড)
              </h2>
              <p className="text-xs text-slate-500 font-bengali">
                ধাপ {step} এর ৪: {step === 1 ? 'কোম্পানি প্রোফাইল' : step === 2 ? 'পদের বিবরণ' : step === 3 ? 'যোগ্যতা ও দায়িত্ব' : 'বেতন ও প্রকাশনা'}
              </p>
            </div>
          </div>

          <button
            onClick={handleClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 dark:hover:text-white transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Step Indicator Bar */}
        <div className="grid grid-cols-4 border-b border-slate-200 dark:border-slate-800">
          {[1, 2, 3, 4].map((s) => (
            <div
              key={s}
              className={`h-1.5 transition-all ${
                s <= step ? 'bg-[#0A2540] dark:bg-amber-400' : 'bg-slate-100 dark:bg-slate-800'
              }`}
            />
          ))}
        </div>

        {isSuccess ? (
          <div className="p-8 sm:p-12 text-center space-y-4">
            <div className="w-16 h-16 rounded-full bg-emerald-100 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 flex items-center justify-center mx-auto border-2 border-emerald-300 dark:border-emerald-700">
              <Check className="w-8 h-8" />
            </div>
            <h3 className="text-xl font-black text-slate-900 dark:text-white font-bengali">
              চাকরির বিজ্ঞপ্তিটি সফলভাবে প্রকাশিত হয়েছে!
            </h3>
            <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 font-bengali max-w-md mx-auto">
              আপনার বিজ্ঞপ্তিটি অগ্রযাত্রা ও বিডিজবস-ক্লাস ক্যারিয়ার ফিডে লাইভ রয়েছে। প্রার্থীরা সিলগালা সিভি স্ন্যাপশটের মাধ্যমে আবেদন করতে পারবেন।
            </p>
            <button
              onClick={handleClose}
              className="mt-4 px-6 py-2.5 rounded-2xl bg-[#0A2540] text-white text-xs font-bold font-bengali cursor-pointer"
            >
              ফিডে ফিরে যান
            </button>
          </div>
        ) : (
          <div className="p-6 sm:p-7 space-y-5">
            
            {/* Step 1: Company Profile */}
            {step === 1 && (
              <div className="space-y-4">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    প্রতিষ্ঠানের নাম (Company Name):
                  </label>
                  <input
                    type="text"
                    required
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    placeholder="যেমন: ব্রেনস্টেশন ২৩ / ব্র্যাক"
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    শিল্প / সেক্টর (Industry):
                  </label>
                  <input
                    type="text"
                    value={companyIndustry}
                    onChange={(e) => setCompanyIndustry(e.target.value)}
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    কর্মস্থল / জেলা (Workplace District):
                  </label>
                  <input
                    type="text"
                    value={locationDistrict}
                    onChange={(e) => setLocationDistrict(e.target.value)}
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                  />
                </div>
              </div>
            )}

            {/* Step 2: Job Role Details */}
            {step === 2 && (
              <div className="space-y-4">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    চাকরির পদবি (Job Title):
                  </label>
                  <input
                    type="text"
                    required
                    value={jobTitle}
                    onChange={(e) => setJobTitle(e.target.value)}
                    placeholder="যেমন: জুনিয়র পাইথন ডেভেলপার"
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">ক্যাটাগরি:</label>
                    <select
                      value={category}
                      onChange={(e) => setCategory(e.target.value)}
                      className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                    >
                      {CAREER_CATEGORIES.map((c) => (
                        <option key={c.id} value={c.id}>{c.nameBn}</option>
                      ))}
                    </select>
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">খালি পদ সংখ্যা:</label>
                    <input
                      type="number"
                      value={vacancy}
                      onChange={(e) => setVacancy(Number(e.target.value))}
                      className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs text-slate-900 dark:text-white"
                    />
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">কাজের ধরন:</label>
                  <div className="flex gap-2">
                    {[
                      { id: 'FULL_TIME', label: 'ফুল-টাইম' },
                      { id: 'INTERNSHIP', label: 'ইন্টার্নশিপ' },
                      { id: 'CONTRACTUAL', label: 'চুক্তিভিত্তিক' }
                    ].map((n) => (
                      <button
                        type="button"
                        key={n.id}
                        onClick={() => setJobNature(n.id as any)}
                        className={`px-3 py-1.5 rounded-xl text-xs font-bengali font-bold border transition ${
                          jobNature === n.id
                            ? 'bg-[#0A2540] text-white border-[#0A2540]'
                            : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700'
                        }`}
                      >
                        {n.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Step 3: Criteria & Requirements */}
            {step === 3 && (
              <div className="space-y-4">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    অভিজ্ঞতার প্রয়োজনীয়তা:
                  </label>
                  <input
                    type="text"
                    value={experienceYears}
                    onChange={(e) => setExperienceYears(e.target.value)}
                    placeholder="যেমন: ০ - ১ বছর (ফ্রেশার স্বাগতম)"
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    শিক্ষাগত যোগ্যতা:
                  </label>
                  <input
                    type="text"
                    value={educationReq}
                    onChange={(e) => setEducationReq(e.target.value)}
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                  />
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    দায়িত্বসমূহ (লাইন ব্রেক দিয়ে লিখুন):
                  </label>
                  <textarea
                    rows={3}
                    value={responsibilitiesText}
                    onChange={(e) => setResponsibilitiesText(e.target.value)}
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                  />
                </div>
              </div>
            )}

            {/* Step 4: Compensation & Finalize */}
            {step === 4 && (
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">সর্বনিম্ন বেতন (টাকা):</label>
                    <input
                      type="number"
                      value={minSalary}
                      onChange={(e) => setMinSalary(Number(e.target.value))}
                      className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs text-slate-900 dark:text-white"
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">সর্বোচ্চ বেতন (টাকা):</label>
                    <input
                      type="number"
                      value={maxSalary}
                      onChange={(e) => setMaxSalary(Number(e.target.value))}
                      className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs text-slate-900 dark:text-white"
                    />
                  </div>
                </div>

                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-700 dark:text-slate-300 font-bengali">
                    আবেদনের শেষ তারিখ:
                  </label>
                  <input
                    type="text"
                    value={deadline}
                    onChange={(e) => setDeadline(e.target.value)}
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-[#FAFAF8] dark:bg-slate-950 text-xs font-bengali text-slate-900 dark:text-white"
                  />
                </div>

                <div className="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 text-xs text-slate-600 dark:text-slate-300 font-bengali flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>অগ্রযাত্রা ভেরিফায়েড নিয়োগকর্তা চুক্তি ও স্বচ্ছতা পলিসি প্রযোজ্য হবে।</span>
                </div>
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="pt-4 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={handleBack}
                  className="px-4 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-xs font-bold font-bengali text-slate-700 dark:text-slate-300 flex items-center gap-1.5 cursor-pointer"
                >
                  <ArrowLeft className="w-3.5 h-3.5" />
                  <span>পূর্ববর্তী</span>
                </button>
              ) : <div />}

              {step < 4 ? (
                <button
                  type="button"
                  onClick={handleNext}
                  className="px-5 py-2.5 rounded-xl bg-[#0A2540] text-white text-xs font-bold font-bengali flex items-center gap-1.5 cursor-pointer"
                >
                  <span>পরবর্তী ধাপ</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handlePublish}
                  className="px-6 py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold font-bengali shadow-sm flex items-center gap-1.5 cursor-pointer"
                >
                  <Check className="w-4 h-4" />
                  <span>বিজ্ঞপ্তিটি এখনই প্রকাশ করুন</span>
                </button>
              )}
            </div>

          </div>
        )}

      </div>
    </div>
  );
};
