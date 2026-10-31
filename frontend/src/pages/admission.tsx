/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Next.js 15+ Centralized Admission Matrix & Blueprint Hub View
 * TOPIC:     Full-Page Bespoke Atmospheric Redesign & Design Symphony
 * FILE:      frontend/src/pages/admission.tsx
 * PURPOSE:   Provides a dignified, multi-tiered Oxford Navy, Pine Emerald & Amber atmospheric
 *            canvas matching the prestige of top-tier Bangladeshi Universities (BUET, DU, Medical, GST).
 * STANDARDS: UI/UX Pro Max, Academic Oxford Navy #0A2540, Pure Academic Palette, Zero-Emoji, WCAG 2.2 AAA
 */

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { AppHead, createCourseSchema } from '../components/layout/Head';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { 
  GraduationCap, 
  Search, 
  CheckCircle2, 
  Clock, 
  ArrowRight, 
  FileText, 
  AlertCircle, 
  Filter,
  Sparkles,
  Layers,
  BookOpen,
  TrendingUp,
  Percent,
  ShieldCheck,
  Target,
  Award,
  Compass,
  Building,
  Building2,
  Users,
  Calculator,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  ExternalLink,
  Sliders,
  Calendar,
  RotateCcw,
  X,
  ArrowUpRight,
  Flame
} from 'lucide-react';
import { apiClient } from '../lib/api-client';
import { useFilterStore } from '../store/useFilterStore';
import { useQuizStore } from '../store/useQuizStore';
import { AdmissionCounselingMatrix } from '../components/admission/AdmissionCounselingMatrix';
import { MigrationCascadeVisualizer } from '../components/admission/MigrationCascadeVisualizer';

interface AdmissionTarget {
  id: string;
  nameBn: string;
  category: 'ENGINEERING' | 'GENERAL_VARSITY' | 'MEDICAL' | 'GST_CLUSTER';
  units: string;
  circularStatus: 'VERIFIED' | 'PENDING_UPDATE';
  lastCheckedDate: string;
  totalMocksAvailable: number;
  negativeMarking: string;
  cutOffScore: string;
  probabilityPercent: number;
  seatCount: string;
  examDate: string;
}

const FALLBACK_TARGETS: AdmissionTarget[] = [
  {
    id: "target_du",
    nameBn: "ঢাকা বিশ্ববিদ্যালয় (DU)",
    category: "GENERAL_VARSITY",
    units: "ক-ইউনিট (বিজ্ঞান অনুষদ), খ-ইউনিট (কলা ও সামাজিক বিজ্ঞান), গ-ইউনিট (ব্যবসায়)",
    circularStatus: "VERIFIED",
    lastCheckedDate: "১০ অক্টোবর ২০২৬",
    totalMocksAvailable: 25,
    negativeMarking: "-০.২৫ প্রতি ভুল উত্তরে",
    cutOffScore: "৭২.৫০ / ১২০",
    probabilityPercent: 84,
    seatCount: "১,৮৫১টি আসন (ক-ইউনিট)",
    examDate: "০৫ ডিসেম্বর ২০২৬"
  },
  {
    id: "target_buet",
    nameBn: "বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (BUET)",
    category: "ENGINEERING",
    units: "ইঞ্জিনিয়ারিং ও স্থাপত্য বিভাগ (প্রিলিমিনারি ও লিখিত)",
    circularStatus: "VERIFIED",
    lastCheckedDate: "০৮ অক্টোবর ২০২৬",
    totalMocksAvailable: 18,
    negativeMarking: "-০.২৫ (প্রিলিমিনারি টেস্ট)",
    cutOffScore: "৭৮.০০ / ১০০",
    probabilityPercent: 76,
    seatCount: "১,৩০৫টি আসন",
    examDate: "১২ ডিসেম্বর ২০২৬"
  },
  {
    id: "target_medical",
    nameBn: "জাতীয় মেডিকেল ভর্তি পরীক্ষা (MBBS/BDS)",
    category: "MEDICAL",
    units: "৩৭টি সরকারি ও বেসরকারি মেডিকেল কলেজ",
    circularStatus: "VERIFIED",
    lastCheckedDate: "১২ অক্টোবর ২০২৬",
    totalMocksAvailable: 30,
    negativeMarking: "-০.২৫ প্রতি ভুল উত্তরে",
    cutOffScore: "৬৮.৫০ / ১০০",
    probabilityPercent: 71,
    seatCount: "৫,৩৮০টি সরকারি আসন",
    examDate: "১৯ ডিসেম্বর ২০২৬"
  },
  {
    id: "target_gst",
    nameBn: "জিএসটি গুচ্ছভুক্ত বিশ্ববিদ্যালয়সমূহ (GST Cluster)",
    category: "GST_CLUSTER",
    units: "২৪টি সমন্বিত সাধারণ ও বিজ্ঞান ও প্রযুক্তি বিশ্ববিদ্যালয় (A, B, C ইউনিট)",
    circularStatus: "VERIFIED",
    lastCheckedDate: "০৬ অক্টোবর ২০২৬",
    totalMocksAvailable: 20,
    negativeMarking: "-০.২৫ প্রতি ভুল উত্তরে",
    cutOffScore: "৫৬.০০ / ১০০",
    probabilityPercent: 88,
    seatCount: "২২,৫০০+ আসন",
    examDate: "২৬ ডিসেম্বর ২০২৬"
  }
];

