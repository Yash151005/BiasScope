# Interpreting BiasScope Results

Guide to understanding bias analysis results and metrics.

## Overall Bias Score

**Range**: 0.0 to 1.0

- **0.0 - 0.3**: Low bias (Green zone)
- **0.3 - 0.7**: Moderate bias (Yellow zone)
- **0.7 - 1.0**: High bias (Red zone)

**Interpretation**: Lower scores indicate less bias. A score of 0 means no detected bias, while 1 indicates maximum bias.

## Fairness Metrics

### Demographic Parity

Measures whether different demographic groups receive similar positive outcomes.

**Good**: Values close to 0 (minimal difference between groups)
**Concerning**: Large differences between groups

### Equalized Odds

Measures whether true positive and false positive rates are similar across groups.

**Good**: Similar rates across all groups
**Concerning**: Significant disparities

### Other Metrics

- **Disparate Impact**: Ratio of positive outcomes between groups
- **Statistical Parity**: Equal probability of positive outcomes
- **Equal Opportunity**: Equal true positive rates

## Feature Influence

Shows which input features most contribute to bias in predictions.

**High Influence**: Feature significantly affects bias
**Low Influence**: Feature has minimal impact on bias

**Action**: Focus on reducing bias from high-influence features.

## Demographic Parity Breakdown

Visual breakdown showing how predictions vary across:

- **Gender**: Male, Female, Other
- **Race**: White, Black, Asian, Hispanic, Other
- **Other Protected Attributes**: Age groups, education levels, etc.

**Interpretation**: 
- Similar values across groups = good
- Large differences = potential bias

## Explainability Insights

Provides understanding of:

- **Feature Importance**: Which features matter most
- **SHAP Values**: Feature contribution to predictions
- **LIME Explanations**: Local interpretability

## Reading the Charts

### Bar Charts
- Height represents metric value
- Compare heights across metrics
- Look for outliers

### Pie Charts
- Slice size represents proportion
- Compare slice sizes across groups
- Look for uneven distributions

### Feature Influence Chart
- Longer bars = higher influence
- Focus on top features
- Consider feature engineering

## Actionable Insights

### If Bias Score is High (>0.7)

1. **Review Feature Influence**: Identify problematic features
2. **Check Demographic Parity**: See which groups are affected
3. **Examine Model Logic**: Review decision-making process
4. **Consider Mitigation**: Apply bias mitigation techniques

### If Bias Score is Moderate (0.3-0.7)

1. **Monitor Closely**: Track over time
2. **Improve Data**: Ensure diverse training data
3. **Fine-tune Model**: Adjust model parameters
4. **Document Findings**: Keep records for compliance

### If Bias Score is Low (<0.3)

1. **Maintain Standards**: Continue current practices
2. **Regular Testing**: Periodic bias checks
3. **Document Success**: Record fair practices

## Common Patterns

### Gender Bias
- Different outcomes for male vs. female
- Often seen in hiring, lending, healthcare

### Racial Bias
- Disparities across racial groups
- Common in criminal justice, credit scoring

### Age Bias
- Discrimination against older/younger individuals
- Seen in employment, insurance

## Best Practices

1. **Regular Analysis**: Test models periodically
2. **Multiple Metrics**: Don't rely on single metric
3. **Context Matters**: Consider domain-specific factors
4. **Document Everything**: Keep records of analyses
5. **Continuous Improvement**: Iterate based on findings

## Further Reading

- [Bias and Fairness Concepts](./bias-fairness-concepts.md)
- [Best Practices](./best-practices.md)
- Fairlearn Documentation
- AIF360 Documentation
