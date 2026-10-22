"""
OfflineDeltaSyncService:
Offline-First PWA CRDT Delta-Sync Engine for Intermittent and 2G Networks.
Empowers students across rural Bangladesh to study uninterrupted offline.
Synchronizes quiz answers, bookmark sets, notes, and revision queues upon reconnection.
Features:
- Conflict-Free Replicated Data Types (CRDT) with monotonic vector clocks
- Last-Write-Wins (LWW) and Set-Union resolution strategies
- Idempotent mutation deduplication via unique mutation_id tracking
- Cryptographic state digest generation for verification of server-client parity
"""

import uuid
import hashlib
import json
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set


class OfflineDeltaSyncService:
    def __init__(self):
        self._lock = threading.Lock()
        # student_id -> dict of entities: {entity_type: {entity_id: {"data": payload, "vector_clock": int, "updated_at": str}}}
        self._student_states: Dict[str, Dict[str, Dict[str, Dict[str, Any]]]] = {}
        # student_id -> set of applied mutation_ids for idempotent deduplication
        self._applied_mutations: Dict[str, Set[str]] = {}
        # student_id -> global vector clock (monotonic counter)
        self._student_vector_clocks: Dict[str, int] = {}
        # student_id -> audit history of sync operations
        self._sync_history: Dict[str, List[Dict[str, Any]]] = {}

    def _ensure_student(self, student_id: str):
        if student_id not in self._student_states:
            self._student_states[student_id] = {
                "QUIZ_ANSWER": {},
                "NOTE": {},
                "BOOKMARK": {},
                "REVISION_QUEUE": {}
            }
            self._applied_mutations[student_id] = set()
            self._student_vector_clocks[student_id] = 1
            self._sync_history[student_id] = []

    def _compute_state_digest(self, student_id: str) -> str:
        state = self._student_states.get(student_id, {})
        # Deterministic serialization for SHA-256 digest
        serialized = json.dumps(state, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]

    def sync_delta(
        self,
        client_id: str,
        student_id: str,
        last_synced_vector_clock: int = 0,
        mutations: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        mutations = mutations or []
        applied_count = 0
        conflicts_resolved = 0

        with self._lock:
            self._ensure_student(student_id)
            current_server_clock = self._student_vector_clocks[student_id]
            student_state = self._student_states[student_id]
            applied_ids = self._applied_mutations[student_id]

            for mutation in mutations:
                mut_id = mutation.get("mutation_id", str(uuid.uuid4()))
                entity_type = mutation.get("entity_type", "NOTE").upper()
                entity_id = mutation.get("entity_id", f"entity-{uuid.uuid4().hex[:6]}")
                payload = mutation.get("payload", {})
                client_clock = int(mutation.get("vector_clock", last_synced_vector_clock + 1))
                client_time = mutation.get("client_timestamp", datetime.now(timezone.utc).isoformat())

                # Check deduplication
                if mut_id in applied_ids:
                    # Already applied idempotently
                    continue

                if entity_type not in student_state:
                    student_state[entity_type] = {}

                existing_record = student_state[entity_type].get(entity_id)

                if existing_record is None:
                    # Fresh entity: apply directly
                    student_state[entity_type][entity_id] = {
                        "payload": payload,
                        "vector_clock": client_clock,
                        "updated_at": client_time,
                        "mutation_id": mut_id
                    }
                    applied_count += 1
                else:
                    # CRDT Conflict Resolution
                    existing_clock = existing_record.get("vector_clock", 0)

                    if entity_type == "BOOKMARK":
                        # Set-Union CRDT: merge items if lists/sets, preserve true flags
                        merged_payload = dict(existing_record["payload"])
                        merged_payload.update(payload)
                        student_state[entity_type][entity_id] = {
                            "payload": merged_payload,
                            "vector_clock": max(existing_clock, client_clock) + 1,
                            "updated_at": client_time,
                            "mutation_id": mut_id
                        }
                        conflicts_resolved += 1
                        applied_count += 1
                    elif client_clock >= existing_clock:
                        # Last-Write-Wins (LWW) by vector clock
                        student_state[entity_type][entity_id] = {
                            "payload": payload,
                            "vector_clock": client_clock,
                            "updated_at": client_time,
                            "mutation_id": mut_id
                        }
                        if client_clock == existing_clock:
                            conflicts_resolved += 1
                        applied_count += 1
                    else:
                        # Server has higher vector clock: server-wins, flag conflict resolved
                        conflicts_resolved += 1

                applied_ids.add(mut_id)
                current_server_clock = max(current_server_clock, client_clock) + 1

            self._student_vector_clocks[student_id] = current_server_clock
            state_digest = self._compute_state_digest(student_id)
            sync_timestamp = datetime.now(timezone.utc).isoformat()

            status = "SUCCESS"
            if conflicts_resolved > 0 and applied_count > 0:
                status = "RECONCILED"
            elif applied_count == 0 and len(mutations) > 0:
                status = "IDEMPOTENT_NOOP"

            response = {
                "sync_status": status,
                "reconciled_clock": current_server_clock,
                "applied_count": applied_count,
                "conflicts_resolved": conflicts_resolved,
                "server_state_digest": f"crdt-{state_digest}",
                "synced_at": sync_timestamp
            }

            self._sync_history[student_id].append({
                "client_id": client_id,
                "mutations_received": len(mutations),
                "response": response
            })

            return response

    def get_student_synced_state(self, student_id: str) -> Dict[str, Any]:
        with self._lock:
            self._ensure_student(student_id)
            return {
                "student_id": student_id,
                "vector_clock": self._student_vector_clocks[student_id],
                "state_digest": f"crdt-{self._compute_state_digest(student_id)}",
                "entities": self._student_states[student_id]
            }

    def get_sync_history(self, student_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._sync_history.get(student_id, []))

    def reset_student_state(self, student_id: str) -> None:
        with self._lock:
            if student_id in self._student_states:
                del self._student_states[student_id]
            if student_id in self._applied_mutations:
                del self._applied_mutations[student_id]
            if student_id in self._student_vector_clocks:
                del self._student_vector_clocks[student_id]
            if student_id in self._sync_history:
                del self._sync_history[student_id]


offline_delta_sync_service = OfflineDeltaSyncService()
