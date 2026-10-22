/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Grand Public Production Launch & System Handover
 * TOPIC:     Phase 141 SEO, 64-District OpenGraph Engine, Production CI/CD & National Handover
 * FILE:      frontend/src/components/seo/SEOHead.tsx
 * PHASE:     Phase 141 - Grand Public Production Launch & Final Handover
 * PURPOSE:   Modular SEO, Dynamic 64-District OpenGraph & JSON-LD Structured Data Engine
 * STANDARDS: Zero-Emoji, Zero-IDOR, Production Grade, WCAG 2.2 AAA, Full 64-District Support
 */

import React from "react";
import Head from "next/head";
import { getDistrictById } from "../../lib/districts";

export interface SEOHeadProps {
  title?: string;
  description?: string;
  canonicalPath?: string;
  districtSlug?: string;
  ogType?: "website" | "article";
  noindex?: boolean;
  courseDetails?: {
    name: string;
    description: string;
    courseCode?: string;
  };
}

const BASE_URL = "https://studentlifecircle.com";
const DEFAULT_TITLE = "Student Life Circle (অগ্রযাত্রা) | বাংলাদেশের জাতীয় পরীক্ষা প্রস্তুতি ও শিক্ষা প্ল্যাটফর্ম";
const DEFAULT_DESCRIPTION = "বাংলাদেশ সরকারের অনুমোদিত NCTB কারিকুলাম, এসএসসি, এইচএসসি, বিশ্ববিদ্যালয় ভর্তি পরীক্ষা, প্রশ্নব্যাংক আর্কাইভ এবং ২৪ ঘণ্টার ডিজিটাল এসক্রো টিউটরিং প্ল্যাটফর্ম।";

export const SEOHead: React.FC<SEOHeadProps> = ({
  title = DEFAULT_TITLE,
  description = DEFAULT_DESCRIPTION,
  canonicalPath = "",
  districtSlug,
  ogType = "website",
  noindex = false,
  courseDetails
}) => {
  const canonicalUrl = `${BASE_URL}${canonicalPath.startsWith("/") ? canonicalPath : `/${canonicalPath}`}`;

  // If a district is specified, customize title, description, and OG image
  let finalTitle = title;
  let finalDescription = description;
  let ogImageUrl = `${BASE_URL}/api/og`;

  if (districtSlug) {
    const districtInfo = getDistrictById(districtSlug);
    if (districtInfo) {
      finalTitle = `${districtInfo.nameBn} জেলা পরীক্ষা প্রস্তুতি ও শিক্ষা হাব | Student Life Circle`;
      finalDescription = `${districtInfo.nameBn} জেলার শিক্ষার্থীদের জন্য ${districtInfo.topExamStream}, লাইভ মডেল টেস্ট ও বোর্ড আর্কাইভ।`;
      ogImageUrl = `${BASE_URL}/api/og?district=${districtInfo.id}`;
    }
  }

  // Schema.org Structured Data (JSON-LD)
  const organizationSchema = {
    "@context": "https://schema.org",
    "@type": "EducationalOrganization",
    name: "Student Life Circle (অগ্রযাত্রা)",
    url: BASE_URL,
    logo: `${BASE_URL}/icons/icon-512x512.png`,
    description: DEFAULT_DESCRIPTION,
    address: {
      "@type": "PostalAddress",
      addressCountry: "BD",
      addressLocality: "Dhaka"
    },
    sameAs: [
      "https://facebook.com/studentlifecircle",
      "https://linkedin.com/company/studentlifecircle"
    ]
  };

  const websiteSchema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: "Student Life Circle",
    url: BASE_URL,
    potentialAction: {
      "@type": "SearchAction",
      target: `${BASE_URL}/practice?q={search_term_string}`,
      "query-input": "required name=search_term_string"
    }
  };

  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      {
        "@type": "ListItem",
        position: 1,
        name: "Home",
        item: BASE_URL
      },
      ...(canonicalPath && canonicalPath !== "/"
        ? [
            {
              "@type": "ListItem",
              position: 2,
              name: canonicalPath.replace(/^\//, "").replace(/-/g, " "),
              item: canonicalUrl
            }
          ]
        : [])
    ]
  };

  const courseSchema = courseDetails
    ? {
        "@context": "https://schema.org",
        "@type": "Course",
        name: courseDetails.name,
        description: courseDetails.description,
        courseCode: courseDetails.courseCode || "BD-NCTB-2026",
        provider: {
          "@type": "EducationalOrganization",
          name: "Student Life Circle (অগ্রযাত্রা)",
          sameAs: BASE_URL
        }
      }
    : null;

  return (
    <Head>
      {/* Primary Meta Tags */}
      <title>{finalTitle}</title>
      <meta name="title" content={finalTitle} />
      <meta name="description" content={finalDescription} />
      <meta name="keywords" content="SSC, HSC, NCTB, Bangladesh Exam, Admission Prep, Board Question, BCS, bKash Escrow, Tuition" />
      <meta name="author" content="Student Life Circle Engineering Team" />
      <meta name="publisher" content="Student Life Circle" />
      <meta name="robots" content={noindex ? "noindex, nofollow" : "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"} />
      <meta name="googlebot" content={noindex ? "noindex, nofollow" : "index, follow"} />

      {/* Canonical and Localization Alternates */}
      <link rel="canonical" href={canonicalUrl} />
      <link rel="alternate" hrefLang="bn-BD" href={canonicalUrl} />
      <link rel="alternate" hrefLang="en" href={`${canonicalUrl}?lang=en`} />
      <link rel="alternate" hrefLang="x-default" href={canonicalUrl} />

      {/* Open Graph / Facebook */}
      <meta property="og:type" content={ogType} />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:title" content={finalTitle} />
      <meta property="og:description" content={finalDescription} />
      <meta property="og:image" content={ogImageUrl} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:image:alt" content={finalTitle} />
      <meta property="og:site_name" content="Student Life Circle" />
      <meta property="og:locale" content="bn_BD" />
      <meta property="og:locale:alternate" content="en_US" />

      {/* Twitter Cards */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:url" content={canonicalUrl} />
      <meta name="twitter:title" content={finalTitle} />
      <meta name="twitter:description" content={finalDescription} />
      <meta name="twitter:image" content={ogImageUrl} />

      {/* JSON-LD Structured Data */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />
      {courseSchema && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(courseSchema) }}
        />
      )}
    </Head>
  );
};

export default SEOHead;
