import React, { useState } from 'react';
import Link from 'next/link';
import { Star, Clock, BookOpen, User, ArrowRight, ShieldCheck, Sparkles } from 'lucide-react';
import {
  GOEDU_CATEGORIES,
  GOEDU_COURSES,
  getCoursesByCategory,
  GoEduCourse
} from '../../data/goeduData';

interface GoEduCourseGridProps {
  initialCategory?: string;
  maxDisplay?: number;
}

export const GoEduCourseGrid: React.FC<GoEduCourseGridProps> = ({
  initialCategory = 'all',
  maxDisplay
}) => {
  const [activeCategory, setActiveCategory] = useState(initialCategory);

  const filteredCourses = getCoursesByCategory(activeCategory);
  const displayCourses = maxDisplay ? filteredCourses.slice(0, maxDisplay) : filteredCourses;

  return (
    <section
      aria-labelledby="popular-courses-heading"
      className="py-14 sm:py-20 px-4 sm:px-6 lg:px-8 bg-[#FFFCF6] dark:bg-gray-900 transition-colors duration-300"
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center max-w-3xl mx-auto mb-10">
          <div className="inline-flex items-center gap-2 py-1.5 px-4 border border-gray-300 dark:border-gray-700 rounded-full mb-4 bg-white/60 dark:bg-gray-800/60 shadow-sm">
            <span className="h-2 w-2 rounded-full bg-[#ED8E22]" aria-hidden="true" />
            <p className="text-xs sm:text-sm font-semibold text-gray-800 dark:text-gray-200">
              অগ্রযাত্রার জনপ্রিয় অনলাইন কোর্সসমূহ
            </p>
          </div>
          <h2
            id="popular-courses-heading"
            className="text-2xl sm:text-4xl font-bold text-[#213130] dark:text-white mb-4 leading-tight"
          >
            এনসিটিবি সিলেবাস ও সমসাময়িক স্কিলসের সেরা কোর্সসমূহ
          </h2>
          <p className="text-gray-600 dark:text-gray-300 text-sm sm:text-base leading-relaxed">
            এইচএসসি বোর্ড পরীক্ষা, ভার্সিটি ও বুয়েট এডমিশন টেস্ট থেকে শুরু করে এআই এবং প্রোগ্রামিং—ধাপে ধাপে
            দক্ষতা গড়ুন বাংলাদেশের বিশ্বস্ত লার্নিং প্ল্যাটফর্মে।
          </p>
        </header>

        {/* Category Pills Filter */}
        <nav
          aria-label="Course category filters"
          className="flex flex-wrap gap-2 sm:gap-3 justify-center mb-10"
        >
          {GOEDU_CATEGORIES.map(cat => {
            const isSelected = activeCategory === cat.id;
            return (
              <button
                key={cat.id}
                type="button"
                onClick={() => setActiveCategory(cat.id)}
                className={`px-4 py-2 rounded-full text-xs sm:text-sm font-semibold transition-all ${
                  isSelected
                    ? 'bg-[#ED8E22] text-white shadow-md scale-105'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:border-[#ED8E22] hover:text-[#ED8E22]'
                }`}
              >
                {cat.bengaliName}
              </button>
            );
          })}
        </nav>

        {/* Course Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {displayCourses.map(course => (
            <article
              key={course.id}
              className="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200/80 dark:border-gray-700 overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col group hover:-translate-y-1"
            >
              {/* Thumbnail Container */}
              <div className="aspect-[16/10] relative overflow-hidden bg-gray-100 dark:bg-gray-700">
                <img
                  src={course.thumbnail}
                  alt={course.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                  loading="lazy"
                />
                {/* Level Badge */}
                <div className="absolute top-3 left-3 flex gap-1.5">
                  <span className="text-[10px] font-bold text-gray-800 bg-white/95 backdrop-blur-sm px-2.5 py-1 rounded-full shadow-sm">
                    {course.levelBengali}
                  </span>
                  {course.isAccredited && (
                    <span className="text-[10px] font-bold text-emerald-800 bg-emerald-100/90 backdrop-blur-sm px-2 py-1 rounded-full flex items-center gap-1 shadow-sm">
                      <ShieldCheck className="w-3 h-3 text-emerald-600" aria-hidden="true" />
                      <span>জিইএসি</span>
                    </span>
                  )}
                </div>

                {/* Duration & Lessons Pill */}
                <div className="absolute bottom-3 right-3 flex items-center gap-2 text-[10px] text-white bg-black/60 backdrop-blur-sm px-2.5 py-1 rounded-full">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" aria-hidden="true" />
                    <span>{Math.round(course.durationMinutes / 60)} ঘন্টা</span>
                  </span>
                  <span>|</span>
                  <span className="flex items-center gap-1">
                    <BookOpen className="w-3 h-3" aria-hidden="true" />
                    <span>{course.totalLessons} পাঠ</span>
                  </span>
                </div>
              </div>

              {/* Card Body */}
              <div className="p-4 sm:p-5 flex-1 flex flex-col justify-between">
                <div>
                  <span className="text-[11px] font-semibold text-[#ED8E22] uppercase tracking-wider">
                    {course.category}
                  </span>
                  <h3 className="font-bold text-base text-gray-900 dark:text-white mt-1 mb-2 line-clamp-2 leading-snug group-hover:text-[#ED8E22] transition-colors">
                    {course.bengaliTitle}
                  </h3>

                  {/* Instructor */}
                  <div className="flex items-center gap-2 mb-3">
                    <img
                      src={course.instructor.photo}
                      alt={course.instructor.name}
                      className="w-6 h-6 rounded-full object-cover border border-amber-200"
                    />
                    <div className="text-xs text-gray-600 dark:text-gray-400 truncate">
                      <span className="font-medium text-gray-800 dark:text-gray-200">
                        {course.instructor.name}
                      </span>
                    </div>
                  </div>

                  {/* Ratings & Students */}
                  <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 pb-3 border-b border-gray-100 dark:border-gray-700/60">
                    <div className="flex items-center gap-1 text-amber-500">
                      <Star className="w-3.5 h-3.5 fill-current" aria-hidden="true" />
                      <span className="font-bold text-gray-800 dark:text-gray-200">
                        {course.rating}
                      </span>
                      <span className="text-gray-400 text-[11px]">({course.ratingCount})</span>
                    </div>
                    <span>{course.totalStudents.toLocaleString()} শিক্ষার্থী</span>
                  </div>
                </div>

                {/* Price & Action */}
                <div className="pt-3.5 flex items-center justify-between">
                  <div className="flex items-baseline gap-1.5">
                    <span className="text-lg font-black text-[#ED8E22]">
                      ৳{course.discountPrice || course.price}
                    </span>
                    {course.discountPrice && (
                      <span className="text-xs line-through text-gray-400">
                        ৳{course.price}
                      </span>
                    )}
                  </div>

                  <Link
                    href={course.routeLink}
                    className="inline-flex items-center gap-1 px-3.5 py-1.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 text-xs font-semibold hover:bg-[#ED8E22] hover:text-white dark:hover:bg-[#ED8E22] dark:hover:text-white transition-all active:scale-95"
                  >
                    <span>শুরু করুন</span>
                    <ArrowRight className="w-3 h-3" aria-hidden="true" />
                  </Link>
                </div>
              </div>
            </article>
          ))}
        </div>

        {/* View All Button */}
        <div className="text-center mt-12">
          <Link
            href="/courses"
            className="inline-flex items-center gap-2 px-8 py-3 rounded-full bg-[#1E293B] text-white hover:bg-gray-800 active:scale-95 transition-all font-semibold text-sm shadow-md"
          >
            <span>সকল ২৮০+ কোর্স ব্রাউজ করুন</span>
            <ArrowRight className="w-4 h-4" aria-hidden="true" />
          </Link>
        </div>
      </div>
    </section>
  );
};
