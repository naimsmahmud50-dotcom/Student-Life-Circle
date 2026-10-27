/**
 * ========================================================================================
 * MODULE:    Flagship Public Educational Portal & GoEdu Design Language Master Experience
 * TOPIC:     GoEdu Design Reverse Engineering & Platform Adaptation (Spec 050)
 * FILE:      frontend/src/pages/index.tsx
 * PURPOSE:   Presents a world-class, high-conversion learning portal for Ogrojatra:
 *            1. GoEdu Signature Sunshine Hero (#FFF6DD) with golden radial glow,
 *               giant typographic watermark, pulsating pill badge, and AI pill search bar.
 *            2. GoEdu Floating Pill Navigation Header with Socratic AI trigger and Cart drawer.
 *            3. Tri-Card Trust Matrix: Google Reviews, Trustpilot Emerald, Facebook 100%.
 *            4. Ultra-Rounded (2.5rem) Featured Accelerator Course Bundle Spotlight.
 *            5. Interactive Course & Subject Grid with Category Filter Pills.
 *            6. Interactive 3D STEM Virtual Labs (Physics Projectile & Chemistry Molecular).
 *            7. Verified Academic Instructors & Faculty Mentors Showcase.
 *            8. 4-Pillar Educational Trust Factors Grid.
 *            9. Interactive Socratic AI Guidance Banner.
 *            10. GoEdu Comprehensive Educational Footer with GEAC Accreditation.
 * STANDARDS: Strict Zero-Emoji Policy, WCAG 2.2 AA Contrast, Responsive 320px-1920px
 * ========================================================================================
 */

import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import {
  Sparkles,
  ArrowRight,
  BookOpen,
  Atom,
  Play,
  Layers,
  Award,
  ShieldCheck,
  CheckCircle2,
  Clock,
  Swords,
  X
} from 'lucide-react';
import { GoEduNavbar } from '../components/goedu/GoEduNavbar';
import { GoEduHero } from '../components/goedu/GoEduHero';
import { GoEduTrustProof } from '../components/goedu/GoEduTrustProof';
import { GoEduBundleSpotlight } from '../components/goedu/GoEduBundleSpotlight';
import { GoEduCourseGrid } from '../components/goedu/GoEduCourseGrid';
import { GoEduInstructors } from '../components/goedu/GoEduInstructors';
import { GoEduTrustFactors } from '../components/goedu/GoEduTrustFactors';
import { GoEduAIBanner } from '../components/goedu/GoEduAIBanner';
import { GoEduFooter } from '../components/goedu/GoEduFooter';
import { SocraticTutorDrawer } from '../components/ai/SocraticTutorDrawer';
import { PhysicsProjectileLab, ChemistryMolecularViewer } from '../components/stem-labs';
import { KaTeXRenderer } from '../components/quiz/katex-renderer';

