import React from 'react';
import { ShieldCheck, Sparkles, Swords, Award } from 'lucide-react';

export const GoEduTrustFactors: React.FC = () => {
  const factors = [
    {
      icon: ShieldCheck,
      title: 'জিইএসি ও প্রাতিষ্ঠানিক স্বীকৃতি',
      desc: 'জাতীয় ও আন্তর্জাতিক গুণগত মানদণ্ডে পর্যালোচিত কোর্স সিলেবাস এবং যাচাইকৃত বিষয়বস্তু।'
    },
    {
      icon: Sparkles,
      title: '২৪/৭ সক্রেটিক এআই টিউটর',
      desc: 'মুখস্থ নয়, ব্লুমস ট্যাক্সোনমি অনুসরণ করে ধাপে ধাপে জটিল গাণিতিক ও বৈজ্ঞানিক সমস্যা সমাধান।'
    },
    {
      icon: Swords,
      title: 'লাইভ চ্যালেঞ্জ ও থ্রিডি সিমুলেশন',
      desc: 'রিয়েল-টাইম কুইজ ব্যাটেল, পদার্থবিজ্ঞান ও রসায়নের ইন্টারেক্টিভ থ্রিডি ভিজ্যুয়াল এক্সপেরিমেন্ট।'
    },
    {
      icon: Award,
      title: 'সার্টিফিকেট ও ক্যারিয়ার প্লেসমেন্ট',
      desc: 'কোর্স সমাপ্তির পর ভেরিফায়েড ডিজিটাল সার্টিফিকেট এবং বিডিজবস ও ক্যারিয়ার রাডার সুবিধা।'
    }
  ];

  return (
    <section className="py-14 sm:py-20 px-4 sm:px-6 lg:px-8 bg-[#FFFCF6] dark:bg-gray-900 transition-colors duration-300">
      <div className="max-w-7xl mx-auto">
        <header className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center gap-2 py-1.5 px-4 border border-gray-300 dark:border-gray-700 rounded-full mb-3 bg-white dark:bg-gray-800 shadow-sm">
            <span className="h-2 w-2 rounded-full bg-[#ED8E22]" aria-hidden="true" />
            <p className="text-xs sm:text-sm font-semibold text-gray-800 dark:text-gray-200">
              আমাদের গুণগত মান ও প্রতিশ্রুতি
            </p>
          </div>
          <h2 className="text-2xl sm:text-4xl font-bold text-[#213130] dark:text-white mb-4 leading-tight">
            কেন শিক্ষার্থী, অভিভাবক ও শিক্ষাপ্রতিষ্ঠানগুলো আমাদের ওপর আস্থা রাখে?
          </h2>
          <p className="text-gray-600 dark:text-gray-300 text-sm sm:text-base leading-relaxed">
            অনলাইন শিক্ষার বিভ্রান্তি দূর করে সুশৃঙ্খল, তথ্যবহুল ও নির্ভরযোগ্য একাডেমিক গাইডেন্স নিশ্চিত করতে
            আমরা নিয়ে এসেছি সম্পূর্ণ সমন্বিত ডিজিটাল লার্নিং প্ল্যাটফর্ম।
          </p>
        </header>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {factors.map((factor, idx) => {
            const Icon = factor.icon;
            return (
              <div
                key={idx}
                className="bg-white dark:bg-gray-800 rounded-2xl p-6 border border-gray-200/80 dark:border-gray-700 shadow-sm hover:shadow-md transition-all duration-300 flex flex-col items-start group hover:-translate-y-1"
              >
                <div className="w-12 h-12 rounded-xl bg-amber-50 dark:bg-amber-950/60 border border-amber-200/60 dark:border-amber-800/40 flex items-center justify-center text-[#ED8E22] mb-4 group-hover:bg-[#ED8E22] group-hover:text-white transition-colors">
                  <Icon className="w-6 h-6" aria-hidden="true" />
                </div>
                <h3 className="font-bold text-base text-gray-900 dark:text-white mb-2">
                  {factor.title}
                </h3>
                <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                  {factor.desc}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
