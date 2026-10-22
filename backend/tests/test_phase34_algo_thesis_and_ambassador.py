"""
Unit, Integration, and Security Test Suite: Phase 34
Verifies:
1. AlgorithmComplexitySandboxService (AST static Big-O complexity, loop nesting, recursion, trace step generator)
2. ThesisCitationGraphService (citation network graph, BibTeX formatting, n-gram shingle plagiarism check, grant matcher)
3. CampusAmbassadorSyndicateService (50+ campus network, task lifecycle, atomic claim locks, reward & tier badges)
4. Section 33 REST Routes in router.py
"""

import unittest
from backend.app.services.algorithm_complexity_sandbox_service import (
    AlgorithmComplexitySandboxService,
    algorithm_complexity_sandbox_service
)
from backend.app.services.thesis_citation_graph_service import (
    ThesisCitationGraphService,
    thesis_citation_graph_service
)
from backend.app.services.campus_ambassador_syndicate_service import (
    CampusAmbassadorSyndicateService,
    campus_ambassador_syndicate_service
)
from backend.app.schemas.algo_thesis_and_ambassador_schema import (
    CodeComplexityRequest,
    AlgorithmTraceRequest,
    ThesisPaperSubmitRequest,
    ThesisSimilarityCheckRequest,
    ClaimAmbassadorTaskRequest,
    SubmitAmbassadorTaskRequest,
    VerifyAmbassadorTaskRequest
)
from backend.app.api.v1.router import (
    analyze_algorithm_complexity,
    simulate_algorithm_trace,
    submit_thesis_paper,
    get_thesis_citation_network,
    check_thesis_similarity,
    match_research_grants,
    list_registered_campuses,
    list_ambassador_tasks,
    claim_ambassador_task,
    submit_ambassador_task_evidence,
    verify_ambassador_task_and_reward,
    get_ambassador_profile
)


