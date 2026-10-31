/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Unified Learning Hub & NCTB Curriculum Navigation
 * TOPIC:     Phase 115, Phase 138 & Modern Academic Editorial Inner Pages Elevation
 * FILE:      frontend/src/pages/learn.tsx
 * PURPOSE:   Standardized academic learning hub with flagship PageHeader,
 *            editorial breadcrumbs, spaced-repetition revision queue, chapter syllabus drawer,
 *            and tactile 3D physics.
 * STANDARDS: Modern Academic Editorial, Pure Academic Palette (#FAF8F3, #1B2A4A, #0A2540),
 *            Zero-Emoji, Zero-Neon, WCAG 2.2 AAA Contrast, 60-75ch Reading Typography
 */

import React, { useState } from 'react';
import Link from 'next/link';
import {
  BookOpen,
  CheckCircle2,
  Clock,
  Play,
  RotateCcw,
  Sparkles,
  ChevronRight,
  ChevronDown,
  Video,
  Award,
  Layers,
  X,
  Compass,
  AlertCircle,
  GraduationCap,
  FileText,
  BookmarkCheck,
  Check,
  ExternalLink,
  Search,
  HelpCircle,
  Lightbulb,
  Target,
  ListChecks,
  BookMarked
} from 'lucide-react';
import { AppHead, createCourseSchema } from '@/components/layout/Head';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { PageHeader } from '@/components/layout/PageHeader';
import { HlsLecturePlayer } from '@/components/video/HlsLecturePlayer';
import {
  Button,
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardMeta,
  CardContent,
  CardFooter,
  Badge,
  Tabs,
  TabsList,
  TabsTrigger,
  Drawer,
  Breadcrumb
} from '@/components/ui';
import { KaTeXRenderer } from '@/components/quiz/katex-renderer';

interface ChapterItem {
  id: string;
  number: number;
  titleBn: string;
  topicCount: number;
  progressPercent: number;
  isRevised: boolean;
  videoLectureId?: string;
  summaryNotes?: {
    overview: string;
    keyFormulas: string[];
    importantPoints: string[];
    textbookPage: string;
  };
}

interface SubjectItem {
  id: string;
  stage: 'MIDDLE' | 'SSC' | 'HSC' | 'ADMISSION';
  titleBn: string;
  titleEn: string;
  chaptersCount: number;
  completedPercent: number;
  chapters: ChapterItem[];
}

const CURATED_SUBJECTS: SubjectItem[] = [
  {
    id: 'sub_phys_1',
    stage: 'HSC',
    titleBn: 'পদার্থবিজ্ঞান ১ম পত্র',
    titleEn: 'HSC Physics 1st Paper',
    chaptersCount: 10,
    completedPercent: 75,
    chapters: [
      {
        id: 'ch_1',
        number: 1,
        titleBn: 'ভেক্টর ও দিক রাশি',
        topicCount: 8,
        progressPercent: 100,
        isRevised: true,
        videoLectureId: 'lec_vec_01',
        summaryNotes: {
          overview: 'ভেক্টর রাশির যোজন, বিয়োজন, ডট গুণন ও ক্রস গুণনের মাধ্যমে দ্বিমাত্রিক ও ত্রিমাত্রিক তলে ভেক্টর বিশ্লেষণ এবং নদী-নৌকার আপেক্ষিক বেগ সংক্রান্ত সমাধান।',
          keyFormulas: [
            'লব্ধি: $R = \\sqrt{P^2 + Q^2 + 2PQ \\cos\\alpha}$',
            'ডট গুণন: $\\vec{A} \\cdot \\vec{B} = AB \\cos\\theta = A_x B_x + A_y B_y + A_z B_z$',
            'ক্রস গুণন: $|\\vec{A} \\times \\vec{B}| = AB \\sin\\theta$'
          ],
          importantPoints: [
            'দুটি ভেক্টর পরস্পর লম্ব হওয়ার শর্ত: $\\vec{A} \\cdot \\vec{B} = 0$',
            'দুটি ভেক্টর পরস্পর সমান্তরাল হওয়ার শর্ত: $\\vec{A} \\times \\vec{B} = 0$',
            'নদী ন্যূনতম সময়ে পারাপারের ক্ষেত্রে লব্ধির দিক নদীর তীরের সাথে $\\theta = 90^\\circ$ হতে হয়।'
          ],
          textbookPage: 'অধ্যায় ২, পৃষ্ঠা ৩৫–৬৮'
        }
      },
      {
        id: 'ch_2',
        number: 2,
        titleBn: 'গতিবিদ্যা ও একমাত্রিক প্রক্ষেপক',
        topicCount: 12,
        progressPercent: 85,
        isRevised: true,
        videoLectureId: 'lec_kin_02',
        summaryNotes: {
          overview: 'একমাত্রিক ও দ্বিমাত্রিক গতি, ত্বরণ, প্রক্ষেপকের গতিপথ এবং প্রাস সংক্রান্ত গাণিতিক সূত্রের প্রতিপাদন ও বাস্তবিক উদাহরণ।',
          keyFormulas: [
            'সর্বোচ্চ উচ্চতা: $H = \\frac{v_0^2 \\sin^2\\theta}{2g}$',
            'উড্ডয়ন কাল: $T = \\frac{2 v_0 \\sin\\theta}{g}$',
            'আনুভূমিক পাল্লা: $R = \\frac{v_0^2 \\sin 2\\theta}{g}$'
          ],
          importantPoints: [
            'সর্বোচ্চ আনুভূমিক পাল্লার জন্য নিক্ষেপণ কোণ $\\theta = 45^\\circ$ হতে হবে।',
            'প্রক্ষেপকের গতিপথ একটি অধিবৃত্ত (প্যারাবোলা)।'
          ],
          textbookPage: 'অধ্যায় ৩, পৃষ্ঠা ৬৯–১০২'
        }
      },
      {
        id: 'ch_3',
        number: 3,
        titleBn: 'নিউটনিয়ান বলবিদ্যা ও ঘূর্ণন গতি',
        topicCount: 14,
        progressPercent: 70,
        isRevised: false,
        videoLectureId: 'lec_newton_03',
        summaryNotes: {
          overview: 'নিউটনের গতির সূত্রসমূহ, ভরবেগের সংরক্ষণশীলতা নীতি, ঘর্ষণ বল, কেন্দ্রমুখী বল, ব্যাংকিং কোণ এবং জড়তার ভ্রামক।',
          keyFormulas: [
            'রাস্তার ব্যাংকিং কোণ: $\\tan\\theta = \\frac{v^2}{rg}$',
            'কৌণিক ভরবেগ: $L = I\\omega = mvr$',
            'ঘূর্ণন গতিশক্তি: $E_k = \\frac{1}{2} I \\omega^2$'
          ],
          importantPoints: [
            'বহিঃস্থ টর্ক শূন্য হলে কৌণিক ভরবেগ ধ্রুব থাকে ($I_1 \\omega_1 = I_2 \\omega_2$)।',
            'জড়তার ভ্রামকের সমান্তরাল ও লম্ব অক্ষ উপপাদ্য বোর্ডের অন্যতম প্রধান বর্ণনামূলক প্রশ্ন।'
          ],
          textbookPage: 'অধ্যায় ৪, পৃষ্ঠা ১০৩–১৪৬'
        }
      },
      {
        id: 'ch_4',
        number: 4,
        titleBn: 'কাজ, শক্তি ও ক্ষমতা',
        topicCount: 10,
        progressPercent: 45,
        isRevised: false,
        videoLectureId: 'lec_work_04',
        summaryNotes: {
          overview: 'পরিবর্তনশীল ও ধ্রুব বল দ্বারা কৃতকাজ, কাজ-শক্তি উপপাদ্য, স্প্রিংয়ের বিভব শক্তি, শক্তির সংরক্ষণশীলতা এবং কর্মদক্ষতা।',
          keyFormulas: [
            'কাজ: $W = \\vec{F} \\cdot \\vec{s} = F s \\cos\\theta$',
            'স্প্রিংয়ের বিভবশক্তি: $U = \\frac{1}{2} k x^2$',
            'কর্মদক্ষতা: $\\eta = \\frac{P_{\\text{out}}}{P_{\\text{in}}} \\times 100\\%$'
          ],
          importantPoints: [
            'কাজ-শক্তি উপপাদ্য: প্রযুক্ত বল দ্বারা মোট কৃতকাজ বস্তুর গতিশক্তির পরিবর্তনের সমান ($W = \\Delta K$)।',
            'অভিকর্ষ বল একটি সংরক্ষণশীল বল।'
          ],
          textbookPage: 'অধ্যায় ৫, পৃষ্ঠা ১৪৭–১৮০'
        }
      }
    ]
  },
  {
    id: 'sub_chem_1',
    stage: 'HSC',
    titleBn: 'রসায়ন ১ম পত্র',
    titleEn: 'HSC Chemistry 1st Paper',
    chaptersCount: 8,
    completedPercent: 60,
    chapters: [
      {
        id: 'ch_c1',
        number: 1,
        titleBn: 'গুণগত রসায়ন ও পরমাণুর গঠন',
        topicCount: 11,
        progressPercent: 90,
        isRevised: true,
        videoLectureId: 'lec_chem_01',
        summaryNotes: {
          overview: 'রাদারফোর্ড ও বোর পরমাণু মডেল, কোয়ান্টাম সংখ্যা, অফবাউ ও হুন্ডের নীতি, এবং দ্রাব্যতা ও দ্রাব্যতা গুণফল ($K_{sp}$)।',
          keyFormulas: [
            'রিডবার্গ সমীকরণ: $\\bar{\\nu} = \\frac{1}{\\lambda} = R_H \\left(\\frac{1}{n_1^2} - \\frac{1}{n_2^2}\\right)$',
            'ডি-ব্রগলির সমীকরণ: $\\lambda = \\frac{h}{mv}$',
            'দ্রাব্যতা গুণফল: $A_x B_y \\rightleftharpoons xA^{y+} + yB^{x-} \\implies K_{sp} = [A^{y+}]^x [B^{x-}]^y$'
          ],
          importantPoints: [
            'হুন্ডের নীতি: সমশক্তি সম্পন্ন অরবিটালে ইলেকট্রনগুলো সর্বাধিক অযুগ্ম অবস্থায় থাকবে এবং তাদের ঘূর্ণন একইমুখী হবে।',
            'অধঃক্ষেপ পড়ার শর্ত: আয়ন গুণফল ($K_{ip}$) > দ্রাব্যতা গুণফল ($K_{sp}$)।'
          ],
          textbookPage: 'অধ্যায় ২, পৃষ্ঠা ৪২–৮৮'
        }
      },
      {
        id: 'ch_c2',
        number: 2,
        titleBn: 'পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন',
        topicCount: 15,
        progressPercent: 65,
        isRevised: false,
        videoLectureId: 'lec_chem_02',
        summaryNotes: {
          overview: 'পর্যায় সারণির বিভিন্ন ব্লকের বৈশিষ্ট্য, পরমাণুর আকার, আয়নীকরণ শক্তি, তড়িৎ ঋণাত্মকতা এবং সংকরায়ন (Hybridization)।',
          keyFormulas: [
            'সংকরায়ন স্টেরিক নম্বর: $SN = \\frac{1}{2} (V + M - C + A)$'
          ],
          importantPoints: [
            'ফাজানের নীতি: ক্যাটায়নের আকার যত ছোট এবং অ্যানায়নের আকার যত বড় হবে, সমযোজী বৈশিষ্ট্য তত বৃদ্ধি পাবে।',
            'পানির অণুতে $sp^3$ সংকরায়ন হওয়া সত্ত্বেও মুক্তজোড় ইলেকট্রন থাকায় বন্ধন কোণ $104.5^\\circ$ হয়।'
          ],
          textbookPage: 'অধ্যায় ৩, পৃষ্ঠা ৮৯–১৪২'
        }
      },
      {
        id: 'ch_c3',
        number: 3,
        titleBn: 'রাসায়নিক পরিবর্তন ও সাম্যাবস্থা',
        topicCount: 14,
        progressPercent: 30,
        isRevised: false,
        videoLectureId: 'lec_chem_03',
        summaryNotes: {
          overview: 'বিক্রিয়ার হার, লা-শাতেলিয়ার নীতি, সাম্যধ্রুবক $K_p$ ও $K_c$ এর সম্পর্ক, এবং বাফার দ্রবণ ও pH গণনা।',
          keyFormulas: [
            'সাম্যধ্রুবক সম্পর্ক: $K_p = K_c (RT)^{\\Delta n}$',
            'হেন্ডারসন-হ্যাসেলবালখ সমীকরণ: $\\text{pH} = \\text{pK}_a + \\log\\frac{[\\text{Salt}]}{[\\text{Acid}]}$'
          ],
          importantPoints: [
            'লা-শাতেলিয়ার নীতি: সাম্যাবস্থায় তাপমাত্রা, চাপ বা ঘনমাত্রা পরিবর্তন করলে সাম্যাবস্থা এমনভাবে স্থানান্তরিত হবে যাতে পরিবর্তনের প্রভাব প্রশমিত হয়।'
          ],
          textbookPage: 'অধ্যায় ৪, পৃষ্ঠা ১৪৩–১৯৮'
        }
      }
    ]
  },
  {
    id: 'sub_math_1',
    stage: 'HSC',
    titleBn: 'উচ্চতর গণিত ১ম পত্র',
    titleEn: 'HSC Higher Mathematics 1st Paper',
    chaptersCount: 10,
    completedPercent: 80,
    chapters: [
      {
        id: 'ch_m1',
        number: 1,
        titleBn: 'ম্যাট্রিক্স ও নির্ণায়ক',
        topicCount: 9,
        progressPercent: 100,
        isRevised: true,
        videoLectureId: 'lec_mat_01',
        summaryNotes: {
          overview: 'ম্যাট্রিক্সের যোগ, বিয়োগ, গুণ, বিপরীত ম্যাট্রিক্স নির্ণয় এবং ক্র্যামারের নিয়মে একঘাত সমীকরণ জোট সমাধান।',
          keyFormulas: [
            'বিপরীত ম্যাট্রিক্স: $A^{-1} = \\frac{1}{|A|} \\text{adj}(A)$, যেখানে $|A| \\neq 0$',
            'ক্র্যামারের নিয়ম: $x = \\frac{D_x}{D}, \\; y = \\frac{D_y}{D}, \\; z = \\frac{D_z}{D}$'
          ],
          importantPoints: [
            'ব্যতিক্রমী ম্যাট্রিক্সের নির্ণায়কের মান শূন্য ($|A| = 0$), যার বিপরীত ম্যাট্রিক্স বিদ্যমান নয়।',
            'ম্যাট্রিক্সের গুণনের শর্ত: প্রথম ম্যাট্রিক্সের কলাম সংখ্যা = দ্বিতীয় ম্যাট্রিক্সের সারি সংখ্যা।'
          ],
          textbookPage: 'অধ্যায় ১, পৃষ্ঠা ১–৪০'
        }
      },
      {
        id: 'ch_m2',
        number: 2,
        titleBn: 'সরলরেখা ও স্থানাঙ্ক জ্যামিতি',
        topicCount: 14,
        progressPercent: 85,
        isRevised: true,
        videoLectureId: 'lec_line_02',
        summaryNotes: {
          overview: 'কার্তেসীয় ও পোলার স্থানাঙ্ক, বিন্দুর অন্তরবিভক্তিকরণ, সরলরেখার ঢাল, বিভিন্ন আকারের সমীকরণ ও মধ্যবর্তী কোণ।',
          keyFormulas: [
            'বিন্দুর দূরত্ব: $d = \\sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$',
            'সরলরেখা হতে বিন্দুর লম্বদূরত্ব: $p = \\frac{|a x_1 + b y_1 + c|}{\\sqrt{a^2 + b^2}}$',
            'দুটি সরলরেখার মধ্যবর্তী কোণ: $\\tan\\theta = \\pm \\frac{m_1 - m_2}{1 + m_1 m_2}$'
          ],
          importantPoints: [
            'পরস্পর লম্ব রেখাদ্বয়ের ঢালের গুণফল: $m_1 m_2 = -1$',
            'পরস্পর সমান্তরাল রেখাদ্বয়ের ঢাল সমান: $m_1 = m_2$'
          ],
          textbookPage: 'অধ্যায় ৩, পৃষ্ঠা ৪১–৯৪'
        }
      },
      {
        id: 'ch_m3',
        number: 3,
        titleBn: 'অন্তরীকরণ ও ক্যালকুলাস',
        topicCount: 16,
        progressPercent: 60,
        isRevised: false,
        videoLectureId: 'lec_diff_03',
        summaryNotes: {
          overview: 'ফাংশনের সীমা (Limit), মূল নিয়মে অন্তরজ নির্ণয়, পর্যায়ক্রমিক অন্তরীকরণ, স্পর্শক ও অভিলম্বের সমীকরণ এবং চরম মান (গুরুমান ও লঘুমান)।',
          keyFormulas: [
            'মূল নিয়মে অন্তরীকরণ: $\\frac{dy}{dx} = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$',
            'গুণফলের সূত্র: $\\frac{d}{dx}(uv) = u \\frac{dv}{dx} + v \\frac{du}{dx}$',
            'ভাগফলের সূত্র: $\\frac{d}{dx}\\left(\\frac{u}{v}\\right) = \\frac{v \\frac{du}{dx} - u \\frac{dv}{dx}}{v^2}$'
          ],
          importantPoints: [
            'চরম মানের প্রয়োজনীয় শর্ত: $f\'(x) = 0$',
            'লঘুমানের জন্য $f\'\'(x) > 0$ এবং গুরুমানের জন্য $f\'\'(x) < 0$।'
          ],
          textbookPage: 'অধ্যায় ৯, পৃষ্ঠা ১৯৫–২৫৪'
        }
      }
    ]
  },
  {
    id: 'sub_ssc_phys',
    stage: 'SSC',
    titleBn: 'পদার্থবিজ্ঞান (এসএসসি)',
    titleEn: 'SSC Physics',
    chaptersCount: 8,
    completedPercent: 90,
    chapters: [
      {
        id: 'ch_s_p1',
        number: 1,
        titleBn: 'ভৌত রাশি ও পরিমাপ',
        topicCount: 7,
        progressPercent: 100,
        isRevised: true,
        videoLectureId: 'lec_ssc_p01',
        summaryNotes: {
          overview: 'পরিমাপের একক, ভার্নিয়ার স্কেল, স্ক্রু গজ এবং পরিমাপে ত্রুটির বিশ্লেষণ।',
          keyFormulas: [
            'ভার্নিয়ার ধ্রুবক: $VC = \\frac{s}{n}$',
            'লঘিষ্ঠ গণন: $LC = \\frac{\\text{Pitch}}{n}$'
          ],
          importantPoints: [
            'ভার্নিয়ার স্কেলের সাহায্যে সাধারণ স্কেলের চেয়ে সূক্ষ্ম পরিমাপ নিশ্চিত করা যায়।'
          ],
          textbookPage: 'অধ্যায় ১, পৃষ্ঠা ১–২০'
        }
      },
      {
        id: 'ch_s_p2',
        number: 2,
        titleBn: 'গতি ও গতির সমীকরণ',
        topicCount: 9,
        progressPercent: 88,
        isRevised: true,
        videoLectureId: 'lec_ssc_p02',
        summaryNotes: {
          overview: 'দূরত্ব ও সরণ, দ্রুতি ও বেগ, সুষম ত্বরণ এবং গতির ৪টি মূল সমীকরণ।',
          keyFormulas: [
            '$v = u + at$',
            '$s = ut + \\frac{1}{2} at^2$',
            '$v^2 = u^2 + 2as$'
          ],
          importantPoints: [
            'মুক্তভাবে পড়ন্ত বস্তুর ক্ষেত্রে গ্যালিলিওর সূত্রসমূহ প্রযোজ্য।'
          ],
          textbookPage: 'অধ্যায় ২, পৃষ্ঠা ২১–৪৫'
        }
      }
    ]
  },
  {
    id: 'sub_ssc_math',
    stage: 'SSC',
    titleBn: 'সাধারণ গণিত (এসএসসি)',
    titleEn: 'SSC General Mathematics',
    chaptersCount: 10,
    completedPercent: 70,
    chapters: [
      {
        id: 'ch_s_m1',
        number: 1,
        titleBn: 'বাস্তব সংখ্যা ও সেট-ফাংশন',
        topicCount: 8,
        progressPercent: 100,
        isRevised: true,
        videoLectureId: 'lec_ssc_m01',
        summaryNotes: {
          overview: 'মূলদ ও অমূলদ সংখ্যা, আবৃত্ত দশমিক, সেটের সংযোগ ও ছেদ, এবং ডোমেন ও রেঞ্জ।',
          keyFormulas: [
            '$n(A \\cup B) = n(A) + n(B) - n(A \\cap B)$'
          ],
          importantPoints: [
            '$\\sqrt{2}, \\sqrt{3}, \\sqrt{5}$ একটি অমূলদ সংখ্যা সংক্রান্ত প্রমাণ বোর্ডের নিয়মিত প্রশ্ন।'
          ],
          textbookPage: 'অধ্যায় ১ ও ২, পৃষ্ঠা ১–৩৫'
        }
      },
      {
        id: 'ch_s_m2',
        number: 2,
        titleBn: 'বীজগাণিতিক রাশি ও সমীকরণ',
        topicCount: 11,
        progressPercent: 65,
        isRevised: false,
        videoLectureId: 'lec_ssc_m02',
        summaryNotes: {
          overview: 'বর্গ ও ঘনের সূত্রাবলী, উৎপাদকে বিশ্লেষণ এবং দ্বিঘাত সমীকরণের মূল নির্ণয়।',
          keyFormulas: [
            '$(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$',
            '$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$'
          ],
          importantPoints: [
            'দ্বিঘাত সমীকরণের নিশ্চায়ক $D = b^2 - 4ac \\ge 0$ হলে মূলদ্বয় বাস্তব হবে।'
          ],
          textbookPage: 'অধ্যায় ৩ ও ৪, পৃষ্ঠা ৩৬–৭৫'
        }
      }
    ]
  }
];

export default function LearnPage() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [selectedStage, setSelectedStage] = useState<'ALL' | 'SSC' | 'HSC' | 'ADMISSION'>('HSC');
  const [activeVideoLecture, setActiveVideoLecture] = useState<{ id: string; title: string } | null>(null);
  const [activeNotesChapter, setActiveNotesChapter] = useState<{ chapter: ChapterItem; subjectTitle: string } | null>(null);
  const [chapterSearchQuery, setChapterSearchQuery] = useState<string>('');
  const [openFaqIndex, setOpenFaqIndex] = useState<number | null>(0);

  const stageFilteredSubjects = selectedStage === 'ALL'
    ? CURATED_SUBJECTS
    : CURATED_SUBJECTS.filter((s) => s.stage === selectedStage);

  const filteredSubjects = chapterSearchQuery.trim() === ''
    ? stageFilteredSubjects
    : stageFilteredSubjects
        .map((sub) => {
          const q = chapterSearchQuery.trim().toLowerCase();
          const matchingChapters = sub.chapters.filter(
            (ch) =>
              ch.titleBn.toLowerCase().includes(q) ||
              sub.titleBn.toLowerCase().includes(q) ||
              (ch.summaryNotes?.overview && ch.summaryNotes.overview.toLowerCase().includes(q))
          );
          return {
            ...sub,
            chapters: matchingChapters
          };
        })
        .filter((sub) => sub.chapters.length > 0);

  return (
    <>
      <AppHead
        title="এনসিটিবি পাঠ্যক্রম ও অধ্যায়ভিত্তিক শিক্ষা | অগ্রযাত্রা"
        description="এনসিটিবি কারিকুলাম অনুযায়ী শ্রেণিভিত্তিক অধ্যায়, ইন্টারেক্টিভ ভিডিও লেকচার ও স্পেসড-রিপিটিশন রিভিশন কিউ।"
        canonicalUrl="/learn"
        ogType="website"
        structuredData={createCourseSchema({
          name: "উচ্চ মাধ্যমিক পদার্থবিজ্ঞান ও গণিত",
          description: "এনসিটিবি কারিকুলাম ২০২৬ অনুযায়ী পদার্থবিজ্ঞান ও গণিতের সম্পূর্ণ পাঠ্যক্রম",
          educationalLevel: "Higher Secondary Certificate"
        })}
      />

      <div className="min-h-screen flex flex-col bg-[#FAFAF8] dark:bg-[#090D16] text-[#1A1A1A] dark:text-slate-100 font-sans selection:bg-[#0A2540] selection:text-white transition-colors duration-200">
        {/* Sticky Unified Global Navigation */}
        <Navbar currentStage="পাঠ্যক্রম ও অধ্যায়ভিত্তিক লার্নিং" />

        <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-10">
          
          {/* Flagship Unified PageHeader */}
          <PageHeader
            category="এনসিটিবি অনুমোদিত ২০২৬ কারিকুলাম"
            title="পাঠ্যক্রম ও অধ্যায়ভিত্তিক শিক্ষা"
            subtitle="জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) অনুমোদিত পাঠ্যবই অনুযায়ী প্রতিটি বিষয়ের পুঙ্খানুপুঙ্খ অধ্যায়, ধারণাগত শিখনফল, বোর্ড প্রশ্নের সংকলন এবং রিভিশন গাইড।"
            watermarkText="CURRICULUM"
            breadcrumbs={[
              { label: 'নীড়পাতা', href: '/' },
              { label: 'পাঠ্যক্রম ও লার্নিং' }
            ]}
            stats={[
              { label: 'কভার্ড বিষয়', value: 'পদার্থ, রসায়ন, গণিত' },
              { label: 'মোট অধ্যায়', value: '২৮টি অধ্যায়' },
              { label: 'ভিডিও লেকচার', value: '১০০% এইচডি', highlight: true },
              { label: 'রিভিশন মেথড', value: 'স্পেসড-রিপিটিশন' }
            ]}
          />

          {/* Section 1: Level Switcher & Chapter Search Console */}
          <div className="relative overflow-hidden rounded-3xl border border-amber-200/60 dark:border-[#262D3D] bg-white/95 dark:bg-[#0B0F19]/95 backdrop-blur-md p-5 sm:p-7 shadow-xs">
            {/* Ambient Warm Amber Glow */}
            <div
              className="pointer-events-none absolute -right-20 -top-20 w-80 h-80 rounded-full bg-radial from-amber-400/12 via-amber-300/5 to-transparent blur-3xl"
              aria-hidden="true"
            />
            
            <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-5">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 rounded-full bg-[#ED8E22] animate-pulse" />
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#B8862B] dark:text-[#ED8E22] font-sans">
                    CURRICULUM LEVEL SELECTOR
                  </span>
                </div>
                <h2 className="text-lg sm:text-xl font-bold font-bengali text-[#0A2540] dark:text-white">
                  শিক্ষাক্রমের স্তর নির্বাচন ও অধ্যায় অনুসন্ধান
                </h2>
                <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali">
                  আপনার কাঙ্ক্ষিত শ্রেণি বা স্তর নির্বাচন করে নির্দিষ্ট বিষয়ের অধ্যায় ও টপিকগুলো ফিল্টার করুন
                </p>
              </div>

              {/* Stage Filter Buttons */}
              <div className="flex flex-wrap items-center gap-2">
                {[
                  { key: 'HSC', label: 'এইচএসসি (Class 11-12)', badge: '১০ অধ্যায়' },
                  { key: 'SSC', label: 'এসএসসি (Class 9-10)', badge: '৮ অধ্যায়' },
                  { key: 'ADMISSION', label: 'বিশ্ববিদ্যালয় ভর্তি', badge: '১০ অধ্যায়' },
                  { key: 'ALL', label: 'সকল স্তর', badge: '২৮ অধ্যায়' },
                ].map((tab) => {
                  const isActive = selectedStage === tab.key;
                  return (
                    <button
                      key={tab.key}
                      type="button"
                      onClick={() => setSelectedStage(tab.key as any)}
                      className={`group relative flex items-center gap-2 px-4 py-2.5 rounded-xl font-bengali text-xs sm:text-sm font-bold transition-all min-h-[44px] cursor-pointer ${
                        isActive
                          ? 'bg-[#0A2540] text-white shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none'
                          : 'bg-[#FAF8F3] dark:bg-slate-900 text-[#1B2A4A] dark:text-slate-300 border border-[#E5E2DA] dark:border-slate-800 hover:border-[#ED8E22]/50 hover:bg-amber-50/50 dark:hover:bg-slate-800'
                      }`}
                    >
                      <span>{tab.label}</span>
                      <span
                        className={`text-[10px] font-sans px-1.5 py-0.5 rounded-md ${
                          isActive
                            ? 'bg-white/20 text-white'
                            : 'bg-amber-100/80 dark:bg-slate-800 text-[#B8862B] dark:text-amber-400'
                        }`}
                      >
                        {tab.badge}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Chapter & Topic Search Bar */}
            <div className="relative z-10 mt-5 pt-5 border-t border-amber-100 dark:border-slate-800 flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
              <div className="relative flex-1">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  value={chapterSearchQuery}
                  onChange={(e) => setChapterSearchQuery(e.target.value)}
                  placeholder="অধ্যায় বা বিষয়ের নাম দিয়ে খুঁজুন (যেমন: ভেক্টর, নিউটনিয়ান বলবিদ্যা, অন্তরীকরণ)..."
                  className="w-full pl-10 pr-10 py-2.5 rounded-xl text-xs sm:text-sm font-bengali bg-white dark:bg-slate-900 border border-[#E5E2DA] dark:border-slate-800 focus:outline-none focus:ring-2 focus:ring-[#ED8E22]/50 focus:border-[#ED8E22] text-[#1B2A4A] dark:text-white placeholder:text-slate-400 transition"
                />
                {chapterSearchQuery && (
                  <button
                    type="button"
                    onClick={() => setChapterSearchQuery('')}
                    aria-label="অনুসন্ধান মুছুন"
                    className="absolute right-3 top-1/2 -translate-y-1/2 p-1 rounded-md text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
              {chapterSearchQuery && (
                <div className="flex items-center gap-2 text-xs font-bengali text-[#0B5D3B] dark:text-emerald-400 px-3 py-2 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/60">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>ফিল্টার সক্রিয়: {filteredSubjects.reduce((acc, s) => acc + s.chapters.length, 0)}টি অধ্যায় পাওয়া গেছে</span>
                </div>
              )}
            </div>
          </div>

          {/* Section 2: Spaced-Repetition Revision Queue (আজকের রিভিশন কিউ) */}
          <div className="relative overflow-hidden rounded-3xl border border-emerald-200/70 dark:border-emerald-950/70 bg-[#F4FAF6]/90 dark:bg-[#071714]/90 p-6 sm:p-8 shadow-xs">
            {/* Background Typographic Watermark */}
            <div
              className="pointer-events-none absolute right-4 -bottom-6 text-7xl sm:text-8xl md:text-9xl font-black tracking-tight text-emerald-900/[0.04] dark:text-emerald-300/[0.03] select-none uppercase font-sans"
              aria-hidden="true"
            >
              REVISION
            </div>

            {/* Ambient Emerald Aura */}
            <div
              className="pointer-events-none absolute -left-16 -top-16 w-72 h-72 rounded-full bg-radial from-emerald-400/12 via-emerald-300/5 to-transparent blur-3xl"
              aria-hidden="true"
            />

            <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-emerald-200/60 dark:border-emerald-900/60 pb-5">
              <div className="flex items-start sm:items-center gap-3.5">
                <div className="w-11 h-11 rounded-2xl bg-emerald-100/80 dark:bg-emerald-900/40 flex items-center justify-center text-[#0B5D3B] dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 shadow-xs shrink-0">
                  <RotateCcw className="w-5 h-5" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-[#0B5D3B] dark:text-emerald-400 font-sans">
                      SM-2 SCIENTIFIC SPACING
                    </span>
                    <Badge variant="success" size="sm">অ্যালগরিদম ট্র্যাকার</Badge>
                  </div>
                  <h2 className="text-lg sm:text-xl font-bold font-bengali text-[#0A2540] dark:text-white pt-0.5">
                    স্পেসড-রিপিটিশন রিভিশন কিউ (আজকের পাঠ তালিকা)
                  </h2>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali pt-0.5">
                    বৈজ্ঞানিক ব্যবধানযুক্ত পুনরাবৃত্তি অনুযায়ী বিস্মৃতি প্রতিরোধে আজকের ৩টি নির্ধারিত পাঠ অবিলম্বে অনুশীলন করুন
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2 self-start sm:self-auto">
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-100/90 dark:bg-amber-950/60 text-[#B8862B] dark:text-amber-300 font-bengali text-xs font-bold border border-amber-300/60 dark:border-amber-800/60">
                  <Clock className="w-3.5 h-3.5" />
                  <span>৩টি টপিক আজ বাকি</span>
                </span>
              </div>
            </div>

            <div className="relative z-10 pt-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="group p-5 rounded-2xl bg-white/95 dark:bg-[#0B141C]/95 border border-emerald-200/80 dark:border-[#223344] hover:border-[#0A2540] dark:hover:border-emerald-500/60 shadow-xs transition-all flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <Badge variant="brand" size="sm">পদার্থবিজ্ঞান ১ম পত্র</Badge>
                      <span className="text-[10px] font-sans font-bold px-2 py-0.5 rounded-full bg-amber-50 dark:bg-amber-950/50 text-[#B8862B] dark:text-amber-400 border border-amber-200 dark:border-amber-900/60">
                        ব্যবধান: ৩য় দিন
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-[#0A2540] dark:text-white font-bengali group-hover:text-[#ED8E22] transition-colors">
                      নিউটনিয়ান বলবিদ্যা (ঘূর্ণন গতিশক্তি ও জড়তার ভ্রামক)
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-slate-400 font-bengali mt-1.5 line-clamp-2">
                      টর্ক, কৌণিক ভরবেগ ও গোলকের অক্ষ সাপেক্ষে জড়তার ভ্রামকের মূল প্রতিপাদন।
                    </p>
                  </div>
                  <Link
                    href="/practice?topic=newtonian_rotation"
                    className="mt-2 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs font-bold font-bengali text-[#0A2540] dark:text-emerald-400 flex items-center justify-between group-hover:translate-x-0.5 transition-transform"
                  >
                    <span className="flex items-center gap-1.5">
                      <Play className="w-3.5 h-3.5 text-[#ED8E22]" />
                      <span>রিভিশন কুইজ শুরু করুন</span>
                    </span>
                    <ChevronRight className="w-4 h-4 text-[#B8862B]" />
                  </Link>
                </div>

                <div className="group p-5 rounded-2xl bg-white/95 dark:bg-[#0B141C]/95 border border-emerald-200/80 dark:border-[#223344] hover:border-[#0A2540] dark:hover:border-emerald-500/60 shadow-xs transition-all flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <Badge variant="success" size="sm">রসায়ন ১ম পত্র</Badge>
                      <span className="text-[10px] font-sans font-bold px-2 py-0.5 rounded-full bg-emerald-50 dark:bg-emerald-950/50 text-[#0B5D3B] dark:text-emerald-300 border border-emerald-200 dark:border-emerald-900/60">
                        ব্যবধান: ৭ম দিন
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-[#0A2540] dark:text-white font-bengali group-hover:text-[#0B5D3B] transition-colors">
                      কোয়ান্টাম সংখ্যা, পাউলির নীতি ও হুন্ডের নীতি
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-slate-400 font-bengali mt-1.5 line-clamp-2">
                      চারটি কোয়ান্টাম সংখ্যার তাৎপর্য ও ক্রোমিয়াম/কপারের ব্যতিক্রমী ইলেকট্রন বিন্যাস।
                    </p>
                  </div>
                  <Link
                    href="/practice?topic=quantum_hund"
                    className="mt-2 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs font-bold font-bengali text-[#0B5D3B] dark:text-emerald-400 flex items-center justify-between group-hover:translate-x-0.5 transition-transform"
                  >
                    <span className="flex items-center gap-1.5">
                      <Play className="w-3.5 h-3.5 text-[#0B5D3B]" />
                      <span>রিভিশন কুইজ শুরু করুন</span>
                    </span>
                    <ChevronRight className="w-4 h-4 text-[#0B5D3B]" />
                  </Link>
                </div>

                <div className="group p-5 rounded-2xl bg-white/95 dark:bg-[#0B141C]/95 border border-emerald-200/80 dark:border-[#223344] hover:border-[#0A2540] dark:hover:border-emerald-500/60 shadow-xs transition-all flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <Badge variant="default" size="sm">উচ্চতর গণিত ১ম পত্র</Badge>
                      <span className="text-[10px] font-sans font-bold px-2 py-0.5 rounded-full bg-blue-50 dark:bg-blue-950/50 text-[#1B2A4A] dark:text-blue-300 border border-blue-200 dark:border-blue-900/60">
                        ব্যবধান: ১৪তম দিন
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-[#0A2540] dark:text-white font-bengali group-hover:text-[#1B2A4A] transition-colors">
                      অন্তরীকরণ (ত্রিকোণমিতিক ডেরিভেটিভ ও চেইন রুল)
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-slate-400 font-bengali mt-1.5 line-clamp-2">
                      ফাংশনের ফাংশন অন্তরীকরণ ও স্পর্শক-অভিলম্বের সমীকরণ নির্ণয়ের বোর্ড কৌশল।
                    </p>
                  </div>
                  <Link
                    href="/practice?topic=calculus_trig"
                    className="mt-2 pt-3 border-t border-slate-100 dark:border-slate-800 text-xs font-bold font-bengali text-[#0A2540] dark:text-blue-400 flex items-center justify-between group-hover:translate-x-0.5 transition-transform"
                  >
                    <span className="flex items-center gap-1.5">
                      <Play className="w-3.5 h-3.5 text-[#0A2540] dark:text-blue-400" />
                      <span>রিভিশন কুইজ শুরু করুন</span>
                    </span>
                    <ChevronRight className="w-4 h-4 text-[#0A2540] dark:text-blue-400" />
                  </Link>
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: NCTB Subjects & Chapters Matrix */}
          <div className="relative overflow-hidden rounded-3xl border border-slate-200/80 dark:border-[#262D3D] bg-[#FAFBFD]/90 dark:bg-[#0A1220]/90 p-6 sm:p-8 shadow-xs">
            {/* Background Typographic Watermark */}
            <div
              className="pointer-events-none absolute right-6 -bottom-6 text-7xl sm:text-8xl md:text-9xl font-black tracking-tight text-slate-900/[0.03] dark:text-white/[0.02] select-none uppercase font-sans"
              aria-hidden="true"
            >
              SYLLABUS
            </div>

            {/* Ambient Navy Aura */}
            <div
              className="pointer-events-none absolute -right-20 -top-20 w-80 h-80 rounded-full bg-radial from-blue-500/8 via-indigo-500/4 to-transparent blur-3xl"
              aria-hidden="true"
            />

            <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200/80 dark:border-slate-800 pb-5 mb-6">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#0A2540] dark:text-sky-400 font-sans">
                    NCTB CURRICULUM SYLLABUS
                  </span>
                  <Badge variant="brand" size="sm">অধ্যায়ভিত্তিক মডিউল</Badge>
                </div>
                <h2 className="text-lg sm:text-2xl font-serif font-bold text-[#0A2540] dark:text-white pt-0.5">
                  পাঠ্যবইয়ের বিষয় ও অধ্যায়সমূহের পূর্ণাঙ্গ তালিকা
                </h2>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 font-bengali pt-0.5">
                  প্রতিটি অধ্যায়ের কনসেপ্ট নোটস, গাণিতিক সূত্রাবলী, ভিডিও লেকচার এবং বোর্ড প্রশ্নের অনুশীলন
                </p>
              </div>

              <div className="flex items-center gap-3">
                <span className="text-xs font-bengali text-slate-500 dark:text-slate-400">
                  মোট বিষয়: <strong className="font-sans text-[#0A2540] dark:text-white">{filteredSubjects.length}</strong> টি
                </span>
              </div>
            </div>

            {/* Subject Cards List */}
            {isLoading ? (
              <div className="space-y-6 animate-pulse">
                {[1, 2].map((i) => (
                  <div key={i} className="p-8 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 space-y-4">
                    <div className="h-6 bg-slate-200 dark:bg-slate-800 rounded w-1/4"></div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="h-24 bg-slate-100 dark:bg-slate-800/60 rounded-xl"></div>
                      <div className="h-24 bg-slate-100 dark:bg-slate-800/60 rounded-xl"></div>
                    </div>
                  </div>
                ))}
              </div>
            ) : filteredSubjects.length === 0 ? (
              <div className="p-12 text-center rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                <div className="w-12 h-12 rounded-full bg-amber-50 dark:bg-amber-950/60 text-[#B8862B] flex items-center justify-center mx-auto mb-3">
                  <Search className="w-6 h-6" />
                </div>
                <h3 className="text-base font-bold font-bengali text-[#0A2540] dark:text-white">
                  কোনো অধ্যায় খুঁজে পাওয়া যায়নি
                </h3>
                <p className="text-xs text-slate-500 font-bengali mt-1">
                  অনুসন্ধান কীওয়ার্ড পরিবর্তন করুন অথবা স্তর ফিল্টার রিসেট করুন।
                </p>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setChapterSearchQuery('');
                    setSelectedStage('ALL');
                  }}
                  className="mt-4 text-xs font-bengali cursor-pointer"
                >
                  ফিল্টার রিসেট করুন
                </Button>
              </div>
            ) : (
              <div className="relative z-10 space-y-8">
                {filteredSubjects.map((sub) => (
                  <div
                    key={sub.id}
                    className="rounded-2xl border border-slate-200/90 dark:border-[#223344] bg-white dark:bg-[#0B121E] overflow-hidden shadow-xs hover:border-[#0A2540]/30 transition-all"
                  >
                    {/* Subject Header with Progress Gauge */}
                    <div className="bg-[#FAF8F3] dark:bg-slate-900/80 border-b border-slate-200/80 dark:border-slate-800 p-5 sm:p-6">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div className="space-y-1">
                          <div className="flex items-center gap-2">
                            <Badge variant="brand" size="sm">
                              {sub.stage}
                            </Badge>
                            <span className="text-xs text-slate-500 font-sans">
                              {sub.titleEn}
                            </span>
                          </div>
                          <h3 className="text-xl sm:text-2xl font-serif font-bold text-[#0A2540] dark:text-white">
                            {sub.titleBn}
                          </h3>
                        </div>

                        {/* Circular Overall Subject Progress */}
                        <div className="flex items-center gap-3 self-start sm:self-auto bg-white dark:bg-slate-900 px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-2xs">
                          <div className="relative w-12 h-12 shrink-0 flex items-center justify-center">
                            <svg className="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
                              <path
                                className="text-slate-200 dark:text-slate-800"
                                strokeWidth="3.2"
                                stroke="currentColor"
                                fill="none"
                                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                              />
                              <path
                                className="text-[#0A2540] dark:text-[#ED8E22] transition-all duration-500"
                                strokeDasharray={`${sub.completedPercent}, 100`}
                                strokeWidth="3.2"
                                strokeLinecap="round"
                                stroke="currentColor"
                                fill="none"
                                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                              />
                            </svg>
                            <span className="absolute text-xs font-sans font-bold text-[#0A2540] dark:text-white tabular-nums">
                              {sub.completedPercent}%
                            </span>
                          </div>

                          <div className="text-left text-xs">
                            <span className="block font-bold font-bengali text-[#0A2540] dark:text-white">সিলেবাস কভারেজ</span>
                            <span className="text-slate-500 font-bengali">{sub.chapters.length} টি অধ্যায় দৃশ্যমান</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Chapters List */}
                    <div className="p-5 sm:p-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {sub.chapters.map((ch) => (
                          <div
                            key={ch.id}
                            className="p-4 sm:p-5 rounded-xl bg-[#FAFBFD] dark:bg-[#070D18] border border-slate-200/80 dark:border-slate-800 hover:border-[#0A2540] dark:hover:border-slate-600 transition-all flex flex-col justify-between gap-4 group"
                          >
                            <div className="flex items-start gap-3.5 min-w-0">
                              {/* Circular Progress Gauge */}
                              <div className="relative w-11 h-11 shrink-0 flex items-center justify-center mt-0.5">
                                <svg className="w-11 h-11 -rotate-90" viewBox="0 0 36 36">
                                  <path
                                    className="text-slate-200 dark:text-slate-800"
                                    strokeWidth="3"
                                    stroke="currentColor"
                                    fill="none"
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                  />
                                  <path
                                    className={ch.progressPercent === 100 ? 'text-[#0B5D3B]' : 'text-[#0A2540] dark:text-sky-400'}
                                    strokeDasharray={`${ch.progressPercent}, 100`}
                                    strokeWidth="3"
                                    strokeLinecap="round"
                                    stroke="currentColor"
                                    fill="none"
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                  />
                                </svg>
                                <span className="absolute text-xs font-sans font-bold text-[#0A2540] dark:text-slate-300">
                                  {ch.number}
                                </span>
                              </div>

                              <div className="min-w-0 flex-1">
                                <div className="flex items-center gap-2 flex-wrap">
                                  <h4 className="text-sm sm:text-base font-bold font-bengali text-[#0A2540] dark:text-white group-hover:text-[#ED8E22] transition-colors">
                                    {ch.titleBn}
                                  </h4>
                                  {ch.progressPercent === 100 && (
                                    <span className="inline-flex items-center gap-1 text-[11px] font-bold font-bengali px-2 py-0.5 rounded-md bg-emerald-100 text-[#0B5D3B] dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                                      <Check className="w-3 h-3" />
                                      সম্পন্ন
                                    </span>
                                  )}
                                </div>
                                <span className="text-xs text-slate-500 dark:text-slate-400 font-bengali block pt-1">
                                  {ch.topicCount} টি পাঠ • {ch.progressPercent}% সম্পন্ন
                                </span>
                              </div>
                            </div>

                            {/* Actions: Notes Drawer, Video Lecture & Practice */}
                            <div className="flex flex-wrap items-center justify-between gap-2 pt-3 border-t border-slate-200/70 dark:border-slate-800">
                              {ch.summaryNotes && (
                                <button
                                  type="button"
                                  onClick={() => setActiveNotesChapter({ chapter: ch, subjectTitle: sub.titleBn })}
                                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-xs font-bold font-bengali text-[#0A2540] dark:text-slate-200 hover:bg-amber-50 hover:border-amber-300 dark:hover:bg-slate-800 transition min-h-[36px] cursor-pointer"
                                >
                                  <FileText className="w-3.5 h-3.5 text-[#B8862B]" />
                                  <span>পড়ুন ও নোটস</span>
                                </button>
                              )}

                              <div className="flex items-center gap-2 ml-auto">
                                {ch.videoLectureId && (
                                  <button
                                    type="button"
                                    onClick={() => setActiveVideoLecture({ id: ch.videoLectureId!, title: ch.titleBn })}
                                    className="p-2 rounded-lg bg-white dark:bg-slate-800 text-[#0A2540] dark:text-slate-200 hover:bg-[#0A2540] hover:text-white transition border border-slate-200 dark:border-slate-700 cursor-pointer min-h-[36px]"
                                    title="লেকচার ভিডিও দেখুন"
                                    aria-label={`লেকচার ভিডিও দেখুন: ${ch.titleBn}`}
                                  >
                                    <Video className="w-4 h-4" />
                                  </button>
                                )}

                                <Link
                                  href={`/practice?chapter=${ch.id}`}
                                  className="px-4 py-1.5 rounded-lg bg-[#0A2540] hover:bg-[#081c30] text-white font-bengali text-xs font-bold shadow-[0_3px_0_0_#071D33] active:translate-y-1 active:shadow-none transition flex items-center gap-1.5 min-h-[36px]"
                                  title="অধ্যায় অনুশীলন করুন"
                                  aria-label={`অনুশীলন করুন: ${ch.titleBn}`}
                                >
                                  <Play className="w-3.5 h-3.5 text-[#ED8E22]" />
                                  <span>অনুশীলন</span>
                                </Link>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Section 4: Board Examination Pedagogical Roadmap */}
          <div className="relative overflow-hidden rounded-3xl border border-amber-200/70 dark:border-[#262D3D] bg-[#FFFDF9]/90 dark:bg-[#0C111C]/90 p-6 sm:p-8 shadow-xs">
            {/* Background Typographic Watermark */}
            <div
              className="pointer-events-none absolute right-4 -bottom-6 text-7xl sm:text-8xl md:text-9xl font-black tracking-tight text-amber-900/[0.04] dark:text-amber-400/[0.02] select-none uppercase font-sans"
              aria-hidden="true"
            >
              GUIDELINES
            </div>

            {/* Ambient Warm Amber Aura */}
            <div
              className="pointer-events-none absolute -left-16 -top-16 w-80 h-80 rounded-full bg-radial from-amber-400/12 via-amber-200/5 to-transparent blur-3xl"
              aria-hidden="true"
            />

            <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-amber-200/60 dark:border-slate-800 pb-5 mb-6">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#B8862B] dark:text-[#ED8E22] font-sans">
                    ACADEMIC METHODOLOGY & MASTERY
                  </span>
                  <Badge variant="warning" size="sm">বোর্ড স্ট্যান্ডার্ড</Badge>
                </div>
                <h2 className="text-lg sm:text-2xl font-serif font-bold text-[#0A2540] dark:text-white pt-0.5">
                  বোর্ড পরীক্ষা ও পাঠ্যক্রম প্রস্তুতি রোডম্যাপ
                </h2>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 font-bengali pt-0.5">
                  এনসিটিবি মূল পাঠ্যবই এবং জাতীয় শিক্ষাক্রমের আলোকে শীর্ষ ফলাফলের ৪টি প্রমাণিত শিক্ষাদান ধাপ
                </p>
              </div>
            </div>

            <div className="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#080E18]/95 border border-amber-200/80 dark:border-slate-800 flex flex-col justify-between space-y-3 shadow-2xs">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-amber-100/80 dark:bg-amber-950/60 flex items-center justify-center text-[#B8862B] dark:text-amber-300 mb-3 border border-amber-200 dark:border-amber-900/60">
                    <Lightbulb className="w-5 h-5" />
                  </div>
                  <h3 className="text-sm font-bold font-bengali text-[#0A2540] dark:text-white">
                    ১. ধারণাগত শিখনফল (Concept First)
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed mt-2">
                    প্রতিটি অধ্যায়ের মৌলিক সংজ্ঞা, ভৌত ব্যাখ্যা ও মূল সূত্রের প্রতিপাদন গভীরভাবে আয়ত্ত করুন।
                  </p>
                </div>
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-[#B8862B] font-bengali font-bold">
                  বোর্ড সিলেবাস ১০০% কভার্ড
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#080E18]/95 border border-amber-200/80 dark:border-slate-800 flex flex-col justify-between space-y-3 shadow-2xs">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-emerald-100/80 dark:bg-emerald-950/60 flex items-center justify-center text-[#0B5D3B] dark:text-emerald-300 mb-3 border border-emerald-200 dark:border-emerald-900/60">
                    <ListChecks className="w-5 h-5" />
                  </div>
                  <h3 className="text-sm font-bold font-bengali text-[#0A2540] dark:text-white">
                    ২. বোর্ড প্রশ্ন সংকলন (Board Archives)
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed mt-2">
                    সকল শিক্ষা বোর্ডের বিগত ৮ বছরের সৃজনশীল (CQ) ও বহুনির্বাচনী (MCQ) প্রশ্নের টাইপভিত্তিক সমাধান।
                  </p>
                </div>
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-[#0B5D3B] font-bengali font-bold">
                  টাইপভিত্তিক বোর্ড আর্কাইভ
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#080E18]/95 border border-amber-200/80 dark:border-slate-800 flex flex-col justify-between space-y-3 shadow-2xs">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-sky-100/80 dark:bg-sky-950/60 flex items-center justify-center text-[#0A2540] dark:text-sky-300 mb-3 border border-sky-200 dark:border-sky-900/60">
                    <BookMarked className="w-5 h-5" />
                  </div>
                  <h3 className="text-sm font-bold font-bengali text-[#0A2540] dark:text-white">
                    ৩. সূত্র ও হ্যান্ডনোট (LaTeX Formulas)
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed mt-2">
                    পরীক্ষার আগের রাতে দ্রুত চোখ বুলিয়ে নেয়ার জন্য প্রয়োজনীয় সব গাণিতিক ফর্মুলার সুবিন্যস্ত শিট।
                  </p>
                </div>
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-[#0A2540] dark:text-sky-400 font-bengali font-bold">
                  কুইক রিভিশন রেডি
                </div>
              </div>

              <div className="p-5 rounded-2xl bg-white/95 dark:bg-[#080E18]/95 border border-amber-200/80 dark:border-slate-800 flex flex-col justify-between space-y-3 shadow-2xs">
                <div>
                  <div className="w-10 h-10 rounded-xl bg-purple-100/80 dark:bg-purple-950/60 flex items-center justify-center text-purple-700 dark:text-purple-300 mb-3 border border-purple-200 dark:border-purple-900/60">
                    <Target className="w-5 h-5" />
                  </div>
                  <h3 className="text-sm font-bold font-bengali text-[#0A2540] dark:text-white">
                    ৪. স্মার্ট প্র্যাকটিস ট্র্যাকার (Adaptive Exam)
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 font-bengali leading-relaxed mt-2">
                    আপনার দুর্বল টপিকগুলো স্বয়ংক্রিয়ভাবে শনাক্ত করে পুনরায় অনুশীলনের সুপারিশ প্রদান করবে।
                  </p>
                </div>
                <div className="pt-2 border-t border-slate-100 dark:border-slate-800 text-[11px] text-purple-700 dark:text-purple-300 font-bengali font-bold">
                  দুর্বলতা দূরীকরণ ব্যবস্থা
                </div>
              </div>
            </div>
          </div>

          {/* Section 5: Curriculum FAQ Accordions */}
          <div className="relative overflow-hidden rounded-3xl border border-slate-200/80 dark:border-[#262D3D] bg-[#FAF8F3]/90 dark:bg-[#0A1220]/90 p-6 sm:p-8 shadow-xs">
            {/* Background Typographic Watermark */}
            <div
              className="pointer-events-none absolute right-4 -bottom-6 text-7xl sm:text-8xl md:text-9xl font-black tracking-tight text-slate-900/[0.03] dark:text-white/[0.02] select-none uppercase font-sans"
              aria-hidden="true"
            >
              ACADEMIC
            </div>

            {/* Ambient Aura */}
            <div
              className="pointer-events-none absolute -right-16 -top-16 w-80 h-80 rounded-full bg-radial from-slate-400/10 via-slate-300/5 to-transparent blur-3xl"
              aria-hidden="true"
            />

            <div className="relative z-10 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200/80 dark:border-slate-800 pb-5 mb-6">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#0A2540] dark:text-sky-400 font-sans">
                    NCTB CURRICULUM FAQ
                  </span>
                  <Badge variant="default" size="sm">সাধারণ জিজ্ঞাসা</Badge>
                </div>
                <h2 className="text-lg sm:text-2xl font-serif font-bold text-[#0A2540] dark:text-white pt-0.5">
                  পাঠ্যক্রম ও অধ্যয়ন নির্দেশিকা সংক্রান্ত প্রশ্নোত্তর
                </h2>
                <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 font-bengali pt-0.5">
                  বোর্ড পরীক্ষা প্রস্তুতি ও কারিকুলাম ট্র্যাকিং নিয়ে শিক্ষার্থীদের বহুল জিজ্ঞাসিত প্রশ্নসমূহ
                </p>
              </div>
            </div>

            <div className="relative z-10 space-y-3 max-w-4xl">
              {[
                {
                  q: 'এখানে দেওয়া পাঠ্যক্রম কি ২০২৬ সালের সর্বশেষ এনসিটিবি সিলেবাস অনুযায়ী সাজানো?',
                  a: 'হ্যাঁ, জাতীয় শিক্ষাক্রম ও পাঠ্যপুস্তক বোর্ড (NCTB) অনুমোদিত সর্বশেষ পাঠ্যবই এবং বোর্ড পরীক্ষার প্রশ্নকাঠামো মেনেই প্রতিটি অধ্যায় ও টপিক অন্তর্ভুক্ত করা হয়েছে।'
                },
                {
                  q: 'স্পেসড-রিপিটিশন (SM-2) রিভিশন পদ্ধতি কীভাবে আমাকে সাহায্য করবে?',
                  a: 'মনোবিজ্ঞানী এবিংহাউসের বিস্মৃতি রেখা (Forgetting Curve) অনুযায়ী মানুষ পড়ার কিছুদিনের মধ্যেই অধিকাংশ ভুলে যায়। আমাদের SM-2 মডেল নির্দিষ্ট ব্যবধানে (১ম, ৩য়, ৭ম ও ১৪তম দিন) আপনাকে রিভিশন কুইজ নেওয়ার তাগিদ দেয়, যা দীর্ঘমেয়াদী স্মৃতিশক্তি নিশ্চিত করে।'
                },
                {
                  q: 'অধ্যায়ের হ্যান্ডনোট এবং গাণিতিক সূত্রাবলী কি প্রিন্ট বা অফলাইনে সংরক্ষণ করা যায়?',
                  a: 'প্রতিটি অধ্যায়ের "পড়ুন ও নোটস" ড্রয়ারে প্রয়োজনীয় সকল গাণিতিক সূত্র LaTeX ফরম্যাটে উপস্থাপিত। আপনি যে কোনো ডিভাইস থেকে এগুলো সহজে পাঠ করতে পারেন এবং ব্রাউজারের প্রিন্ট অপশন ব্যবহার করে পিডিএফ আকারে সংরক্ষণ করতে পারেন।'
                },
                {
                  q: 'সৃজনশীল প্রশ্ন (CQ) লেখার ক্ষেত্রে কোন বিষয়ের উপর জোর দেওয়া উচিত?',
                  a: 'জ্ঞান ও অনুধাবনমূলক প্রশ্নের জন্য পাঠ্যবইয়ের সঠিক সংজ্ঞা ও ব্যাখ্যা জরুরি। প্রয়োগ ও উচ্চতর দক্ষতার ক্ষেত্রে গাণিতিক সূত্রের সঠিক উপস্থাপনা, একক ও যথাযথ চিত্র অঙ্কন নিশ্চিত করতে হবে।'
                }
              ].map((item, idx) => {
                const isOpen = openFaqIndex === idx;
                return (
                  <div
                    key={idx}
                    className="rounded-2xl border border-slate-200/80 dark:border-slate-800 bg-white/95 dark:bg-[#070D18]/95 overflow-hidden transition-all shadow-2xs"
                  >
                    <button
                      type="button"
                      onClick={() => setOpenFaqIndex(isOpen ? null : idx)}
                      className="w-full text-left px-5 py-4 flex items-center justify-between gap-4 font-bengali font-bold text-sm sm:text-base text-[#0A2540] dark:text-white hover:text-[#ED8E22] transition cursor-pointer"
                    >
                      <span className="flex items-center gap-2.5">
                        <HelpCircle className="w-4 h-4 text-[#B8862B] shrink-0" />
                        <span>{item.q}</span>
                      </span>
                      <ChevronDown
                        className={`w-4 h-4 text-slate-400 shrink-0 transition-transform duration-200 ${
                          isOpen ? 'rotate-180 text-[#ED8E22]' : ''
                        }`}
                      />
                    </button>
                    {isOpen && (
                      <div className="px-5 pb-5 pt-1 text-xs sm:text-sm text-slate-600 dark:text-slate-300 font-bengali leading-relaxed border-t border-slate-100 dark:border-slate-800/60">
                        {item.a}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

        </main>

        {/* Global Dignified Footer */}
        <Footer />
      </div>

      {/* Chapter Editorial Notes Drawer (60-75ch Textbook Reading Standard) */}
      <Drawer
        isOpen={!!activeNotesChapter}
        onClose={() => setActiveNotesChapter(null)}
        title={activeNotesChapter?.chapter.titleBn || ''}
        side="right"
      >
        {activeNotesChapter && (
          <div className="space-y-6 max-w-[70ch] leading-[1.8] text-[#1A1A1A] font-bengali text-sm sm:text-base">
            <div className="flex items-center gap-2 border-b border-[#E5E2DA] pb-3">
              <Badge variant="brand" size="sm">{activeNotesChapter.subjectTitle}</Badge>
              <Badge variant="default" size="sm">অধ্যায় {activeNotesChapter.chapter.number}</Badge>
              <span className="text-xs text-[#5B5B5B] ml-auto">
                {activeNotesChapter.chapter.summaryNotes?.textbookPage}
              </span>
            </div>

            <div>
              <h4 className="font-serif font-bold text-base text-[#1B2A4A] mb-2">
                ১. সারসংক্ষেপ ও শিখনফল
              </h4>
              <p className="text-[#333333] leading-relaxed">
                {activeNotesChapter.chapter.summaryNotes?.overview}
              </p>
            </div>

            {/* Flat Bordered Callout Box for Formulas */}
            <div className="bg-[#FAF8F3] border border-[#E5E2DA] rounded-xl p-4 sm:p-5 space-y-3">
              <div className="flex items-center gap-2 text-[#1B2A4A] font-bold text-sm">
                <BookmarkCheck className="w-4 h-4 text-[#B8862B]" />
                <span>প্রয়োজনীয় গাণিতিক সূত্রাবলী</span>
              </div>
              <div className="space-y-2 pt-1 font-sans">
                {activeNotesChapter.chapter.summaryNotes?.keyFormulas.map((f, idx) => (
                  <div key={idx} className="bg-white p-2.5 rounded-lg border border-[#E5E2DA] text-sm overflow-x-auto">
                    <KaTeXRenderer text={f} />
                  </div>
                ))}
              </div>
            </div>

            {/* Flat Bordered Callout for Exam Tips */}
            <div className="bg-[#F0F7F4] border border-[#CDE5DB] rounded-xl p-4 sm:p-5 space-y-2">
              <div className="flex items-center gap-2 text-[#0B5D3B] font-bold text-sm">
                <Check className="w-4 h-4" />
                <span>এনসিটিবি বোর্ড পরীক্ষার জন্য গুরুত্বপূর্ণ পর্যবেক্ষণ</span>
              </div>
              <ul className="space-y-1.5 list-disc list-inside text-sm text-[#065F46] leading-relaxed">
                {activeNotesChapter.chapter.summaryNotes?.importantPoints.map((pt, idx) => (
                  <li key={idx}>
                    <KaTeXRenderer text={pt} />
                  </li>
                ))}
              </ul>
            </div>

            {/* Drawer Actions */}
            <div className="pt-4 border-t border-[#E5E2DA] flex flex-wrap gap-3">
              <Link
                href={`/practice?chapter=${activeNotesChapter.chapter.id}`}
                className="flex-1"
              >
                <Button variant="primary" className="w-full">
                  <Play className="w-4 h-4 mr-1.5 text-[#B8862B]" />
                  <span>এই অধ্যায়ের বোর্ড প্রশ্ন অনুশীলন</span>
                </Button>
              </Link>

              {activeNotesChapter.chapter.videoLectureId && (
                <Button
                  variant="outline"
                  onClick={() => {
                    const vidId = activeNotesChapter.chapter.videoLectureId!;
                    const vidTitle = activeNotesChapter.chapter.titleBn;
                    setActiveNotesChapter(null);
                    setActiveVideoLecture({ id: vidId, title: vidTitle });
                  }}
                >
                  <Video className="w-4 h-4 mr-1.5 text-[#1B2A4A]" />
                  <span>ভিডিও লেকচার</span>
                </Button>
              )}
            </div>
          </div>
        )}
      </Drawer>

      {/* HLS Video Lecture Player Modal */}
      {activeVideoLecture && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 animate-in fade-in"
        >
          <div className="relative w-full max-w-4xl bg-white dark:bg-slate-900 rounded-2xl border border-[#E5E2DA] shadow-xl overflow-hidden flex flex-col">
            <div className="flex items-center justify-between px-6 py-4 border-b border-[#E5E2DA] bg-[#FAF8F3] dark:bg-slate-950/60">
              <div className="flex items-center gap-2">
                <Video className="w-5 h-5 text-[#1B2A4A]" />
                <span className="font-bold font-bengali text-[#1B2A4A] dark:text-white text-sm sm:text-base">
                  {activeVideoLecture.title} (HLS Adaptive Stream)
                </span>
              </div>
              <button
                type="button"
                onClick={() => setActiveVideoLecture(null)}
                aria-label="ভিডিও বন্ধ করুন"
                className="p-2 rounded-lg bg-white dark:bg-slate-800 text-[#5B5B5B] hover:text-[#1A1A1A] hover:bg-[#FAF8F3] transition border border-[#E5E2DA] cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 sm:p-6">
              <HlsLecturePlayer
                lectureId={activeVideoLecture.id}
                studentId="std_curr_user"
                titleBn={activeVideoLecture.title}
                durationSeconds={480}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
