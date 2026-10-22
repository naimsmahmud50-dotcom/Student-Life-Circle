/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Public Scholarship Disbursement Ledger Modal
 * TOPIC:     Phase 113 National Merit Scholarship Pool & Autonomous Disbursement
 * FILE:      frontend/src/components/scholarship/DisbursementLedgerModal.tsx
 * PHASE:     Phase 113 - National Merit Scholarship Pool & Autonomous Disbursement
 * PURPOSE:   Provides transparent, tamper-evident public audit verification of
 *            micro-scholarship payouts while strictly protecting minor student PII
 *            through anonymized cryptographic SHA-256 ledger seals and dual-custodian signatures.
 * STANDARDS: OWASP ASVS L2, FinTech B2C Security, Pure Academic Design, Strict Zero-Emoji
 */

import React, { useState, useMemo } from 'react';
import {
  X,
  ShieldCheck,
  CheckCircle2,
  Lock,
  Search,
  Filter,
  ExternalLink,
  Award,
  Wallet,
  Building,
  Calendar,
  FileText
} from 'lucide-react';

export interface PublicLedgerRecord {
  receipt_id: string;
  anonymous_student_token: string;
  district: string;
  disbursed_amount_bdt: number;
  gateway_provider: string;
  gateway_transaction_ref: string;
  masked_wallet: string;
  ledger_seal_sha256: string;
  disbursed_at: number;
  verification_status: string;
}

export interface DisbursementLedgerModalProps {
  isOpen: boolean;
  onClose: () => void;
  records?: PublicLedgerRecord[];
}

const DEFAULT_RECORDS: PublicLedgerRecord[] = [
  {
    receipt_id: 'rcpt_782941fa9b',
    anonymous_student_token: 'STU-****-8241',
    district: 'Kurigram',
    disbursed_amount_bdt: 10000.0,
    gateway_provider: 'BKASH',
    gateway_transaction_ref: 'B2C_BKASH_9A42F8C1D07E',
    masked_wallet: '017*****821',
    ledger_seal_sha256: '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08',
    disbursed_at: Math.floor(Date.now() / 1000) - 3600 * 2,
    verification_status: 'VERIFIED_ON_LEDGER',
  },
  {
    receipt_id: 'rcpt_519382bb2c',
    anonymous_student_token: 'STU-****-3109',
    district: 'Sunamganj',
    disbursed_amount_bdt: 10000.0,
    gateway_provider: 'BKASH',
    gateway_transaction_ref: 'B2C_BKASH_8812A93CD41F',
    masked_wallet: '018*****904',
    ledger_seal_sha256: '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
    disbursed_at: Math.floor(Date.now() / 1000) - 3600 * 5,
    verification_status: 'VERIFIED_ON_LEDGER',
  },
  {
    receipt_id: 'rcpt_192847fc3d',
    anonymous_student_token: 'STU-****-9482',
    district: 'Bandarban',
    disbursed_amount_bdt: 8000.0,
    gateway_provider: 'NAGAD',
    gateway_transaction_ref: 'B2C_NAGAD_6672E904B12A',
    masked_wallet: '016*****115',
    ledger_seal_sha256: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
    disbursed_at: Math.floor(Date.now() / 1000) - 3600 * 8,
    verification_status: 'VERIFIED_ON_LEDGER',
  },
  {
    receipt_id: 'rcpt_384729fe4a',
    anonymous_student_token: 'STU-****-5520',
    district: 'Barguna',
    disbursed_amount_bdt: 10000.0,
    gateway_provider: 'BKASH',
    gateway_transaction_ref: 'B2C_BKASH_4419C72EA991',
    masked_wallet: '019*****742',
    ledger_seal_sha256: 'ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d',
    disbursed_at: Math.floor(Date.now() / 1000) - 3600 * 12,
    verification_status: 'VERIFIED_ON_LEDGER',
  },
  {
    receipt_id: 'rcpt_901824aa5b',
    anonymous_student_token: 'STU-****-7183',
    district: 'Lalmonirhat',
    disbursed_amount_bdt: 8000.0,
    gateway_provider: 'NAGAD',
    gateway_transaction_ref: 'B2C_NAGAD_3301B84FC229',
    masked_wallet: '013*****489',
    ledger_seal_sha256: '87563ca5932598be698f2b347b409748b6c8672958296200fb16f2ca91ea2ee2',
    disbursed_at: Math.floor(Date.now() / 1000) - 3600 * 18,
    verification_status: 'VERIFIED_ON_LEDGER',
  },
];

