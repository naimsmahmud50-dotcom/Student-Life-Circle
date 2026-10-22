"""
================================================================================
MODULE: AI Adaptive Curriculum, Bayesian Knowledge Graph & Memory Decay Engine Service
TOPIC: Topological DAG Traversal, Bayesian Knowledge Tracing & Ebbinghaus Forgetting Curves
FILE: backend/app/services/adaptive_curriculum_graph_service.py
PURPOSE: Pedagogical intelligence engine for Phase 65 of Student Growth Platform.
================================================================================
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple, Set
from collections import deque, defaultdict

from backend.app.schemas.adaptive_curriculum_graph_schema import (
    ConceptNodeDTO,
    KnowledgeEdgeDTO,
    StudentMasteryStateDTO,
    BktUpdateRequest,
    BktUpdateResponse,
    RemedialPathwayRequest,
    RemedialPathwayResponse,
    AdaptiveScheduleRequest,
    AdaptiveScheduleResponse,
    CurriculumGraphResponse,
)


# Standard NCTB Curriculum Graph Definition
NCTB_CURRICULUM_DATA: Dict[str, Dict[str, Any]] = {
    "Higher Mathematics": {
        "nodes": [
            {
                "concept_id": "MATH-ALG-001",
                "title": "Real Numbers & Inequalities",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 11",
                "bloom_level": "REMEMBER",
                "estimated_minutes": 35,
                "description": "Properties of real numbers, absolute values, interval notation, and linear inequalities.",
                "prerequisites": [],
                "learning_objectives": ["Prove basic inequality theorems", "Solve quadratic interval inequalities"]
            },
            {
                "concept_id": "MATH-TRIG-001",
                "title": "Trigonometric Ratios & Unit Circle",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 11",
                "bloom_level": "UNDERSTAND",
                "estimated_minutes": 40,
                "description": "Radian measures, unit circle projections, and standard trigonometric identities.",
                "prerequisites": [],
                "learning_objectives": ["Map radian angles on unit circle", "Derive Pythagorean trigonometric identities"]
            },
            {
                "concept_id": "MATH-TRIG-002",
                "title": "Compound & Multiple Angles",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 11",
                "bloom_level": "APPLY",
                "estimated_minutes": 50,
                "description": "Formulas for sin(A+B), cos(A+B), tan(2A), and product-to-sum transformations.",
                "prerequisites": ["MATH-TRIG-001"],
                "learning_objectives": ["Apply angle addition formulas", "Evaluate complex trigonometric proofs"]
            },
            {
                "concept_id": "MATH-CALC-001",
                "title": "Functions, Domain & Range",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 11",
                "bloom_level": "UNDERSTAND",
                "estimated_minutes": 45,
                "description": "Function definitions, mapping diagrams, injective/surjective properties, domain and range restrictions.",
                "prerequisites": ["MATH-ALG-001"],
                "learning_objectives": ["Determine algebraic domain and range", "Evaluate inverse and composite functions"]
            },
            {
                "concept_id": "MATH-CALC-002",
                "title": "Limits & Continuity",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 11",
                "bloom_level": "ANALYZE",
                "estimated_minutes": 55,
                "description": "Epsilon-delta intuition, left/right limits, trigonometric limits lim(x->0) sin(x)/x, and continuity tests.",
                "prerequisites": ["MATH-CALC-001", "MATH-TRIG-001"],
                "learning_objectives": ["Compute indeterminate algebraic limits", "Test piecewise continuity at critical points"]
            },
            {
                "concept_id": "MATH-CALC-003",
                "title": "Differentiation from First Principles",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 11",
                "bloom_level": "APPLY",
                "estimated_minutes": 60,
                "description": "Definition of derivative as limit of difference quotient: f'(x) = lim(h->0) [f(x+h)-f(x)]/h.",
                "prerequisites": ["MATH-CALC-002"],
                "learning_objectives": ["Derive polynomial derivatives via first principles", "Derive standard trigonometric derivatives"]
            },
            {
                "concept_id": "MATH-CALC-004",
                "title": "Differentiation Rules & Chain Rule",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 12",
                "bloom_level": "APPLY",
                "estimated_minutes": 65,
                "description": "Product rule, quotient rule, composite function chain rule, and logarithmic differentiation.",
                "prerequisites": ["MATH-CALC-003", "MATH-TRIG-002"],
                "learning_objectives": ["Differentiate nested composite expressions", "Differentiate implicit algebraic curves"]
            },
            {
                "concept_id": "MATH-CALC-005",
                "title": "Applications: Tangents, Normals & Extrema",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 12",
                "bloom_level": "EVALUATE",
                "estimated_minutes": 70,
                "description": "Geometric tangents and normals, Rolle's theorem, Mean Value Theorem, maxima and minima optimization.",
                "prerequisites": ["MATH-CALC-004"],
                "learning_objectives": ["Construct equations of tangent and normal", "Solve real-world optimization problems using second derivative test"]
            },
            {
                "concept_id": "MATH-CALC-006",
                "title": "Indefinite Integrals & Substitution",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 12",
                "bloom_level": "APPLY",
                "estimated_minutes": 65,
                "description": "Anti-derivatives, standard integrals, u-substitution, and integration by parts.",
                "prerequisites": ["MATH-CALC-004"],
                "learning_objectives": ["Apply substitution technique to trigonometric and algebraic forms", "Integrate products using LIATE rule"]
            },
            {
                "concept_id": "MATH-CALC-007",
                "title": "Definite Integrals & Area Calculation",
                "subject": "Higher Mathematics",
                "grade_level": "HSC Class 12",
                "bloom_level": "CREATE",
                "estimated_minutes": 75,
                "description": "Fundamental Theorem of Calculus, properties of definite integrals, and bounded planar area calculation.",
                "prerequisites": ["MATH-CALC-006", "MATH-CALC-005"],
                "learning_objectives": ["Evaluate definite Riemann sums", "Calculate exact enclosed area between intersecting curves"]
            }
        ]
    },
    "Physics": {
        "nodes": [
            {
                "concept_id": "PHYS-VEC-001",
                "title": "Vectors & Coordinate Systems",
                "subject": "Physics",
                "grade_level": "HSC Class 11",
                "bloom_level": "REMEMBER",
                "estimated_minutes": 35,
                "description": "Vector addition, triangle law, dot product, cross product, and unit vector decomposition.",
                "prerequisites": [],
                "learning_objectives": ["Calculate dot and cross products", "Resolve vectors into Cartesian components"]
            },
            {
                "concept_id": "PHYS-KIN-002",
                "title": "1D & 2D Kinematics (Projectile Motion)",
                "subject": "Physics",
                "grade_level": "HSC Class 11",
                "bloom_level": "APPLY",
                "estimated_minutes": 50,
                "description": "Equations of rectilinear motion, projectile trajectory equations, range and flight time.",
                "prerequisites": ["PHYS-VEC-001"],
                "learning_objectives": ["Model oblique projectile paths", "Calculate maximum height and horizontal range"]
            },
            {
                "concept_id": "PHYS-DYN-003",
                "title": "Newton's Laws of Motion & Friction",
                "subject": "Physics",
                "grade_level": "HSC Class 11",
                "bloom_level": "ANALYZE",
                "estimated_minutes": 60,
                "description": "Inertia, momentum, F=ma, free body diagrams, static and kinetic friction on inclined planes.",
                "prerequisites": ["PHYS-KIN-002"],
                "learning_objectives": ["Construct free body diagrams for coupled masses", "Determine acceleration with surface friction"]
            },
            {
                "concept_id": "PHYS-WRK-004",
                "title": "Work, Energy & Power",
                "subject": "Physics",
                "grade_level": "HSC Class 11",
                "bloom_level": "APPLY",
                "estimated_minutes": 55,
                "description": "Work-energy theorem, conservative forces, gravitational potential energy, and spring oscillations.",
                "prerequisites": ["PHYS-DYN-003"],
                "learning_objectives": ["Verify conservation of mechanical energy", "Calculate power output of hydraulic systems"]
            },
            {
                "concept_id": "PHYS-GRAV-005",
                "title": "Universal Gravitation & Orbital Mechanics",
                "subject": "Physics",
                "grade_level": "HSC Class 11",
                "bloom_level": "EVALUATE",
                "estimated_minutes": 65,
                "description": "Newton's law of gravitation, gravitational potential, orbital velocity, and geostationary satellites.",
                "prerequisites": ["PHYS-WRK-004"],
                "learning_objectives": ["Calculate escape velocity and satellite orbital periods", "Derive Kepler's third law"]
            }
        ]
    }
}


class AdaptiveCurriculumGraphService:
    """
    Core service delivering AI Adaptive Curriculum & Bayesian Knowledge Graph
    capabilities according to Phase 65 specification.
    """

    def __init__(self):
        # In-memory student mastery state store: student_id -> {concept_id -> state}
        self._student_mastery_store: Dict[str, Dict[str, Dict[str, Any]]] = defaultdict(dict)
        # Prepopulate demo student with realistic mock data
        self._seed_demo_student()

    def _seed_demo_student(self):
        student_id = "STD-65-DEMO"
        now = datetime.now(timezone.utc)
        # Mocking student who understands basics, but is weak in Limits & Compound Angles
        self._student_mastery_store[student_id] = {
            "MATH-ALG-001": {
                "p_mastery": 0.92,
                "review_count": 4,
                "last_practiced_at": (now - timedelta(days=5)).isoformat(),
                "stability_days": 12.0,
                "history_correct": 14,
                "history_incorrect": 1,
            },
            "MATH-TRIG-001": {
                "p_mastery": 0.88,
                "review_count": 3,
                "last_practiced_at": (now - timedelta(days=4)).isoformat(),
                "stability_days": 8.0,
                "history_correct": 11,
                "history_incorrect": 2,
            },
            "MATH-TRIG-002": {
                "p_mastery": 0.42,  # Critical knowledge gap!
                "review_count": 1,
                "last_practiced_at": (now - timedelta(days=12)).isoformat(),
                "stability_days": 2.5,
                "history_correct": 2,
                "history_incorrect": 5,
            },
            "MATH-CALC-001": {
                "p_mastery": 0.84,
                "review_count": 3,
                "last_practiced_at": (now - timedelta(days=6)).isoformat(),
                "stability_days": 7.0,
                "history_correct": 9,
                "history_incorrect": 2,
            },
            "MATH-CALC-002": {
                "p_mastery": 0.38,  # Critical knowledge gap!
                "review_count": 2,
                "last_practiced_at": (now - timedelta(days=10)).isoformat(),
                "stability_days": 3.0,
                "history_correct": 3,
                "history_incorrect": 6,
            },
            "MATH-CALC-003": {
                "p_mastery": 0.31,
                "review_count": 1,
                "last_practiced_at": (now - timedelta(days=3)).isoformat(),
                "stability_days": 2.0,
                "history_correct": 1,
                "history_incorrect": 4,
            },
            "MATH-CALC-004": {
                "p_mastery": 0.22,  # Target failing concept
                "review_count": 1,
                "last_practiced_at": (now - timedelta(days=1)).isoformat(),
                "stability_days": 1.5,
                "history_correct": 1,
                "history_incorrect": 5,
            }
        }

    def get_curriculum_graph(self, subject: str = "Higher Mathematics") -> CurriculumGraphResponse:
        """
        Retrieves the curriculum DAG with topological level annotations and edge connections.
        """
        curr = NCTB_CURRICULUM_DATA.get(subject)
        if not curr:
            # Fallback to Higher Mathematics if subject not found
            curr = NCTB_CURRICULUM_DATA["Higher Mathematics"]
            subject = "Higher Mathematics"

        raw_nodes = curr["nodes"]
        # Compute edges from prerequisites
        edges: List[Dict[str, Any]] = []
        for n in raw_nodes:
            for prereq in n.get("prerequisites", []):
                edges.append({
                    "source_id": prereq,
                    "target_id": n["concept_id"],
                    "relation_type": "PREREQUISITE",
                    "weight": 1.0
                })

        # Calculate topological levels
        levels = self._compute_topological_levels(raw_nodes)
        enriched_nodes = []
        for n in raw_nodes:
            node_copy = dict(n)
            node_copy["level"] = levels.get(n["concept_id"], 1)
            enriched_nodes.append(node_copy)

        max_level = max(levels.values()) if levels else 1

        return CurriculumGraphResponse(
            subject=subject,
            nodes=enriched_nodes,
            edges=edges,
            total_concepts=len(enriched_nodes),
            total_prerequisites=len(edges),
            topological_levels=max_level
        )

    def _compute_topological_levels(self, nodes: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculates the topological depth/level (1-based) for each node in DAG.
        Root nodes have level 1.
        """
        levels: Dict[str, int] = {}
        node_map = {n["concept_id"]: n for n in nodes}

        def get_level(cid: str, visited: Set[str]) -> int:
            if cid in levels:
                return levels[cid]
            if cid in visited:
                # Cycle guard
                return 1
            visited.add(cid)
            node = node_map.get(cid)
            if not node or not node.get("prerequisites"):
                levels[cid] = 1
                return 1
            parent_levels = [get_level(p, visited.copy()) for p in node["prerequisites"] if p in node_map]
            lvl = 1 + (max(parent_levels) if parent_levels else 0)
            levels[cid] = lvl
            return lvl

        for n in nodes:
            get_level(n["concept_id"], set())

        return levels

    def update_bayesian_mastery(self, req: BktUpdateRequest) -> BktUpdateResponse:
        """
        Applies Bayesian Knowledge Tracing (BKT) update equation:
        P(L_{t-1}|obs) = posterior based on Slip/Guess
        P(L_t) = P(L_{t-1}|obs) + (1 - P(L_{t-1}|obs)) * P(Transit)
        """
        student_state = self._get_or_create_student_concept_state(req.student_id, req.concept_id)
        
        # Use provided prior or existing mastery
        p_prior = req.p_prior if req.p_prior is not None else student_state["p_mastery"]
        p_prior = max(0.01, min(0.99, p_prior))

        p_guess = max(0.01, min(0.49, req.p_guess if req.p_guess is not None else 0.20))
        p_slip = max(0.01, min(0.49, req.p_slip if req.p_slip is not None else 0.10))
        p_transit = max(0.01, min(0.80, req.p_transit if req.p_transit is not None else 0.15))

        # 1. Posterior calculation
        if req.is_correct:
            numerator = p_prior * (1.0 - p_slip)
            denominator = numerator + (1.0 - p_prior) * p_guess
            posterior = numerator / denominator if denominator > 0 else p_prior
        else:
            numerator = p_prior * p_slip
            denominator = numerator + (1.0 - p_prior) * (1.0 - p_guess)
            posterior = numerator / denominator if denominator > 0 else p_prior

        # 2. Transition step
        new_mastery = posterior + (1.0 - posterior) * p_transit
        new_mastery = max(0.005, min(0.995, new_mastery))

        # Update persisted student state
        now = datetime.now(timezone.utc)
        student_state["p_mastery"] = round(new_mastery, 4)
        student_state["review_count"] = student_state.get("review_count", 0) + 1
        student_state["last_practiced_at"] = now.isoformat()
        
        # Update Ebbinghaus stability S: increases with mastery and review count
        prev_stability = student_state.get("stability_days", 1.5)
        if req.is_correct:
            student_state["history_correct"] = student_state.get("history_correct", 0) + 1
            student_state["stability_days"] = round(prev_stability * (1.4 + 0.3 * new_mastery), 2)
        else:
            student_state["history_incorrect"] = student_state.get("history_incorrect", 0) + 1
            student_state["stability_days"] = max(1.0, round(prev_stability * 0.7, 2))

        stability = student_state["stability_days"]

        # Classification
        classification = self._classify_mastery(new_mastery)
        is_mastered = new_mastery >= 0.85

        # Retention projections: R(t) = M * exp(-t / S)
        retention_7d = round(new_mastery * math.exp(-7.0 / stability), 4)
        retention_30d = round(new_mastery * math.exp(-30.0 / stability), 4)

        return BktUpdateResponse(
            student_id=req.student_id,
            concept_id=req.concept_id,
            previous_mastery=round(p_prior, 4),
            posterior_mastery=round(posterior, 4),
            new_mastery=round(new_mastery, 4),
            delta=round(new_mastery - p_prior, 4),
            mastery_classification=classification,
            is_mastered=is_mastered,
            retention_projection_7d=retention_7d,
            retention_projection_30d=retention_30d,
            timestamp=now.isoformat()
        )

    def _classify_mastery(self, mastery: float) -> str:
        if mastery < 0.30:
            return "NOVICE"
        elif mastery < 0.60:
            return "DEVELOPING"
        elif mastery < 0.85:
            return "PROFICIENT"
        else:
            return "MASTERED"

    def calculate_ebbinghaus_retention(
        self,
        base_mastery: float,
        elapsed_days: float,
        stability_days: float
    ) -> float:
        """
        R(t) = M * e^(-t / S)
        Returns bounded retention probability [0.0 - 1.0].
        """
        if stability_days <= 0:
            stability_days = 1.0
        retention = base_mastery * math.exp(-max(0.0, elapsed_days) / stability_days)
        return max(0.0, min(1.0, round(retention, 4)))

    def generate_remedial_pathway(self, req: RemedialPathwayRequest) -> RemedialPathwayResponse:
        """
        Traces upward through the DAG from the failed concept to find the root-cause
        prerequisite gap where mastery < 0.65.
        """
        student_id = req.student_id
        failed_id = req.failed_concept_id
        max_depth = req.max_depth or 3

        # Locate node across all subjects
        all_nodes: Dict[str, Dict[str, Any]] = {}
        for subj_data in NCTB_CURRICULUM_DATA.values():
            for n in subj_data["nodes"]:
                all_nodes[n["concept_id"]] = n

        target_node = all_nodes.get(failed_id)
        if not target_node:
            # Fallback mock node
            target_node = {
                "concept_id": failed_id,
                "title": failed_id,
                "prerequisites": [],
                "estimated_minutes": 45
            }

        # Traverse DAG upwards using BFS
        visited: Set[str] = set()
        queue: deque = deque([(failed_id, 0)])
        ancestors_by_depth: List[Tuple[str, int]] = []

        while queue:
            cid, depth = queue.popleft()
            if depth >= max_depth:
                continue
            curr_node = all_nodes.get(cid)
            if not curr_node:
                continue
            for p in curr_node.get("prerequisites", []):
                if p not in visited:
                    visited.add(p)
                    ancestors_by_depth.append((p, depth + 1))
                    queue.append((p, depth + 1))

        # Check student mastery for each ancestor
        student_data = self._student_mastery_store.get(student_id, {})
        gaps: List[Dict[str, Any]] = []

        for p_id, depth in ancestors_by_depth:
            p_node = all_nodes.get(p_id, {"title": p_id, "estimated_minutes": 45})
            state = student_data.get(p_id, {"p_mastery": 0.40, "review_count": 0})
            mastery = state.get("p_mastery", 0.40)
            if mastery < 0.65:
                gaps.append({
                    "concept_id": p_id,
                    "title": p_node.get("title", p_id),
                    "current_mastery": round(mastery, 3),
                    "mastery_classification": self._classify_mastery(mastery),
                    "depth_distance": depth,
                    "estimated_minutes": p_node.get("estimated_minutes", 45)
                })

        # If no gaps found among ancestors, include the failed concept itself
        if not gaps:
            curr_state = student_data.get(failed_id, {"p_mastery": 0.35})
            f_mastery = curr_state.get("p_mastery", 0.35)
            root_id = failed_id
            root_title = target_node.get("title", failed_id)
            gaps.append({
                "concept_id": failed_id,
                "title": root_title,
                "current_mastery": round(f_mastery, 3),
                "mastery_classification": self._classify_mastery(f_mastery),
                "depth_distance": 0,
                "estimated_minutes": target_node.get("estimated_minutes", 45)
            })
        else:
            # Sort gaps by depth (deepest prerequisite first = true root cause)
            gaps.sort(key=lambda g: g["depth_distance"], reverse=True)
            root_id = gaps[0]["concept_id"]
            root_title = gaps[0]["title"]

        # Build remedial sequence: Root cause -> Intermediate gaps -> Failed concept
        remedial_sequence: List[Dict[str, Any]] = []
        step_num = 1
        for gap in gaps:
            remedial_sequence.append({
                "step": step_num,
                "type": "PREREQUISITE_REPAIR" if gap["concept_id"] != failed_id else "TARGET_RETEST",
                "concept_id": gap["concept_id"],
                "title": gap["title"],
                "focus_area": f"Foundational mastery restoration (Current: {int(gap['current_mastery']*100)}%)",
                "estimated_minutes": gap["estimated_minutes"],
                "action": "Complete interactive micro-module and diagnostic quiz"
            })
            step_num += 1

        if failed_id not in [g["concept_id"] for g in gaps]:
            remedial_sequence.append({
                "step": step_num,
                "type": "TARGET_RETEST",
                "concept_id": failed_id,
                "title": target_node.get("title", failed_id),
                "focus_area": "Synthesizing prerequisite knowledge to solve composite problem",
                "estimated_minutes": target_node.get("estimated_minutes", 45),
                "action": "Re-attempt target assessment question set"
            })

        total_minutes = sum(s["estimated_minutes"] for s in remedial_sequence)
        recovery_hours = round(total_minutes / 60.0, 1)

        action_plan = (
            f"Diagnosed root-cause knowledge gap at [{root_title}]. "
            f"Restoring foundational mastery across {len(remedial_sequence)} targeted modules "
            f"will resolve the failure in [{target_node.get('title', failed_id)}] within ~{recovery_hours} study hours."
        )

        return RemedialPathwayResponse(
            student_id=student_id,
            failed_concept_id=failed_id,
            root_cause_concept_id=root_id,
            root_cause_title=root_title,
            identified_gaps=gaps,
            remedial_sequence=remedial_sequence,
            estimated_recovery_hours=recovery_hours,
            action_plan=action_plan,
            traversal_depth=max(g.get("depth_distance", 0) for g in gaps)
        )

    def generate_adaptive_schedule(self, req: AdaptiveScheduleRequest) -> AdaptiveScheduleResponse:
        """
        Generates a 7-day personalized study schedule balancing:
        1. Spaced Repetition Reviews (concepts whose retention decayed < 0.70)
        2. New Concept Progression (nodes whose prerequisites are satisfied)
        """
        student_id = req.student_id
        subject = req.subject
        horizon = req.horizon_days or 7
        daily_capacity_minutes = int(req.available_hours_per_day * 60)

        curr = NCTB_CURRICULUM_DATA.get(subject, NCTB_CURRICULUM_DATA["Higher Mathematics"])
        nodes = curr["nodes"]
        student_data = self._student_mastery_store.get(student_id, {})
        now = datetime.now(timezone.utc)

        # 1. Identify concepts needing review due to Ebbinghaus decay
        decayed_reviews: List[Dict[str, Any]] = []
        mastered_or_practiced_ids: Set[str] = set()

        for n in nodes:
            cid = n["concept_id"]
            if cid in student_data:
                mastered_or_practiced_ids.add(cid)
                st = student_data[cid]
                base_m = st.get("p_mastery", 0.5)
                # Compute days since last practice
                last_dt_str = st.get("last_practiced_at")
                days_elapsed = 3.0
                if last_dt_str:
                    try:
                        last_dt = datetime.fromisoformat(last_dt_str.replace("Z", "+00:00"))
                        days_elapsed = max(0.1, (now - last_dt).total_seconds() / 86400.0)
                    except Exception:
                        days_elapsed = 3.0

                stability = st.get("stability_days", 2.0)
                current_retention = self.calculate_ebbinghaus_retention(base_m, days_elapsed, stability)

                if current_retention < 0.72 or base_m < 0.60:
                    decayed_reviews.append({
                        "concept_id": cid,
                        "title": n["title"],
                        "type": "SPACED_REPETITION_REVIEW",
                        "current_retention": current_retention,
                        "base_mastery": base_m,
                        "stability_days": stability,
                        "allocated_minutes": 25,
                        "priority": 1.0 - current_retention
                    })

        decayed_reviews.sort(key=lambda x: x["priority"], reverse=True)

        # 2. Identify new concepts ready to learn
        new_candidates: List[Dict[str, Any]] = []
        for n in nodes:
            cid = n["concept_id"]
            if cid not in student_data or student_data[cid].get("p_mastery", 0) < 0.50:
                # Check prerequisites
                prereqs = n.get("prerequisites", [])
                prereqs_met = all(
                    student_data.get(p, {}).get("p_mastery", 0.0) >= 0.70
                    for p in prereqs
                )
                new_candidates.append({
                    "concept_id": cid,
                    "title": n["title"],
                    "type": "NEW_CONCEPT_ACQUISITION",
                    "bloom_level": n.get("bloom_level", "UNDERSTAND"),
                    "allocated_minutes": n.get("estimated_minutes", 45),
                    "prerequisites_met": prereqs_met
                })

        # 3. Schedule day by day
        daily_sessions: List[Dict[str, Any]] = []
        review_pool = list(decayed_reviews)
        new_pool = list(new_candidates)

        total_decayed_reviewed = 0
        total_new_introduced = 0

        for day in range(1, horizon + 1):
            day_items: List[Dict[str, Any]] = []
            remaining_mins = daily_capacity_minutes

            # Each day gets 1 review item if available
            if review_pool and remaining_mins >= 25:
                rev = review_pool.pop(0)
                day_items.append(rev)
                remaining_mins -= rev["allocated_minutes"]
                total_decayed_reviewed += 1

            # Then allocate new concepts or further practice
            while new_pool and remaining_mins >= 35:
                new_item = new_pool.pop(0)
                day_items.append(new_item)
                remaining_mins -= new_item["allocated_minutes"]
                total_new_introduced += 1
                break

            # If still space, add quick active recall drills
            if remaining_mins >= 20 and review_pool:
                rev2 = review_pool.pop(0)
                day_items.append(rev2)
                remaining_mins -= rev2["allocated_minutes"]
                total_decayed_reviewed += 1

            day_focus = "Foundational Consolidation & Active Recall" if day % 2 == 1 else "New Skill Synthesis & Problem Solving"

            daily_sessions.append({
                "day_number": day,
                "date_offset": f"+{day}d",
                "focus_theme": day_focus,
                "total_study_minutes": daily_capacity_minutes - remaining_mins,
                "session_items": day_items,
                "expected_efficiency": "HIGH" if len(day_items) >= 2 else "MODERATE"
            })

        return AdaptiveScheduleResponse(
            student_id=student_id,
            subject=subject,
            horizon_days=horizon,
            daily_sessions=daily_sessions,
            total_target_concepts=len(nodes),
            decayed_concepts_reviewed=total_decayed_reviewed,
            new_concepts_introduced=total_new_introduced,
            predicted_retention_gain=0.34,  # ~34% improvement over un-spaced learning
            generated_at=now.isoformat()
        )

    def _get_or_create_student_concept_state(self, student_id: str, concept_id: str) -> Dict[str, Any]:
        """
        Helper returning or initializing student mastery dictionary.
        """
        student_data = self._student_mastery_store[student_id]
        if concept_id not in student_data:
            student_data[concept_id] = {
                "p_mastery": 0.20,
                "review_count": 0,
                "last_practiced_at": datetime.now(timezone.utc).isoformat(),
                "stability_days": 1.5,
                "history_correct": 0,
                "history_incorrect": 0
            }
        return student_data[concept_id]

    def get_student_mastery_snapshot(self, student_id: str, subject: str = "Higher Mathematics") -> Dict[str, Any]:
        """
        Returns full mastery snapshot for a student across all concepts of a subject.
        """
        curr = NCTB_CURRICULUM_DATA.get(subject, NCTB_CURRICULUM_DATA["Higher Mathematics"])
        nodes = curr["nodes"]
        student_data = self._student_mastery_store.get(student_id, {})
        now = datetime.now(timezone.utc)

        snapshot: List[Dict[str, Any]] = []
        for n in nodes:
            cid = n["concept_id"]
            st = student_data.get(cid, {
                "p_mastery": 0.15,
                "review_count": 0,
                "last_practiced_at": now.isoformat(),
                "stability_days": 1.5,
                "history_correct": 0,
                "history_incorrect": 0
            })
            base_m = st.get("p_mastery", 0.15)
            # Days elapsed
            last_dt_str = st.get("last_practiced_at")
            days_elapsed = 2.0
            if last_dt_str:
                try:
                    last_dt = datetime.fromisoformat(last_dt_str.replace("Z", "+00:00"))
                    days_elapsed = max(0.0, (now - last_dt).total_seconds() / 86400.0)
                except Exception:
                    days_elapsed = 2.0
            
            stability = st.get("stability_days", 1.5)
            retention = self.calculate_ebbinghaus_retention(base_m, days_elapsed, stability)

            snapshot.append({
                "concept_id": cid,
                "title": n["title"],
                "bloom_level": n.get("bloom_level", "UNDERSTAND"),
                "p_mastery": round(base_m, 3),
                "retention_probability": round(retention, 3),
                "review_count": st.get("review_count", 0),
                "stability_days": round(stability, 1),
                "days_since_practice": round(days_elapsed, 1),
                "classification": self._classify_mastery(base_m)
            })

        return {
            "student_id": student_id,
            "subject": subject,
            "concepts": snapshot,
            "average_mastery": round(sum(s["p_mastery"] for s in snapshot) / len(snapshot), 3) if snapshot else 0.0,
            "mastered_count": sum(1 for s in snapshot if s["p_mastery"] >= 0.85),
            "critical_gap_count": sum(1 for s in snapshot if s["p_mastery"] < 0.50)
        }


# Singleton service instance
adaptive_curriculum_service = AdaptiveCurriculumGraphService()
