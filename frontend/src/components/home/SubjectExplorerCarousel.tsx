/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Homepage Subject Explorer Carousel (Swiper & Academic Editorial)
 * FILE:      frontend/src/components/home/SubjectExplorerCarousel.tsx
 * PURPOSE:   Provides a touch-friendly, accessible Swiper carousel showcasing
 *            NCTB core academic subjects with chapter counts, KaTeX mathematical formulas,
 *            and direct practice links.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Academic Editorial, Swiper touch/keyboard navigation.
 */

import React, { useRef } from 'react';
import Link from 'next/link';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, A11y, Keyboard } from 'swiper/modules';
import type { Swiper as SwiperType } from 'swiper';
import {
  Atom,
  FlaskConical,
  Compass,
  Dna,
  Binary,
  Calculator,
  ChevronLeft,
  ChevronRight,
  ArrowRight,
  BookOpen,
  CheckCircle2,
} from 'lucide-react';
import { KaTeXRenderer } from '@/components/quiz/katex-renderer';

export interface SubjectItem {
  id: string;
  name_bn: string;
  name_en: string;
  level: string;
  chaptersCount: number;
  boardQuestionsCount: number;
  formulaPreview: string;
  summary_bn: string;
  icon: React.ReactNode;
  accentColor: string;
  link: string;
}

const BENGALI_DIGITS = ['০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'];
function toBnDigits(num: number): string {
  return String(num).replace(/\d/g, (d) => BENGALI_DIGITS[parseInt(d, 10)]);
}

const SUBJECTS_DATA: SubjectItem[] = [
  {
    id: 'physics',
    name_bn: 'পদার্থবিজ্ঞান (Physics)',
    name_en: 'Physics 1st & 2nd Paper',
    level: 'এইচএসসি ও এসএসসি',
    chaptersCount: 22,
    boardQuestionsCount: 128,
    formulaPreview: '$H = \\frac{v_0^2 \\sin^2\\theta}{2g} \\quad R = \\frac{v_0^2 \\sin 2\\theta}{g}$',
    summary_bn: 'বলবিদ্যা, কাজ ও শক্তি, মহাকর্ষ, তরঙ্গ, স্থির তড়িৎ ও আধুনিক পদার্থবিজ্ঞান।',
    icon: <Atom className="w-5 h-5" />,
    accentColor: '#1B2A4A',
    link: '/practice?subject=Physics',
  },
  {
    id: 'chemistry',
    name_bn: 'রসায়ন (Chemistry)',
    name_en: 'Chemistry 1st & 2nd Paper',
    level: 'এইচএসসি ও এসএসসি',
    chaptersCount: 20,
    boardQuestionsCount: 115,
    formulaPreview: '$\\text{pH} = -\\log_{10}[\\text{H}^+] \\quad \\Delta G = \\Delta H - T\\Delta S$',
    summary_bn: 'গুণগত রসায়ন, পর্যায়বৃত্ত ধর্ম, জৈব রসায়ন, রাসায়নিক পরিবর্তন ও তড়িৎ রসায়ন।',
    icon: <FlaskConical className="w-5 h-5" />,
    accentColor: '#0B5D3B',
    link: '/practice?subject=Chemistry',
  },
  {
    id: 'higher-math',
    name_bn: 'উচ্চতর গণিত (Higher Mathematics)',
    name_en: 'Higher Math 1st & 2nd Paper',
    level: 'এইচএসসি ও এসএসসি',
    chaptersCount: 24,
    boardQuestionsCount: 142,
    formulaPreview: '$\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C \\quad (n \\neq -1)$',
    summary_bn: 'ম্যাট্রিক্স ও নির্ণায়ক, সরলরেখা, বৃত্ত, ত্রিকোণমিতি, অন্তরীকরণ ও যোগজীকরণ।',
    icon: <Compass className="w-5 h-5" />,
    accentColor: '#B8862B',
    link: '/practice?subject=HigherMathematics',
  },
  {
    id: 'biology',
    name_bn: 'জীববিজ্ঞান (Biology)',
    name_en: 'Biology 1st & 2nd Paper',
    level: 'এইচএসসি ও এসএসসি',
    chaptersCount: 24,
    boardQuestionsCount: 108,
    formulaPreview: '$\\text{ATP} + \\text{H}_2\\text{O} \\rightleftharpoons \\text{ADP} + \\text{P}_i + 7.3\\text{ kcal}$',
    summary_bn: 'কোষ ও এর গঠন, জেনেটিক্স ও বিবর্তন, উদ্ভিদ শারীরতত্ত্ব এবং মানব শারীরতত্ত্ব।',
    icon: <Dna className="w-5 h-5" />,
    accentColor: '#0B5D3B',
    link: '/practice?subject=Biology',
  },
  {
    id: 'ict',
    name_bn: 'তথ্য ও যোগাযোগ প্রযুক্তি (ICT)',
    name_en: 'Information & Communication Technology',
    level: 'এইচএসসি একাদশ-দ্বাদশ',
    chaptersCount: 6,
    boardQuestionsCount: 96,
    formulaPreview: '$(1011)_2 = 1\\cdot 2^3 + 0\\cdot 2^2 + 1\\cdot 2^1 + 1\\cdot 2^0 = (11)_{10}$',
    summary_bn: 'সংখ্যা পদ্ধতি, ডিজিটাল লজিক গেইট, এইচটিএমএল ওয়েব ডিজাইন ও সি প্রোগ্রামিং।',
    icon: <Binary className="w-5 h-5" />,
    accentColor: '#1B2A4A',
    link: '/practice?subject=ICT',
  },
  {
    id: 'general-math',
    name_bn: 'সাধারণ গণিত (General Mathematics)',
    name_en: 'General Mathematics Class 9-10',
    level: 'এসএসসি শ্রেণি ৯-১০',
    chaptersCount: 17,
    boardQuestionsCount: 150,
    formulaPreview: '$a^2 + b^2 = c^2 \\quad x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$',
    summary_bn: 'বাস্তব সংখ্যা, বীজগণিতীয় রাশি, জ্যামিতিক উপপাদ্য, ত্রিকোণমিতি ও পরিমিতি।',
    icon: <Calculator className="w-5 h-5" />,
    accentColor: '#B8862B',
    link: '/practice?subject=GeneralMath',
  },
];

