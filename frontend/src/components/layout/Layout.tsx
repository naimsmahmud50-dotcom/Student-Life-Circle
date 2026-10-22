/**
 * ========================================================================================
 * MODULE:    Unified Layout Wrapper & Theme Provider Shell
 * TOPIC:     Dual Light/Dark Theme Context, Shell Responsive Grid & Accessibility
 * FILE:      frontend/src/components/layout/Layout.tsx
 * PURPOSE:   Provides consistent high-performance page layout across the platform.
 *            Synchronizes CSS variables for light and dark themes, includes skip links
 *            for keyboard accessibility, and conditionally displays the journey sidebar.
 * AUDIENCE:  Page Implementers, Frontend Engineers & Accessibility Auditors
 * STANDARDS: UI/UX Pro Max, WCAG 2.2 AA Skip Navigation, Zero-Emoji Policy
 * ========================================================================================
 */

import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';
import { Footer } from './Footer';

interface LayoutProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
  showSidebar?: boolean;
  activeStageId?: string;
}

export const Layout: React.FC<LayoutProps> = ({
  children,
  title = 'অগ্রযাত্রা - Student Life Circle | একটি প্রোফাইল। একটি দীর্ঘযাত্রা।',
  description = 'বাংলাদেশের প্রাথমিক শিক্ষা থেকে ক্যারিয়ার পর্যন্ত সকল শিক্ষার্থীর জন্য নির্ভরযোগ্য প্ল্যাটফর্ম।',
  showSidebar = true,
  activeStageId = 'hsc'
}) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Check saved theme or system preference
    const saved = localStorage.getItem('theme') as 'light' | 'dark' | null;
    if (saved) {
      setTheme(saved);
      if (saved === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setTheme('dark');
      document.documentElement.classList.add('dark');
    }
  }, []);

  const toggleTheme = () => {
    const next = theme === 'light' ? 'dark' : 'light';
    setTheme(next);
    localStorage.setItem('theme', next);
    if (next === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 font-sans transition-colors duration-200">
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content={theme === 'dark' ? '#0F172A' : '#2563EB'} />
      </Head>

      {/* Accessible Skip Navigation Link for Screen Readers */}
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 focus:p-3 focus:bg-blue-600 focus:text-white focus:rounded-lg focus:shadow-lg"
      >
        মূল বিষয়ে চলে যান (Skip to main content)
      </a>

      {/* Top Navigation */}
      <Navbar theme={theme} onToggleTheme={toggleTheme} />

      {/* Main Body Grid */}
      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        {showSidebar && (
          <div className="hidden lg:block">
            <Sidebar activeStageId={activeStageId} />
          </div>
        )}

        <main id="main-content" className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
          {children}
        </main>
      </div>

      {/* Bottom Footer */}
      <Footer />
    </div>
  );
};
