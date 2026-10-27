import React, { useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { Search, Sparkles, Filter, BookOpen } from 'lucide-react';
import { GoEduNavbar } from '../components/goedu/GoEduNavbar';
import { GoEduCourseGrid } from '../components/goedu/GoEduCourseGrid';
import { GoEduBundleSpotlight } from '../components/goedu/GoEduBundleSpotlight';
import { GoEduAIBanner } from '../components/goedu/GoEduAIBanner';
import { GoEduFooter } from '../components/goedu/GoEduFooter';
import { SocraticTutorDrawer } from '../components/ai/SocraticTutorDrawer';

export default function CoursesPage() {
  const router = useRouter();
  const queryParam = (router.query.query as string) || '';
  const categoryParam = (router.query.category as string) || 'all';

  const [isSocraticDrawerOpen, setIsSocraticDrawerOpen] = useState(false);

  return (
    <>
      <Head>
        <title>অনলাইন কোর্সসমূহ | গোএডু ও অগ্রযাত্রা</title>
        <meta
          name="description"
          content="এনসিটিবি উচ্চমাধ্যমিক স্টেম, বিশ্ববিদ্যালয় ভর্তি প্রস্তুতি এবং প্রফেশনাল স্কিলসের সেরা অনলাইন কোর্সসমূহ।"
        />
      </Head>

      <div className="min-h-screen bg-[#FFFCF6] dark:bg-gray-900 text-gray-900 dark:text-white flex flex-col transition-colors duration-300">
        {/* Floating Pill Header */}
        <GoEduNavbar onOpenSocraticDrawer={() => setIsSocraticDrawerOpen(true)} />

        {/* Courses Hero Banner */}
        <div className="pt-24 sm:pt-28 pb-10 sm:pb-12 px-4 sm:px-6 lg:px-8 bg-[#FFF6DD] dark:bg-gray-900 border-b border-amber-200/60 dark:border-gray-800">
          <div className="max-w-5xl mx-auto text-center space-y-3">
            <div className="inline-flex items-center gap-2 py-1 px-3.5 bg-white/90 dark:bg-gray-800 rounded-full border border-gray-200 dark:border-gray-700 shadow-sm">
              <span className="h-2 w-2 rounded-full bg-[#ED8E22] animate-pulse" aria-hidden="true" />
              <span className="text-xs font-semibold text-gray-800 dark:text-gray-200">
                জিইএসি এক্রিডিটেড সিলেবাস ও ভেরিফাইড কোর্স লাইব্রেরি
              </span>
            </div>

            <h1 className="text-3xl sm:text-5xl font-black text-[#213130] dark:text-white tracking-tight">
              অনলাইন কোর্স ও লার্নিং পাথওয়ে
            </h1>
            <p className="text-gray-600 dark:text-gray-300 text-sm sm:text-base max-w-2xl mx-auto leading-relaxed">
              উচ্চমাধ্যমিক বিজ্ঞান, ক্যালকুলাস, পদার্থবিজ্ঞান, আইসিটি এবং এডমিশন টেস্টের জন্য বিশেষায়িত কোর্সসমূহ।
              প্রতিটি কোর্সের সাথে রয়েছে সার্বক্ষণিক সক্রেটিক এআই সলভার সহায়তা।
            </p>
          </div>
        </div>

        {/* Main Courses Interactive Grid */}
        <main className="flex-1">
          <GoEduCourseGrid initialCategory={categoryParam} />
          <GoEduBundleSpotlight />
          <GoEduAIBanner onOpenSocraticDrawer={() => setIsSocraticDrawerOpen(true)} />
        </main>

        {/* Global Footer */}
        <GoEduFooter />

        {/* Socratic AI Tutor Drawer */}
        <SocraticTutorDrawer
          isOpen={isSocraticDrawerOpen}
          onClose={() => setIsSocraticDrawerOpen(false)}
        />
      </div>
    </>
  );
}
