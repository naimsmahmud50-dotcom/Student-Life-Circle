/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - MODULE DIRECTORY & DUAL PERSPECTIVE:
 * MODULE:    Next.js 15+ 69 Enterprise Modules Directory & Perspective Controller
 * TOPIC:     Dual-Perspective Switcher (Student Core Hub vs All 69 Directory), Dynamic Search
 * FILE:      frontend/src/modules/ModuleDirectory.tsx
 * PURPOSE:   Provides seamless switching between the calm 5-module "Student Core Hub" and the
 *            full "All 69 Modules Enterprise Directory". Enables instant text search, category
 *            filtering, deep-linking, and on-demand dynamic rendering using DYNAMIC_MODULE_MAP
 *            without loading unused modules into the main bundle.
 * AUDIENCE:  Platform Architects, Navigation Reviewers & UI/UX Engineers
 * STANDARDS: UI/UX Pro Max, Cognitive Load Optimization, Strict Zero-Emoji Architecture
 * ========================================================================================
 */

import React, { useState } from 'react';
import { 
  Search, 
  Layers, 
  GraduationCap, 
  ShieldCheck, 
  Cpu, 
  Activity, 
  ArrowRight, 
  ExternalLink, 
  Sparkles, 
  Filter,
  CheckCircle2,
  X
} from 'lucide-react';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { MODULES_REGISTRY, ModuleMetadata, ModuleCategory, ModuleTier } from './registry';
import { DYNAMIC_MODULE_MAP } from './dynamic';

