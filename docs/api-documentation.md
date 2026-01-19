# BiasScope API Documentation

Complete API reference for BiasScope backend.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. For production, implement authentication as needed.

## Endpoints

### Health Check

#### GET `/`

Check if API is running.

**Response**:
```json
{
  "message": "BiasScope API is running",
  "version": "1.0.0"
}
```

#### GET `/health`

Detailed health check.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-19T12:00:00"
}
```

### Analysis Endpoints

#### POST `/api/analysis/start`

Start a new bias analysis.

**Request Body**:
```json
{
  "model_url": "https://your-model-api.com/predict"
}
```

**Response** (200 OK):
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "message": "Analysis started successfully"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid request body
- `500 Internal Server Error`: Failed to start analysis

#### GET `/api/analysis/{analysis_id}`

Get analysis results by ID.

**Path Parameters**:
- `analysis_id` (string): UUID of the analysis

**Response** (200 OK):
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "model_url": "https://your-model-api.com/predict",
  "status": "completed",
  "progress": 100,
  "created_at": "2024-01-19T12:00:00",
  "updated_at": "2024-01-19T12:05:00",
  "completed_at": "2024-01-19T12:05:00",
  "results": {
    "overall_bias_score": 0.45,
    "fairness_metrics": [
      {
        "metric": "demographic_parity_gender",
        "value": 0.12
      },
      {
        "metric": "demographic_parity_race",
        "value": 0.18
      }
    ],
    "feature_influence": [
      {
        "feature": "income",
        "influence": 0.45,
        "importance": 0.45
      },
      {
        "feature": "age",
        "influence": 0.32,
        "importance": 0.32
      }
    ],
    "demographic_parity": [
      {
        "name": "Gender: male",
        "value": 0.65
      },
      {
        "name": "Gender: female",
        "value": 0.58
      }
    ],
    "explainability_insights": {
      "method": "correlation_analysis",
      "top_features": [
        {
          "feature": "income",
          "importance": 0.45
        }
      ]
    }
  },
  "report_generated": true,
  "report_path": "../reports/550e8400-e29b-41d4-a716-446655440000_report.pdf"
}
```

**Status Values**:
- `started`: Analysis just started
- `in_progress`: Analysis is running
- `completed`: Analysis finished successfully
- `failed`: Analysis encountered an error

**Error Responses**:
- `404 Not Found`: Analysis not found
- `500 Internal Server Error`: Failed to fetch analysis

#### GET `/api/analysis/{analysis_id}/report`

Download analysis report as PDF.

**Path Parameters**:
- `analysis_id` (string): UUID of the analysis

**Response** (200 OK):
- Content-Type: `application/pdf`
- File download with filename: `biasscope-report-{analysis_id}.pdf`

**Error Responses**:
- `404 Not Found`: Report not found or not ready
- `500 Internal Server Error`: Failed to generate report

#### GET `/api/analyses`

List all analyses with pagination.

**Query Parameters**:
- `limit` (integer, optional): Number of results per page (default: 10)
- `skip` (integer, optional): Number of results to skip (default: 0)

**Response** (200 OK):
```json
{
  "analyses": [
    {
      "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
      "model_url": "https://your-model-api.com/predict",
      "status": "completed",
      "progress": 100,
      "created_at": "2024-01-19T12:00:00"
    }
  ],
  "limit": 10,
  "skip": 0
}
```

## Data Models

### AnalysisRequest

```json
{
  "model_url": "string (URL)"
}
```

### AnalysisResponse

```json
{
  "analysis_id": "string (UUID)",
  "status": "string",
  "message": "string"
}
```

### AnalysisResults

```json
{
  "overall_bias_score": "number (0-1)",
  "fairness_metrics": [
    {
      "metric": "string",
      "value": "number"
    }
  ],
  "feature_influence": [
    {
      "feature": "string",
      "influence": "number",
      "importance": "number"
    }
  ],
  "demographic_parity": [
    {
      "name": "string",
      "value": "number"
    }
  ],
  "explainability_insights": {
    "method": "string",
    "top_features": [
      {
        "feature": "string",
        "importance": "number"
      }
    ]
  }
}
```

## Model API Requirements

Your model API should:

1. **Accept POST requests** to the provided URL
2. **Accept JSON payload** with features:
```json
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

3. **Return JSON response** with prediction:
```json
{
  "prediction": 0.85,
  "result": "approved"
}
```

Or any JSON format - BiasScope will extract the prediction value.

## Error Handling

All endpoints return standard HTTP status codes:

- `200 OK`: Success
- `400 Bad Request`: Invalid request
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error responses include a `detail` field:
```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider adding rate limiting.

## CORS

CORS is configured to allow requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

For production, update CORS settings in `backend/main.py`.

## Interactive API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Examples

### cURL Examples

**Start Analysis**:
```bash
curl -X POST "http://localhost:8000/api/analysis/start" \
  -H "Content-Type: application/json" \
  -d '{"model_url": "https://your-model-api.com/predict"}'
```

**Get Results**:
```bash
curl "http://localhost:8000/api/analysis/{analysis_id}"
```

**Download Report**:
```bash
curl "http://localhost:8000/api/analysis/{analysis_id}/report" \
  --output report.pdf
```

### Python Examples

```python
import requests

# Start analysis
response = requests.post(
    "http://localhost:8000/api/analysis/start",
    json={"model_url": "https://your-model-api.com/predict"}
)
analysis_id = response.json()["analysis_id"]

# Get results
results = requests.get(
    f"http://localhost:8000/api/analysis/{analysis_id}"
).json()

# Download report
report = requests.get(
    f"http://localhost:8000/api/analysis/{analysis_id}/report"
)
with open("report.pdf", "wb") as f:
    f.write(report.content)
```

### JavaScript Examples

```javascript
// Start analysis
const response = await fetch('http://localhost:8000/api/analysis/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model_url: 'https://your-model-api.com/predict'
  })
});
const { analysis_id } = await response.json();

// Get results
const results = await fetch(
  `http://localhost:8000/api/analysis/${analysis_id}`
).then(r => r.json());

// Download report
const report = await fetch(
  `http://localhost:8000/api/analysis/${analysis_id}/report`
).then(r => r.blob());
```
