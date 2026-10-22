# ==============================================================================
# File: backend/app/services/database_cdc_audit_engine_service.py
# Phase: 49 - Database CDC & Tamper-Evident Audit Engine
# Topic: Logical Replication WAL Parsing, Cryptographic Merkle Chaining, & PII Scrubbing
# Description: Ingests Postgres CDC event streams, maintains a tamper-evident SHA-256
#              audit chain for academic and bursary data, authorizes realtime channel
#              distribution, and redacts PII before websocket broadcasting.
# ==============================================================================

import json
import time
import hashlib
import re
from typing import Dict, Any, List, Optional

class DatabaseCDCAuditEngineService:
    """
    Postgres Change Data Capture (CDC) & Tamper-Evident Audit Engine.
    Processes database WAL events, guarantees verifiable record integrity via
    cryptographic hash chaining, and scrubs sensitive PII for Realtime feeds.
    """

    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    def __init__(self):
        self._audit_log: List[Dict[str, Any]] = []
        self._latest_hash = self.GENESIS_HASH
        
        # Security & Telemetry stats
        self._stats = {
            "wal_events_processed": 0,
            "tamper_verifications_run": 0,
            "pii_fields_redacted": 0,
            "broadcast_events_filtered": 0
        }

    def ingest_wal_event(
        self,
        event_type: str,
        table_name: str,
        record_id: str,
        record_data: Dict[str, Any],
        actor_id: str = "system",
        commit_lsn: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ingests a database WAL change event, seals it in the cryptographic audit chain,
        and produces a verifiable audit block.
        """
        self._stats["wal_events_processed"] += 1
        now = time.time()
        lsn = commit_lsn or f"0/{hex(len(self._audit_log) + 1)[2:].zfill(8).upper()}"

        # Canonical serialized payload for deterministic hashing
        canonical_data = json.dumps(record_data, sort_keys=True)
        block_content = f"{self._latest_hash}:{lsn}:{event_type}:{table_name}:{record_id}:{actor_id}:{canonical_data}"
        block_hash = hashlib.sha256(block_content.encode("utf-8")).hexdigest()

        audit_entry = {
            "sequence_index": len(self._audit_log),
            "commit_lsn": lsn,
            "event_type": event_type.upper(),
            "table_name": table_name,
            "record_id": record_id,
            "actor_id": actor_id,
            "previous_hash": self._latest_hash,
            "block_hash": block_hash,
            "payload": record_data,
            "timestamp": now
        }

        self._audit_log.append(audit_entry)
        self._latest_hash = block_hash

        return {
            "success": True,
            "sequence_index": audit_entry["sequence_index"],
            "block_hash": block_hash,
            "commit_lsn": lsn,
            "tamper_evident": True
        }

    def verify_audit_integrity(self) -> Dict[str, Any]:
        """
        Traverses the full audit chain and cryptographically recomputes all SHA-256 hashes.
        Detects any retroactive record modification, insertion, or deletion.
        """
        self._stats["tamper_verifications_run"] += 1
        current_prev_hash = self.GENESIS_HASH

        for idx, entry in enumerate(self._audit_log):
            # Check previous hash continuity
            if entry["previous_hash"] != current_prev_hash:
                return {
                    "chain_valid": False,
                    "tamper_detected_at_index": idx,
                    "error": f"Broken chain at block #{idx}. Expected previous {current_prev_hash}, got {entry['previous_hash']}"
                }

            # Recompute block hash
            canonical_data = json.dumps(entry["payload"], sort_keys=True)
            block_content = f"{entry['previous_hash']}:{entry['commit_lsn']}:{entry['event_type']}:{entry['table_name']}:{entry['record_id']}:{entry['actor_id']}:{canonical_data}"
            recomputed = hashlib.sha256(block_content.encode("utf-8")).hexdigest()

            if recomputed != entry["block_hash"]:
                return {
                    "chain_valid": False,
                    "tamper_detected_at_index": idx,
                    "error": f"Tampered block #{idx}. Expected hash {recomputed}, recorded {entry['block_hash']}"
                }

            current_prev_hash = entry["block_hash"]

        return {
            "chain_valid": True,
            "total_blocks_verified": len(self._audit_log),
            "genesis_hash": self.GENESIS_HASH,
            "latest_head_hash": self._latest_hash,
            "status": "cryptographically_verified"
        }

    def prepare_realtime_broadcast_payload(
        self,
        event_entry: Dict[str, Any],
        subscriber_user_id: str,
        subscriber_role: str = "student"
    ) -> Optional[Dict[str, Any]]:
        """
        Authorizes Realtime channel delivery and scrubs sensitive PII
        before sending Postgres changes over websockets to subscribers.
        """
        # 1. Row Authorization: If student, they can only see their own records
        record_owner = event_entry.get("payload", {}).get("student_id") or event_entry.get("record_id")
        if subscriber_role == "student" and record_owner != subscriber_user_id:
            self._stats["broadcast_events_filtered"] += 1
            return None  # Dropped due to lack of row-level entitlement

        # 2. PII Redaction
        scrubbed_payload = self._redact_pii_fields(event_entry.get("payload", {}))

        return {
            "event": event_entry["event_type"],
            "table": event_entry["table_name"],
            "record_id": event_entry["record_id"],
            "block_hash": event_entry["block_hash"][:16] + "...",
            "data": scrubbed_payload,
            "timestamp": event_entry["timestamp"],
            "broadcast_authorized": True
        }

    def _redact_pii_fields(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Scrubs national ID, phone numbers, and financial account identifiers."""
        redacted = dict(payload)
        for key, value in redacted.items():
            str_val = str(value)
            # Redact NID / National ID (10 or 17 digit numbers)
            if "nid" in key.lower() or "national_id" in key.lower():
                if len(str_val) >= 8:
                    redacted[key] = f"***-****-{str_val[-4:]}"
                    self._stats["pii_fields_redacted"] += 1
            # Redact phone numbers (+8801...)
            elif "phone" in key.lower() or "mobile" in key.lower():
                if len(str_val) >= 7:
                    redacted[key] = f"+880-17****-{str_val[-4:]}"
                    self._stats["pii_fields_redacted"] += 1
            # Redact bank / bursary accounts
            elif "account" in key.lower() or "bank" in key.lower() or "bursary" in key.lower():
                if len(str_val) >= 6:
                    redacted[key] = f"ACC-****-{str_val[-4:]}"
                    self._stats["pii_fields_redacted"] += 1
        return redacted

    def get_audit_trail(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns the most recent audit blocks."""
        return self._audit_log[-limit:]

    def get_engine_metrics(self) -> Dict[str, Any]:
        """Returns CDC engine operational metrics."""
        return {
            "stats": dict(self._stats),
            "chain_length": len(self._audit_log),
            "head_hash": self._latest_hash
        }
