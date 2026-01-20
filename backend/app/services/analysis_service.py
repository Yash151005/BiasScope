"""
Analysis Service - Core logic for bias and fairness analysis
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from app.database.mongodb import get_database
from app.database.schemas import AnalysisDocument
from app.services.data_generator import DataGenerator
from app.services.model_client import ModelClient
from app.services.bias_analyzer import BiasAnalyzer
from app.services.report_generator import ReportGenerator
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class AnalysisService:
    """Service for managing bias analysis workflows"""

    def __init__(self):
        self.data_generator = DataGenerator()
        self.model_client = ModelClient()
        self.bias_analyzer = BiasAnalyzer()
        self.report_generator = ReportGenerator()

    async def create_analysis(
        self, analysis_id: str, model_url: str
    ) -> None:
        """Create a new analysis record in the database"""
        db = await get_database()
        analysis_doc = {
            "analysis_id": analysis_id,
            "model_url": model_url,
            "status": "started",
            "progress": 0.0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "synthetic_inputs": [],
            "model_outputs": [],
            "bias_scores": [],
            "report_generated": False,
        }
        await db.analyses.insert_one(analysis_doc)
        logger.info(f"Created analysis record: {analysis_id}")

    async def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get analysis by ID"""
        db = await get_database()
        analysis = await db.analyses.find_one({"analysis_id": analysis_id})
        if analysis:
            analysis["_id"] = str(analysis["_id"])
        return analysis

    async def update_analysis(
        self, analysis_id: str, updates: Dict[str, Any]
    ) -> None:
        """Update analysis record"""
        db = await get_database()
        updates["updated_at"] = datetime.utcnow()
        await db.analyses.update_one(
            {"analysis_id": analysis_id}, {"$set": updates}
        )

    async def list_analyses(
        self, limit: int = 10, skip: int = 0
    ) -> List[Dict[str, Any]]:
        """List all analyses with pagination"""
        db = await get_database()
        cursor = db.analyses.find().sort("created_at", -1).skip(skip).limit(limit)
        analyses = await cursor.to_list(length=limit)
        for analysis in analyses:
            analysis["_id"] = str(analysis["_id"])
        return analyses

    async def run_analysis(self, analysis_id: str, model_url: str) -> None:
        """
        Run the complete bias analysis workflow
        """
        try:
            logger.info(f"Starting analysis workflow for {analysis_id}")

            # Step 1: Generate synthetic data (20% progress)
            await self.update_analysis(analysis_id, {"status": "in_progress", "progress": 10})
            logger.info(f"[{analysis_id}] Generating synthetic data...")
            synthetic_data = await self.data_generator.generate_data()
            await self.update_analysis(
                analysis_id,
                {
                    "synthetic_inputs": [
                        {
                            "input_id": f"input_{i}",
                            "features": data,
                            "timestamp": datetime.utcnow(),
                        }
                        for i, data in enumerate(synthetic_data)
                    ],
                    "progress": 20,
                },
            )

            # Step 2: Send requests to model API (40% progress)
            logger.info(f"[{analysis_id}] Sending requests to model API...")
            model_outputs = []
            total_inputs = len(synthetic_data)
            attempts = 0
            failures = 0
            for i, input_data in enumerate(synthetic_data):
                attempts += 1
                try:
                    output = await self.model_client.predict(model_url, input_data)
                    model_outputs.append(
                        {
                            "input_id": f"input_{i}",
                            "output": output,
                            "timestamp": datetime.utcnow(),
                        }
                    )
                except Exception as e:
                    failures += 1
                    logger.warning(f"[{analysis_id}] Failed to get prediction for input {i}: {str(e)}")
                finally:
                    # Always advance progress based on attempts, not successes,
                    # so users don't feel "stuck" when an endpoint rejects requests.
                    progress = 20 + int((i + 1) / total_inputs * 40)
                    await self.update_analysis(analysis_id, {"progress": progress})

                # Fail fast if the endpoint is clearly not a usable prediction API.
                # Example: a website returning 403/HTML, auth wall, etc.
                if attempts >= 10 and len(model_outputs) == 0 and failures == attempts:
                    raise RuntimeError(
                        "Model endpoint rejected all requests (0 successful predictions). "
                        "Please provide a valid prediction API endpoint (POST JSON → JSON)."
                    )

            await self.update_analysis(
                analysis_id, {"model_outputs": model_outputs, "progress": 60}
            )

            # Step 3: Run bias analysis (80% progress)
            logger.info(f"[{analysis_id}] Running bias analysis...")
            await self.update_analysis(analysis_id, {"progress": 65})
            bias_results = await self.bias_analyzer.analyze(
                synthetic_data, model_outputs
            )
            await self.update_analysis(
                analysis_id,
                {
                    "bias_scores": [
                        {
                            "metric_name": metric["metric"],
                            "value": metric["value"],
                            "passed": metric.get("passed", True),
                        }
                        for metric in bias_results.get("fairness_metrics", [])
                    ],
                    "results": bias_results,
                    "progress": 80,
                },
            )

            # Step 4: Generate report (100% progress)
            logger.info(f"[{analysis_id}] Generating report...")
            await self.update_analysis(analysis_id, {"progress": 90})
            report_path = await self.report_generator.generate_report(
                analysis_id, bias_results
            )
            await self.update_analysis(
                analysis_id,
                {
                    "status": "completed",
                    "progress": 100,
                    "completed_at": datetime.utcnow(),
                    "report_generated": True,
                    "report_path": report_path,
                },
            )

            logger.info(f"Analysis {analysis_id} completed successfully")

        except Exception as e:
            logger.error(f"Error in analysis workflow for {analysis_id}: {str(e)}")
            await self.update_analysis(
                analysis_id,
                {
                    "status": "failed",
                    "error_message": str(e),
                },
            )

    async def generate_report(self, analysis_id: str) -> Optional[str]:
        """Generate and return report path"""
        try:
            analysis = await self.get_analysis(analysis_id)
            if not analysis:
                logger.warning(f"Analysis not found: {analysis_id}")
                return None

            if analysis.get("report_generated") and analysis.get("report_path"):
                logger.info(f"Report already generated for {analysis_id}")
                return analysis["report_path"]

            if analysis.get("status") == "completed" and analysis.get("results"):
                logger.info(f"Generating new report for {analysis_id}")
                try:
                    report_path = await self.report_generator.generate_report(
                        analysis_id, analysis["results"]
                    )
                    await self.update_analysis(
                        analysis_id,
                        {
                            "report_generated": True,
                            "report_path": report_path,
                        },
                    )
                    logger.info(f"Report generated successfully: {report_path}")
                    return report_path
                except Exception as e:
                    logger.error(f"Error generating report: {str(e)}")
                    import traceback
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    raise

            logger.warning(f"Analysis not in completed state or missing results: {analysis_id}")
            return None
        except Exception as e:
            logger.error(f"Error in generate_report for {analysis_id}: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
