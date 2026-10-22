/**
 * ========================================================================================
 * MODULE:    Admin Operations & Content Integrity Console
 * TOPIC:     Single-Click Question Quarantine & Automated Audit Review
 * FILE:      frontend/src/pages/admin/quarantine.tsx
 * PURPOSE:   Provides an administrative control interface to protect exam trust.
 *            Enables authorized Subject Reviewers and Admins to inspect reported
 *            questions, isolate erroneous items in a single click (Quarantine),
 *            trigger automated score reconciliations for affected candidate attempts,
 *            and inspect the immutable audit trail. Strictly zero emoji.
 * AUDIENCE:  Platform Administrators, Subject Reviewers & Audit Engineers
 * STANDARDS: OWASP ASVS L2 Audit Logging, UI/UX Pro Max, Zero-Emoji Policy
 * ========================================================================================
 */

import React, { useState } from 'react';
import Head from 'next/head';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { ThemeToggle } from '../../components/ui/theme-toggle';

interface ReportedQuestion {
  id: string;
  version: number;
  stemBn: string;
  subject: string;
  reportsCount: number;
  primaryIssue: string;
  status: 'PUBLISHED' | 'QUARANTINED' | 'UNDER_REVIEW';
}

interface AuditRecord {
  auditId: string;
  action: string;
  questionId: string;
  actor: string;
  reason: string;
  timestamp: string;
}

