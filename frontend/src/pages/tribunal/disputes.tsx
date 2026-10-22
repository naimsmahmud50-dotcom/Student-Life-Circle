/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Parent-Teacher Conference & Escrow Dispute Tribunal
 * TOPIC:     Phase 130 Institutional Appointment & Formal Escrow Arbitration
 * FILE:      frontend/src/pages/tribunal/disputes.tsx
 * PHASE:     Phase 130 - Institutional PTC & Escrow Dispute Tribunal
 * PURPOSE:   Provides formal institutional escrow dispute tribunal docket interface,
 *            3-party arbitration case management, cryptographic evidence viewer,
 *            ombudsman settlement controls, and 3D tactile button interactions.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Strict Supabase RLS, Pure Academic UI
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Scale,
  ShieldCheck,
  FileText,
  CheckCircle2,
  AlertCircle,
  Gavel,
  Clock,
  ChevronRight,
  RotateCcw,
  Users,
  Layers,
  Lock,
  Award,
  ArrowRight,
  Sparkles,
  DollarSign
} from 'lucide-react';
import { AppHead } from '../../components/layout/Head';
import { Navbar } from '../../components/layout/Navbar';
import { Footer } from '../../components/layout/Footer';
import { toBengaliDigits } from '../../lib/i18n';

interface DisputeCaseItem {
  id: string;
  caseNumber: string;
  guardianName: string;
  tutorName: string;
  subjectBn: string;
  escrowAmount: number;
  status: 'LODGED' | 'EVIDENCE_SUBMITTED' | 'IN_HEARING' | 'RESOLVED_SPLIT' | 'RESOLVED_RELEASE';
  lodgedDate: string;
  guardianGrievanceBn: string;
  tutorCounterBn: string;
  evidenceList: {
    id: string;
    title: string;
    submitter: string;
    hash: string;
    verified: boolean;
  }[];
  defaultSplitTutor: number; // 0.0 to 1.0
}

const SAMPLE_DISPUTES: DisputeCaseItem[] = [
  {
    id: 'disp_001',
    caseNumber: 'TRIB-2026-881',
    guardianName: 'মো. রফিকুল ইসলাম (অভিভাবক)',
    tutorName: 'তানভীর আহমেদ (বুয়েট সিএসই - টিউটর)',
    subjectBn: 'উচ্চতর গণিত ও পদার্থবিজ্ঞান (HSC 2026)',
    escrowAmount: 8500,
    status: 'IN_HEARING',
    lodgedDate: '১২ অক্টোবর ২০২৬',
    guardianGrievanceBn: 'চুক্তিবদ্ধ ১২টি ক্লাসের মধ্যে টিউটর ৮টি ক্লাস নিয়েছেন এবং শেষ মুহূর্তের মডেল টেস্ট না নিয়েই অবশিষ্ট অর্থ উত্তোলনের দাবি করেছেন।',
    tutorCounterBn: 'আমি নির্ধারিত ৮টি বিস্তারিত ক্লাসের পাশাপাশি অনলাইনে অতিরিক্ত ৩টি সমস্যা সমাধান সেশন নিয়েছি। শিক্ষার্থীর অনুপস্থিতির কারণে শেষ ক্লাসটি স্থগিত ছিল।',
    evidenceList: [
      {
        id: 'ev_01',
        title: 'ডিজিটাল ক্লাসরুম এটেনডেন্স লগ (৮ সেশন উপস্থিতি)',
        submitter: 'তানভীর আহমেদ (টিউটর)',
        hash: 'e89f41b2c79a25d7e01f681a',
        verified: true,
      },
      {
        id: 'ev_02',
        title: 'হোয়াটসঅ্যাপ চ্যাট ও ক্লাস স্থগিতের স্ক্রিনশট',
        submitter: 'মো. রফিকুল ইসলাম (অভিভাবক)',
        hash: 'b12a8839c4d817f590a214ee',
        verified: true,
      },
      {
        id: 'ev_03',
        title: 'সিলবাস ট্র্যাকার অগ্রগতি প্রতিবেদন (৭২% সম্পন্ন)',
        submitter: 'প্ল্যাটফর্ম অডিট সিস্টেম',
        hash: 'fa99321c7d88e00192bc54a1',
        verified: true,
      },
    ],
    defaultSplitTutor: 0.70, // 70% to tutor, 30% to guardian
  },
  {
    id: 'disp_002',
    caseNumber: 'TRIB-2026-894',
    guardianName: 'সুলতানা পারভীন (অভিভাবক)',
    tutorName: 'মেহজাবিন চৌধুরী (ঢাবি রসায়ন - টিউটর)',
    subjectBn: 'জৈব রসায়ন প্র্যাকটিক্যাল ও মডেল টেস্ট',
    escrowAmount: 5000,
    status: 'EVIDENCE_SUBMITTED',
    lodgedDate: '১৫ অক্টোবর ২০২৬',
    guardianGrievanceBn: 'পরিকল্পিত ৪টি ল্যাব সেশনের মধ্যে টিউটর মাত্র ১টি পরিচালনা করেছেন। অবশিষ্ট ৪,০০০ টাকা অবিলম্বে রিফান্ড আবশ্যক।',
    tutorCounterBn: 'ল্যাব উপকরণের অপ্রতুলতার কারণে থিওরিটিক্যাল ড্রাফটিং সম্পন্ন হয়েছে। অবশিষ্ট ৩টি সেশন আগামী সপ্তাহে নেওয়ার আবেদন জানিয়েছি।',
    evidenceList: [
      {
        id: 'ev_11',
        title: 'হোম ভিজিট বায়োমেট্রিক চেক-ইন রিপোর্ট (১টি ভিজিট)',
        submitter: 'সুলতানা পারভীন (অভিভাবক)',
        hash: '44c01a9df8217bb3a01123fe',
        verified: true,
      },
    ],
    defaultSplitTutor: 0.25,
  },
];

