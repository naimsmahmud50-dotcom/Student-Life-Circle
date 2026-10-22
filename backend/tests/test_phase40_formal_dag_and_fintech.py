"""
Unit, Integration, and Security Test Suite for Phase 40:
- Formal Verification & AST Invariant Sandbox
- Decentralized Knowledge Graph IPFS Merkle DAG Engine
- FinTech Quantitative Risk & Black-Scholes Analytics
"""

import unittest
from backend.app.services.formal_verification_service import FormalVerificationZ3SolverService
from backend.app.services.decentralized_knowledge_dag_service import DecentralizedKnowledgeDagService
from backend.app.services.fintech_quant_risk_service import FintechQuantRiskService
from backend.app.schemas.formal_dag_and_fintech_schema import (
    HoareVerificationRequest,
    MutationScoreRequest,
    CreateDagNodeRequest,
    BlackScholesRequest,
    PortfolioVarRequest
)


class TestPhase40FormalDagAndFintech(unittest.TestCase):
    def setUp(self):
        DecentralizedKnowledgeDagService.clear_store()

    # -------------------------------------------------------------------------
    # 1. Formal Verification & AST Sandbox Tests
    # -------------------------------------------------------------------------
    def test_hoare_triple_proven_valid_simple_sum(self):
        """Test verifying valid contract: result = n * 2 where n >= 0 implies result >= 0."""
        code = "result = n * 2"
        res = FormalVerificationZ3SolverService.verify_hoare_triple(
            code_str=code,
            pre_condition="n >= 0",
            post_condition="result >= 0"
        )
        self.assertTrue(res["valid"])
        self.assertEqual(res["verdict"], "PROVEN_VALID")
        self.assertIsNone(res["counterexample"])

    def test_hoare_triple_counterexample_found(self):
        """Test detecting violation when code computes wrong result."""
        code = "result = n - 10"
        res = FormalVerificationZ3SolverService.verify_hoare_triple(
            code_str=code,
            pre_condition="n >= 0",
            post_condition="result >= 0"
        )
        self.assertFalse(res["valid"])
        self.assertEqual(res["verdict"], "COUNTEREXAMPLE_FOUND")
        self.assertIsNotNone(res["counterexample"])

    def test_hoare_triple_syntax_error(self):
        """Test handling malformed Python syntax gracefully."""
        code = "def malformed(::: broken"
        res = FormalVerificationZ3SolverService.verify_hoare_triple(
            code_str=code,
            pre_condition="n >= 0",
            post_condition="result >= 0"
        )
        self.assertFalse(res["valid"])
        self.assertEqual(res["verdict"], "SYNTAX_ERROR")

    def test_hoare_triple_empty_code(self):
        """Test empty code rejection."""
        res = FormalVerificationZ3SolverService.verify_hoare_triple(
            code_str="",
            pre_condition="n >= 0",
            post_condition="result >= 0"
        )
        self.assertFalse(res["valid"])
        self.assertEqual(res["verdict"], "SYNTAX_ERROR")

    def test_hoare_triple_security_violation_import(self):
        """Test security audit: blocking dangerous os/sys/subprocess imports."""
        code = "import os\nresult = 42"
        res = FormalVerificationZ3SolverService.verify_hoare_triple(
            code_str=code,
            pre_condition="n >= 0",
            post_condition="result >= 0"
        )
        self.assertFalse(res["valid"])
        self.assertEqual(res["verdict"], "SAFETY_VIOLATION")
        self.assertIn("os", res["message"])

    def test_hoare_triple_security_violation_dangerous_call(self):
        """Test blocking eval/exec/open calls inside sandbox."""
        code = "eval('1 + 1')\nresult = 2"
        res = FormalVerificationZ3SolverService.verify_hoare_triple(
            code_str=code,
            pre_condition="n >= 0",
            post_condition="result >= 0"
        )
        self.assertFalse(res["valid"])
        self.assertEqual(res["verdict"], "SAFETY_VIOLATION")

    def test_hoare_ranking_function_termination(self):
        """Test termination verification with ranking function variant."""
        code = "result = 0\nfor i in range(n):\n    result += i"
        res = FormalVerificationZ3SolverService.verify_hoare_triple(
            code_str=code,
            pre_condition="n >= 0",
            post_condition="result >= 0",
            ranking_variant="n - i"
        )
        self.assertTrue(res["valid"])
        self.assertTrue(res["termination_proven"])

    def test_mutation_score_high_adequacy(self):
        """Test mutation testing adequacy calculation when killed >= 85%."""
        res = FormalVerificationZ3SolverService.calculate_mutation_score(
            total_mutants=100,
            killed_mutants=92
        )
        self.assertEqual(res["total_mutants"], 100)
        self.assertEqual(res["killed_mutants"], 92)
        self.assertEqual(res["survived_mutants"], 8)
        self.assertEqual(res["mutation_score_pct"], 92.0)
        self.assertEqual(res["adequacy_rating"], "HIGH_ADEQUACY")

    def test_mutation_score_zero_mutants_safe(self):
        """Test mutation score division-by-zero security guard."""
        res = FormalVerificationZ3SolverService.calculate_mutation_score(
            total_mutants=0,
            killed_mutants=0
        )
        self.assertEqual(res["mutation_score_pct"], 0.0)
        self.assertEqual(res["adequacy_rating"], "INSUFFICIENT_MUTANTS")

    def test_mutation_score_clamping(self):
        """Test negative and overflow clamping on mutation inputs."""
        res = FormalVerificationZ3SolverService.calculate_mutation_score(
            total_mutants=50,
            killed_mutants=60  # Cannot exceed total
        )
        self.assertEqual(res["killed_mutants"], 50)
        self.assertEqual(res["mutation_score_pct"], 100.0)

    # -------------------------------------------------------------------------
    # 2. Decentralized Merkle DAG (IPFS) Tests
    # -------------------------------------------------------------------------
    def test_merkle_dag_node_creation_and_cid(self):
        """Test creating an IPFS-style Merkle DAG syllabus node with valid CIDv1."""
        node = DecentralizedKnowledgeDagService.create_dag_node(
            title="Calculus Differential Equations",
            content="# Chapter 7: Second-Order Linear ODEs",
            author="Prof. Rahman (BUET)",
            tags=["calculus", "ode", "stem"]
        )
        self.assertIn("cid", node)
        self.assertTrue(node["cid"].startswith("bafy"))
        self.assertEqual(node["title"], "Calculus Differential Equations")
        self.assertEqual(node["pin_status"], "PINNED_LOCAL")
        self.assertIn("sha256_hash", node)

    def test_merkle_dag_integrity_valid(self):
        """Test cryptographic integrity verification of an uncorrupted node."""
        node = DecentralizedKnowledgeDagService.create_dag_node(
            title="Quantum Mechanics 101",
            content="Schrodinger Wave Equation",
            author="Dr. Fatima"
        )
        verify_res = DecentralizedKnowledgeDagService.verify_node_integrity(node["cid"])
        self.assertTrue(verify_res["verified"])
        self.assertEqual(verify_res["status"], "VALID_IMMUTABLE")

    def test_merkle_dag_tamper_detected(self):
        """Test tamper detection when payload is silently modified in memory."""
        node = DecentralizedKnowledgeDagService.create_dag_node(
            title="Chemistry Organic Synthesis",
            content="Benzene ring reactions",
            author="Dr. Kamal"
        )
        # Maliciously mutate stored content directly
        DecentralizedKnowledgeDagService._dag_store[node["cid"]]["content"] = "Tampered fake notes"
        verify_res = DecentralizedKnowledgeDagService.verify_node_integrity(node["cid"])
        self.assertFalse(verify_res["verified"])
        self.assertEqual(verify_res["status"], "CORRUPTED_TAMPER_DETECTED")

    def test_merkle_dag_self_cycle_prevented(self):
        """Test rejection of self-referential cycle."""
        node1 = DecentralizedKnowledgeDagService.create_dag_node(
            title="Physics Root",
            content="Newtonian Kinematics",
            author="Faculty"
        )
        with self.assertRaises(ValueError):
            DecentralizedKnowledgeDagService.add_parent_link(node1["cid"], node1["cid"])

    def test_merkle_dag_transitive_cycle_prevented(self):
        """Test rejection of transitive cycle (A -> B -> A)."""
        node_a = DecentralizedKnowledgeDagService.create_dag_node("Node A", "Content A", "Author")
        node_b = DecentralizedKnowledgeDagService.create_dag_node("Node B", "Content B", "Author", parent_cids=[node_a["cid"]])
        # Attempting to make Node A a child of Node B creates cycle A -> B -> A
        with self.assertRaises(ValueError):
            DecentralizedKnowledgeDagService.add_parent_link(node_a["cid"], node_b["cid"])

    def test_merkle_dag_global_status(self):
        """Test retrieving DAG store statistics."""
        DecentralizedKnowledgeDagService.create_dag_node("Node A", "Content A", "Author 1")
        DecentralizedKnowledgeDagService.create_dag_node("Node B", "Content B", "Author 2")
        status = DecentralizedKnowledgeDagService.get_dag_status()
        self.assertEqual(status["total_nodes"], 2)
        self.assertGreater(status["total_bytes"], 0)
        self.assertEqual(status["pinned_nodes"], 2)

    # -------------------------------------------------------------------------
    # 3. FinTech Quantitative Risk & Black-Scholes Tests
    # -------------------------------------------------------------------------
    def test_black_scholes_standard_call_and_put(self):
        """Test standard textbook European option pricing: S=100, K=100, T=1, r=0.05, sigma=0.20."""
        res = FintechQuantRiskService.calculate_black_scholes(
            spot_price=100.0,
            strike_price=100.0,
            time_to_maturity=1.0,
            risk_free_rate=0.05,
            volatility=0.20
        )
        # Standard textbook Call is ~10.45, Put is ~5.57
        self.assertAlmostEqual(res["call_price"], 10.45, delta=0.1)
        self.assertAlmostEqual(res["put_price"], 5.57, delta=0.1)
        # Put-Call Parity: C - P = S - K * exp(-r*T) = 100 - 100 * exp(-0.05) = ~4.877
        parity_diff = (res["call_price"] - res["put_price"]) - (100.0 - 100.0 * 0.951229)
        self.assertAlmostEqual(parity_diff, 0.0, delta=0.1)

    def test_black_scholes_zero_and_negative_clamping(self):
        """Test singularity safety guard when zero/negative inputs are provided."""
        res = FintechQuantRiskService.calculate_black_scholes(
            spot_price=-10.0,
            strike_price=0.0,
            time_to_maturity=0.0,
            risk_free_rate=0.0,
            volatility=-0.5
        )
        self.assertGreaterEqual(res["call_price"], 0.0)
        self.assertGreaterEqual(res["put_price"], 0.0)
        self.assertIn("greeks", res)

    def test_black_scholes_greeks_consistency(self):
        """Test Delta is between 0 and 1 for Call, and -1 and 0 for Put."""
        res = FintechQuantRiskService.calculate_black_scholes(
            spot_price=105.0,
            strike_price=100.0,
            time_to_maturity=0.5,
            risk_free_rate=0.04,
            volatility=0.25
        )
        greeks = res["greeks"]
        self.assertGreater(greeks["call_delta"], 0.0)
        self.assertLess(greeks["call_delta"], 1.0)
        self.assertGreater(greeks["put_delta"], -1.0)
        self.assertLess(greeks["put_delta"], 0.0)
        self.assertAlmostEqual(greeks["call_delta"] - greeks["put_delta"], 1.0, places=4)
        self.assertGreater(greeks["gamma"], 0.0)
        self.assertGreater(greeks["vega_per_pct"], 0.0)

    def test_portfolio_var_calculation(self):
        """Test calculating 1-day Parametric VaR at 95% and 99%."""
        res = FintechQuantRiskService.calculate_portfolio_var(
            portfolio_value=100000.0,
            expected_annual_return=0.10,
            annual_volatility=0.15,
            holding_period_days=1,
            risk_free_rate=0.04
        )
        self.assertEqual(res["portfolio_value"], 100000.0)
        self.assertEqual(res["holding_period_days"], 1)
        self.assertGreater(res["var_95_amount"], 0.0)
        self.assertGreater(res["var_99_amount"], res["var_95_amount"])  # 99% VaR strictly > 95% VaR
        # Sharpe ratio = (0.10 - 0.04) / 0.15 = 0.4
        self.assertAlmostEqual(res["annualized_sharpe_ratio"], 0.4, places=2)
        self.assertEqual(res["risk_adjusted_rating"], "ACCEPTABLE")

    def test_portfolio_var_zero_portfolio_safe(self):
        """Test portfolio VaR security guard with zero assets."""
        res = FintechQuantRiskService.calculate_portfolio_var(
            portfolio_value=0.0,
            expected_annual_return=0.0,
            annual_volatility=0.0,
            holding_period_days=1
        )
        self.assertEqual(res["var_95_amount"], 0.0)
        self.assertEqual(res["var_99_amount"], 0.0)


if __name__ == "__main__":
    unittest.main()