export const SubjectExplorerCarousel: React.FC = () => {
  const swiperRef = useRef<SwiperType | null>(null);

  return (
    <div className="w-full space-y-6">
      {/* Top Header & Navigation Controls */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 pb-2">
        <div className="space-y-1">
          <div className="text-xs font-semibold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
            জাতীয় পাঠ্যক্রম বিষয়সমূহ
          </div>
          <h2 className="text-2xl sm:text-3xl font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali tracking-tight">
            বিষয়ভিত্তিক প্রশ্ন ও সমাধান এক্সপ্লোরার
          </h2>
          <p className="text-xs sm:text-sm text-[#5B5B5B] dark:text-slate-400 font-bengali leading-relaxed max-w-xl">
            এনসিটিবি পাঠ্যক্রমের প্রতিটি অধ্যায়ের তাত্ত্বিক ধারণা, বিগত ১০ বছরের আসল বোর্ড প্রশ্ন এবং নির্ভুল গাণিতিক KaTeX সমীকরণ।
          </p>
        </div>

        {/* Carousel Prev/Next Buttons */}
        <div className="flex items-center gap-2 self-start sm:self-auto shrink-0" aria-label="ক্যারোজেল নিয়ন্ত্রণ">
          <button
            type="button"
            onClick={() => swiperRef.current?.slidePrev()}
            aria-label="পূর্ববর্তী বিষয়সমূহ"
            className="w-10 h-10 rounded-xl bg-white dark:bg-[#121B2D] border border-amber-200/80 dark:border-[#262D3D] hover:bg-[#FFF9EB] dark:hover:bg-[#1A263E] text-[#1B2A4A] dark:text-[#F5F2EB] flex items-center justify-center transition shadow-xs active:translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-[#ED8E22]"
          >
            <ChevronLeft className="w-5 h-5 text-[#ED8E22]" />
          </button>
          <button
            type="button"
            onClick={() => swiperRef.current?.slideNext()}
            aria-label="পরবর্তী বিষয়সমূহ"
            className="w-10 h-10 rounded-xl bg-white dark:bg-[#121B2D] border border-amber-200/80 dark:border-[#262D3D] hover:bg-[#FFF9EB] dark:hover:bg-[#1A263E] text-[#1B2A4A] dark:text-[#F5F2EB] flex items-center justify-center transition shadow-xs active:translate-y-0.5 focus:outline-none focus:ring-2 focus:ring-[#ED8E22]"
          >
            <ChevronRight className="w-5 h-5 text-[#ED8E22]" />
          </button>
        </div>
      </div>

      {/* Swiper Container */}
      <div className="relative">
        <Swiper
          modules={[Navigation, Pagination, A11y, Keyboard]}
          onSwiper={(swiper) => {
            swiperRef.current = swiper;
          }}
          spaceBetween={20}
          slidesPerView={1}
          breakpoints={{
            640: {
              slidesPerView: 2,
              spaceBetween: 20,
            },
            1024: {
              slidesPerView: 3,
              spaceBetween: 24,
            },
          }}
          keyboard={{ enabled: true }}
          pagination={{
            clickable: true,
            el: '.subject-swiper-pagination',
            bulletClass: 'inline-block w-2.5 h-2.5 rounded-full bg-amber-200 dark:bg-slate-700 mx-1 cursor-pointer transition-all',
            bulletActiveClass: '!bg-[#ED8E22] dark:!bg-amber-400 !w-6',
          }}
          className="pb-12"
        >
          {SUBJECTS_DATA.map((subject) => (
            <SwiperSlide key={subject.id} className="h-auto">
              <div className="h-full flex flex-col justify-between p-6 sm:p-7 rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-[#262D3D] shadow-xs hover:border-[#ED8E22]/60 hover:shadow-md transition-all duration-200">
                <div className="space-y-4">
                  {/* Top Bar with Icon & Level */}
                  <div className="flex items-center justify-between">
                    <div
                      className="w-10 h-10 rounded-xl flex items-center justify-center border border-amber-200/80 dark:border-[#262D3D]"
                      style={{
                        backgroundColor: '#FFF9EB',
                        color: subject.accentColor,
                      }}
                    >
                      {subject.icon}
                    </div>
                    <span className="text-[11px] font-semibold px-2.5 py-1 rounded-md bg-[#FFF9EB] dark:bg-[#0E1526] text-[#525252] dark:text-slate-400 border border-amber-200/80 dark:border-[#262D3D] font-bengali">
                      {subject.level}
                    </span>
                  </div>

                  {/* Subject Title */}
                  <div className="space-y-1">
                    <h3 className="text-lg font-serif font-bold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali leading-snug">
                      {subject.name_bn}
                    </h3>
                    <div className="text-[11px] font-medium text-[#525252] dark:text-slate-400 font-sans">
                      {subject.name_en}
                    </div>
                  </div>

                  {/* Summary */}
                  <p className="text-xs text-[#525252] dark:text-slate-300 leading-relaxed font-bengali line-clamp-2">
                    {subject.summary_bn}
                  </p>

                  {/* KaTeX Math Formula Preview Box */}
                  <div className="p-3 rounded-xl bg-[#FFFDF9] dark:bg-[#0E1526] border border-amber-200/60 dark:border-[#262D3D] text-[11px] overflow-x-auto">
                    <div className="text-[10px] text-[#525252] dark:text-slate-400 font-bengali pb-1 flex items-center justify-between">
                      <span>নমুনা সমীকরণ ও সূত্র</span>
                      <span className="font-semibold text-[#0B5D3B] dark:text-emerald-400">KaTeX</span>
                    </div>
                    <div className="pt-0.5 text-[#1B2A4A] dark:text-[#F5F2EB]">
                      <KaTeXRenderer content={subject.formulaPreview} className="text-xs" />
                    </div>
                  </div>

                  {/* Subject Badges */}
                  <div className="flex items-center gap-3 text-xs text-[#525252] dark:text-slate-400 pt-1">
                    <div className="flex items-center gap-1.5 font-bengali">
                      <BookOpen className="w-3.5 h-3.5 text-[#ED8E22] shrink-0" />
                      <span>{toBnDigits(subject.chaptersCount)}টি অধ্যায়</span>
                    </div>
                    <div className="flex items-center gap-1.5 font-bengali">
                      <CheckCircle2 className="w-3.5 h-3.5 text-[#0B5D3B] dark:text-emerald-400 shrink-0" />
                      <span>{toBnDigits(subject.boardQuestionsCount)}+ বোর্ড প্রশ্ন</span>
                    </div>
                  </div>
                </div>

                {/* Bottom Action */}
                <div className="pt-5 mt-5 border-t border-amber-200/60 dark:border-[#262D3D]">
                  <Link
                    href={subject.link}
                    className="w-full inline-flex items-center justify-between py-2.5 px-3.5 rounded-xl bg-[#FFF9EB] dark:bg-[#0E1526] hover:bg-[#FFF2D1] dark:hover:bg-[#1A263E] text-[#1B2A4A] dark:text-[#F5F2EB] text-xs font-semibold border border-amber-200/80 dark:border-[#262D3D] transition group font-bengali"
                  >
                    <span>অনুশীলন শুরু করুন</span>
                    <ArrowRight className="w-4 h-4 text-[#ED8E22] group-hover:translate-x-1 transition-transform" />
                  </Link>
                </div>
              </div>
            </SwiperSlide>
          ))}
        </Swiper>

        {/* Bullet Pagination Container */}
        <div className="subject-swiper-pagination flex justify-center items-center mt-2" />
      </div>
    </div>
  );
};
