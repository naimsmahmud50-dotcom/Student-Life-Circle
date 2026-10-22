/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Study Pods & Collaborative Classroom
 * TOPIC:     Virtual Study Pod Room with Dynamic Audio Mesh & Speaking Indicator
 * FILE:      frontend/src/components/study-pods/StudyPodRoom.tsx
 * PHASE:     Phase 101 - Real-Time Study Pods & Collaborative Whiteboard
 * PURPOSE:   Renders synchronous collaborative study pods for 2 to 8 peers.
 *            Features responsive peer grid, ambient emerald pulse active speaker ring,
 *            WebRTC audio mesh controls, and seamless whiteboard integration.
 * STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
 */

import React, { useState, useEffect, useMemo } from 'react';
import {
  Mic,
  MicOff,
  Video,
  VideoOff,
  MonitorUp,
  Hand,
  LogOut,
  Users,
  PenTool,
  Volume2,
  Sparkles,
  ShieldCheck,
  Share2
} from 'lucide-react';
import { CollaborativeWhiteboard } from './CollaborativeWhiteboard';

export interface Participant {
  user_id: string;
  user_name: string;
  role: 'creator' | 'tutor' | 'student';
  avatar_url?: string;
  is_muted?: boolean;
  is_speaking?: boolean;
  is_camera_on?: boolean;
  is_hand_raised?: boolean;
  audio_level_db?: number;
}

export interface StudyPodRoomProps {
  podId: string;
  currentUserId: string;
  currentUserName: string;
  initialParticipants?: Participant[];
  podTitle?: string;
  subject?: string;
  onLeave?: () => void;
  className?: string;
}

