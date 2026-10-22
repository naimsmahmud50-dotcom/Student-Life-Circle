/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Frontend Emergency Mesh & Radio Engineering Page
 * TOPIC:     Daylight-Readable LoRa Radio Studio & Solar Station Telemetry Host
 * FILE:      frontend/src/pages/emergency-mesh.tsx
 * PHASE:     Phase 106 - Rural LoRaWAN Emergency Bridge & Solar Micro-Hub
 * PURPOSE:   Provides full host page mounting LoRaRadioStudio and SolarStationTelemetry
 *            with responsive grid layout, status indicators, and offline DTN assurance.
 * STANDARDS: Delay-Tolerant Networking (DTN), CRC16 Frame Validation, Zero-Emoji, Field-Grade
 */

import React, { useState } from 'react';
import {
  Radio,
  Sun,
  ShieldCheck,
  Activity,
  Layers,
  ArrowRight,
  WifiOff,
  BatteryCharging,
  Cpu,
  RefreshCw,
  Info
} from 'lucide-react';
import { AppHead } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { LoRaRadioStudio } from '@/components/emergency-mesh/LoRaRadioStudio';
import { SolarStationTelemetry } from '@/components/emergency-mesh/SolarStationTelemetry';

export default function EmergencyMeshPage() {
  const [activeTab, setActiveTab] = useState<'studio' | 'telemetry' | 'both'>('both');
  const [lastPacketTime, setLastPacketTime] = useState<string | null>(null);

  const handlePacketTransmitted = (packet: any) => {
    setLastPacketTime(new Date().toLocaleTimeString('bn-BD'));
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-bengali selection:bg-teal-500/30 selection:text-teal-200">
      <AppHead
        title="পল্লী LoRaWAN জরুরি রেডিও ও সোলার মাইক্রো-হাব | অগ্রযাত্রা"
        description="চরম বন্যা ও প্রাকৃতিক দুর্যোগে ইন্টারনেট বিচ্ছিন্ন চর ও হাওর অঞ্চলের শিক্ষার্থীদের পরীক্ষা ও একাডেমিক সংযোগের জন্য সাব-গিগা হার্জ জরুরি রেডিও মেশ ও সোলার হাব।"
      />
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-8">
        {/* Field Instrument Top Hero Banner */}
        <section className="relative overflow-hidden rounded-2xl bg-white dark:bg-[#121B2D] border border-[#E5E2DA] dark:border-[#24314A] p-6 sm:p-8 shadow-xs">
          <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-3">
              <div className="inline-flex items-center gap-2.5 px-3 py-1.5 rounded-full bg-teal-950/80 border border-teal-500/40 text-teal-300 text-xs font-mono font-medium tracking-wide">
                <Radio className="w-3.5 h-3.5 text-teal-400 animate-pulse" />
                <span>OFF-GRID MESH PROTOCOL: LORAWAN + DTN (868/433 MHZ)</span>
              </div>
              <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight text-white font-sans">
                পল্লী LoRaWAN জরুরি রেডিও ও সোলার মাইক্রো-হাব
              </h1>
              <p className="text-slate-300 text-sm sm:text-base max-w-3xl leading-relaxed">
                ব্রহ্মপুত্র চর ও হাওর অঞ্চলের ইন্টারনেট-বিচ্ছিন্ন শিক্ষার্থীদের জন্য সাব-গিগা হার্জ রেডিও নেটওয়ার্ক।
                সোলার ব্যাটারি চালিত মাইক্রো-হাবের মাধ্যমে বিদ্যুৎ ও ফাইবার সংযোগ ছাড়াই উত্তরপত্র ও জরুরি নির্দেশনা পৌঁছাবে কেন্দ্রে।
              </p>
            </div>

            {/* Quick Operational Metrics */}
            <div className="flex flex-wrap md:flex-col gap-3 shrink-0">
              <div className="px-4 py-2.5 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex items-center gap-3">
                <WifiOff className="w-4 h-4 text-amber-400" />
                <div>
                  <div className="text-[11px] text-slate-400 font-sans uppercase">ইন্টারনেট অবস্থা</div>
                  <div className="text-xs font-semibold text-amber-300">অফ-গ্রিড (DTN বাফার সক্রিয়)</div>
                </div>
              </div>
              <div className="px-4 py-2.5 rounded-2xl bg-slate-800/80 border border-slate-700/80 flex items-center gap-3">
                <BatteryCharging className="w-4 h-4 text-emerald-400" />
                <div>
                  <div className="text-[11px] text-slate-400 font-sans uppercase">পাওয়ার ব্যাকআপ</div>
                  <div className="text-xs font-semibold text-emerald-300">১২.৮V LiFePO4 সোলার গ্রিড</div>
                </div>
              </div>
            </div>
          </div>

          {/* View Mode Switcher */}
          <div className="mt-8 pt-6 border-t border-slate-800 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-2 bg-slate-950/80 p-1.5 rounded-2xl border border-slate-800">
              <button
                type="button"
                onClick={() => setActiveTab('both')}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                  activeTab === 'both'
                    ? 'bg-teal-700 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                সম্মিলিত দৃশ্য (রেডিও + সোলার)
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('studio')}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                  activeTab === 'studio'
                    ? 'bg-teal-700 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                রেডিও কন্ট্রোল স্টুডিও
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('telemetry')}
                className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                  activeTab === 'telemetry'
                    ? 'bg-teal-700 text-white shadow-md'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                সোলার হাব টেলিমেট্রি
              </button>
            </div>

            {lastPacketTime && (
              <div className="text-xs text-teal-400 font-mono flex items-center gap-2">
                <Activity className="w-3.5 h-3.5" />
                <span>সর্বশেষ প্রেরিত প্যাকেট: {lastPacketTime}</span>
              </div>
            )}
          </div>
        </section>

        {/* Studio & Telemetry Display Grid */}
        <div className="space-y-8">
          {(activeTab === 'both' || activeTab === 'studio') && (
            <section className="space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-white flex items-center gap-2 font-sans">
                  <Radio className="w-4 h-4 text-teal-400" />
                  <span>সাব-গিগা হার্জ LoRa ট্রান্সসিভার কন্ট্রোল</span>
                </h2>
                <span className="text-xs text-slate-400 font-mono">CCITT CRC-16 PROTECTED</span>
              </div>
              <LoRaRadioStudio onPacketTransmitted={handlePacketTransmitted} />
            </section>
          )}

          {(activeTab === 'both' || activeTab === 'telemetry') && (
            <section className="space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-bold text-white flex items-center gap-2 font-sans">
                  <Sun className="w-4 h-4 text-amber-400" />
                  <span>সোলার মাইক্রো-হাব পাওয়ার ও মেশ নোড টেলিমেট্রি</span>
                </h2>
                <span className="text-xs text-slate-400 font-mono">12.8V LiFePO4 TELEMETRY</span>
              </div>
              <SolarStationTelemetry />
            </section>
          )}
        </div>

        {/* DTN & Mesh Protocol Specifications Footer Card */}
        <section className="p-6 rounded-3xl bg-slate-900/60 border border-slate-800 text-slate-300 space-y-4">
          <div className="flex items-center gap-2.5 text-teal-400 text-sm font-semibold">
            <Info className="w-4 h-4" />
            <span>ফিল্ড গাইড ও ডিলে-টলারেন্ট নেটওয়ার্কিং (DTN) নির্দেশিকা</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-400 leading-relaxed font-sans">
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">১. সর্বোচ্চ ২৫৬ বাইট বাইনারি ফ্রেম</div>
              <p>
                প্রতিটি উত্তরপত্র ও জরুরি অ্যালার্ট সংকুচিত বাইনারি ফ্রেমে এনকোড করা হয় যাতে LoRaWAN ফিজিক্যাল ফ্রেম সীমা ২৫৬ বাইট অতিক্রম না করে।
              </p>
            </div>
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">২. CRC16-CCITT ত্রুটি পরীক্ষণ</div>
              <p>
                বন্যা ও ঝড়ো বাতাসে নয়েজযুক্ত রেডিও চ্যানেলে কোনো বিট পরিবর্তন হলে ১৬-বিট চেকসামের মাধ্যমে অবৈধ প্যাকেট তাৎক্ষণিক বাতিল করা হয়।
              </p>
            </div>
            <div className="space-y-1.5 p-4 rounded-2xl bg-slate-950/60 border border-slate-800/80">
              <div className="font-semibold text-slate-200">৩. স্টোর-অ্যান্ড-ফরোয়ার্ড বাফারিং</div>
              <p>
                মূল সার্ভারের সাথে সংযোগ না থাকলেও শিক্ষার্থী ডিভাইস বা হাবের ফ্ল্যাশ মেমোরিতে উত্তরপত্র সংরক্ষিত থাকে এবং গেটওয়ে সচল হলে স্বয়ংক্রিয়ভাবে সিঙ্ক হয়।
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
