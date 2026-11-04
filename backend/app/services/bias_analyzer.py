"""Fairness metrics for black-box model predictions."""

from typing import Any, Dict, List, Optional, Sequence
import math
import numpy as np
import pandas as pd
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class BiasAnalyzer:
    """Calculate non-fabricated prediction and group fairness statistics."""

    def __init__(self, protected_attributes: Optional[Sequence[str]] = None):
        self.protected_attributes = list(protected_attributes or ("gender", "race"))

    async def analyze(
        self,
        synthetic_inputs: List[Dict[str, Any]],
        model_outputs: List[Dict[str, Any]],
        *,
        protected_attributes: Optional[Sequence[str]] = None,
        ground_truth: Optional[Sequence[Any]] = None,
        favorable_threshold: float = 0.5,
    ) -> Dict[str, Any]:
        if not synthetic_inputs or not model_outputs:
            raise ValueError("At least one valid input and prediction are required")

        rows = []
        for output in model_outputs:
            prediction = self._extract_prediction(output.get("output"))
            if prediction is None:
                logger.warning("Skipping a model response without a scalar prediction")
                continue
            input_id = output.get("input_id", "")
            index = int(input_id.rsplit("_", 1)[-1]) if "_" in input_id else None
            if index is None or index >= len(synthetic_inputs):
                continue
            row = dict(synthetic_inputs[index])
            row["prediction"] = prediction
            rows.append(row)

        if not rows:
            raise ValueError("Model responses did not contain usable scalar predictions")
        df = pd.DataFrame(rows)
        attributes = [
            a for a in (protected_attributes or self.protected_attributes)
            if a in df.columns
        ]
        if not 0 <= favorable_threshold <= 1:
            raise ValueError("favorable_threshold must be between 0 and 1")
        df["favorable_prediction"] = (df["prediction"] >= favorable_threshold).astype(int)
        metrics: List[Dict[str, Any]] = []
        parity: List[Dict[str, Any]] = []
        disparities: List[float] = []
        for attribute in attributes:
            grouped = df.groupby(attribute, dropna=False)["favorable_prediction"].agg(["mean", "count"])
            rates = grouped["mean"].to_dict()
            if len(rates) < 2:
                continue
            reference = next(iter(rates))
            reference_rate = float(rates[reference])
            differences = [abs(float(rate) - reference_rate) for rate in rates.values()]
            disparity = max(differences)
            disparities.append(disparity)
            ratio = (
                min(float(rate) for rate in rates.values()) /
                max(float(rate) for rate in rates.values())
                if max(float(rate) for rate in rates.values()) > 0 else None
            )
            metrics.extend([
                {"metric": f"demographic_parity_difference_{attribute}", "value": disparity,
                 "reference_group": str(reference), "group_rates": {str(k): float(v) for k, v in rates.items()}},
                {"metric": f"disparate_impact_ratio_{attribute}", "value": ratio,
                 "reference_group": str(reference), "group_rates": {str(k): float(v) for k, v in rates.items()}},
            ])
            if ground_truth is not None and len(ground_truth) == len(synthetic_inputs):
                labels = [
                    ground_truth[int(output["input_id"].rsplit("_", 1)[-1])]
                    for output in model_outputs
                    if self._extract_prediction(output.get("output")) is not None
                ]
                if len(labels) == len(rows):
                    df["ground_truth"] = [
                        float(label) >= favorable_threshold for label in labels
                    ]
                    tpr_by_group = {}
                    fpr_by_group = {}
                    for group, group_df in df.groupby(attribute, dropna=False):
                        positives = group_df[group_df["ground_truth"]]
                        negatives = group_df[~group_df["ground_truth"]]
                        tpr_by_group[str(group)] = (
                            float(positives["favorable_prediction"].mean())
                            if len(positives) else None
                        )
                        fpr_by_group[str(group)] = (
                            float(negatives["favorable_prediction"].mean())
                            if len(negatives) else None
                        )
                    valid_tprs = [value for value in tpr_by_group.values() if value is not None]
                    valid_fprs = [value for value in fpr_by_group.values() if value is not None]
                    if len(valid_tprs) >= 2 and len(valid_fprs) >= 2:
                        metrics.append({
                            "metric": f"equal_opportunity_difference_{attribute}",
                            "value": max(valid_tprs) - min(valid_tprs),
                            "group_true_positive_rates": tpr_by_group,
                        })
                        metrics.append({
                            "metric": f"equalized_odds_difference_{attribute}",
                            "value": max(
                                max(valid_tprs) - min(valid_tprs),
                                max(valid_fprs) - min(valid_fprs),
                            ),
                            "group_true_positive_rates": tpr_by_group,
                            "group_false_positive_rates": fpr_by_group,
                        })
            for group, row in grouped.iterrows():
                parity.append({
                    "attribute": attribute,
                    "group": str(group),
                    "name": f"{attribute}: {group}",
                    "value": float(row["mean"]),
                    "count": int(row["count"]),
                })

        feature_influence = self._calculate_feature_influence(df)
        return {
            "overall_bias_score": min(1.0, max(disparities, default=0.0)),
            "fairness_metrics": metrics,
            "feature_influence": feature_influence,
            "demographic_parity": parity,
            "explainability_insights": {
                "method": "group_rate_and_correlation",
                "supported": False,
                "top_features": feature_influence[:10],
                "note": "These are statistical associations, not SHAP/LIME causal explanations.",
            },
            "prediction_summary": {
                "successful_predictions": len(rows),
                "input_count": len(synthetic_inputs),
                "excluded_predictions": len(model_outputs) - len(rows),
                "favorable_threshold": favorable_threshold,
                "ground_truth_available": ground_truth is not None,
            },
        }

    @classmethod
    def _extract_prediction(cls, value: Any) -> Optional[float]:
        if isinstance(value, bool):
            return float(value)
        if isinstance(value, (int, float)) and math.isfinite(float(value)):
            return float(value)
        if isinstance(value, dict):
            for key in ("prediction", "result", "score", "value", "output"):
                if key in value:
                    result = cls._extract_prediction(value[key])
                    if result is not None:
                        return result
        if isinstance(value, list) and len(value) == 1:
            return cls._extract_prediction(value[0])
        return None

    @staticmethod
    def _calculate_feature_influence(df: pd.DataFrame) -> List[Dict[str, Any]]:
        result = []
        for column in df.select_dtypes(include=[np.number]).columns:
            if column == "prediction":
                continue
            correlation = df[column].corr(df["prediction"])
            if pd.notna(correlation):
                result.append({
                    "feature": column,
                    "influence": abs(float(correlation)),
                    "importance": abs(float(correlation)),
                })
        return sorted(result, key=lambda item: item["influence"], reverse=True)
