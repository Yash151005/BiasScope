# Bias and Fairness Concepts

Educational guide to understanding bias and fairness in AI systems.

## What is Bias?

Bias in AI refers to systematic errors or unfairness in model predictions that disadvantage certain groups or individuals.

### Types of Bias

1. **Data Bias**: Training data doesn't represent reality
2. **Algorithmic Bias**: Model learns biased patterns
3. **Measurement Bias**: Metrics don't capture fairness
4. **Representation Bias**: Underrepresentation of groups
5. **Historical Bias**: Past discrimination encoded in data

## What is Fairness?

Fairness means treating individuals and groups equitably, without discrimination based on protected attributes.

### Protected Attributes

Common protected attributes include:
- Gender
- Race/Ethnicity
- Age
- Religion
- Disability
- Sexual orientation

## Fairness Metrics

### Demographic Parity

Also called statistical parity. Requires equal positive outcome rates across groups.

**Formula**: P(Ŷ=1|A=a) = P(Ŷ=1|A=b) for all groups a, b

**Use Case**: When equal acceptance rates are desired

### Equalized Odds

Requires equal true positive and false positive rates across groups.

**Formula**: 
- P(Ŷ=1|Y=1, A=a) = P(Ŷ=1|Y=1, A=b)
- P(Ŷ=1|Y=0, A=a) = P(Ŷ=1|Y=0, A=b)

**Use Case**: When both errors matter equally

### Equal Opportunity

Requires equal true positive rates across groups.

**Formula**: P(Ŷ=1|Y=1, A=a) = P(Ŷ=1|Y=1, A=b)

**Use Case**: When false negatives are critical

### Calibration

Predictions should be equally accurate across groups.

**Use Case**: When probability estimates matter

## Common Bias Scenarios

### Hiring Bias
- Model favors certain demographics
- Unequal interview rates
- Salary disparities

### Lending Bias
- Credit decisions vary by race/gender
- Loan approval disparities
- Interest rate differences

### Healthcare Bias
- Treatment recommendations vary
- Diagnostic accuracy differences
- Resource allocation disparities

### Criminal Justice Bias
- Sentencing recommendations
- Recidivism predictions
- Risk assessment disparities

## Mitigation Strategies

### Pre-processing
- Remove biased features
- Balance training data
- Augment underrepresented groups

### In-processing
- Fairness constraints during training
- Adversarial debiasing
- Fair representation learning

### Post-processing
- Adjust decision thresholds
- Calibrate predictions
- Apply fairness constraints

## Legal and Ethical Considerations

### Regulations
- **EU AI Act**: Requirements for high-risk AI
- **GDPR**: Right to explanation
- **US Fair Lending**: Equal credit opportunity
- **EEOC**: Employment discrimination laws

### Ethical Principles
- Transparency
- Accountability
- Non-discrimination
- Human oversight

## Best Practices

1. **Diverse Data**: Ensure representative training data
2. **Regular Testing**: Periodic bias audits
3. **Multiple Metrics**: Don't rely on single metric
4. **Documentation**: Record decisions and rationale
5. **Stakeholder Input**: Include affected communities
6. **Continuous Monitoring**: Track performance over time

## Tools and Frameworks

### Fairlearn
- Fairness assessment
- Mitigation algorithms
- Microsoft's open-source toolkit

### AIF360
- Comprehensive fairness metrics
- Bias detection
- IBM's toolkit

### SHAP
- Model explainability
- Feature importance
- Shapley values

### LIME
- Local interpretability
- Feature explanations
- Model-agnostic

## Further Reading

- Fairlearn Documentation: https://fairlearn.org/
- AIF360 Documentation: https://aif360.mybluemix.net/
- SHAP Documentation: https://shap.readthedocs.io/
- "Fairness and Machine Learning" by Barocas et al.
- "The Ethical Algorithm" by Kearns and Roth

## Glossary

- **Protected Attribute**: Characteristic protected by law (race, gender, etc.)
- **Disparate Impact**: Unintended discrimination
- **Disparate Treatment**: Intentional discrimination
- **Confusion Matrix**: Table of prediction vs. actual
- **ROC Curve**: Receiver Operating Characteristic
- **AUC**: Area Under Curve
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
