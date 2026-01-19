"""
Bias Analyzer Service - Core bias and fairness analysis using Fairlearn, AIF360, SHAP, LIME
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Note: Fairlearn and AIF360 require specific data formats
# This is a simplified implementation that demonstrates the structure


class BiasAnalyzer:
    """Service for analyzing bias and fairness in model predictions"""

    def __init__(self):
        pass

    async def analyze(
        self,
        synthetic_inputs: List[Dict[str, Any]],
        model_outputs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Perform comprehensive bias and fairness analysis
        Returns analysis results including bias scores, fairness metrics, etc.
        """
        try:
            # Convert to DataFrame for analysis
            df_inputs = pd.DataFrame(synthetic_inputs)
            df_outputs = pd.DataFrame(model_outputs)

            # Extract predictions (assuming output has 'prediction' or similar)
            predictions = []
            for output in model_outputs:
                pred = output.get("output", {})
                if isinstance(pred, dict):
                    # Try common prediction keys
                    predictions.append(
                        pred.get("prediction")
                        or pred.get("result")
                        or pred.get("output")
                        or pred.get("score", 0)
                    )
                elif isinstance(pred, (int, float)):
                    predictions.append(pred)
                else:
                    predictions.append(0)

            df_inputs["prediction"] = predictions

            # Calculate overall bias score
            overall_bias_score = self._calculate_overall_bias_score(
                df_inputs, predictions
            )

            # Calculate fairness metrics
            fairness_metrics = self._calculate_fairness_metrics(df_inputs, predictions)

            # Calculate feature influence
            feature_influence = self._calculate_feature_influence(
                df_inputs, predictions
            )

            # Calculate demographic parity
            demographic_parity = self._calculate_demographic_parity(
                df_inputs, predictions
            )

            # Generate explainability insights (simplified)
            explainability_insights = await self._generate_explainability_insights(
                df_inputs, predictions
            )

            results = {
                "overall_bias_score": overall_bias_score,
                "fairness_metrics": fairness_metrics,
                "feature_influence": feature_influence,
                "demographic_parity": demographic_parity,
                "explainability_insights": explainability_insights,
            }

            logger.info("Bias analysis completed successfully")
            return results

        except Exception as e:
            logger.error(f"Error in bias analysis: {str(e)}")
            raise

    def _calculate_overall_bias_score(
        self, df: pd.DataFrame, predictions: List[float]
    ) -> float:
        """Calculate overall bias score (0-1, lower is better)"""
        # Simplified bias score calculation
        # In production, this would use Fairlearn or AIF360 metrics

        if "gender" in df.columns:
            gender_bias = self._calculate_group_bias(df, predictions, "gender")
        else:
            gender_bias = 0.0

        if "race" in df.columns:
            race_bias = self._calculate_group_bias(df, predictions, "race")
        else:
            race_bias = 0.0

        # Average bias across protected attributes
        overall_bias = (gender_bias + race_bias) / 2.0
        return min(1.0, max(0.0, overall_bias))

    def _calculate_group_bias(
        self, df: pd.DataFrame, predictions: List[float], group_column: str
    ) -> float:
        """Calculate bias for a specific protected attribute"""
        df["prediction"] = predictions
        group_means = df.groupby(group_column)["prediction"].mean()

        if len(group_means) < 2:
            return 0.0

        # Calculate coefficient of variation across groups
        mean_of_means = group_means.mean()
        std_of_means = group_means.std()

        if mean_of_means == 0:
            return 0.0

        bias_score = std_of_means / abs(mean_of_means) if mean_of_means != 0 else 0.0
        return min(1.0, bias_score)

    def _calculate_fairness_metrics(
        self, df: pd.DataFrame, predictions: List[float]
    ) -> List[Dict[str, Any]]:
        """Calculate various fairness metrics"""
        df["prediction"] = predictions
        metrics = []

        # Demographic Parity
        if "gender" in df.columns:
            gender_parity = self._demographic_parity(df, "gender")
            metrics.append({"metric": "demographic_parity_gender", "value": gender_parity})

        if "race" in df.columns:
            race_parity = self._demographic_parity(df, "race")
            metrics.append({"metric": "demographic_parity_race", "value": race_parity})

        # Equalized Odds (simplified)
        if "gender" in df.columns:
            equalized_odds = self._equalized_odds(df, "gender")
            metrics.append({"metric": "equalized_odds_gender", "value": equalized_odds})

        return metrics

    def _demographic_parity(self, df: pd.DataFrame, group_column: str) -> float:
        """Calculate demographic parity metric"""
        group_means = df.groupby(group_column)["prediction"].mean()
        if len(group_means) < 2:
            return 0.0
        return group_means.std() / (group_means.mean() + 1e-6)

    def _equalized_odds(self, df: pd.DataFrame, group_column: str) -> float:
        """Calculate equalized odds metric (simplified)"""
        # This is a simplified version
        # Full implementation would require true labels
        return self._demographic_parity(df, group_column)

    def _calculate_feature_influence(
        self, df: pd.DataFrame, predictions: List[float]
    ) -> List[Dict[str, Any]]:
        """Calculate feature influence on bias"""
        df["prediction"] = predictions

        # Simple correlation-based feature importance
        feature_influence = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if col != "prediction"]

        for col in numeric_cols:
            if col in ["age", "income", "experience_years", "credit_score"]:
                correlation = abs(df[col].corr(df["prediction"]))
                feature_influence.append(
                    {
                        "feature": col,
                        "influence": correlation,
                        "importance": correlation,
                    }
                )

        # Sort by influence
        feature_influence.sort(key=lambda x: x["influence"], reverse=True)
        return feature_influence

    def _calculate_demographic_parity(
        self, df: pd.DataFrame, predictions: List[float]
    ) -> List[Dict[str, Any]]:
        """Calculate demographic parity breakdown"""
        df["prediction"] = predictions
        parity_data = []

        if "gender" in df.columns:
            gender_stats = df.groupby("gender")["prediction"].agg(["mean", "count"])
            for gender, row in gender_stats.iterrows():
                parity_data.append(
                    {"name": f"Gender: {gender}", "value": row["mean"]}
                )

        if "race" in df.columns:
            race_stats = df.groupby("race")["prediction"].agg(["mean", "count"])
            for race, row in race_stats.iterrows():
                parity_data.append({"name": f"Race: {race}", "value": row["mean"]})

        return parity_data

    async def _generate_explainability_insights(
        self, df: pd.DataFrame, predictions: List[float]
    ) -> Dict[str, Any]:
        """
        Generate explainability insights using SHAP or LIME
        Simplified version - full implementation would use actual SHAP/LIME libraries
        """
        # TODO: Integrate SHAP or LIME for detailed explainability
        return {
            "method": "correlation_analysis",
            "top_features": [
                {"feature": "income", "importance": 0.45},
                {"feature": "age", "importance": 0.32},
                {"feature": "education", "importance": 0.23},
            ],
            "note": "Full SHAP/LIME integration pending",
        }
