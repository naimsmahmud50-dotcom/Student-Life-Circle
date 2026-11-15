/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Corporate Recruiter Page
 * TOPIC:     Linear/Wellfound Tier Talent Acquisition & Cryptographic Skill Pipeline
 * FILE:      frontend/src/pages/recruiter.tsx
 * PHASE:     Phase 109 - Corporate Talent Acquisition & Cryptographic Skill Pipeline
 * PURPOSE:   Provides enterprise recruiters with a high-density, keyboard-accessible talent hub:
 *            1. Real-time cosine vector matching against verified student skill profiles.
 *            2. Sealed CV snapshot verification ensuring academic immutability.
 *            3. 1-click interview offer dispatch with compensation and scheduling terms.
 *            4. Integration with standard Navbar, Footer, and AppHead.
 * STANDARDS: W3C Verifiable Credentials, Vector Cosine Similarity, Zero-Emoji, UI/UX Pro Max
 */

import React, { useEffect } from 'react';
import {
  Briefcase,
  ShieldCheck,
  Building2,
  Award,
  Sparkles,
  CheckCircle2,
  Code,
  Info
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { CorporateRecruiterPortal } from '@/components/career/CorporateRecruiterPortal';
import { useTranslation } from '@/lib/i18n';

export default function RecruiterPage() {
  const { t, locale } = useTranslation();
  const isBn = locale === 'bn';

  const title = isBn
    ? "কর্পোরেট রিক্রুটার পোর্টাল ও ক্রিপ্টোগ্রাফিক ট্যালেন্ট পাইপলাইন | অগ্রযাত্রা"
    : "Corporate Recruiter Portal & Cryptographic Talent Pipeline | Ogrojatra";
  const description = isBn
    ? "বুয়েট, ঢাবি, সাস্ট ও আইইউটির শীর্ষ গ্র্যাজুয়েটদের যাচাইকৃত দক্ষতা ও প্রজেক্ট পোর্টফোলিও। ডিরেক্ট হায়ার ও রিয়েল-টাইম ভেক্টর ম্যাচিং।"
    : "Verified skill credentials and project portfolios of top university graduates. Direct hiring pipeline with real-time cosine vector matching.";

  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.title = title;
    }
  }, [title]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-bengali selection:bg-blue-500/30 selection:text-blue-200">
      <AppHead
        title={title}
        description={description}
      />
      <Navbar currentStage={isBn ? "কর্পোরেট রিক্রুটার (Recruiter)" : "Corporate Recruiter"} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
        <CorporateRecruiterPortal />

        {/* Corporate Trust & W3C Verifiable Standards Explainer */}
        <section className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800 text-slate-300 space-y-4">
          <div className="flex items-center gap-2.5 text-blue-400 text-sm font-semibold">
            <Info className="w-4 h-4" />
            <span>{isBn ? "কর্পোরেট নিয়োগ নির্দেশিকা ও ক্রিপ্টোগ্রাফিক ভেরিফিকেশন নীতি" : "Corporate Recruitment & Cryptographic Verification Guide"}</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-400 leading-relaxed font-sans">
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">
                {isBn ? "১. W3C ভেরিফায়েড স্কিল সনদ" : "1. W3C Verified Skill Credentials"}
              </div>
              <p>
                {isBn
                  ? "প্রতিটি প্রার্থীর দক্ষতা ল্যাব টেস্ট, প্রোজেক্ট ইমপ্লিমেন্টেশন ও কোড অ্যাসেসমেন্টের মাধ্যমে যাচাই করে ক্রিপ্টোগ্রাফিক হ্যাশ সিগনেচার দিয়ে সিল করা হয়।"
                  : "Every candidate's competencies are audited via lab evaluations, project implementations, and code assessments, cryptographically sealed with hash signatures."}
              </p>
            </div>
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">
                {isBn ? "২. কোসাইন ভেক্টর মিল (Cosine Similarity)" : "2. Cosine Vector Similarity"}
              </div>
              <p>
                {isBn
                  ? "আপনার নিয়োগের প্রযুক্তিগত চাহিদার সাথে প্রার্থীর দক্ষতার ডাইমেনশনাল ভেক্টর বিশ্লেষণ করে শতভাগ নিরপেক্ষ উপযুক্ততা স্কোর নির্ণয় করা হয়।"
                  : "Dimensional vector analysis calculates completely objective compatibility scores matching your technical hiring requirements with candidate skill vectors."}
              </p>
            </div>
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">
                {isBn ? "৩. সরাসরি নিয়োগ ও নো-স্প্যাম গ্যারান্টি" : "3. Direct Hiring & Zero Spam Guarantee"}
              </div>
              <p>
                {isBn
                  ? "মধ্যস্থতাকারী ছাড়াই সরাসরি যাচাইকৃত প্রার্থীর সাথে ১-ক্লিকে ইন্টারভিউ অফার ও বেতন আলোচনা চূড়ান্ত করুন।"
                  : "Directly dispatch interview invitations and settle compensation with verified talent in 1 click, free from intermediary friction."}
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
