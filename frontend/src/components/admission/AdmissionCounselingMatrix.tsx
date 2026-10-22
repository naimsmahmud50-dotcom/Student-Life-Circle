/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Admission Counseling Matrix & Preference Builder
 * TOPIC:     Interactive University Preference Ordering & Real-Time Probability Meters
 * FILE:      frontend/src/components/admission/AdmissionCounselingMatrix.tsx
 * PHASE:     Phase 107 - Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
 * PURPOSE:   Provides an elite guidance counseling room interface for admission candidates:
 *            1. Drag/reorder preference card stack with tactile physical controls.
 *            2. Real-time admission probability meters and historical cutoff benchmarks.
 *            3. Transparent affirmative action quota selection and auto-spillover explanations.
 *            4. Tactile 3D action buttons with physical press mechanics.
 * STANDARDS: Pareto-Optimal Deferred Acceptance, Quota Spillover Balancing, Zero-Emoji, UI/UX Pro Max
 */

import React, { useState, useMemo } from 'react';
import {
  GraduationCap,
  Award,
  Compass,
  Layers,
  CheckCircle2,
  ChevronUp,
  ChevronDown,
  Plus,
  Trash2,
  Sparkles,
  Sliders,
  ShieldCheck,
  TrendingUp,
  Info,
  Building2,
  AlertCircle
} from 'lucide-react';

export interface AdmissionProgram {
  program_id: string;
  institution_name: string;
  department_name: string;
  short_name: string;
  total_capacity: number;
  historical_cutoff_rank: number;
  category: string;
  cluster: string;
}

export interface AdmissionCounselingMatrixProps {
  initialRank?: number;
  initialScore?: number;
  candidateName?: string;
  onSavePreferences?: (preferences: string[], quota: string) => void;
  className?: string;
}

const DEFAULT_PROGRAMS: AdmissionProgram[] = [
  {
    program_id: 'BUET_CSE',
    institution_name: 'বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (BUET)',
    department_name: 'কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)',
    short_name: 'বুয়েট সিএসই',
    total_capacity: 120,
    historical_cutoff_rank: 165,
    category: 'Engineering',
    cluster: 'ENGINEERING'
  },
  {
    program_id: 'BUET_EEE',
    institution_name: 'বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (BUET)',
    department_name: 'ইলেকট্রিক্যাল অ্যান্ড ইলেকট্রনিক ইঞ্জিনিয়ারিং (EEE)',
    short_name: 'বুয়েট ট্রিপল-ই',
    total_capacity: 195,
    historical_cutoff_rank: 450,
    category: 'Engineering',
    cluster: 'ENGINEERING'
  },
  {
    program_id: 'DMC_MBBS',
    institution_name: 'ঢাকা মেডিকেল কলেজ (DMC)',
    department_name: 'ব্যাচেলর অব মেডিসিন অ্যান্ড ব্যাচেলর অব সার্জারি (MBBS)',
    short_name: 'ডিএমসি এমবিবিএস',
    total_capacity: 230,
    historical_cutoff_rank: 260,
    category: 'Medical',
    cluster: 'MEDICAL'
  },
  {
    program_id: 'DU_CSE',
    institution_name: 'ঢাকা বিশ্ববিদ্যালয় (DU)',
    department_name: 'কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)',
    short_name: 'ঢাবি সিএসই',
    total_capacity: 60,
    historical_cutoff_rank: 320,
    category: 'Science',
    cluster: 'GENERAL_PUBLIC'
  },
  {
    program_id: 'DU_EEE',
    institution_name: 'ঢাকা বিশ্ববিদ্যালয় (DU)',
    department_name: 'ইলেকট্রিক্যাল অ্যান্ড ইলেকট্রনিক ইঞ্জিনিয়ারিং (EEE)',
    short_name: 'ঢাবি ট্রিপল-ই',
    total_capacity: 70,
    historical_cutoff_rank: 680,
    category: 'Science',
    cluster: 'GENERAL_PUBLIC'
  },
  {
    program_id: 'JU_CSE',
    institution_name: 'জাহাঙ্গীরনগর বিশ্ববিদ্যালয় (JU)',
    department_name: 'কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)',
    short_name: 'জাবি সিএসই',
    total_capacity: 55,
    historical_cutoff_rank: 850,
    category: 'Science',
    cluster: 'GENERAL_PUBLIC'
  },
  {
    program_id: 'CKET_CSE',
    institution_name: 'চুয়েট-কুয়েট-রুয়েট সমন্বিত প্রকৌশল গুচ্ছ (CKET)',
    department_name: 'কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)',
    short_name: 'প্রকৌশল গুচ্ছ সিএসই',
    total_capacity: 180,
    historical_cutoff_rank: 1150,
    category: 'Engineering',
    cluster: 'ENGINEERING'
  },
  {
    program_id: 'RU_CSE',
    institution_name: 'রাজশাহী বিশ্ববিদ্যালয় (RU)',
    department_name: 'কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)',
    short_name: 'রাবি সিএসই',
    total_capacity: 50,
    historical_cutoff_rank: 1380,
    category: 'Science',
    cluster: 'GENERAL_PUBLIC'
  }
];

