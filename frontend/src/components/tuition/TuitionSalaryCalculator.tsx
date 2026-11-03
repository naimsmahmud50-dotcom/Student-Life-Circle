/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Interactive Tuition Salary Calculator
 * TOPIC:     CareTutors-Style Market Salary Guide & Estimation Tool
 * FILE:      frontend/src/components/tuition/TuitionSalaryCalculator.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, Deterministic Salary Estimation, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { useTranslation } from '../../lib/i18n';
import { Calculator, Sparkles, MapPin, Calendar, BookOpen, ArrowRight, ShieldCheck } from 'lucide-react';

interface TuitionSalaryCalculatorProps {
  className?: string;
  onRequestTutorWithSalary?: (salaryText: string) => void;
}

export const TuitionSalaryCalculator: React.FC<TuitionSalaryCalculatorProps> = ({
  className = '',
  onRequestTutorWithSalary,
}) => {
  const { isBengali } = useTranslation();
  const [district, setDistrict] = useState<string>('ঢাকা');
  const [medium, setMedium] = useState<string>('বাংলা মাধ্যম');
  const [classGroup, setClassGroup] = useState<string>('secondary_ssc');
  const [daysPerWeek, setDaysPerWeek] = useState<number>(3);

  // Compute recommended salary
  const calculateSalary = () => {
    let baseMin = 5000;
    let baseMax = 7000;

    // Class group weight
    if (classGroup === 'primary') {
      baseMin = 4000;
      baseMax = 5500;
    } else if (classGroup === 'lower_secondary') {
      baseMin = 5500;
      baseMax = 7500;
    } else if (classGroup === 'secondary_ssc') {
      baseMin = 7500;
      baseMax = 10000;
    } else if (classGroup === 'higher_hsc') {
      baseMin = 9000;
      baseMax = 12500;
    } else if (classGroup === 'admission') {
      baseMin = 11000;
      baseMax = 16000;
    }

    // Medium multiplier
    if (medium === 'ইংলিশ ভার্সন') {
      baseMin = Math.round(baseMin * 1.25);
      baseMax = Math.round(baseMax * 1.25);
    } else if (medium === 'ইংলিশ মিডিয়াম') {
      baseMin = Math.round(baseMin * 1.6);
      baseMax = Math.round(baseMax * 1.65);
    }

    // District adjustment
    if (district !== 'ঢাকা') {
      baseMin = Math.round(baseMin * 0.8);
      baseMax = Math.round(baseMax * 0.85);
    }

    // Days multiplier relative to 3 days base
    const dayFactor = daysPerWeek / 3;
    const finalMin = Math.round((baseMin * dayFactor) / 500) * 500;
    const finalMax = Math.round((baseMax * dayFactor) / 500) * 500;

    return {
      min: finalMin,
      max: finalMax,
      minBn: finalMin.toLocaleString('bn-BD'),
      maxBn: finalMax.toLocaleString('bn-BD'),
      perClassBn: Math.round(finalMin / (daysPerWeek * 4)).toLocaleString('bn-BD'),
    };
  };

  const salary = calculateSalary();
  const formattedSalaryText = isBengali
    ? `${salary.minBn} - ${salary.maxBn} টাকা/মাস`
    : `BDT ${salary.min.toLocaleString('en-US')} - ${salary.max.toLocaleString('en-US')} / month`;

  return (
    <div
      className={`p-6 sm:p-8 rounded-3xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs font-bengali ${className}`}
      aria-labelledby="salary-calculator-heading"
    >
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 pb-4 border-b border-amber-100 dark:border-[#262D3D]">
        <div>
          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 uppercase tracking-wider mb-1">
            <Calculator className="w-3.5 h-3.5" />
            <span>{isBengali ? "বাজারদর অনুযায়ী সঠিক পারিশ্রমিক গাইড" : "Market-Standard Salary Benchmark"}</span>
          </span>
          <h3
            id="salary-calculator-heading"
            className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white"
          >
            {isBengali ? "টিউশন পারিশ্রমিক ক্যালকুলেটর" : "Tuition Salary Calculator"}
          </h3>
        </div>

        <div className="text-xs text-slate-500 flex items-center gap-1">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>{isBengali ? "অভিভাবক ও শিক্ষক উভয়ের জন্য আদর্শ রেইট" : "Fair rates for both parents and tutors"}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        {/* Controls Column */}
        <div className="lg:col-span-7 space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* District */}
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1.5">
                {isBengali ? "জেলা / এলাকা:" : "District / Area:"}
              </label>
              <select
                value={district}
                onChange={(e) => setDistrict(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
              >
                <option value="ঢাকা">{isBengali ? "ঢাকা জেলা" : "Dhaka District"}</option>
                <option value="চট্টগ্রাম">{isBengali ? "চট্টগ্রাম জেলা" : "Chattogram District"}</option>
                <option value="রাজশাহী">{isBengali ? "রাজশাহী জেলা" : "Rajshahi District"}</option>
                <option value="সিলেট">{isBengali ? "সিলেট জেলা" : "Sylhet District"}</option>
                <option value="অন্যান্য জেলা">{isBengali ? "অন্যান্য জেলা" : "Other Districts"}</option>
              </select>
            </div>

            {/* Medium */}
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1.5">
                {isBengali ? "শিক্ষার্থীর মাধ্যম:" : "Curriculum Medium:"}
              </label>
              <select
                value={medium}
                onChange={(e) => setMedium(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
              >
                <option value="বাংলা মাধ্যম">{isBengali ? "বাংলা মাধ্যম" : "Bangla Medium"}</option>
                <option value="ইংলিশ ভার্সন">{isBengali ? "ইংলিশ ভার্সন (NCTB)" : "English Version (NCTB)"}</option>
                <option value="ইংলিশ মিডিয়াম">{isBengali ? "ইংলিশ মিডিয়াম (O/A Level)" : "English Medium (Cambridge / Edexcel)"}</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Class Group */}
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1.5">
                {isBengali ? "শ্রেণি বিভাগ:" : "Academic Grade:"}
              </label>
              <select
                value={classGroup}
                onChange={(e) => setClassGroup(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
              >
                <option value="primary">{isBengali ? "১ম - ৫ম শ্রেণি (প্রাইমারি)" : "Class 1 - 5 (Primary)"}</option>
                <option value="lower_secondary">{isBengali ? "৬ষ্ঠ - ৮ম শ্রেণি (জুনিয়র)" : "Class 6 - 8 (Junior Secondary)"}</option>
                <option value="secondary_ssc">{isBengali ? "৯ম - ১০ম শ্রেণি (এসএসসি)" : "Class 9 - 10 (SSC / O Level)"}</option>
                <option value="higher_hsc">{isBengali ? "একাদশ - দ্বাদশ শ্রেণি (এইচএসসি)" : "Class 11 - 12 (HSC / A Level)"}</option>
                <option value="admission">{isBengali ? "বিশ্ববিদ্যালয় ভর্তি প্রস্তুতি" : "University Admission Preparation"}</option>
              </select>
            </div>

            {/* Days per week */}
            <div>
              <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1.5">
                {isBengali ? "সপ্তাহে ক্লাসের দিন:" : "Days Per Week:"}
              </label>
              <div className="flex gap-2">
                {[2, 3, 4, 5].map((d) => (
                  <button
                    key={d}
                    type="button"
                    onClick={() => setDaysPerWeek(d)}
                    className={`flex-1 py-2 rounded-xl border text-xs font-bold transition-all ${
                      daysPerWeek === d
                        ? 'bg-[#ED8E22] text-white border-[#ED8E22]'
                        : 'bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                    }`}
                  >
                    {isBengali ? `${d} দিন` : `${d} Days`}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Estimation Display Column */}
        <div className="lg:col-span-5 flex flex-col justify-between p-6 rounded-3xl bg-[#FFF9EB]/70 dark:bg-[#0B0F19] border border-amber-200/60 dark:border-[#262D3D] space-y-4">
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
              {isBengali ? "প্রস্তাবিত মাসিক পারিশ্রমিক পরিসর:" : "Estimated Monthly Honorarium:"}
            </span>
            <div className="text-2xl sm:text-3xl font-bold font-mono text-emerald-800 dark:text-emerald-400 mt-1 leading-tight">
              {isBengali
                ? `${salary.minBn} - ${salary.maxBn} ৳/মাস`
                : `BDT ${salary.min.toLocaleString('en-US')} - ${salary.max.toLocaleString('en-US')} / mo`}
            </div>
            <div className="text-xs text-slate-500 mt-1">
              {isBengali
                ? `(ক্লাস প্রতি আনুমানিক ৳${salary.perClassBn} টাকা • সপ্তাহে ${daysPerWeek} দিন)`
                : `(~BDT ${Math.round(salary.min / (daysPerWeek * 4)).toLocaleString('en-US')} per class • ${daysPerWeek} days/week)`}
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/60 dark:border-[#262D3D] text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
            {isBengali
              ? "এই পারিশ্রমিক বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (বুয়েট), ঢাকা বিশ্ববিদ্যালয় ও মেডিকেল কলেজের শীর্ষ শিক্ষার্থীবান্ধব স্ট্যান্ডার্ড অনুযায়ী তৈরি।"
              : "Benchmarked against standard honorarium metrics for top scholars from BUET, DU, and Medical Colleges."}
          </div>

          {onRequestTutorWithSalary && (
            <button
              onClick={() => onRequestTutorWithSalary(formattedSalaryText)}
              className="w-full py-2.5 px-4 rounded-xl bg-[#ED8E22] hover:bg-[#D97D1A] active:bg-[#C57013] text-white font-bold text-xs sm:text-sm flex items-center justify-center gap-2 shadow-sm transition-all cursor-pointer"
            >
              <span>{isBengali ? "এই বাজেটে টিউটর রিকোয়ারমেন্ট দিন" : "Post Requirement with this Budget"}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
