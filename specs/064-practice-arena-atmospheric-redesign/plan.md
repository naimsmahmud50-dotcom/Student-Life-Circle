# Technical Plan: 064-practice-arena-atmospheric-redesign

## 1. Architectural Strategy
The practice hub (`frontend/src/pages/practice.tsx`) will be upgraded with modern atmospheric design tokens, subtle background typographic watermarks, ambient radial glows, and high-contrast academic typography, harmonizing directly with `PageHeader` (`PRACTICE`).

### Visual Hierarchy:
1. **Interactive Question Navigator Bar (`NAVIGATOR`):**
   - Frosted ivory surface (`bg-white/95 dark:bg-[#0E1526]/95 backdrop-blur-md rounded-3xl border border-amber-200/70`).
   - Counter metrics: Active Question index, answered questions count, pending questions count, percentage progress bar.
   - 10-Question Quick Jump Matrix: Circular pills numbered 1 to 10 with status colors (Current active in Oxford Navy/Amber, Answered in Emerald with check icon, Unanswered in neutral border).
2. **Atmospheric Question Arena Card (`ARENA`):**
   - Warm ivory/slate canvas (`bg-[#FFFDF9]/95 dark:bg-[#0C1220]/95 border border-amber-200/80 rounded-3xl`).
   - Typographic watermark: `ARENA`.
   - Chapter pill & difficulty badge.
   - KaTeX high-contrast stem rendering.
   - Keyboard navigation helper pills (`[১] [২] [৩] [৪] / [A] [B] [C] [D]`).
   - Interactive `OptionCard` list with active selection and post-submit instant feedback.
   - Tactile 3D Action buttons (`Button` with `shadow-[0_4px_0_0_#051329] active:translate-y-1 active:shadow-none`).
3. **Formula Reference & Quick Revision Sheet (`FORMULAS`):**
   - Sage-Emerald container with watermark `FORMULAS`.
   - 4 LaTeX mathematical cards covering Newtonian Mechanics, Gravitational Law, Harmonic Motion, and Thermodynamics.
4. **Adaptive Scoring & Examination Protocol (`PROTOCOL`):**
   - Oxford Navy container with watermark `PROTOCOL` detailing zero-negative marking, offline buffering, idempotent submission, and Socratic analysis.
5. **Practice Strategy & FAQ Accordions (`STRATEGY`):**
   - Interactive accordion items answering board vs olympiad question strategies and calculation techniques.
6. **Flagship Completion & Review View (`MASTERY`):**
   - When exam completes, renders celebratory percentile badge, 4 metric cards, Socratic chapter mastery breakdown, and full answer review list.

---

## 2. Dependencies & Constraints
- Exclusively modify `frontend/src/pages/practice.tsx`.
- Use Lucide icons: `CheckCircle2`, `XCircle`, `RotateCcw`, `ArrowRight`, `ArrowLeft`, `Clock`, `WifiOff`, `Wifi`, `Sparkles`, `ChevronRight`, `ChevronDown`, `HelpCircle`, `Award`, `BarChart3`, `Check`, `BookOpen`, `Layers`, `Compass`, `FileText`, `Lightbulb`, `Target`, `ListChecks`.
- Zero emojis anywhere.
- TypeScript verification with `npx tsc --noEmit`.
- Next.js static build check with `npm run build:pages`.