export default function DisputeTribunalPage() {
  const [selectedCaseIndex, setSelectedCaseIndex] = useState<number>(0);
  const [rulingSelection, setRulingSelection] = useState<'SPLIT' | 'RELEASE' | 'REFUND'>('SPLIT');
  const [customTutorRatio, setCustomTutorRatio] = useState<number>(70);
  const [isRulingExecuted, setIsRulingExecuted] = useState<boolean>(false);

  const currentCase = SAMPLE_DISPUTES[selectedCaseIndex];
  const escrowTotal = currentCase.escrowAmount;

  // Calculated payouts
  let tutorPayout = 0;
  let guardianPayout = 0;

  if (rulingSelection === 'RELEASE') {
    tutorPayout = escrowTotal;
    guardianPayout = 0;
  } else if (rulingSelection === 'REFUND') {
    tutorPayout = 0;
    guardianPayout = escrowTotal;
  } else {
    tutorPayout = Math.round((escrowTotal * customTutorRatio) / 100);
    guardianPayout = escrowTotal - tutorPayout;
  }

  const handleExecuteRuling = () => {
    setIsRulingExecuted(true);
  };

  const handleReset = () => {
    setIsRulingExecuted(false);
    setRulingSelection('SPLIT');
    setCustomTutorRatio(70);
  };

  return (
    <div className="min-h-screen bg-[#FAFAF8] text-[#0A2540] flex flex-col font-sans">
      <AppHead
        title="প্রাতিষ্ঠানিক এসক্রো বিরোধ নিষ্পত্তি ট্রাইব্যুনাল | অগ্রযাত্রা"
        description="শিক্ষক, অভিভাবক ও প্রাতিষ্ঠানিক অম্বুডসম্যান সমন্বিত ৩-পক্ষীয় এসক্রো আরবিট্রেশন ও সুরক্ষিত নিষ্পত্তি আদালত।"
      />

      <Navbar />

      {/* Tribunal Bench Header */}
      <section className="bg-[#0A2540] text-white py-12 px-4 sm:px-6 lg:px-8 border-b-4 border-[#B45309]">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-300 mb-3">
            <Link href="/" className="hover:text-white transition-colors">হোম</Link>
            <ChevronRight className="w-3.5 h-3.5" />
            <Link href="/tuition" className="hover:text-white transition-colors">টিউশন ভল্ট</Link>
            <ChevronRight className="w-3.5 h-3.5" />
            <span className="text-amber-400">এসক্রো বিরোধ ট্রাইব্যুনাল</span>
          </div>

          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-white/10 text-amber-300 text-xs font-medium mb-3">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>ASVS L2 জিরো-IDOR নীতি • ৩-পক্ষীয় প্রাতিষ্ঠানিক আরবিট্রেশন বেঞ্চ</span>
              </div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-white flex items-center gap-3">
                <Scale className="w-8 h-8 text-amber-400 shrink-0" />
                <span>প্রাতিষ্ঠানিক এসক্রো বিরোধ নিষ্পত্তি ট্রাইব্যুনাল</span>
              </h1>
              <p className="mt-2 text-sm sm:text-base text-slate-200 max-w-3xl leading-relaxed">
                অভিভাবক, গৃহশিক্ষক ও নিরপেক্ষ অ্যাকাডেমিক অম্বুডসম্যানের উপস্থিতিতে টিউটরিং ফি এসক্রো সংক্রান্ত বিরোধের চূড়ান্ত আইনি ও আর্থিক নিষ্পত্তি।
              </p>
            </div>

            <div className="flex items-center gap-3">
              <Link
                href="/guardian/ptc"
                className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg border border-white/30 bg-white/5 hover:bg-white/10 text-white transition-colors"
              >
                <Users className="w-4 h-4 text-amber-300" />
                <span>অভিভাবক-শিক্ষক কনফারেন্স (PTC)</span>
              </Link>
              <button
                onClick={handleReset}
                className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
              >
                <RotateCcw className="w-4 h-4 text-slate-300" />
                <span>কেস রিসেট</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Main Tribunal Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* Left Column: Active Docket Case List (4 Cols) */}
          <div className="lg:col-span-4 space-y-4">
            <div className="bg-white rounded-xl border border-slate-300 p-5 shadow-sm">
              <div className="flex items-center gap-2 mb-3 pb-2 border-b border-slate-200">
                <FileText className="w-5 h-5 text-[#0A2540]" />
                <h2 className="text-sm font-bold uppercase tracking-wider text-[#0A2540]">
                  সক্রিয় বিরোধ ডকেট তালিকা (Active Dockets)
                </h2>
              </div>

              <div className="space-y-3">
                {SAMPLE_DISPUTES.map((d, idx) => (
                  <button
                    key={d.id}
                    onClick={() => {
                      setSelectedCaseIndex(idx);
                      setIsRulingExecuted(false);
                    }}
                    className={`w-full text-left p-4 rounded-lg border transition-all ${
                      selectedCaseIndex === idx
                        ? 'border-[#0A2540] bg-slate-50 ring-1 ring-[#0A2540]'
                        : 'border-slate-200 hover:border-slate-300 bg-white'
                    }`}
                  >
                    <div className="flex justify-between items-center mb-1.5">
                      <span className="font-mono text-xs font-bold text-[#0A2540]">{d.caseNumber}</span>
                      <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-amber-100 text-amber-800">
                        {d.status === 'IN_HEARING' ? 'শুনানী চলছে' : 'প্রমাণাধীন'}
                      </span>
                    </div>

                    <h3 className="text-xs font-bold text-slate-800 line-clamp-1">{d.subjectBn}</h3>
                    <p className="text-[11px] text-slate-500 mt-0.5">{d.tutorName}</p>

                    <div className="mt-3 pt-2 border-t border-slate-200 flex justify-between items-center text-xs">
                      <span className="text-slate-500">বিরোধকৃত এসক্রো:</span>
                      <span className="font-extrabold text-[#0A2540]">৳ {toBengaliDigits(d.escrowAmount.toLocaleString())}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Zero-IDOR Security Assurance Card */}
            <div className="bg-slate-100 rounded-xl p-5 border border-slate-300 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
                <ShieldCheck className="w-4 h-4 text-emerald-700" />
                <span>জিরো-IDOR ও আরএলএস নিরাপত্তা নীতি</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                সুপাবেস RLS পলিসির মাধ্যমে নিশ্চিত করা হয়েছে যে, সংশ্লিষ্ট অভিভাবক এবং গৃহশিক্ষক ছাড়া কোনো তৃতীয় ব্যবহারকারী বা অননুমোদিত ব্যক্তি এই মামলার নথি বা প্রমাণ দেখতে পারবে না।
              </p>
            </div>
          </div>

          {/* Right Column: Case File, Evidence Vault & Ombudsman Rulings (8 Cols) */}
          <div className="lg:col-span-8 space-y-6">

            {/* Case Particulars Header Card */}
            <div className="bg-white rounded-xl border border-slate-300 p-6 shadow-sm">
              <div className="flex flex-wrap items-center justify-between gap-3 mb-4 pb-4 border-b border-slate-200">
                <div>
                  <span className="font-mono text-xs font-bold text-slate-500 block">কেস রেফারেন্স</span>
                  <h3 className="text-lg sm:text-xl font-bold text-[#0A2540]">{currentCase.caseNumber}</h3>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-500 block">লকড এসক্রো পরিমাণ</span>
                  <span className="text-xl sm:text-2xl font-black text-[#0A2540]">
                    ৳ {toBengaliDigits(currentCase.escrowAmount.toLocaleString())}
                  </span>
                </div>
              </div>

              {/* Opposing Claims Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-rose-50/60 border border-rose-200">
                  <span className="text-xs font-bold text-rose-900 block mb-1">
                    অভিভাবকের আনুষ্ঠানিক অভিযোগ:
                  </span>
                  <span className="text-[11px] text-slate-500 block mb-2">{currentCase.guardianName}</span>
                  <p className="text-xs text-slate-800 leading-relaxed">
                    "{currentCase.guardianGrievanceBn}"
                  </p>
                </div>

                <div className="p-4 rounded-lg bg-blue-50/60 border border-blue-200">
                  <span className="text-xs font-bold text-blue-900 block mb-1">
                    গৃহশিক্ষকের আত্মপক্ষ বক্তব্য:
                  </span>
                  <span className="text-[11px] text-slate-500 block mb-2">{currentCase.tutorName}</span>
                  <p className="text-xs text-slate-800 leading-relaxed">
                    "{currentCase.tutorCounterBn}"
                  </p>
                </div>
              </div>
            </div>

            {/* Hashed Evidence Inspection Vault */}
            <div className="bg-white rounded-xl border border-slate-300 p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-200">
                <div className="flex items-center gap-2">
                  <Lock className="w-5 h-5 text-[#0A2540]" />
                  <h3 className="text-base font-bold text-[#0A2540]">
                    প্রমাণ সংরক্ষণাগার (SHA-256 Tamper-Proof Vault)
                  </h3>
                </div>
                <span className="text-xs text-slate-500 font-medium">
                  {toBengaliDigits(currentCase.evidenceList.length)} টি অকাট্য প্রমাণপত্র দাখিলকৃত
                </span>
              </div>

              <div className="space-y-3">
                {currentCase.evidenceList.map((ev) => (
                  <div
                    key={ev.id}
                    className="p-3.5 rounded-lg border border-slate-200 bg-slate-50 flex flex-col sm:flex-row sm:items-center justify-between gap-2"
                  >
                    <div className="space-y-0.5">
                      <div className="flex items-center gap-2">
                        <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                        <span className="text-xs font-bold text-slate-900">{ev.title}</span>
                      </div>
                      <span className="text-[11px] text-slate-500 block">দাখিলকারী: {ev.submitter}</span>
                    </div>

                    <div className="text-left sm:text-right shrink-0">
                      <span className="font-mono text-[10px] text-slate-500 block">
                        SHA-256: {ev.hash}...
                      </span>
                      <span className="text-[10px] font-bold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded inline-block mt-0.5">
                        অডিট ভেরিফাইড
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Ombudsman Arbitration Ruling Bench */}
            <div className="bg-white rounded-xl border-2 border-[#0A2540] p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-200">
                <Gavel className="w-5 h-5 text-[#B45309]" />
                <h3 className="text-base font-bold text-[#0A2540]">
                  অম্বুডসম্যান আরবিট্রেশন ও মীমাংসা রায় (Arbitration Bench)
                </h3>
              </div>

              {!isRulingExecuted ? (
                <div className="space-y-5">
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <button
                      onClick={() => setRulingSelection('SPLIT')}
                      className={`p-3.5 rounded-lg border text-left transition-all ${
                        rulingSelection === 'SPLIT'
                          ? 'border-[#0A2540] bg-slate-50 ring-1 ring-[#0A2540]'
                          : 'border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      <span className="text-xs font-bold text-[#0A2540] block mb-1">
                        ১. আনুপাতিক ভাগ (Split)
                      </span>
                      <p className="text-[11px] text-slate-600 leading-tight">
                        সম্পাদিত ক্লাসের অনুপাতে অর্থ বণ্টন (শিক্ষক ও অভিভাবক)।
                      </p>
                    </button>

                    <button
                      onClick={() => setRulingSelection('RELEASE')}
                      className={`p-3.5 rounded-lg border text-left transition-all ${
                        rulingSelection === 'RELEASE'
                          ? 'border-[#0A2540] bg-slate-50 ring-1 ring-[#0A2540]'
                          : 'border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      <span className="text-xs font-bold text-[#0A2540] block mb-1">
                        ২. সম্পূর্ণ শিক্ষককে প্রদান
                      </span>
                      <p className="text-[11px] text-slate-600 leading-tight">
                        ১০০% এসক্রো গৃহশিক্ষকের অ্যাকাউন্টে স্থানান্তর।
                      </p>
                    </button>

                    <button
                      onClick={() => setRulingSelection('REFUND')}
                      className={`p-3.5 rounded-lg border text-left transition-all ${
                        rulingSelection === 'REFUND'
                          ? 'border-[#0A2540] bg-slate-50 ring-1 ring-[#0A2540]'
                          : 'border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      <span className="text-xs font-bold text-[#0A2540] block mb-1">
                        ৩. সম্পূর্ণ অভিভাবককে রিফান্ড
                      </span>
                      <p className="text-[11px] text-slate-600 leading-tight">
                        ১০০% এসক্রো অভিভাবকের ওয়ালেটে ফেরত।
                      </p>
                    </button>
                  </div>

                  {/* Split slider if selected */}
                  {rulingSelection === 'SPLIT' && (
                    <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
                      <div className="flex justify-between items-center text-xs font-bold">
                        <span className="text-slate-700">শিক্ষকের বরাদ্দ অনুপাত:</span>
                        <span className="text-[#0A2540]">{toBengaliDigits(customTutorRatio)}%</span>
                      </div>
                      <input
                        type="range"
                        min="10"
                        max="90"
                        step="5"
                        value={customTutorRatio}
                        onChange={(e) => setCustomTutorRatio(parseInt(e.target.value, 10))}
                        className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-[#0A2540]"
                      />
                      <div className="flex justify-between text-[10px] text-slate-500 font-medium">
                        <span>১০% শিক্ষক (৯০% অভিভাবক)</span>
                        <span>৫০% সমবণ্টন</span>
                        <span>৯০% শিক্ষক (১০% অভিভাবক)</span>
                      </div>
                    </div>
                  )}

                  {/* Calculated Payout Summary Cards */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3.5 rounded-lg bg-emerald-50 border border-emerald-300">
                      <span className="text-xs text-emerald-800 font-medium block">শিক্ষককে প্রদেয়:</span>
                      <span className="text-lg font-bold text-emerald-950">
                        ৳ {toBengaliDigits(tutorPayout.toLocaleString())}
                      </span>
                    </div>

                    <div className="p-3.5 rounded-lg bg-blue-50 border border-blue-300">
                      <span className="text-xs text-blue-800 font-medium block">অভিভাবককে রিফান্ড:</span>
                      <span className="text-lg font-bold text-blue-950">
                        ৳ {toBengaliDigits(guardianPayout.toLocaleString())}
                      </span>
                    </div>
                  </div>

                  {/* 3D Tactile Push Button to Execute Ruling */}
                  <button
                    onClick={handleExecuteRuling}
                    className="w-full py-3.5 px-4 bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] hover:bg-[#081C30] active:translate-y-1 active:shadow-none transition-all font-semibold rounded-lg flex items-center justify-center gap-2 text-sm"
                  >
                    <Gavel className="w-4 h-4 text-amber-300" />
                    <span>চূড়ান্ত আরবিট্রেশন রায় প্রদান ও এসক্রো রিলিজ করুন</span>
                  </button>
                </div>
              ) : (
                <div className="p-5 bg-emerald-50 rounded-lg border-2 border-emerald-600 space-y-3">
                  <div className="flex items-center gap-2 text-emerald-900 font-bold text-sm">
                    <CheckCircle2 className="w-5 h-5 text-emerald-700" />
                    <span>আরবিট্রেশন রায় সফলভাবে কার্যকরের নির্দেশ জারি হয়েছে</span>
                  </div>
                  <p className="text-xs text-emerald-900 leading-relaxed font-medium">
                    অম্বুডসম্যানের বিচারিক রায়ানুযায়ী শিক্ষককে <strong>৳ {toBengaliDigits(tutorPayout.toLocaleString())}</strong> এবং অভিভাবককে <strong>৳ {toBengaliDigits(guardianPayout.toLocaleString())}</strong> স্বয়ংক্রিয়ভাবে ডিসবার্স করা হয়েছে। ডকেটটি সফলভাবে নিষ্পন্ন ও সিলগালা করা হয়েছে।
                  </p>
                  <div className="pt-2 border-t border-emerald-200 flex justify-between text-[11px] text-emerald-800 font-mono">
                    <span>রুলিং হ্যাশ: e499ac0032a76f...</span>
                    <span>স্ট্যাটাস: RESOLVED_SPLIT</span>
                  </div>
                </div>
              )}
            </div>

          </div>

        </div>
      </main>

      <Footer />
    </div>
  );
}
