"""
Autonomous Academic Thesis & Research Paper Citation Graph Engine
Provides semantic citation index, BibTeX formatting, n-gram shingle plagiarism detection,
and student research grant matching across Bangladeshi universities.
"""

import re
import uuid
import datetime
from typing import Dict, List, Any, Optional, Set


class ThesisCitationGraphService:
    """Enterprise academic citation graph, plagiarism scanner, and grant matching engine."""

    def __init__(self):
        self._theses: Dict[str, Dict[str, Any]] = {}
        self._citation_graph_edges: List[Dict[str, str]] = []  # {"source": paper_id, "target": paper_id}
        self._research_grants: List[Dict[str, Any]] = []
        self._initialize_seed_data()

    def _initialize_seed_data(self):
        # 1. Seed Theses
        seed_papers = [
            {
                "paper_id": "THESIS-BUET-2024-01",
                "title": "Low-Resource Neural Machine Translation for Regional Bangla Dialects",
                "abstract": "We present an unsupervised syntactic alignment framework utilizing cross-lingual subword embeddings tailored specifically for Chittagonian, Sylheti, and Noakhali dialects against standard Bangla.",
                "authors": ["Tanvir Ahmed", "Nusrat Jahan", "Dr. Mohammad Kaykobad"],
                "institution": "BUET",
                "department": "Computer Science & Engineering",
                "publication_year": 2024,
                "doi": "10.1109/BANGLA.NLP.2024.101",
                "keywords": ["Bangla NLP", "Machine Translation", "Low-Resource Languages", "Transformers"],
                "cites": ["THESIS-DU-2023-01"],
                "cited_by": ["THESIS-SUST-2024-02"],
                "created_at": "2024-06-15T10:00:00Z"
            },
            {
                "paper_id": "THESIS-DU-2023-01",
                "title": "Securing Mobile Financial Services via On-Device Behavioral Biometrics",
                "abstract": "This thesis explores non-intrusive continuous authentication on Android smartphones utilizing keystroke dynamics, touchscreen gyroscope telemetry, and lightweight federated inference.",
                "authors": ["Rahim Uddin", "Farhana Islam"],
                "institution": "University of Dhaka",
                "department": "Computer Science & Engineering",
                "publication_year": 2023,
                "doi": "10.1007/MFS.SEC.2023.204",
                "keywords": ["Cybersecurity", "Fintech", "Behavioral Biometrics", "Federated Learning"],
                "cites": [],
                "cited_by": ["THESIS-BUET-2024-01", "THESIS-NSU-2024-03"],
                "created_at": "2023-11-20T14:30:00Z"
            },
            {
                "paper_id": "THESIS-SUST-2024-02",
                "title": "Acoustic Wavelet Feature Extraction for Low-Latency Bangla Speech Recognition",
                "abstract": "We propose a real-time speech-to-text pipeline optimized for edge mobile devices, leveraging continuous wavelet transforms and connectionist temporal classification.",
                "authors": ["Ariful Haque", "Dr. M. Rezaur Rahman"],
                "institution": "SUST",
                "department": "Electrical & Electronic Engineering",
                "publication_year": 2024,
                "doi": "10.1016/SUST.SPEECH.2024.305",
                "keywords": ["Speech Recognition", "Acoustic Signal Processing", "Wavelet Transform", "Edge AI"],
                "cites": ["THESIS-BUET-2024-01"],
                "cited_by": [],
                "created_at": "2024-08-10T09:15:00Z"
            },
            {
                "paper_id": "THESIS-NSU-2024-03",
                "title": "Privacy-Preserving Federated Learning for Cross-Hospital Chest X-Ray Screening",
                "abstract": "A decentralized collaborative medical image classification network deployed across three tertiary hospitals in Dhaka to identify tuberculosis without sharing raw patient DICOM scans.",
                "authors": ["Tasnim Chowdhury", "Shakil Mahmud"],
                "institution": "North South University",
                "department": "Electrical & Computer Engineering",
                "publication_year": 2024,
                "doi": "10.1016/MED.AI.2024.409",
                "keywords": ["Medical Imaging", "Federated Learning", "Healthcare AI", "Differential Privacy"],
                "cites": ["THESIS-DU-2023-01"],
                "cited_by": [],
                "created_at": "2024-09-05T16:45:00Z"
            }
        ]

        for p in seed_papers:
            p["citation_count"] = len(p["cited_by"])
            p["bibtex"] = self._generate_bibtex(p)
            self._theses[p["paper_id"]] = p

        # 2. Seed Research Grants
        self._research_grants = [
            {
                "grant_id": "GRANT-UGC-2025-01",
                "title": "UGC National Student Research Grant in AI & Deep Tech",
                "funding_agency": "University Grants Commission (UGC) Bangladesh",
                "amount_bdt": 150000.0,
                "eligibility_criteria": ["Undergraduate final year thesis student", "Minimum CGPA 3.50", "Bangla NLP or Hardware IoT focus"],
                "deadline": "2025-11-30",
                "application_url": "https://ugc.gov.bd/grants/student-ai-2025"
            },
            {
                "grant_id": "GRANT-ICT-2025-02",
                "title": "ICT Division Fellowship for Digital Transformation & Cybersecurity",
                "funding_agency": "ICT Division, Ministry of Posts, Telecommunications & IT",
                "amount_bdt": 200000.0,
                "eligibility_criteria": ["Enrolled university student", "Cybersecurity, FinTech, or Blockchain thesis proposal"],
                "deadline": "2025-12-15",
                "application_url": "https://ictd.gov.bd/fellowships/cyber-fintech-2025"
            },
            {
                "grant_id": "GRANT-DAAD-2025-03",
                "title": "DAAD-Bangladesh STEM Undergraduate Mobility Grant",
                "funding_agency": "German Academic Exchange Service (DAAD)",
                "amount_bdt": 350000.0,
                "eligibility_criteria": ["3rd/4th year undergraduate student", "Renewable energy or biomedical engineering research"],
                "deadline": "2026-01-31",
                "application_url": "https://daad-bangladesh.org/stem-mobility-2025"
            }
        ]

    def _generate_bibtex(self, paper: Dict[str, Any]) -> str:
        first_author = paper["authors"][0].split()[-1].lower() if paper.get("authors") else "anonymous"
        slug = f"{first_author}_{paper.get('publication_year', 2025)}_{paper.get('paper_id', 'id').lower()}"
        authors_bib = " and ".join(paper.get("authors", []))
        return (
            f"@article{{{slug},\n"
            f"  title = {{{paper.get('title')}}},\n"
            f"  author = {{{authors_bib}}},\n"
            f"  institution = {{{paper.get('institution')}}},\n"
            f"  department = {{{paper.get('department')}}},\n"
            f"  year = {{{paper.get('publication_year')}}},\n"
            f"  doi = {{{paper.get('doi')}}}\n"
            f"}}"
        )

    def submit_thesis_paper(
        self,
        title: str,
        abstract: str,
        authors: List[str],
        institution: str,
        department: str,
        publication_year: int = 2025,
        keywords: Optional[List[str]] = None,
        cited_paper_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Submits a new student thesis and links citation edges."""
        title_sanitized = title.strip()
        abstract_sanitized = abstract.strip()
        if not title_sanitized or not abstract_sanitized:
            raise ValueError("Thesis title and abstract cannot be empty.")
        if not authors:
            raise ValueError("At least one author must be specified.")

        paper_id = f"THESIS-{institution.upper()[:4]}-{publication_year}-{uuid.uuid4().hex[:4].upper()}"
        cites_list = cited_paper_ids or []

        # Validate cited paper IDs exist in repository
        valid_cites = [cid for cid in cites_list if cid in self._theses]

        paper = {
            "paper_id": paper_id,
            "title": title_sanitized,
            "abstract": abstract_sanitized,
            "authors": [a.strip() for a in authors if a.strip()],
            "institution": institution.strip(),
            "department": department.strip(),
            "publication_year": publication_year,
            "doi": f"10.5281/zenodo.{uuid.uuid4().int % 10000000}",
            "keywords": keywords or [],
            "cites": valid_cites,
            "cited_by": [],
            "citation_count": 0,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        paper["bibtex"] = self._generate_bibtex(paper)

        # Update cited papers' incoming citation records
        for cid in valid_cites:
            self._theses[cid]["cited_by"].append(paper_id)
            self._theses[cid]["citation_count"] = len(self._theses[cid]["cited_by"])

        self._theses[paper_id] = paper
        return paper

    def get_paper_citation_network(self, paper_id: str) -> Dict[str, Any]:
        """Returns the paper details and its immediate 1-hop citation network."""
        if paper_id not in self._theses:
            raise ValueError(f"Thesis paper '{paper_id}' not found in repository.")

        target = self._theses[paper_id]
        nodes = [target]
        edges = []

        # Add papers that this paper cites
        for c_id in target["cites"]:
            if c_id in self._theses:
                nodes.append(self._theses[c_id])
                edges.append({"source": paper_id, "target": c_id, "relation": "CITES"})

        # Add papers that cite this paper
        for b_id in target["cited_by"]:
            if b_id in self._theses:
                if self._theses[b_id] not in nodes:
                    nodes.append(self._theses[b_id])
                edges.append({"source": b_id, "target": paper_id, "relation": "CITED_BY"})

        return {
            "root_paper": target,
            "network_nodes": nodes,
            "network_edges": edges,
            "total_citations": target["citation_count"]
        }

    def check_thesis_similarity(self, text_sample: str, min_shingle_size: int = 3) -> Dict[str, Any]:
        """
        Calculates n-gram token shingle Jaccard similarity against all registered abstracts.
        Guarantees zero regex ReDoS.
        """
        clean_text = text_sample.strip().lower()
        if len(clean_text) < 15:
            raise ValueError("Input text sample too short for reliable similarity analysis (minimum 15 characters).")

        # Safe tokenization without unbounded regex backtracking
        tokens = [t for t in re.findall(r"[a-z0-9]+", clean_text) if len(t) > 1]
        if len(tokens) < min_shingle_size:
            return {
                "originality_score": 100.0,
                "highest_similarity": 0.0,
                "flagged_as_duplicate": False,
                "matches": []
            }

        input_shingles = self._compute_shingles(tokens, min_shingle_size)
        matches: List[Dict[str, Any]] = []
        highest_sim = 0.0

        for p_id, p_data in self._theses.items():
            corpus_text = (p_data["title"] + " " + p_data["abstract"]).lower()
            corpus_tokens = [t for t in re.findall(r"[a-z0-9]+", corpus_text) if len(t) > 1]
            corpus_shingles = self._compute_shingles(corpus_tokens, min_shingle_size)

            intersection = input_shingles.intersection(corpus_shingles)
            union = input_shingles.union(corpus_shingles)
            jaccard = len(intersection) / len(union) if union else 0.0

            if jaccard > 0.05:  # Report matches with > 5% shingle similarity
                matched_phrases = [" ".join(tokens[i:i+min_shingle_size]) for i in range(min(3, len(tokens)-min_shingle_size+1))]
                matches.append({
                    "paper_id": p_id,
                    "title": p_data["title"],
                    "institution": p_data["institution"],
                    "similarity_score": round(jaccard * 100.0, 2),
                    "matched_fragments": matched_phrases[:3]
                })
                if jaccard > highest_sim:
                    highest_sim = jaccard

        matches.sort(key=lambda x: x["similarity_score"], reverse=True)
        originality = max(0.0, round((1.0 - highest_sim) * 100.0, 2))

        return {
            "originality_score": originality,
            "highest_similarity": round(highest_sim * 100.0, 2),
            "flagged_as_duplicate": highest_sim >= 0.70,
            "matches": matches
        }

    def _compute_shingles(self, tokens: List[str], n: int) -> Set[str]:
        shingles = set()
        for i in range(len(tokens) - n + 1):
            shingle = " ".join(tokens[i:i + n])
            shingles.add(shingle)
        return shingles

    def match_research_grants(self, field_of_study: str, academic_level: str = "UNDERGRADUATE") -> Dict[str, Any]:
        """Matches student field of study and criteria against available research endowments."""
        query = field_of_study.lower()
        matched = []
        for g in self._research_grants:
            # Check eligibility and keywords
            title_keywords = g["title"].lower() + " " + " ".join(g["eligibility_criteria"]).lower()
            is_match = any(word in title_keywords for word in query.split() if len(word) > 2)
            if is_match or "stem" in title_keywords or "ai" in query:
                matched.append(g)

        return {
            "matched_grants": matched or self._research_grants[:2],
            "total_matched": len(matched) if matched else 2
        }

    def list_all_papers(self) -> List[Dict[str, Any]]:
        return list(self._theses.values())


# Export singleton instance
thesis_citation_graph_service = ThesisCitationGraphService()
