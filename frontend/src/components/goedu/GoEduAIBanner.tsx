import React from 'react';
import Link from 'next/link';
import { Sparkles, ArrowRight, MessageSquare, Compass, BrainCircuit } from 'lucide-react';

interface GoEduAIBannerProps {
  onOpenSocraticDrawer?: () => void;
}

export const GoEduAIBanner: React.FC<GoEduAIBannerProps> = ({ onOpenSocraticDrawer }) => {
  return (
    <section className="py-12 sm:py-16 px-4 sm:px-6 lg:px-8 container mx-auto">
      <div className="relative rounded-[2.5rem] overflow-hidden bg-gradient-to-r from-[#213130] via-slate-900 to-[#1E293B] text-white p-8 sm:p-12 lg:p-16 shadow-2xl">
        {/* Subtle Background Glow */}
        <div
          className="absolute top-0 right-0 w-96 h-96 bg-[#ED8E22]/15 rounded-full blur-3xl pointer-events-none"
          aria-hidden="true"
        />

        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center gap-2 py-1.5 px-4 bg-white/10 backdrop-blur-md rounded-full border border-white/20 text-amber-300 text-xs sm:text-sm font-semibold mb-6">
            <Sparkles className="w-4 h-4 text-[#ED8E22]" aria-hidden="true" />
            <span>বুদ্ধিমান লার্নিং এসিস্ট্যান্ট</span>
          </div>

          <h2 className="text-2xl sm:text-4xl lg:text-5xl font-black mb-5 leading-tight tracking-tight">
            কোথা থেকে শুরু করবেন বুঝতে পারছেন না?{' '}
            <span className="text-[#ED8E22]">সক্রেটিক এআইকে</span> জিজ্ঞেস করুন
          </h2>

          <p className="text-gray-300 text-sm sm:text-base lg:text-lg mb-8 leading-relaxed max-w-2xl">
            আপনার বর্তমান ক্লাস, লক্ষ্য ও দুর্বলতার ক্ষেত্র জানান। আমাদের সক্রেটিক এআই তাৎক্ষণিকভাবে আপনার
            জন্য সেরা স্টাডি প্ল্যান, প্রয়োজনীয় কোর্স এবং অনুশীলনী প্রশ্ন সাজিয়ে দেবে।
          </p>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4">
            <button
              type="button"
              onClick={onOpenSocraticDrawer}
              className="inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-full bg-[#ED8E22] text-white font-bold text-sm sm:text-base hover:bg-[#d47c1a] active:scale-95 transition-all shadow-lg"
            >
              <BrainCircuit className="w-5 h-5" aria-hidden="true" />
              <span>এআই মেন্টরের সাথে কথা বলুন</span>
            </button>

            <Link
              href="/socratic/solver"
              className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-full bg-white/10 hover:bg-white/20 text-white font-semibold text-sm sm:text-base transition-colors border border-white/15"
            >
              <span>হোয়াইটবোর্ড সলভার পেজ</span>
              <ArrowRight className="w-4 h-4" aria-hidden="true" />
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
};