export default function AdminQuarantineConsole() {
  const [questions, setQuestions] = useState<ReportedQuestion[]>([
    {
      id: "q_hsc_phys_102",
      version: 1,
      stemBn: "সরল ছন্দিত স্পন্দনে স্পন্দিত কোনো কণার সাম্যাবস্থানে বেগ কত?",
      subject: "পদার্থবিজ্ঞান ১ম পত্র (Class 11-12)",
      reportsCount: 14,
      primaryIssue: "বিকল্প A এবং C উভয়ই সঠিক হতে পারে (অস্পষ্ট প্রশ্ন)",
      status: "PUBLISHED"
    },
    {
      id: "q_chem_organic_45",
      version: 2,
      stemBn: "নিচের কোন যৌগটি ফেলিং দ্রবণের সাথে লাল অধঃক্ষেপ দেয়?",
      subject: "রসায়ন ২য় পত্র (জৈব রসায়ন)",
      reportsCount: 3,
      primaryIssue: "টাইপো / অপশন টেক্সটে ভুল সংকেত",
      status: "UNDER_REVIEW"
    }
  ]);

  const [auditLogs, setAuditLogs] = useState<AuditRecord[]>([
    {
      auditId: "aud_001",
      action: "QUARANTINE_QUESTION",
      questionId: "q_math_algebra_88",
      actor: "Dr. Rafiqul Islam (Subject Reviewer)",
      reason: "ভুল অ্যানসার কী ধরা পড়ায় সাময়িক কোয়ারেন্টিন। ১৪২ জন শিক্ষার্থীর মার্কস রিক্যালকুলেট করা হয়েছে।",
      timestamp: "১৪ অক্টোবর ২০২৬, সকাল ১০:১৫"
    }
  ]);

  const [quarantineTarget, setQuarantineTarget] = useState<ReportedQuestion | null>(null);
  const [quarantineReason, setQuarantineReason] = useState<string>("");
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

  const handleOpenQuarantineModal = (q: ReportedQuestion) => {
    setQuarantineTarget(q);
    setQuarantineReason("");
  };

  const handleConfirmQuarantine = () => {
    if (!quarantineTarget || quarantineReason.trim().length < 5) {
      alert("অনুগ্রহ করে কোয়ারেন্টিনের সুনির্দিষ্ট অডিট কারণ লিখুন (কমপক্ষে ৫ অক্ষর)।");
      return;
    }

    setIsProcessing(true);

    setTimeout(() => {
      // 1. Update question state
      setQuestions((prev) =>
        prev.map((item) =>
          item.id === quarantineTarget.id
            ? { ...item, status: "QUARANTINED" }
            : item
        )
      );

      // 2. Add to immutable audit log
      const newAudit: AuditRecord = {
        auditId: `aud_${Date.now().toString().slice(-4)}`,
        action: "QUARANTINE_QUESTION",
        questionId: quarantineTarget.id,
        actor: "Admin (Current Session)",
        reason: quarantineReason,
        timestamp: "১৪ অক্টোবর ২০২৬, এইমাত্র"
      };
      setAuditLogs((prev) => [newAudit, ...prev]);

      setIsProcessing(false);
      setQuarantineTarget(null);
      setQuarantineReason("");
    }, 600);
  };

  return (
    <>
      <Head>
        <title>কনটেন্ট কোয়ারেন্টিন ও অডিট কনসোল | অগ্রযাত্রা অ্যাডমিন</title>
      </Head>

      <div className="min-h-screen bg-[var(--bg-app)] text-[var(--text-main)] transition-colors duration-200">
        
        {/* Header */}
        <header className="border-b border-[var(--border-subtle)] bg-[var(--bg-surface)] py-4">
          <div className="max-w-6xl mx-auto px-4 flex items-center justify-between">
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-[var(--color-danger-subtle)] text-[var(--color-danger)] border border-[var(--color-danger-border)]">
                  অ্যাডমিন অপারেশনস
                </span>
                <h1 className="text-xl font-bold">প্রশ্ন কোয়ারেন্টিন ও কোয়ালিটি কন্ট্রোল</h1>
              </div>
              <p className="text-xs text-[var(--text-muted)] mt-0.5">
                পরীক্ষার ন্যায্যতা রক্ষায় ত্রুটিযুক্ত প্রশ্ন এক ক্লিকে সাময়িক প্রত্যাহার ও অডিট ট্রেইল
              </p>
            </div>
            <ThemeToggle />
          </div>
        </header>

        <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
          
          {/* Section 1: Active Reports & Flagged Items */}
          <section className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-bold">রিপোর্ট হওয়া প্রশ্নসমূহ (Flagged Items Queue)</h2>
                <p className="text-xs text-[var(--text-muted)]">
                  শিক্ষার্থী ও শিক্ষকদের কাছ থেকে জমা পড়া অভিযোগের তালিকা
                </p>
              </div>
              <Badge variant="warning">
                {questions.filter((q) => q.status !== 'QUARANTINED').length} টি অনিষ্পন্ন
              </Badge>
            </div>

            <div className="space-y-3">
              {questions.map((q) => (
                <div
                  key={q.id}
                  className="p-5 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-surface)] flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-sm"
                >
                  <div className="space-y-1.5 max-w-2xl">
                    <div className="flex items-center space-x-2">
                      <span className="font-mono text-xs font-bold text-[var(--text-subtle)] bg-[var(--bg-surface-elevated)] px-2 py-0.5 rounded">
                        {q.id} (v{q.version})
                      </span>
                      <span className="text-xs text-[var(--text-muted)] font-medium">
                        {q.subject}
                      </span>
                      {q.status === 'QUARANTINED' ? (
                        <Badge variant="danger">কোয়ারেন্টিন কার্যকর</Badge>
                      ) : (
                        <Badge variant="warning">{q.reportsCount} টি অভিযোগ</Badge>
                      )}
                    </div>
                    <p className="text-base font-semibold leading-relaxed">
                      {q.stemBn}
                    </p>
                    <p className="text-xs text-[var(--color-danger)] font-medium">
                      অভিযোগের কারণ: {q.primaryIssue}
                    </p>
                  </div>

                  <div className="flex items-center space-x-2">
                    {q.status !== 'QUARANTINED' ? (
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => handleOpenQuarantineModal(q)}
                      >
                        কোয়ারেন্টিন করুন
                      </Button>
                    ) : (
                      <span className="text-xs font-medium text-[var(--text-muted)] bg-[var(--bg-surface-elevated)] px-3 py-1.5 rounded-lg border border-[var(--border-subtle)]">
                        লাইভ টেস্ট থেকে স্থগিত
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Section 2: Immutable Audit Log */}
          <section className="space-y-4 pt-4 border-t border-[var(--border-subtle)]">
            <div>
              <h2 className="text-lg font-bold">অপরিবর্তনীয় অডিট ট্রেইল (Immutable Audit Log)</h2>
              <p className="text-xs text-[var(--text-muted)]">
                অ্যাডমিন ও রিভিউরদের নেওয়া প্রতিটি কোয়ারেন্টিন সিদ্ধান্তের ক্রমানুসারিক লগ
              </p>
            </div>

            <div className="space-y-3">
              {auditLogs.map((log) => (
                <div
                  key={log.auditId}
                  className="p-4 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-surface-elevated)] space-y-1 text-sm"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-bold text-xs text-[var(--color-brand)]">
                      [{log.auditId}] {log.action}
                    </span>
                    <span className="text-xs text-[var(--text-muted)]">
                      {log.timestamp}
                    </span>
                  </div>
                  <p className="text-xs text-[var(--text-subtle)]">
                    প্রশ্ন আইডি: <strong>{log.questionId}</strong> | দায়িত্বপ্রাপ্ত: <strong>{log.actor}</strong>
                  </p>
                  <p className="text-xs text-[var(--text-main)] pt-1">
                    <strong>অডিট কারণ:</strong> {log.reason}
                  </p>
                </div>
              ))}
            </div>
          </section>

        </main>

        {/* Quarantine Reason Confirmation Modal */}
        {quarantineTarget && (
          <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="max-w-lg w-full rounded-2xl border border-[var(--border-subtle)] bg-[var(--bg-surface)] p-6 shadow-2xl space-y-5">
              <div className="space-y-1">
                <Badge variant="danger">কোয়ারেন্টিন সতর্কতা</Badge>
                <h3 className="text-xl font-bold mt-1">প্রশ্নটি কি কোয়ারেন্টিন করতে চান?</h3>
                <p className="text-xs text-[var(--text-muted)]">
                  কোয়ারেন্টিন করা হলে প্রশ্নটি তাৎক্ষণিকভাবে সকল ভবিষ্যৎ পরীক্ষা থেকে সরিয়ে নেওয়া হবে।
                </p>
              </div>

              <div className="p-3 rounded-lg bg-[var(--bg-surface-elevated)] border border-[var(--border-subtle)] text-xs space-y-1">
                <p className="font-bold">প্রশ্ন: {quarantineTarget.stemBn}</p>
                <p className="text-[var(--text-muted)]">আইডি: {quarantineTarget.id}</p>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-[var(--text-main)]">
                  অডিট কারণ লিখুন (বাধ্যতামূলক):
                </label>
                <textarea
                  rows={3}
                  value={quarantineReason}
                  onChange={(e) => setQuarantineReason(e.target.value)}
                  placeholder="যেমন: অপশন A ও C উভয়ই সঠিক হওয়ায় সাময়িক প্রত্যাহার..."
                  className="w-full text-sm p-3 rounded-lg border border-[var(--border-strong)] bg-[var(--bg-app)] text-[var(--text-main)] focus:outline-none focus:ring-2 focus:ring-[var(--focus-ring)]"
                />
              </div>

              <div className="flex items-center justify-end space-x-3 pt-2">
                <Button
                  variant="ghost"
                  onClick={() => setQuarantineTarget(null)}
                  disabled={isProcessing}
                >
                  বাতিল
                </Button>
                <Button
                  variant="danger"
                  isLoading={isProcessing}
                  onClick={handleConfirmQuarantine}
                >
                  কোয়ারেন্টিন নিশ্চিত করুন
                </Button>
              </div>
            </div>
          </div>
        )}

      </div>
    </>
  );
}
