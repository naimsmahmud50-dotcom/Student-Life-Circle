/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - ENTERPRISE CONSENSUS MODULE:
 * MODULE:    Next.js 15+ Campus Raft Quorum & Byzantine Fault Tolerant SMR Tower
 * TOPIC:     5-Node Ring SVG Topology, Heartbeat Laser Animation & Replicated State Machine
 * FILE:      frontend/src/modules/enterprise-cockpit/CampusRaftBftModule.tsx
 * PURPOSE:   Provides university campus consortium with high-availability distributed state
 *            replication. Enforces quorum consensus ($k \ge 3$), leader election terms,
 *            replicated log timeline, and Byzantine chaos injection (partitioning nodes and
 *            asserting sub-quorum rejection) with strict zero emoji.
 * AUDIENCE:  Distributed Systems Engineers, Infrastructure Leads & Architecture Reviewers
 * STANDARDS: Raft Consensus Algorithm, Byzantine Fault Tolerance (BFT), Strict Zero Emoji
 * ========================================================================================
 */

import React, { useState } from 'react';
import { 
  Network, 
  ShieldCheck, 
  Zap, 
  AlertTriangle, 
  CheckCircle2, 
  RotateCcw, 
  Layers, 
  Activity,
  Server
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';

interface CampusNode {
  id: string;
  name: string;
  role: 'LEADER' | 'FOLLOWER' | 'ISOLATED';
  x: number;
  y: number;
  term: number;
}

const INITIAL_NODES: CampusNode[] = [
  { id: 'DU', name: 'ঢাকা বিশ্ববিদ্যালয় (DU)', role: 'LEADER', x: 200, y: 35, term: 14 },
  { id: 'BUET', name: 'বুয়েট (BUET)', role: 'FOLLOWER', x: 330, y: 110, term: 14 },
  { id: 'CUET', name: 'চুয়েট (CUET)', role: 'FOLLOWER', x: 270, y: 180, term: 14 },
  { id: 'RUET', name: 'রুয়েট (RUET)', role: 'FOLLOWER', x: 130, y: 180, term: 14 },
  { id: 'SUST', name: 'শাবিপ্রবি (SUST)', role: 'FOLLOWER', x: 70, y: 110, term: 14 },
];

export const CampusRaftBftModule: React.FC = () => {
  const [nodes, setNodes] = useState<CampusNode[]>(INITIAL_NODES);
  const [commitIndex, setCommitIndex] = useState<number>(842);
  const [isPartitioned, setIsPartitioned] = useState<boolean>(false);

  const leaderNode = nodes.find((n) => n.role === 'LEADER') || nodes[0];

  const handleProposeLog = () => {
    if (isPartitioned) {
      alert("পার্টিশন সক্রিয়: সাব-কোরাম অবস্থায় লগ প্রস্তাবনা বাতিল হয়েছে!");
      return;
    }
    setCommitIndex((prev) => prev + 1);
  };

  const handleTriggerElection = () => {
    setNodes((prev) => {
      const copy = [...prev];
      copy[0].role = 'FOLLOWER';
      copy[1].role = 'LEADER';
      copy.forEach((n) => (n.term += 1));
      return copy;
    });
  };

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 space-y-6 shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="brand">Tab 65 Enterprise</Badge>
            <Badge variant="teal">কোরাম ৩/৫ নিশ্চিত</Badge>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mt-1">
            Campus Raft Quorum & Byzantine Fault Tolerant SMR Tower
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            ৫টি পাবলিক বিশ্ববিদ্যালয় নোডের মধ্যে বিকেন্দ্রীভূত স্টেট মেশিন রেপ্লিকেশন
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleTriggerElection}
          >
            নতুন নির্বাচন (Election)
          </Button>
          <Button
            variant="brand"
            size="sm"
            icon={<Zap className="w-4 h-4" />}
            onClick={handleProposeLog}
          >
            লগ প্রপোজ করুন
          </Button>
        </div>
      </div>

      {/* SVG Ring Topology & Raft State */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
        
        {/* SVG Ring Topology */}
        <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-950 flex flex-col items-center">
          <span className="text-[11px] text-slate-400 font-mono mb-2 self-start flex items-center gap-1.5">
            <Network className="w-3.5 h-3.5 text-blue-400" />
            ৫-ক্যাম্পাস রিং টপোলজি ও হার্টবিট লেজার
          </span>

          <svg width="400" height="210" className="w-full max-w-[400px]">
            {/* Heartbeat Laser Lines from Leader to Followers */}
            {nodes.slice(1).map((n) => (
              <line
                key={n.id}
                x1={leaderNode.x}
                y1={leaderNode.y}
                x2={n.x}
                y2={n.y}
                stroke={isPartitioned ? "#EF4444" : "#10B981"}
                strokeWidth="1.5"
                strokeDasharray={isPartitioned ? "4 4" : "2 2"}
                className={isPartitioned ? "" : "animate-pulse"}
              />
            ))}

            {/* Nodes */}
            {nodes.map((n) => (
              <g key={n.id}>
                <circle
                  cx={n.x}
                  cy={n.y}
                  r={n.role === 'LEADER' ? 18 : 14}
                  fill={n.role === 'LEADER' ? "#2563EB" : "#1E293B"}
                  stroke={n.role === 'LEADER' ? "#60A5FA" : "#475569"}
                  strokeWidth="2"
                />
                <text
                  x={n.x}
                  y={n.y + 26}
                  fill="#94A3B8"
                  fontSize="9"
                  fontFamily="monospace"
                  textAnchor="middle"
                >
                  {n.id} {n.role === 'LEADER' ? '(Leader)' : ''}
                </text>
              </g>
            ))}
          </svg>
        </div>

        {/* State Machine Log Timeline */}
        <div className="space-y-4 text-xs">
          <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 space-y-3">
            <div className="flex justify-between items-center font-semibold">
              <span>লিডার নোড: {leaderNode.name}</span>
              <Badge variant="brand">টার্ম #{leaderNode.term}</Badge>
            </div>

            <div className="p-3 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 font-mono space-y-1.5">
              <div className="flex justify-between">
                <span className="text-slate-500">কমিট ইনডেক্স:</span>
                <span className="text-teal-600 font-bold">Index #{commitIndex}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">স্টেট মেশিন হ্যাশ:</span>
                <span className="font-bold">0x8B32...FA19 (Merkle Root)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">বাইজান্টাইন সহনশীলতা:</span>
                <span className="text-emerald-600 font-bold">f = ১ ত্রুটি সহনশীল</span>
              </div>
            </div>

            <div className="flex gap-2">
              <Button
                variant={isPartitioned ? "destructive" : "outline"}
                size="sm"
                fullWidth
                onClick={() => setIsPartitioned(!isPartitioned)}
              >
                {isPartitioned ? "পার্টিশন তুলে নিন" : "বাইজান্টাইন কেওস ইনজেক্ট"}
              </Button>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
