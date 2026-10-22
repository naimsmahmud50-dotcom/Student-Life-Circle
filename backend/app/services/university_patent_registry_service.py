"""
Autonomous Intellectual Property & University Patent Filing Registry Service
Manages patent disclosures, formal claims formatting, cryptographic audit seals,
and prior art novelty analysis for university researchers and student innovators.
"""

import re
import uuid
import hashlib
import datetime
from typing import Dict, List, Any, Optional


class UniversityPatentRegistryService:
    """Enterprise university patent registry and prior art search engine."""

    def __init__(self):
        self._patents: Dict[str, Dict[str, Any]] = {}
        self._initialize_seed_data()

    def _initialize_seed_data(self):
        seed_patents = [
            {
                "patent_id": "PAT-BUET-2024-001",
                "title": "Edge-Optimized Spiking Neural Processor for Bangla Acoustic Feature Extraction",
                "abstract": "An ultra-low power asynchronous neuromorphic CMOS core computing continuous wavelet speech features at sub-millivolt supply levels for resource-constrained edge devices.",
                "inventors": ["Tanvir Ahmed", "Prof. Dr. Mohammad Kaykobad"],
                "institution": "BUET",
                "ipc_classification": "G06F 17/14",
                "technical_field": "AI & Neuromorphic Electronics",
                "claims": [
                    "A neuromorphic CMOS circuit architecture comprising asynchronous event-driven synaptic arrays.",
                    "The circuit of claim 1 wherein each wavelet filter bank operates in the subthreshold analog domain."
                ],
                "novelty_score": 94.5,
                "cryptographic_disclosure_seal": "SEAL-SHA256-BUET-94A8C1102B98",
                "filed_at": "2024-05-10T12:00:00Z"
            },
            {
                "patent_id": "PAT-DU-2023-002",
                "title": "Continuous Behavioral Biometrics Authentication for Mobile Financial Services",
                "abstract": "A machine learning system embedded within mobile client firmware measuring touchscreen pressure micro-vibrations and keystroke latency to continuously verify user identity.",
                "inventors": ["Rahim Uddin", "Farhana Islam"],
                "institution": "University of Dhaka",
                "ipc_classification": "G06F 21/32",
                "technical_field": "Cybersecurity & Fintech",
                "claims": [
                    "A computer-implemented method for biometric continuous authentication on handheld mobile devices.",
                    "The method of claim 1 wherein sensor gyroscope telemetry is transformed into an on-device anomaly score."
                ],
                "novelty_score": 91.2,
                "cryptographic_disclosure_seal": "SEAL-SHA256-DU-88F41A990D2C",
                "filed_at": "2023-11-15T09:30:00Z"
            },
            {
                "patent_id": "PAT-SUST-2024-003",
                "title": "Adaptive Wavelet Inverter Control for Solar-Battery Microgrids",
                "abstract": "A real-time embedded power electronic controller mitigating harmonic resonance and voltage sag in rural microgrids through instant sub-cycle phase frequency adjustment.",
                "inventors": ["Ariful Haque", "Dr. M. Rezaur Rahman"],
                "institution": "SUST",
                "ipc_classification": "H02M 7/48",
                "technical_field": "Renewable Energy & Power Electronics",
                "claims": [
                    "A power converter controller for multi-source solar microgrids comprising a high-speed DSP phase detector.",
                    "The controller of claim 1 capable of isolated islanding transition within 4 milliseconds."
                ],
                "novelty_score": 88.7,
                "cryptographic_disclosure_seal": "SEAL-SHA256-SUST-77B21C440E1A",
                "filed_at": "2024-07-22T15:45:00Z"
            }
        ]

        for p in seed_patents:
            self._patents[p["patent_id"]] = p

    def file_patent_disclosure(
        self,
        title: str,
        abstract: str,
        inventors: List[str],
        institution: str,
        ipc_classification: str = "G06F",
        claims: Optional[List[str]] = None,
        technical_field: str = "AI and Semiconductor Electronics"
    ) -> Dict[str, Any]:
        """
        Registers a new university patent disclosure with automated cryptographic seal.
        """
        title_clean = title.strip()
        abstract_clean = abstract.strip()
        if not title_clean or not abstract_clean:
            raise ValueError("Patent disclosure title and abstract cannot be empty.")
        if not inventors:
            raise ValueError("At least one inventor must be specified.")

        pat_id = f"PAT-{institution.upper()[:4]}-{datetime.datetime.now().year}-{uuid.uuid4().hex[:4].upper()}"

        # Generate formal claims if not provided
        formal_claims = claims or [
            f"An apparatus for {title_clean.lower()}, comprising one or more integrated processing modules.",
            "The apparatus of claim 1, configured to operate within bounded thermal and energy limits."
        ]

        # Calculate Novelty Score against existing corpus
        prior_art_res = self.search_prior_art(abstract_clean)
        novelty = prior_art_res["average_novelty_score"]

        # Generate Cryptographic SHA-256 Seal
        payload = f"{pat_id}:{title_clean}:{abstract_clean}:{institution}".encode("utf-8")
        seal = f"SEAL-SHA256-{institution.upper()[:4]}-{hashlib.sha256(payload).hexdigest()[:12].upper()}"

        patent_record = {
            "patent_id": pat_id,
            "title": title_clean,
            "abstract": abstract_clean,
            "inventors": [i.strip() for i in inventors if i.strip()],
            "institution": institution.strip(),
            "ipc_classification": ipc_classification.strip(),
            "technical_field": technical_field.strip(),
            "claims": formal_claims,
            "novelty_score": round(novelty, 1),
            "cryptographic_disclosure_seal": seal,
            "filed_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

        self._patents[pat_id] = patent_record
        return patent_record

    def get_patent_disclosure(self, patent_id: str) -> Dict[str, Any]:
        if patent_id not in self._patents:
            raise ValueError(f"Patent disclosure '{patent_id}' not found.")
        return self._patents[patent_id]

    def search_prior_art(self, search_query: str, min_novelty_threshold: float = 0.3) -> Dict[str, Any]:
        """
        Compares query tokens against registered disclosures to compute similarity and novelty.
        """
        clean_q = search_query.strip().lower()
        if len(clean_q) < 5:
            raise ValueError("Prior art search query must contain at least 5 characters.")

        q_tokens = set(re.findall(r"[a-z0-9]+", clean_q))
        matches = []
        max_sim = 0.0

        for p_id, p in self._patents.items():
            corpus_text = (p["title"] + " " + p["abstract"] + " " + " ".join(p["claims"])).lower()
            c_tokens = set(re.findall(r"[a-z0-9]+", corpus_text))

            inter = q_tokens.intersection(c_tokens)
            union = q_tokens.union(c_tokens)
            sim = len(inter) / len(union) if union else 0.0

            if sim > 0.03:
                matches.append({
                    "patent_id": p_id,
                    "title": p["title"],
                    "institution": p["institution"],
                    "similarity_index": round(sim * 100.0, 1),
                    "overlapping_claims": [c[:60] + "..." for c in p["claims"][:2]]
                })
                if sim > max_sim:
                    max_sim = sim

        matches.sort(key=lambda x: x["similarity_index"], reverse=True)
        avg_novelty = max(10.0, round((1.0 - max_sim) * 100.0, 1))

        return {
            "search_query": search_query,
            "matches": matches,
            "is_patentable_novel": avg_novelty >= 60.0,
            "average_novelty_score": avg_novelty
        }

    def list_all_patents(self) -> List[Dict[str, Any]]:
        return list(self._patents.values())


# Export singleton instance
university_patent_registry_service = UniversityPatentRegistryService()
