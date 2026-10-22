/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    National Merit Scholarship Endowment Card Component
 * TOPIC:     Phase 113 National Merit Scholarship Pool & Autonomous Disbursement
 * FILE:      frontend/src/components/scholarship/ScholarshipEndowmentCard.tsx
 * PHASE:     Phase 113 - National Merit Scholarship Pool & Autonomous Disbursement
 * PURPOSE:   Renders prestigious Oxford/Cambridge caliber endowment grant cards
 *            with district quota allocations, bKash/Nagad B2C disbursement telemetry,
 *            tactile 3D Oxford Navy buttons, double-spending defense, and zero emojis.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React from 'react';
import {
  Award,
  ShieldCheck,
  Heart,
  Wallet,
  CheckCircle2,
  Building,
  TrendingUp,
  MapPin,
  Users,
  Lock,
  ExternalLink,
  Sparkles,
  ArrowRight
} from 'lucide-react';

export interface DistrictAllocation {
  allocated: number;
  funded: number;
}

export interface ScholarshipPoolData {
  pool_id: string;
  title_bn: string;
  title_en: string;
  sponsor_name: string;
  total_endowment_bdt: number;
  disbursed_bdt: number;
  remaining_bdt: number;
  grant_per_student_bdt: number;
  funded_students_count: number;
  target_quota_count: number;
  district_allocations: Record<string, DistrictAllocation>;
  status: string;
}

export interface ScholarshipEndowmentCardProps {
  pool: ScholarshipPoolData;
  onApplyClick?: (poolId: string) => void;
  onApproveClick?: (poolId: string) => void;
  onOpenLedgerModal?: () => void;
  isEvaluatorOrCustodian?: boolean;
}