export const AdmissionCounselingMatrix: React.FC<AdmissionCounselingMatrixProps> = ({
  initialRank = 142,
  initialScore = 88.5,
  candidateName = 'মাহমুদ হাসান',
  onSavePreferences,
  className = ''
}) => {
  const [meritRank, setMeritRank] = useState<number>(initialRank);
  const [selectedQuota, setSelectedQuota] = useState<string>('GENERAL');
  const [preferenceList, setPreferenceList] = useState<string[]>([
    'BUET_CSE',
    'DU_CSE',
    'BUET_EEE',
    'DMC_MBBS',
    'JU_CSE',
    'CKET_CSE'
  ]);
  const [isSaved, setIsSaved] = useState<boolean>(false);

  // Available programs that can be added
  const availableToAdd = useMemo(() => {
    return DEFAULT_PROGRAMS.filter((p) => !preferenceList.includes(p.program_id));
  }, [preferenceList]);

  // Probability calculation helper
  const calculateProbability = (cutoff: number) => {
    const quotaMultipliers: Record<string, number> = {
      GENERAL: 1.0,
      FREEDOM_FIGHTER: 1.45,
      TRIBAL: 1.80,
      DISTRICT: 1.25,
      SPECIAL_NEEDS: 2.10
    };
    const effectiveCutoff = cutoff * (quotaMultipliers[selectedQuota] || 1.0);

    if (meritRank <= effectiveCutoff * 0.70) {
      return {
        percent: Math.min(98, Math.round(92 + ((effectiveCutoff * 0.7 - meritRank) / effectiveCutoff) * 6)),
        label: 'উচ্চ সম্ভাবনা',
        gradient: 'from-emerald-500/20 to-teal-500/20 border-emerald-500/40 text-emerald-300',
        barColor: 'bg-emerald-500'
      };
    } else if (meritRank <= effectiveCutoff) {
      const progress = (effectiveCutoff - meritRank) / (effectiveCutoff * 0.30);
      return {
        percent: Math.round(65 + progress * 24),
        label: 'সন্তোষজনক',
        gradient: 'from-blue-500/20 to-teal-500/20 border-blue-500/40 text-blue-300',
        barColor: 'bg-blue-500'
      };
    } else if (meritRank <= effectiveCutoff * 1.35) {
      const progress = (effectiveCutoff * 1.35 - meritRank) / (effectiveCutoff * 0.35);
      return {
        percent: Math.round(25 + progress * 35),
        label: 'উচ্চাকাঙ্ক্ষী লক্ষ্য',
        gradient: 'from-amber-500/20 to-orange-500/20 border-amber-500/40 text-amber-300',
        barColor: 'bg-amber-500'
      };
    } else {
      return {
        percent: Math.max(8, Math.round(20 - ((meritRank - effectiveCutoff * 1.35) / effectiveCutoff) * 12)),
        label: 'ঝুঁকিপূর্ণ',
        gradient: 'from-rose-500/20 to-red-500/20 border-rose-500/40 text-rose-300',
        barColor: 'bg-rose-500'
      };
    }
  };

  const handleMoveUp = (index: number) => {
    if (index === 0) return;
    const updated = [...preferenceList];
    const temp = updated[index - 1];
    updated[index - 1] = updated[index];
    updated[index] = temp;
    setPreferenceList(updated);
    setIsSaved(false);
  };

  const handleMoveDown = (index: number) => {
    if (index === preferenceList.length - 1) return;
    const updated = [...preferenceList];
    const temp = updated[index + 1];
    updated[index + 1] = updated[index];
    updated[index] = temp;
    setPreferenceList(updated);
    setIsSaved(false);
  };

  const handleRemove = (programId: string) => {
    setPreferenceList(preferenceList.filter((id) => id !== programId));
    setIsSaved(false);
  };

  const handleAdd = (programId: string) => {
    setPreferenceList([...preferenceList, programId]);
    setIsSaved(false);
  };

  const handleSave = () => {
    setIsSaved(true);
    if (onSavePreferences) {
      onSavePreferences(preferenceList, selectedQuota);
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Guidance Top Card */}
      <div className="rounded-3xl bg-slate-900/90 border border-slate-800 p-6 sm:p-8 shadow-xl backdrop-blur-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-800/80">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-950/80 border border-blue-500/30 text-blue-300 text-xs font-mono font-medium">
              <Compass className="w-3.5 h-3.5 text-blue-400" />
              <span>GALE-SHAPLEY DEFERRED ACCEPTANCE ENGINE</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white font-sans flex items-center gap-2.5">
              <GraduationCap className="w-6 h-6 text-blue-400" />
              <span>পছন্দক্রম ম্যাট্রিক্স ও ভর্তি সম্ভাবনা বিশ্লেষক</span>
            </h2>
            <p className="text-xs sm:text-sm text-slate-300 max-w-2xl font-bengali leading-relaxed">
              গেলে-শ্যাপলি অ্যালগরিদমের কারণে পছন্দক্রম সত্যবাদী রাখা সম্পূর্ণ নিরাপদ। উপরের পছন্দ না পেলে স্বয়ংক্রিয়ভাবে
              পরের পছন্দ বিবেচিত হবে, কোনো পেনাল্টি বা আসন হারানোর ঝুঁকি নেই।
            </p>
          </div>

          {/* Candidate Profile Widget */}
          <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-950/80 border border-slate-800">
            <div className="w-12 h-12 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-300 font-bold text-lg font-sans">
              {candidateName.charAt(0)}
            </div>
            <div className="space-y-0.5">
              <div className="text-sm font-semibold text-white font-sans">{candidateName}</div>
              <div className="text-xs text-slate-400 flex items-center gap-2 font-mono">
                <span>মেধা স্কোর: {initialScore}</span>
                <span className="text-slate-600">|</span>
                <span className="text-emerald-400 font-semibold font-sans">মেধা ক্রম: #{meritRank}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Merit Rank Adjuster & Quota Selectors */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300 font-sans flex items-center justify-between">
              <span>সিমুলেটেড মেধা ক্রম (Merit Rank)</span>
              <span className="text-blue-400 font-mono">#{meritRank}</span>
            </label>
            <input
              type="range"
              min="1"
              max="2000"
              value={meritRank}
              onChange={(e) => {
                setMeritRank(parseInt(e.target.value, 10));
                setIsSaved(false);
              }}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
            <div className="flex justify-between text-[11px] text-slate-500 font-mono">
              <span>#1 (শীর্ষ মেধা)</span>
              <span>#500 (বুয়েট/ডিএমসি কাটঅফ)</span>
              <span>#2000 (বিশ্ববিদ্যালয় কাটঅফ)</span>
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300 font-sans flex items-center gap-1.5">
              <Award className="w-3.5 h-3.5 text-amber-400" />
              <span>কোটা ক্যাটাগরি (স্বয়ংক্রিয় সাধারণ স্পিল-ওভার প্রযোজ্য)</span>
            </label>
            <div className="grid grid-cols-3 sm:grid-cols-5 gap-2">
              {[
                { id: 'GENERAL', label: 'সাধারণ' },
                { id: 'FREEDOM_FIGHTER', label: 'মুক্তিযোদ্ধা' },
                { id: 'TRIBAL', label: 'উপজাতি' },
                { id: 'DISTRICT', label: 'জেলা' },
                { id: 'SPECIAL_NEEDS', label: 'প্রতিবন্ধী' }
              ].map((q) => (
                <button
                  key={q.id}
                  type="button"
                  onClick={() => {
                    setSelectedQuota(q.id);
                    setIsSaved(false);
                  }}
                  className={`px-3 py-2 rounded-xl text-xs font-medium transition-all text-center ${
                    selectedQuota === q.id
                      ? 'bg-blue-600 text-white shadow-md font-semibold'
                      : 'bg-slate-800/80 text-slate-400 hover:text-slate-200 border border-slate-700/60'
                  }`}
                >
                  {q.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Preference Stack */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-blue-400" />
            <h3 className="text-base font-bold text-white font-sans">
              আপনার সক্রিয় পছন্দক্রম ({preferenceList.length}টি বিভাগ নির্বাচিত)
            </h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">DRAG & DROP / ARROW SORTED</span>
        </div>

        <div className="space-y-3">
          {preferenceList.map((programId, index) => {
            const program = DEFAULT_PROGRAMS.find((p) => p.program_id === programId);
            if (!program) return null;
            const prob = calculateProbability(program.historical_cutoff_rank);

            return (
              <div
                key={program.program_id}
                className="group relative flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 sm:p-5 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-slate-700/80 shadow-md transition-all backdrop-blur-md"
              >
                {/* Priority Rank & Details */}
                <div className="flex items-start sm:items-center gap-4">
                  <div className="w-8 h-8 shrink-0 rounded-xl bg-blue-950 border border-blue-500/40 flex items-center justify-center text-blue-300 font-bold text-xs font-sans">
                    {index + 1}
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-sm sm:text-base font-bold text-white font-sans">
                        {program.department_name}
                      </span>
                      <span className="text-[11px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono border border-slate-700">
                        {program.cluster}
                      </span>
                    </div>
                    <div className="text-xs text-slate-400 font-bengali flex items-center gap-2">
                      <Building2 className="w-3.5 h-3.5 text-slate-500" />
                      <span>{program.institution_name}</span>
                      <span className="text-slate-600">•</span>
                      <span className="font-mono text-slate-300">
                        বিগত কাটঅফ: #{program.historical_cutoff_rank}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Probability Meter & Controls */}
                <div className="flex items-center gap-4 shrink-0">
                  <div className="w-36 sm:w-44 space-y-1.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className={`px-2 py-0.5 rounded-md border text-[10px] font-semibold ${prob.gradient}`}>
                        {prob.label}
                      </span>
                      <span className="font-sans font-bold text-slate-200 text-xs">
                        {prob.percent}%
                      </span>
                    </div>
                    <div className="w-full h-1.5 rounded-full bg-slate-800 overflow-hidden">
                      <div
                        className={`h-full ${prob.barColor} transition-all duration-500 rounded-full`}
                        style={{ width: `${prob.percent}%` }}
                      />
                    </div>
                  </div>

                  {/* Reorder and Delete Controls */}
                  <div className="flex items-center gap-1 border-l border-slate-800 pl-3">
                    <button
                      type="button"
                      disabled={index === 0}
                      onClick={() => handleMoveUp(index)}
                      className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 disabled:opacity-30 disabled:hover:bg-transparent"
                      title="উপরে নিন"
                    >
                      <ChevronUp className="w-4 h-4" />
                    </button>
                    <button
                      type="button"
                      disabled={index === preferenceList.length - 1}
                      onClick={() => handleMoveDown(index)}
                      className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 disabled:opacity-30 disabled:hover:bg-transparent"
                      title="নিচে নিন"
                    >
                      <ChevronDown className="w-4 h-4" />
                    </button>
                    <button
                      type="button"
                      onClick={() => handleRemove(program.program_id)}
                      className="p-1.5 rounded-lg text-rose-400/80 hover:text-rose-300 hover:bg-rose-950/40 ml-1"
                      title="মুছে ফেলুন"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Add Remaining Programs Drawer */}
        {availableToAdd.length > 0 && (
          <div className="p-4 rounded-2xl bg-slate-900/40 border border-slate-800/80 space-y-3">
            <div className="text-xs font-semibold text-slate-400 font-sans flex items-center gap-1.5">
              <Plus className="w-3.5 h-3.5 text-blue-400" />
              <span>পছন্দক্রমে আরও বিভাগ যুক্ত করুন:</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {availableToAdd.map((p) => (
                <button
                  key={p.program_id}
                  type="button"
                  onClick={() => handleAdd(p.program_id)}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/80 text-xs text-slate-200 transition-all font-sans"
                >
                  <Plus className="w-3 h-3 text-blue-400" />
                  <span>{p.short_name}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Save & Confirm Actions */}
        <div className="pt-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs text-slate-400 flex items-center gap-2">
            <Info className="w-4 h-4 text-blue-400 shrink-0" />
            <span>
              সংরক্ষণের পর কেন্দ্রীয় কাউন্সেলিং সার্ভারে আপনার পছন্দক্রম আপডেট হবে এবং তাৎক্ষণিক এলোকেশন সিমুলেট করা যাবে।
            </span>
          </div>

          <button
            type="button"
            onClick={handleSave}
            className="w-full sm:w-auto px-8 py-3.5 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white font-sans text-sm font-semibold shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none transition-all flex items-center justify-center gap-2"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>{isSaved ? 'পছন্দক্রম সংরক্ষিত হয়েছে' : 'পছন্দক্রম সংরক্ষণ করুন'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
