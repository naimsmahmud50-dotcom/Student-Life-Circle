/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Section Performance Analytics Card Component
 * TOPIC:     Phase 114 Institutional White-Label Portal & Teacher Cockpit
 * FILE:      frontend/src/components/institution/SectionAnalyticsCard.tsx
 * PHASE:     Phase 114 - Institutional White-Label Portal & Teacher Cockpit
 * PURPOSE:   Visualizes section-wide performance distribution, statistical spread,
 *            standard deviation, and diagnostic weak topic clusters without
 *            public student shaming.
 * STANDARDS: UI/UX Pro Max, Pure Academic Palette, WCAG 2.2 AAA, Strict Zero-Emoji
 */

import React from 'react';
import {
  BarChart3,
  TrendingUp,
  AlertCircle,
  CheckCircle2,
  HelpCircle,
  BookOpen,
  ShieldCheck,
  Activity,
  Layers,
  Award
} from 'lucide-react';

export interface DistributionBrackets {
  tier_below_40: number;
  tier_40_59: number;
  tier_60_79: number;
  tier_80_100: number;
}

export interface WeakTopicCluster {
  topic_name_bn: string;
  accuracy_percent: number;
  remedial_tip_bn: string;
}

export interface SectionAnalyticsData {
  total_examinees: number;
  average_score: number;
  median_score: number;
  standard_deviation: number;
  highest_score: number;
  lowest_score: number;
  distribution_brackets: DistributionBrackets;
  weak_topics: WeakTopicCluster[];
}

export interface SectionAnalyticsCardProps {
  analytics: SectionAnalyticsData;
  sectionName?: string;
  examTitle?: string;
}

