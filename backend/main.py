"""
BiasScope Backend - FastAPI Application
Main entry point for the bias analysis API
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydantic import field_validator
from typing import Optional, Dict, Any
import uuid
from datetime import datetime
from urllib.parse import urlparse

from app.services.analysis_service import AnalysisService
from app.database.mongodb import get_database
from app.utils.logger import setup_logger

logger = setup_logger(__name__)
app = FastAPI(title="BiasScope API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    model_url: str

    @field_validator("model_url")
    @classmethod
    def normalize_model_url(cls, v: str) -> str:
        """
        Accept http/https URLs and also scheme-less inputs like:
        - localhost:5000/predict
        - 127.0.0.1:8000/predict
        - example.com/predict

        If scheme is missing, default to http://
        """
        if v is None:
            raise ValueError("model_url is required")

        v = v.strip()
        if not v:
            raise ValueError("model_url is required")

        parsed = urlparse(v)
        if not parsed.scheme:
            v = f"http://{v}"
            parsed = urlparse(v)

        if parsed.scheme not in ("http", "https"):
            raise ValueError("model_url must start with http:// or https:// (or omit the scheme)")

        if not parsed.netloc:
            raise ValueError("model_url must include a host (e.g., localhost:5000)")

        return v


class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    message: str


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    await get_database()
    logger.info("BiasScope API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("BiasScope API shutting down")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "BiasScope API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/api/analysis/start", response_model=AnalysisResponse)
async def start_analysis(
    request: AnalysisRequest, background_tasks: BackgroundTasks
):
    """
    Start a new bias analysis for the provided AI model API
    """
    try:
        analysis_id = str(uuid.uuid4())
        analysis_service = AnalysisService()

        # Store initial analysis record
        await analysis_service.create_analysis(
            analysis_id=analysis_id,
            model_url=str(request.model_url),
        )

        # Start analysis in background
        background_tasks.add_task(
            analysis_service.run_analysis,
            analysis_id=analysis_id,
            model_url=str(request.model_url),
        )

        logger.info(f"Started analysis {analysis_id} for model {request.model_url}")

        return AnalysisResponse(
            analysis_id=analysis_id,
            status="started",
            message="Analysis started successfully",
        )
    except Exception as e:
        logger.error(f"Error starting analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")


@app.get("/api/analysis/{analysis_id}")
async def get_analysis_results(analysis_id: str):
    """
    Get analysis results by analysis ID
    """
    try:
        analysis_service = AnalysisService()
        results = await analysis_service.get_analysis(analysis_id)

        if not results:
            raise HTTPException(status_code=404, detail="Analysis not found")

        return results
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching analysis {analysis_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch analysis: {str(e)}")


@app.get("/api/analysis/{analysis_id}/report")
async def download_report(analysis_id: str):
    """
    Download analysis report as PDF
    """
    try:
        analysis_service = AnalysisService()
        report_path = await analysis_service.generate_report(analysis_id)

        if not report_path:
            raise HTTPException(status_code=404, detail="Report not found or not ready")

        return FileResponse(
            report_path,
            media_type="application/pdf",
            filename=f"biasscope-report-{analysis_id}.pdf",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report for {analysis_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")


@app.get("/api/analyses")
async def list_analyses(limit: int = 10, skip: int = 0):
    """
    List all analyses with pagination
    """
    try:
        analysis_service = AnalysisService()
        analyses = await analysis_service.list_analyses(limit=limit, skip=skip)
        return {"analyses": analyses, "limit": limit, "skip": skip}
    except Exception as e:
        logger.error(f"Error listing analyses: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list analyses: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
