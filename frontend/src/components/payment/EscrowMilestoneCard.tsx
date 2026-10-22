/**
 * ==============================================================================
 * DEVELOPER ARCHITECTURE NOTE (Phase 81 - Escrow Milestone Card Component):
 * This component visualizes the Dual-Party Tuition Milestone Escrow Vault state
 * for both guardian and tutor perspectives.
 * Key Architectural Features:
 * 1. Multi-State Milestone Progression:
 *    - HELD_IN_ESCROW: Funds locked and waiting for teaching sessions.
 *    - SESSION_LOGGED: Tutor logged session topic and duration.
 *    - MILESTONE_APPROVED / FUNDS_DISBURSED: 95% net honorarium released to tutor wallet.
 *    - DISPUTE_FROZEN: Funds frozen pending institutional arbitrator decision.
 * 2. Role-Aware Interactive Controls:
 *    - Guardians can trigger milestone approval or raise an arbitration dispute.
 *    - Tutors can log new teaching sessions with syllabus topics.
 * 3. Strict Zero-Emoji Governance: Uses exclusively Lucide SVG vectors and clean technical text.
 * ==============================================================================
 */

import React, { useState } from "react";
import {
  CheckCircle2,
  Clock,
  ShieldAlert,
  DollarSign,
  BookOpen,
  FileCheck,
  ShieldCheck,
  AlertCircle
} from "lucide-react";

export interface EscrowMilestoneCardProps {
  contractId: string;
  guardianId: string;
  tutorId: string;
  amountBdt: number;
  gateway: "BKASH" | "NAGAD";
  sessionsAgreed: number;
  sessionsCompleted: number;
  status:
    | "PENDING_DEPOSIT"
    | "HELD_IN_ESCROW"
    | "SESSION_LOGGED"
    | "MILESTONE_APPROVED"
    | "FUNDS_DISBURSED"
    | "DISPUTE_FROZEN"
    | "ARBITRATED_RELEASE"
    | "ARBITRATED_REFUND";
  currentUserRole?: "guardian" | "educator" | "admin";
  onSessionLogged?: (sessionData: any) => void;
  onMilestoneApproved?: (result: any) => void;
  onDisputeRaised?: (disputeData: any) => void;
}

export const EscrowMilestoneCard: React.FC<EscrowMilestoneCardProps> = ({
  contractId,
  guardianId,
  tutorId,
  amountBdt,
  gateway,
  sessionsAgreed,
  sessionsCompleted,
  status: initialStatus,
  currentUserRole = "guardian",
  onSessionLogged,
  onMilestoneApproved,
  onDisputeRaised
}) => {
  const [status, setStatus] = useState(initialStatus);
  const [completedCount, setCompletedCount] = useState(sessionsCompleted);
  const [isLoading, setIsLoading] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  const progressPercent = Math.min(100, Math.round((completedCount / sessionsAgreed) * 100));

  const handleApproveMilestone = async () => {
    setIsLoading(true);
    setFeedback(null);
    try {
      const res = await fetch("/api/v1/payments/escrow/milestone/approve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contract_id: contractId,
          guardian_id: guardianId
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Approval failed.");

      setStatus("FUNDS_DISBURSED");
      setFeedback("Milestone approved. Net honorarium disbursed to tutor wallet.");
      if (onMilestoneApproved) onMilestoneApproved(data);
    } catch (err: any) {
      setFeedback(err.message || "Failed to approve milestone.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogSession = async () => {
    setIsLoading(true);
    setFeedback(null);
    try {
      const nextSession = completedCount + 1;
      const res = await fetch("/api/v1/payments/escrow/session/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contract_id: contractId,
          tutor_id: tutorId,
          session_number: nextSession,
          topic: `Class Chapter ${nextSession} Review`
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Session logging failed.");

      setCompletedCount(nextSession);
      setStatus("SESSION_LOGGED");
      setFeedback(`Session ${nextSession} successfully logged for guardian review.`);
      if (onSessionLogged) onSessionLogged(data);
    } catch (err: any) {
      setFeedback(err.message || "Failed to log session.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleRaiseDispute = async () => {
    const reason = prompt("State the arbitration reason for freezing escrow:");
    if (!reason) return;

    setIsLoading(true);
    setFeedback(null);
    try {
      const res = await fetch("/api/v1/payments/escrow/dispute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contract_id: contractId,
          disputant_id: currentUserRole === "educator" ? tutorId : guardianId,
          reason
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Dispute request failed.");

      setStatus("DISPUTE_FROZEN");
      setFeedback("Escrow frozen. An institutional administrator will arbitrate.");
      if (onDisputeRaised) onDisputeRaised(data);
    } catch (err: any) {
      setFeedback(err.message || "Failed to raise dispute.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm space-y-4">
      {/* Card Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-blue-600 dark:text-blue-400" />
          <span className="text-xs font-mono text-slate-500 uppercase">
            Contract: {contractId}
          </span>
        </div>

        {/* Status Badge */}
        <span
          className={`px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
            status === "FUNDS_DISBURSED" || status === "ARBITRATED_RELEASE"
              ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300"
              : status === "DISPUTE_FROZEN"
              ? "bg-red-100 text-red-800 dark:bg-red-950/60 dark:text-red-300"
              : status === "SESSION_LOGGED"
              ? "bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300"
              : "bg-blue-100 text-blue-800 dark:bg-blue-950/60 dark:text-blue-300"
          }`}
        >
          {status.replace(/_/g, " ")}
        </span>
      </div>

      {/* Financial Details */}
      <div className="grid grid-cols-2 gap-3 p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg text-sm">
        <div>
          <div className="text-xs text-slate-500">Escrow Amount</div>
          <div className="text-base font-bold text-slate-900 dark:text-slate-100">
            {amountBdt.toFixed(2)} BDT
          </div>
        </div>
        <div>
          <div className="text-xs text-slate-500">Payment Gateway</div>
          <div className="text-sm font-semibold text-slate-700 dark:text-slate-300">
            {gateway === "BKASH" ? "bKash Merchant" : "Nagad Encrypted"}
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs text-slate-600 dark:text-slate-400">
          <span>Syllabus Progress</span>
          <span>
            {completedCount} of {sessionsAgreed} sessions ({progressPercent}%)
          </span>
        </div>
        <div className="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-blue-600 transition-all duration-300"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Feedback Message */}
      {feedback && (
        <div className="flex items-center gap-2 p-2.5 bg-blue-50 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300 rounded text-xs">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{feedback}</span>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center gap-2 pt-1">
        {currentUserRole === "guardian" && status !== "FUNDS_DISBURSED" && status !== "DISPUTE_FROZEN" && (
          <button
            onClick={handleApproveMilestone}
            disabled={isLoading}
            className="flex-1 py-2 px-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50"
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            Approve & Release Funds
          </button>
        )}

        {currentUserRole === "educator" && status !== "FUNDS_DISBURSED" && status !== "DISPUTE_FROZEN" && (
          <button
            onClick={handleLogSession}
            disabled={isLoading}
            className="flex-1 py-2 px-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50"
          >
            <BookOpen className="w-3.5 h-3.5" />
            Log Completed Session
          </button>
        )}

        {status !== "FUNDS_DISBURSED" && status !== "DISPUTE_FROZEN" && (
          <button
            onClick={handleRaiseDispute}
            disabled={isLoading}
            className="py-2 px-3 border border-red-300 dark:border-red-800 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors disabled:opacity-50"
          >
            <ShieldAlert className="w-3.5 h-3.5" />
            Dispute
          </button>
        )}
      </div>
    </div>
  );
};