export const SectionAnalyticsCard: React.FC<SectionAnalyticsCardProps> = ({
  analytics,
  sectionName = 'শাখা ক (বিজ্ঞান)',
  examTitle = 'পদার্থবিজ্ঞান ১ম পত্র সেকশন মডেল টেস্ট'
}) => {
  const total = analytics.total_examinees || 1;
  const tiers = [
    {
      key: 'tier_80_100',
      label: '৮০% - ১০০% (শ্রেষ্ঠত্ব)',
      count: analytics.distribution_brackets.tier_80_100,
      color: 'bg-emerald-600',
      textColor: 'text-emerald-700 dark:text-emerald-400',
      bgLight: 'bg-emerald-50 dark:bg-emerald-950/40'
    },
    {
      key: 'tier_60_79',
      label: '৬০% - ৭৯% (সন্তোষজনক)',
      count: analytics.distribution_brackets.tier_60_79,
      color: 'bg-sky-600',
      textColor: 'text-sky-700 dark:text-sky-400',
      bgLight: 'bg-sky-50 dark:bg-sky-950/40'
    },
    {
      key: 'tier_40_59',
      label: '৪০% - ৫৯% (উন্নয়নশীল)',
      count: analytics.distribution_brackets.tier_40_59,
      color: 'bg-amber-600',
      textColor: 'text-amber-700 dark:text-amber-400',
      bgLight: 'bg-amber-50 dark:bg-amber-950/40'
    },
    {
      key: 'tier_below_40',
      label: '৪০% এর কম (পুনরাবৃত্তি প্রয়োজন)',
      count: analytics.distribution_brackets.tier_below_40,
      color: 'bg-rose-600',
      textColor: 'text-rose-700 dark:text-rose-400',
      bgLight: 'bg-rose-50 dark:bg-rose-950/40'
    }
  ];

  return (
    <div className="bg-[#FAFAF8] dark:bg-[#0B132B] border-2 border-slate-300 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-sm transition-all duration-200 hover:shadow-md">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-200 dark:border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center shadow-sm">
            <BarChart3 className="w-6 h-6 text-amber-300" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-bold text-amber-800 dark:text-amber-300 uppercase tracking-wider font-display">
                সেকশন পারফরম্যান্স ডায়াগনস্টিক
              </span>
              <span className="text-xs text-slate-400">|</span>
              <span className="text-xs text-slate-600 dark:text-slate-400 font-bengali">
                {sectionName}
              </span>
            </div>
            <h3 className="text-lg sm:text-xl font-bold font-bengali text-slate-900 dark:text-white leading-snug">
              {examTitle}
            </h3>
          </div>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span className="text-xs font-medium font-bengali text-slate-700 dark:text-slate-300">
            গোপনীয়তা সুরক্ষিত (ব্যক্তিগত র্যাংক প্রদর্শন নিষিদ্ধ)
          </span>
        </div>
      </div>

      {/* Primary Statistical Matrix */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 my-6">
        <div className="bg-white dark:bg-slate-900/60 p-4 rounded-2xl border border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 mb-1">
            <Layers className="w-4 h-4 text-sky-600" />
            <span className="text-xs font-bengali">মোট পরীক্ষার্থী</span>
          </div>
          <div className="text-2xl font-bold font-mono tabular-nums text-slate-900 dark:text-white">
            {analytics.total_examinees}
          </div>
          <div className="text-[11px] text-slate-500 font-display">
            অংশগ্রহণকারী শিক্ষার্থী
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900/60 p-4 rounded-2xl border border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 mb-1">
            <TrendingUp className="w-4 h-4 text-emerald-600" />
            <span className="text-xs font-bengali">গড় নম্বর (Mean)</span>
          </div>
          <div className="text-2xl font-bold font-mono tabular-nums text-emerald-700 dark:text-emerald-400">
            {analytics.average_score.toFixed(1)} / 50
          </div>
          <div className="text-[11px] text-slate-500 font-display">
            গাণিতিক গড় মান
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900/60 p-4 rounded-2xl border border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 mb-1">
            <Award className="w-4 h-4 text-amber-600" />
            <span className="text-xs font-bengali">মধ্যমা (Median)</span>
          </div>
          <div className="text-2xl font-bold font-mono tabular-nums text-slate-900 dark:text-white">
            {analytics.median_score.toFixed(1)}
          </div>
          <div className="text-[11px] text-slate-500 font-display">
            মাঝামাঝি অবস্থানকারী স্কোর
          </div>
        </div>

        <div className="bg-white dark:bg-slate-900/60 p-4 rounded-2xl border border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-2 text-slate-500 dark:text-slate-400 mb-1">
            <Activity className="w-4 h-4 text-indigo-600" />
            <span className="text-xs font-bengali">পরিমিত ব্যবধান (Std Dev)</span>
          </div>
          <div className="text-2xl font-bold font-mono tabular-nums text-indigo-700 dark:text-indigo-400">
            {analytics.standard_deviation.toFixed(2)}
          </div>
          <div className="text-[11px] text-slate-500 font-display">
            দক্ষতার বিস্তার বা বৈচিত্র্য
          </div>
        </div>
      </div>

      {/* Visual Performance Distribution Curve */}
      <div className="bg-white dark:bg-slate-900/60 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 my-6">
        <div className="flex items-center justify-between mb-4">
          <h4 className="text-sm font-bold font-bengali text-slate-900 dark:text-white flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-[#0A2540]" />
            গ্রেড ও নম্বর বণ্টনের বিতরণ রেখাচিত্র (Histogram)
          </h4>
          <span className="text-xs text-slate-500 font-mono">
            সর্বোচ্চ: {analytics.highest_score} | সর্বনিম্ন: {analytics.lowest_score}
          </span>
        </div>

        <div className="space-y-3">
          {tiers.map((tier) => {
            const pct = Math.round((tier.count / total) * 100);
            return (
              <div key={tier.key} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bengali font-medium text-slate-700 dark:text-slate-300">
                    {tier.label}
                  </span>
                  <div className="flex items-center gap-2 font-mono tabular-nums">
                    <span className="font-bold text-slate-900 dark:text-white">{tier.count} জন</span>
                    <span className="text-slate-400">({pct}%)</span>
                  </div>
                </div>
                <div className="h-3 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${tier.color}`}
                    style={{ width: `${Math.max(4, pct)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Weak Topic Clusters & Pedagogical Remedial Guidance */}
      <div className="mt-6">
        <div className="flex items-center justify-between mb-3">
          <h4 className="text-sm font-bold font-bengali text-slate-900 dark:text-white flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-amber-700 dark:text-amber-400" />
            সেকশন দুর্বল বিষয় ক্লাস্টার ও নিরাময়মূলক শিক্ষক গাইডলাইন
          </h4>
          <span className="text-xs text-slate-500 font-display">
            স্বয়ংক্রিয় পেডাগোজিক্যাল বিশ্লেষণ
          </span>
        </div>

        {analytics.weak_topics.length === 0 ? (
          <div className="p-4 bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800 rounded-2xl flex items-center gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            <p className="text-xs font-bengali text-emerald-800 dark:text-emerald-300">
              অভিনন্দন! এই সেকশনের শিক্ষার্থীরা প্রতিটি বিষয়ে সন্তোষজনক পারদর্শিতা অর্জন করেছে।
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {analytics.weak_topics.map((topic, idx) => (
              <div
                key={idx}
                className="p-4 bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-2xl hover:border-amber-300 dark:hover:border-amber-700 transition-colors"
              >
                <div className="flex items-start justify-between gap-2 mb-2">
                  <span className="text-xs font-bold font-bengali text-slate-900 dark:text-white">
                    {topic.topic_name_bn}
                  </span>
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-mono font-bold bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 whitespace-nowrap">
                    সঠিকতা {topic.accuracy_percent.toFixed(1)}%
                  </span>
                </div>
                <div className="flex items-start gap-2 text-xs font-bengali text-slate-600 dark:text-slate-400 bg-amber-50/50 dark:bg-amber-950/20 p-2.5 rounded-xl border border-amber-200/50 dark:border-amber-900/30">
                  <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                  <p className="leading-relaxed">{topic.remedial_tip_bn}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
