import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import {
  User,
  Moon,
  Sun,
  Menu,
  X,
  ShoppingBag,
  Sparkles,
  BookOpen,
  GraduationCap,
  Layers,
  Swords,
  Users,
  Search,
  ChevronRight
} from 'lucide-react';

interface GoEduNavbarProps {
  onOpenSocraticDrawer?: () => void;
}

export const GoEduNavbar: React.FC<GoEduNavbarProps> = ({ onOpenSocraticDrawer }) => {
  const router = useRouter();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [savedCount, setSavedCount] = useState(2);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleDarkMode = () => {
    setIsDarkMode(prev => {
      const next = !prev;
      if (next) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      return next;
    });
  };

  const navItems = [
    { label: 'হোম', enLabel: 'Home', href: '/' },
    { label: 'কোর্সসমূহ', enLabel: 'Courses', href: '/courses' },
    { label: 'একাডেমিক হাব', enLabel: 'Bundles', href: '/academic-hub' },
    { label: 'সক্রেটিক এআই', enLabel: 'AI Tutor', href: '/socratic/solver' },
    { label: 'লাইভ চ্যালেঞ্জ', enLabel: 'Live Challenge', href: '/live-challenge' },
    { label: 'হোম টিউটর', enLabel: 'Tuition', href: '/tuition' },
  ];

  const isActive = (path: string) => {
    if (path === '/' && router.pathname === '/') return true;
    if (path !== '/' && router.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <>
      <header
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          isScrolled
            ? 'bg-[#FFFCF6]/95 dark:bg-gray-900/95 backdrop-blur-md shadow-sm py-2.5'
            : 'bg-transparent py-4'
        }`}
      >
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-14">
            {/* Logo */}
            <Link
              href="/"
              className="flex items-center gap-2 text-gray-900 dark:text-white font-bold text-xl tracking-tight transition-transform hover:scale-[1.02]"
            >
              <div className="w-9 h-9 rounded-full bg-[#ED8E22] flex items-center justify-center text-white shadow-md">
                <GraduationCap className="w-5 h-5" aria-hidden="true" />
              </div>
              <div className="flex flex-col">
                <span className="text-lg leading-tight font-black tracking-tight text-[#213130] dark:text-white">
                  অগ্রযাত্রা <span className="text-[#ED8E22] text-xs font-semibold uppercase tracking-wider">Edu</span>
                </span>
                <span className="text-[10px] text-gray-500 dark:text-gray-400 font-medium tracking-wide">
                  Student Life Circle
                </span>
              </div>
            </Link>

            {/* Desktop Pill Navigation */}
            <nav
              aria-label="Primary Navigation"
              className="hidden lg:flex items-center bg-[#E7E7E7] dark:bg-gray-800 rounded-full px-2 py-1.5 shadow-inner"
            >
              {navItems.map(item => {
                const active = isActive(item.href);
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`relative px-4 py-1.5 text-xs font-semibold rounded-full transition-all duration-200 ${
                      active
                        ? 'bg-white dark:bg-gray-700 text-[#ED8E22] dark:text-white shadow-sm'
                        : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-white/50 dark:hover:bg-gray-700/50'
                    }`}
                  >
                    {item.label}
                  </Link>
                );
              })}
            </nav>

            {/* Right Action Icons */}
            <div className="flex items-center gap-2 sm:gap-3">
              {/* Socratic AI Direct Action */}
              <button
                type="button"
                onClick={onOpenSocraticDrawer || (() => router.push('/socratic/solver'))}
                aria-label="Open Socratic AI Solver"
                className="hidden sm:inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-[#ED8E22] text-white text-xs font-semibold hover:bg-[#d47c1a] active:scale-95 transition-all shadow-sm"
              >
                <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
                <span>এআই সলভার</span>
              </button>

              {/* Cart / Saved Items Trigger */}
              <button
                type="button"
                onClick={() => setIsCartOpen(true)}
                aria-label="Saved items drawer"
                className="relative p-2 rounded-full text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              >
                <ShoppingBag className="w-5 h-5" aria-hidden="true" />
                {savedCount > 0 && (
                  <span className="absolute top-1 right-1 w-4 h-4 bg-[#ED8E22] text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                    {savedCount}
                  </span>
                )}
              </button>

              {/* Theme Toggle */}
              <button
                type="button"
                onClick={toggleDarkMode}
                aria-label="Toggle dark mode theme"
                className="p-2 rounded-full text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              >
                {isDarkMode ? (
                  <Sun className="w-5 h-5 text-amber-400" aria-hidden="true" />
                ) : (
                  <Moon className="w-5 h-5" aria-hidden="true" />
                )}
              </button>

              {/* User Profile / Log In */}
              <Link
                href="/dashboard"
                aria-label="Student profile and dashboard"
                className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-full text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 text-xs font-semibold transition-colors"
              >
                <User className="w-4 h-4" aria-hidden="true" />
                <span>প্রোফাইল</span>
              </Link>

              {/* Mobile Hamburger Toggle */}
              <button
                type="button"
                onClick={() => setIsMobileMenuOpen(true)}
                aria-label="Open mobile navigation menu"
                className="flex lg:hidden items-center justify-center w-9 h-9 rounded-full text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              >
                <Menu className="w-5 h-5" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Drawer Backdrop */}
      {isMobileMenuOpen && (
        <div
          role="presentation"
          onClick={() => setIsMobileMenuOpen(false)}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[99] transition-opacity duration-300"
        />
      )}

      {/* Mobile Drawer Panel */}
      <div
        className={`fixed top-0 right-0 h-full w-4/5 max-w-sm z-[100] bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-800 shadow-2xl flex flex-col transition-transform duration-300 ease-out ${
          isMobileMenuOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between px-5 py-4 border-b border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/60">
          <div className="flex items-center gap-3">
            <span className="h-10 w-10 rounded-full bg-[#ED8E22] flex items-center justify-center font-bold text-white shadow-md">
              অ
            </span>
            <div className="flex flex-col">
              <span className="font-semibold text-sm text-gray-800 dark:text-gray-100">
                শিক্ষার্থী প্রোফাইল
              </span>
              <span className="text-xs text-amber-600 dark:text-amber-400 font-medium">
                অগ্রযাত্রা প্ল্যাটফর্ম
              </span>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setIsMobileMenuOpen(false)}
            aria-label="Close Mobile Navigation"
            className="p-1.5 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-500 transition-colors"
          >
            <X className="w-5 h-5" aria-hidden="true" />
          </button>
        </div>

        <nav aria-label="Mobile Navigation" className="flex-1 overflow-y-auto px-4 py-4 space-y-1">
          {navItems.map(item => {
            const active = isActive(item.href);
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className={`flex items-center justify-between px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
                  active
                    ? 'bg-amber-50 dark:bg-amber-950/40 text-[#ED8E22] font-semibold'
                    : 'text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-800'
                }`}
              >
                <span>{item.label}</span>
                <ChevronRight className="w-4 h-4 text-gray-400" aria-hidden="true" />
              </Link>
            );
          })}

          <div className="pt-4 mt-4 border-t border-gray-100 dark:border-gray-800">
            <Link
              href="/socratic/solver"
              onClick={() => setIsMobileMenuOpen(false)}
              className="flex items-center gap-2.5 px-4 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 text-white font-semibold text-sm shadow-md"
            >
              <Sparkles className="w-4 h-4" aria-hidden="true" />
              <span>সক্রেটিক এআই টিউটর খুলুন</span>
            </Link>
          </div>
        </nav>
      </div>

      {/* Cart / Saved Drawer */}
      {isCartOpen && (
        <div
          role="presentation"
          onClick={() => setIsCartOpen(false)}
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[99] transition-opacity duration-300"
        />
      )}

      <div
        className={`fixed top-0 right-0 h-full w-full sm:w-[400px] z-[100] bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-800 shadow-2xl flex flex-col transition-transform duration-300 ease-out ${
          isCartOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex items-center justify-between p-5 border-b border-gray-100 dark:border-gray-800">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-amber-100 dark:bg-amber-950/60 rounded-xl text-[#ED8E22]">
              <ShoppingBag className="w-5 h-5" aria-hidden="true" />
            </div>
            <div>
              <h2 className="font-bold text-base text-gray-900 dark:text-white">সংরক্ষিত কোর্স ও রিসোর্স</h2>
              <p className="text-xs text-gray-500 dark:text-gray-400">{savedCount} টি আইটেম নির্বাচিত</p>
            </div>
          </div>
          <button
            type="button"
            onClick={() => setIsCartOpen(false)}
            aria-label="Close Cart Drawer"
            className="p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 transition-colors"
          >
            <X className="w-5 h-5" aria-hidden="true" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-5 space-y-3">
          <div className="p-3.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/40">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-bold text-[#ED8E22] bg-amber-50 dark:bg-amber-950/60 px-2 py-0.5 rounded-full">
                  হায়ার ম্যাথ
                </span>
                <h3 className="font-semibold text-sm text-gray-900 dark:text-white mt-1">
                  ডিফারেনশিয়াল ক্যালকুলাস ও অ্যাপ্লিকেশন
                </h3>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">প্রফেসর সায়মা সুরাইয়া</p>
              </div>
              <span className="font-bold text-sm text-[#ED8E22]">৳৫০০</span>
            </div>
          </div>

          <div className="p-3.5 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/40">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-[10px] font-bold text-[#ED8E22] bg-amber-50 dark:bg-amber-950/60 px-2 py-0.5 rounded-full">
                  আইসিটি
                </span>
                <h3 className="font-semibold text-sm text-gray-900 dark:text-white mt-1">
                  বুলিয়ান অ্যালজেব্রা ও লজিক গেট মাস্টারক্লাস
                </h3>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">ড. তানভীর আহমেদ</p>
              </div>
              <span className="font-bold text-sm text-[#ED8E22]">৳৪০০</span>
            </div>
          </div>
        </div>

        <div className="p-5 border-t border-gray-100 dark:border-gray-800 bg-gray-50 dark:bg-gray-800/60 space-y-3">
          <div className="flex justify-between text-sm font-semibold text-gray-900 dark:text-white">
            <span>সর্বমোট ফি</span>
            <span className="text-[#ED8E22]">৳৯০০</span>
          </div>
          <Link
            href="/academic-hub"
            onClick={() => setIsCartOpen(false)}
            className="w-full inline-flex items-center justify-center py-2.5 rounded-full bg-[#ED8E22] text-white font-semibold text-sm hover:bg-[#d47c1a] active:scale-95 transition-all shadow-md"
          >
            এনরোলমেন্ট সম্পন্ন করুন
          </Link>
        </div>
      </div>
    </>
  );
};
