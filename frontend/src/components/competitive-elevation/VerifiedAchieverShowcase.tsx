/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Verified Achiever Showcase & Institutional Testimonials
 * TOPIC:     Academic Rigor & Social Proof with Authentic Scholar Monograms (Zero 10MS Photo Assets)
 * FILE:      frontend/src/components/competitive-elevation/VerifiedAchieverShowcase.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, Authentic Academic Monograms, Strict Originality, WCAG 2.2 AAA
 */

import React from 'react';
import { VERIFIED_ACHIEVERS } from './data/academicElevationData';
import { BadgeCheck, Quote, School, Award } from 'lucide-react';

interface VerifiedAchieverShowcaseProps {
  className?: string;
}

export const VerifiedAchieverShowcase: React.FC<VerifiedAchieverShowcaseProps> = ({
  className = '',
}) => {
  return (
    <section className={`w-full py-8 ${className}`} aria-labelledby="achievers-showcase-heading">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-8 px-2 gap-4">
        <div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-200 uppercase tracking-wider">
            <Award className="w-3.5 h-3.5" />
            <span>ভেরিফায়েড জাতীয় মেধা তালিকা</span>
          </span>
          <h2
            id="achievers-showcase-heading"
            className="mt-2 text-2xl sm:text-3xl font-bold font-serif text-slate-900 leading-tight"
          >
            দেশসেরা শিক্ষার্থীদের সাফল্যের অভিজ্ঞতা
          </h2>
          <p className="mt-1 text-sm text-slate-600">
            বোর্ড, বিশ্ববিদ্যালয় ও প্রতিযোগিতামূলক পরীক্ষায় অগ্রযাত্রার শিক্ষার্থীদের বাস্তব সাফল্য
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs text-slate-500 bg-white px-3 py-2 rounded-xl border border-slate-200">
          <BadgeCheck className="w-4 h-4 text-emerald-600" />
          <span>শিক্ষা প্রতিষ্ঠান ও জাতীয় বোর্ড কর্তৃক ভেরিফায়েড</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 px-1">
        {VERIFIED_ACHIEVERS.map((achiever) => (
          <div
            key={achiever.id}
            className="flex flex-col justify-between bg-white rounded-2xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition-shadow duration-200 relative"
          >
            <Quote className="absolute top-4 right-4 w-6 h-6 text-slate-200 -z-0 pointer-events-none" />

            <div>
              {/* Scholar Monogram Crest Header (Zero 10MS scraped photos) */}
              <div className="flex items-center gap-3 mb-4">
                <div
                  className={`w-11 h-11 rounded-full border-2 flex items-center justify-center font-bold text-base font-serif shadow-sm ${achiever.accentBg}`}
                >
                  {achiever.initials}
                </div>
                <div>
                  <h3 className="font-bold text-sm text-slate-900 leading-snug">
                    {achiever.nameBn}
                  </h3>
                  <div className="flex items-center gap-1 text-[11px] text-slate-500 mt-0.5">
                    <School className="w-3 h-3 text-slate-400" />
                    <span className="truncate max-w-[170px]">{achiever.institutionBn}</span>
                  </div>
                </div>
              </div>

              {/* Achievement Badge */}
              <div className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-900 text-xs font-semibold mb-3">
                <BadgeCheck className="w-3.5 h-3.5 text-emerald-700" />
                <span>{achiever.milestoneBn}</span>
              </div>

              {/* Quote text */}
              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed italic">
                &ldquo;{achiever.quoteBn}&rdquo;
              </p>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400 font-medium">
              <span>{achiever.batchBn}</span>
              <span className="text-emerald-700 font-semibold">ভেরিফায়েড শিক্ষার্থী</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};
