# Bug Assessment: Webpack Runtime TypeError (__webpack_require__.t is not a function)

## Summary
When navigating to pages that utilize the core `Button` component or other Radix UI primitives (such as `/career`), a fatal runtime error appeared in Next.js Webpack Pages Router:
`Runtime TypeError: __webpack_require__.t is not a function`
occurring at `(pages-dir-browser)/./node_modules/@radix-ui/react-slot/dist/index.mjs` through `__barrel_optimize__?names=Slot!=!...`.

## Root Cause Analysis
1. In `frontend/next.config.js`, the experimental option `optimizePackageImports` included:
   ```javascript
   optimizePackageImports: [
     'lucide-react',
     '@radix-ui/react-dialog',
     '@radix-ui/react-dropdown-menu',
     '@radix-ui/react-slot',
     '@radix-ui/react-tabs',
     'zustand',
   ]
   ```
2. `optimizePackageImports` is an SWC compiler transformation designed for large multi-export barrel packages (such as icon collections like `lucide-react`).
3. Small, single-purpose ESM packages like `@radix-ui/react-slot` only export two symbols (`Slot` and `Slottable`) and include namespace interop logic (`import * as React from 'react'`).
4. In Next.js Pages router with Webpack 5, applying `optimizePackageImports` to `@radix-ui/react-slot` caused Next.js to rewrite module imports to synthetic barrel loaders (`__barrel_optimize__?names=Slot!=!...`).
5. This loader relies on Webpack's `__webpack_require__.t` helper (fake namespace creation). Because Webpack's client runtime template did not anticipate dynamic inclusion of `.t` for Pages router client chunks on initial bundle creation, any navigation to `/career` resulted in an unhandled runtime exception: `__webpack_require__.t is not a function`.

## Risk Assessment & Scope
- High client-side crash impact across any route utilizing `Button` or Radix primitives if barrel optimization was enabled for them.
- Remediation must be strictly scoped to `frontend/next.config.js` to ensure zero disruption to any application logic, components, or API endpoints.
