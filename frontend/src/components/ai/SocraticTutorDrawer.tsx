/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Socratic AI Interface - Multi-Modal Streaming Tutor Drawer
 * TOPIC:     Server-Sent Events (SSE), KaTeX Formula Markdown, Voice Input, Vision Upload
 * FILE:      frontend/src/components/ai/SocraticTutorDrawer.tsx
 * PURPOSE:   Provides an interactive, floating Socratic tutor drawer accessible from any
 *            quiz or learning view across the Ogrojatra platform:
 *            1. Real-Time SSE Token Streaming: Uses fetch ReadableStream to render responses
 *               token-by-token with zero buffering.
 *            2. Mathematical Markdown & KaTeX: Integrates KaTeXRenderer for formula parsing
 *               ($...$ and $$...$$) alongside markdown headers, lists, and code blocks.
 *            3. Multi-Modal Vision: Accepts photos of handwritten math/physics problems,
 *               encodes to base64, and presents visual thumbnail preview.
 *            4. Bengali Voice Input: Uses Web Speech API (bn-BD) for hands-free audio questions.
 *            5. Human Pedagogical Vibe: Socratic inquiry, gentle guidance, and zero AI emojis.
 * AUDIENCE:  Frontend Developers, Accessibility Reviewers, AI Integration Engineers
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 Level AA (48px targets), Strict Zero-Emoji
 * ========================================================================================
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  Sparkles, 
  Send, 
  Mic, 
  MicOff, 
  Image as ImageIcon, 
  X, 
  RotateCcw, 
  HelpCircle, 
  ChevronRight, 
  AlertCircle,
  FileText
} from 'lucide-react';
import { KaTeXRenderer } from '../quiz/katex-renderer';

export interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  imageBase64?: string;
  timestamp: string;
  isStreaming?: boolean;
}

export interface SocraticTutorDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  subject?: string;
  currentQuestionStem?: string;
}

const QUICK_SOCRATIC_PROMPTS = [
  'এই সমস্যাটির প্রথম যৌক্তিক ধাপ কী হতে পারে?',
  'আমাকে একটি সহজ ক্লু বা সংকেত দিয়ে সাহায্য করুন',
  'আমার চিন্তা বা সমীকরণে কোনো ভুল আছে কি?',
  'বাস্তব জীবনের উদাহরণ দিয়ে এই সূত্রটি ব্যাখ্যা করুন'
];

