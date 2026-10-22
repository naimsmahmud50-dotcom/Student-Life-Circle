"""
================================================================================
MODULE: Core Security & Compliance Engine (অডিট লেজার ও ক্রিপ্টোগ্রাফিক সুরক্ষা)
TOPIC: Tamper-Evident SHA-256 Chained Audit Ledger & Event Dispatcher
FILE: backend/app/core/audit_ledger.py
PURPOSE: Implements an immutable, append-only, cryptographically chained audit
         ledger that records high-stakes operations (question quarantining,
         score reconciliations, guardian consent grants, and credential issuance).
         Provides instant mathematical verification to detect any unauthorized
         database tampering or record alterations.
AUDIENCE: Platform Auditors, Security Engineers, Compliance Officers, Developers.
STANDARDS: OWASP ASVS Level 2 (V7 Audit Architecture), ISO/IEC 27001, FIPS 180-4.
================================================================================
"""

import copy
import hashlib
import json
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


def _canonical_json(data: Any) -> str:
    """Produces deterministic, canonical JSON for reliable SHA-256 hashing."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


class AuditBlock:
    """Represents a single immutable cryptographic block in the audit chain."""

    def __init__(
        self,
        block_index: int,
        timestamp: str,
        event_type: str,
        actor_id: str,
        actor_role: str,
        payload: Dict[str, Any],
        prev_hash: str,
        block_hash: Optional[str] = None,
    ):
        self.block_index = block_index
        self.timestamp = timestamp
        self.event_type = event_type
        self.actor_id = actor_id
        self.actor_role = actor_role
        self.payload = copy.deepcopy(payload)
        self.prev_hash = prev_hash
        self.block_hash = block_hash or self.compute_hash()

    def compute_hash(self) -> str:
        """Computes the SHA-256 hash across all block fields including previous hash."""
        serialized_payload = _canonical_json(self.payload)
        hash_preimage = (
            f"{self.block_index}|"
            f"{self.timestamp}|"
            f"{self.event_type}|"
            f"{self.actor_id}|"
            f"{self.actor_role}|"
            f"{serialized_payload}|"
            f"{self.prev_hash}"
        )
        return hashlib.sha256(hash_preimage.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Serializes block to a dictionary."""
        return {
            "block_index": self.block_index,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "actor_id": self.actor_id,
            "actor_role": self.actor_role,
            "payload": copy.deepcopy(self.payload),
            "prev_hash": self.prev_hash,
            "block_hash": self.block_hash,
        }


class AuditLedger:
    """Thread-safe, append-only cryptographic audit ledger."""

    GENESIS_PREV_HASH = "0" * 64

    def __init__(self) -> None:
        self._blocks: List[AuditBlock] = []
        self._lock = threading.Lock()
        self._initialize_genesis_block()

    def _initialize_genesis_block(self) -> None:
        """Initializes the genesis anchor block if ledger is empty."""
        with self._lock:
            if not self._blocks:
                genesis = AuditBlock(
                    block_index=0,
                    timestamp="2026-01-01T00:00:00Z",
                    event_type="LEDGER_GENESIS",
                    actor_id="SYSTEM",
                    actor_role="SYSTEM_CORE",
                    payload={"description": "Platform Cryptographic Audit Ledger Initialized"},
                    prev_hash=self.GENESIS_PREV_HASH,
                )
                self._blocks.append(genesis)

    def record_event(
        self,
        event_type: str,
        actor_id: str,
        actor_role: str,
        payload: Dict[str, Any],
        timestamp: Optional[str] = None,
    ) -> AuditBlock:
        """Appends a new immutable event block chained to the previous block's hash."""
        if not event_type or not actor_id:
            raise ValueError("event_type and actor_id are strictly required for audit logging")

        iso_timestamp = timestamp or datetime.now(timezone.utc).isoformat()

        with self._lock:
            prev_block = self._blocks[-1]
            new_index = len(self._blocks)
            new_block = AuditBlock(
                block_index=new_index,
                timestamp=iso_timestamp,
                event_type=event_type,
                actor_id=actor_id,
                actor_role=actor_role,
                payload=payload,
                prev_hash=prev_block.block_hash,
            )
            self._blocks.append(new_block)
            return new_block

    def verify_integrity(self) -> Tuple[bool, Optional[int], str]:
        """
        Verifies the cryptographic integrity of the entire ledger chain.
        Returns: (is_valid, corrupted_block_index, verification_message)
        """
        with self._lock:
            if not self._blocks:
                return False, None, "Ledger is empty: missing genesis block"

            # 1. Verify Genesis
            genesis = self._blocks[0]
            if genesis.block_index != 0 or genesis.prev_hash != self.GENESIS_PREV_HASH:
                return False, 0, "Corrupted genesis block anchor"

            expected_genesis_hash = genesis.compute_hash()
            if genesis.block_hash != expected_genesis_hash:
                return False, 0, f"Genesis block hash mismatch (computed={expected_genesis_hash}, stored={genesis.block_hash})"

            # 2. Verify Chain Links
            for i in range(1, len(self._blocks)):
                current = self._blocks[i]
                previous = self._blocks[i - 1]

                # Verify sequential indexing
                if current.block_index != i:
                    return False, i, f"Block index discontinuity at index {i}"

                # Verify chain linkage
                if current.prev_hash != previous.block_hash:
                    return False, i, f"Broken chain link at block {i}: prev_hash does not match prior block hash"

                # Verify self hash
                recomputed_hash = current.compute_hash()
                if current.block_hash != recomputed_hash:
                    return False, i, f"Tampered block payload at block {i}: content hash mismatch"

            return True, None, f"All {len(self._blocks)} blocks verified cryptographically valid"

    def get_blocks(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves paginated blocks for administrative compliance view."""
        with self._lock:
            sliced = self._blocks[offset : offset + limit]
            return [b.to_dict() for b in sliced]

    def get_total_blocks(self) -> int:
        """Returns total blocks recorded in the ledger."""
        with self._lock:
            return len(self._blocks)

    def reset_for_testing(self) -> None:
        """Resets the ledger back to genesis for isolated test runs."""
        with self._lock:
            self._blocks.clear()
        self._initialize_genesis_block()


# Global Singleton Ledger Instance
audit_ledger = AuditLedger()
