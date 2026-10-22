/**
 * ========================================================================================
 * DEVELOPER TEST SCRIPT - NO AUTO-REFRESH VERIFICATION:
 * MODULE:    Playwright Headless Browser Verification for HMR Stability
 * FILE:      frontend/scripts/test-no-auto-refresh.js
 * PURPOSE:   Proves that http://localhost:3000/ loads cleanly and does NOT auto-refresh
 *            in a loop. Monitors navigations and console messages over an extended window.
 * STANDARDS: Strict Zero-Emoji Policy
 * ========================================================================================
 */

const { chromium } = require('@playwright/test');
const path = require('path');

(async () => {
  console.log('[TEST] Launching browser to verify auto-refresh stability...');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/opt/google/chrome/chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });

  const page = await context.newPage();

  let isLoaded = false;
  let reloadsAfterLoad = 0;
  page.on('framenavigated', (frame) => {
    if (frame === page.mainFrame()) {
      if (isLoaded) {
        reloadsAfterLoad++;
        console.log(`[UNEXPECTED RELOAD #${reloadsAfterLoad}] ${frame.url()}`);
      } else {
        console.log(`[INITIAL NAVIGATE] ${frame.url()}`);
      }
    }
  });

  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      consoleErrors.push(msg.text());
    }
  });

  console.log('[TEST] Navigating to http://localhost:3000/ ...');
  await page.goto('http://localhost:3000/', { waitUntil: 'networkidle', timeout: 30000 });
  isLoaded = true;

  console.log('[TEST] Page loaded. Observing for 10 seconds to detect any unexpected reloads...');
  await page.waitForTimeout(10000);

  // Check how many reloads occurred after load
  console.log(`[TEST] Post-load reloads observed: ${reloadsAfterLoad}`);

  // Check header text
  const headerBrand = await page.$eval('header span', (el) => el.textContent.trim()).catch(() => 'NOT_FOUND');
  console.log(`[TEST] Brand element text: "${headerBrand}"`);

  // Check for any nextjs error overlays
  const hasErrorOverlay = await page.evaluate(() => {
    const nextPortal = document.querySelector('nextjs-portal');
    if (!nextPortal) return false;
    const shadow = nextPortal.shadowRoot;
    if (!shadow) return false;
    return !!shadow.querySelector('[data-nextjs-dialog-overlay]') || !!shadow.querySelector('[data-nextjs-toast][data-error="true"]');
  });
  console.log(`[TEST] Next.js Error Overlay present: ${hasErrorOverlay}`);

  // Take screenshot
  const screenshotPath = '/home/mahmud-hasan/.gemini/antigravity/brain/c5c668bd-b2fe-422c-9bde-01b605b414be/localhost_autorefresh_fixed.png';
  await page.screenshot({ path: screenshotPath, fullPage: false });
  console.log(`[TEST] Screenshot saved to ${screenshotPath}`);

  await browser.close();

  if (reloadsAfterLoad > 0) {
    console.error(`[FAIL] Page auto-reloaded ${reloadsAfterLoad} time(s) after load!`);
    process.exit(1);
  }

  if (hasErrorOverlay) {
    console.error('[FAIL] Next.js error overlay is active on the page!');
    process.exit(1);
  }

  console.log('[SUCCESS] Auto-refresh loop is 100% fixed! Page remained stable with 0 reloads.');
})();
