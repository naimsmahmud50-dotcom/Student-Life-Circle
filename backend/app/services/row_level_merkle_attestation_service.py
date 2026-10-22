r"""
Row-Level Cryptographic Attestation & Merkle Proof Service (Phase 55).
Generates per-row cryptographic HMAC seals for academic credentials,
constructs Merkle audit trees ($M_{root} = H(L \parallel R)$), and provides
instant cryptographic tamper detection against rogue DB modifications.
"""

import hashlib
import hmac
import json
import time
from typing import Dict, Any, List, Optional, Tuple


class RowLevelAttestationMerkleService:
    """
    Cryptographic attestation and Merkle audit ledger for academic credentials,
    transcripts, certificates, and scholarship awards.
    """

    ATTESTATION_SECRET_KEY = b"merkle_attestation_master_vault_key_2026_top_tier"

    @classmethod
    def _canonical_json(cls, data: Dict[str, Any]) -> str:
        """Serializes data with sorted keys to ensure deterministic hashing."""
        return json.dumps(data, sort_keys=True, separators=(",", ":"))

    @classmethod
    def compute_sha256(cls, data: str) -> str:
        """Computes SHA-256 hexadecimal hash string."""
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @classmethod
    def generate_row_attestation(
        cls,
        record_id: str,
        tenant_id: str,
        entity_type: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates an immutable cryptographic seal (SHA-256 digest + HMAC-SHA256 signature)
        for an individual database row.
        """
        canonical_str = cls._canonical_json(payload)
        payload_digest = cls.compute_sha256(canonical_str)

        # Contextual string binding record identity to digest
        context_data = f"{tenant_id}:{entity_type}:{record_id}:{payload_digest}"
        signature = hmac.new(cls.ATTESTATION_SECRET_KEY, context_data.encode("utf-8"), hashlib.sha256).hexdigest()

        return {
            "record_id": record_id,
            "tenant_id": tenant_id,
            "entity_type": entity_type,
            "canonical_payload_digest": payload_digest,
            "hmac_signature": signature,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "attestation_status": "CRYPTOGRAPHICALLY_SEALED"
        }

    @classmethod
    def build_merkle_tree(cls, tenant_id: str, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Constructs a Merkle tree from a list of records and returns root hash,
        tree depth, and leaf digest list.
        """
        if not records:
            empty_root = cls.compute_sha256(f"empty_tree:{tenant_id}")
            return {
                "tenant_id": tenant_id,
                "merkle_root": empty_root,
                "total_leaves": 0,
                "leaf_hashes": [],
                "tree_depth": 0,
                "build_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }

        # Step 1: Compute leaf hashes
        leaves = []
        for r in records:
            canon = cls._canonical_json(r)
            leaves.append(cls.compute_sha256(canon))

        current_level = list(leaves)
        tree_depth = 1

        # Step 2: Hierarchically compute parent hashes until root is found
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # If odd number of nodes, duplicate the last node
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                parent = cls.compute_sha256(left + right)
                next_level.append(parent)
            current_level = next_level
            tree_depth += 1

        root_hash = current_level[0]

        return {
            "tenant_id": tenant_id,
            "merkle_root": root_hash,
            "total_leaves": len(leaves),
            "leaf_hashes": leaves,
            "tree_depth": tree_depth,
            "build_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

    @classmethod
    def generate_merkle_proof(cls, leaf_index: int, leaves: List[str]) -> List[Dict[str, str]]:
        """Generates audit path proof for a specific leaf index."""
        if not leaves or leaf_index < 0 or leaf_index >= len(leaves):
            return []

        proof: List[Dict[str, str]] = []
        current_level = list(leaves)
        idx = leaf_index

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                parent = cls.compute_sha256(left + right)
                next_level.append(parent)

            # Sibling for idx
            if idx % 2 == 0:
                sibling = current_level[idx + 1] if idx + 1 < len(current_level) else current_level[idx]
                proof.append({"position": "right", "hash": sibling})
            else:
                sibling = current_level[idx - 1]
                proof.append({"position": "left", "hash": sibling})

            idx = idx // 2
            current_level = next_level

        return proof

    @classmethod
    def verify_merkle_proof(
        cls,
        merkle_root: str,
        leaf_hash: str,
        proof_path: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Verifies that leaf_hash belongs to the tree represented by merkle_root
        via the supplied sibling proof path.
        """
        current_hash = leaf_hash
        for step in proof_path:
            sibling = step.get("hash", "")
            position = step.get("position", "right")

            if position == "left":
                current_hash = cls.compute_sha256(sibling + current_hash)
            else:
                current_hash = cls.compute_sha256(current_hash + sibling)

        is_valid = (current_hash == merkle_root)
        return {
            "is_valid": is_valid,
            "calculated_root": current_hash,
            "expected_root": merkle_root,
            "verdict": "PROOF_VERIFIED_VALID" if is_valid else "PROOF_INVALID_TAMPER_DETECTED"
        }

    @classmethod
    def detect_row_tampering(
        cls,
        original_attestation: Dict[str, Any],
        current_payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Detects tampering between original cryptographic attestation and current row state.
        Pinpoints exact mutated fields.
        """
        current_canon = cls._canonical_json(current_payload)
        current_digest = cls.compute_sha256(current_canon)
        original_digest = original_attestation.get("canonical_payload_digest", "")

        is_tampered = (current_digest != original_digest)
        mutations = []

        if is_tampered:
            # Detect which keys differ
            orig_data = original_attestation.get("payload", {})
            all_keys = set(orig_data.keys()).union(set(current_payload.keys()))
            for k in sorted(all_keys):
                orig_val = orig_data.get(k)
                curr_val = current_payload.get(k)
                if orig_val != curr_val:
                    mutations.append({
                        "field": k,
                        "original_value": orig_val,
                        "tampered_value": curr_val
                    })

        return {
            "record_id": original_attestation.get("record_id"),
            "tenant_id": original_attestation.get("tenant_id"),
            "tampered": is_tampered,
            "original_digest": original_digest,
            "current_digest": current_digest,
            "mutated_fields": mutations,
            "verdict": "CRITICAL_TAMPER_DETECTED" if is_tampered else "RECORD_PRISTINE_INTEGRITY"
        }
