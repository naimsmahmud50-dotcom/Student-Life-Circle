"""
/**
 * DEVELOPER ARCHITECTURE NOTE:
 * MODULE:    Parent-Teacher Conference & Escrow Dispute Tribunal
 * TOPIC:     Phase 130 Institutional Appointment & Formal Escrow Arbitration
 * FILE:      backend/portal/__init__.py
 * PHASE:     Phase 130 - Institutional PTC & Escrow Dispute Tribunal
 * PURPOSE:   Exports the parent-teacher conference booking system and models.
 * STANDARDS: Zero-Emoji, Zero-IDOR, Strict Supabase RLS, Pure Academic UI
 */
"""

from backend.portal.ptc_booking import (
    PTCBookingManager,
    PTCStatus,
    PTCAgendaTopic,
    AppointmentSlot,
    PTCAppointment,
    UnauthorizedPTCAccessException,
    PTCSlotConflictException,
)

__all__ = [
    "PTCBookingManager",
    "PTCStatus",
    "PTCAgendaTopic",
    "AppointmentSlot",
    "PTCAppointment",
    "UnauthorizedPTCAccessException",
    "PTCSlotConflictException",
]
