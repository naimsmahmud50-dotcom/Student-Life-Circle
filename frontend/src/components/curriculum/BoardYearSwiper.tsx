/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Board Archive Year & Board Swiper Bar
 * FILE:      frontend/src/components/curriculum/BoardYearSwiper.tsx
 * PURPOSE:   Provides touch-ergonomic horizontal swiping for NCTB Board Examination Years (2015-2025)
 *            and Education Boards using Swiper with zero-layout shift.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA, Academic Editorial, Swiper touch/keyboard navigation.
 */

import React, { useRef } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, A11y, Keyboard, FreeMode } from 'swiper/modules';
import type { Swiper as SwiperType } from 'swiper';
import { Calendar, ChevronLeft, ChevronRight, Award } from 'lucide-react';

export interface BoardYearSwiperProps {
  years: string[];
  selectedYear: string;
  onSelectYear: (year: string) => void;
  boards: { key: string; label_bn: string }[];
  selectedBoard: string;
  onSelectBoard: (board: string) => void;
}

export const BoardYearSwiper: React.FC<BoardYearSwiperProps> = ({
  years,
  selectedYear,
  onSelectYear,
  boards,
  selectedBoard,
  onSelectBoard,
}) => {
  const yearSwiperRef = useRef<SwiperType | null>(null);
  const boardSwiperRef = useRef<SwiperType | null>(null);

  return (
    <div className="space-y-4 p-5 rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#262D3D] shadow-sm">
      {/* 1. Year Selector Swiper */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-semibold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
            <Calendar className="w-4 h-4 text-[#B8862B]" />
            <span>পরীক্ষার বছর নির্বাচন করুন (২০১৫ – ২০২৫)</span>
          </div>

          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={() => yearSwiperRef.current?.slidePrev()}
              aria-label="পূর্ববর্তী বছরসমূহ"
              className="w-7 h-7 rounded-lg bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D] hover:bg-[#F5F2EB] dark:hover:bg-[#1A263E] text-[#1B2A4A] dark:text-[#F5F2EB] flex items-center justify-center transition active:translate-y-0.5"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <button
              type="button"
              onClick={() => yearSwiperRef.current?.slideNext()}
              aria-label="পরবর্তী বছরসমূহ"
              className="w-7 h-7 rounded-lg bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D] hover:bg-[#F5F2EB] dark:hover:bg-[#1A263E] text-[#1B2A4A] dark:text-[#F5F2EB] flex items-center justify-center transition active:translate-y-0.5"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <Swiper
          modules={[Navigation, A11y, Keyboard, FreeMode]}
          onSwiper={(swiper) => {
            yearSwiperRef.current = swiper;
          }}
          slidesPerView="auto"
          spaceBetween={8}
          freeMode={true}
          keyboard={{ enabled: true }}
          className="w-full !py-1"
        >
          {years.map((yr) => {
            const isSelected = selectedYear === yr;
            const label = yr === 'all' ? 'সকল বছর' : `${yr} সাল`;
            return (
              <SwiperSlide key={yr} className="!w-auto">
                <button
                  type="button"
                  onClick={() => onSelectYear(yr)}
                  className={`px-4 py-2 rounded-xl text-xs font-semibold font-bengali transition-all duration-150 border shrink-0 min-h-[38px] flex items-center justify-center ${
                    isSelected
                      ? 'bg-[#1B2A4A] text-white border-[#1B2A4A] shadow-xs scale-[1.02]'
                      : 'bg-[#FAF8F3] dark:bg-[#0E1526] text-[#1A1A1A] dark:text-slate-300 border-[#E5E2DA] dark:border-[#262D3D] hover:border-[#1B2A4A]/40'
                  }`}
                >
                  {label}
                </button>
              </SwiperSlide>
            );
          })}
        </Swiper>
      </div>

      {/* 2. Board Selector Swiper */}
      <div className="space-y-2 pt-2 border-t border-[#E5E2DA] dark:border-[#262D3D]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-semibold text-[#1B2A4A] dark:text-[#F5F2EB] font-bengali">
            <Award className="w-4 h-4 text-[#0B5D3B]" />
            <span>শিক্ষাবোর্ড নির্বাচন করুন (১০টি সাধারণ ও কারিগরি বোর্ড)</span>
          </div>

          <div className="flex items-center gap-1.5">
            <button
              type="button"
              onClick={() => boardSwiperRef.current?.slidePrev()}
              aria-label="পূর্ববর্তী বোর্ডসমূহ"
              className="w-7 h-7 rounded-lg bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D] hover:bg-[#F5F2EB] dark:hover:bg-[#1A263E] text-[#1B2A4A] dark:text-[#F5F2EB] flex items-center justify-center transition active:translate-y-0.5"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <button
              type="button"
              onClick={() => boardSwiperRef.current?.slideNext()}
              aria-label="পরবর্তী বোর্ডসমূহ"
              className="w-7 h-7 rounded-lg bg-[#FAF8F3] dark:bg-[#0E1526] border border-[#E5E2DA] dark:border-[#262D3D] hover:bg-[#F5F2EB] dark:hover:bg-[#1A263E] text-[#1B2A4A] dark:text-[#F5F2EB] flex items-center justify-center transition active:translate-y-0.5"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <Swiper
          modules={[Navigation, A11y, Keyboard, FreeMode]}
          onSwiper={(swiper) => {
            boardSwiperRef.current = swiper;
          }}
          slidesPerView="auto"
          spaceBetween={8}
          freeMode={true}
          keyboard={{ enabled: true }}
          className="w-full !py-1"
        >
          {boards.map((b) => {
            const isSelected = selectedBoard === b.key;
            return (
              <SwiperSlide key={b.key} className="!w-auto">
                <button
                  type="button"
                  onClick={() => onSelectBoard(b.key)}
                  className={`px-3.5 py-2 rounded-xl text-xs font-semibold font-bengali transition-all duration-150 border shrink-0 min-h-[38px] flex items-center justify-center ${
                    isSelected
                      ? 'bg-[#0B5D3B] text-white border-[#0B5D3B] shadow-xs scale-[1.02]'
                      : 'bg-[#FAF8F3] dark:bg-[#0E1526] text-[#1A1A1A] dark:text-slate-300 border-[#E5E2DA] dark:border-[#262D3D] hover:border-[#0B5D3B]/40'
                  }`}
                >
                  {b.label_bn}
                </button>
              </SwiperSlide>
            );
          })}
        </Swiper>
      </div>
    </div>
  );
};
