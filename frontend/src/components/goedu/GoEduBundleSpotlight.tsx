import React from 'react';
import Link from 'next/link';
import { CheckCircle2, ArrowRight, Sparkles, Layers, BookOpen, Clock } from 'lucide-react';
import { GOEDU_BUNDLES } from '../../data/goeduData';

export const GoEduBundleSpotlight: React.FC = () => {
  const featuredBundle = GOEDU_BUNDLES[0];

  return (
    <section className="py-12 sm:py-16 px-4 sm:px-6 lg:px-8 container mx-auto">
      <div className="relative border border-amber-200/70 dark:border-gray-700 rounded-[2.5rem] overflow-hidden p-6 sm:p-10 lg:p-14 bg-gradient-to-br from-amber-500/10 via-[#FFF6DD]/40 to-white dark:from-gray-800 dark:via-gray-800/80 dark:to-gray-900 shadow-md">
        <div className="flex flex-col lg:flex-row items-center justify-between gap-10 lg:gap-14">
          {/* Left Content */}
          <div className="flex-1 text-center lg:text-left flex flex-col items-center lg:items-start max-w-2xl">
            {/* Pill Tag */}
            <div className="inline-flex items-center gap-2 py-1.5 px-4 bg-white dark:bg-gray-700 rounded-full border border-amber-200 dark:border-gray-600 shadow-sm mb-4">
              <span className="h-2 w-2 rounded-full bg-[#ED8E22] animate-pulse" aria-hidden="true" />
              <span className="text-xs sm:text-sm font-bold text-gray-800 dark:text-gray-100">
                {featuredBundle.tag}
              </span>
            </div>

            {/* Title */}
            <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-black text-[#1E293B] dark:text-white mb-4 leading-tight">
              {featuredBundle.bengaliTitle}
            </h2>

            {/* Subtitle / Description */}
            <p className="text-gray-600 dark:text-gray-300 text-sm sm:text-base leading-relaxed mb-6">
              {featuredBundle.description}
            </p>

            {/* Highlights List */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 mb-8 w-full text-left">
              {featuredBundle.highlights.map((item, idx) => (
                <div key={idx} className="flex items-center gap-2 text-xs sm:text-sm text-gray-700 dark:text-gray-200 font-medium">
                  <CheckCircle2 className="w-4 h-4 text-[#ED8E22] shrink-0" aria-hidden="true" />
                  <span>{item}</span>
                </div>
              ))}
            </div>

            {/* Price & Action */}
            <div className="flex flex-col sm:flex-row items-center gap-4 sm:gap-6 w-full sm:w-auto">
              <div className="flex items-baseline gap-2">
                <span className="text-2xl sm:text-3xl font-extrabold text-[#ED8E22]">
                  ৳{featuredBundle.bundlePrice}
                </span>
                <span className="text-sm sm:text-base line-through text-gray-400">
                  ৳{featuredBundle.originalPrice}
                </span>
                <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-2 py-0.5 rounded-full">
                  ৬৭% ছাড়
                </span>
              </div>

              <Link
                href={featuredBundle.routeLink}
                className="inline-flex items-center justify-center gap-2 px-6 sm:px-8 py-3 rounded-full bg-[#1E293B] dark:bg-amber-500 text-white dark:text-gray-900 hover:bg-gray-800 dark:hover:bg-amber-400 active:scale-95 transition-all font-semibold text-sm sm:text-base shadow-md"
              >
                <span>বান্ডেল বিস্তারিত দেখুন</span>
                <ArrowRight className="w-4 h-4" aria-hidden="true" />
              </Link>
            </div>
          </div>

          {/* Right Visual Card Stack */}
          <div className="w-full lg:w-5/12 max-w-md">
            <div className="relative p-6 bg-white dark:bg-gray-800 rounded-3xl border border-gray-200 dark:border-gray-700 shadow-xl">
              <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-700">
                <span className="text-xs font-bold text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/60 px-3 py-1 rounded-full">
                  ৫টি কোর্স প্যাকেজ
                </span>
                <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
                  <Clock className="w-3.5 h-3.5" aria-hidden="true" />
                  <span>৩০+ ঘন্টা লাইভ ও রেকর্ডেড</span>
                </div>
              </div>

              <div className="space-y-3 py-4">
                <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-700/50 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-amber-100 dark:bg-amber-900/60 flex items-center justify-center text-[#ED8E22]">
                    <Sparkles className="w-4 h-4" aria-hidden="true" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-gray-900 dark:text-white truncate">
                      জেনারেটিভ এআই ও প্রম্পট ইঞ্জিনিয়ারিং
                    </p>
                    <p className="text-[11px] text-gray-500 dark:text-gray-400">১০টি প্র্যাক্টিক্যাল প্রজেক্ট</p>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-700/50 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/60 flex items-center justify-center text-blue-600 dark:text-blue-400">
                    <BookOpen className="w-4 h-4" aria-hidden="true" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-gray-900 dark:text-white truncate">
                      এইচএসসি স্টেম ও ক্যালকুলাস অ্যাপ্লিকেশন
                    </p>
                    <p className="text-[11px] text-gray-500 dark:text-gray-400">বোর্ড প্রশ্ন ও সলভার গাইড</p>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-gray-50 dark:bg-gray-700/50 flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-900/60 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
                    <Layers className="w-4 h-4" aria-hidden="true" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-gray-900 dark:text-white truncate">
                      ক্যারিয়ার রেডিনেস ও কর্পোরেট সফট স্কিলস
                    </p>
                    <p className="text-[11px] text-gray-500 dark:text-gray-400">সিভি ও ইন্টারভিউ প্রেপারেশন</p>
                  </div>
                </div>
              </div>

              <div className="pt-2 text-center">
                <span className="text-[11px] text-gray-500 dark:text-gray-400">
                  এনরোল করলেই আজীবন লাইব্রেরি এক্সেস ও নো-কস্ট রিভিশন
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
