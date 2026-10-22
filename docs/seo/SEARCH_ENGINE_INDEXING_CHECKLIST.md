<!--
  DEVELOPER ARCHITECTURE NOTE:
  MODULE:    Grand Public Production Launch & System Handover
  TOPIC:     Phase 141 SEO, 64-District OpenGraph Engine, Production CI/CD & National Handover
  FILE:      docs/seo/SEARCH_ENGINE_INDEXING_CHECKLIST.md
  PHASE:     Phase 141 - Grand Public Production Launch & Final Handover
  PURPOSE:   Comprehensive search engine submission, verification, and indexing checklist
  STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Full 64-District Support
-->

# Search Engine Indexing & Verification Checklist

This checklist guides the engineering and growth teams through the authoritative submission, verification, and monitoring of **Student Life Circle (অগ্রযাত্রা)** on Google Search Console, Bing Webmaster Tools, and regional educational search indexes.

---

## 1. Domain Ownership Verification

### Google Search Console (GSC)
- [ ] Log in to [Google Search Console](https://search.google.com/search-console).
- [ ] Add property using Domain level: `studentlifecircle.com`.
- [ ] Obtain the DNS TXT verification token (e.g. `google-site-verification=XXXXXXXXXXXXXXXXXXXX`).
- [ ] Add the TXT record to your DNS provider (Cloudflare / Namecheap / Route 53):
  ```text
  Type: TXT
  Host: @
  Value: google-site-verification=XXXXXXXXXXXXXXXXXXXX
  TTL: Auto / 300
  ```
- [ ] Alternative: Embed verification meta tag into `frontend/src/pages/_document.tsx` if DNS propagation takes time.
- [ ] Click **Verify** in GSC.

### Bing Webmaster Tools
- [ ] Log in to [Bing Webmaster Tools](https://www.bing.com/webmasters).
- [ ] Import property directly from Google Search Console (recommended for instant verification).
- [ ] Alternatively, add the CNAME record or Bing verification meta tag.
- [ ] Enable **IndexNow** key for instant URL indexing upon content updates.

---

## 2. Sitemap Submission

- [ ] Verify that `https://studentlifecircle.com/sitemap.xml` is returning HTTP 200 with valid XML.
- [ ] In Google Search Console: Navigate to **Indexing** > **Sitemaps**.
- [ ] Enter `sitemap.xml` in the "Add a new sitemap" input and click **Submit**.
- [ ] Confirm status reads "Success" and all submitted URLs are discovered.
- [ ] In Bing Webmaster: Navigate to **Sitemaps** > **Submit Sitemap** and enter `https://studentlifecircle.com/sitemap.xml`.

---

## 3. URL Inspection & Live Test

Perform live URL inspection in GSC for the following core landing pages:
1. `https://studentlifecircle.com/` (Homepage)
2. `https://studentlifecircle.com/practice` (Exam Practice Engine)
3. `https://studentlifecircle.com/board-archives` (Past Board Papers)
4. `https://studentlifecircle.com/tuition` (Escrow Tuition Marketplace)
5. `https://studentlifecircle.com/curriculum/lexicon` (NCTB Bilingual Lexicon)

**Verification Criteria**:
- "URL is available to Google"
- Crawl allowed: Yes (robots.txt allows `/`)
- Page fetch: Successful
- Indexing allowed: Yes (no noindex tag present)
- Canonical URL: Declared user canonical matches Google-selected canonical.

---

## 4. Rich Results & JSON-LD Validation

- [ ] Open the [Google Rich Results Test](https://search.google.com/test/rich-results).
- [ ] Test `https://studentlifecircle.com/`.
- [ ] Verify detected structured data:
  - `EducationalOrganization`: Valid name, logo, URL, and address.
  - `WebSite`: Valid SearchAction query-input for internal search.
  - `BreadcrumbList`: Correct positional hierarchy.
  - `Course`: Valid provider and course code metadata on subject pages.
- [ ] Confirm **0 errors** and **0 critical warnings**.

---

## 5. Core Web Vitals & Mobile Usability

- [ ] Run Google Lighthouse in Chrome DevTools on desktop and simulated mobile 3G/4G:
  - **Performance**: $\ge 95$
  - **Accessibility**: $\ge 98$
  - **Best Practices**: 100
  - **SEO**: 100
- [ ] Confirm Core Web Vitals targets:
  - **Largest Contentful Paint (LCP)**: $< 1.0\text{s}$
  - **Cumulative Layout Shift (CLS)**: $0.00$
  - **Interaction to Next Paint (INP)**: $< 150\text{ms}$

---

## 6. Social Share Card Verification

- [ ] Test dynamic OpenGraph card for Dhaka:
  `curl -I "https://studentlifecircle.com/api/og?district=dhaka"`
  Confirm `Content-Type: image/svg+xml; charset=utf-8` and `200 OK`.
- [ ] Test on [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/):
  - Paste `https://studentlifecircle.com/`
  - Click "Scrape Again"
  - Verify og:image renders crisp Bengali text and Oxford Navy background.
- [ ] Test on [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/):
  - Confirm metadata, image preview, and title render correctly.
- [ ] Test Twitter Card preview:
  - Verify card format renders as `summary_large_image`.
