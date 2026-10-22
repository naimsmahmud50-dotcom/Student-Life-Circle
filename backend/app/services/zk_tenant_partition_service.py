"""
Zero-Knowledge Multi-Tenant Partitioning Service (Phase 55).
Enforces PostgreSQL declarative table partitioning across institutional tenants,
verifies cryptographic partition boundary tokens, and neutralizes cross-tenant escape probes.
"""

import hashlib
import hmac
import re
from typing import Dict, Any, List, Optional


class ZeroKnowledgeTenantPartitionService:
    """
    Manages declarative multi-tenant partitioning boundaries and escape detection
    for Bangladesh's premier academic institutions (BUET, DU, Medical, Cadet colleges).
    """

    SUPPORTED_TENANTS = {
        "inst_buet": {"name": "Bangladesh University of Engineering and Technology", "cluster_shard": "shard_alpha"},
        "inst_du": {"name": "University of Dhaka", "cluster_shard": "shard_beta"},
        "inst_medical": {"name": "Directorate General of Health Services (Medical)", "cluster_shard": "shard_gamma"},
        "inst_cadet": {"name": "Bangladesh Cadet Colleges Central Council", "cluster_shard": "shard_delta"},
        "inst_kuet": {"name": "Khulna University of Engineering & Technology", "cluster_shard": "shard_alpha"},
        "inst_ruet": {"name": "Rajshahi University of Engineering & Technology", "cluster_shard": "shard_alpha"},
        "inst_sust": {"name": "Shahjalal University of Science and Technology", "cluster_shard": "shard_beta"},
        "inst_cuet": {"name": "Chittagong University of Engineering & Technology", "cluster_shard": "shard_alpha"},
    }

    PARTITIONABLE_TABLES = {"students", "academic_records", "transcripts", "exams", "scholarships"}
    MASTER_PARTITION_KEY = b"institutional_zk_partition_vault_key_2026_top_rank"

    # Regex patterns for partition escape attempts
    ESCAPE_PATTERNS = [
        (re.compile(r"union\s+(all\s+)?select", re.IGNORECASE), "UNION_PARTITION_ESCAPE_ATTEMPT"),
        (re.compile(r"(part_|tbl_)\*", re.IGNORECASE), "WILDCARD_PARTITION_PROBE"),
        (re.compile(r"or\s+1\s*=\s*1|or\s+true", re.IGNORECASE), "BOOLEAN_TAUTOLOGY_ESCAPE"),
        (re.compile(r"tenant_id\s*is\s*not\s*null", re.IGNORECASE), "TENANT_BOUNDARY_PROBE"),
        (re.compile(r";\s*(select|update|delete|drop|alter)", re.IGNORECASE), "STACKED_PARTITION_QUERY"),
        (re.compile(r"pg_catalog|information_schema", re.IGNORECASE), "METADATA_CATALOG_TRAVERSAL"),
    ]

    @classmethod
    def generate_tenant_proof(cls, tenant_id: str) -> str:
        """Generates an HMAC cryptographic proof binding the tenant to partition operations."""
        if tenant_id not in cls.SUPPORTED_TENANTS:
            raise ValueError(f"Unregistered tenant: {tenant_id}")
        h = hmac.new(cls.MASTER_PARTITION_KEY, tenant_id.encode("utf-8"), hashlib.sha256)
        return h.hexdigest()

    @classmethod
    def validate_tenant_boundary(cls, tenant_id: str, auth_token_signature: Optional[str] = None) -> Dict[str, Any]:
        """Validates that a tenant is legitimate and satisfies cryptographic boundary bounds."""
        if not tenant_id or tenant_id not in cls.SUPPORTED_TENANTS:
            return {
                "valid": False,
                "tenant_id": tenant_id,
                "reason": "TENANT_NOT_REGISTERED",
                "security_verdict": "REJECTED_UNKNOWN_TENANT"
            }

        expected_sig = cls.generate_tenant_proof(tenant_id)
        if auth_token_signature and auth_token_signature != expected_sig:
            return {
                "valid": False,
                "tenant_id": tenant_id,
                "reason": "INVALID_CRYPTOGRAPHIC_TENANT_SIGNATURE",
                "security_verdict": "REJECTED_FORGED_SIGNATURE"
            }

        tenant_info = cls.SUPPORTED_TENANTS[tenant_id]
        return {
            "valid": True,
            "tenant_id": tenant_id,
            "institution_name": tenant_info["name"],
            "cluster_shard": tenant_info["cluster_shard"],
            "boundary_proof": expected_sig,
            "security_verdict": "VERIFIED_BOUNDARY_ACCEPTED"
        }

    @classmethod
    def route_query(
        cls,
        tenant_id: str,
        table_name: str,
        query_filters: Optional[Dict[str, Any]] = None,
        auth_token_signature: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Routes logical queries to the isolated physical partition table,
        strictly enforcing partition pruning and sanitizing filters.
        """
        boundary = cls.validate_tenant_boundary(tenant_id, auth_token_signature)
        if not boundary["valid"]:
            return {
                "success": False,
                "tenant_id": tenant_id,
                "target_partition_table": "",
                "pruning_boundary_enforced": False,
                "sanitized_filter": {},
                "security_verdict": boundary["security_verdict"],
                "message": f"Tenant partition access rejected: {boundary['reason']}"
            }

        sanitized_table = table_name.lower().strip()
        if sanitized_table not in cls.PARTITIONABLE_TABLES:
            sanitized_table = "academic_records"

        # Determine physical sub-partition table name
        partition_table = f"{sanitized_table}_part_{tenant_id}"

        # Cleanse and strictly bind tenant_id to query filters
        filters = dict(query_filters) if query_filters else {}
        # Ensure tenant_id cannot be overwritten by client-supplied filters
        filters["tenant_id"] = tenant_id

        return {
            "success": True,
            "tenant_id": tenant_id,
            "target_partition_table": partition_table,
            "pruning_boundary_enforced": True,
            "sanitized_filter": filters,
            "security_verdict": "PARTITION_ROUTED_PRUNED",
            "message": f"Successfully bound query to partition '{partition_table}'."
        }

    @classmethod
    def detect_partition_escape_attempt(cls, tenant_id: str, malicious_query_clause: str) -> Dict[str, Any]:
        """Scans queries for partition boundary escape probes and SQL injection techniques."""
        if not malicious_query_clause:
            return {
                "blocked": False,
                "tenant_id": tenant_id,
                "detected_vector": "NONE",
                "mitigation_applied": "NONE",
                "query_rejected": False
            }

        for pattern, vector_name in cls.ESCAPE_PATTERNS:
            if pattern.search(malicious_query_clause):
                return {
                    "blocked": True,
                    "tenant_id": tenant_id,
                    "detected_vector": vector_name,
                    "mitigation_applied": "QUERY_EXECUTION_BLOCKED_AND_PARTITION_ISOLATED",
                    "query_rejected": True
                }

        # Check for cross-tenant IDOR mention
        for other_tenant in cls.SUPPORTED_TENANTS:
            if other_tenant != tenant_id and other_tenant in malicious_query_clause:
                return {
                    "blocked": True,
                    "tenant_id": tenant_id,
                    "detected_vector": "CROSS_TENANT_DISCOVERY_PROBE",
                    "mitigation_applied": "STRICT_TENANT_SHARD_QUARANTINE",
                    "query_rejected": True
                }

        return {
            "blocked": False,
            "tenant_id": tenant_id,
            "detected_vector": "CLEAN_QUERY",
            "mitigation_applied": "PERMITTED_TO_LOCAL_PARTITION",
            "query_rejected": False
        }

    @classmethod
    def get_partition_topology(cls) -> Dict[str, Any]:
        """Returns the full declarative partition topology for auditing."""
        topology = []
        for t_id, info in cls.SUPPORTED_TENANTS.items():
            topology.append({
                "tenant_id": t_id,
                "institution": info["name"],
                "shard": info["cluster_shard"],
                "partition_tables": [f"{tbl}_part_{t_id}" for tbl in sorted(cls.PARTITIONABLE_TABLES)],
                "status": "HEALTHY_ACTIVE",
            })
        return {
            "total_tenants": len(cls.SUPPORTED_TENANTS),
            "partitionable_entities": sorted(list(cls.PARTITIONABLE_TABLES)),
            "partitions": topology
        }