const ADMISSION_FAQS = [
  {
    question: "সেকেন্ড টাইম ভর্তি পরীক্ষার নিয়ম ও মার্কস কর্তন নীতি কী?",
    answer: "মেডিকেল ভর্তি পরীক্ষায় দ্বিতীয়বার অংশগ্রহণকারীদের মোট প্রাপ্ত নম্বর থেকে ৫ নম্বর (এবং পূর্ববর্তী শিক্ষাবর্ষে সরকারি মেডিকেল/ডেন্টালে ভর্তিকৃতদের ক্ষেত্রে ৭.৫ নম্বর) কর্তন করা হয়। ঢাকা বিশ্ববিদ্যালয় ও বুয়েটে সেকেন্ড টাইম সুযোগ নেই। তবে জিএসটি গুচ্ছ, জাহাঙ্গীরনগর বিশ্ববিদ্যালয় (JU) ও রাজশাহী বিশ্ববিদ্যালয়ে (RU) সেকেন্ড টাইম সুযোগ বিদ্যমান।"
  },
  {
    question: "বুয়েট ও অন্যান্য প্রকৌশল ভর্তি পরীক্ষায় কোন কোন ক্যালকুলেটর অনুমোদিত?",
    answer: "বুয়েট ভর্তি পরীক্ষায় শুধুমাত্র নন-প্রোগ্রামেবল সায়েন্টিফিক ক্যালকুলেটর অনুমোদিত (যেমন: Casio fx-991ES Plus, fx-991EX ClassWiz, fx-100MS ইত্যাদি)। মেমরি স্টোরেজ বা টেক্সট সেভ করা যায় এমন কোনো প্রোগ্রামেবল ক্যালকুলেটর পরীক্ষার হলে সম্পূর্ণ নিষিদ্ধ।"
  },
  {
    question: "নেগেটিভ মার্কিং পলিসি কীভাবে চূড়ান্ত স্কোর প্রভাবিত করে?",
    answer: "প্রতিটি ভুল উত্তরের জন্য ০.২৫ নম্বর কাটা যায়। চারটি ভুল উত্তরের পেনাল্টিতে ১টি সঠিক উত্তরের সমান মার্ক কর্তন হয়। তাই আন্দাজে উত্তর না দিয়ে অপশন এলিমিনেশন মেথডে নিশ্চিত হওয়া ছাড়া উত্তর দাগানো পরিহার করাই কাট-অফ সুরক্ষিত রাখার মূল চাবিকাঠি।"
  },
  {
    question: "কোটা সংক্রান্ত আবেদন ও প্রয়োজনীয় প্রত্যয়নপত্র কী কী?",
    answer: "মুক্তিযোদ্ধা, উপজাতি/ক্ষুদ্র নৃগোষ্ঠী, শারীরিক প্রতিবন্ধী ও পোষ্য কোটায় আবেদনকারীদের সংশ্লিষ্ট মন্ত্রণালয়ের উপযুক্ত কর্তৃপক্ষ কর্তৃক ইস্যুকৃত মূল সনদপত্র ও অনলাইন ভেরিফিকেশন ট্র্যাকিং নম্বর আবেদনের সময় নির্ভুলভাবে প্রদান করতে হবে।"
  }
];

