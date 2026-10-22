# Bug Fix: Restrict optimizePackageImports in Next.js Configuration

## Remediation Details
1. Target File: `frontend/next.config.js`
2. Change: Removed non-barrel packages (`@radix-ui/react-dialog`, `@radix-ui/react-dropdown-menu`, `@radix-ui/react-slot`, `@radix-ui/react-tabs`, `zustand`) from `experimental.optimizePackageImports`.
3. Kept `optimizePackageImports: ['lucide-react']`, which is the intended use case for barrel import optimization.
4. Cleared `.next` build cache to eliminate any stale synthetic barrel chunks.
5. Restarted the development server cleanly on port 3000.

## Impact & Safety
- Zero application code was modified outside of `frontend/next.config.js`.
- All Radix UI primitives continue to import normally via direct ESM imports without barrel overhead.
- No other features or routes are adversely affected.
