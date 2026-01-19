# Getting Started with BiasScope

Welcome to BiasScope! This guide will help you get started with analyzing AI models for bias and fairness.

## What is BiasScope?

BiasScope is an automated tool that evaluates AI models for bias and fairness. Simply provide your model's API endpoint, and BiasScope will:

- Generate synthetic test data automatically
- Send requests to your model
- Analyze responses for bias and fairness
- Generate comprehensive visual reports

## Prerequisites

- An AI model with a REST API endpoint
- The model should accept JSON input and return JSON output
- Basic understanding of bias and fairness concepts (optional)

## Quick Start

### Step 1: Access BiasScope

1. Open the BiasScope frontend in your browser (typically `http://localhost:3000`)
2. You'll see the home page with an overview of features

### Step 2: Start an Analysis

1. Click "Start Analysis" or navigate to "New Analysis"
2. Enter your AI model's API URL (e.g., `https://your-model-api.com/predict`)
3. Click "Start Analysis"

### Step 3: Monitor Progress

- The system will show real-time progress
- You can see:
  - Data generation progress
  - Model API requests
  - Bias analysis progress
  - Report generation

### Step 4: View Results

Once analysis completes:

1. View interactive visualizations
2. Review bias scores and fairness metrics
3. Download PDF report
4. Analyze feature influence on bias

## Understanding Your Model API

Your model API should:

- Accept POST requests
- Accept JSON payload with features (e.g., `{age: 30, gender: "male", ...}`)
- Return JSON response with prediction/output

Example request:
```json
POST https://your-model-api.com/predict
Content-Type: application/json

{
  "age": 30,
  "gender": "male",
  "race": "white",
  "education": "bachelor",
  "income": 50000,
  "experience_years": 5
}
```

Example response:
```json
{
  "prediction": 0.75,
  "result": "approved"
}
```

## Next Steps

- Read [User Interface Guide](./user-interface.md) for detailed UI walkthrough
- Learn about [Interpreting Results](./interpreting-results.md)
- Understand [Bias and Fairness Concepts](./bias-fairness-concepts.md)

## Getting Help

If you encounter issues:

1. Check that your model API is accessible
2. Verify the API accepts the expected input format
3. Review error messages in the UI
4. Check backend logs for detailed error information
