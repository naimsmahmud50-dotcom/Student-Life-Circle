/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Parent-Teacher Conference & Escrow Dispute Tribunal
 * TOPIC:     Phase 130 Institutional Appointment & Formal Escrow Arbitration
 * FILE:      frontend/src/pages/guardian/ptc.tsx
 * PHASE:     Phase 130 - Institutional PTC & Escrow Dispute Tribunal
 * PURPOSE:   Provides guardian interface for booking institutional Parent-Teacher
 *            Conferences (PTC), selecting verified educators, scheduling time slots,
 *            setting conference agendas, and reviewing confirmed passes.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Strict Supabase RLS, Pure Academic UI
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  Calendar,
  Clock,
  Users,
  CheckCircle2,
  ShieldCheck,
  FileText,
  Sparkles,
  RotateCcw,
  Building2,
  Award,
  ArrowRight,
  ChevronRight,
  Lock,
  MessageSquare,
  AlertCircle
} from 'lucide-react';
import { AppHead } from '../../components/layout/Head';
import { Navbar } from '../../components/layout/Navbar';
import { Footer } from '../../components/layout/Footer';
import { toBengaliDigits } from '../../lib/i18n';

interface EducatorOption {
  id: string;
  nameBn: string;
  institutionBn: string;
  subjectBn: string;
  experienceBn: string;
  rating: number;
}

const EDUCATORS: EducatorOption[] = [
  {
    id: 't_01',
    nameBn: 'প্রকৌশলী সাজিদ আহমেদ',
    institutionBn: 'নটর ডেম কলেজ (অতিথি প্রভাষক) ও বুয়েট অ্যালামনাই',
    subjectBn: 'পদার্থবিজ্ঞান (HSC 2026)',
    experienceBn: '৮ বছরের অভিজ্ঞতা',
    rating: 4.9,
  },
  {
    id: 't_02',
    nameBn: 'ফারহানা ইয়াসমিন',
    institutionBn: 'ভিকারুননিসা নূন স্কুল অ্যান্ড কলেজ ও ঢাবি গণিত',
    subjectBn: 'উচ্চতর গণিত ও ক্যালকুলাস',
    experienceBn: '৬ বছরের অভিজ্ঞতা',
    rating: 4.8,
  },
  {
    id: 't_03',
    nameBn: 'ড. রফিকুল আলম',
    institutionBn: 'ঢাকা রেসিডেনসিয়াল মডেল কলেজ ও ঢাকা মেডিকেল অ্যালামনাই',
    subjectBn: 'জীববিজ্ঞান ও মেডিকেল প্রস্তুতি',
    experienceBn: '১২ বছরের অভিজ্ঞতা',
    rating: 5.0,
  },
];

interface TimeSlotOption {
  id: string;
  timeRangeBn: string;
  isAvailable: boolean;
}

const TIME_SLOTS: TimeSlotOption[] = [
  { id: 's_1', timeRangeBn: '০৩:০০ - ০৩:৩০ অপরাহ্ন', isAvailable: true },
  { id: 's_2', timeRangeBn: '০৩:৪০ - ০৪:১০ অপরাহ্ন', isAvailable: false },
  { id: 's_3', timeRangeBn: '০৪:২০ - ০৪:৫০ অপরাহ্ন', isAvailable: true },
  { id: 's_4', timeRangeBn: '০৫:০০ - ০৫:৩০ অপরাহ্ন', isAvailable: true },
  { id: 's_5', timeRangeBn: '০৭:০০ - ০৭:৩০ সন্ধ্যা', isAvailable: true },
];

