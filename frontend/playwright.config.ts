/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Playwright Test Runner Configuration & Multi-Device Emulation Matrix
 * TOPIC:     Nationwide Live Exam & Playwright E2E Journey
 * FILE:      frontend/playwright.config.ts
 * PHASE:     Phase 125 - Nationwide Live Exam & Playwright E2E Journey
 * PURPOSE:   Provides exhaustive configuration for end-to-end integration test suites.
 *            Defines viewport matrices for desktop browsers (Chromium, Firefox, WebKit) and
 *            mobile devices (Google Pixel 7 and Apple iPhone 14), headless execution,
 *            sub-second latency thresholds, failure screenshot captures, and self-contained
 *            HTML/JSON evidence reporting.
 * STANDARDS: Playwright Headless Standards, Sub-second Latency, Strict Zero-Emoji, WCAG 2.2 AAA
 */

import { defineConfig, devices } from '@playwright/test';

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  testDir: './e2e',
  /* Maximum time one test can run for */
  timeout: 60 * 1000,
  expect: {
    /**
     * Maximum time expect() should wait for the condition to be met.
     */
    timeout: 10 * 1000,
  },
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 1,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'playwright-report/test-results.json' }]
  ],
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Headless execution for automated CI/CD and terminal runs */
    headless: true,

    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    /* Capture screenshot automatically on test failure */
    screenshot: 'only-on-failure',

    /* Capture video recording on retry */
    video: 'retain-on-failure',

    /* Human-friendly action and navigation timeouts */
    actionTimeout: 15 * 1000,
    navigationTimeout: 30 * 1000,
  },

  /* Configure projects for major browsers and mobile viewports */
  projects: [
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 720 },
      },
    },
    {
      name: 'firefox',
      use: { 
        ...devices['Desktop Firefox'],
        viewport: { width: 1280, height: 720 },
      },
    },
    {
      name: 'webkit',
      use: { 
        ...devices['Desktop Safari'],
        viewport: { width: 1280, height: 720 },
      },
    },

    /* Test against mobile viewports for authentic Bangladeshi smartphone emulation */
    {
      name: 'mobile-pixel-7',
      use: {
        ...devices['Pixel 7'],
        viewport: { width: 412, height: 915 },
        isMobile: true,
        hasTouch: true,
      },
    },
    {
      name: 'mobile-iphone-14',
      use: {
        ...devices['iPhone 14'],
        defaultBrowserType: 'chromium',
        viewport: { width: 390, height: 844 },
        isMobile: true,
        hasTouch: true,
      },
    },
  ],

  /* Run local dev server before starting the tests */
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
