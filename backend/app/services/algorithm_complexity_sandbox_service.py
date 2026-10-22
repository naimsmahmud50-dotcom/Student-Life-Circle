"""
Algorithm Complexity Sandbox & AST Code Analyzer Service
Enterprise-grade static code analysis using Python's standard `ast` module.
Zero unsafe execution (`eval`/`exec`). Generates step-by-step algorithm trace frames.
"""

import ast
import time
from typing import Dict, List, Any, Optional, Tuple


class ComplexityASTVisitor(ast.NodeVisitor):
    """Safely traverses AST nodes to compute loop depths, recursion, and allocations."""
    def __init__(self):
        self.loop_count = 0
        self.max_nesting_depth = 0
        self.current_loop_depth = 0
        self.function_defs = {}
        self.current_function = None
        self.has_recursion = False
        self.recursive_branch_factor = 0
        self.allocates_dynamic_array = False
        self.allocates_2d_matrix = False

    def visit_FunctionDef(self, node: ast.FunctionDef):
        old_fn = self.current_function
        self.current_function = node.name
        self.function_defs[node.name] = {"calls": 0, "node": node}
        self.generic_visit(node)
        self.current_function = old_fn

    def visit_For(self, node: ast.For):
        self.loop_count += 1
        self.current_loop_depth += 1
        if self.current_loop_depth > self.max_nesting_depth:
            self.max_nesting_depth = self.current_loop_depth
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_While(self, node: ast.While):
        self.loop_count += 1
        self.current_loop_depth += 1
        if self.current_loop_depth > self.max_nesting_depth:
            self.max_nesting_depth = self.current_loop_depth
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            callee = node.func.id
            if self.current_function and callee == self.current_function:
                self.has_recursion = True
                self.function_defs[self.current_function]["calls"] += 1
                self.recursive_branch_factor = max(self.recursive_branch_factor, self.function_defs[self.current_function]["calls"])
        self.generic_visit(node)

    def visit_ListComp(self, node: ast.ListComp):
        self.allocates_dynamic_array = True
        # Check for nested list comprehension e.g. [[0 for _ in range(n)] for _ in range(m)]
        for generator in node.generators:
            if isinstance(generator.iter, ast.Call):
                self.allocates_dynamic_array = True
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp):
        # Detect [0] * n patterns
        if isinstance(node.op, ast.Mult):
            if isinstance(node.left, ast.List) or isinstance(node.right, ast.List):
                self.allocates_dynamic_array = True
        self.generic_visit(node)


