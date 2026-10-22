/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - CENTRALIZED SEO & SOCIAL METADATA COMPONENT:
 * MODULE:    Next.js 15+ Advanced SEO, OpenGraph (OG), Twitter Card & Schema.org JSON-LD
 * TOPIC:     Semantic Social Previews, Dynamic Meta Tags & Structured Data Generation
 * FILE:      frontend/src/components/layout/Head.tsx
 * PURPOSE:   Provides centralized metadata injection for all platform routes. Generates
 *            localized OpenGraph tags, high-resolution Twitter Summary Large Image cards,
 *            canonical URLs, crawler directives (noIndex for minor privacy), and semantic
 *            JSON-LD structured data schemas (EducationalOrganization, Course, JobPosting,
 *            and BreadcrumbList) for maximum Lighthouse SEO scores (>= 95).
 * AUDIENCE:  Frontend Architects, SEO Specialists, Social Graph Auditors & Full-Stack Developers
 * STANDARDS: OpenGraph Protocol, Twitter Cards Specs, Schema.org Standards, Strict Zero-Emoji Policy
 * ========================================================================================
 */

import React from 'react';
import NextHead from 'next/head';

export interface StructuredDataCourse {
  name: string;
  description: string;
  providerName?: string;
  educationalLevel?: string;
  url?: string;
}

export interface StructuredDataJobPosting {
  title: string;
  description: string;
  datePosted: string;
  employmentType?: string;
  hiringOrganization: string;
  location: string;
  baseSalary?: string;
}

export interface BreadcrumbItem {
  name: string;
  url: string;
}

export interface AppHeadProps {
  title?: string;
  description?: string;
  keywords?: string[] | string;
  canonicalUrl?: string;
  ogType?: 'website' | 'article' | 'profile' | 'course';
  ogImage?: string;
  publishedTime?: string;
  modifiedTime?: string;
  noIndex?: boolean;
  structuredData?: Record<string, any> | Array<Record<string, any>>;
}

const DEFAULT_TITLE = 'অগ্রযাত্রা | Student Growth Platform (একটি প্রোফাইল। একটি দীর্ঘযাত্রা)';
const DEFAULT_DESCRIPTION = 'বাংলাদেশের শিক্ষার্থীদের প্রথম সার্বিক শিক্ষাজীবন, অ্যাডাপটিভ এনসিটিবি প্র্যাকটিস, লাইভ প্রতিযোগিতা এবং সুরক্ষিত টিউশন হাব।';
const DEFAULT_KEYWORDS = [
  'অগ্রযাত্রা',
  'Student Growth Platform',
  'NCTB MCQ Practice',
  'HSC Exam Prep',
  'University Admission Bangladesh',
  'Verified Tuition Hub',
  'Minor Child Safety',
  'Offline CRDT Quiz',
];
const DEFAULT_OG_IMAGE = 'https://ogrojatra.edu.bd/og/default-platform-preview.png';
const BASE_DOMAIN = 'https://ogrojatra.edu.bd';

/**
 * Standard EducationalOrganization Schema for the platform
 */
export function createOrganizationSchema(): Record<string, any> {
  return {
    '@context': 'https://schema.org',
    '@type': 'EducationalOrganization',
    name: 'অগ্রযাত্রা (Student Growth Platform)',
    alternateName: 'Ogrojatra',
    url: BASE_DOMAIN,
    logo: `${BASE_DOMAIN}/icons/icon-512x512.png`,
    description: DEFAULT_DESCRIPTION,
    foundingDate: '2026',
    address: {
      '@type': 'PostalAddress',
      addressCountry: 'BD',
      addressLocality: 'Dhaka',
    },
    sameAs: [
      'https://facebook.com/ogrojatra_bd',
      'https://twitter.com/ogrojatra_bd',
      'https://linkedin.com/company/ogrojatra-edu',
    ],
  };
}

/**
 * Semantic Course Schema Generator for academic modules & practice sets
 */
