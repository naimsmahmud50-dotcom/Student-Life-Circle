import hashlib
import time
from typing import Any, Dict, List, Optional


class WalArchiveIntegrityService:
    """
    PostgreSQL Write-Ahead Log (WAL) Archive Continuity & Replication Lag Engine.
    Ensures continuous physical replication, protects hot-standby replicas against silent gaps,
    and enforces institutional RPO recovery bounds (< 60s archive lag).
    """

    WAL_SEGMENT_SIZE_BYTES = 16 * 1024 * 1024  # 16 MB PostgreSQL standard

    def __init__(self):
        self._segments: List[Dict[str, Any]] = []
        self._seed_initial_wal_chain()

    def _seed_initial_wal_chain(self):
        """Seeds initial sequential WAL segments (Timeline 1, Segments 1 to 4)."""
        now = int(time.time()) - 180
        for seg_num in range(1, 5):
            seg_name = self.format_segment_name(timeline_id=1, log_id=0, seg_id=seg_num)
            checksum = hashlib.sha256(f"wal_{seg_name}".encode()).hexdigest()
            self.register_wal_segment(
                segment_name=seg_name,
                timeline_id=1,
                segment_number=seg_num,
                checksum=checksum,
                timestamp=now + (seg_num * 30),
            )

    @staticmethod
    def format_segment_name(timeline_id: int, log_id: int, seg_id: int) -> str:
        """Formats 24-character PostgreSQL WAL filename: 8 hex chars timeline + 8 log + 8 seg."""
        t_hex = hex(timeline_id)[2:].upper().zfill(8)
        l_hex = hex(log_id)[2:].upper().zfill(8)
        s_hex = hex(seg_id)[2:].upper().zfill(8)
        return f"{t_hex}{l_hex}{s_hex}"

    def register_wal_segment(
        self,
        segment_name: str,
        timeline_id: int,
        segment_number: int,
        checksum: str,
        timestamp: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Registers an incoming 16MB WAL segment into the continuous archive catalog.
        """
        now = timestamp if timestamp is not None else int(time.time())
        # Validate 24-character hexadecimal format
        if len(segment_name) != 24 or not all(c in "0123456789ABCDEFabcdef" for c in segment_name):
            return {
                "accepted": False,
                "error": "Invalid WAL segment filename: must be exactly 24 hexadecimal characters.",
                "segment_name": segment_name,
            }

        seg_entry = {
            "segment_name": segment_name,
            "timeline_id": timeline_id,
            "segment_number": segment_number,
            "size_bytes": self.WAL_SEGMENT_SIZE_BYTES,
            "checksum": checksum,
            "archived_at": now,
        }
        self._segments.append(seg_entry)
        # Sort by timeline then segment number
        self._segments.sort(key=lambda s: (s["timeline_id"], s["segment_number"]))

        return {
            "accepted": True,
            "segment_name": segment_name,
            "timeline_id": timeline_id,
            "segment_number": segment_number,
            "checksum": checksum,
            "archived_at": now,
        }

    def verify_wal_chain_continuity(self) -> Dict[str, Any]:
        """
        Scans all archived WAL segments to verify gapless continuity ($S_{i+1} = S_i + 1$).
        Detects missing logs that would cause replica sync failures or PITR aborts.
        """
        if not self._segments:
            return {
                "is_continuous": True,
                "total_segments": 0,
                "missing_segments_count": 0,
                "missing_segments": [],
                "status": "EMPTY_ARCHIVE",
            }

        missing_segments: List[str] = []
        timelines_analyzed = set()

        # Group by timeline
        by_timeline: Dict[int, List[Dict[str, Any]]] = {}
        for s in self._segments:
            tid = s["timeline_id"]
            timelines_analyzed.add(tid)
            by_timeline.setdefault(tid, []).append(s)

        for tid, segs in by_timeline.items():
            for i in range(len(segs) - 1):
                curr_num = segs[i]["segment_number"]
                next_num = segs[i + 1]["segment_number"]
                if next_num != curr_num + 1:
                    # Gap detected
                    for missing in range(curr_num + 1, next_num):
                        missing_name = self.format_segment_name(timeline_id=tid, log_id=0, seg_id=missing)
                        missing_segments.append(missing_name)

        is_continuous = len(missing_segments) == 0

        return {
            "is_continuous": is_continuous,
            "total_segments": len(self._segments),
            "timelines_count": len(timelines_analyzed),
            "missing_segments_count": len(missing_segments),
            "missing_segments": missing_segments,
            "latest_segment": self._segments[-1]["segment_name"] if self._segments else None,
            "status": "ARCHIVE_CHAIN_PRISTINE" if is_continuous else "ARCHIVE_CHAIN_BROKEN_GAPS_DETECTED",
        }

    def evaluate_archive_lag_and_sla(self, max_lag_seconds: int = 60) -> Dict[str, Any]:
        """
        Calculates time gap between current epoch and the latest archived segment timestamp.
        Verifies adherence to institutional RPO disaster SLA (< 60 seconds).
        """
        if not self._segments:
            return {
                "current_lag_seconds": 9999,
                "sla_seconds": max_lag_seconds,
                "sla_met": False,
                "throughput_mb_sec": 0.0,
                "status": "NO_WAL_ARCHIVED",
            }

        now = int(time.time())
        latest = self._segments[-1]
        lag_seconds = max(0, now - latest["archived_at"])
        sla_met = lag_seconds <= max_lag_seconds

        # Compute throughput over available span
        span = max(1, self._segments[-1]["archived_at"] - self._segments[0]["archived_at"])
        total_mb = (len(self._segments) * 16)
        throughput = round(total_mb / span, 2)

        return {
            "current_lag_seconds": lag_seconds,
            "sla_seconds": max_lag_seconds,
            "sla_met": sla_met,
            "latest_segment": latest["segment_name"],
            "total_archived_mb": total_mb,
            "throughput_mb_sec": throughput,
            "status": "OPTIMAL_ARCHIVE_SLA" if sla_met else "ARCHIVE_LAG_EXCEEDED",
        }
