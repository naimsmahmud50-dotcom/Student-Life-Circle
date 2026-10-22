/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Dignified Academic Gamification
 * TOPIC:     Empathetic Streak Shield & Review Recovery Modal
 * FILE:      frontend/src/components/gamification/StreakShieldModal.tsx
 * PHASE:     Phase 102 - Dignified Gamification & Verifiable Social Proof
 * PURPOSE:   Provides an empathetic streak preservation and recovery dialog.
 *            Replaces punishing, toxic streak resets with mindful recovery drills,
 *            warm amber ambient glowing aesthetics, and zero-emoji compliance.
 * STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
 */

import React, { useState } from 'react';
import {
  Flame,
  ShieldCheck,
  CheckCircle2,
  Clock,
  ArrowRight,
  Sparkles,
  X,
  HeartHandshake,
  BookOpen
} from 'lucide-react';

export interface StreakShieldModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentStreak: number;
  availableShields: number;
  isStreakAtRisk?: boolean;
  onRecoverViaDrill?: () => void;
  onActivateShield?: () => void;
  className?: string;
}

export const StreakShieldModal: React.FC<StreakShieldModalProps> = ({
  isOpen,
  onClose,
  currentStreak = 24,
  availableShields = 2,
  isStreakAtRisk = false,
  onRecoverViaDrill,
  onActivateShield,
  className = ''
}) => {
  const [drillCompleted, setDrillCompleted] = useState<boolean>(false);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  if (!isOpen) return null;

  const handleStartDrill = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      setDrillCompleted(true);
      onRecoverViaDrill?.();
    }, 1200);
  };

  const handleClaimShield = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setIsProcessing(false);
      onActivateShield?.();
      onClose();
    }, 800);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 animate-in fade-in select-none font-bengali">
      <div
        className={`relative w-full max-w-lg p-6 sm:p-8 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800/80 shadow-2xl space-y-6 ${className}`}
      >
        {/* Close Button */}
        <button
          type="button"
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-full text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          title="বন্ধ করুন"
        >
          <X className="w-5 h-5" strokeWidth={1.75} />
        </button>

        {/* Ambient Amber Radiance Flame Header */}
        <div className="flex flex-col items-center text-center space-y-3 pt-2">
          <div className="relative">
            <div className="relative w-20 h-20 rounded-2xl bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800 flex items-center justify-center text-amber-600 dark:text-amber-400 shadow-xs">
              <Flame className="w-10 h-10 text-amber-600 dark:text-amber-400 fill-amber-500/20" strokeWidth={1.75} />
            </div>
            {/* Active Shield Floating Pill */}
            <div className="absolute -bottom-2 -right-2 px-2 py-0.5 rounded-full bg-blue-600 text-white text-[11px] font-bold font-numeric flex items-center gap-1 shadow-md">
              <ShieldCheck className="w-3 h-3" strokeWidth={2} />
              <span>{availableShields} টি শিল্ড</span>
            </div>
          </div>

          <div className="space-y-1">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white font-display">
              {currentStreak} দিনের অবিচল অধ্যবসায়
            </h2>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 dark:bg-amber-950/40 text-amber-600 dark:text-amber-400 border border-amber-200 dark:border-amber-800/60 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" strokeWidth={1.75} />
              <span>সহানুভূতিশীল স্ট্রিক সুরক্ষা</span>
            </div>
          </div>
        </div>

        {/* Empathetic Human Microcopy Callout */}
        <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 text-sm text-slate-700 dark:text-slate-300 leading-relaxed space-y-2">
          <div className="flex items-start gap-2.5">
            <HeartHandshake className="w-5 h-5 text-blue-500 mt-0.5 shrink-0" strokeWidth={1.75} />
            <p className="font-medium text-slate-800 dark:text-slate-200">
              "পড়াশোনা একটানা লড়াই নয়, বিরতি নেওয়াও জরুরি। তোমার স্ট্রিক সুরক্ষিত আছে।"
            </p>
          </div>
          <p className="text-xs text-slate-500 dark:text-slate-400 pl-7">
            অসুস্থতা কিংবা সেমিস্টার ফাইনাল পরীক্ষার কারণে পড়াশোনায় সাময়িক বিরতি সম্পূর্ণ স্বাভাবিক। আগ্রাসী গেমিং চাপের বদলে আমরা তোমার ধারাবাহিক প্রচেষ্টাকে সম্মান জানাই।
          </p>
        </div>

        {/* Action State: Drill Recovery vs Shield Activation */}
        {drillCompleted ? (
          <div className="p-4 rounded-2xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 text-center space-y-2 animate-in zoom-in-95">
            <div className="w-10 h-10 rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mx-auto">
              <CheckCircle2 className="w-6 h-6" strokeWidth={1.75} />
            </div>
            <h3 className="text-sm font-bold text-emerald-800 dark:text-emerald-300">
              স্ট্রিক সফলভাবে পুনরুদ্ধার হয়েছে!
            </h3>
            <p className="text-xs text-emerald-700 dark:text-emerald-400">
              একটি ৫ মিনিটের রিভিশন ড্রিল সম্পন্ন করায় তোমার অধ্যবসায় অক্ষুণ্ণ রাখা হয়েছে।
            </p>
          </div>
        ) : isStreakAtRisk ? (
          <div className="space-y-3">
            <div className="flex items-center justify-between text-xs text-slate-500 dark:text-slate-400 px-1">
              <span>পুনরুদ্ধার পদ্ধতি:</span>
              <span className="font-semibold text-blue-500">৫টি দ্রুত প্রশ্নের রিভিশন</span>
            </div>
            <button
              type="button"
              onClick={handleStartDrill}
              disabled={isProcessing}
              className="w-full btn-push-brand py-3 px-5 text-sm font-bold text-white bg-blue-600 rounded-2xl flex items-center justify-center gap-2 shadow-lg active:scale-95 transition-all disabled:opacity-50"
            >
              <BookOpen className="w-4 h-4" strokeWidth={1.75} />
              <span>{isProcessing ? 'যাচাই করা হচ্ছে...' : 'স্ট্রিক রিকভারি ড্রিল শুরু করুন'}</span>
              <ArrowRight className="w-4 h-4" strokeWidth={1.75} />
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-700 dark:text-amber-300">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-amber-500" strokeWidth={1.75} />
                <span>আজকের জন্য স্ট্রিক ফ্রিজ সক্রিয় করুন</span>
              </div>
              <span className="font-numeric font-bold">{availableShields} অবশিষ্ট</span>
            </div>

            <div className="flex items-center gap-2 pt-1">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 py-2.5 px-4 rounded-2xl border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-sm font-semibold hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
              >
                পরে করব
              </button>
              <button
                type="button"
                onClick={handleClaimShield}
                disabled={isProcessing || availableShields <= 0}
                className="flex-1 py-2.5 px-4 rounded-2xl bg-amber-600 hover:bg-amber-500 text-white text-sm font-semibold shadow-md active:scale-95 transition-all disabled:opacity-50"
              >
                {isProcessing ? 'সুরক্ষিত হচ্ছে...' : 'শিল্ড সক্রিয় করুন'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
