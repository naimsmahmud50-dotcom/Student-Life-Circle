"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE - PHASE 85 CORE WEB VITALS & SEO VERIFICATION SUITE:
MODULE:    Automated Test Suite for Performance Tuning, Core Web Vitals & SEO
TOPIC:     LCP < 1.2s, INP < 100ms, CLS = 0, Next.js Brotli/AVIF, JSON-LD Schemas & Lighthouse
FILE:      backend/tests/test_phase85_core_web_vitals_seo.py
PURPOSE:   Provides exhaustive automated verification of Phase 85 deliverables:
           1. Next.js 15+ performance configuration (Brotli compression, AVIF/WebP, tree-shaking)
           2. Font preloading (dns-prefetch, preconnect, font-display: swap) in _document.tsx
           3. Centralized AppHead SEO component with OpenGraph, Twitter Cards & JSON-LD
           4. Semantic Schema.org generators (EducationalOrganization, Course, JobPosting, Breadcrumbs)
           5. Core routes SEO wiring (index, practice, tuition, admission, career, modules)
           6. Automated Lighthouse audit results asserting scores >= 95 across all categories
           7. Core Web Vitals targets: LCP < 1.2s, INP < 100ms, CLS = 0
           8. Strict Zero-Emoji compliance and Developer Architecture Notes on every file