class TestPhase34AlgoThesisAndAmbassador(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.algo_service = AlgorithmComplexitySandboxService()
        self.thesis_service = ThesisCitationGraphService()
        self.ambassador_service = CampusAmbassadorSyndicateService()

    # -------------------------------------------------------------------------
    # 1. AlgorithmComplexitySandboxService Tests
    # -------------------------------------------------------------------------

    def test_constant_complexity_o1(self):
        code = "def add(a, b):\n    c = a + b\n    return c"
        res = self.algo_service.analyze_complexity(code)
        self.assertTrue(res["ast_parsed"])
        self.assertEqual(res["detected_loops"], 0)
        self.assertEqual(res["max_loop_nesting"], 0)
        self.assertFalse(res["has_recursion"])
        self.assertEqual(res["time_complexity"], "O(1)")
        self.assertEqual(res["space_complexity"], "O(1)")

    def test_linear_complexity_on(self):
        code = "def find_max(arr):\n    m = arr[0]\n    for x in arr:\n        if x > m:\n            m = x\n    return m"
        res = self.algo_service.analyze_complexity(code)
        self.assertTrue(res["ast_parsed"])
        self.assertEqual(res["detected_loops"], 1)
        self.assertEqual(res["max_loop_nesting"], 1)
        self.assertEqual(res["time_complexity"], "O(N)")
        self.assertEqual(res["space_complexity"], "O(1)")

    def test_quadratic_complexity_on2(self):
        code = "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(n - i - 1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr"
        res = self.algo_service.analyze_complexity(code)
        self.assertEqual(res["detected_loops"], 2)
        self.assertEqual(res["max_loop_nesting"], 2)
        self.assertEqual(res["time_complexity"], "O(N^2)")

    def test_cubic_complexity_on3(self):
        code = "def matrix_mult(A, B, n):\n    C = [[0]*n for _ in range(n)]\n    for i in range(n):\n        for j in range(n):\n            for k in range(n):\n                C[i][j] += A[i][k] * B[k][j]\n    return C"
        res = self.algo_service.analyze_complexity(code)
        self.assertEqual(res["max_loop_nesting"], 3)
        self.assertEqual(res["time_complexity"], "O(N^3)")

    def test_exponential_recursion_o2n(self):
        code = "def fib(n):\n    if n <= 1:\n        return n\n    return fib(n - 1) + fib(n - 2)"
        res = self.algo_service.analyze_complexity(code)
        self.assertTrue(res["has_recursion"])
        self.assertEqual(res["time_complexity"], "O(2^N)")
        self.assertEqual(res["space_complexity"], "O(N)")

    def test_logarithmic_complexity_halving(self):
        code = "def binary_search(arr, x):\n    low = 0\n    high = len(arr) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if arr[mid] == x: return mid\n        elif arr[mid] < x: low = mid + 1\n        else: high = mid - 1\n    return -1"
        res = self.algo_service.analyze_complexity(code)
        self.assertEqual(res["time_complexity"], "O(log N)")

    def test_syntax_error_handled_gracefully(self):
        bad_code = "def invalid_syntax(\n    print('missing paren'"
        res = self.algo_service.analyze_complexity(bad_code)
        self.assertFalse(res["ast_parsed"])
        self.assertEqual(res["time_complexity"], "SYNTAX_ERROR")

    def test_empty_code_raises_error(self):
        with self.assertRaises(ValueError):
            self.algo_service.analyze_complexity("   ")

    def test_excessive_code_length_raises_error(self):
        with self.assertRaises(ValueError):
            self.algo_service.analyze_complexity("x = 1\n" * 5000)

    def test_malicious_code_string_safe(self):
        # Verify that malicious python string containing subprocess/exec is never run
        payload = "__import__('os').system('echo pwned')"
        res = self.algo_service.analyze_complexity(payload)
        self.assertTrue(res["ast_parsed"])
        self.assertEqual(res["time_complexity"], "O(1)")

    def test_algorithm_trace_bubble_sort(self):
        res = self.algo_service.generate_algorithm_trace("BUBBLE_SORT", [4, 2, 7, 1])
        self.assertEqual(res["algorithm"], "BUBBLE_SORT")
        self.assertGreater(res["total_steps"], 2)
        self.assertEqual(res["final_state"], [1, 2, 4, 7])

    def test_algorithm_trace_merge_sort(self):
        res = self.algo_service.generate_algorithm_trace("MERGE_SORT", [6, 1, 8, 3])
        self.assertEqual(res["algorithm"], "MERGE_SORT")
        self.assertEqual(res["final_state"], [1, 3, 6, 8])

    def test_algorithm_trace_quick_sort(self):
        res = self.algo_service.generate_algorithm_trace("QUICK_SORT", [10, 5, 2, 8])
        self.assertEqual(res["algorithm"], "QUICK_SORT")
        self.assertEqual(res["final_state"], [2, 5, 8, 10])

    def test_algorithm_trace_binary_search(self):
        res = self.algo_service.generate_algorithm_trace("BINARY_SEARCH", [1, 3, 5, 7, 9])
        self.assertEqual(res["algorithm"], "BINARY_SEARCH")
        self.assertGreaterEqual(res["total_steps"], 2)

    def test_algorithm_trace_fibonacci_dp(self):
        res = self.algo_service.generate_algorithm_trace("FIBONACCI_DP", [6])
        self.assertEqual(res["algorithm"], "FIBONACCI_DP")
        self.assertEqual(res["final_state"][-1], 8)  # fib(6) = 8

    def test_unsupported_algorithm_raises_error(self):
        with self.assertRaises(ValueError):
            self.algo_service.generate_algorithm_trace("UNKNOWN_ALGO", [1, 2, 3])

    # -------------------------------------------------------------------------
    # 2. ThesisCitationGraphService Tests
    # -------------------------------------------------------------------------

    def test_seed_theses_loaded(self):
        papers = self.thesis_service.list_all_papers()
        self.assertGreaterEqual(len(papers), 4)

    def test_submit_thesis_paper_success(self):
        paper = self.thesis_service.submit_thesis_paper(
            title="Transformer Compression for Edge Devices in Smart Agriculture",
            abstract="We introduce 4-bit integer quantization for agricultural crop disease classification on Raspberry Pi.",
            authors=["Fahim Montasir", "Dr. Sadia Sharmin"],
            institution="BUET",
            department="CSE",
            publication_year=2025,
            keywords=["Edge AI", "Quantization"],
            cited_paper_ids=["THESIS-BUET-2024-01"]
        )
        self.assertTrue(paper["paper_id"].startswith("THESIS-BUET"))
        self.assertIn("@article", paper["bibtex"])
        self.assertEqual(paper["cites"], ["THESIS-BUET-2024-01"])

        # Check citation count increment on target paper
        net = self.thesis_service.get_paper_citation_network("THESIS-BUET-2024-01")
        self.assertIn(paper["paper_id"], net["root_paper"]["cited_by"])

    def test_empty_title_or_abstract_raises_error(self):
        with self.assertRaises(ValueError):
            self.thesis_service.submit_thesis_paper(
                title="",
                abstract="Some abstract",
                authors=["Author"],
                institution="DU",
                department="CSE"
            )

    def test_get_paper_citation_network(self):
        net = self.thesis_service.get_paper_citation_network("THESIS-DU-2023-01")
        self.assertEqual(net["root_paper"]["paper_id"], "THESIS-DU-2023-01")
        self.assertGreater(len(net["network_nodes"]), 1)
        self.assertGreater(len(net["network_edges"]), 0)

    def test_get_nonexistent_paper_citation_network_raises_error(self):
        with self.assertRaises(ValueError):
            self.thesis_service.get_paper_citation_network("INVALID-ID-999")

    def test_check_thesis_similarity_duplicate(self):
        # Use text identical to existing DU thesis title and abstract
        abstract = "Securing Mobile Financial Services via On-Device Behavioral Biometrics. This thesis explores non-intrusive continuous authentication on Android smartphones utilizing keystroke dynamics, touchscreen gyroscope telemetry, and lightweight federated inference."
        res = self.thesis_service.check_thesis_similarity(abstract)
        self.assertGreater(res["highest_similarity"], 80.0)
        self.assertTrue(res["flagged_as_duplicate"])
        self.assertGreater(len(res["matches"]), 0)

    def test_check_thesis_similarity_original(self):
        text = "Quantum electrodynamics under curved spacetime manifolds with topological solitons in graphene lattice."
        res = self.thesis_service.check_thesis_similarity(text)
        self.assertLess(res["highest_similarity"], 10.0)
        self.assertFalse(res["flagged_as_duplicate"])

    def test_short_text_similarity_raises_error(self):
        with self.assertRaises(ValueError):
            self.thesis_service.check_thesis_similarity("Too short")

    def test_match_research_grants(self):
        res = self.thesis_service.match_research_grants("Artificial Intelligence and Deep Tech")
        self.assertGreaterEqual(res["total_matched"], 1)
        self.assertIn("grant_id", res["matched_grants"][0])

    # -------------------------------------------------------------------------
    # 3. CampusAmbassadorSyndicateService Tests
    # -------------------------------------------------------------------------

    def test_list_campuses(self):
        campuses = self.ambassador_service.list_campuses()
        self.assertGreaterEqual(len(campuses), 18)
        buet_found = any(c["campus_id"] == "CAMPUS-BUET" for c in campuses)
        self.assertTrue(buet_found)

    def test_list_tasks_and_filters(self):
        tasks = self.ambassador_service.list_tasks(status="AVAILABLE")
        self.assertGreater(len(tasks), 0)
        for t in tasks:
            self.assertEqual(t["status"], "AVAILABLE")

    def test_claim_task_success(self):
        task = self.ambassador_service.claim_task("TASK-2025-001", "student-202")
        self.assertEqual(task["status"], "CLAIMED")
        self.assertEqual(task["claimed_by"], "student-202")

    def test_claim_already_claimed_task_raises_error(self):
        # Claim once
        self.ambassador_service.claim_task("TASK-2025-002", "student-303")
        # Try claiming again
        with self.assertRaises(ValueError):
            self.ambassador_service.claim_task("TASK-2025-002", "student-404")

    def test_submit_task_evidence_success(self):
        self.ambassador_service.claim_task("TASK-2025-003", "student-505")
        task = self.ambassador_service.submit_task_evidence(
            task_id="TASK-2025-003",
            student_id="student-505",
            evidence_url="https://github.com/agrojatra/stem-workshop",
            impact_report="Conducted peer tutoring sessions for 85 high-school students."
        )
        self.assertEqual(task["status"], "SUBMITTED")
        self.assertEqual(task["evidence_url"], "https://github.com/agrojatra/stem-workshop")

    def test_submit_task_evidence_invalid_url_raises_error(self):
        with self.assertRaises(ValueError):
            self.ambassador_service.submit_task_evidence(
                task_id="TASK-2025-004",
                student_id="student-101",
                evidence_url="file:///etc/passwd",
                impact_report="Detailed report of work."
            )

    def test_verify_and_reward_task_approved(self):
        # Ensure student-101's TASK-2025-004 is submitted
        t = self.ambassador_service._tasks["TASK-2025-004"]
        t["status"] = "SUBMITTED"

        res = self.ambassador_service.verify_and_reward_task(
            task_id="TASK-2025-004",
            verifier_id="faculty-mentor-01",
            approved=True,
            feedback="Exceptional execution and documented student impact."
        )
        self.assertEqual(res["status"], "REWARDED")
        prof = self.ambassador_service.get_ambassador_profile("student-101")
        self.assertGreaterEqual(prof["total_points"], 1700)
        self.assertEqual(prof["tier"], "GOLD_LEAD_FELLOW")
        self.assertTrue(len(prof["digital_badge_signature"]) > 10)

    # -------------------------------------------------------------------------
    # 4. Section 33 REST Routes Tests
    # -------------------------------------------------------------------------

    async def test_route_analyze_algorithm_complexity(self):
        payload = CodeComplexityRequest(code="def simple(): return 42")
        res = await analyze_algorithm_complexity(payload)
        self.assertTrue(res["ast_parsed"])
        self.assertEqual(res["time_complexity"], "O(1)")

    async def test_route_simulate_algorithm_trace(self):
        payload = AlgorithmTraceRequest(algorithm="BUBBLE_SORT", input_data=[3, 1, 2])
        res = await simulate_algorithm_trace(payload)
        self.assertEqual(res["algorithm"], "BUBBLE_SORT")
        self.assertEqual(res["final_state"], [1, 2, 3])

    async def test_route_submit_thesis_and_citations(self):
        payload = ThesisPaperSubmitRequest(
            title="Biometric Keystroke Dynamics on Mobile",
            abstract="Study of typing cadence under adversarial synthetic mimicry.",
            authors=["Samiul Islam"],
            institution="DU",
            department="CSE",
            publication_year=2025,
            cited_paper_ids=["THESIS-DU-2023-01"]
        )
        paper = await submit_thesis_paper(payload)
        self.assertTrue(paper["paper_id"].startswith("THESIS-DU"))

        # Query citations
        net = await get_thesis_citation_network(paper["paper_id"])
        self.assertEqual(net["root_paper"]["paper_id"], paper["paper_id"])

    async def test_route_check_thesis_similarity(self):
        payload = ThesisSimilarityCheckRequest(text_sample="Study of typing cadence under adversarial synthetic mimicry.")
        res = await check_thesis_similarity(payload)
        self.assertIn("originality_score", res)

    async def test_route_match_research_grants(self):
        res = await match_research_grants(field_of_study="Cybersecurity & FinTech")
        self.assertGreaterEqual(res["total_matched"], 1)

    async def test_route_campus_ambassador_workflow(self):
        campuses = await list_registered_campuses()
        self.assertGreaterEqual(campuses["total_campuses"], 18)

        tasks = await list_ambassador_tasks()
        self.assertGreater(len(tasks), 0)

        # Profile retrieval
        prof = await get_ambassador_profile("student-test-999")
        self.assertEqual(prof["student_id"], "student-test-999")
        self.assertEqual(prof["tier"], "BRONZE_AMBASSADOR")


if __name__ == '__main__':
    unittest.main()
