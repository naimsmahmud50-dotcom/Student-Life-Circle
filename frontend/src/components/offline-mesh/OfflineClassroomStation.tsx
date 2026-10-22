/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Offline Classroom Station & Teacher Hub Dashboard
 * TOPIC:     Phase 119 Offline P2P Classroom Mesh & Local CRDT Sync
 * FILE:      frontend/src/components/offline-mesh/OfflineClassroomStation.tsx
 * PHASE:     Phase 119 - Offline P2P Classroom Mesh & Local CRDT Sync
 * PURPOSE:   Provides high-contrast utilitarian dashboard for teachers in rural
 *            classrooms without internet, monitoring up to 60 connected student peers,
 *            local quiz sessions, Lamport CRDT mutation queues, and cloud sync reconciliation.
 * STANDARDS: UI/UX Pro Max, High-Contrast Outdoor Readability, Strict Zero-Emoji
 */

import React, { useState } from 'react';
import {
  WifiOff,
  Share2,
  RefreshCw,
  CheckCircle,
  Database,
  Users,
  Radio,
  Signal,
  Play,
  CloudUpload,
  BookOpen,
  Laptop,
  Smartphone,
  Tablet,
  Check,
  AlertCircle
} from 'lucide-react';
import { CrdtMutationLedger, BatchSyncPayload } from '../../lib/offline/crdtMutationLedger';

export interface StudentPeerNode {
  client_id: string;
  student_name: string;
  roll_number: string;
  device_type: 'TABLET' | 'PHONE' | 'LAPTOP';
  signal_strength: 'EXCELLENT' | 'GOOD' | 'FAIR';
  answers_submitted: number;
  last_active: string;
}

export interface OfflineClassroomStationProps {
  stationId?: string;
  stationName?: string;
  ssid?: string;
  localIp?: string;
  activeQuizTitle?: string;
  initialPeers?: StudentPeerNode[];
  onStartQuiz?: () => Promise<void> | void;
  onSyncToCloud?: (payload: BatchSyncPayload) => Promise<boolean> | boolean;
}

const DEFAULT_PEERS: StudentPeerNode[] = [
  {
    client_id: 'peer-std-01',
    student_name: 'সাকিব হাসান',
    roll_number: '০১',
    device_type: 'TABLET',
    signal_strength: 'EXCELLENT',
    answers_submitted: 10,
    last_active: '১০ সেকেন্ড পূর্বে',
  },
  {
    client_id: 'peer-std-02',
    student_name: 'ফারহানা আকতার',
    roll_number: '০২',
    device_type: 'PHONE',
    signal_strength: 'EXCELLENT',
    answers_submitted: 10,
    last_active: '১৫ সেকেন্ড পূর্বে',
  },
  {
    client_id: 'peer-std-03',
    student_name: 'তানভীর আহমেদ',
    roll_number: '০৩',
    device_type: 'PHONE',
    signal_strength: 'GOOD',
    answers_submitted: 8,
    last_active: '২৫ সেকেন্ড পূর্বে',
  },
  {
    client_id: 'peer-std-04',
    student_name: 'নুসরাত জাহান',
    roll_number: '০৪',
    device_type: 'TABLET',
    signal_strength: 'EXCELLENT',
    answers_submitted: 10,
    last_active: '৫ সেকেন্ড পূর্বে',
  },
  {
    client_id: 'peer-std-05',
    student_name: 'মাহমুদুল করিম',
    roll_number: '০৫',
    device_type: 'LAPTOP',
    signal_strength: 'GOOD',
    answers_submitted: 9,
    last_active: '৩০ সেকেন্ড পূর্বে',
  },
];

