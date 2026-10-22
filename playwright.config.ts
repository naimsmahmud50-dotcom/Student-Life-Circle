/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - ROOT PLAYWRIGHT FORWARDER:
 * MODULE:    Root Playwright Configuration Forwarder
 * TOPIC:     Unified Monorepo & Root E2E Execution Bridge
 * FILE:      playwright.config.ts
 * PURPOSE:   Forwards test configurations to frontend/playwright.config.ts, allowing tests
 *            to be executed directly from repository root via `npx playwright test` or
 *            from within the `frontend/` workspace directory.
 * AUDIENCE:  DevOps Engineers, CI/CD Pipelines & Test Automation Engineers
 * STANDARDS: Strict Zero-Emoji Architecture
 * ========================================================================================
 */

import config from './frontend/playwright.config';

export default {
  ...config,
  testDir: './frontend/e2e',
};
