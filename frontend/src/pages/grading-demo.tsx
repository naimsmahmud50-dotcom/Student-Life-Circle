/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Handwritten Script OCR & Rubric Grader Page
 * FILE:      frontend/src/pages/grading-demo.tsx
 * PHASE:     Phase 103 - Handwritten Script OCR & Step-by-Step Rubric Grader
 * PURPOSE:   Demonstration and testing page for handwritten exam paper ingestion,
 *            NCTB 4-step rubric evaluation, and compassionate teacher marking feedback.
 * STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
 */

import React, { useState } from 'react';
import {
  FileText,
  Camera,
  GraduationCap,
  Sparkles,
  ShieldCheck,
  BookOpen,
  ArrowRight,
  HelpCircle
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { HandwrittenUploadModal } from '@/components/grading/HandwrittenUploadModal';
import { GradingFeedbackCard } from '@/components/grading/GradingFeedbackCard';
import { KaTeXRenderer } from '@/components/quiz/katex-renderer';

export default function GradingDemoPage() {
  const [isUploadOpen, setIsUploadOpen] = useState<boolean>(false);
  const [hasEvaluated, setHasEvaluated] = useState<boolean>(true);
  const [score, setScore] = useState<number>(3.0);

  const handleScriptSubmitted = (data: { questionId: string; imageBase64: string; contrastLevel: number }) => {
    setHasEvaluated(true);
    setScore(3.0);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-bengali">
      <AppHead
        title="হাতে লেখা খাতা মূল্যায়ন ও মার্কিং রুব্রিক | অগ্রযাত্রা"
        description="উচ্চ মাধ্যমিক ও ভর্তি পরীক্ষার বর্ণনামূলক গণিত ও বিজ্ঞান খাতার স্বয়ংক্রিয় শিক্ষক-মান মূল্যায়ণ।"
      />

      <Navbar />

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col space-y-8">
        {/* Header Intro */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-800/80">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">
              <Camera className="w-4 h-4" strokeWidth={1.75} />
              <span>স্মার্ট খাতা মূল্যায়ন (OCR Rubric Grader)</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight font-display">
              হাতে লেখা খাতা স্ক্যান ও ধাপভিত্তিক মার্কিং
            </h1>
            <p className="text-sm text-slate-400 mt-1 max-w-2xl">
              শুধু এমসিকিউ নয়, এবার খাতার বর্ণনামূলক গাণিতিক সমাধানও নিখুঁতভাবে যাচাই হবে শিক্ষক-সুলভ মমতায়।
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => setIsUploadOpen(true)}
              className="px-5 py-2.5 rounded-2xl bg-blue-600 text-white font-semibold text-xs shadow-[0_4px_0_0_#1D4ED8] hover:shadow-[0_2px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none transition-all flex items-center gap-2"
            >
              <Camera className="w-4 h-4" strokeWidth={1.75} />
              <span>নতুন খাতার ছবি তুলুন</span>
            </button>
          </div>
        </div>

        {/* Exam Problem Statement Box */}
        <section className="p-6 rounded-3xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-blue-400 uppercase tracking-wider">
              পরীক্ষার উদ্দীপক ও প্রশ্ন (HSC পদার্থবিজ্ঞান ১ম পত্র)
            </span>
            <span className="px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 text-xs font-numeric font-semibold">
              পূর্ণমান: ৪.০
            </span>
          </div>

          <h3 className="text-base font-bold text-white leading-relaxed">
            একটি প্রক্ষেপককে ভূ-পৃষ্ঠ থেকে <span className="font-numeric">40 m/s</span> বেগে <span className="font-numeric">30°</span> কোণে নিক্ষেপ করা হলো। এর সর্বাধিক উচ্চতা (<span className="font-mono">H</span>) কত হবে? [অভিকর্ষজ ত্বরণ <span className="font-numeric">g = 9.8 m/s²</span>]
          </h3>

          <div className="p-3 rounded-2xl bg-slate-950/80 border border-slate-800 flex items-center gap-3 text-xs text-slate-400">
            <span className="font-semibold text-slate-300 shrink-0">প্রত্যাশিত সমীকরণ:</span>
            <KaTeXRenderer content="$H = \frac{u^2 \sin^2\theta}{2g}$" />
          </div>
        </section>

        {/* Evaluated Teacher Feedback Card */}
        {hasEvaluated && (
          <section className="space-y-4">
            <div className="flex items-center justify-between px-1">
              <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                শিক্ষকের খাতা মূল্যায়ন ও মার্কিং শিট
              </span>
              <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" strokeWidth={1.75} />
                <span>NCTB বোর্ড স্ট্যান্ডার্ড যাচাইকৃত</span>
              </span>
            </div>

            <GradingFeedbackCard
              questionTitle="প্রক্ষেপকের সর্বাধিক উচ্চতা নির্ণয়"
              totalScore={score}
              maxScore={4.0}
              percentage={75.0}
              steps={[]}
              teacherSummary="বেশ ভালো চেষ্টা করেছ! সূত্র ও মান বসানো চমৎকার হয়েছে, তবে শেষের দিকে গণনায় সামান্য মনোযোগ দিলেই পূর্ণ ৪/৪ নম্বর অর্জন সম্ভব।"
              onRetryDrill={() => setIsUploadOpen(true)}
            />
          </section>
        )}
      </main>

      <Footer />

      {/* Upload Modal */}
      <HandwrittenUploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onSubmitScript={handleScriptSubmitted}
        questionId="q-physics-projectile-01"
        problemTitle="প্রক্ষেপকের সর্বাধিক উচ্চতা নির্ণয় (HSC পদার্থবিজ্ঞান)"
      />
    </div>
  );
}
