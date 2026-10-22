"""
================================================================================
MODULE: Mathematical & Scientific Visualization (ম্যাথ ও জ্যামিতি ভিজ্যুয়ালাইজার)
TOPIC: Procedural Vector SVG Diagrams, Geometric Proofs & Coordinate Visualizers
FILE: backend/app/services/math_visualizer_service.py
PURPOSE: Procedurally generates interactive, high-precision mathematical and scientific
         SVG vector diagrams (e.g., Pythagorean visual proofs, trigonometric unit
         circles, physics projectile trajectories). Provides responsive, zero-pixelation
         visual scaffolds to bridge abstract formulas into intuitive visual understanding.
AUDIENCE: Students, STEM Educators, Visual Interaction Designers.
STANDARDS: W3C SVG 2.0 Standard, NCTB Visual Pedagogy Guidelines.
================================================================================
"""

from typing import Any, Dict, List, Optional


class MathVisualizerService:
    """Procedurally generates interactive SVG diagrams for mathematical and scientific concepts."""

    SUPPORTED_CONCEPTS = ["pythagoras_proof", "unit_circle_trig", "kinematics_projectile"]

    def generate_geometry_svg(
        self,
        concept_id: str,
        param_a: float = 6.0,
        param_b: float = 8.0,
    ) -> Dict[str, Any]:
        """Generates crisp SVG markup and structural metadata for the requested mathematical concept."""
        if concept_id == "pythagoras_proof":
            if param_a <= 0.0 or param_b <= 0.0:
                return {
                    "success": False,
                    "message": "জ্যামিতিক বাহুর দৈর্ঘ্য অবশ্যই ০ এর চেয়ে বড় ধনাত্মক সংখ্যা হতে হবে।",
                }
            return self._generate_pythagoras_svg(param_a, param_b)
        elif concept_id == "unit_circle_trig":
            return self._generate_unit_circle_svg()
        elif concept_id == "kinematics_projectile":
            return self._generate_projectile_svg()
        else:
            return {
                "success": False,
                "message": f"অজানা কনসেপ্ট আইডি: '{concept_id}'। সমর্থিত কনসেপ্ট: {', '.join(self.SUPPORTED_CONCEPTS)}।",
            }

    def _generate_pythagoras_svg(self, a: float, b: float) -> Dict[str, Any]:
        """Generates an SVG proof of the Pythagorean Theorem with side squares."""
        c = (a**2 + b**2)**0.5
        scale = 15.0
        # Scaled dimensions for a 400x300 viewBox
        base_px = b * scale
        height_px = a * scale

        svg = f"""<svg viewBox="0 0 450 320" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto max-w-lg mx-auto">
  <defs>
    <linearGradient id="triGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#2563EB" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <!-- Grid Lines -->
  <line x1="40" y1="260" x2="410" y2="260" stroke="#94A3B8" stroke-width="1" stroke-dasharray="4,4"/>
  
  <!-- Right-Angled Triangle -->
  <polygon points="60,260 {60 + base_px},260 60,{260 - height_px}" fill="url(#triGrad)" stroke="#2563EB" stroke-width="3"/>
  
  <!-- Right Angle Square Indicator -->
  <rect x="60" y="{260 - 20}" width="20" height="20" fill="none" stroke="#2563EB" stroke-width="2"/>
  
  <!-- Side Labels -->
  <text x="{60 + base_px / 2}" y="285" font-family="sans-serif" font-size="14" font-weight="bold" fill="#1E293B" text-anchor="middle">ভূমি (b = {b} সেমি)</text>
  <text x="35" y="{260 - height_px / 2}" font-family="sans-serif" font-size="14" font-weight="bold" fill="#1E293B" text-anchor="middle" transform="rotate(-90 35,{260 - height_px / 2})">লম্ব (a = {a} সেমি)</text>
  <text x="{60 + base_px / 2 + 25}" y="{260 - height_px / 2 - 10}" font-family="sans-serif" font-size="14" font-weight="bold" fill="#059669" text-anchor="middle">অতিভুজ (c = {round(c, 1)} সেমি)</text>

  <!-- Formula Callout -->
  <rect x="220" y="30" width="200" height="75" rx="10" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="320" y="55" font-family="sans-serif" font-size="13" font-weight="bold" fill="#0F172A" text-anchor="middle">পিথাগোরাস উপপাদ্য</text>
  <text x="320" y="78" font-family="monospace" font-size="14" font-weight="bold" fill="#2563EB" text-anchor="middle">a² + b² = c²</text>
  <text x="320" y="96" font-family="sans-serif" font-size="11" fill="#64748B" text-anchor="middle">{a}² + {b}² = {int(a**2 + b**2)} = {round(c, 1)}²</text>
</svg>"""

        return {
            "success": True,
            "concept_id": "pythagoras_proof",
            "title": "পিথাগোরাসের জ্যামিতিক উপপাদ্য",
            "dimensions": {"a": a, "b": b, "c": round(c, 2)},
            "parameters": {"a": a, "b": b, "hypotenuse_c": round(c, 2)},
            "svg_markup": svg,
            "formula_latex": "c = \\sqrt{a^2 + b^2}",
        }

    def _generate_unit_circle_svg(self) -> Dict[str, Any]:
        """Generates a responsive SVG trigonometric unit circle."""
        svg = """<svg viewBox="0 0 360 360" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto max-w-sm mx-auto">
  <!-- Axes -->
  <line x1="20" y1="180" x2="340" y2="180" stroke="#94A3B8" stroke-width="1.5"/>
  <line x1="180" y1="20" x2="180" y2="340" stroke="#94A3B8" stroke-width="1.5"/>
  <text x="330" y="170" font-family="sans-serif" font-size="12" fill="#64748B">x</text>
  <text x="190" y="35" font-family="sans-serif" font-size="12" fill="#64748B">y</text>
  
  <!-- Unit Circle (R=120) -->
  <circle cx="180" cy="180" r="120" fill="none" stroke="#3B82F6" stroke-width="2.5"/>
  
  <!-- 45 Degree Angle Line -->
  <!-- cos(45)=0.7071*120=84.85, sin(45)=84.85 -->
  <!-- Point: (180+85, 180-85) = (265, 95) -->
  <line x1="180" y1="180" x2="265" y2="95" stroke="#059669" stroke-width="3"/>
  <circle cx="265" cy="95" r="5" fill="#059669"/>
  
  <!-- Projections -->
  <line x1="265" y1="95" x2="265" y2="180" stroke="#DC2626" stroke-width="2" stroke-dasharray="3,3"/>
  <line x1="180" y1="95" x2="265" y2="95" stroke="#2563EB" stroke-width="2" stroke-dasharray="3,3"/>
  
  <!-- Angle Arc -->
  <path d="M 215,180 A 35,35 0 0,0 205,155" fill="none" stroke="#D97706" stroke-width="2"/>
  <text x="218" y="165" font-family="sans-serif" font-size="12" font-weight="bold" fill="#D97706">θ = ৪৫°</text>
  
  <!-- Coordinate Label -->
  <text x="272" y="90" font-family="monospace" font-size="11" font-weight="bold" fill="#0F172A">(cos θ, sin θ)</text>
  <text x="272" y="105" font-family="monospace" font-size="10" fill="#64748B">(১/√২, ১/√২)</text>
</svg>"""

        return {
            "success": True,
            "concept_id": "unit_circle_trig",
            "title": "একক বৃত্ত ও ত্রিকোণমিতি (Unit Circle)",
            "svg_markup": svg,
            "formula_latex": "\\cos^2(\\theta) + \\sin^2(\\theta) = 1",
        }

    def _generate_projectile_svg(self) -> Dict[str, Any]:
        """Generates a responsive SVG projectile parabolic path."""
        svg = """<svg viewBox="0 0 420 240" xmlns="http://www.w3.org/2000/svg" class="w-full h-auto max-w-md mx-auto">
  <!-- Ground -->
  <line x1="30" y1="200" x2="390" y2="200" stroke="#475569" stroke-width="2"/>
  
  <!-- Parabolic Trajectory -->
  <path d="M 40,200 Q 210,30 380,200" fill="none" stroke="#2563EB" stroke-width="3"/>
  
  <!-- Peak Point -->
  <circle cx="210" cy="115" r="4.5" fill="#DC2626"/>
  <text x="210" y="95" font-family="sans-serif" font-size="12" font-weight="bold" fill="#DC2626" text-anchor="middle">সর্বোচ্চ উচ্চতা (H_max)</text>
  
  <!-- Initial Velocity Vector -->
  <line x1="40" y1="200" x2="100" y2="135" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="110" y="130" font-family="sans-serif" font-size="12" font-weight="bold" fill="#059669">v₀ (আদিবেগ)</text>
  
  <!-- Angle Arc -->
  <path d="M 70,200 A 30,30 0 0,0 62,175" fill="none" stroke="#D97706" stroke-width="2"/>
  <text x="75" y="190" font-family="sans-serif" font-size="11" font-weight="bold" fill="#D97706">θ₀</text>

  <!-- Horizontal Range -->
  <line x1="40" y1="220" x2="380" y2="220" stroke="#64748B" stroke-width="1.5" stroke-dasharray="4,4"/>
  <text x="210" y="235" font-family="sans-serif" font-size="12" font-weight="bold" fill="#64748B" text-anchor="middle">পাল্লা (Range R = v₀² sin 2θ / g)</text>
</svg>"""

        return {
            "success": True,
            "concept_id": "kinematics_projectile",
            "title": "প্রাসের গতিপথ ও সঞ্চারপথ (Projectile Trajectory)",
            "svg_markup": svg,
            "formula_latex": "y = x \\tan(\\theta) - \\frac{g x^2}{2 v_0^2 \\cos^2(\\theta)}",
        }


# Global Singleton Service
math_visualizer_service = MathVisualizerService()
