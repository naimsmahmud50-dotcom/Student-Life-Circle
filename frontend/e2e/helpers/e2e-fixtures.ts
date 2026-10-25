/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - E2E TEST FIXTURES & HELPER SUITE:
 * MODULE:    Playwright End-to-End Test Harness & Network Interceptors
 * TOPIC:     Deterministic Mock APIs, Minor Protection Fixtures & Zero-Emoji Audit Engine
 * FILE:      frontend/e2e/helpers/e2e-fixtures.ts
 * PURPOSE:   Provides reusable fixtures, synthetic response generators, network offline/online
 *            simulators, console error traps, and strict Zero-Emoji regex validators for
 *            all Playwright integration tests. Ensures tests run deterministically across
 *            headless Chromium, Firefox, WebKit, and mobile viewport emulations.
 * AUDIENCE:  QA Engineers, Automation Architects & Full-Stack Developers
 * STANDARDS: Playwright Fixture API, UI/UX Pro Max, Minor Safety, Strict Zero-Emoji Policy
 * ========================================================================================
 */

import { test as base, expect, Page, BrowserContext } from '@playwright/test';

/**
 * Strict Zero-Emoji regular expression covering standard Unicode emoji blocks,
 * supplemental symbols, pictographs, emoticons, transport, and dingbats.
 */
export const EMOJI_REGEX = /[\u{1F300}-\u{1F5FF}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F900}-\u{1F9FF}\u{1F018}-\u{1F270}\u{238C}-\u{2454}\u{20D0}-\u{20FF}\u{1FA70}-\u{1FAFF}]/u;

export interface TestUser {
  id: string;
  fullName: string;
  phoneOrEmail: string;
  age: number;
  stage: 'PRIMARY' | 'MIDDLE' | 'SSC' | 'HSC' | 'ADMISSION' | 'UNIVERSITY' | 'JOB_SEEKER';
  medium: 'BANGLA' | 'ENGLISH_VERSION';
  role: 'student' | 'guardian' | 'tutor';
  isMinor: boolean;
}

export const SAMPLE_STUDENT_MINOR: TestUser = {
  id: 'usr_test_minor_01',
  fullName: 'তানভীর আহমেদ',
  phoneOrEmail: '01711000001',
  age: 15,
  stage: 'HSC',
  medium: 'BANGLA',
  role: 'student',
  isMinor: true,
};

export const SAMPLE_STUDENT_ADULT: TestUser = {
  id: 'usr_test_adult_02',
  fullName: 'নুসরাত জাহান',
  phoneOrEmail: '01811000002',
  age: 18,
  stage: 'ADMISSION',
  medium: 'BANGLA',
  role: 'student',
  isMinor: false,
};

export const SAMPLE_TUTOR_VERIFIED: TestUser = {
  id: 'usr_test_tutor_03',
  fullName: 'ইঞ্জিনিয়ার ফারহান কবির',
  phoneOrEmail: '01911000003',
  age: 23,
  stage: 'UNIVERSITY',
  medium: 'BANGLA',
  role: 'tutor',
  isMinor: false,
};

/**
 * Attaches console and page error traps to the page to assert zero JavaScript exceptions.
 */
export function setupConsoleTrap(page: Page, options?: { ignoreNetworkDisconnect?: boolean }) {
  const errors: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      const text = msg.text();
      if (options?.ignoreNetworkDisconnect && text.includes('ERR_INTERNET_DISCONNECTED')) {
        return;
      }
      errors.push(`[Console Error] ${text}`);
    }
  });
  page.on('pageerror', (err) => {
    if (options?.ignoreNetworkDisconnect && err.message.includes('ERR_INTERNET_DISCONNECTED')) {
      return;
    }
    errors.push(`[Page Error] ${err.message}`);
  });
  return {
    getErrors: () => errors,
    assertZeroErrors: () => {
      expect(errors).toEqual([]);
    },
  };
}

/**
 * Asserts that a given string or page content is 100% free of emojis.
 */
export function assertZeroEmojis(content: string, contextDescription: string = 'Content') {
  const match = content.match(EMOJI_REGEX);
  if (match) {
    throw new Error(
      `Strict Zero-Emoji Policy Violation in ${contextDescription}: Found emoji '${match[0]}' (code point: ${match[0].codePointAt(0)?.toString(16)})`
    );
  }
}

/**
 * Mocks the central backend API routes for deterministic, offline-capable E2E testing.
 */
