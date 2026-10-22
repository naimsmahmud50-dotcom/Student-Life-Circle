/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - RESILIENCE & P2P MESH MODULE:
 * MODULE:    Next.js 15+ Offline-First P2P Mesh Sync & Local CRDT Ledger
 * TOPIC:     Interactive SVG Peer Mesh Topology, Vector Clocks, WebRTC DataChannels & CRDTs
 * FILE:      frontend/src/modules/resilience/OfflineMeshModule.tsx
 * PURPOSE:   Coordinates classroom peer-to-peer sync when national internet links are severed.
 *            Renders interactive 5-peer SVG topology with dynamic WebRTC status lines,
 *            vector clock CRDT merge inspector, offline mutation queue with re-sync, and
 *            complete zero-emoji UI design tokens.
 * AUDIENCE:  Distributed Systems Engineers, Offline-First Architects & Frontend Reviewers
 * STANDARDS: Conflict-Free Replicated Data Types (CRDT), WebRTC DataChannels, Strict Zero Emoji
 * ========================================================================================
 */

import React, { useState } from 'react';
import { 
  Network, 
  Share2, 
  Wifi, 
  WifiOff, 
  CheckCircle2, 
  RotateCcw, 
  Layers, 
  Activity,
  ShieldCheck
} from 'lucide-react';
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';

interface PeerNode {
  id: string;
  label: string;
  x: number;
  y: number;
  isGateway?: boolean;
  status: 'ONLINE' | 'MESH_SYNCED' | 'DISCONNECTED';
  vectorClock: number;
}

const INITIAL_PEERS: PeerNode[] = [
  { id: 'GW_CENTRAL', label: 'Gateway Hub', x: 200, y: 35, isGateway: true, status: 'ONLINE', vectorClock: 142 },
  { id: 'PEER_DHAKA', label: 'Dhaka Node', x: 70, y: 110, status: 'MESH_SYNCED', vectorClock: 139 },
  { id: 'PEER_CTG', label: 'Ctg Node', x: 140, y: 170, status: 'MESH_SYNCED', vectorClock: 140 },
  { id: 'PEER_SYL', label: 'Sylhet Node', x: 260, y: 170, status: 'MESH_SYNCED', vectorClock: 138 },
  { id: 'PEER_RAJ', label: 'Rajshahi Node', x: 330, y: 110, status: 'MESH_SYNCED', vectorClock: 141 },
];