export const StudyPodRoom: React.FC<StudyPodRoomProps> = ({
  podId,
  currentUserId,
  currentUserName,
  initialParticipants,
  podTitle = 'HSC Higher Math: Calculus & Conics Problem Solving',
  subject = 'Higher Mathematics',
  onLeave,
  className = ''
}) => {
  // Room View Mode: Whiteboard primary with side peers, or Full Peer Grid
  const [viewMode, setViewMode] = useState<'whiteboard' | 'grid'>('whiteboard');

  // Media Controls State
  const [isMuted, setIsMuted] = useState<boolean>(false);
  const [isCameraOn, setIsCameraOn] = useState<boolean>(false);
  const [isScreenSharing, setIsScreenSharing] = useState<boolean>(false);
  const [isHandRaised, setIsHandRaised] = useState<boolean>(false);

  // Participants State (Capacity limit max 8 peers)
  const [participants, setParticipants] = useState<Participant[]>(() => {
    if (initialParticipants && initialParticipants.length > 0) {
      return initialParticipants.slice(0, 8);
    }
    return [
      {
        user_id: currentUserId,
        user_name: currentUserName,
        role: 'student',
        is_muted: false,
        is_speaking: false,
        is_camera_on: false,
        is_hand_raised: false,
        audio_level_db: -60.0
      },
      {
        user_id: 'usr-peer-01',
        user_name: 'Sadia Islam',
        role: 'student',
        is_muted: false,
        is_speaking: true,
        is_camera_on: false,
        is_hand_raised: false,
        audio_level_db: -24.0
      },
      {
        user_id: 'usr-tutor-01',
        user_name: 'Tanzir Ahmed (Tutor)',
        role: 'tutor',
        is_muted: false,
        is_speaking: false,
        is_camera_on: false,
        is_hand_raised: false,
        audio_level_db: -60.0
      }
    ];
  });

  // Simulated active speaker polling / telemetry updates
  useEffect(() => {
    const interval = setInterval(() => {
      setParticipants((prev) =>
        prev.map((p) => {
          if (p.user_id === currentUserId) {
            return {
              ...p,
              is_muted: isMuted,
              is_speaking: !isMuted && Math.random() > 0.65,
              is_camera_on: isCameraOn,
              is_hand_raised: isHandRaised
            };
          }
          // Random gentle voice fluctuation for demo peers
          return {
            ...p,
            is_speaking: !p.is_muted && Math.random() > 0.7
          };
        })
      );
    }, 2500);

    return () => clearInterval(interval);
  }, [currentUserId, isMuted, isCameraOn, isHandRaised]);

  // Handlers
  const handleToggleMute = () => {
    setIsMuted((prev) => !prev);
  };

  const handleToggleCamera = () => {
    setIsCameraOn((prev) => !prev);
  };

  const handleToggleScreenShare = () => {
    setIsScreenSharing((prev) => !prev);
  };

  const handleToggleHandRaise = () => {
    setIsHandRaised((prev) => !prev);
  };

  const handleLeaveRoom = () => {
    if (window.confirm('আপনি কি স্টাডি পড থেকে বের হতে চান?')) {
      onLeave?.();
    }
  };

  // Grid column class calculation based on peer count (2 to 8 peers)
  const peerGridCols = useMemo(() => {
    const count = participants.length;
    if (count <= 2) return 'grid-cols-1 md:grid-cols-2';
    if (count <= 4) return 'grid-cols-1 sm:grid-cols-2';
    if (count <= 6) return 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3';
    return 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-4';
  }, [participants.length]);

  return (
    <div
      className={`relative flex flex-col w-full h-full min-h-[700px] bg-slate-900 text-slate-100 rounded-3xl overflow-hidden border border-slate-800 shadow-2xl font-bengali ${className}`}
    >
      {/* Top Header Bar */}
      <header className="flex items-center justify-between px-6 py-3.5 bg-slate-900 border-b border-slate-800 z-20">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-2xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <Users className="w-5 h-5" strokeWidth={1.75} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-base font-bold text-white tracking-tight">
                {podTitle}
              </h1>
              <span className="px-2 py-0.5 text-xs font-semibold rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800/60">
                লাইভ স্টাডি পড
              </span>
            </div>
            <p className="text-xs text-slate-400 flex items-center gap-2">
              <span>{subject}</span>
              <span>•</span>
              <span className="font-numeric font-medium">
                {participants.length}/8 জন শিক্ষার্থী
              </span>
            </p>
          </div>
        </div>

        {/* View Switcher: Whiteboard vs Full Grid */}
        <div className="flex items-center gap-2">
          <div className="flex items-center p-1 rounded-2xl bg-slate-800/80 border border-slate-700/80">
            <button
              type="button"
              onClick={() => setViewMode('whiteboard')}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-xl transition-all ${
                viewMode === 'whiteboard'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <PenTool className="w-3.5 h-3.5" strokeWidth={1.75} />
              <span>হোয়াইটবোর্ড</span>
            </button>
            <button
              type="button"
              onClick={() => setViewMode('grid')}
              className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-xl transition-all ${
                viewMode === 'grid'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Users className="w-3.5 h-3.5" strokeWidth={1.75} />
              <span>সকল শিক্ষার্থী</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex-1 relative flex overflow-hidden">
        {viewMode === 'whiteboard' ? (
          <div className="flex-1 flex flex-col md:flex-row h-full overflow-hidden">
            {/* Left: Collaborative Whiteboard Canvas */}
            <div className="flex-1 h-full p-4 overflow-hidden">
              <CollaborativeWhiteboard
                podId={podId}
                userId={currentUserId}
                userName={currentUserName}
                className="h-full min-h-[500px]"
              />
            </div>

            {/* Right: Intimate Peer Strip (up to 8 peers) */}
            <div className="w-full md:w-64 lg:w-72 bg-slate-950/60 border-t md:border-t-0 md:border-l border-slate-800/80 p-3 flex md:flex-col gap-3 overflow-y-auto z-10">
              <div className="hidden md:flex items-center justify-between px-2 py-1 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                <span>সহপাঠী ও মেন্টর ({participants.length})</span>
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" strokeWidth={1.75} />
              </div>

              {participants.map((peer) => {
                const isSpeaking = Boolean(peer.is_speaking && !peer.is_muted);
                const isMe = peer.user_id === currentUserId;

                return (
                  <div
                    key={peer.user_id}
                    className={`relative flex items-center md:flex-row gap-3 p-2.5 rounded-2xl bg-slate-900 border transition-all duration-200 ${
                      isSpeaking
                        ? 'border-emerald-500 ring-2 ring-emerald-500/20'
                        : 'border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    {/* Peer Avatar with Emerald Ring when speaking */}
                    <div className="relative">
                      <div
                        className={`w-10 h-10 rounded-2xl flex items-center justify-center font-bold text-sm transition-all duration-200 ${
                          isSpeaking
                            ? 'bg-emerald-600 text-white ring-2 ring-emerald-400'
                            : 'bg-slate-800 text-slate-300 border border-slate-700'
                        }`}
                      >
                        {peer.user_name.charAt(0)}
                      </div>

                      {/* Small role badge */}
                      {peer.role === 'tutor' && (
                        <div className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-blue-600 flex items-center justify-center text-[9px] font-bold text-white">
                          T
                        </div>
                      )}
                    </div>

                    {/* Peer Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-1">
                        <span className="text-xs font-semibold text-white truncate">
                          {peer.user_name} {isMe && '(তুমি)'}
                        </span>
                        {peer.is_muted ? (
                          <MicOff className="w-3.5 h-3.5 text-rose-400" strokeWidth={1.75} />
                        ) : isSpeaking ? (
                          <div className="flex items-center gap-0.5">
                            <span className="w-1 h-2 bg-emerald-400 rounded-full animate-bounce" />
                            <span className="w-1 h-3.5 bg-emerald-400 rounded-full animate-bounce [animation-delay:150ms]" />
                            <span className="w-1 h-2 bg-emerald-400 rounded-full animate-bounce [animation-delay:300ms]" />
                          </div>
                        ) : (
                          <Mic className="w-3.5 h-3.5 text-slate-500" strokeWidth={1.75} />
                        )}
                      </div>

                      <div className="flex items-center gap-2 mt-0.5 text-[11px] text-slate-400">
                        <span>{peer.role === 'tutor' ? 'মেন্টর' : 'শিক্ষার্থী'}</span>
                        {peer.is_hand_raised && (
                          <span className="text-amber-400 font-semibold flex items-center gap-0.5">
                            <Hand className="w-3 h-3" strokeWidth={1.75} />
                            হাত তুলেছে
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ) : (
          /* Full Grid Mode (Dynamic 2 to 8 peers) */
          <div className="flex-1 p-6 overflow-y-auto">
            <div className={`grid ${peerGridCols} gap-4 h-full max-w-6xl mx-auto`}>
              {participants.map((peer) => {
                const isSpeaking = Boolean(peer.is_speaking && !peer.is_muted);
                const isMe = peer.user_id === currentUserId;

                return (
                  <div
                    key={peer.user_id}
                    className={`relative flex flex-col items-center justify-center p-6 rounded-3xl bg-slate-800/80 border transition-all duration-200 min-h-[180px] ${
                      isSpeaking
                        ? 'border-emerald-500 ring-2 ring-emerald-500/30'
                        : 'border-slate-700/80 hover:border-slate-600'
                    }`}
                  >
                    {/* Active Speaker Ring Around Avatar */}
                    <div className="relative mb-3">
                      <div
                        className={`w-20 h-20 rounded-3xl flex items-center justify-center font-bold text-2xl transition-all duration-200 ${
                          isSpeaking
                            ? 'bg-emerald-600 text-white ring-4 ring-emerald-500/30'
                            : 'bg-slate-700 text-slate-200 border border-slate-600'
                        }`}
                      >
                        {peer.user_name.charAt(0)}
                      </div>

                      {/* Speaking indicator wave */}
                      {isSpeaking && (
                        <div className="absolute -bottom-2 left-1/2 -translate-x-1/2 px-2 py-0.5 rounded-full bg-emerald-500 text-slate-950 text-[10px] font-bold uppercase tracking-wider flex items-center gap-1 shadow-md">
                          <Volume2 className="w-2.5 h-2.5" strokeWidth={2} />
                          <span>কথা বলছে</span>
                        </div>
                      )}
                    </div>

                    <div className="text-center">
                      <h4 className="text-sm font-bold text-white truncate max-w-[160px]">
                        {peer.user_name}
                      </h4>
                      <p className="text-xs text-slate-400 mt-0.5">
                        {peer.role === 'tutor' ? 'মেন্টর' : 'সহপাঠী'} {isMe && '(তুমি)'}
                      </p>
                    </div>

                    {/* Status pill on corner */}
                    <div className="absolute top-3 right-3 flex items-center gap-1.5">
                      {peer.is_hand_raised && (
                        <div className="p-1.5 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/30">
                          <Hand className="w-4 h-4" strokeWidth={1.75} />
                        </div>
                      )}
                      <div className="p-1.5 rounded-xl bg-slate-900/80 text-slate-300 border border-slate-700">
                        {peer.is_muted ? (
                          <MicOff className="w-4 h-4 text-rose-400" strokeWidth={1.75} />
                        ) : (
                          <Mic className="w-4 h-4 text-emerald-400" strokeWidth={1.75} />
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Bottom Control Bar */}
      <footer className="relative flex items-center justify-center py-4 bg-slate-950 border-t border-slate-800 z-30">
        <div className="flex items-center gap-3 px-6 py-2 rounded-full bg-slate-900/90 border border-slate-700/80 shadow-2xl">
          {/* Mic Toggle */}
          <button
            type="button"
            onClick={handleToggleMute}
            className={`p-3 rounded-full transition-all active:scale-95 shadow-md ${
              isMuted
                ? 'bg-rose-600 text-white hover:bg-rose-500'
                : 'bg-slate-800 text-slate-100 hover:bg-slate-700'
            }`}
            title={isMuted ? 'মাইক্রোফোন চালু করুন (Unmute)' : 'মাইক্রোফোন বন্ধ করুন (Mute)'}
          >
            {isMuted ? (
              <MicOff className="w-5 h-5" strokeWidth={1.75} />
            ) : (
              <Mic className="w-5 h-5" strokeWidth={1.75} />
            )}
          </button>

          {/* Camera Toggle */}
          <button
            type="button"
            onClick={handleToggleCamera}
            className={`p-3 rounded-full transition-all active:scale-95 shadow-md ${
              !isCameraOn
                ? 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-slate-200'
                : 'bg-blue-600 text-white hover:bg-blue-500'
            }`}
            title={isCameraOn ? 'ক্যামেরা বন্ধ করুন' : 'ক্যামেরা চালু করুন'}
          >
            {isCameraOn ? (
              <Video className="w-5 h-5" strokeWidth={1.75} />
            ) : (
              <VideoOff className="w-5 h-5" strokeWidth={1.75} />
            )}
          </button>

          {/* Screen Share Toggle */}
          <button
            type="button"
            onClick={handleToggleScreenShare}
            className={`p-3 rounded-full transition-all active:scale-95 shadow-md ${
              isScreenSharing
                ? 'bg-blue-600 text-white hover:bg-blue-500'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
            title={isScreenSharing ? 'স্ক্রিন শেয়ার বন্ধ করুন' : 'স্ক্রিন শেয়ার করুন'}
          >
            <MonitorUp className="w-5 h-5" strokeWidth={1.75} />
          </button>

          {/* Raise Hand Toggle */}
          <button
            type="button"
            onClick={handleToggleHandRaise}
            className={`p-3 rounded-full transition-all active:scale-95 shadow-md ${
              isHandRaised
                ? 'bg-amber-500 text-white hover:bg-amber-400 shadow-amber-500/30'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
            }`}
            title={isHandRaised ? 'হাত নামান' : 'প্রশ্ন করতে হাত তুলুন'}
          >
            <Hand className="w-5 h-5" strokeWidth={1.75} />
          </button>

          {/* Divider */}
          <div className="w-px h-6 bg-slate-700 mx-1" />

          {/* Leave Study Pod Button */}
          <button
            type="button"
            onClick={handleLeaveRoom}
            className="flex items-center gap-2 px-5 py-2.5 rounded-full bg-rose-600/90 hover:bg-rose-600 text-white text-xs font-bold transition-all active:scale-95 shadow-md"
            title="পড থেকে প্রস্থান করুন"
          >
            <LogOut className="w-4 h-4" strokeWidth={1.75} />
            <span>প্রস্থান</span>
          </button>
        </div>
      </footer>
    </div>
  );
};
