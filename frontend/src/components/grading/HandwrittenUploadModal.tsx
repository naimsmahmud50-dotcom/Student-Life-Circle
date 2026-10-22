/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Handwritten Script OCR & Submission
 * TOPIC:     Camera Snapshot & High-Contrast Exam Script Ingestion Modal
 * FILE:      frontend/src/components/grading/HandwrittenUploadModal.tsx
 * PHASE:     Phase 103 - Handwritten Script OCR & Step-by-Step Rubric Grader
 * PURPOSE:   Provides mobile-first camera capture and image upload with real-time
 *            contrast/binarization enhancement for rural mobile low-light photos,
 *            NCTB problem selection, and tactile submission controls.
 * STANDARDS: UI/UX Pro Max, OWASP ASVS L2, Zero-Emoji, Human-Centric
 */

import React, { useState, useRef } from 'react';
import {
  Camera,
  UploadCloud,
  Sliders,
  CheckCircle2,
  X,
  FileText,
  Sparkles,
  RefreshCw,
  ArrowRight,
  Eye,
  ShieldCheck
} from 'lucide-react';

export interface HandwrittenUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmitScript: (payload: { questionId: string; imageBase64: string; contrastLevel: number }) => void;
  questionId?: string;
  problemTitle?: string;
  className?: string;
}

