# TASKS: Phase 129 — Multi-Dialect Regional Audio Tutoring & Voice Viva-Voce Evaluator

- [x] **Task 1**: Implement `backend/audio/__init__.py` and `backend/audio/viva_evaluator.py` with multi-dialect normalizer (Chittagong, Sylhet, Barisal, Standard), NCTB 4-tier rubric evaluation, and 15-minute in-memory buffer manager.
- [x] **Task 2**: Implement `backend/migrations/007_viva_evaluator_rls.sql` with zero-audio-retention policy and strict Supabase RLS.
- [x] **Task 3**: Implement `frontend/src/pages/viva/evaluator.tsx` with formal audio laboratory console, segmented VU level meter, 3D tactile buttons, dialect selector, and rubric scorecard.
- [x] **Task 4**: Implement `backend/tests/test_phase129_viva_evaluator.py` automated test suite.
- [x] **Task 5**: Run `python3 backend/scripts/run_zero_emoji_sweep.py` asserting 0 emoji violations across all repository files.
- [x] **Task 6**: Run `python3 -m unittest backend/tests/test_phase129_viva_evaluator.py` asserting all Phase 129 tests pass.
- [x] **Task 7**: Run full repository test discovery (`python3 -m unittest discover -s backend/tests -p "test_*.py"`) verifying all 1,440+ existing tests pass with 0 failures and 0 errors.
- [x] **Task 8**: Build Next.js frontend (`npm run build`) ensuring all static pages compile cleanly.
- [x] **Task 9**: Generate `PHASE_129_VIVA_EVALUATOR_REPORT.md` artifact and conclude.