export default function FlagshipLandingPage() {
  const [isSocraticDrawerOpen, setIsSocraticDrawerOpen] = useState(false);
  const [activeLabModal, setActiveLabModal] = useState<'physics' | 'chemistry' | null>(null);

  // Live Challenge Countdown timer state (hours, minutes, seconds)
  const [countdown, setCountdown] = useState({ hours: 1, minutes: 24, seconds: 45 });

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev.seconds > 0) {
          return { ...prev, seconds: prev.seconds - 1 };
        } else if (prev.minutes > 0) {
          return { ...prev, minutes: 59, seconds: 59 };
        } else if (prev.hours > 0) {
          return { hours: prev.hours - 1, minutes: 59, seconds: 59 };
        }
        return { hours: 0, minutes: 0, seconds: 0 };
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <>
      <Head>
        <title>অগ্রযাত্রা | বাংলাদেশের সেরা অনলাইন কোর্স ও সক্রেটিক এআই সলভার</title>
        <meta
          name="description"
          content="এনসিটিবি উচ্চমাধ্যমিক স্টেম, বিশ্ববিদ্যালয় ভর্তি প্রস্তুতি এবং প্রফেশনাল স্কিলসের জিইএসি অনুমোদিত অনলাইন কোর্স প্ল্যাটফর্ম।"
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="canonical" href="https://ogrojatra.edu.bd/" />
      </Head>

      <div className="min-h-screen bg-[#FFFCF6] dark:bg-gray-900 text-gray-900 dark:text-white flex flex-col selection:bg-amber-200 dark:selection:bg-amber-900 transition-colors duration-300">
        {/* Floating Pill Navigation Header */}
        <GoEduNavbar onOpenSocraticDrawer={() => setIsSocraticDrawerOpen(true)} />

        <main id="main-content" className="flex-1 w-full">
          {/* Section 1: Sunshine Hero with Typographic Watermark & AI Search */}
          <GoEduHero
            onOpenSocraticDrawer={() => setIsSocraticDrawerOpen(true)}
            onSearchSubmit={query => {
              if (query.trim()) {
                window.location.href = `/courses?query=${encodeURIComponent(query.trim())}`;
              }
            }}
          />

          {/* Section 2: Tri-Card Social Proof Matrix */}
          <GoEduTrustProof />

          {/* Section 3: Featured Accelerator Bundle Spotlight (rounded-[2.5rem]) */}
          <GoEduBundleSpotlight />

          {/* Section 4: Popular Courses & Categorized Skills Grid */}
          <GoEduCourseGrid maxDisplay={8} />

          {/* Section 5: Interactive 3D STEM Virtual Labs (Unique Ogrojatra Feature with GoEdu Polish) */}
          <section className="py-14 sm:py-20 px-4 sm:px-6 lg:px-8 bg-[#FFF6DD]/50 dark:bg-gray-900/60 border-t border-b border-amber-200/50 dark:border-gray-800 transition-colors duration-300">
            <div className="max-w-7xl mx-auto">
              <header className="text-center max-w-3xl mx-auto mb-12">
                <div className="inline-flex items-center gap-2 py-1 px-4 border border-amber-300 dark:border-gray-700 rounded-full mb-3 bg-white dark:bg-gray-800 shadow-sm">
                  <span className="h-2 w-2 rounded-full bg-[#ED8E22]" aria-hidden="true" />
                  <p className="text-xs sm:text-sm font-semibold text-gray-800 dark:text-gray-200">
                    ইন্টারেক্টিভ থ্রিডি বিজ্ঞান ল্যাব ও সিমুলেশন
                  </p>
                </div>
                <h2 className="text-2xl sm:text-4xl font-bold text-[#213130] dark:text-white mb-4 leading-tight">
                  তত্ত্ব নয়, বিজ্ঞান শিখুন বাস্তব সিমুলেশনের মাধ্যমে
                </h2>
                <p className="text-gray-600 dark:text-gray-300 text-sm sm:text-base leading-relaxed">
                  পদার্থবিজ্ঞানের গতিবিদ্যা ও রসায়নের আণবিক বন্ধন পরীক্ষা করুন ভার্চুয়াল থ্রিডি ল্যাবে।
                  মুখস্থ বিদ্যা বাদ দিয়ে বিজ্ঞানের অন্তর্দৃষ্টি গড়ে তুলুন।
                </p>
              </header>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
                {/* Lab 1: Physics Projectile Simulator */}
                <div className="bg-white dark:bg-gray-800 rounded-3xl p-6 sm:p-8 border border-gray-200 dark:border-gray-700 shadow-md flex flex-col justify-between group hover:shadow-xl transition-all">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-xs font-bold text-[#ED8E22] bg-amber-50 dark:bg-amber-950/60 px-3 py-1 rounded-full">
                        পদার্থবিজ্ঞান ১ম পত্র: গতিবিদ্যা
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">৩ডি ভার্চুয়াল ল্যাব</span>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                      প্রক্ষেপক গতি ও ট্র্যাজেক্টরি সিমুলেটর
                    </h3>
                    <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-300 mb-4 leading-relaxed">
                      বিভিন্ন নিক্ষেপণ কোণ ও প্রাথমিক বেগে প্রক্ষেপকের গতিপথ, পাল্লা (Range) ও সর্বোচ্চ উচ্চতা
                      সরাসরি গ্রাফে পর্যবেক্ষণ করুন।
                    </p>
                    <div className="p-3 bg-gray-50 dark:bg-gray-900 rounded-xl mb-4 font-mono text-xs text-gray-700 dark:text-gray-300">
                      <KaTeXRenderer mathContent="R = \frac{v_0^2 \sin(2\theta)}{g}, \quad H = \frac{v_0^2 \sin^2\theta}{2g}" />
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setActiveLabModal('physics')}
                    className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-full bg-[#1E293B] dark:bg-amber-500 text-white dark:text-gray-900 font-semibold text-sm hover:bg-gray-800 dark:hover:bg-amber-400 active:scale-95 transition-all shadow-md"
                  >
                    <Play className="w-4 h-4 fill-current" aria-hidden="true" />
                    <span>ভার্চুয়াল ল্যাব চালু করুন</span>
                  </button>
                </div>

                {/* Lab 2: Chemistry Molecular Lab */}
                <div className="bg-white dark:bg-gray-800 rounded-3xl p-6 sm:p-8 border border-gray-200 dark:border-gray-700 shadow-md flex flex-col justify-between group hover:shadow-xl transition-all">
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-xs font-bold text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/60 px-3 py-1 rounded-full">
                        রসায়ন ১ম পত্র: রাসায়নিক বন্ধন
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">৩ডি মলিকিউলার ভিউয়ার</span>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                      আণবিক জ্যামিতি ও হাইব্রিডাইজেশন ল্যাব
                    </h3>
                    <p className="text-xs sm:text-sm text-gray-600 dark:text-gray-300 mb-4 leading-relaxed">
                      মিথেন, পানি এবং অ্যামোনিয়ার মুক্তজোড় ইলেকট্রন ও বন্ধন কোণের ত্রিমাত্রিক গঠন রোটেশন করে
                      বিশ্লেষণ করুন।
                    </p>
                    <div className="p-3 bg-gray-50 dark:bg-gray-900 rounded-xl mb-4 font-mono text-xs text-gray-700 dark:text-gray-300">
                      <KaTeXRenderer mathContent="\text{sp}^3 \text{ Hybridization: } \theta_{\text{CH}_4} = 109.5^\circ, \quad \theta_{\text{H}_2\text{O}} = 104.5^\circ" />
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={() => setActiveLabModal('chemistry')}
                    className="w-full inline-flex items-center justify-center gap-2 py-3 rounded-full bg-[#1E293B] dark:bg-amber-500 text-white dark:text-gray-900 font-semibold text-sm hover:bg-gray-800 dark:hover:bg-amber-400 active:scale-95 transition-all shadow-md"
                  >
                    <Atom className="w-4 h-4" aria-hidden="true" />
                    <span>আণবিক ল্যাব চালু করুন</span>
                  </button>
                </div>
              </div>
            </div>
          </section>

          {/* Section 6: Live Challenge Countdown & Arena Gateway */}
          <section className="py-12 px-4 sm:px-6 lg:px-8 container mx-auto">
            <div className="rounded-3xl bg-gradient-to-r from-amber-500 to-orange-500 text-white p-6 sm:p-10 flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
              <div className="space-y-2 text-center md:text-left">
                <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/20 rounded-full text-xs font-bold uppercase tracking-wider">
                  <Swords className="w-3.5 h-3.5" aria-hidden="true" />
                  <span>লাইভ জাতীয় চ্যালেঞ্জ</span>
                </div>
                <h3 className="text-2xl sm:text-3xl font-black">
                  আজকের মেগা কুইজ ব্যাটেল: উচ্চতর গণিত ও পদার্থবিজ্ঞান
                </h3>
                <p className="text-xs sm:text-sm text-amber-100 max-w-xl">
                  সারাদেশের শিক্ষার্থীদের সাথে লাইভ স্পিড টেস্টে অংশ নিন এবং রিয়েল-টাইম জাতীয় লিডারবোর্ডে নিজের স্থান যাচাই করুন।
                </p>
              </div>

              <div className="flex items-center gap-4 shrink-0">
                <div className="flex items-center gap-2 text-center">
                  <div className="bg-white/20 backdrop-blur-md px-3 py-2 rounded-xl">
                    <span className="block text-xl font-bold font-mono">
                      {String(countdown.hours).padStart(2, '0')}
                    </span>
                    <span className="text-[10px] text-amber-100 uppercase">ঘন্টা</span>
                  </div>
                  <span className="text-xl font-bold">:</span>
                  <div className="bg-white/20 backdrop-blur-md px-3 py-2 rounded-xl">
                    <span className="block text-xl font-bold font-mono">
                      {String(countdown.minutes).padStart(2, '0')}
                    </span>
                    <span className="text-[10px] text-amber-100 uppercase">মিনিট</span>
                  </div>
                  <span className="text-xl font-bold">:</span>
                  <div className="bg-white/20 backdrop-blur-md px-3 py-2 rounded-xl">
                    <span className="block text-xl font-bold font-mono">
                      {String(countdown.seconds).padStart(2, '0')}
                    </span>
                    <span className="text-[10px] text-amber-100 uppercase">সেকেন্ড</span>
                  </div>
                </div>

                <Link
                  href="/live-challenge"
                  className="px-6 py-3 rounded-full bg-white text-[#ED8E22] font-bold text-sm hover:bg-amber-50 active:scale-95 transition-all shadow-md shrink-0"
                >
                  এরিনায় যোগ দিন
                </Link>
              </div>
            </div>
          </section>

          {/* Section 7: Instructors Showcase */}
          <GoEduInstructors />

          {/* Section 8: Trust Factors */}
          <GoEduTrustFactors />

          {/* Section 9: Socratic AI Guidance Banner */}
          <GoEduAIBanner onOpenSocraticDrawer={() => setIsSocraticDrawerOpen(true)} />
        </main>

        {/* Global Footer */}
        <GoEduFooter />

        {/* Floating Global Socratic AI Tutor Drawer */}
        <SocraticTutorDrawer
          isOpen={isSocraticDrawerOpen}
          onClose={() => setIsSocraticDrawerOpen(false)}
        />

        {/* Interactive 3D STEM Lab Modals */}
        {activeLabModal && (
          <div
            role="dialog"
            aria-modal="true"
            aria-label="3D Virtual Lab Simulator"
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
          >
            <div className="relative w-full max-w-4xl bg-white dark:bg-gray-900 rounded-3xl p-6 shadow-2xl border border-gray-200 dark:border-gray-800 max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between pb-4 mb-4 border-b border-gray-100 dark:border-gray-800">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                  {activeLabModal === 'physics'
                    ? 'গতিবিদ্যা ও প্রক্ষেপক ৩ডি ভার্চুয়াল ল্যাব'
                    : 'আণবিক জ্যামিতি ও বন্ধন কোণ ৩ডি ল্যাব'}
                </h3>
                <button
                  type="button"
                  onClick={() => setActiveLabModal(null)}
                  aria-label="Close Lab Modal"
                  className="p-1.5 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500"
                >
                  <X className="w-5 h-5" aria-hidden="true" />
                </button>
              </div>

              {activeLabModal === 'physics' ? (
                <PhysicsProjectileLab />
              ) : (
                <ChemistryMolecularViewer />
              )}
            </div>
          </div>
        )}
      </div>
    </>
  );
}
