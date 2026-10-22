"""
Index Optimizer Advisor Service (Phase 56).
Analyzes query selectivity ($S = |Q| / |T|$), recommends composite and partial indexes,
and eliminates redundant indexes to reduce write amplification.
"""

from typing import Dict, Any, List, Optional


class IndexOptimizerAdvisorService:
    """
    Automated query plan analyzer and index advisor for high-concurrency workloads
    (Live MCQ exams, real-time scoreboards, admission lookups).
    """

    @classmethod
    def calculate_selectivity(cls, table_row_count: int, estimated_matched_rows: int) -> float:
        """Calculates query selectivity ratio S = matched / total."""
        if table_row_count <= 0:
            return 1.0
        return round(min(1.0, max(0.0, estimated_matched_rows / table_row_count)), 4)

    @classmethod
    def recommend_index(
        cls,
        table_name: str,
        query_clause: str,
        filter_columns: List[str],
        sort_columns: Optional[List[str]] = None,
        table_row_count: int = 100000,
        estimated_matched_rows: int = 250
    ) -> Dict[str, Any]:
        """
        Recommends optimal index structure, ordering columns by the Leftmost Prefix Rule
        (equality columns first, then range/sort columns).
        """
        table = table_name.lower().strip()
        selectivity = cls.calculate_selectivity(table_row_count, estimated_matched_rows)

        sort_cols = sort_columns or []
        combined_cols: List[str] = []

        # Leftmost prefix: add filter columns first, avoiding duplicates
        for col in filter_columns:
            if col not in combined_cols:
                combined_cols.append(col)

        for col in sort_cols:
            if col not in combined_cols:
                combined_cols.append(col)

        if not combined_cols:
            combined_cols = ["id"]

        col_slug = "_".join(combined_cols[:3])
        index_name = f"idx_{table}_{col_slug}"

        # Detect partial index opportunity
        is_partial = False
        predicate = ""
        clause_lower = query_clause.lower()
        if "is_active = true" in clause_lower or "is_active is true" in clause_lower:
            is_partial = True
            predicate = "WHERE is_active = true"
            index_name += "_active"
        elif "status = 'published'" in clause_lower:
            is_partial = True
            predicate = "WHERE status = 'published'"
            index_name += "_published"

        where_part = f" {predicate}" if is_partial else ""
        cols_str = ", ".join(combined_cols)

        create_sql = f"CREATE INDEX CONCURRENTLY IF NOT EXISTS {index_name} ON {table} ({cols_str}){where_part};"

        # Speedup estimation
        if selectivity <= 0.01:
            speedup = 95.0
            index_type = "COMPOSITE_BTREE_HIGH_SELECTIVITY"
        elif selectivity <= 0.05:
            speedup = 85.0
            index_type = "COMPOSITE_BTREE_STANDARD"
        else:
            speedup = 45.0
            index_type = "BTREE_MODERATE_SELECTIVITY"

        if is_partial:
            index_type = "PARTIAL_FILTERED_BTREE"

        return {
            "table_name": table,
            "recommended_index_name": index_name,
            "index_type": index_type,
            "selectivity": selectivity,
            "create_index_sql": create_sql,
            "estimated_speedup_percent": speedup,
            "lock_safety": "NON_BLOCKING_CONCURRENT"
        }

    @classmethod
    def scan_redundant_indexes(cls, existing_indexes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Detects prefix redundancies (e.g. index on (col_a) is redundant if (col_a, col_b) exists).
        """
        redundancies: List[Dict[str, Any]] = []

        # Map index names to column lists
        index_map = {}
        for idx in existing_indexes:
            name = idx.get("name")
            cols = idx.get("columns", [])
            table = idx.get("table", "unknown")
            if name and cols:
                index_map[name] = {"table": table, "columns": cols}

        # Compare pairs
        for name_a, data_a in index_map.items():
            for name_b, data_b in index_map.items():
                if name_a != name_b and data_a["table"] == data_b["table"]:
                    cols_a = data_a["columns"]
                    cols_b = data_b["columns"]
                    # If cols_a is a strict prefix of cols_b
                    if len(cols_a) < len(cols_b) and cols_b[:len(cols_a)] == cols_a:
                        redundancies.append({
                            "redundant_index": name_a,
                            "covered_by": name_b,
                            "table": data_a["table"],
                            "redundant_columns": cols_a,
                            "super_index_columns": cols_b,
                            "recommendation": f"DROP INDEX CONCURRENTLY IF EXISTS {name_a};"
                        })

        saved_iops = min(35.0, len(redundancies) * 8.5)

        return {
            "total_indexes_scanned": len(existing_indexes),
            "redundant_indexes_found": len(redundancies),
            "redundancies": redundancies,
            "saved_write_iops_estimate_percent": round(saved_iops, 1)
        }
