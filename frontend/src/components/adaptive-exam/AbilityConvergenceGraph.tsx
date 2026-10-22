/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Psychometric Visualization & Ability Graph
 * TOPIC:     3-PL Item Response Theory (IRT) Ability Convergence Graph
 * FILE:      frontend/src/components/adaptive-exam/AbilityConvergenceGraph.tsx
 * PHASE:     Phase 105 - AI Adaptive CAT Examination Tower
 * PURPOSE:   Provides an HTML5 SVG visualizer displaying the examinee's latent ability
 *            trajectory (Theta), 95% confidence corridor (Theta +/- 1.96 * SE),
 *            and dynamic Fisher Information convergence with emerald glow styling.
 * STANDARDS: UI/UX Pro Max, IRT 3-PL Latent Ability Math, Zero-Emoji, Human-Centric
 */

import React, { useMemo } from 'react';
import { TrendingUp, Target, ShieldCheck, Compass, CheckCircle2 } from 'lucide-react';

export interface TrajectoryPoint {
  step: number;
  theta: number;
  standard_error: number;
  difficulty_b: number;
  is_correct: boolean;
}

export interface AbilityConvergenceGraphProps {
  trajectory: TrajectoryPoint[];
  currentTheta: number;
  standardError: number;
  targetSe?: number;
  percentileRank?: number;
  admissionReadiness?: string;
  className?: string;
}

