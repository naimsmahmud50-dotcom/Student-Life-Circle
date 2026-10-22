"""
AdaptiveLearningPathService:
Dynamic Remedial Learning Pathway Engine.
Synthesizes personalized micro-curricula sprint maps from student quiz error patterns
and Computerized Adaptive Testing (CAT) diagnostics.
Features:
- Prerequisite Knowledge Graph dependency mapping
- Misconception identification and targeted 3-minute micro-lecture scheduling
- Incremental mastery calculation and readiness scoring
- Thread-safe pathway persistence and step progression
"""

import uuid
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class AdaptiveLearningPathService:
    # Subject Knowledge Dependency Graph (Topic -> Prerequisites)
    CONCEPT_GRAPH = {
        "Higher Mathematics": {
            "chain_rule": {
                "title": "Calculus: Chain Rule & Composite Functions",
                "prerequisite": "Differential Limits & Polynomial Derivatives",
                "micro_lecture_min": 3,
                "drill_count": 2
            },
            "integration_by_parts": {
                "title": "Calculus: Integration by Parts (LIATE Rule)",
                "prerequisite": "Standard Indefinite Integrals & Product Rule",
                "micro_lecture_min": 4,
                "drill_count": 3
            },
            "conic_sections": {
                "title": "Coordinate Geometry: Conic Sections & Eccentricity",
                "prerequisite": "Standard Parabola Equations",
                "micro_lecture_min": 3,
                "drill_count": 2
            }
        },
        "Physics": {
            "rotational_dynamics": {
                "title": "Mechanics: Moment of Inertia & Torque",
                "prerequisite": "Linear Newton's Second Law",
                "micro_lecture_min": 3,
                "drill_count": 2
            },
            "doppler_effect": {
                "title": "Waves: Doppler Effect in Sound",
                "prerequisite": "Harmonic Wave Frequency & Velocity",
                "micro_lecture_min": 3,
                "drill_count": 2
            }
        }
    }

    def __init__(self):
        self._lock = threading.Lock()
        self._pathways: Dict[str, Dict[str, Any]] = {}

    def generate_pathway(
        self,
        student_id: str,
        subject: str,
        weak_topic_ids: List[str],
        target_mastery_pct: float = 90.0
    ) -> Dict[str, Any]:
        with self._lock:
            pathway_id = f"path-{uuid.uuid4().hex[:10]}"
            subject_graph = self.CONCEPT_GRAPH.get(subject, self.CONCEPT_GRAPH["Higher Mathematics"])

            steps = []
            step_order = 1

            for topic_id in weak_topic_ids:
                concept_info = subject_graph.get(topic_id)
                if not concept_info:
                    concept_info = {
                        "title": f"Core Competency: {topic_id.replace('_', ' ').title()}",
                        "prerequisite": "Fundamental Principles",
                        "micro_lecture_min": 3,
                        "drill_count": 2
                    }

                # Step A: Diagnostic Prerequisite Check
                steps.append({
                    "step_id": f"step-{step_order}",
                    "step_order": step_order,
                    "step_type": "DIAGNOSTIC",
                    "title": f"Prerequisite Check: {concept_info['prerequisite']}",
                    "duration_minutes": 2,
                    "resource_url": f"/classroom/diagnostic/{topic_id}",
                    "prerequisite_concept": concept_info["prerequisite"],
                    "status": "PENDING"
                })
                step_order += 1

                # Step B: 3-Minute Focused Micro-Lecture
                steps.append({
                    "step_id": f"step-{step_order}",
                    "step_order": step_order,
                    "step_type": "MICRO_LECTURE",
                    "title": f"Targeted Sprint: {concept_info['title']}",
                    "duration_minutes": concept_info["micro_lecture_min"],
                    "resource_url": f"/classroom/video-sprint/{topic_id}",
                    "prerequisite_concept": concept_info["prerequisite"],
                    "status": "PENDING"
                })
                step_order += 1

                # Step C: Precision Practice Drill
                steps.append({
                    "step_id": f"step-{step_order}",
                    "step_order": step_order,
                    "step_type": "PRACTICE_DRILL",
                    "title": f"Adaptive Drill ({concept_info['drill_count']} Questions)",
                    "duration_minutes": 4,
                    "resource_url": f"/practice/drill/{topic_id}",
                    "prerequisite_concept": concept_info["title"],
                    "status": "PENDING"
                })
                step_order += 1

            # Final Step: Mastery Milestone Challenge
            steps.append({
                "step_id": f"step-{step_order}",
                "step_order": step_order,
                "step_type": "MASTERY_ASSESSMENT",
                "title": f"Syllabus Mastery Milestone Exam: {subject}",
                "duration_minutes": 10,
                "resource_url": f"/assessment/mastery/{subject.lower().replace(' ', '-')}",
                "prerequisite_concept": "All Remedial Sprints",
                "status": "PENDING"
            })

            # Calculate estimated readiness metrics
            current_readiness = max(40.0, 85.0 - (len(weak_topic_ids) * 12.5))
            projected_readiness = min(100.0, target_mastery_pct)

            pathway = {
                "pathway_id": pathway_id,
                "student_id": student_id,
                "subject": subject,
                "current_readiness_pct": round(current_readiness, 1),
                "projected_mastery_pct": round(projected_readiness, 1),
                "steps": steps,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            self._pathways[pathway_id] = pathway
            return pathway

    def get_pathway(self, pathway_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._pathways.get(pathway_id)

    def complete_step(self, pathway_id: str, step_id: str) -> Dict[str, Any]:
        with self._lock:
            if pathway_id not in self._pathways:
                raise ValueError(f"Pathway '{pathway_id}' not found.")
            pathway = self._pathways[pathway_id]
            step_found = False
            completed_count = 0
            for step in pathway["steps"]:
                if step["step_id"] == step_id:
                    step["status"] = "COMPLETED"
                    step_found = True
                if step["status"] == "COMPLETED":
                    completed_count += 1
            if not step_found:
                raise ValueError(f"Step '{step_id}' not found in pathway.")

            # Recalculate current readiness dynamically
            total_steps = len(pathway["steps"])
            progress_ratio = completed_count / total_steps
            delta = pathway["projected_mastery_pct"] - pathway["current_readiness_pct"]
            pathway["current_readiness_pct"] = round(pathway["current_readiness_pct"] + (delta * (1 / total_steps)), 1)
            return pathway

adaptive_learning_path_service = AdaptiveLearningPathService()