export const ModuleDirectory: React.FC = () => {
  const [perspective, setPerspective] = useState<ModuleTier>('core');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [activeModuleId, setActiveModuleId] = useState<string | null>(null);

  // Filter modules based on perspective, category, and search query
  const filteredModules = MODULES_REGISTRY.filter((mod) => {
    // In 'core' perspective, strictly show core tier modules (Tabs 1 - 5)
    if (perspective === 'core' && mod.tier !== 'core') {
      return false;
    }

    // Category filter
    if (selectedCategory !== 'ALL' && mod.category !== selectedCategory) {
      return false;
    }

    // Text search query
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchTitle = mod.title.toLowerCase().includes(q);
      const matchDesc = mod.description.toLowerCase().includes(q);
      const matchTags = mod.tags.some((t) => t.toLowerCase().includes(q));
      if (!matchTitle && !matchDesc && !matchTags) return false;
    }

    return true;
  });

  const ActiveComponent = activeModuleId ? DYNAMIC_MODULE_MAP[activeModuleId] : null;
  const activeModuleMeta = MODULES_REGISTRY.find((m) => m.id === activeModuleId);

  return (
    <div className="space-y-8">
      {/* Perspective Controller Card */}
      <div className="rounded-2xl border border-[#E5E2DA] dark:border-[#263147] bg-[#FDFCF9] dark:bg-[#111827] p-6 shadow-paper-md space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#E5E2DA] dark:border-[#263147] pb-4">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="brand">ওয়ার্কস্পেস পারস্পেক্টিভ</Badge>
              <Badge variant="teal">৬৯ এন্টারপ্রাইজ মডিউল আর্কিটেকচার</Badge>
            </div>
            <h2 className="text-2xl font-bold font-serif-bn text-[#0A2540] dark:text-[#E8EFF8] mt-1">
              {perspective === 'core' ? "শিক্ষার্থী কোর হাব (Student Core Hub)" : "অল ৬৯ এন্টারপ্রাইজ মডিউল ডিরেক্টরি"}
            </h2>
            <p className="text-xs text-[#5A687D] dark:text-[#94A3B8] mt-0.5">
              {perspective === 'core'
                ? "দৈনন্দিন পড়াশোনা ও পরীক্ষার জন্য শান্ত ও সরলীকৃত ৫টি কোর মডিউল ভিউ"
                : "৬৯টি স্বয়ংক্রিয় এন্টারপ্রাইজ রিসার্চ, স্টেম ল্যাব ও রেজিলিয়েন্স মডিউল ভিউ"}
            </p>
          </div>

          {/* Dual-Perspective Switcher Buttons */}
          <div className="flex items-center p-1 rounded-xl bg-[#F0EDE6] dark:bg-[#172030] border border-[#E2DDD3] dark:border-[#263147]">
            <button
              onClick={() => {
                setPerspective('core');
                setSelectedCategory('ALL');
              }}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
                perspective === 'core'
                  ? "bg-[#FDFCF9] dark:bg-[#1E293B] text-[#0A2540] dark:text-[#E8EFF8] shadow-paper-xs"
                  : "text-[#5A687D] dark:text-[#94A3B8] hover:text-[#0A2540] dark:hover:text-[#E8EFF8]"
              }`}
            >
              কোর হাব (Tabs 1-5)
            </button>
            <button
              onClick={() => setPerspective('enterprise')}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
                perspective === 'enterprise'
                  ? "bg-[#FDFCF9] dark:bg-[#1E293B] text-[#0A2540] dark:text-[#E8EFF8] shadow-paper-xs"
                  : "text-[#5A687D] dark:text-[#94A3B8] hover:text-[#0A2540] dark:hover:text-[#E8EFF8]"
              }`}
            >
              সমস্ত মডিউল (Tabs 1-69)
            </button>
          </div>
        </div>

        {/* Search & Category Filter Controls */}
        <div className="flex flex-col sm:flex-row gap-3 items-stretch sm:items-center justify-between">
          {/* Category Filter Pills (Visible when in enterprise perspective) */}
          {perspective === 'enterprise' ? (
            <div className="flex flex-wrap gap-1.5">
              {[
                { id: 'ALL', label: 'সকল ক্যাটাগরি' },
                { id: 'academic', label: 'একাডেমিক (Academic)' },
                { id: 'resilience', label: 'রেজিলিয়েন্স (Resilience)' },
                { id: 'stem-sandboxes', label: 'স্টেম ল্যাব (STEM Labs)' },
                { id: 'enterprise-cockpit', label: 'সিকিউরিটি ও ককপিট' },
              ].map((c) => (
                <button
                  key={c.id}
                  onClick={() => setSelectedCategory(c.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                    selectedCategory === c.id
                      ? "btn-tactile-primary text-white font-bold"
                      : "btn-tactile-outline text-[#5A687D] dark:text-[#CBD5E1]"
                  }`}
                >
                  {c.label}
                </button>
              ))}
            </div>
          ) : (
            <div className="text-xs text-[#5A687D] dark:text-[#94A3B8] font-medium">
              কোর হাব ফিল্টার: শুধুমাত্র দৈনন্দিন আবশ্যকীয় শিক্ষার্থী ফিচার প্রদর্শিত হচ্ছে
            </div>
          )}

          {/* Quick Search Input */}
          <div className="relative min-w-[260px]">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-[#5A687D] dark:text-[#94A3B8]" />
            <input
              type="text"
              placeholder="মডিউল নাম বা ট্যাগ খুঁজুন..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 text-xs rounded-xl bg-[#FAF8F5] dark:bg-[#0C1422] border border-[#E2DDD3] dark:border-[#2D3A52] text-[#1B2A4A] dark:text-[#E2E8F0] placeholder-[#5A687D] dark:placeholder-[#94A3B8] shadow-inner-bevel focus:outline-none focus:ring-2 focus:ring-[#0A2540] dark:focus:ring-[#3B82F6]"
            />
          </div>
        </div>
      </div>

      {/* Active Dynamic Module Embed Container */}
      {ActiveComponent && (
        <div className="space-y-3">
          <div className="flex justify-between items-center px-1">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              সক্রিয় ডাইনামিক কম্পোনেন্ট ভিউ: {activeModuleMeta?.title}
            </span>
            <Button
              variant="ghost"
              size="sm"
              icon={<X className="w-4 h-4" />}
              onClick={() => setActiveModuleId(null)}
            >
              ভিউ বন্ধ করুন
            </Button>
          </div>
          <ActiveComponent />
        </div>
      )}

      {/* Modules Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredModules.map((mod) => (
          <div
            key={mod.id}
            className={`p-5 rounded-2xl border bg-[#FDFCF9] dark:bg-[#111827] flex flex-col justify-between space-y-4 shadow-paper-xs hover:shadow-paper-md transition-all ${
              activeModuleId === mod.id
                ? "border-emerald-700 dark:border-emerald-500 ring-2 ring-emerald-600/20"
                : "border-[#E5E2DA] dark:border-[#263147]"
            }`}
          >
            <div className="space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-[#F0EDE6] dark:bg-[#172030] text-[#0A2540] dark:text-[#CBD5E1]">
                  Tab #{mod.tabNumber}
                </span>
                <Badge variant={mod.tier === 'core' ? 'brand' : 'teal'}>
                  {mod.badgeLabel || mod.category}
                </Badge>
              </div>

              <h4 className="text-base font-bold font-serif-bn text-[#0A2540] dark:text-[#E8EFF8] leading-snug">
                {mod.title}
              </h4>
              <p className="text-xs text-[#5A687D] dark:text-[#94A3B8] leading-relaxed">
                {mod.description}
              </p>

              {/* Tags */}
              <div className="flex flex-wrap gap-1 pt-1">
                {mod.tags.slice(0, 3).map((tag) => (
                  <span
                    key={tag}
                    className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[#FAF8F5] dark:bg-[#162032] text-[#5A687D] dark:text-[#94A3B8] border border-[#E2DDD3] dark:border-[#263147]"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </div>

            {/* Launch Action */}
            <div className="pt-2 border-t border-[#E5E2DA] dark:border-[#263147] flex items-center justify-between">
              {mod.tier === 'core' ? (
                <a
                  href={`/${mod.id}`}
                  className="text-xs font-bold text-emerald-800 dark:text-emerald-400 flex items-center gap-1 hover:underline"
                >
                  <span>পেজে যান</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              ) : DYNAMIC_MODULE_MAP[mod.id] ? (
                <Button
                  variant="primary"
                  size="sm"
                  fullWidth
                  icon={<ArrowRight className="w-4 h-4" />}
                  onClick={() => {
                    setActiveModuleId(mod.id);
                    window.scrollTo({ top: 350, behavior: 'smooth' });
                  }}
                >
                  {activeModuleId === mod.id ? "বর্তমানে সক্রিয়" : "মডিউল চালু করুন"}
                </Button>
              ) : (
                <span className="text-[11px] text-[#5A687D] dark:text-[#94A3B8] font-mono">
                  প্রিভিউ ইন্টিগ্রেশন সক্রিয়
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
