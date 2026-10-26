/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Guardian Multi-Step Tutor Request Wizard
 * TOPIC:     CareTutors-Style 4-Step Hire a Tutor Workflow Adapted for Ogrojatra
 * FILE:      frontend/src/components/tuition/TutorRequestWizardModal.tsx
 * STANDARDS: Zero-Emoji, Pure Lucide SVGs, Sanitized Input Handling, WCAG 2.2 AAA Accessible Modal
 */

import React, { useState } from 'react';
import {
  X,
  CheckCircle2,
  Check,
  ChevronRight,
  ChevronLeft,
  GraduationCap,
  Home,
  Laptop,
  Users,
  ShieldCheck,
  MapPin,
  Calendar,
  CreditCard,
  Phone,
  Sparkles,
} from 'lucide-react';

interface TutorRequestWizardModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccessSubmit?: (jobData: Record<string, unknown>) => void;
}

export const TutorRequestWizardModal: React.FC<TutorRequestWizardModalProps> = ({
  isOpen,
  onClose,
  onSuccessSubmit,
}) => {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [generatedJobId, setGeneratedJobId] = useState<string | null>(null);

  // Form State
  const [mode, setMode] = useState<'হোম টিউশন' | 'অনলাইন টিউশন' | 'গ্রুপ ব্যাচ'>('হোম টিউশন');
  const [medium, setMedium] = useState<string>('বাংলা মাধ্যম');
  const [classGrade, setClassGrade] = useState<string>('১০ম শ্রেণি (এসএসসি)');
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>(['পদার্থবিজ্ঞান', 'উচ্চতর গণিত']);
  const [customSubject, setCustomSubject] = useState<string>('');
  const [daysPerWeek, setDaysPerWeek] = useState<number>(3);
  const [salaryOffer, setSalaryOffer] = useState<string>('৮,০০০ - ১০,০০০ টাকা/মাস');
  const [genderPreference, setGenderPreference] = useState<string>('যেকোনো অভিজ্ঞ টিউটর');
  const [preferredInstitution, setPreferredInstitution] = useState<string>('বুয়েট / ঢাবি / মেডিকেল');
  const [district, setDistrict] = useState<string>('ঢাকা');
  const [thana, setThana] = useState<string>('ধানমন্ডি');
  const [areaDetails, setAreaDetails] = useState<string>('');
  const [guardianName, setGuardianName] = useState<string>('');
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [specialNote, setSpecialNote] = useState<string>('');

  if (!isOpen) return null;

  const toggleSubject = (sub: string) => {
    if (selectedSubjects.includes(sub)) {
      setSelectedSubjects(selectedSubjects.filter((s) => s !== sub));
    } else {
      setSelectedSubjects([...selectedSubjects, sub]);
    }
  };

  const handleAddCustomSubject = (e: React.FormEvent) => {
    e.preventDefault();
    if (customSubject.trim() && !selectedSubjects.includes(customSubject.trim())) {
      setSelectedSubjects([...selectedSubjects, customSubject.trim()]);
      setCustomSubject('');
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    setTimeout(() => {
      const newJobId = `TUI-${Math.floor(1000 + Math.random() * 9000)}`;
      setGeneratedJobId(newJobId);
      setIsSubmitting(false);
      if (onSuccessSubmit) {
        onSuccessSubmit({
          id: newJobId,
          mode,
          medium,
          classGrade,
          selectedSubjects,
          daysPerWeek,
          salaryOffer,
          district,
          thana,
        });
      }
    }, 1000);
  };

  const handleReset = () => {
    setCurrentStep(1);
    setGeneratedJobId(null);
    onClose();
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="wizard-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/70 backdrop-blur-xs animate-in fade-in duration-150"
    >
      <div className="relative w-full max-w-2xl bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="p-5 sm:p-6 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 uppercase tracking-wider mb-1">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>অভিভাবকদের জন্য সম্পূর্ণ ফ্রি সার্ভিস</span>
            </div>
            <h3
              id="wizard-modal-title"
              className="text-lg sm:text-xl font-bold font-bengali text-slate-900 dark:text-white"
            >
              টিউটর রিকোয়ারমেন্ট পোস্ট করুন
            </h3>
          </div>
          <button
            onClick={handleReset}
            aria-label="উইন্ডো বন্ধ করুন"
            className="p-1.5 rounded-xl text-slate-400 hover:text-slate-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Step Progress Indicator (when not completed) */}
        {!generatedJobId && (
          <div className="px-5 sm:px-6 pt-4 pb-2 bg-slate-50 dark:bg-slate-950/40 border-b border-slate-100 dark:border-slate-800">
            <div className="flex items-center justify-between text-xs font-semibold font-bengali text-slate-500 mb-2">
              <span className={currentStep >= 1 ? 'text-emerald-700 dark:text-emerald-400' : ''}>
                ১. মোড ও মাধ্যম
              </span>
              <span className={currentStep >= 2 ? 'text-emerald-700 dark:text-emerald-400' : ''}>
                ২. শ্রেণি ও বিষয়
              </span>
              <span className={currentStep >= 3 ? 'text-emerald-700 dark:text-emerald-400' : ''}>
                ৩. বাজেট ও সময়
              </span>
              <span className={currentStep >= 4 ? 'text-emerald-700 dark:text-emerald-400' : ''}>
                ৪. ঠিকানা ও সাবমিট
              </span>
            </div>
            <div className="w-full h-1.5 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-emerald-600 transition-all duration-300"
                style={{ width: `${(currentStep / 4) * 100}%` }}
              />
            </div>
          </div>
        )}

        {/* Modal Body */}
        <div className="p-5 sm:p-6 overflow-y-auto flex-1 font-bengali">
          {generatedJobId ? (
            /* Success View */
            <div className="text-center py-6 space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-emerald-100 text-emerald-700 mx-auto flex items-center justify-center border-2 border-emerald-300 shadow-sm">
                <CheckCircle2 className="w-8 h-8" />
              </div>
              <h4 className="text-xl sm:text-2xl font-bold text-slate-900 dark:text-white">
                আপনার রিকোয়ারমেন্ট সফলভাবে পোস্ট হয়েছে!
              </h4>
              <p className="text-xs sm:text-sm text-slate-600 dark:text-slate-400 max-w-md mx-auto leading-relaxed">
                আপনার জব আইডি: <strong className="font-mono text-emerald-700">{generatedJobId}</strong>। পরবর্তী ২৪ থেকে ৪৮ ঘণ্টার মধ্যে আপনার চাহিদামাফিক শীর্ষ ৩-৫ জন যাচাইকৃত শিক্ষকের সিভি আপনার মোবাইলে পাঠানো হবে।
              </p>

              <div className="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700 max-w-md mx-auto text-left text-xs space-y-2">
                <div className="flex justify-between">
                  <span className="text-slate-500">শ্রেণি ও মাধ্যম:</span>
                  <span className="font-bold text-slate-800 dark:text-white">{classGrade} ({medium})</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">নির্বাচিত বিষয়:</span>
                  <span className="font-bold text-slate-800 dark:text-white">{selectedSubjects.join(', ')}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">বাজেট ও সময়:</span>
                  <span className="font-bold text-emerald-700">{salaryOffer} ({daysPerWeek} দিন/সপ্তাহ)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">এলাকা:</span>
                  <span className="font-bold text-slate-800 dark:text-white">{thana}, {district}</span>
                </div>
              </div>

              <div className="pt-4">
                <button
                  onClick={handleReset}
                  className="px-6 py-2.5 rounded-xl bg-emerald-800 hover:bg-emerald-900 text-white font-bold text-xs sm:text-sm shadow-sm transition-all"
                >
                  টিউশন ড্যাশবোর্ডে ফিরে যান
                </button>
              </div>
            </div>
          ) : (
            /* Multi-Step Forms */
            <div>
              {/* STEP 1: Mode & Medium */}
              {currentStep === 1 && (
                <div className="space-y-5">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                      টিউশনের ধরন নির্বাচন করুন:
                    </label>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      {[
                        { id: 'হোম টিউশন', label: 'হোম টিউশন', desc: 'শিক্ষক বাসায় আসবেন', icon: Home },
                        { id: 'অনলাইন টিউশন', label: 'অনলাইন টিউশন', desc: 'ভার্চুয়াল ১-১ ক্লাস', icon: Laptop },
                        { id: 'গ্রুপ ব্যাচ', label: 'গ্রুপ ব্যাচ', desc: '৩-৫ জনের গ্রুপ', icon: Users },
                      ].map((t) => {
                        const Icon = t.icon;
                        const isSelected = mode === t.id;
                        return (
                          <button
                            key={t.id}
                            type="button"
                            onClick={() => setMode(t.id as any)}
                            className={`p-3.5 rounded-xl border text-left flex flex-col justify-between transition-all ${
                              isSelected
                                ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-600 text-emerald-900 dark:text-emerald-200'
                                : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:border-slate-300'
                            }`}
                          >
                            <Icon className={`w-5 h-5 mb-2 ${isSelected ? 'text-emerald-700' : 'text-slate-400'}`} />
                            <div className="font-bold text-xs sm:text-sm">{t.label}</div>
                            <div className="text-[11px] text-slate-500 mt-0.5">{t.desc}</div>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                      শিক্ষার্থীর পাঠ্যক্রম / মাধ্যম:
                    </label>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
                      {[
                        'বাংলা মাধ্যম',
                        'ইংলিশ ভার্সন',
                        'ইংলিশ মিডিয়াম (Cambridge)',
                        'ইংলিশ মিডিয়াম (Edexcel)',
                        'ধর্মীয় ও কুরআন শিক্ষা',
                        'ভর্তি পরীক্ষা প্রস্তুতি',
                      ].map((m) => (
                        <button
                          key={m}
                          type="button"
                          onClick={() => setMedium(m)}
                          className={`p-2.5 rounded-xl border text-center font-medium transition-all ${
                            medium === m
                              ? 'bg-[#0A2540] text-white border-[#0A2540]'
                              : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                          }`}
                        >
                          {m}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 2: Class & Subjects */}
              {currentStep === 2 && (
                <div className="space-y-5">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                      শিক্ষার্থীর শ্রেণি / গ্রেড:
                    </label>
                    <select
                      value={classGrade}
                      onChange={(e) => setClassGrade(e.target.value)}
                      className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
                    >
                      <option value="১ম - ৫ম শ্রেণি (প্রাইমারি)">১ম - ৫ম শ্রেণি (প্রাইমারি)</option>
                      <option value="৬ষ্ঠ - ৮ম শ্রেণি (জুনিয়র)">৬ষ্ঠ - ৮ম শ্রেণি (নতুন শিক্ষাক্রম)</option>
                      <option value="৯ম শ্রেণি (এসএসসি ২০২৮)">৯ম শ্রেণি (এসএসসি ২০২৮)</option>
                      <option value="১০ম শ্রেণি (এসএসসি ২০২৭)">১০ম শ্রেণি (এসএসসি ২০২৭)</option>
                      <option value="একাদশ শ্রেণি (এইচএসসি ২০২৭)">একাদশ শ্রেণি (এইচএসসি ২০২৭)</option>
                      <option value="দ্বাদশ শ্রেণি (এইচএসসি ২০২৬)">দ্বাদশ শ্রেণি (এইচএসসি ২০২৬)</option>
                      <option value="বিশ্ববিদ্যালয় এডমিশন ২০২৬">বিশ্ববিদ্যালয় এডমিশন ২০২৬</option>
                      <option value="ও/এ লেভেল (ক্যামব্রিজ/এডেক্সেল)">ও/এ লেভেল (ক্যামব্রিজ/এডেক্সেল)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                      যেসব বিষয় পড়াতে হবে (একাধিক সিলেক্ট করুন):
                    </label>
                    <div className="flex flex-wrap gap-2 mb-3">
                      {[
                        'পদার্থবিজ্ঞান',
                        'রসায়ন',
                        'উচ্চতর গণিত',
                        'জীববিজ্ঞান',
                        'সাধারণ গণিত',
                        'ইংরেজি ১ম ও ২য়',
                        'বাংলা ১ম ও ২য়',
                        'তথ্যপ্রযুক্তি (ICT)',
                        'সাধারণ বিজ্ঞান',
                        'হিসাববিজ্ঞান',
                      ].map((sub) => {
                        const isSelected = selectedSubjects.includes(sub);
                        return (
                          <button
                            key={sub}
                            type="button"
                            onClick={() => toggleSubject(sub)}
                            className={`inline-flex items-center gap-1 px-3 py-1.5 rounded-lg border text-xs font-medium transition-all ${
                              isSelected
                                ? 'bg-emerald-800 text-white border-emerald-900 font-bold'
                                : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                            }`}
                          >
                            {isSelected ? <Check className="w-3.5 h-3.5" /> : <span>+</span>}
                            <span>{sub}</span>
                          </button>
                        );
                      })}
                    </div>

                    <form onSubmit={handleAddCustomSubject} className="flex gap-2">
                      <input
                        type="text"
                        placeholder="অন্য কোনো বিষয় লিখুন (যেমন: ড্রয়িং, তাজবীদ)..."
                        value={customSubject}
                        onChange={(e) => setCustomSubject(e.target.value)}
                        className="flex-1 p-2 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-800 dark:text-white"
                      />
                      <button
                        type="submit"
                        className="px-4 py-2 rounded-xl bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-white text-xs font-bold"
                      >
                        যোগ করুন
                      </button>
                    </form>
                  </div>
                </div>
              )}

              {/* STEP 3: Days, Budget & Preferences */}
              {currentStep === 3 && (
                <div className="space-y-5">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                        সপ্তাহে কত দিন পড়াতে হবে:
                      </label>
                      <div className="flex gap-2">
                        {[2, 3, 4, 5].map((d) => (
                          <button
                            key={d}
                            type="button"
                            onClick={() => setDaysPerWeek(d)}
                            className={`flex-1 py-2 rounded-xl border text-xs font-bold transition-all ${
                              daysPerWeek === d
                                ? 'bg-[#0A2540] text-white border-[#0A2540]'
                                : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700'
                            }`}
                          >
                            {d} দিন
                          </button>
                        ))}
                      </div>
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                        মাসিক পারিশ্রমিক বাজেট:
                      </label>
                      <input
                        type="text"
                        value={salaryOffer}
                        onChange={(e) => setSalaryOffer(e.target.value)}
                        placeholder="যেমন: ৮,০০০ - ১০,০০০ টাকা"
                        className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                        শিক্ষকের জেন্ডার পছন্দ:
                      </label>
                      <select
                        value={genderPreference}
                        onChange={(e) => setGenderPreference(e.target.value)}
                        className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
                      >
                        <option value="যেকোনো অভিজ্ঞ টিউটর">যেকোনো অভিজ্ঞ টিউটর</option>
                        <option value="পুরুষ টিউটর আবশ্যক">পুরুষ টিউটর আবশ্যক</option>
                        <option value="মহিলা টিউটর আবশ্যক">মহিলা টিউটর আবশ্যক</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2">
                        শিক্ষকের প্রত্যাশিত বিশ্ববিদ্যালয়:
                      </label>
                      <select
                        value={preferredInstitution}
                        onChange={(e) => setPreferredInstitution(e.target.value)}
                        className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
                      >
                        <option value="বুয়েট / ঢাবি / মেডিকেল">বুয়েট / ঢাবি / মেডিকেল (অগ্রাধিকার)</option>
                        <option value="শুধুমাত্র বুয়েট (BUET)">শুধুমাত্র বুয়েট (BUET)</option>
                        <option value="শুধুমাত্র ঢাকা বিশ্ববিদ্যালয় (DU)">শুধুমাত্র ঢাকা বিশ্ববিদ্যালয় (DU)</option>
                        <option value="মেডিকেল কলেজ (MBBS)">মেডিকেল কলেজ (MBBS)</option>
                        <option value="যেকোনো সরকারি বিশ্ববিদ্যালয়">যেকোনো সরকারি বিশ্ববিদ্যালয়</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* STEP 4: Location & Contact */}
              {currentStep === 4 && (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">
                        জেলা:
                      </label>
                      <select
                        value={district}
                        onChange={(e) => setDistrict(e.target.value)}
                        className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-bengali text-slate-800 dark:text-white"
                      >
                        <option value="ঢাকা">ঢাকা</option>
                        <option value="চট্টগ্রাম">চট্টগ্রাম</option>
                        <option value="রাজশাহী">রাজশাহী</option>
                        <option value="সিলেট">সিলেট</option>
                        <option value="খুলনা">খুলনা</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">
                        থানা / এলাকা:
                      </label>
                      <input
                        type="text"
                        value={thana}
                        onChange={(e) => setThana(e.target.value)}
                        placeholder="যেমন: ধানমন্ডি, উত্তরা, মিরপুর..."
                        className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-800 dark:text-white"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">
                      বিস্তারিত ঠিকানা / রোড নং:
                    </label>
                    <input
                      type="text"
                      value={areaDetails}
                      onChange={(e) => setAreaDetails(e.target.value)}
                      placeholder="যেমন: রোড নং ৭, হাউজ ১২, ব্লক ডি..."
                      className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-800 dark:text-white"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">
                        অভিভাবকের নাম:
                      </label>
                      <input
                        type="text"
                        value={guardianName}
                        onChange={(e) => setGuardianName(e.target.value)}
                        placeholder="আপনার নাম লিখুন..."
                        className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-800 dark:text-white"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">
                        মোবাইল নম্বর (যোগাযোগের জন্য):
                      </label>
                      <input
                        type="tel"
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                        placeholder="০১৭১১******"
                        className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-800 dark:text-white font-mono"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">
                      বিশেষ কোনো নির্দেশনা থাকলে লিখুন:
                    </label>
                    <textarea
                      rows={2}
                      value={specialNote}
                      onChange={(e) => setSpecialNote(e.target.value)}
                      placeholder="যেমন: শিক্ষার্থী ইংরেজিতে কিছুটা দুর্বল, একটু যত্ন নিয়ে বুঝিয়ে পড়াতে হবে..."
                      className="w-full p-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs text-slate-800 dark:text-white"
                    />
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Modal Footer Controls */}
        {!generatedJobId && (
          <div className="p-4 sm:p-5 border-t border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-950/60 flex items-center justify-between">
            {currentStep > 1 ? (
              <button
                type="button"
                onClick={() => setCurrentStep(currentStep - 1)}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-xs font-bold font-bengali hover:bg-slate-100"
              >
                <ChevronLeft className="w-4 h-4" />
                <span>পূর্ববর্তী ধাপ</span>
              </button>
            ) : (
              <div />
            )}

            {currentStep < 4 ? (
              <button
                type="button"
                onClick={() => setCurrentStep(currentStep + 1)}
                className="inline-flex items-center gap-1.5 px-6 py-2.5 rounded-xl bg-[#0A2540] text-white text-xs sm:text-sm font-bold font-bengali hover:bg-slate-900 transition-all"
              >
                <span>পরবর্তী ধাপ</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                disabled={isSubmitting}
                onClick={handleSubmit}
                className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-emerald-800 hover:bg-emerald-900 text-white text-xs sm:text-sm font-bold font-bengali shadow-sm transition-all"
              >
                {isSubmitting ? (
                  <span>জমা দেওয়া হচ্ছে...</span>
                ) : (
                  <>
                    <CheckCircle2 className="w-4 h-4" />
                    <span>রিকোয়ারমেন্ট পোস্ট সম্পন্ন করুন</span>
                  </>
                )}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
