# Plan: 049 - Live MCQ Routine & Mega Model Test Calendar Hub

## Technical Architecture & Design Decisions
1. **Module Isolation**:
   - `frontend/src/modules/exam-routine/`: Isolated UI components, custom hooks, and Zod schemas.
   - `frontend/src/pages/routines/index.tsx`: Next.js Page route wrapper with `FeatureGate`.
   - `backend/app/api/v1/endpoints/exam_routine_router.py`: Isolated FastAPI router mounted at `/routines`.
   - `backend/app/services/exam_routine_service.py`: Business logic for routines, negative marking, and percentiles.
   - `backend/app/schemas/exam_routine_schema.py`: Pydantic v2 schemas.
2. **Database Migration**:
   - `backend/migrations/017_exam_routine_and_model_test_rls.sql`: Creates `exam_routines` and `routine_subscriptions` with Supabase RLS policies and rollback instructions.
3. **Feature Flagging**:
   - `frontend/src/config/featureFlags.ts` & `backend/app/core/config.py`: `FEATURE_EXAM_ROUTINE` default `false`.
4. **Integration Points**:
   - `Navbar.tsx`: Single conditional link inside navigation.
   - `registry.ts`: Entry 70 appended to `MODULES_REGISTRY`.
   - `router.py`: `api_router.include_router(exam_routine_router, prefix="/routines", tags=["Exam Routines"])`.
5. **Testing**:
   - Backend unit tests in `backend/tests/test_phase164_exam_routine_and_model_test.py`.
   - Frontend component test in `frontend/src/modules/exam-routine/__tests__/examRoutine.test.mjs`.
