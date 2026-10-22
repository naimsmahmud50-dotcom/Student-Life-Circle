"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Parent-Teacher Conference & Escrow Dispute Tribunal
 * TOPIC:     Phase 130 Institutional Appointment & Formal Escrow Arbitration
 * FILE:      backend/portal/ptc_booking.py
 * PHASE:     Phase 130 - Institutional PTC & Escrow Dispute Tribunal
 * PURPOSE:   Provides formal institutional Parent-Teacher Conference (PTC) booking,
 *            time-slot reservation conflict avoidance, discussion agenda tracking,
 *            and Zero-IDOR tenancy access defense.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Strict Supabase RLS, Pure Academic UI
 */
"""

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class UnauthorizedPTCAccessException(PermissionError):
    """Raised when an actor attempts to inspect or mutate an appointment they do not belong to (Zero-IDOR)."""
    pass


class PTCSlotConflictException(ValueError):
    """Raised when an educator or guardian is already booked for an overlapping time window."""
    pass


class PTCStatus(str, Enum):
    REQUESTED = "REQUESTED"
    CONFIRMED = "CONFIRMED"
    IN_SESSION = "IN_SESSION"
    CONCLUDED = "CONCLUDED"
    RESCHEDULED = "RESCHEDULED"
    CANCELLED = "CANCELLED"


class PTCAgendaTopic(str, Enum):
    ACADEMIC_PROGRESS = "ACADEMIC_PROGRESS"
    EXAM_PREPARATION = "EXAM_PREPARATION"
    DISCIPLINE_BEHAVIOR = "DISCIPLINE_BEHAVIOR"
    MENTAL_WELLBEING = "MENTAL_WELLBEING"
    TUITION_ROADMAP = "TUITION_ROADMAP"


@dataclass
class AppointmentSlot:
    slot_id: str
    start_timestamp: float
    end_timestamp: float
    duration_minutes: int = 30


@dataclass
class PTCAppointment:
    id: str
    guardian_id: str
    teacher_id: str
    student_id: str
    slot: AppointmentSlot
    agenda_topic: PTCAgendaTopic
    notes_bn: str
    notes_en: str
    status: PTCStatus = PTCStatus.REQUESTED
    meeting_passcode: str = field(default="")
    concluded_summary: str = field(default="")
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


class PTCBookingManager:
    """
    Manages institutional Parent-Teacher Conference appointments,
    detecting scheduling conflicts and enforcing Zero-IDOR tenancy.
    """

    def __init__(self):
        # appointment_id -> PTCAppointment
        self._appointments: Dict[str, PTCAppointment] = {}

    @classmethod
    def generate_meeting_passcode(cls, appt_id: str, guardian_id: str, teacher_id: str) -> str:
        """Generates cryptographic 6-digit conference access code."""
        digest = hashlib.sha256(f"{appt_id}:{guardian_id}:{teacher_id}".encode("utf-8")).hexdigest()
        return f"{int(digest[:6], 16) % 900000 + 100000}"

    def assert_authorized_party(self, appointment: PTCAppointment, caller_id: str) -> None:
        """
        Zero-IDOR Tenancy Invariant:
        Only the designated Guardian or paired Educator has clearance to access appointment details.
        """
        if caller_id != appointment.guardian_id and caller_id != appointment.teacher_id:
            raise UnauthorizedPTCAccessException(
                f"Zero-IDOR Violation: User '{caller_id}' is not an authorized party "
                f"to PTC appointment '{appointment.id}'."
            )

    def _has_conflict(self, teacher_id: str, start_ts: float, end_ts: float) -> bool:
        """Checks if the teacher has any active appointment overlapping [start_ts, end_ts]."""
        for appt in self._appointments.values():
            if appt.teacher_id == teacher_id and appt.status in [
                PTCStatus.REQUESTED,
                PTCStatus.CONFIRMED,
                PTCStatus.IN_SESSION
            ]:
                # Overlap check
                if not (end_ts <= appt.slot.start_timestamp or start_ts >= appt.slot.end_timestamp):
                    return True
        return False

    def book_appointment(
        self,
        appointment_id: str,
        guardian_id: str,
        teacher_id: str,
        student_id: str,
        slot_id: str,
        start_timestamp: float,
        duration_minutes: int,
        agenda_topic: PTCAgendaTopic,
        notes_bn: str,
        notes_en: str
    ) -> PTCAppointment:
        """
        Reserves a formal PTC appointment if the educator is free during the slot.
        """
        end_timestamp = start_timestamp + (duration_minutes * 60.0)

        # Conflict check
        if self._has_conflict(teacher_id, start_timestamp, end_timestamp):
            raise PTCSlotConflictException(
                f"Scheduling Conflict: Teacher '{teacher_id}' is already booked for an appointment during this slot."
            )

        passcode = self.generate_meeting_passcode(appointment_id, guardian_id, teacher_id)
        slot = AppointmentSlot(
            slot_id=slot_id,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            duration_minutes=duration_minutes
        )

        appt = PTCAppointment(
            id=appointment_id,
            guardian_id=guardian_id,
            teacher_id=teacher_id,
            student_id=student_id,
            slot=slot,
            agenda_topic=agenda_topic,
            notes_bn=notes_bn,
            notes_en=notes_en,
            status=PTCStatus.REQUESTED,
            meeting_passcode=passcode
        )
        self._appointments[appointment_id] = appt
        return appt

    def confirm_appointment(self, appointment_id: str, caller_id: str) -> PTCAppointment:
        """Teacher confirms the conference request."""
        appt = self._appointments.get(appointment_id)
        if not appt:
            raise KeyError(f"Appointment '{appointment_id}' not found.")

        self.assert_authorized_party(appt, caller_id)
        appt.status = PTCStatus.CONFIRMED
        appt.updated_at = time.time()
        return appt

    def conclude_appointment(
        self,
        appointment_id: str,
        caller_id: str,
        summary_bn: str
    ) -> PTCAppointment:
        """Concludes the appointment and records institutional notes."""
        appt = self._appointments.get(appointment_id)
        if not appt:
            raise KeyError(f"Appointment '{appointment_id}' not found.")

        self.assert_authorized_party(appt, caller_id)
        appt.status = PTCStatus.CONCLUDED
        appt.concluded_summary = summary_bn
        appt.updated_at = time.time()
        return appt

    def cancel_appointment(
        self,
        appointment_id: str,
        caller_id: str,
        reason: str
    ) -> PTCAppointment:
        """Cancels the appointment by either party."""
        appt = self._appointments.get(appointment_id)
        if not appt:
            raise KeyError(f"Appointment '{appointment_id}' not found.")

        self.assert_authorized_party(appt, caller_id)
        appt.status = PTCStatus.CANCELLED
        appt.concluded_summary = f"Cancelled by {caller_id}: {reason}"
        appt.updated_at = time.time()
        return appt

    def get_appointment_for_actor(
        self,
        appointment_id: str,
        caller_id: str
    ) -> PTCAppointment:
        """
        Retrieves appointment strictly asserting Zero-IDOR tenancy clearance.
        """
        appt = self._appointments.get(appointment_id)
        if not appt:
            raise KeyError(f"Appointment '{appointment_id}' not found.")

        self.assert_authorized_party(appt, caller_id)
        return appt
