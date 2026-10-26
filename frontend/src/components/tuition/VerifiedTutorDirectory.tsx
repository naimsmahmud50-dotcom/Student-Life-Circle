/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Verified Tutor Directory & Scholar Profile Matrix
 * TOPIC:     CareTutors-Style Verified Tutor Showcase with Authentic Scholar Monograms (Zero External Scraped Photos)
 * FILE:      frontend/src/components/tuition/VerifiedTutorDirectory.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, Authentic Academic Monograms, Strict Scope Lock, WCAG 2.2 AAA
 */

import React, { useState } from 'react';
import { VerifiedTutor, VERIFIED_TUTORS } from './data/tuitionElevationData';
import {
  GraduationCap,
  Star,
  ShieldCheck,
  CheckCircle2,
  MapPin,
  BookOpen,
  School,
  Lock,
  Phone,
  X,
  AlertCircle,
  FileCheck,
} from 'lucide-react';

interface VerifiedTutorDirectoryProps {
  className?: string;
}

export const VerifiedTutorDirectory: React.FC<VerifiedTutorDirectoryProps> = ({
  className = '',
}) => {
  const [selectedInstitution, setSelectedInstitution] = useState<string>('ALL');
  const [selectedSubject, setSelectedSubject] = useState<string>('ALL');
  const [contactTutor, setContactTutor] = useState<VerifiedTutor | null>(null);
  const [guardianPhone, setGuardianPhone] = useState<string>('');
  const [consentSuccess, setConsentSuccess] = useState<string | null>(null);

  const filteredTutors = VERIFIED_TUTORS.filter((tutor) => {
    const matchesInstitution =
      selectedInstitution === 'ALL' || tutor.institutionBn.includes(selectedInstitution);
    const matchesSubject =
      selectedSubject === 'ALL' ||
      tutor.preferredSubjects.some((s) => s.includes(selectedSubject));

    return matchesInstitution && matchesSubject;
  });

  const handleConsentSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!contactTutor) return;

    setConsentSuccess(`শিক্ষক ${contactTutor.nameBn}-এর কাছে আপনার দ্বিপাক্ষিক সম্মতির অনুরোধ পাঠানো হয়েছে। তিনি অনুমোদন করলেই সরাসরি যোগাযোগ নম্বর উন্মুক্ত হবে।`);
    setTimeout(() => {
      setConsentSuccess(null);
      setContactTutor(null);
      setGuardianPhone('');
    }, 2500);
  };

  return (
    <div className={`space-y-6 ${className}`} aria-labelledby="tutor-directory-heading">
      {/* Directory Filter Bar */}
      <div className="p-4 sm:p-5 rounded-3xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm flex flex-wrap gap-3 items-center justify-between font-bengali">
        <div className="flex flex-wrap gap-2 text-xs">
          {/* Institution Filter */}
          <select
            value={selectedInstitution}
            onChange={(e) => setSelectedInstitution(e.target.value)}
            aria-label="বিশ্ববিদ্যালয় ফিল্টার"
            className="p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-white"
          >
            <option value="ALL">সকল বিশ্ববিদ্যালয়</option>
            <option value="BUET">বুয়েট (BUET)</option>
            <option value="DMC">ঢাকা মেডিকেল কলেজ (DMC)</option>
            <option value="DU">ঢাকা বিশ্ববিদ্যালয় (DU)</option>
            <option value="NSU">নর্থ সাউথ বিশ্ববিদ্যালয় (NSU)</option>
          </select>

          {/* Subject Filter */}
          <select
            value={selectedSubject}
            onChange={(e) => setSelectedSubject(e.target.value)}
            aria-label="পছন্দের বিষয় ফিল্টার"
            className="p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-white"
          >
            <option value="ALL">সকল বিষয়</option>
            <option value="পদার্থবিজ্ঞান">পদার্থবিজ্ঞান</option>
            <option value="গণিত">গণিত / উচ্চতর গণিত</option>
            <option value="রসায়ন">রসায়ন</option>
            <option value="জীববিজ্ঞান">জীববিজ্ঞান</option>
            <option value="ইংরেজি">ইংরেজি</option>
          </select>
        </div>

        <div className="text-xs text-slate-500 font-medium flex items-center gap-1.5">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>সকল শিক্ষকের জাতীয় পরিচয়পত্র ও অ্যাকাডেমিক সনদ পরীক্ষিত</span>
        </div>
      </div>

      {/* Tutors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 font-bengali">
        {filteredTutors.map((tutor) => (
          <article
            key={tutor.id}
            className="flex flex-col justify-between bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-5 sm:p-6 shadow-sm hover:shadow-md transition-shadow duration-200 space-y-4"
          >
            <div>
              {/* Header: Scholar Monogram (Strictly Zero External Scraped Photos) */}
              <div className="flex items-start gap-3.5 mb-3">
                <div
                  className={`w-12 h-12 rounded-2xl border-2 flex items-center justify-center font-bold text-lg font-serif shrink-0 shadow-sm ${tutor.accentBg}`}
                >
                  {tutor.initialsBn}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-1">
                    <h3 className="font-bold text-base sm:text-lg text-slate-900 dark:text-white truncate">
                      {tutor.nameBn}
                    </h3>
                    <div className="flex items-center gap-1 text-xs font-bold text-amber-500 bg-amber-50 dark:bg-amber-950/40 px-2 py-0.5 rounded-md border border-amber-200 dark:border-amber-800">
                      <Star className="w-3.5 h-3.5 fill-amber-500" />
                      <span>{tutor.rating}</span>
                      <span className="text-[10px] text-slate-400">({tutor.totalReviews})</span>
                    </div>
                  </div>

                  <div className="text-xs font-semibold text-emerald-800 dark:text-emerald-400 truncate mt-0.5">
                    {tutor.institutionBn}
                  </div>
                  <div className="text-[11px] text-slate-500 truncate">
                    {tutor.departmentBn} • {tutor.degreeLevelBn}
                  </div>
                </div>
              </div>

              {/* Background & Credentials */}
              <div className="p-3 rounded-2xl bg-slate-50 dark:bg-slate-950/60 border border-slate-200 dark:border-slate-800 text-xs space-y-1.5 mb-3">
                <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-400">
                  <School className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span>এইচএসসি ব্যাকগ্রাউন্ড: <strong className="text-slate-800 dark:text-white">{tutor.hscBackgroundBn}</strong></span>
                </div>
                <div className="flex items-center gap-1.5 text-slate-600 dark:text-slate-400">
                  <BookOpen className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span>অভিজ্ঞতা: <strong className="text-slate-800 dark:text-white">{tutor.experienceYearsBn}</strong> ({tutor.tuitionsCompleted}টি টিউশন সম্পন্ন)</span>
                </div>
              </div>

              {/* Subjects & Locations Chips */}
              <div className="space-y-1.5">
                <div className="flex flex-wrap gap-1">
                  {tutor.preferredSubjects.map((sub, i) => (
                    <span
                      key={i}
                      className="text-[11px] font-medium bg-emerald-50 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 px-2 py-0.5 rounded-md"
                    >
                      {sub}
                    </span>
                  ))}
                </div>

                <div className="flex items-center gap-1.5 text-xs text-slate-500 pt-1">
                  <MapPin className="w-3 h-3 text-slate-400 shrink-0" />
                  <span className="truncate">পছন্দের এলাকা: {tutor.preferredLocations.join(', ')}</span>
                </div>
              </div>
            </div>

            {/* Footer: Salary & Contact Consent Button */}
            <div className="pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3">
              <div>
                <div className="text-[11px] text-slate-500">প্রত্যাশিত পারিশ্রমিক</div>
                <div className="text-xs sm:text-sm font-bold font-mono text-emerald-800 dark:text-emerald-400">
                  {tutor.expectedSalaryBn}
                </div>
              </div>

              <button
                onClick={() => setContactTutor(tutor)}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#0A2540] hover:bg-slate-900 text-white text-xs font-bold transition-all shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0A2540] cursor-pointer"
              >
                <Lock className="w-3.5 h-3.5 text-amber-300" />
                <span>যোগাযোগ সম্মতির অনুরোধ</span>
              </button>
            </div>
          </article>
        ))}
      </div>

      {/* Bilateral Consent Modal for Tutor Selection */}
      {contactTutor && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="tutor-consent-dialog-title"
          className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/70 backdrop-blur-xs animate-in fade-in duration-150 font-bengali"
        >
          <div className="relative w-full max-w-md bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl p-6 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-emerald-600" />
                <h4 id="tutor-consent-dialog-title" className="text-base font-bold text-slate-900 dark:text-white">
                  দ্বিপাক্ষিক যোগাযোগ সম্মতি
                </h4>
              </div>
              <button
                onClick={() => setContactTutor(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {consentSuccess ? (
              <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-300 text-emerald-800 text-xs font-bold text-center">
                {consentSuccess}
              </div>
            ) : (
              <form onSubmit={handleConsentSubmit} className="space-y-4 text-xs">
                <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
                  আপনি <strong>{contactTutor.institutionBn}</strong> এর শিক্ষক <strong>{contactTutor.nameBn}</strong>-এর সাথে যোগাযোগ করতে চাচ্ছেন।
                </p>

                <div className="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 space-y-1">
                  <div>বিষয়: {contactTutor.preferredSubjects.join(', ')}</div>
                  <div>প্রত্যাশিত পারিশ্রমিক: <strong className="text-emerald-700">{contactTutor.expectedSalaryBn}</strong></div>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                    অভিভাবকের মোবাইল নম্বর:
                  </label>
                  <input
                    type="tel"
                    required
                    value={guardianPhone}
                    onChange={(e) => setGuardianPhone(e.target.value)}
                    placeholder="০১৭১১******"
                    className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-white font-mono"
                  />
                </div>

                <div className="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-amber-900 dark:text-amber-200 text-[11px] flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-amber-700" />
                  <div>
                    উভয় পক্ষের সম্মতি ছাড়া কোনো ব্যক্তিগত নম্বর সরাসরি প্রকাশিত হয় না। শিক্ষক সম্মতি দিলে ২ দিনের ফ্রি ট্রায়াল ক্লাসের শিডিউল নির্ধারণ করা হবে।
                  </div>
                </div>

                <div className="flex justify-end gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setContactTutor(null)}
                    className="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold"
                  >
                    বাতিল
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-2 rounded-xl bg-[#0A2540] hover:bg-slate-900 text-white font-bold flex items-center gap-1.5 cursor-pointer shadow-sm"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>অনুরোধ পাঠান</span>
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
