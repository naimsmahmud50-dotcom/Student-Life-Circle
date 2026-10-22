"""
========================================================================================
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Curriculum Knowledge Graph & Dynamic Remedial Navigator Service
TOPIC:     Phase 118 Curriculum Knowledge Graph & Dynamic Remedial Navigator
FILE:      backend/app/services/curriculum_knowledge_graph_service.py
PHASE:     Phase 118 - Curriculum Knowledge Graph & Dynamic Remedial Navigator
PURPOSE:   Constructs Directed Acyclic Graph (DAG) of NCTB curriculum topics, enforces
           strict cycle-free topological traversal, identifies prerequisite gaps
           from student mastery records, and generates 3-step dynamic remedial pathways.
STANDARDS: UI/UX Pro Max, NCTB Curriculum Standards, Pedagogical Gap Recovery, Strict Zero-Emoji
========================================================================================
"""

from typing import Any, Dict, List, Optional, Set, Tuple


class KnowledgeGraphException(Exception):
    """Base exception for curriculum knowledge graph errors."""
    pass


class TopicNotFoundException(KnowledgeGraphException):
    """Raised when a topic ID is not found in the knowledge graph."""
    pass


class CycleDetectedException(KnowledgeGraphException):
    """Raised when an edge creates a cyclic dependency in the curriculum DAG."""
    pass


