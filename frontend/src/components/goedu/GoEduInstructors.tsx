import React from 'react';
import { Star, GraduationCap, Users, BookOpen } from 'lucide-react';
import { GOEDU_INSTRUCTORS } from '../../data/goeduData';

export const GoEduInstructors: React.FC = () => {
  return (
    <section className="py-14 sm:py-20 px-4 sm:px-6 lg:px-8 bg-[#FFFCF6] dark:bg-gray-900 border-t border-b border-gray-100 dark:border-gray-800 transition-colors duration-300">
      <div className="max-w-7xl mx-auto">
        <header className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center gap-2 py-1.5 px-4 border border-gray-300 dark:border-gray-700 rounded-full mb-3 bg-white dark:bg-gray-800 shadow-sm">
            <span className="h-2 w-2 rounded-full bg-[#ED8E22]" aria-hidden="true" />
            <p className="text-xs sm:text-sm font-semibold text-gray-800 dark:text-gray-200">
              আমাদের অভিজ্ঞ শিক্ষক ও মেন্টরবৃন্দ
            </p>
          </div>
          <h2 className="text-2xl sm:text-4xl font-bold text-[#213130] dark:text-white mb-4 leading-tight">
            শীর্ষ একাডেমিশিয়ান ও ইন্ডাস্ট্রি বিশেষজ্ঞদের সান্নিধ্যে শিখুন
          </h2>
          <p className="text-gray-600 dark:text-gray-300 text-sm sm:text-base leading-relaxed">
            বাংলাদেশের শীর্ষ বিশ্ববিদ্যালয় ও গবেষণা প্রতিষ্ঠানের শিক্ষকগণের নির্দেশনায় প্রতিটি লেকচার তৈরি
            এবং জিইএসি বিশেষজ্ঞ প্যানেল দ্বারা পরীক্ষিত।
          </p>
        </header>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {GOEDU_INSTRUCTORS.map(instructor => (
            <div
              key={instructor.id}
              className="bg-white dark:bg-gray-800 rounded-2xl p-5 border border-gray-200/80 dark:border-gray-700 shadow-sm hover:shadow-lg transition-all duration-300 flex flex-col items-center text-center group hover:-translate-y-1"
            >
              <div className="relative mb-4">
                <img
                  src={instructor.photo}
                  alt={instructor.name}
                  className="w-24 h-24 sm:w-28 sm:h-28 rounded-full object-cover border-2 border-amber-200 dark:border-amber-500/40 shadow-md group-hover:scale-105 transition-transform"
                />
                <div className="absolute -bottom-1 -right-1 bg-white dark:bg-gray-700 p-1 rounded-full shadow-sm">
                  <div className="w-5 h-5 bg-[#ED8E22] rounded-full flex items-center justify-center text-white text-[10px]">
                    <GraduationCap className="w-3 h-3" aria-hidden="true" />
                  </div>
                </div>
              </div>

              <h3 className="font-bold text-base text-gray-900 dark:text-white mb-1 group-hover:text-[#ED8E22] transition-colors">
                {instructor.name}
              </h3>
              <p className="text-xs text-[#ED8E22] font-medium mb-1 line-clamp-1">
                {instructor.role}
              </p>
              <p className="text-[11px] text-gray-500 dark:text-gray-400 mb-3 line-clamp-1">
                {instructor.institution}
              </p>

              <p className="text-xs text-gray-600 dark:text-gray-300 mb-4 line-clamp-2 leading-relaxed">
                {instructor.bio}
              </p>

              <div className="mt-auto w-full pt-3 border-t border-gray-100 dark:border-gray-700/60 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                <div className="flex items-center gap-1 text-amber-500">
                  <Star className="w-3.5 h-3.5 fill-current" aria-hidden="true" />
                  <span className="font-bold text-gray-700 dark:text-gray-300">{instructor.rating}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Users className="w-3.5 h-3.5" aria-hidden="true" />
                  <span>{instructor.totalStudents.toLocaleString()}</span>
                </div>
                <div className="flex items-center gap-1">
                  <BookOpen className="w-3.5 h-3.5" aria-hidden="true" />
                  <span>{instructor.totalCourses} কোর্স</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
