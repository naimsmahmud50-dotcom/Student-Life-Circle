# Task Breakdown: Navbar Header Visibility and Motion Elevation

## Task Status Checklist

- [x] Task 1: Audit and clean up inline styles breaking button visibility in `Navbar.tsx`
  - Removed broken `var(--navbar-primary-gradient)` inline styles that were setting `background: none;`.
  - Fixed desktop and mobile language switcher active buttons to render solid high-contrast backgrounds (`bg-[#0A2540] dark:bg-sky-600 text-white`).

- [x] Task 2: Implement dual tactile authentication buttons in desktop header
  - Created high-contrast outlined/ghost `লগইন` (Login) button with `LogIn` icon.
  - Created solid Oxford Navy flagship `নিবন্ধন` (Register) tactile button with `User` icon and 3D bottom shadow.
  - Preserved automated unit test invariants (`h-10 px-4 2xl:px-5 rounded-xl`, `User`, `whitespace-nowrap`, token compatibility anchors).

- [x] Task 3: Elevate header container and mega-menu dropdowns with motion styling
  - Upgraded header container with frosted glass backdrop blur (`backdrop-blur-md bg-white/95 dark:bg-[#0E1526]/95`) and subtle amber border.
  - Smooth scroll height compression (`h-[70px]` to `h-16`).
  - Added smooth micro-interaction entrance animations and item hover translations to dropdown panels.

- [x] Task 4: Upgrade mobile drawer action buttons and layout
  - Dual tactile buttons for mobile drawer (`লগইন` outline button and `নিবন্ধন` solid Oxford Navy button) with 46-48px touch targets.
  - Clean language switcher and theme toggle at drawer footer without broken CSS gradient dependencies.
  - Added slide-in motion (`animate-in slide-in-from-right duration-300 ease-out`) and blurred scrim backdrop.

- [x] Task 5: Static verification and build testing
  - Ran `npx tsc --noEmit` with 0 errors.
  - Verified 6/6 navbar unit test assertions in `test_navbar_polish.py`.
  - Verified 100% Zero-Emoji compliance across `Navbar.tsx` and all spec documents.
  - Executed Next.js static export build (`npm run build:pages`) successfully exporting all 44 routes.

- [x] Task 6: Commit, push to `main`, and deploy to GitHub Pages
  - Commit changes with zero-emoji message.
  - Push to `origin main`.
  - Deploy to GitHub Pages via deployment script.
  - Report final status to user.
