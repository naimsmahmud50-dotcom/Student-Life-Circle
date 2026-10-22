/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    National Payment Gateway & Security Lockdown
 * TOPIC:     Phase 140 bKash, Nagad, SSLCommerz Escrow, IPN Webhooks & OWASP ASVS L2 Audit
 * FILE:      frontend/src/components/payment/PaymentDrawer.tsx
 * PHASE:     Phase 140 - National Payment Gateway & Live Security Audit
 * PURPOSE:   Unified tactile checkout drawer supporting bKash, Nagad, and Cards (SSLCommerz) with 24h escrow assurance
 * STANDARDS: Zero-Emoji, Zero-IDOR, OWASP ASVS L2, Atomic DB Transactions, Server Authority
 */

import React, { useState } from "react";
import {
  CreditCard,
  ShieldCheck,
  Lock,
  Clock,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  FileText,
  RefreshCw,
  X,
  Smartphone
} from "lucide-react";

export type PaymentGatewayType = "BKASH" | "NAGAD" | "SSLCOMMERZ";

export interface PaymentDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  referenceId: string;
  purposeTitle: string;
  serverAmountBdt: number;
  customerName?: string;
  customerPhone?: string;
  onSuccess?: (receipt: any) => void;
}

export const PaymentDrawer: React.FC<PaymentDrawerProps> = ({
  isOpen,
  onClose,
  referenceId,
  purposeTitle,
  serverAmountBdt,
  customerName = "শিক্ষার্থী",
  customerPhone = "01700000000",
  onSuccess
}) => {
  const [selectedGateway, setSelectedGateway] = useState<PaymentGatewayType>("BKASH");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [completedTrx, setCompletedTrx] = useState<any | null>(null);

  if (!isOpen) return null;

  const handleInitiatePayment = async () => {
    setIsLoading(true);
    setErrorMsg(null);

    try {
      const idempotencyKey = `IDEMP_${Date.now()}_${Math.random().toString(36).substring(2, 9).toUpperCase()}`;

      const res = await fetch("/api/v1/payments/checkout/initiate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Idempotency-Key": idempotencyKey
        },
        body: JSON.stringify({
          gateway: selectedGateway,
          reference_id: referenceId,
          purpose: purposeTitle,
          customer_name: customerName,
          customer_phone: customerPhone
        })
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "পেমেন্ট সেশন তৈরিতে ত্রুটি হয়েছে। পুনরায় চেষ্টা করুন।");
      }

      // If gateway returns checkout redirect URL
      if (data.checkout_url) {
        // Simulated or live gateway redirection
        if (data.is_sandbox) {
          // Direct simulated success in sandbox test environment
          const simulatedTrx = {
            status: "SUCCESS",
            transaction_id: data.transaction_id || `TRX_${Date.now()}`,
            gateway: selectedGateway,
            amount_bdt: serverAmountBdt,
            purpose: purposeTitle,
            timestamp: new Date().toISOString()
          };
          setCompletedTrx(simulatedTrx);
          if (onSuccess) onSuccess(simulatedTrx);
        } else {
          window.location.href = data.checkout_url;
        }
      } else {
        setCompletedTrx(data);
        if (onSuccess) onSuccess(data);
      }
    } catch (err: any) {
      setErrorMsg(err.message || "পেমেন্ট প্রসেসিংয়ে বিঘ্ন ঘটেছে।");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 p-4">
      <div className="relative w-full max-w-lg rounded-2xl border border-slate-800 bg-[#0B132B] p-6 text-slate-100 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400">
              <ShieldCheck className="h-6 w-6" aria-hidden="true" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-100 font-bengali">সুরক্ষিত পেমেন্ট গেটওয়ে</h2>
              <p className="text-xs text-slate-400 font-bengali">সার্ভার-ভেরিফাইড ২৪ ঘণ্টার ডিজিটাল এসক্রো প্রোটেকশন</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors"
            aria-label="বন্ধ করুন"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Content */}
        {!completedTrx ? (
          <div className="mt-5 space-y-5">
            {/* Order Summary */}
            <div className="rounded-xl border border-slate-800/80 bg-slate-900/60 p-4">
              <div className="flex justify-between items-center text-sm">
                <span className="text-slate-400 font-bengali">সেবা / কোর্স:</span>
                <span className="font-semibold text-slate-200 font-bengali">{purposeTitle}</span>
              </div>
              <div className="flex justify-between items-center text-sm mt-2">
                <span className="text-slate-400 font-bengali">রেফারেন্স আইডি:</span>
                <span className="font-mono text-xs text-cyan-400">{referenceId}</span>
              </div>
              <div className="mt-3 pt-3 border-t border-slate-800 flex justify-between items-center">
                <span className="text-sm font-medium text-slate-300 font-bengali">নির্ধারিত ফি:</span>
                <div className="text-right">
                  <span className="text-2xl font-black text-cyan-400 font-latin">৳ {serverAmountBdt.toLocaleString()}</span>
                  <span className="text-xs text-slate-500 block font-bengali">সার্ভার-অথরিটেটিভ প্রাইসিং</span>
                </div>
              </div>
            </div>

            {/* Gateway Selection Tabs */}
            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-400 font-bengali">
                পেমেন্ট চ্যানেল নির্বাচন করুন
              </label>
              <div className="grid grid-cols-3 gap-2.5">
                {/* bKash */}
                <button
                  type="button"
                  onClick={() => setSelectedGateway("BKASH")}
                  className={`flex flex-col items-center justify-center gap-1.5 rounded-xl border p-3.5 transition-all text-center ${
                    selectedGateway === "BKASH"
                      ? "border-pink-500 bg-pink-500/10 text-pink-400 shadow-[0_3px_0_0_#9d174d]"
                      : "border-slate-800 bg-slate-900/50 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  <Smartphone className="h-5 w-5" aria-hidden="true" />
                  <span className="text-xs font-bold font-bengali">বিকাশ (bKash)</span>
                </button>

                {/* Nagad */}
                <button
                  type="button"
                  onClick={() => setSelectedGateway("NAGAD")}
                  className={`flex flex-col items-center justify-center gap-1.5 rounded-xl border p-3.5 transition-all text-center ${
                    selectedGateway === "NAGAD"
                      ? "border-amber-500 bg-amber-500/10 text-amber-400 shadow-[0_3px_0_0_#b45309]"
                      : "border-slate-800 bg-slate-900/50 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  <Smartphone className="h-5 w-5" aria-hidden="true" />
                  <span className="text-xs font-bold font-bengali">নগদ (Nagad)</span>
                </button>

                {/* Cards / SSLCommerz */}
                <button
                  type="button"
                  onClick={() => setSelectedGateway("SSLCOMMERZ")}
                  className={`flex flex-col items-center justify-center gap-1.5 rounded-xl border p-3.5 transition-all text-center ${
                    selectedGateway === "SSLCOMMERZ"
                      ? "border-cyan-500 bg-cyan-500/10 text-cyan-400 shadow-[0_3px_0_0_#0e7490]"
                      : "border-slate-800 bg-slate-900/50 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  <CreditCard className="h-5 w-5" aria-hidden="true" />
                  <span className="text-xs font-bold font-bengali">কার্ড / নেটব্যাংকিং</span>
                </button>
              </div>
            </div>

            {/* Escrow Guarantee Pill */}
            <div className="flex items-start gap-2.5 rounded-xl bg-slate-900/80 border border-slate-800 p-3 text-xs text-slate-400">
              <Clock className="h-4 w-4 text-cyan-400 shrink-0 mt-0.5" aria-hidden="true" />
              <div className="font-bengali leading-relaxed">
                <span className="font-semibold text-slate-300">২৪ ঘণ্টার স্বয়ংক্রিয় সুরক্ষা নিশ্চয়তা:</span> আপনার প্রদত্ত অর্থ সরাসরি প্ল্যাটফর্মের এনক্রিপ্টেড এসক্রো ভল্টে সংরক্ষিত থাকবে। ক্লাস বা সেশন সম্পন্ন না হলে অথবা সন্তুষ্ট না হলে বিরোধ নিষ্পত্তি বা রিফান্ডের নিশ্চয়তা রয়েছে।
              </div>
            </div>

            {/* Error Message */}
            {errorMsg && (
              <div className="flex items-center gap-2 rounded-xl bg-red-500/10 border border-red-500/30 p-3 text-xs text-red-400 font-bengali">
                <AlertCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
                <span>{errorMsg}</span>
              </div>
            )}

            {/* Checkout Action Button */}
            <button
              type="button"
              disabled={isLoading}
              onClick={handleInitiatePayment}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold py-3.5 px-4 shadow-[0_4px_0_0_#0891b2] active:translate-y-1 transition-all disabled:opacity-50 disabled:pointer-events-none font-bengali"
            >
              {isLoading ? (
                <>
                  <RefreshCw className="h-5 w-5 animate-spin" aria-hidden="true" />
                  <span>পেমেন্ট সেশন প্রসেস হচ্ছে...</span>
                </>
              ) : (
                <>
                  <Lock className="h-4 w-4" aria-hidden="true" />
                  <span>৳ {serverAmountBdt.toLocaleString()} নিরাপদে পরিশোধ করুন</span>
                  <ArrowRight className="h-4 w-4 ml-1" aria-hidden="true" />
                </>
              )}
            </button>
          </div>
        ) : (
          /* Transaction Completed Confirmation View */
          <div className="mt-5 space-y-4 text-center">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              <CheckCircle2 className="h-8 w-8" aria-hidden="true" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-100 font-bengali">পেমেন্ট সফল ও এসক্রোতে সংরক্ষিত</h3>
              <p className="text-xs text-slate-400 font-bengali mt-1">
                আপনার লেনদেনটি সফলভাবে সম্পন্ন হয়েছে এবং ডিজিটাল রসিদ প্রস্তুত।
              </p>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 text-left text-xs space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400 font-bengali">ট্রানজ্যাকশন আইডি:</span>
                <span className="font-mono text-cyan-400 font-semibold">{completedTrx.transaction_id || "TRX_VERIFIED"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 font-bengali">পেমেন্ট মেথড:</span>
                <span className="font-semibold text-slate-200">{completedTrx.gateway || selectedGateway}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400 font-bengali">পরিশোধিত অর্থ:</span>
                <span className="font-bold text-emerald-400">৳ {serverAmountBdt.toLocaleString()} BDT</span>
              </div>
            </div>

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 rounded-xl border border-slate-800 bg-slate-900/60 py-3 text-xs font-semibold text-slate-300 hover:bg-slate-800 transition-colors font-bengali"
              >
                বন্ধ করুন
              </button>
              <button
                type="button"
                onClick={() => {
                  window.open(`/api/v1/payments/invoice/${completedTrx.transaction_id || "SLC"}/download`, "_blank");
                }}
                className="flex-1 flex items-center justify-center gap-1.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 py-3 text-xs font-bold text-slate-950 shadow-[0_3px_0_0_#0891b2] active:translate-y-0.5 transition-all font-bengali"
              >
                <FileText className="h-4 w-4" aria-hidden="true" />
                <span>ডিজিটাল রসিদ ডাউনলোড</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PaymentDrawer;
