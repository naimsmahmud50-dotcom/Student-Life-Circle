"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    National STEM Olympiad Arena & Tournament Engine
TOPIC:     Phase 127 Real-time Competitive Olympiad & Live Bracket Ladder
FILE:      backend/olympiad/__init__.py
PHASE:     Phase 127 - National Live Multiplayer STEM Olympiad Arena
PURPOSE:   Package initializer for the National STEM Olympiad & Tournament Engine module.
STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Sub-50ms Latency
========================================================================================
"""

from .tournament_engine import (
    TournamentEngine,
    OlympiadParticipant,
    TournamentMatch,
    MedalTier,
    CheatingAnomalyException,
)

__all__ = [
    "TournamentEngine",
    "OlympiadParticipant",
    "TournamentMatch",
    "MedalTier",
    "CheatingAnomalyException",
]