export const DisbursementLedgerModal: React.FC<DisbursementLedgerModalProps> = ({
  isOpen,
  onClose,
  records = DEFAULT_RECORDS,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [districtFilter, setDistrictFilter] = useState('all');
  const [gatewayFilter, setGatewayFilter] = useState('all');

  const filteredRecords = useMemo(() => {
    return records.filter((r) => {
      if (districtFilter !== 'all' && r.district.toLowerCase() !== districtFilter.toLowerCase()) {
        return false;
      }
      if (gatewayFilter !== 'all' && r.gateway_provider.toUpperCase() !== gatewayFilter.toUpperCase()) {
        return false;
      }
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        return (
          r.anonymous_student_token.toLowerCase().includes(q) ||
          r.district.toLowerCase().includes(q) ||
          r.gateway_transaction_ref.toLowerCase().includes(q) ||
          r.ledger_seal_sha256.toLowerCase().includes(q)
        );
      }
      return true;
    });
  }, [records, districtFilter, gatewayFilter, searchQuery]);

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/70 animate-fade-in"
    >
      <div className="bg-[#FAFAF8] dark:bg-[#0B132B] border-2 border-slate-300 dark:border-slate-700 w-full max-w-4xl rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Modal Header */}
        <div className="p-6 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center shadow-sm">
              <ShieldCheck className="w-5 h-5 text-amber-300" />
            </div>
            <div>
              <h2 id="modal-title" className="text-lg sm:text-xl font-bold font-bengali text-slate-900 dark:text-white leading-tight">
                পাবলিক স্কলারশিপ ডিসবার্সমেন্ট লেজার
              </h2>
              <p className="text-xs text-slate-500 font-display">
                Cryptographic SHA-256 Audit Trail & Anonymized Payout Receipts
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="w-9 h-9 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 flex items-center justify-center text-slate-600 dark:text-slate-300 transition-colors"
            aria-label="Close modal"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search & Filter Bar */}
        <div className="p-4 bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center gap-3">
          <div className="relative flex-1 min-w-[200px]">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="টোকেন আইডি, ট্রানজ্যাকশন হ্যাশ বা জেলা খুঁজুন..."
              className="w-full pl-9 pr-3 py-1.5 text-xs font-bengali bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0A2540] text-slate-900 dark:text-white"
            />
          </div>

          <select
            value={districtFilter}
            onChange={(e) => setDistrictFilter(e.target.value)}
            className="px-3 py-1.5 text-xs font-bengali bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white"
          >
            <option value="all">সকল জেলা</option>
            <option value="Kurigram">কুড়িগ্রাম</option>
            <option value="Sunamganj">সুনামগঞ্জ</option>
            <option value="Bandarban">বান্দরবান</option>
            <option value="Barguna">বরগুনা</option>
            <option value="Lalmonirhat">লালমনিরহাট</option>
          </select>

          <select
            value={gatewayFilter}
            onChange={(e) => setGatewayFilter(e.target.value)}
            className="px-3 py-1.5 text-xs font-display bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white"
          >
            <option value="all">All Gateways</option>
            <option value="BKASH">bKash B2C</option>
            <option value="NAGAD">Nagad Bulk</option>
          </select>
        </div>

        {/* Ledger Records Table */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-3">
          {filteredRecords.length === 0 ? (
            <div className="text-center py-12 text-slate-400 font-bengali text-xs">
              কোনো লেনদেন রেকর্ড পাওয়া যায়নি।
            </div>
          ) : (
            filteredRecords.map((item) => (
              <div
                key={item.receipt_id}
                className="p-4 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm space-y-2.5 transition-all hover:border-[#0A2540]/40"
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-1 rounded-lg bg-[#0A2540] text-white font-mono text-xs font-bold">
                      {item.anonymous_student_token}
                    </span>
                    <span className="px-2.5 py-0.5 rounded-md bg-amber-100 dark:bg-amber-950/60 text-amber-800 dark:text-amber-300 font-bengali text-xs font-medium">
                      {item.district === 'Kurigram'
                        ? 'কুড়িগ্রাম'
                        : item.district === 'Sunamganj'
                        ? 'সুনামগঞ্জ'
                        : item.district === 'Bandarban'
                        ? 'বান্দরবান'
                        : item.district === 'Barguna'
                        ? 'বরগুনা'
                        : item.district}
                    </span>
                    <span className="text-[11px] text-slate-400 font-display">
                      {new Date(item.disbursed_at * 1000).toLocaleString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </span>
                  </div>

                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 text-[11px] font-bold font-display flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                      <span>{item.verification_status}</span>
                    </span>
                    <strong className="text-base text-slate-900 dark:text-white font-display font-bold">
                      ৳{item.disbursed_amount_bdt.toLocaleString('en-US')}
                    </strong>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-display text-slate-600 dark:text-slate-400 pt-1">
                  <div>
                    <span className="text-slate-400">Gateway Ref: </span>
                    <span className="font-mono text-slate-800 dark:text-slate-200">
                      {item.gateway_transaction_ref} ({item.gateway_provider})
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-400">Wallet Masked: </span>
                    <span className="font-mono text-slate-800 dark:text-slate-200">
                      {item.masked_wallet}
                    </span>
                  </div>
                </div>

                <div className="pt-1.5 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-[10px] font-mono text-slate-400">
                  <span className="truncate max-w-[80%]" title={item.ledger_seal_sha256}>
                    SHA-256 Seal: {item.ledger_seal_sha256}
                  </span>
                  <span className="text-emerald-600 font-semibold font-display">
                    Dual-Authorized
                  </span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-4 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500 font-bengali">
          <span>
            সর্বমোট অডিটকৃত অনুদান: <strong>৳{records.reduce((acc, r) => acc + r.disbursed_amount_bdt, 0).toLocaleString('en-US')}</strong>
          </span>
          <button
            type="button"
            onClick={onClose}
            className="px-5 py-2 bg-[#0A2540] hover:bg-[#0E3357] text-white rounded-xl text-xs font-semibold shadow-sm transition-all"
          >
            লেজার বন্ধ করুন
          </button>
        </div>
      </div>
    </div>
  );
};
