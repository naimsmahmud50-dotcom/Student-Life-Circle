/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Live Examination & Nationwide Competitive Elevation
 * TOPIC:     Phase 142 Live MCQ Reverse Engineering & Competitive Superiority
 * FILE:      frontend/src/components/live-challenge/ExamRulesProtocolModal.tsx
 * PHASE:     Phase 142 - Live MCQ Competitive Elevation
 * PURPOSE:   Proctoring and exam ethics guidelines modal inspired by Live MCQ's anti-cheat rules,
 *            formalizing tab-switch guards, server sync, and negative marking standards.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Human Craftsmanship
 */

import React, { useEffect } from 'react';
import {
  ShieldCheck,
  Clock,
  AlertTriangle,
  Lock,
  WifiOff,
  CheckCircle2,
  X,
  FileText
} from 'lucide-react';

interface ExamRulesProtocolModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const ExamRulesProtocolModal: React.FC<ExamRulesProtocolModalProps> = ({
  isOpen,
  onClose
}) => {
  // Handle ESC key to close
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="exam-rules-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in"
    >
      <div 
        className="relative w-full max-w-2xl bg-white dark:bg-slate-900 rounded-3xl border-2 border-slate-200 dark:border-slate-800 shadow-2xl p-6 sm:p-8 space-y-6 max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-[#0A2540] dark:bg-slate-800 text-amber-300 flex items-center justify-center shrink-0">
              <ShieldCheck className="w-6 h-6 text-amber-300" />
            </div>
            <div>
              <h2 id="exam-rules-title" className="text-lg sm:text-xl font-bold font-bengali text-slate-900 dark:text-white">
                লাইভ পরীক্ষার নিয়মাবলী ও অ্যান্টি-চিট প্রোটোকল
              </h2>
              <p className="text-xs text-slate-500 font-bengali mt-0.5">
                অংশগ্রহণের পূর্বে প্রোটোকলগুলো মনোযোগ সহকারে পড়ুন।
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            aria-label="নিয়মাবলী বন্ধ করুন"
            className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 flex items-center justify-center transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Rules Content */}
        <div className="space-y-4 text-xs sm:text-sm font-bengali text-slate-700 dark:text-slate-300 leading-relaxed">
          {/* Rule 1: Server Timer */}
          <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex items-start gap-3">
            <Clock className="w-5 h-5 text-[#0A2540] dark:text-amber-300 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white mb-1">
                ১. সার্ভার-অথরিটেটিভ টাইমার ও অটো-সাবমিশন
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                পরীক্ষাটি সেন্ট্রাল সার্ভার ঘড়ির সাথে সিঙ্ক্রোনাইজড। স্থানীয় ডিভাইসের সময় পরিবর্তন করলেও কোনো প্রভাব পড়বে না। বরাদ্দকৃত সময় শেষ হওয়ার সাথে সাথে আপনার উত্তরপত্র স্বয়ংক্রিয়ভাবে জমা হয়ে যাবে।
              </p>
            </div>
          </div>

          {/* Rule 2: Tab Switching & Anti-Cheat */}
          <div className="p-4 rounded-2xl bg-[#991B1B]/5 dark:bg-[#991B1B]/15 border border-[#991B1B]/20 dark:border-[#991B1B]/40 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-[#991B1B] dark:text-rose-300 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-[#991B1B] dark:text-rose-300 mb-1">
                ২. অ্যান্টি-চিট গার্ড ও ট্যাব পরিবর্তন সতর্কতা
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                লাইভ চলাকালীন অন্য কোনো ব্রাউজার ট্যাব, উইন্ডো বা অ্যাপ্লিকেশনে সুইচ করলে সিস্টেম তা স্বয়ংক্রিয়ভাবে সনাক্ত করবে। ৩ বার পেজ পরিবর্তন বা ফোকাস হারালে উত্তরপত্র অন-দ্য-স্পট ডিসকোয়ালিফাই ও সাবমিট হতে পারে।
              </p>
            </div>
          </div>

          {/* Rule 3: Negative Marking */}
          <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex items-start gap-3">
            <FileText className="w-5 h-5 text-amber-700 dark:text-amber-400 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white mb-1">
                ৩. নেগেটিভ মার্কিং পদ্ধতি (-০.২৫)
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                প্রতিটি ভুল উত্তরের জন্য ০.২৫ নম্বর কর্তন করা হবে। যে প্রশ্নের উত্তর দেওয়া হবে না, তার জন্য কোনো নম্বর কাটা হবে না। নিশ্চিত না হয়ে আন্দাজে উত্তর দেওয়া থেকে বিরত থাকুন।
              </p>
            </div>
          </div>

          {/* Rule 4: Offline Resilience */}
          <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex items-start gap-3">
            <WifiOff className="w-5 h-5 text-emerald-700 dark:text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white mb-1">
                ৪. অফলাইন বাফার ও মিলি-সেকেন্ড নেটওয়ার্ক রেজিলিয়েন্স
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                পরীক্ষার মাঝে ইন্টারনেট সংযোগ বিচ্ছিন্ন হলে আতঙ্কিত হবেন না। আপনার সিলেক্ট করা উত্তরগুলো স্থানীয় মেমরিতে নিরাপদে এনক্রিপ্টেড থাকবে এবং সংযোগ ফিরে আসার সাথে সাথে ব্যাকগ্রাউন্ডে সিঙ্ক হবে।
              </p>
            </div>
          </div>

          {/* Rule 5: Privacy */}
          <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex items-start gap-3">
            <Lock className="w-5 h-5 text-slate-700 dark:text-slate-300 shrink-0 mt-0.5" />
            <div>
              <h3 className="font-bold text-slate-900 dark:text-white mb-1">
                ৫. গোপনীয়তা ও ছদ্মনাম লিডারবোর্ড
              </h3>
              <p className="text-slate-600 dark:text-slate-400">
                শিক্ষার্থীদের সুরক্ষায় লিডারবোর্ডে ফোন নম্বর সম্পূর্ণ গোপন রাখা হয়। আপনি চাইলে সেটিংস থেকে পাবলিক লিডারবোর্ড র‍্যাঙ্কিংয়ে আপনার স্কোর গোপন রাখার বিকল্প নির্বাচন করতে পারেন।
              </p>
            </div>
          </div>
        </div>

        {/* Footer / Acknowledgment */}
        <div className="pt-4 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-xs font-bengali text-emerald-700 dark:text-emerald-400">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>প্রোটোকলগুলো এনসিটিবি ও জাতীয় প্রতিযোগিতামূলক নীতিমালার সাথে সামঞ্জস্যপূর্ণ</span>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-[#0A2540] text-white hover:bg-slate-800 font-bold font-bengali text-xs transition min-h-[44px]"
          >
            আমি নিয়মাবলী বুঝেছি ও একমত
          </button>
        </div>
      </div>
    </div>
  );
};
