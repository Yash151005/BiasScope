# BiasScope Database Schema

Complete MongoDB database schema documentation.

**Designed by: Tejas** - Schema design and data consistency lead

## Database: `biasscope`

## Collection: `analyses`

Main collection storing all analysis records.

### Document Structure

```javascript
{
  // Identification
  "_id": ObjectId,
  "analysis_id": String (unique, UUID),
  
  // Model Information
  "model_url": String (URL),
  
  // Status Tracking
  "status": String, // "started", "in_progress", "completed", "failed"
  "progress": Number, // 0-100
  
  // Timestamps
  "created_at": DateTime (UTC),
  "updated_at": DateTime (UTC),
  "completed_at": DateTime (UTC, optional),
  
  // Test Data
  "synthetic_inputs": [
    {
      "input_id": String,
      "features": {
        "age": Number,
        "gender": String,
        "race": String,
        "education": String,
        "income": Number,
        "experience_years": Number,
        "location": String,
        "credit_score": Number,
        // ... other features
      },
      "timestamp": DateTime (UTC)
    }
  ],
  
  "model_outputs": [
    {
      "input_id": String,
      "output": Any, // Model prediction/output
      "timestamp": DateTime (UTC)
    }
  ],
  
  // Analysis Results
  "bias_scores": [
    {
      "metric_name": String,
      "value": Number,
      "threshold": Number (optional),
      "passed": Boolean
    }
  ],
  
  "results": {
    "overall_bias_score": Number (0-1),
    "fairness_metrics": [
      {
        "metric": String,
        "value": Number,
        "group": String (optional)
      }
    ],
    "feature_influence": [
      {
        "feature": String,
        "influence": Number,
        "importance": Number
      }
    ],
    "demographic_parity": [
      {
        "name": String,
        "value": Number
      }
    ],
    "explainability_insights": {
      "method": String,
      "top_features": [
        {
          "feature": String,
          "importance": Number
        }
      ],
      "note": String (optional)
    }
  },
  
  // Report Metadata
  "report_generated": Boolean,
  "report_path": String (optional),
  
  // Error Handling
  "error_message": String (optional)
}
```

## Indexes

### Primary Indexes

```javascript
// Unique index on analysis_id
db.analyses.createIndex(
  { "analysis_id": 1 },
  { unique: true }
)

// Status index for filtering
db.analyses.createIndex(
  { "status": 1 }
)

// Created at index for sorting
db.analyses.createIndex(
  { "created_at": -1 }
)

// Model URL index for searching
db.analyses.createIndex(
  { "model_url": 1 }
)
```

### Compound Indexes

```javascript
// Status and created_at for common queries
db.analyses.createIndex(
  { "status": 1, "created_at": -1 }
)
```

## Data Types

### Status Values

- `started`: Analysis just initiated
- `in_progress`: Analysis is currently running
- `completed`: Analysis finished successfully
- `failed`: Analysis encountered an error

### Feature Types

**Numeric Features**:
- `age`: Integer (18-80)
- `income`: Float (positive)
- `experience_years`: Integer (0-40)
- `credit_score`: Integer (300-850)

**Categorical Features**:
- `gender`: String ("male", "female", "other")
- `race`: String ("white", "black", "asian", "hispanic", "other")
- `education`: String ("high_school", "bachelor", "master", "phd")
- `location`: String (city name)

### Bias Score Range

- `overall_bias_score`: Float (0.0 - 1.0)
  - 0.0 = No bias
  - 1.0 = Maximum bias

## Relationships

### Input-Output Linking

Inputs and outputs are linked by `input_id`:
- Each `synthetic_inputs` entry has an `input_id`
- Corresponding `model_outputs` entry has matching `input_id`
- Format: `"input_{index}"` (e.g., "input_0", "input_1")

## Data Consistency Rules

1. **Timestamps**: All timestamps stored in UTC
2. **Analysis ID**: Must be unique UUID
3. **Progress**: Must be between 0 and 100
4. **Status Transitions**: 
   - `started` → `in_progress` → `completed` or `failed`
   - Cannot go backwards
5. **Results**: Only present when `status` is `completed`
6. **Error Message**: Only present when `status` is `failed`
7. **Report Path**: Only present when `report_generated` is `true`

## Query Examples

### Find Analysis by ID

```javascript
db.analyses.findOne({ "analysis_id": "550e8400-e29b-41d4-a716-446655440000" })
```

### Find All Completed Analyses

```javascript
db.analyses.find({ "status": "completed" })
```

### Find Recent Analyses

```javascript
db.analyses.find()
  .sort({ "created_at": -1 })
  .limit(10)
```

### Find Analyses by Model URL

```javascript
db.analyses.find({ "model_url": "https://example.com/predict" })
```

### Find In-Progress Analyses

```javascript
db.analyses.find({ "status": "in_progress" })
```

### Update Analysis Progress

```javascript
db.analyses.updateOne(
  { "analysis_id": "550e8400-e29b-41d4-a716-446655440000" },
  {
    "$set": {
      "progress": 50,
      "updated_at": new Date()
    }
  }
)
```

### Get Analysis Counts by Status

```javascript
db.analyses.aggregate([
  {
    $group: {
      _id: "$status",
      count: { $sum: 1 }
    }
  }
])
```

## Initialization Script

Run `database/init_indexes.js` to create indexes:

```bash
mongo biasscope database/init_indexes.js
```

## Backup and Restore

### Backup

```bash
mongodump --db=biasscope --out=./backup
```

### Restore

```bash
mongorestore --db=biasscope ./backup/biasscope
```

## Performance Considerations

1. **Indexes**: Ensure indexes are created for common queries
2. **Pagination**: Use `skip()` and `limit()` for large result sets
3. **Projection**: Use projection to limit returned fields
4. **Aggregation**: Use aggregation pipeline for complex queries

## Migration Notes

When updating the schema:

1. **Additive Changes**: New optional fields can be added safely
2. **Breaking Changes**: Update application code before deploying
3. **Data Migration**: Write migration scripts for data transformations
4. **Index Updates**: Update indexes when query patterns change

## Security Considerations

1. **Input Validation**: Validate all inputs before storing
2. **Sanitization**: Sanitize user-provided URLs
3. **Access Control**: Implement proper access control in application
4. **Encryption**: Consider encrypting sensitive data at rest
5. **Audit Logging**: Log all database operations for audit