export default function ParentTeacherConferencePage() {
  const [selectedEducatorId, setSelectedEducatorId] = useState<string>('t_01');
  const [selectedSlotId, setSelectedSlotId] = useState<string>('s_1');
  const [selectedAgenda, setSelectedAgenda] = useState<string>('ACADEMIC_PROGRESS');
  const [notes, setNotes] = useState<string>('মডেল টেস্টের পদার্থবিজ্ঞান দ্বিতীয় পত্রে নম্বরের অবনতি এবং রিভিশন কৌশল নিয়ে আলোচনা করতে চাই।');
  const [isBooked, setIsBooked] = useState<boolean>(false);

  const selectedEducator = EDUCATORS.find((e) => e.id === selectedEducatorId) || EDUCATORS[0];
  const selectedSlot = TIME_SLOTS.find((s) => s.id === selectedSlotId) || TIME_SLOTS[0];

  const handleBooking = (e: React.FormEvent) => {
    e.preventDefault();
    setIsBooked(true);
  };

  const handleReset = () => {
    setIsBooked(false);
  };

  return (
    <div className="min-h-screen bg-[#FAFAF8] text-[#0A2540] flex flex-col font-sans">
      <AppHead
        title="প্রাতিষ্ঠানিক অভিভাবক-শিক্ষক কনফারেন্স (PTC) বুকিং | অগ্রযাত্রা"
        description="শিক্ষার্থী অগ্রগতি পর্যালোচনা, পরীক্ষার কৌশল এবং একাডেমিক সমন্বয়ের জন্য ভেরিফাইড শিক্ষকদের সাথে ওয়ান-টু-ওয়ান কনফারেন্স বুকিং।"
      />

      <Navbar />

      {/* Conference Portal Header */}
      <section className="bg-[#0A2540] text-white py-12 px-4 sm:px-6 lg:px-8 border-b-4 border-[#B45309]">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-300 mb-3">
            <Link href="/" className="hover:text-white transition-colors">হোম</Link>
            <ChevronRight className="w-3.5 h-3.5" />
            <Link href="/guardian" className="hover:text-white transition-colors">অভিভাবক ট্রাস্ট হাব</Link>
            <ChevronRight className="w-3.5 h-3.5" />
            <span className="text-amber-400">পিটিসি কনফারেন্স বুকিং</span>
          </div>

          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-white/10 text-amber-300 text-xs font-medium mb-3">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>ASVS L2 জিরো-IDOR প্রাইভেসি • ভেরিফাইড একাডেমিক শিক্ষক প্যানেল</span>
              </div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-white flex items-center gap-3">
                <Users className="w-8 h-8 text-amber-400 shrink-0" />
                <span>প্রাতিষ্ঠানিক অভিভাবক-শিক্ষক কনফারেন্স (PTC) বুকিং</span>
              </h1>
              <p className="mt-2 text-sm sm:text-base text-slate-200 max-w-3xl leading-relaxed">
                সন্তানের পড়াশোনার অগ্রগতি, পরীক্ষার প্রস্তুতি ও দুর্বল বিষয়ের কৌশলগত উত্তরণে প্রাতিষ্ঠানিক শিক্ষকদের সাথে সরাসরি ভার্চুয়াল বা ক্যাম্পাসে বৈঠকের সময়সূচী নির্ধারণ।
              </p>
            </div>

            <div className="flex items-center gap-3">
              <Link
                href="/tribunal/disputes"
                className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg border border-white/30 bg-white/5 hover:bg-white/10 text-white transition-colors"
              >
                <ShieldCheck className="w-4 h-4 text-amber-300" />
                <span>এসক্রো বিরোধ ট্রাইব্যুনাল</span>
              </Link>
              <button
                onClick={handleReset}
                className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
              >
                <RotateCcw className="w-4 h-4 text-slate-300" />
                <span>নতুন বুকিং</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Main Booking Interface */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* Left Column: Booking Form (7 Cols) */}
          <div className="lg:col-span-7 space-y-6">

            {!isBooked ? (
              <form onSubmit={handleBooking} className="space-y-6">

                {/* 1. Educator Selection */}
                <div className="bg-white rounded-xl border border-slate-300 p-6 shadow-sm">
                  <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-200">
                    <Building2 className="w-5 h-5 text-[#0A2540]" />
                    <h2 className="text-base font-bold text-[#0A2540]">১. সংশ্লিষ্ট প্রাতিষ্ঠানিক শিক্ষক নির্বাচন</h2>
                  </div>

                  <div className="space-y-3">
                    {EDUCATORS.map((t) => (
                      <label
                        key={t.id}
                        className={`flex items-start gap-3 p-3.5 rounded-lg border cursor-pointer transition-all ${
                          selectedEducatorId === t.id
                            ? 'border-[#0A2540] bg-slate-50 ring-1 ring-[#0A2540]'
                            : 'border-slate-200 hover:border-slate-300 bg-white'
                        }`}
                      >
                        <input
                          type="radio"
                          name="educator"
                          value={t.id}
                          checked={selectedEducatorId === t.id}
                          onChange={(e) => setSelectedEducatorId(e.target.value)}
                          className="mt-1 text-[#0A2540] focus:ring-[#0A2540]"
                        />
                        <div className="flex-1 space-y-0.5">
                          <div className="flex items-center justify-between">
                            <span className="text-sm font-bold text-[#0A2540]">{t.nameBn}</span>
                            <span className="text-xs font-semibold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                              স্কোর: {toBengaliDigits(t.rating)}/৫.০
                            </span>
                          </div>
                          <p className="text-xs text-slate-600">{t.institutionBn}</p>
                          <div className="flex items-center gap-3 pt-1 text-[11px] text-slate-500">
                            <span>বিষয়: <strong className="text-slate-700">{t.subjectBn}</strong></span>
                            <span>•</span>
                            <span>{t.experienceBn}</span>
                          </div>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                {/* 2. Conference Slot Picker */}
                <div className="bg-white rounded-xl border border-slate-300 p-6 shadow-sm">
                  <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-200">
                    <Clock className="w-5 h-5 text-[#0A2540]" />
                    <h2 className="text-base font-bold text-[#0A2540]">২. সময়সূচি ও স্লট নির্বাচন (২৫ অক্টোবর ২০২৬)</h2>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {TIME_SLOTS.map((slot) => (
                      <button
                        key={slot.id}
                        type="button"
                        disabled={!slot.isAvailable}
                        onClick={() => setSelectedSlotId(slot.id)}
                        className={`p-3 rounded-lg border text-left transition-all ${
                          !slot.isAvailable
                            ? 'border-slate-200 bg-slate-100 opacity-50 cursor-not-allowed'
                            : selectedSlotId === slot.id
                            ? 'border-[#0A2540] bg-slate-50 ring-1 ring-[#0A2540]'
                            : 'border-slate-200 hover:border-slate-300 bg-white'
                        }`}
                      >
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-xs font-bold text-slate-800">{slot.timeRangeBn}</span>
                          <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                            slot.isAvailable ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'
                          }`}>
                            {slot.isAvailable ? 'উপলব্ধ' : 'বুকড'}
                          </span>
                        </div>
                        <span className="text-[11px] text-slate-500">৩০ মিনিট একক বৈঠক</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* 3. Discussion Agenda */}
                <div className="bg-white rounded-xl border border-slate-300 p-6 shadow-sm">
                  <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-200">
                    <MessageSquare className="w-5 h-5 text-[#0A2540]" />
                    <h2 className="text-base font-bold text-[#0A2540]">৩. সভার মূল আলোচ্য বিষয় ও নোট</h2>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                        প্রধান এজেন্ডা নির্বাচন করুন
                      </label>
                      <select
                        value={selectedAgenda}
                        onChange={(e) => setSelectedAgenda(e.target.value)}
                        className="w-full text-sm rounded-lg border border-slate-300 px-3.5 py-2.5 bg-white text-[#0A2540] focus:ring-2 focus:ring-[#0A2540] font-medium"
                      >
                        <option value="ACADEMIC_PROGRESS">শ্রেণিকক্ষে পড়াশোনার অগ্রগতি ও ফলাফল পর্যালোচনা</option>
                        <option value="EXAM_PREPARATION">আসন্ন বোর্ড/ভর্তি পরীক্ষার চূড়ান্ত রিভিশন কৌশল</option>
                        <option value="DISCIPLINE_BEHAVIOR">হোমওয়ার্ক নিয়মিতকরণ ও মনোযোগ নিয়ন্ত্রণ</option>
                        <option value="MENTAL_WELLBEING">মানসিক চাপ ও প্রেষণা কাউন্সেলিং</option>
                        <option value="TUITION_ROADMAP">টিউটরিং কারিকুলাম ও এসক্রো রিলিজ পর্যালোচনা</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-xs font-semibold text-slate-700 uppercase mb-1.5">
                        শিক্ষককে পূর্বাবগত করার জন্য বিশেষ পর্যবেক্ষণ (ঐচ্ছিক)
                      </label>
                      <textarea
                        rows={3}
                        value={notes}
                        onChange={(e) => setNotes(e.target.value)}
                        className="w-full text-xs rounded-lg border border-slate-300 p-3 text-slate-800 focus:ring-2 focus:ring-[#0A2540]"
                        placeholder="সন্তানের দুর্বল বিষয় বা শিক্ষকের পরামর্শ চাওয়া নির্দিষ্ট বিষয় লিখুন..."
                      />
                    </div>
                  </div>
                </div>

                {/* 3D Tactile Push Button to Book Appointment */}
                <button
                  type="submit"
                  className="w-full py-3.5 px-4 bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] hover:bg-[#081C30] active:translate-y-1 active:shadow-none transition-all font-semibold rounded-lg flex items-center justify-center gap-2 text-sm"
                >
                  <Calendar className="w-4 h-4 text-amber-300" />
                  <span>কনফারেন্স অ্যাপয়েন্টমেন্ট নিশ্চিত করুন (Confirm PTC Booking)</span>
                </button>

              </form>
            ) : (
              /* Confirmed Appointment Docket Card */
              <div className="bg-emerald-50 border-2 border-emerald-600 rounded-xl p-6 shadow-sm space-y-4">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-6 h-6 text-emerald-700 shrink-0" />
                  <div>
                    <h3 className="text-base font-bold text-emerald-950">
                      অভিভাবক-শিক্ষক কনফারেন্স সফলভাবে বুকিং সম্পন্ন হয়েছে
                    </h3>
                    <span className="text-xs text-emerald-800">
                      অ্যাপয়েন্টমেন্ট ট্র্যাকিং আইডি: <strong>PTC-2026-9921</strong>
                    </span>
                  </div>
                </div>

                <div className="bg-white p-4 rounded-lg border border-emerald-300 text-xs space-y-2 text-slate-800">
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">শিক্ষক:</span>
                    <span className="font-bold text-[#0A2540]">{selectedEducator.nameBn}</span>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">তারিখ ও সময়:</span>
                    <span className="font-bold text-slate-900">২৫ অক্টোবর ২০২৬, {selectedSlot.timeRangeBn}</span>
                  </div>
                  <div className="flex justify-between border-b border-slate-100 pb-2">
                    <span className="text-slate-500">নিরাপদ কনফারেন্স পাসকোড:</span>
                    <span className="font-mono font-bold text-emerald-800 text-sm">৮৯২-৩৪১</span>
                  </div>
                  <div className="flex justify-between pt-1">
                    <span className="text-slate-500">আলোচ্য এজেন্ডা:</span>
                    <span className="font-semibold text-slate-900">শ্রেণিকক্ষে পড়াশোনার অগ্রগতি পর্যালোচনা</span>
                  </div>
                </div>

                <p className="text-xs text-emerald-900 leading-relaxed font-medium">
                  নির্ধারিত সময়ে প্ল্যাটফর্মের এনক্রিপ্টেড ভিডিও কনফারেন্স কক্ষে প্রবেশের জন্য শিক্ষক ও অভিভাবক উভয়কেই এসএমএস এবং ইমেইলে সিকিউর ওয়ান-টাইম লিংক পাঠানো হবে।
                </p>

                <div className="pt-2">
                  <button
                    onClick={handleReset}
                    className="w-full py-2.5 px-4 bg-emerald-800 hover:bg-emerald-900 text-white font-semibold rounded-lg text-xs transition-colors"
                  >
                    আরেকটি কনফারেন্স বুক করুন
                  </button>
                </div>
              </div>
            )}

          </div>

          {/* Right Column: Conference Guidelines & Privacy Tenancy (5 Cols) */}
          <div className="lg:col-span-5 space-y-6">

            {/* Selected Booking Summary Docket */}
            <div className="bg-white rounded-xl border border-slate-300 p-6 shadow-sm space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-slate-200">
                <FileText className="w-5 h-5 text-[#0A2540]" />
                <h3 className="text-sm font-bold uppercase tracking-wider text-[#0A2540]">
                  বুকিং ডকেট বিবরণী (Docket Summary)
                </h3>
              </div>

              <div className="space-y-3 text-xs">
                <div className="flex justify-between text-slate-600">
                  <span>নির্বাচিত শিক্ষক:</span>
                  <span className="font-bold text-slate-900">{selectedEducator.nameBn}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>বিষয় ক্ষেত্র:</span>
                  <span className="font-semibold text-slate-800">{selectedEducator.subjectBn}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>সেশন সময়সীমা:</span>
                  <span className="font-semibold text-slate-800">{selectedSlot.timeRangeBn}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>কনফারেন্স মোড:</span>
                  <span className="font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    এনক্রিপ্টেড অডিও/ভিডিও
                  </span>
                </div>
              </div>
            </div>

            {/* Zero-IDOR Tenancy Shield */}
            <div className="bg-slate-100 rounded-xl p-5 border border-slate-300 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
                <ShieldCheck className="w-4 h-4 text-emerald-700" />
                <span>ASVS L2 Zero-IDOR গোপনীয়তা নিশ্চয়তা</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                অভিভাবক ও সংশ্লিষ্ট শিক্ষক ছাড়া প্ল্যাটফর্মের কোনো তৃতীয় পক্ষ কনফারেন্স বুকিং তথ্য, পাসকোড বা আলোচনার সারাংশ দেখতে পারবে না। সম্পূর্ণ সেশন ডেটা সুপাবেস আরএলএস দিয়ে কঠোরভাবে সুরক্ষিত।
              </p>
            </div>

            {/* Institutional PTC Protocol */}
            <div className="bg-white rounded-xl border border-slate-300 p-6 shadow-sm space-y-3">
              <div className="flex items-center gap-2 pb-2 border-b border-slate-200">
                <Award className="w-5 h-5 text-[#0A2540]" />
                <h3 className="text-sm font-bold text-[#0A2540]">প্রাতিষ্ঠানিক কনফারেন্স আচরণবিধি</h3>
              </div>
              <ul className="space-y-2 text-xs text-slate-600 list-disc list-inside leading-relaxed">
                <li>সভার ১০ মিনিট পূর্বে প্রস্তুতি নোট পর্যালোচনা করুন।</li>
                <li>নির্ধারিত ৩০ মিনিটের মধ্যে আলোচনা সম্পন্ন করার নিয়ম বজায় রাখুন।</li>
                <li>কনফারেন্স শেষে উভয় পক্ষ যৌথভাবে সিদ্ধান্ত সারসংক্ষেপ অনুমোদন করবেন।</li>
              </ul>
            </div>

          </div>

        </div>
      </main>

      <Footer />
    </div>
  );
}
