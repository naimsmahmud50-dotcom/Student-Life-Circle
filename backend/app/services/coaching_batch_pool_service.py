"""
Coaching Batch Pool Service for Agrojatra Platform.
Enables neighborhood multi-guardian micro-coaching batch creation,
fractional escrow cost-splitting (1/N) with zero-leak rounding reconciliation,
and real-time attendance telemetry.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional


class CoachingBatchPoolService:
    def __init__(self):
        # In-memory storage for coaching batches and session logs
        self._batches: Dict[str, Dict[str, Any]] = {}
        self._seed_default_batches()

    def _seed_default_batches(self):
        """Seed initial real-world micro-coaching batches for Dhaka and regional clusters."""
        b1_id = "BATCH-DHK-PHY-01"
        self._batches[b1_id] = {
            "batch_id": b1_id,
            "batch_title": "Dhanmondi HSC 2026 Advanced Physics Circle",
            "subject": "Physics (Vector & Mechanics)",
            "curriculum": "NCTB_SCIENCE",
            "lead_guardian_id": "guard-001",
            "total_monthly_fee_bdt": 6000.0,
            "max_capacity": 4,
            "guardians": [
                {
                    "guardian_id": "guard-001",
                    "guardian_name": "Rafiqul Islam",
                    "student_name": "Tanvir Islam",
                    "joined_at": "2026-10-01T10:00:00+00:00",
                    "escrow_status": "LOCKED",
                },
                {
                    "guardian_id": "guard-002",
                    "guardian_name": "Nasreen Sultana",
                    "student_name": "Sadia Sultana",
                    "joined_at": "2026-10-02T11:30:00+00:00",
                    "escrow_status": "LOCKED",
                },
                {
                    "guardian_id": "guard-003",
                    "guardian_name": "Mahbubur Rahman",
                    "student_name": "Farhan Rahman",
                    "joined_at": "2026-10-03T14:15:00+00:00",
                    "escrow_status": "LOCKED",
                },
            ],
            "sessions": [
                {
                    "session_id": "SES-001",
                    "session_topic": "Vector Calculus & Dot Products in Kinematics",
                    "attendees": ["guard-001", "guard-002", "guard-003"],
                    "attendance_pct": 100.0,
                    "duration_minutes": 90,
                    "mentor_notes": "All students demonstrated firm grasp of 3D unit vectors.",
                    "logged_at": "2026-10-10T16:00:00+00:00",
                }
            ],
            "status": "ACTIVE",
            "created_at": "2026-10-01T09:00:00+00:00",
        }

    def _recalculate_shares(self, batch: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Calculates exact 1/N escrow cost-splitting.
        Ensures sum of individual guardian shares equals total_monthly_fee_bdt to the exact cent,
        preventing fractional escrow rounding drift leaks.
        """
        guardians = batch["guardians"]
        n = len(guardians)
        if n == 0:
            return []

        total_fee = batch["total_monthly_fee_bdt"]
        base_split = round(total_fee / n, 2)

        # Calculate remainder discrepancy due to cents rounding
        calculated_total = round(base_split * n, 2)
        remainder_drift = round(total_fee - calculated_total, 2)

        shares = []
        for idx, g in enumerate(guardians):
            allocated = base_split
            if idx == 0:
                # Absorb remainder in lead guardian's allotment
                allocated = round(allocated + remainder_drift, 2)

            shares.append({
                "guardian_id": g["guardian_id"],
                "guardian_name": g["guardian_name"],
                "student_name": g["student_name"],
                "allocated_amount_bdt": allocated,
                "percentage_split": round((allocated / total_fee) * 100, 1),
                "escrow_status": g.get("escrow_status", "LOCKED"),
            })

        return shares

    def create_batch(
        self,
        batch_title: str,
        subject: str,
        lead_guardian_id: str,
        total_monthly_fee_bdt: float = 5000.0,
        max_capacity: int = 5,
        curriculum: str = "NCTB_SCIENCE",
        lead_guardian_name: str = "Lead Guardian",
        student_name: str = "Student 1",
    ) -> Dict[str, Any]:
        """Creates a new collaborative micro-coaching batch with lead guardian as first member."""
        batch_id = f"BATCH-{uuid.uuid4().hex[:8].upper()}"
        now_iso = datetime.now(timezone.utc).isoformat()

        cap = max(2, min(max_capacity, 15))
        fee = max(500.0, float(total_monthly_fee_bdt))

        new_batch = {
            "batch_id": batch_id,
            "batch_title": batch_title,
            "subject": subject,
            "curriculum": curriculum,
            "lead_guardian_id": lead_guardian_id,
            "total_monthly_fee_bdt": fee,
            "max_capacity": cap,
            "guardians": [
                {
                    "guardian_id": lead_guardian_id,
                    "guardian_name": lead_guardian_name,
                    "student_name": student_name,
                    "joined_at": now_iso,
                    "escrow_status": "LOCKED",
                }
            ],
            "sessions": [],
            "status": "FORMING",
            "created_at": now_iso,
        }

        self._batches[batch_id] = new_batch
        shares = self._recalculate_shares(new_batch)

        return {
            "batch_id": batch_id,
            "batch_title": batch_title,
            "subject": subject,
            "total_monthly_fee_bdt": fee,
            "max_capacity": cap,
            "current_guardians": 1,
            "cost_per_guardian_bdt": shares[0]["allocated_amount_bdt"],
            "guardian_shares": shares,
            "status": "FORMING",
            "created_at": now_iso,
        }

    def join_guardian(
        self,
        batch_id: str,
        guardian_id: str,
        guardian_name: str,
        student_name: str,
    ) -> Dict[str, Any]:
        """Allows a neighborhood guardian to join the pool, dynamically redistributing the cost."""
        if batch_id not in self._batches:
            raise ValueError(f"Coaching batch with ID '{batch_id}' not found.")

        batch = self._batches[batch_id]

        if len(batch["guardians"]) >= batch["max_capacity"]:
            raise ValueError(f"Coaching batch is already at full capacity ({batch['max_capacity']}).")

        # Guard against duplicate joins
        for g in batch["guardians"]:
            if g["guardian_id"] == guardian_id:
                raise ValueError(f"Guardian '{guardian_id}' is already enrolled in this batch.")

        now_iso = datetime.now(timezone.utc).isoformat()
        batch["guardians"].append({
            "guardian_id": guardian_id,
            "guardian_name": guardian_name,
            "student_name": student_name,
            "joined_at": now_iso,
            "escrow_status": "LOCKED",
        })

        if len(batch["guardians"]) >= batch["max_capacity"]:
            batch["status"] = "FULL_ACTIVE"
        else:
            batch["status"] = "ACTIVE"

        shares = self._recalculate_shares(batch)
        cost_per = round(batch["total_monthly_fee_bdt"] / len(batch["guardians"]), 2)

        return {
            "batch_id": batch_id,
            "batch_title": batch["batch_title"],
            "subject": batch["subject"],
            "total_monthly_fee_bdt": batch["total_monthly_fee_bdt"],
            "max_capacity": batch["max_capacity"],
            "current_guardians": len(batch["guardians"]),
            "cost_per_guardian_bdt": cost_per,
            "guardian_shares": shares,
            "status": batch["status"],
            "created_at": batch["created_at"],
        }

    def log_session_attendance(
        self,
        batch_id: str,
        session_topic: str,
        attendees: List[str],
        duration_minutes: int = 60,
        mentor_notes: str = "",
    ) -> Dict[str, Any]:
        """Logs session completion and attendee telemetry for guardian visibility."""
        if batch_id not in self._batches:
            raise ValueError(f"Coaching batch with ID '{batch_id}' not found.")

        batch = self._batches[batch_id]
        total_enrolled = len(batch["guardians"])
        att_count = len(attendees)
        att_pct = round((att_count / max(total_enrolled, 1)) * 100.0, 1) if total_enrolled > 0 else 0.0

        session_id = f"SES-{uuid.uuid4().hex[:6].upper()}"
        now_iso = datetime.now(timezone.utc).isoformat()

        session_entry = {
            "session_id": session_id,
            "session_topic": session_topic,
            "attendees": attendees,
            "attendance_pct": att_pct,
            "duration_minutes": duration_minutes,
            "mentor_notes": mentor_notes,
            "logged_at": now_iso,
        }

        batch["sessions"].append(session_entry)

        return {
            "session_id": session_id,
            "batch_id": batch_id,
            "session_topic": session_topic,
            "attendee_count": att_count,
            "attendance_pct": att_pct,
            "logged_at": now_iso,
        }

    def get_batch_details(self, batch_id: str) -> Dict[str, Any]:
        """Retrieves comprehensive details of a coaching batch with computed shares."""
        if batch_id not in self._batches:
            raise ValueError(f"Coaching batch with ID '{batch_id}' not found.")

        batch = self._batches[batch_id]
        shares = self._recalculate_shares(batch)
        cost_per = round(batch["total_monthly_fee_bdt"] / max(len(batch["guardians"]), 1), 2)

        return {
            "batch_id": batch["batch_id"],
            "batch_title": batch["batch_title"],
            "subject": batch["subject"],
            "curriculum": batch["curriculum"],
            "total_monthly_fee_bdt": batch["total_monthly_fee_bdt"],
            "max_capacity": batch["max_capacity"],
            "current_guardians": len(batch["guardians"]),
            "cost_per_guardian_bdt": cost_per,
            "guardian_shares": shares,
            "sessions": batch["sessions"],
            "status": batch["status"],
            "created_at": batch["created_at"],
        }

    def list_batches(self) -> List[Dict[str, Any]]:
        """Lists all available coaching batches."""
        result = []
        for b in self._batches.values():
            shares = self._recalculate_shares(b)
            cost_per = round(b["total_monthly_fee_bdt"] / max(len(b["guardians"]), 1), 2)
            result.append({
                "batch_id": b["batch_id"],
                "batch_title": b["batch_title"],
                "subject": b["subject"],
                "total_monthly_fee_bdt": b["total_monthly_fee_bdt"],
                "max_capacity": b["max_capacity"],
                "current_guardians": len(b["guardians"]),
                "cost_per_guardian_bdt": cost_per,
                "status": b["status"],
            })
        return result


coaching_batch_pool_service = CoachingBatchPoolService()
