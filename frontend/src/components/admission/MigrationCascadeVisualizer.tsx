/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Admission Migration Cascade Visualizer
 * TOPIC:     Multi-Round Upward Seat Reallocation & Vacancy Ripple Visualizer
 * FILE:      frontend/src/components/admission/MigrationCascadeVisualizer.tsx
 * PHASE:     Phase 107 - Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
 * PURPOSE:   Provides an interactive visualizer illustrating multi-round seat reallocation:
 *            1. Simulates candidate withdrawals (BUET / Medical cross-admissions).
 *            2. Shows upward seat cascade ripples round-by-round with upward promotion badges.
 *            3. Interactive round scrubber and cut-off rank change telemetry.
 *            4. Tactile 3D button mechanics with physical press depth.
 * STANDARDS: Pareto-Optimal Deferred Acceptance, Quota Spillover Balancing, Zero-Emoji, UI/UX Pro Max
 */

import React, { useState } from 'react';
import {
  TrendingUp,
  ArrowRight,
  RefreshCw,
  Award,
  Layers,
  CheckCircle2,
  Sliders,
  Sparkles,
  Compass,
  ArrowUpRight,
  Building2,
  Users
} from 'lucide-react';

export interface MigrationStep {
  student_id: string;
  name: string;
  merit_rank: number;
  from_program: string;
  to_program: string;
  upgrade_description: string;
}

export interface CascadeRound {
  round_number: number;
  title: string;
  active_students: number;
  matched_students: number;
  migrations: MigrationStep[];
  program_cutoffs: Record<string, number>;
}

export interface MigrationCascadeVisualizerProps {
  className?: string;
  onSimulationRun?: () => void;
}

const MOCK_CASCADE_ROUNDS: CascadeRound[] = [
  {
    round_number: 1,
    title: 'প্রথম পর্যায়: প্রাথমিক মেধাভিত্তিক আসন বরাদ্দ',
    active_students: 120,
    matched_students: 112,
    migrations: [],
    program_cutoffs: {
      BUET_CSE: 165,
      BUET_EEE: 450,
      DU_CSE: 320,
      DMC_MBBS: 260,
      JU_CSE: 850,
      CKET_CSE: 1150
    }
  },
  {
    round_number: 2,
    title: 'দ্বিতীয় পর্যায়: মেডিকেলে ভর্তি ও বুয়েট আসন বাতিলের পর প্রথম মাইগ্রেশন',
    active_students: 110,
    matched_students: 110,
    migrations: [
      {
        student_id: 'STU_104',
        name: 'তানভীর আহমেদ',
        merit_rank: 168,
        from_program: 'BUET_EEE',
        to_program: 'BUET_CSE',
        upgrade_description: 'বুয়েট ট্রিপল-ই থেকে বুয়েট সিএসইতে আসন মাইগ্রেশন'
      },
      {
        student_id: 'STU_215',
        name: 'সাদিয়া তাসনিম',
        merit_rank: 325,
        from_program: 'JU_CSE',
        to_program: 'DU_CSE',
        upgrade_description: 'জাবি সিএসই থেকে ঢাবি সিএসইতে আসন মাইগ্রেশন'
      },
      {
        student_id: 'STU_482',
        name: 'আরিফুল ইসলাম',
        merit_rank: 462,
        from_program: 'CKET_CSE',
        to_program: 'BUET_EEE',
        upgrade_description: 'প্রকৌশল গুচ্ছ থেকে বুয়েট ট্রিপল-ই তে আসন মাইগ্রেশন'
      }
    ],
    program_cutoffs: {
      BUET_CSE: 172,
      BUET_EEE: 465,
      DU_CSE: 335,
      DMC_MBBS: 265,
      JU_CSE: 875,
      CKET_CSE: 1180
    }
  },
  {
    round_number: 3,
    title: 'তৃতীয় পর্যায়: চূড়ান্ত মাইগ্রেশন ও কোটা স্পিল-ওভার সমন্বয়',
    active_students: 110,
    matched_students: 110,
    migrations: [
      {
        student_id: 'STU_338',
        name: 'ফারহান চৌধুরী',
        merit_rank: 340,
        from_program: 'DU_EEE',
        to_program: 'DU_CSE',
        upgrade_description: 'ঢাবি ট্রিপল-ই থেকে ঢাবি সিএসইতে কোটা স্পিল-ওভার মাইগ্রেশন'
      },
      {
        student_id: 'STU_890',
        name: 'নুসরাত জাহান',
        merit_rank: 885,
        from_program: 'অপেক্ষমাণ তালিকা',
        to_program: 'JU_CSE',
        upgrade_description: 'অপেক্ষমাণ তালিকা থেকে জাবি সিএসইতে চূড়ান্ত অন্তর্ভুক্তি'
      }
    ],
    program_cutoffs: {
      BUET_CSE: 175,
      BUET_EEE: 472,
      DU_CSE: 342,
      DMC_MBBS: 268,
      JU_CSE: 895,
      CKET_CSE: 1195
    }
  }
];