export const ScholarshipEndowmentCard: React.FC<ScholarshipEndowmentCardProps> = ({
  pool,
  onApplyClick,
  onApproveClick,
  onOpenLedgerModal,
  isEvaluatorOrCustodian = false
}) => {
  const percentFunded = Math.min(
    100,
    Math.round((pool.funded_students_count / (pool.target_quota_count || 1)) * 100)
  );

  return (
    <div className="bg-[#FAFAF8] dark:bg-[#0B132B] border-2 border-slate-300 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-md relative overflow-hidden transition-all duration-200 hover:shadow-lg">
      
      {/* Top Header: Sponsor Badge & Pool Status */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-5 border-b border-slate-200 dark:border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center shadow-sm">
            <Award className="w-6 h-6 text-amber-300" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-bold text-amber-800 dark:text-amber-300 uppercase tracking-wider font-display">
                {pool.sponsor_name}
              </span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse" />
            </div>
            <h3 className="text-lg sm:text-xl font-bold font-bengali text-slate-900 dark:text-white leading-snug">
              {pool.title_bn}
            </h3>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-display">
              {pool.title_en}
            </p>
          </div>
        </div>

        {/* Grant Size Badge */}
        <div className="bg-white dark:bg-slate-900 px-4 py-2 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm text-right">
          <span className="text-[10px] text-slate-500 uppercase font-semibold block font-display">
            শিক্ষার্থী প্রতি অনুদান
          </span>
          <strong className="text-base sm:text-lg text-[#0A2540] dark:text-amber-300 font-display font-extrabold">
            ৳{pool.grant_per_student_bdt.toLocaleString('en-US')}
          </strong>
        </div>
      </div>

      {/* Financial Health & Beneficiary Progress Bar */}
      <div className="py-6 space-y-3">
        <div className="flex items-center justify-between text-xs font-display">
          <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-300">
            <Users className="w-4 h-4 text-[#0A2540] dark:text-amber-400" />
            <span className="font-bengali font-semibold">সুবিধাভোগী শিক্ষার্থী:</span>
            <strong className="text-slate-900 dark:text-white font-bold">
              {pool.funded_students_count} / {pool.target_quota_count} জন
            </strong>
          </div>
          <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-300">
            <Wallet className="w-4 h-4 text-emerald-600" />
            <span className="font-bengali font-semibold">অবশিষ্ট তহবিল:</span>
            <strong className="text-slate-900 dark:text-white font-bold">
              ৳{pool.remaining_bdt.toLocaleString('en-US')}
            </strong>
          </div>
        </div>

        {/* Progress Track */}
        <div className="w-full h-3 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden p-0.5 border border-slate-300/50 dark:border-slate-700">
          <div
            className="h-full bg-gradient-to-r from-[#0A2540] to-amber-600 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${percentFunded}%` }}
          />
        </div>
        <div className="flex justify-between text-[11px] text-slate-500 font-display">
          <span>বরাদ্দ: ৳{pool.total_endowment_bdt.toLocaleString('en-US')}</span>
          <span className="font-semibold text-amber-800 dark:text-amber-300">
            {percentFunded}% কোটা পূর্ণ
          </span>
        </div>
      </div>

      {/* Priority District Quotas Grid */}
      <div className="space-y-2.5 pt-2">
        <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800 dark:text-slate-200 font-bengali">
          <MapPin className="w-3.5 h-3.5 text-amber-700 dark:text-amber-400" />
          <span>অনগ্রসর ও সীমান্তবর্তী জেলা কোটা বণ্টন:</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-bengali">
          {Object.entries(pool.district_allocations).map(([district, allocation]) => {
            const isFull = allocation.funded >= allocation.allocated;
            return (
              <div
                key={district}
                className="p-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 flex flex-col justify-between"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-800 dark:text-slate-200">
                    {district === 'Kurigram'
                      ? 'কুড়িগ্রাম'
                      : district === 'Sunamganj'
                      ? 'সুনামগঞ্জ'
                      : district === 'Bandarban'
                      ? 'বান্দরবান'
                      : district === 'Barguna'
                      ? 'বরগুনা'
                      : district === 'Lalmonirhat'
                      ? 'লালমনিরহাট'
                      : district === 'Netrokona'
                      ? 'নেত্রকোণা'
                      : district === 'Panchagarh'
                      ? 'পঞ্চগড়'
                      : district === 'Gaibandha'
                      ? 'গাইবান্ধা'
                      : 'সাধারণ মেধা'}
                  </span>
                  {isFull ? (
                    <span className="w-2 h-2 rounded-full bg-amber-500" title="কোটা পূর্ণ" />
                  ) : (
                    <span className="w-2 h-2 rounded-full bg-emerald-500" title="আবেদন গ্রহণযোগ্য" />
                  )}
                </div>
                <div className="mt-1 flex items-center justify-between text-[11px] text-slate-500 font-display">
                  <span>পূরণ: {allocation.funded}/{allocation.allocated}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Security & Double-Spending Protection Guarantee */}
      <div className="mt-5 p-3 rounded-xl bg-slate-100 dark:bg-slate-900/80 border border-slate-200/80 dark:border-slate-800 flex items-center justify-between text-[11px] font-bengali text-slate-600 dark:text-slate-400">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>দ্বৈত-অনুমোদন (Dual-Auth) ও বিকাশ/নগদ বিটুসি ডিরেক্ট ডিসবার্সমেন্ট সুরক্ষাপ্রাপ্ত</span>
        </div>
        <button
          type="button"
          onClick={onOpenLedgerModal}
          className="hover:underline text-[#0A2540] dark:text-amber-400 font-semibold flex items-center gap-1 shrink-0 ml-2"
        >
          <span>পাবলিক লেজার অডিট</span>
          <ExternalLink className="w-3 h-3" />
        </button>
      </div>

      {/* Action Buttons: Tactile 3D Oxford Navy Depth */}
      <div className="mt-6 pt-5 border-t border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3">
        <div className="text-xs text-slate-500 font-bengali">
          যোগ্যতা: এসএসসি/এইচএসসি GPA 5.0 বা শীর্ষ ৫% + মাসিক পারিবারিক আয় ≤ ১৫,০০০ টাকা
        </div>

        <div className="flex items-center gap-3 ml-auto">
          {isEvaluatorOrCustodian && (
            <button
              type="button"
              onClick={() => onApproveClick?.(pool.pool_id)}
              className="px-4 py-2.5 bg-white dark:bg-slate-900 hover:bg-slate-50 text-slate-800 dark:text-slate-200 border-2 border-[#0A2540] dark:border-slate-600 rounded-2xl text-xs font-semibold font-bengali shadow-[0_3px_0_0_#0A2540] active:translate-y-0.5 active:shadow-none transition-all flex items-center gap-2"
            >
              <ShieldCheck className="w-4 h-4 text-emerald-600" />
              <span>বৃত্তি অনুমোদন করুন</span>
            </button>
          )}

          <button
            type="button"
            onClick={() => onApplyClick?.(pool.pool_id)}
            className="px-6 py-2.5 bg-[#0A2540] hover:bg-[#0E3357] text-white rounded-2xl text-xs sm:text-sm font-semibold font-bengali shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none transition-all flex items-center gap-2"
          >
            <Heart className="w-4 h-4 text-amber-300" />
            <span>আবেদন জমা দিন</span>
            <ArrowRight className="w-4 h-4 text-slate-300" />
          </button>
        </div>
      </div>
    </div>
  );
};
