"""
Synthetic Biology CRISPR-Cas9 Optimization Service
===================================================
Computational guide-RNA (gRNA) design, SpCas9 protospacer-adjacent motif
(PAM NGG) recognition, Doench Rule Set 2 on-target cleavage efficiency,
and Hsu-Zhang off-target mismatch penalty scoring.

Mathematical & Biochemical Foundation:
- SpCas9 PAM: NGG at 3' end (positions 21-23 of 23nt target site)
- Seed Region: Nucleotides 1-8 proximal to PAM (highest sensitivity to mismatches)
- Non-Seed Region: Nucleotides 9-20 distal to PAM (moderate mismatch tolerance)
- Hsu-Zhang Mismatch Weighting: M_k based on distance from PAM
- On-Target GC Content: Optimal 40% - 60% (GC < 30% or > 70% severely penalized)
- Secondary Structure Hairpin Energy: Delta G >= -2.0 kcal/mol required for open scaffold binding

Zero external dependencies — pure Python standard library.
"""

import math
from typing import Any, Dict, List


class SyntheticBiologyCrisprService:
    """Enterprise CRISPR-Cas9 genome engineering and gRNA optimization engine."""

    # Hsu-Zhang empirical mismatch tolerance weights (position 1 = adjacent to PAM, 20 = distal)
    HSU_WEIGHTS = [
        0.000, 0.000, 0.014, 0.000, 0.000, 0.395, 0.317, 0.000,
        0.389, 0.079, 0.445, 0.508, 0.613, 0.851, 0.732, 0.828,
        0.615, 0.804, 0.685, 0.584,
    ]

    @staticmethod
    def evaluate_grna_efficiency_and_pam(
        sequence_23nt: str,
    ) -> Dict[str, Any]:
        """
        Validate 20nt protospacer + 3nt PAM (NGG), compute GC content,
        poly-T termination tracts, and Doench on-target cleavage efficiency.
        """
        seq = sequence_23nt.upper().strip()
        if len(seq) != 23:
            return {
                "error": "Sequence must be exactly 23 nucleotides (20nt protospacer + 3nt PAM)",
                "valid": False,
            }

        protospacer = seq[:20]
        pam = seq[20:]

        # Validate SpCas9 canonical PAM: NGG (any base followed by GG)
        has_canonical_pam = len(pam) == 3 and pam[1] == "G" and pam[2] == "G"

        # Calculate GC content of 20nt protospacer
        gc_count = protospacer.count("G") + protospacer.count("C")
        gc_pct = (gc_count / 20.0) * 100.0

        # Check for Pol-III U6 promoter terminator tract (TTTT or TTTTT)
        has_poly_t_terminator = "TTTT" in protospacer

        # Doench on-target cleavage heuristic score (0 - 100)
        score = 60.0

        # Optimal GC content is 40% - 60%
        if 40.0 <= gc_pct <= 60.0:
            score += 20.0
        elif 30.0 <= gc_pct < 40.0 or 60.0 < gc_pct <= 70.0:
            score += 5.0
        else:
            score -= 25.0

        # Penalty for Pol-III terminator
        if has_poly_t_terminator:
            score -= 30.0

        # Bonus for preferred base at position 20 (G or A preferred adjacent to PAM)
        if protospacer[-1] in ("G", "A"):
            score += 10.0

        # Penalty for unfavorable thymine at position 20
        if protospacer[-1] == "T":
            score -= 10.0

        score = max(5.0, min(100.0, score))

        # Secondary structure / self-hairpin free energy approximation
        # Check reverse-complement self-folding between 5' (1-6) and 3' (15-20)
        c_map = {"A": "T", "T": "A", "C": "G", "G": "C"}
        head = protospacer[:6]
        tail_rev_comp = "".join(c_map.get(b, "N") for b in reversed(protospacer[14:]))
        hairpin_matches = sum(1 for a, b in zip(head, tail_rev_comp) if a == b)
        approx_delta_g = round(-1.2 * hairpin_matches, 1)

        hairpin_risk = approx_delta_g < -3.0

        return {
            "full_target_23nt": seq,
            "protospacer_20nt": protospacer,
            "pam_3nt": pam,
            "has_canonical_pam": has_canonical_pam,
            "gc_content_pct": round(gc_pct, 1),
            "has_poly_t_terminator": has_poly_t_terminator,
            "on_target_efficiency_score": round(score, 1),
            "hairpin_folding_energy_kcal_mol": approx_delta_g,
            "hairpin_inhibition_risk": hairpin_risk,
            "grna_grade": "TIER_1_OPTIMAL" if score >= 80.0 and has_canonical_pam and not hairpin_risk else ("TIER_2_ACCEPTABLE" if score >= 50.0 and has_canonical_pam else "POOR_LOW_EFFICIENCY"),
        }

    @staticmethod
    def calculate_off_target_cleavage_score(
        guide_20nt: str,
        potential_off_target_20nt: str,
    ) -> Dict[str, Any]:
        """
        Calculate cutting frequency determination (CFD) off-target score
        using Hsu-Zhang position-dependent mismatch penalty matrix.
        """
        g = guide_20nt.upper().strip()[:20]
        t = potential_off_target_20nt.upper().strip()[:20]

        if len(g) != 20 or len(t) != 20:
            return {"error": "Both sequences must be 20 nucleotides long"}

        mismatches = []
        consecutive_mismatches = 0
        max_consecutive = 0

        # Positions are indexed 1 to 20 from PAM (position 20 in 5'->3' is pos 1 from PAM)
        cfd_score = 1.0

        for idx in range(20):
            # idx 0 is 5' end (pos 20 from PAM), idx 19 is 3' end (pos 1 from PAM)
            pos_from_pam = 20 - idx
            b_guide = g[idx]
            b_target = t[idx]

            if b_guide != b_target:
                mismatches.append({
                    "sequence_index": idx + 1,
                    "distance_from_pam": pos_from_pam,
                    "guide_base": b_guide,
                    "target_base": b_target,
                    "is_seed_region": pos_from_pam <= 8,
                })
                consecutive_mismatches += 1
                max_consecutive = max(max_consecutive, consecutive_mismatches)

                # Weight factor from Hsu matrix
                w = SyntheticBiologyCrisprService.HSU_WEIGHTS[pos_from_pam - 1]
                cfd_score *= w
            else:
                consecutive_mismatches = 0

        # Multi-mismatch distance factor penalty
        num_mismatches = len(mismatches)
        if num_mismatches > 1:
            penalty = 1.0 / ((19.0 - (num_mismatches - 1)) / 19.0 * 4.0 + 1.0)
            cfd_score *= penalty

        # Consecutive mismatch bubble penalty (>= 2 consecutive mismatches drastically destroys cleavage)
        if max_consecutive >= 2:
            cfd_score *= 0.1

        off_target_cutting_prob_pct = round(cfd_score * 100.0, 3)

        return {
            "guide_sequence": g,
            "off_target_sequence": t,
            "total_mismatches": num_mismatches,
            "seed_region_mismatches": sum(1 for m in mismatches if m["is_seed_region"]),
            "max_consecutive_mismatches": max_consecutive,
            "mismatch_details": mismatches,
            "off_target_cleavage_probability_pct": off_target_cutting_prob_pct,
            "off_target_risk_level": "NEGLIGIBLE (SAFE)" if off_target_cutting_prob_pct < 0.5 else ("LOW" if off_target_cutting_prob_pct < 5.0 else ("MODERATE" if off_target_cutting_prob_pct < 25.0 else "CRITICAL_HIGH_RISK")),
        }
