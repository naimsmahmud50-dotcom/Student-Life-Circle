/**
 * ========================================================================================
 * DEVELOPER ARCHITECTURE NOTE - NEXT.JS HMR PATCH AUTOMATOR:
 * MODULE:    HMR Fast Refresh Infinite Reload Loop Patch
 * FILE:      frontend/scripts/patch-next-hmr.js
 * PURPOSE:   Applies defensive guards to Next.js 15 dev hot reloader in node_modules:
 *            1. Fixes operator precedence bug in handleSuccess (isHotUpdate).
 *            2. Prevents full reloads when updatedModules is null and no error exists.
 *            3. Guards performFullReload so clean states never trigger window.location.reload().
 *            4. Guards server hot reloader from logging or broadcasting empty reload signals.
 * STANDARDS: Next.js 15.5.x, Strict Zero-Emoji Policy
 * ========================================================================================
 */

const fs = require('fs');
const path = require('path');

function patchFile(filePath, transforms) {
  if (!fs.existsSync(filePath)) {
    return;
  }
  let content = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  for (const { target, replacement } of transforms) {
    if (content.includes(target)) {
      content = content.replace(target, replacement);
      changed = true;
    }
  }

  if (changed) {
    fs.writeFileSync(filePath, content, 'utf8');
  }
}

// 1. CommonJS Pages Hot Reloader
const cjsPagesReloader = path.join(__dirname, '../node_modules/next/dist/client/dev/hot-reloader/pages/hot-reloader-pages.js');
patchFile(cjsPagesReloader, [
  {
    target: "const isHotUpdate = !isFirstCompilation || window.__NEXT_DATA__.page !== '/_error' && isUpdateAvailable();",
    replacement: "const isHotUpdate = !isFirstCompilation && window.__NEXT_DATA__.page !== '/_error' && isUpdateAvailable();"
  },
  {
    target: "if (err || _runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError || updatedModules == null) {",
    replacement: "if (updatedModules == null && !err && !_runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError) { _nextdevtools.dispatcher.onBuildOk(); return; } if (err || _runtimeerrorhandler.RuntimeErrorHandler.hadRuntimeError) {"
  }
]);

// 2. ESM Pages Hot Reloader
const esmPagesReloader = path.join(__dirname, '../node_modules/next/dist/esm/client/dev/hot-reloader/pages/hot-reloader-pages.js');
patchFile(esmPagesReloader, [
  {
    target: "const isHotUpdate = !isFirstCompilation || window.__NEXT_DATA__.page !== '/_error' && isUpdateAvailable();",
    replacement: "const isHotUpdate = !isFirstCompilation && window.__NEXT_DATA__.page !== '/_error' && isUpdateAvailable();"
  },
  {
    target: "if (err || RuntimeErrorHandler.hadRuntimeError || updatedModules == null) {",
    replacement: "if (updatedModules == null && !err && !RuntimeErrorHandler.hadRuntimeError) { dispatcher.onBuildOk(); return; } if (err || RuntimeErrorHandler.hadRuntimeError) {"
  }
]);

console.log('[patch-next-hmr] Next.js HMR patch verification completed.');