export const MigrationCascadeVisualizer: React.FC<MigrationCascadeVisualizerProps> = ({
  className = '',
  onSimulationRun
}) => {
  const [currentRoundIndex, setCurrentRoundIndex] = useState<number>(1);
  const [isSimulating, setIsSimulating] = useState<boolean>(false);

  const activeRound = MOCK_CASCADE_ROUNDS[currentRoundIndex];

  const handleRunSimulation = () => {
    setIsSimulating(true);
    let nextIdx = 0;
    const interval = setInterval(() => {
      nextIdx += 1;
      if (nextIdx < MOCK_CASCADE_ROUNDS.length) {
        setCurrentRoundIndex(nextIdx);
      } else {
        clearInterval(interval);
        setIsSimulating(false);
      }
    }, 1200);

    if (onSimulationRun) {
      onSimulationRun();
    }
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Visualizer Top Shell */}
      <div className="rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#24314A] p-6 sm:p-8 shadow-xs space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-800">
          <div className="space-y-1.5">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-950/80 border border-blue-500/30 text-blue-300 text-xs font-mono font-medium">
              <TrendingUp className="w-3.5 h-3.5 text-blue-400" />
              <span>UPWARD MIGRATION CASCADE SIMULATOR</span>
            </div>
            <h3 className="text-xl font-bold text-white font-sans flex items-center gap-2.5">
              <Layers className="w-5 h-5 text-blue-400" />
              <span>আসন মাইগ্রেশন রিপল ও ঊর্ধ্বমুখী বরাদ্দ সিমুলেশন</span>
            </h3>
            <p className="text-xs sm:text-sm text-slate-300 font-bengali max-w-2xl leading-relaxed">
              মেডিকেল বা উচ্চতর বুয়েট বিভাগে শিক্ষার্থী ভর্তি হওয়ার পর ঢাবি বা গুচ্ছে আসন শূন্য হলে কীভাবে নিচ থেকে
              মেধা অনুযায়ী প্রার্থীরা স্বয়ংক্রিয়ভাবে উপরের পছন্দের বিভাগে উন্নীত হন, তা দেখুন।
            </p>
          </div>

          <button
            type="button"
            disabled={isSimulating}
            onClick={handleRunSimulation}
            className="px-6 py-3.5 rounded-2xl bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-sans text-xs sm:text-sm font-semibold shadow-[0_4px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none transition-all flex items-center justify-center gap-2 shrink-0"
          >
            <RefreshCw className={`w-4 h-4 ${isSimulating ? 'animate-spin' : ''}`} />
            <span>{isSimulating ? 'সিমুলেশন চলছে...' : 'মাইগ্রেশন সিমুলেশন চালু করুন'}</span>
          </button>
        </div>

        {/* Round Navigation Scrubber */}
        <div className="flex items-center justify-between gap-2 bg-slate-950/80 p-2 rounded-2xl border border-slate-800">
          {MOCK_CASCADE_ROUNDS.map((round, idx) => (
            <button
              key={round.round_number}
              type="button"
              onClick={() => setCurrentRoundIndex(idx)}
              className={`flex-1 py-2.5 px-3 rounded-xl text-xs font-sans transition-all flex flex-col sm:flex-row items-center justify-center gap-2 ${
                currentRoundIndex === idx
                  ? 'bg-blue-600 text-white shadow-md font-semibold'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <span className="font-mono font-bold">রাউন্ড {round.round_number}</span>
              <span className="hidden md:inline text-[11px] opacity-80">
                {idx === 0 ? 'প্রাথমিক' : idx === 1 ? '১ম মাইগ্রেশন' : 'চূড়ান্ত'}
              </span>
            </button>
          ))}
        </div>

        {/* Round Overview Card */}
        <div className="p-5 rounded-2xl bg-slate-950/60 border border-slate-800/80 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <h4 className="text-sm font-bold text-white font-sans flex items-center gap-2">
              <Award className="w-4 h-4 text-amber-400" />
              <span>{activeRound.title}</span>
            </h4>
            <div className="flex items-center gap-3 text-xs font-mono text-slate-400">
              <span>বরাদ্দপ্রাপ্ত: {activeRound.matched_students} জন</span>
              <span>•</span>
              <span className="text-emerald-400 font-semibold">
                মাইগ্রেশন সম্পন্ন: {activeRound.migrations.length} জন
              </span>
            </div>
          </div>

          {/* Upward Migration Badges & Paths */}
          {activeRound.migrations.length > 0 ? (
            <div className="space-y-3 pt-2">
              <div className="text-xs font-semibold text-slate-400 font-sans">
                এই রাউন্ডে আসন প্রাপ্তি ও ঊর্ধ্বমুখী উন্নয়ন:
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {activeRound.migrations.map((mig) => (
                  <div
                    key={mig.student_id}
                    className="p-3.5 rounded-xl bg-slate-900/90 border border-blue-500/30 flex items-center justify-between gap-3 shadow-sm hover:border-blue-500/60 transition-all"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-white font-sans">{mig.name}</span>
                        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-500/30">
                          মেধা: #{mig.merit_rank}
                        </span>
                      </div>
                      <div className="text-[11px] text-slate-300 font-bengali">
                        {mig.upgrade_description}
                      </div>
                    </div>

                    <div className="shrink-0 flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 text-xs font-mono">
                      <span>{mig.from_program}</span>
                      <ArrowRight className="w-3 h-3 text-emerald-400" />
                      <span className="font-bold text-white">{mig.to_program}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 text-xs text-slate-400 text-center font-bengali">
              প্রাথমিক রাউন্ডে মেধা তালিকা ও প্রথম পছন্দের ভিত্তিতে ১০০% স্থিতিশীল বরাদ্দ কার্যকর হয়েছে।
            </div>
          )}
        </div>

        {/* Dynamic Cutoff Ranks Table */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs">
            <span className="font-semibold text-slate-300 font-sans flex items-center gap-1.5">
              <Building2 className="w-3.5 h-3.5 text-blue-400" />
              <span>এই রাউন্ড শেষে প্রধান বিভাগসমূহের কাটঅফ মেধা ক্রম:</span>
            </span>
            <span className="text-slate-500 font-mono">DYNAMIC CUT-OFF EXPANSION</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {Object.entries(activeRound.program_cutoffs).map(([pId, cutoff]) => (
              <div
                key={pId}
                className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1 text-center"
              >
                <div className="text-[11px] font-mono text-slate-400">{pId.replace('_', ' ')}</div>
                <div className="text-sm font-bold text-blue-400 font-sans">
                  #{cutoff}
                </div>
                <div className="text-[10px] text-emerald-400 font-mono flex items-center justify-center gap-0.5">
                  <ArrowUpRight className="w-3 h-3" />
                  <span>কাটঅফ সম্প্রসারিত</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