export function createCourseSchema(course: StructuredDataCourse): Record<string, any> {
  return {
    '@context': 'https://schema.org',
    '@type': 'Course',
    name: course.name,
    description: course.description,
    provider: {
      '@type': 'EducationalOrganization',
      name: course.providerName || 'অগ্রযাত্রা শিক্ষা একাডেমি',
      sameAs: BASE_DOMAIN,
    },
    educationalLevel: course.educationalLevel || 'HSC / SSC / University Admission',
    url: course.url || BASE_DOMAIN,
    isAccessibleForFree: true,
    inLanguage: 'bn-BD',
  };
}

/**
 * Semantic JobPosting / Tutor Requirement Schema Generator
 */
export function createJobPostingSchema(job: StructuredDataJobPosting): Record<string, any> {
  return {
    '@context': 'https://schema.org',
    '@type': 'JobPosting',
    title: job.title,
    description: job.description,
    datePosted: job.datePosted,
    employmentType: job.employmentType || 'PART_TIME',
    hiringOrganization: {
      '@type': 'Organization',
      name: job.hiringOrganization,
    },
    jobLocation: {
      '@type': 'Place',
      address: {
        '@type': 'PostalAddress',
        addressLocality: job.location,
        addressCountry: 'BD',
      },
    },
    baseSalary: job.baseSalary
      ? {
          '@type': 'MonetaryAmount',
          currency: 'BDT',
          value: {
            '@type': 'QuantitativeValue',
            unitText: 'MONTH',
            value: job.baseSalary,
          },
        }
      : undefined,
  };
}

/**
 * BreadcrumbList Schema Generator for nested navigation
 */
export function createBreadcrumbSchema(items: BreadcrumbItem[]): Record<string, any> {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url.startsWith('http') ? item.url : `${BASE_DOMAIN}${item.url}`,
    })),
  };
}

export const AppHead: React.FC<AppHeadProps> = ({
  title = DEFAULT_TITLE,
  description = DEFAULT_DESCRIPTION,
  keywords = DEFAULT_KEYWORDS,
  canonicalUrl,
  ogType = 'website',
  ogImage = DEFAULT_OG_IMAGE,
  publishedTime,
  modifiedTime,
  noIndex = false,
  structuredData,
}) => {
  const fullTitle = title.includes('অগ্রযাত্রা') ? title : `${title} | অগ্রযাত্রা`;
  const keywordString = Array.isArray(keywords) ? keywords.join(', ') : keywords;
  const canonical = canonicalUrl ? (canonicalUrl.startsWith('http') ? canonicalUrl : `${BASE_DOMAIN}${canonicalUrl}`) : undefined;

  // Prepare Schema array
  const schemas: Array<Record<string, any>> = [];
  if (structuredData) {
    if (Array.isArray(structuredData)) {
      schemas.push(...structuredData);
    } else {
      schemas.push(structuredData);
    }
  }

  return (
    <NextHead>
      {/* Basic Metadata */}
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywordString} />
      {canonical && <link rel="canonical" href={canonical} />}

      {/* Robots Directive: Ensure minor profiles and private views are shielded */}
      <meta
        name="robots"
        content={noIndex ? 'noindex, nofollow, noarchive' : 'index, follow, max-image-preview:large, max-snippet:-1'}
      />

      {/* OpenGraph Protocol (Facebook, WhatsApp, LinkedIn, Discord) */}
      <meta property="og:site_name" content="অগ্রযাত্রা (Student Growth Platform)" />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:type" content={ogType} />
      {canonical && <meta property="og:url" content={canonical} />}
      <meta property="og:image" content={ogImage} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:image:alt" content={fullTitle} />
      <meta property="og:locale" content="bn_BD" />
      {publishedTime && <meta property="article:published_time" content={publishedTime} />}
      {modifiedTime && <meta property="article:modified_time" content={modifiedTime} />}

      {/* Twitter Cards */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:site" content="@ogrojatra_bd" />
      <meta name="twitter:creator" content="@ogrojatra_bd" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImage} />
      <meta name="twitter:image:alt" content={fullTitle} />

      {/* Semantic JSON-LD Structured Data */}
      {schemas.map((schema, index) => (
        <script
          key={`structured-data-${index}`}
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(schema),
          }}
        />
      ))}
    </NextHead>
  );
};

export default AppHead;
