"""
========================================================================================
MODULE:    Unified Omni-Search Engine
TOPIC:     Cross-Platform Multi-Facet Search (10MS + CareTutors + Bdjobs)
FILE:      backend/app/services/omni_search_service.py
PURPOSE:   Provides unified fast search indexing and ranked relevance scoring across:
           1. 10 Minute School: Video micro-lectures, chapters, and syllabus milestones.
           2. CareTutors: Live tuition requirements by region, class, and remuneration.
           3. Bdjobs: Student internships, tech openings, and skill criteria.
STANDARDS: Normalized Faceted Indexing, Fuzzy Multi-Token Scoring, Sub-10ms Latency
AUDIENCE:  Search Engineers, Frontend Architects & AI Agents
========================================================================================
"""

from typing import Any, Dict, List, Optional
from backend.app.services.video_classroom_service import video_classroom_service
from backend.app.services.tuition_marketplace_service import tuition_marketplace_service
from backend.app.services.job_placement_service import job_placement_service


class OmniSearchService:
    """
    Unified multi-facet search engine providing global search across all 3 platforms.
    """

    CATEGORY_ALL = "ALL"
    CATEGORY_LECTURES = "ACADEMIC_LECTURES"
    CATEGORY_TUITIONS = "TUITIONS"
    CATEGORY_INTERNSHIPS = "INTERNSHIPS"

    def __init__(self):
        pass

    def search(
        self,
        query: str,
        category: str = "ALL",
        limit: int = 15
    ) -> Dict[str, Any]:
        """
        Executes unified search query with fuzzy ranking and returns normalized results.
        """
        clean_query = (query or "").strip().lower()
        results: List[Dict[str, Any]] = []

        # ------------------------------------------------------------------------------
        # 1. Search 10 Minute School Video Lectures
        # ------------------------------------------------------------------------------
        if category in (self.CATEGORY_ALL, self.CATEGORY_LECTURES):
            results.extend(self._search_lectures(clean_query))

        # ------------------------------------------------------------------------------
        # 2. Search CareTutors Live Tuition Listings
        # ------------------------------------------------------------------------------
        if category in (self.CATEGORY_ALL, self.CATEGORY_TUITIONS):
            results.extend(self._search_tuitions(clean_query))

        # ------------------------------------------------------------------------------
        # 3. Search Bdjobs Student Internships & Career Openings
        # ------------------------------------------------------------------------------
        if category in (self.CATEGORY_ALL, self.CATEGORY_INTERNSHIPS):
            results.extend(self._search_internships(clean_query))

        # Sort by relevance score descending
        sorted_results = sorted(results, key=lambda x: x["relevance_score"], reverse=True)
        bounded_results = sorted_results[:max(1, limit)]

        return {
            "success": True,
            "query": query,
            "category": category,
            "total_matches": len(bounded_results),
            "results": bounded_results,
            "message": f"Found {len(bounded_results)} matches across the unified platform."
        }

    def _search_lectures(self, query: str) -> List[Dict[str, Any]]:
        """Searches micro-lectures and syllabus roadmap."""
        lectures = [
            {
                "id": "vid_diff_01",
                "title": "Class 7 Math: Unitary Method, Velocity & Relative Speed",
                "subtitle": "NCTB Curriculum • Chapter 4 (Lecture 1) • 1080p 60fps",
                "badge": "10MS Micro-Lecture",
                "keywords": ["math", "unitary", "velocity", "speed", "distance", "nctb", "class 7", "algebra", "differentiation"],
                "action_url": "#tab-practice"
            },
            {
                "id": "vid_diff_02",
                "title": "HSC Higher Math: Differential Calculus & Chain Rule",
                "subtitle": "NCTB HSC 2026 • Chapter 9 (Calculus) • In-Lecture Quizzes",
                "badge": "HSC Masterclass",
                "keywords": ["calculus", "chain rule", "derivative", "trigonometry", "hsc", "higher math", "physics"],
                "action_url": "#tab-practice"
            },
            {
                "id": "vid_phys_03",
                "title": "HSC Physics: Newton's Laws & Impulse of Force",
                "subtitle": "Engineering Admission Hub • BUET & Medical Blueprints",
                "badge": "Physics Olympiad",
                "keywords": ["physics", "newton", "force", "impulse", "momentum", "admission", "buet"],
                "action_url": "#tab-practice"
            }
        ]

        matches = []
        for item in lectures:
            score = self._compute_relevance(query, item["title"], item["keywords"])
            if score > 0.0 or not query:
                matches.append({
                    "id": item["id"],
                    "category": self.CATEGORY_LECTURES,
                    "title": item["title"],
                    "subtitle": item["subtitle"],
                    "badge": item["badge"],
                    "relevance_score": score if query else 0.85,
                    "action_url": item["action_url"],
                    "meta": {"platform": "10_MINUTE_SCHOOL"}
                })
        return matches

    def _search_tuitions(self, query: str) -> List[Dict[str, Any]]:
        """Searches live CareTutors tuition feed."""
        matches = []
        tuitions = tuition_marketplace_service.get_tuition_feed()
        for t in tuitions:
            keywords = [
                t["subject"].lower(),
                t["location_district"].lower(),
                t["location_thana"].lower(),
                f"class {t['class_grade']}",
                t.get("requirements", "").lower()
            ]
            title = f"Class {t['class_grade']} {t['subject']} — {t['location_thana']}, {t['location_district']}"
            score = self._compute_relevance(query, title, keywords)
            if score > 0.0 or not query:
                matches.append({
                    "id": t["id"],
                    "category": self.CATEGORY_TUITIONS,
                    "title": title,
                    "subtitle": f"{t['salary_budget_bdt']} BDT/month • {t['days_per_week']} Days/Week • Masked Shield Active",
                    "badge": "CareTutors Verified",
                    "relevance_score": score if query else 0.80,
                    "action_url": "#tab-tuition",
                    "meta": {
                        "district": t["location_district"],
                        "thana": t["location_thana"],
                        "budget_bdt": t["salary_budget_bdt"]
                    }
                })
        return matches

    def _search_internships(self, query: str) -> List[Dict[str, Any]]:
        """Searches Bdjobs verified student internships."""
        matches = []
        jobs = job_placement_service.get_job_feed()
        for j in jobs:
            keywords = [
                j["title"].lower(),
                j["company_name"].lower(),
                j["domain"].lower(),
                j["work_mode"].lower(),
                j.get("location", "").lower()
            ] + [s.lower() for s in j.get("required_skills", [])]
            score = self._compute_relevance(query, f"{j['title']} at {j['company_name']}", keywords)
            if score > 0.0 or not query:
                matches.append({
                    "id": j["id"],
                    "category": self.CATEGORY_INTERNSHIPS,
                    "title": f"{j['title']} ({j['company_name']})",
                    "subtitle": f"{j['salary_range_bdt']} • {j['work_mode']} • Verified Employer",
                    "badge": "Bdjobs Direct",
                    "relevance_score": score if query else 0.90,
                    "action_url": "#tab-career",
                    "meta": {
                        "company": j["company_name"],
                        "domain": j["domain"],
                        "skills": j.get("required_skills", [])
                    }
                })
        return matches

    def _compute_relevance(self, query: str, title: str, keywords: List[str]) -> float:
        """Computes normalized fuzzy relevance score between 0.0 and 1.0."""
        clean_q = (query or "").strip().lower()
        if not clean_q:
            return 0.5

        title_lower = title.lower()
        # 1. Exact full match in title
        if clean_q == title_lower:
            return 1.0
        # 2. Exact substring match in title
        if clean_q in title_lower:
            return 0.85

        tokens = [t.strip(",.:;?!'\"-") for t in clean_q.split() if t.strip(",.:;?!'\"-")]
        if not tokens:
            return 0.5

        matched_tokens = 0
        for token in tokens:
            if token in title_lower or any(token in kw for kw in keywords):
                matched_tokens += 1

        if matched_tokens == 0:
            return 0.0

        return round(0.4 + (0.5 * (matched_tokens / len(tokens))), 2)


# Singleton instance
omni_search_service = OmniSearchService()
