/**
 * ========================================================================================
 * MODULE:    AI Question Bank & Draft Review Console
 * TOPIC:     Human-in-the-Loop SME Review Queue, Fast Keyboard Review & In-line Moderation
 * FILE:      frontend/src/pages/admin/review-queue.tsx
 * PURPOSE:   Provides a dedicated administrative review queue for AI-generated and
 *            teacher-submitted draft questions. Enforces the strict human Subject
 *            Matter Expert (SME) approval gate before any question can enter student-facing
 *            examination pools. Features master-detail layout, inline content editing,
 *            keyboard shortcuts (A/R/E/J/K), persistent URL filters, and bulk moderation.
 * AUDIENCE:  Subject Matter Experts, Curriculum Directors & Quality Assurance Leads
 * STANDARDS: Modern Academic Editorial, ASVS L2 RBAC, WCAG 2.2 AA, Strict Zero-Emoji
 * ========================================================================================
 */

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import {
  CheckCircle2,
  XCircle,
  Edit3,
  Sparkles,
  Search,
  Filter,
  ArrowRight,
  ShieldCheck,
  RotateCcw,
  BookOpen,
  Layers,
  ArrowLeft,
  ChevronRight,
  ChevronLeft,
  Save,
  Clock,
  User,
  SlidersHorizontal,
  CornerDownRight,
  Send,
  AlertTriangle,
  History,
  X
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { ThemeToggle } from '../../components/ui/theme-toggle';
import { useAuth } from '@/lib/auth-context';
import { withAdminAuth } from '@/components/auth/AdminAuthGuard';
import { apiClient } from '@/lib/api-client';
import { toBengaliDigits, useTranslation } from '../../lib/i18n';

interface OptionItem {
  id?: string;
  option_key: string;
  option_text_bn: string;
  is_correct: boolean;
  distractor_rationale?: string;
}

interface DraftQuestion {
  id: string;
  version: number;
  status: 'NEEDS_REVIEW' | 'DRAFT' | 'APPROVED' | 'REJECTED' | 'NEEDS_CHANGES' | 'PUBLISHED';
  subject: string;
  topic: string;
  concept: string;
  stem_bn: string;
  stem_en?: string;
  options: OptionItem[];
  explanation_bn: string;
  explanation_en?: string;
  difficulty: string;
  cognitive_skill: string;
  curriculum: string;
  class_grade: number;
  is_ai_generated: boolean;
  ai_confidence_score: number;
  ai_model: string;
  deduplication_similarity: number;
  is_duplicate_flag: boolean;
  source_attribution?: string;
  creator_user_id: string;
  reviewed_by?: string;
  reviewed_at?: string;
  rejection_feedback?: string;
  created_at: string;
}

interface StatusCounts {
  all: number;
  needs_review: number;
  draft: number;
  approved: number;
  rejected: number;
  needs_changes: number;
}

const DEFAULT_COUNTS: StatusCounts = {
  all: 6,
  needs_review: 3,
  draft: 1,
  approved: 1,
  rejected: 1,
  needs_changes: 0,
};

const SUBJECT_OPTIONS = [
  { value: 'ALL', labelBn: 'সকল বিষয়', labelEn: 'All Subjects' },
  { value: 'পদার্থবিজ্ঞান', labelBn: 'পদার্থবিজ্ঞান', labelEn: 'Physics' },
  { value: 'রসায়ন', labelBn: 'রসায়ন', labelEn: 'Chemistry' },
  { value: 'উচ্চতর গণিত', labelBn: 'উচ্চতর গণিত', labelEn: 'Higher Math' },
  { value: 'জীববিজ্ঞান', labelBn: 'জীববিজ্ঞান', labelEn: 'Biology' },
  { value: 'তথ্য ও যোগাযোগ প্রযুক্তি', labelBn: 'তথ্য ও যোগাযোগ প্রযুক্তি', labelEn: 'ICT' },
];

const DIFFICULTY_OPTIONS = [
  { value: 'ALL', labelBn: 'সকল স্তর', labelEn: 'All Difficulties' },
  { value: 'EASY', labelBn: 'সহজ (EASY)', labelEn: 'Easy (EASY)' },
  { value: 'MEDIUM', labelBn: 'মধ্যম (MEDIUM)', labelEn: 'Medium (MEDIUM)' },
  { value: 'HARD', labelBn: 'কঠিন (HARD)', labelEn: 'Hard (HARD)' },
];

const SOURCE_OPTIONS = [
  { value: 'ALL', labelBn: 'সকল উৎস', labelEn: 'All Sources' },
  { value: 'AI_GENERATED', labelBn: 'এআই জেনারেটেড', labelEn: 'AI Generated' },
  { value: 'TEACHER_SUBMISSION', labelBn: 'শিক্ষক সাবমিশন', labelEn: 'Teacher Submission' },
];

const REJECTION_PRESETS_BN = [
  'এনসিটিবি কারিকুলাম মানদণ্ডের সাথে অমিল',
  'বিকল্প উত্তরে অস্পষ্টতা বা একাধিক সঠিক উত্তর দৃশ্যমান',
  'সঠিক উত্তরের স্বপক্ষে প্রদত্ত ব্যাখ্যা পর্যাপ্ত নয়',
  'ব্লুমস ট্যাক্সোনমি স্তর সামঞ্জস্যপূর্ণ নয়',
  'প্রশ্নপত্রে মুদ্রণ বা বৈজ্ঞানিক পরিভাষা সংক্রান্ত ত্রুটি রয়েছে',
];

const REJECTION_PRESETS_EN = [
  'Non-compliance with NCTB curriculum benchmark',
  'Ambiguity in options or multiple correct answers detected',
  'Pedagogical explanation lacks sufficient rationale',
  'Bloom taxonomy cognitive level misalignment',
  'Typographical error or scientific terminology inaccuracy',
];

const LOCAL_STORAGE_BACKUP_KEY = 'ogrojatra_draft_review_cache';

function ReviewQueuePageComponent() {
  const router = useRouter();
  const { user } = useAuth();
  const { t, locale } = useTranslation();
  const isBn = locale === 'bn';

  const pageTitle = isBn
    ? "এআই ড্রাফট রিভিউ কিউ | অগ্রযাত্রা অ্যাডমিন"
    : "AI Draft Review Queue | Ogrojatra Admin";

  useEffect(() => {
    if (typeof document !== 'undefined') {
      document.title = pageTitle;
    }
  }, [pageTitle]);

  // URL Query Initialization
  const queryStatus = (router.query.status as string) || 'NEEDS_REVIEW';
  const querySubject = (router.query.subject as string) || 'ALL';
  const queryDifficulty = (router.query.difficulty as string) || 'ALL';
  const querySearch = (router.query.search as string) || '';

  // Main State
  const [drafts, setDrafts] = useState<DraftQuestion[]>([]);
  const [counts, setCounts] = useState<StatusCounts>(DEFAULT_COUNTS);
  const [selectedDraftId, setSelectedDraftId] = useState<string | null>(null);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Filter States
  const [statusFilter, setStatusFilter] = useState<string>(queryStatus);
  const [subjectFilter, setSubjectFilter] = useState<string>(querySubject);
  const [difficultyFilter, setDifficultyFilter] = useState<string>(queryDifficulty);
  const [sourceFilter, setSourceFilter] = useState<string>('ALL');
  const [searchInput, setSearchInput] = useState<string>(querySearch);
  const [activeSearch, setActiveSearch] = useState<string>(querySearch);

  // Rejection Modal State
  const [rejectModalOpen, setRejectModalOpen] = useState<boolean>(false);
  const [rejectTargetId, setRejectTargetId] = useState<string | null>(null);
  const [rejectionReason, setRejectionReason] = useState<string>('');

  // Inline Editing State
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [editForm, setEditForm] = useState<{
    stem_bn: string;
    options: OptionItem[];
    explanation_bn: string;
    difficulty: string;
    cognitive_skill: string;
  }>({
    stem_bn: '',
    options: [],
    explanation_bn: '',
    difficulty: 'MEDIUM',
    cognitive_skill: 'APPLICATION',
  });

  // Toast State
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  const showToast = useCallback((message: string, type: 'success' | 'error' = 'success') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  }, []);

  // Sync URL when filters change
  const syncUrlParams = useCallback((newFilters: { status?: string; subject?: string; difficulty?: string; search?: string }) => {
    const nextQuery: Record<string, string> = { ...router.query } as Record<string, string>;

    if (newFilters.status) nextQuery.status = newFilters.status;
    if (newFilters.subject) {
      if (newFilters.subject === 'ALL') delete nextQuery.subject;
      else nextQuery.subject = newFilters.subject;
    }
    if (newFilters.difficulty) {
      if (newFilters.difficulty === 'ALL') delete nextQuery.difficulty;
      else nextQuery.difficulty = newFilters.difficulty;
    }
    if (newFilters.search !== undefined) {
      if (!newFilters.search.trim()) delete nextQuery.search;
      else nextQuery.search = newFilters.search.trim();
    }

    router.replace({ pathname: '/admin/review-queue', query: nextQuery }, undefined, { shallow: true });
  }, [router]);

  // Fetch Drafts from Backend
  const loadDrafts = useCallback(async () => {
    setIsLoading(true);
    setErrorMsg(null);
    try {
      const res = await apiClient.getDraftQuestions({
        status: statusFilter,
        subject: subjectFilter !== 'ALL' ? subjectFilter : undefined,
        difficulty: difficultyFilter !== 'ALL' ? difficultyFilter : undefined,
        source: sourceFilter !== 'ALL' ? sourceFilter : undefined,
        search: activeSearch.trim() || undefined,
        page: 1,
        limit: 50,
      });

      if (res && res.items) {
        setDrafts(res.items);
        if (res.counts) {
          setCounts(res.counts);
        }
        // Save to offline backup cache
        try {
          localStorage.setItem(LOCAL_STORAGE_BACKUP_KEY, JSON.stringify(res.items));
        } catch {}

        // If currently selected ID is not in new list, pick the first one
        if (res.items.length > 0) {
          if (!selectedDraftId || !res.items.find((item: DraftQuestion) => item.id === selectedDraftId)) {
            setSelectedDraftId(res.items[0].id);
          }
        } else {
          setSelectedDraftId(null);
        }
      }
    } catch (err: any) {
      console.warn('Backend API request failed; attempting localStorage fallback:', err);
      // Fallback from cache
      try {
        const cached = localStorage.getItem(LOCAL_STORAGE_BACKUP_KEY);
        if (cached) {
          const parsed = JSON.parse(cached);
          setDrafts(parsed);
          if (parsed.length > 0 && !selectedDraftId) {
            setSelectedDraftId(parsed[0].id);
          }
        } else {
          setErrorMsg(isBn ? 'সার্ভারের সাথে সংযোগ স্থাপন করা সম্ভব হয়নি। অনুগ্রহ করে ইন্টারনেট সংযোগ পরীক্ষা করুন।' : 'Failed to connect to backend server. Please verify your network.');
        }
      } catch {
        setErrorMsg(isBn ? 'ডেটা লোড করতে ব্যর্থ হয়েছে।' : 'Failed to load question draft data.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [statusFilter, subjectFilter, difficultyFilter, sourceFilter, activeSearch, selectedDraftId, isBn]);

  useEffect(() => {
    loadDrafts();
  }, [loadDrafts]);

  // Currently Selected Draft
  const selectedDraft = useMemo(() => {
    return drafts.find((d) => d.id === selectedDraftId) || null;
  }, [drafts, selectedDraftId]);

  // Reset Edit Form when Selected Draft Changes
  useEffect(() => {
    if (selectedDraft) {
      setEditForm({
        stem_bn: selectedDraft.stem_bn || '',
        options: selectedDraft.options ? JSON.parse(JSON.stringify(selectedDraft.options)) : [],
        explanation_bn: selectedDraft.explanation_bn || '',
        difficulty: selectedDraft.difficulty || 'MEDIUM',
        cognitive_skill: selectedDraft.cognitive_skill || 'APPLICATION',
      });
      setIsEditing(false);
    }
  }, [selectedDraft]);

  // Approve Action Handler
  const handleApprove = async (questionId: string) => {
    if (!questionId || isSubmitting) return;
    setIsSubmitting(true);

    // Optimistic Update
    const prevDrafts = [...drafts];
    setDrafts((prev) =>
      prev.map((d) => (d.id === questionId ? { ...d, status: 'APPROVED' as const, reviewed_by: user?.fullName || 'SME Reviewer' } : d))
    );

    try {
      await apiClient.approveDraftQuestion(questionId, 'বিষয় বিশেষজ্ঞ প্যানেল কর্তৃক পরীক্ষিত ও অনুমোদিত।');
      showToast(isBn ? 'প্রশ্নটি সফলভাবে অনুমোদিত হয়েছে এবং সক্রিয় পরীক্ষা পুলে যুক্ত হয়েছে।' : 'Question approved successfully and added to active exam pool.', 'success');
      loadDrafts();
    } catch (err: any) {
      // Rollback
      setDrafts(prevDrafts);
      showToast((isBn ? 'অনুমোদন ব্যর্থ হয়েছে: ' : 'Approval failed: ') + (err.message || (isBn ? 'অপ্রত্যাশিত ত্রুটি' : 'Unexpected error')), 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Reject Action Handler
  const handleConfirmReject = async () => {
    if (!rejectTargetId || !rejectionReason.trim() || isSubmitting) return;
    setIsSubmitting(true);

    const prevDrafts = [...drafts];
    const targetId = rejectTargetId;
    const reason = rejectionReason.trim();

    // Optimistic Update
    setDrafts((prev) =>
      prev.map((d) => (d.id === targetId ? { ...d, status: 'REJECTED' as const, rejection_feedback: reason } : d))
    );

    try {
      await apiClient.rejectDraftQuestion(targetId, reason, 'REJECT');
      showToast(isBn ? 'প্রশ্নটি সংশোধন ফিডব্যাকসহ প্রত্যাখ্যাত হয়েছে।' : 'Question rejected with revision feedback.', 'success');
      setRejectModalOpen(false);
      setRejectionReason('');
      setRejectTargetId(null);
      loadDrafts();
    } catch (err: any) {
      setDrafts(prevDrafts);
      showToast((isBn ? 'প্রত্যাখ্যান ব্যর্থ হয়েছে: ' : 'Rejection failed: ') + (err.message || (isBn ? 'অপ্রত্যাশিত ত্রুটি' : 'Unexpected error')), 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Inline Edit and Approve Handler
  const handleSaveAndApproveEdit = async () => {
    if (!selectedDraftId || isSubmitting) return;
    setIsSubmitting(true);

    const prevDrafts = [...drafts];

    try {
      await apiClient.editAndApproveDraftQuestion(selectedDraftId, {
        stem_bn: editForm.stem_bn,
        options: editForm.options,
        explanation_bn: editForm.explanation_bn,
        difficulty: editForm.difficulty,
        cognitive_skill: editForm.cognitive_skill,
        comments: 'বিষয় বিশেষজ্ঞ কর্তৃক ইনলাইন পরিমার্জন ও অনুমোদন সম্পন্ন।',
      });
      showToast(isBn ? 'প্রশ্নটি সম্পাদিত ও অনুমোদিত হয়ে সক্রিয় পরীক্ষা পুলে যুক্ত হয়েছে।' : 'Question edited and approved for examination pool.', 'success');
      setIsEditing(false);
      loadDrafts();
    } catch (err: any) {
      setDrafts(prevDrafts);
      showToast((isBn ? 'সম্পাদনা ও অনুমোদন ব্যর্থ হয়েছে: ' : 'Edit and approval failed: ') + (err.message || (isBn ? 'অপ্রত্যাশিত ত্রুটি' : 'Unexpected error')), 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Bulk Actions
  const handleBulkAction = async (action: 'APPROVE' | 'REJECT') => {
    if (selectedIds.size === 0 || isSubmitting) return;
    const ids = Array.from(selectedIds);
    setIsSubmitting(true);

    try {
      await apiClient.bulkActionDraftQuestions(
        ids,
        action,
        action === 'APPROVE' ? 'ব্যাচ প্যানেল অনুমোদন সম্পন্ন।' : 'ব্যাচ প্রত্যাখ্যান সম্পন্ন।'
      );
      showToast(`${toBengaliDigits(ids.length)}টি প্রশ্ন সফলভাবে ${action === 'APPROVE' ? 'অনুমোদিত' : 'প্রত্যাখ্যাত'} হয়েছে।`, 'success');
      setSelectedIds(new Set());
      loadDrafts();
    } catch (err: any) {
      showToast('বাল্ক অ্যাকশন ব্যর্থ হয়েছে: ' + (err.message || 'ত্রুটি'), 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Select / Deselect All
  const toggleSelectAll = () => {
    if (selectedIds.size === drafts.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(drafts.map((d) => d.id)));
    }
  };

  const toggleSelectOne = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  // Fast Review Keyboard Shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ignore if user is currently typing in an input or textarea or modal is open
      const tag = (e.target as HTMLElement)?.tagName?.toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select' || rejectModalOpen || isEditing) {
        return;
      }

      if (e.key === 'a' || e.key === 'A') {
        e.preventDefault();
        if (selectedDraftId) {
          handleApprove(selectedDraftId);
        }
      } else if (e.key === 'r' || e.key === 'R') {
        e.preventDefault();
        if (selectedDraftId) {
          setRejectTargetId(selectedDraftId);
          setRejectModalOpen(true);
        }
      } else if (e.key === 'e' || e.key === 'E') {
        e.preventDefault();
        if (selectedDraft) {
          setIsEditing((prev) => !prev);
        }
      } else if (e.key === 'j' || e.key === 'ArrowDown') {
        e.preventDefault();
        if (drafts.length > 0) {
          const currentIndex = drafts.findIndex((d) => d.id === selectedDraftId);
          if (currentIndex < drafts.length - 1) {
            setSelectedDraftId(drafts[currentIndex + 1].id);
          }
        }
      } else if (e.key === 'k' || e.key === 'ArrowUp') {
        e.preventDefault();
        if (drafts.length > 0) {
          const currentIndex = drafts.findIndex((d) => d.id === selectedDraftId);
          if (currentIndex > 0) {
            setSelectedDraftId(drafts[currentIndex - 1].id);
          }
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectedDraftId, drafts, rejectModalOpen, isEditing, handleApprove]);

  return (
    <div className="min-h-screen bg-[var(--bg-canvas)] text-[var(--text-main)] font-sans antialiased">
      <Head>
        <title>{pageTitle}</title>
        <meta
          name="description"
          content={
            isBn
              ? "এনসিটিবি কারিকুলাম সমন্বিত এআই প্রশ্ন ব্যাংক ও হিউম্যান-ইন-দ্য-লুপ রিভিউ কিউ"
              : "NCTB curriculum-aligned AI question bank and human-in-the-loop review queue."
          }
        />
      </Head>

      {/* Global Toast Alert */}
      {toast && (
        <div
          role="alert"
          className={`fixed top-4 right-4 z-50 flex items-center gap-3 px-4 py-3 rounded-xl border shadow-lg text-sm font-medium transition-all animate-in fade-in slide-in-from-top-2 ${
            toast.type === 'success'
              ? 'bg-emerald-50 dark:bg-emerald-950/80 border-emerald-300 dark:border-emerald-800 text-emerald-800 dark:text-emerald-200'
              : 'bg-rose-50 dark:bg-rose-950/80 border-rose-300 dark:border-rose-800 text-rose-800 dark:text-rose-200'
          }`}
        >
          {toast.type === 'success' ? (
            <CheckCircle2 className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0" strokeWidth={2} />
          ) : (
            <AlertTriangle className="w-5 h-5 text-rose-600 dark:text-rose-400 shrink-0" strokeWidth={2} />
          )}
          <span>{toast.message}</span>
        </div>
      )}

      {/* Top Header & Breadcrumb */}
      <header className="border-b border-[var(--border-hairline)] bg-[var(--bg-card)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              {/* Breadcrumb */}
              <nav aria-label="Breadcrumb" className="flex items-center gap-2 text-xs text-[var(--text-muted)] mb-2">
                <Link href="/" className="hover:text-[var(--text-main)] transition-colors">
                  {isBn ? "হোম" : "Home"}
                </Link>
                <span>/</span>
                <Link href="/admin" className="hover:text-[var(--text-main)] transition-colors">
                  {isBn ? "অ্যাডমিন" : "Admin"}
                </Link>
                <span>/</span>
                <span className="text-[var(--text-main)] font-semibold">
                  {isBn ? "এআই ড্রাফট রিভিউ কিউ" : "AI Draft Review Queue"}
                </span>
              </nav>

              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center shrink-0">
                  <Sparkles className="w-5 h-5" strokeWidth={2} />
                </div>
                <div>
                  <h1 className="text-2xl font-serif font-bold text-[var(--text-main)] tracking-tight">
                    {isBn ? "এআই প্রশ্ন ব্যাংক ও ড্রাফট পাইপলাইন" : "AI Question Bank & Draft Pipeline"}
                  </h1>
                  <p className="text-xs text-[var(--text-muted)] mt-0.5">
                    {isBn
                      ? "এনসিটিবি কারিকুলাম মানদণ্ড অনুযায়ী এআই-ড্রাফট মূল্যায়ন, বিষয়বস্তু সংশোধন ও মানব পর্যালোচক অনুমোদন গেটওয়ে"
                      : "NCTB curriculum-aligned AI draft evaluation, content remediation, and human-in-the-loop expert approval gateway."}
                  </p>
                </div>
              </div>
            </div>

            {/* Quick Actions & Navigation */}
            <div className="flex items-center gap-3 shrink-0">
              <Link
                href="/admin/quarantine"
                className="inline-flex items-center gap-2 h-10 px-4 rounded-xl text-xs font-semibold border border-[var(--border-subtle)] bg-[var(--bg-canvas)] hover:bg-[var(--bg-card)] text-[var(--text-main)] transition-all"
              >
                <AlertTriangle className="w-4 h-4 text-rose-500" strokeWidth={1.75} />
                <span>{isBn ? "কোয়ারেন্টিন কনসোল" : "Quarantine Console"}</span>
              </Link>

              <Link
                href="/admin"
                className="inline-flex items-center gap-2 h-10 px-4 rounded-xl text-xs font-semibold border border-[var(--border-subtle)] bg-[var(--bg-canvas)] hover:bg-[var(--bg-card)] text-[var(--text-main)] transition-all"
              >
                <Layers className="w-4 h-4 text-cyan-500" strokeWidth={1.75} />
                <span>{isBn ? "অ্যাডমিন হাব" : "Admin Hub"}</span>
              </Link>

              <ThemeToggle />
            </div>
          </div>

          {/* Status Counter Tabs */}
          <div className="flex items-center gap-2 overflow-x-auto pt-6 border-t border-[var(--border-hairline)] mt-5 pb-1">
            {[
              { key: 'NEEDS_REVIEW', label: isBn ? 'রিভিউ আবশ্যক' : 'Needs Review', count: counts.needs_review, color: 'text-amber-600 dark:text-amber-400' },
              { key: 'ALL', label: isBn ? 'সকল ড্রাফট' : 'All Drafts', count: counts.all, color: 'text-slate-600 dark:text-slate-300' },
              { key: 'DRAFT', label: isBn ? 'ড্রাফট স্টোর' : 'Draft Store', count: counts.draft, color: 'text-blue-600 dark:text-blue-400' },
              { key: 'APPROVED', label: isBn ? 'অনুমোদিত ও সক্রিয়' : 'Approved & Active', count: counts.approved, color: 'text-emerald-600 dark:text-emerald-400' },
              { key: 'REJECTED', label: isBn ? 'প্রত্যাখ্যাত' : 'Rejected', count: counts.rejected, color: 'text-rose-600 dark:text-rose-400' },
              { key: 'NEEDS_CHANGES', label: isBn ? 'সংশোধন আবশ্যক' : 'Needs Changes', count: counts.needs_changes, color: 'text-orange-600 dark:text-orange-400' },
            ].map((tab) => {
              const isActive = statusFilter.toUpperCase() === tab.key;
              return (
                <button
                  key={tab.key}
                  type="button"
                  onClick={() => {
                    setStatusFilter(tab.key);
                    syncUrlParams({ status: tab.key });
                  }}
                  className={`inline-flex items-center gap-2 h-9 px-4 rounded-xl text-xs font-bold whitespace-nowrap transition-all border cursor-pointer ${
                    isActive
                      ? 'bg-[var(--bg-canvas)] border-[var(--color-primary)] text-[var(--text-main)] shadow-xs'
                      : 'border-transparent text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-canvas)]'
                  }`}
                >
                  <span>{tab.label}</span>
                  <span className={`px-2 py-0.5 rounded-full text-[11px] font-mono bg-slate-100 dark:bg-slate-800 ${tab.color}`}>
                    {isBn ? toBengaliDigits(tab.count) : tab.count}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </header>

      {/* Main Review Workplace */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Filter & Search Bar */}
        <div className="bg-[var(--bg-card)] p-4 rounded-2xl border border-[var(--border-hairline)] mb-6 shadow-xs">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
            {/* Search Input */}
            <div className="md:col-span-5 relative">
              <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-[var(--text-muted)]" strokeWidth={1.75} />
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    setActiveSearch(searchInput);
                    syncUrlParams({ search: searchInput });
                  }
                }}
                placeholder={isBn ? 'প্রশ্ন, টপিক বা আইডি খুঁজুন...' : 'Search question, topic, or ID...'}
                className="w-full h-10 pl-10 pr-16 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-sm text-[var(--text-main)] placeholder-[var(--text-muted)] focus:outline-hidden focus:border-[var(--color-primary)]"
              />
              {searchInput && (
                <button
                  type="button"
                  onClick={() => {
                    setSearchInput('');
                    setActiveSearch('');
                    syncUrlParams({ search: '' });
                  }}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-[var(--text-muted)] hover:text-[var(--text-main)] cursor-pointer"
                >
                  {isBn ? 'মুছুন' : 'Clear'}
                </button>
              )}
            </div>

            {/* Subject Dropdown */}
            <div className="md:col-span-3">
              <select
                value={subjectFilter}
                onChange={(e) => {
                  setSubjectFilter(e.target.value);
                  syncUrlParams({ subject: e.target.value });
                }}
                className="w-full h-10 px-3 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-xs font-medium text-[var(--text-main)] focus:outline-hidden focus:border-[var(--color-primary)] cursor-pointer"
              >
                {SUBJECT_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {isBn ? opt.labelBn : opt.labelEn}
                  </option>
                ))}
              </select>
            </div>

            {/* Difficulty Dropdown */}
            <div className="md:col-span-2">
              <select
                value={difficultyFilter}
                onChange={(e) => {
                  setDifficultyFilter(e.target.value);
                  syncUrlParams({ difficulty: e.target.value });
                }}
                className="w-full h-10 px-3 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-xs font-medium text-[var(--text-main)] focus:outline-hidden focus:border-[var(--color-primary)] cursor-pointer"
              >
                {DIFFICULTY_OPTIONS.map((opt) => (
                  <option key={opt.value} value={opt.value}>
                    {isBn ? opt.labelBn : opt.labelEn}
                  </option>
                ))}
              </select>
            </div>

            {/* Action buttons */}
            <div className="md:col-span-2 flex items-center gap-2 justify-end">
              <button
                type="button"
                onClick={() => {
                  setActiveSearch(searchInput);
                  syncUrlParams({ search: searchInput });
                }}
                className="h-10 px-4 rounded-xl text-xs font-bold bg-cyan-600 hover:bg-cyan-500 text-white shadow-xs transition-colors cursor-pointer"
              >
                {isBn ? 'অনুসন্ধান' : 'Search'}
              </button>
              <button
                type="button"
                onClick={loadDrafts}
                title={isBn ? 'রিফ্রেশ করুন' : 'Refresh'}
                className="h-10 w-10 flex items-center justify-center rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-[var(--text-main)] hover:bg-[var(--bg-card)] transition-colors cursor-pointer"
              >
                <RotateCcw className={`w-4 h-4 ${isLoading ? 'animate-spin text-cyan-500' : ''}`} strokeWidth={1.75} />
              </button>
            </div>
          </div>

          {/* Keyboard Shortcuts Hint Bar */}
          <div className="mt-3 pt-3 border-t border-[var(--border-hairline)] flex flex-wrap items-center justify-between text-[11px] text-[var(--text-muted)]">
            <div className="flex items-center gap-4">
              <span className="font-semibold text-[var(--text-main)]">
                {isBn ? 'দ্রুত কিবোর্ড শর্টকাট:' : 'Keyboard Shortcuts:'}
              </span>
              <span><kbd className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 font-mono text-[10px]">A</kbd> {isBn ? 'অনুমোদন' : 'Approve'}</span>
              <span><kbd className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 font-mono text-[10px]">R</kbd> {isBn ? 'প্রত্যাখ্যান' : 'Reject'}</span>
              <span><kbd className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 font-mono text-[10px]">E</kbd> {isBn ? 'সম্পাদনা' : 'Edit'}</span>
              <span><kbd className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 font-mono text-[10px]">J</kbd> / <kbd className="px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 font-mono text-[10px]">K</kbd> {isBn ? 'পরবর্তী/পূর্ববর্তী' : 'Next/Prev'}</span>
            </div>
            <span className="text-[10px] uppercase font-mono tracking-wider">Zero-Unreviewed Policy Active</span>
          </div>
        </div>

        {/* Bulk Action Bar (Visible when items selected) */}
        {selectedIds.size > 0 && (
          <div className="mb-4 p-3 bg-cyan-500/10 border border-cyan-500/30 rounded-xl flex items-center justify-between animate-in fade-in">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-cyan-600 dark:text-cyan-400" strokeWidth={2} />
              <span className="text-xs font-bold text-cyan-900 dark:text-cyan-100">
                {isBn ? `${toBengaliDigits(selectedIds.size)}টি প্রশ্ন নির্বাচিত হয়েছে` : `${selectedIds.size} Questions Selected`}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => handleBulkAction('APPROVE')}
                disabled={isSubmitting}
                className="h-8 px-3 rounded-lg text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors cursor-pointer"
              >
                {isBn ? 'নির্বাচিত অনুমোদন করুন' : 'Approve Selected'}
              </button>
              <button
                type="button"
                onClick={() => handleBulkAction('REJECT')}
                disabled={isSubmitting}
                className="h-8 px-3 rounded-lg text-xs font-bold bg-rose-600 hover:bg-rose-500 text-white transition-colors cursor-pointer"
              >
                {isBn ? 'নির্বাচিত প্রত্যাখ্যান করুন' : 'Reject Selected'}
              </button>
              <button
                type="button"
                onClick={() => setSelectedIds(new Set())}
                className="h-8 px-2.5 rounded-lg text-xs text-[var(--text-muted)] hover:text-[var(--text-main)] cursor-pointer"
              >
                {isBn ? 'বাতিল' : 'Cancel'}
              </button>
            </div>
          </div>
        )}

        {/* Error Banner */}
        {errorMsg && (
          <div className="mb-6 p-4 rounded-xl border border-rose-300 bg-rose-50 dark:bg-rose-950/40 text-rose-800 dark:text-rose-200 text-sm flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0" strokeWidth={1.75} />
              <span>{errorMsg}</span>
            </div>
            <button
              type="button"
              onClick={loadDrafts}
              className="text-xs font-bold underline hover:no-underline cursor-pointer"
            >
              {isBn ? 'পুনরায় চেষ্টা করুন' : 'Retry'}
            </button>
          </div>
        )}

        {/* Master-Detail Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* Left Column: Draft Queue List (5 columns) */}
          <div className="lg:col-span-5 bg-[var(--bg-card)] rounded-2xl border border-[var(--border-hairline)] overflow-hidden shadow-xs">
            {/* Queue List Header */}
            <div className="px-4 py-3 border-b border-[var(--border-hairline)] bg-[var(--bg-canvas)]/50 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={drafts.length > 0 && selectedIds.size === drafts.length}
                  onChange={toggleSelectAll}
                  className="rounded border-[var(--border-subtle)] text-cyan-600 focus:ring-0 cursor-pointer"
                  title={isBn ? 'সব নির্বাচন করুন' : 'Select All'}
                />
                <span className="text-xs font-bold text-[var(--text-main)]">
                  {isBn ? `ড্রাফট তালিকা (${toBengaliDigits(drafts.length)}টি)` : `Draft List (${drafts.length})`}
                </span>
              </div>
              <span className="text-[11px] text-[var(--text-muted)]">
                {isBn ? 'ক্লিক করে বিস্তারিত দেখুন' : 'Click to inspect details'}
              </span>
            </div>

            {/* Queue Items */}
            <div className="divide-y divide-[var(--border-hairline)] max-h-[720px] overflow-y-auto">
              {isLoading ? (
                // Loading Skeleton
                <div className="p-4 space-y-3">
                  {[1, 2, 3, 4].map((n) => (
                    <div key={n} className="p-4 rounded-xl bg-slate-100 dark:bg-slate-800/50 animate-pulse space-y-2">
                      <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/3" />
                      <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-full" />
                      <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded w-1/2" />
                    </div>
                  ))}
                </div>
              ) : drafts.length === 0 ? (
                // Empty State
                <div className="p-12 text-center">
                  <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-800 text-[var(--text-muted)] flex items-center justify-center mx-auto mb-3">
                    <CheckCircle2 className="w-6 h-6" strokeWidth={1.5} />
                  </div>
                  <h3 className="text-sm font-bold text-[var(--text-main)]">
                    {isBn ? 'কোনো ড্রাফট প্রশ্ন মেলেনি' : 'No draft questions found'}
                  </h3>
                  <p className="text-xs text-[var(--text-muted)] mt-1 max-w-xs mx-auto">
                    {isBn
                      ? 'বর্তমান ফিল্টারে পর্যালোচনার জন্য কোনো প্রশ্ন অবশিষ্ট নেই। অন্য ফিল্টার বেছে নিন।'
                      : 'No questions match the current filters. Try selecting another filter.'}
                  </p>
                </div>
              ) : (
                drafts.map((d) => {
                  const isSelected = d.id === selectedDraftId;
                  const isChecked = selectedIds.has(d.id);

                  return (
                    <div
                      key={d.id}
                      data-testid={`draft-card-${d.id}`}
                      onClick={() => setSelectedDraftId(d.id)}
                      className={`p-4 transition-all cursor-pointer select-none ${
                        isSelected
                          ? 'bg-cyan-50/60 dark:bg-cyan-950/20 border-l-4 border-l-cyan-600'
                          : 'hover:bg-slate-50 dark:hover:bg-slate-800/40'
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onClick={(e) => toggleSelectOne(d.id, e)}
                          onChange={() => {}}
                          className="mt-1 rounded border-[var(--border-subtle)] text-cyan-600 focus:ring-0 cursor-pointer"
                        />

                        <div className="flex-1 min-w-0">
                          {/* Top Meta Line */}
                          <div className="flex items-center justify-between gap-2 mb-1.5">
                            <span className="text-[11px] font-mono text-[var(--text-muted)] font-semibold">
                              {d.id}
                            </span>
                            <span
                              className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                                d.status === 'NEEDS_REVIEW'
                                  ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20'
                                  : d.status === 'APPROVED'
                                  ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20'
                                  : d.status === 'REJECTED'
                                  ? 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20'
                                  : d.status === 'NEEDS_CHANGES'
                                  ? 'bg-orange-500/10 text-orange-600 dark:text-orange-400 border-orange-500/20'
                                  : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300 border-slate-200'
                              }`}
                            >
                              {d.status === 'NEEDS_REVIEW'
                                ? (isBn ? 'রিভিউ আবশ্যক' : 'Needs Review')
                                : d.status === 'APPROVED'
                                ? (isBn ? 'অনুমোদিত' : 'Approved')
                                : d.status === 'REJECTED'
                                ? (isBn ? 'প্রত্যাখ্যাত' : 'Rejected')
                                : d.status === 'NEEDS_CHANGES'
                                ? (isBn ? 'সংশোধন আবশ্যক' : 'Needs Changes')
                                : (isBn ? 'ড্রাফট' : 'Draft')}
                            </span>
                          </div>

                          {/* Stem Snippet */}
                          <h4 className="text-xs font-semibold text-[var(--text-main)] line-clamp-2 leading-relaxed">
                            {d.stem_en && !isBn ? d.stem_en : d.stem_bn}
                          </h4>

                          {/* Subject & Confidence Badges */}
                          <div className="flex items-center gap-2 mt-2 flex-wrap">
                            <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-[var(--text-muted)]">
                              {d.subject}
                            </span>
                            <span className="text-[10px] font-medium px-1.5 py-0.5 rounded bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400">
                              {d.difficulty}
                            </span>
                            {d.ai_confidence_score && (
                              <span className="text-[10px] font-mono text-purple-600 dark:text-purple-400">
                                {Math.round(d.ai_confidence_score * 100)}% {isBn ? 'এআই স্কোর' : 'AI Score'}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          {/* Right Column: Detailed Inspector & Action Console (7 columns) */}
          <div className="lg:col-span-7 bg-[var(--bg-card)] rounded-2xl border border-[var(--border-hairline)] overflow-hidden shadow-xs">
            {selectedDraft ? (
              <div>
                {/* Inspector Top Bar */}
                <div className="px-6 py-4 border-b border-[var(--border-hairline)] bg-[var(--bg-canvas)]/50 flex flex-wrap items-center justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono font-bold text-cyan-600 dark:text-cyan-400">
                        {selectedDraft.id}
                      </span>
                      <span className="text-xs text-[var(--text-muted)] font-mono">
                        (v{toBengaliDigits(selectedDraft.version)})
                      </span>
                      <span className="text-xs text-[var(--text-muted)]">|</span>
                      <span className="text-xs font-medium text-[var(--text-main)]">
                        {selectedDraft.subject} &bull; {selectedDraft.topic}
                      </span>
                    </div>
                    {selectedDraft.concept && (
                      <p className="text-[11px] text-[var(--text-muted)] mt-0.5">
                        বিষয়বস্তু ধারণা: {selectedDraft.concept}
                      </p>
                    )}
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => setIsEditing((prev) => !prev)}
                      className={`inline-flex items-center gap-1.5 h-8 px-3 rounded-lg text-xs font-semibold border transition-all cursor-pointer ${
                        isEditing
                          ? 'bg-amber-500/10 border-amber-500/40 text-amber-700 dark:text-amber-300'
                          : 'border-[var(--border-subtle)] bg-[var(--bg-canvas)] hover:bg-[var(--bg-card)] text-[var(--text-main)]'
                      }`}
                    >
                      <Edit3 className="w-3.5 h-3.5" strokeWidth={1.75} />
                      <span>{isEditing ? (isBn ? 'সম্পাদনা বাতিল' : 'Cancel Edit') : (isBn ? 'ইনলাইন সম্পাদনা' : 'Inline Edit')}</span>
                    </button>
                  </div>
                </div>

                {/* Inspector Body */}
                <div className="p-6 space-y-6">
                  {isEditing ? (
                    // ================= INLINE EDITING FORM =================
                    <div className="space-y-4">
                      <div>
                        <label className="block text-xs font-bold text-[var(--text-main)] mb-1">
                          {isBn ? 'প্রশ্নের মূল বক্তব্য (Stem):' : 'Question Stem:'}
                        </label>
                        <textarea
                          rows={3}
                          value={editForm.stem_bn}
                          onChange={(e) => setEditForm({ ...editForm, stem_bn: e.target.value })}
                          className="w-full p-3 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-sm text-[var(--text-main)] focus:outline-hidden focus:border-[var(--color-primary)] font-serif"
                        />
                      </div>

                      {/* Options Editing */}
                      <div>
                        <label className="block text-xs font-bold text-[var(--text-main)] mb-2">
                          {isBn ? 'বিকল্প উত্তরসমূহ (সঠিক উত্তর চিহ্নিত করুন):' : 'Answer Options (Select correct option):'}
                        </label>
                        <div className="space-y-2">
                          {editForm.options.map((opt, idx) => (
                            <div key={opt.option_key} className="flex items-center gap-2">
                              <input
                                type="radio"
                                name="correct_option"
                                checked={opt.is_correct}
                                onChange={() => {
                                  setEditForm({
                                    ...editForm,
                                    options: editForm.options.map((o, i) => ({
                                      ...o,
                                      is_correct: i === idx,
                                    })),
                                  });
                                }}
                                className="text-emerald-600 focus:ring-0 cursor-pointer"
                                title={isBn ? "সঠিক উত্তর হিসেবে নির্বাচন করুন" : "Select as correct answer"}
                              />
                              <span className="w-6 text-xs font-mono font-bold text-[var(--text-main)]">
                                {opt.option_key}.
                              </span>
                              <input
                                type="text"
                                value={opt.option_text_bn}
                                onChange={(e) => {
                                  const nextOptions = [...editForm.options];
                                  nextOptions[idx].option_text_bn = e.target.value;
                                  setEditForm({ ...editForm, options: nextOptions });
                                }}
                                className="flex-1 h-9 px-3 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-xs text-[var(--text-main)]"
                              />
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Explanation Editing */}
                      <div>
                        <label className="block text-xs font-bold text-[var(--text-main)] mb-1">
                          {isBn ? 'বিশদ ব্যাখ্যা (Explanation):' : 'Pedagogical Explanation:'}
                        </label>
                        <textarea
                          rows={3}
                          value={editForm.explanation_bn}
                          onChange={(e) => setEditForm({ ...editForm, explanation_bn: e.target.value })}
                          className="w-full p-3 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-xs text-[var(--text-main)] focus:outline-hidden focus:border-[var(--color-primary)] font-serif"
                        />
                      </div>

                      {/* Form Actions */}
                      <div className="flex items-center justify-end gap-2 pt-3 border-t border-[var(--border-hairline)]">
                        <button
                          type="button"
                          onClick={() => setIsEditing(false)}
                          className="h-9 px-4 rounded-xl text-xs font-semibold border border-[var(--border-subtle)] hover:bg-[var(--bg-canvas)] cursor-pointer"
                        >
                          {isBn ? 'বাতিল' : 'Cancel'}
                        </button>
                        <button
                          type="button"
                          onClick={handleSaveAndApproveEdit}
                          disabled={isSubmitting}
                          className="inline-flex items-center gap-1.5 h-9 px-4 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white transition-colors cursor-pointer"
                        >
                          <Save className="w-3.5 h-3.5" strokeWidth={2} />
                          <span>{isBn ? 'সংরক্ষণ ও অনুমোদন করুন' : 'Save & Approve'}</span>
                        </button>
                      </div>
                    </div>
                  ) : (
                    // ================= READ-ONLY INSPECTOR VIEW =================
                    <>
                      {/* Question Stem */}
                      <div>
                        <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--text-muted)] block mb-1">
                          {isBn ? 'প্রশ্নের বিবরণ (Stem)' : 'Question Stem'}
                        </span>
                        <div className="p-4 rounded-xl bg-[var(--bg-canvas)] border border-[var(--border-hairline)]">
                          <p className="text-base font-serif text-[var(--text-main)] leading-relaxed">
                            {selectedDraft.stem_bn}
                          </p>
                          {selectedDraft.stem_en && (
                            <p className="text-xs text-[var(--text-muted)] italic mt-2 border-t border-[var(--border-hairline)] pt-2 font-sans">
                              {selectedDraft.stem_en}
                            </p>
                          )}
                        </div>
                      </div>

                      {/* Options Grid */}
                      <div>
                        <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--text-muted)] block mb-2">
                          {isBn ? 'বিকল্প উত্তর ও বিভ্রান্তিকারী যুক্তি (Distractor Rationale)' : 'Options & Distractor Rationale'}
                        </span>
                        <div className="space-y-2.5">
                          {selectedDraft.options?.map((opt) => (
                            <div
                              key={opt.option_key}
                              className={`p-3.5 rounded-xl border transition-all ${
                                opt.is_correct
                                  ? 'bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-500/40 text-emerald-950 dark:text-emerald-100'
                                  : 'bg-[var(--bg-canvas)] border-[var(--border-hairline)] text-[var(--text-main)]'
                              }`}
                            >
                              <div className="flex items-start justify-between gap-2">
                                <div className="flex items-center gap-2.5">
                                  <span
                                    className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold font-mono ${
                                      opt.is_correct
                                        ? 'bg-emerald-600 text-white'
                                        : 'bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300'
                                    }`}
                                  >
                                    {opt.option_key}
                                  </span>
                                  <span className="text-sm font-semibold">{opt.option_text_bn}</span>
                                </div>
                                {opt.is_correct && (
                                  <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600 dark:text-emerald-400">
                                    <CheckCircle2 className="w-3.5 h-3.5" strokeWidth={2} />
                                    <span>{isBn ? 'সঠিক উত্তর' : 'Correct Answer'}</span>
                                  </span>
                                )}
                              </div>
                              {opt.distractor_rationale && (
                                <p className="text-xs text-[var(--text-muted)] mt-2 pl-8 leading-relaxed">
                                  {opt.distractor_rationale}
                                </p>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Explanation Block */}
                      {selectedDraft.explanation_bn && (
                        <div>
                          <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--text-muted)] block mb-1">
                            {isBn ? 'শিক্ষামূলক সমাধান ও ব্যাখ্যা (Pedagogical Explanation)' : 'Pedagogical Explanation & Solution'}
                          </span>
                          <div className="p-4 rounded-xl bg-[var(--bg-canvas)] border border-[var(--border-hairline)] text-xs text-[var(--text-main)] font-serif leading-relaxed">
                            {selectedDraft.explanation_bn}
                          </div>
                        </div>
                      )}

                      {/* AI Quality & Deduplication Metadata */}
                      <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-900/40 border border-[var(--border-subtle)]">
                        <div className="flex items-center gap-2 mb-3">
                          <Sparkles className="w-4 h-4 text-purple-500" strokeWidth={1.75} />
                          <span className="text-xs font-bold text-[var(--text-main)]">
                            {isBn ? 'এআই অডিট ও কোয়ালিটি স্কোরবোর্ড' : 'AI Quality & Audit Scoreboard'}
                          </span>
                        </div>
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                          <div>
                            <span className="text-[10px] text-[var(--text-muted)] block">{isBn ? 'জেনারেটিভ মডেল' : 'Generative Model'}</span>
                            <span className="font-mono font-medium">{selectedDraft.ai_model || 'Claude-3.5-Sonnet'}</span>
                          </div>
                          <div>
                            <span className="text-[10px] text-[var(--text-muted)] block">{isBn ? 'ব্লুমস ট্যাক্সোনমি স্তর' : 'Bloom Taxonomy Level'}</span>
                            <span className="font-medium text-indigo-600 dark:text-indigo-400">
                              {selectedDraft.cognitive_skill}
                            </span>
                          </div>
                          <div>
                            <span className="text-[10px] text-[var(--text-muted)] block">{isBn ? 'ডুপ্লিকেশন সাদৃশ্য' : 'Duplication Similarity'}</span>
                            <span className="font-mono text-emerald-600 dark:text-emerald-400">
                              {selectedDraft.deduplication_similarity} {isBn ? '(ইউনিক)' : '(Unique)'}
                            </span>
                          </div>
                          <div>
                            <span className="text-[10px] text-[var(--text-muted)] block">{isBn ? 'নির্ভুলতা স্কোর' : 'Confidence Score'}</span>
                            <span className="font-mono font-bold text-purple-600 dark:text-purple-400">
                              {Math.round((selectedDraft.ai_confidence_score || 0.94) * 100)}%
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Rejection Feedback Banner if Rejected */}
                      {selectedDraft.rejection_feedback && (
                        <div className="p-4 rounded-xl border border-rose-300 dark:border-rose-800 bg-rose-50/60 dark:bg-rose-950/20 text-xs">
                          <span className="font-bold text-rose-700 dark:text-rose-400 block mb-1">
                            {isBn ? 'প্রত্যাখ্যানের কারণ ও পর্যালোচক মন্তব্য:' : 'Rejection Reason & Reviewer Feedback:'}
                          </span>
                          <p className="text-[var(--text-main)]">{selectedDraft.rejection_feedback}</p>
                        </div>
                      )}
                    </>
                  )}
                </div>

                {/* Bottom Decision Action Bar */}
                <div className="px-6 py-4 border-t border-[var(--border-hairline)] bg-[var(--bg-canvas)] flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-2">
                    {/* Navigation shortcuts */}
                    <button
                      type="button"
                      onClick={() => {
                        const idx = drafts.findIndex((d) => d.id === selectedDraftId);
                        if (idx > 0) setSelectedDraftId(drafts[idx - 1].id);
                      }}
                      className="inline-flex items-center gap-1 h-9 px-3 rounded-xl text-xs font-semibold border border-[var(--border-subtle)] bg-[var(--bg-card)] hover:bg-[var(--bg-canvas)] transition-colors cursor-pointer"
                    >
                      <ChevronLeft className="w-4 h-4" />
                      <span>{isBn ? 'পূর্ববর্তী (K)' : 'Previous (K)'}</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        const idx = drafts.findIndex((d) => d.id === selectedDraftId);
                        if (idx < drafts.length - 1) setSelectedDraftId(drafts[idx + 1].id);
                      }}
                      className="inline-flex items-center gap-1 h-9 px-3 rounded-xl text-xs font-semibold border border-[var(--border-subtle)] bg-[var(--bg-card)] hover:bg-[var(--bg-canvas)] transition-colors cursor-pointer"
                    >
                      <span>{isBn ? 'পরবর্তী (J)' : 'Next (J)'}</span>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => {
                        setRejectTargetId(selectedDraft.id);
                        setRejectModalOpen(true);
                      }}
                      disabled={isSubmitting}
                      className="inline-flex items-center gap-1.5 h-9 px-4 rounded-xl text-xs font-bold border border-rose-300 dark:border-rose-800 bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-300 hover:bg-rose-100 transition-colors cursor-pointer"
                    >
                      <XCircle className="w-4 h-4" strokeWidth={2} />
                      <span>{isBn ? 'প্রত্যাখ্যান করুন (R)' : 'Reject (R)'}</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => handleApprove(selectedDraft.id)}
                      disabled={isSubmitting}
                      className="inline-flex items-center gap-1.5 h-9 px-5 rounded-xl text-xs font-bold bg-emerald-600 hover:bg-emerald-500 text-white shadow-xs transition-colors cursor-pointer"
                    >
                      <CheckCircle2 className="w-4 h-4" strokeWidth={2} />
                      <span>{isBn ? 'অনুমোদন করুন (A)' : 'Approve (A)'}</span>
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-16 text-center text-[var(--text-muted)]">
                <BookOpen className="w-10 h-10 mx-auto mb-3 opacity-40" strokeWidth={1.5} />
                <h3 className="text-sm font-bold text-[var(--text-main)]">
                  {isBn ? 'কোনো প্রশ্ন নির্বাচিত নেই' : 'No Question Selected'}
                </h3>
                <p className="text-xs mt-1">
                  {isBn ? 'বাম পাশের তালিকা থেকে একটি প্রশ্ন নির্বাচন করুন।' : 'Select a question from the queue list to inspect.'}
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Mandatory Rejection Reason Modal */}
      {rejectModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
          <div className="w-full max-w-lg bg-[var(--bg-card)] rounded-2xl border border-[var(--border-hairline)] shadow-2xl p-6 space-y-4">
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-rose-500/10 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0">
                  <XCircle className="w-5 h-5" strokeWidth={2} />
                </div>
                <div>
                  <h3 className="text-base font-bold text-[var(--text-main)]">
                    {isBn ? 'প্রশ্নটি প্রত্যাখ্যানের কারণ উল্লেখ করুন' : 'Specify Rejection Reason'}
                  </h3>
                  <p className="text-xs text-[var(--text-muted)]">
                    {isBn ? 'অডিটে সংরক্ষণের জন্য সুনির্দিষ্ট কারণ আবশ্যক।' : 'Specific rationale is mandatory for the audit log.'}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setRejectModalOpen(false)}
                className="text-[var(--text-muted)] hover:text-[var(--text-main)] cursor-pointer"
                aria-label={isBn ? "বন্ধ করুন" : "Dismiss"}
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Presets */}
            <div>
              <span className="text-[11px] font-bold text-[var(--text-muted)] block mb-1.5">
                {isBn ? 'সচরাচর ব্যবহৃত কারণসমূহ:' : 'Commonly Used Presets:'}
              </span>
              <div className="flex flex-wrap gap-1.5">
                {(isBn ? REJECTION_PRESETS_BN : REJECTION_PRESETS_EN).map((preset) => (
                  <button
                    key={preset}
                    type="button"
                    onClick={() => setRejectionReason(preset)}
                    className="text-[11px] px-2.5 py-1 rounded-lg border border-[var(--border-subtle)] bg-[var(--bg-canvas)] hover:border-[var(--color-primary)] text-[var(--text-main)] transition-colors cursor-pointer text-left"
                  >
                    {preset}
                  </button>
                ))}
              </div>
            </div>

            {/* Custom Reason Textarea */}
            <div>
              <label className="block text-xs font-semibold text-[var(--text-main)] mb-1">
                {isBn ? 'বিস্তারিত ফিডব্যাক মন্তব্য:' : 'Detailed Feedback Comment:'}
              </label>
              <textarea
                rows={4}
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                placeholder={isBn ? 'কেন প্রশ্নটি বাতিল বা সংশোধন প্রয়োজন তা সংক্ষেপে লিখুন...' : 'Briefly explain why this question is being rejected or needs revision...'}
                className="w-full p-3 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-canvas)] text-xs text-[var(--text-main)] focus:outline-hidden focus:border-rose-500"
              />
            </div>

            {/* Modal Actions */}
            <div className="flex items-center justify-end gap-2 pt-2 border-t border-[var(--border-hairline)]">
              <button
                type="button"
                onClick={() => setRejectModalOpen(false)}
                className="h-9 px-4 rounded-xl text-xs font-semibold border border-[var(--border-subtle)] hover:bg-[var(--bg-canvas)] cursor-pointer"
              >
                {isBn ? 'বাতিল' : 'Cancel'}
              </button>
              <button
                type="button"
                onClick={handleConfirmReject}
                disabled={!rejectionReason.trim() || isSubmitting}
                className="h-9 px-5 rounded-xl text-xs font-bold bg-rose-600 hover:bg-rose-500 text-white disabled:opacity-50 transition-colors cursor-pointer"
              >
                {isBn ? 'প্রত্যাখ্যান নিশ্চিত করুন' : 'Confirm Rejection'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default withAdminAuth(ReviewQueuePageComponent);
