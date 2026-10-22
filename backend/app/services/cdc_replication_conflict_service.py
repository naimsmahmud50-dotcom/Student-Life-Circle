"""
Cross-Region CDC Replication & Conflict Resolution Service (Phase 55).
Decodes logical WAL CDC events across regional clusters (Dhaka Primary,
Chittagong DR Node, Singapore Edge), applies CRDT vector clock and LWW
conflict-free reconciliation, and monitors replication slot lag SLAs.
"""

import time
from typing import Dict, Any, List, Optional, Tuple


class CdcReplicationConflictService:
    """
    Manages multi-datacenter bi-directional replication, logical decoding,
    conflict-free resolution (CRDT/LWW), and replication slot health.
    """

    SUPPORTED_REGIONS = {"region_dhaka", "region_chittagong", "region_singapore"}
    MAX_ALLOWABLE_LAG_SECONDS = 2.0  # Real-time multi-region SLA threshold
    MAX_ALLOWABLE_LAG_BYTES = 64 * 1024 * 1024  # 64 MB

    def __init__(self):
        self._dlq_quarantine: List[Dict[str, Any]] = []
        self._replication_events: List[Dict[str, Any]] = []

    @classmethod
    def _parse_lsn_to_int(cls, lsn: str) -> int:
        """Converts PostgreSQL LSN string (e.g. '16/3400A120') to a 64-bit integer."""
        try:
            parts = lsn.split("/")
            if len(parts) == 2:
                hi = int(parts[0], 16)
                lo = int(parts[1], 16)
                return (hi << 32) + lo
        except Exception:
            pass
        return 0

    @classmethod
    def compare_vector_clocks(cls, clock_a: Dict[str, int], clock_b: Dict[str, int]) -> str:
        """
        Compares two vector clocks.
        Returns:
            'A_GREATER' if clock_a strictly dominates clock_b
            'B_GREATER' if clock_b strictly dominates clock_a
            'EQUAL' if both are identical
            'CONCURRENT' if neither dominates (true concurrency conflict)
        """
        all_keys = set(clock_a.keys()).union(set(clock_b.keys()))
        a_has_greater = False
        b_has_greater = False

        for k in all_keys:
            val_a = clock_a.get(k, 0)
            val_b = clock_b.get(k, 0)
            if val_a > val_b:
                a_has_greater = True
            elif val_b > val_a:
                b_has_greater = True

        if a_has_greater and not b_has_greater:
            return "A_GREATER"
        elif b_has_greater and not a_has_greater:
            return "B_GREATER"
        elif not a_has_greater and not b_has_greater:
            return "EQUAL"
        else:
            return "CONCURRENT"

    def decode_and_process_event(
        self,
        event_id: str,
        region_origin: str,
        table_name: str,
        operation: str,
        row_data: Dict[str, Any],
        vector_clock: Dict[str, int],
        commit_lsn: str,
        timestamp: Optional[float] = None
    ) -> Dict[str, Any]:
        """Decodes and validates an incoming CDC replication event."""
        if region_origin not in self.SUPPORTED_REGIONS:
            self.quarantine_dead_letter(event_id, "UNRECOGNIZED_SOURCE_REGION", {"region": region_origin})
            return {
                "event_id": event_id,
                "status": "QUARANTINED_DLQ",
                "applied_operation": "NONE",
                "conflict_detected": True,
                "resolution_strategy": "DEAD_LETTER_ISOLATION",
                "winning_region": "NONE",
                "updated_vector_clock": vector_clock
            }

        ts = timestamp or time.time()
        event_record = {
            "event_id": event_id,
            "region_origin": region_origin,
            "table_name": table_name,
            "operation": operation.upper(),
            "row_data": row_data,
            "vector_clock": dict(vector_clock),
            "commit_lsn": commit_lsn,
            "timestamp": ts,
            "processed_at": time.time()
        }
        self._replication_events.append(event_record)

        return {
            "event_id": event_id,
            "status": "APPLIED_REPLICATED",
            "applied_operation": operation.upper(),
            "conflict_detected": False,
            "resolution_strategy": "DIRECT_REPLICATION",
            "winning_region": region_origin,
            "updated_vector_clock": vector_clock
        }

    def resolve_replication_conflict(
        self,
        local_record: Dict[str, Any],
        incoming_event: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resolves conflicts between local database state and incoming replication event.
        Uses Vector Clocks + Last-Write-Wins (LWW) with deterministic region ordering.
        """
        local_clock = local_record.get("vector_clock", {})
        incoming_clock = incoming_event.get("vector_clock", {})

        clock_cmp = self.compare_vector_clocks(local_clock, incoming_clock)

        # Case 1: Incoming strictly dominates
        if clock_cmp == "B_GREATER":
            merged_clock = self._merge_clocks(local_clock, incoming_clock)
            return {
                "conflict_detected": False,
                "winner": "INCOMING",
                "resolution_strategy": "VECTOR_CLOCK_DOMINANCE",
                "verdict": "APPLY_INCOMING_UPDATE",
                "merged_vector_clock": merged_clock,
                "active_data": incoming_event.get("row_data")
            }

        # Case 2: Local strictly dominates (incoming is a stale retry or delayed message)
        if clock_cmp == "A_GREATER" or clock_cmp == "EQUAL":
            return {
                "conflict_detected": True,
                "winner": "LOCAL",
                "resolution_strategy": "LOCAL_CLOCK_DOMINANCE_STALE_EVENT",
                "verdict": "IGNORE_INCOMING_EVENT",
                "merged_vector_clock": local_clock,
                "active_data": local_record.get("row_data")
            }

        # Case 3: Concurrent updates! Apply CRDT Last-Write-Wins (LWW)
        local_ts = local_record.get("timestamp", 0.0)
        incoming_ts = incoming_event.get("timestamp", 0.0)

        if incoming_ts > local_ts:
            winner = "INCOMING"
        elif incoming_ts < local_ts:
            winner = "LOCAL"
        else:
            # Deterministic tie-breaker: order by region name
            local_region = local_record.get("region_origin", "")
            incoming_region = incoming_event.get("region_origin", "")
            winner = "INCOMING" if incoming_region > local_region else "LOCAL"

        merged_clock = self._merge_clocks(local_clock, incoming_clock)
        active_data = incoming_event.get("row_data") if winner == "INCOMING" else local_record.get("row_data")

        return {
            "conflict_detected": True,
            "winner": winner,
            "resolution_strategy": "CRDT_LAST_WRITE_WINS_LWW",
            "verdict": f"RESOLVED_VIA_LWW_{winner}_WINS",
            "merged_vector_clock": merged_clock,
            "active_data": active_data
        }

    @staticmethod
    def _merge_clocks(clock_a: Dict[str, int], clock_b: Dict[str, int]) -> Dict[str, int]:
        """Returns the point-wise maximum of two vector clocks."""
        all_keys = set(clock_a.keys()).union(set(clock_b.keys()))
        merged = {}
        for k in all_keys:
            merged[k] = max(clock_a.get(k, 0), clock_b.get(k, 0))
        return merged

    def quarantine_dead_letter(self, event_id: str, reason: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Places an unresolvable event into the dead-letter queue for operator inspection."""
        entry = {
            "event_id": event_id,
            "reason": reason,
            "payload": payload,
            "quarantined_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self._dlq_quarantine.append(entry)
        return entry

    def get_replication_slot_lag(
        self,
        slot_name: str,
        source_region: str,
        target_region: str,
        current_lsn: str,
        confirmed_flush_lsn: str,
        last_flush_timestamp: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Evaluates replication slot byte lag and duration lag against institutional SLA.
        """
        curr_int = self._parse_lsn_to_int(current_lsn)
        flush_int = self._parse_lsn_to_int(confirmed_flush_lsn)
        byte_lag = max(0, curr_int - flush_int)

        now = time.time()
        flush_time = last_flush_timestamp or (now - 0.25)
        time_lag_seconds = max(0.0, round(now - flush_time, 3))

        sla_pass = (time_lag_seconds <= self.MAX_ALLOWABLE_LAG_SECONDS) and (byte_lag <= self.MAX_ALLOWABLE_LAG_BYTES)

        return {
            "slot_name": slot_name,
            "source_region": source_region,
            "target_region": target_region,
            "current_lsn": current_lsn,
            "confirmed_flush_lsn": confirmed_flush_lsn,
            "byte_lag": byte_lag,
            "byte_lag_mb": round(byte_lag / (1024 * 1024), 2),
            "time_lag_seconds": time_lag_seconds,
            "sla_threshold_seconds": self.MAX_ALLOWABLE_LAG_SECONDS,
            "sla_status": "SLA_COMPLIANT_ACTIVE" if sla_pass else "LAG_EXCEEDED_WARNING",
            "dlq_quarantine_count": len(self._dlq_quarantine)
        }
