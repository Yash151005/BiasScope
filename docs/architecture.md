# BiasScope System Architecture

Complete technical architecture documentation for BiasScope.

## Overview

BiasScope follows a clean, modular architecture with clear separation of concerns:

```
┌─────────────┐
│  Frontend   │  React + Tailwind CSS
│  (Port 3000)│
└──────┬──────┘
       │ HTTP/REST
       │
┌──────▼──────┐
│   Backend   │  FastAPI
│  (Port 8000)│
└──────┬──────┘
       │
   ┌───┴───┬──────────┬──────────┐
   │       │          │          │
┌──▼──┐ ┌──▼──┐  ┌────▼────┐ ┌──▼──┐
│Mongo│ │Redis│  │ Reports │ │Model│
│  DB │ │(Opt)│  │  Folder │ │ API │
└─────┘ └─────┘  └─────────┘ └─────┘
```

## Components

### Frontend (`frontend/`)

**Technology**: React 18, Tailwind CSS, Vite

**Responsibilities**:
- User interface and interactions
- API communication
- Data visualization
- Progress tracking

**Key Files**:
- `src/App.jsx` - Main application component
- `src/pages/` - Page components
- `src/components/` - Reusable UI components

**Team**: Rushikesh (lead), Sandip (styling), Tejas (data components)

### Backend (`backend/`)

**Technology**: FastAPI, Python 3.9+

**Responsibilities**:
- API endpoints
- Business logic
- Data processing
- Report generation

**Key Modules**:
- `main.py` - FastAPI application
- `app/services/` - Core business logic
- `app/database/` - Database operations

**Services**:
1. **AnalysisService**: Orchestrates analysis workflow
2. **DataGenerator**: Generates synthetic test data
3. **ModelClient**: Communicates with user's model API
4. **BiasAnalyzer**: Performs bias and fairness analysis
5. **ReportGenerator**: Creates visual and PDF reports

### Database (`database/`)

**Technology**: MongoDB

**Responsibilities**:
- Persistent storage
- Analysis records
- Test data storage
- Results storage

**Schema Design**: Tejas (lead)

**Collections**:
- `analyses` - Main analysis records

### Reports (`reports/`)

**Technology**: Matplotlib, Plotly, ReportLab

**Responsibilities**:
- PDF report generation
- Interactive HTML reports
- Visualizations

**Formats**:
- PDF (ReportLab)
- HTML (Plotly)

## Data Flow

### Analysis Workflow

1. **User Input**: User provides model API URL via frontend
2. **API Request**: Frontend sends POST to `/api/analysis/start`
3. **Analysis Creation**: Backend creates analysis record in MongoDB
4. **Background Task**: Analysis runs asynchronously
5. **Data Generation**: Synthetic data generated (Faker/CTGAN)
6. **Model Requests**: Backend sends requests to user's model API
7. **Bias Analysis**: Results analyzed using Fairlearn/AIF360
8. **Report Generation**: Visual and PDF reports created
9. **Storage**: Results stored in MongoDB
10. **Frontend Polling**: Frontend polls for results
11. **Display**: Results displayed with visualizations

## API Endpoints

### POST `/api/analysis/start`
Start new analysis

**Request**:
```json
{
  "model_url": "https://example.com/predict"
}
```

**Response**:
```json
{
  "analysis_id": "uuid",
  "status": "started",
  "message": "Analysis started successfully"
}
```

### GET `/api/analysis/{analysis_id}`
Get analysis results

**Response**:
```json
{
  "analysis_id": "uuid",
  "status": "completed",
  "progress": 100,
  "results": {
    "overall_bias_score": 0.45,
    "fairness_metrics": [...],
    "feature_influence": [...],
    "demographic_parity": [...]
  }
}
```

### GET `/api/analysis/{analysis_id}/report`
Download PDF report

**Response**: PDF file

## Technology Stack Details

### Frontend Stack
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Recharts**: Data visualization
- **Axios**: HTTP client
- **Lucide React**: Icons

### Backend Stack
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Motor**: Async MongoDB driver
- **Pydantic**: Data validation
- **Faker**: Synthetic data generation
- **Fairlearn**: Fairness assessment
- **AIF360**: AI Fairness toolkit
- **SHAP/LIME**: Explainability
- **Matplotlib/Plotly**: Visualization
- **ReportLab**: PDF generation

### Database Stack
- **MongoDB**: NoSQL database
- **Motor**: Async Python driver

## Security Considerations

1. **Input Validation**: All inputs validated with Pydantic
2. **CORS**: Configured for frontend origins only
3. **Error Handling**: Comprehensive error handling
4. **Rate Limiting**: Can be added for production
5. **Authentication**: Can be added for multi-user scenarios

## Scalability

### Current Design
- Single server deployment
- Background tasks for long-running operations
- MongoDB for persistence

### Future Enhancements
- Celery for distributed task processing
- Redis for caching and task queue
- Horizontal scaling with load balancer
- CDN for static assets

## Deployment

### Development
```bash
# Frontend
cd frontend && npm run dev

# Backend
cd backend && uvicorn main:app --reload
```

### Production
- Frontend: Build static files, serve with Nginx
- Backend: Deploy with Gunicorn/Uvicorn
- MongoDB: Managed service or dedicated server
- Reports: File system or object storage

## Monitoring

- Application logs via Python logging
- MongoDB query performance
- API response times
- Error tracking (can integrate Sentry)

## Future Improvements

1. User authentication and authorization
2. Multi-user support
3. Scheduled analyses
4. Comparison between analyses
5. Export to various formats
6. Integration with CI/CD pipelines
7. Advanced visualization options
8. Real-time WebSocket updates
