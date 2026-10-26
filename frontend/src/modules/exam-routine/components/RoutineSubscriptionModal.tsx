/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    RoutineSubscriptionModal Component
 * TOPIC:     Exam Routine Reminder Channel Selector & One-Click Subscription Modal
 * FILE:      frontend/src/modules/exam-routine/components/RoutineSubscriptionModal.tsx
 * PURPOSE:   Provides multi-channel alert subscription for upcoming daily routines
 *            and Friday Mega Model Tests via in-app push and browser alerts.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA, Zero-Emoji
 * ========================================================================================
 */

import React, { useState } from 'react';
import { X, Bell, CheckCircle2, ShieldCheck, Smartphone, Mail } from 'lucide-react';
import { ExamRoutineItem } from '../types/examRoutine.types';

interface RoutineSubscriptionModalProps {
  routine: ExamRoutineItem | null;
  onClose: () => void;
  onSubscribe: (routineId: string, channels: string[]) => Promise<{ message: string }>;
}

export const RoutineSubscriptionModal: React.FC<RoutineSubscriptionModalProps> = ({
  routine,
  onClose,
  onSubscribe,
}) => {
  const [channels, setChannels] = useState<string[]>(['IN_APP', 'PUSH']);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  if (!routine) return null;

  const toggleChannel = (channel: string) => {
    if (channels.includes(channel)) {
      if (channels.length > 1) {
        setChannels(channels.filter((c) => c !== channel));
      }
    } else {
      setChannels([...channels, channel]);
    }
  };

  const handleConfirm = async () => {
    setIsSubmitting(true);
    try {
      const res = await onSubscribe(routine.id, channels);
      setSuccessMessage(res.message);
      setTimeout(() => {
        onClose();
      }, 1800);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="sub-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm animate-in fade-in duration-200"
    >
      <div className="relative w-full max-w-md rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900 shadow-2xl p-6 space-y-5">
        {/* Header */}
        <div className="flex items-start justify-between border-b border-slate-100 pb-3 dark:border-slate-800">
          <div className="space-y-1">
            <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-600 dark:text-emerald-400">
              <Bell className="h-4 w-4" />
              <span>পরীক্ষা অনুস্মারক নির্ধারণ</span>
            </span>
            <h2 id="sub-modal-title" className="text-base font-serif font-bold text-slate-900 dark:text-slate-100">
              {routine.title}
            </h2>
          </div>

          <button
            type="button"
            onClick={onClose}
            aria-label="মডাল বন্ধ করুন"
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-800 dark:hover:text-slate-200 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        {successMessage ? (
          <div className="rounded-xl border border-emerald-300 bg-emerald-50 p-5 text-center dark:border-emerald-900/60 dark:bg-emerald-950/30 space-y-2">
            <CheckCircle2 className="h-8 w-8 text-emerald-600 mx-auto" />
            <h3 className="text-sm font-semibold text-emerald-800 dark:text-emerald-200">
              অ্যালার্ট নিশ্চিত হয়েছে
            </h3>
            <p className="text-xs text-emerald-700 dark:text-emerald-300">
              {successMessage}
            </p>
          </div>
        ) : (
          <div className="space-y-4 text-xs text-slate-600 dark:text-slate-300">
            <p>
              পরীক্ষা শুরুর ৩০ মিনিট পূর্বে আপনাকে স্বয়ংক্রিয় রিমাইন্ডার পাঠানো হবে যাতে কোনো মডেল টেস্ট বাদ না পড়ে।
            </p>

            <div className="space-y-2.5">
              <span className="font-semibold text-slate-800 dark:text-slate-200">
                নোটিফিকেশন চ্যানেল নির্বাচন করুন:
              </span>

              {/* In App Option */}
              <label 
                onClick={() => toggleChannel('IN_APP')}
                className={`flex items-center justify-between p-3 rounded-lg border cursor-pointer transition-colors ${
                  channels.includes('IN_APP')
                    ? 'border-emerald-500 bg-emerald-50/50 dark:border-emerald-500/60 dark:bg-emerald-950/20'
                    : 'border-slate-200 dark:border-slate-800'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Bell className="h-4 w-4 text-emerald-600" />
                  <div>
                    <span className="font-semibold text-slate-800 dark:text-slate-200">ইন-অ্যাপ ড্রয়ার নোটিফিকেশন</span>
                    <p className="text-[11px] text-slate-500">অগ্রযাত্রা ওয়েব পোর্টালে নোটিফিকেশন ডায়লগ</p>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={channels.includes('IN_APP')}
                  onChange={() => {}}
                  className="rounded text-emerald-600 focus:ring-emerald-500 h-4 w-4"
                />
              </label>

              {/* Browser Push Option */}
              <label 
                onClick={() => toggleChannel('PUSH')}
                className={`flex items-center justify-between p-3 rounded-lg border cursor-pointer transition-colors ${
                  channels.includes('PUSH')
                    ? 'border-emerald-500 bg-emerald-50/50 dark:border-emerald-500/60 dark:bg-emerald-950/20'
                    : 'border-slate-200 dark:border-slate-800'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Smartphone className="h-4 w-4 text-emerald-600" />
                  <div>
                    <span className="font-semibold text-slate-800 dark:text-slate-200">মোবাইল ও ব্রাউজার পুশ</span>
                    <p className="text-[11px] text-slate-500">ডিভাইস ডিসপ্লেতে ইনস্ট্যান্ট অ্যালার্ট</p>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={channels.includes('PUSH')}
                  onChange={() => {}}
                  className="rounded text-emerald-600 focus:ring-emerald-500 h-4 w-4"
                />
              </label>

              {/* Email Option */}
              <label 
                onClick={() => toggleChannel('EMAIL')}
                className={`flex items-center justify-between p-3 rounded-lg border cursor-pointer transition-colors ${
                  channels.includes('EMAIL')
                    ? 'border-emerald-500 bg-emerald-50/50 dark:border-emerald-500/60 dark:bg-emerald-950/20'
                    : 'border-slate-200 dark:border-slate-800'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Mail className="h-4 w-4 text-emerald-600" />
                  <div>
                    <span className="font-semibold text-slate-800 dark:text-slate-200">ইমেইল সারসংক্ষেপ</span>
                    <p className="text-[11px] text-slate-500">নিবন্ধিত ইমেইলে সিলেবাস ও লিংক পাঠানো</p>
                  </div>
                </div>
                <input
                  type="checkbox"
                  checked={channels.includes('EMAIL')}
                  onChange={() => {}}
                  className="rounded text-emerald-600 focus:ring-emerald-500 h-4 w-4"
                />
              </label>
            </div>

            <div className="pt-2 flex items-center justify-end gap-2.5">
              <button
                type="button"
                onClick={onClose}
                className="rounded-lg border border-slate-300 px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
              >
                বাতিল
              </button>

              <button
                type="button"
                onClick={handleConfirm}
                disabled={isSubmitting || channels.length === 0}
                className="rounded-lg bg-emerald-600 hover:bg-emerald-500 px-4 py-2 text-xs font-semibold text-white transition-colors disabled:opacity-50"
              >
                {isSubmitting ? 'সংরক্ষণ করা হচ্ছে...' : 'অ্যালার্ট নিশ্চিত করুন'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
