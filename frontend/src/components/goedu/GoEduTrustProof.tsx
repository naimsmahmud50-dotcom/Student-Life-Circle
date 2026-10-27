import React from 'react';
import { Star, Shield, ThumbsUp } from 'lucide-react';

export const GoEduTrustProof: React.FC = () => {
  return (
    <section className="py-14 sm:py-16 px-4 sm:px-6 lg:px-8 bg-[#FFFCF6] dark:bg-gray-900 transition-colors duration-300">
      <div className="max-w-6xl mx-auto text-center">
        <h2 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-[#213130] dark:text-white mb-3 leading-tight">
          দেশজুড়ে হাজারো শিক্ষার্থীর আস্থার প্রতীক
        </h2>
        <p className="max-w-3xl mx-auto text-gray-600 dark:text-gray-300 text-sm sm:text-base mb-10 leading-relaxed">
          বাস্তব স্কিল ও পরীক্ষায় ধারাবাহিক সাফল্যের জন্য আমাদের ওপর আস্থা রাখেন শিক্ষার্থীরা। শীর্ষ রেটিং ও ভেরিফাইড
          রিভিউ আমাদের প্রতিশ্রুতির প্রমাণ।
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6 max-w-4xl mx-auto">
          {/* Google Reviews Card */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-5 sm:p-6 border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow flex flex-col items-center justify-center">
            <div className="flex items-center gap-1 mb-2 font-bold text-lg sm:text-xl">
              <span className="text-[#4285F4]">G</span>
              <span className="text-[#EA4335]">o</span>
              <span className="text-[#FBBC05]">o</span>
              <span className="text-[#4285F4]">g</span>
              <span className="text-[#34A853]">l</span>
              <span className="text-[#EA4335]">e</span>
              <span className="text-gray-700 dark:text-gray-200 text-sm ml-1">Reviews</span>
            </div>
            <div className="flex gap-1 mb-2 text-[#FBBC05]">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-4 h-4 fill-current" aria-hidden="true" />
              ))}
            </div>
            <span className="text-xs font-semibold text-gray-800 dark:text-gray-200">
              ৪.৯ / ৫.০ (১২,০০০+ শিক্ষার্থী)
            </span>
            <span className="text-[11px] text-gray-500 dark:text-gray-400 mt-1">
              যাচাইকৃত গুগল রেটিং
            </span>
          </div>

          {/* Trustpilot Card */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-5 sm:p-6 border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow flex flex-col items-center justify-center">
            <div className="flex items-center gap-1.5 mb-2">
              <div className="w-5 h-5 bg-[#00B67A] rounded-sm flex items-center justify-center text-white">
                <Star className="w-3.5 h-3.5 fill-current" aria-hidden="true" />
              </div>
              <span className="font-bold text-gray-900 dark:text-white tracking-tight text-base sm:text-lg">
                Trustpilot
              </span>
            </div>
            <div className="flex gap-1 mb-2">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className="w-4 h-4 bg-[#00B67A] rounded-[2px] flex items-center justify-center text-white"
                >
                  <Star className="w-2.5 h-2.5 fill-current" aria-hidden="true" />
                </div>
              ))}
            </div>
            <span className="text-xs font-semibold text-gray-800 dark:text-gray-200">
              ৪.৯৫ স্টার স্কোর
            </span>
            <span className="text-[11px] text-gray-500 dark:text-gray-400 mt-1">
              এক্সিলেন্ট ক্যাটাগরি সার্টিফিকেট
            </span>
          </div>

          {/* Facebook Recommendation Card */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-5 sm:p-6 border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow flex flex-col items-center justify-center">
            <div className="flex items-center gap-1.5 mb-1 text-[#0066F5]">
              <ThumbsUp className="w-5 h-5" aria-hidden="true" />
              <span className="font-bold text-base sm:text-lg">Facebook Review</span>
            </div>
            <div className="text-2xl sm:text-3xl font-extrabold text-[#0066F5] dark:text-[#3B82F6] my-1">
              ১০০%
            </div>
            <span className="text-xs font-semibold text-gray-800 dark:text-gray-200">
              লার্নারদের দ্বারা রেকমেন্ডেড
            </span>
            <span className="text-[11px] text-gray-500 dark:text-gray-400 mt-1">
              সামাজিক মাধ্যমে সক্রিয় ফিডব্যাক
            </span>
          </div>
        </div>
      </div>
    </section>
  );
};