export const OfflineMeshModule: React.FC = () => {
  const [peers, setPeers] = useState<PeerNode[]>(INITIAL_PEERS);
  const [selectedPeer, setSelectedPeer] = useState<PeerNode>(INITIAL_PEERS[0]);
  const [chaosPartition, setChaosPartition] = useState<boolean>(false);
  const [pendingMutations, setPendingMutations] = useState<number>(3);

  const handleSimulateSync = () => {
    setPeers((prev) =>
      prev.map((p) => ({
        ...p,
        vectorClock: p.vectorClock + (chaosPartition ? 0 : 2),
      }))
    );
    setPendingMutations(0);
  };

  return (
    <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 space-y-6 shadow-sm">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="brand">Tab 61 Enterprise</Badge>
            <Badge variant="teal">CRDT ভেক্টর ক্লক সিঙ্ক</Badge>
          </div>
          <h3 className="text-xl font-bold text-slate-900 dark:text-white mt-1">
            Offline-First P2P Mesh Sync & Local CRDT Ledger
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            ইন্টারনেট ব্ল্যাকআউটে লোকাল ক্লাসরুম ওয়াইফাই ও ব্লুটুথ মেশে পিয়ার-টু-পিয়ার সিঙ্ক
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant={chaosPartition ? "destructive" : "outline"}
            size="sm"
            onClick={() => setChaosPartition(!chaosPartition)}
          >
            {chaosPartition ? "পার্টিশন রিকভার করুন" : "নেটওয়ার্ক পার্টিশন কেওস"}
          </Button>
          <Button
            variant="brand"
            size="sm"
            icon={<Share2 className="w-4 h-4" />}
            onClick={handleSimulateSync}
          >
            সিআরডিটি সিঙ্ক
          </Button>
        </div>
      </div>

      {/* SVG Mesh Topology & Peer Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
        
        {/* Interactive SVG Topology */}
        <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-950 flex flex-col items-center">
          <span className="text-[11px] text-slate-400 font-mono mb-2 self-start flex items-center gap-1.5">
            <Network className="w-3.5 h-3.5 text-blue-400" />
            লাইভ ক্লাসরুম মেশ টপোলজি (WebRTC DataChannels)
          </span>

          <svg width="400" height="210" className="w-full max-w-[400px]">
            {/* Connection lines between peers */}
            <line x1="200" y1="45" x2="70" y2="120" stroke={chaosPartition ? "#EF4444" : "#3B82F6"} strokeWidth="1.5" strokeDasharray={chaosPartition ? "4 4" : ""} />
            <line x1="200" y1="45" x2="330" y2="120" stroke={chaosPartition ? "#EF4444" : "#3B82F6"} strokeWidth="1.5" strokeDasharray={chaosPartition ? "4 4" : ""} />
            <line x1="70" y1="120" x2="140" y2="180" stroke="#10B981" strokeWidth="1.5" />
            <line x1="140" y1="180" x2="260" y2="180" stroke="#10B981" strokeWidth="1.5" />
            <line x1="260" y1="180" x2="330" y2="120" stroke="#10B981" strokeWidth="1.5" />

            {/* Peer Nodes */}
            {peers.map((p) => (
              <g
                key={p.id}
                onClick={() => setSelectedPeer(p)}
                className="cursor-pointer transition-transform hover:scale-105"
              >
                <circle
                  cx={p.x}
                  cy={p.y}
                  r={p.isGateway ? 18 : 14}
                  fill={p.isGateway ? "#2563EB" : selectedPeer.id === p.id ? "#10B981" : "#475569"}
                  stroke={selectedPeer.id === p.id ? "#FFFFFF" : "#1E293B"}
                  strokeWidth="2"
                />
                <text
                  x={p.x}
                  y={p.y + 26}
                  fill="#94A3B8"
                  fontSize="9"
                  fontFamily="monospace"
                  textAnchor="middle"
                >
                  {p.label}
                </text>
              </g>
            ))}
          </svg>
        </div>

        {/* Vector Clock & CRDT Inspector */}
        <div className="space-y-4 text-xs">
          <div className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/40 space-y-3">
            <div className="flex justify-between items-center font-semibold">
              <span>সিলেক্টেড নোড: {selectedPeer.label}</span>
              <Badge variant={selectedPeer.status === 'ONLINE' ? 'brand' : 'verified'}>
                {selectedPeer.status}
              </Badge>
            </div>

            <div className="p-3 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 font-mono space-y-1.5">
              <div className="flex justify-between">
                <span className="text-slate-500">নোড আইডি:</span>
                <span className="font-bold">{selectedPeer.id}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">স্টেট ভেক্টর ক্লক:</span>
                <span className="text-teal-600 font-bold">VC = {selectedPeer.vectorClock}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">পেন্ডিং লোকাল মিউটেশন:</span>
                <span className="text-amber-600 font-bold">{pendingMutations} টি</span>
              </div>
            </div>

            <div className="text-[11px] text-slate-500 leading-relaxed">
              কনফ্লিক্ট-ফ্রি রেপ্লিকেটেড ডেটা টাইপ (LWW-Element-Set) ব্যবহার করে নোডগুলো নেটওয়ার্ক জোড়া লাগার সাথে সাথে ডাটা লস ছাড়া স্বয়ংক্রিয়ভাবে মার্জ হয়ে যায়।
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