export async function setupMockApiRoutes(page: Page) {
  // Mock SMS OTP Send Endpoint
  await page.route('**/api/v1/auth/otp/send', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status: 'DISPATCHED',
        provider: 'greenweb',
        expires_in_seconds: 180,
        message_bn: 'আপনার অগ্রযাত্রা ওটিপি কোড সফলভাবে পাঠানো হয়েছে।',
      }),
    });
  });

  // Mock SMS OTP Verify Endpoint
  await page.route('**/api/v1/auth/otp/verify', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        verified: true,
        token: 'mock_jwt_verified_token_sample',
        message_bn: 'ওটিপি ভেরিফিকেশন সফল হয়েছে।',
      }),
    });
  });

  // Mock Practice Questions Endpoint
  await page.route('**/api/v1/practice/sets*', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        curriculum: 'HSC',
        subject: 'পদার্থবিজ্ঞান ১ম পত্র',
        totalQuestions: 5,
        items: [
          {
            id: 'q_hsc_phy_1',
            stemBn: 'একটি বস্তুর ভর ১০ কেজি এবং এর ওপর ৫০ নিউটন বল প্রয়োগ করা হলো। বস্তুটির ত্বরণ কত হবে?',
            options: [
              { id: 'opt_1a', key: 'A', textBn: '২ মি/সে²', isCorrect: false },
              { id: 'opt_1b', key: 'B', textBn: '৫ মি/সে²', isCorrect: true },
              { id: 'opt_1c', key: 'C', textBn: '১০ মি/সে²', isCorrect: false },
              { id: 'opt_1d', key: 'D', textBn: '৫০ মি/সে²', isCorrect: false },
            ],
            explanationBn: 'নিউটনের ২য় সূত্র: F = ma ⇒ a = F/m = ৫০/১০ = ৫ মি/সে²।',
            sourceCitation: 'এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৩য় অধ্যায়',
          },
          {
            id: 'q_hsc_phy_2',
            stemBn: 'মহাকর্ষীয় ধ্রুবক G এর এসআই (SI) একক কোনটি?',
            options: [
              { id: 'opt_2a', key: 'A', textBn: 'N m² kg⁻²', isCorrect: true },
              { id: 'opt_2b', key: 'B', textBn: 'N m kg⁻¹', isCorrect: false },
              { id: 'opt_2c', key: 'C', textBn: 'N m² kg⁻¹', isCorrect: false },
              { id: 'opt_2d', key: 'D', textBn: 'N kg⁻²', isCorrect: false },
            ],
            explanationBn: 'F = G (m1 m2)/r² ⇒ G = F r² / (m1 m2) ⇒ N m² kg⁻²।',
            sourceCitation: 'এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৬ষ্ঠ অধ্যায়',
          },
          {
            id: 'q_hsc_phy_3',
            stemBn: 'সরল ছন্দিত স্পন্দনশীল কণার সাম্যাবস্থানে কোনটির মান সর্বোচ্চ হয়?',
            options: [
              { id: 'opt_3a', key: 'A', textBn: 'বিভব শক্তি', isCorrect: false },
              { id: 'opt_3b', key: 'B', textBn: 'গতিশক্তি', isCorrect: true },
              { id: 'opt_3c', key: 'C', textBn: 'ত্বরণ', isCorrect: false },
              { id: 'opt_3d', key: 'D', textBn: 'বল', isCorrect: false },
            ],
            explanationBn: 'সাম্যাবস্থানে বেগ সর্বোচ্চ হওয়ায় গতিশক্তি সর্বোচ্চ থাকে।',
            sourceCitation: 'এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, ৮ম অধ্যায়',
          },
          {
            id: 'q_hsc_phy_4',
            stemBn: 'পানির ত্রৈধ বিন্দুর তাপমাত্রা কেলভিন স্কেলে কত?',
            options: [
              { id: 'opt_4a', key: 'A', textBn: '২৭৩.১৬ K', isCorrect: true },
              { id: 'opt_4b', key: 'B', textBn: '২৭৩.০০ K', isCorrect: false },
              { id: 'opt_4c', key: 'C', textBn: '৩৭৩.১৬ K', isCorrect: false },
              { id: 'opt_4d', key: 'D', textBn: '১০০.০০ K', isCorrect: false },
            ],
            explanationBn: 'বিশুদ্ধ বরফ, পানি ও জলীয় বাষ্পের সাম্যাবস্থার তাপমাত্রা ২৭৩.১৬ কেলভিন।',
            sourceCitation: 'এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, তাপগতিবিদ্যা',
          },
          {
            id: 'q_hsc_phy_5',
            stemBn: 'আদর্শ গ্যাসের অভ্যন্তরীণ শক্তি শুধুমাত্র কোনটির ওপর নির্ভর করে?',
            options: [
              { id: 'opt_5a', key: 'A', textBn: 'চাপ', isCorrect: false },
              { id: 'opt_5b', key: 'B', textBn: 'তাপমাত্রা', isCorrect: true },
              { id: 'opt_5c', key: 'C', textBn: 'আয়তন', isCorrect: false },
              { id: 'opt_5d', key: 'D', textBn: 'ঘনত্ব', isCorrect: false },
            ],
            explanationBn: 'জুলের সূত্রানুসারে আদর্শ গ্যাসের অভ্যন্তরীণ শক্তি কেবল পরম তাপমাত্রার অপেক্ষক।',
            sourceCitation: 'এনসিটিবি পদার্থবিজ্ঞান ১ম পত্র, তাপগতিবিদ্যা',
          },
        ],
      }),
    });
  });

  // Mock Quiz Attempts Batch Sync Endpoint
  await page.route('**/api/v1/quiz-attempts/sync', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        synced_count: 5,
        status: 'MUTATIONS_APPLIED',
        resolved_conflicts: 0,
        sync_timestamp: new Date().toISOString(),
      }),
    });
  });

  // Mock Live Challenges Endpoint
  await page.route(/\/api\/v1\/live-challenges/, async (route) => {
    if (route.request().url().includes('leaderboard')) {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { rank: 1, handle: "মেধাবী_শিক্ষার্থী_৯৯", score: 24.5, accuracyPercent: 98.0, streakCount: 14 },
          { rank: 2, handle: "অভিযাত্রী_নক্ষত্র_০৭", score: 23.75, accuracyPercent: 95.0, streakCount: 11 },
          { rank: 3, handle: "ক্যালকুলাস_মাস্টার_২১", score: 23.0, accuracyPercent: 92.0, streakCount: 9 },
          { rank: 4, handle: "আপনি (বর্তমান স্কোর)", score: 21.5, accuracyPercent: 88.0, streakCount: 7, isCurrentUser: true }
        ]),
      });
      return;
    }
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        id: "chal_nat_2026",
        titleBn: "জাতীয় স্টেম অলিম্পিয়াড ২০২৬ - পর্ব ০১",
        titleEn: "National STEM Olympiad 2026 - Phase 1",
        startTimeRemainingSeconds: 1200,
        registeredCount: 4850,
        durationMinutes: 25,
        totalQuestions: 25,
        negativeMarkingRatio: 0.25,
        syllabusSummaryBn: "এইচএসসি পদার্থবিজ্ঞান (বলবিদ্যা ও কাজ-শক্তি), রসায়ন (পর্যায়বৃত্ত ধর্ম) ও উচ্চতর গণিত (ম্যাট্রিক্স)"
      }),
    });
  });

  // Mock Quiz Attempts Individual Answer Submission
  await page.route(/\/api\/v1\/quiz-attempts/, async (route) => {
    const idempotencyKey = route.request().headers()['x-idempotency-key'] || 'test-mock-key';
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      headers: {
        'x-idempotency-key': idempotencyKey,
      },
      body: JSON.stringify({
        status: 'ACCEPTED',
        idempotency_key: idempotencyKey,
        saved: true,
        timestamp: new Date().toISOString(),
      }),
    });
  });

  // Mock Tuition Marketplace Listing Endpoint
  await page.route(/\/api\/v1\/tuitions/, async (route) => {
    if (route.request().method() === 'POST') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'REGISTERED',
          message_bn: 'দ্বিপাক্ষিক সম্মতি অনুরোধ নিবন্ধিত হয়েছে।',
        }),
      });
      return;
    }
    const tuitionItems = [
          {
            id: 'tui_101',
            classGrade: 11,
            subject: 'পদার্থবিজ্ঞান ও উচ্চতর গণিত',
            medium: 'বাংলা মাধ্যম',
            location: 'ঢাকা, ধানমন্ডি',
            mode: 'হোম টিউশন',
            salary: '৮,০০০ - ১০,০০০ টাকা/মাস',
            daysPerWeek: 3,
            postedDate: '১৩ অক্টোবর ২০২৬',
            contactUnlocked: false,
            tutorInstitution: 'বুয়েট (ECE)',
            isVerifiedTutor: true,
          },
          {
            id: 'tui_102',
            classGrade: 9,
            subject: 'সাধারণ বিজ্ঞান ও গণিত',
            medium: 'ইংরেজি ভার্সন',
            location: 'ঢাকা, উত্তরা',
            mode: 'অনলাইন',
            salary: '৬,০০০ - ৭,০০০ টাকা/মাস',
            daysPerWeek: 2,
            postedDate: '১৪ অক্টোবর ২০২৬',
            contactUnlocked: false,
            tutorInstitution: 'ঢাকা বিশ্ববিদ্যালয় (ফলিত গণিত)',
            isVerifiedTutor: true,
          },
    ];
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        total: tuitionItems.length,
        data: tuitionItems,
        items: tuitionItems,
      }),
    });
  });

  // Mock Escrow Vault Deposit & Checkout Endpoint
  await page.route('**/api/v1/payments/escrow/deposit', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        vault_id: 'escrow_vault_test_999',
        status: 'HELD_IN_ESCROW',
        currency: 'BDT',
        gross_amount: 8000.0,
        platform_fee_percent: 5.0,
        net_tutor_payout: 7600.0,
        trx_id: 'TRX_BKASH_99228833',
        message_bn: 'টিউশন ফি সফলভাবে এসক্রো ভল্টে জমা হয়েছে।',
      }),
    });
  });
}

/**
 * Custom extended Playwright test fixture
 */
export const test = base.extend<{
  mockApi: void;
  consoleTrap: ReturnType<typeof setupConsoleTrap>;
}>({
  mockApi: async ({ page }, use) => {
    await setupMockApiRoutes(page);
    await use();
  },
  consoleTrap: async ({ page }, use) => {
    const trap = setupConsoleTrap(page);
    await use(trap);
  },
});

export { expect };
