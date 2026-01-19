# BiasScope Backend

Python-based FastAPI backend for BiasScope AI Bias & Fairness Analysis tool.

## Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - Database for storing analysis data
- **Faker** - Synthetic data generation
- **Fairlearn** - Fairness assessment library
- **AIF360** - AI Fairness 360 toolkit
- **SHAP/LIME** - Model explainability
- **Matplotlib/Plotly** - Data visualization
- **ReportLab** - PDF report generation

## Features

- RESTful API for bias analysis workflows
- Automated synthetic data generation
- Model API integration
- Comprehensive bias and fairness analysis
- Visual and PDF report generation
- Background task processing

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB (running locally or remote)
- pip or poetry

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Start MongoDB (if running locally):
```bash
# On Windows with MongoDB installed
mongod
```

### Running the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI) available at `http://localhost:8000/docs`

## API Endpoints

- `POST /api/analysis/start` - Start a new bias analysis
- `GET /api/analysis/{analysis_id}` - Get analysis results
- `GET /api/analysis/{analysis_id}/report` - Download analysis report
- `GET /api/analyses` - List all analyses

## Project Structure

```
backend/
├── app/
│   ├── database/          # MongoDB schemas and connection
│   ├── services/          # Core business logic
│   │   ├── analysis_service.py
│   │   ├── data_generator.py
│   │   ├── model_client.py
│   │   ├── bias_analyzer.py
│   │   └── report_generator.py
│   ├── utils/             # Utility functions
│   └── config.py          # Configuration settings
├── main.py                # FastAPI application entry point
├── requirements.txt       # Python dependencies
└── README.md
```

## Database Schema

The MongoDB database stores:
- Analysis metadata (ID, status, progress)
- Synthetic input data
- Model outputs
- Bias scores and fairness metrics
- Report metadata

Designed by **Tejas** - Schema design and data consistency lead.
