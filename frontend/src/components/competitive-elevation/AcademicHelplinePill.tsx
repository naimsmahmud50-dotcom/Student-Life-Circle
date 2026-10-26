/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Academic 24/7 Helpline & Scholar Support Pill
 * TOPIC:     10MS 16910 Helpline UX Pattern Adapted for Ogrojatra
 * FILE:      frontend/src/components/competitive-elevation/AcademicHelplinePill.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, Sanitized Tel URI, Accessible Disclosure, Zero-CLS
 */

import React, { useState } from 'react';
import Link from 'next/link';
import { PhoneCall, X, Headphones, Sparkles, MessageSquare, Clock } from 'lucide-react';

interface AcademicHelplinePillProps {
  className?: string;
  shortCode?: string;
}

export const AcademicHelplinePill: React.FC<AcademicHelplinePillProps> = ({
  className = '',
  shortCode = '16910',
}) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <aside
      aria-label="সার্বক্ষণিক একাডেমিক সহায়তা"
      className={`fixed bottom-5 right-5 z-40 ${className}`}
    >
      {/* Expanded Support Card */}
      {isOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="helpline-dialog-title"
          className="mb-3 w-80 max-w-[calc(100vw-2.5rem)] bg-white rounded-2xl border border-slate-200 shadow-xl p-4 sm:p-5 text-left animate-in fade-in slide-in-from-bottom-2 duration-150"
        >
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center">
                <Headphones className="w-4 h-4" />
              </div>
              <div>
                <h4 id="helpline-dialog-title" className="text-sm font-bold text-slate-900 leading-tight">
                  একাডেমিক সহায়তা ডেস্ক
                </h4>
                <div className="flex items-center gap-1 text-[11px] text-emerald-700 font-medium">
                  <Clock className="w-3 h-3" />
                  <span>২৪ ঘণ্টা সার্বক্ষণিক উন্মুক্ত</span>
                </div>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              aria-label="সহায়তা উইন্ডো বন্ধ করুন"
              className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="py-3 text-xs text-slate-600 leading-relaxed">
            কোর্স ভর্তি, লাইভ অলিম্পিয়াড রেজিস্ট্রেশন বা অ্যাকাডেমিক যেকোনো পরামর্শের জন্য সরাসরি কথা বলুন আমাদের অভিজ্ঞ শিক্ষা উপদেষ্টাদের সাথে।
          </div>

          <div className="space-y-2">
            <a
              href={`tel:${shortCode}`}
              className="flex items-center justify-center gap-2 w-full py-2.5 px-4 rounded-xl bg-emerald-800 hover:bg-emerald-900 active:bg-emerald-950 text-white font-bold text-sm shadow-sm transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 focus-visible:ring-offset-2"
            >
              <PhoneCall className="w-4 h-4" />
              <span>কল করুন: ১৬৯১০ (টোল ফ্রি)</span>
            </a>

            <Link
              href="/socratic"
              onClick={() => setIsOpen(false)}
              className="flex items-center justify-center gap-2 w-full py-2 px-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium text-xs transition-colors"
            >
              <Sparkles className="w-3.5 h-3.5 text-emerald-700" />
              <span>সক্রেটিক এআই চ্যাটে প্রশ্ন করুন</span>
            </Link>
          </div>
        </div>
      )}

      {/* Floating Trigger Pill */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="dialog"
        className="flex items-center gap-2 px-4 py-2.5 rounded-full bg-emerald-800 hover:bg-emerald-900 active:bg-emerald-950 text-white font-semibold text-xs sm:text-sm shadow-lg shadow-emerald-950/20 border border-emerald-700 transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-600 focus-visible:ring-offset-2"
      >
        <div className="relative flex items-center justify-center">
          <PhoneCall className="w-4 h-4" />
          <span className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
        </div>
        <span className="font-serif">সহায়তা: {shortCode}</span>
      </button>
    </aside>
  );
};
