# Bug Fix: Collaborative Study Circles & Gamified Bounty Tribunal Edge Cases

- **Slug**: `collaborative-study-and-bounty-tribunal`
- **Fixed**: 2026-10-14T19:27:10Z
- **Assessment**: ./assessment.md
- **Status**: applied

## Summary
Enforced role-based authorization for whiteboard modifications, clamped LaTeX formula lengths, and instituted duplicate pending submission guards in the bounty arena.

## Changes

| File | Change | Notes |
|------|--------|-------|
| `backend/app/services/study_room_service.py` | modified | Blocked OBSERVER role from modifying whiteboard; bounded formula length <= 2000 chars. |
| `backend/app/services/bounty_tribunal_service.py` | modified | Added active pending review duplicate guard per scholar. |
| `backend/tests/test_phase27_collaborative_study_and_bounties.py` | added tests | Added `test_observer_cannot_modify_whiteboard`, `test_formula_length_limit`, and `test_duplicate_pending_solution_rejected`. |

## Local Verification
- Commands run: `python3 -m unittest discover -s backend/tests -p "test_*.py"` -> 200 tests passed in 0.198s.
- Manual checks: Verified seed study room status is `ACTIVE` and WebRTC tokens are cryptographically generated.

## Deviations from Assessment
None.
