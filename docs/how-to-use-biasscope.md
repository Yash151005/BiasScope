# How to Use BiasScope

Step-by-step guide to using BiasScope for AI bias analysis.

## Prerequisites

1. **AI Model with API**: Your model must have a REST API endpoint
2. **API Accessibility**: The endpoint must be publicly accessible or accessible from BiasScope server
3. **JSON Format**: API should accept JSON input and return JSON output

## Step-by-Step Guide

### Step 1: Prepare Your Model API

Ensure your model API:

- Accepts POST requests
- Accepts JSON payload with features
- Returns JSON response

**Example API Endpoint**:
```
POST https://your-model-api.com/predict
Content-Type: application/json

{
  "age": 30,
  "gender": "male",
  "race": "white",
  "education": "bachelor",
  "income": 50000,
  "experience_years": 5,
  "credit_score": 720
}
```

**Expected Response**:
```json
{
  "prediction": 0.85,
  "result": "approved",
  "confidence": 0.92
}
```

### Step 2: Start Analysis

1. Open BiasScope frontend (typically `http://localhost:3000`)
2. Click "Start Analysis" or navigate to "New Analysis"
3. Enter your model API URL
4. Click "Start Analysis" button

### Step 3: Monitor Progress

The system will show:

- **Progress Bar**: Percentage complete (0-100%)
- **Status Updates**: Current stage of analysis
- **Estimated Time**: Approximate completion time

**Stages**:
1. Data Generation (0-20%)
2. Model API Requests (20-60%)
3. Bias Analysis (60-80%)
4. Report Generation (80-100%)

### Step 4: Review Results

Once analysis completes, you'll see:

#### Overall Bias Score
- Single metric summarizing bias
- Color-coded (green/yellow/red)
- Quick assessment indicator

#### Fairness Metrics
- Multiple fairness measurements
- Bar chart visualization
- Detailed breakdowns

#### Feature Influence
- Which features affect bias most
- Horizontal bar chart
- Prioritized list

#### Demographic Parity
- Breakdown by protected attributes
- Pie chart visualization
- Group comparisons

### Step 5: Download Report

1. Click "Download Report" button
2. PDF report will download
3. Report includes:
   - All metrics and scores
   - Tables and summaries
   - Visualizations
   - Recommendations

## Understanding Results

### Low Bias Score (<0.3)
✅ **Good**: Model shows minimal bias
- Continue current practices
- Regular monitoring recommended

### Moderate Bias Score (0.3-0.7)
⚠️ **Caution**: Some bias detected
- Review feature influence
- Check demographic parity
- Consider mitigation strategies

### High Bias Score (>0.7)
❌ **Critical**: Significant bias detected
- Immediate review required
- Identify problematic features
- Implement mitigation measures

## Tips for Best Results

### 1. Ensure API Reliability
- Stable endpoint
- Reasonable response times
- Error handling

### 2. Provide Complete Features
- Include all relevant features
- Consistent data types
- Valid value ranges

### 3. Understand Your Model
- Know what features it uses
- Understand prediction format
- Be aware of model limitations

### 4. Interpret in Context
- Consider domain-specific factors
- Review multiple metrics
- Don't rely on single score

## Common Issues and Solutions

### Issue: Analysis Fails to Start
**Solutions**:
- Verify API URL is correct
- Check API is accessible
- Ensure API accepts POST requests
- Check API returns valid JSON

### Issue: Analysis Stuck at Data Generation
**Solutions**:
- Check backend logs
- Verify data generator is working
- Check MongoDB connection

### Issue: Model API Errors
**Solutions**:
- Verify API endpoint
- Check API authentication
- Ensure correct input format
- Review API error messages

### Issue: Results Seem Incorrect
**Solutions**:
- Verify model is working correctly
- Check input data format
- Review model predictions
- Compare with manual testing

## Advanced Usage

### Multiple Analyses
- Run analyses periodically
- Compare results over time
- Track improvements

### Different Models
- Test model variants
- Compare bias levels
- Identify best model

### Feature Analysis
- Focus on high-influence features
- Test feature removal
- Analyze feature interactions

## Integration

### CI/CD Pipeline
- Add BiasScope to testing pipeline
- Automated bias checks
- Fail builds on high bias

### Monitoring
- Regular scheduled analyses
- Alert on bias increases
- Track trends over time

## Best Practices

1. **Regular Testing**: Test models periodically
2. **Document Results**: Keep records of analyses
3. **Compare Over Time**: Track bias trends
4. **Multiple Metrics**: Review all metrics, not just overall score
5. **Context Matters**: Consider domain-specific factors
6. **Action on Findings**: Implement mitigation when needed
7. **Stakeholder Communication**: Share results with team

## Getting Help

If you need assistance:

1. Check documentation
2. Review error messages
3. Check backend logs
4. Verify API connectivity
5. Test with simple examples

## Next Steps

After using BiasScope:

1. Review results carefully
2. Identify areas for improvement
3. Implement mitigation strategies
4. Re-test after changes
5. Document findings and actions
