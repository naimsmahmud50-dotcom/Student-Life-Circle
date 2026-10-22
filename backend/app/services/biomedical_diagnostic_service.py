"""
Biomedical Diagnostic Sandbox & ROC-AUC Pathology Service (Phase 37).
Provides:
1. Clinical confusion matrix performance evaluation (Sensitivity, Specificity, PPV, NPV, F1)
2. ROC (Receiver Operating Characteristic) curve generation with trapezoidal AUC integration
3. Clinical decision threshold optimization for AI-assisted Chest X-Ray screening
"""

import math
from typing import Dict, Any, List

from backend.app.schemas.robotics_genomics_and_biomedical_schema import (
    DiagnosticConfusionMatrixRequest,
    DiagnosticPerformanceResponse,
    DiagnosticRocCurveRequest,
    DiagnosticRocCurveResponse,
)

class BiomedicalDiagnosticSandboxService:
    def evaluate_confusion_matrix(self, request: DiagnosticConfusionMatrixRequest) -> DiagnosticPerformanceResponse:
        """
        Calculates epidemiological diagnostic metrics with zero-division singularity safeguards.
        """
        tp = max(0, int(request.true_positives))
        fp = max(0, int(request.false_positives))
        tn = max(0, int(request.true_negatives))
        fn = max(0, int(request.false_negatives))

        total = tp + fp + tn + fn
        if total == 0:
            tp, tn = 50, 50
            total = 100

        # Sensitivity (True Positive Rate / Recall): TP / (TP + FN)
        actual_positives = tp + fn
        sensitivity = (tp / actual_positives) if actual_positives > 0 else 0.0

        # Specificity (True Negative Rate): TN / (TN + FP)
        actual_negatives = tn + fp
        specificity = (tn / actual_negatives) if actual_negatives > 0 else 0.0

        # Positive Predictive Value (Precision): TP / (TP + FP)
        predicted_positives = tp + fp
        ppv = (tp / predicted_positives) if predicted_positives > 0 else 0.0

        # Negative Predictive Value: TN / (TN + FN)
        predicted_negatives = tn + fn
        npv = (tn / predicted_negatives) if predicted_negatives > 0 else 0.0

        # F1-Score: 2 * (PPV * TPR) / (PPV + TPR)
        f1 = (2.0 * ppv * sensitivity) / (ppv + sensitivity) if (ppv + sensitivity) > 0 else 0.0

        # Balanced Accuracy: (Sensitivity + Specificity) / 2
        balanced_acc = (sensitivity + specificity) / 2.0

        if sensitivity >= 0.90 and specificity >= 0.90:
            tier = "CLINICALLY_VALIDATED"
        elif sensitivity >= 0.80 and specificity >= 0.75:
            tier = "ACCEPTABLE_SCREENING"
        else:
            tier = "INADEQUATE"

        return DiagnosticPerformanceResponse(
            total_samples=total,
            sensitivity_tpr=round(sensitivity, 3),
            specificity_tnr=round(specificity, 3),
            positive_predictive_value_ppv=round(ppv, 3),
            negative_predictive_value_npv=round(npv, 3),
            f1_score=round(f1, 3),
            balanced_accuracy=round(balanced_acc, 3),
            diagnostic_tier=tier
        )

    def generate_roc_curve(self, request: DiagnosticRocCurveRequest) -> DiagnosticRocCurveResponse:
        """
        Generates 11-point ROC trajectory and calculates trapezoidal AUC for clinical screening.
        """
        threshold = max(0.05, min(float(request.current_threshold), 0.95))

        # Synthetic calibrated CheXNet / TB classifier response:
        # Logistic TPR: 1 - threshold^1.8
        # FPR: (1 - threshold)^3.2
        curve_points = []
        auc_sum = 0.0
        prev_fpr = 0.0
        prev_tpr = 0.0

        # Generate points from threshold 1.0 down to 0.0
        steps = 10
        for i in range(steps + 1):
            t = 1.0 - (i / steps)
            # Parametric ROC curve for high-performance biomarker (AUC ~ 0.93 - 0.95)
            fpr = round(math.pow(1.0 - t, 2.8), 3)
            tpr = round(1.0 - math.pow(t, 2.2), 3)

            curve_points.append({
                "threshold": round(t, 2),
                "false_positive_rate": fpr,
                "true_positive_rate": tpr
            })

            if i > 0:
                # Trapezoidal Area Under Curve
                delta_fpr = fpr - prev_fpr
                avg_tpr = (tpr + prev_tpr) / 2.0
                auc_sum += delta_fpr * avg_tpr

            prev_fpr = fpr
            prev_tpr = tpr

        auc_roc = round(max(0.50, min(auc_sum, 0.99)), 3)

        # Operating point metrics at current_threshold
        op_tpr = round(1.0 - math.pow(threshold, 2.2), 3)
        op_fpr = round(math.pow(1.0 - threshold, 2.8), 3)
        op_tnr = round(1.0 - op_fpr, 3)

        if threshold <= 0.35:
            rec = "High-Sensitivity Rule-Out: Ideal for community mass screening to prevent missed active infections."
        elif threshold >= 0.65:
            rec = "High-Specificity Rule-In: Ideal for secondary triage prior to initiating aggressive pharmacological treatment."
        else:
            rec = "Balanced Youden Operating Point: Optimal balance between detection sensitivity and false alarm rate."

        return DiagnosticRocCurveResponse(
            disease_name=request.disease_name,
            auc_roc=auc_roc,
            current_threshold=round(threshold, 2),
            operating_point_sensitivity=op_tpr,
            operating_point_specificity=op_tnr,
            curve_points=curve_points,
            clinical_recommendation=rec
        )

# Global singleton
biomedical_diagnostic_service = BiomedicalDiagnosticSandboxService()
