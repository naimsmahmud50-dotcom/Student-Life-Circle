/**
 * ========================================================================================
 * MODULE:    PostCSS Configuration
 * TOPIC:     Tailwind CSS & Autoprefixer Build Pipeline
 * FILE:      frontend/postcss.config.js
 * PURPOSE:   Applies Tailwind utility preprocessing and browser vendor prefixing.
 * AUDIENCE:  Build Pipeline, Webpack & Next.js Compiler
 * STANDARDS: PostCSS 8 Standard
 * ========================================================================================
 */

module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