export const SocraticTutorDrawer: React.FC<SocraticTutorDrawerProps> = ({
  isOpen,
  onClose,
  subject = 'physics',
  currentQuestionStem
}) => {
  const [sessionId, setSessionId] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState<string>('');
  const [isStreaming, setIsStreaming] = useState<boolean>(false);
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [speechError, setSpeechError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const recognitionRef = useRef<any>(null);

  // Initialize or restore session ID
  useEffect(() => {
    let storedSession = typeof window !== 'undefined' ? localStorage.getItem('ogrojatra_socratic_session') : null;
    if (!storedSession) {
      storedSession = `soc_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
      if (typeof window !== 'undefined') {
        localStorage.setItem('ogrojatra_socratic_session', storedSession);
      }
    }
    setSessionId(storedSession);

    // Initial greeting message in authentic Bengali (strict zero emoji)
    setMessages([
      {
        id: 'msg_welcome',
        sender: 'assistant',
        text: 'আসসালামু আলাইকুম। আমি আপনার অগ্রযাত্রা সক্রেটিক শিক্ষক। সরাসরি উত্তর দেওয়া আমার লক্ষ্য নয়; বরং আপনি যাতে ধাপে ধাপে নিজে বিষয়টি বুঝতে ও সমাধান করতে পারেন, সেজন্য আমি আপনাকে দিকনির্দেশনা দেব।\n\nআপনি কোন বিষয় বা সমীকরণটি নিয়ে ভাবছেন? প্রয়োজনে আপনার খাতার ছবি আপলোড করতে পারেন বা মাইক্রোফোনে প্রশ্ন করতে পারেন।',
        timestamp: new Date().toLocaleTimeString('bn-BD', { hour: '2-digit', minute: '2-digit' })
      }
    ]);
  }, []);

  // Pre-fill question stem if opened from a specific quiz card
  useEffect(() => {
    if (currentQuestionStem && isOpen) {
      setInputValue(`এই প্রশ্নটি বুঝতে পারছি না: "${currentQuestionStem}"। আমাকে প্রথম পদক্ষেপটি বুঝিয়ে দিন।`);
    }
  }, [currentQuestionStem, isOpen]);

  // Scroll to bottom on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isStreaming]);

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Handle Speech Recognition (Web Speech API)
  const toggleSpeechRecognition = useCallback(() => {
    if (isRecording) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsRecording(false);
      return;
    }

    setSpeechError(null);
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setSpeechError('আপনার ব্রাউজারে স্পিচ রিকগনিশন সমর্থন করে না। ক্রোম বা এজ ব্রাউজার ব্যবহার করুন।');
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = 'bn-BD';
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => {
        setIsRecording(true);
      };

      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
          setInputValue((prev) => (prev ? `${prev} ${transcript}` : transcript));
        }
      };

      recognition.onerror = (event: any) => {
        setIsRecording(false);
        setSpeechError(`ভয়েস রিকগনিশনে ত্রুটি হয়েছে: ${event.error || 'অজানা ত্রুটি'}`);
      };

      recognition.onend = () => {
        setIsRecording(false);
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (err: any) {
      setIsRecording(false);
      setSpeechError('ভয়েস ইনপুট শুরু করতে সমস্যা হয়েছে।');
    }
  }, [isRecording]);

  // Handle Image Selection and Base64 Conversion
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      alert('অনুগ্রহ করে শুধুমাত্র ছবি ফাইল (PNG, JPG, WEBP) নির্বাচন করুন।');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert('ছবির আকার সর্বোচ্চ ৫ মেগাবাইট হতে পারবে।');
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        setSelectedImage(reader.result);
      }
    };
    reader.readAsDataURL(file);
  };

  // Reset conversation session
  const handleResetSession = async () => {
    const newSession = `soc_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    setSessionId(newSession);
    if (typeof window !== 'undefined') {
      localStorage.setItem('ogrojatra_socratic_session', newSession);
    }

    try {
      await fetch('/api/v1/socratic/sessions/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId })
      });
    } catch {
      // Ignore network reset errors
    }

    setMessages([
      {
        id: 'msg_welcome_reset',
        sender: 'assistant',
        text: 'কথোপকথন নতুন করে শুরু করা হয়েছে। আপনার নতুন সমস্যা বা প্রশ্নটি লিখুন।',
        timestamp: new Date().toLocaleTimeString('bn-BD', { hour: '2-digit', minute: '2-digit' })
      }
    ]);
    setSelectedImage(null);
  };

  // Dispatch message and read Server-Sent Events (SSE) stream
  const handleSendMessage = async (customQuery?: string) => {
    const textToSend = (customQuery || inputValue).trim();
    if (!textToSend && !selectedImage) return;
    if (isStreaming) return;

    const userMessageId = `user_${Date.now()}`;
    const assistantMessageId = `asst_${Date.now()}`;

    const userMsg: ChatMessage = {
      id: userMessageId,
      sender: 'user',
      text: textToSend,
      imageBase64: selectedImage || undefined,
      timestamp: new Date().toLocaleTimeString('bn-BD', { hour: '2-digit', minute: '2-digit' })
    };

    const initialAssistantMsg: ChatMessage = {
      id: assistantMessageId,
      sender: 'assistant',
      text: '',
      timestamp: new Date().toLocaleTimeString('bn-BD', { hour: '2-digit', minute: '2-digit' }),
      isStreaming: true
    };

    setMessages((prev) => [...prev, userMsg, initialAssistantMsg]);
    setInputValue('');
    const currentImg = selectedImage;
    setSelectedImage(null);
    setIsStreaming(true);

    try {
      // POST endpoint to handle large base64 image streams cleanly
      const response = await fetch('/api/v1/socratic/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream'
        },
        body: JSON.stringify({
          session_id: sessionId,
          query: textToSend,
          image_base64: currentImg,
          subject: subject
        })
      });

      if (!response.ok || !response.body) {
        throw new Error(`HTTP Error ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let accumulatedText = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const rawJson = line.substring(6).trim();
            if (!rawJson) continue;

            try {
              const eventData = JSON.parse(rawJson);
              if (eventData.token) {
                accumulatedText += eventData.token;
                setMessages((prev) =>
                  prev.map((msg) =>
                    msg.id === assistantMessageId
                      ? { ...msg, text: accumulatedText }
                      : msg
                  )
                );
              }
              if (eventData.done) {
                setIsStreaming(false);
              }
            } catch {
              // Parse error handling for partial JSON chunks
            }
          }
        }
      }

      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMessageId
            ? { ...msg, text: accumulatedText, isStreaming: false }
            : msg
        )
      );
    } catch (err) {
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMessageId
            ? {
                ...msg,
                text: 'অনলাইন সংযোগে সমস্যা দেখা দিয়েছে। আপনার প্রশ্নটি সংক্ষেপে পুনরায় জিজ্ঞাসা করুন।',
                isStreaming: false
              }
            : msg
        )
      );
    } finally {
      setIsStreaming(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-label="সক্রেটিক এআই টিউটর ড্রোয়ার"
      className="fixed inset-0 z-50 overflow-hidden"
    >
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50 transition-opacity"
        onClick={onClose}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-0 sm:pl-10">
        <div className="w-screen max-w-xl bg-[var(--bg-surface)] border-l border-[var(--border-subtle)] shadow-2xl flex flex-col h-full">
          
          {/* Header */}
          <div className="px-5 py-4 border-b border-[var(--border-subtle)] flex items-center justify-between bg-[var(--bg-surface-elevated)]">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-[var(--color-brand)]/10 text-[var(--color-brand)] flex items-center justify-center border border-[var(--color-brand)]/20">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-base font-semibold text-[var(--text-main)] flex items-center space-x-2">
                  <span>অগ্রযাত্রা সক্রেটিক শিক্ষক</span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-[var(--color-brand-subtle)] text-[var(--color-brand)] font-medium">
                    লাইভ গাইড
                  </span>
                </h2>
                <p className="text-xs text-[var(--text-muted)]">
                  ধাপে ধাপে বিশ্লেষণ ও আত্মবিশ্বাস অর্জনের ডিজিটাল সঙ্গী
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-1">
              <button
                type="button"
                onClick={handleResetSession}
                title="সেশন নতুন করে শুরু করুন"
                aria-label="কথোপকথন রিসেট করুন"
                className="p-2.5 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-surface)] transition-colors min-h-[44px] min-w-[44px] flex items-center justify-center"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
              <button
                type="button"
                onClick={onClose}
                aria-label="ড্রোয়ার বন্ধ করুন"
                className="p-2.5 rounded-lg text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-surface)] transition-colors min-h-[44px] min-w-[44px] flex items-center justify-center"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Quick Prompt Suggestions */}
          <div className="px-4 py-2.5 bg-[var(--bg-surface)] border-b border-[var(--border-subtle)] overflow-x-auto whitespace-nowrap scrollbar-none flex space-x-2">
            {QUICK_SOCRATIC_PROMPTS.map((promptText, idx) => (
              <button
                key={idx}
                type="button"
                disabled={isStreaming}
                onClick={() => handleSendMessage(promptText)}
                className="inline-flex items-center space-x-1.5 px-3 py-1.5 text-xs rounded-full bg-[var(--bg-surface-elevated)] border border-[var(--border-subtle)] text-[var(--text-muted)] hover:text-[var(--color-brand)] hover:border-[var(--color-brand)]/40 transition-colors shrink-0 disabled:opacity-50 min-h-[36px]"
              >
                <HelpCircle className="w-3.5 h-3.5" />
                <span>{promptText}</span>
              </button>
            ))}
          </div>

          {/* Chat Messages Body */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div
                  className={`max-w-[88%] rounded-2xl p-4 shadow-sm ${
                    msg.sender === 'user'
                      ? 'bg-[var(--color-brand)] text-[var(--color-brand-contrast)] rounded-tr-sm'
                      : 'bg-[var(--bg-surface-elevated)] text-[var(--text-main)] border border-[var(--border-subtle)] rounded-tl-sm'
                  }`}
                >
                  {/* Attached Image Thumbnail */}
                  {msg.imageBase64 && (
                    <div className="mb-3 rounded-lg overflow-hidden border border-black/10 max-h-48">
                      <img
                        src={msg.imageBase64}
                        alt="হাতে লেখা প্রশ্নের স্ন্যাপশট"
                        className="w-full h-auto object-cover"
                      />
                    </div>
                  )}

                  {/* Message Content rendered with KaTeX */}
                  <div className="text-sm leading-relaxed whitespace-pre-wrap font-normal">
                    <KaTeXRenderer content={msg.text} />
                    {msg.isStreaming && (
                      <span className="inline-block w-2 h-4 ml-1 bg-current animate-pulse align-middle" />
                    )}
                  </div>
                </div>

                <span className="text-[10px] text-[var(--text-subtle)] mt-1 px-1">
                  {msg.timestamp}
                </span>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Image Upload Thumbnail Preview Area */}
          {selectedImage && (
            <div className="px-4 py-2 border-t border-[var(--border-subtle)] bg-[var(--bg-surface-elevated)] flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <img
                  src={selectedImage}
                  alt="সংযুক্ত ছবি"
                  className="w-12 h-12 rounded object-cover border border-[var(--border-strong)]"
                />
                <span className="text-xs text-[var(--text-main)] font-medium">
                  হাতে লেখা প্রশ্নের ছবি যুক্ত হয়েছে
                </span>
              </div>
              <button
                type="button"
                onClick={() => setSelectedImage(null)}
                aria-label="ছবি বাতিল করুন"
                className="p-1.5 rounded text-[var(--text-muted)] hover:text-red-500"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Speech Error Banner */}
          {speechError && (
            <div className="px-4 py-1.5 bg-amber-500/10 text-amber-700 dark:text-amber-300 text-xs flex items-center space-x-2 border-t border-amber-500/20">
              <AlertCircle className="w-3.5 h-3.5 shrink-0" />
              <span>{speechError}</span>
            </div>
          )}

          {/* Input Footer */}
          <div className="p-4 border-t border-[var(--border-subtle)] bg-[var(--bg-surface)]">
            <div className="flex items-end space-x-2">
              {/* Image Upload Button */}
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="hidden"
                id="socratic-image-upload"
              />
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                title="হাতে লেখা প্রশ্নের ছবি আপলোড করুন"
                aria-label="ছবি আপলোড করুন"
                className="p-3 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-surface-elevated)] text-[var(--text-muted)] hover:text-[var(--color-brand)] hover:border-[var(--color-brand)] transition-colors min-h-[48px] min-w-[48px] flex items-center justify-center shrink-0"
              >
                <ImageIcon className="w-5 h-5" />
              </button>

              {/* Bengali Voice Recording Button */}
              <button
                type="button"
                onClick={toggleSpeechRecognition}
                title={isRecording ? 'ভয়েস ইনপুট বন্ধ করুন' : 'বাংলায় কথা বলে প্রশ্ন করুন'}
                aria-label={isRecording ? 'ভয়েস বন্ধ করুন' : 'বাংলায় কথা বলুন'}
                className={`p-3 rounded-xl border transition-all min-h-[48px] min-w-[48px] flex items-center justify-center shrink-0 ${
                  isRecording
                    ? 'bg-red-500/10 text-red-600 border-red-500 animate-pulse'
                    : 'border-[var(--border-subtle)] bg-[var(--bg-surface-elevated)] text-[var(--text-muted)] hover:text-[var(--color-brand)] hover:border-[var(--color-brand)]'
                }`}
              >
                {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
              </button>

              {/* Text Input Area */}
              <div className="flex-1 relative">
                <textarea
                  ref={inputRef}
                  rows={2}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSendMessage();
                    }
                  }}
                  placeholder="আপনার প্রশ্ন বা সমীকরণটি লিখুন... (Enter চাপলে সেন্ড হবে)"
                  className="w-full px-3.5 py-2.5 text-sm rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-surface-elevated)] text-[var(--text-main)] placeholder-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--focus-ring)] resize-none"
                />
              </div>

              {/* Send Button */}
              <button
                type="button"
                disabled={(!inputValue.trim() && !selectedImage) || isStreaming}
                onClick={() => handleSendMessage()}
                title="বার্তা পাঠান"
                aria-label="বার্তা পাঠান"
                className="p-3 rounded-xl bg-[var(--color-brand)] text-[var(--color-brand-contrast)] hover:opacity-90 transition-opacity disabled:opacity-40 disabled:cursor-not-allowed min-h-[48px] min-w-[48px] flex items-center justify-center shrink-0"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};
