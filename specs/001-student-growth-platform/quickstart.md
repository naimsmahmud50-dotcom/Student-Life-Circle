# Quickstart & Verification Guide: Student Growth Platform (অগ্রযাত্রা)

**Feature:** `specs/001-student-growth-platform`  
**Execution Mode:** Local Development & Continuous Verification  

---

## 1. Prerequisites
- Python 3.12+ (Python 3.14 compatible)
- Node.js 18+ (for Next.js frontend preview)
- PostgreSQL 16+ & Redis 7+ (for live deployment)

---

## 2. Backend Automated Verification
Run the comprehensive unit test suite covering:
1. Server-authoritative timekeeper & clock anti-tampering
2. Deterministic quiz question and option shuffling
3. Idempotent answer saves with network retry safety
4. Fair scoring with negative marking and automatic mistake queueing
5. Single-click question quarantine and immutable audit logging
6. Role-Based (RBAC) and Attribute-Based (ABAC) zero-IDOR protection
7. Triple deduplication (exact hash + token similarity)

```bash
PYTHONPATH=. python3 -m unittest backend/tests/test_quiz_engine.py
```

Expected Output:
```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```

---

## 3. Architecture Validation Checklist
- [x] **Zero-Emoji Policy**: All buttons, badges, and headings in `frontend/src/` use Lucide SVG vectors without cartoon emojis.
- [x] **Dual Themes**: Complete Light Mode (White ground) and Dark Mode (Deep Navy Slate) implemented with `ThemeToggle`.
- [x] **Server-Authoritative Clock**: Timers and expirations calculated strictly server-side in `backend/app/core/timekeeper.py`.
- [x] **Single-Click Quarantine**: Admin console and backend service at `backend/app/services/quarantine_service.py` and `frontend/src/pages/admin/quarantine.tsx`.
- [x] **Explanatory File Headers**: Every source file contains an explicit top-level block explaining purpose, module, and standards.
