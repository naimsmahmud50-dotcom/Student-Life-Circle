"""
Global Research Grant & Post-Doctoral Fellowship Clearinghouse Service (Phase 36).
Provides international fellowship discovery (Fulbright, DAAD, Erasmus Mundus, Commonwealth, MEXT),
Statement of Purpose (SOP) lexical density & research rigor evaluation, and multi-currency grant budget allocation.
"""

import re
from typing import List, Optional, Dict, Any

from backend.app.schemas.satellite_grant_and_swarm_schema import (
    FellowshipSearchQuery,
    FellowshipResponse,
    SopEvaluationRequest,
    SopEvaluationResponse,
    GrantBudgetCalculationRequest,
    GrantBudgetCalculationResponse,
)

class GlobalResearchGrantService:
    USD_TO_BDT_RATE: float = 121.50

    def __init__(self):
        self._fellowships: List[Dict[str, Any]] = [
            {
                "fellowship_id": "FULBRIGHT-FOREIGN-STUDENT-2025",
                "title": "Fulbright Foreign Student Program",
                "sponsor_agency": "U.S. Department of State & US Embassy Dhaka",
                "host_countries": ["United States"],
                "degree_levels": ["MASTERS", "PHD"],
                "funding_type": "FULL_RIDE",
                "monthly_stipend_approx_bdt": 290000.0,
                "annual_allowance_usd": 48000.0,
                "deadline": "2025-05-31",
                "eligibility_summary": "Bangladeshi citizens with outstanding academic records (minimum 16 years of formal education), leadership potential, and commitment to return to Bangladesh.",
                "official_portal_url": "https://bd.usembassy.gov/fulbright-foreign-student-program/"
            },
            {
                "fellowship_id": "DAAD-EPOS-2025",
                "title": "DAAD Development-Related Postgraduate Courses (EPOS)",
                "sponsor_agency": "German Academic Exchange Service (DAAD)",
                "host_countries": ["Germany"],
                "degree_levels": ["MASTERS", "PHD"],
                "funding_type": "FULL_RIDE",
                "monthly_stipend_approx_bdt": 155000.0,
                "annual_allowance_usd": 22000.0,
                "deadline": "2025-08-31",
                "eligibility_summary": "Bachelor degree holder with minimum 2 years of professional work experience; strong focus on engineering, economics, public health, or agriculture.",
                "official_portal_url": "https://www.daad.de/en/study-and-research-in-germany/scholarships/"
            },
            {
                "fellowship_id": "ERASMUS-MUNDUS-EMJM-2025",
                "title": "Erasmus Mundus Joint Masters Scholarship (EMJM)",
                "sponsor_agency": "European Commission",
                "host_countries": ["France", "Germany", "Sweden", "Italy", "Netherlands"],
                "degree_levels": ["MASTERS"],
                "funding_type": "FULL_RIDE",
                "monthly_stipend_approx_bdt": 182000.0,
                "annual_allowance_usd": 28000.0,
                "deadline": "2025-02-15",
                "eligibility_summary": "Top 5% university graduates across all disciplines. Mobility across at least 2 distinct European universities required.",
                "official_portal_url": "https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus_en"
            },
            {
                "fellowship_id": "COMMONWEALTH-SCHOLARSHIP-2025",
                "title": "Commonwealth Master's & PhD Scholarships",
                "sponsor_agency": "Commonwealth Scholarship Commission (CSC UK)",
                "host_countries": ["United Kingdom"],
                "degree_levels": ["MASTERS", "PHD"],
                "funding_type": "FULL_RIDE",
                "monthly_stipend_approx_bdt": 245000.0,
                "annual_allowance_usd": 42000.0,
                "deadline": "2024-12-12",
                "eligibility_summary": "Citizens of Commonwealth developing countries (including Bangladesh); cannot otherwise afford to study in the UK without scholarship support.",
                "official_portal_url": "https://cscuk.fcdo.gov.uk/scholarships/"
            },
            {
                "fellowship_id": "MEXT-RESEARCH-2025",
                "title": "Monbukagakusho (MEXT) University Recommendation Fellowship",
                "sponsor_agency": "Ministry of Education, Culture, Sports, Science and Technology Japan",
                "host_countries": ["Japan"],
                "degree_levels": ["MASTERS", "PHD", "POSTDOC"],
                "funding_type": "FULL_RIDE",
                "monthly_stipend_approx_bdt": 168000.0,
                "annual_allowance_usd": 26000.0,
                "deadline": "2025-01-20",
                "eligibility_summary": "Under age 35, outstanding CGPA in STEM/humanities, willingness to learn Japanese language fundamentals upon arrival in Tokyo/Kyoto/Tohoku.",
                "official_portal_url": "https://www.bd.emb-japan.go.jp/itpr_en/mext_scholarship.html"
            }
        ]

    def list_fellowships(self, query: Optional[FellowshipSearchQuery] = None) -> List[FellowshipResponse]:
        """
        Filters international fellowships based on degree level, field, or host country.
        """
        results = []
        for f in self._fellowships:
            if query:
                if query.degree_level and query.degree_level.upper() not in [lvl.upper() for lvl in f["degree_levels"]]:
                    continue
                if query.destination_country:
                    match_country = any(
                        query.destination_country.lower() in c.lower() for c in f["host_countries"]
                    )
                    if not match_country:
                        continue
            results.append(FellowshipResponse(**f))
        return results

    def evaluate_sop(self, request: SopEvaluationRequest) -> SopEvaluationResponse:
        """
        Analyzes Statement of Purpose (SOP) text for lexical density, academic rigor,
        structural completeness, and research readiness.
        """
        raw_text = request.sop_text.strip()
        tokens = re.findall(r'\b[a-zA-Z]{2,}\b', raw_text.lower())
        word_count = len(tokens)

        if word_count < 30:
            return SopEvaluationResponse(
                target_fellowship=request.target_fellowship_id,
                word_count=word_count,
                lexical_density_pct=0.0,
                academic_rigor_score=15.0,
                overall_readiness_tier="NEEDS_REVISION",
                strengths=["Basic intent expressed"],
                weaknesses=["SOP draft is excessively brief (< 30 words); lacks research thesis and methodology."],
                actionable_recommendations=[
                    "Expand introduction with a clear research problem statement.",
                    "Articulate 2-3 specific empirical or theoretical research objectives.",
                    "Highlight relevant undergraduate research or industrial achievements."
                ]
            )

        unique_tokens = set(tokens)
        lexical_density = round((len(unique_tokens) / word_count) * 100.0, 1)

        # Dimension Rubric Analysis
        has_research_objective = any(w in raw_text.lower() for w in ["objective", "hypothesis", "research question", "investigate", "explore", "aim"])
        has_methodology = any(w in raw_text.lower() for w in ["methodology", "simulation", "empirical", "framework", "experiment", "quantitative", "dataset"])
        has_impact = any(w in raw_text.lower() for w in ["contribution", "impact", "advancement", "bangladesh", "societal", "sustainable", "significance"])
        has_advisor_fit = any(w in raw_text.lower() for w in ["faculty", "laboratory", "professor", "curriculum", "department", "initiative"])

        # Base scoring
        score = 40.0
        if 40.0 <= lexical_density <= 75.0:
            score += 15.0
        elif lexical_density > 75.0:
            score += 10.0

        if has_research_objective:
            score += 15.0
        if has_methodology:
            score += 15.0
        if has_impact:
            score += 10.0
        if has_advisor_fit:
            score += 5.0

        score = min(100.0, max(20.0, score))

        strengths = []
        weaknesses = []
        recommendations = []

        if has_research_objective:
            strengths.append("Clear research problem and intellectual curiosity identified.")
        else:
            weaknesses.append("Lacks explicit hypothesis or research question definition.")
            recommendations.append("State your central investigative question clearly in the second paragraph.")

        if has_methodology:
            strengths.append("Mentions methodological techniques and analytical frameworks.")
        else:
            weaknesses.append("Methodology is abstract; missing specific empirical tools or models.")
            recommendations.append("Specify laboratory techniques, computational toolkits (e.g. PyTorch, MATLAB), or datasets you intend to deploy.")

        if has_impact:
            strengths.append("Articulates practical development or societal impact.")
        else:
            weaknesses.append("Broader significance and post-graduation impact not clearly outlined.")
            recommendations.append("Describe how your research will address pressing technical challenges in your home country or global industry.")

        if has_advisor_fit:
            strengths.append("Demonstrates alignment with host faculty and institutional resources.")
        else:
            recommendations.append("Name 1-2 prospective faculty advisors or research clusters at the target institution.")

        if score >= 85.0:
            tier = "HIGHLY_COMPETITIVE"
        elif score >= 70.0:
            tier = "COMPETITIVE"
        else:
            tier = "NEEDS_REVISION"

        return SopEvaluationResponse(
            target_fellowship=request.target_fellowship_id,
            word_count=word_count,
            lexical_density_pct=lexical_density,
            academic_rigor_score=round(score, 1),
            overall_readiness_tier=tier,
            strengths=strengths or ["Constructive academic tone"],
            weaknesses=weaknesses or ["Minor formatting refinements recommended"],
            actionable_recommendations=recommendations or ["Review for precision with institutional advisor."]
        )

    def calculate_grant_budget(self, request: GrantBudgetCalculationRequest) -> GrantBudgetCalculationResponse:
        """
        Calculates research grant budget, indirect institutional overheads, and converts to BDT.
        """
        direct_costs = max(0.0, float(request.direct_research_costs_usd))
        equipment = max(0.0, float(request.equipment_stipend_usd))
        travel = max(0.0, float(request.travel_conference_usd))
        overhead_rate = max(0.0, min(float(request.overhead_rate_pct), 65.0))

        subtotal_direct = direct_costs + equipment + travel
        overhead_usd = subtotal_direct * (overhead_rate / 100.0)
        total_usd = subtotal_direct + overhead_usd
        total_bdt = total_usd * self.USD_TO_BDT_RATE

        return GrantBudgetCalculationResponse(
            direct_costs_usd=round(subtotal_direct, 2),
            overhead_usd=round(overhead_usd, 2),
            total_budget_usd=round(total_usd, 2),
            total_budget_bdt=round(total_bdt, 2),
            effective_exchange_rate_bdt=self.USD_TO_BDT_RATE,
            breakdown_usd={
                "direct_research_costs": round(direct_costs, 2),
                "equipment_stipend": round(equipment, 2),
                "travel_conference": round(travel, 2),
                "institutional_overhead": round(overhead_usd, 2)
            }
        )

# Global singleton
global_research_grant_service = GlobalResearchGrantService()
