/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Exam Routine Seed & Fallback Data
 * TOPIC:     Realistic 200-Day BCS & Varsity Admission Routine Calendar Content
 * FILE:      frontend/src/modules/exam-routine/data/examRoutineData.ts
 * PURPOSE:   Provides authentic academic seed data for 200-day BCS and Admission
 *            schedules with Bengali syllabi, accurate negative marking rules,
 *            and weekly mega model test milestones.
 * STANDARDS: Zero-Emoji, Pure Academic Bengali, Zero Placeholder Text
 * ========================================================================================
 */

export interface ExamRoutineItem {
  id: string;
  routine_code: string;
  title: string;
  exam_type: 'BCS_PRELI' | 'ADMISSION_VARSITY' | 'HSC_BOARD' | 'BANK_OFFICER';
  track_category: 'BANGLA' | 'ENGLISH' | 'MATH_SCIENCE' | 'GK' | 'GENERAL';
  day_number: number;
  syllabus_summary: string;
  start_time: string;
  end_time: string;
  duration_minutes: number;
  total_questions: number;
  total_marks: number;
  negative_mark_factor: number;
  is_mega_model_test: boolean;
  is_published: boolean;
  live_participant_count: number;
}

export const INITIAL_EXAM_ROUTINES: ExamRoutineItem[] = [
  {
    id: 'rtn-bcs-001',
    routine_code: 'BCS-200-DAY-001',
    title: 'প্রাচীন ও মধ্যযুগের বাংলা সাহিত্য: চর্যাপদ ও মঙ্গলকাব্য',
    exam_type: 'BCS_PRELI',
    track_category: 'BANGLA',
    day_number: 1,
    syllabus_summary: 'চর্যাপদের আবিষ্কার, পুঁথি পরিচয়, কবিবৃন্দ, শ্রীকৃষ্ণকীর্তন, বৈষ্ণব পদাবলী এবং মনসামঙ্গল কাব্য।',
    start_time: '2026-10-25T04:00:00Z',
    end_time: '2026-11-25T18:00:00Z',
    duration_minutes: 30,
    total_questions: 50,
    total_marks: 50,
    negative_mark_factor: 0.25,
    is_mega_model_test: false,
    is_published: true,
    live_participant_count: 4820,
  },
  {
    id: 'rtn-bcs-002',
    routine_code: 'BCS-200-DAY-002',
    title: 'English Grammar: Parts of Speech, Inversion & Modifiers',
    exam_type: 'BCS_PRELI',
    track_category: 'ENGLISH',
    day_number: 2,
    syllabus_summary: 'Classification of nouns, pronoun-antecedent agreement, adjective clauses, dangling modifiers, parallel structures.',
    start_time: '2026-10-26T04:00:00Z',
    end_time: '2026-11-26T18:00:00Z',
    duration_minutes: 30,
    total_questions: 50,
    total_marks: 50,
    negative_mark_factor: 0.25,
    is_mega_model_test: false,
    is_published: true,
    live_participant_count: 5130,
  },
  {
    id: 'rtn-bcs-003',
    routine_code: 'BCS-200-DAY-003',
    title: 'গাণিতিক যুক্তি: বাস্তব সংখ্যা, লসাগু-গসাগু ও শতকরা',
    exam_type: 'BCS_PRELI',
    track_category: 'MATH_SCIENCE',
    day_number: 3,
    syllabus_summary: 'মূলদ ও অমূলদ সংখ্যা নির্ণয়, বিভাজ্যতার শর্তাবলি, অনুপাত-সমানুপাত এবং শতকরার বাস্তব প্রয়োগ।',
    start_time: '2026-10-27T04:00:00Z',
    end_time: '2026-11-27T18:00:00Z',
    duration_minutes: 30,
    total_questions: 50,
    total_marks: 50,
    negative_mark_factor: 0.25,
    is_mega_model_test: false,
    is_published: true,
    live_participant_count: 5390,
  },
  {
    id: 'rtn-bcs-004',
    routine_code: 'BCS-200-DAY-004',
    title: 'বাংলাদেশ বিষয়াবলী: প্রাচীন বাংলার জনপদ ও ঐতিহাসিক প্রেক্ষাপট',
    exam_type: 'BCS_PRELI',
    track_category: 'GK',
    day_number: 4,
    syllabus_summary: 'মৌর্য ও গুপ্ত যুগ, পাল ও সেন রাজবংশ, সুলতানি আমল ও ঐতিহাসিক শাসন ব্যবস্থার বিবর্তন।',
    start_time: '2026-10-28T04:00:00Z',
    end_time: '2026-11-28T18:00:00Z',
    duration_minutes: 30,
    total_questions: 50,
    total_marks: 50,
    negative_mark_factor: 0.25,
    is_mega_model_test: false,
    is_published: true,
    live_participant_count: 4620,
  },
  {
    id: 'rtn-bcs-mega-001',
    routine_code: 'BCS-200-MEGA-001',
    title: 'সাপ্তাহিক শুক্রবার মেগা মডেল টেস্ট ১: পূর্ণাঙ্গ ২০০ নম্বর বিসিএস প্রিলিমিনারি সিমুলেশন',
    exam_type: 'BCS_PRELI',
    track_category: 'GENERAL',
    day_number: 7,
    syllabus_summary: '১ম সপ্তাহের সামগ্রিক সিলেবাস: বাংলা ৩৫, ইংরেজি ৩৫, বাংলাদেশ বিষয়াবলী ৩০, আন্তর্জাতিক বিষয়াবলী ২০, গাণিতিক যুক্তি ১৫, মানসিক দক্ষতা ১৫, সাধারণ বিজ্ঞান ১৫, কম্পিউটার ১৫, ভূগোল ১০, নৈতিকতা ১০।',
    start_time: '2026-10-31T04:00:00Z',
    end_time: '2026-11-01T16:00:00Z',
    duration_minutes: 120,
    total_questions: 200,
    total_marks: 200,
    negative_mark_factor: 0.50,
    is_mega_model_test: true,
    is_published: true,
    live_participant_count: 18940,
  },
  {
    id: 'rtn-adm-du-001',
    routine_code: 'ADM-DU-KA-001',
    title: "ঢাকা বিশ্ববিদ্যালয় 'ক' ইউনিট: পদার্থবিজ্ঞান ১ম পত্র (ভেক্টর ও নিউটনীয় বলবিদ্যা)",
    exam_type: 'ADMISSION_VARSITY',
    track_category: 'MATH_SCIENCE',
    day_number: 1,
    syllabus_summary: 'ডট ও ক্রস গুণন, প্রাস, ভরবেগের সংরক্ষণশীলতা সূত্র, কেন্দ্রমুখী বল ও সান্দ্রতা সংক্রান্ত গাণিতিক সমস্যা।',
    start_time: '2026-10-26T04:00:00Z',
    end_time: '2026-11-26T18:00:00Z',
    duration_minutes: 45,
    total_questions: 60,
    total_marks: 60,
    negative_mark_factor: 0.25,
    is_mega_model_test: false,
    is_published: true,
    live_participant_count: 6730,
  },
  {
    id: 'rtn-adm-buet-001',
    routine_code: 'ADM-BUET-PRELI-001',
    title: 'বুয়েট প্রাক-নির্বাচনী মেগা মডেল টেস্ট: উচ্চতর গণিত ও রসায়ন সমন্বিত',
    exam_type: 'ADMISSION_VARSITY',
    track_category: 'MATH_SCIENCE',
    day_number: 7,
    syllabus_summary: 'ক্যালকুলাস (অন্তরীকরণ ও যোগজীকরণ), কোণিক, গুণগত রসায়ন, রাসায়নিক পরিবর্তন এবং জারণ-বিজারণ ব্যালেন্সিং।',
    start_time: '2026-11-01T04:00:00Z',
    end_time: '2026-11-02T16:00:00Z',
    duration_minutes: 60,
    total_questions: 100,
    total_marks: 100,
    negative_mark_factor: 0.25,
    is_mega_model_test: true,
    is_published: true,
    live_participant_count: 9820,
  },
  {
    id: 'rtn-hsc-001',
    routine_code: 'HSC-BOARD-001',
    title: 'এইচএসসি বোর্ড স্ট্যান্ডার্ড ফাইনাল মডেল: তথ্য ও যোগাযোগ প্রযুক্তি (আইসিটি)',
    exam_type: 'HSC_BOARD',
    track_category: 'MATH_SCIENCE',
    day_number: 3,
    syllabus_summary: 'এইচটিএমএল স্ট্রাকচার, সি প্রোগ্রামিং লুপিং স্টেটমেন্ট ও বুলিয়ান অ্যালজেব্রার সমীকরণ সরলীকরণ।',
    start_time: '2026-10-26T04:00:00Z',
    end_time: '2026-11-15T18:00:00Z',
    duration_minutes: 25,
    total_questions: 25,
    total_marks: 25,
    negative_mark_factor: 0.25,
    is_mega_model_test: false,
    is_published: true,
    live_participant_count: 3410,
  },
];
