/**
 * DEVELOPER ARCHITECTURE NOTE:
 * ========================================================================================
 * MODULE:    Study Pods & Collaborative Classroom Page
 * FILE:      frontend/src/pages/study-pod.tsx
 * PHASE:     Phase 101 - Real-Time Study Pods & Collaborative Whiteboard
 * PURPOSE:   Provides full-page real-time study pod classroom experience:
 *            1. Global Layout: Responsive Navbar and comprehensive Footer wrapper.
 *            2. StudyPodRoom Integration: Dynamic 2-8 student audio/video grid with VAD pulses.
 *            3. Collaborative Whiteboard: HTML5 vector drawing and KaTeX math notation stamps.
 *            4. Strict Zero-Emoji compliance: 100% Lucide-React SVG vectors.
 * AUDIENCE:  HSC & Admission Students, Peer Study Cohorts, Tutors.
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AAA Contrast, Zero Layout Shift, Zero-Emoji.
 * ========================================================================================
 */

import React, { useState } from 'react';
import {
  Users,
  PenTool,
  ShieldCheck,
  Sparkles,
  ArrowRight,
  BookOpen,
  HelpCircle,
  Plus
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { StudyPodRoom } from '@/components/study-pods/StudyPodRoom';

export default function StudyPodPage() {
  const [activePodId, setActivePodId] = useState<string>('pod-hsc-higher-math-2026');
  const [isInRoom, setIsInRoom] = useState<boolean>(true);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-bengali">
      <AppHead
        title="লাইভ স্টাডি পড ও হোয়াইটবোর্ড | অগ্রযাত্রা"
        description="উচ্চ মাধ্যমিক ও বিশ্ববিদ্যালয় ভর্তি পরীক্ষার জন্য সহপাঠীদের সাথে রিয়েল-টাইম স্টাডি পড ও গাণিতিক হোয়াইটবোর্ড।"
      />

      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col">
        {/* Breadcrumb & Intro */}
        <div className="mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold text-blue-400 uppercase tracking-wider mb-1">
              <Users className="w-4 h-4" strokeWidth={1.75} />
              <span>সহশিক্ষণ সার্কেল (Peer Study Pods)</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight font-display">
              রিয়েল-টাইম স্টাডি পড ও সহযোগী হোয়াইটবোর্ড
            </h1>
            <p className="text-sm text-slate-400 mt-1 max-w-2xl">
              সর্বোচ্চ ৮ জন শিক্ষার্থীর নিবিড় ভার্চুয়াল স্টাডি গ্রুপ। রিয়েল-টাইম অডিও মেশ, ফ্রিহ্যান্ড জ্যামিতি এবং KaTeX গাণিতিক সমীকরণ সমাধান করুন একসাথে।
            </p>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-950/80 border border-emerald-800/60 text-emerald-400 text-xs font-semibold">
              <ShieldCheck className="w-4 h-4" strokeWidth={1.75} />
              <span>P2P এনক্রিপ্টেড অডিও মেশ</span>
            </div>
          </div>
        </div>

        {/* Room Container */}
        {isInRoom ? (
          <div className="flex-1 w-full">
            <StudyPodRoom
              podId={activePodId}
              currentUserId="usr-me-student-01"
              currentUserName="তুমি (Student)"
              podTitle="HSC Higher Math: Calculus & Conics Problem Solving"
              subject="Higher Mathematics"
              onLeave={() => setIsInRoom(false)}
            />
          </div>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center p-12 rounded-3xl bg-slate-900 border border-slate-800 text-center space-y-4">
            <div className="w-16 h-16 rounded-3xl bg-blue-600/20 text-blue-400 flex items-center justify-center mx-auto">
              <BookOpen className="w-8 h-8" strokeWidth={1.75} />
            </div>
            <h2 className="text-xl font-bold text-white">
              তুমি স্টাডি পড থেকে প্রস্থান করেছ
            </h2>
            <p className="text-sm text-slate-400 max-w-md">
              তুমি যেকোনো সময় তোমার সহপাঠীদের সাথে পুনরায় এই স্টাডি পডে যোগ দিতে পারো।
            </p>
            <button
              type="button"
              onClick={() => setIsInRoom(true)}
              className="btn-push-brand px-6 py-2.5 rounded-2xl bg-blue-600 text-white font-semibold text-sm shadow-lg active:scale-95 transition-all"
            >
              পুনরায় প্রবেশ করুন
            </button>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
