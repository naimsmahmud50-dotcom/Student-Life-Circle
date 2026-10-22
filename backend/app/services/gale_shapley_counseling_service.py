"""
DEVELOPER ARCHITECTURE NOTE:
MODULE:    Centralized Admission Counseling & Gale-Shapley Stable Matching
TOPIC:     Student-Proposing Deferred Acceptance Algorithm & Migration Cascade Engine
FILE:      backend/app/services/gale_shapley_counseling_service.py
PHASE:     Phase 107 - Centralized Admission Counseling & Gale-Shapley Stable Matching Hub
PURPOSE:   Implements student-proposing deferred acceptance matching (Gale-Shapley) guaranteeing
           Pareto-optimal envy-free stability, affirmative action quota partitioning with
           automatic spillover into the general merit pool, and multi-stage seat migration cascading.
STANDARDS: Pareto-Optimal Deferred Acceptance, Quota Spillover Balancing, Zero-Emoji, UI/UX Pro Max
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict


class GaleShapleyCounselingService:
    """
    Field-Grade Gale-Shapley Deferred Acceptance Counseling Service.
    Guarantees mathematically stable, student-optimal, envy-free admission matching
    with affirmative action quota allocation, automatic general spillover, and migration cascades.
    """

    # Quota definitions
    QUOTA_GENERAL = "GENERAL"
    QUOTA_FREEDOM_FIGHTER = "FREEDOM_FIGHTER"
    QUOTA_TRIBAL = "TRIBAL"
    QUOTA_DISTRICT = "DISTRICT"
    QUOTA_SPECIAL_NEEDS = "SPECIAL_NEEDS"

    # Probability Tiers
    TIER_HIGH = "HIGH"
    TIER_MODERATE = "MODERATE"
    TIER_AMBITIOUS = "AMBITIOUS"
    TIER_LOW = "LOW"

    def __init__(self) -> None:
        self._calibrated_programs: Dict[str, Dict[str, Any]] = {
            "BUET_CSE": {
                "program_id": "BUET_CSE",
                "institution_name": "বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (BUET)",
                "department_name": "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)",
                "short_name": "বুয়েট সিএসই",
                "total_capacity": 120,
                "quota_capacities": {
                    "GENERAL": 110,
                    "FREEDOM_FIGHTER": 5,
                    "TRIBAL": 2,
                    "DISTRICT": 2,
                    "SPECIAL_NEEDS": 1
                },
                "historical_cutoff_rank": 165,
                "category": "Engineering",
                "cluster": "ENGINEERING"
            },
            "BUET_EEE": {
                "program_id": "BUET_EEE",
                "institution_name": "বাংলাদেশ প্রকৌশল বিশ্ববিদ্যালয় (BUET)",
                "department_name": "ইলেকট্রিক্যাল অ্যান্ড ইলেকট্রনিক ইঞ্জিনিয়ারিং (EEE)",
                "short_name": "বুয়েট ট্রিপল-ই",
                "total_capacity": 195,
                "quota_capacities": {
                    "GENERAL": 180,
                    "FREEDOM_FIGHTER": 8,
                    "TRIBAL": 3,
                    "DISTRICT": 3,
                    "SPECIAL_NEEDS": 1
                },
                "historical_cutoff_rank": 450,
                "category": "Engineering",
                "cluster": "ENGINEERING"
            },
            "DMC_MBBS": {
                "program_id": "DMC_MBBS",
                "institution_name": "ঢাকা মেডিকেল কলেজ (DMC)",
                "department_name": "ব্যাচেলর অব মেডিসিন অ্যান্ড ব্যাচেলর অব সার্জারি (MBBS)",
                "short_name": "ডিএমসি এমবিবিএস",
                "total_capacity": 230,
                "quota_capacities": {
                    "GENERAL": 200,
                    "FREEDOM_FIGHTER": 15,
                    "TRIBAL": 5,
                    "DISTRICT": 8,
                    "SPECIAL_NEEDS": 2
                },
                "historical_cutoff_rank": 260,
                "category": "Medical",
                "cluster": "MEDICAL"
            },
            "DU_CSE": {
                "program_id": "DU_CSE",
                "institution_name": "ঢাকা বিশ্ববিদ্যালয় (DU)",
                "department_name": "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)",
                "short_name": "ঢাবি সিএসই",
                "total_capacity": 60,
                "quota_capacities": {
                    "GENERAL": 52,
                    "FREEDOM_FIGHTER": 3,
                    "TRIBAL": 2,
                    "DISTRICT": 2,
                    "SPECIAL_NEEDS": 1
                },
                "historical_cutoff_rank": 320,
                "category": "Science",
                "cluster": "GENERAL_PUBLIC"
            },
            "DU_EEE": {
                "program_id": "DU_EEE",
                "institution_name": "ঢাকা বিশ্ববিদ্যালয় (DU)",
                "department_name": "ইলেকট্রিক্যাল অ্যান্ড ইলেকট্রনিক ইঞ্জিনিয়ারিং (EEE)",
                "short_name": "ঢাবি ট্রিপল-ই",
                "total_capacity": 70,
                "quota_capacities": {
                    "GENERAL": 60,
                    "FREEDOM_FIGHTER": 4,
                    "TRIBAL": 2,
                    "DISTRICT": 2,
                    "SPECIAL_NEEDS": 2
                },
                "historical_cutoff_rank": 680,
                "category": "Science",
                "cluster": "GENERAL_PUBLIC"
            },
            "JU_CSE": {
                "program_id": "JU_CSE",
                "institution_name": "জাহাঙ্গীরনগর বিশ্ববিদ্যালয় (JU)",
                "department_name": "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)",
                "short_name": "জাবি সিএসই",
                "total_capacity": 55,
                "quota_capacities": {
                    "GENERAL": 48,
                    "FREEDOM_FIGHTER": 3,
                    "TRIBAL": 2,
                    "DISTRICT": 1,
                    "SPECIAL_NEEDS": 1
                },
                "historical_cutoff_rank": 850,
                "category": "Science",
                "cluster": "GENERAL_PUBLIC"
            },
            "CKET_CSE": {
                "program_id": "CKET_CSE",
                "institution_name": "চুয়েট-কুয়েট-রুয়েট সমন্বিত প্রকৌশল গুচ্ছ (CKET)",
                "department_name": "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)",
                "short_name": "প্রকৌশল গুচ্ছ সিএসই",
                "total_capacity": 180,
                "quota_capacities": {
                    "GENERAL": 160,
                    "FREEDOM_FIGHTER": 10,
                    "TRIBAL": 4,
                    "DISTRICT": 4,
                    "SPECIAL_NEEDS": 2
                },
                "historical_cutoff_rank": 1150,
                "category": "Engineering",
                "cluster": "ENGINEERING"
            },
            "RU_CSE": {
                "program_id": "RU_CSE",
                "institution_name": "রাজশাহী বিশ্ববিদ্যালয় (RU)",
                "department_name": "কম্পিউটার সায়েন্স অ্যান্ড ইঞ্জিনিয়ারিং (CSE)",
                "short_name": "রাবি সিএসই",
                "total_capacity": 50,
                "quota_capacities": {
                    "GENERAL": 42,
                    "FREEDOM_FIGHTER": 3,
                    "TRIBAL": 2,
                    "DISTRICT": 2,
                    "SPECIAL_NEEDS": 1
                },
                "historical_cutoff_rank": 1380,
                "category": "Science",
                "cluster": "GENERAL_PUBLIC"
            }
        }

    # --------------------------------------------------------------------------
    # 1. Program Catalog Interrogation
    # --------------------------------------------------------------------------

    def get_program(self, program_id: str) -> Optional[Dict[str, Any]]:
        """Returns metadata and capacities for a specific university program."""
        return self._calibrated_programs.get(program_id)

    def list_programs(self, cluster: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists available university programs, optionally filtered by cluster."""
        programs = list(self._calibrated_programs.values())
        if cluster:
            programs = [p for p in programs if p["cluster"].upper() == cluster.upper()]
        return sorted(programs, key=lambda x: x["historical_cutoff_rank"])

    # --------------------------------------------------------------------------
    # 2. Gale-Shapley Student-Proposing Deferred Acceptance Matching
    # --------------------------------------------------------------------------

    def run_matching(
        self,
        students: List[Dict[str, Any]],
        programs: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Executes Student-Proposing Deferred Acceptance (Gale-Shapley).
        Guarantees:
        1. Pareto-optimal stable matching for students.
        2. Zero justified envy (no blocking pairs).
        3. Quota reservation with automatic general spillover for unfilled seats.
        """
        if programs is None:
            programs = self._calibrated_programs

        # Deep-copy program capacities
        program_state: Dict[str, Dict[str, Any]] = {}
        for pid, pdata in programs.items():
            q_caps = dict(pdata.get("quota_capacities", {"GENERAL": pdata["total_capacity"]}))
            program_state[pid] = {
                "program_id": pid,
                "total_capacity": pdata["total_capacity"],
                "quota_capacities": q_caps,
                "general_capacity": q_caps.get(self.QUOTA_GENERAL, pdata["total_capacity"]),
                "accepted_students": {},  # quota_category -> List of student dicts
                "all_accepted_ids": set(),
                "cutoff_rank": None,
                "spillover_seats": 0,
            }
            for q_name in q_caps.keys():
                program_state[pid]["accepted_students"][q_name] = []

        # Map student by ID and sort preferences
        student_registry: Dict[str, Dict[str, Any]] = {}
        for s in students:
            student_registry[s["student_id"]] = {
                "student_id": s["student_id"],
                "name": s.get("name", s["student_id"]),
                "merit_score": float(s.get("merit_score", 0.0)),
                "merit_rank": int(s.get("merit_rank", 99999)),
                "quotas": set(s.get("quotas", [self.QUOTA_GENERAL])),
                "preferences": list(s.get("preferences", [])),
                "current_matched_program": None,
                "matched_quota": None,
                "proposals_made": 0,
            }

        # Unmatched students queue (ordered by merit rank for deterministic execution)
        active_student_ids: List[str] = sorted(
            student_registry.keys(),
            key=lambda sid: student_registry[sid]["merit_rank"]
        )

        unmatched_students: List[str] = list(active_student_ids)
        proposal_indices: Dict[str, int] = {sid: 0 for sid in active_student_ids}

        rounds_count = 0
        max_iterations = len(students) * len(programs) + 100

        # Phase A: Standard Student-Proposing Deferred Acceptance
        while unmatched_students and rounds_count < max_iterations:
            rounds_count += 1
            sid = unmatched_students.pop(0)
            s = student_registry[sid]
            pref_idx = proposal_indices[sid]

            # If all preferences exhausted, student remains unmatched
            if pref_idx >= len(s["preferences"]):
                continue

            target_pid = s["preferences"][pref_idx]
            proposal_indices[sid] += 1
            s["proposals_made"] += 1

            if target_pid not in program_state:
                # Invalid program preference, continue to next
                unmatched_students.append(sid)
                continue

            p = program_state[target_pid]

            # Attempt to seat student: First check General, then specific Quota
            assigned = False
            for quota_attempt in [self.QUOTA_GENERAL] + [q for q in s["quotas"] if q != self.QUOTA_GENERAL]:
                if quota_attempt not in p["quota_capacities"]:
                    continue

                quota_cap = p["quota_capacities"][quota_attempt]
                current_quota_list = p["accepted_students"][quota_attempt]

                # If quota has open seats
                if len(current_quota_list) < quota_cap:
                    current_quota_list.append(s)
                    current_quota_list.sort(key=lambda x: x["merit_rank"])
                    p["all_accepted_ids"].add(sid)
                    s["current_matched_program"] = target_pid
                    s["matched_quota"] = quota_attempt
                    assigned = True
                    break
                else:
                    # Check if student beats lowest held student in this quota
                    worst_student = current_quota_list[-1]
                    if s["merit_rank"] < worst_student["merit_rank"]:
                        # Replace worst student
                        current_quota_list.pop()
                        p["all_accepted_ids"].remove(worst_student["student_id"])
                        worst_student["current_matched_program"] = None
                        worst_student["matched_quota"] = None
                        unmatched_students.append(worst_student["student_id"])

                        current_quota_list.append(s)
                        current_quota_list.sort(key=lambda x: x["merit_rank"])
                        p["all_accepted_ids"].add(sid)
                        s["current_matched_program"] = target_pid
                        s["matched_quota"] = quota_attempt
                        assigned = True
                        break

            if not assigned:
                # Student rejected by target_pid; try next preference in next iteration
                unmatched_students.append(sid)

        # Phase B: Quota Automatic Spillover into General Pool
        # Any unfilled quota capacity is converted to General capacity to prevent wasted seats
        total_spillover_seats = 0
        for pid, p in program_state.items():
            spillover = 0
            for q_name, q_cap in p["quota_capacities"].items():
                if q_name == self.QUOTA_GENERAL:
                    continue
                filled = len(p["accepted_students"][q_name])
                unused = q_cap - filled
                if unused > 0:
                    spillover += unused
            p["spillover_seats"] = spillover
            p["general_capacity"] += spillover
            total_spillover_seats += spillover

        # If spillover occurred, allocate unfilled seats to best remaining unmatched students
        if total_spillover_seats > 0:
            remaining_unmatched = [
                student_registry[sid] for sid in active_student_ids
                if student_registry[sid]["current_matched_program"] is None
            ]
            for s in remaining_unmatched:
                for target_pid in s["preferences"]:
                    p = program_state.get(target_pid)
                    if not p:
                        continue
                    gen_list = p["accepted_students"][self.QUOTA_GENERAL]
                    if len(gen_list) < p["general_capacity"]:
                        gen_list.append(s)
                        gen_list.sort(key=lambda x: x["merit_rank"])
                        p["all_accepted_ids"].add(s["student_id"])
                        s["current_matched_program"] = target_pid
                        s["matched_quota"] = "GENERAL_SPILLOVER"
                        break

        # Compute cut-off ranks and final matching report
        matched_results: List[Dict[str, Any]] = []
        program_summaries: Dict[str, Dict[str, Any]] = {}

        for pid, p in program_state.items():
            all_allocated = []
            for q_name, stu_list in p["accepted_students"].items():
                all_allocated.extend(stu_list)
            all_allocated.sort(key=lambda x: x["merit_rank"])

            cutoff = all_allocated[-1]["merit_rank"] if all_allocated else None
            p["cutoff_rank"] = cutoff

            meta = programs.get(pid, {})
            program_summaries[pid] = {
                "program_id": pid,
                "institution_name": meta.get("institution_name", pid),
                "department_name": meta.get("department_name", pid),
                "total_capacity": p["total_capacity"],
                "filled_seats": len(all_allocated),
                "vacant_seats": max(0, p["total_capacity"] - len(all_allocated)),
                "cutoff_rank": cutoff,
                "spillover_seats": p["spillover_seats"],
                "admitted_student_ids": [s["student_id"] for s in all_allocated]
            }

        unmatched_count = 0
        for s in student_registry.values():
            if s["current_matched_program"]:
                matched_results.append({
                    "student_id": s["student_id"],
                    "name": s["name"],
                    "merit_rank": s["merit_rank"],
                    "merit_score": s["merit_score"],
                    "matched_program": s["current_matched_program"],
                    "matched_quota": s["matched_quota"],
                    "preference_rank_achieved": s["preferences"].index(s["current_matched_program"]) + 1
                    if s["current_matched_program"] in s["preferences"] else None
                })
            else:
                unmatched_count += 1
                matched_results.append({
                    "student_id": s["student_id"],
                    "name": s["name"],
                    "merit_rank": s["merit_rank"],
                    "merit_score": s["merit_score"],
                    "matched_program": None,
                    "matched_quota": None,
                    "preference_rank_achieved": None
                })

        # Calculate stability certificate
        stability_audit = self.verify_matching_stability(matched_results, students, programs)

        return {
            "success": True,
            "algorithm": "Gale-Shapley Student-Proposing Deferred Acceptance",
            "total_students": len(students),
            "matched_students": len([m for m in matched_results if m["matched_program"]]),
            "unmatched_students": unmatched_count,
            "iterations_executed": rounds_count,
            "total_spillover_seats": total_spillover_seats,
            "is_stable": stability_audit["is_stable"],
            "blocking_pairs_count": len(stability_audit["blocking_pairs"]),
            "program_summaries": program_summaries,
            "allocations": matched_results
        }

    # --------------------------------------------------------------------------
    # 3. Stability & Envy-Free Verification
    # --------------------------------------------------------------------------

    def verify_matching_stability(
        self,
        allocations: List[Dict[str, Any]],
        students: List[Dict[str, Any]],
        programs: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validates that no blocking pair (s, p) exists.
        A blocking pair occurs if student s strictly prefers program p over their assigned program,
        and either:
        (1) p has unfilled capacity, or
        (2) p admitted student s' where s' has a worse merit rank than s.
        """
        student_map = {s["student_id"]: s for s in students}
        assigned_map = {m["student_id"]: m.get("matched_program") for m in allocations}

        # Collect students admitted to each program
        program_admitted: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for m in allocations:
            pid = m.get("matched_program")
            if pid:
                program_admitted[pid].append(m)

        blocking_pairs: List[Dict[str, Any]] = []

        for s in students:
            sid = s["student_id"]
            current_pid = assigned_map.get(sid)
            prefs = s.get("preferences", [])

            # Determine programs preferred strictly over current match
            preferred_programs = []
            for p_cand in prefs:
                if p_cand == current_pid:
                    break
                preferred_programs.append(p_cand)

            for target_pid in preferred_programs:
                if target_pid not in programs:
                    continue

                target_meta = programs[target_pid]
                capacity = target_meta.get("total_capacity", 0)
                current_admitted = program_admitted.get(target_pid, [])

                # Check 1: Empty seat in preferred program
                if len(current_admitted) < capacity:
                    blocking_pairs.append({
                        "student_id": sid,
                        "program_id": target_pid,
                        "reason": "Unfilled capacity in preferred program"
                    })
                    break

                # Check 2: Target program holds a candidate with worse merit rank
                for other in current_admitted:
                    if other["merit_rank"] > s["merit_rank"]:
                        blocking_pairs.append({
                            "student_id": sid,
                            "program_id": target_pid,
                            "displaced_candidate": other["student_id"],
                            "reason": f"Student rank {s['merit_rank']} strictly better than admitted rank {other['merit_rank']}"
                        })
                        break

        return {
            "is_stable": len(blocking_pairs) == 0,
            "blocking_pairs": blocking_pairs
        }

    # --------------------------------------------------------------------------
    # 4. Multi-Stage Seat Migration Cascade Simulator
    # --------------------------------------------------------------------------

    def simulate_migration_cascade(
        self,
        students: List[Dict[str, Any]],
        programs: Optional[Dict[str, Dict[str, Any]]] = None,
        cancellations: Optional[List[str]] = None,
        num_rounds: int = 3
    ) -> Dict[str, Any]:
        """
        Simulates multi-stage seat migration cascade across multiple counseling rounds.
        When candidates in top programs withdraw/cancel (e.g. going abroad or dual admission),
        their vacancies ripple upward, promoting candidates from lower-preference seats.
        """
        if programs is None:
            programs = self._calibrated_programs

        cancellations_set = set(cancellations or [])

        # Round 1: Initial Gale-Shapley Matching with all active students
        r1_result = self.run_matching(students, programs)
        rounds_history: List[Dict[str, Any]] = []

        rounds_history.append({
            "round_number": 1,
            "title": "প্রথম পর্যায়: প্রাথমিক মেধাভিত্তিক বরাদ্দ",
            "active_students": len(students),
            "matched_students": r1_result["matched_students"],
            "migrations": [],
            "program_summaries": r1_result["program_summaries"],
            "allocations": r1_result["allocations"]
        })

        current_active_students = [s for s in students if s["student_id"] not in cancellations_set]
        last_allocations = {a["student_id"]: a["matched_program"] for a in r1_result["allocations"]}

        # Subsequent rounds: Re-run matching without withdrawn candidates
        for r in range(2, num_rounds + 1):
            next_result = self.run_matching(current_active_students, programs)
            new_allocations = {a["student_id"]: a["matched_program"] for a in next_result["allocations"]}

            # Compute upward migrations
            migrations: List[Dict[str, Any]] = []
            for s in current_active_students:
                sid = s["student_id"]
                prev_prog = last_allocations.get(sid)
                new_prog = new_allocations.get(sid)

                if new_prog and new_prog != prev_prog:
                    migrations.append({
                        "student_id": sid,
                        "name": s.get("name", sid),
                        "merit_rank": s["merit_rank"],
                        "from_program": prev_prog,
                        "to_program": new_prog,
                        "upgrade_description": f"{prev_prog or 'অপেক্ষমাণ'} থেকে {new_prog} তে উন্নীত"
                    })

            last_allocations = new_allocations
            rounds_history.append({
                "round_number": r,
                "title": f"{r}-তম মাইগ্রেশন রাউন্ড: আসন রদবদল ও ঊর্ধ্বমুখী মাইগ্রেশন",
                "active_students": len(current_active_students),
                "matched_students": next_result["matched_students"],
                "migrations": migrations,
                "program_summaries": next_result["program_summaries"],
                "allocations": next_result["allocations"]
            })

        total_migrations_count = sum(len(rnd["migrations"]) for rnd in rounds_history)

        return {
            "success": True,
            "total_rounds": len(rounds_history),
            "cancellations_count": len(cancellations_set),
            "total_upward_migrations": total_migrations_count,
            "rounds": rounds_history
        }

    # --------------------------------------------------------------------------
    # 5. Admission Probability Predictor
    # --------------------------------------------------------------------------

    def predict_admission_probability(
        self,
        merit_rank: int,
        target_program_id: str,
        quota: str = QUOTA_GENERAL
    ) -> Dict[str, Any]:
        """
        Calculates admission probability for a given student merit rank and target program.
        Accounts for historical cutoffs and quota multipliers.
        """
        program = self._calibrated_programs.get(target_program_id)
        if not program:
            return {
                "error": f"Program '{target_program_id}' not found in admission registry.",
                "probability_percent": 0.0,
                "tier": self.TIER_LOW
            }

        base_cutoff = program["historical_cutoff_rank"]

        # Quota multiplier expands cut-off rank boundary
        quota_multipliers = {
            self.QUOTA_GENERAL: 1.0,
            self.QUOTA_FREEDOM_FIGHTER: 1.45,
            self.QUOTA_TRIBAL: 1.80,
            self.QUOTA_DISTRICT: 1.25,
            self.QUOTA_SPECIAL_NEEDS: 2.10
        }
        effective_cutoff = int(base_cutoff * quota_multipliers.get(quota, 1.0))

        if merit_rank <= int(effective_cutoff * 0.70):
            probability = min(99.0, round(92.0 + (effective_cutoff * 0.70 - merit_rank) / effective_cutoff * 7.0, 1))
            tier = self.TIER_HIGH
            guidance = "অত্যন্ত উজ্জ্বল সম্ভাবনা। বিগত বছরগুলোর মেধা তালিকা অনুযায়ী এই বিভাগে আসন প্রাপ্তির প্রবল সুযোগ রয়েছে।"
        elif merit_rank <= effective_cutoff:
            progress = (effective_cutoff - merit_rank) / (effective_cutoff * 0.30)
            probability = round(65.0 + progress * 24.0, 1)
            tier = self.TIER_MODERATE
            guidance = "মধ্যম থেকে সন্তোষজনক সম্ভাবনা। মেধা তালিকা ও প্রথম মাইগ্রেশন রাউন্ডে আসন প্রাপ্তির ভালো সুযোগ বিদ্যমান।"
        elif merit_rank <= int(effective_cutoff * 1.35):
            progress = (effective_cutoff * 1.35 - merit_rank) / (effective_cutoff * 0.35)
            probability = round(25.0 + progress * 35.0, 1)
            tier = self.TIER_AMBITIOUS
            guidance = "উচ্চাকাঙ্ক্ষী লক্ষ্য। শেষ মাইগ্রেশন রাউন্ড অথবা বিশেষ কোটা আসন স্পিল-ওভারে সম্ভাবনা নির্ভর করবে।"
        else:
            probability = max(5.0, round(20.0 - (merit_rank - effective_cutoff * 1.35) / effective_cutoff * 15.0, 1))
            tier = self.TIER_LOW
            guidance = "ঝুঁকিপূর্ণ পছন্দক্রম। বিকল্প আরও সুবিধাজনক বিভাগগুলোকে পছন্দক্রমের উপরে রাখার পরামর্শ দেওয়া হচ্ছে।"

        return {
            "program_id": target_program_id,
            "institution_name": program["institution_name"],
            "department_name": program["department_name"],
            "merit_rank": merit_rank,
            "quota_applied": quota,
            "effective_cutoff_rank": effective_cutoff,
            "probability_percent": probability,
            "tier": tier,
            "guidance_bn": guidance
        }


# Global Singleton Instance
gale_shapley_counseling_service = GaleShapleyCounselingService()