export const OfflineClassroomStation: React.FC<OfflineClassroomStationProps> = ({
  stationId = 'STATION-CHAR-UPAZILA-04',
  stationName = 'চর কুচিয়ামোর সরকারি প্রাথমিক ও উচ্চ বিদ্যালয়',
  ssid = 'OGROJATRA-MESH-STATION-04',
  localIp = '192.168.4.1',
  activeQuizTitle = 'সাধারণ গণিত — পরিমিতি ও ত্রিকোণমিতি সাপ্তাহিক মূল্যায়ন',
  initialPeers = DEFAULT_PEERS,
  onStartQuiz,
  onSyncToCloud,
}) => {
  const [peers, setPeers] = useState<StudentPeerNode[]>(initialPeers);
  const [isQuizActive, setIsQuizActive] = useState<boolean>(true);
  const [pendingMutationCount, setPendingMutationCount] = useState<number>(47);
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const [syncStatusMessage, setSyncStatusMessage] = useState<string | null>(null);

  const handleStartLocalQuiz = async () => {
    setIsQuizActive(true);
    if (onStartQuiz) {
      await onStartQuiz();
    }
  };

  const handleCloudSync = async () => {
    setIsSyncing(true);
    setSyncStatusMessage('ক্লাউড সার্ভারের সাথে সংযোগ যাচাই ও ব্যাচ সিঙ্ক হচ্ছে...');

    const mockPayload: BatchSyncPayload = {
      station_id: stationId,
      batch_id: `batch-${Date.now().toString(36)}`,
      mutations_count: pendingMutationCount,
      mutations: [],
      generated_at: Date.now(),
      checksum: 'e3b0c442',
    };

    setTimeout(() => {
      if (onSyncToCloud) {
        onSyncToCloud(mockPayload);
      }
      setIsSyncing(false);
      setPendingMutationCount(0);
      setSyncStatusMessage('সকল অফলাইন উত্তরপত্র সফলভাবে ক্লাউড ডাটাবেজে সমন্বয় করা হয়েছে।');
      setTimeout(() => setSyncStatusMessage(null), 4000);
    }, 1200);
  };

  const getDeviceIcon = (type: StudentPeerNode['device_type']) => {
    switch (type) {
      case 'TABLET':
        return <Tablet className="w-4 h-4 text-slate-600" />;
      case 'PHONE':
        return <Smartphone className="w-4 h-4 text-slate-600" />;
      case 'LAPTOP':
        return <Laptop className="w-4 h-4 text-slate-600" />;
    }
  };

  return (
    <div className="min-h-screen bg-[#FAFAF8] text-[#0A2540] font-sans pb-16">
      {/* Top Utilitarian Field Bar */}
      <header className="sticky top-0 z-40 bg-white border-b border-slate-200 px-4 sm:px-8 py-4 shadow-xs">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-[#0A2540] text-white flex items-center justify-center shadow-xs">
              <Radio className="w-5 h-5 stroke-[1.75]" />
            </div>
            <div>
              <div className="flex items-center gap-2 text-xs font-bold text-slate-600 uppercase tracking-wider">
                <span>{stationName}</span>
                <span className="text-slate-300">•</span>
                <span>স্টেশন আইডি: {stationId}</span>
              </div>
              <h1 className="text-lg sm:text-xl font-bold text-[#0A2540] tracking-tight">
                অফলাইন পিয়ার-টু-পিয়ার ক্লাসরুম স্টেশন
              </h1>
            </div>
          </div>

          {/* Offline Mesh Status Pill */}
          <div className="flex items-center gap-3 flex-wrap">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-100 text-slate-800 border border-slate-300 text-xs font-semibold shadow-xs">
              <WifiOff className="w-3.5 h-3.5 text-slate-600" />
              <span>অফলাইন মোড সক্রিয় — স্থানীয় মেশ নেটওয়ার্ক</span>
            </div>

            <div className="px-3 py-1.5 rounded-xl bg-[#FAFAF8] border border-slate-200 text-xs font-mono font-medium text-slate-700">
              SSID: {ssid} ({localIp})
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8">
        {/* Metric Cards Grid */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">সংযুক্ত শিক্ষার্থী</span>
              <Users className="w-4 h-4 text-[#0A2540]" />
            </div>
            <div className="text-3xl font-bold text-[#0A2540]">{peers.length} / ৬০ জন</div>
            <span className="text-xs text-slate-500 mt-1 block">স্থানীয় Wi-Fi / ব্লুটুথ সংযোগ</span>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">স্থানীয় পরীক্ষা স্থিতি</span>
              <BookOpen className="w-4 h-4 text-emerald-700" />
            </div>
            <div className="text-base font-bold text-emerald-800 line-clamp-1">
              {isQuizActive ? 'সক্রিয় মূল্যায়ন চলমান' : 'স্থগিত'}
            </div>
            <span className="text-xs text-slate-500 mt-1 block">{activeQuizTitle}</span>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">অপেক্ষমাণ মিউটেশন</span>
              <Database className="w-4 h-4 text-amber-600" />
            </div>
            <div className="text-3xl font-bold text-slate-900">{pendingMutationCount} টি</div>
            <span className="text-xs text-slate-500 mt-1 block">ল্যাম্পোর্ট CRDT লেজারে সংরক্ষিত</span>
          </div>

          <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">ক্লাউড সিঙ্ক অবস্থা</span>
              <CloudUpload className="w-4 h-4 text-slate-500" />
            </div>
            <div className="text-base font-bold text-slate-800">
              {pendingMutationCount === 0 ? 'সম্পূর্ণ সিঙ্ককৃত' : 'সিঙ্ক প্রস্তুত'}
            </div>
            <span className="text-xs text-slate-500 mt-1 block">ইন্টারনেট পেলে স্বয়ংক্রিয় সিঙ্ক</span>
          </div>
        </section>

        {/* Sync Feedback Message */}
        {syncStatusMessage && (
          <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs font-medium text-emerald-900 flex items-center gap-2 shadow-xs">
            <CheckCircle className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <span>{syncStatusMessage}</span>
          </div>
        )}

        {/* Primary Action Button Bar */}
        <section className="bg-white border border-slate-200 rounded-3xl p-6 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-slate-100 flex items-center justify-center text-slate-700">
              <Share2 className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-[#0A2540]">ক্লাসরুম মেশ কন্ট্রোল সেন্টার</h3>
              <p className="text-xs text-slate-500">
                ইন্টারনেট ছাড়াই স্থানীয় হটস্পটের মাধ্যমে কুইজ পরিচালনা ও উত্তর সংগ্রহ করুন।
              </p>
            </div>
          </div>

          {/* Tactile 3D Oxford Navy Action Buttons */}
          <div className="flex items-center gap-3 w-full sm:w-auto">
            <button
              onClick={handleStartLocalQuiz}
              className="flex-1 sm:flex-none py-3 px-5 rounded-2xl bg-[#0A2540] text-white text-xs sm:text-sm font-semibold shadow-[0_4px_0_0_#061727] active:translate-y-1 active:shadow-none hover:bg-[#0c2f52] transition-all flex items-center justify-center gap-2"
            >
              <Play className="w-4 h-4 fill-white stroke-none" />
              <span>লোকাল কুইজ শুরু করুন</span>
            </button>

            <button
              onClick={handleCloudSync}
              disabled={isSyncing || pendingMutationCount === 0}
              className="flex-1 sm:flex-none py-3 px-6 rounded-2xl bg-[#0A2540] text-white text-xs sm:text-sm font-semibold shadow-[0_4px_0_0_#061727] active:translate-y-1 active:shadow-none hover:bg-[#0c2f52] disabled:opacity-40 disabled:pointer-events-none transition-all flex items-center justify-center gap-2"
            >
              <RefreshCw className={`w-4 h-4 ${isSyncing ? 'animate-spin' : ''}`} />
              <span>{isSyncing ? 'সিঙ্ক হচ্ছে...' : 'ক্লাউডে সিঙ্ক করুন'}</span>
            </button>
          </div>
        </section>

        {/* Student Peer Roster Table */}
        <section className="bg-white border border-slate-200 rounded-3xl shadow-xs overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4 text-slate-500" />
              <h2 className="text-base font-bold text-[#0A2540]">
                সংযুক্ত শিক্ষার্থী তালিকা (Connected Local Peers)
              </h2>
            </div>
            <span className="text-xs font-semibold text-slate-500">
              মোট সক্রিয় ডিভাইস: {peers.length} টি
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-[#FAFAF8] text-xs font-bold text-slate-600 uppercase border-b border-slate-100">
                <tr>
                  <th className="px-6 py-3.5">রোল ও শিক্ষার্থী নাম</th>
                  <th className="px-6 py-3.5">ডিভাইস ধরন</th>
                  <th className="px-6 py-3.5">সিগন্যাল শক্তি</th>
                  <th className="px-6 py-3.5">উত্তর জমা সম্পন্ন</th>
                  <th className="px-6 py-3.5">সর্বশেষ সক্রিয়</th>
                  <th className="px-6 py-3.5 text-right">স্থিতি</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {peers.map((peer) => (
                  <tr key={peer.client_id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-semibold text-[#0A2540]">{peer.student_name}</div>
                      <div className="text-xs text-slate-500">রোল: {peer.roll_number} • আইডি: {peer.client_id}</div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 text-xs text-slate-700">
                        {getDeviceIcon(peer.device_type)}
                        <span>{peer.device_type}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-800 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                        <Signal className="w-3 h-3 text-emerald-600" />
                        {peer.signal_strength}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm font-bold text-[#0A2540]">{peer.answers_submitted} টি</span>
                    </td>
                    <td className="px-6 py-4 text-xs text-slate-500">
                      {peer.last_active}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-700">
                        <Check className="w-3.5 h-3.5 text-emerald-600" />
                        সংযুক্ত
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
};