export const AbilityConvergenceGraph: React.FC<AbilityConvergenceGraphProps> = ({
  trajectory,
  currentTheta,
  standardError,
  targetSe = 0.25,
  percentileRank = 50.0,
  admissionReadiness = 'উচ্চ মাধ্যমিক এ প্লাস প্রত্যাশী',
  className = '',
}) => {
  // SVG Dimensions & Padding
  const width = 640;
  const height = 280;
  const padding = { top: 32, right: 32, bottom: 44, left: 56 };
  const graphWidth = width - padding.left - padding.right;
  const graphHeight = height - padding.top - padding.bottom;

  const minTheta = -3.0;
  const maxTheta = 3.0;
  const maxSteps = Math.max(trajectory.length, 10);

  // Coordinate Mapping
  const getX = (step: number) => padding.left + ((step - 1) / Math.max(maxSteps - 1, 1)) * graphWidth;
  const getY = (theta: number) => {
    const clamped = Math.max(minTheta, Math.min(maxTheta, theta));
    const normalized = (clamped - minTheta) / (maxTheta - minTheta);
    return padding.top + (1 - normalized) * graphHeight;
  };

  // Generate SVG Path for Theta Trajectory
  const linePath = useMemo(() => {
    if (trajectory.length === 0) return '';
    return trajectory
      .map((pt, i) => `${i === 0 ? 'M' : 'L'} ${getX(pt.step)} ${getY(pt.theta)}`)
      .join(' ');
  }, [trajectory]);

  // Generate SVG Polygon for 95% Confidence Corridor (Theta +/- 1.96 * SE)
  const confidenceAreaPath = useMemo(() => {
    if (trajectory.length === 0) return '';
    const upperPoints = trajectory.map(
      (pt) => `${getX(pt.step)} ${getY(Math.min(maxTheta, pt.theta + 1.96 * pt.standard_error))}`
    );
    const lowerPoints = [...trajectory]
      .reverse()
      .map((pt) => `${getX(pt.step)} ${getY(Math.max(minTheta, pt.theta - 1.96 * pt.standard_error))}`);
    return `M ${upperPoints.join(' L ')} L ${lowerPoints.join(' L ')} Z`;
  }, [trajectory]);

  const thetaTicks = [-2.0, -1.0, 0.0, 1.0, 2.0];

  return (
    <div className={`p-6 rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-xl transition-all ${className}`}>
      {/* Header & Psychometric Metadata */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-5 border-b border-slate-100 dark:border-slate-800/80">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 dark:bg-emerald-950/60 border border-emerald-200/60 dark:border-emerald-800/60 text-emerald-600 dark:text-emerald-400 text-xs font-semibold">
            <Compass className="w-3.5 h-3.5" strokeWidth={1.75} />
            <span className="font-bengali">আইআরটি ৩-পিএল সামর্থ্য রূপরেখা</span>
          </div>
          <h3 className="text-lg font-bold font-bengali text-slate-900 dark:text-white flex items-center gap-2">
            <span>দক্ষতা অভিসরণ গতিপ্রকৃতি (Ability Convergence)</span>
          </h3>
        </div>

        {/* Live Percentile & Error Readout */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-xs text-slate-500 dark:text-slate-400 font-bengali">জাতীয় পারসেন্টাইল</div>
            <div className="text-xl font-black font-display text-emerald-600 dark:text-emerald-400">
              {percentileRank.toFixed(1)}%
            </div>
          </div>
          <div className="h-8 w-px bg-slate-200 dark:bg-slate-700" />
          <div className="text-right">
            <div className="text-xs text-slate-500 dark:text-slate-400 font-bengali">পরিমাপ ত্রুটি (SE)</div>
            <div className="text-sm font-mono font-bold text-slate-800 dark:text-slate-200">
              ±{standardError.toFixed(3)}
            </div>
          </div>
        </div>
      </div>

      {/* SVG Canvas Chart */}
      <div className="relative w-full overflow-x-auto pt-4">
        <svg
          viewBox={`0 0 ${width} ${height}`}
          className="w-full h-auto min-w-[540px] select-none"
        >
          <defs>
            {/* Emerald Glow Filter */}
            <filter id="emerald-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>

            {/* Gradient for Confidence Band */}
            <linearGradient id="ci-gradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#10B981" stopOpacity="0.25" />
              <stop offset="50%" stopColor="#10B981" stopOpacity="0.10" />
              <stop offset="100%" stopColor="#10B981" stopOpacity="0.02" />
            </linearGradient>
          </defs>

          {/* Horizontal Gridlines & Theta Reference Marks */}
          {thetaTicks.map((tick) => {
            const y = getY(tick);
            return (
              <g key={tick}>
                <line
                  x1={padding.left}
                  y1={y}
                  x2={width - padding.right}
                  y2={y}
                  stroke="currentColor"
                  strokeDasharray={tick === 0 ? '0' : '4 4'}
                  className={
                    tick === 0
                      ? 'text-slate-300 dark:text-slate-700 stroke-[1.5]'
                      : 'text-slate-100 dark:text-slate-800/80 stroke-1'
                  }
                />
                <text
                  x={padding.left - 10}
                  y={y + 4}
                  textAnchor="end"
                  className="fill-slate-400 dark:fill-slate-500 text-[11px] font-mono"
                >
                  {tick > 0 ? `+${tick.toFixed(1)}` : tick.toFixed(1)}
                </text>
              </g>
            );
          })}

          {/* Vertical Step Markers */}
          {Array.from({ length: maxSteps }, (_, i) => i + 1).map((step) => {
            const x = getX(step);
            return (
              <g key={step}>
                <line
                  x1={x}
                  y1={padding.top}
                  x2={x}
                  y2={height - padding.bottom}
                  stroke="currentColor"
                  className="text-slate-100 dark:text-slate-800/60 stroke-1"
                  strokeDasharray="2 4"
                />
                <text
                  x={x}
                  y={height - padding.bottom + 20}
                  textAnchor="middle"
                  className="fill-slate-400 dark:fill-slate-500 text-[11px] font-mono"
                >
                  Q{step}
                </text>
              </g>
            );
          })}

          {/* 95% Confidence Band Area */}
          {confidenceAreaPath && (
            <path d={confidenceAreaPath} fill="url(#ci-gradient)" />
          )}

          {/* Theta Trajectory Polyline */}
          {linePath && (
            <path
              d={linePath}
              fill="none"
              stroke="#10B981"
              strokeWidth="3.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              filter="url(#emerald-glow)"
            />
          )}

          {/* Data Points */}
          {trajectory.map((pt) => {
            const cx = getX(pt.step);
            const cy = getY(pt.theta);
            return (
              <g key={pt.step}>
                {/* Outer Ring */}
                <circle
                  cx={cx}
                  cy={cy}
                  r={5.5}
                  className={
                    pt.is_correct
                      ? 'fill-emerald-500 stroke-white dark:stroke-slate-900 stroke-2'
                      : 'fill-amber-500 stroke-white dark:stroke-slate-900 stroke-2'
                  }
                />
              </g>
            );
          })}

          {/* Active Tip Pulse Ring */}
          {trajectory.length > 0 && (
            <g>
              <circle
                cx={getX(trajectory[trajectory.length - 1].step)}
                cy={getY(trajectory[trajectory.length - 1].theta)}
                r={10}
                className="fill-emerald-500/20 stroke-emerald-400 animate-pulse stroke-1"
              />
            </g>
          )}
        </svg>
      </div>

      {/* Footer Diagnostic Note */}
      <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between text-xs gap-2">
        <div className="flex items-center gap-2 text-slate-600 dark:text-slate-300 font-bengali">
          <ShieldCheck className="w-4 h-4 text-emerald-500" strokeWidth={1.75} />
          <span>প্রাক্কলিত সামর্থ্য:</span>
          <span className="font-semibold text-emerald-600 dark:text-emerald-400 font-display">
            {admissionReadiness}
          </span>
        </div>

        <div className="text-slate-400 font-mono text-[11px]">
          Target SE &lt; {targetSe.toFixed(2)} | Current: {standardError.toFixed(3)}
        </div>
      </div>
    </div>
  );
};

export default AbilityConvergenceGraph;
