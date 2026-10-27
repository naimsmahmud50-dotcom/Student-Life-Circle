import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { Search, Sparkles, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';

interface GoEduHeroProps {
  onSearchSubmit?: (query: string) => void;
  onOpenSocraticDrawer?: () => void;
}

export const GoEduHero: React.FC<GoEduHeroProps> = ({
  onSearchSubmit,
  onOpenSocraticDrawer
}) => {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSearchSubmit) {
      onSearchSubmit(searchQuery);
    } else {
      router.push(`/courses?query=${encodeURIComponent(searchQuery)}`);
    }
  };

  const quickTags = [
    { label: 'ক্যালকুলাস', query: 'calculus' },
    { label: 'গতিবিদ্যা ও প্রক্ষেপক', query: 'physics' },
    { label: 'বুলিয়ান অ্যালজেব্রা', query: 'ict' },
    { label: 'ভার্সিটি ও বুয়েট এডমিশন', query: 'admission' },
    { label: 'জেনারেটিভ এআই', query: 'ai' },
  ];

  return (
    <section
      aria-labelledby="hero-heading"
      className="hero-section relative z-30 w-full bg-[#FFF6DD] dark:bg-gray-900 flex flex-col pt-24 sm:pt-28 pb-12 sm:pb-16 overflow-hidden transition-colors duration-300"
    >
      {/* Background Radial Glow */}
      <div
        className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
        style={{
          height: '65vh',
          minHeight: '380px',
          background:
            'radial-gradient(ellipse 65% 90% at 50% 100%, rgba(255, 178, 0, 0.70) 0%, rgba(243, 172, 8, 0.35) 45%, rgba(253, 215, 70, 0) 100%)'
        }}
        aria-hidden="true"
      />

      {/* Giant Typographic Watermark (GoEdu Signature) */}
      <div
        className="absolute z-0 pointer-events-none select-none w-full top-12 left-0 flex justify-center overflow-hidden"
        aria-hidden="true"
      >
        <p
          className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[24vw] md:text-[clamp(4rem,26vw,24rem)] uppercase tracking-wider"
          style={{
            lineHeight: 0.95,
            backgroundImage:
              'linear-gradient(to bottom, rgba(243, 172, 8, 0.45) 15%, rgba(253, 215, 70, 0.05) 100%)'
          }}
        >
          ogrojatra
        </p>
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10 flex flex-col items-center text-center">
        {/* Pulsating Pill Tag */}
        <div className="inline-flex items-center gap-2 py-1.5 px-4 bg-white/95 dark:bg-gray-800/95 border border-gray-200 dark:border-gray-700 rounded-full shadow-sm mb-6">
          <span className="h-2 w-2 rounded-full bg-[#ED8E22] shrink-0 animate-pulse" aria-hidden="true" />
          <p className="text-xs sm:text-sm font-semibold text-gray-800 dark:text-gray-200">
            জিইএসি অনুমোদিত সিলেবাস ও সার্বক্ষণিক সক্রেটিক এআই মেন্টর
          </p>
        </div>

        {/* High-Impact Heading */}
        <div className="max-w-4xl mx-auto space-y-4 mb-8">
          <h1
            id="hero-heading"
            className="text-3xl sm:text-5xl lg:text-6xl font-black text-[#213130] dark:text-white leading-[1.2] tracking-tight"
          >
            বাংলাদেশের সেরা একাডেমিক ও প্রফেশনাল{' '}
            <span className="text-[#ED8E22]">অনলাইন কোর্স</span>
          </h1>
          <p className="text-gray-600 dark:text-gray-300 text-sm sm:text-base lg:text-lg max-w-2xl mx-auto leading-relaxed">
            উচ্চমাধ্যমিক স্টেম (গণিত, পদার্থবিজ্ঞান, রসায়ন, আইসিটি) এবং বিশ্ববিদ্যালয় ভর্তি পরীক্ষায়
            সেরা প্রস্তুতির জন্য বিশ্বমানের কোর্স, লাইভ চ্যালেঞ্জ এবং সক্রেটিক এআই সলভার।
          </p>
        </div>

        {/* GoEdu Signature Pill Search Bar with AI Recommendation */}
        <div className="w-full max-w-3xl mx-auto mb-6">
          <form
            onSubmit={handleSubmit}
            className="relative flex items-center bg-white/95 dark:bg-gray-800/95 rounded-full px-3 sm:px-5 py-2 sm:py-2.5 gap-2 sm:gap-3 shadow-lg border border-gray-200/80 dark:border-gray-700 transition-all hover:border-[#ED8E22]"
          >
            <Search className="w-4 h-4 sm:w-5 sm:h-5 text-[#ED8E22] shrink-0 ml-1" aria-hidden="true" />
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="কোর্সের নাম, টপিক বা বিষয় লিখে সার্চ করুন..."
              className="flex-1 bg-transparent outline-none text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 text-xs sm:text-sm md:text-base min-w-0"
              aria-label="Search courses"
            />
            <div className="flex items-center gap-1.5 sm:gap-2 shrink-0">
              <button
                type="submit"
                aria-label="Search"
                className="h-8 w-8 sm:h-9 sm:w-9 flex items-center justify-center rounded-full bg-[#ED8E22] text-white hover:bg-[#d47c1a] active:scale-95 transition-all shadow-sm shrink-0"
              >
                <ArrowRight className="w-4 h-4" aria-hidden="true" />
              </button>

              <button
                type="button"
                onClick={onOpenSocraticDrawer || (() => router.push('/socratic/solver'))}
                aria-label="Let AI Recommend a Course or Topic"
                className="inline-flex items-center justify-center gap-1.5 rounded-full bg-[#ED8E22] text-white font-semibold hover:bg-[#d47c1a] active:scale-95 transition-all shrink-0 px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm shadow-sm"
              >
                <Sparkles className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
                <span className="hidden sm:inline">এআই সহায়তা নিন</span>
                <span className="sm:hidden">এআই</span>
              </button>
            </div>
          </form>
        </div>

        {/* Quick Suggestion Pills */}
        <div className="flex flex-wrap items-center justify-center gap-2 max-w-2xl text-xs">
          <span className="text-gray-500 dark:text-gray-400 font-medium">জনপ্রিয় বিষয়:</span>
          {quickTags.map(tag => (
            <button
              key={tag.query}
              type="button"
              onClick={() => {
                setSearchQuery(tag.label);
                if (onSearchSubmit) onSearchSubmit(tag.query);
                else router.push(`/courses?query=${encodeURIComponent(tag.query)}`);
              }}
              className="px-3 py-1 rounded-full bg-white/80 dark:bg-gray-800/80 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:border-[#ED8E22] hover:text-[#ED8E22] transition-colors"
            >
              {tag.label}
            </button>
          ))}
        </div>

        {/* Highlights Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 sm:gap-8 mt-10 pt-6 border-t border-amber-200/50 dark:border-gray-800 max-w-3xl w-full">
          <div className="flex items-center justify-center gap-2 text-gray-700 dark:text-gray-300 text-xs sm:text-sm">
            <ShieldCheck className="w-4 h-4 text-[#ED8E22]" aria-hidden="true" />
            <span className="font-medium">জিইএসি অ্যাক্রেডিটেড মান</span>
          </div>
          <div className="flex items-center justify-center gap-2 text-gray-700 dark:text-gray-300 text-xs sm:text-sm">
            <CheckCircle2 className="w-4 h-4 text-[#ED8E22]" aria-hidden="true" />
            <span className="font-medium">১০০% ভেরিফাইড কোর্স</span>
          </div>
          <div className="col-span-2 sm:col-span-1 flex items-center justify-center gap-2 text-gray-700 dark:text-gray-300 text-xs sm:text-sm">
            <Sparkles className="w-4 h-4 text-[#ED8E22]" aria-hidden="true" />
            <span className="font-medium">২৪/৭ সক্রেটিক ইন্টারঅ্যাকশন</span>
          </div>
        </div>
      </div>
    </section>
  );
};