export default function AdmissionPage() {
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [targets, setTargets] = useState<AdmissionTarget[]>(FALLBACK_TARGETS);
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'targets' | 'counseling' | 'migration' | 'strategy' | 'faqs'>('targets');
  const [openFaqIndex, setOpenFaqIndex] = useState<number | null>(0);

  const { startAttempt } = useQuizStore();
  const { curriculumLevel } = useFilterStore();

  useEffect(() => {
    let isMounted = true;
    async function loadAdmissionData() {
      setIsLoading(true);
      try {
        const response = (await apiClient.getAdmissionTests?.(
          selectedCategory !== 'ALL' ? selectedCategory : undefined
        )) || (await apiClient.getAdmissionPrograms(
          selectedCategory !== 'ALL' ? selectedCategory : undefined
        ));
        if (isMounted && response?.data?.length > 0) {
          setTargets(response.data);
        }
      } catch {
        // Fallback
      } finally {
        if (isMounted) setIsLoading(false);
      }
    }

    loadAdmissionData();

    return () => {
      isMounted = false;
    };
  }, [selectedCategory]);

  const filtered = targets.filter((t) => {
    const matchesCategory = selectedCategory === 'ALL' || t.category === selectedCategory;
    const matchesQuery = !searchQuery || t.nameBn.toLowerCase().includes(searchQuery.toLowerCase()) || t.units.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesQuery;
  });

  const getTargetMonogram = (id: string) => {
    switch (id) {
      case 'target_du':
        return {
          monogram: 'DU',
          bgClass: 'bg-[#0A2540] text-amber-300 border-amber-300/40',
          accentColor: '#0A2540'
        };
      case 'target_buet':
        return {
          monogram: 'BUET',
          bgClass: 'bg-[#991B1B] text-amber-200 border-amber-300/40',
          accentColor: '#991B1B'
        };
      case 'target_medical':
        return {
          monogram: 'DMC',
          bgClass: 'bg-[#065F46] text-emerald-200 border-emerald-300/40',
          accentColor: '#065F46'
        };
      case 'target_gst':
        return {
          monogram: 'GST',
          bgClass: 'bg-[#581C87] text-purple-200 border-purple-300/40',
          accentColor: '#581C87'
        };
      default:
        return {
          monogram: 'UNI',
          bgClass: 'bg-[#0A2540] text-white border-white/20',
          accentColor: '#0A2540'
        };
    }
  };

  const toggleFaq = (idx: number) => {
    setOpenFaqIndex(openFaqIndex === idx ? null : idx);
  };

  return (
    <>
      <AppHead
        title="বিশ্ববিদ্যালয় ভর্তি প্রস্তুতি হাব (Admission Matrix) | অগ্রযাত্রা"
        description="ঢাকা বিশ্ববিদ্যালয়, বুয়েট, মেডিকেল ও জিএসটি গুচ্ছ ভর্তি পরীক্ষার অফিশিয়াল সার্কুলার, বিষয়ভিত্তিক নেগেティブ মার্কিং মডেল টেস্ট ও কাট-মার্ক অ্যানালিটিক্স।"
        canonicalUrl="/admission"
        ogType="course"
        structuredData={createCourseSchema({
          name: "বিশ্ববিদ্যালয় ভর্তি প্রস্তুতি ও গেইল-শ্যাপলি ম্যাচিং",
          description: "বুয়েট, ঢাবি, মেডিকেল ও জিএসটি পরীক্ষার নেগেティブ মার্কিং প্রস্তুতি প্ল্যাটফর্ম",
          educationalLevel: "University Admission",
          url: "https://ogrojatra.edu.bd/admission"
        })}
      />

      <div className="min-h-screen bg-[#FFFCF6] dark:bg-[#0B0F19] text-[#213130] dark:text-[#F5F2EB] transition-colors duration-200 flex flex-col justify-between font-sans selection:bg-[#ED8E22] selection:text-white">
        
        {/* Global Standard Navigation Bar */}
        <Navbar currentStage="বিশ্ববিদ্যালয় ভর্তি প্রস্তুতি হাব" />

        {/* Admission Bespoke Atmospheric Hero with ADMISSION Watermark */}
        <section className="relative overflow-hidden pt-8 pb-10 sm:pt-12 sm:pb-14 border-b border-amber-200/60 dark:border-[#262D3D] bg-[#FFF6DD]/80 dark:bg-[#0B0F19] transition-colors">
          {/* GoEdu University Prestige Sunburst Glow */}
          <div
            className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
            style={{
              height: '100%',
              minHeight: '260px',
              background:
                'radial-gradient(ellipse 65% 90% at 50% 100%, rgba(255, 178, 0, 0.45) 0%, rgba(153, 27, 27, 0.12) 50%, rgba(253, 215, 70, 0) 100%)'
            }}
            aria-hidden="true"
          />

          {/* Giant Typographic Watermark */}
          <div
            className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
            aria-hidden="true"
          >
            <p
              className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,20vw,15rem)] uppercase tracking-wider select-none opacity-85"
              style={{
                lineHeight: 0.95,
                backgroundImage:
                  'linear-gradient(to bottom, rgba(243, 172, 8, 0.28) 15%, rgba(253, 215, 70, 0.02) 100%)'
              }}
            >
              ADMISSION
            </p>
          </div>

          <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 relative z-10 space-y-6">
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-white dark:bg-[#121B2D] text-[#ED8E22] border border-amber-200/70 dark:border-slate-700 shadow-xs">
                <Target className="w-3.5 h-3.5 mr-1 text-[#ED8E22]" />
                পরীক্ষা-নির্দিষ্ট প্রস্তুতি মোড
              </span>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
                <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-600" />
                অফিশিয়াল সার্কুলার ও ব্লুপ্রিন্ট সমন্বিত
              </span>
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-white dark:bg-[#121B2D] text-slate-700 dark:text-slate-300 border border-amber-200/60 dark:border-slate-700">
                <Award className="w-3.5 h-3.5 mr-1 text-[#ED8E22]" />
                জাতীয় মেধাভিত্তিক ম্যাচিং
              </span>
            </div>

            <div className="space-y-2 max-w-4xl">
              <h1 className="text-2xl sm:text-4xl font-serif font-bold tracking-tight text-[#1B2A4A] dark:text-[#F5F2EB]">
                বিশ্ববিদ্যালয় ভর্তি প্রস্তুতি হাব
              </h1>
              <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed font-bengali">
                ঢাকা বিশ্ববিদ্যালয় (DU Ka), বুয়েট (BUET), মেডিকেল (MBBS/BDS) এবং জিএসটি গুচ্ছ ভর্তি পরীক্ষার অফিশিয়াল সিলেবাস,
                নেগেটিভ মার্কিং (-০.২৫) অ্যালগরিদম এবং বিগত বছরের কাট-অফ নম্বর অনুযায়ী প্রস্তুতি ও রিয়েল-টাইম চান্স প্রবাবিলিটি যাচাই করুন।
              </p>
            </div>

            {/* Cut-off Forecaster CTA Banner */}
            <div className="bg-white/95 dark:bg-[#121B2D] text-slate-900 dark:text-white rounded-3xl p-5 sm:p-6 border border-amber-200/80 dark:border-[#262D3D] shadow-xs flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 backdrop-blur-xs">
              <div className="space-y-1.5">
                <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-bold bg-[#FFF9EB] dark:bg-amber-950/60 text-[#ED8E22] border border-amber-200/80 dark:border-amber-800">
                  <Sparkles className="w-3.5 h-3.5 text-[#ED8E22]" />
                  <span>কাট-অফ ফোরকাস্টার ও সিগময়েড র‍্যাংক প্রেডিক্টর</span>
                </div>
                <h3 className="text-base sm:text-lg font-bold text-[#1B2A4A] dark:text-white font-bengali">
                  স্বায়ত্তশাসিত চান্স মিটার ও বিশ্ববিদ্যালয় ম্যাচিং
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali max-w-2xl">
                  আপনার এসএসসি/এইচএসসি জিপিএ ও টেস্ট স্কোর ইনপুট দিয়ে বুয়েট, ঢাবি, মেডিকেল ও গুচ্ছের ক্যালিব্রেটেড চান্স মিটার যাচাই করুন।
                </p>
              </div>
              <Link
                href="/admission/predictor"
                className="shrink-0 px-5 py-2.5 bg-[#ED8E22] hover:bg-[#D97D1A] text-white font-bold text-xs sm:text-sm rounded-2xl shadow-[0_4px_0_0_#C57013] active:translate-y-1 active:shadow-none transition-all flex items-center gap-2 cursor-pointer"
              >
                <span>ফোরকাস্টার ওপেন করুন</span>
                <ArrowRight className="w-4 h-4 text-white" />
              </Link>
            </div>

            {/* 4 Realtime Platform Metric Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-2">
              <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex items-center gap-3.5 shadow-xs">
                <div className="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-950/50 text-[#0A2540] dark:text-blue-300 flex items-center justify-center font-bold shrink-0">
                  <Building2 className="w-5 h-5 text-[#0A2540] dark:text-blue-300" />
                </div>
                <div>
                  <div className="text-xl sm:text-2xl font-black font-bengali text-slate-900 dark:text-white">
                    ৪টি ক্লাস্টার
                  </div>
                  <div className="text-xs text-slate-500 font-bengali">পাবলিক, ইঞ্জি., মেডিকেল ও গুচ্ছ</div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex items-center gap-3.5 shadow-xs">
                <div className="w-10 h-10 rounded-xl bg-emerald-100 dark:bg-emerald-950/50 text-emerald-800 dark:text-emerald-300 flex items-center justify-center font-bold shrink-0">
                  <Users className="w-5 h-5 text-emerald-700 dark:text-emerald-300" />
                </div>
                <div>
                  <div className="text-xl sm:text-2xl font-black font-bengali text-slate-900 dark:text-white">
                    ৩১,০৩৬+
                  </div>
                  <div className="text-xs text-slate-500 font-bengali">মোট সমন্বিত সরকারি আসন</div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex items-center gap-3.5 shadow-xs">
                <div className="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-950/50 text-amber-800 dark:text-amber-300 flex items-center justify-center font-bold shrink-0">
                  <BookOpen className="w-5 h-5 text-amber-700 dark:text-amber-300" />
                </div>
                <div>
                  <div className="text-xl sm:text-2xl font-black font-bengali text-slate-900 dark:text-white">
                    ৯৩টি
                  </div>
                  <div className="text-xs text-slate-500 font-bengali">পূর্ণাঙ্গ ও বিষয়ভিত্তিক মডেল টেস্ট</div>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 flex items-center gap-3.5 shadow-xs">
                <div className="w-10 h-10 rounded-xl bg-rose-100 dark:bg-rose-950/50 text-rose-800 dark:text-rose-300 flex items-center justify-center font-bold shrink-0">
                  <Percent className="w-5 h-5 text-rose-700 dark:text-rose-300" />
                </div>
                <div>
                  <div className="text-xl sm:text-2xl font-black font-bengali text-slate-900 dark:text-white">
                    -০.২৫
                  </div>
                  <div className="text-xs text-slate-500 font-bengali">নেগেটিভ মার্কিং পলিসি ক্যালিব্রেশন</div>
                </div>
              </div>
            </div>

            {/* Master Tab Navigation Switcher */}
            <div className="flex items-center gap-2 overflow-x-auto pb-1 border-t border-amber-200/60 dark:border-slate-800 pt-4">
              <button
                onClick={() => setActiveTab('targets')}
                className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition flex items-center gap-1.5 whitespace-nowrap cursor-pointer ${
                  activeTab === 'targets'
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 border border-amber-200/60 dark:border-slate-700'
                }`}
              >
                <Target className="w-3.5 h-3.5" />
                <span>বিশ্ববিদ্যালয় ব্লুপ্রিন্ট ও মডেল টেস্ট (Targets)</span>
              </button>

              <button
                onClick={() => setActiveTab('counseling')}
                className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition flex items-center gap-1.5 whitespace-nowrap cursor-pointer ${
                  activeTab === 'counseling'
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 border border-amber-200/60 dark:border-slate-700'
                }`}
              >
                <Compass className="w-3.5 h-3.5" />
                <span>চয়েস লিস্ট ও কাউন্সেলিং রুম (Counseling)</span>
              </button>

              <button
                onClick={() => setActiveTab('migration')}
                className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition flex items-center gap-1.5 whitespace-nowrap cursor-pointer ${
                  activeTab === 'migration'
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 border border-amber-200/60 dark:border-slate-700'
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                <span>আসন মাইগ্রেশন ক্যাসকেড (Migration Ripple)</span>
              </button>

              <button
                onClick={() => setActiveTab('strategy')}
                className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition flex items-center gap-1.5 whitespace-nowrap cursor-pointer ${
                  activeTab === 'strategy'
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 border border-amber-200/60 dark:border-slate-700'
                }`}
              >
                <BookOpen className="w-3.5 h-3.5" />
                <span>নেগেটিভ মার্কিং স্ট্র্যাটেজি ও গাইড</span>
              </button>

              <button
                onClick={() => setActiveTab('faqs')}
                className={`px-4 py-2 rounded-xl text-xs font-bold font-bengali transition flex items-center gap-1.5 whitespace-nowrap cursor-pointer ${
                  activeTab === 'faqs'
                    ? 'bg-[#0A2540] text-white shadow-xs'
                    : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 border border-amber-200/60 dark:border-slate-700'
                }`}
              >
                <HelpCircle className="w-3.5 h-3.5" />
                <span>ভর্তি নীতিমালা ও এফএকিউ (Policies)</span>
              </button>
            </div>

          </div>
        </section>

        <main className="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 space-y-8 flex-1">

          {/* TAB 1: University Blueprints & Model Test Targets */}
          {activeTab === 'targets' && (
            <div className="space-y-6">
              
              {/* Elevated University Search & Multi-Vector Filter Console */}
              <div className="relative overflow-hidden rounded-3xl border border-amber-200/60 dark:border-[#262D3D] bg-white/95 dark:bg-[#0B0F19]/95 backdrop-blur-md p-5 sm:p-7 shadow-xs space-y-4">
                
                {/* Subtle Warm Halo */}
                <div
                  className="absolute top-0 right-0 w-96 h-96 pointer-events-none select-none z-0"
                  style={{
                    background: 'radial-gradient(circle at 100% 0%, rgba(237, 142, 34, 0.12) 0%, rgba(253, 215, 70, 0.03) 55%, transparent 100%)'
                  }}
                  aria-hidden="true"
                />

                <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
                  {/* Category Filter Pills */}
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-xs font-semibold text-slate-600 dark:text-slate-300 font-bengali mr-1 flex items-center gap-1">
                      <Filter className="w-3.5 h-3.5 text-[#ED8E22]" />
                      <span>ক্লাস্টার:</span>
                    </span>

                    {[
                      { key: 'ALL', label: 'সকল বিশ্ববিদ্যালয়', count: targets.length },
                      { key: 'GENERAL_VARSITY', label: 'সাধারণ পাবলিক (DU, JU, RU)', count: targets.filter(t => t.category === 'GENERAL_VARSITY').length },
                      { key: 'ENGINEERING', label: 'ইঞ্জিনিয়ারিং (BUET, CKRUET)', count: targets.filter(t => t.category === 'ENGINEERING').length },
                      { key: 'MEDICAL', label: 'মেডিকেল (MBBS / BDS)', count: targets.filter(t => t.category === 'MEDICAL').length },
                      { key: 'GST_CLUSTER', label: 'গুচ্ছ ক্লাস্টার (GST)', count: targets.filter(t => t.category === 'GST_CLUSTER').length },
                    ].map((cat) => (
                      <button
                        key={cat.key}
                        onClick={() => setSelectedCategory(cat.key)}
                        className={`
                          px-3.5 py-1.5 rounded-xl text-xs font-bengali font-bold transition-all cursor-pointer flex items-center gap-1.5
                          ${selectedCategory === cat.key
                            ? "bg-[#0A2540] dark:bg-amber-400 text-white dark:text-slate-950 shadow-xs ring-1 ring-[#0A2540]/30"
                            : "bg-white dark:bg-[#121B2D] text-slate-700 dark:text-slate-300 border border-amber-200/60 dark:border-slate-700/60 hover:bg-amber-50/50 dark:hover:bg-slate-800"
                          }
                        `}
                      >
                        <span>{cat.label}</span>
                        <span className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full ${selectedCategory === cat.key ? "bg-white/20 text-white dark:text-slate-950" : "bg-slate-100 dark:bg-slate-800 text-slate-500"}`}>
                          {cat.count}
                        </span>
                      </button>
                    ))}
                  </div>

                  {/* Keyword Search Input */}
                  <div className="relative min-w-[280px]">
                    <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-[#ED8E22]" />
                    <input
                      type="text"
                      placeholder="বিশ্ববিদ্যালয় বা ইউনিট খুঁজুন (যেমন: BUET, ক-ইউনিট)..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full pl-10 pr-9 py-2.5 text-xs sm:text-sm rounded-2xl bg-white dark:bg-[#121B2D] border border-amber-200/70 dark:border-slate-700/80 text-slate-900 dark:text-white placeholder:text-slate-400 font-bengali focus:outline-none focus:ring-2 focus:ring-[#ED8E22]/30 focus:border-[#ED8E22] shadow-xs transition"
                    />
                    {searchQuery && (
                      <button
                        onClick={() => setSearchQuery('')}
                        className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1 cursor-pointer"
                        aria-label="ক্লিয়ার সার্চ"
                      >
                        <X className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>
                </div>

              </div>

              {/* Elevated University Blueprints Grid Container */}
              <div className="relative overflow-hidden rounded-3xl border border-slate-200/80 dark:border-[#262D3D] bg-[#FAFBFD]/90 dark:bg-[#0A1220]/90 p-6 sm:p-8 shadow-xs space-y-6">
                
                {/* Oxford Navy Atmospheric Halo Stop */}
                <div
                  className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
                  style={{
                    height: '100%',
                    minHeight: '260px',
                    background:
                      'radial-gradient(ellipse 65% 90% at 30% 100%, rgba(10, 37, 64, 0.12) 0%, rgba(10, 37, 64, 0.03) 45%, transparent 100%)'
                  }}
                  aria-hidden="true"
                />

                {/* Ambient Typographic Watermark */}
                <div
                  className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
                  aria-hidden="true"
                >
                  <p
                    className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,18vw,12rem)] uppercase tracking-wider select-none opacity-85"
                    style={{
                      lineHeight: 0.95,
                      backgroundImage:
                        'linear-gradient(to bottom, rgba(10, 37, 64, 0.16) 15%, rgba(10, 37, 64, 0.01) 100%)'
                    }}
                  >
                    BLUEPRINT
                  </p>
                </div>

                {/* Feed Header */}
                <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200/60 dark:border-slate-800 pb-4">
                  <div className="flex items-center gap-2.5">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-white dark:bg-[#121B2D] text-[#0A2540] dark:text-blue-300 border border-slate-200 dark:border-slate-800 shadow-xs font-bengali">
                      <Target className="w-3.5 h-3.5 mr-1.5 text-[#ED8E22]" />
                      ভর্তি পরীক্ষা ব্লুপ্রিন্ট
                    </span>
                    <span className="text-xs sm:text-sm font-bold text-slate-700 dark:text-slate-300 font-bengali">
                      মোট <strong className="text-slate-900 dark:text-white font-mono">{filtered.length}</strong> টি বিশ্ববিদ্যালয় টার্গেট সক্রিয় রয়েছে
                    </span>
                  </div>

                  <span className="text-xs text-slate-500 font-bengali flex items-center gap-1.5">
                    <ShieldCheck className="w-4 h-4 text-emerald-600" />
                    <span>২০২৬ শিক্ষাবর্ষের অফিশিয়াল সিলেবাস ও কাট-অফ সমন্বিত</span>
                  </span>
                </div>

                {/* Cards Grid */}
                <div className="relative z-10">
                  {isLoading ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-pulse">
                      {[1, 2, 3, 4].map((i) => (
                        <div key={i} className="p-6 rounded-3xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 space-y-4">
                          <div className="flex justify-between items-center">
                            <div className="h-5 w-24 bg-slate-200 dark:bg-slate-800 rounded-md" />
                            <div className="h-5 w-32 bg-slate-200 dark:bg-slate-800 rounded-md" />
                          </div>
                          <div className="h-6 w-3/4 bg-slate-200 dark:bg-slate-800 rounded-md" />
                          <div className="h-4 w-1/2 bg-slate-200 dark:bg-slate-800 rounded-md" />
                          <div className="h-24 w-full bg-slate-100 dark:bg-slate-800 rounded-xl" />
                        </div>
                      ))}
                    </div>
                  ) : filtered.length === 0 ? (
                    <div className="rounded-3xl border-2 border-dashed border-slate-300 dark:border-slate-800 p-8 sm:p-12 text-center space-y-4 bg-white/80 dark:bg-slate-900/80 backdrop-blur-xs">
                      <div className="w-14 h-14 rounded-2xl bg-amber-50 dark:bg-amber-950/40 text-amber-600 flex items-center justify-center mx-auto border border-amber-200/60">
                        <AlertCircle className="w-7 h-7" />
                      </div>
                      <div className="space-y-1">
                        <h3 className="text-base font-bold text-slate-900 dark:text-white font-bengali">
                          কোনো বিশ্ববিদ্যালয় লক্ষ্য পাওয়া যায়নি
                        </h3>
                        <p className="text-xs text-slate-500 font-bengali max-w-sm mx-auto leading-relaxed">
                          আপনার দেওয়া ফিল্টার বা সার্চ শব্দের সাথে মিল পাওয়া যায়নি। ফিল্টার পরিবর্তন করে পুনরায় চেষ্টা করুন।
                        </p>
                      </div>
                      <button
                        onClick={() => {
                          setSelectedCategory('ALL');
                          setSearchQuery('');
                        }}
                        className="px-5 py-2.5 rounded-2xl bg-[#0A2540] hover:bg-[#081c30] text-white text-xs font-bold font-bengali shadow-[0_4px_0_0_#071D33] active:translate-y-1 active:shadow-none transition flex items-center gap-1.5 mx-auto cursor-pointer"
                      >
                        <RotateCcw className="w-3.5 h-3.5 text-amber-300" />
                        <span>ফিল্টার রিসেট করুন</span>
                      </button>
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {filtered.map((target) => {
                        const monogramInfo = getTargetMonogram(target.id);

                        return (
                          <div
                            key={target.id}
                            className="p-6 sm:p-7 rounded-3xl border border-slate-200/90 dark:border-[#232F45] bg-white/95 dark:bg-[#101A2C]/95 space-y-5 shadow-xs hover:border-amber-300 dark:hover:border-amber-500/50 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200 flex flex-col justify-between group"
                          >
                            <div className="space-y-4">
                              {/* Top Row: Category Tag & Circular Verification Badge */}
                              <div className="flex items-center justify-between">
                                <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700 shadow-xs">
                                  {target.category}
                                </span>
                                {target.circularStatus === 'VERIFIED' ? (
                                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold font-bengali bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 shadow-xs">
                                    <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-600" />
                                    অফিশিয়াল সার্কুলার ভেরিফায়েড
                                  </span>
                                ) : (
                                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold font-bengali bg-amber-50 dark:bg-amber-950/40 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-800 shadow-xs">
                                    <AlertCircle className="w-3.5 h-3.5 mr-1 text-amber-600" />
                                    খসড়া তথ্য (যাচাইাধীন)
                                  </span>
                                )}
                              </div>

                              {/* Target Identity Row: Monogram & Name */}
                              <div className="flex items-start gap-4">
                                <div className={`w-13 h-13 sm:w-14 sm:h-14 rounded-2xl ${monogramInfo.bgClass} flex items-center justify-center text-sm sm:text-base font-black shrink-0 shadow-xs border group-hover:scale-105 transition-transform`}>
                                  {monogramInfo.monogram}
                                </div>
                                <div className="space-y-1">
                                  <h2 className="text-lg sm:text-xl font-bold font-bengali text-[#0A2540] dark:text-white group-hover:text-[#ED8E22] dark:group-hover:text-amber-300 transition-colors">
                                    {target.nameBn}
                                  </h2>
                                  <p className="text-xs text-slate-500 font-medium font-bengali leading-relaxed">
                                    ইউনিটসমূহ: {target.units}
                                  </p>
                                </div>
                              </div>

                              {/* Negative Marking Badge in Burgundy Crimson (#991B1B) & Stats Container */}
                              <div className="p-4 sm:p-5 rounded-2xl bg-[#FAFAF8] dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 text-xs space-y-3.5 shadow-xs">
                                <div className="flex items-center justify-between pb-2.5 border-b border-slate-200 dark:border-slate-800">
                                  <span className="text-slate-600 dark:text-slate-400 font-bengali font-medium">নেগেটিভ মার্কিং পলিসি:</span>
                                  <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold font-mono bg-[#991B1B]/10 text-[#991B1B] border border-[#991B1B]/30 dark:bg-[#991B1B]/20 dark:text-rose-300 dark:border-[#991B1B]/40 shadow-xs">
                                    {target.negativeMarking}
                                  </span>
                                </div>

                                <div className="grid grid-cols-2 gap-3 text-xs">
                                  <div className="p-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-xs">
                                    <span className="text-slate-500 font-bengali block">উপলব্ধ মডেল টেস্ট:</span>
                                    <span className="font-mono font-bold text-slate-900 dark:text-white text-base tabular-nums">
                                      {target.totalMocksAvailable} টি
                                    </span>
                                  </div>
                                  <div className="p-2.5 rounded-xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-xs">
                                    <span className="text-slate-500 font-bengali block">বিগত বছরের কাট-অফ:</span>
                                    <span className="font-mono font-bold text-[#0A2540] dark:text-amber-300 text-base tabular-nums">
                                      {target.cutOffScore}
                                    </span>
                                  </div>
                                </div>

                                {/* Past-Year Cut-off Probability Meter */}
                                <div className="pt-2 border-t border-slate-200 dark:border-slate-800 space-y-1.5">
                                  <div className="flex justify-between items-center text-xs">
                                    <span className="text-slate-700 dark:text-slate-300 flex items-center gap-1 font-bengali font-semibold">
                                      <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />
                                      কাট-অফ অতিক্রমের সম্ভাব্য হার:
                                    </span>
                                    <span className="font-mono font-black text-emerald-700 dark:text-emerald-400 tabular-nums">
                                      {target.probabilityPercent}%
                                    </span>
                                  </div>
                                  <div className="w-full bg-slate-200 dark:bg-slate-800 rounded-full h-2.5 overflow-hidden">
                                    <div 
                                      className="bg-emerald-600 dark:bg-emerald-400 h-2.5 rounded-full transition-all duration-500" 
                                      style={{ width: `${target.probabilityPercent}%` }}
                                    />
                                  </div>
                                </div>

                                <div className="flex flex-wrap justify-between gap-1 text-[11px] text-slate-500 font-bengali pt-1 border-t border-slate-200/60 dark:border-slate-800">
                                  <span className="flex items-center gap-1">
                                    <Users className="w-3.5 h-3.5 text-slate-400" />
                                    <span>আসন সংখ্যা: {target.seatCount}</span>
                                  </span>
                                  <span className="flex items-center gap-1 text-slate-500">
                                    <Calendar className="w-3.5 h-3.5 text-slate-400" />
                                    <span>পরীক্ষার তারিখ: {target.examDate}</span>
                                  </span>
                                </div>
                              </div>
                            </div>

                            {/* Actions with 3D Tactile Buttons */}
                            <div className="grid grid-cols-2 gap-3 pt-2">
                              <button 
                                onClick={() => {
                                  startAttempt('diag_' + target.id, 20, 1200);
                                  window.location.href = '/practice';
                                }}
                                className="px-4 py-2.5 rounded-2xl bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700 font-bold font-bengali text-xs shadow-xs active:translate-y-0.5 transition flex items-center justify-center gap-1.5 cursor-pointer"
                              >
                                <Compass className="w-3.5 h-3.5 text-slate-500" />
                                <span>ডায়াগনস্টিক টেস্ট</span>
                              </button>
                              <button 
                                onClick={() => {
                                  startAttempt('mock_' + target.id, 50, 3600);
                                  window.location.href = '/practice';
                                }}
                                className="px-4 py-2.5 rounded-2xl bg-[#0A2540] hover:bg-[#081c30] text-white font-bold font-bengali text-xs shadow-[0_4px_0_0_#071D33] active:translate-y-1 active:shadow-none transition flex items-center justify-center gap-1.5 cursor-pointer"
                              >
                                <span>মডেল টেস্ট দিন</span>
                                <ArrowRight className="w-4 h-4 text-amber-300" />
                              </button>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>

              </div>

            </div>
          )}

          {/* TAB 2: Admission Counseling Matrix & Preference Builder */}
          {activeTab === 'counseling' && (
            <div className="space-y-6">
              <div className="relative overflow-hidden rounded-3xl border border-emerald-200/60 dark:border-emerald-950/70 bg-[#F4FAF6]/90 dark:bg-[#071714]/90 p-6 sm:p-8 shadow-xs space-y-6">
                
                {/* Emerald Atmospheric Halo */}
                <div
                  className="absolute bottom-0 right-0 w-full pointer-events-none select-none z-0"
                  style={{
                    height: '100%',
                    minHeight: '280px',
                    background:
                      'radial-gradient(ellipse 65% 85% at 80% 100%, rgba(16, 185, 129, 0.16) 0%, rgba(16, 185, 129, 0.05) 50%, transparent 100%)'
                  }}
                  aria-hidden="true"
                />

                {/* Thematic Typographic Watermark */}
                <div
                  className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
                  aria-hidden="true"
                >
                  <p
                    className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,18vw,12rem)] uppercase tracking-wider select-none opacity-85"
                    style={{
                      lineHeight: 0.95,
                      backgroundImage:
                        'linear-gradient(to bottom, rgba(16, 185, 129, 0.22) 15%, rgba(16, 185, 129, 0.02) 100%)'
                    }}
                  >
                    COUNSELING
                  </p>
                </div>

                <div className="relative z-10 space-y-1.5 border-b border-emerald-200/60 dark:border-emerald-900/60 pb-5">
                  <div className="flex items-center gap-2">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100/90 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-300/80 dark:border-emerald-800 shadow-xs font-bengali">
                      <Compass className="w-3.5 h-3.5 mr-1 text-emerald-600 dark:text-emerald-400" />
                      গেইল-শ্যাপলি অ্যালগরিদম ম্যাচিং
                    </span>
                  </div>
                  <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#0B251F] dark:text-[#E8F8F4]">
                    ভর্তি কাউন্সেলিং রুম ও বিশ্ববিদ্যালয় চয়েস লিস্ট বিল্ডার
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
                    পছন্দক্রম সাজিয়ে রিয়েল-টাইম ভর্তি সম্ভাবনা ও কোটা স্পিলওভার পর্যালোচনা করুন
                  </p>
                </div>

                {/* Render AdmissionCounselingMatrix */}
                <div className="relative z-10">
                  <AdmissionCounselingMatrix initialRank={1845} initialScore={82.5} />
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: Multi-Round Migration Cascade Visualizer */}
          {activeTab === 'migration' && (
            <div className="space-y-6">
              <div className="relative overflow-hidden rounded-3xl border border-indigo-200/60 dark:border-indigo-950/70 bg-[#F8FAFD]/90 dark:bg-[#09111E]/90 p-6 sm:p-8 shadow-xs space-y-6">
                
                {/* Indigo Atmospheric Halo */}
                <div
                  className="absolute bottom-0 right-0 w-full pointer-events-none select-none z-0"
                  style={{
                    height: '100%',
                    minHeight: '260px',
                    background:
                      'radial-gradient(ellipse 65% 90% at 75% 100%, rgba(99, 102, 241, 0.14) 0%, rgba(99, 102, 241, 0.03) 50%, transparent 100%)'
                  }}
                  aria-hidden="true"
                />

                {/* Thematic Typographic Watermark */}
                <div
                  className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
                  aria-hidden="true"
                >
                  <p
                    className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,18vw,12rem)] uppercase tracking-wider select-none opacity-85"
                    style={{
                      lineHeight: 0.95,
                      backgroundImage:
                        'linear-gradient(to bottom, rgba(99, 102, 241, 0.18) 15%, rgba(99, 102, 241, 0.01) 100%)'
                    }}
                  >
                    CASCADE
                  </p>
                </div>

                <div className="relative z-10 space-y-1.5 border-b border-indigo-200/60 dark:border-indigo-900/60 pb-5">
                  <div className="flex items-center gap-2">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-indigo-100/90 dark:bg-indigo-950/60 text-indigo-900 dark:text-indigo-300 border border-indigo-300/80 dark:border-indigo-800 shadow-xs font-bengali">
                      <Layers className="w-3.5 h-3.5 mr-1 text-indigo-600 dark:text-indigo-400" />
                      আপওয়ার্ড সিট ক্যাসকেড টেলিমেট্রি
                    </span>
                  </div>
                  <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#0A1A3A] dark:text-[#EEF2FF]">
                    মাল্টি-রাউন্ড বিশ্ববিদ্যালয় আসন মাইগ্রেশন ও ভ্যাকেন্সি রিপল সিমুলেটর
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
                    বুয়েট ও মেডিকেল ভর্তির পর বিশ্ববিদ্যালয়সমূহে আসন শূন্য হওয়া এবং আপওয়ার্ড মাইগ্রেশন দেখুন
                  </p>
                </div>

                {/* Render MigrationCascadeVisualizer */}
                <div className="relative z-10">
                  <MigrationCascadeVisualizer />
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: Negative Marking Strategy & Guidelines */}
          {activeTab === 'strategy' && (
            <div className="space-y-6">
              <div className="relative overflow-hidden rounded-3xl border border-amber-200/70 dark:border-amber-950/70 bg-[#FFFDF5]/90 dark:bg-[#0E131E]/90 p-6 sm:p-8 shadow-xs space-y-6">
                
                {/* Soft Golden Halo */}
                <div
                  className="absolute bottom-0 left-0 w-full pointer-events-none select-none z-0"
                  style={{
                    height: '100%',
                    minHeight: '260px',
                    background:
                      'radial-gradient(ellipse 65% 90% at 20% 100%, rgba(245, 158, 11, 0.14) 0%, rgba(245, 158, 11, 0.03) 50%, transparent 100%)'
                  }}
                  aria-hidden="true"
                />

                {/* Typographic Watermark */}
                <div
                  className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
                  aria-hidden="true"
                >
                  <p
                    className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,18vw,12rem)] uppercase tracking-wider select-none opacity-85"
                    style={{
                      lineHeight: 0.95,
                      backgroundImage:
                        'linear-gradient(to bottom, rgba(245, 158, 11, 0.20) 15%, rgba(245, 158, 11, 0.01) 100%)'
                    }}
                  >
                    STRATEGY
                  </p>
                </div>

                <div className="relative z-10 border-b border-amber-200/60 dark:border-slate-800 pb-5 space-y-1.5">
                  <div className="flex items-center gap-2">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-amber-100/90 dark:bg-amber-950/60 text-amber-900 dark:text-amber-300 border border-amber-300/80 dark:border-amber-800 shadow-xs font-bengali">
                      <BookOpen className="w-3.5 h-3.5 mr-1 text-amber-600 dark:text-amber-400" />
                      ভর্তি পরীক্ষা ট্যাকটিক্যাল গাইড
                    </span>
                  </div>

                  <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#1E293B] dark:text-[#F8FAFC]">
                    নেগেটিভ মার্কিং নিয়ন্ত্রণ ও বিষয়ভিত্তিক প্রস্তুতি কৌশল
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
                    শীর্ষস্থানীয় বিশ্ববিদ্যালয় ও মেডিকেল পরীক্ষায় নেগেটিভ মার্কিংয়ের পেনাল্টি এড়িয়ে কাট-অফ সুরক্ষিত রাখার নির্দেশিকা
                  </p>
                </div>

                {/* 4 Strategy Cards */}
                <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#111A2C]/95 border border-amber-200/70 dark:border-slate-800 shadow-xs space-y-2.5 hover:shadow-md transition">
                    <span className="text-xs font-bold text-rose-700 dark:text-rose-400 font-bengali flex items-center gap-1.5">
                      <Percent className="w-4 h-4 text-rose-600" />
                      <span>১. ০.২৫ পেনাল্টি মিনিমাইজেশন</span>
                    </span>
                    <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
                      আন্দাজে উত্তর না দিয়ে অপশন এলিমিনেশন মেথড ব্যবহার করুন। দুটি অপশন নিশ্চিতভাবে বাদ দিতে পারলে তবেই রিস্ক নিন।
                    </p>
                  </div>

                  <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#111A2C]/95 border border-amber-200/70 dark:border-slate-800 shadow-xs space-y-2.5 hover:shadow-md transition">
                    <span className="text-xs font-bold text-[#0A2540] dark:text-amber-300 font-bengali flex items-center gap-1.5">
                      <Clock className="w-4 h-4 text-[#ED8E22]" />
                      <span>২. টাইম ম্যানেজমেন্ট পেসিং</span>
                    </span>
                    <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
                      প্রতিটি বহুনির্বাচনী প্রশ্নের জন্য সর্বোচ্চ ৩৬ থেকে ৪৫ সেকেন্ড বরাদ্দ রাখুন। জটিল গাণিতিক সমস্যা পরবর্তী রাউন্ডের জন্য রাখুন।
                    </p>
                  </div>

                  <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#111A2C]/95 border border-amber-200/70 dark:border-slate-800 shadow-xs space-y-2.5 hover:shadow-md transition">
                    <span className="text-xs font-bold text-emerald-700 dark:text-emerald-400 font-bengali flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                      <span>৩. হাই-ইয়েল্ড চ্যাপ্টার ব্লুপ্রিন্ট</span>
                    </span>
                    <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
                      বিগত ১০ বছরের প্রশ্ন এনালাইসিস করে পদার্থ, রসায়ন, গণিত ও জীববিজ্ঞানের শীর্ষ ৭০% প্রশ্ন যে অধ্যায়গুলো থেকে আসে সেগুলো রিভিশন দিন।
                    </p>
                  </div>

                  <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#111A2C]/95 border border-amber-200/70 dark:border-slate-800 shadow-xs space-y-2.5 hover:shadow-md transition">
                    <span className="text-xs font-bold text-indigo-700 dark:text-indigo-400 font-bengali flex items-center gap-1.5">
                      <Calculator className="w-4 h-4 text-indigo-600" />
                      <span>৪. ক্যালকুলেটর ও হ্যান্ড শর্টকাট</span>
                    </span>
                    <p className="text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed">
                      বুয়েটের জন্য fx-991ES Plus ক্যালকুলেটরের দ্রুত ব্যবহারের কৌশল এবং ঢাবি/মেডিকেলের জন্য ক্যালকুলেটরহীন মানসিক হিসাব চর্চা করুন।
                    </p>
                  </div>
                </div>

                {/* Subject Weightage Breakdown Table */}
                <div className="relative z-10 overflow-x-auto rounded-2xl border border-amber-200/70 dark:border-slate-800 bg-white/95 dark:bg-[#111A2C]/95 shadow-xs">
                  <table className="w-full text-left text-xs font-bengali border-collapse">
                    <thead>
                      <tr className="border-b border-amber-200/60 dark:border-slate-800 bg-amber-50/70 dark:bg-slate-900 text-slate-800 dark:text-slate-200">
                        <th className="p-4 font-bold">ইউনিভার্সিটি ক্লাস্টার</th>
                        <th className="p-4 font-bold">পদার্থবিজ্ঞান</th>
                        <th className="p-4 font-bold">রসায়ন</th>
                        <th className="p-4 font-bold">উচ্চতর গণিত</th>
                        <th className="p-4 font-bold">জীববিজ্ঞান / অন্যান্য</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-amber-100/60 dark:divide-slate-800">
                      <tr className="hover:bg-amber-50/40 dark:hover:bg-slate-800/40 transition">
                        <td className="p-4 font-bold text-slate-900 dark:text-white">ঢাকা বিশ্ববিদ্যালয় (ক-ইউনিট)</td>
                        <td className="p-4 text-slate-700 dark:text-slate-300">২৫ নম্বর (MCQ + লিখিত)</td>
                        <td className="p-4 text-slate-700 dark:text-slate-300">২৫ নম্বর (MCQ + লিখিত)</td>
                        <td className="p-4 text-slate-700 dark:text-slate-300">২৫ নম্বর (বাধ্যতামূলক/ঐচ্ছিক)</td>
                        <td className="p-4 text-slate-700 dark:text-slate-300">২৫ নম্বর (বাধ্যতামূলক/ঐচ্ছিক)</td>
                      </tr>
                      <tr className="hover:bg-amber-50/40 dark:hover:bg-slate-800/40 transition">
                        <td className="p-4 font-bold text-slate-900 dark:text-white">বুয়েট (প্রিলি ও লিখিত)</td>
                        <td className="p-4 text-slate-700 dark:text-slate-300">১০০ নম্বর লিখিত</td>
                        <td className="p-4 text-slate-700 dark:text-slate-300">১০০ নম্বর লিখিত</td>
                        <td className="p-4 text-slate-700 dark:text-slate-300">২০০ নম্বর লিখিত</td>
                        <td className="p-4 text-slate-400">প্রযোজ্য নয়</td>
                      </tr>
                      <tr className="hover:bg-amber-50/40 dark:hover:bg-slate-800/40 transition">
                        <td className="p-4 font-bold text-slate-900 dark:text-white">জাতীয় মেডিকেল (MBBS)</td>
                        <td className="p-4 text-slate-700 dark:text-slate-300">২০ নম্বর</td>
                        <td className="p-4 text-slate-700 dark:text-slate-300">২৫ নম্বর</td>
                        <td className="p-4 text-slate-400">প্রযোজ্য নয়</td>
                        <td className="p-4 text-emerald-700 dark:text-emerald-400 font-bold">৩০ নম্বর (জীববিজ্ঞান) + ইংরেজি ১৫ + জিকে ১০</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

              </div>
            </div>
          )}

          {/* TAB 5: Admission Policies & FAQ Accordion */}
          {activeTab === 'faqs' && (
            <div className="space-y-6">
              <div className="relative overflow-hidden rounded-3xl border border-slate-200/80 dark:border-[#262D3D] bg-white/95 dark:bg-[#0B0F19]/95 p-6 sm:p-8 shadow-xs space-y-6">
                
                {/* Thematic Typographic Watermark */}
                <div
                  className="absolute z-0 pointer-events-none select-none w-full top-2 sm:top-4 left-0 flex justify-center overflow-hidden"
                  aria-hidden="true"
                >
                  <p
                    className="font-black bg-clip-text text-transparent w-full text-center m-0 text-[18vw] md:text-[clamp(3.5rem,18vw,12rem)] uppercase tracking-wider select-none opacity-85"
                    style={{
                      lineHeight: 0.95,
                      backgroundImage:
                        'linear-gradient(to bottom, rgba(10, 37, 64, 0.16) 15%, rgba(10, 37, 64, 0.01) 100%)'
                    }}
                  >
                    POLICIES
                  </p>
                </div>

                <div className="relative z-10 border-b border-slate-200/60 dark:border-slate-800 pb-5 space-y-1.5">
                  <div className="flex items-center gap-2">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-white dark:bg-[#121B2D] text-emerald-800 dark:text-emerald-300 border border-slate-200 dark:border-slate-800 shadow-xs font-bengali">
                      <HelpCircle className="w-3.5 h-3.5 mr-1 text-emerald-600" />
                      ভর্তি নির্দেশিকা ও সচরাচর জিজ্ঞাসা
                    </span>
                  </div>

                  <h2 className="text-xl sm:text-2xl font-serif font-bold tracking-tight font-bengali text-[#0A2540] dark:text-white">
                    সচরাচর জিজ্ঞাসিত প্রশ্নাবলী (Admission FAQ)
                  </h2>
                  <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali">
                    বিশ্ববিদ্যালয় ভর্তি পরীক্ষা, ক্যালকুলেটর নীতিমালা, কোটা নিয়মাবলী ও নেগেটিভ মার্কিং সম্পর্কিত তথ্যাদি
                  </p>
                </div>

                <div className="relative z-10 space-y-3">
                  {ADMISSION_FAQS.map((faq, idx) => {
                    const isOpen = openFaqIndex === idx;
                    return (
                      <div
                        key={idx}
                        className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-[#FAFAF8] dark:bg-slate-950/60 overflow-hidden transition-all"
                      >
                        <button
                          onClick={() => toggleFaq(idx)}
                          className="w-full p-4 sm:p-5 text-left flex items-center justify-between gap-4 font-bold text-xs sm:text-sm text-slate-900 dark:text-white font-bengali hover:text-[#0A2540] dark:hover:text-amber-300 transition cursor-pointer"
                        >
                          <span>{faq.question}</span>
                          {isOpen ? (
                            <ChevronUp className="w-4 h-4 text-[#ED8E22] shrink-0" />
                          ) : (
                            <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
                          )}
                        </button>

                        {isOpen && (
                          <div className="px-4 sm:px-5 pb-5 text-xs text-slate-600 dark:text-slate-300 font-bengali leading-relaxed border-t border-slate-200/60 dark:border-slate-800 pt-3.5">
                            {faq.answer}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

        </main>

        {/* Global Standard 4-Tier Dignified Footer */}
        <Footer />

      </div>
    </>
  );
}