export const HandwrittenUploadModal: React.FC<HandwrittenUploadModalProps> = ({
  isOpen,
  onClose,
  onSubmitScript,
  questionId = 'q-physics-projectile-01',
  problemTitle = 'প্রক্ষেপকের সর্বাধিক উচ্চতা নির্ণয় (HSC পদার্থবিজ্ঞান)',
  className = ''
}) => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [contrastLevel, setContrastLevel] = useState<number>(120);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        setSelectedImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSimulateSample = () => {
    // Generates a mock handwritten math answer sample for instant testing
    const sampleCanvas = document.createElement('canvas');
    sampleCanvas.width = 600;
    sampleCanvas.height = 360;
    const ctx = sampleCanvas.getContext('2d');
    if (ctx) {
      // Paper background with ruled lines
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 600, 360);
      ctx.strokeStyle = '#E2E8F0';
      ctx.lineWidth = 1;
      for (let y = 40; y < 360; y += 32) {
        ctx.beginPath();
        ctx.moveTo(30, y);
        ctx.lineTo(570, y);
        ctx.stroke();
      }
      // Margin line
      ctx.strokeStyle = '#FECACA';
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(80, 20);
      ctx.lineTo(80, 340);
      ctx.stroke();

      // Simulated handwriting
      ctx.fillStyle = '#1E3A8A';
      ctx.font = 'bold 16px "Hind Siliguri", sans-serif';
      ctx.fillText('ধাপ ১: সূত্রানুযায়ী, H = (u² sin²θ) / (2g)', 95, 65);
      ctx.fillText('ধাপ ২: দেওয়া আছে, u = 40 m/s, θ = 30°, g = 9.8 m/s²', 95, 125);
      ctx.fillText('ধাপ ৩: H = (40² × sin²30°) / (2 × 9.8)', 95, 185);
      ctx.fillText('      = (1600 × 0.25) / 19.6 = 400 / 19.6', 95, 225);
      ctx.fillText('ধাপ ৪: উত্তর: H = 20.4 m', 95, 290);
    }
    setSelectedImage(sampleCanvas.toDataURL('image/png'));
  };

  const handleSubmit = () => {
    if (!selectedImage) return;
    setIsSubmitting(true);
    setTimeout(() => {
      setIsSubmitting(false);
      onSubmitScript({
        questionId,
        imageBase64: selectedImage,
        contrastLevel
      });
      onClose();
    }, 1000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 animate-in fade-in select-none font-bengali">
      <div
        className={`relative w-full max-w-xl p-6 sm:p-8 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200/80 dark:border-slate-800/80 shadow-2xl space-y-6 ${className}`}
      >
        {/* Header */}
        <div className="flex items-start justify-between gap-4 pb-2 border-b border-slate-100 dark:border-slate-800">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold text-blue-600 dark:text-blue-400 uppercase tracking-wider mb-1">
              <Camera className="w-4 h-4" strokeWidth={1.75} />
              <span>হাতে লেখা খাতা স্ক্যানার (Handwritten OCR)</span>
            </div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-900 dark:text-white font-display">
              {problemTitle}
            </h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-2 rounded-full text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            title="বন্ধ করুন"
          >
            <X className="w-5 h-5" strokeWidth={1.75} />
          </button>
        </div>

        {/* Upload Container: Dashed drag-and-drop zone */}
        {!selectedImage ? (
          <div
            onClick={() => fileInputRef.current?.click()}
            className="group cursor-pointer border-2 border-dashed border-blue-300 dark:border-blue-800 hover:border-blue-500 rounded-3xl bg-blue-50/30 hover:bg-blue-50/60 dark:bg-slate-800/30 dark:hover:bg-slate-800/60 p-8 sm:p-10 flex flex-col items-center justify-center text-center transition-all duration-200 space-y-3"
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              capture="environment"
              onChange={handleFileChange}
              className="hidden"
            />
            <div className="w-16 h-16 rounded-3xl bg-blue-600/10 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-105 transition-transform shadow-sm">
              <UploadCloud className="w-8 h-8" strokeWidth={1.75} />
            </div>
            <div>
              <p className="text-base font-bold text-slate-900 dark:text-white">
                উত্তরপত্রের ছবি ড্র্যাগ করুন বা ক্লিক করে আপলোড করুন
              </p>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                মোবাইল ক্যামেরা দিয়ে সরাসরি খাতার স্পষ্ট ছবি তুলুন (JPG, PNG, WebP)
              </p>
            </div>

            <div className="pt-2">
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleSimulateSample();
                }}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-xs font-semibold hover:bg-blue-600 hover:text-white transition-all shadow-sm"
              >
                <Sparkles className="w-3.5 h-3.5" strokeWidth={1.75} />
                <span>নমুনা খাতা দিয়ে তাৎক্ষণিক পরীক্ষা করুন</span>
              </button>
            </div>
          </div>
        ) : (
          /* Preview with Contrast Slider for Rural Mobile Optimization */
          <div className="space-y-4">
            <div className="relative rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-700 bg-slate-950 flex items-center justify-center max-h-64">
              <img
                src={selectedImage}
                alt="হাতে লেখা খাতার প্রিভিউ"
                style={{ filter: `contrast(${contrastLevel}%)` }}
                className="max-h-64 object-contain transition-all duration-150"
              />
              <button
                type="button"
                onClick={() => setSelectedImage(null)}
                className="absolute top-3 right-3 p-1.5 rounded-full bg-slate-900/80 text-white hover:bg-rose-600 transition-colors shadow-md"
                title="ছবি পরিবর্তন করুন"
              >
                <RefreshCw className="w-4 h-4" strokeWidth={1.75} />
              </button>
            </div>

            {/* Contrast Adjustment Slider */}
            <div className="p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 space-y-1.5">
              <div className="flex items-center justify-between text-xs text-slate-600 dark:text-slate-300">
                <span className="flex items-center gap-1.5 font-semibold">
                  <Sliders className="w-3.5 h-3.5 text-blue-500" strokeWidth={1.75} />
                  <span>কালি স্পষ্টীকরণ (Binarization & Contrast):</span>
                </span>
                <span className="font-numeric font-bold text-blue-600 dark:text-blue-400">
                  {contrastLevel}%
                </span>
              </div>
              <input
                type="range"
                min="100"
                max="200"
                value={contrastLevel}
                onChange={(e) => setContrastLevel(Number(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                স্বল্প আলোতে তোলা খাতার হালকা বলপেন লেখাকে কৃত্রিম বুদ্ধিমত্তা সহজে পড়তে পারবে।
              </p>
            </div>
          </div>
        )}

        {/* Footer Actions */}
        <div className="flex items-center justify-between gap-3 pt-2 border-t border-slate-100 dark:border-slate-800">
          <div className="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
            <ShieldCheck className="w-4 h-4 text-emerald-500" strokeWidth={1.75} />
            <span>NCTB ৪-ধাপীয় মার্কিং রুব্রিক প্রযোজ্য</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2.5 rounded-2xl border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-sm font-semibold hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
            >
              বাতিল
            </button>
            <button
              type="button"
              onClick={handleSubmit}
              disabled={!selectedImage || isSubmitting}
              className="px-6 py-2.5 rounded-2xl bg-blue-600 text-white font-semibold text-sm shadow-[0_4px_0_0_#1D4ED8] hover:shadow-[0_2px_0_0_#1D4ED8] active:translate-y-1 active:shadow-none transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1.5"
            >
              <FileText className="w-4 h-4" strokeWidth={1.75} />
              <span>{isSubmitting ? 'খাতা বিশ্লেষণ হচ্ছে...' : 'খাতা জমা দিন'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
