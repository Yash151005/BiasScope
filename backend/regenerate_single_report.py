import asyncio
from app.services.analysis_service import AnalysisService

async def regenerate_single_report(analysis_id):
    service = AnalysisService()
    print(f"Regenerating report for analysis: {analysis_id}")
    path = await service.generate_report(analysis_id)
    if path:
        print(f"Report generated: {path}")
    else:
        print("Failed to generate report.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python regenerate_single_report.py <analysis_id>")
        exit(1)
    asyncio.run(regenerate_single_report(sys.argv[1]))
