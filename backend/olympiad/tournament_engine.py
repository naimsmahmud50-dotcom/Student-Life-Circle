"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    National STEM Olympiad Arena & Tournament Engine
TOPIC:     Phase 127 Real-time Competitive Olympiad & Live Bracket Ladder
FILE:      backend/olympiad/tournament_engine.py
PHASE:     Phase 127 - National Live Multiplayer STEM Olympiad Arena
PURPOSE:   Provides Elo rating calculations, balanced matchmaking pairing,
           latency-compensated server timers, anti-cheating time-locked HMAC validation,
           tournament bracket progression, and NCTB/IMO percentile medal allocation.
STANDARDS: Zero-Emoji, Pure Academic Design, ASVS L2, Sub-50ms Latency
========================================================================================
"""

import hashlib
import hmac
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class CheatingAnomalyException(Exception):
    """Raised when submission telemetry violates cryptographic, latency, or clock invariants."""
    pass


class MedalTier(str, Enum):
    """Scholastic medal designations aligned with Bangladesh & International Olympiads."""
    GOLD = "স্বর্ণপদক"
    SILVER = "রৌপ্যপদক"
    BRONZE = "ব্রোঞ্জপদক"
    HONORABLE_MENTION = "বিশেষ সম্মাননা"
    PARTICIPATION = "অংশগ্রহণ সনদ"


@dataclass
class OlympiadParticipant:
    """Represents a competitive student candidate in the National STEM Olympiad arena."""
    id: str
    name: str
    elo_rating: float
    institution: str = "ঢাকা কলেজ"
    score: float = 0.0
    total_time_ms: float = 0.0
    matches_played: int = 0
    wins: int = 0


@dataclass
class TournamentMatch:
    """Represents a competitive head-to-head match within a tournament bracket."""
    match_id: str
    round_number: int
    round_name: str
    participant_a_id: str
    participant_b_id: str
    winner_id: Optional[str] = None
    score_a: float = 0.0
    score_b: float = 0.0
    latency_a_ms: float = 0.0
    latency_b_ms: float = 0.0
    status: str = "SCHEDULED"  # SCHEDULED, IN_PROGRESS, COMPLETED


class TournamentEngine:
    """
    Core competitive tournament engine powering the National STEM Olympiad Arena.
    Implements FIDE Elo calculations, network latency compensation, anti-cheat hashes,
    bracket ladder scheduling, and percentile-based medal tier distributions.
    """

    DEFAULT_K_FACTOR = 32.0
    MAX_ALLOWABLE_JITTER_MS = 1500.0  # Absorbs rural Bangladeshi mobile packet jitter
    MAX_SUBMISSION_TRANSIT_WINDOW_MS = 60000.0  # Stale submission threshold

    # ---------------------------------------------------------------------------
    # 1. Elo Rating & Matchmaking Pairing System
    # ---------------------------------------------------------------------------

    @staticmethod
    def calculate_expected_score(rating_a: float, rating_b: float) -> float:
        """
        Calculates the expected win probability for participant A against participant B
        using the standard logistic Elo curve.
        """
        exponent = (rating_b - rating_a) / 400.0
        return 1.0 / (1.0 + math.pow(10.0, exponent))

    @classmethod
    def update_elo_rating(
        cls,
        rating_a: float,
        rating_b: float,
        score_a: float,
        k_factor: Optional[float] = None,
    ) -> Tuple[float, float]:
        """
        Updates Elo ratings for two participants following a completed match.
        score_a: 1.0 for A win, 0.5 for draw, 0.0 for B win.
        Returns: (new_rating_a, new_rating_b) rounded to 2 decimal places.
        """
        if k_factor is None:
            k_factor = cls.DEFAULT_K_FACTOR

        expected_a = cls.calculate_expected_score(rating_a, rating_b)
        expected_b = 1.0 - expected_a
        score_b = 1.0 - score_a

        new_rating_a = rating_a + k_factor * (score_a - expected_a)
        new_rating_b = rating_b + k_factor * (score_b - expected_b)

        return round(new_rating_a, 2), round(new_rating_b, 2)

    @classmethod
    def pair_participants_by_elo(
        cls, participants: List[OlympiadParticipant]
    ) -> List[Tuple[OlympiadParticipant, OlympiadParticipant]]:
        """
        Pairs participants contiguous by Elo rating to ensure balanced competitive matches.
        Sorts descending by rating, pairing (P0, P1), (P2, P3), etc.
        """
        sorted_candidates = sorted(participants, key=lambda p: p.elo_rating, reverse=True)
        pairs: List[Tuple[OlympiadParticipant, OlympiadParticipant]] = []

        for i in range(0, len(sorted_candidates) - 1, 2):
            pairs.append((sorted_candidates[i], sorted_candidates[i + 1]))

        return pairs

    # ---------------------------------------------------------------------------
    # 2. Latency-Compensated Server Timer
    # ---------------------------------------------------------------------------

    @classmethod
    def validate_and_compensate_latency(
        cls,
        client_timestamp_ms: float,
        server_now_ms: float,
        rtt_ms: float,
        question_start_server_ms: float,
    ) -> float:
        """
        Validates client submission timestamp against server time and network RTT,
        neutralizing rural mobile network transit latency while detecting clock tampering.

        Returns: Latency-compensated time-to-solve in seconds.
        Raises: CheatingAnomalyException if timestamps indicate tampering or stale replay.
        """
        # Ensure RTT is non-negative
        rtt_ms = max(0.0, rtt_ms)
        one_way_transit_latency_ms = rtt_ms / 2.0

        # Anti-Cheating Invariant 1: Client clock cannot be in the future beyond allowable jitter
        if client_timestamp_ms > (server_now_ms + cls.MAX_ALLOWABLE_JITTER_MS):
            raise CheatingAnomalyException(
                f"Clock manipulation anomaly detected: client timestamp {client_timestamp_ms}ms "
                f"exceeds server timestamp {server_now_ms}ms by more than allowable jitter."
            )

        # Anti-Cheating Invariant 2: Stale / Replayed submissions beyond allowable transit window
        if (server_now_ms - client_timestamp_ms) > cls.MAX_SUBMISSION_TRANSIT_WINDOW_MS:
            raise CheatingAnomalyException(
                "Stale submission anomaly: request timestamp exceeds maximum allowable transit window."
            )

        # Calculate effective answer dispatch timestamp on student device
        effective_client_submission_ms = client_timestamp_ms - one_way_transit_latency_ms

        # Compensated elapsed time since question opened on server
        raw_elapsed_ms = effective_client_submission_ms - question_start_server_ms
        compensated_seconds = max(0.05, raw_elapsed_ms / 1000.0)

        return round(compensated_seconds, 3)

    # ---------------------------------------------------------------------------
    # 3. Anti-Cheating Time-Locked Cryptographic Hash Verification
    # ---------------------------------------------------------------------------

    @staticmethod
    def generate_time_locked_hash(
        secret_salt: str,
        tournament_id: str,
        question_id: str,
        participant_id: str,
        option_id: str,
        timestamp_ms: int,
        nonce: str,
    ) -> str:
        """
        Mints a SHA-256 HMAC cryptographic token binding the exact student answer,
        millisecond timestamp, and unique request nonce to prevent replay attacks.
        """
        payload = f"{tournament_id}:{question_id}:{participant_id}:{option_id}:{timestamp_ms}:{nonce}"
        return hmac.new(
            secret_salt.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    @classmethod
    def verify_time_locked_hash(
        cls,
        secret_salt: str,
        tournament_id: str,
        question_id: str,
        participant_id: str,
        option_id: str,
        timestamp_ms: int,
        nonce: str,
        provided_hash: str,
    ) -> bool:
        """
        Validates the submission token in constant time to eliminate timing side-channels.
        """
        expected_hash = cls.generate_time_locked_hash(
            secret_salt=secret_salt,
            tournament_id=tournament_id,
            question_id=question_id,
            participant_id=participant_id,
            option_id=option_id,
            timestamp_ms=timestamp_ms,
            nonce=nonce,
        )
        return hmac.compare_digest(expected_hash, provided_hash)

    # ---------------------------------------------------------------------------
    # 4. Instant Scholastic Medal Tier Calculation
    # ---------------------------------------------------------------------------

    @classmethod
    def calculate_medal_tiers(
        cls, participants: List[OlympiadParticipant]
    ) -> List[Dict[str, object]]:
        """
        Allocates prestige academic medal tiers based on competitive percentile ranks,
        mirroring the International Mathematical Olympiad (IMO) and National STEM benchmarks:
        - Top 8%: Gold Medal ("স্বর্ণপদক")
        - Next 17% (8% to 25%): Silver Medal ("রৌপ্যপদক")
        - Next 25% (25% to 50%): Bronze Medal ("ব্রোঞ্জপদক")
        - Next 25% (50% to 75%): Honorable Mention ("বিশেষ সম্মাননা")
        - Remaining: Certificate of Participation ("অংশগ্রহণ সনদ")

        Tie-breaking rule: Primary = Higher Score, Secondary = Lowest Latency-Compensated Time.
        """
        if not participants:
            return []

        # Sort: Primary by score descending, Secondary by total_time_ms ascending
        ranked = sorted(
            participants,
            key=lambda p: (-p.score, p.total_time_ms),
        )

        total_count = len(ranked)
        results: List[Dict[str, object]] = []

        for index, candidate in enumerate(ranked):
            rank = index + 1
            percentile = ((total_count - index) / total_count) * 100.0

            # Determine medal tier
            if rank <= math.ceil(total_count * 0.08):
                medal = MedalTier.GOLD
            elif rank <= math.ceil(total_count * 0.25):
                medal = MedalTier.SILVER
            elif rank <= math.ceil(total_count * 0.50):
                medal = MedalTier.BRONZE
            elif rank <= math.ceil(total_count * 0.75):
                medal = MedalTier.HONORABLE_MENTION
            else:
                medal = MedalTier.PARTICIPATION

            results.append({
                "rank": rank,
                "participant_id": candidate.id,
                "name": candidate.name,
                "institution": candidate.institution,
                "score": candidate.score,
                "total_time_ms": candidate.total_time_ms,
                "elo_rating": candidate.elo_rating,
                "percentile": round(percentile, 2),
                "medal_tier": medal.value,
                "medal_code": medal.name,
            })

        return results

    # ---------------------------------------------------------------------------
    # 5. Tournament Ladder Progression Engine
    # ---------------------------------------------------------------------------

    @classmethod
    def generate_bracket_matches(
        cls,
        participants: List[OlympiadParticipant],
        round_number: int = 1,
        round_name: str = "Round of 16",
    ) -> List[TournamentMatch]:
        """
        Generates bracket matches for a designated tournament stage from paired participants.
        """
        pairs = cls.pair_participants_by_elo(participants)
        matches: List[TournamentMatch] = []

        for idx, (p_a, p_b) in enumerate(pairs, start=1):
            matches.append(
                TournamentMatch(
                    match_id=f"match_r{round_number}_{idx}",
                    round_number=round_number,
                    round_name=round_name,
                    participant_a_id=p_a.id,
                    participant_b_id=p_b.id,
                    status="SCHEDULED",
                )
            )

        return matches

    @classmethod
    def resolve_match(
        cls,
        match: TournamentMatch,
        score_a: float,
        score_b: float,
        latency_a_ms: float,
        latency_b_ms: float,
    ) -> TournamentMatch:
        """
        Resolves a match outcome applying primary score and tie-breaking by lowest latency.
        """
        match.score_a = score_a
        match.score_b = score_b
        match.latency_a_ms = latency_a_ms
        match.latency_b_ms = latency_b_ms
        match.status = "COMPLETED"

        if score_a > score_b:
            match.winner_id = match.participant_a_id
        elif score_b > score_a:
            match.winner_id = match.participant_b_id
        else:
            # Tie-break: lowest latency wins
            if latency_a_ms <= latency_b_ms:
                match.winner_id = match.participant_a_id
            else:
                match.winner_id = match.participant_b_id

        return match

    @classmethod
    def advance_to_next_round(
        cls,
        completed_matches: List[TournamentMatch],
        all_participants: Dict[str, OlympiadParticipant],
        next_round_number: int,
        next_round_name: str,
    ) -> List[TournamentMatch]:
        """
        Filters winners from completed matches and generates pairings for the subsequent round.
        """
        winners: List[OlympiadParticipant] = []
        for m in completed_matches:
            if m.winner_id and m.winner_id in all_participants:
                winners.append(all_participants[m.winner_id])

        return cls.generate_bracket_matches(
            participants=winners,
            round_number=next_round_number,
            round_name=next_round_name,
        )