class CurriculumKnowledgeGraphService:
    """
    Service managing curriculum topics as a Directed Acyclic Graph (DAG),
    recursive prerequisite gap analysis, and 3-step dynamic remedial pathway synthesis.
    """

    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._init_seed_graph()

    def _init_seed_graph(self) -> None:
        """
        Seeds canonical NCTB curriculum topics spanning Class 6 to HSC and University Admission.
        """
        seed_topics = [
            # --- Mathematics & Higher Mathematics Stream ---
            {
                "topic_id": "math-cl6-fractions",
                "title_bn": "ভগ্নাংশ ও মৌলিক পাটিগণিত",
                "title_en": "Fractions and Elementary Arithmetic",
                "subject": "সাধারণ গণিত",
                "class_grade": 6,
                "domain": "পাটিগণিত",
                "prerequisites": [],
                "core_formulas": ["\\frac{a}{b} \\pm \\frac{c}{d} = \\frac{ad \\pm bc}{bd}"],
                "recommended_minutes": 30,
                "x": 80,
                "y": 100,
            },
            {
                "topic_id": "math-cl8-algebraic-identities",
                "title_bn": "বীজগণিতীয় সূত্রাবলী ও বর্গ-ঘন নির্ণয়",
                "title_en": "Algebraic Formulae and Identities",
                "subject": "সাধারণ গণিত",
                "class_grade": 8,
                "domain": "বীজগণিত",
                "prerequisites": ["math-cl6-fractions"],
                "core_formulas": [
                    "(a+b)^2 = a^2 + 2ab + b^2",
                    "(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3"
                ],
                "recommended_minutes": 45,
                "x": 240,
                "y": 100,
            },
            {
                "topic_id": "math-cl9-trigonometric-ratios",
                "title_bn": "ত্রিকোণমিতিক অনুপাত ও অভেদাবলী",
                "title_en": "Trigonometric Ratios and Basic Identities",
                "subject": "উচ্চতর গণিত",
                "class_grade": 9,
                "domain": "ত্রিকোণমিতি",
                "prerequisites": ["math-cl8-algebraic-identities"],
                "core_formulas": [
                    "\\sin^2\\theta + \\cos^2\\theta = 1",
                    "\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta}"
                ],
                "recommended_minutes": 60,
                "x": 420,
                "y": 80,
            },
            {
                "topic_id": "math-cl10-coordinate-geometry",
                "title_bn": "স্থানাঙ্ক জ্যামিতি ও সরলরেখার ঢাল",
                "title_en": "Coordinate Geometry and Slope of Lines",
                "subject": "উচ্চতর গণিত",
                "class_grade": 10,
                "domain": "জ্যামিতি",
                "prerequisites": ["math-cl8-algebraic-identities"],
                "core_formulas": [
                    "m = \\frac{y_2 - y_1}{x_2 - x_1}",
                    "y - y_1 = m(x - x_1)"
                ],
                "recommended_minutes": 60,
                "x": 420,
                "y": 180,
            },
            {
                "topic_id": "math-hsc-functions-limits",
                "title_bn": "ফাংশন ও সীমার প্রাথমিক ধারণা",
                "title_en": "Functions and Intuition of Limits",
                "subject": "উচ্চতর গণিত ১ম পত্র",
                "class_grade": 11,
                "domain": "ক্যালকুলাস",
                "prerequisites": [
                    "math-cl9-trigonometric-ratios",
                    "math-cl10-coordinate-geometry"
                ],
                "core_formulas": [
                    "\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1",
                    "\\lim_{x \\to 0} \\frac{e^x - 1}{x} = 1"
                ],
                "recommended_minutes": 75,
                "x": 620,
                "y": 130,
            },
            {
                "topic_id": "math-hsc-differentiation",
                "title_bn": "অন্তরীকরণ ও তাৎক্ষণিক পরিবর্তনের হার",
                "title_en": "Differentiation and Instantaneous Rates",
                "subject": "উচ্চতর গণিত ১ম পত্র",
                "class_grade": 11,
                "domain": "ক্যালকুলাস",
                "prerequisites": ["math-hsc-functions-limits"],
                "core_formulas": [
                    "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
                    "\\frac{d}{dx}[u \\cdot v] = u\\frac{dv}{dx} + v\\frac{du}{dx}"
                ],
                "recommended_minutes": 90,
                "x": 820,
                "y": 130,
            },
            {
                "topic_id": "math-hsc-integration",
                "title_bn": "সমাকলন ও আবদ্ধ ক্ষেত্রের ক্ষেত্রফল",
                "title_en": "Integral Calculus and Area Under Curves",
                "subject": "উচ্চতর গণিত ১ম পত্র",
                "class_grade": 12,
                "domain": "ক্যালকুলাস",
                "prerequisites": ["math-hsc-differentiation"],
                "core_formulas": [
                    "\\int x^n dx = \\frac{x^{n+1}}{n+1} + C",
                    "A = \\int_a^b f(x) dx"
                ],
                "recommended_minutes": 90,
                "x": 1020,
                "y": 130,
            },

            # --- Physics Stream ---
            {
                "topic_id": "phys-cl9-kinematics-motion",
                "title_bn": "গতি ও একমাত্রিক গতির সমীকরণ",
                "title_en": "Kinematics and 1D Equations of Motion",
                "subject": "পদার্থবিজ্ঞান",
                "class_grade": 9,
                "domain": "বলবিদ্যা",
                "prerequisites": ["math-cl8-algebraic-identities"],
                "core_formulas": [
                    "v = u + at",
                    "s = ut + \\frac{1}{2}at^2",
                    "v^2 = u^2 + 2as"
                ],
                "recommended_minutes": 60,
                "x": 420,
                "y": 300,
            },
            {
                "topic_id": "phys-cl9-newton-laws",
                "title_bn": "বলের ধারণা ও নিউটনের গতিসূত্র",
                "title_en": "Force and Newton's Laws of Motion",
                "subject": "পদার্থবিজ্ঞান",
                "class_grade": 9,
                "domain": "বলবিদ্যা",
                "prerequisites": ["phys-cl9-kinematics-motion"],
                "core_formulas": [
                    "F = ma",
                    "p = mv"
                ],
                "recommended_minutes": 60,
                "x": 620,
                "y": 300,
            },
            {
                "topic_id": "phys-hsc-vectors-motion",
                "title_bn": "ভেক্টর রাশির যোজন ও দ্বিমাত্রিক গতি (প্রাস)",
                "title_en": "Vectors and Projectile Motion",
                "subject": "পদার্থবিজ্ঞান ১ম পত্র",
                "class_grade": 11,
                "domain": "বলবিদ্যা",
                "prerequisites": [
                    "math-cl9-trigonometric-ratios",
                    "phys-cl9-kinematics-motion"
                ],
                "core_formulas": [
                    "R = \\sqrt{P^2 + Q^2 + 2PQ\\cos\\alpha}",
                    "H = \\frac{v_0^2 \\sin^2\\theta}{2g}"
                ],
                "recommended_minutes": 75,
                "x": 620,
                "y": 420,
            },
            {
                "topic_id": "phys-hsc-newtonian-mechanics",
                "title_bn": "নিউটনীয় বলবিদ্যা ও কৌণিক ভরবেগ",
                "title_en": "Newtonian Mechanics and Angular Momentum",
                "subject": "পদার্থবিজ্ঞান ১ম পত্র",
                "class_grade": 11,
                "domain": "বলবিদ্যা",
                "prerequisites": [
                    "phys-cl9-newton-laws",
                    "phys-hsc-vectors-motion",
                    "math-hsc-differentiation"
                ],
                "core_formulas": [
                    "\\tau = I\\alpha",
                    "L = I\\omega",
                    "F = \\frac{dp}{dt}"
                ],
                "recommended_minutes": 90,
                "x": 860,
                "y": 350,
            },

            # --- Chemistry Stream ---
            {
                "topic_id": "chem-cl9-atomic-structure",
                "title_bn": "পরমাণুর গঠন ও ইলেকট্রন বিন্যাস",
                "title_en": "Atomic Structure and Electron Configuration",
                "subject": "রসায়ন",
                "class_grade": 9,
                "domain": "পদার্থের গঠন",
                "prerequisites": [],
                "core_formulas": ["2n^2"],
                "recommended_minutes": 50,
                "x": 420,
                "y": 550,
            },
            {
                "topic_id": "chem-hsc-periodic-trends",
                "title_bn": "পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন",
                "title_en": "Periodic Properties and Chemical Bonding",
                "subject": "রসায়ন ১ম পত্র",
                "class_grade": 11,
                "domain": "মৌলের পর্যায়বৃত্ত ধর্ম",
                "prerequisites": ["chem-cl9-atomic-structure"],
                "core_formulas": ["\\Delta H = \\Sigma D(\\text{reactant}) - \\Sigma D(\\text{product})"],
                "recommended_minutes": 75,
                "x": 680,
                "y": 550,
            },
        ]

        for topic in seed_topics:
            self._nodes[topic["topic_id"]] = topic

        # Validate that the initial seed graph is strictly cycle-free
        self.validate_dag()

    def add_topic(
        self,
        topic_id: str,
        title_bn: str,
        title_en: str,
        subject: str,
        class_grade: int,
        domain: str,
        prerequisites: List[str],
        core_formulas: Optional[List[str]] = None,
        recommended_minutes: int = 45,
        x: int = 100,
        y: int = 100,
    ) -> Dict[str, Any]:
        """
        Adds or updates a topic in the curriculum knowledge graph.
        Enforces DAG cycle prevention.
        """
        # Ensure all referenced prerequisites exist
        for prereq_id in prerequisites:
            if prereq_id not in self._nodes:
                raise TopicNotFoundException(f"Prerequisite topic '{prereq_id}' does not exist.")

        node = {
            "topic_id": topic_id,
            "title_bn": title_bn,
            "title_en": title_en,
            "subject": subject,
            "class_grade": class_grade,
            "domain": domain,
            "prerequisites": list(set(prerequisites)),
            "core_formulas": core_formulas or [],
            "recommended_minutes": recommended_minutes,
            "x": x,
            "y": y,
        }

        # Tentatively add and check for cycles
        old_node = self._nodes.get(topic_id)
        self._nodes[topic_id] = node

        try:
            self.validate_dag()
        except CycleDetectedException:
            # Rollback
            if old_node:
                self._nodes[topic_id] = old_node
            else:
                del self._nodes[topic_id]
            raise

        return node

    def get_topic(self, topic_id: str) -> Dict[str, Any]:
        """Fetches topic node by ID."""
        if topic_id not in self._nodes:
            raise TopicNotFoundException(f"Curriculum topic '{topic_id}' not found.")
        return self._nodes[topic_id]

    def validate_dag(self) -> None:
        """
        Validates that the curriculum knowledge graph contains no cycles.
        Uses 3-color DFS marking:
        0 = UNVISITED, 1 = VISITING (currently in recursion stack), 2 = VISITED.
        """
        state: Dict[str, int] = {node_id: 0 for node_id in self._nodes}

        def dfs(node_id: str, path: List[str]) -> None:
            state[node_id] = 1
            path.append(node_id)

            node = self._nodes[node_id]
            for prereq_id in node.get("prerequisites", []):
                if prereq_id in self._nodes:
                    if state[prereq_id] == 1:
                        cycle_path = " -> ".join(path + [prereq_id])
                        raise CycleDetectedException(f"Curriculum DAG cycle detected: {cycle_path}")
                    if state[prereq_id] == 0:
                        dfs(prereq_id, path)

            path.pop()
            state[node_id] = 2

        for node_id in self._nodes:
            if state[node_id] == 0:
                dfs(node_id, [])

    def get_prerequisites(
        self,
        topic_id: str,
        recursive: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Returns prerequisite topics for a given topic in topological order
        (foundational dependencies appear before higher-level topics).
        """
        target = self.get_topic(topic_id)
        if not recursive:
            return [self.get_topic(pid) for pid in target.get("prerequisites", [])]

        visited: Set[str] = set()
        topo_order: List[str] = []

        def dfs(curr_id: str):
            visited.add(curr_id)
            node = self._nodes[curr_id]
            for pid in node.get("prerequisites", []):
                if pid not in visited and pid in self._nodes:
                    dfs(pid)
            if curr_id != topic_id:
                topo_order.append(curr_id)

        dfs(topic_id)
        return [self._nodes[pid] for pid in topo_order]

    def identify_prerequisite_gaps(
        self,
        topic_id: str,
        student_mastery_map: Optional[Dict[str, float]] = None,
        threshold: float = 0.70,
    ) -> List[Dict[str, Any]]:
        """
        Scans all recursive prerequisites of topic_id.
        Flags any prerequisite whose student mastery is strictly below the threshold.
        """
        mastery = student_mastery_map or {}
        prereqs = self.get_prerequisites(topic_id, recursive=True)

        gaps = []
        for p in prereqs:
            pid = p["topic_id"]
            current_score = mastery.get(pid, 0.0)
            if current_score < threshold:
                gaps.append({
                    "topic_id": pid,
                    "title_bn": p["title_bn"],
                    "title_en": p["title_en"],
                    "subject": p["subject"],
                    "class_grade": p["class_grade"],
                    "current_mastery": round(current_score, 2),
                    "required_mastery": threshold,
                    "mastery_gap": round(threshold - current_score, 2),
                    "core_formulas": p.get("core_formulas", []),
                })
        return gaps

    def generate_remedial_pathway(
        self,
        topic_id: str,
        student_mastery_map: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Generates a personalized 3-step remedial pathway for a student struggling with topic_id.
        Step 1: Quick Concept Refresher (5 mins)
        Step 2: Guided Worked Example (5 mins)
        Step 3: Mastery Diagnostic Drill (5 mins)
        """
        target = self.get_topic(topic_id)
        gaps = self.identify_prerequisite_gaps(topic_id, student_mastery_map)

        # Focus foundational gap: earliest root gap or immediate prerequisite
        primary_gap = gaps[0] if gaps else None

        refresher_content_bn = (
            f"‘{target['title_bn']}’ বুঝতে হলে আগে "
            + (f"‘{primary_gap['title_bn']}’ (শ্রেণি {primary_gap['class_grade']}) " if primary_gap else "প্রাথমিক মৌলিক সূত্রাবলী ")
            + f"পুনর্মূল্যায়ন করা আবশ্যক। মূল ধারণাটি হলো পরিবর্তন বা সম্পর্কের বিশ্লেষণ।"
        )

        canonical_formula = target["core_formulas"][0] if target["core_formulas"] else "E = mc^2"
        gap_formula = primary_gap["core_formulas"][0] if primary_gap and primary_gap["core_formulas"] else None

        steps = [
            {
                "step_number": 1,
                "step_name_bn": "সংক্ষিপ্ত মৌলিক ধারণা পুনশ্চরণ (Concept Refresher)",
                "duration_minutes": 5,
                "pedagogy_focus": "পূর্বশর্ত ও মূল ধারণার সংযোগ",
                "summary_bn": refresher_content_bn,
                "formula_highlight": gap_formula or canonical_formula,
            },
            {
                "step_number": 2,
                "step_name_bn": "ধাপে ধাপে নির্দেশিত সমাধান (Guided Worked Example)",
                "duration_minutes": 5,
                "pedagogy_focus": "বাস্তব সমস্যার ধাপে ধাপে গাণিতিক প্রয়োগ",
                "problem_bn": f"একটি আদর্শ ক্ষেত্রে {target['title_bn']} সমীকরণের প্রয়োগ করে অজ্ঞাত রাশির মান নির্ণয় করো।",
                "formula_breakdown": canonical_formula,
                "solution_steps": [
                    "১. প্রদত্ত উপাত্তসমূহ চিহ্নিত করে আদর্শ এককে রূপান্তর করা।",
                    "২. সংশ্লিষ্ট মৌলিক সমীকরণ নির্বাচন করা।",
                    "৩. বীজগণিতীয় প্রতিস্থাপন ও নির্ভুল মান গণনা করা।",
                ],
            },
            {
                "step_number": 3,
                "step_name_bn": "দক্ষতা যাচাই ড্রিল (Mastery Diagnostic Drill)",
                "duration_minutes": 5,
                "pedagogy_focus": "৩টি দ্রুত নির্ণায়ক প্রশ্নের মাধ্যমে দক্ষতা নিশ্চিতকরণ",
                "drill_questions_count": 3,
                "success_criterion": "৮০% বা তদূর্ধ্ব সঠিক উত্তর পরবর্তী মূল পাঠে ফিরে যাওয়ার সুযোগ দেবে।",
            },
        ]

        return {
            "target_topic_id": topic_id,
            "target_title_bn": target["title_bn"],
            "subject": target["subject"],
            "class_grade": target["class_grade"],
            "total_duration_minutes": 15,
            "detected_gaps_count": len(gaps),
            "primary_gap": primary_gap,
            "all_gaps": gaps,
            "steps": steps,
        }

    def get_graph_snapshot(
        self,
        subject: Optional[str] = None,
        class_grade: Optional[int] = None,
        student_mastery_map: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Returns topic nodes with coordinate positioning and prerequisite edges
        for interactive SVG atlas rendering.
        """
        mastery = student_mastery_map or {}
        nodes = []
        edges = []

        filtered_ids: Set[str] = set()

        for tid, node in self._nodes.items():
            if subject and node["subject"] != subject:
                continue
            if class_grade and node["class_grade"] != class_grade:
                continue

            filtered_ids.add(tid)
            score = mastery.get(tid, 0.5)

            # Categorize mastery band
            if score >= 0.80:
                mastery_band = "MASTERED"
            elif score >= 0.50:
                mastery_band = "IN_PROGRESS"
            else:
                mastery_band = "GAP"

            nodes.append({
                "topic_id": tid,
                "title_bn": node["title_bn"],
                "title_en": node["title_en"],
                "subject": node["subject"],
                "class_grade": node["class_grade"],
                "domain": node["domain"],
                "core_formulas": node["core_formulas"],
                "mastery_score": round(score * 100, 1),
                "mastery_band": mastery_band,
                "x": node["x"],
                "y": node["y"],
            })

        for tid in filtered_ids:
            node = self._nodes[tid]
            for pid in node.get("prerequisites", []):
                if pid in filtered_ids:
                    edges.append({
                        "source": pid,
                        "target": tid,
                    })

        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "nodes": nodes,
            "edges": edges,
        }


# Global singleton instance
curriculum_knowledge_graph_service = CurriculumKnowledgeGraphService()