class AlgorithmComplexitySandboxService:
    """Enterprise AST static complexity analyzer and visual trace generator."""

    def analyze_complexity(self, code: str, language: str = "python", function_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Parses code using AST and derives asymptotic Big-O time and space bounds.
        Guarantees 0 execution risks.
        """
        code_sanitized = code.strip()
        if not code_sanitized:
            raise ValueError("Input code cannot be empty.")
        if len(code_sanitized) > 10000:
            raise ValueError("Code length exceeds maximum allowed limit of 10,000 characters.")

        try:
            tree = ast.parse(code_sanitized)
        except SyntaxError as e:
            return {
                "code_length": len(code_sanitized),
                "ast_parsed": False,
                "detected_loops": 0,
                "max_loop_nesting": 0,
                "has_recursion": False,
                "time_complexity": "SYNTAX_ERROR",
                "space_complexity": "SYNTAX_ERROR",
                "asymptotic_bound_explanation": f"Failed to parse Abstract Syntax Tree: {e.msg} at line {e.lineno}",
                "recommendations": ["Ensure valid Python 3 syntax before running complexity analysis."]
            }

        visitor = ComplexityASTVisitor()
        visitor.visit(tree)

        # Derive Time Complexity
        time_comp = "O(1)"
        space_comp = "O(1)"
        explanation_parts = []
        recommendations = []

        if visitor.has_recursion:
            if visitor.recursive_branch_factor >= 2:
                time_comp = "O(2^N)"
                explanation_parts.append(f"Detected exponential branching recursion ({visitor.recursive_branch_factor} recursive calls per stack frame).")
                recommendations.append("Consider memoization or bottom-up dynamic programming to reduce O(2^N) to O(N).")
            else:
                if visitor.max_nesting_depth >= 1:
                    time_comp = "O(N log N)"
                    explanation_parts.append("Detected divide-and-conquer recurrence with linear loop partitioning.")
                else:
                    time_comp = "O(N)"
                    explanation_parts.append("Detected linear recursion with depth proportional to N.")
            space_comp = "O(N)"  # Call stack depth
        else:
            if visitor.max_nesting_depth == 0:
                time_comp = "O(1)"
                explanation_parts.append("No loops or recursive calls detected; instructions execute in constant time.")
            elif visitor.max_nesting_depth == 1:
                # Check for log N loop patterns (e.g., while i > 0: i //= 2 or binary search)
                code_lower = code_sanitized.lower()
                if "//= 2" in code_lower or "/= 2" in code_lower or ">> 1" in code_lower or "binary_search" in code_lower:
                    time_comp = "O(log N)"
                    explanation_parts.append("Detected logarithmic halving loop pattern.")
                else:
                    time_comp = "O(N)"
                    explanation_parts.append("Detected single-level loop iteration over input bounds.")
            elif visitor.max_nesting_depth == 2:
                time_comp = "O(N^2)"
                explanation_parts.append("Detected quadratic nested loop iteration (depth = 2).")
                recommendations.append("Nested loops scale quadratically; consider hash maps, sorting, or two-pointer technique.")
            elif visitor.max_nesting_depth == 3:
                time_comp = "O(N^3)"
                explanation_parts.append("Detected cubic nested loop iteration (depth = 3).")
                recommendations.append("Cubic complexity is inefficient for N > 500; optimize matrix operations or reduce loop dimensions.")
            else:
                time_comp = f"O(N^{visitor.max_nesting_depth})"
                explanation_parts.append(f"Detected deep nested loop iteration with nesting depth {visitor.max_nesting_depth}.")
                recommendations.append("Extreme nesting depth found. Refactor into modular helper routines.")

        if visitor.allocates_dynamic_array or "[]" in code_sanitized or "list(" in code_sanitized:
            if visitor.max_nesting_depth >= 2 and ("[[" in code_sanitized or "matrix" in code_sanitized.lower()):
                space_comp = "O(N^2)"
                explanation_parts.append("Allocates 2D auxiliary data structure proportional to N x N.")
            else:
                space_comp = "O(N)"
                explanation_parts.append("Allocates linear auxiliary storage or maintains dynamic array buffer.")
        else:
            if not visitor.has_recursion:
                space_comp = "O(1)"
                explanation_parts.append("Operates in-place with constant O(1) auxiliary variables.")

        if not recommendations:
            recommendations.append("Algorithm adheres to optimal asymptotic bounds for its computational pattern.")

        return {
            "code_length": len(code_sanitized),
            "ast_parsed": True,
            "detected_loops": visitor.loop_count,
            "max_loop_nesting": visitor.max_nesting_depth,
            "has_recursion": visitor.has_recursion,
            "time_complexity": time_comp,
            "space_complexity": space_comp,
            "asymptotic_bound_explanation": " ".join(explanation_parts),
            "recommendations": recommendations
        }

    def generate_algorithm_trace(self, algorithm: str, input_data: List[int]) -> Dict[str, Any]:
        """
        Simulates canonical algorithm execution and records discrete step snapshots.
        """
        algo_key = algorithm.upper().strip()
        data = list(input_data)[:20]  # Cap input data to 20 elements for performance and clarity
        if not data:
            data = [5, 2, 9, 1, 5, 6]

        start_time = time.perf_counter()
        steps: List[Dict[str, Any]] = []

        if algo_key == "BUBBLE_SORT":
            steps = self._trace_bubble_sort(data)
        elif algo_key == "MERGE_SORT":
            steps = self._trace_merge_sort(data)
        elif algo_key == "QUICK_SORT":
            steps = self._trace_quick_sort(data)
        elif algo_key == "BINARY_SEARCH":
            steps = self._trace_binary_search(data)
        elif algo_key == "FIBONACCI_DP":
            steps = self._trace_fibonacci_dp(data[0] if data else 7)
        else:
            raise ValueError(f"Unsupported algorithm '{algorithm}'. Supported: BUBBLE_SORT, MERGE_SORT, QUICK_SORT, BINARY_SEARCH, FIBONACCI_DP")

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        final_state = steps[-1]["current_state"] if steps else data

        return {
            "algorithm": algo_key,
            "input_data": data,
            "total_steps": len(steps),
            "steps": steps,
            "final_state": final_state,
            "time_taken_ms": round(elapsed_ms, 3)
        }

    def _trace_bubble_sort(self, data: List[int]) -> List[Dict[str, Any]]:
        arr = list(data)
        n = len(arr)
        steps = [{
            "step_number": 1,
            "action": "INITIALIZE",
            "current_state": list(arr),
            "highlighted_indices": [],
            "description": f"Starting Bubble Sort on array of size {n}."
        }]

        step_num = 2
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                desc = f"Comparing arr[{j}]={arr[j]} and arr[{j+1}]={arr[j+1]}."
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    desc += f" Swapped because {arr[j+1]} < {arr[j]}."
                steps.append({
                    "step_number": step_num,
                    "action": "COMPARE_AND_SWAP" if swapped else "COMPARE",
                    "current_state": list(arr),
                    "highlighted_indices": [j, j + 1],
                    "description": desc
                })
                step_num += 1
            if not swapped:
                steps.append({
                    "step_number": step_num,
                    "action": "EARLY_TERMINATION",
                    "current_state": list(arr),
                    "highlighted_indices": [],
                    "description": "No swaps occurred in this pass. Array is fully sorted."
                })
                break

        return steps

    def _trace_merge_sort(self, data: List[int]) -> List[Dict[str, Any]]:
        arr = list(data)
        steps = [{
            "step_number": 1,
            "action": "INITIALIZE",
            "current_state": list(arr),
            "highlighted_indices": [],
            "description": f"Starting Divide-and-Conquer Merge Sort on {arr}."
        }]

        step_counter = [2]

        def merge_sort_recursive(sub: List[int], offset: int) -> List[int]:
            if len(sub) <= 1:
                return sub
            mid = len(sub) // 2
            left = merge_sort_recursive(sub[:mid], offset)
            right = merge_sort_recursive(sub[mid:], offset + mid)

            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            merged.extend(left[i:])
            merged.extend(right[j:])

            # Update master view
            arr[offset:offset + len(merged)] = merged
            steps.append({
                "step_number": step_counter[0],
                "action": "MERGE_SUBARRAYS",
                "current_state": list(arr),
                "highlighted_indices": list(range(offset, offset + len(merged))),
                "description": f"Merged sub-arrays into sorted segment: {merged} at indices [{offset}:{offset+len(merged)-1}]."
            })
            step_counter[0] += 1
            return merged

        merge_sort_recursive(arr, 0)
        return steps

    def _trace_quick_sort(self, data: List[int]) -> List[Dict[str, Any]]:
        arr = list(data)
        steps = [{
            "step_number": 1,
            "action": "INITIALIZE",
            "current_state": list(arr),
            "highlighted_indices": [],
            "description": f"Starting QuickSort with Lomuto partitioning on {arr}."
        }]

        step_counter = [2]

        def quick_sort_recursive(low: int, high: int):
            if low < high:
                pivot = arr[high]
                i = low - 1
                for j in range(low, high):
                    if arr[j] <= pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                arr[i + 1], arr[high] = arr[high], arr[i + 1]
                p_idx = i + 1

                steps.append({
                    "step_number": step_counter[0],
                    "action": "PARTITION_PIVOT",
                    "current_state": list(arr),
                    "highlighted_indices": [p_idx],
                    "description": f"Pivot {pivot} partitioned into correct position index {p_idx}."
                })
                step_counter[0] += 1

                quick_sort_recursive(low, p_idx - 1)
                quick_sort_recursive(p_idx + 1, high)

        quick_sort_recursive(0, len(arr) - 1)
        return steps

    def _trace_binary_search(self, data: List[int]) -> List[Dict[str, Any]]:
        sorted_arr = sorted(list(data))
        target = sorted_arr[len(sorted_arr) // 2]  # Search for middle element by default
        steps = [{
            "step_number": 1,
            "action": "INITIALIZE",
            "current_state": list(sorted_arr),
            "highlighted_indices": [],
            "description": f"Initialized Binary Search on sorted array for target {target}."
        }]

        low, high = 0, len(sorted_arr) - 1
        step_num = 2
        while low <= high:
            mid = (low + high) // 2
            mid_val = sorted_arr[mid]
            steps.append({
                "step_number": step_num,
                "action": "EVALUATE_MID",
                "current_state": list(sorted_arr),
                "highlighted_indices": [low, mid, high],
                "description": f"Low={low}, High={high}, Mid={mid} (val={mid_val}). Target is {target}."
            })
            step_num += 1

            if mid_val == target:
                steps.append({
                    "step_number": step_num,
                    "action": "TARGET_FOUND",
                    "current_state": list(sorted_arr),
                    "highlighted_indices": [mid],
                    "description": f"Target element {target} located at index {mid}."
                })
                break
            elif mid_val < target:
                low = mid + 1
            else:
                high = mid - 1

        return steps

    def _trace_fibonacci_dp(self, n: int) -> List[Dict[str, Any]]:
        target_n = max(2, min(int(n), 12))
        dp = [0] * (target_n + 1)
        dp[0] = 0
        dp[1] = 1

        steps = [
            {
                "step_number": 1,
                "action": "BASE_CASES",
                "current_state": list(dp),
                "highlighted_indices": [0, 1],
                "description": f"Initialized DP table with base cases: dp[0]=0, dp[1]=1."
            }
        ]

        for i in range(2, target_n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
            steps.append({
                "step_number": i,
                "action": "COMPUTE_STATE",
                "current_state": list(dp),
                "highlighted_indices": [i - 2, i - 1, i],
                "description": f"dp[{i}] = dp[{i-1}] ({dp[i-1]}) + dp[{i-2}] ({dp[i-2]}) = {dp[i]}."
            })

        return steps


# Export singleton instance
algorithm_complexity_sandbox_service = AlgorithmComplexitySandboxService()
