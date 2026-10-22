/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Quiz Interface - Primitives Barrel
 * TOPIC:     Unified Academic Quiz Suite Barrel Exports
 * FILE:      frontend/src/components/quiz/index.ts
 * PHASE:     Phase 141 - Rebuild Shared Components
 * PURPOSE:   Centralizes export of all academic quiz & question UI components:
 *            QuestionCard, OptionCard, KaTeXRenderer, ScientificDiagram,
 *            QuizProgress, QuizResultSummary, ExplanationBlock, and ServerTimer.
 * STANDARDS: Zero-Emoji, WCAG 2.2 AAA Contrast, Academic Editorial Monograph Style
 */

export * from './katex-renderer';
export * from './question-card';
export * from './option-card';
export * from './scientific-diagram';
export * from './server-timer';
export * from './quiz-progress';
export * from './quiz-result-summary';
export * from './explanation-block';
