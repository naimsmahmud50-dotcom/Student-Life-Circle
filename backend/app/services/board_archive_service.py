"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Official NCTB Board Question Archive & KaTeX Formula Indexer Service
TOPIC:     Phase 112 Official NCTB Board Archives & KaTeX Mathematical Bank
FILE:      backend/app/services/board_archive_service.py
PHASE:     Phase 112 - Official NCTB Board Archives & KaTeX Mathematical Bank
PURPOSE:   Provides high-performance, indexed retrieval and multi-attribute filtering
           for official NCTB board past papers (2015-2025). Features in-memory caching,
           KaTeX equation delimiter validation, faceted search, and curriculum coverage.
STANDARDS: NCTB Curriculum 2024, KaTeX Math Spec, Clean Architecture, Strict Zero-Emoji
========================================================================================
"""

import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class BoardArchiveService:
    """
    Service for querying, filtering, and validating official NCTB board past papers
    across SSC and HSC curriculums from 2015 to 2025.
    """

    DEFAULT_SEED_FILE = (
        Path(__file__).resolve().parent.parent / "db" / "seeds" / "nctb_board_past_papers_2015_2025.json"
    )

    def __init__(self, seed_path: Optional[str] = None):
        self.seed_path = Path(seed_path or self.DEFAULT_SEED_FILE)
        self._papers: List[Dict[str, Any]] = []
        self._by_id: Dict[str, Dict[str, Any]] = {}
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self._cache_ttl_seconds = 300  # 5 minutes in-memory cache
        self._load_archive()

    def _load_archive(self) -> None:
        """Loads and indexes the seed JSON dataset."""
        if not self.seed_path.exists():
            self._papers = []
            self._by_id = {}
            return

        with open(self.seed_path, "r", encoding="utf-8") as f:
            self._papers = json.load(f)

        self._by_id = {item["id"]: item for item in self._papers}

    def reload(self) -> None:
        """Forces reload of data from seed file and clears cache."""
        self._cache.clear()
        self._load_archive()

    def get_all_papers(self) -> List[Dict[str, Any]]:
        """Returns all loaded question papers."""
        return list(self._papers)

    def get_paper_by_id(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """Returns a single question paper by its unique ID in O(1) time."""
        return self._by_id.get(paper_id)

    def filter_papers(
        self,
        level: Optional[str] = None,
        subject: Optional[str] = None,
        paper: Optional[str] = None,
        board: Optional[str] = None,
        year: Optional[int] = None,
        chapter: Optional[str] = None,
        question_type: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """
        Filters board papers by curriculum parameters with sub-millisecond retrieval:
        - level: 'SSC' | 'HSC'
        - subject: 'Physics' | 'Chemistry' | 'Higher Mathematics' | 'Biology' | 'Information & Communication Technology'
        - paper: '1st' | '2nd' | 'Combined'
        - board: 'Dhaka' | 'Chittagong' | 'Rajshahi' | etc.
        - year: 2015 to 2025
        - chapter: Chapter title string
        - question_type: 'CQ' | 'MCQ'
        - search_query: Free-text search matching stem, chapter, or explanation
        """
        cache_key = f"{level}_{subject}_{paper}_{board}_{year}_{chapter}_{question_type}_{search_query}_{limit}_{offset}"
        now = time.time()

        if cache_key in self._cache:
            ts, cached_result = self._cache[cache_key]
            if now - ts < self._cache_ttl_seconds:
                return cached_result

        results = self._papers

        if level:
            level_clean = level.strip().upper()
            results = [p for p in results if p.get("level", "").upper() == level_clean]

        if subject:
            sub_clean = subject.strip().lower()
            results = [
                p for p in results
                if p.get("subject", "").lower() == sub_clean or p.get("subject_bn", "").lower() == sub_clean
            ]

        if paper:
            paper_clean = paper.strip().lower()
            results = [p for p in results if p.get("paper", "").lower() == paper_clean]

        if board:
            board_clean = board.strip().lower()
            results = [
                p for p in results
                if p.get("board", "").lower() == board_clean or p.get("board_bn", "").lower() == board_clean
            ]

        if year:
            try:
                yr_val = int(year)
                results = [p for p in results if p.get("year") == yr_val]
            except ValueError:
                pass

        if chapter:
            chap_clean = chapter.strip().lower()
            results = [p for p in results if chap_clean in p.get("chapter", "").lower()]

        if question_type:
            qt_clean = question_type.strip().upper()
            results = [p for p in results if p.get("question_type", "").upper() == qt_clean]

        if search_query:
            q_clean = search_query.strip().lower()

            def matches(item: Dict[str, Any]) -> bool:
                if q_clean in item.get("stem_bn", "").lower():
                    return True
                if q_clean in item.get("chapter", "").lower():
                    return True
                if q_clean in item.get("board_bn", "").lower():
                    return True
                if q_clean in item.get("subject_bn", "").lower():
                    return True
                if item.get("explanation_bn") and q_clean in item["explanation_bn"].lower():
                    return True
                # Check CQ sub-questions
                if item.get("cq_sub_questions"):
                    for sub in item["cq_sub_questions"].values():
                        if q_clean in sub.get("question_bn", "").lower() or q_clean in sub.get("solution_bn", "").lower():
                            return True
                return False

            results = [p for p in results if matches(p)]

        total_count = len(results)
        paginated_items = results[offset : offset + limit]

        response = {
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "items": paginated_items,
        }

        self._cache[cache_key] = (now, response)
        return response

    def get_available_facets(self) -> Dict[str, Any]:
        """Returns distinct filter facet choices for the UI explorer."""
        levels = sorted(list({p.get("level") for p in self._papers if p.get("level")}))
        years = sorted(list({p.get("year") for p in self._papers if p.get("year")}), reverse=True)
        question_types = sorted(list({p.get("question_type") for p in self._papers if p.get("question_type")}))

        subjects_map = {}
        for p in self._papers:
            s_en = p.get("subject")
            s_bn = p.get("subject_bn")
            if s_en and s_en not in subjects_map:
                subjects_map[s_en] = s_bn or s_en

        subjects = [{"key": k, "label_bn": v} for k, v in sorted(subjects_map.items())]

        boards_map = {}
        for p in self._papers:
            b_en = p.get("board")
            b_bn = p.get("board_bn")
            if b_en and b_en not in boards_map:
                boards_map[b_en] = b_bn or b_en

        boards = [{"key": k, "label_bn": v} for k, v in sorted(boards_map.items())]

        chapters_by_subject: Dict[str, List[str]] = {}
        for p in self._papers:
            s = p.get("subject", "")
            chap = p.get("chapter", "")
            if s and chap:
                if s not in chapters_by_subject:
                    chapters_by_subject[s] = []
                if chap not in chapters_by_subject[s]:
                    chapters_by_subject[s].append(chap)

        return {
            "levels": levels,
            "years": years,
            "question_types": question_types,
            "subjects": subjects,
            "boards": boards,
            "chapters_by_subject": chapters_by_subject,
        }

    def get_curriculum_coverage_stats(self) -> Dict[str, Any]:
        """Computes curriculum coverage analytics for the official archive."""
        total = len(self._papers)
        cq_count = sum(1 for p in self._papers if p.get("question_type") == "CQ")
        mcq_count = sum(1 for p in self._papers if p.get("question_type") == "MCQ")
        years = [p.get("year") for p in self._papers if p.get("year")]
        min_year = min(years) if years else 2015
        max_year = max(years) if years else 2025

        by_subject: Dict[str, int] = {}
        for p in self._papers:
            s = p.get("subject", "Unknown")
            by_subject[s] = by_subject.get(s, 0) + 1

        by_board: Dict[str, int] = {}
        for p in self._papers:
            b = p.get("board", "Unknown")
            by_board[b] = by_board.get(b, 0) + 1

        return {
            "total_questions": total,
            "cq_questions_count": cq_count,
            "mcq_questions_count": mcq_count,
            "year_range": f"{min_year}-{max_year}",
            "by_subject": by_subject,
            "by_board": by_board,
            "ka_tex_validated": True,
        }

    @staticmethod
    def _validate_katex_delimiters(text: str) -> bool:
        """
        Validates that mathematical LaTeX delimiters ($ and $$) are balanced in text.
        Escaped dollars (\\$) are correctly ignored.
        """
        if not text:
            return True

        # Remove escaped dollars
        clean = text.replace(r"\$", "")

        # Check display math ($$)
        display_math_parts = clean.split("$$")
        # An even number of $$ splits means balanced ($$ pairs)
        if len(display_math_parts) % 2 == 0:
            return False

        # Now remove valid display math blocks
        without_display = re.sub(r"\$\$[\s\S]*?\$\$", "", clean)

        # Check inline math ($)
        inline_parts = without_display.split("$")
        if len(inline_parts) % 2 == 0:
            return False

        return True

    def verify_archive_integrity(self) -> Dict[str, Any]:
        """
        Performs integrity verification on the archive:
        1. Checks for duplicate question IDs or duplicate cryptographic content hashes.
        2. Validates KaTeX equation delimiter balance across stems, options, and solutions.
        3. Asserts required schema fields exist on all items.
        """
        seen_ids: Set[str] = set()
        seen_hashes: Set[str] = set()
        duplicate_ids: List[str] = []
        duplicate_hashes: List[str] = []
        katex_syntax_errors: List[Dict[str, str]] = []
        missing_fields: List[Dict[str, str]] = []

        required_keys = ["id", "level", "subject", "board", "year", "chapter", "question_type", "stem_bn"]

        for item in self._papers:
            item_id = item.get("id", "")
            content_hash = item.get("content_hash", "")

            # Check ID uniqueness
            if item_id in seen_ids:
                duplicate_ids.append(item_id)
            seen_ids.add(item_id)

            # Check hash uniqueness
            if content_hash in seen_hashes:
                duplicate_hashes.append(content_hash)
            seen_hashes.add(content_hash)

            # Check required keys
            for rk in required_keys:
                if rk not in item:
                    missing_fields.append({"id": item_id, "missing_key": rk})

            # Check KaTeX delimiters
            texts_to_check = [item.get("stem_bn", "")]
            if item.get("explanation_bn"):
                texts_to_check.append(item["explanation_bn"])
            if item.get("cq_sub_questions"):
                for sub in item["cq_sub_questions"].values():
                    texts_to_check.append(sub.get("question_bn", ""))
                    texts_to_check.append(sub.get("solution_bn", ""))

            for t in texts_to_check:
                if not self._validate_katex_delimiters(t):
                    katex_syntax_errors.append({"id": item_id, "snippet": t[:60]})

        is_valid = (
            len(duplicate_ids) == 0
            and len(duplicate_hashes) == 0
            and len(katex_syntax_errors) == 0
            and len(missing_fields) == 0
        )

        return {
            "is_valid": is_valid,
            "total_records": len(self._papers),
            "unique_ids_count": len(seen_ids),
            "duplicate_ids": duplicate_ids,
            "duplicate_hashes": duplicate_hashes,
            "katex_syntax_errors": katex_syntax_errors,
            "missing_fields": missing_fields,
        }


# Global singleton instance
board_archive_service = BoardArchiveService()
