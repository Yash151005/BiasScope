# BiasScope Reports

Directory for storing generated analysis reports.

## Report Types

### PDF Reports
- Generated using ReportLab
- Contains comprehensive analysis results
- Includes tables, metrics, and summaries
- Format: `{analysis_id}_report.pdf`

### Interactive HTML Reports
- Generated using Plotly
- Interactive visualizations
- Charts and graphs for bias metrics
- Format: `{analysis_id}_interactive.html`

## Report Contents

1. **Overall Bias Score** - Summary metric (0-1 scale)
2. **Fairness Metrics** - Detailed fairness measurements
3. **Feature Influence** - Impact of features on bias
4. **Demographic Parity** - Breakdown by protected attributes
5. **Explainability Insights** - SHAP/LIME explanations

Reports are automatically generated when an analysis completes and can be downloaded via the API or frontend.
