"""
National STEM Olympiad Arena & Mathematical Proof Evaluator Service
Covers BdMO (Math), BdPhO (Physics), BdIO (Informatics), and BDBO (Biology).
Provides fractional scoring rubrics, penalty timers, and Olympiad percentile leaderboards.
"""

import uuid
import datetime
from typing import Dict, List, Any, Optional


class NationalOlympiadArenaService:
    """Enterprise Olympiad contest arena, automated proof grader, and leaderboard engine."""

    def __init__(self):
        self._problems: Dict[str, Dict[str, Any]] = {}
        self._submissions: Dict[str, Dict[str, Any]] = {}
        self._leaderboards: Dict[str, List[Dict[str, Any]]] = {}
        self._initialize_seed_data()

    def _initialize_seed_data(self):
        seed_problems = [
            {
                "problem_id": "OLYMP-BDMO-2024-01",
                "competition": "BDMO",
                "year": 2024,
                "division": "HIGHER_SECONDARY",
                "title": "Diophantine Sum of Squares for 2025",
                "statement": "Find all pairs of non-negative integers (x, y) such that x^2 + y^2 = 2025. Provide the exact count of unique ordered integer pairs.",
                "difficulty_elo": 1850,
                "max_score": 10.0,
                "expected_numerical_answer": 8.0,
                "numerical_tolerance": 0.01,
                "key_keywords": ["factorization", "gaussian", "mod 4", "prime"],
                "sample_hint": "Note that 2025 = 45^2 = 3^4 * 5^2. Use prime factorization over Gaussian integers.",
                "official_solution": "2025 = 3^4 * 5^2. Any prime factor of form 4k+3 (i.e. 3) must appear with even exponent (which it does, 3^4). The prime 5 = 1^2 + 2^2 has exponent 2. The total number of representations as sum of two squares is r_2(2025) = 4 * (d_1(2025) - d_3(2025)) = 4 * 3 = 12 representations in Z x Z, yielding 8 non-negative ordered pairs: (0, 45), (45, 0), (27, 36), (36, 27), (15, 42), (42, 15), and variations."
            },
            {
                "problem_id": "OLYMP-BDPHO-2024-02",
                "competition": "BDPHO",
                "year": 2024,
                "division": "HIGHER_SECONDARY",
                "title": "Relativistic Compton Shift in Dense Electron Gas",
                "statement": "A photon of initial wavelength 0.024 nm scatters at 90 degrees off a stationary electron. Calculate the scattered photon wavelength in picometers (pm).",
                "difficulty_elo": 1920,
                "max_score": 10.0,
                "expected_numerical_answer": 26.43,
                "numerical_tolerance": 0.1,
                "key_keywords": ["compton", "wavelength", "scattering", "lambda"],
                "sample_hint": "Use Compton formula: Delta_lambda = (h / m_e c) * (1 - cos(theta)). Note Compton wavelength h/(m_e c) = 2.43 pm.",
                "official_solution": "Delta_lambda = lambda_C * (1 - cos(90 deg)) = 2.426 pm * (1 - 0) = 2.426 pm. Final wavelength lambda' = 24.0 pm + 2.43 pm = 26.43 pm."
            },
            {
                "problem_id": "OLYMP-BDIO-2024-03",
                "competition": "BDIO",
                "year": 2024,
                "division": "SECONDARY",
                "title": "Subtree Centroid Decomposition Path Query",
                "statement": "Given a tree of N = 100,000 vertices, find the maximum diameter after removing any single vertex of degree >= 3. For the benchmark star graph with 10 peripheral leaves, state the new diameter.",
                "difficulty_elo": 1780,
                "max_score": 10.0,
                "expected_numerical_answer": 2.0,
                "numerical_tolerance": 0.01,
                "key_keywords": ["centroid", "diameter", "tree", "bfs"],
                "sample_hint": "Consider the disconnection of the central hub.",
                "official_solution": "Removing the center hub from a star graph leaves disconnected components of single vertices with diameter 0, or components of diameter 2 depending on residual connectivity."
            },
            {
                "problem_id": "OLYMP-BDBO-2024-04",
                "competition": "BDBO",
                "year": 2024,
                "division": "JUNIOR",
                "title": "Hardy-Weinberg Equilibrium Genotype Frequency",
                "statement": "In a closed population in Hardy-Weinberg equilibrium, the frequency of homozygous recessive individuals (q^2) is 0.09. Calculate the percentage of heterozygous carriers (2pq).",
                "difficulty_elo": 1550,
                "max_score": 10.0,
                "expected_numerical_answer": 42.0,
                "numerical_tolerance": 0.5,
                "key_keywords": ["allele", "heterozygous", "hardy", "weinberg"],
                "sample_hint": "q = sqrt(0.09) = 0.3. Then p = 1 - q = 0.7.",
                "official_solution": "q = 0.3, p = 0.7. Heterozygous frequency 2pq = 2 * 0.7 * 0.3 = 0.42 or 42.0%."
            }
        ]

        for p in seed_problems:
            self._problems[p["problem_id"]] = p

        # Seed Leaderboard
        self._leaderboards["BDMO"] = [
            {"rank": 1, "student_id": "stu-olym-01", "student_name": "Sabbir Hossain", "division": "HIGHER_SECONDARY", "total_score": 29.5, "solved_count": 3, "percentile": 99.8},
            {"rank": 2, "student_id": "stu-olym-02", "student_name": "Ananya Sen", "division": "HIGHER_SECONDARY", "total_score": 28.0, "solved_count": 3, "percentile": 98.4},
            {"rank": 3, "student_id": "stu-olym-03", "student_name": "Fahim Shahriar", "division": "SECONDARY", "total_score": 26.5, "solved_count": 3, "percentile": 96.1}
        ]

    def list_problems(self, competition: Optional[str] = None, division: Optional[str] = None) -> List[Dict[str, Any]]:
        probs = list(self._problems.values())
        if competition:
            probs = [p for p in probs if p["competition"] == competition.upper()]
        if division:
            probs = [p for p in probs if p["division"] == division.upper()]
        return probs

    def get_problem(self, problem_id: str) -> Dict[str, Any]:
        if problem_id not in self._problems:
            raise ValueError(f"Olympiad problem '{problem_id}' not found.")
        return self._problems[problem_id]

    def submit_solution(
        self,
        problem_id: str,
        student_id: str,
        student_name: str,
        solution_text: str,
        numerical_answer: Optional[float] = None,
        time_spent_seconds: int = 120
    ) -> Dict[str, Any]:
        """
        Evaluates Olympiad submission against mathematical rubrics, numerical tolerances,
        and applies time decay penalty for competitive fairness.
        """
        problem = self.get_problem(problem_id)
        sub_id = f"SUB-{uuid.uuid4().hex[:6].upper()}"

        solution_clean = solution_text.strip()
        if len(solution_clean) < 10:
            raise ValueError("Solution proof text must contain at least 10 characters detailing derivation.")

        # Check numerical correctness if expected
        is_num_correct = False
        num_score = 0.0
        if problem.get("expected_numerical_answer") is not None and numerical_answer is not None:
            expected = problem["expected_numerical_answer"]
            tol = problem.get("numerical_tolerance", 0.05)
            if abs(numerical_answer - expected) <= tol:
                is_num_correct = True
                num_score = 6.0  # 60% weight for accurate answer
            else:
                num_score = 0.0

        # Check proof reasoning keywords (up to 40% weight)
        matched_kw_count = 0
        sol_lower = solution_clean.lower()
        for kw in problem.get("key_keywords", []):
            if kw.lower() in sol_lower:
                matched_kw_count += 1

        total_kw = len(problem.get("key_keywords", []))
        proof_score = (matched_kw_count / total_kw * 4.0) if total_kw > 0 else 4.0

        raw_score = num_score + proof_score
        is_fully_correct = is_num_correct and (proof_score >= 2.0)

        # Time penalty: 0.005 points per second exceeding 180 seconds
        time_penalty = max(0.0, (time_spent_seconds - 180) * 0.005)
        net_score = max(0.0, round(raw_score - time_penalty, 2))

        submission = {
            "submission_id": sub_id,
            "problem_id": problem_id,
            "student_id": student_id,
            "student_name": student_name,
            "is_correct": is_fully_correct,
            "fractional_score": round(raw_score, 2),
            "max_score": problem["max_score"],
            "time_penalty": round(time_penalty, 2),
            "net_score": net_score,
            "feedback": (
                "Flawless mathematical proof and numerical precision."
                if is_fully_correct
                else "Partial credit awarded for conceptual derivation steps."
            ),
            "official_solution_breakdown": problem["official_solution"],
            "submitted_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

        self._submissions[sub_id] = submission
        return submission

    def get_leaderboard(self, competition: str = "BDMO") -> Dict[str, Any]:
        comp_key = competition.upper()
        entries = self._leaderboards.get(comp_key, self._leaderboards.get("BDMO", []))
        return {
            "competition": comp_key,
            "entries": entries,
            "total_participants": len(entries)
        }


# Export singleton instance
national_olympiad_arena_service = NationalOlympiadArenaService()
