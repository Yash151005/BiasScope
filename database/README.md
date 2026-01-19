# BiasScope Database

MongoDB database management for BiasScope AI Bias & Fairness Analysis tool.

## Database Design

**Lead: Tejas** - Schema design and data consistency

## Collections

### `analyses`

Main collection storing analysis records with the following schema:

```javascript
{
  analysis_id: String (unique),
  model_url: String,
  status: String, // "started", "in_progress", "completed", "failed"
  progress: Number (0-100),
  created_at: DateTime,
  updated_at: DateTime,
  completed_at: DateTime (optional),
  
  // Test data
  synthetic_inputs: Array<SyntheticInput>,
  model_outputs: Array<ModelOutput>,
  
  // Results
  bias_scores: Array<BiasScore>,
  results: AnalysisResults (optional),
  
  // Report metadata
  report_generated: Boolean,
  report_path: String (optional),
  
  // Error handling
  error_message: String (optional)
}
```

### Data Models

#### SyntheticInput
```javascript
{
  input_id: String,
  features: Object, // {age, gender, race, education, income, ...}
  timestamp: DateTime
}
```

#### ModelOutput
```javascript
{
  input_id: String,
  output: Any, // Model prediction/output
  timestamp: DateTime
}
```

#### BiasScore
```javascript
{
  metric_name: String,
  value: Number,
  threshold: Number (optional),
  passed: Boolean
}
```

#### AnalysisResults
```javascript
{
  overall_bias_score: Number,
  fairness_metrics: Array<FairnessMetric>,
  feature_influence: Array<FeatureInfluence>,
  demographic_parity: Array<DemographicParity>,
  explainability_insights: Object (optional)
}
```

## Setup

1. Install MongoDB: https://www.mongodb.com/try/download/community

2. Start MongoDB:
```bash
mongod
```

3. Create database (automatically created on first write):
```javascript
use biasscope
```

## Indexes

Recommended indexes for performance:

```javascript
// Analysis ID index (unique)
db.analyses.createIndex({ "analysis_id": 1 }, { unique: true })

// Status index for filtering
db.analyses.createIndex({ "status": 1 })

// Created at index for sorting
db.analyses.createIndex({ "created_at": -1 })
```

## Connection

The backend connects to MongoDB using the connection string specified in `backend/.env`:

```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=biasscope
```

## Data Consistency

- All timestamps stored in UTC
- Analysis IDs are UUIDs (unique)
- Input-output pairs linked by `input_id`
- Results validated before storage
- Atomic updates for progress tracking