AUDIENCE:  Frontend Architects, SEO Reviewers, CI/CD Quality Gates & System Auditors
STANDARDS: Google Core Web Vitals, Schema.org Standards, Strict Zero-Emoji Governance
========================================================================================
"""

import unittest
import os
import json
import re
from pathlib import Path

# Strict Zero-Emoji Regex
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U00002600-\U000026FF\U00002700-\U000027BF\U0001F900-\U0001F9FF\U0001F018-\U0001F270\U0000238C-\U00002454\U000020D0-\U000020FF\U0001FA70-\U0001FAFF]"
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = REPO_ROOT / "frontend"
PAGES_DIR = FRONTEND_DIR / "src" / "pages"
LAYOUT_DIR = FRONTEND_DIR / "src" / "components" / "layout"
SCRIPTS_DIR = FRONTEND_DIR / "scripts"
REPORT_DIR = FRONTEND_DIR / "playwright-report"


class TestPhase85CoreWebVitalsSEO(unittest.TestCase):
    """
    Automated verification suite validating Phase 85 Performance, Core Web Vitals & SEO deliverables.
    """

    def test_next_config_performance_optimizations(self):
        """
        Verify that frontend/next.config.js includes Brotli compression, AVIF/WebP,
        and tree-shaking package imports.
        """
        next_config_file = FRONTEND_DIR / "next.config.js"
        self.assertTrue(next_config_file.exists(), "frontend/next.config.js must exist")

        content = next_config_file.read_text(encoding="utf-8")

        # Brotli compression
        self.assertIn("compress: true", content)

        # Powered by header suppressed
        self.assertIn("poweredByHeader: false", content)

        # Modern image formats
        self.assertIn("'image/avif'", content)
        self.assertIn("'image/webp'", content)

        # Tree-shaking package imports
        self.assertIn("optimizePackageImports", content)
        self.assertIn("'lucide-react'", content)

        # Caching headers for service worker and static chunks
        self.assertIn("max-age=31536000, immutable", content)
        self.assertIn("/sw.js", content)
        self.assertIn("/manifest.json", content)

    def test_font_preloading_and_cwv_optimizations(self):
        """
        Verify that _document.tsx configures dns-prefetch, preconnect, and font-display: swap.
        """
        doc_file = PAGES_DIR / "_document.tsx"
        self.assertTrue(doc_file.exists(), "frontend/src/pages/_document.tsx must exist")

        doc_content = doc_file.read_text(encoding="utf-8")
        self.assertIn('rel="dns-prefetch" href="https://fonts.googleapis.com"', doc_content)
        self.assertIn('rel="dns-prefetch" href="https://fonts.gstatic.com"', doc_content)
        self.assertIn('rel="preconnect" href="https://fonts.googleapis.com"', doc_content)
        self.assertIn('rel="preconnect" href="https://fonts.gstatic.com"', doc_content)
        self.assertIn('display=swap', doc_content)
        self.assertIn('Noto+Sans+Bengali', doc_content)
        self.assertIn('Inter', doc_content)

        # Verify globals.css
        css_file = FRONTEND_DIR / "src" / "styles" / "globals.css"
        css_content = css_file.read_text(encoding="utf-8")
        self.assertIn("display=swap", css_content)
        self.assertIn("font-family: 'Noto Sans Bengali'", css_content)

    def test_app_head_seo_component_features(self):
        """
        Verify that Head.tsx exports AppHead with OpenGraph, Twitter Cards, and Schema.org support.
        """
        head_file = LAYOUT_DIR / "Head.tsx"
        self.assertTrue(head_file.exists(), "frontend/src/components/layout/Head.tsx must exist")

        content = head_file.read_text(encoding="utf-8")

        # OpenGraph tags
        self.assertIn('property="og:title"', content)
        self.assertIn('property="og:description"', content)
        self.assertIn('property="og:image"', content)
        self.assertIn('property="og:type"', content)
        self.assertIn('property="og:site_name"', content)
        self.assertIn('property="og:locale"', content)

        # Twitter Cards
        self.assertIn('name="twitter:card"', content)
        self.assertIn('name="twitter:site"', content)
        self.assertIn('name="twitter:title"', content)
        self.assertIn('name="twitter:description"', content)

        # Canonical URL and Robots
        self.assertIn('rel="canonical"', content)
        self.assertIn('name="robots"', content)

        # JSON-LD application/ld+json
        self.assertIn('type="application/ld+json"', content)

    def test_structured_data_schemas_validity(self):
        """
        Verify that Schema.org schema generator functions produce valid structured data.
        """
        head_file = LAYOUT_DIR / "Head.tsx"
        content = head_file.read_text(encoding="utf-8")

        self.assertIn("createOrganizationSchema", content)
        self.assertIn("createCourseSchema", content)
        self.assertIn("createJobPostingSchema", content)
        self.assertIn("createBreadcrumbSchema", content)

        self.assertIn("'@type': 'EducationalOrganization'", content)
        self.assertIn("'@type': 'Course'", content)
        self.assertIn("'@type': 'JobPosting'", content)
        self.assertIn("'@type': 'BreadcrumbList'", content)

    def test_core_pages_seo_wiring(self):
        """
        Verify that all core dynamic routes have AppHead wired with localized metadata.
        """
        pages_to_check = [
            ("index.tsx", "অগ্রযাত্রা | একটি প্রোফাইল। একটি দীর্ঘযাত্রা"),
            ("practice.tsx", "যেকোনো সময় অনুশীলন (Anytime Practice)"),
            ("tuition.tsx", "সুরক্ষিত টিউশন মার্কেটপ্লেস ও দ্বিপাক্ষিক সম্মতি হাব"),
            ("admission.tsx", "বিশ্ববিদ্যালয় ভর্তি প্রস্তুতি হাব (Admission Matrix)"),
            ("career.tsx", "দক্ষতা প্রমাণ ও ক্যারিয়ার হাব (Career Portfolio)"),
            ("modules.tsx", "৬৯টি এন্টারপ্রাইজ মডিউল ডিরেক্টরি"),
        ]

        for page_name, expected_title in pages_to_check:
            page_path = PAGES_DIR / page_name
            self.assertTrue(page_path.exists(), f"Page {page_name} must exist")
            content = page_path.read_text(encoding="utf-8")

            self.assertIn("AppHead", content, f"{page_name} must use AppHead")
            self.assertIn(expected_title, content, f"{page_name} must define expected title")
            self.assertIn("canonicalUrl", content, f"{page_name} must specify canonicalUrl")

    def test_lighthouse_audit_execution_and_thresholds(self):
        """
        Verify that run-lighthouse-audit.py runs cleanly and asserts scores >= 95 and CWV targets.
        """
        script_file = SCRIPTS_DIR / "run-lighthouse-audit.py"
        self.assertTrue(script_file.exists(), "frontend/scripts/run-lighthouse-audit.py must exist")

        import importlib.util
        spec = importlib.util.spec_from_file_location("run_lighthouse", script_file)
        run_lh = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run_lh)

        results = run_lh.run_lighthouse_audit()
        run_lh.generate_lighthouse_report(results)

        # Assert all 4 category scores >= 95
        self.assertTrue(results["all_categories_above_95"], "All Lighthouse categories must be >= 95")
        self.assertGreaterEqual(results["overall_scores"]["performance"], 95.0)
        self.assertGreaterEqual(results["overall_scores"]["accessibility"], 95.0)
        self.assertGreaterEqual(results["overall_scores"]["best_practices"], 95.0)
        self.assertGreaterEqual(results["overall_scores"]["seo"], 95.0)

        # Assert Core Web Vitals thresholds:
        # LCP < 1.2s (1200ms)
        self.assertTrue(results["core_web_vitals_summary"]["lcp_target_met"])
        self.assertLess(results["core_web_vitals_summary"]["lcp_max_ms"], 1200)

        # INP < 100ms
        self.assertTrue(results["core_web_vitals_summary"]["inp_target_met"])
        self.assertLess(results["core_web_vitals_summary"]["inp_max_ms"], 100)

        # CLS = 0
        self.assertTrue(results["core_web_vitals_summary"]["cls_target_met"])
        self.assertEqual(results["core_web_vitals_summary"]["cls_max"], 0.000)

        # Verify output report files
        json_report = REPORT_DIR / "lighthouse-audit.json"
        html_report = REPORT_DIR / "lighthouse-report.html"
        self.assertTrue(json_report.exists(), "lighthouse-audit.json must be generated")
        self.assertTrue(html_report.exists(), "lighthouse-report.html must be generated")

    def test_strict_zero_emoji_compliance_across_all_phase85_files(self):
        """
        Strictly assert zero emojis across all Phase 85 files, configs, scripts, and reports.
        """
        files_to_audit = [
            FRONTEND_DIR / "next.config.js",
            PAGES_DIR / "_document.tsx",
            FRONTEND_DIR / "src" / "styles" / "globals.css",
            LAYOUT_DIR / "Head.tsx",
            LAYOUT_DIR / "index.ts",
            PAGES_DIR / "index.tsx",
            PAGES_DIR / "practice.tsx",
            PAGES_DIR / "tuition.tsx",
            PAGES_DIR / "admission.tsx",
            PAGES_DIR / "career.tsx",
            PAGES_DIR / "modules.tsx",
            SCRIPTS_DIR / "run-lighthouse-audit.py",
            REPORT_DIR / "lighthouse-report.html",
        ]

        for file_path in files_to_audit:
            if not file_path.exists():
                continue
            content = file_path.read_text(encoding="utf-8")
            emojis = EMOJI_PATTERN.findall(content)
            self.assertEqual(
                emojis,
                [],
                f"Strict Zero-Emoji Violation in {file_path.name}: Found emojis {emojis}"
            )

    def test_developer_architecture_notes_present_on_all_phase85_files(self):
        """
        Verify that every newly created or updated Phase 85 file begins with a prominent DEVELOPER ARCHITECTURE NOTE.
        """
        files_to_check = [
            FRONTEND_DIR / "next.config.js",
            PAGES_DIR / "_document.tsx",
            FRONTEND_DIR / "src" / "styles" / "globals.css",
            LAYOUT_DIR / "Head.tsx",
            LAYOUT_DIR / "index.ts",
            PAGES_DIR / "index.tsx",
            PAGES_DIR / "practice.tsx",
            PAGES_DIR / "tuition.tsx",
            PAGES_DIR / "admission.tsx",
            PAGES_DIR / "career.tsx",
            PAGES_DIR / "modules.tsx",
            SCRIPTS_DIR / "run-lighthouse-audit.py",
        ]

        for file_path in files_to_check:
            self.assertTrue(file_path.exists(), f"File {file_path.name} must exist")
            content = file_path.read_text(encoding="utf-8")
            self.assertIn(
                "DEVELOPER ARCHITECTURE NOTE",
                content,
                f"File {file_path.name} must contain a prominent DEVELOPER ARCHITECTURE NOTE"
            )


if __name__ == "__main__":
    unittest.main()
